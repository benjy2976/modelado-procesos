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


def test_reanalisis_conserva_el_anterior_y_listado_compacto(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioResolucion(repositorio)
    obs = servicio.agregar("S4.3", elemento="", texto="Duda", autor="Equipo", revision_esperada=_revision(servicio))
    servicio.registrar_analisis(
        "S4.3", obs["id"], texto="Primera lectura", clase="FALTA-EVIDENCIA", autor="Claudia",
        revision_esperada=_revision(servicio),
    )  # fmt: skip
    servicio.registrar_propuesta(
        "S4.3", obs["id"], opciones=[{"titulo": "Esperar", "detalle": "x", "efecto": "PENDIENTE-EVIDENCIA"}],
        autor="Claudia", revision_esperada=_revision(servicio),
    )  # fmt: skip
    with pytest.raises(ErrorDominio, match="motivo"):
        servicio.registrar_analisis(
            "S4.3", obs["id"], texto="Segunda", clase="ERROR-MODELO", autor="Claudia",
            revision_esperada=_revision(servicio),
        )  # fmt: skip
    nueva = servicio.registrar_analisis(
        "S4.3", obs["id"], texto="Segunda lectura", clase="ERROR-MODELO", autor="Claudia",
        revision_esperada=_revision(servicio), motivo="Revisión con capítulo completo",
        hipotesis=["Intervención económica: considerada"],
    )  # fmt: skip
    anterior = nueva["resoluciones_anteriores"][0]
    assert anterior["propuesta"]["opciones"][0]["titulo"] == "Esperar"
    assert anterior["reemplazada"]["motivo"] == "Revisión con capítulo completo"
    assert nueva["resolucion"]["analisis"]["hipotesis"] == ["Intervención económica: considerada"]
    assert "resolucion" not in servicio.por_etapa(codigo="S4.3", detalle=False)["observaciones"][0]


def test_mcp_responde_con_confirmacion_compacta(repositorio: RepositorioProcesos) -> None:
    import json

    servidor = crear_servidor(repositorio)
    servicio = ServicioResolucion(repositorio)
    resultado = asyncio.run(servidor.call_tool("registrar_observacion", {
        "codigo": "S4.3", "elemento": "", "texto": "Diagrama", "revision_esperada": _revision(servicio)}))  # fmt: skip
    datos = json.loads(resultado.content[0].text)
    assert set(datos) == {"id", "referencia", "etapa", "estado", "revision", "ultimo_evento"}


rev2 = _revision


def test_cerrar_con_decision_deja_registro_y_lo_exige(repositorio: RepositorioProcesos) -> None:
    """Cerrar sin cambio de modelo exige tipo y texto de una persona; ya no se cierra «en blanco»."""
    servicio = ServicioResolucion(repositorio)
    rev = _revision(servicio)
    obs = servicio.agregar("S4.3", elemento="Tarea_1", texto="¿Aplica?", autor="Equipo", revision_esperada=rev)
    with pytest.raises(ErrorDominio, match="persona"):
        servicio.cerrar("S4.3", obs["id"], tipo="ACLARADA", autor="Claudia", texto="x", revision_esperada=rev)
    with pytest.raises(ErrorDominio, match="respuesta"):
        servicio.cerrar("S4.3", obs["id"], tipo="ACLARADA", autor="Equipo", texto=" ", revision_esperada=rev2(servicio))
    pendiente = servicio.cerrar(
        "S4.3", obs["id"], tipo="PENDIENTE-EVIDENCIA", autor="Equipo", texto="<p>Falta la directiva</p>",
        revision_esperada=_revision(servicio),
    )  # fmt: skip
    assert pendiente["etapa"] == "PENDIENTE-EVIDENCIA" and pendiente["estado"] == "ABIERTA"
    cerrada = servicio.cerrar(
        "S4.3", obs["id"], tipo="ACLARADA", autor="Equipo", texto="<p>Se confirmó en reunión</p>",
        revision_esperada=_revision(servicio),
    )  # fmt: skip
    assert cerrada["estado"] == "RESUELTA" and cerrada["resolucion"]["cierre"]["tipo"] == "ACLARADA"
    assert cerrada["historial"][-1]["accion"] == "CERRADA-ACLARADA"
    cliente = TestClient(crear_aplicacion(repositorio))
    otra = servicio.agregar("S4.3", elemento="", texto="Otra", autor="Equipo", revision_esperada=_revision(servicio))
    respuesta = cliente.post(
        f"/api/procesos/S4.3/observaciones/{otra['id']}/cierre",
        json={"tipo": "NO-PROCEDE", "autor": "Equipo", "texto": "<p>No aplica a contrata</p>",
              "revision_esperada": _revision(servicio)},
    )  # fmt: skip
    assert respuesta.status_code == 200 and respuesta.json()["resolucion"]["cierre"]["tipo"] == "NO-PROCEDE"


def test_reabrir_sin_decision_vuelve_a_por_decidir(repositorio: RepositorioProcesos) -> None:
    """Una observación cerrada sin decisión se reabre con su análisis y propuesta, lista para decidir."""
    servicio = ServicioResolucion(repositorio)
    obs = servicio.agregar("S4.3", elemento="", texto="¿Aplica?", autor="Equipo", revision_esperada=rev2(servicio))
    servicio.registrar_analisis(
        "S4.3", obs["id"], texto="Análisis", clase="FALTA-EVIDENCIA", autor="Claudia", revision_esperada=rev2(servicio)
    )
    opciones = [{"titulo": "A", "detalle": "x", "efecto": "ACLARACION", "elementos": [], "recomendada": True},
                {"titulo": "B", "detalle": "y", "efecto": "NO-PROCEDE", "elementos": []}]  # fmt: skip
    rev = rev2(servicio)
    servicio.registrar_propuesta("S4.3", obs["id"], opciones=opciones, autor="Claudia", revision_esperada=rev)
    servicio.actualizar_estado("S4.3", obs["id"], "RESUELTA", rev2(servicio), "Equipo")
    reabierta = servicio.actualizar_estado("S4.3", obs["id"], "ABIERTA", rev2(servicio), "Equipo")
    assert reabierta["etapa"] == "PROPUESTA" and reabierta["resolucion"]["propuesta"]
    assert "resoluciones_anteriores" not in reabierta


def test_responder_y_decidir_el_agente_aplica_o_devuelve(repositorio: RepositorioProcesos) -> None:
    """Rediseño: la persona decide en texto libre; el agente cierra como aclaración o devuelve si es ambigua."""
    servicio = ServicioResolucion(repositorio)
    obs = servicio.agregar("S4.3", elemento="", texto="¿Aplica?", autor="Equipo", revision_esperada=rev2(servicio))
    servicio.definir(
        "S4.3", obs["id"], tipo="MANUAL", autor="Equipo", texto="<p>Revisar esto</p>", formato="html",
        revision_esperada=rev2(servicio),
    )  # fmt: skip
    devuelta = servicio.devolver_decision(
        "S4.3", obs["id"], pregunta="<p>¿Cambio el diagrama o solo aclaro?</p>", autor="Claudia",
        revision_esperada=rev2(servicio),
    )  # fmt: skip
    assert devuelta["etapa"] == "REGISTRADA" and "definicion" not in devuelta["resolucion"]
    assert devuelta["resolucion"]["decisiones_devueltas"][0]["texto"] == "<p>Revisar esto</p>"
    assert devuelta["respuestas"][-1]["autor"] == "Claudia"
    servicio.definir(
        "S4.3", obs["id"], tipo="MANUAL", autor="Equipo", texto="<p>Es una aclaración</p>", formato="html",
        revision_esperada=rev2(servicio),
    )  # fmt: skip
    with pytest.raises(ErrorDominio, match="sesión"):
        servicio.registrar_aplicacion(
            "S4.3", obs["id"], texto="x", autor="Claudia", revision_esperada=rev2(servicio), resultado="CAMBIO-MODELO"
        )
    cerrada = servicio.registrar_aplicacion(
        "S4.3", obs["id"], texto="Aclarado sin cambios", autor="Claudia", revision_esperada=rev2(servicio),
        resultado="ACLARADA",
    )  # fmt: skip
    assert cerrada["estado"] == "RESUELTA" and cerrada["resolucion"]["aplicacion"]["resultado"] == "ACLARADA"
