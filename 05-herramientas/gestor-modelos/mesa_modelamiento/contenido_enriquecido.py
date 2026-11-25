"""Saneamiento del HTML de observaciones y respuestas con una lista blanca de etiquetas sin atributos.

El HTML se guarda ya saneado para que cualquier lector (visor Nuxt, visor estático, CLI o MCP) reciba
contenido seguro. Solo se conservan formatos de texto: títulos, párrafos, énfasis, tachado y listas.
"""

from __future__ import annotations

from html import escape
from html.parser import HTMLParser

ETIQUETAS = {"h3", "h4", "p", "br", "strong", "b", "em", "i", "u", "s", "del", "ul", "ol", "li", "blockquote"}
SIN_CIERRE = {"br"}
CIERRE_IMPLICITO = {"li", "p"}
DESCARTAR_CONTENIDO = {"script", "style", "template", "iframe", "object", "noscript", "svg", "math"}
EQUIVALENTES = {"strike": "s", "h1": "h3", "h2": "h3", "h5": "h4", "h6": "h4", "div": "p"}
MAXIMO_HTML = 20000


class _Saneador(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.salida: list[str] = []
        self.abiertas: list[str] = []
        self.descartando = 0
        self.texto_visible: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if tag in DESCARTAR_CONTENIDO:
            self.descartando += 1
            return
        tag = EQUIVALENTES.get(tag, tag)
        if self.descartando or tag not in ETIQUETAS:
            return
        if tag in CIERRE_IMPLICITO and self.abiertas and self.abiertas[-1] == tag:
            self.salida.append(f"</{self.abiertas.pop()}>")  # <li> y <p> sin cierre, como en el navegador.
        self.salida.append(f"<{tag}>")
        if tag not in SIN_CIERRE:
            self.abiertas.append(tag)

    def handle_startendtag(self, tag: str, attrs) -> None:  # noqa: ANN001
        if not self.descartando and EQUIVALENTES.get(tag, tag) in SIN_CIERRE:
            self.salida.append("<br>")

    def handle_endtag(self, tag: str) -> None:
        if tag in DESCARTAR_CONTENIDO:
            self.descartando = max(0, self.descartando - 1)
            return
        tag = EQUIVALENTES.get(tag, tag)
        if self.descartando or tag not in self.abiertas:
            return
        while self.abiertas:  # Cierra también las etiquetas mal anidadas que quedaron dentro.
            abierta = self.abiertas.pop()
            self.salida.append(f"</{abierta}>")
            if abierta == tag:
                break

    def handle_data(self, data: str) -> None:
        if not self.descartando:
            self.salida.append(escape(data, quote=False))
            self.texto_visible.append(data)

    def resultado(self) -> tuple[str, str]:
        self.salida.extend(f"</{t}>" for t in reversed(self.abiertas))
        return "".join(self.salida).strip(), " ".join("".join(self.texto_visible).split())


def sanear_html(contenido: str) -> tuple[str, str]:
    """Devuelve el HTML saneado y su texto visible normalizado."""
    saneador = _Saneador()
    saneador.feed(contenido)
    saneador.close()
    return saneador.resultado()
