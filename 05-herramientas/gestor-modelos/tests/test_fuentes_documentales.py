"""Controles de la cadena PDF sin depender de la biblioteca institucional."""

from pathlib import Path

import pytest
from pypdf import PdfReader, PdfWriter

from mesa_modelamiento.fuentes_extraccion import (
    evaluar_extraccion,
    extraer_nativo,
    preparar_cotejo,
    resolver_colisiones_cache,
)
from mesa_modelamiento.fuentes_preparacion import (
    cargar_manifiesto,
    diagnosticar_texto,
    guardar_manifiesto,
    inventariar,
    planificar_extraccion,
)


def _biblioteca(raiz: Path) -> Path:
    original = raiz / "01-referencias" / "04-contrataciones-publicas" / "originales" / "ejemplo.pdf"
    original.parent.mkdir(parents=True)
    escritor = PdfWriter()
    escritor.add_blank_page(width=612, height=792)
    with original.open("wb") as salida:
        escritor.write(salida)
    catalogo = raiz / "01-referencias" / "00-catalogo" / "registro-descargas.csv"
    catalogo.parent.mkdir(parents=True)
    catalogo.write_text(
        "id_fuente,archivo,url_final,sha256\n"
        "PRUEBA-001,01-referencias/04-contrataciones-publicas/originales/ejemplo.pdf,https://example.org/a.pdf,\n",
        encoding="utf-8",
    )
    return original


def test_inventario_diagnostico_y_plan_no_mutan_original(tmp_path: Path) -> None:
    original = _biblioteca(tmp_path)
    contenido = original.read_bytes()
    assert inventariar(tmp_path)["pdf_presentes"] == 1
    assert diagnosticar_texto(tmp_path)["paginas_medidas"] == 1
    assert planificar_extraccion(tmp_path)["estados"] == {"OCR-INTEGRAL": 1}
    dato = next(iter(cargar_manifiesto(tmp_path)["documentos"].values()))
    assert dato["plan"]["ocr"] == [1]
    assert dato["hash_coincide"]
    assert original.read_bytes() == contenido
    assert inventariar(tmp_path)["pdf_presentes"] == 1
    assert diagnosticar_texto(tmp_path)["procesados"] == 0


def test_extraccion_paginada_y_cotejo_marcan_ocr_pendiente(tmp_path: Path) -> None:
    _biblioteca(tmp_path)
    inventariar(tmp_path)
    diagnosticar_texto(tmp_path)
    planificar_extraccion(tmp_path)
    assert extraer_nativo(tmp_path)["procesados"] == 1
    evaluacion = evaluar_extraccion(tmp_path)
    assert evaluacion["paginas_ocr_pendientes"] == 1
    dato = next(iter(cargar_manifiesto(tmp_path)["documentos"].values()))
    texto = (tmp_path / dato["extraccion"]["ruta"]).read_text(encoding="utf-8")
    assert "<!-- pagina_pdf: 1; pagina_impresa: NO-DETERMINADA -->" in texto
    assert "OCR PENDIENTE" in texto
    cotejo = preparar_cotejo(tmp_path, "PRUEBA-001", 1)
    assert (tmp_path / cotejo["vista"]).is_file()


def test_ocr_en_copia_derivada_reemplaza_solo_pagina_pendiente(tmp_path: Path, monkeypatch) -> None:
    from mesa_modelamiento import fuentes_ocr
    from mesa_modelamiento.fuentes_extraccion import extraer_ocr

    original = _biblioteca(tmp_path)
    contenido = original.read_bytes()
    inventariar(tmp_path)
    diagnosticar_texto(tmp_path)
    planificar_extraccion(tmp_path)
    extraer_nativo(tmp_path)
    vistos = []

    def simular_ocr(ruta: Path, titulo: str) -> dict:
        vistos.append((ruta.resolve(), titulo))
        assert ruta.is_file()
        assert ruta.resolve() != original.resolve()
        return {"job_id": "prueba", "paginas": ["Texto reconocido"], "baja_confianza": []}

    monkeypatch.setattr(fuentes_ocr, "procesar_lote", simular_ocr)
    assert extraer_ocr(tmp_path)["paginas_ocr"] == 1
    dato = next(iter(cargar_manifiesto(tmp_path)["documentos"].values()))
    texto = (tmp_path / dato["extraccion"]["ruta"]).read_text(encoding="utf-8")
    assert "Texto reconocido" in texto
    assert dato["extraccion"]["metodos"] == ["ocr"]
    assert original.read_bytes() == contenido
    assert extraer_ocr(tmp_path)["paginas_ocr"] == 0
    assert len(vistos) == 1


def test_ocr_sin_url_exige_id_explicito(tmp_path: Path, monkeypatch) -> None:
    from mesa_modelamiento import fuentes_ocr
    from mesa_modelamiento.fuentes_extraccion import extraer_ocr

    _biblioteca(tmp_path)
    registro = tmp_path / "01-referencias" / "00-catalogo" / "registro-descargas.csv"
    registro.write_text(registro.read_text(encoding="utf-8").replace("https://example.org/a.pdf", ""), encoding="utf-8")
    inventariar(tmp_path)
    diagnosticar_texto(tmp_path)
    planificar_extraccion(tmp_path)
    extraer_nativo(tmp_path)
    vistos = []

    def simular_ocr(_ruta: Path, _titulo: str) -> dict:
        vistos.append(True)
        return {"job_id": "prueba", "paginas": ["Texto"], "baja_confianza": []}

    monkeypatch.setattr(fuentes_ocr, "procesar_lote", simular_ocr)
    assert extraer_ocr(tmp_path)["documentos_intentados"] == 0
    assert not vistos
    assert extraer_ocr(tmp_path, permitir_ids_sin_url=["PRUEBA-001"])["paginas_ocr"] == 1


def test_evaluacion_detecta_cache_alterada(tmp_path: Path) -> None:
    _biblioteca(tmp_path)
    inventariar(tmp_path)
    diagnosticar_texto(tmp_path)
    planificar_extraccion(tmp_path)
    extraer_nativo(tmp_path)
    dato = next(iter(cargar_manifiesto(tmp_path)["documentos"].values()))
    ruta = tmp_path / dato["extraccion"]["ruta"]
    ruta.write_text(ruta.read_text(encoding="utf-8") + "cambio no registrado\n", encoding="utf-8")
    assert evaluar_extraccion(tmp_path)["estados"] == {"CACHE-ALTERADA": 1}


def test_pdf_duplicados_con_mismo_id_conservan_procedencia_distinta(tmp_path: Path, monkeypatch) -> None:
    from mesa_modelamiento import fuentes_ocr
    from mesa_modelamiento.fuentes_extraccion import extraer_ocr

    primero = _biblioteca(tmp_path)
    segundo = primero.with_name("copia.pdf")
    segundo.write_bytes(primero.read_bytes())
    registro = tmp_path / "01-referencias" / "00-catalogo" / "registro-descargas.csv"
    registro.write_text(
        registro.read_text(encoding="utf-8")
        + "PRUEBA-001,01-referencias/04-contrataciones-publicas/originales/copia.pdf,https://example.org/b.pdf,\n",
        encoding="utf-8",
    )
    assert inventariar(tmp_path)["duplicados_sha256"] == 1
    diagnosticar_texto(tmp_path)
    planificar_extraccion(tmp_path)
    extraer_nativo(tmp_path)
    rutas = [d["extraccion"]["ruta"] for d in cargar_manifiesto(tmp_path)["documentos"].values()]
    assert len(set(rutas)) == 2
    assert resolver_colisiones_cache(tmp_path)["derivados_separados"] == 0
    assert evaluar_extraccion(tmp_path)["estados"] == {"OCR-PENDIENTE": 2}
    with pytest.raises(Exception, match="ID no identifica"):
        preparar_cotejo(tmp_path, "PRUEBA-001", 1)
    vista = preparar_cotejo(
        tmp_path,
        "PRUEBA-001",
        1,
        "01-referencias/04-contrataciones-publicas/originales/copia.pdf",
    )
    assert (tmp_path / vista["vista"]).is_file()
    llamadas = []

    def simular_ocr(_ruta: Path, _titulo: str) -> dict:
        llamadas.append(len(llamadas) + 1)
        return {"job_id": str(llamadas[-1]), "paginas": [f"Texto {llamadas[-1]}"], "baja_confianza": []}

    monkeypatch.setattr(fuentes_ocr, "procesar_lote", simular_ocr)
    assert extraer_ocr(tmp_path)["paginas_ocr"] == 2
    documentos = list(cargar_manifiesto(tmp_path)["documentos"].values())
    textos = [(tmp_path / d["extraccion"]["ruta"]).read_text(encoding="utf-8") for d in documentos]
    assert "Texto 1" in textos[0] and "Texto 2" in textos[1]
    assert len({d["extraccion"]["ruta"] for d in documentos}) == 2


def test_ocr_reanuda_solo_paginas_pendientes(tmp_path: Path, monkeypatch) -> None:
    from mesa_modelamiento import fuentes_ocr
    from mesa_modelamiento.fuentes_extraccion import extraer_ocr

    original = _biblioteca(tmp_path)
    escritor = PdfWriter()
    escritor.add_blank_page(width=612, height=792)
    escritor.add_blank_page(width=612, height=792)
    with original.open("wb") as salida:
        escritor.write(salida)
    inventariar(tmp_path)
    diagnosticar_texto(tmp_path)
    planificar_extraccion(tmp_path)
    extraer_nativo(tmp_path)
    manifiesto = cargar_manifiesto(tmp_path)
    dato = next(iter(manifiesto["documentos"].values()))
    dato["ocr_lotes"] = {"1": "trabajo-previo"}
    carpeta = (tmp_path / dato["extraccion"]["ruta"]).with_suffix(".ocr")
    carpeta.mkdir()
    (carpeta / "p1.md").write_text("Primera página", encoding="utf-8")
    guardar_manifiesto(tmp_path, manifiesto)

    def simular_ocr(ruta: Path, _titulo: str) -> dict:
        assert len(PdfReader(ruta).pages) == 1
        return {"job_id": "trabajo-nuevo", "paginas": ["Segunda página"], "baja_confianza": []}

    monkeypatch.setattr(fuentes_ocr, "procesar_lote", simular_ocr)
    assert extraer_ocr(tmp_path)["paginas_ocr"] == 1
    dato = next(iter(cargar_manifiesto(tmp_path)["documentos"].values()))
    texto = (tmp_path / dato["extraccion"]["ruta"]).read_text(encoding="utf-8")
    assert "Primera página" in texto and "Segunda página" in texto
