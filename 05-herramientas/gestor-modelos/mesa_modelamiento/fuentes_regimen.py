"""Régimen de ejecución de cada documento de la biblioteca, por reglas de carpeta y excepciones explícitas."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from .fuentes_preparacion import REFERENCIAS
from .repositorio import ErrorDominio

REGLAS = REFERENCIAS / "00-catalogo" / "regimen-documental.json"
SIN_REGLA = "NO-DETERMINADO"


def cargar_reglas(raiz: Path) -> dict:
    ruta = raiz / REGLAS
    if not ruta.is_file():
        return {"valores": {SIN_REGLA: ""}, "reglas": [], "excepciones": []}
    return json.loads(ruta.read_text(encoding="utf-8"))


def clasificar(reglas: dict, ruta: str) -> tuple[str, str]:
    """Régimen y criterio: la excepción exacta prevalece; si no, la regla de prefijo más largo."""
    for excepcion in reglas.get("excepciones", []):
        if excepcion["ruta"] == ruta:
            return excepcion["regimen"], excepcion["criterio"]
    candidatas = [r for r in reglas.get("reglas", []) if ruta.startswith(r["prefijo"])]
    if not candidatas:
        return SIN_REGLA, "Sin regla de carpeta"
    regla = max(candidatas, key=lambda r: len(r["prefijo"]))
    return regla["regimen"], regla["criterio"]


def comprobar(raiz: Path, rutas: list[str]) -> dict:
    """Valida valores y prefijos, y resume la clasificación de los documentos indicados."""
    raiz = raiz.resolve()
    reglas = cargar_reglas(raiz)
    valores = set(reglas.get("valores", {}))
    hallazgos = []
    if reglas.get("estado") == "VALIDADO":
        hallazgos.append("ESTADO: la clasificación no puede declararse VALIDADO por la herramienta")
    for entrada in reglas.get("reglas", []) + reglas.get("excepciones", []):
        if entrada.get("regimen") not in valores:
            hallazgos.append(f"VALOR-DESCONOCIDO {entrada.get('regimen')}")
        destino = entrada.get("prefijo") or entrada.get("ruta", "")
        if not (raiz / destino).exists():
            hallazgos.append(f"RUTA-INEXISTENTE {destino}")
    clasificados = {ruta: clasificar(reglas, ruta)[0] for ruta in rutas}
    return {
        "documentos": len(clasificados),
        "por_regimen": dict(sorted(Counter(clasificados.values()).items())),
        "no_determinados": sorted(r for r, v in clasificados.items() if v == SIN_REGLA),
        "hallazgos": hallazgos,
    }


def validar_valor(raiz: Path, valor: str) -> str:
    if valor not in cargar_reglas(raiz.resolve()).get("valores", {}):
        raise ErrorDominio(f"Régimen desconocido: {valor}")
    return valor
