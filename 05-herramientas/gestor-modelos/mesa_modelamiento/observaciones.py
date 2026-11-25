"""Registro de revision compatible con los JSON del visor existente."""

from __future__ import annotations

import hashlib
import json
import os
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree

from filelock import FileLock, Timeout

from .contenido_enriquecido import MAXIMO_HTML, sanear_html
from .repositorio import ErrorDominio, RepositorioProcesos

BPMN = "{http://www.omg.org/spec/BPMN/20100524/MODEL}"


def _revision(datos: dict) -> str:
    canonico = json.dumps(datos, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonico.encode("utf-8")).hexdigest()


class ServicioObservaciones:
    """Escritura atomica y serializada entre CLI, API y MCP locales."""

    def __init__(self, repositorio: RepositorioProcesos):
        self.repositorio = repositorio
        self._bloqueo = threading.RLock()

    def _bloqueo_archivo(self, codigo: str) -> FileLock:
        # Los locks son operativos y no forman parte del expediente versionado.
        self.repositorio.carpeta(codigo)
        carpeta = self.repositorio.raiz / "99-temporal" / "modelos" / "bloqueos"
        carpeta.mkdir(parents=True, exist_ok=True)
        return FileLock(str(carpeta / f"{codigo}.observaciones.lock"), timeout=10)

    def _leer(self, codigo: str) -> tuple[Path, dict]:
        rutas = self.repositorio.rutas(codigo)
        archivo = rutas["observaciones"]
        if archivo.is_file():
            try:
                datos = json.loads(archivo.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise ErrorDominio("Archivo de observaciones ilegible", 500) from exc
            if not isinstance(datos, dict) or not isinstance(datos.get("observaciones"), list):
                raise ErrorDominio("Archivo de observaciones invalido", 500)
        else:
            datos = {
                "modelo": rutas["html"].relative_to(self.repositorio.raiz).as_posix(),
                "observaciones": [],
            }
        return archivo, datos

    def listar(self, codigo: str) -> dict:
        with self._bloqueo:
            _, datos = self._leer(codigo)
            return {**datos, "revision": _revision(datos)}

    def _comprobar_revision(self, datos: dict, esperada: str) -> None:
        if not esperada or esperada != _revision(datos):
            raise ErrorDominio("Las observaciones cambiaron; recarga antes de guardar", 409)

    def _comprobar_elemento(self, codigo: str, elemento: str) -> None:
        if elemento == "":
            return
        if not isinstance(elemento, str) or len(elemento) > 200:
            raise ErrorDominio("ID BPMN invalido")
        try:
            raiz = ElementTree.parse(self.repositorio.bpmn(codigo)).getroot()
        except ElementTree.ParseError as exc:
            raise ErrorDominio("BPMN invalido", 500) from exc
        if not any(nodo.tag.startswith(BPMN) and nodo.get("id") == elemento for nodo in raiz.iter()):
            raise ErrorDominio("El elemento no existe en el BPMN", 404)

    @staticmethod
    def _validar_texto_autor(texto: str, autor: str, formato: str = "texto") -> str:
        """Valida autor y contenido; devuelve el texto listo para guardar (HTML ya saneado)."""
        if not isinstance(autor, str) or not 1 <= len(autor.strip()) <= 100:
            raise ErrorDominio("Autor o equipo invalido")
        if formato not in {"texto", "html"}:
            raise ErrorDominio("Formato de texto invalido")
        if not isinstance(texto, str):
            raise ErrorDominio("El texto debe tener entre 1 y 4000 caracteres")
        if formato == "texto":
            if not 1 <= len(texto.strip()) <= 4000:
                raise ErrorDominio("El texto debe tener entre 1 y 4000 caracteres")
            return texto.strip()
        if len(texto) > MAXIMO_HTML:
            raise ErrorDominio(f"El contenido HTML no debe superar {MAXIMO_HTML} caracteres")
        saneado, visible = sanear_html(texto)
        if not 1 <= len(visible) <= 4000:
            raise ErrorDominio("El texto visible debe tener entre 1 y 4000 caracteres")
        return saneado

    def agregar(
        self,
        codigo: str,
        *,
        elemento: str,
        texto: str,
        autor: str,
        revision_esperada: str,
        tipo: str = "OBSERVACION",
        referencia: str = "",
        formato: str = "texto",
    ) -> dict:
        if tipo not in {"OBSERVACION", "COMENTARIO"}:
            raise ErrorDominio("Tipo de registro invalido")
        contenido = self._validar_texto_autor(texto, autor, formato)
        if not isinstance(referencia, str) or len(referencia) > 100:
            raise ErrorDominio("Referencia invalida")
        try:
            with self._bloqueo, self._bloqueo_archivo(codigo):
                self._comprobar_elemento(codigo, elemento)
                archivo, datos = self._leer(codigo)
                self._comprobar_revision(datos, revision_esperada)
                fecha = datetime.now(timezone.utc).isoformat()
                registro = {
                    "id": str(uuid.uuid4()),
                    "elemento": elemento,
                    "referencia": referencia,
                    "texto": contenido,
                    "formato": formato,
                    "autor": autor.strip(),
                    "tipo": tipo,
                    "estado": "ABIERTA",
                    "fecha": fecha,
                    "historial": [{"accion": "CREADA", "fecha": fecha, "autor": autor.strip()}],
                    "respuestas": [],
                }
                datos["observaciones"].append(registro)
                self._guardar(archivo, datos)
                return {**registro, "revision": _revision(datos)}
        except Timeout as exc:
            raise ErrorDominio("El registro de observaciones esta ocupado", 409) from exc

    def responder(
        self, codigo: str, identificador: str, texto: str, autor: str, revision_esperada: str, formato: str = "texto"
    ) -> dict:
        contenido = self._validar_texto_autor(texto, autor, formato)
        try:
            with self._bloqueo, self._bloqueo_archivo(codigo):
                archivo, datos = self._leer(codigo)
                self._comprobar_revision(datos, revision_esperada)
                registro = next((o for o in datos["observaciones"] if o.get("id") == identificador), None)
                if registro is None:
                    raise ErrorDominio("Observacion no encontrada", 404)
                fecha = datetime.now(timezone.utc).isoformat()
                respuesta = {
                    "id": str(uuid.uuid4()),
                    "texto": contenido,
                    "formato": formato,
                    "autor": autor.strip(),
                    "fecha": fecha,
                }
                registro.setdefault("respuestas", []).append(respuesta)
                registro.setdefault("historial", []).append(
                    {"accion": "RESPONDIDA", "fecha": fecha, "autor": autor.strip()}
                )
                registro["actualizada"] = fecha
                self._guardar(archivo, datos)
                return {**registro, "revision": _revision(datos)}
        except Timeout as exc:
            raise ErrorDominio("El registro de observaciones esta ocupado", 409) from exc

    def actualizar_estado(
        self, codigo: str, identificador: str, estado: str, revision_esperada: str, autor: str = ""
    ) -> dict:
        if estado not in {"ABIERTA", "RESUELTA"}:
            raise ErrorDominio("Estado de observacion invalido")
        if not isinstance(autor, str) or len(autor) > 100:
            raise ErrorDominio("Autor o equipo invalido")
        try:
            with self._bloqueo, self._bloqueo_archivo(codigo):
                archivo, datos = self._leer(codigo)
                self._comprobar_revision(datos, revision_esperada)
                registro = next((o for o in datos["observaciones"] if o.get("id") == identificador), None)
                if registro is None:
                    raise ErrorDominio("Observacion no encontrada", 404)
                if registro["estado"] == estado:
                    return {**registro, "revision": _revision(datos)}
                fecha = datetime.now(timezone.utc).isoformat()
                registro["estado"] = estado
                registro["actualizada"] = fecha
                evento = {"accion": "ESTADO_CAMBIADO", "fecha": fecha, "estado": estado}
                if autor.strip():
                    evento["autor"] = autor.strip()
                registro.setdefault("historial", []).append(evento)
                self._guardar(archivo, datos)
                return {**registro, "revision": _revision(datos)}
        except Timeout as exc:
            raise ErrorDominio("El registro de observaciones esta ocupado", 409) from exc

    @staticmethod
    def _guardar(archivo: Path, datos: dict) -> None:
        temporal = archivo.with_name(f"{archivo.name}.{uuid.uuid4().hex}.tmp")
        try:
            temporal.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.replace(temporal, archivo)
        finally:
            temporal.unlink(missing_ok=True)
