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
from renderizar_plantuml import REPO_ROOT, download_verified, sha256

LOCK_PATH = Path(__file__).with_name("bpmn-js.lock.json")
BPMN = "http://www.omg.org/spec/BPMN/20100524/MODEL"
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
<script>__JS__</script>__EVENT_MARKERS__
<script>const c = document.createElement('div'); c.style.cssText = 'width:3000px;height:2000px';
document.body.appendChild(c); const v = new BpmnJS({container: c});
v.importXML(__X__).then(() => { __APPLY_EVENT_MARKERS__return v.saveSVG(); })
 .then(r => { document.getElementById('svg').textContent = r.svg; })
 .catch(e => { document.getElementById('svg').textContent = 'ERROR ' + e; });</script></body></html>"""


# bpmn-js 17 conserva correctamente la semantica de un subproceso de evento contraido, pero no dibuja en su
# esquina superior izquierda el evento que lo dispara. La figura 2.91 del manual BPMN exige ese marcador visual.
# Este posprocesador usa exclusivamente los glifos BPMN de mensaje, temporizador y condicion; no modifica el XML.
MARCADORES_SUBPROCESO_EVENTO = r"""
function crearSvg(nombre, atributos) {
  const nodo = document.createElementNS('http://www.w3.org/2000/svg', nombre);
  Object.entries(atributos || {}).forEach(([k, v]) => nodo.setAttribute(k, v));
  return nodo;
}
function trazoSvg(d, color, ancho) {
  return crearSvg('path', {
    d: d, fill: 'none', stroke: color, 'stroke-width': ancho || '1.5',
    'stroke-linecap': 'round', 'stroke-linejoin': 'round'
  });
}
function marcarSubprocesosEvento(visor) {
  const registro = visor.get('elementRegistry');
  registro.filter(elemento => {
    const bo = elemento.businessObject;
    return bo && bo.$type === 'bpmn:SubProcess' && bo.triggeredByEvent &&
      elemento.di && elemento.di.isExpanded === false;
  }).forEach(elemento => {
    const bo = elemento.businessObject;
    const inicio = (bo.flowElements || []).find(e => e.$type === 'bpmn:StartEvent');
    const definicion = inicio && (inicio.eventDefinitions || [])[0];
    const gfx = registro.getGraphics(elemento);
    const visual = gfx && gfx.querySelector('.djs-visual');
    if (!inicio || !definicion || !visual || visual.querySelector('[data-marker="event-subprocess-trigger"]')) return;

    const rectangulo = visual.querySelector('rect');
    const color = (rectangulo && (rectangulo.style.stroke || rectangulo.getAttribute('stroke'))) || '#03689A';
    const relleno = (rectangulo && (rectangulo.style.fill || rectangulo.getAttribute('fill'))) || '#FFFFFF';
    const grupo = crearSvg('g', {
      transform: 'translate(8 8) scale(0.62)',
      'data-marker': 'event-subprocess-trigger',
      'pointer-events': 'none'
    });
    grupo.appendChild(crearSvg('circle', {
      cx: '18', cy: '18', r: '16', fill: relleno, stroke: color, 'stroke-width': '2',
      'stroke-dasharray': inicio.isInterrupting === false ? '4 3' : 'none'
    }));

    if (definicion.$type === 'bpmn:MessageEventDefinition') {
      grupo.appendChild(trazoSvg(
        'M8.5 11.3 L8.5 23.9 L27.4 23.9 L27.4 11.3 Z M8.5 11.3 L18 16.7 L27.4 11.3', color, '1.5'
      ));
    } else if (definicion.$type === 'bpmn:TimerEventDefinition') {
      grupo.appendChild(crearSvg('circle', {
        cx: '18', cy: '18', r: '10.5', fill: 'none', stroke: color, 'stroke-width': '1.7'
      }));
      grupo.appendChild(trazoSvg('M18 18 L20.25 10.5 M18 18 L23.25 19.5', color, '1.7'));
      for (let angulo = 0; angulo < 360; angulo += 30) {
        grupo.appendChild(crearSvg('path', {
          d: 'M18 25.5 L18 27.5', transform: `rotate(${angulo} 18 18)`, fill: 'none',
          stroke: color, 'stroke-width': '1', 'stroke-linecap': 'round'
        }));
      }
    } else if (definicion.$type === 'bpmn:ConditionalEventDefinition') {
      grupo.appendChild(trazoSvg(
        'M10.5 8.5 L25 8.5 L25 26.5 L10.5 26.5 Z ' +
        'M12.5 11.5 L23 11.5 M12.5 14.5 L23 14.5 M12.5 17.5 L23 17.5 ' +
        'M12.5 20.5 L23 20.5 M12.5 23.5 L23 23.5', color, '1.2'
      ));
    } else {
      return;
    }
    visual.appendChild(grupo);
  });
}
"""


VISOR = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__T__</title>
<style>html,body{margin:0;height:100%;font:14px Arial,sans-serif;background:#fff}#c{height:calc(100% - 34px)}
header{padding:8px 12px;border-bottom:1px solid #ddd}.bjs-drilldown{display:none}</style></head>
<body><header>__T__ · vista local con bpmn-js (rueda: zoom; arrastrar: mover)</header><div id="c"></div>
<script>__JS__</script>__EVENT_MARKERS__
<script>const xml = __X__; const v = new BpmnJS({container: '#c'});
v.importXML(xml).then(r => { __APPLY_EVENT_MARKERS__window.listo = true; window.avisos = r.warnings.length;
  v.get('canvas').zoom('fit-viewport'); })
 .catch(e => { document.body.insertAdjacentHTML('beforeend', '<pre>' + e + '</pre>'); window.listo = true; });</script>
</body></html>
"""


VISOR_ENLAZADO = """<!doctype html>
<!-- GENERADO - NO EDITAR. Fuente: __F__; bpmn-js fijado por el proyecto. -->
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>__T__</title>
<style>html,body{margin:0;height:100%;font:14px Arial,sans-serif;background:#fff}#c{height:calc(100% - 34px)}
header{padding:8px 12px;border-bottom:1px solid #ddd}.bjs-drilldown{display:none}</style></head>
<body><header>__T__ · vista interactiva (rueda: zoom; arrastrar: mover)</header><div id="c"></div>
<script src="__JS__"></script>__EVENT_MARKERS__
<script>const xml = __X__; const v = new BpmnJS({container: '#c'});
v.importXML(xml).then(r => { __APPLY_EVENT_MARKERS__window.listo = true; window.avisos = r.warnings.length;
  v.get('canvas').zoom('fit-viewport'); })
 .catch(e => { document.body.insertAdjacentHTML('beforeend', '<pre>' + e + '</pre>'); window.listo = true; });</script>
</body></html>
"""


def pagina_visor_enlazada(nombre: str, bpmn: Path, destino: Path) -> str:
    """Vista interactiva versionable: lleva solo el diagrama y enlaza la copia versionada de bpmn-js por ruta
    relativa, de modo que funciona sin internet desde que se clona el repositorio."""
    datos = bpmn.read_bytes()
    usa_marcadores = subprocesos_evento_contraidos(datos) > 0
    js = os.path.relpath(biblioteca(), destino.parent).replace(os.sep, "/")
    pagina = VISOR_ENLAZADO.replace("__T__", html.escape(nombre)).replace("__F__", html.escape(bpmn.name))
    pagina = pagina.replace("__X__", json.dumps(colorear(datos)))
    pagina = pagina.replace(
        "__EVENT_MARKERS__", f"\n<script>{MARCADORES_SUBPROCESO_EVENTO}</script>" if usa_marcadores else ""
    ).replace("__APPLY_EVENT_MARKERS__", "marcarSubprocesosEvento(v); " if usa_marcadores else "")
    return pagina.replace("__JS__", html.escape(js))


def pagina_visor(nombre: str, xml: str) -> str:
    """Vista HTML autonoma: bpmn-js local fijado, colores de estilo Bizagi, zoom y desplazamiento."""
    datos = xml.encode("utf-8")
    usa_marcadores = subprocesos_evento_contraidos(datos) > 0
    pagina = VISOR.replace("__T__", html.escape(nombre)).replace("__X__", json.dumps(colorear(datos)))
    pagina = pagina.replace(
        "__EVENT_MARKERS__", f"\n<script>{MARCADORES_SUBPROCESO_EVENTO}</script>" if usa_marcadores else ""
    ).replace("__APPLY_EVENT_MARKERS__", "marcarSubprocesosEvento(v); " if usa_marcadores else "")
    return pagina.replace("__JS__", biblioteca().read_text(encoding="utf-8"))


def load_lock() -> dict[str, object]:
    data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    if not {"version", "artifacts"} <= set(data):
        raise RuntimeError(f"Faltan campos en {LOCK_PATH}")
    return data


def biblioteca() -> Path:
    """Ruta de bpmn-js: la copia versionada en vendor/ (verificada por hash) o, si falta, la del cache descargado."""
    artifact = load_lock()["artifacts"]["navigated_viewer"]
    versionada = REPO_ROOT / artifact.get("vendor_path", "")
    if artifact.get("vendor_path") and versionada.is_file():
        if sha256(versionada) != artifact["sha256"].lower():
            raise RuntimeError(f"La copia versionada de bpmn-js no coincide con el hash fijado: {versionada}")
        return versionada
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


def subprocesos_evento_contraidos(xml: bytes) -> int:
    """Cuenta los subprocesos de evento cuya representacion DI exige el marcador del evento de inicio."""
    raiz = etree.fromstring(xml)
    formas = {
        forma.get("bpmnElement"): forma.get("isExpanded")
        for forma in raiz.iter(f"{{{BDI}}}BPMNShape")
    }
    return sum(
        1 for subproceso in raiz.iter(f"{{{BPMN}}}subProcess")
        if subproceso.get("triggeredByEvent") == "true" and formas.get(subproceso.get("id")) == "false"
    )


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
    esperados = subprocesos_evento_contraidos(xml)
    contenido = colorear(xml) if color else xml.decode("utf-8")
    pagina = PAGINA.replace("__JS__", biblioteca().read_text(encoding="utf-8")).replace(
        "__X__", json.dumps(contenido)
    )
    pagina = pagina.replace(
        "__EVENT_MARKERS__", f"\n<script>{MARCADORES_SUBPROCESO_EVENTO}</script>" if esperados else ""
    ).replace("__APPLY_EVENT_MARKERS__", "marcarSubprocesosEvento(v); " if esperados else "")
    with tempfile.TemporaryDirectory() as tmp:
        ruta = Path(tmp) / "render.html"
        ruta.write_text(pagina, encoding="utf-8")
        resultado = ejecutar(["--virtual-time-budget=20000", "--dump-dom", ruta.as_uri()])
    encontrado = re.search(r'<pre id="svg">(.*?)</pre>', resultado.stdout, re.DOTALL)
    svg = html.unescape(encontrado.group(1)) if encontrado else ""
    if "<svg" not in svg[:400]:
        raise RuntimeError(f"bpmn-js no produjo un SVG para {source}: {svg[:300] or resultado.stderr[-400:]}")
    dibujados = svg.count('data-marker="event-subprocess-trigger"')
    if dibujados != esperados:
        raise RuntimeError(
            f"Marcadores de subproceso de evento incompletos en {source}: {dibujados} de {esperados}."
        )
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
    parser.add_argument("--html", type=Path, help="Vista interactiva HTML de salida (opcional)")
    parser.add_argument("--titulo", default="", help="Titulo de la vista interactiva (por defecto, el del archivo)")
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
        if args.html:
            destino = args.html.resolve()
            pagina = pagina_visor_enlazada(args.titulo or source.stem, source, destino)
            escribir(destino, pagina.encode("utf-8"))
            print(f"GENERADO: {destino}")
        return 0
    except (OSError, RuntimeError, urllib.error.URLError, etree.XMLSyntaxError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
