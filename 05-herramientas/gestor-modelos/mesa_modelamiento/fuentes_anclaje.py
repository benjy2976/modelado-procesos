"""Anclaje de una cita a rectángulos de página en el PDF original y verificación de anclas guardadas.

Los rectángulos se expresan como proporciones de la página con origen arriba a la izquierda, igual
que ``<codigo>-fuentes-visor.json``. Una página sin capa de texto (OCR) no se ancla automáticamente.
"""

from __future__ import annotations

import json
import logging
import unicodedata
from contextlib import closing
from pathlib import Path

from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTAnno, LTChar, LTTextContainer, LTTextLine
from pypdf import PdfReader

from .fuentes_busqueda import _conectar
from .fuentes_preparacion import REFERENCIAS, _sha256
from .repositorio import ErrorDominio

logging.getLogger("pdfminer").setLevel(logging.ERROR)
MINIMO_TRAMO = 12  # Caracteres compactos mínimos por página para aceptar un corte entre páginas.


def _normal(caracter: str) -> str:
    """Letras y dígitos sin tildes ni mayúsculas; los espacios se conservan y la puntuación se descarta."""
    salida = ""
    for c in unicodedata.normalize("NFKD", caracter):
        if unicodedata.combining(c):
            continue
        if c.isspace():
            salida += " "
        elif c.isalnum():
            salida += c.casefold()
    return salida


def normalizar_cita(texto: str) -> str:
    return " ".join("".join(_normal(c) for c in texto).split())


def _lineas(disposicion) -> list[list[tuple[str, tuple | None]]]:
    lineas = []

    def recorrer(nodo) -> None:
        for hijo in nodo:
            if isinstance(hijo, LTTextLine):
                lineas.append([(o.get_text(), o.bbox if isinstance(o, LTChar) else None) for o in hijo
                               if isinstance(o, (LTChar, LTAnno))])  # fmt: skip
            elif isinstance(hijo, LTTextContainer):
                recorrer(hijo)

    recorrer(disposicion)
    return lineas


def _flujo(lineas: list[list[tuple[str, tuple | None]]]) -> tuple[str, list[tuple[int, tuple | None]]]:
    """Texto normalizado de la página y, por cada carácter, su renglón y caja."""
    texto, mapa = [], []

    def espacio() -> None:
        if texto and texto[-1] != " ":
            texto.append(" ")
            mapa.append((-1, None))

    for numero, linea in enumerate(lineas):
        while linea and not linea[-1][0].strip():  # El salto final del renglón no es un espacio del texto.
            linea = linea[:-1]
        bruto = "".join(c for c, _ in linea)
        for caracter, caja in linea:
            normal = _normal(caracter)
            if not normal and caja is not None and mapa and mapa[-1][0] == numero and mapa[-1][1]:
                # La puntuación no cuenta para buscar, pero su caja amplía el resaltado del carácter previo.
                previa = mapa[-1][1]
                union = (
                    min(previa[0], caja[0]),
                    min(previa[1], caja[1]),
                    max(previa[2], caja[2]),
                    max(previa[3], caja[3]),
                )
                mapa[-1] = (numero, union)
            for c in normal:
                if c == " ":
                    espacio()
                else:
                    texto.append(c)
                    mapa.append((numero, caja))
        if not bruto.endswith("-"):  # Palabra partida con guion al final del renglón: se une sin espacio.
            espacio()
    return "".join(texto), mapa


def rectangulo_valido(rectangulo) -> bool:
    if not isinstance(rectangulo, list) or len(rectangulo) != 4:
        return False
    if not all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in rectangulo):
        return False
    return rectangulo[0] < rectangulo[2] and rectangulo[1] < rectangulo[3]


def _original(raiz: Path, ruta: str) -> Path:
    archivo = (raiz / ruta).resolve()
    referencias = (raiz / REFERENCIAS).resolve()
    if referencias not in archivo.parents or archivo.suffix.lower() != ".pdf":
        raise ErrorDominio("Solo se anclan PDF de la biblioteca 01-referencias")
    return archivo


def _pagina(archivo: Path, numero: int) -> tuple[str, list, tuple]:
    """Texto normalizado y compacto de una página, su mapa de cajas y el marco de la página."""
    disposicion = next(extract_pages(archivo, page_numbers=[numero - 1], laparams=LAParams()))
    texto, mapa = _flujo(_lineas(disposicion))
    # Se compara sin espacios: ligaduras partidas («fi nalidad») o espacios de composición no deben impedir el ancla.
    compacto = [(c, m) for c, m in zip(texto, mapa, strict=True) if c != " "]
    return "".join(c for c, _ in compacto), [m for _, m in compacto], disposicion.bbox


def _rectangulos(mapa: list, inicio: int, largo: int, marco: tuple) -> list[list[float]]:
    x0, y0, x1, y1 = marco
    ancho, alto = x1 - x0, y1 - y0
    por_renglon: dict[int, list[tuple]] = {}
    for renglon, caja in mapa[inicio : inicio + largo]:
        if caja is not None:
            por_renglon.setdefault(renglon, []).append(caja)
    salida = []
    for cajas in (por_renglon[k] for k in sorted(por_renglon)):
        a, b = min(c[0] for c in cajas), min(c[1] for c in cajas)
        c, d = max(c[2] for c in cajas), max(c[3] for c in cajas)
        salida.append([round((a - x0) / ancho, 4), round((y1 - d) / alto, 4),
                       round((c - x0) / ancho, 4), round((y1 - b) / alto, 4)])  # fmt: skip
    return salida


def _verificar(raiz: Path, ruta: str, sha256: str | None) -> tuple[Path, dict, str | None]:
    archivo = _original(raiz.resolve(), ruta)
    if not archivo.is_file():
        return archivo, {}, "ARCHIVO-FALTANTE"
    actual = _sha256(archivo)
    if sha256 and sha256.upper() != actual:
        return archivo, {"sha256": actual.lower()}, "HASH-DISTINTO"
    return archivo, {"sha256": actual.lower()}, None


def anclar(raiz: Path, ruta: str, pagina: int, cita: str, sha256: str | None = None) -> dict:
    """Ubica la cita en una página y devuelve un rectángulo por renglón, o el motivo por el que no se puede."""
    archivo, extra, falla = _verificar(raiz, ruta, sha256)
    salida = {"ruta": ruta, "pagina": pagina, "rectangulos": [], **extra}
    if falla:
        return {**salida, "estado": falla}
    if not 1 <= pagina <= len(PdfReader(archivo, strict=False).pages):
        return {**salida, "estado": "PAGINA-INEXISTENTE"}
    texto, mapa, marco = _pagina(archivo, pagina)
    if not texto:
        return {**salida, "estado": "SIN-CAPA-TEXTO"}
    buscada = normalizar_cita(cita).replace(" ", "")
    inicio = texto.find(buscada) if buscada else -1
    if inicio < 0:
        return {**salida, "estado": "CITA-NO-HALLADA"}
    rectangulos = _rectangulos(mapa, inicio, len(buscada), marco)
    return {**salida, "estado": "ANCLADO", "rectangulos": rectangulos, "ocurrencias": texto.count(buscada)}


def anclar_entre_paginas(raiz: Path, ruta: str, paginas: list[int], cita: str, sha256: str | None = None) -> dict:
    """Ancla una cita que continúa de una página a la siguiente y devuelve un tramo por página.

    El corte se detecta en el texto: el prefijo más largo de la cita que figura en una página y cuyo
    resto aparece en la página siguiente. Los tramos se marcan `citado`; el rol de antecedente lo decide
    quien registra la referencia.
    """
    archivo, extra, falla = _verificar(raiz, ruta, sha256)
    salida = {"ruta": ruta, "rectangulos": [], "tramos": [], **extra}
    if falla:
        return {**salida, "estado": falla}
    buscada = normalizar_cita(cita).replace(" ", "")
    paginas_pdf = {}
    for actual, siguiente in zip(paginas, paginas[1:], strict=False):
        if siguiente != actual + 1:
            continue
        for numero in (actual, siguiente):
            paginas_pdf.setdefault(numero, _pagina(archivo, numero))
        texto_a, mapa_a, marco_a = paginas_pdf[actual]
        texto_b, mapa_b, marco_b = paginas_pdf[siguiente]
        bajo, alto = 0, len(buscada) - 1
        while bajo < alto:  # Mayor prefijo presente en la primera página (la presencia es monótona).
            medio = (bajo + alto + 1) // 2
            bajo, alto = (medio, alto) if buscada[:medio] in texto_a else (bajo, medio - 1)
        resto = buscada[bajo:]
        if bajo < MINIMO_TRAMO or len(resto) < MINIMO_TRAMO or resto not in texto_b:
            continue
        inicio_a, inicio_b = texto_a.rfind(buscada[:bajo]), texto_b.find(resto)
        tramos = [
            {"pagina": actual, "rol": "citado", "rectangulos": _rectangulos(mapa_a, inicio_a, bajo, marco_a)},
            {"pagina": siguiente, "rol": "citado", "rectangulos": _rectangulos(mapa_b, inicio_b, len(resto), marco_b)},
        ]
        return {**salida, "estado": "ANCLADO", "pagina": actual, "rectangulos": tramos[0]["rectangulos"],
                "tramos": tramos}  # fmt: skip
    return {**salida, "estado": "CITA-NO-HALLADA"}


def anclar_fragmento(raiz: Path, fragmento: str, cita: str) -> dict:
    """Ancla la cita en la página del fragmento que la contiene o, si cruza el salto, en dos tramos."""
    base, _ = _conectar(raiz)
    with closing(base):
        fila = base.execute(
            "SELECT ruta, sha256, ubicacion, tipo FROM fragmentos WHERE id = ?", (fragmento,)
        ).fetchone()
    if fila is None:
        raise ErrorDominio("Fragmento inexistente en el índice", 404)
    ubicacion = json.loads(fila[2])
    if fila[3] != "pdf":
        return {"fragmento": fragmento, "estado": "NO-PDF", "ubicacion": ubicacion}
    intentos = []
    for pagina in ubicacion["paginas"]:
        resultado = anclar(raiz, fila[0], pagina, cita, fila[1])
        intentos.append({"pagina": pagina, "estado": resultado["estado"]})
        if resultado["estado"] in ("ANCLADO", "HASH-DISTINTO"):
            return {"fragmento": fragmento, **resultado, "intentos": intentos}
    if len(ubicacion["paginas"]) > 1:
        cruzada = anclar_entre_paginas(raiz, fila[0], ubicacion["paginas"], cita, fila[1])
        if cruzada["estado"] == "ANCLADO":
            return {"fragmento": fragmento, **cruzada, "intentos": intentos}
    return {"fragmento": fragmento, "ruta": fila[0], "estado": "CITA-NO-HALLADA", "intentos": intentos}


def verificar_anclas(raiz: Path, fuentes_visor: Path) -> list[dict]:
    """Comprueba archivo, hash, página y rectángulos de cada ancla guardada para el visor."""
    raiz = raiz.resolve()
    if not fuentes_visor.is_file():
        return []
    datos = json.loads(fuentes_visor.read_text(encoding="utf-8"))
    paginas: dict[str, int] = {}
    salida = []
    for elemento, anclas in datos.get("elementos", {}).items():
        for orden, ancla in enumerate(anclas):
            archivo = raiz / ancla.get("ruta", "")
            estado = "VIGENTE"
            if not archivo.is_file():
                estado = "ARCHIVO-FALTANTE"
            elif _sha256(archivo) != str(ancla.get("sha256", "")).upper():
                estado = "HASH-DISTINTO"
            else:
                total = paginas.setdefault(ancla["ruta"], len(PdfReader(archivo, strict=False).pages))
                tramos = ancla.get("tramos") or [
                    {"pagina": ancla.get("pagina", 0), "rectangulos": ancla.get("rectangulos")}
                ]
                if any(not 1 <= int(t.get("pagina", 0)) <= total for t in tramos):
                    estado = "PAGINA-INEXISTENTE"
                elif any(not t.get("rectangulos") for t in tramos):
                    estado = "SIN-RECTANGULOS"
                elif not all(rectangulo_valido(r) for t in tramos for r in t["rectangulos"]):
                    estado = "RECTANGULO-INVALIDO"
            salida.append({"elemento": elemento, "orden": orden, "pagina": ancla.get("pagina"), "estado": estado})
    return salida
