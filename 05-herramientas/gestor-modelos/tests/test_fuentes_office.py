"""Conversión Office con documentos sintéticos; no depende de la biblioteca institucional."""

import io
import re
import zipfile
from pathlib import Path

from mesa_modelamiento.fuentes_docx import convertir_docx
from mesa_modelamiento.fuentes_indice import generar_indice
from mesa_modelamiento.fuentes_numeracion import formatear
from mesa_modelamiento.fuentes_office import cargar_manifiesto_office, extraer_office
from mesa_modelamiento.fuentes_ooxml import convertir_pptx, fichar_xlsx

NS_W = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
HOJA = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"


def _paquete(partes: dict[str, str]) -> bytes:
    salida = io.BytesIO()
    with zipfile.ZipFile(salida, "w") as paquete:
        for nombre, contenido in partes.items():
            paquete.writestr(nombre, contenido)
    return salida.getvalue()


def _p(texto: str, num: str | None = None, nivel: int = 0, estilo: str | None = None, extra: str = "") -> str:
    ppr = f'<w:pStyle w:val="{estilo}"/>' if estilo else ""
    if num:
        ppr += f'<w:numPr><w:ilvl w:val="{nivel}"/><w:numId w:val="{num}"/></w:numPr>'
    return f"<w:p><w:pPr>{ppr}</w:pPr><w:r><w:t>{texto}</w:t></w:r>{extra}</w:p>"


def _nivel(ilvl: int, formato: str, texto: str) -> str:
    return (
        f'<w:lvl w:ilvl="{ilvl}"><w:start w:val="1"/><w:numFmt w:val="{formato}"/><w:lvlText w:val="{texto}"/></w:lvl>'
    )


NUMERACION = (
    f"<w:numbering {NS_W}>"
    f'<w:abstractNum w:abstractNumId="1">{_nivel(0, "decimal", "%1.")}{_nivel(1, "decimal", "%1.%2.")}'
    f"{_nivel(2, 'lowerLetter', '%3)')}</w:abstractNum>"
    f'<w:abstractNum w:abstractNumId="2">{_nivel(0, "bullet", "•")}</w:abstractNum>'
    '<w:num w:numId="1"><w:abstractNumId w:val="1"/></w:num>'
    '<w:num w:numId="2"><w:abstractNumId w:val="2"/></w:num>'
    '<w:num w:numId="3"><w:abstractNumId w:val="1"/>'
    '<w:lvlOverride w:ilvl="0"><w:startOverride w:val="5"/></w:lvlOverride></w:num>'
    "</w:numbering>"
)
ESTILOS = (
    f"<w:styles {NS_W}>"
    '<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>'
    '<w:style w:type="paragraph" w:styleId="Titulo1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/>'
    '<w:pPr><w:numPr><w:numId w:val="1"/></w:numPr><w:outlineLvl w:val="0"/></w:pPr></w:style>'
    "</w:styles>"
)
TABLA = (
    "<w:tbl>"
    '<w:tr><w:trPr><w:tblHeader/></w:trPr><w:tc><w:tcPr><w:gridSpan w:val="2"/></w:tcPr>'
    "<w:p><w:r><w:t>Encabezado combinado</w:t></w:r></w:p></w:tc></w:tr>"
    '<w:tr><w:tc><w:tcPr><w:vMerge w:val="restart"/></w:tcPr><w:p><w:r><w:t>Vertical</w:t></w:r></w:p></w:tc>'
    "<w:tc><w:p><w:r><w:t>B2 &amp; más</w:t></w:r></w:p></w:tc></w:tr>"
    "<w:tr><w:tc><w:tcPr><w:vMerge/></w:tcPr><w:p/></w:tc>"
    "<w:tc><w:p><w:r><w:t>B3</w:t></w:r></w:p></w:tc></w:tr>"
    "</w:tbl>"
)
CUERPO = "".join(
    [
        _p("Disposiciones", estilo="Titulo1"),
        _p("Alcance", "1", 1),
        _p("primero", "1", 2),
        _p("segundo", "1", 2),
        _p("Plazo", "1", 1),
        _p("tercero", "1", 2),
        _p("viñeta", "2", 0),
        '<w:p><w:r><w:br w:type="page"/><w:t>Tras salto </w:t></w:r>'
        "<w:del><w:r><w:delText>BORRADO</w:delText></w:r></w:del>"
        '<w:ins><w:r><w:t>insertado</w:t></w:r></w:ins><w:r><w:footnoteReference w:id="2"/></w:r></w:p>',
        TABLA,
        _p("Obligaciones", estilo="Titulo1"),
        _p("Reinicio", "3", 0),
        _p("4.4.1. Texto con numeral escrito"),
    ]
)
NOTAS = (
    f"<w:footnotes {NS_W}>"
    '<w:footnote w:type="separator" w:id="-1"><w:p><w:r><w:separator/></w:r></w:p></w:footnote>'
    '<w:footnote w:id="2"><w:p><w:r><w:t>Nota de prueba</w:t></w:r></w:p></w:footnote>'
    "</w:footnotes>"
)


def _docx() -> bytes:
    return _paquete(
        {
            "word/document.xml": f"<w:document {NS_W}><w:body>{CUERPO}</w:body></w:document>",
            "word/numbering.xml": NUMERACION,
            "word/styles.xml": ESTILOS,
            "word/footnotes.xml": NOTAS,
        }
    )


def _pptx() -> bytes:
    ns = (
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
        'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    )
    rel = 'xmlns="http://schemas.openxmlformats.org/package/2006/relationships"'
    forma = (
        "<p:sp><p:nvSpPr><p:nvPr>{ph}</p:nvPr></p:nvSpPr>"
        "<p:txBody><a:p><a:r><a:t>{t}</a:t></a:r></a:p></p:txBody></p:sp>"
    )
    arbol = forma.format(ph='<p:ph type="title"/>', t="Mapa de procesos") + forma.format(ph="", t="Nivel 0")
    return _paquete(
        {
            "ppt/presentation.xml": f'<p:presentation {ns}><p:sldIdLst><p:sldId id="256" r:id="rId1"/>'
            "</p:sldIdLst></p:presentation>",
            "ppt/_rels/presentation.xml.rels": f'<Relationships {rel}><Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
            'Target="slides/slide1.xml"/></Relationships>',
            "ppt/slides/slide1.xml": f"<p:sld {ns}><p:cSld><p:spTree>{arbol}</p:spTree></p:cSld></p:sld>",
        }
    )


def _xlsx() -> bytes:
    ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
    nsr = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
    rel = 'xmlns="http://schemas.openxmlformats.org/package/2006/relationships"'
    return _paquete(
        {
            "xl/workbook.xml": f'<workbook {ns} {nsr}><sheets><sheet name="Datos" sheetId="1" r:id="rId1"/>'
            '<sheet name="Oculta" sheetId="2" state="hidden" r:id="rId2"/></sheets></workbook>',
            "xl/_rels/workbook.xml.rels": f"<Relationships {rel}>"
            f'<Relationship Id="rId1" Type="{HOJA}" Target="worksheets/sheet1.xml"/>'
            f'<Relationship Id="rId2" Type="{HOJA}" Target="/xl/worksheets/sheet2.xml"/></Relationships>',
            "xl/sharedStrings.xml": f"<sst {ns}><si><t>Meta</t></si><si><t>Monto</t></si></sst>",
            "xl/worksheets/sheet1.xml": f'<worksheet {ns}><dimension ref="A1:B2"/><sheetData>'
            '<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c></row>'
            '<row r="2"><c r="A2"><v>10</v></c><c r="B2"><f>A2*2</f><v>20</v></c></row>'
            '</sheetData><mergeCells count="1"><mergeCell ref="A3:B3"/></mergeCells></worksheet>',
            "xl/worksheets/sheet2.xml": f"<worksheet {ns}><sheetData/></worksheet>",
        }
    )


def test_numeracion_multinivel_tablas_y_notas() -> None:
    texto, resumen = convertir_docx(_docx())
    assert "# 1. Disposiciones" in texto
    for esperado in ("1.1. Alcance", "a) primero", "b) segundo", "1.2. Plazo", "a) tercero", "- viñeta"):
        assert f"\n{esperado}\n" in texto
    assert "# 2. Obligaciones" in texto
    assert "\n5. Reinicio\n" in texto
    assert "<!-- salto_pagina -->" in texto
    assert "BORRADO" not in texto and "Tras salto insertado[^2]" in texto
    assert "[^2]: Nota de prueba" in texto
    assert '<th colspan="2">Encabezado combinado</th>' in texto
    assert '<td rowspan="2">Vertical</td><td>B2 &amp; más</td>' in texto
    assert "<tr><td>B3</td></tr>" in texto
    assert re.search(r"<!-- parrafo: 2; numeral: 1\.1\.; seccion: 1\. Disposiciones -->", texto)
    assert "numeral_texto: 4.4.1." in texto
    assert resumen["tablas"] == 1 and resumen["notas_pie"] == 1 and resumen["saltos_pagina"] == 1
    assert resumen["numerales_reconstruidos"] == 8 and resumen["vinetas"] == 1


def test_formatos_de_numero() -> None:
    assert formatear(28, "lowerLetter") == "bb"
    assert formatear(14, "upperRoman") == "XIV"
    assert formatear(3, "decimalZero") == "03"


def test_pptx_y_ficha_xlsx() -> None:
    texto, resumen = convertir_pptx(_pptx())
    assert texto.startswith("<!-- diapositiva: 1 -->") and "## Mapa de procesos" in texto and "Nivel 0" in texto
    assert resumen["diapositivas"] == 1
    hojas = fichar_xlsx(_xlsx())["hojas"]
    assert hojas[0]["primera_fila_con_datos"] == {"fila": 1, "valores": ["Meta", "Monto"]}
    assert hojas[0]["formulas"] == 1 and hojas[0]["celdas_combinadas"] == 1 and hojas[0]["rango"] == "A1:B2"
    assert hojas[1]["estado"] == "hidden" and hojas[1]["filas_con_datos"] == 0


def _biblioteca(raiz: Path) -> dict[str, Path]:
    carpeta = raiz / "01-referencias" / "04-contrataciones-publicas" / "bases"
    carpeta.mkdir(parents=True)
    archivos = {"docx": carpeta / "bases obra.docx", "pptx": carpeta / "anexo.pptx", "xlsx": carpeta / "anexo.xlsx"}
    archivos["docx"].write_bytes(_docx())
    archivos["pptx"].write_bytes(_pptx())
    archivos["xlsx"].write_bytes(_xlsx())
    (carpeta / "danado.docx").write_bytes(b"no es un zip")
    catalogo = raiz / "01-referencias" / "00-catalogo" / "registro-descargas.csv"
    catalogo.parent.mkdir(parents=True)
    catalogo.write_text(
        "id_fuente,archivo,url_final,sha256\n"
        "BAS-001,01-referencias/04-contrataciones-publicas/bases/bases obra.docx,https://example.org/b.docx,\n"
        "BAS-002,01-referencias/04-contrataciones-publicas/bases/ausente.xlsx,https://example.org/c.xlsx,\n",
        encoding="utf-8",
    )
    return archivos


def test_extraccion_office_reanudable_e_indice_enlazado(tmp_path: Path) -> None:
    archivos = _biblioteca(tmp_path)
    contenidos = {k: v.read_bytes() for k, v in archivos.items()}
    resultado = extraer_office(tmp_path)
    assert resultado["presentes"] == {"docx": 2, "pptx": 1, "xlsx": 1}
    assert resultado["estados"] == {
        "EXTRAIDO-ESTRUCTURADO-PENDIENTE-COTEJO": 2,
        "FICHADO": 1,
        "NO-CONFIABLE": 1,
    }
    assert resultado["faltantes_catalogo"] == ["01-referencias/04-contrataciones-publicas/bases/ausente.xlsx"]
    assert {k: v.read_bytes() for k, v in archivos.items()} == contenidos
    dato = cargar_manifiesto_office(tmp_path)["documentos"][archivos["docx"].relative_to(tmp_path).as_posix()]
    assert dato["id"] == "BAS-001"
    derivado = (tmp_path / dato["extraccion"]["ruta"]).read_text(encoding="utf-8")
    assert '"unidad_ancla": "parrafo"' in derivado and "1.1. Alcance" in derivado
    segundo = extraer_office(tmp_path)
    assert segundo["reutilizados"] == 4 and segundo["procesados"] == 0

    indice = generar_indice(tmp_path)
    assert indice["documentos"] == 4 and indice["con_texto"] == 2
    ruta_indice = tmp_path / indice["indice"]
    enlaces = re.findall(r"\]\(([^)]+)\)", ruta_indice.read_text(encoding="utf-8"))
    assert len(enlaces) == 6
    for enlace in enlaces:
        assert (ruta_indice.parent / enlace.replace("%20", " ")).is_file(), enlace
