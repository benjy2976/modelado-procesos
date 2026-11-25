"""Etapas de resolución de observaciones (DEC-065) por servicio, API y MCP."""

import asyncio
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mesa_modelamiento.api import crear_aplicacion
from mesa_modelamiento.mcp_adapter import crear_servidor
from mesa_modelamiento.repositorio import ErrorDominio, RepositorioProcesos
from mesa_modelamiento.resolucion import ServicioResolucion


@pytest.fixture
def repositorio(tmp_path: Path) -> RepositorioProcesos:
    carpeta = tmp_path / "02-procesos" / "S4-prueba" / "S4-3-ejecucion"
    carpeta.mkdir(parents=True)
    (carpeta / "S4-3-diagrama-proceso.bpmn").write_text(
        '<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"><process id="P"><task id="Tarea_1" />'
        "</process></definitions>",
        encoding="utf-8",
    )
    (carpeta / "S4-3-diagrama-proceso-tabla.md").write_text(
        "---\ncodigo_proceso: S4.3\n---\n\n## Elementos\n\n| ID | Numero | Tipo | Nombre |\n| --- | --- | --- | --- |\n"
        "| Tarea_1 | 1 | tarea | Revisar |\n",
        encoding="utf-8",
    )
    (carpeta / "S4-3-sustento.md").write_text("# Sustento\n", encoding="utf-8")
    return RepositorioProcesos(tmp_path)


def _revision(servicio: ServicioResolucion) -> str:
    return servicio.listar("S4.3")["revision"]


def test_ciclo_completo_de_etapas(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioResolucion(repositorio)
    obs = servicio.agregar(
        "S4.3", elemento="Tarea_1", texto="¿Quién revisa?", autor="Equipo", revision_esperada=_revision(servicio)
    )
    assert obs["etapa"] == "REGISTRADA"
    identificador = obs["id"]
    opciones = [
        {"titulo": "El coordinador", "detalle": "Solo SGGOS", "efecto": "CAMBIO-MODELO", "elementos": ["Tarea_1"],
         "recomendada": True},
        {"titulo": "Aclarar en el sustento", "detalle": "Sin cambio de flujo", "efecto": "ACLARACION"},
    ]  # fmt: skip
    with pytest.raises(ErrorDominio, match="etapa REGISTRADA"):
        servicio.registrar_propuesta(
            "S4.3", identificador, opciones=opciones, autor="Claudia", revision_esperada=_revision(servicio)
        )
    analizada = servicio.registrar_analisis(
        "S4.3", identificador, texto="Falta el responsable.", clase="EXPLICACION-AUSENTE", autor="Claudia",
        revision_esperada=_revision(servicio), fuentes=["DEC-063"],
    )  # fmt: skip
    assert analizada["etapa"] == "EN-ANALISIS"
    propuesta = servicio.registrar_propuesta(
        "S4.3", identificador, opciones=opciones, autor="Claudia", revision_esperada=_revision(servicio)
    )
    assert [o["id"] for o in propuesta["resolucion"]["propuesta"]["opciones"]] == ["A", "B"]
    with pytest.raises(ErrorDominio, match="persona"):
        servicio.definir(
            "S4.3", identificador, tipo="OPCION", opciones=["A"], autor="Claudia", revision_esperada=_revision(servicio)
        )
    with pytest.raises(ErrorDominio, match="una sola"):
        servicio.definir(
            "S4.3",
            identificador,
            tipo="OPCIONES",
            opciones=["A", "B"],
            autor="Equipo",
            revision_esperada=_revision(servicio),
        )
    cliente = TestClient(crear_aplicacion(repositorio))
    respuesta = cliente.post(
        f"/api/procesos/S4.3/observaciones/{identificador}/definicion",
        json={"tipo": "OPCION", "opciones": ["A"], "autor": "Equipo", "revision_esperada": _revision(servicio)},
    )
    assert respuesta.status_code == 200 and respuesta.json()["etapa"] == "DEFINIDA"
    tabla = repositorio.rutas("S4.3")["tabla"]
    tabla.write_text(tabla.read_text(encoding="utf-8") + "\n", encoding="utf-8")
    with pytest.raises(ErrorDominio, match="cambió"):
        servicio.iniciar_correccion("S4.3", identificador, autor="Claudia", revision_esperada=_revision(servicio))
    corrigiendo = servicio.iniciar_correccion(
        "S4.3", identificador, autor="Claudia", revision_esperada=_revision(servicio), confirmar_vigencia=True
    )
    assert corrigiendo["etapa"] == "EN-CORRECCION"
    with pytest.raises(ErrorDominio, match="sesión"):
        servicio.registrar_aplicacion(
            "S4.3", identificador, texto="Hecho", autor="Claudia", revision_esperada=_revision(servicio)
        )
    resuelta = servicio.registrar_aplicacion(
        "S4.3", identificador, texto="Carril ajustado", autor="Claudia", revision_esperada=_revision(servicio),
        sesion="abc", cambios=["tabla", "sustento"], validacion="D1-D5 sin hallazgos",
    )  # fmt: skip
    assert resuelta["etapa"] == "RESUELTA" and resuelta["estado"] == "RESUELTA"

    otra = servicio.agregar(
        "S4.3", elemento="", texto="Misma duda", autor="Equipo", revision_esperada=_revision(servicio)
    )
    vinculada = servicio.definir(
        "S4.3",
        otra["id"],
        tipo="VINCULADA",
        vinculada_a=identificador,
        autor="Equipo",
        revision_esperada=_revision(servicio),
    )
    assert vinculada["resolucion"]["definicion"]["vinculada_a"]["id"] == identificador
    manual = servicio.agregar("S4.3", elemento="", texto="Otra", autor="Equipo", revision_esperada=_revision(servicio))
    definida = servicio.definir(
        "S4.3", manual["id"], tipo="MANUAL", texto="<p>Mi respuesta</p>", formato="html", autor="Equipo",
        revision_esperada=_revision(servicio),
    )  # fmt: skip
    assert definida["resolucion"]["definicion"]["texto"] == "<p>Mi respuesta</p>"
    conteo = servicio.por_etapa(codigo="S4.3")["por_etapa"]
    assert conteo == {"RESUELTA": 1, "DEFINIDA": 2}
    assert [o["id"] for o in servicio.por_etapa("DEFINIDA")["observaciones"]] == [otra["id"], manual["id"]]

    reabierta = servicio.actualizar_estado("S4.3", identificador, "ABIERTA", _revision(servicio), "Equipo")
    assert reabierta["etapa"] == "REGISTRADA" and len(reabierta["resoluciones_anteriores"]) == 1


def test_mcp_no_expone_la_definicion(repositorio: RepositorioProcesos) -> None:
    nombres = {h.name for h in asyncio.run(crear_servidor(repositorio).list_tools())}
    assert {"registrar_analisis", "registrar_propuesta", "observaciones_por_etapa", "iniciar_correccion",
            "registrar_aplicacion"} <= nombres  # fmt: skip
    assert not any("defin" in nombre for nombre in nombres)
