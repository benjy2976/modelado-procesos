"""Inventario de elementos de un modelo y registro auditable de afirmaciones contra fuentes.

El registro es una bitácora de eventos inmutables por afirmación. La herramienta verifica identificadores,
citas e idempotencia; el resultado (sustentada, inferencia, contradicción...) es una propuesta del autor
del registro y nunca una validación normativa.
"""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from .fuentes_busqueda import _conectar
from .fuentes_preparacion import _guardar, _sha256
from .repositorio import ErrorDominio, RepositorioProcesos

AUDITORIAS = Path("05-herramientas/gestor-modelos/auditorias")
ASPECTOS = {"actor", "accion", "condicion", "plazo", "documento", "entrada-salida", "decision", "excepcion",
            "secuencia", "existencia"}  # fmt: skip
RESULTADOS = {"SUSTENTADA", "INFERENCIA", "CONTRADICCION", "EVIDENCIA-INSUFICIENTE", "NO-APLICA"}
CLASES = {"EXIGENCIA-NORMATIVA", "EVIDENCIA-OBSERVADA", "DECISION-PROYECTO", "PROPUESTA"}
REQUIERE_FUENTE = {"SUSTENTADA", "CONTRADICCION"}
RELACIONES = {"directa", "antecedente", "analogia"}  # Una cita antecedente o análoga no sustenta por sí sola.
ESTADOS_COBERTURA = {"REPRESENTADO", "NO-REPRESENTADO", "FUERA-DE-ALCANCE"}


def _normalizar(texto: str) -> str:
    sin_tildes = "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c))
    return " ".join(re.findall(r"\w+", sin_tildes.casefold()))


def carpeta_auditoria(raiz: Path, codigo: str) -> Path:
    RepositorioProcesos(raiz).carpeta(codigo)
    return raiz / AUDITORIAS / codigo.replace(".", "-")


def _tabla(texto: str, titulo: str) -> list[dict[str, str]]:
    seccion = re.search(rf"^## {re.escape(titulo)}\s*$(.*?)(?=^## |\Z)", texto, re.M | re.S)
    if not seccion:
        return []
    filas = [linea.strip() for linea in seccion.group(1).splitlines() if linea.strip().startswith("|")]
    if len(filas) < 2:
        return []
    columnas = [c.strip() for c in filas[0].strip("|").split("|")]
    return [dict(zip(columnas, (c.strip() for c in f.strip("|").split("|")), strict=False)) for f in filas[2:]]


def inventariar_elementos(raiz: Path, codigo: str) -> dict:
    """Lista cajas, eventos, compuertas, flujos, carriles y mensajes con IDs estables de auditoría."""
    raiz = raiz.resolve()
    tabla = RepositorioProcesos(raiz).rutas(codigo)["tabla"]
    if not tabla.is_file():
        raise ErrorDominio(f"{codigo} no tiene tabla de modelo (SIN-MODELO)", 404)
    texto = tabla.read_text(encoding="utf-8")
    items = []
    for pool in _tabla(texto, "Pools"):
        for carril in (c.strip() for c in pool.get("Carriles", "").split(";") if c.strip()):
            items.append({"id": f"C:{pool['Pool']}/{carril}", "clase": "carril", "nombre": carril})
    for fila in _tabla(texto, "Elementos"):
        items.append({"id": fila["ID"], "clase": "elemento", "tipo": fila.get("Tipo", ""),
                      "nombre": fila.get("Nombre", ""),
                      "carril": fila.get("Carril", ""), "clase_modelo": fila.get("Clase", ""),
                      "fuente_modelo": fila.get("Fuente", "")})  # fmt: skip
        for destino in (d.strip() for d in fila.get("Siguiente", "").split(";") if d.strip()):
            objetivo = re.match(r"([A-Za-z0-9]+)\s*(?:\[(.*)\])?", destino)
            if objetivo:
                items.append({"id": f"F:{fila['ID']}>{objetivo.group(1)}", "clase": "flujo",
                              "nombre": objetivo.group(2) or ""})  # fmt: skip
    for mensaje in _tabla(texto, "Mensajes"):
        items.append(
            {"id": f"M:{mensaje['Desde']}>{mensaje['Hacia']}", "clase": "mensaje", "nombre": mensaje["Nombre"]}
        )
    inventario = {
        "esquema": "inventario-auditoria-v1",
        "codigo": codigo,
        "tabla": tabla.relative_to(raiz).as_posix(),
        "revision_tabla": _sha256(tabla),
        "fecha": datetime.now(UTC).isoformat(timespec="seconds"),
        "items": items,
    }
    _guardar(carpeta_auditoria(raiz, codigo) / "inventario.json", inventario)
    conteo: dict[str, int] = {}
    for item in items:
        conteo[item["clase"]] = conteo.get(item["clase"], 0) + 1
    return {"codigo": codigo, "revision_tabla": inventario["revision_tabla"], "items": len(items), "por_clase": conteo}


def cargar_inventario(raiz: Path, codigo: str) -> dict:
    ruta = carpeta_auditoria(raiz, codigo) / "inventario.json"
    if not ruta.is_file():
        raise ErrorDominio("Falta el inventario; ejecute 'auditoria inventariar-elementos' primero")
    return json.loads(ruta.read_text(encoding="utf-8"))


def eventos(raiz: Path, codigo: str) -> list[dict]:
    ruta = carpeta_auditoria(raiz, codigo) / "registro.jsonl"
    if not ruta.is_file():
        return []
    return [json.loads(linea) for linea in ruta.read_text(encoding="utf-8").splitlines() if linea.strip()]


def vigentes(raiz: Path, codigo: str) -> dict[str, dict]:
    """Último evento de cada afirmación; una rectificación sustituye al anterior sin borrarlo."""
    return {evento["clave"]: evento for evento in eventos(raiz, codigo)}


def _validar(entrada: dict, ids: set[str], base) -> tuple[list[str], list[dict]]:
    errores, fuentes = [], []
    etiqueta = f"{entrada.get('elemento')}/{entrada.get('aspecto')}"
    if entrada.get("elemento") not in ids:
        errores.append(f"ID-AUSENTE {etiqueta}")
    if entrada.get("aspecto") not in ASPECTOS:
        errores.append(f"ASPECTO {etiqueta}")
    if entrada.get("resultado") not in RESULTADOS:
        errores.append(f"RESULTADO {etiqueta}: {entrada.get('resultado')}")
    if entrada.get("clase") not in CLASES:
        errores.append(f"CLASE {etiqueta}: {entrada.get('clase')}")
    if not str(entrada.get("afirmacion", "")).strip() or not str(entrada.get("razonamiento", "")).strip():
        errores.append(f"TEXTO-VACIO {etiqueta}")
    if entrada.get("resultado") in REQUIERE_FUENTE and not entrada.get("fuentes"):
        errores.append(f"SIN-FUENTE {etiqueta}")
    fuentes_entrada = entrada.get("fuentes") or []
    for fuente in fuentes_entrada:
        if fuente.get("relacion") not in RELACIONES or not str(fuente.get("ambito", "")).strip():
            errores.append(
                f"CONTEXTO-CITA {etiqueta}: indique ámbito del pasaje y relación (directa/antecedente/analogia)"
            )
    if entrada.get("resultado") == "SUSTENTADA" and not any(f.get("relacion") == "directa" for f in fuentes_entrada):
        errores.append(f"SIN-FUENTE-DIRECTA {etiqueta}: un antecedente o una analogía no sustentan por sí solos")
    for fuente in fuentes_entrada:
        fila = base.execute(
            "SELECT id, ruta, sha256, ubicacion, texto FROM fragmentos WHERE id = ?", (fuente.get("fragmento"),)
        ).fetchone()
        if fila is None:
            errores.append(f"CITA-INVALIDA {etiqueta}: fragmento {fuente.get('fragmento')} inexistente")
            continue
        cita = fuente.get("cita", "")
        if cita and _normalizar(cita) not in _normalizar(fila[4]):
            errores.append(f"CITA-INVALIDA {etiqueta}: la cita no aparece en {fila[0]}")
        contexto = {"ambito": fuente.get("ambito", ""), "relacion": fuente.get("relacion", "")}
        fuentes.append({"fragmento": fila[0], "ruta": fila[1], "sha256": fila[2], "ubicacion": json.loads(fila[3]),
                        "cita": cita, **contexto})  # fmt: skip
    return errores, fuentes


def registrar(raiz: Path, codigo: str, entradas: list[dict], actor: str = "agente-ia") -> dict:
    """Valida todo el lote antes de escribir; no duplica afirmaciones idénticas."""
    raiz = raiz.resolve()
    inventario = cargar_inventario(raiz, codigo)
    tabla = raiz / inventario["tabla"]
    if _sha256(tabla) != inventario["revision_tabla"]:
        raise ErrorDominio("La tabla cambió después del inventario; vuelva a inventariar", 409)
    ids = {item["id"] for item in inventario["items"]}
    base, desactualizado = _conectar(raiz)
    if desactualizado:
        raise ErrorDominio("El índice de fuentes está desactualizado; ejecute 'fuentes indexar'", 409)
    errores, preparados = [], []
    with closing(base):
        for entrada in entradas:
            fallas, fuentes = _validar(entrada, ids, base)
            errores += fallas
            preparados.append((entrada, fuentes))
    if errores:
        raise ErrorDominio("Lote rechazado sin escribir: " + "; ".join(errores[:20]))
    previos = vigentes(raiz, codigo)
    nuevos, repetidos, rectificaciones = [], 0, 0
    fecha = datetime.now(UTC).isoformat(timespec="seconds")
    for entrada, fuentes in preparados:
        clave = hashlib.sha256(
            f"{entrada['elemento']}|{entrada['aspecto']}|{_normalizar(entrada['afirmacion'])}".encode()
        ).hexdigest()[:16]
        contenido = {
            "elemento": entrada["elemento"],
            "aspecto": entrada["aspecto"],
            "afirmacion": entrada["afirmacion"].strip(),
            "resultado": entrada["resultado"],
            "clase": entrada["clase"],
            "fuentes": fuentes,
            "razonamiento": entrada["razonamiento"].strip(),
            "revision_tabla": inventario["revision_tabla"],
        }
        previo = previos.get(clave)
        if previo and all(previo.get(k) == v for k, v in contenido.items()):
            repetidos += 1
            continue
        rectificaciones += previo is not None
        evento = {"clave": clave, "tipo": "rectificacion" if previo else "registro", **contenido,
                  "fecha": fecha, "actor": actor}  # fmt: skip
        evento["evento"] = hashlib.sha256(json.dumps(evento, sort_keys=True).encode()).hexdigest()[:16]
        nuevos.append(evento)
        previos[clave] = evento
    ruta = carpeta_auditoria(raiz, codigo) / "registro.jsonl"
    with ruta.open("a", encoding="utf-8") as archivo:
        for evento in nuevos:
            archivo.write(json.dumps(evento, ensure_ascii=False) + "\n")
    return {"codigo": codigo, "registrados": len(nuevos) - rectificaciones, "rectificaciones": rectificaciones,
            "repetidos": repetidos, "registro": ruta.relative_to(raiz).as_posix()}  # fmt: skip


def registrar_cobertura(raiz: Path, codigo: str, entradas: list[dict]) -> dict:
    """Mapea cada obligación del pasaje rector a un elemento o declara por qué no está representada.

    Complementa el registro modelo→fuente con la dirección fuente→modelo; reemplaza la cobertura anterior
    del proceso (el historial queda en Git) y rechaza todo el lote ante un error.
    """
    raiz = raiz.resolve()
    inventario = cargar_inventario(raiz, codigo)
    if _sha256(raiz / inventario["tabla"]) != inventario["revision_tabla"]:
        raise ErrorDominio("La tabla cambió después del inventario; vuelva a inventariar", 409)
    ids = {item["id"] for item in inventario["items"]}
    errores, filas = [], []
    base, _ = _conectar(raiz)
    with closing(base):
        for n, entrada in enumerate(entradas, 1):
            etiqueta = f"cobertura {n}"
            fila = base.execute("SELECT id, ruta, sha256, ubicacion, texto FROM fragmentos WHERE id = ?",
                                (entrada.get("fragmento"),)).fetchone()  # fmt: skip
            if fila is None:
                errores.append(f"CITA-INVALIDA {etiqueta}: fragmento inexistente")
                continue
            if not entrada.get("cita") or _normalizar(entrada["cita"]) not in _normalizar(fila[4]):
                errores.append(f"CITA-INVALIDA {etiqueta}: la cita no aparece en {fila[0]}")
            if entrada.get("estado") not in ESTADOS_COBERTURA:
                errores.append(f"ESTADO {etiqueta}: {entrada.get('estado')}")
            elementos = entrada.get("elementos") or []
            if entrada.get("estado") == "REPRESENTADO" and (not elementos or set(elementos) - ids):
                errores.append(f"ID-AUSENTE {etiqueta}: {sorted(set(elementos) - ids) or 'sin elementos'}")
            if not str(entrada.get("obligacion", "")).strip() or not str(entrada.get("razonamiento", "")).strip():
                errores.append(f"TEXTO-VACIO {etiqueta}")
            filas.append({"fragmento": fila[0], "ruta": fila[1], "sha256": fila[2], "ubicacion": json.loads(fila[3]),
                          "cita": entrada.get("cita", ""), "obligacion": entrada.get("obligacion", ""),
                          "aspecto": entrada.get("aspecto", ""), "estado": entrada.get("estado"),
                          "elementos": elementos, "razonamiento": entrada.get("razonamiento", "")})  # fmt: skip
    if errores:
        raise ErrorDominio("Cobertura rechazada sin escribir: " + "; ".join(errores[:20]))
    datos = {"codigo": codigo, "revision_tabla": inventario["revision_tabla"],
             "fecha": datetime.now(UTC).isoformat(timespec="seconds"), "obligaciones": filas}  # fmt: skip
    _guardar(carpeta_auditoria(raiz, codigo) / "cobertura-fuente.json", datos)
    conteo: dict[str, int] = {}
    for fila in filas:
        conteo[fila["estado"]] = conteo.get(fila["estado"], 0) + 1
    return {"codigo": codigo, "obligaciones": len(filas), "por_estado": conteo}


def cargar_cobertura(raiz: Path, codigo: str) -> dict:
    ruta = carpeta_auditoria(raiz, codigo) / "cobertura-fuente.json"
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.is_file() else {"obligaciones": []}
