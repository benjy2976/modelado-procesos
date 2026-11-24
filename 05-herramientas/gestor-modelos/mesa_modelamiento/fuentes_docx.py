"""Conversión de DOCX a Markdown con anclas de párrafo y numeración automática reconstruida.

Un DOCX no tiene páginas fijas: el ancla estable es el número de párrafo del cuerpo. La numeración
automática de Word no está en el texto, por eso se recalcula desde ``numbering.xml`` y ``styles.xml``.
"""

from __future__ import annotations

import io
import re
import zipfile
from dataclasses import dataclass, field
from html import escape
from xml.etree import ElementTree as ET

from .fuentes_numeracion import Estilos, Numeracion, W, valor

MC_FALLBACK = "{http://schemas.openxmlformats.org/markup-compatibility/2006}Fallback"
# Texto eliminado con control de cambios, instrucciones de campo y la copia de compatibilidad
# de los objetos alternativos no forman parte del texto visible.
OMITIDOS = {W + "del", W + "moveFrom", W + "instrText", W + "delText", W + "pPr", W + "rPr", MC_FALLBACK}
SECCION = re.compile(r"(SECCI[ÓO]N|CAP[ÍI]TULO|ANEXO|PARTE)\b")
NUMERAL_ESCRITO = re.compile(r"(\d+(?:\.\d+)*\.\d*|\d+(?:\.\d+)+)\s")


@dataclass
class _Estado:
    con_paginas: bool
    pagina: int = 1
    parrafos: int = 0
    tablas: int = 0
    salto: bool = False
    notas: list[str] = field(default_factory=list)
    seccion: list[str] = field(default_factory=list)
    resumen: dict = field(
        default_factory=lambda: {"numerales_reconstruidos": 0, "vinetas": 0, "saltos_pagina": 0, "secciones": 0}
    )


def _limpio(texto: str) -> str:
    return texto.replace("-->", "- ->").replace(";", ",").replace("\n", " ").strip()[:120]


def _texto(elemento: ET.Element, estado: _Estado, contar_paginas: bool = True) -> str:
    partes: list[str] = []

    def recorrer(nodo: ET.Element) -> None:
        etiqueta = nodo.tag
        if etiqueta in OMITIDOS:
            return
        if etiqueta == W + "t":
            partes.append(nodo.text or "")
        elif etiqueta == W + "tab":
            partes.append("\t")
        elif etiqueta in (W + "br", W + "cr"):
            if nodo.get(W + "type") == "page":
                estado.salto = True
                partes.append(" ")
            else:
                partes.append("\n")
        elif etiqueta == W + "noBreakHyphen":
            partes.append("-")
        elif etiqueta == W + "lastRenderedPageBreak" and contar_paginas:
            estado.pagina += 1
        elif etiqueta == W + "footnoteReference":
            identificador = nodo.get(W + "id", "")
            partes.append(f"[^{identificador}]")
            if identificador not in estado.notas:
                estado.notas.append(identificador)
        for hijo in nodo:
            recorrer(hijo)

    recorrer(elemento)
    return re.sub(r"[ \t]+\n", "\n", "".join(partes)).strip()


def _bloques(contenedor: ET.Element):
    for hijo in contenedor:
        if hijo.tag in (W + "p", W + "tbl", W + "tc"):
            yield hijo
        elif hijo.tag == W + "sdt":
            contenido = hijo.find(W + "sdtContent")
            if contenido is not None:
                yield from _bloques(contenido)
        elif hijo.tag == W + "customXml":
            yield from _bloques(hijo)


def _numerar(parrafo: ET.Element, estilos: Estilos, numeracion: Numeracion, estado: _Estado) -> tuple[str, str]:
    """Devuelve el prefijo Markdown y el numeral reconstruido de un párrafo."""
    ppr = parrafo.find(W + "pPr")
    estilo = valor(ppr, W + "pStyle") or estilos.defecto
    numpr = ppr.find(W + "numPr") if ppr is not None else None
    num_id = valor(numpr, W + "numId")
    nivel = valor(numpr, W + "ilvl")
    if num_id is None and estilo:
        num_id, nivel_estilo = estilos.numeracion(estilo)
        nivel = nivel if nivel is not None else nivel_estilo
    resultado = numeracion.siguiente(num_id, nivel, estilo)
    if resultado is None:
        return "", ""
    texto, vineta = resultado
    if vineta:
        estado.resumen["vinetas"] += 1
        return "- ", ""
    if not texto:
        return "", ""
    estado.resumen["numerales_reconstruidos"] += 1
    return f"{texto} ", texto


def _parrafo(parrafo: ET.Element, estilos: Estilos, numeracion: Numeracion, estado: _Estado) -> str:
    estado.parrafos += 1
    pagina = estado.pagina
    ppr = parrafo.find(W + "pPr")
    estado.salto = ppr is not None and ppr.find(W + "pageBreakBefore") is not None
    prefijo, numeral = _numerar(parrafo, estilos, numeracion, estado)
    texto = _texto(parrafo, estado)
    salto = estado.salto
    if salto:
        estado.resumen["saltos_pagina"] += 1
    if not texto:
        return "<!-- salto_pagina -->\n" if salto else ""
    titulo = estilos.nivel_titulo(valor(ppr, W + "pStyle") or estilos.defecto)
    if titulo is not None:
        estado.seccion = estado.seccion[:titulo] + [_limpio(numeral + " " + texto)]
        estado.resumen["secciones"] += 1
    elif SECCION.match(texto) and texto.isupper():
        estado.seccion = [_limpio(texto)]
        estado.resumen["secciones"] += 1
    campos = [f"parrafo: {estado.parrafos}"]
    if estado.con_paginas:
        campos.append(f"pagina_word_aprox: {pagina}")
    if numeral:
        campos.append(f"numeral: {_limpio(numeral)}")
    escrito = NUMERAL_ESCRITO.match(texto)
    if escrito:
        campos.append(f"numeral_texto: {escrito.group(1)}")
    if estado.seccion:
        campos.append(f"seccion: {' > '.join(estado.seccion)}")
    marca = "#" * min(titulo + 1, 6) + " " if titulo is not None else ""
    previo = "<!-- salto_pagina -->\n" if salto else ""
    return f"{previo}<!-- {'; '.join(campos)} -->\n{marca}{prefijo}{texto}\n"


def _celda(celda: ET.Element, estilos: Estilos, numeracion: Numeracion, estado: _Estado) -> str:
    partes = []
    for bloque in _bloques(celda):
        if bloque.tag == W + "p":
            prefijo, _ = _numerar(bloque, estilos, numeracion, estado)
            texto = _texto(bloque, estado)
            if texto:
                partes.append(escape(prefijo + texto).replace("\n", "<br>"))
        elif bloque.tag == W + "tbl":
            for fila in bloque.iter(W + "tr"):
                textos = [_texto(c, estado) for c in fila.iter(W + "tc")]
                partes.append(escape(" | ".join(t for t in textos if t)))
    return "<br>".join(partes)


def _tabla(tabla: ET.Element, estilos: Estilos, numeracion: Numeracion, estado: _Estado) -> str:
    estado.tablas += 1
    inicio = f"tabla: {estado.tablas}; tras_parrafo: {estado.parrafos}"
    if estado.con_paginas:
        inicio += f"; pagina_word_aprox: {estado.pagina}"
    if estado.seccion:
        inicio += f"; seccion: {' > '.join(estado.seccion)}"
    filas: list[list[dict]] = []
    abiertas: dict[int, dict] = {}
    for fila in tabla.findall(W + "tr"):
        trpr = fila.find(W + "trPr")
        encabezado = trpr is not None and trpr.find(W + "tblHeader") is not None
        columna = int(valor(trpr, W + "gridBefore") or 0)
        celdas: list[dict] = []
        for celda in _bloques(fila):
            if celda.tag != W + "tc":
                continue
            tcpr = celda.find(W + "tcPr")
            ancho = int(valor(tcpr, W + "gridSpan") or 1)
            fusion = tcpr.find(W + "vMerge") if tcpr is not None else None
            if fusion is not None and fusion.get(W + "val") != "restart" and columna in abiertas:
                abiertas[columna]["filas"] += 1
                columna += ancho
                continue
            dato = {"texto": _celda(celda, estilos, numeracion, estado), "columnas": ancho, "filas": 1}
            dato["etiqueta"] = "th" if encabezado else "td"
            if fusion is not None:
                abiertas[columna] = dato
            else:
                abiertas.pop(columna, None)
            celdas.append(dato)
            columna += ancho
        filas.append(celdas)
    lineas = [f"<!-- {inicio} -->", "<table>"]
    for celdas in filas:
        html = ""
        for c in celdas:
            atributos = (f' colspan="{c["columnas"]}"' if c["columnas"] > 1 else "") + (
                f' rowspan="{c["filas"]}"' if c["filas"] > 1 else ""
            )
            html += f"<{c['etiqueta']}{atributos}>{c['texto']}</{c['etiqueta']}>"
        lineas.append(f"<tr>{html}</tr>")
    lineas.append("</table>")
    return "\n".join(lineas) + "\n"


def _notas(xml: bytes | None, referencias: list[str], estado: _Estado) -> list[str]:
    if not xml or not referencias:
        return []
    textos = {
        nota.get(W + "id", ""): _texto(nota, estado, contar_paginas=False)
        for nota in ET.fromstring(xml).findall(W + "footnote")
    }
    return [f"[^{i}]: {textos.get(i, '').replace(chr(10), ' ')}" for i in referencias]


def convertir_docx(datos: bytes) -> tuple[str, dict]:
    """Convierte un DOCX; devuelve el cuerpo Markdown y un resumen verificable."""
    with zipfile.ZipFile(io.BytesIO(datos)) as paquete:
        partes = {n: paquete.read(n) for n in paquete.namelist() if n.startswith("word/") and n.endswith(".xml")}
    documento = partes["word/document.xml"]
    estilos = Estilos(partes.get("word/styles.xml"))
    numeracion = Numeracion(partes.get("word/numbering.xml"), estilos)
    estado = _Estado(con_paginas=b"lastRenderedPageBreak" in documento)
    cuerpo = ET.fromstring(documento).find(W + "body")
    bloques = []
    for bloque in _bloques(cuerpo):
        if bloque.tag == W + "p":
            bloques.append(_parrafo(bloque, estilos, numeracion, estado))
        elif bloque.tag == W + "tbl":
            bloques.append(_tabla(bloque, estilos, numeracion, estado))
    notas = _notas(partes.get("word/footnotes.xml"), estado.notas, estado)
    texto = "\n".join(b for b in bloques if b)
    if notas:
        texto += "\n<!-- notas_pie -->\n\n" + "\n".join(notas) + "\n"
    resumen = {
        "parrafos": estado.parrafos,
        "parrafos_con_texto": texto.count("<!-- parrafo: "),
        "tablas": estado.tablas,
        "notas_pie": len(notas),
        "paginas_word_aprox": estado.pagina if estado.con_paginas else None,
        **estado.resumen,
    }
    return texto, resumen
