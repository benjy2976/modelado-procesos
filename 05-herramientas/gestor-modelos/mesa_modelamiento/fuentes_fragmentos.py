"""Ejecución reanudable de la segmentación sobre los textos derivados de PDF y Office."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

from .fuentes_extraccion import BASE
from .fuentes_office import cargar_manifiesto_office
from .fuentes_preparacion import MANIFIESTO, _guardar, _sha256
from .fuentes_segmentacion import segmentar_office, segmentar_pdf

SEGMENTOS = BASE / "segmentos"
MANIFIESTO_SEGMENTOS = BASE / "segmentacion.json"
VERSION = "segmentacion-v4"
FALLAS = {"CACHE-FALTANTE", "ORIGINAL-CAMBIO", "PAGINACION-DISTINTA", "CACHE-ALTERADA", "MARCADORES-DISTINTOS"}
UMBRAL_COBERTURA = 0.98


def _fuentes(raiz: Path):
    ruta_pdf = raiz / MANIFIESTO
    if ruta_pdf.is_file():
        for dato in json.loads(ruta_pdf.read_text(encoding="utf-8")).get("documentos", {}).values():
            extraccion = dato.get("extraccion")
            if extraccion and dato.get("evaluacion_extraccion") not in FALLAS:
                yield dato, "pdf", extraccion
    for dato in cargar_manifiesto_office(raiz).get("documentos", {}).values():
        if dato.get("extraccion"):
            yield dato, dato["tipo"], dato["extraccion"]


def cargar_manifiesto_segmentos(raiz: Path) -> dict:
    ruta = raiz / MANIFIESTO_SEGMENTOS
    return json.loads(ruta.read_text(encoding="utf-8")) if ruta.is_file() else {"documentos": {}}


def _documento(dato: dict) -> str:
    """Clave del documento: el hash de la ruta distingue copias idénticas guardadas en carpetas distintas."""
    return f"{dato['sha256'][:16].lower()}-{hashlib.sha256(dato['ruta'].encode()).hexdigest()[:8]}"


def _completar(fragmento: dict, dato: dict, tipo: str, extraccion: dict) -> dict:
    metodos = extraccion.get("metodos") or []
    if tipo == "pdf":
        usados = {metodos[p - 1] for p in fragmento["ubicacion"]["paginas"] if 0 < p <= len(metodos)}
    else:
        usados = {"estructura-ooxml"}
    return {
        "id": f"{_documento(dato)}:{fragmento['clave']}",
        "documento": {"id": dato["id"], "ruta": dato["ruta"], "sha256": dato["sha256"], "tipo": tipo},
        **fragmento,
        "metodos": sorted(usados),
        "estado_texto": extraccion["estado"],
    }


def _segmentar_documento(raiz: Path, dato: dict, tipo: str, extraccion: dict) -> dict:
    ruta_texto = raiz / extraccion["ruta"]
    if _sha256(ruta_texto) != extraccion["sha256_texto"]:
        return {"estado": "TEXTO-ALTERADO"}
    texto = ruta_texto.read_text(encoding="utf-8")
    fragmentos, metricas = segmentar_pdf(texto) if tipo == "pdf" else segmentar_office(texto)
    completos = [_completar(f, dato, tipo, extraccion) for f in fragmentos]
    destino = raiz / SEGMENTOS / Path(extraccion["ruta"]).parent.name / f"{Path(extraccion['ruta']).stem}.jsonl"
    destino.parent.mkdir(parents=True, exist_ok=True)
    temporal = destino.with_suffix(".tmp")
    temporal.write_text("".join(json.dumps(f, ensure_ascii=False) + "\n" for f in completos), encoding="utf-8")
    temporal.replace(destino)
    cubiertos = sum(len(re.sub(r"\s", "", f["texto"])) for f in completos)
    origen = metricas.pop("caracteres_origen")
    return {
        "estado": "SEGMENTADO",
        "segmentos": destino.relative_to(raiz).as_posix(),
        "sha256_segmentos": _sha256(destino),
        "fragmentos": len(completos),
        "estructuras": dict(Counter(f["estructura"] for f in completos)),
        "cobertura": round(cubiertos / origen, 4) if origen else 1.0,
        "claves_repetidas": sum(bool(f.get("clave_repetida")) for f in completos),
        "partidos": sum(bool(f.get("partido")) for f in completos),
        **metricas,
    }


def segmentar(raiz: Path, max_documentos: int | None = None) -> dict:
    """Divide cada texto derivado en fragmentos con ubicación; no repite textos sin cambios."""
    raiz = raiz.resolve()
    anteriores = cargar_manifiesto_segmentos(raiz).get("documentos", {})
    documentos: dict[str, dict] = {}
    manifiesto = {"esquema": "segmentacion-v1", "version": VERSION, "documentos": documentos}
    procesados = reutilizados = 0
    for dato, tipo, extraccion in _fuentes(raiz):
        previo = anteriores.get(dato["ruta"], {})
        base = {
            "id": dato["id"],
            "ruta": dato["ruta"],
            "tipo": tipo,
            "sha256": dato["sha256"],
            "texto": extraccion["ruta"],
            "sha256_texto": extraccion["sha256_texto"],
            "version": VERSION,
        }
        vigente = all(previo.get(k) == base[k] for k in ("sha256_texto", "version"))
        if vigente and previo.get("estado") == "SEGMENTADO" and (raiz / previo["segmentos"]).is_file():
            documentos[dato["ruta"]] = previo
            reutilizados += 1
            continue
        if max_documentos is not None and procesados >= max_documentos:
            documentos[dato["ruta"]] = {**base, "estado": "PENDIENTE"}
            continue
        documentos[dato["ruta"]] = {**base, **_segmentar_documento(raiz, dato, tipo, extraccion)}
        procesados += 1
        manifiesto["actualizado"] = datetime.now(UTC).isoformat(timespec="seconds")
        _guardar(raiz / MANIFIESTO_SEGMENTOS, manifiesto)
    manifiesto["actualizado"] = datetime.now(UTC).isoformat(timespec="seconds")
    _guardar(raiz / MANIFIESTO_SEGMENTOS, manifiesto)
    segmentados = [d for d in documentos.values() if d.get("estado") == "SEGMENTADO"]
    baja = sorted((d["cobertura"], d["ruta"]) for d in segmentados if d["cobertura"] < UMBRAL_COBERTURA)
    return {
        "documentos": len(documentos),
        "estados": dict(Counter(d["estado"] for d in documentos.values())),
        "procesados": procesados,
        "reutilizados": reutilizados,
        "fragmentos": sum(d["fragmentos"] for d in segmentados),
        "modos": dict(Counter(d["modo"] for d in segmentados)),
        "cobertura_minima": min((d["cobertura"] for d in segmentados), default=None),
        "cobertura_baja": [{"ruta": r, "cobertura": c} for c, r in baja[:20]],
        "claves_repetidas": sum(d["claves_repetidas"] for d in segmentados),
        "manifiesto": MANIFIESTO_SEGMENTOS.as_posix(),
    }


def cargar_fragmentos(raiz: Path):
    """Recorre los fragmentos vigentes en orden de documento."""
    for dato in cargar_manifiesto_segmentos(raiz).get("documentos", {}).values():
        if dato.get("estado") != "SEGMENTADO":
            continue
        with (raiz / dato["segmentos"]).open(encoding="utf-8") as archivo:
            for orden, linea in enumerate(archivo):
                yield orden, json.loads(linea)
