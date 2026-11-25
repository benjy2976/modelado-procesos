"""Canales de conocimiento de solo lectura (DEC-066) compartidos por CLI y MCP."""

import asyncio
import json
from pathlib import Path

import pytest

from mesa_modelamiento import conocimiento as c
from mesa_modelamiento.mcp_adapter import crear_servidor
from mesa_modelamiento.repositorio import ErrorDominio, RepositorioProcesos

NOTA = (
    "---\ntipo: guia\nestado_documento: VIGENTE\ntags:\n  - tema/conocimiento\nproceso:\n  - S4.3\n---\n\n"
    "# Guía {n}\n\nTexto sobre paralización. Ver [glosario](../glosario.md).\n"
)


@pytest.fixture
def raiz(tmp_path: Path) -> Path:
    (tmp_path / "03-conocimiento" / "fuentes").mkdir(parents=True)
    (tmp_path / "03-conocimiento" / "fuentes" / "guia-a.md").write_text(NOTA.format(n="A"), encoding="utf-8")
    (tmp_path / "03-conocimiento" / "reglas").mkdir()
    (tmp_path / "03-conocimiento" / "reglas" / "reg-x-001.yaml").write_text(
        "id_regla: REG-X-001\ntitulo: Regla de prueba\ndominio: contrataciones\naplicabilidad:\n  procesos: [S4.3]\n"
        "validacion:\n  estado: BORRADOR-IA\nfuente:\n  id_documento: DOC-1\n",
        encoding="utf-8",
    )
    originales = tmp_path / "01-referencias" / "01-institucionales-grh" / "originales"
    originales.mkdir(parents=True)
    (originales / "secreto.md").write_text("# No", encoding="utf-8")
    (tmp_path / "glosario.md").write_text(
        "# Glosario\n\n| Termino | Definicion de trabajo | Fuente pendiente |\n|---|---|---|\n"
        "| Paquete de contexto | Conjunto mínimo de archivos. | No |\n",
        encoding="utf-8",
    )
    (tmp_path / "00-gobernanza").mkdir()
    (tmp_path / "00-gobernanza" / "registro-decisiones.md").write_text(
        "| ID | Fecha | Decision | Motivo | Impacto | Responsable |\n|---|---|---|---|---|---|\n"
        "| DEC-001 | 2026-01-01 | Primera | M | I | R |\n\n| DEC-002 | 2026-01-02 | Segunda sobre S4.3 | M | I | R |\n",
        encoding="utf-8",
    )
    cache = tmp_path / "01-referencias" / "09-derivados-texto" / "cache"
    (cache / "DOC-1").mkdir(parents=True)
    (cache / "DOC-1" / "abc.md").write_text(
        '<!-- metadatos: {"id_documento": "DOC-1"} -->\n<!-- pagina_pdf: 1; pagina_impresa: 1 -->\nUno\n'
        "<!-- pagina_pdf: 2; pagina_impresa: 2 -->\nDos\n",
        encoding="utf-8",
    )
    (cache / "preparacion-pdf.json").write_text(
        json.dumps({"documentos": {"01-referencias/04-x/doc.pdf": {
            "id": "DOC-1", "ruta": "01-referencias/04-x/doc.pdf", "titulo": "Documento uno",
            "plan": {"estado": "NATIVO"},
            "extraccion": {"ruta": "01-referencias/09-derivados-texto/cache/DOC-1/abc.md"}}}}),
        encoding="utf-8",
    )  # fmt: skip
    return tmp_path


def test_notas_filtradas_y_lectura_acotada(raiz: Path) -> None:
    listado = c.listar_notas(raiz, tipo="guia", proceso="S4.3", texto="paralizacion")
    assert listado["total"] == 1 and listado["resultados"][0]["titulo"] == "Guía A"
    nota = c.leer_nota(raiz, "03-conocimiento/fuentes/guia-a.md", max_caracteres=500)
    assert nota["propiedades"]["tipo"] == "guia" and nota["enlaces"] == ["03-conocimiento/glosario.md"]
    for prohibida in ("01-referencias/01-institucionales-grh/originales/secreto.md", "../fuera.md", "99-temporal/x.md"):
        with pytest.raises(ErrorDominio):
            c.leer_nota(raiz, prohibida)


def test_biblioteca_reglas_glosario_y_decisiones(raiz: Path) -> None:
    assert c.listar_documentos(raiz, texto="uno")["resultados"][0]["id"] == "DOC-1"
    texto = c.leer_texto_documento(raiz, "DOC-1", pagina_desde=2, paginas=1)
    assert texto["paginas"] == [2] and "Dos" in texto["texto"] and "Uno" not in texto["texto"]
    assert [r["id"] for r in c.listar_reglas(raiz, proceso="S4.3.2.6")["reglas"]] == ["REG-X-001"]
    assert c.listar_reglas(raiz, proceso="S1")["total"] == 0
    assert c.leer_regla(raiz, "REG-X-001")["regla"]["titulo"] == "Regla de prueba"
    assert c.buscar_glosario(raiz, "contexto")["total"] == 1
    decisiones = c.buscar_decisiones(raiz, texto="S4.3")["decisiones"]
    assert [d["id"] for d in decisiones] == ["DEC-002"]
    assert c.buscar_decisiones(raiz, identificador="DEC-001")["decisiones"][0]["decision"] == "Primera"
    with pytest.raises(ErrorDominio):
        c.etiquetas(raiz, "aplicar")


def test_mcp_expone_los_canales_de_conocimiento(raiz: Path) -> None:
    servidor = crear_servidor(RepositorioProcesos(raiz))
    nombres = {h.name for h in asyncio.run(servidor.list_tools())}
    assert {"buscar_notas", "leer_nota", "listar_documentos", "leer_documento", "leer_texto_documento",
            "listar_temas", "listar_reglas", "leer_regla", "buscar_glosario", "buscar_decisiones",
            "revisar_etiquetas", "paquete_contexto"} <= nombres  # fmt: skip
