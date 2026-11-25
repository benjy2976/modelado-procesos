"""Cola de trabajos para los agentes de OpenClaw (DEC-068), compartida por CLI, API y MCP.

Un trabajo pide a un agente una etapa sobre una observación: ANALISIS (análisis y propuesta, a pedido del usuario)
o APLICACION (aplicar lo definido por una persona). La cola es estado operativo: vive fuera de Git, en
`.mesa-trabajos/`, y la trazabilidad durable queda en la observación (etapas, historial y evidencia).
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from filelock import FileLock, Timeout

from .repositorio import ErrorDominio, RepositorioProcesos

TIPOS = ("ANALISIS", "APLICACION")
ESTADOS = ("PENDIENTE", "EN-CURSO", "HECHO", "ERROR", "CANCELADO")
ACTIVOS = ("PENDIENTE", "EN-CURSO")
VENCIMIENTO_MINUTOS = 45  # Un trabajo tomado y no completado en este plazo vuelve a quedar disponible.


def _ahora() -> datetime:
    return datetime.now(timezone.utc)


class ServicioTrabajos:
    """Encola, entrega y cierra trabajos con bloqueo de archivo y escritura atómica."""

    def __init__(self, repositorio: RepositorioProcesos, almacen: Path | None = None):
        self.repositorio = repositorio
        base = almacen or repositorio.raiz / "05-herramientas" / "gestor-modelos" / ".mesa-trabajos"
        self.almacen = base.resolve()

    @property
    def _archivo(self) -> Path:
        return self.almacen / "cola.json"

    def _bloqueo(self) -> FileLock:
        self.almacen.mkdir(parents=True, exist_ok=True)
        return FileLock(str(self.almacen / "cola.lock"), timeout=10)

    def _leer(self) -> dict:
        if not self._archivo.is_file():
            return {"trabajos": []}
        try:
            return json.loads(self._archivo.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ErrorDominio("Cola de trabajos ilegible", 500) from exc

    def _guardar(self, datos: dict) -> None:
        temporal = self._archivo.with_name(f"cola.{uuid.uuid4().hex}.tmp")
        try:
            temporal.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.replace(temporal, self._archivo)
        finally:
            temporal.unlink(missing_ok=True)

    @staticmethod
    def _evento(trabajo: dict, accion: str, autor: str, **extra: object) -> None:
        trabajo.setdefault("historial", []).append(
            {"accion": accion, "autor": autor, "fecha": _ahora().isoformat(), **extra}
        )

    @staticmethod
    def _vencido(trabajo: dict) -> bool:
        tomado = trabajo.get("tomado_en")
        if trabajo.get("estado") != "EN-CURSO" or not tomado:
            return False
        return _ahora() - datetime.fromisoformat(tomado) > timedelta(minutes=VENCIMIENTO_MINUTOS)

    def encolar(
        self, tipo: str, codigo: str, observacion: str, solicitante: str, referencia: str = "", nota: str = ""
    ) -> dict:
        """Crea un trabajo; si ya hay uno activo del mismo tipo para la observación, lo devuelve sin duplicar."""
        if tipo not in TIPOS:
            raise ErrorDominio(f"Tipo de trabajo inválido; use {TIPOS}")
        if not isinstance(solicitante, str) or not 1 <= len(solicitante.strip()) <= 100:
            raise ErrorDominio("Indique quién solicita el trabajo")
        self.repositorio.carpeta(codigo)
        try:
            with self._bloqueo():
                datos = self._leer()
                for trabajo in datos["trabajos"]:
                    if (trabajo["tipo"], trabajo["observacion"], trabajo["estado"]) in {
                        (tipo, observacion, estado) for estado in ACTIVOS
                    } and not self._vencido(trabajo):
                        return {**trabajo, "duplicado": True}
                trabajo = {
                    "id": str(uuid.uuid4()), "tipo": tipo, "codigo": codigo, "observacion": observacion,
                    "referencia": referencia, "estado": "PENDIENTE", "solicitante": solicitante.strip(),
                    "nota": nota.strip()[:1000], "creado": _ahora().isoformat(), "intentos": 0,
                }  # fmt: skip
                self._evento(trabajo, "ENCOLADO", solicitante.strip())
                datos["trabajos"].append(trabajo)
                self._guardar(datos)
                return trabajo
        except Timeout as exc:
            raise ErrorDominio("La cola de trabajos está ocupada", 409) from exc

    def listar(
        self,
        estado: str | None = None,
        tipo: str | None = None,
        codigo: str | None = None,
        observacion: str | None = None,
        limite: int = 100,
    ) -> dict:
        datos = self._leer()
        conteo: dict[str, int] = {}
        elegidos = []
        for trabajo in datos["trabajos"]:
            efectivo = "PENDIENTE" if self._vencido(trabajo) else trabajo["estado"]
            conteo[efectivo] = conteo.get(efectivo, 0) + 1
            filtros = ((estado, efectivo), (tipo, trabajo["tipo"]), (codigo, trabajo["codigo"]),
                       (observacion, trabajo["observacion"]))  # fmt: skip
            if all(esperado in (None, real) for esperado, real in filtros):
                elegidos.append({**trabajo, "estado": efectivo})
        elegidos = elegidos[-max(1, min(int(limite), 500)) :]
        return {"total": len(elegidos), "por_estado": conteo, "trabajos": elegidos}

    def tomar(self, tipo: str, agente: str, codigo: str | None = None, lote: bool = False) -> dict:
        """Entrega el trabajo pendiente más antiguo (o, con lote, todos los del mismo proceso) y lo marca EN-CURSO.

        La aplicación se toma por lote para editar cada proceso en una sola sesión."""
        if tipo not in TIPOS:
            raise ErrorDominio(f"Tipo de trabajo inválido; use {TIPOS}")
        try:
            with self._bloqueo():
                datos = self._leer()
                disponibles = [t for t in datos["trabajos"] if t["tipo"] == tipo
                               and (t["estado"] == "PENDIENTE" or self._vencido(t))
                               and codigo in (None, t["codigo"])]  # fmt: skip
                if not disponibles:
                    return {"tomados": [], "detalle": "No hay trabajos pendientes"}
                primero = disponibles[0]
                elegidos = [t for t in disponibles if t["codigo"] == primero["codigo"]] if lote else [primero]
                for trabajo in elegidos:
                    trabajo.update(estado="EN-CURSO", tomado_por=agente, tomado_en=_ahora().isoformat())
                    trabajo["intentos"] = trabajo.get("intentos", 0) + 1
                    self._evento(trabajo, "TOMADO", agente)
                self._guardar(datos)
                return {"tomados": elegidos, "codigo": primero["codigo"]}
        except Timeout as exc:
            raise ErrorDominio("La cola de trabajos está ocupada", 409) from exc

    def completar(self, identificador: str, agente: str, resultado: str, estado: str = "HECHO") -> dict:
        """Cierra un trabajo como HECHO o ERROR con un resumen; la evidencia completa queda en la observación."""
        if estado not in {"HECHO", "ERROR"}:
            raise ErrorDominio("El trabajo se completa como HECHO o ERROR")
        if not isinstance(resultado, str) or not resultado.strip():
            raise ErrorDominio("Indique el resultado del trabajo")
        return self._cerrar(identificador, agente, estado, resultado.strip()[:4000], ("EN-CURSO",))

    def cancelar(self, identificador: str, autor: str, motivo: str) -> dict:
        if not isinstance(motivo, str) or not motivo.strip():
            raise ErrorDominio("Indique el motivo de la cancelación")
        return self._cerrar(identificador, autor, "CANCELADO", motivo.strip()[:1000], ACTIVOS)

    def _cerrar(self, identificador: str, autor: str, estado: str, texto: str, permitidos: tuple) -> dict:
        try:
            with self._bloqueo():
                datos = self._leer()
                trabajo = next((t for t in datos["trabajos"] if t["id"] == identificador), None)
                if trabajo is None:
                    raise ErrorDominio("Trabajo no encontrado", 404)
                if trabajo["estado"] not in permitidos:
                    raise ErrorDominio(f"El trabajo está {trabajo['estado']}", 409)
                trabajo.update(estado=estado, resultado=texto, terminado=_ahora().isoformat())
                self._evento(trabajo, estado, autor)
                self._guardar(datos)
                return trabajo
        except Timeout as exc:
            raise ErrorDominio("La cola de trabajos está ocupada", 409) from exc
