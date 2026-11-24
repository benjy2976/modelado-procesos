"""Reconstrucción de la numeración automática de Word a partir de estilos y definiciones de lista."""

from __future__ import annotations

import re
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
TITULO = re.compile(r"(?:heading|t[íi]tulo)\s*(\d)", re.IGNORECASE)
ROMANOS = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"), (40, "xl")]
ROMANOS += [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]


def valor(elemento: ET.Element | None, ruta: str) -> str | None:
    if elemento is None:
        return None
    hallado = elemento.find(ruta)
    return None if hallado is None else hallado.get(W + "val")


def _romano(numero: int) -> str:
    salida = ""
    for cantidad, letra in ROMANOS:
        while numero >= cantidad:
            salida += letra
            numero -= cantidad
    return salida


def formatear(numero: int, formato: str) -> str:
    """Aplica el formato de número de WordprocessingML; los no previstos caen a decimal."""
    if formato == "decimalZero":
        return f"{numero:02d}"
    if formato in ("lowerLetter", "upperLetter"):
        letra = chr(ord("a") + (numero - 1) % 26) * ((numero - 1) // 26 + 1) if numero > 0 else ""
        return letra.upper() if formato == "upperLetter" else letra
    if formato in ("lowerRoman", "upperRoman"):
        romano = _romano(numero)
        return romano.upper() if formato == "upperRoman" else romano
    if formato == "ordinal":
        return f"{numero}°"
    if formato == "none":
        return ""
    return str(numero)


class Estilos:
    """Herencia de estilos de párrafo relevante para numeración y títulos."""

    def __init__(self, xml: bytes | None) -> None:
        self.base: dict[str, str] = {}
        self.numpr: dict[str, tuple[str | None, str | None]] = {}
        self.esquema: dict[str, int] = {}
        self.nombre: dict[str, str] = {}
        self.defecto: str | None = None
        if not xml:
            return
        for estilo in ET.fromstring(xml).findall(W + "style"):
            if estilo.get(W + "type") != "paragraph":
                continue
            identificador = estilo.get(W + "styleId", "")
            if estilo.get(W + "default") in ("1", "true"):
                self.defecto = identificador
            self.nombre[identificador] = valor(estilo, W + "name") or ""
            base = valor(estilo, W + "basedOn")
            if base:
                self.base[identificador] = base
            ppr = estilo.find(W + "pPr")
            numpr = ppr.find(W + "numPr") if ppr is not None else None
            if numpr is not None:
                self.numpr[identificador] = (valor(numpr, W + "numId"), valor(numpr, W + "ilvl"))
            nivel = valor(ppr, W + "outlineLvl")
            if nivel is not None and nivel.isdigit():
                self.esquema[identificador] = int(nivel)

    def _cadena(self, estilo: str | None):
        vistos = set()
        while estilo and estilo not in vistos and len(vistos) < 30:
            vistos.add(estilo)
            yield estilo
            estilo = self.base.get(estilo)

    def numeracion(self, estilo: str) -> tuple[str | None, str | None]:
        for actual in self._cadena(estilo):
            if actual in self.numpr:
                return self.numpr[actual]
        return None, None

    def nivel_titulo(self, estilo: str | None) -> int | None:
        for actual in self._cadena(estilo):
            if actual in self.esquema:
                nivel = self.esquema[actual]
                return nivel if nivel < 9 else None
            coincidencia = TITULO.fullmatch(self.nombre.get(actual, "").strip())
            if coincidencia:
                return int(coincidencia.group(1)) - 1
        return None


def _nivel(elemento: ET.Element) -> dict:
    reinicio = valor(elemento, W + "lvlRestart")
    return {
        "inicio": int(valor(elemento, W + "start") or 1),
        "formato": valor(elemento, W + "numFmt") or "decimal",
        "texto": valor(elemento, W + "lvlText") or "",
        "reinicio": int(reinicio) if reinicio is not None else None,
        "legal": elemento.find(W + "isLgl") is not None,
        "estilo": valor(elemento, W + "pStyle"),
    }


class Numeracion:
    """Contadores de listas en orden de documento, con la semántica de reinicio de Word."""

    def __init__(self, xml: bytes | None, estilos: Estilos) -> None:
        self.estilos = estilos
        self.abstractos: dict[str, dict[int, dict]] = {}
        self.enlaces: dict[str, str] = {}
        self.listas: dict[str, tuple[str, dict[int, int], dict[int, dict]]] = {}
        self.contadores: dict[str, dict[int, int]] = {}
        self.usadas: set[str] = set()
        if not xml:
            return
        raiz = ET.fromstring(xml)
        for abstracto in raiz.findall(W + "abstractNum"):
            identificador = abstracto.get(W + "abstractNumId", "")
            niveles = abstracto.findall(W + "lvl")
            self.abstractos[identificador] = {int(n.get(W + "ilvl", "0")): _nivel(n) for n in niveles}
            enlace = valor(abstracto, W + "numStyleLink")
            if enlace:
                self.enlaces[identificador] = enlace
        for lista in raiz.findall(W + "num"):
            inicios, niveles = {}, {}
            for cambio in lista.findall(W + "lvlOverride"):
                nivel = int(cambio.get(W + "ilvl", "0"))
                inicio = valor(cambio, W + "startOverride")
                if inicio is not None:
                    inicios[nivel] = int(inicio)
                definicion = cambio.find(W + "lvl")
                if definicion is not None:
                    niveles[nivel] = _nivel(definicion)
            self.listas[lista.get(W + "numId", "")] = (valor(lista, W + "abstractNumId") or "", inicios, niveles)

    def _abstracto(self, identificador: str) -> str:
        """Sigue un vínculo a estilo de numeración hasta la definición con niveles."""
        enlace = self.enlaces.get(identificador)
        if enlace and not self.abstractos.get(identificador):
            num_id, _ = self.estilos.numeracion(enlace)
            if num_id in self.listas:
                return self.listas[num_id][0]
        return identificador

    def siguiente(self, num_id: str | None, nivel: str | None, estilo: str | None) -> tuple[str, bool] | None:
        """Avanza el contador del párrafo y devuelve (numeral, es_viñeta); None si no está numerado."""
        if not num_id or num_id == "0" or num_id not in self.listas:
            return None
        abstracto, inicios, propios = self.listas[num_id]
        abstracto = self._abstracto(abstracto)
        niveles = {**self.abstractos.get(abstracto, {}), **propios}
        if nivel is None:
            nivel = next((str(n) for n, d in niveles.items() if estilo and d["estilo"] == estilo), "0")
        actual = int(nivel)
        if actual not in niveles:
            return None
        contador = self.contadores.setdefault(abstracto, {})
        if num_id not in self.usadas:
            self.usadas.add(num_id)
            for posicion, inicio in inicios.items():
                contador[posicion] = inicio - 1
        definicion = niveles[actual]
        contador[actual] = contador.get(actual, definicion["inicio"] - 1) + 1
        for posicion in [p for p in contador if p > actual]:
            reinicio = niveles.get(posicion, {}).get("reinicio")
            limite = posicion if reinicio is None else reinicio
            if limite != 0 and actual < limite:
                del contador[posicion]
        if definicion["formato"] == "bullet":
            return definicion["texto"], True

        def sustituir(coincidencia: re.Match) -> str:
            posicion = int(coincidencia.group(1)) - 1
            otro = niveles.get(posicion, {"inicio": 1, "formato": "decimal"})
            numero = contador.get(posicion, otro["inicio"])
            return formatear(numero, "decimal" if definicion["legal"] else otro["formato"])

        return re.sub(r"%(\d)", sustituir, definicion["texto"]).strip(), False
