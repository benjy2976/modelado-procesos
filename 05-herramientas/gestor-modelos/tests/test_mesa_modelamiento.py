"""Contratos de lectura y escritura compartidos por CLI, API y MCP."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mesa_modelamiento.api import crear_aplicacion
from mesa_modelamiento.observaciones import ServicioObservaciones
from mesa_modelamiento.repositorio import ErrorDominio, RepositorioProcesos


@pytest.fixture
def repositorio(tmp_path: Path) -> RepositorioProcesos:
    carpeta = tmp_path / "02-procesos" / "S4-prueba" / "S4-3-ejecucion"
    carpeta.mkdir(parents=True)
    (carpeta / "S4-3-diagrama-proceso.bpmn").write_text(
        '<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">'
        '<process id="P"><task id="Tarea_1" /></process></definitions>',
        encoding="utf-8",
    )
    return RepositorioProcesos(tmp_path)


def test_observaciones_revision_y_elemento(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioObservaciones(repositorio)
    revision = servicio.listar("S4.3")["revision"]
    creada = servicio.agregar(
        "S4.3",
        elemento="Tarea_1",
        texto="Revisar responsable",
        autor="Equipo",
        revision_esperada=revision,
    )
    assert creada["estado"] == "ABIERTA"
    assert creada["revision"] != revision
    with pytest.raises(ErrorDominio, match="recarga") as desfasada:
        servicio.agregar("S4.3", elemento="", texto="Otra", autor="Equipo", revision_esperada=revision)
    assert desfasada.value.codigo_http == 409
    with pytest.raises(ErrorDominio, match="no existe"):
        servicio.agregar(
            "S4.3",
            elemento="Tarea_falsa",
            texto="Otra",
            autor="Equipo",
            revision_esperada=creada["revision"],
        )
    archivo = repositorio.rutas("S4.3")["observaciones"]
    assert len(json.loads(archivo.read_text(encoding="utf-8"))["observaciones"]) == 1


def test_api_comparte_registro_y_no_acepta_origen_externo(repositorio: RepositorioProcesos) -> None:
    cliente = TestClient(crear_aplicacion(repositorio))
    assert cliente.get("/api/salud").json() == {"estado": "ok"}
    assert cliente.get("/api/procesos/S4.3/bpmn").headers["content-disposition"].startswith("inline")
    revision = cliente.get("/api/procesos/S4.3/observaciones").json()["revision"]
    entrada = {
        "elemento": "Tarea_1",
        "texto": "Corregir flujo",
        "autor": "Equipo",
        "revision_esperada": revision,
    }
    assert (
        cliente.post(
            "/api/procesos/S4.3/observaciones", json=entrada, headers={"Origin": "https://externo.invalid"}
        ).status_code
        == 403
    )
    respuesta = cliente.post("/api/procesos/S4.3/observaciones", json=entrada)
    assert respuesta.status_code == 201
    assert len(ServicioObservaciones(repositorio).listar("S4.3")["observaciones"]) == 1
    assert cliente.post("/api/procesos/S4.3/observaciones", json=entrada).status_code == 409
