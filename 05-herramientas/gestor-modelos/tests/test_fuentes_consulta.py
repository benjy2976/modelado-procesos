"""Segmentación, índice léxico, contexto y temas con textos sintéticos."""

import hashlib
import json
from pathlib import Path

import pytest

from mesa_modelamiento.fuentes_busqueda import buscar, contexto, expresion, indexar
from mesa_modelamiento.fuentes_fragmentos import segmentar
from mesa_modelamiento.fuentes_segmentacion import segmentar_office, segmentar_pdf
from mesa_modelamiento.fuentes_temas import VOCABULARIO, comprobar, sugerir, terminos_de
from mesa_modelamiento.repositorio import ErrorDominio

CABECERA = "Reglamento de prueba, texto consolidado"


def _pagina(numero: int, *lineas: str) -> str:
    cuerpo = "\n".join([CABECERA, f"Página {numero} de 5", *lineas])
    return f"\n<!-- pagina_pdf: {numero}; pagina_impresa: NO-DETERMINADA -->\n\n{cuerpo}\n"


NORMA = "".join(
    [
        '<!-- metadatos: {"esquema": "texto-pdf-paginado-v1"} -->\n',
        _pagina(1, "REGLAMENTO DE PRUEBA", "Aprobado por decreto de prueba."),
        _pagina(
            2,
            "TÍTULO I",
            "DISPOSICIONES GENERALES",
            "Artículo 1. Objeto",
            "El presente reglamento regula la reducción de prestaciones.",
            "Artículo 2. Reducción de prestaciones",
            "2.1. La entidad puede ordenar la reducción de prestaciones hasta el 25%.",
        ),
        _pagina(
            3,
            "Artículo 2. Reducción de prestaciones",
            "2.2. No se requiere adenda; basta la publicación de la resolución.",
            "Artículo 5 de la Ley se aplica de forma supletoria.",
            "Artículo 3. Paralización de obra",
            "Cuando la obra está paralizada se registra el reinicio de obra.",
        ),
        _pagina(
            4, "CAPÍTULO II", "SUSPENSIÓN", "Artículo 4. Suspensión del plazo", "La suspensión del plazo se pacta."
        ),
        _pagina(5, "Disposición final única. Vigencia desde su publicación."),
    ]
)

GUIA = "".join(
    _pagina(n, f"{n}.1 Recomendación {nombre}", "Texto de orientación " * 30)
    for n, nombre in enumerate(("uno", "dos", "tres", "cuatro"), 1)
)

OFFICE = """<!-- metadatos: {} -->

<!-- parrafo: 1; seccion: CAPÍTULO III -->
CAPÍTULO III

<!-- parrafo: 2; numeral: 3.3.10; seccion: CAPÍTULO III -->
3.3.10 ELABORACIÓN DEL EXPEDIENTE TÉCNICO DE PRESTACIONES ADICIONALES[^39]

<!-- parrafo: 4; seccion: CAPÍTULO III -->
[PRECISAR QUIÉN ESTARÁ A CARGO]

<!-- tabla: 1; tras_parrafo: 4; seccion: CAPÍTULO III -->
<table>
<tr><td>OBLIGACIONES</td></tr>
</table>

<!-- notas_pie -->

[^39]: Nota de prueba.
"""


def test_pdf_por_articulo_cruza_paginas_y_omite_cabeceras() -> None:
    fragmentos, metricas = segmentar_pdf(NORMA)
    por_clave = {f["clave"]: f for f in fragmentos}
    assert metricas["modo"] == "ARTICULOS" and metricas["lineas_repetidas_omitidas"] == 2
    assert set(por_clave) == {"preambulo", "art-1", "art-2.1", "art-2.2", "art-3", "art-4"}
    assert por_clave["art-2.1"]["texto"].startswith("Artículo 2. Reducción") and por_clave["art-2.1"]["titulo"]
    assert por_clave["art-2.2"]["ubicacion"]["paginas"] == [3]
    assert por_clave["art-2.2"]["articulo"] == "2" and "Artículo 5 de la Ley" in por_clave["art-2.2"]["texto"]
    assert por_clave["art-3"]["ubicacion"]["paginas"] == [3]
    assert por_clave["art-4"]["encabezados"] == ["TÍTULO I DISPOSICIONES GENERALES", "CAPÍTULO II SUSPENSIÓN"]
    assert por_clave["art-4"]["ubicacion"]["paginas"] == [4, 5]
    assert all(CABECERA not in f["texto"] and "Página" not in f["texto"] for f in fragmentos)


def test_pdf_reconoce_variantes_de_encabezado_de_articulo() -> None:
    texto = _pagina(1, "Artículo 1.- Objeto de la norma.", "Texto.", "Artículo 2. - El empleador cumple.")
    texto += _pagina(2, "Artículo 3°.- Ámbito.", "Según el Artículo 2 de la Ley citada.")
    entradas, _ = segmentar_pdf(
        _pagina(1, "CAPÍTULO IX ANEXOS 29", "Artículo 1.- Objeto", "Artículo 2.- Alcance")
        + _pagina(2, "Artículo 1.- Objeto de la norma.", "Texto del objeto.")
        + _pagina(3, "Artículo 2.- Alcance general.", "Texto del alcance.")
        + _pagina(4, "Texto final del alcance.")
    )
    estructuras = {f["clave"]: f["estructura"] for f in entradas}
    assert estructuras["art-1~2"] == estructuras["art-2~2"] == "ENCABEZADO-SIN-CUERPO"
    assert all(not f["encabezados"] for f in entradas)
    fragmentos, metricas = segmentar_pdf(texto)
    assert metricas["modo"] == "ARTICULOS"
    articulos = [f for f in fragmentos if f["estructura"] != "PREAMBULO"]
    assert [f["articulo"] for f in articulos] == ["1", "2", "3"]
    assert articulos[0]["titulo"] == "Objeto de la norma." and "Según el Artículo 2" in articulos[2]["texto"]


def test_pdf_sin_articulos_y_office() -> None:
    fragmentos, metricas = segmentar_pdf(GUIA)
    assert metricas["modo"] == "BLOQUES" and {f["estructura"] for f in fragmentos} == {"BLOQUE-PAGINA"}
    assert [f["ubicacion"]["desde"] for f in fragmentos] == [1, 2, 3, 4]
    fragmentos, _ = segmentar_office(OFFICE)
    por_clave = {f["clave"]: f for f in fragmentos}
    assert set(por_clave) == {"par-1", "par-2", "tabla-1", "notas-pie"}
    assert por_clave["par-2"]["numeral"] == "3.3.10" and por_clave["par-2"]["ubicacion"] == {
        "tipo": "parrafo",
        "desde": 2,
        "hasta": 4,
    }
    assert "[PRECISAR" in por_clave["par-2"]["texto"] and por_clave["par-2"]["encabezados"] == ["CAPÍTULO III"]


def test_expresion_cita_palabras_y_no_acepta_operadores() -> None:
    assert expresion('reducción OR "x" NEAR') == '("reducción" AND "OR" AND "x" AND "NEAR")'
    assert expresion("plazo", terminos=["suspensión del plazo"]) == '("plazo") AND ("suspensión del plazo")'
    assert expresion("acta de recepción", modo="frase") == '"acta de recepción"'
    assert (
        expresion("área usuaria sustenta sobre la reducción", modo="flexible")
        == '("área" AND "usuar"* AND "susten"* AND "reducci"*)'
    )
    assert expresion("de la", modo="flexible") == '("de" AND "la")'


def _sha(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest().upper()


def _biblioteca(raiz: Path) -> None:
    cache = raiz / "01-referencias" / "09-derivados-texto" / "cache"
    documentos = {}
    casos = (("norma", NORMA, "NOR-001"), ("guia", GUIA, "GUI-001"), ("guia", GUIA, "GUI-002"))
    for nombre, texto, identificador in casos:
        original = f"01-referencias/04-contrataciones-publicas/{identificador}/{nombre}.pdf"
        sha = hashlib.sha256(nombre.encode()).hexdigest().upper()
        derivado = cache / identificador / f"{sha[:16].lower()}.md"
        derivado.parent.mkdir(parents=True, exist_ok=True)
        derivado.write_text(texto, encoding="utf-8")
        documentos[original] = {
            "id": identificador,
            "ruta": original,
            "sha256": sha,
            "evaluacion_extraccion": "EXTRAIDO-NATIVO-PENDIENTE-COTEJO",
            "extraccion": {
                "ruta": derivado.relative_to(raiz).as_posix(),
                "sha256_texto": _sha(derivado),
                "estado": "EXTRAIDO-NATIVO-PENDIENTE-COTEJO",
                "metodos": ["nativo", "nativo", "ocr", "nativo", "nativo"],
            },
        }
    (cache / "preparacion-pdf.json").write_text(json.dumps({"documentos": documentos}), encoding="utf-8")
    (raiz / "02-procesos" / "S4-3-2-7-gestion-reducciones").mkdir(parents=True)
    vocabulario = {
        "esquema": "temas-busqueda-v1",
        "estado": "BORRADOR-IA",
        "temas": [
            {"id": "reduccion", "etiqueta": "Reducción", "procesos": ["S4.3.2.7"],
             "terminos": ["reducción de prestaciones"], "relacionados": ["paralizacion"]},
            {"id": "paralizacion", "etiqueta": "Paralización", "procesos": [],
             "terminos": ["paralizada", "reinicio de obra"], "relacionados": []},
        ],
    }  # fmt: skip
    (raiz / VOCABULARIO).parent.mkdir(parents=True)
    (raiz / VOCABULARIO).write_text(json.dumps(vocabulario, ensure_ascii=False), encoding="utf-8")


def test_segmentar_indexar_buscar_contexto_y_temas(tmp_path: Path) -> None:
    _biblioteca(tmp_path)
    resultado = segmentar(tmp_path)
    assert resultado["estados"] == {"SEGMENTADO": 3} and resultado["cobertura_minima"] == 1.0
    assert segmentar(tmp_path)["reutilizados"] == 3
    with pytest.raises(ErrorDominio):
        buscar(tmp_path, "plazo")
    assert indexar(tmp_path)["fragmentos"] >= 14  # La copia idéntica de la guía conserva fragmentos propios.

    hallado = buscar(tmp_path, "reducción prestaciones", limite=3)
    assert hallado["resultados"][0]["documento"]["id"] == "NOR-001" and not hallado["indice_desactualizado"]
    assert "«" in hallado["resultados"][0]["extracto"]
    assert buscar(tmp_path, "publicación resolución", filtros={"articulo": "2"})["resultados"][0]["numeral"] == "2.2"
    assert buscar(tmp_path, "reducción", filtros={"id_documento": "GUI-001"})["coincidencias"] == 0
    assert buscar(tmp_path, "", filtros={"articulo": "2"})["coincidencias"] == 2
    assert buscar(tmp_path, "reducciones prestación", modo="todas")["coincidencias"] == 0
    flexible = buscar(tmp_path, "reducciones prestación", modo="flexible", limite=4)
    assert flexible["coincidencias"] >= 2 and not any(r.get("relajado") for r in flexible["resultados"][:2])
    relajada = buscar(tmp_path, "paralizada inexistentepalabra", modo="flexible", limite=3)
    assert relajada["coincidencias"] == 0 and relajada["resultados"][0]["relajado"]
    acotado = buscar(tmp_path, "orientación", max_caracteres=10)
    assert acotado["devueltos"] == 1 and acotado["truncado"]
    con_ocr = buscar(tmp_path, "adenda")["resultados"][0]
    assert con_ocr["metodos"] == ["ocr"] and con_ocr["ubicacion"]["paginas"] == [3]

    vecinos = contexto(tmp_path, con_ocr["id"], vecinos=1)["fragmentos"]
    assert [f["central"] for f in vecinos] == [False, True, False]
    assert contexto(tmp_path, con_ocr["id"], vecinos=1, max_caracteres=10)["fragmentos"][0]["central"]

    terminos, usados = terminos_de(tmp_path, "reduccion", con_relacionados=True)
    assert usados == ["reduccion", "paralizacion"] and "reinicio de obra" in terminos
    assert comprobar(tmp_path)["errores"] == 0
    sugerencias = sugerir(tmp_path)
    assert sugerencias["por_tema"]["reduccion"] >= 2 and sugerencias["por_tema"]["paralizacion"] == 1
    assert comprobar(tmp_path)["sugerencias"] == sugerencias["sugerencias"]

    (tmp_path / VOCABULARIO).write_text(
        json.dumps({"esquema": "temas-busqueda-v1", "estado": "VALIDADO", "temas": [
            {"id": "x", "etiqueta": "X", "procesos": ["S9.9"], "terminos": ["a"], "relacionados": ["x"],
             "equivalentes": ["b"]}]}),
        encoding="utf-8",
    )  # fmt: skip
    codigos = {h["codigo"] for h in comprobar(tmp_path)["hallazgos"]}
    assert {"ESTADO", "PROCESO-INEXISTENTE", "RELACION-INVALIDA", "EQUIVALENCIA-NO-PERMITIDA"} <= codigos
    with pytest.raises(ErrorDominio):
        sugerir(tmp_path)


def test_banco_de_preguntas_metricas_conocidas(tmp_path: Path) -> None:
    from mesa_modelamiento.fuentes_pruebas import BANCOS, medir, preparar

    _biblioteca(tmp_path)
    segmentar(tmp_path)
    indexar(tmp_path)
    norma = "01-referencias/04-contrataciones-publicas/NOR-001/norma.pdf"
    banco = {
        "esquema": "banco-recuperacion-v1",
        "estado": "PROVISIONAL-IA",
        "preguntas": [
            {"id": "P1", "tipo": "POSITIVA", "consulta": "publicación resolución adenda",
             "esperados": [{"ruta": norma, "clave": "art-2.2"}]},
            {"id": "P2", "tipo": "POSITIVA", "consulta": "reinicio", "tema": "paralizacion",
             "esperados": [{"ruta": norma, "clave": "art-3"}]},
            {"id": "P3", "tipo": "POSITIVA", "consulta": "inexistentepalabra",
             "esperados": [{"ruta": norma, "clave": "art-4"}]},
            {"id": "N1", "tipo": "NEGATIVA", "consulta": "orientación",
             "no_esperados": [{"ruta": norma, "clave": "art-1"}]},
        ],
    }  # fmt: skip
    (tmp_path / BANCOS).mkdir(parents=True)
    (tmp_path / BANCOS / "piloto.json").write_text(json.dumps(banco, ensure_ascii=False), encoding="utf-8")
    preparado = preparar(tmp_path, "piloto")
    assert preparado["hallazgos"] == [] and preparado["positivas"] == 3 and all(preparado["resueltas"][0]["fragmentos"])
    resultado = medir(tmp_path, "piloto")
    assert resultado["metricas"]["acierto@1"] == round(2 / 3, 3) and resultado["metricas"]["acierto@10"] == round(
        2 / 3, 3
    )
    assert resultado["metricas"]["mrr"] == round(2 / 3, 3) and resultado["metricas"]["negativas_limpias"] == 1.0
    assert (tmp_path / resultado["archivo"]).is_file()

    banco["preguntas"].append(
        {"id": "P1", "tipo": "POSITIVA", "consulta": "x", "esperados": [{"ruta": norma, "clave": "art-99"}]}
    )
    (tmp_path / BANCOS / "piloto.json").write_text(json.dumps(banco, ensure_ascii=False), encoding="utf-8")
    codigos = {h["codigo"] for h in preparar(tmp_path, "piloto")["hallazgos"]}
    assert codigos == {"ID-REPETIDO", "PASAJE-INEXISTENTE"}
    with pytest.raises(ErrorDominio):
        medir(tmp_path, "piloto")
    with pytest.raises(ErrorDominio):
        preparar(tmp_path, "../fuera")
