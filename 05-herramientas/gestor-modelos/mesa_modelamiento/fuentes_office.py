"""Preparación de DOCX, PPTX y XLSX de la biblioteca con manifiesto propio y reanudable."""

from __future__ import annotations

import json
import zipfile
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from xml.etree import ElementTree as ET

from .fuentes_docx import convertir_docx
from .fuentes_extraccion import BASE, _destino
from .fuentes_ooxml import convertir_pptx, fichar_xlsx
from .fuentes_preparacion import REFERENCIAS, _catalogo, _guardar, _sha256

MANIFIESTO_OFFICE = BASE / "preparacion-office.json"
VERSION = "office-ooxml-v1"
TIPOS = {".docx": "docx", ".pptx": "pptx", ".xlsx": "xlsx"}
ESTADO_TEXTO = "EXTRAIDO-ESTRUCTURADO-PENDIENTE-COTEJO"
ANCLAS = {"docx": "parrafo", "pptx": "diapositiva"}
AVISO = {
    "docx": "Numeración automática reconstruida desde numbering.xml; cotejar el numeral con el documento abierto.",
    "pptx": "Texto por diapositiva sin disposición visual; cotejar con la presentación abierta.",
}


def cargar_manifiesto_office(raiz: Path) -> dict:
    ruta = raiz / MANIFIESTO_OFFICE
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.is_file() else {"documentos": {}}


def _originales(raiz: Path):
    for ruta in sorted((raiz / REFERENCIAS).rglob("*")):
        relativa = ruta.relative_to(raiz).as_posix()
        if relativa.startswith(BASE.parent.as_posix()) or ruta.name.startswith("~$"):
            continue
        if ruta.suffix.lower() in TIPOS and ruta.is_file():
            yield ruta, relativa


def _escribir_texto(raiz: Path, dato: dict, cuerpo: str, resumen: dict) -> dict:
    tipo = dato["tipo"]
    encabezado = {
        "esquema": f"texto-{tipo}-estructurado-v1",
        "id_documento": dato["id"],
        "original": dato["ruta"],
        "sha256_original": dato["sha256"],
        "fuente_url": dato["url"],
        "herramienta": f"modelador-procesos/{VERSION}",
        "fecha_extraccion": datetime.now(UTC).isoformat(timespec="seconds"),
        "estado_calidad": ESTADO_TEXTO,
        "unidad_ancla": ANCLAS[tipo],
        "aviso": AVISO[tipo],
    }
    destino = _destino(raiz, dato)
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporal = destino.with_suffix(".tmp")
    cabecera = f"<!-- metadatos: {json.dumps(encabezado, ensure_ascii=False)} -->"
    temporal.write_text(f"{cabecera}\n\n{cuerpo}", encoding="utf-8")
    temporal.replace(destino)
    return {
        "ruta": destino.relative_to(raiz).as_posix(),
        "sha256_texto": _sha256(destino),
        "estado": ESTADO_TEXTO,
        "unidad_ancla": ANCLAS[tipo],
        "resumen": resumen,
    }


def _procesar(raiz: Path, ruta: Path, dato: dict) -> None:
    datos = ruta.read_bytes()
    if dato["tipo"] == "xlsx":
        dato["ficha"] = fichar_xlsx(datos)
        dato["estado"] = "FICHADO"
        return
    cuerpo, resumen = convertir_docx(datos) if dato["tipo"] == "docx" else convertir_pptx(datos)
    dato["extraccion"] = _escribir_texto(raiz, dato, cuerpo, resumen)
    dato["estado"] = ESTADO_TEXTO


def _reutilizable(raiz: Path, previo: dict, sha: str) -> bool:
    if previo.get("sha256") != sha or previo.get("version") != VERSION or previo.get("estado") == "PENDIENTE":
        return False
    extraccion = previo.get("extraccion")
    return not extraccion or (raiz / extraccion["ruta"]).is_file()


def extraer_office(raiz: Path, max_documentos: int | None = None) -> dict:
    """Convierte DOCX/PPTX a Markdown anclado y ficha XLSX; nunca modifica los originales."""
    raiz = raiz.resolve()
    indice, _ = _catalogo(raiz)
    anteriores = cargar_manifiesto_office(raiz).get("documentos", {})
    documentos: dict[str, dict] = {}
    procesados = reutilizados = 0
    manifiesto = {"esquema": "preparacion-office-v1", "version_conversor": VERSION, "documentos": documentos}
    for ruta, relativa in _originales(raiz):
        sha = _sha256(ruta)
        ficha = indice.get(relativa, {})
        previo = anteriores.get(relativa, {})
        if _reutilizable(raiz, previo, sha):
            documentos[relativa] = previo
            reutilizados += 1
            continue
        dato = {
            "id": ficha.get("id") or f"PENDIENTE-{sha[:12]}",
            "ruta": relativa,
            "tipo": TIPOS[ruta.suffix.lower()],
            "sha256": sha,
            "bytes": ruta.stat().st_size,
            "catalogado": relativa in indice,
            "hash_coincide": not ficha.get("sha256_registrado") or sha == ficha["sha256_registrado"].upper(),
            "url": ficha.get("url", ""),
            "titulo": ficha.get("titulo", ""),
            "version": VERSION,
            "estado": "PENDIENTE",
        }
        documentos[relativa] = dato
        if max_documentos is not None and procesados >= max_documentos:
            continue
        try:
            _procesar(raiz, ruta, dato)
        except (zipfile.BadZipFile, KeyError, ET.ParseError, ValueError) as exc:
            dato["estado"] = "NO-CONFIABLE"
            dato["error"] = f"{type(exc).__name__}: {exc}"[:300]
        procesados += 1
        manifiesto["actualizado"] = datetime.now(UTC).isoformat(timespec="seconds")
        _guardar(raiz / MANIFIESTO_OFFICE, manifiesto)
    hashes: dict[str, list[str]] = defaultdict(list)
    for relativa, dato in documentos.items():
        hashes[dato["sha256"]].append(relativa)
    manifiesto["faltantes_catalogo"] = sorted(
        r for r in indice if Path(r).suffix.lower() in TIPOS and r not in documentos
    )
    manifiesto["duplicados_sha256"] = [rutas for rutas in hashes.values() if len(rutas) > 1]
    manifiesto["actualizado"] = datetime.now(UTC).isoformat(timespec="seconds")
    _guardar(raiz / MANIFIESTO_OFFICE, manifiesto)
    return {
        "presentes": dict(sorted(Counter(d["tipo"] for d in documentos.values()).items())),
        "estados": dict(sorted(Counter(d["estado"] for d in documentos.values()).items())),
        "procesados": procesados,
        "reutilizados": reutilizados,
        "sin_catalogo": sum(not d["catalogado"] for d in documentos.values()),
        "hash_distinto": sum(not d["hash_coincide"] for d in documentos.values()),
        "faltantes_catalogo": manifiesto["faltantes_catalogo"],
        "duplicados_sha256": len(manifiesto["duplicados_sha256"]),
        "manifiesto": MANIFIESTO_OFFICE.as_posix(),
    }
