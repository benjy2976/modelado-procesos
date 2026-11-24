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


def anclar(raiz: Path, ruta: str, pagina: int, cita: str, sha256: str | None = None) -> dict:
    """Ubica la cita en una página y devuelve un rectángulo por renglón, o el motivo por el que no se puede."""
    raiz = raiz.resolve()
    archivo = _original(raiz, ruta)
    salida = {"ruta": ruta, "pagina": pagina, "rectangulos": []}
    if not archivo.is_file():
        return {**salida, "estado": "ARCHIVO-FALTANTE"}
    actual = _sha256(archivo)
    salida["sha256"] = actual.lower()
    if sha256 and sha256.upper() != actual:
        return {**salida, "estado": "HASH-DISTINTO"}
    if not 1 <= pagina <= len(PdfReader(archivo, strict=False).pages):
        return {**salida, "estado": "PAGINA-INEXISTENTE"}
    disposicion = next(extract_pages(archivo, page_numbers=[pagina - 1], laparams=LAParams()))
    texto, mapa = _flujo(_lineas(disposicion))
    if not texto.strip():
        return {**salida, "estado": "SIN-CAPA-TEXTO"}
    buscada = normalizar_cita(cita)
    inicio = texto.find(buscada) if buscada else -1
    if inicio < 0:
        return {**salida, "estado": "CITA-NO-HALLADA"}
    x0, y0, x1, y1 = disposicion.bbox
    ancho, alto = x1 - x0, y1 - y0
    por_renglon: dict[int, list[tuple]] = {}
    for renglon, caja in mapa[inicio : inicio + len(buscada)]:
        if caja is not None:
            por_renglon.setdefault(renglon, []).append(caja)
    rectangulos = []
    for cajas in (por_renglon[k] for k in sorted(por_renglon)):
        a, b = min(c[0] for c in cajas), min(c[1] for c in cajas)
        c, d = max(c[2] for c in cajas), max(c[3] for c in cajas)
        rectangulos.append([round((a - x0) / ancho, 4), round((y1 - d) / alto, 4),
                            round((c - x0) / ancho, 4), round((y1 - b) / alto, 4)])  # fmt: skip
    return {**salida, "estado": "ANCLADO", "rectangulos": rectangulos, "ocurrencias": texto.count(buscada)}


def anclar_fragmento(raiz: Path, fragmento: str, cita: str) -> dict:
    """Ancla la cita en la primera página del fragmento que la contiene."""
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
                if not 1 <= int(ancla.get("pagina", 0)) <= total:
                    estado = "PAGINA-INEXISTENTE"
                elif not ancla.get("rectangulos"):
                    estado = "SIN-RECTANGULOS"
                elif not all(rectangulo_valido(r) for r in ancla["rectangulos"]):
                    estado = "RECTANGULO-INVALIDO"
            salida.append({"elemento": elemento, "orden": orden, "pagina": ancla.get("pagina"), "estado": estado})
    return salida
