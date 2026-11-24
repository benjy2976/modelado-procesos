"""Índice Markdown legible de la caché: enlaza cada original con su texto derivado."""

from __future__ import annotations

import json
import os
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import quote

from .fuentes_extraccion import BASE
from .fuentes_office import cargar_manifiesto_office
from .fuentes_preparacion import MANIFIESTO

INDICE = BASE / "00-indice.md"


def _enlace(raiz: Path, ruta: str) -> str:
    relativa = Path(os.path.relpath(raiz / ruta, raiz / BASE)).as_posix()
    return quote(relativa, safe="/-._~")


def _celda(texto: str) -> str:
    return texto.replace("|", "/").replace("\n", " ")


def _fila_pdf(dato: dict) -> dict:
    extraccion = dato.get("extraccion") or {}
    metodos = Counter(extraccion.get("metodos", []))
    if not metodos:
        metodo = "—"
    elif set(metodos) == {"nativo"}:
        metodo = "nativo"
    elif set(metodos) == {"ocr"}:
        metodo = "OCR"
    else:
        metodo = f"mixto ({metodos.get('ocr', 0)} pág. OCR)"
    estado = dato.get("evaluacion_extraccion") or extraccion.get("estado") or dato.get("plan", {}).get("estado", "")
    paginas = extraccion.get("paginas") or dato.get("diagnostico", {}).get("total", 0)
    return {
        "tipo": "PDF",
        "texto": extraccion.get("ruta"),
        "contenido": f"{paginas} pág.",
        "metodo": metodo,
        "estado": estado,
    }


def _fila_office(dato: dict) -> dict:
    resumen = (dato.get("extraccion") or {}).get("resumen", {})
    if dato["tipo"] == "docx":
        contenido = f"{resumen.get('parrafos_con_texto', 0)} párr., {resumen.get('tablas', 0)} tablas"
    elif dato["tipo"] == "pptx":
        contenido = f"{resumen.get('diapositivas', 0)} diap."
    else:
        contenido = f"{len(dato.get('ficha', {}).get('hojas', []))} hojas (ficha en manifiesto)"
    return {
        "tipo": dato["tipo"].upper(),
        "texto": (dato.get("extraccion") or {}).get("ruta"),
        "contenido": contenido,
        "metodo": "estructura OOXML",
        "estado": dato.get("estado", ""),
    }


def generar_indice(raiz: Path) -> dict:
    """Reescribe ``cache/00-indice.md`` a partir de los manifiestos PDF y Office."""
    raiz = raiz.resolve()
    filas = []
    ruta_pdf = raiz / MANIFIESTO
    if ruta_pdf.is_file():
        for dato in json.loads(ruta_pdf.read_text(encoding="utf-8")).get("documentos", {}).values():
            filas.append({**_fila_pdf(dato), "id": dato["id"], "ruta": dato["ruta"], "titulo": dato.get("titulo", "")})
    for dato in cargar_manifiesto_office(raiz).get("documentos", {}).values():
        filas.append({**_fila_office(dato), "id": dato["id"], "ruta": dato["ruta"], "titulo": dato.get("titulo", "")})
    grupos: dict[str, list[dict]] = defaultdict(list)
    for fila in filas:
        partes = Path(fila["ruta"]).parts
        grupos[" / ".join(partes[1:-1]) or partes[0]].append(fila)
    tipos = Counter(f["tipo"] for f in filas)
    con_texto = sum(bool(f["texto"]) for f in filas)
    lineas = [
        "# Índice de la caché de textos derivados",
        "",
        "Archivo generado por `modelador-procesos fuentes indice`; no editar a mano. "
        f"Actualizado: {datetime.now(UTC).isoformat(timespec='seconds')}.",
        "",
        "Cada fila enlaza el **original** (la evidencia) y su **texto derivado** (solo para búsqueda). "
        "El texto derivado no sustituye al original ni acredita fidelidad, vigencia o validez normativa.",
        "",
        f"Documentos: {len(filas)} ({', '.join(f'{n} {t}' for t, n in sorted(tipos.items()))}); "
        f"con texto derivado: {con_texto}.",
    ]
    for grupo in sorted(grupos):
        lineas += [
            "",
            f"## {grupo}",
            "",
            "| ID | Documento | Tipo | Texto | Contenido | Método | Estado |",
            "|---|---|---|---|---|---|---|",
        ]
        for fila in sorted(grupos[grupo], key=lambda f: (f["id"], f["ruta"])):
            nombre = _celda(fila["titulo"] or Path(fila["ruta"]).name)
            documento = f"[{nombre}]({_enlace(raiz, fila['ruta'])})"
            texto = f"[abrir]({_enlace(raiz, fila['texto'])})" if fila["texto"] else "—"
            lineas.append(
                f"| {fila['id']} | {documento} | {fila['tipo']} | {texto} | {fila['contenido']} | "
                f"{fila['metodo']} | {_celda(fila['estado'])} |"
            )
    destino = raiz / INDICE
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporal = destino.with_suffix(".tmp")
    temporal.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    temporal.replace(destino)
    return {"indice": INDICE.as_posix(), "documentos": len(filas), "con_texto": con_texto, "grupos": len(grupos)}
