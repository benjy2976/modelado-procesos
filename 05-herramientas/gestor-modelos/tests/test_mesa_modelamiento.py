"""Contratos de lectura y escritura compartidos por CLI, API y MCP."""

import asyncio
import hashlib
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pypdf import PdfWriter

from mesa_modelamiento.api import crear_aplicacion
from mesa_modelamiento.contrato import contenido_openapi
from mesa_modelamiento.mcp_adapter import crear_servidor
from mesa_modelamiento.observaciones import ServicioObservaciones
from mesa_modelamiento.repositorio import ErrorDominio, RepositorioProcesos
from mesa_modelamiento.sesiones import ServicioSesiones


@pytest.fixture
def repositorio(tmp_path: Path) -> RepositorioProcesos:
    carpeta = tmp_path / "02-procesos" / "S4-prueba" / "S4-3-ejecucion"
    carpeta.mkdir(parents=True)
    (carpeta / "S4-3-diagrama-proceso.bpmn").write_text(
        '<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">'
        '<process id="P"><task id="Tarea_1" /></process></definitions>',
        encoding="utf-8",
    )
    (carpeta / "S4-3-diagrama-proceso-tabla.md").write_text(
        "---\ncodigo_proceso: S4.3\n---\n\n## Elementos\n\n| ID | Numero | Tipo | Nombre |\n"
        "| --- | --- | --- | --- |\n| Tarea_1 | 1 | tarea | Revisar |\n",
        encoding="utf-8",
    )
    (carpeta / "S4-3-sustento.md").write_text("# Sustento de prueba\n", encoding="utf-8")
    referencia = tmp_path / "01-referencias" / "nota.txt"
    referencia.parent.mkdir(parents=True)
    referencia.write_text("Pasaje de prueba", encoding="utf-8")
    (carpeta / "S4-3-fuentes-visor.json").write_text(
        json.dumps({"elementos": {"Tarea_1": [{"ruta": "01-referencias/nota.txt", "fragmento": "Pasaje"}]}}),
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


def test_observaciones_html_se_guardan_saneadas(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioObservaciones(repositorio)
    revision = servicio.listar("S4.3")["revision"]
    entrada = (
        '<h2 onclick="x()">Título</h2><p><b>Negrita</b> <i>cursiva</i> <strike>tachado</strike>'
        '<a href="javascript:alert(1)">enlace</a></p><script>alert(1)</script><ul><li>uno<li>dos</ul>'
    )
    creada = servicio.agregar(
        "S4.3", elemento="", texto=entrada, autor="Equipo", revision_esperada=revision, formato="html"
    )
    assert creada["formato"] == "html"
    assert creada["texto"] == (
        "<h3>Título</h3><p><b>Negrita</b> <i>cursiva</i> <s>tachado</s>enlace</p><ul><li>uno</li><li>dos</li></ul>"
    )
    respuesta = servicio.responder(
        "S4.3", creada["id"], "<p>a &lt; b</p>", "Claudia", creada["revision"], formato="html"
    )
    assert respuesta["respuestas"][0]["texto"] == "<p>a &lt; b</p>"
    with pytest.raises(ErrorDominio, match="visible"):
        servicio.agregar(
            "S4.3",
            elemento="",
            texto="<p><script>x</script></p>",
            autor="Equipo",
            revision_esperada=respuesta["revision"],
            formato="html",
        )
    with pytest.raises(ErrorDominio, match="Formato"):
        servicio.agregar(
            "S4.3", elemento="", texto="x", autor="Equipo", revision_esperada=respuesta["revision"], formato="md"
        )
    cliente = TestClient(crear_aplicacion(repositorio))
    listado = cliente.get("/api/procesos/S4.3/observaciones").json()
    assert listado["observaciones"][0]["formato"] == "html"


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


def test_openapi_versionado_coincide_con_api() -> None:
    contrato = Path(__file__).resolve().parents[1] / "contracts" / "openapi.json"
    assert contrato.read_text(encoding="utf-8") == contenido_openapi()


def test_mcp_y_api_comparten_proceso_y_observaciones(repositorio: RepositorioProcesos) -> None:
    cliente = TestClient(crear_aplicacion(repositorio))
    servidor = crear_servidor(repositorio)
    lectura = asyncio.run(servidor.call_tool("leer_proceso", {"codigo": "S4.3"}))
    assert json.loads(lectura.content[0].text) == cliente.get("/api/procesos/S4.3").json()

    revision = cliente.get("/api/procesos/S4.3/observaciones").json()["revision"]
    asyncio.run(
        servidor.call_tool(
            "registrar_observacion",
            {
                "codigo": "S4.3",
                "elemento": "Tarea_1",
                "texto": "Revisar desde MCP",
                "revision_esperada": revision,
            },
        )
    )
    assert cliente.get("/api/procesos/S4.3/observaciones").json()["observaciones"][0]["texto"] == ("Revisar desde MCP")


def test_documentos_solo_sirven_rutas_registradas(repositorio: RepositorioProcesos) -> None:
    cliente = TestClient(crear_aplicacion(repositorio))
    tabla = cliente.get("/api/procesos/S4.3/documentos/tabla")
    assert tabla.status_code == 200
    assert tabla.headers["content-disposition"].startswith("inline")
    assert "codigo_proceso: S4.3" in tabla.text
    fuente = cliente.get("/api/procesos/S4.3/fuentes/Tarea_1/0")
    assert fuente.status_code == 200
    assert fuente.text == "Pasaje de prueba"
    assert cliente.get("/api/procesos/S4.3/fuentes/Tarea_1/1").status_code == 404
    assert cliente.get("/api/procesos/S4.3/documentos/desconocido").status_code == 404


def test_lectura_fuente_comparte_api_mcp_y_no_inventa_texto_pdf(repositorio: RepositorioProcesos) -> None:
    cliente = TestClient(crear_aplicacion(repositorio))
    servidor = crear_servidor(repositorio)
    url = "/api/procesos/S4.3/fuentes/Tarea_1/0/lectura"
    lectura = cliente.get(url)
    assert lectura.status_code == 200
    assert lectura.json()["texto"] == "Pasaje de prueba"
    assert lectura.json()["coincidencia_fragmento"]
    respuesta_mcp = asyncio.run(
        servidor.call_tool("leer_fuente", {"codigo": "S4.3", "referencia": "Tarea_1", "indice": 0})
    )
    assert json.loads(respuesta_mcp.content[0].text) == lectura.json()
    assert cliente.get("/api/procesos/S4.3/fuentes/Tarea_1/1/lectura").status_code == 404

    pdf = repositorio.raiz / "01-referencias" / "sin-texto.pdf"
    escritor = PdfWriter()
    escritor.add_blank_page(width=300, height=400)
    with pdf.open("wb") as archivo:
        escritor.write(archivo)
    referencias = repositorio.carpeta("S4.3") / "S4-3-fuentes-visor.json"
    referencias.write_text(
        json.dumps(
            {
                "elementos": {
                    "Tarea_1": [{"ruta": "01-referencias/sin-texto.pdf", "pagina": 1, "fragmento": "Texto inexistente"}]
                }
            }
        ),
        encoding="utf-8",
    )
    sin_texto = cliente.get(url)
    assert sin_texto.status_code == 200
    assert sin_texto.json()["estado"] == "SIN_TEXTO_EXTRAIBLE"
    assert sin_texto.json()["texto"] == ""
    assert not sin_texto.json()["coincidencia_fragmento"]


def test_ancla_pdf_depende_de_pagina_rectangulos_y_hash(repositorio: RepositorioProcesos) -> None:
    pdf = repositorio.raiz / "01-referencias" / "ancla.pdf"
    escritor = PdfWriter()
    escritor.add_blank_page(width=300, height=400)
    with pdf.open("wb") as archivo:
        escritor.write(archivo)
    sha256 = hashlib.sha256(pdf.read_bytes()).hexdigest()
    referencias = repositorio.carpeta("S4.3") / "S4-3-fuentes-visor.json"
    referencias.write_text(
        json.dumps(
            {
                "elementos": {
                    "Tarea_1": [
                        {
                            "ruta": "01-referencias/ancla.pdf",
                            "pagina": 1,
                            "sha256": sha256,
                            "rectangulos": [[0.1, 0.2, 0.6, 0.3]],
                        }
                    ]
                }
            }
        ),
        encoding="utf-8",
    )
    cliente = TestClient(crear_aplicacion(repositorio))
    ancla = cliente.get("/api/procesos/S4.3").json()["fuentes_visor"]["Tarea_1"][0]
    assert ancla["estado_ancla"] == "DISPONIBLE"
    assert ancla["rectangulos"] == [[0.1, 0.2, 0.6, 0.3]]

    pdf.write_bytes(pdf.read_bytes() + b"\n")
    obsoleta = cliente.get("/api/procesos/S4.3").json()["fuentes_visor"]["Tarea_1"][0]
    assert obsoleta["estado_ancla"] == "HASH_DISTINTO"
    assert obsoleta["rectangulos"] == []


def test_respuestas_historial_y_conflicto_de_revision(repositorio: RepositorioProcesos) -> None:
    cliente = TestClient(crear_aplicacion(repositorio))
    revision = cliente.get("/api/procesos/S4.3/observaciones").json()["revision"]
    creada = cliente.post(
        "/api/procesos/S4.3/observaciones",
        json={"elemento": "", "texto": "Revisar el diagrama", "autor": "Equipo", "revision_esperada": revision},
    ).json()
    respuesta = cliente.post(
        f"/api/procesos/S4.3/observaciones/{creada['id']}/respuestas",
        json={"texto": "Se revisará", "autor": "Revisor", "revision_esperada": creada["revision"]},
    )
    assert respuesta.status_code == 201
    respondida = respuesta.json()
    assert respondida["respuestas"][0]["texto"] == "Se revisará"
    assert [evento["accion"] for evento in respondida["historial"]] == ["CREADA", "RESPONDIDA"]
    assert (
        cliente.patch(
            f"/api/procesos/S4.3/observaciones/{creada['id']}",
            json={"estado": "RESUELTA", "revision_esperada": creada["revision"]},
        ).status_code
        == 409
    )
    cerrada = cliente.patch(
        f"/api/procesos/S4.3/observaciones/{creada['id']}",
        json={"estado": "RESUELTA", "revision_esperada": respondida["revision"], "autor": "Revisor"},
    ).json()
    assert cerrada["estado"] == "RESUELTA"
    assert cerrada["historial"][-1]["estado"] == "RESUELTA"


def test_responder_registro_anterior_sin_historial(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioObservaciones(repositorio)
    archivo = repositorio.rutas("S4.3")["observaciones"]
    archivo.write_text(
        json.dumps(
            {
                "modelo": "modelo.html",
                "observaciones": [
                    {
                        "id": "obs-1",
                        "elemento": "",
                        "texto": "Anterior",
                        "autor": "Equipo",
                        "estado": "ABIERTA",
                        "fecha": "2026-01-01",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    revision = servicio.listar("S4.3")["revision"]
    actualizada = servicio.responder("S4.3", "obs-1", "Respuesta nueva", "Revisor", revision)
    assert actualizada["respuestas"][0]["texto"] == "Respuesta nueva"
    assert actualizada["historial"][0]["accion"] == "RESPONDIDA"


def test_sesion_copia_estado_real_y_detecta_conflicto(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioSesiones(repositorio, repositorio.raiz / ".mesa-sesiones")
    ruta = repositorio.rutas("S4.3")["sustento"]
    ruta.write_bytes(b"# Cambio previo sin commit\n")
    sesion = servicio.iniciar("S4.3")
    identificador = sesion["sesion"]
    assert servicio.contenido("S4.3", identificador, "sustento")["texto"] == "# Cambio previo sin commit\n"
    with pytest.raises(ErrorDominio, match="sesión activa"):
        servicio.iniciar("S4.3")
    documento = servicio.contenido("S4.3", identificador, "sustento")
    editado = servicio.editar("S4.3", identificador, "sustento", "# Versión revisada\n", documento["revision"])
    assert editado["revision"] != documento["revision"]
    with pytest.raises(ErrorDominio, match="recargue"):
        servicio.editar("S4.3", identificador, "sustento", "# Otra\n", documento["revision"])
    preparado = servicio.preparar("S4.3", identificador)
    assert preparado["aplicable"]
    assert "Cambio previo sin commit" in preparado["diff"]
    ruta.write_bytes("# Tercera edición concurrente\n".encode("utf-8"))
    with pytest.raises(ErrorDominio, match="cambió desde la copia"):
        servicio.integrar("S4.3", identificador, editado["revision_sesion"])
    assert ruta.read_text(encoding="utf-8") == "# Tercera edición concurrente\n"
    assert (repositorio.raiz / ".mesa-sesiones" / "S4.3" / identificador / "origen" / ruta.name).read_text(
        encoding="utf-8"
    ) == "# Cambio previo sin commit\n"


def test_integracion_conserva_instantanea_y_excluye_aprobado(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioSesiones(repositorio, repositorio.raiz / ".mesa-sesiones")
    ruta = repositorio.rutas("S4.3")["sustento"]
    anterior = ruta.read_bytes()
    sesion = servicio.iniciar("S4.3")
    identificador = sesion["sesion"]
    revision = servicio.contenido("S4.3", identificador, "sustento")["revision"]
    editado = servicio.editar("S4.3", identificador, "sustento", "# Sustento corregido\n", revision)
    assert servicio.preparar("S4.3", identificador)["aplicable"]
    resultado = servicio.integrar("S4.3", identificador, editado["revision_sesion"])
    assert resultado["cambios"] == ["sustento"]
    assert ruta.read_text(encoding="utf-8") == "# Sustento corregido\n"
    respaldo = repositorio.raiz / ".mesa-sesiones" / "S4.3" / identificador / "origen" / ruta.name
    assert respaldo.read_bytes() == anterior
    ruta.write_text("---\nestado_institucional: APROBADO\n---\n# Texto\n", encoding="utf-8")
    with pytest.raises(ErrorDominio, match="APROBADO"):
        servicio.iniciar("S4.3")


def test_api_y_mcp_comparten_sesion_editable(repositorio: RepositorioProcesos) -> None:
    cliente = TestClient(crear_aplicacion(repositorio))
    servidor = crear_servidor(repositorio)
    creada = cliente.post("/api/procesos/S4.3/sesiones")
    assert creada.status_code == 201
    identificador = creada.json()["sesion"]
    leida = asyncio.run(servidor.call_tool("leer_sesion", {"codigo": "S4.3", "sesion": identificador}))
    assert json.loads(leida.content[0].text)["sesion"] == identificador
    documento = cliente.get(f"/api/procesos/S4.3/sesiones/{identificador}/documentos/sustento").json()
    asyncio.run(
        servidor.call_tool(
            "editar_documento_copia",
            {
                "codigo": "S4.3",
                "sesion": identificador,
                "nombre": "sustento",
                "texto": "# Editado mediante MCP\n",
                "revision_esperada": documento["revision"],
            },
        )
    )
    assert (
        cliente.get(f"/api/procesos/S4.3/sesiones/{identificador}/documentos/sustento").json()["texto"]
        == "# Editado mediante MCP\n"
    )
    assert (
        cliente.put(
            f"/api/procesos/S4.3/sesiones/{identificador}/documentos/sustento",
            json={"texto": "# Desfasado\n", "revision_esperada": documento["revision"]},
        ).status_code
        == 409
    )
    cerrada = cliente.post(f"/api/procesos/S4.3/sesiones/{identificador}/cierre")
    assert cerrada.status_code == 200
    assert cerrada.json()["estado"] == "CERRADA"


def test_mcp_prepara_e_integra_sustento_sin_alterar_bpmn(repositorio: RepositorioProcesos) -> None:
    servidor = crear_servidor(repositorio)
    sesion = json.loads(asyncio.run(servidor.call_tool("iniciar_edicion", {"codigo": "S4.3"})).content[0].text)
    identificador = sesion["sesion"]
    documento = json.loads(
        asyncio.run(
            servidor.call_tool(
                "leer_documento_copia", {"codigo": "S4.3", "sesion": identificador, "nombre": "sustento"}
            )
        )
        .content[0]
        .text
    )
    editado = json.loads(
        asyncio.run(
            servidor.call_tool(
                "editar_documento_copia",
                {
                    "codigo": "S4.3",
                    "sesion": identificador,
                    "nombre": "sustento",
                    "texto": "# Aclarado\n",
                    "revision_esperada": documento["revision"],
                },
            )
        )
        .content[0]
        .text
    )
    preparado = json.loads(
        asyncio.run(servidor.call_tool("preparar_cambio", {"codigo": "S4.3", "sesion": identificador})).content[0].text
    )
    assert preparado["aplicable"]
    assert preparado["cambios"] == ["sustento"]
    bpmn_antes = repositorio.bpmn("S4.3").read_bytes()
    resultado = json.loads(
        asyncio.run(
            servidor.call_tool(
                "aplicar_cambio",
                {"codigo": "S4.3", "sesion": identificador, "revision_esperada": editado["revision_sesion"]},
            )
        )
        .content[0]
        .text
    )
    assert resultado["estado"] == "INTEGRADA"
    assert repositorio.rutas("S4.3")["sustento"].read_text(encoding="utf-8").strip() == "# Aclarado"
    assert repositorio.bpmn("S4.3").read_bytes() == bpmn_antes


def test_ancla_con_tramos_en_varias_paginas(repositorio: RepositorioProcesos) -> None:
    pdf = repositorio.raiz / "01-referencias" / "tramos.pdf"
    escritor = PdfWriter()
    escritor.add_blank_page(width=300, height=400)
    escritor.add_blank_page(width=300, height=400)
    with pdf.open("wb") as archivo:
        escritor.write(archivo)
    sha256 = hashlib.sha256(pdf.read_bytes()).hexdigest()
    tramos = [
        {"pagina": 1, "rol": "antecedente", "rectangulos": [[0.1, 0.8, 0.5, 0.85]]},
        {"pagina": 2, "rol": "citado", "rectangulos": [[0.1, 0.05, 0.6, 0.1]]},
    ]
    entrada = {"ruta": "01-referencias/tramos.pdf", "pagina": 1, "sha256": sha256,
               "rectangulos": tramos[0]["rectangulos"], "tramos": tramos}  # fmt: skip
    referencias = repositorio.carpeta("S4.3") / "S4-3-fuentes-visor.json"
    referencias.write_text(json.dumps({"elementos": {"Tarea_1": [entrada]}}), encoding="utf-8")
    cliente = TestClient(crear_aplicacion(repositorio))
    ancla = cliente.get("/api/procesos/S4.3").json()["fuentes_visor"]["Tarea_1"][0]
    assert ancla["estado_ancla"] == "DISPONIBLE" and ancla["tramos"] == tramos

    invalido = {**entrada, "tramos": [{**tramos[0], "rol": "otro"}]}
    referencias.write_text(json.dumps({"elementos": {"Tarea_1": [invalido]}}), encoding="utf-8")
    with pytest.raises(ValueError, match="Tramos de ancla invalidos"):
        repositorio.leer_modelo("S4.3")


def test_sesion_anclas_aceptacion_de_hallazgos_y_cierre_idempotente(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioSesiones(repositorio)
    identificador = servicio.iniciar("S4.3")["sesion"]
    with pytest.raises(ErrorDominio, match="no existe"):
        servicio.anclar("S4.3", identificador, "Tarea_9", "x:y", "cita", "Título", "art. 1", "vigente")
    documento = servicio.contenido("S4.3", identificador, "fuentes_visor")
    datos = json.loads(documento["texto"])
    datos["elementos"]["Retirada"] = [{"ruta": "01-referencias/nota.txt", "fragmento": "x"}]
    servicio.editar("S4.3", identificador, "fuentes_visor", json.dumps(datos), documento["revision"])
    retiro = servicio.retirar_anclas("S4.3", identificador, huerfanas=True)
    assert retiro["retiradas"] == ["Retirada"]
    assert servicio.retirar_anclas("S4.3", identificador, huerfanas=True)["retiradas"] == []
    with pytest.raises(ErrorDominio, match="justificación"):
        servicio.preparar("S4.3", identificador, generar=False, aceptar_hallazgos="corta")
    with pytest.raises(ErrorDominio, match="sustento"):
        servicio.preparar(
            "S4.3", identificador, generar=False, aceptar_hallazgos="Hallazgos D4 ya revisados y aceptados"
        )
    sustento = servicio.contenido("S4.3", identificador, "sustento")
    servicio.editar("S4.3", identificador, "sustento", sustento["texto"] + "\nD4 justificado.\n", sustento["revision"])
    preparado = servicio.preparar(
        "S4.3", identificador, generar=False, aceptar_hallazgos="Hallazgos D4 ya revisados y aceptados"
    )
    assert preparado["hallazgos_aceptados"]["justificacion"] == "Hallazgos D4 ya revisados y aceptados"
    assert preparado["aplicable"]
    assert servicio.cerrar("S4.3", identificador)["estado"] == "CERRADA"
    repetido = servicio.cerrar("S4.3", identificador)
    assert repetido["estado"] == "CERRADA" and "ya había terminado" in repetido["detalle"]


def test_generacion_exige_justificacion_para_forzar(repositorio: RepositorioProcesos) -> None:
    from mesa_modelamiento.generacion import generar_modelo, validar_justificacion

    with pytest.raises(ErrorDominio, match="justificación"):
        validar_justificacion("breve")
    with pytest.raises(ErrorDominio, match="justificación"):
        generar_modelo(repositorio, "S4.3", forzar=True, justificacion="")


def test_observacion_por_id_de_tabla_o_numero(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioObservaciones(repositorio)
    identificador = next(iter(repositorio.leer_modelo("S4.3")["elementos"]))
    bpmn = repositorio.rutas("S4.3")["bpmn"]
    bpmn.write_text(bpmn.read_text(encoding="utf-8").replace('id="Tarea_1"', f'id="{identificador}"'), encoding="utf-8")
    creada = servicio.agregar(
        "S4.3", elemento="1", texto="Por número", autor="Claudia", revision_esperada=servicio.listar("S4.3")["revision"]
    )
    assert creada["elemento"] == identificador and creada["referencia"] == "Caja 1 (Tarea_1)"


def test_mcp_expone_paridad_y_errores_de_dominio_legibles(repositorio: RepositorioProcesos) -> None:
    servidor = crear_servidor(repositorio)
    nombres = {herramienta.name for herramienta in asyncio.run(servidor.list_tools())}
    esperadas = {"generar_modelo", "anclar_en_copia", "retirar_anclas_copia", "auditoria_inventariar",
                 "auditoria_registrar", "auditoria_cobertura", "auditoria_reconfirmar", "auditoria_correr",
                 "auditoria_interfaces", "auditoria_informe", "buscar_fuentes", "contexto_fragmento",
                 "anclar_cita"}  # fmt: skip
    assert esperadas <= nombres
    from mcp.server.mcpserver.exceptions import ToolError

    with pytest.raises(ToolError, match="HTTP 404"):
        asyncio.run(servidor.call_tool("leer_elemento", {"codigo": "S4.3", "identificador": "No_existe"}))
