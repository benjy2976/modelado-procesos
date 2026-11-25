"""Etapas de resolución de observaciones (DEC-065), compartidas por CLI, API y MCP.

REGISTRADA → EN-ANALISIS → PROPUESTA → DEFINIDA → EN-CORRECCION → RESUELTA (o PENDIENTE-EVIDENCIA).
El agente analiza y propone; solo una persona define; la corrección aplica exactamente lo definido y se cierra
con evidencia. Ninguna etapa equivale a revisión de equipo, opinión técnica ni aprobación.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from datetime import datetime, timezone

from filelock import Timeout

from .observaciones import ServicioObservaciones, _revision
from .repositorio import ErrorDominio
from .trabajos import ServicioTrabajos

ETAPAS = ("REGISTRADA", "EN-ANALISIS", "PROPUESTA", "DEFINIDA", "EN-CORRECCION", "PENDIENTE-EVIDENCIA", "RESUELTA")
CLASES = ("ERROR-MODELO", "EXPLICACION-AUSENTE", "DIFERENCIA-CRITERIO", "FALTA-EVIDENCIA", "FUERA-DE-ALCANCE")
EFECTOS = ("CAMBIO-MODELO", "CAMBIO-SUSTENTO", "DECISION", "ACLARACION", "NO-PROCEDE", "PENDIENTE-EVIDENCIA")
DEFINICIONES = ("OPCION", "OPCIONES", "MANUAL", "VINCULADA")
AUTORES_AGENTE = {"claudia"}
MAXIMO_OPCIONES = 8


def etapa(registro: dict) -> str:
    """Etapa de un registro; los anteriores a DEC-065 se derivan de su estado."""
    return registro.get("etapa") or ("RESUELTA" if registro.get("estado") == "RESUELTA" else "REGISTRADA")


class ServicioResolucion(ServicioObservaciones):
    """Amplía las observaciones con análisis, propuesta, definición y aplicación trazables."""

    def _revision_modelo(self, codigo: str) -> str | None:
        tabla = self.repositorio.rutas(codigo)["tabla"]
        return hashlib.sha256(tabla.read_bytes()).hexdigest() if tabla.is_file() else None

    def _mutar(
        self, codigo: str, identificador: str, revision_esperada: str, cambio: Callable[[dict, str], str]
    ) -> dict:
        """Aplica un cambio a un registro con revisión esperada, bloqueo y evento de historial."""
        try:
            with self._bloqueo, self._bloqueo_archivo(codigo):
                archivo, datos = self._leer(codigo)
                self._comprobar_revision(datos, revision_esperada)
                registro = next((o for o in datos["observaciones"] if o.get("id") == identificador), None)
                if registro is None:
                    raise ErrorDominio("Observacion no encontrada", 404)
                fecha = datetime.now(timezone.utc).isoformat()
                accion = cambio(registro, fecha)
                registro["actualizada"] = fecha
                registro.setdefault("historial", []).append(
                    {"accion": accion, "fecha": fecha, "autor": registro["_autor_evento"], "estado": etapa(registro)}
                )
                registro.pop("_autor_evento", None)
                self._guardar(archivo, datos)
                return {**registro, "revision": _revision(datos)}
        except Timeout as exc:
            raise ErrorDominio("El registro de observaciones esta ocupado", 409) from exc

    @staticmethod
    def _exigir_etapa(registro: dict, permitidas: tuple[str, ...], accion: str) -> None:
        actual = etapa(registro)
        if actual not in permitidas:
            raise ErrorDominio(f"No se puede {accion} una observación en etapa {actual}", 409)

    def registrar_analisis(
        self,
        codigo: str,
        identificador: str,
        *,
        texto: str,
        clase: str,
        autor: str,
        revision_esperada: str,
        fuentes: list[str] | None = None,
        formato: str = "texto",
        hipotesis: list[str] | None = None,
        motivo: str = "",
    ) -> dict:
        """Etapa EN-ANALISIS: qué entiende el agente, contexto consultado, hipótesis consideradas y clase.

        Un nuevo análisis conserva el anterior (con su propuesta) en resoluciones_anteriores y exige motivo."""
        if clase not in CLASES:
            raise ErrorDominio(f"Clase de análisis inválida; use {CLASES}")
        contenido = self._validar_texto_autor(texto, autor, formato)
        fuentes = [str(f).strip() for f in fuentes or [] if str(f).strip()][:30]
        hipotesis = [str(h).strip()[:400] for h in hipotesis or [] if str(h).strip()][:20]
        revision_modelo = self._revision_modelo(codigo)

        def cambio(registro: dict, fecha: str) -> str:
            self._exigir_etapa(registro, ("REGISTRADA", "EN-ANALISIS", "PROPUESTA", "DEFINIDA"), "analizar")
            anterior = registro.get("resolucion") or {}
            if anterior.get("analisis"):  # Nada se sobrescribe: el análisis previo y su propuesta se conservan.
                if not motivo.strip():
                    raise ErrorDominio("Indique el motivo para reemplazar el análisis anterior")
                registro.setdefault("resoluciones_anteriores", []).append(
                    {**anterior, "reemplazada": {"fecha": fecha, "autor": autor.strip(), "motivo": motivo.strip()}}
                )
            registro["resolucion"] = {
                "analisis": {
                    "texto": contenido,
                    "formato": formato,
                    "clase": clase,
                    "fuentes": fuentes,
                    "hipotesis": hipotesis,
                    "autor": autor.strip(),
                    "fecha": fecha,
                    "revision_modelo": revision_modelo,
                }
            }
            registro["etapa"] = "EN-ANALISIS"
            registro["_autor_evento"] = autor.strip()
            return "ANALIZADA"

        return self._mutar(codigo, identificador, revision_esperada, cambio)

    def registrar_propuesta(
        self,
        codigo: str,
        identificador: str,
        *,
        opciones: list[dict],
        autor: str,
        revision_esperada: str,
        seleccion: str = "UNICA",
    ) -> dict:
        """Etapa PROPUESTA: una o varias opciones; seleccion UNICA o MULTIPLE."""
        if seleccion not in {"UNICA", "MULTIPLE"}:
            raise ErrorDominio("La selección debe ser UNICA o MULTIPLE")
        if not isinstance(opciones, list) or not 1 <= len(opciones) <= MAXIMO_OPCIONES:
            raise ErrorDominio(f"Indique entre 1 y {MAXIMO_OPCIONES} opciones")
        preparadas, recomendadas = [], 0
        for numero, opcion in enumerate(opciones):
            if not isinstance(opcion, dict):
                raise ErrorDominio("Cada opción debe ser un objeto")
            titulo = str(opcion.get("titulo", "")).strip()
            if not 1 <= len(titulo) <= 160:
                raise ErrorDominio(f"La opción {numero + 1} necesita un título de hasta 160 caracteres")
            if opcion.get("efecto") not in EFECTOS:
                raise ErrorDominio(f"Efecto inválido en la opción {numero + 1}; use {EFECTOS}")
            formato = opcion.get("formato", "texto")
            detalle = self._validar_texto_autor(str(opcion.get("detalle", "")), autor, formato)
            recomendadas += bool(opcion.get("recomendada"))
            preparadas.append(
                {
                    "id": chr(ord("A") + numero),
                    "titulo": titulo,
                    "detalle": detalle,
                    "formato": formato,
                    "efecto": opcion["efecto"],
                    "elementos": [str(e) for e in opcion.get("elementos") or []][:30],
                    "fuentes": [str(f) for f in opcion.get("fuentes") or []][:30],
                    "recomendada": bool(opcion.get("recomendada")),
                }
            )
        if recomendadas > 1 and seleccion == "UNICA":
            raise ErrorDominio("Con selección única solo una opción puede ser la recomendada")

        def cambio(registro: dict, fecha: str) -> str:
            self._exigir_etapa(registro, ("EN-ANALISIS", "PROPUESTA"), "proponer para")
            registro["resolucion"]["propuesta"] = {
                "seleccion": seleccion,
                "opciones": preparadas,
                "autor": autor.strip(),
                "fecha": fecha,
            }
            registro["resolucion"].pop("definicion", None)
            registro["etapa"] = "PROPUESTA"
            registro["_autor_evento"] = autor.strip()
            return "PROPUESTA"

        return self._mutar(codigo, identificador, revision_esperada, cambio)

    def definir(
        self,
        codigo: str,
        identificador: str,
        *,
        tipo: str,
        autor: str,
        revision_esperada: str,
        opciones: list[str] | None = None,
        texto: str = "",
        formato: str = "texto",
        vinculada_a: str = "",
    ) -> dict:
        """Etapa DEFINIDA: solo una persona acoge una opción, varias, una respuesta manual o un vínculo."""
        if tipo not in DEFINICIONES:
            raise ErrorDominio(f"Tipo de definición inválido; use {DEFINICIONES}")
        if not isinstance(autor, str) or autor.strip().casefold() in AUTORES_AGENTE:
            raise ErrorDominio("La definición la hace una persona; el agente solo analiza y propone", 403)
        contenido = self._validar_texto_autor(texto, autor, formato) if (texto or tipo == "MANUAL") else ""
        elegidas = list(dict.fromkeys(opciones or []))
        vinculo = None
        if tipo == "VINCULADA":
            otra = next((o for o in self.listar(codigo)["observaciones"] if o["id"] == vinculada_a), None)
            if otra is None or otra["id"] == identificador:
                raise ErrorDominio("Indique otra observación del mismo proceso para vincular", 404)
            if etapa(otra) != "RESUELTA":
                raise ErrorDominio("Solo se vincula a una observación ya resuelta", 409)
            vinculo = {"id": otra["id"], "referencia": otra.get("referencia")}
        revision_modelo = self._revision_modelo(codigo)

        def cambio(registro: dict, fecha: str) -> str:
            resolucion = registro.setdefault("resolucion", {})
            if tipo in {"OPCION", "OPCIONES"}:
                self._exigir_etapa(registro, ("PROPUESTA",), "acoger opciones de")
                propuesta = resolucion["propuesta"]
                validas = {o["id"] for o in propuesta["opciones"]}
                if not elegidas or set(elegidas) - validas:
                    raise ErrorDominio(f"Elija opciones existentes: {sorted(validas)}")
                if tipo == "OPCION" and len(elegidas) != 1:
                    raise ErrorDominio("OPCION acoge exactamente una opción")
                if propuesta["seleccion"] == "UNICA" and len(elegidas) > 1:
                    raise ErrorDominio("La propuesta admite una sola opción")
            else:
                self._exigir_etapa(registro, ("REGISTRADA", "EN-ANALISIS", "PROPUESTA"), "definir")
            resolucion["definicion"] = {
                "tipo": tipo,
                "opciones": elegidas if tipo in {"OPCION", "OPCIONES"} else [],
                "texto": contenido,
                "formato": formato,
                "vinculada_a": vinculo,
                "autor": autor.strip(),
                "fecha": fecha,
                "revision_modelo": revision_modelo,
            }
            registro["etapa"] = "DEFINIDA"
            registro["_autor_evento"] = autor.strip()
            return "DEFINIDA"

        registro = self._mutar(codigo, identificador, revision_esperada, cambio)
        # Lo definido se aplica en otra pasada (DEC-065): queda en la cola para el agente de aplicación (DEC-068).
        trabajo = ServicioTrabajos(self.repositorio).encolar(
            "APLICACION", codigo, identificador, autor.strip(), registro.get("referencia") or ""
        )
        return {**registro, "trabajo": {"id": trabajo["id"], "tipo": trabajo["tipo"], "estado": trabajo["estado"]}}

    def solicitar_analisis(self, codigo: str, identificador: str, solicitante: str, nota: str = "") -> dict:
        """Encola el análisis de una observación a pedido de una persona (botón «Solicitar análisis»)."""
        registro = next((o for o in self.listar(codigo)["observaciones"] if o["id"] == identificador), None)
        if registro is None:
            raise ErrorDominio("Observacion no encontrada", 404)
        actual = etapa(registro)
        if actual not in ("REGISTRADA", "EN-ANALISIS", "PROPUESTA"):
            raise ErrorDominio(f"No se solicita análisis de una observación en etapa {actual}", 409)
        if actual == "PROPUESTA" and not nota.strip():
            raise ErrorDominio("Para reanalizar una propuesta indique el motivo en la nota")
        return ServicioTrabajos(self.repositorio).encolar(
            "ANALISIS", codigo, identificador, solicitante, registro.get("referencia") or "", nota
        )

    def iniciar_correccion(
        self, codigo: str, identificador: str, *, autor: str, revision_esperada: str, confirmar_vigencia: bool = False
    ) -> dict:
        """Etapa EN-CORRECCION. Si la tabla cambió desde la definición, exige confirmar que sigue aplicando."""
        actual = self._revision_modelo(codigo)

        def cambio(registro: dict, fecha: str) -> str:
            self._exigir_etapa(registro, ("DEFINIDA",), "corregir")
            definida = registro["resolucion"]["definicion"].get("revision_modelo")
            if definida and actual != definida and not confirmar_vigencia:
                raise ErrorDominio(
                    "La tabla cambió desde la definición; confirme que la definición sigue aplicando "
                    "(confirmar_vigencia) o vuelva a analizar",
                    409,
                )
            registro["resolucion"]["correccion"] = {
                "autor": autor.strip(),
                "fecha": fecha,
                "revision_modelo": actual,
                "vigencia_confirmada": bool(definida and actual != definida),
            }
            registro["etapa"] = "EN-CORRECCION"
            registro["_autor_evento"] = autor.strip()
            return "CORRECCION-INICIADA"

        return self._mutar(codigo, identificador, revision_esperada, cambio)

    def registrar_aplicacion(
        self,
        codigo: str,
        identificador: str,
        *,
        texto: str,
        autor: str,
        revision_esperada: str,
        cerrar: bool = True,
        sesion: str = "",
        cambios: list[str] | None = None,
        validacion: str = "",
        decision: str = "",
        formato: str = "texto",
    ) -> dict:
        """Cierra con evidencia (RESUELTA) o deja la observación en PENDIENTE-EVIDENCIA si cerrar es falso."""
        contenido = self._validar_texto_autor(texto, autor, formato)
        if decision and not decision.startswith("DEC-"):
            raise ErrorDominio("La decisión debe ser un identificador DEC-NNN")

        def cambio(registro: dict, fecha: str) -> str:
            self._exigir_etapa(registro, ("EN-CORRECCION", "DEFINIDA"), "registrar la aplicación de")
            definicion = registro["resolucion"].get("definicion") or {}
            efectos = {
                o["efecto"]
                for o in (registro["resolucion"].get("propuesta") or {}).get("opciones", [])
                if o["id"] in definicion.get("opciones", [])
            }
            if cerrar and "CAMBIO-MODELO" in efectos and not sesion:
                raise ErrorDominio("Un cambio de modelo se cierra con la sesión de edición que lo integró")
            registro["resolucion"]["aplicacion"] = {
                "texto": contenido,
                "formato": formato,
                "sesion": sesion or None,
                "cambios": [str(c) for c in cambios or []][:30],
                "validacion": validacion[-4000:] or None,
                "decision": decision or None,
                "autor": autor.strip(),
                "fecha": fecha,
                "cerrada": cerrar,
                "revision_modelo": self._revision_modelo(codigo),
            }
            registro["etapa"] = "RESUELTA" if cerrar else "PENDIENTE-EVIDENCIA"
            registro["estado"] = "RESUELTA" if cerrar else "ABIERTA"
            registro["_autor_evento"] = autor.strip()
            return "APLICADA" if cerrar else "EN-ESPERA-DE-EVIDENCIA"

        return self._mutar(codigo, identificador, revision_esperada, cambio)

    def por_etapa(self, etapa_buscada: str | None = None, codigo: str | None = None, detalle: bool = True) -> dict:
        """Observaciones por etapa en un proceso o en todo el árbol (p. ej. las DEFINIDA para corregir)."""
        if etapa_buscada and etapa_buscada not in ETAPAS:
            raise ErrorDominio(f"Etapa inválida; use {ETAPAS}")
        codigos = [codigo] if codigo else self._codigos()
        resultado, conteo = [], {}
        for actual in codigos:
            try:
                if not self.repositorio.rutas(actual)["observaciones"].is_file():
                    continue
            except ErrorDominio:
                continue
            for registro in self.listar(actual)["observaciones"]:
                nombre = etapa(registro)
                conteo[nombre] = conteo.get(nombre, 0) + 1
                if etapa_buscada in (None, nombre):
                    resultado.append(
                        {
                            "codigo": actual,
                            "id": registro["id"],
                            "referencia": registro.get("referencia"),
                            "tipo": registro.get("tipo"),
                            "etapa": nombre,
                            "autor": registro.get("autor"),
                            "texto": registro["texto"][:240],
                            **({"resolucion": registro.get("resolucion")} if detalle else {}),
                        }
                    )
        return {"etapa": etapa_buscada, "total": len(resultado), "por_etapa": conteo, "observaciones": resultado}

    def _codigos(self) -> list[str]:
        salida: list[str] = []

        def recorrer(nodo: dict) -> None:
            if nodo.get("codigo"):
                salida.append(nodo["codigo"])
            for hijo in nodo.get("hijos", []):
                recorrer(hijo)

        recorrer(self.repositorio.arbol())
        return [c for c in salida if c != "Nivel 0"]
