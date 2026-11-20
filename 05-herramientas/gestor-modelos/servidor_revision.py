"""Servidor local del visor BPMN y de observaciones persistentes.

Uso: python servidor_revision.py [--puerto 8765]
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import threading
import uuid
from datetime import datetime, timezone
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, quote, urlparse
from xml.etree import ElementTree


RAIZ = Path(__file__).resolve().parents[2]
BLOQUEO = threading.Lock()


def modelo_valido(nombre: str) -> Path:
    if not isinstance(nombre, str) or not nombre.endswith("-diagrama-proceso.html"):
        raise ValueError("Modelo inválido")
    ruta = (RAIZ / nombre).resolve()
    if not ruta.is_relative_to((RAIZ / "02-procesos").resolve()) or not ruta.is_file():
        raise ValueError("Modelo fuera de 02-procesos o inexistente")
    return ruta


def archivo_observaciones(modelo: Path) -> Path:
    return modelo.with_name(modelo.name.replace("-diagrama-proceso.html", "-observaciones.json"))


def leer(modelo: Path) -> dict:
    ruta = archivo_observaciones(modelo)
    if not ruta.exists():
        return {"modelo": modelo.relative_to(RAIZ.resolve()).as_posix(), "observaciones": []}
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    if not isinstance(datos, dict) or not isinstance(datos.get("observaciones"), list):
        raise ValueError("Archivo de observaciones inválido")
    return datos


def guardar(modelo: Path, datos: dict) -> None:
    ruta = archivo_observaciones(modelo)
    temporal = ruta.with_name(ruta.name + f".{uuid.uuid4().hex}.tmp")
    try:
        temporal.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporal, ruta)
    finally:
        temporal.unlink(missing_ok=True)


def elemento_valido(modelo: Path, elemento: str) -> bool:
    if elemento == "":
        return True
    bpmn = modelo.with_suffix(".bpmn")
    if not bpmn.is_file():
        return False
    try:
        return any(n.get("id") == elemento for n in ElementTree.parse(bpmn).iter())
    except ElementTree.ParseError:
        return False


def arbol_procesos() -> dict:
    """Indice de carpetas; los niveles sin BPMN siguen siendo navegables."""
    base = RAIZ / "02-procesos"
    def nodo(carpeta: Path) -> dict:
        identidad = re.match(r"^(S\d+(?:-\d+)*)-(.+)$", carpeta.name)
        codigo = identidad.group(1).replace("-", ".") if identidad else ""
        indice = next(iter(sorted(carpeta.glob("00-*.md"))), None)
        modelo = next(iter(sorted(carpeta.glob("*-diagrama-proceso.html"))), None)
        hijos = [nodo(p) for p in sorted(carpeta.iterdir()) if p.is_dir()
                 and p.name != "to-be" and not p.name.startswith(("modelos-", "."))]
        return {
            "codigo": codigo,
            "nombre": (identidad.group(2) if identidad else carpeta.name).replace("-", " ").capitalize(),
            "indice": "/" + indice.relative_to(RAIZ).as_posix() if indice else "",
            "modelo": "/" + modelo.relative_to(RAIZ).as_posix() if modelo else "",
            "hijos": hijos,
        }
    mapa = base / "mapa-de-procesos-institucional"
    return {
        "codigo": "Nivel 0", "nombre": "Mapa de procesos institucional",
        "indice": "/" + (mapa / "mapa-procesos-nivel-0.md").relative_to(RAIZ).as_posix(),
        "modelo": "", "hijos": [
            nodo(p) for p in sorted(base.iterdir()) if p.is_dir() and p.name.startswith(("S1-", "S2-", "S3-", "S4-"))
        ],
    }


def html_arbol(nodo: dict) -> str:
    titulo = html.escape(f'{nodo["codigo"]} · {nodo["nombre"]}')
    enlace = nodo["modelo"] or nodo["indice"]
    etiqueta = f'<a href="{quote(enlace, safe="/")}">{titulo}</a>' if enlace else titulo
    hijos = "".join(html_arbol(h) for h in nodo["hijos"])
    if hijos:
        detalle = f'<a href="{quote(enlace, safe="/")}">{"Abrir diagrama" if nodo["modelo"] else "Abrir índice"}</a>' if enlace else ""
        abierto = " open" if nodo["codigo"] == "Nivel 0" else ""
        return f'<li><details{abierto}><summary>{titulo}</summary>{detalle}<ul>{hijos}</ul></details></li>'
    return f'<li>{etiqueta}</li>'


def fuente_valida(ruta: str) -> Path:
    if not isinstance(ruta, str) or not ruta.startswith(("01-referencias/", "02-procesos/", "03-conocimiento/")):
        raise ValueError("Ruta de fuente no permitida")
    archivo = (RAIZ / ruta).resolve()
    if (not archivo.is_relative_to(RAIZ.resolve()) or not archivo.is_file()
        or archivo.suffix.lower() not in {".md", ".txt", ".html"}):
        raise ValueError("Fuente de texto inexistente o no permitida")
    if ruta.startswith("02-procesos/") and archivo.suffix.lower() != ".md":
        raise ValueError("Solo se admiten notas Markdown de procesos")
    return archivo


def vista_markdown(archivo: Path, contenido: str, fragmento: str) -> bytes:
    """Visor local: Markdown con HTML de origen deshabilitado y metadatos plegados."""
    cabecera = re.match(r"\A---\n(.*?)\n---\n?", contenido, re.DOTALL)
    metadatos = cabecera.group(1) if cabecera else ""
    if cabecera:
        contenido = contenido[cabecera.end():]
    ruta = archivo.relative_to(RAIZ.resolve()).as_posix()
    datos = json.dumps({"texto": contenido, "fragmento": fragmento, "ruta": ruta}, ensure_ascii=False).replace("<", "\\u003c")
    detalle = (f'<details class="metadatos"><summary>Metadatos del documento</summary>'
               f'<pre>{html.escape(metadatos)}</pre></details>') if metadatos else ""
    pagina = f'''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(archivo.name)}</title>
<style>
html{{scroll-behavior:smooth}}body{{margin:0;color:#203044;background:#fff;font:15px/1.6 system-ui,Arial,sans-serif}}
main{{max-width:1100px;margin:auto;padding:20px 28px 60px}}.archivo{{font-size:12px;color:#667789;margin-bottom:14px}}
h1,h2,h3{{line-height:1.25;scroll-margin-top:20px}}h1{{font-size:25px}}h2{{font-size:20px;border-bottom:1px solid #dce4eb;padding-bottom:5px;margin-top:32px}}h3{{font-size:17px;margin-top:24px}}
p,li{{max-width:90ch}}a{{color:#08659c}}a:hover{{text-decoration:underline}}
table{{display:block;max-width:100%;overflow-x:auto;border-collapse:collapse;margin:18px 0;font-size:13px}}
th,td{{border:1px solid #d3dde5;padding:7px 10px;text-align:left;vertical-align:top;min-width:90px}}
th{{background:#eef3f8;white-space:nowrap}}tr:nth-child(even) td{{background:#f8fafc}}
blockquote{{border-left:4px solid #9cbad0;margin:16px 0;padding:2px 16px;background:#f5f8fa}}
pre{{overflow-x:auto;background:#f3f6f8;padding:12px;border-radius:5px}}code{{background:#f1f4f6;padding:1px 3px;border-radius:3px}}
pre code{{background:none;padding:0}}hr{{border:0;border-top:1px solid #dce4eb;margin:26px 0}}
.metadatos{{margin:0 0 20px;border:1px solid #dce4eb;border-radius:6px;padding:7px 12px;color:#526579}}
.metadatos summary{{cursor:pointer}}.metadatos pre{{font-size:12px;white-space:pre-wrap}}
#estado-fragmento{{color:#657789;font-size:12px}}mark{{background:#ffe17d;outline:2px solid #e2aa22}}
#indice{{border:1px solid #dce4eb;border-radius:6px;padding:8px 14px;margin:16px 0;background:#f8fafc}}
#indice summary{{cursor:pointer;font-weight:600}}#indice ul{{columns:2;padding-left:20px;margin:8px 0}}#indice li{{break-inside:avoid;font-size:13px}}
@media(max-width:700px){{main{{padding:14px}}#indice ul{{columns:1}}}}
</style></head><body><main><div class="archivo">{html.escape(archivo.name)}</div>{detalle}
<p id="estado-fragmento"></p><details id="indice"><summary>Secciones del documento</summary><ul></ul></details>
<article id="contenido"></article></main>
<script type="application/json" id="datos-md">{datos}</script>
<script src="/05-herramientas/gestor-modelos/vendor/markdown-it.umd.min.js"></script>
<script>
const datos = JSON.parse(document.getElementById('datos-md').textContent);
const md = window.markdownit({{html:false,linkify:true}});
const contenido = document.getElementById('contenido');
contenido.innerHTML = md.render(datos.texto);
const indice = document.querySelector('#indice ul');
const identificadores = new Set();
for (const [i, titulo] of [...contenido.querySelectorAll('h1,h2,h3')].entries()) {{
  const base = titulo.textContent.toLocaleLowerCase('es').normalize('NFD')
    .replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'') || 'seccion-' + i;
  let id = base, n = 2;
  while (identificadores.has(id)) id = base + '-' + n++;
  identificadores.add(id); titulo.id = id;
  const li = document.createElement('li'), a = document.createElement('a');
  a.href = '#' + titulo.id; a.textContent = titulo.textContent;
  li.append(a); indice.append(li);
}}
if (!indice.children.length) document.getElementById('indice').hidden = true;
for (const a of contenido.querySelectorAll('a[href]')) {{
  const href = a.getAttribute('href');
  if (href.startsWith('#')) continue;
  const destino = new URL(href, new URL('/' + datos.ruta, location.origin));
  if (destino.origin === location.origin && destino.pathname.toLowerCase().endsWith('.md')) {{
    a.href = '/ver-fuente?ruta=' + encodeURIComponent(decodeURIComponent(destino.pathname.slice(1))) + destino.hash;
  }} else {{ a.href = destino.href; a.target = '_blank'; a.rel = 'noopener'; }}
}}
const estado = document.getElementById('estado-fragmento');
if (datos.fragmento) {{
  const walker = document.createTreeWalker(contenido, NodeFilter.SHOW_TEXT);
  let nodo, encontrado = null;
  while ((nodo = walker.nextNode())) {{
    const pos = nodo.data.toLocaleLowerCase('es').indexOf(datos.fragmento.toLocaleLowerCase('es'));
    if (pos >= 0) {{
      const rango = document.createRange(); rango.setStart(nodo,pos); rango.setEnd(nodo,pos+datos.fragmento.length);
      encontrado = document.createElement('mark'); rango.surroundContents(encontrado); break;
    }}
  }}
  estado.textContent = encontrado ? 'Fragmento resaltado en el documento.' : 'No se encontro el fragmento registrado.';
  if (encontrado) requestAnimationFrame(() => encontrado.scrollIntoView({{block:'center'}}));
}} else {{ estado.hidden = true; }}
</script></body></html>'''
    return pagina.encode("utf-8")


class Manejador(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(RAIZ), **kwargs)

    def _json(self, codigo: int, datos: dict) -> None:
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(cuerpo)

    def _cuerpo(self) -> dict:
        longitud = int(self.headers.get("Content-Length", "0"))
        if not 0 < longitud <= 16384:
            raise ValueError("Tamaño de solicitud inválido")
        datos = json.loads(self.rfile.read(longitud))
        if not isinstance(datos, dict):
            raise ValueError("Se requiere un objeto JSON")
        return datos

    def _origen_valido(self) -> bool:
        origen = self.headers.get("Origin")
        if not origen:
            return True
        parsed = urlparse(origen)
        return parsed.scheme == "http" and parsed.netloc in {
            f"127.0.0.1:{self.server.server_port}", f"localhost:{self.server.server_port}"
        }

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/ver-fuente":
            try:
                parametros = parse_qs(parsed.query)
                archivo = fuente_valida(parametros.get("ruta", [""])[0])
                fragmento = parametros.get("fragmento", [""])[0][:500]
                contenido = archivo.read_text(encoding="utf-8")
                if archivo.suffix.lower() == ".md":
                    cuerpo = vista_markdown(archivo, contenido, fragmento)
                else:
                    if fragmento:
                        posicion = contenido.casefold().find(fragmento.casefold())
                        if posicion >= 0:
                            texto = (html.escape(contenido[:posicion]) + "<mark id='pasaje'>"
                                     + html.escape(contenido[posicion:posicion + len(fragmento)]) + "</mark>"
                                     + html.escape(contenido[posicion + len(fragmento):]))
                        else:
                            texto = html.escape(contenido)
                    else:
                        texto = html.escape(contenido)
                    cuerpo = (f'<!doctype html><html lang="es"><meta charset="utf-8">'
                              f'<style>body{{font:15px/1.5 system-ui;margin:24px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}'
                              f'mark{{background:#ffe087}}</style><h1>{html.escape(archivo.name)}</h1>'
                              f'<p>Fragmento {"resaltado" if fragmento and "<mark" in texto else "sin localizar o no registrado"}.</p>'
                              f'<pre>{texto}</pre><script>document.getElementById("pasaje")?.scrollIntoView()</script></html>').encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(cuerpo)))
                self.end_headers()
                self.wfile.write(cuerpo)
            except (ValueError, OSError, UnicodeError) as exc:
                self._json(400, {"error": str(exc)})
            return
        if parsed.path == "/":
            enlaces = html_arbol(arbol_procesos())
            cuerpo = ('<!doctype html><html lang="es"><meta charset="utf-8">'
                      '<title>Visor de procesos</title><body style="font:16px system-ui;max-width:900px;margin:40px auto">'
                      '<h1>Mapa de procesos institucional · Nivel 0</h1><p>Selecciona una rama o un diagrama para revisar su sustento y observaciones.</p>'
                      f'<ul>{enlaces}</ul></body></html>').encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(cuerpo)))
            self.end_headers()
            self.wfile.write(cuerpo)
            return
        if parsed.path == "/api/arbol":
            self._json(200, arbol_procesos())
            return
        if parsed.path != "/api/observaciones":
            if parsed.path.startswith("/api/"):
                self._json(404, {"error": "Ruta no encontrada"})
                return
            return super().do_GET()
        try:
            modelo = modelo_valido(parse_qs(parsed.query).get("modelo", [""])[0])
            with BLOQUEO:
                self._json(200, leer(modelo))
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            self._json(400, {"error": str(exc)})

    def do_POST(self) -> None:
        if self.path != "/api/observaciones":
            self._json(404, {"error": "Ruta no encontrada"})
            return
        if not self._origen_valido():
            self._json(403, {"error": "Origen no autorizado"})
            return
        try:
            entrada = self._cuerpo()
            modelo = modelo_valido(entrada.get("modelo", ""))
            elemento = entrada.get("elemento", "")
            texto = entrada.get("texto", "")
            autor = entrada.get("autor", "Equipo")
            if not isinstance(elemento, str) or not elemento_valido(modelo, elemento):
                raise ValueError("Elemento BPMN inválido")
            if not isinstance(texto, str) or not 1 <= len(texto.strip()) <= 4000:
                raise ValueError("La observación debe tener entre 1 y 4000 caracteres")
            if not isinstance(autor, str) or len(autor) > 100:
                raise ValueError("Autor inválido")
            with BLOQUEO:
                datos = leer(modelo)
                observacion = {
                    "id": str(uuid.uuid4()), "elemento": elemento,
                    "referencia": str(entrada.get("referencia", ""))[:100],
                    "texto": texto.strip(), "autor": autor.strip() or "Equipo",
                    "estado": "ABIERTA", "fecha": datetime.now(timezone.utc).isoformat()
                }
                datos["observaciones"].append(observacion)
                guardar(modelo, datos)
            self._json(201, observacion)
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            self._json(400, {"error": str(exc)})

    def do_PATCH(self) -> None:
        if self.path != "/api/observaciones":
            self._json(404, {"error": "Ruta no encontrada"})
            return
        if not self._origen_valido():
            self._json(403, {"error": "Origen no autorizado"})
            return
        try:
            entrada = self._cuerpo()
            modelo = modelo_valido(entrada.get("modelo", ""))
            if entrada.get("estado") not in {"ABIERTA", "RESUELTA"}:
                raise ValueError("Estado inválido")
            with BLOQUEO:
                datos = leer(modelo)
                observacion = next((o for o in datos["observaciones"] if o.get("id") == entrada.get("id")), None)
                if observacion is None:
                    raise ValueError("Observación no encontrada")
                observacion["estado"] = entrada["estado"]
                observacion["actualizada"] = datetime.now(timezone.utc).isoformat()
                guardar(modelo, datos)
            self._json(200, observacion)
        except (ValueError, OSError, json.JSONDecodeError) as exc:
            self._json(400, {"error": str(exc)})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--puerto", type=int, default=8765)
    args = parser.parse_args()
    servidor = ThreadingHTTPServer(("127.0.0.1", args.puerto), Manejador)
    print(f"Visor local: http://127.0.0.1:{args.puerto}/", flush=True)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        servidor.server_close()


if __name__ == "__main__":
    main()
