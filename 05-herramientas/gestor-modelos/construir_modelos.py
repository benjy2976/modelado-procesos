"""Construye o comprueba los diagramas BPMN de todos los procesos en modelamiento (DEC-025, DEC-026).

Busca `02-procesos/**/<codigo>-diagrama-proceso-tabla.md` y, para cada uno:
- en la etapa logica (el `.bpmn` versionado lleva la marca de tabla_a_bpmn.py o aun no existe), genera el BPMN desde
  la tabla, lo valida (D1-D4) y, si no hay hallazgos, actualiza `<codigo>-diagrama-proceso.bpmn`;
- en la etapa formal (el `.bpmn` ya no lleva la marca), respeta el BPMN como fuente maestra y no lo regenera;
- genera `<codigo>-diagrama-proceso.svg`, `.png` y la vista interactiva `.html` con renderizar_bpmn.py; la vista
  enlaza la copia versionada de bpmn-js en vendor/ y funciona sin internet.
Ademas deja en `99-temporal/modelos/` la copia para Bizagi y el informe de validacion de cada modelo, y una pagina
`index.html` que enlaza las vistas interactivas. Esos productos de trabajo no se versionan.

Uso: python construir_modelos.py [--check] [--forzar]
  --check   no escribe: comprueba que cada BPMN, SVG y HTML versionado coincide con lo que se generaria.
  --forzar  actualiza el BPMN aunque la validacion tenga hallazgos (deben explicarse en el sustento).
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import renderizar_bpmn
from renderizar_plantuml import REPO_ROOT

AQUI = Path(__file__).resolve().parent
MARCA = "GENERADO con tabla_a_bpmn.py"
TRABAJO = REPO_ROOT / "99-temporal" / "modelos"


def tablas() -> list[Path]:
    """Diagramas de proceso en modelamiento y el catalogo de simbolos de la paleta (prueba de regresion, DEC-027)."""
    return sorted([*(REPO_ROOT / "02-procesos").rglob("*-diagrama-proceso-tabla.md"),
                   *(AQUI / "catalogo").glob("*-diagrama-proceso-tabla.md")])


def hallazgos(informe: str) -> list[str]:
    """Lineas del informe que impiden adoptar el BPMN generado."""
    malos = []
    for linea in informe.splitlines():
        texto = linea.strip()
        if ("INVÁLIDO" in texto or "CON HALLAZGOS" in texto or texto.startswith(("BLOQUEO", "ELEMENTOS SIN LLEGADA"))
                or re.search(r"D2 referencias: \d+ problema", texto) or re.search(r"D4 trazado .*: \d+ hallazgo", texto)
                or re.search(r"D5 notacion .*: \d+ hallazgo", texto)):
            malos.append(texto)
    return malos


def generar(tabla: Path, destino: Path) -> tuple[Path, str]:
    """Ejecuta tabla_a_bpmn.py y devuelve el BPMN generado y el informe de validacion."""
    destino.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([sys.executable, str(AQUI / "tabla_a_bpmn.py"), str(tabla), str(destino)],
                       capture_output=True, text=True, encoding="utf-8", check=False)
    base = re.sub(r"[^\w\-]+", "_", tabla.stem).strip("_")
    bpmn = destino / f"{base}.bpmn"
    if r.returncode or not bpmn.exists():
        raise RuntimeError(f"tabla_a_bpmn.py fallo con {tabla.name}:\n{(r.stdout + r.stderr).strip()[-1500:]}")
    informe = (destino / "validacion.txt").read_text(encoding="utf-8")
    return bpmn, informe


def titulo(tabla: Path) -> str:
    m = re.search(r"^#\s+(.+)$", tabla.read_text(encoding="utf-8"), re.MULTILINE)
    return m.group(1).strip() if m else tabla.stem


def main() -> int:
    parser = argparse.ArgumentParser(description="Construye o comprueba los diagramas BPMN en modelamiento.")
    parser.add_argument("--check", action="store_true", help="Solo comprueba; no escribe en el repositorio.")
    parser.add_argument("--forzar", action="store_true", help="Adopta el BPMN aunque la validacion tenga hallazgos.")
    args = parser.parse_args()

    encontradas = tablas()
    if not encontradas:
        print("No hay tablas de diagrama en 02-procesos.")
        return 0
    errores, filas = 0, []
    for tabla in encontradas:
        base = tabla.name[: -len("-tabla.md")]
        bpmn = tabla.with_name(f"{base}.bpmn")
        svg, png, vista = bpmn.with_suffix(".svg"), bpmn.with_suffix(".png"), bpmn.with_suffix(".html")
        rel = tabla.relative_to(REPO_ROOT).as_posix()
        formal = bpmn.exists() and MARCA not in bpmn.read_text(encoding="utf-8")[:600]
        trabajo = TRABAJO / base
        try:
            if args.check:
                with tempfile.TemporaryDirectory() as tmp:
                    if not formal:
                        generado, _ = generar(tabla, Path(tmp))
                        if not bpmn.exists() or generado.read_bytes() != bpmn.read_bytes():
                            print(f"DESACTUALIZADO: {bpmn.relative_to(REPO_ROOT)}")
                            errores += 1
                            continue
                    if not svg.exists() or renderizar_bpmn.render_svg(bpmn) != svg.read_bytes():
                        print(f"DESACTUALIZADO: {svg.relative_to(REPO_ROOT)}")
                        errores += 1
                        continue
                    pagina = renderizar_bpmn.pagina_visor_enlazada(titulo(tabla), bpmn, vista).encode("utf-8")
                    if not vista.exists() or vista.read_bytes() != pagina:
                        print(f"DESACTUALIZADO: {vista.relative_to(REPO_ROOT)}")
                        errores += 1
                        continue
                print(f"OK: {rel}")
                continue

            if trabajo.exists():
                shutil.rmtree(trabajo)
            if formal:
                informe = "Etapa formal: el BPMN versionado es la fuente maestra; no se regenera desde la tabla."
                estado = "formal"
            else:
                generado, informe = generar(tabla, trabajo)
                problemas = hallazgos(informe)
                if problemas and not args.forzar:
                    print(f"NO ADOPTADO: {rel}")
                    for p in problemas:
                        print(f"    {p}")
                    errores += 1
                    filas.append((base, titulo(tabla), "con hallazgos", informe, None))
                    continue
                if not bpmn.exists() or generado.read_bytes() != bpmn.read_bytes():
                    renderizar_bpmn.escribir(bpmn, generado.read_bytes())
                    print(f"GENERADO: {bpmn.relative_to(REPO_ROOT)}")
                estado = "logica" if not problemas else "logica con hallazgos (--forzar)"
            contenido = renderizar_bpmn.render_svg(bpmn)
            if not svg.exists() or svg.read_bytes() != contenido or not png.exists():
                renderizar_bpmn.escribir(svg, contenido)
                renderizar_bpmn.render_png(contenido, png)
                print(f"GENERADO: {svg.relative_to(REPO_ROOT)} y .png")
            pagina = renderizar_bpmn.pagina_visor_enlazada(titulo(tabla), bpmn, vista).encode("utf-8")
            if not vista.exists() or vista.read_bytes() != pagina:
                renderizar_bpmn.escribir(vista, pagina)
                print(f"GENERADO: {vista.relative_to(REPO_ROOT)}")
            filas.append((base, titulo(tabla), estado, informe, vista))
        except (OSError, RuntimeError) as error:
            print(f"ERROR: {rel}: {error}", file=sys.stderr)
            errores += 1

    if not args.check:
        TRABAJO.mkdir(parents=True, exist_ok=True)
        items = []
        for base, nombre, estado, informe, vista in filas:
            carpeta = TRABAJO / base
            bizagi = next((carpeta / "bizagi").glob("*.bpmn"), None) if (carpeta / "bizagi").exists() else None
            enlaces = []
            if vista:
                rel = os.path.relpath(vista, TRABAJO).replace(os.sep, "/")
                enlaces.append(f'<a href="{html.escape(rel)}">vista interactiva</a>')
            if bizagi:
                enlaces.append(f'<a href="{base}/bizagi/{bizagi.name}">copia para Bizagi</a>')
            items.append(f"<tr><td>{html.escape(nombre)}</td><td>{html.escape(estado)}</td>"
                         f"<td>{' · '.join(enlaces)}</td><td><pre>{html.escape(informe.strip())}</pre></td></tr>")
        (TRABAJO / "index.html").write_text(
            '<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Modelos en modelamiento</title>'
            "<style>body{font:14px Arial,sans-serif;margin:24px}table{border-collapse:collapse}"
            "td,th{border:1px solid #ccc;padding:6px 10px;vertical-align:top}pre{margin:0;font-size:11px;"
            "white-space:pre-wrap;max-width:720px}</style></head><body><h1>Modelos en modelamiento</h1>"
            "<p>Generado por construir_modelos.py; no se versiona.</p><table><tr><th>Modelo</th><th>Etapa</th>"
            "<th>Enlaces</th><th>Validacion</th></tr>" + "".join(items) + "</table></body></html>\n",
            encoding="utf-8")
        print(f"Indice: {(TRABAJO / 'index.html').relative_to(REPO_ROOT)}")
    return 1 if errores else 0


if __name__ == "__main__":
    raise SystemExit(main())
