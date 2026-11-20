"""API local para la interfaz Nuxt de la mesa de modelamiento."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

from .observaciones import ServicioObservaciones
from .repositorio import ErrorDominio, RepositorioProcesos


class NuevaObservacion(BaseModel):
    elemento: str = ""
    referencia: str = ""
    texto: str = Field(min_length=1, max_length=4000)
    autor: str = Field(min_length=1, max_length=100)
    tipo: str = "OBSERVACION"
    revision_esperada: str


class CambioEstado(BaseModel):
    estado: str
    revision_esperada: str


def crear_aplicacion(repositorio: RepositorioProcesos | None = None) -> FastAPI:
    repositorio = repositorio or RepositorioProcesos.desde_entorno()
    observaciones = ServicioObservaciones(repositorio)
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

    @app.get("/api/salud")
    def salud() -> dict:
        return {"estado": "ok"}

    @app.get("/api/arbol")
    def arbol() -> dict:
        return repositorio.arbol()

    @app.get("/api/procesos/{codigo}")
    def modelo(codigo: str) -> dict:
        return repositorio.leer_modelo(codigo)

    @app.get("/api/procesos/{codigo}/bpmn")
    def bpmn(codigo: str) -> FileResponse:
        ruta = repositorio.bpmn(codigo)
        return FileResponse(ruta, media_type="application/xml", filename=ruta.name, content_disposition_type="inline")

    @app.get("/api/procesos/{codigo}/observaciones")
    def listar_observaciones(codigo: str) -> dict:
        return observaciones.listar(codigo)

    @app.post("/api/procesos/{codigo}/observaciones", status_code=201)
    def crear_observacion(codigo: str, entrada: NuevaObservacion, request: Request) -> dict:
        comprobar_origen(request)
        return observaciones.agregar(codigo, **entrada.model_dump())

    @app.patch("/api/procesos/{codigo}/observaciones/{identificador}")
    def cambiar_estado(codigo: str, identificador: str, entrada: CambioEstado, request: Request) -> dict:
        comprobar_origen(request)
        return observaciones.actualizar_estado(codigo, identificador, **entrada.model_dump())

    return app


app = crear_aplicacion()
