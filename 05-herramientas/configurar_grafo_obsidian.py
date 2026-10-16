"""Aplica al grafo local de Obsidian los grupos de color y filtros comunes del proyecto (DEC-018).

`.obsidian/graph.json` no se versiona porque Obsidian reescribe en el el zoom y otros
valores en cada uso. Este script escribe solo los grupos de color y, si se indica, el
filtro de una vista; conserva el resto de la configuracion personal.

Uso, desde la raiz del repositorio y con Obsidian cerrado o sin el grafo abierto:

    python 05-herramientas/configurar_grafo_obsidian.py
    python 05-herramientas/configurar_grafo_obsidian.py --vista conocimiento
    python 05-herramientas/configurar_grafo_obsidian.py --vista navegacion
    python 05-herramientas/configurar_grafo_obsidian.py --vista modelo-procesos
    python 05-herramientas/configurar_grafo_obsidian.py --vista proceso --codigo S4.3
    python 05-herramientas/configurar_grafo_obsidian.py --check
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAFO = ROOT / ".obsidian" / "graph.json"

# El orden importa: Obsidian aplica el primer grupo que coincide con cada nota.
GRUPOS = (
    ("Procesos en alcance", "[alcance_proyecto:EN-ALCANCE]", 0xFF7F0E),
    ("Procesos de referencia", "[alcance_proyecto:REFERENCIA]", 0xC7C7C7),
    ("Actores externos", "path:03-conocimiento/actores-y-roles", 0xE6C229),
    ("Notas indice", "[tipo:mapa-de-contenido]", 0x9AA0A6),
    (
        "Documentos NT",
        (
            "[documento_nt:ficha-producto-proceso] OR [documento_nt:ficha-indicador] "
            "OR [documento_nt:procedimiento] OR [documento_nt:inventario] OR [documento_nt:mapa]"
        ),
        0x1F77B4,
    ),
    ("Sustentos", "file:sustento", 0x17BECF),
    ("Conocimiento", "path:03-conocimiento", 0x2CA02C),
    ("Referencias", "path:01-referencias", 0x8C564B),
    ("Gobernanza", "path:00-gobernanza", 0x9467BD),
)

VISTAS = {
    "navegacion": "",
    "conocimiento": "-[tipo:mapa-de-contenido] -file:00-GESTION-POR-PROCESOS-GRH -file:README -path:00-gobernanza/plantillas",
    "modelo-procesos": (
        "(path:02-procesos [tipo:mapa-de-contenido] -path:02-procesos/to-be) OR path:03-conocimiento/actores-y-roles"
    ),
    "proceso": None,  # se construye con --codigo
}


def filtro_proceso(codigo: str) -> str:
    partes = codigo.strip().upper().split(".")
    cadena = ["-".join(partes[: i + 1]).lower() for i in range(len(partes))]
    return "tag:#proceso/" + "/".join(cadena)


def grupos_obsidian() -> list[dict]:
    return [{"query": consulta, "color": {"a": 1, "rgb": rgb}} for _, consulta, rgb in GRUPOS]


def leer() -> dict:
    if not GRAFO.exists():
        return {}
    try:
        return json.loads(GRAFO.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        sys.exit(f"ERROR: {GRAFO} no es JSON valido: {error}")


def escribir(config: dict) -> None:
    GRAFO.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporal = tempfile.mkstemp(dir=GRAFO.parent, prefix=".graph-", suffix=".json")
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as salida:
            json.dump(config, salida, ensure_ascii=False, indent=2)
            salida.write("\n")
        os.replace(temporal, GRAFO)
    except BaseException:
        Path(temporal).unlink(missing_ok=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--vista", choices=sorted(VISTAS), help="filtro del grafo global que se aplicara")
    parser.add_argument("--codigo", help="codigo NT del proceso para la vista 'proceso', por ejemplo S4.3")
    parser.add_argument("--check", action="store_true", help="solo comprueba si los grupos estan aplicados")
    args = parser.parse_args()

    config = leer()
    if args.check:
        if config.get("colorGroups") == grupos_obsidian():
            print("OK: grupos de color del proyecto aplicados.")
            return 0
        print("PENDIENTE: los grupos de color difieren de los del proyecto.")
        return 1

    if args.vista == "proceso" and not args.codigo:
        parser.error("la vista 'proceso' requiere --codigo, por ejemplo --codigo S4.3")
    filtro = filtro_proceso(args.codigo) if args.vista == "proceso" else VISTAS.get(args.vista)
    config["colorGroups"] = grupos_obsidian()
    if args.vista is not None:
        config["search"] = filtro
    escribir(config)
    print(f"Grupos aplicados en {GRAFO.relative_to(ROOT)}:")
    for nombre, consulta, _ in GRUPOS:
        print(f"  - {nombre}: {consulta}")
    if args.vista is not None:
        print(f"Vista '{args.vista}': {filtro or '(sin filtro)'}")
    print("Si Obsidian esta abierto, cierre y vuelva a abrir el grafo para ver los cambios.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
