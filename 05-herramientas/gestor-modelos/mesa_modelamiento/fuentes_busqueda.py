"""Índice léxico local (SQLite FTS5) y consultas acotadas sobre los fragmentos de la biblioteca.

El índice es regenerable desde la segmentación y nunca sustituye al original: cada resultado lleva
documento, hash, ubicación, método de extracción y estado de cotejo.
"""

from __future__ import annotations

import json
import re
import sqlite3
from contextlib import closing
from pathlib import Path

from .fuentes_extraccion import BASE
from .fuentes_fragmentos import MANIFIESTO_SEGMENTOS, cargar_fragmentos
from .fuentes_preparacion import _sha256
from .repositorio import ErrorDominio

INDICE_DB = BASE / "indice-fuentes.sqlite"
COLUMNAS = (
    "id, orden, doc_id, ruta, sha256, tipo, area, articulo, numeral, titulo, encabezados, ubicacion, "
    "estructura, metodos, estado_texto, clave_repetida, texto"
)
LIMITE_MAXIMO = 50


def indexar(raiz: Path) -> dict:
    """Reconstruye el índice completo en un archivo temporal y lo reemplaza al terminar."""
    raiz = raiz.resolve()
    manifiesto = raiz / MANIFIESTO_SEGMENTOS
    if not manifiesto.is_file():
        raise ErrorDominio("Falta la segmentación; ejecute 'fuentes segmentar' primero")
    destino = raiz / INDICE_DB
    temporal = destino.with_suffix(".tmp")
    temporal.unlink(missing_ok=True)
    with closing(sqlite3.connect(temporal)) as base:
        base.executescript(
            f"""
            CREATE TABLE fragmentos (rowid INTEGER PRIMARY KEY, {COLUMNAS.replace(", ", " TEXT, ")} TEXT);
            CREATE UNIQUE INDEX fragmento_id ON fragmentos(id);
            CREATE INDEX vecindad ON fragmentos(sha256, orden);
            CREATE VIRTUAL TABLE fts USING fts5(texto, titulo, encabezados, content='fragmentos',
                content_rowid='rowid', tokenize='unicode61 remove_diacritics 2');
            CREATE TABLE meta (clave TEXT PRIMARY KEY, valor TEXT);
            """
        )
        total = 0
        for orden, f in cargar_fragmentos(raiz):
            documento = f["documento"]
            fila = (
                f["id"], orden, documento["id"], documento["ruta"], documento["sha256"], documento["tipo"],
                Path(documento["ruta"]).parts[1], f.get("articulo"), f.get("numeral"), f.get("titulo"),
                " > ".join(f.get("encabezados") or []), json.dumps(f["ubicacion"], ensure_ascii=False),
                f["estructura"], ",".join(f["metodos"]), f["estado_texto"], int(bool(f.get("clave_repetida"))),
                f["texto"],
            )  # fmt: skip
            base.execute(f"INSERT INTO fragmentos ({COLUMNAS}) VALUES ({', '.join('?' * len(fila))})", fila)
            total += 1
        base.execute("INSERT INTO fts(fts) VALUES ('rebuild')")
        base.execute("INSERT INTO meta VALUES ('sha256_segmentacion', ?)", (_sha256(manifiesto),))
        base.commit()
    temporal.replace(destino)
    return {"indice": INDICE_DB.as_posix(), "fragmentos": total}


def _conectar(raiz: Path) -> tuple[sqlite3.Connection, bool]:
    ruta = raiz.resolve() / INDICE_DB
    if not ruta.is_file():
        raise ErrorDominio("Falta el índice; ejecute 'fuentes indexar' primero")
    base = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
    base.row_factory = sqlite3.Row
    registrado = base.execute("SELECT valor FROM meta WHERE clave='sha256_segmentacion'").fetchone()[0]
    manifiesto = raiz.resolve() / MANIFIESTO_SEGMENTOS
    return base, not manifiesto.is_file() or _sha256(manifiesto) != registrado


# Palabras sin contenido que en modo flexible no se exigen; en los demás modos se respetan.
VACIAS = set(
    "a al ante bajo con contra de del desde durante el en entre hacia hasta la las lo los mediante o para por "
    "que se segun sin sobre su sus tras u un una unos unas y".split()
)
MODOS = ("todas", "alguna", "frase", "flexible")


def _palabra_flexible(palabra: str) -> str:
    """Raíz por prefijo para tolerar flexión («sustenta» -> «susten*» halla «sustente»)."""
    if len(palabra) < 6 or palabra.isdigit():
        return f'"{palabra}"'
    return f'"{palabra[: max(5, len(palabra) - 2)]}"*'


def expresion(consulta: str, modo: str = "todas", terminos: list[str] | None = None) -> str:
    """Traduce la consulta a FTS5 citando cada palabra; nunca pasa operadores escritos por el usuario.

    Los términos de un tema se unen entre sí con OR y restringen la consulta con AND. ``flexible``
    omite palabras vacías y busca por raíz; ``flexible-alguna`` es su versión relajada con OR.
    """
    palabras = re.findall(r"\w+", consulta)
    partes = []
    if modo.startswith("flexible"):
        utiles = [p for p in palabras if p.casefold() not in VACIAS] or palabras
        union = " OR " if modo == "flexible-alguna" else " AND "
        if utiles:
            partes.append("(" + union.join(_palabra_flexible(p) for p in utiles) + ")")
    elif palabras and modo == "frase":
        partes.append('"' + " ".join(palabras) + '"')
    elif palabras:
        partes.append("(" + (" OR " if modo == "alguna" else " AND ").join(f'"{p}"' for p in palabras) + ")")
    frases = [" ".join(re.findall(r"\w+", termino)) for termino in terminos or []]
    citadas = [f'"{frase}"' for frase in frases if frase]
    if citadas:
        partes.append("(" + " OR ".join(citadas) + ")")
    return " AND ".join(partes)


def _resultado(fila: sqlite3.Row, extracto: str | None = None) -> dict:
    salida = {
        "id": fila["id"],
        "documento": {"id": fila["doc_id"], "ruta": fila["ruta"], "sha256": fila["sha256"], "tipo": fila["tipo"]},
        "ubicacion": json.loads(fila["ubicacion"]),
        "estructura": fila["estructura"],
        "articulo": fila["articulo"],
        "numeral": fila["numeral"],
        "titulo": fila["titulo"],
        "encabezados": fila["encabezados"],
        "metodos": fila["metodos"].split(",") if fila["metodos"] else [],
        "estado_texto": fila["estado_texto"],
        "clave_repetida": bool(int(fila["clave_repetida"])),
    }
    if extracto is not None:
        salida["extracto"] = extracto
    return salida


def buscar(raiz: Path, consulta: str, *, modo: str = "todas", terminos: list[str] | None = None,
           filtros: dict | None = None, limite: int = 8, max_caracteres: int = 6000) -> dict:  # fmt: skip
    """Pasajes candidatos con ubicación verificable, limitados en cantidad y en caracteres."""
    filtros = {k: v for k, v in (filtros or {}).items() if v}
    limite = max(1, min(limite, LIMITE_MAXIMO))
    fts = expresion(consulta, modo, terminos)
    if not fts and not filtros:
        raise ErrorDominio("Indique una consulta, un tema o al menos un filtro")
    condiciones, valores = [], []
    for campo, columna in (("id_documento", "doc_id"), ("tipo", "tipo"), ("area", "area"), ("articulo", "articulo")):
        if campo in filtros:
            condiciones.append(f"f.{columna} = ?")
            valores.append(filtros[campo])
    if "archivo" in filtros:
        condiciones.append("f.ruta LIKE ?")
        valores.append(f"%{filtros['archivo']}%")
    base, desactualizado = _conectar(raiz)
    with closing(base):
        total, filas = _consultar(base, fts, condiciones, valores, limite)
        relajada = ""
        if modo == "flexible" and len(filas) < limite and len(re.findall(r"\w+", consulta)) > 1:
            # Con todas las raíces hay pocos pasajes: se completan con coincidencias parciales, marcadas.
            relajada = expresion(consulta, "flexible-alguna", terminos)
            vistos = {f["id"] for f in filas}
            extra = _consultar(base, relajada, condiciones, valores, limite)[1]
            filas += [dict(f) | {"relajado": True} for f in extra if f["id"] not in vistos][: limite - len(filas)]
    resultados, usados = [], 0
    for fila in filas:
        if resultados and usados + len(fila["extracto"]) > max_caracteres:
            break
        usados += len(fila["extracto"])
        resultados.append(_resultado(fila, fila["extracto"]) | ({"relajado": True} if _relajado(fila) else {}))
    return {
        "consulta": consulta,
        "expresion_fts": fts,
        "expresion_relajada": relajada,
        "filtros": filtros,
        "coincidencias": total,
        "devueltos": len(resultados),
        "truncado": len(resultados) < min(total, limite),
        "indice_desactualizado": desactualizado,
        "resultados": resultados,
    }


def _relajado(fila) -> bool:
    return isinstance(fila, dict) and bool(fila.get("relajado"))


def _consultar(base: sqlite3.Connection, fts: str, condiciones: list[str], valores: list, limite: int):
    condiciones, valores = list(condiciones), list(valores)
    if fts:
        desde = "fts JOIN fragmentos f ON f.rowid = fts.rowid"
        condiciones.insert(0, "fts MATCH ?")
        valores.insert(0, fts)
        extracto, orden = "snippet(fts, -1, '«', '»', ' … ', 48)", "bm25(fts, 1.0, 1.0, 0.5)"
    else:
        desde, extracto, orden = "fragmentos f", "substr(f.texto, 1, 400)", "f.sha256, f.orden"
    donde = " AND ".join(condiciones)
    try:
        total = base.execute(f"SELECT count(*) FROM {desde} WHERE {donde}", valores).fetchone()[0]
        filas = base.execute(
            f"SELECT f.*, {extracto} AS extracto FROM {desde} WHERE {donde} ORDER BY {orden} LIMIT ?",
            [*valores, limite],
        ).fetchall()
    except sqlite3.OperationalError as exc:
        raise ErrorDominio(f"Consulta no válida: {exc}") from exc
    return total, filas


def contexto(raiz: Path, identificador: str, vecinos: int = 1, max_caracteres: int = 8000) -> dict:
    """Texto completo del fragmento y de sus vecinos del mismo documento, dentro de un presupuesto."""
    base, desactualizado = _conectar(raiz)
    with closing(base):
        central = base.execute("SELECT * FROM fragmentos WHERE id = ?", (identificador,)).fetchone()
        if central is None:
            raise ErrorDominio("Fragmento inexistente en el índice", 404)
        orden = int(central["orden"])
        filas = base.execute(
            "SELECT * FROM fragmentos WHERE sha256 = ? AND CAST(orden AS INTEGER) BETWEEN ? AND ? "
            "ORDER BY CAST(orden AS INTEGER)",
            (central["sha256"], orden - max(0, vecinos), orden + max(0, vecinos)),
        ).fetchall()
    usados = len(central["texto"])
    salida = []
    for fila in sorted(filas, key=lambda f: abs(int(f["orden"]) - orden)):
        es_central = fila["id"] == identificador
        if not es_central and usados + len(fila["texto"]) > max_caracteres:
            continue
        usados += 0 if es_central else len(fila["texto"])
        salida.append({**_resultado(fila), "texto": fila["texto"], "central": es_central, "orden": int(fila["orden"])})
    salida.sort(key=lambda f: f["orden"])
    return {"fragmento": identificador, "indice_desactualizado": desactualizado, "caracteres": usados,
            "fragmentos": salida}  # fmt: skip
