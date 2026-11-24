"""Texto de PPTX por diapositiva y ficha de inventario de XLSX, sin convertir hojas a Markdown."""

from __future__ import annotations

import io
import posixpath
import zipfile
from xml.etree import ElementTree as ET

P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
REL = "{http://schemas.openxmlformats.org/package/2006/relationships}"
MAX_ENCABEZADOS = 12


def _relaciones(paquete: zipfile.ZipFile, parte: str) -> dict[str, tuple[str, str]]:
    """Relaciones de una parte OPC: id -> (tipo, ruta resuelta dentro del paquete)."""
    carpeta, nombre = posixpath.split(parte)
    ruta = posixpath.join(carpeta, "_rels", nombre + ".rels")
    if ruta not in paquete.namelist():
        return {}
    salida = {}
    for rel in ET.fromstring(paquete.read(ruta)).findall(REL + "Relationship"):
        destino = rel.get("Target", "")
        if destino.startswith("/"):
            resuelto = destino.lstrip("/")
        else:
            resuelto = posixpath.normpath(posixpath.join(carpeta, destino))
        salida[rel.get("Id", "")] = (rel.get("Type", ""), resuelto)
    return salida


def _parrafo_dibujo(parrafo: ET.Element) -> str:
    partes = []
    for nodo in parrafo.iter():
        if nodo.tag == A + "t":
            partes.append(nodo.text or "")
        elif nodo.tag == A + "br":
            partes.append("\n")
    return "".join(partes).strip()


def _formas(contenedor: ET.Element) -> list[str]:
    lineas = []
    for forma in contenedor:
        if forma.tag == P + "grpSp":
            lineas.extend(_formas(forma))
        elif forma.tag == P + "sp":
            marcador = forma.find(f"{P}nvSpPr/{P}nvPr/{P}ph")
            titulo = marcador is not None and marcador.get("type") in ("title", "ctrTitle")
            for parrafo in forma.iter(A + "p"):
                texto = _parrafo_dibujo(parrafo)
                if texto:
                    lineas.append(f"## {texto}" if titulo else texto)
        elif forma.tag == P + "graphicFrame":
            for fila in forma.iter(A + "tr"):
                celdas = [" ".join(_parrafo_dibujo(p) for p in c.iter(A + "p")).strip() for c in fila.iter(A + "tc")]
                if any(celdas):
                    lineas.append("| " + " | ".join(c.replace("|", "/") for c in celdas) + " |")
    return lineas


def convertir_pptx(datos: bytes) -> tuple[str, dict]:
    """Texto de cada diapositiva en orden de presentación, con sus notas del orador."""
    with zipfile.ZipFile(io.BytesIO(datos)) as paquete:
        presentacion = ET.fromstring(paquete.read("ppt/presentation.xml"))
        relaciones = _relaciones(paquete, "ppt/presentation.xml")
        lista = presentacion.find(P + "sldIdLst")
        identificadores = [d.get(R + "id", "") for d in lista] if lista is not None else []
        bloques, con_notas = [], 0
        for numero, identificador in enumerate(identificadores, 1):
            parte = relaciones[identificador][1]
            diapositiva = ET.fromstring(paquete.read(parte))
            arbol = diapositiva.find(f"{P}cSld/{P}spTree")
            lineas = _formas(arbol) if arbol is not None else []
            for tipo, destino in _relaciones(paquete, parte).values():
                if tipo.endswith("/notesSlide") and destino in paquete.namelist():
                    notas = ET.fromstring(paquete.read(destino)).find(f"{P}cSld/{P}spTree")
                    texto = [t for t in (_formas(notas) if notas is not None else []) if not t.isdigit()]
                    if texto:
                        con_notas += 1
                        lineas.append("Notas del orador: " + " ".join(texto))
            bloques.append(f"<!-- diapositiva: {numero} -->\n" + "\n\n".join(lineas) + "\n")
    return "\n".join(bloques), {"diapositivas": len(identificadores), "diapositivas_con_notas": con_notas}


def _valor_celda(celda: ET.Element, compartidas: list[str]) -> str:
    tipo = celda.get("t")
    if tipo == "inlineStr":
        return "".join(t.text or "" for t in celda.iter(S + "t")).strip()
    bruto = celda.findtext(S + "v") or ""
    if tipo == "s" and bruto.isdigit() and int(bruto) < len(compartidas):
        return compartidas[int(bruto)].strip()
    return bruto.strip()


def _ficha_hoja(paquete: zipfile.ZipFile, parte: str, compartidas: list[str]) -> dict:
    ficha = {"rango": "", "filas_con_datos": 0, "celdas_con_valor": 0, "formulas": 0, "celdas_combinadas": 0}
    primera = None
    with paquete.open(parte) as flujo:
        for _, nodo in ET.iterparse(flujo):
            if nodo.tag == S + "dimension":
                ficha["rango"] = nodo.get("ref", "")
            elif nodo.tag == S + "mergeCell":
                ficha["celdas_combinadas"] += 1
            elif nodo.tag == S + "row":
                valores = []
                for celda in nodo.findall(S + "c"):
                    ficha["formulas"] += celda.find(S + "f") is not None
                    texto = _valor_celda(celda, compartidas)
                    if texto:
                        valores.append(texto[:60])
                if valores:
                    ficha["filas_con_datos"] += 1
                    ficha["celdas_con_valor"] += len(valores)
                    if primera is None:
                        primera = {"fila": int(nodo.get("r", "0") or 0), "valores": valores[:MAX_ENCABEZADOS]}
                nodo.clear()
    ficha["primera_fila_con_datos"] = primera
    return ficha


def fichar_xlsx(datos: bytes) -> dict:
    """Inventario de hojas para localizar y citar celdas; no transcribe el contenido."""
    with zipfile.ZipFile(io.BytesIO(datos)) as paquete:
        libro = ET.fromstring(paquete.read("xl/workbook.xml"))
        relaciones = _relaciones(paquete, "xl/workbook.xml")
        compartidas = []
        if "xl/sharedStrings.xml" in paquete.namelist():
            raiz = ET.fromstring(paquete.read("xl/sharedStrings.xml"))
            compartidas = ["".join(t.text or "" for t in si.iter(S + "t")) for si in raiz.findall(S + "si")]
        hojas = []
        contenedor = libro.find(S + "sheets")
        for hoja in contenedor if contenedor is not None else []:
            tipo, parte = relaciones.get(hoja.get(R + "id", ""), ("", ""))
            dato = {"nombre": hoja.get("name", ""), "estado": hoja.get("state", "visible")}
            if tipo.endswith("/worksheet") and parte in paquete.namelist():
                dato.update(_ficha_hoja(paquete, parte, compartidas))
            else:
                dato["tipo"] = tipo.rsplit("/", 1)[-1] or "desconocido"
            hojas.append(dato)
    return {"hojas": hojas}
