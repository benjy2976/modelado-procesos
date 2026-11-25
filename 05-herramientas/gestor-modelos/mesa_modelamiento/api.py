"""API local para la interfaz Nuxt de la mesa de modelamiento."""

from __future__ import annotations

from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from .documentos import ServicioDocumentos
from .esquemas import (
    DocumentoCopia,
    EdicionCopia,
    IntegracionVista,
    LecturaFuente,
    ListadoObservaciones,
    ModeloVista,
    NodoArbol,
    PreparacionSesion,
    RegistroObservacion,
    Salud,
    SesionVista,
)
from .observaciones import ServicioObservaciones
from .repositorio import ErrorDominio, RepositorioProcesos
from .sesiones import ServicioSesiones


class NuevaObservacion(BaseModel):
    elemento: str = ""
    referencia: str = ""
    texto: str = Field(min_length=1, max_length=20000)
    autor: str = Field(min_length=1, max_length=100)
    tipo: str = "OBSERVACION"
    formato: Literal["texto", "html"] = "texto"
    revision_esperada: str


class CambioEstado(BaseModel):
    estado: str
    revision_esperada: str
    autor: str = ""


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


def crear_aplicacion(repositorio: RepositorioProcesos | None = None) -> FastAPI:
    repositorio = repositorio or RepositorioProcesos.desde_entorno()
    observaciones = ServicioObservaciones(repositorio)
    documentos = ServicioDocumentos(repositorio)
    sesiones = ServicioSesiones(repositorio)
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

    @app.get("/api/procesos/{codigo}", response_model=ModeloVista, response_model_exclude_unset=True)
    def modelo(codigo: str) -> dict:
        return repositorio.leer_modelo(codigo)

    @app.get("/api/procesos/{codigo}/bpmn")
    def bpmn(codigo: str) -> FileResponse:
        ruta = repositorio.bpmn(codigo)
        return FileResponse(ruta, media_type="application/xml", filename=ruta.name, content_disposition_type="inline")

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
        "/api/procesos/{codigo}/sesiones",
        status_code=201,
        response_model=SesionVista,
        response_model_exclude_unset=True,
    )
    def iniciar_sesion(codigo: str, request: Request) -> dict:
        comprobar_origen(request)
        return sesiones.iniciar(codigo)

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
