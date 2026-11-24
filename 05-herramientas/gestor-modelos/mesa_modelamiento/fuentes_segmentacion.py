"""Segmentación de textos derivados en fragmentos estables enlazados a su ubicación en el original.

Los PDF normativos se dividen por artículo y numeral; los demás PDF por bloques de página. Los DOCX
se dividen por numeral o sección y conservan el número de párrafo. Una estructura no reconocida se
declara como bloque, nunca se presenta como artículo.
"""

from __future__ import annotations

import re
from collections import Counter

# El título debe empezar en mayúscula: «Artículo 5 de la Ley...» al inicio de una línea es una cita, no un encabezado.
ARTICULO = re.compile(r"\s*(?:Art[íi]culo|ART[ÍI]CULO)\s+(\d+(?:-[A-Z])?)[\s.°º:\-–—”“\"'’´`]*($|[A-ZÁÉÍÓÚÑ¿\"“(].*$)")
ENCABEZADO = re.compile(
    r"\s*(LIBRO|T[ÍI]TULO|CAP[ÍI]TULO|SUBCAP[ÍI]TULO|SECCI[ÓO]N|SUBSECCI[ÓO]N)\s+([IVXLC\d]+|[ÚU]NIC[OA])\b"
)
NIVELES = {"LIBRO": 0, "TITULO": 1, "CAPITULO": 2, "SUBCAPITULO": 3, "SECCION": 4, "SUBSECCION": 5}
PAGINA = re.compile(r"<!-- pagina_pdf: (\d+);")
MARCA_DOCX = re.compile(r"<!-- (parrafo|tabla|diapositiva): (\d+)(.*?) -->")
MAX_FRAGMENTO = 4000
BLOQUE = 1500
MIN_ARTICULOS = 3


def _normalizar_repeticion(linea: str) -> str:
    return re.sub(r"\d+", "#", re.sub(r"\s+", " ", linea)).strip().lower()


def _paginas_pdf(texto: str) -> list[tuple[int, list[str]]]:
    paginas: list[tuple[int, list[str]]] = []
    for linea in texto.splitlines():
        coincidencia = PAGINA.match(linea)
        if coincidencia:
            paginas.append((int(coincidencia.group(1)), []))
        elif paginas and not linea.startswith("<!-- metadatos:"):
            paginas[-1][1].append(linea.rstrip())
    return paginas


def _repetidas(paginas: list[tuple[int, list[str]]]) -> set[str]:
    """Líneas de cabecera o pie que aparecen en la mitad o más de las páginas."""
    if len(paginas) < 4:
        return set()
    conteo: Counter[str] = Counter()
    for _, lineas in paginas:
        utiles = [linea for linea in lineas if linea.strip()]
        # Un encabezado normativo al borde de varias páginas no es cabecera aunque coincida tras normalizar dígitos.
        candidatas = [x for x in utiles[:3] + utiles[-3:] if not ARTICULO.match(x) and not ENCABEZADO.match(x)]
        extremos = {_normalizar_repeticion(linea) for linea in candidatas}
        conteo.update(e for e in extremos if 0 < len(e) <= 120)
    return {linea for linea, veces in conteo.items() if veces >= len(paginas) / 2}


def _encabezados(estado: list[str], linea: str, siguiente: str) -> list[str]:
    coincidencia = ENCABEZADO.match(linea)
    if not coincidencia:
        return estado
    tipo = coincidencia.group(1).upper().translate(str.maketrans("ÍÓ", "IO"))
    nivel = NIVELES.get(tipo, 5)
    nombre = re.sub(r"\s+", " ", linea).strip()
    if re.search(r"\s\d{1,4}$", nombre):
        return estado  # Entrada de un índice de contenido: termina en número de página.
    if siguiente and siguiente.isupper() and len(siguiente) < 140 and not ENCABEZADO.match(siguiente):
        nombre += " " + re.sub(r"\s+", " ", siguiente).strip()
    niveles = [e for e in estado if NIVELES.get(e.split()[0].upper().translate(str.maketrans("ÍÓ", "IO")), 5) < nivel]
    return niveles + [nombre]


def _texto(lineas: list[tuple[int, str]]) -> str:
    return re.sub(r"\n{3,}", "\n\n", "\n".join(linea for _, linea in lineas)).strip()


def _fragmento(clave: str, estructura: str, lineas: list[tuple[int, str]], **campos) -> dict:
    paginas = sorted({p for p, linea in lineas if linea.strip()}) or sorted({p for p, _ in lineas})
    return {
        "clave": clave,
        "estructura": estructura,
        "ubicacion": {"tipo": "pagina_pdf", "desde": paginas[0], "hasta": paginas[-1], "paginas": paginas},
        "texto": _texto(lineas),
        **campos,
    }


def _bloques(lineas: list[tuple[int, str]], clave: str, estructura: str, encabezados: list[str]) -> list[dict]:
    """Divide en párrafos acumulados hasta ``BLOQUE`` caracteres sin cortar un párrafo."""
    salida, actual, tamano = [], [], 0
    for indice, (pagina, linea) in enumerate(lineas):
        actual.append((pagina, linea))
        tamano += len(linea)
        fin_parrafo = not linea.strip() or indice == len(lineas) - 1
        if tamano >= BLOQUE and fin_parrafo:
            salida.append(actual)
            actual, tamano = [], 0
    if any(linea.strip() for _, linea in actual):
        salida.append(actual)
    if len(salida) == 1:
        return [_fragmento(clave, estructura, salida[0], encabezados=encabezados)]
    return [
        _fragmento(f"{clave}-b{n}", estructura, partes, encabezados=encabezados) for n, partes in enumerate(salida, 1)
    ]


def _retroceder(lineas: list[tuple[int, str]], inicio: int, limite: int) -> int:
    """Inicio del bloque de títulos o capítulos (y su nombre) que precede a un artículo y le pertenece."""
    corte, i = inicio, inicio - 1
    while i >= limite:
        texto = lineas[i][1].strip()
        if not texto:
            i -= 1
            continue
        if ENCABEZADO.match(texto):
            corte, i = i, i - 1
            continue
        anterior = next((x.strip() for _, x in reversed(lineas[limite:i]) if x.strip()), "")
        if texto.isupper() and len(texto) < 140 and ENCABEZADO.match(anterior):
            i -= 1
            continue
        break
    return corte


def _articulos(lineas: list[tuple[int, str]], inicios: list[int]) -> list[dict]:
    previos = [-1] + inicios[:-1]
    cortes = [_retroceder(lineas, inicio, previo + 1) for inicio, previo in zip(inicios, previos, strict=True)]
    fragmentos: list[dict] = []
    if any(linea.strip() for _, linea in lineas[: cortes[0]]):
        fragmentos += _bloques(lineas[: cortes[0]], "preambulo", "PREAMBULO", [])
    estado: list[str] = []
    pendiente = 0
    for posicion, (inicio, corte) in enumerate(zip(inicios, cortes, strict=True)):
        for i in range(pendiente, inicio):
            siguiente = next((linea for _, linea in lineas[i + 1 : i + 4] if linea.strip()), "")
            estado = _encabezados(estado, lineas[i][1], siguiente)
        pendiente = inicio
        fin = cortes[posicion + 1] if posicion + 1 < len(cortes) else len(lineas)
        tramo, propio = lineas[corte:fin], inicio - corte
        coincidencia = ARTICULO.match(tramo[propio][1])
        articulo, titulo = coincidencia.group(1), coincidencia.group(2).strip()[:160]
        patron = re.compile(rf"\s*{re.escape(articulo)}\.\d+\.?\s")
        partes = [0] + [i for i, (_, linea) in enumerate(tramo) if i > propio and patron.match(linea)]
        cabecera_vacia = len(partes) > 1 and all(
            i == propio or not x.strip() or x.strip().isupper() or ENCABEZADO.match(x)
            for i, (_, x) in enumerate(tramo[: partes[1]])
        )
        comunes = {"articulo": articulo, "titulo": titulo, "encabezados": list(estado)}
        for n, (a, b) in enumerate(zip(partes, partes[1:] + [len(tramo)], strict=True)):
            sub = tramo[0 if n == 1 and cabecera_vacia else a : b]
            if n == 0:
                if not cabecera_vacia:
                    sin_cuerpo = len(partes) == 1 and len(_texto(sub[propio:])) <= len(tramo[propio][1].strip()) + 2
                    estructura = "ENCABEZADO-SIN-CUERPO" if sin_cuerpo else "ARTICULO"
                    fragmentos.append(_fragmento(f"art-{articulo}", estructura, sub, numeral=articulo, **comunes))
                continue
            numeral = re.match(r"\s*(\d+\.\d+)", tramo[a][1]).group(1)
            fragmentos.append(_fragmento(f"art-{numeral}", "NUMERAL", sub, numeral=numeral, **comunes))
    return fragmentos


def segmentar_pdf(texto: str) -> tuple[list[dict], dict]:
    """Fragmentos de un Markdown paginado y métricas de cobertura."""
    paginas = _paginas_pdf(texto)
    repetidas = _repetidas(paginas)
    lineas = [
        (n, linea) for n, contenido in paginas for linea in contenido if _normalizar_repeticion(linea) not in repetidas
    ]
    inicios, previo = [], None
    for i, (_, linea) in enumerate(lineas):
        coincidencia = ARTICULO.match(linea)
        if coincidencia and coincidencia.group(1) != previo:
            inicios.append(i)
            previo = coincidencia.group(1)
        elif coincidencia:
            # Encabezado repetido del mismo artículo (salto de página o capa duplicada del PDF).
            lineas[i] = (lineas[i][0], "")
    if len(inicios) >= MIN_ARTICULOS:
        fragmentos, modo = _articulos(lineas, inicios), "ARTICULOS"
    else:
        fragmentos, modo = [], "BLOQUES"
        for numero, contenido in paginas:
            filtradas = [(numero, linea) for linea in contenido if _normalizar_repeticion(linea) not in repetidas]
            fragmentos += _bloques(filtradas, f"p{numero}", "BLOQUE-PAGINA", [])
    origen = sum(len(re.sub(r"\s", "", linea)) for _, linea in lineas)
    return _cerrar(fragmentos), {"modo": modo, "lineas_repetidas_omitidas": len(repetidas), "caracteres_origen": origen}


def segmentar_office(texto: str) -> tuple[list[dict], dict]:
    """Fragmentos de DOCX por numeral o sección, de tablas y de diapositivas PPTX."""
    unidades = []
    cuerpo = texto.split("\n<!-- notas_pie -->", 1)
    for coincidencia in MARCA_DOCX.finditer(cuerpo[0]):
        fin = cuerpo[0].find("\n<!-- ", coincidencia.end())
        contenido = cuerpo[0][coincidencia.end() : fin if fin >= 0 else None].strip()
        campos = dict(re.findall(r"; (\w+): ([^;]*)", coincidencia.group(3)))
        unidades.append((coincidencia.group(1), int(coincidencia.group(2)), campos, contenido))
    fragmentos: list[dict] = []
    actual: list[tuple] = []

    def cerrar() -> None:
        if not actual:
            return
        tipo, numero, campos, _ = actual[0]
        clave = {"parrafo": "par", "tabla": "tabla", "diapositiva": "diap"}[tipo] + f"-{numero}"
        numeral = campos.get("numeral") or campos.get("numeral_texto")
        fragmentos.append(
            {
                "clave": clave,
                "estructura": "NUMERAL" if numeral else {"parrafo": "BLOQUE-PARRAFOS"}.get(tipo, tipo.upper()),
                "ubicacion": {"tipo": tipo, "desde": numero, "hasta": actual[-1][1]},
                "texto": "\n\n".join(u[3] for u in actual if u[3]),
                "numeral": numeral,
                "encabezados": campos["seccion"].split(" > ") if campos.get("seccion") else [],
            }
        )
        actual.clear()

    for unidad in unidades:
        tipo, _, campos, contenido = unidad
        frontera = tipo != "parrafo" or campos.get("numeral") or campos.get("numeral_texto")
        tamano = sum(len(u[3]) for u in actual)
        if frontera or tamano >= BLOQUE or (actual and actual[0][0] != "parrafo"):
            cerrar()
        actual.append(unidad)
    cerrar()
    if len(cuerpo) > 1 and cuerpo[1].strip():
        notas = cuerpo[1].strip()
        fragmentos.append(
            {"clave": "notas-pie", "estructura": "NOTAS-PIE", "ubicacion": {"tipo": "notas_pie"}, "texto": notas}
        )
    origen = sum(len(re.sub(r"\s", "", u[3])) for u in unidades) + (
        len(re.sub(r"\s", "", cuerpo[1])) if len(cuerpo) > 1 else 0
    )
    return _cerrar(fragmentos), {"modo": "ESTRUCTURA-OOXML", "caracteres_origen": origen}


def _cerrar(fragmentos: list[dict]) -> list[dict]:
    """Parte fragmentos excesivos y hace únicas las claves; la ocurrencia más extensa conserva la clave base."""
    salida = []
    for fragmento in fragmentos:
        texto = fragmento["texto"]
        if len(texto) <= MAX_FRAGMENTO:
            salida.append(fragmento)
            continue
        trozos, actual = [], ""
        for parrafo in re.split(r"\n\s*\n", texto):
            if actual and len(actual) + len(parrafo) > MAX_FRAGMENTO:
                trozos.append(actual)
                actual = ""
            actual = f"{actual}\n\n{parrafo}" if actual else parrafo
        trozos.append(actual)
        for n, trozo in enumerate(trozos, 1):
            salida.append({**fragmento, "clave": f"{fragmento['clave']}-parte{n}", "texto": trozo, "partido": True})
    por_clave: dict[str, list[dict]] = {}
    for fragmento in salida:
        por_clave.setdefault(fragmento["clave"], []).append(fragmento)
    for clave, grupo in por_clave.items():
        if len(grupo) > 1:
            for orden, fragmento in enumerate(sorted(grupo, key=lambda f: -len(f["texto"]))[1:], 2):
                fragmento["clave"] = f"{clave}~{orden}"
                fragmento["clave_repetida"] = True
    for fragmento in salida:
        fragmento["caracteres"] = len(fragmento["texto"])
    return [f for f in salida if f["texto"].strip()]
