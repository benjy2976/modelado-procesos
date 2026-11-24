"""Vocabulario de temas de búsqueda y sugerencias léxicas con procedencia.

Un tema es una pista de recuperación: no declara equivalencia jurídica ni clasifica una norma.
Las sugerencias se guardan en la caché, son regenerables y no se presentan como conocimiento validado.
"""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from .fuentes_busqueda import _conectar, expresion
from .fuentes_extraccion import BASE
from .fuentes_preparacion import _sha256
from .repositorio import ErrorDominio, RepositorioProcesos

VOCABULARIO = Path("05-herramientas/gestor-modelos/catalogo/temas-busqueda.json")
SUGERENCIAS = BASE / "temas-sugeridos.jsonl"
VERSION = "temas-lexico-v1"
IDENTIFICADOR = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ESTADOS = {"BORRADOR-IA", "PROPUESTA", "REVISADO-EQUIPO"}
CAMPOS_PROHIBIDOS = {"equivalentes", "sinonimos_juridicos", "validado"}


def _normalizar(texto: str) -> str:
    sin_tildes = "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))
    return " ".join(re.findall(r"\w+", sin_tildes.casefold()))


def cargar_vocabulario(raiz: Path) -> dict:
    ruta = raiz / VOCABULARIO
    if not ruta.is_file():
        raise ErrorDominio("Falta el vocabulario de temas de búsqueda")
    return json.loads(ruta.read_text(encoding="utf-8"))


def _hallazgos_vocabulario(raiz: Path, vocabulario: dict) -> list[dict]:
    hallazgos = []

    def agregar(codigo: str, detalle: str, severidad: str = "ERROR") -> None:
        hallazgos.append({"codigo": codigo, "severidad": severidad, "detalle": detalle})

    if vocabulario.get("esquema") != "temas-busqueda-v1":
        agregar("ESQUEMA", "Se esperaba temas-busqueda-v1")
    if vocabulario.get("estado") not in ESTADOS:
        agregar("ESTADO", f"Estado no admitido: {vocabulario.get('estado')}; la herramienta no acepta VALIDADO")
    temas = vocabulario.get("temas") or []
    identificadores = [t.get("id", "") for t in temas]
    for repetido in [i for i, n in Counter(identificadores).items() if n > 1]:
        agregar("ID-REPETIDO", repetido)
    usos: Counter[str] = Counter()
    repositorio = RepositorioProcesos(raiz)
    for tema in temas:
        nombre = tema.get("id", "")
        if not IDENTIFICADOR.fullmatch(nombre):
            agregar("ID-INVALIDO", nombre)
        if not str(tema.get("etiqueta", "")).strip():
            agregar("ETIQUETA-VACIA", nombre)
        for campo in CAMPOS_PROHIBIDOS & set(tema):
            agregar("EQUIVALENCIA-NO-PERMITIDA", f"{nombre}: el campo '{campo}' no forma parte del vocabulario")
        terminos = tema.get("terminos") or []
        if not terminos or not all(isinstance(t, str) and _normalizar(t) for t in terminos):
            agregar("TERMINOS", f"{nombre}: lista vacía o términos sin palabras")
        usos.update({_normalizar(t) for t in terminos if isinstance(t, str)})
        for relacionado in tema.get("relacionados") or []:
            if relacionado == nombre or relacionado not in identificadores:
                agregar("RELACION-INVALIDA", f"{nombre} -> {relacionado}")
        for codigo in tema.get("procesos") or []:
            try:
                repositorio.carpeta(codigo)
            except ErrorDominio:
                agregar("PROCESO-INEXISTENTE", f"{nombre}: {codigo}")
    for termino in [t for t, n in usos.items() if n > 1]:
        agregar("TERMINO-COMPARTIDO", termino, "ADVERTENCIA")
    return hallazgos


def comprobar(raiz: Path) -> dict:
    """Verifica el esquema del vocabulario y la procedencia de las sugerencias registradas."""
    raiz = raiz.resolve()
    vocabulario = cargar_vocabulario(raiz)
    hallazgos = _hallazgos_vocabulario(raiz, vocabulario)
    temas = {t.get("id") for t in vocabulario.get("temas") or []}
    sugerencias = 0
    ruta = raiz / SUGERENCIAS
    if ruta.is_file():
        for numero, linea in enumerate(ruta.read_text(encoding="utf-8").splitlines(), 1):
            dato = json.loads(linea)
            sugerencias += 1
            procedencia = dato.get("procedencia") or {}
            if dato.get("tema") not in temas:
                hallazgos.append({"codigo": "SUGERENCIA-TEMA", "severidad": "ERROR", "detalle": f"línea {numero}"})
            if not all(procedencia.get(k) for k in ("metodo", "version", "fecha", "sha256_vocabulario")):
                hallazgos.append(
                    {"codigo": "SUGERENCIA-PROCEDENCIA", "severidad": "ERROR", "detalle": f"línea {numero}"}
                )
    errores = sum(h["severidad"] == "ERROR" for h in hallazgos)
    return {"temas": len(temas), "sugerencias": sugerencias, "errores": errores, "hallazgos": hallazgos}


def terminos_de(raiz: Path, tema: str, con_relacionados: bool = False) -> tuple[list[str], list[str]]:
    """Términos de búsqueda de un tema y, si se pide, de sus relacionados (que no son equivalentes)."""
    temas = {t["id"]: t for t in cargar_vocabulario(raiz.resolve())["temas"]}
    if tema not in temas:
        raise ErrorDominio(f"Tema inexistente: {tema}", 404)
    usados = [tema] + (temas[tema].get("relacionados") or [] if con_relacionados else [])
    return [termino for t in usados for termino in temas[t]["terminos"]], usados


def sugerir(raiz: Path, proceso: str | None = None) -> dict:
    """Asigna temas candidatos a fragmentos por coincidencia de términos; no interpreta su contenido."""
    raiz = raiz.resolve()
    vocabulario = cargar_vocabulario(raiz)
    if any(h["severidad"] == "ERROR" for h in _hallazgos_vocabulario(raiz, vocabulario)):
        raise ErrorDominio("El vocabulario tiene errores; ejecute 'fuentes temas comprobar'")
    temas = [
        t for t in vocabulario["temas"] if not proceso or any(c.startswith(proceso) for c in t.get("procesos") or [])
    ]
    procedencia = {
        "metodo": "coincidencia-lexica",
        "version": VERSION,
        "fecha": datetime.now(UTC).isoformat(timespec="seconds"),
        "sha256_vocabulario": _sha256(raiz / VOCABULARIO),
    }
    registros = []
    base, desactualizado = _conectar(raiz)
    with closing(base):
        for tema in temas:
            filas = base.execute(
                "SELECT f.id, f.ruta, f.titulo, f.encabezados, f.texto "
                "FROM fts JOIN fragmentos f ON f.rowid = fts.rowid WHERE fts MATCH ?",
                (expresion("", terminos=tema["terminos"]),),
            ).fetchall()
            for fila in filas:
                cuerpo = f" {_normalizar(fila['texto'])} "
                cabecera = f" {_normalizar((fila['titulo'] or '') + ' ' + (fila['encabezados'] or ''))} "
                hallados = [t for t in tema["terminos"] if f" {_normalizar(t)} " in cuerpo + cabecera]
                veces = sum(cuerpo.count(f" {_normalizar(t)} ") for t in hallados)
                en_cabecera = any(f" {_normalizar(t)} " in cabecera for t in hallados)
                registros.append(
                    {
                        "fragmento": fila["id"],
                        "ruta": fila["ruta"],
                        "tema": tema["id"],
                        "terminos": hallados,
                        "confianza": "MEDIA" if en_cabecera or veces >= 2 else "BAJA",
                        "procedencia": procedencia,
                    }
                )
    destino = raiz / SUGERENCIAS
    temporal = destino.with_suffix(".tmp")
    temporal.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in registros), encoding="utf-8")
    temporal.replace(destino)
    return {
        "proceso": proceso,
        "temas": len(temas),
        "sugerencias": len(registros),
        "fragmentos": len({r["fragmento"] for r in registros}),
        "documentos": len({r["ruta"] for r in registros}),
        "por_tema": dict(Counter(r["tema"] for r in registros)),
        "por_confianza": dict(Counter(r["confianza"] for r in registros)),
        "indice_desactualizado": desactualizado,
        "archivo": SUGERENCIAS.as_posix(),
    }
