"""API local para la interfaz Nuxt de la mesa de modelamiento."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response, StreamingResponse
from pydantic import BaseModel, Field

from . import relevo_cliente
from .documentos import ServicioDocumentos
from .esquemas import (
    ConteoObservaciones,
    DocumentoCopia,
    EdicionCopia,
    EstadoChat,
    EstadoModelo,
    IntegracionVista,
    LecturaFuente,
    LiberacionVista,
    ListadoObservaciones,
    ListadoTrabajos,
    ListadoVersiones,
    ModeloVista,
    NodoArbol,
    ObservacionesPorEtapa,
    PreparacionSesion,
    RegistroObservacion,
    Salud,
    SesionVista,
    TrabajoVista,
    VersionDetalle,
)
from .exportaciones import bpmn_para_bizagi
from .repositorio import ErrorDominio, RepositorioProcesos
from .resolucion import ServicioResolucion
from .sesiones import ServicioSesiones
from .trabajos import ServicioTrabajos
from .versiones import ServicioVersiones


class NuevaObservacion(BaseModel):
    elemento: str = ""
    referencia: str = ""
    texto: str = Field(min_length=1, max_length=20000)
    autor: str = Field(min_length=1, max_length=100)
    tipo: str = "OBSERVACION"
    formato: Literal["texto", "html"] = "texto"
    revision_esperada: str


class SolicitudAnalisis(BaseModel):
    autor: str = Field(min_length=1, max_length=100)
    nota: str = Field(default="", max_length=1000)


class TurnoChat(BaseModel):
    conversacion: str = Field(pattern=r"^M-[0-9A-Za-z.-]{6,80}$")
    mensaje: str = Field(min_length=1, max_length=8000)
    contexto: dict[str, str | None] = Field(default_factory=dict)


class DefinicionEntrada(BaseModel):
    tipo: Literal["OPCION", "OPCIONES", "MANUAL", "VINCULADA"]
    autor: str = Field(min_length=1, max_length=100)
    revision_esperada: str
    opciones: list[str] = Field(default_factory=list, max_length=8)
    texto: str = Field(default="", max_length=20000)
    formato: Literal["texto", "html"] = "texto"
    vinculada_a: str = ""


class CierreEntrada(BaseModel):
    tipo: Literal["ACLARADA", "NO-PROCEDE", "PENDIENTE-EVIDENCIA"]
    autor: str = Field(min_length=1, max_length=100)
    texto: str = Field(min_length=1, max_length=20000)
    formato: Literal["texto", "html"] = "html"
    revision_esperada: str


class CambioEstado(BaseModel):
    estado: str
    revision_esperada: str
    autor: str = ""


class NuevaRedaccion(BaseModel):
    texto: str = Field(min_length=1, max_length=20000)
    autor: str = Field(min_length=1, max_length=100)
    motivo: str = Field(min_length=10, max_length=300)
    formato: Literal["texto", "html"] = "html"
    revision_esperada: str


class NuevaRespuesta(BaseModel):
    texto: str = Field(min_length=1, max_length=20000)
    autor: str = Field(min_length=1, max_length=100)
    formato: Literal["texto", "html"] = "texto"
    revision_esperada: str


class EdicionDocumento(BaseModel):
    texto: str = Field(min_length=1, max_length=2_000_000)
    revision_esperada: str


class PreparacionEntrada(BaseModel):
    aceptar_hallazgos: str = Field(default="", max_length=2000)


class IntegracionSesion(BaseModel):
    revision_esperada: int = Field(ge=0)


class InicioSesion(BaseModel):
    titular: str = Field(default="persona", min_length=1, max_length=120)
    motivo: str = Field(default="", max_length=500)
    modo: Literal["EDICION", "BORRADOR"] = "EDICION"
    observacion: str | None = Field(default=None, max_length=40)


class LiberacionModelo(BaseModel):
    autor: str = Field(min_length=1, max_length=120)
    motivo: str = Field(min_length=10, max_length=500)


def crear_aplicacion(repositorio: RepositorioProcesos | None = None) -> FastAPI:
    repositorio = repositorio or RepositorioProcesos.desde_entorno()
    observaciones = ServicioResolucion(repositorio)
    trabajos = ServicioTrabajos(repositorio)
    documentos = ServicioDocumentos(repositorio)
    sesiones = ServicioSesiones(repositorio)
    versiones = ServicioVersiones(repositorio, sesiones=sesiones.almacen)
    app = FastAPI(title="Mesa de modelamiento", version="0.1.0")

    @app.exception_handler(ErrorDominio)
    async def error_dominio(_request: Request, exc: ErrorDominio) -> JSONResponse:
        return JSONResponse(
            {"error": {"code": exc.codigo_http, "message": str(exc)}},
            status_code=exc.codigo_http,
        )

    def comprobar_origen(request: Request) -> None:
        origen = request.headers.get("origin")
        if origen and origen.rstrip("/") != str(request.base_url).rstrip("/"):
            raise ErrorDominio("Origen no autorizado", 403)

    @app.get("/api/salud", response_model=Salud)
    def salud() -> dict:
        return {"estado": "ok"}

    @app.get("/api/arbol", response_model=NodoArbol)
    def arbol() -> dict:
        return repositorio.arbol()

    @app.get("/api/observaciones/abiertas", response_model=ConteoObservaciones)
    def conteo_observaciones() -> dict:
        return observaciones.conteo_abiertas()

    @app.get("/api/procesos/{codigo}", response_model=ModeloVista, response_model_exclude_unset=True)
    def modelo(codigo: str) -> dict:
        return repositorio.leer_modelo(codigo)

    @app.get("/api/procesos/{codigo}/bpmn")
    def bpmn(codigo: str) -> FileResponse:
        ruta = repositorio.bpmn(codigo)
        return FileResponse(ruta, media_type="application/xml", filename=ruta.name, content_disposition_type="inline")

    @app.get("/api/procesos/{codigo}/bizagi")
    def bizagi(codigo: str) -> Response:
        return Response(bpmn_para_bizagi(repositorio.bpmn(codigo).read_bytes()), media_type="application/xml")

    @app.get("/api/procesos/{codigo}/documentos/{tipo}")
    def documento_proceso(codigo: str, tipo: str) -> FileResponse:
        ruta = documentos.documento_proceso(codigo, tipo)
        return FileResponse(
            ruta, media_type="text/markdown; charset=utf-8", filename=ruta.name, content_disposition_type="inline"
        )

    @app.get("/api/procesos/{codigo}/fuentes/{ref}/{indice}")
    def fuente(codigo: str, ref: str, indice: int) -> FileResponse:
        ruta = documentos.fuente(codigo, ref, indice)
        media = "application/pdf" if ruta.suffix.lower() == ".pdf" else "text/plain; charset=utf-8"
        return FileResponse(ruta, media_type=media, filename=ruta.name, content_disposition_type="inline")

    @app.get("/api/procesos/{codigo}/fuentes/{ref}/{indice}/lectura", response_model=LecturaFuente)
    def lectura_fuente(codigo: str, ref: str, indice: int) -> dict:
        return documentos.leer_fuente(codigo, ref, indice)

    @app.get(
        "/api/procesos/{codigo}/observaciones", response_model=ListadoObservaciones, response_model_exclude_unset=True
    )
    def listar_observaciones(codigo: str) -> dict:
        return observaciones.listar(codigo)

    @app.post(
        "/api/procesos/{codigo}/observaciones",
        status_code=201,
        response_model=RegistroObservacion,
        response_model_exclude_unset=True,
    )
    def crear_observacion(codigo: str, entrada: NuevaObservacion, request: Request) -> dict:
        comprobar_origen(request)
        return observaciones.agregar(codigo, **entrada.model_dump())

    @app.put(
        "/api/procesos/{codigo}/observaciones/{identificador}/texto",
        response_model=RegistroObservacion,
        response_model_exclude_unset=True,
    )
    def redactar_observacion(codigo: str, identificador: str, entrada: NuevaRedaccion, request: Request) -> dict:
        comprobar_origen(request)
        return observaciones.redactar(codigo, identificador, **entrada.model_dump())

    @app.post(
        "/api/procesos/{codigo}/observaciones/{identificador}/respuestas",
        status_code=201,
        response_model=RegistroObservacion,
        response_model_exclude_unset=True,
    )
    def responder_observacion(codigo: str, identificador: str, entrada: NuevaRespuesta, request: Request) -> dict:
        comprobar_origen(request)
        return observaciones.responder(codigo, identificador, **entrada.model_dump())

    @app.patch(
        "/api/procesos/{codigo}/observaciones/{identificador}",
        response_model=RegistroObservacion,
        response_model_exclude_unset=True,
    )
    def cambiar_estado(codigo: str, identificador: str, entrada: CambioEstado, request: Request) -> dict:
        comprobar_origen(request)
        return observaciones.actualizar_estado(codigo, identificador, **entrada.model_dump())

    @app.post(
        "/api/procesos/{codigo}/observaciones/{identificador}/definicion",
        response_model=RegistroObservacion,
        response_model_exclude_unset=True,
    )
    def definir_observacion(codigo: str, identificador: str, entrada: DefinicionEntrada, request: Request) -> dict:
        """Una persona acoge opciones, escribe una respuesta manual o vincula a otra observación resuelta."""
        comprobar_origen(request)
        return observaciones.definir(codigo, identificador, **entrada.model_dump())

    @app.post(
        "/api/procesos/{codigo}/observaciones/{identificador}/cierre",
        response_model=RegistroObservacion,
        response_model_exclude_unset=True,
    )
    def cerrar_observacion(codigo: str, identificador: str, entrada: CierreEntrada, request: Request) -> dict:
        """Una persona cierra sin cambio de modelo (aclarada, no procede) o la deja pendiente de evidencia."""
        comprobar_origen(request)
        return observaciones.cerrar(codigo, identificador, **entrada.model_dump())

    @app.post(
        "/api/procesos/{codigo}/observaciones/{identificador}/solicitud-analisis",
        status_code=202,
        response_model=TrabajoVista,
        response_model_exclude_unset=True,
    )
    def solicitar_analisis(codigo: str, identificador: str, entrada: SolicitudAnalisis, request: Request) -> dict:
        """Encola el análisis de una observación y despierta al agente de análisis por el relevo (DEC-068)."""
        comprobar_origen(request)
        trabajo = observaciones.solicitar_analisis(codigo, identificador, entrada.autor, entrada.nota)
        relevo_cliente.despertar("ANALISIS")
        return trabajo

    @app.get("/api/procesos/{codigo}/trabajos", response_model=ListadoTrabajos)
    def trabajos_del_proceso(codigo: str, estado: str | None = None) -> dict:
        return trabajos.listar(estado=estado, codigo=codigo)

    @app.get("/api/trabajos", response_model=ListadoTrabajos)
    def listar_trabajos(estado: str | None = None, tipo: str | None = None) -> dict:
        return trabajos.listar(estado=estado, tipo=tipo)

    @app.get("/api/chat/estado", response_model=EstadoChat)
    def estado_chat() -> dict:
        return {"configurado": relevo_cliente.configurado()}

    @app.post("/api/procesos/{codigo}/chat")
    def chat(codigo: str, entrada: TurnoChat, request: Request) -> StreamingResponse:
        """Turno de chat con el agente mesa-chat; retransmite el SSE del relevo sin reinterpretarlo."""
        comprobar_origen(request)
        repositorio.carpeta(codigo)
        respuesta = relevo_cliente.abrir_turno(codigo, entrada.conversacion, entrada.mensaje, entrada.contexto)

        def lineas():
            with respuesta:
                yield from respuesta

        return StreamingResponse(lineas(), media_type="text/event-stream", headers={"Cache-Control": "no-store"})

    @app.get("/api/observaciones/etapas", response_model=ObservacionesPorEtapa)
    def observaciones_por_etapa(etapa: str | None = None, codigo: str | None = None) -> dict:
        """Observaciones por etapa de resolución en un proceso o en todo el árbol."""
        return observaciones.por_etapa(etapa, codigo)

    @app.post(
        "/api/procesos/{codigo}/sesiones",
        status_code=201,
        response_model=SesionVista,
        response_model_exclude_unset=True,
    )
    def iniciar_sesion(codigo: str, request: Request, entrada: InicioSesion | None = None) -> dict:
        comprobar_origen(request)
        entrada = entrada or InicioSesion()
        return sesiones.iniciar(codigo, entrada.titular, entrada.motivo, entrada.modo, entrada.observacion)

    @app.get("/api/procesos/{codigo}/edicion", response_model=EstadoModelo)
    def estado_modelo(codigo: str) -> dict:
        return sesiones.estado(codigo)

    @app.get("/api/procesos/{codigo}/versiones", response_model=ListadoVersiones)
    def listar_versiones(codigo: str) -> dict:
        return versiones.listar(codigo)

    @app.get("/api/procesos/{codigo}/versiones/{numero}", response_model=VersionDetalle)
    def leer_version(codigo: str, numero: int) -> dict:
        return versiones.leer(codigo, numero)

    @app.get("/api/procesos/{codigo}/versiones/{numero}/bpmn")
    def bpmn_version(codigo: str, numero: int) -> Response:
        return Response(versiones.bpmn(codigo, numero), media_type="application/xml")

    @app.get("/api/procesos/{codigo}/versiones/{numero}/bizagi")
    def bizagi_version(codigo: str, numero: int) -> Response:
        return Response(bpmn_para_bizagi(versiones.bpmn(codigo, numero)), media_type="application/xml")

    @app.post("/api/procesos/{codigo}/edicion/liberacion", response_model=LiberacionVista)
    def liberar_modelo(codigo: str, entrada: LiberacionModelo, request: Request) -> dict:
        comprobar_origen(request)
        return sesiones.liberar(codigo, entrada.autor, entrada.motivo)

    @app.get(
        "/api/procesos/{codigo}/sesiones/activa", response_model=SesionVista | None, response_model_exclude_unset=True
    )
    def sesion_activa(codigo: str) -> dict | None:
        return sesiones.activa(codigo)

    @app.get(
        "/api/procesos/{codigo}/sesiones/{identificador}", response_model=SesionVista, response_model_exclude_unset=True
    )
    def leer_sesion(codigo: str, identificador: str) -> dict:
        return sesiones.leer(codigo, identificador)

    @app.get("/api/procesos/{codigo}/sesiones/{identificador}/documentos/{nombre}", response_model=DocumentoCopia)
    def leer_copia(codigo: str, identificador: str, nombre: str) -> dict:
        return sesiones.contenido(codigo, identificador, nombre)

    @app.put("/api/procesos/{codigo}/sesiones/{identificador}/documentos/{nombre}", response_model=EdicionCopia)
    def editar_copia(codigo: str, identificador: str, nombre: str, entrada: EdicionDocumento, request: Request) -> dict:
        comprobar_origen(request)
        return sesiones.editar(codigo, identificador, nombre, **entrada.model_dump())

    @app.post("/api/procesos/{codigo}/sesiones/{identificador}/preparacion", response_model=PreparacionSesion)
    def preparar_sesion(
        codigo: str, identificador: str, request: Request, entrada: PreparacionEntrada | None = None
    ) -> dict:
        comprobar_origen(request)
        return sesiones.preparar(codigo, identificador, aceptar_hallazgos=entrada.aceptar_hallazgos if entrada else "")

    @app.post("/api/procesos/{codigo}/sesiones/{identificador}/integracion", response_model=IntegracionVista)
    def integrar_sesion(codigo: str, identificador: str, entrada: IntegracionSesion, request: Request) -> dict:
        comprobar_origen(request)
        return sesiones.integrar(codigo, identificador, entrada.revision_esperada)

    @app.post(
        "/api/procesos/{codigo}/sesiones/{identificador}/cierre",
        response_model=SesionVista,
        response_model_exclude_unset=True,
    )
    def cerrar_sesion(codigo: str, identificador: str, request: Request) -> dict:
        comprobar_origen(request)
        return sesiones.cerrar(codigo, identificador)

    return app


app = crear_aplicacion()
