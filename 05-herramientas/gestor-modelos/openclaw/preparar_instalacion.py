"""Genera los archivos que instala el script 217 de ia-familiar a partir de esta carpeta (DEC-068).

Uso: python3 openclaw/preparar_instalacion.py <carpeta-del-script-217>

Escribe ``patch-agentes-mesa.json5`` (herramientas y modelo por agente para ``openclaw config patch``),
``agentes.tsv`` (agente, modelo, número de herramientas) y ``<agente>.AGENTS.md`` (rol + ``comun.md``).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ORIGEN = Path(__file__).resolve().parent


def preparar(destino: Path) -> dict:
    configuracion = json.loads((ORIGEN / "agentes.json").read_text(encoding="utf-8"))
    servidor = configuracion["servidor_mcp"]
    lineas = (ORIGEN / "comun.md").read_text(encoding="utf-8").splitlines()
    comun = "\n".join(linea for linea in lineas if not linea.startswith("<!-- markdownlint")).strip()
    destino.mkdir(parents=True, exist_ok=True)
    entradas, filas = {}, []
    for agente, datos in configuracion["agentes"].items():
        permitidas = [f"{servidor}__{herramienta}" for herramienta in datos["herramientas"]]
        entradas[agente] = {
            "models": {datos["modelo"]: {"agentRuntime": {"id": "openclaw"}}},
            "tools": {"profile": "minimal", "allow": permitidas, "sandbox": {"tools": {"allow": permitidas}}},
        }
        filas.append(f"{agente}\t{datos['modelo']}\t{len(permitidas)}\n")
        rol = (ORIGEN / f"{agente}.AGENTS.md").read_text(encoding="utf-8")
        (destino / f"{agente}.AGENTS.md").write_text(f"{rol.rstrip()}\n\n{comun}\n", encoding="utf-8")
    parche = json.dumps({"agents": {"entries": entradas}}, ensure_ascii=False, indent=2) + "\n"
    (destino / "patch-agentes-mesa.json5").write_text(parche, encoding="utf-8")
    (destino / "agentes.tsv").write_text("".join(filas), encoding="utf-8")
    return entradas


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    for nombre, entrada in preparar(Path(sys.argv[1])).items():
        print(nombre, len(entrada["tools"]["allow"]), "herramientas")
