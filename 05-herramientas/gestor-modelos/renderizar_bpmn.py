"""Renderiza BPMN 2.0 a SVG y PNG con bpmn-js fijado y un navegador local sin ventana.

No usa servicios externos al renderizar: bpmn-js se descarga una vez desde la URL fijada en `bpmn-js.lock.json`,
se comprueba por SHA-256 y se guarda en `99-temporal/herramientas/bpmn-js/`. El navegador (Edge o Chrome) corre
sin ventana, con un perfil temporal propio. El .bpmn fuente no se modifica: los colores de estilo Bizagi se aplican
a una copia en memoria.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from renderizar_plantuml import REPO_ROOT, download_verified

LOCK_PATH = Path(__file__).with_name("bpmn-js.lock.json")
BDI = "http://www.omg.org/spec/BPMN/20100524/DI"
COLOR = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
ESTILO = {  # tipo BPMN -> (relleno, borde), aproximado a la paleta de Bizagi Modeler
    "startEvent": ("#E6FF97", "#62A716"),
    "endEvent": ("#EEAAAA", "#A23030"),
    "intermediateCatchEvent": ("#FFFFE0", "#A6A600"),
    "intermediateThrowEvent": ("#FFFFE0", "#A6A600"),
    "boundaryEvent": ("#FFFFE0", "#A6A600"),
    "task": ("#ECEFFF", "#03689A"),
    "userTask": ("#ECEFFF", "#03689A"),
    "manualTask": ("#ECEFFF", "#03689A"),
    "serviceTask": ("#ECEFFF", "#03689A"),
    "sendTask": ("#ECEFFF", "#03689A"),
    "receiveTask": ("#ECEFFF", "#03689A"),
    "scriptTask": ("#ECEFFF", "#03689A"),
    "businessRuleTask": ("#ECEFFF", "#03689A"),
    "callActivity": ("#ECEFFF", "#03689A"),
    "subProcess": ("#ECEFFF", "#03689A"),
    "exclusiveGateway": ("#FFFF99", "#A6A600"),
    "parallelGateway": ("#FFFF99", "#A6A600"),
    "inclusiveGateway": ("#FFFF99", "#A6A600"),
    "eventBasedGateway": ("#FFFF99", "#A6A600"),
    "complexGateway": ("#FFFF99", "#A6A600"),
}
NAVEGADORES = (
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
)
PAGINA = """<!doctype html><html><head><meta charset="utf-8"></head><body><pre id="svg"></pre>
<script>__JS__</script>
<script>const c = document.createElement('div'); c.style.cssText = 'width:3000px;height:2000px';
document.body.appendChild(c); const v = new BpmnJS({container: c});
v.importXML(__X__).then(() => v.saveSVG()).then(r => { document.getElementById('svg').textContent = r.svg; })
 .catch(e => { document.getElementById('svg').textContent = 'ERROR ' + e; });</script></body></html>"""


def load_lock() -> dict[str, object]:
    data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    if not {"version", "artifacts"} <= set(data):
        raise RuntimeError(f"Faltan campos en {LOCK_PATH}")
    return data


def biblioteca() -> Path:
    """Ruta local de bpmn-js, descargada y verificada si hace falta."""
    artifact = load_lock()["artifacts"]["navigated_viewer"]
    return download_verified(artifact["url"], REPO_ROOT / artifact["cache_path"], artifact["sha256"])


def navegador() -> str:
    """Edge o Chrome. La variable BPMN_NAVEGADOR permite indicar otra ruta."""
    for candidato in [os.environ.get("BPMN_NAVEGADOR", ""), *NAVEGADORES]:
        if candidato and Path(candidato).is_file():
            return candidato
    for nombre in ("msedge", "chrome", "google-chrome", "chromium", "chromium-browser"):
        if shutil.which(nombre):
            return shutil.which(nombre)
    raise RuntimeError("No se encontro Edge ni Chrome; indique la ruta en la variable BPMN_NAVEGADOR.")


def colorear(xml: bytes) -> str:
    """Copia del BPMN con colores de estilo Bizagi (BPMN in Color) y etiquetas en negro."""
    raiz = etree.fromstring(xml)
    tipos = {
        e.get("id"): etree.QName(e).localname
        for e in raiz.iter()
        if isinstance(e.tag, str) and e.get("id")
    }
    for forma in raiz.iter(f"{{{BDI}}}BPMNShape"):
        estilo = ESTILO.get(tipos.get(forma.get("bpmnElement")))
        if estilo:
            forma.set(f"{{{COLOR}}}background-color", estilo[0])
            forma.set(f"{{{COLOR}}}border-color", estilo[1])
            etiqueta = forma.find(f"{{{BDI}}}BPMNLabel")
            if etiqueta is None:
                etiqueta = etree.SubElement(forma, f"{{{BDI}}}BPMNLabel")
            etiqueta.set(f"{{{COLOR}}}color", "#000000")
    etree.cleanup_namespaces(raiz, top_nsmap={"color": COLOR})
    return etree.tostring(raiz, encoding="unicode")


def ejecutar(argumentos: list[str], timeout: int = 60) -> subprocess.CompletedProcess:
    """Navegador sin ventana con perfil temporal; un reintento si se demora."""
    ultimo = None
    for _ in range(2):
        with tempfile.TemporaryDirectory() as perfil:
            comando = [
                navegador(), "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
                "--no-default-browser-check", "--disable-extensions", f"--user-data-dir={perfil}", *argumentos,
            ]
            try:
                return subprocess.run(
                    comando, capture_output=True, text=True, encoding="utf-8", errors="replace",
                    timeout=timeout, check=False,
                )
            except subprocess.TimeoutExpired as error:
                ultimo = error
    raise RuntimeError(f"El navegador no respondio en {timeout} s: {ultimo}")


def render_svg(source: Path, color: bool = True) -> bytes:
    xml = source.read_bytes()
    contenido = colorear(xml) if color else xml.decode("utf-8")
    pagina = PAGINA.replace("__JS__", biblioteca().read_text(encoding="utf-8")).replace(
        "__X__", json.dumps(contenido)
    )
    with tempfile.TemporaryDirectory() as tmp:
        ruta = Path(tmp) / "render.html"
        ruta.write_text(pagina, encoding="utf-8")
        resultado = ejecutar(["--virtual-time-budget=20000", "--dump-dom", ruta.as_uri()])
    encontrado = re.search(r'<pre id="svg">(.*?)</pre>', resultado.stdout, re.DOTALL)
    svg = html.unescape(encontrado.group(1)) if encontrado else ""
    if "<svg" not in svg[:400]:
        raise RuntimeError(f"bpmn-js no produjo un SVG para {source}: {svg[:300] or resultado.stderr[-400:]}")
    orden: dict[str, str] = {}
    for marcador in re.findall(r'id="(marker-[0-9a-z]+)"', svg):  # bpmn-js numera las flechas al azar
        orden.setdefault(marcador, f"marker-{len(orden) + 1}")
    svg = re.sub(r"marker-[0-9a-z]+", lambda m: orden.get(m.group(0), m.group(0)), svg)
    svg = svg.replace("\r\n", "\n")
    aviso = f"<!-- GENERADO - NO EDITAR. Fuente: {source.name}; bpmn-js fijado por el proyecto. -->\n"
    if svg.startswith("<?xml"):
        fin = svg.index("?>") + 2
        svg = svg[:fin] + "\n" + aviso + svg[fin:].lstrip("\n")
    else:
        svg = aviso + svg
    return svg.encode("utf-8")


def render_png(svg: bytes, destino: Path, escala: int = 2) -> None:
    texto = svg.decode("utf-8")
    caja = re.search(r'viewBox="([-\d.]+) ([-\d.]+) ([\d.]+) ([\d.]+)"', texto)
    if not caja:
        raise RuntimeError("El SVG no declara viewBox.")
    ancho, alto = int(float(caja.group(3))) + 2, int(float(caja.group(4))) + 2
    with tempfile.TemporaryDirectory() as tmp:
        vista = Path(tmp) / "png.html"
        vista.write_text(
            '<!doctype html><html><body style="margin:0;background:#fff">'
            + texto[texto.index("<svg"):] + "</body></html>",
            encoding="utf-8",
        )
        temporal = Path(tmp) / "salida.png"
        ejecutar([f"--window-size={ancho},{alto}", f"--force-device-scale-factor={escala}",
                  f"--screenshot={temporal}", vista.as_uri()])
        if not temporal.exists():
            raise RuntimeError("El navegador no produjo el PNG.")
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(temporal, destino)


def escribir(destino: Path, contenido: bytes) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destino.parent, delete=False) as temporal:
        temporal.write(contenido)
        ruta = Path(temporal.name)
    os.replace(ruta, destino)


def main() -> int:
    parser = argparse.ArgumentParser(description="Renderiza BPMN 2.0 a SVG y PNG con bpmn-js fijado.")
    parser.add_argument("source", type=Path, help="Archivo .bpmn de entrada")
    parser.add_argument("--output", type=Path, required=True, help="Archivo SVG de salida")
    parser.add_argument("--png", type=Path, help="Archivo PNG de salida (opcional)")
    parser.add_argument("--escala", type=int, default=2, help="Escala del PNG (por defecto 2)")
    parser.add_argument("--sin-color", action="store_true", help="Sin la paleta de estilo Bizagi")
    parser.add_argument("--check", action="store_true",
                        help="Comprueba que el SVG vigente coincide, sin sobrescribirlo.")
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    if not source.is_file():
        parser.error(f"No existe la fuente: {source}")
    if source.suffix.lower() != ".bpmn":
        parser.error("La fuente debe tener extension .bpmn")
    try:
        svg = render_svg(source, color=not args.sin_color)
        if args.check:
            if not output.exists():
                print(f"DESACTUALIZADO: falta {output}", file=sys.stderr)
                return 1
            if output.read_bytes() != svg:
                print(f"DESACTUALIZADO: {output}", file=sys.stderr)
                return 1
            print(f"OK: {output}")
            return 0
        escribir(output, svg)
        print(f"GENERADO: {output}")
        if args.png:
            render_png(svg, args.png.resolve(), args.escala)
            print(f"GENERADO: {args.png.resolve()}")
        return 0
    except (OSError, RuntimeError, urllib.error.URLError, etree.XMLSyntaxError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
