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

    def _resolver_elemento(self, codigo: str, elemento: str, referencia: str) -> tuple[str, str]:
        """Acepta el ID BPMN, el ID de la tabla o el número de caja; completa la referencia «Caja N (ID)»."""
        if not elemento or not isinstance(elemento, str):
            return elemento, referencia
        try:
            raiz = ElementTree.parse(self.repositorio.bpmn(codigo)).getroot()
            if any(nodo.get("id") == elemento for nodo in raiz.iter()):
                return elemento, referencia
        except (ErrorDominio, OSError, ElementTree.ParseError):
            return elemento, referencia
        try:
            elementos = self.repositorio.leer_modelo(codigo).get("elementos", {})
        except (ErrorDominio, OSError, ValueError):
            return elemento, referencia
        if elemento in elementos:
            datos = elementos[elemento]
        else:
            coincidencias = [(clave, datos) for clave, datos in elementos.items()
                             if elemento in (datos.get("ref"), str(datos.get("numero") or ""))]  # fmt: skip
            if len(coincidencias) != 1:
                return elemento, referencia
            elemento, datos = coincidencias[0]
        if not referencia and datos.get("ref"):
            numero = datos.get("numero")
            referencia = f"Caja {numero} ({datos['ref']})" if numero else datos["ref"]
        return elemento, referencia

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
        elemento, referencia = self._resolver_elemento(codigo, elemento, referencia)
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
                    "etapa": "REGISTRADA",
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
                if estado == "RESUELTA":
                    registro["etapa"] = "RESUELTA"
                else:
                    resolucion = registro.get("resolucion") or {}
                    decidida = any(resolucion.get(c) for c in ("definicion", "correccion", "aplicacion", "cierre"))
                    if decidida:  # Reabrir conserva la resolución anterior y reinicia el ciclo de etapas (DEC-065).
                        registro.setdefault("resoluciones_anteriores", []).append(registro.pop("resolucion"))
                        registro["etapa"] = "REGISTRADA"
                    else:  # Cerrada sin decisión: se retoma donde quedó, con su análisis y propuesta.
                        registro["etapa"] = (
                            "PROPUESTA"
                            if resolucion.get("propuesta")
                            else "EN-ANALISIS"
                            if resolucion.get("analisis")
                            else "REGISTRADA"
                        )
                evento = {"accion": "ESTADO_CAMBIADO", "fecha": fecha, "estado": estado}
                if autor.strip():
                    evento["autor"] = autor.strip()
                registro.setdefault("historial", []).append(evento)
                self._guardar(archivo, datos)
                return {**registro, "revision": _revision(datos)}
        except Timeout as exc:
            raise ErrorDominio("El registro de observaciones esta ocupado", 409) from exc

    def redactar(
        self,
        codigo: str,
        identificador: str,
        texto: str,
        autor: str,
        revision_esperada: str,
        motivo: str,
        formato: str = "html",
    ) -> dict:
        """Mejora la redacción de una observación sin cambiar su sentido; solo su autor puede hacerlo.

        El texto anterior y su formato quedan en el historial (evento REDACTADA), de modo que el análisis y la
        propuesta siguen siendo verificables contra lo que se escribió originalmente."""
        contenido = self._validar_texto_autor(texto, autor, formato)
        motivo = (motivo or "").strip()
        if len(motivo) < 10 or len(motivo) > 300:
            raise ErrorDominio("Indique el motivo de la nueva redacción (10 a 300 caracteres)")
        try:
            with self._bloqueo, self._bloqueo_archivo(codigo):
                archivo, datos = self._leer(codigo)
                self._comprobar_revision(datos, revision_esperada)
                registro = next((o for o in datos["observaciones"] if o.get("id") == identificador), None)
                if registro is None:
                    raise ErrorDominio("Observacion no encontrada", 404)
                if registro.get("autor", "").strip().casefold() != autor.strip().casefold():
                    raise ErrorDominio("Solo el autor de la observación puede cambiar su redacción", 403)
                if registro.get("texto") == contenido and registro.get("formato", "texto") == formato:
                    return {**registro, "revision": _revision(datos)}
                fecha = datetime.now(timezone.utc).isoformat()
                registro.setdefault("historial", []).append(
                    {
                        "accion": "REDACTADA",
                        "fecha": fecha,
                        "autor": autor.strip(),
                        "motivo": motivo,
                        "texto_anterior": registro.get("texto", ""),
                        "formato_anterior": registro.get("formato", "texto"),
                    }
                )
                registro.update(texto=contenido, formato=formato, actualizada=fecha)
                self._guardar(archivo, datos)
                return {**registro, "revision": _revision(datos)}
        except Timeout as exc:
            raise ErrorDominio("El registro de observaciones esta ocupado", 409) from exc

    def conteo_abiertas(self) -> dict:
        """Observaciones ABIERTAS por proceso, para los contadores del árbol; omite los procesos sin abiertas."""

        def codigos(nodo: dict) -> list[str]:
            return [nodo["codigo"], *(c for hijo in nodo["hijos"] for c in codigos(hijo))]

        abiertas = {}
        for codigo in codigos(self.repositorio.arbol())[1:]:  # el primero es «Nivel 0», sin carpeta propia
            archivo = self.repositorio.rutas(codigo)["observaciones"]
            if not archivo.is_file():
                continue
            try:
                datos = json.loads(archivo.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue  # un archivo ilegible se informa al abrir el proceso, no rompe el árbol
            cantidad = sum(1 for o in datos.get("observaciones", []) if o.get("estado") == "ABIERTA")
            if cantidad:
                abiertas[codigo] = cantidad
        return {"abiertas": abiertas}

    def anotar_evento(self, codigo: str, identificador: str, evento: dict) -> None:
        """Agrega al historial un evento generado por el sistema (p. ej., la versión que atendió la observación).

        No exige revisión esperada: no cambia contenido ni estado, solo deja trazabilidad durable en Git."""
        try:
            with self._bloqueo, self._bloqueo_archivo(codigo):
                archivo, datos = self._leer(codigo)
                registro = next((o for o in datos["observaciones"] if o.get("id") == identificador), None)
                if registro is None:
                    raise ErrorDominio("Observacion no encontrada", 404)
                registro.setdefault("historial", []).append({**evento, "fecha": datetime.now(timezone.utc).isoformat()})
                self._guardar(archivo, datos)
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
