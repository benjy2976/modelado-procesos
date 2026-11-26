"""Exportaciones del BPMN para otras herramientas, generadas al momento desde el XML vigente o de una versión."""

from __future__ import annotations

import sys
from pathlib import Path

from lxml import etree

from .repositorio import ErrorDominio


def bpmn_para_bizagi(contenido: bytes) -> bytes:
    """Convierte el BPMN del generador al dialecto que importa Bizagi Modeler (`_bpmn_a_bizagi.py`, DEC-025)."""
    modulo = Path(__file__).resolve().parents[1]
    if str(modulo) not in sys.path:
        sys.path.insert(0, str(modulo))
    from _bpmn_a_bizagi import convertir

    try:
        raiz = etree.fromstring(contenido, etree.XMLParser(remove_blank_text=True, resolve_entities=False))
    except etree.XMLSyntaxError as exc:
        raise ErrorDominio("El BPMN no es XML válido; no se pudo convertir para Bizagi", 422) from exc
    convertir(raiz)
    return etree.tostring(raiz.getroottree(), xml_declaration=True, encoding="UTF-8")
