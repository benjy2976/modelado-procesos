"""Exportación reproducible del contrato OpenAPI de la API local."""

from __future__ import annotations

import json
from pathlib import Path

from .api import app

CONTRATO = Path(__file__).resolve().parents[1] / "contracts" / "openapi.json"


def contenido_openapi() -> str:
    """Serializar el schema generado, sin mantener una segunda definición manual."""
    return json.dumps(app.openapi(), ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def sincronizar_contrato(*, comprobar: bool = False) -> bool:
    """Escribir o comprobar el snapshot; devuelve False si la copia está desfasada."""
    contenido = contenido_openapi()
    if comprobar:
        return CONTRATO.exists() and CONTRATO.read_text(encoding="utf-8") == contenido
    CONTRATO.parent.mkdir(parents=True, exist_ok=True)
    CONTRATO.write_text(contenido, encoding="utf-8")
    return True
