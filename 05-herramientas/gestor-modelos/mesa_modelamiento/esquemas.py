"""Esquemas de transporte de las lecturas usadas por la interfaz."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class NodoArbol(BaseModel):
    codigo: str
    nombre: str
    indice: str | None
    bpmn: str | None
    hijos: list[NodoArbol]


class ElementoVista(BaseModel):
    ref: str
    numero: str = ""
    pool: str = ""
    carril: str = ""
    tipo: str = ""
    nombre: str = ""
    documentos: str = ""
    plazo: str = ""
    disparador: str = ""
    anotacion: str = ""
    clase: str = ""
    fuente: str = ""
    destino: str | None = None
    destino_tipo: str | None = None


class TramoAncla(BaseModel):
    pagina: int
    rol: str
    rectangulos: list[list[float]] = Field(default_factory=list)


class FuenteVista(BaseModel):
    ruta: str
    pagina: int | None = None
    fragmento: str = ""
    titulo: str = ""
    ubicacion: str = ""
    consulta: str = ""
    vigencia: str = ""
    sha256: str = ""
    rectangulos: list[list[float]] = Field(default_factory=list)
    tramos: list[TramoAncla] = Field(default_factory=list)
    estado_ancla: str = "SIN_COORDENADAS"


class LecturaFuente(FuenteVista):
    sha256: str
    estado: str
    coincidencia_fragmento: bool
    texto: str
    truncado: bool


class ModeloVista(BaseModel):
    codigo: str
    modelo: str
    padre: str
    tabla: str
    sustento: str
    elementos: dict[str, ElementoVista]
    flujos: dict[str, dict[str, Any]]
    fuentes_visor: dict[str, list[FuenteVista]]
    revision_tabla: str
    bpmn_url: str | None


class Salud(BaseModel):
    estado: str


class EventoObservacion(BaseModel):
    accion: str
    fecha: str
    autor: str | None = None
    estado: str | None = None


class RespuestaObservacion(BaseModel):
    id: str
    texto: str
    formato: str = "texto"
    autor: str
    fecha: str


class ObservacionVista(BaseModel):
    id: str
    elemento: str = ""
    referencia: str = ""
    texto: str
    formato: str = "texto"
    autor: str
    tipo: str = "OBSERVACION"
    estado: str = "ABIERTA"
    fecha: str
    actualizada: str | None = None
    historial: list[EventoObservacion] = Field(default_factory=list)
    respuestas: list[RespuestaObservacion] = Field(default_factory=list)


class ListadoObservaciones(BaseModel):
    modelo: str
    observaciones: list[ObservacionVista]
    revision: str


class RegistroObservacion(ObservacionVista):
    revision: str


class ArchivoSesion(BaseModel):
    nombre: str
    sha256: str | None


class ValidacionSesion(BaseModel):
    salida: str
    errores: str
    codigo: int


class PreparacionSesion(BaseModel):
    revision_sesion: int
    cambios: list[str]
    diff: str
    validacion: ValidacionSesion
    aplicable: bool
    numeracion: dict[str, int] | None = None
    hallazgos_aceptados: dict[str, str] | None = None


class SesionVista(BaseModel):
    sesion: str
    codigo: str
    creada: str
    estado: str
    archivos: dict[str, ArchivoSesion]
    revision: int
    preparacion: PreparacionSesion | None = None
    integrada: str | None = None


class DocumentoCopia(BaseModel):
    nombre: str
    texto: str
    revision: str


class EdicionCopia(BaseModel):
    nombre: str
    revision: str
    revision_sesion: int


class IntegracionVista(BaseModel):
    sesion: str
    codigo: str
    estado: str
    cambios: list[str]
