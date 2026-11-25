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


class AnalisisVista(BaseModel):
    texto: str
    formato: str = "texto"
    clase: str
    fuentes: list[str] = Field(default_factory=list)
    hipotesis: list[str] = Field(default_factory=list)
    autor: str
    fecha: str
    revision_modelo: str | None = None


class ReemplazoVista(BaseModel):
    fecha: str
    autor: str
    motivo: str


class OpcionVista(BaseModel):
    id: str
    titulo: str
    detalle: str
    formato: str = "texto"
    efecto: str
    elementos: list[str] = Field(default_factory=list)
    fuentes: list[str] = Field(default_factory=list)
    recomendada: bool = False


class PropuestaVista(BaseModel):
    seleccion: str
    opciones: list[OpcionVista]
    autor: str
    fecha: str


class VinculoVista(BaseModel):
    id: str
    referencia: str | None = None


class DefinicionVista(BaseModel):
    tipo: str
    opciones: list[str] = Field(default_factory=list)
    texto: str = ""
    formato: str = "texto"
    vinculada_a: VinculoVista | None = None
    autor: str
    fecha: str
    revision_modelo: str | None = None


class CorreccionVista(BaseModel):
    autor: str
    fecha: str
    revision_modelo: str | None = None
    vigencia_confirmada: bool = False


class AplicacionVista(BaseModel):
    texto: str
    formato: str = "texto"
    sesion: str | None = None
    cambios: list[str] = Field(default_factory=list)
    validacion: str | None = None
    decision: str | None = None
    autor: str
    fecha: str
    cerrada: bool = True
    revision_modelo: str | None = None


class ResolucionVista(BaseModel):
    analisis: AnalisisVista | None = None
    propuesta: PropuestaVista | None = None
    definicion: DefinicionVista | None = None
    correccion: CorreccionVista | None = None
    aplicacion: AplicacionVista | None = None
    reemplazada: ReemplazoVista | None = None


class ObservacionVista(BaseModel):
    id: str
    elemento: str = ""
    referencia: str = ""
    texto: str
    formato: str = "texto"
    autor: str
    tipo: str = "OBSERVACION"
    estado: str = "ABIERTA"
    etapa: str | None = None
    fecha: str
    actualizada: str | None = None
    historial: list[EventoObservacion] = Field(default_factory=list)
    respuestas: list[RespuestaObservacion] = Field(default_factory=list)
    resolucion: ResolucionVista | None = None
    resoluciones_anteriores: list[ResolucionVista] = Field(default_factory=list)


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


class ObservacionEnEtapa(BaseModel):
    codigo: str
    id: str
    referencia: str | None = None
    tipo: str | None = None
    etapa: str
    autor: str | None = None
    texto: str
    resolucion: ResolucionVista | None = None


class ObservacionesPorEtapa(BaseModel):
    etapa: str | None = None
    total: int
    por_etapa: dict[str, int]
    observaciones: list[ObservacionEnEtapa]
