"""Sesiones aisladas y recuperables para editar modelos lógicos."""

from __future__ import annotations

import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

from filelock import FileLock, Timeout

from .auditoria import _tabla
from .generacion import validar_justificacion
from .repositorio import ErrorDominio, RepositorioProcesos
from .visor_datos import datos_visor

SESION = re.compile(r"[0-9a-f]{32}\Z")
EDITABLES = ("tabla", "sustento", "fuentes_visor")
GENERADOS = ("bpmn", "html")
# EDICION toma el bloqueo del proceso (un solo titular); BORRADOR es una copia que no bloquea y solo se integra
# si el proceso está libre (DEC-069).
MODOS = ("EDICION", "BORRADOR")


def _ahora() -> datetime:
    return datetime.now(timezone.utc)


def _vigencia() -> timedelta:
    """Minutos sin actividad tras los que vence el bloqueo de edición (MESA_BLOQUEO_MINUTOS, 30 por defecto)."""
    try:
        minutos = int(os.environ.get("MESA_BLOQUEO_MINUTOS", "30"))
    except ValueError:
        minutos = 30
    return timedelta(minutes=max(1, minutos))


def _hash(contenido: bytes) -> str:
    return hashlib.sha256(contenido).hexdigest()


def _es_aprobado(contenido: bytes) -> bool:
    texto = contenido.decode("utf-8-sig", errors="replace")
    cabecera = texto.split("---", 2)
    return len(cabecera) >= 3 and bool(re.search(r"(?m)^estado_institucional:\s*APROBADO\s*$", cabecera[1]))


class ServicioSesiones:
    """Un titular de edición por proceso, con bloqueo que vence; nunca borra instantáneas ni sesiones cerradas."""

    def __init__(self, repositorio: RepositorioProcesos, almacen: Path | None = None):
        self.repositorio = repositorio
        self.almacen = (almacen or repositorio.raiz / "05-herramientas" / "gestor-modelos" / ".mesa-sesiones").resolve()

    def _carpeta_proceso(self, codigo: str) -> Path:
        self.repositorio.carpeta(codigo)
        return self.almacen / codigo

    def _bloqueo(self, codigo: str) -> FileLock:
        carpeta = self._carpeta_proceso(codigo)
        carpeta.mkdir(parents=True, exist_ok=True)
        return FileLock(str(carpeta / ".edicion.lock"), timeout=10)

    def _sesion(self, codigo: str, identificador: str) -> Path:
        if not SESION.fullmatch(identificador):
            raise ErrorDominio("Identificador de sesión inválido")
        carpeta = self._carpeta_proceso(codigo) / identificador
        if not carpeta.is_dir():
            raise ErrorDominio("Sesión no encontrada", 404)
        return carpeta

    @staticmethod
    def _manifest(carpeta: Path) -> dict:
        try:
            return json.loads((carpeta / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ErrorDominio("Manifiesto de sesión ilegible", 500) from exc

    @staticmethod
    def _guardar_json(ruta: Path, datos: dict) -> None:
        temporal = ruta.with_name(f".{ruta.name}.{uuid.uuid4().hex}.tmp")
        try:
            temporal.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            os.replace(temporal, ruta)
        finally:
            temporal.unlink(missing_ok=True)

    def _rutas(self, codigo: str) -> dict[str, Path]:
        rutas = self.repositorio.rutas(codigo)
        rutas["fuentes_visor"] = self.repositorio.carpeta(codigo) / f"{codigo.replace('.', '-')}-fuentes-visor.json"
        return rutas

    def _leer_activa(self, codigo: str) -> dict | None:
        """Registro del bloqueo de edición del proceso, o None si está libre."""
        archivo = self._carpeta_proceso(codigo) / "activa.json"
        if not archivo.is_file():
            return None
        try:
            registro = json.loads(archivo.read_text(encoding="utf-8"))
            if not SESION.fullmatch(registro["sesion"]):
                raise KeyError("sesion")
        except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ErrorDominio("Registro de sesión activa ilegible", 500) from exc
        return registro

    @staticmethod
    def _vigente(registro: dict) -> bool:
        """Un bloqueo sin vencimiento (anterior a DEC-069) se considera vigente hasta liberarlo."""
        vence = registro.get("vence")
        return not vence or datetime.fromisoformat(vence) > _ahora()

    def _soltar(self, codigo: str, registro: dict, estado: str, **extra: object) -> None:
        """Marca la sesión titular con el estado dado (si seguía abierta) y deja el proceso libre."""
        try:
            carpeta = self._sesion(codigo, registro["sesion"])
            manifest = self._manifest(carpeta)
            if manifest["estado"] == "ABIERTA":
                manifest.update(estado=estado, terminada=_ahora().isoformat(), **extra)
                self._guardar_json(carpeta / "manifest.json", manifest)
        except ErrorDominio:
            pass  # la carpeta de una sesión ilegible o ausente no impide liberar el proceso
        (self._carpeta_proceso(codigo) / "activa.json").unlink(missing_ok=True)

    def _ocupante(self, codigo: str) -> dict | None:
        """Bloqueo vigente del proceso; si venció, lo suelta (la sesión queda VENCIDA) y devuelve None."""
        registro = self._leer_activa(codigo)
        if registro and not self._vigente(registro):
            self._soltar(codigo, registro, "VENCIDA")
            return None
        return registro

    def _renovar(self, codigo: str, manifest: dict) -> None:
        """Exige que una sesión de EDICION siga siendo titular y prolonga su bloqueo; los borradores no bloquean."""
        if manifest.get("modo", "EDICION") != "EDICION":
            return
        registro = self._ocupante(codigo)
        if registro is None:
            raise ErrorDominio("La sesión perdió el bloqueo del proceso (venció o fue liberada); inicie otra", 409)
        if registro["sesion"] != manifest["sesion"]:
            raise ErrorDominio(f"El proceso está en edición por {registro.get('titular', 'otra sesión')}", 409)
        registro["renovado"] = _ahora().isoformat()
        registro["vence"] = (_ahora() + _vigencia()).isoformat()
        self._guardar_json(self._carpeta_proceso(codigo) / "activa.json", registro)

    def estado(self, codigo: str) -> dict:
        """Estado del modelo para coordinar editores: LIBRE, EN-EDICION (titular y vencimiento) o APROBADO."""
        try:
            with self._bloqueo(codigo):
                rutas = self._rutas(codigo)
                aprobado = any(rutas[n].is_file() and _es_aprobado(rutas[n].read_bytes()) for n in EDITABLES)
                registro = self._ocupante(codigo)
                borradores = []
                base = self._carpeta_proceso(codigo)
                for manifiesto in sorted(base.glob("*/manifest.json")):
                    try:
                        datos = json.loads(manifiesto.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError):
                        continue
                    if datos.get("modo") == "BORRADOR" and datos.get("estado") == "ABIERTA":
                        borradores.append({k: datos.get(k) for k in ("sesion", "titular", "motivo", "creada")})
        except Timeout as exc:
            raise ErrorDominio("El proceso está ocupado", 409) from exc
        estado = "APROBADO" if aprobado else "EN-EDICION" if registro else "LIBRE"
        # Huella barata del contenido vigente: la vista la compara para recargar el diagrama cuando cambia.
        marcas = [
            f"{n}:{r.stat().st_mtime_ns}:{r.stat().st_size}" if r.is_file() else f"{n}:-"
            for n, r in sorted(rutas.items())
            if n in (*EDITABLES, "bpmn")
        ]
        huella = hashlib.sha256("|".join(marcas).encode("utf-8")).hexdigest()[:16]
        return {"codigo": codigo, "estado": estado, "bloqueo": registro, "borradores": borradores, "huella": huella}

    def iniciar(
        self,
        codigo: str,
        titular: str = "persona",
        motivo: str = "",
        modo: str = "EDICION",
        observacion: str | None = None,
        trabajo: str | None = None,
    ) -> dict:
        """Captura bytes del árbol de trabajo, incluidos los no confirmados en Git.

        En modo EDICION toma el bloqueo del proceso a nombre del titular; si otro lo tiene vigente, responde 409 con
        quién y hasta cuándo. En modo BORRADOR no bloquea."""
        if modo not in MODOS:
            raise ErrorDominio(f"Modo inválido; use {MODOS}")
        titular = (titular or "").strip()[:120]
        if not titular:
            raise ErrorDominio("Indique el titular de la sesión")
        motivo = (motivo or "").strip()[:500]
        try:
            with self._bloqueo(codigo):
                base = self._carpeta_proceso(codigo)
                activa = base / "activa.json"
                if modo == "EDICION":
                    registro = self._ocupante(codigo)
                    if registro:
                        quien = registro.get("titular", "otra sesión")
                        hasta = f" hasta {registro['vence']}" if registro.get("vence") else ""
                        para = f" ({registro['motivo']})" if registro.get("motivo") else ""
                        raise ErrorDominio(
                            f"El proceso está en edición por {quien}{para}{hasta}; sesión {registro['sesion']}", 409
                        )
                rutas = self._rutas(codigo)
                if not rutas["tabla"].is_file() or not rutas["sustento"].is_file():
                    raise ErrorDominio("El proceso requiere tabla y sustento para editar", 404)
                for nombre in EDITABLES:
                    if rutas[nombre].is_file() and _es_aprobado(rutas[nombre].read_bytes()):
                        raise ErrorDominio(f"El documento {nombre} está APROBADO y no puede editarse", 409)
                identificador = uuid.uuid4().hex
                carpeta = base / identificador
                origen = carpeta / "origen"
                copia = carpeta / "copia"
                origen.mkdir(parents=True)
                copia.mkdir()
                archivos: dict[str, dict] = {}
                for nombre in (*EDITABLES, *GENERADOS):
                    ruta = rutas[nombre]
                    if ruta.is_file():
                        contenido = ruta.read_bytes()
                        (origen / ruta.name).write_bytes(contenido)
                        (copia / ruta.name).write_bytes(contenido)
                        archivos[nombre] = {"nombre": ruta.name, "sha256": _hash(contenido)}
                    else:
                        archivos[nombre] = {"nombre": ruta.name, "sha256": None}
                        if nombre == "fuentes_visor":
                            (copia / ruta.name).write_text('{"elementos": {}}\n', encoding="utf-8")
                creada = _ahora()
                manifest = {
                    "sesion": identificador,
                    "codigo": codigo,
                    "creada": creada.isoformat(),
                    "estado": "ABIERTA",
                    "modo": modo,
                    "titular": titular,
                    "motivo": motivo,
                    "observacion": observacion,
                    "trabajo": trabajo,
                    "archivos": archivos,
                    "revision": 0,
                }
                self._guardar_json(carpeta / "manifest.json", manifest)
                if modo == "EDICION":
                    self._guardar_json(
                        activa,
                        {
                            "sesion": identificador,
                            "titular": titular,
                            "motivo": motivo,
                            "observacion": observacion,
                            "trabajo": trabajo,
                            "desde": creada.isoformat(),
                            "vence": (creada + _vigencia()).isoformat(),
                        },
                    )
                return manifest
        except Timeout as exc:
            raise ErrorDominio("El proceso está ocupado", 409) from exc

    def leer(self, codigo: str, identificador: str) -> dict:
        carpeta = self._sesion(codigo, identificador)
        return self._manifest(carpeta)

    def activa(self, codigo: str) -> dict | None:
        """Sesión titular del bloqueo vigente; None si el proceso está libre o el bloqueo venció."""
        try:
            with self._bloqueo(codigo):
                registro = self._ocupante(codigo)
        except Timeout as exc:
            raise ErrorDominio("El proceso está ocupado", 409) from exc
        return self.leer(codigo, registro["sesion"]) if registro else None

    def liberar(self, codigo: str, autor: str, motivo: str) -> dict:
        """Una persona libera un bloqueo (por ejemplo, de un agente caído); la sesión queda LIBERADA con el motivo."""
        autor, motivo = (autor or "").strip()[:120], (motivo or "").strip()[:500]
        if not autor or len(motivo) < 10:
            raise ErrorDominio("Indique autor y un motivo de al menos 10 caracteres")
        try:
            with self._bloqueo(codigo):
                registro = self._leer_activa(codigo)
                if registro is None:
                    return {"codigo": codigo, "estado": "LIBRE", "detalle": "El proceso ya estaba libre"}
                self._soltar(codigo, registro, "LIBERADA", liberada_por=autor, motivo_liberacion=motivo)
                liberada = {"liberada": registro["sesion"], "titular": registro.get("titular")}
                return {"codigo": codigo, "estado": "LIBRE", **liberada}
        except Timeout as exc:
            raise ErrorDominio("El proceso está ocupado", 409) from exc

    def contenido(self, codigo: str, identificador: str, nombre: str) -> dict:
        if nombre not in EDITABLES:
            raise ErrorDominio("Documento no editable", 404)
        carpeta = self._sesion(codigo, identificador)
        manifest = self._manifest(carpeta)
        ruta = carpeta / "copia" / manifest["archivos"][nombre]["nombre"]
        contenido = ruta.read_bytes()
        return {"nombre": nombre, "texto": contenido.decode("utf-8"), "revision": _hash(contenido)}

    def editar(self, codigo: str, identificador: str, nombre: str, texto: str, revision_esperada: str) -> dict:
        if nombre not in EDITABLES:
            raise ErrorDominio("Documento no editable", 404)
        if not isinstance(texto, str) or not texto.strip() or len(texto.encode("utf-8")) > 2_000_000:
            raise ErrorDominio("Contenido vacío o demasiado grande")
        try:
            with self._bloqueo(codigo):
                carpeta = self._sesion(codigo, identificador)
                manifest = self._manifest(carpeta)
                if manifest["estado"] != "ABIERTA":
                    raise ErrorDominio("La sesión no está abierta", 409)
                self._renovar(codigo, manifest)
                ruta = carpeta / "copia" / manifest["archivos"][nombre]["nombre"]
                actual = ruta.read_bytes()
                if _hash(actual) != revision_esperada:
                    raise ErrorDominio("La copia cambió; recargue el documento", 409)
                nuevo = texto.encode("utf-8")
                if _es_aprobado(actual) or _es_aprobado(nuevo):
                    raise ErrorDominio("No se edita un documento APROBADO", 409)
                if nombre == "fuentes_visor":
                    try:
                        datos = json.loads(texto)
                    except json.JSONDecodeError as exc:
                        raise ErrorDominio("Metadatos JSON inválidos") from exc
                    if not isinstance(datos, dict) or not isinstance(datos.get("elementos"), dict):
                        raise ErrorDominio("Metadatos de fuentes inválidos")
                if nuevo != actual:
                    temporal = ruta.with_name(f".{ruta.name}.{uuid.uuid4().hex}.tmp")
                    try:
                        temporal.write_bytes(nuevo)
                        os.replace(temporal, ruta)
                    finally:
                        temporal.unlink(missing_ok=True)
                    manifest["revision"] += 1
                    manifest.pop("preparacion", None)
                    self._guardar_json(carpeta / "manifest.json", manifest)
                return {"nombre": nombre, "revision": _hash(nuevo), "revision_sesion": manifest["revision"]}
        except Timeout as exc:
            raise ErrorDominio("El proceso está ocupado", 409) from exc

    def _ids_tabla_copia(self, codigo: str, identificador: str) -> set[str]:
        tabla = self.contenido(codigo, identificador, "tabla")["texto"]
        return {fila["ID"] for fila in _tabla(tabla, "Elementos") if fila.get("ID")}

    def anclar(
        self,
        codigo: str,
        identificador: str,
        elemento: str,
        fragmento: str,
        cita: str,
        titulo: str,
        ubicacion: str,
        vigencia: str,
    ) -> dict:
        """Ancla una cita verificada de un fragmento a una caja de la copia; reemplaza el ancla de igual ubicación."""
        from .fuentes_anclaje import anclar_fragmento

        if elemento not in self._ids_tabla_copia(codigo, identificador):
            raise ErrorDominio(f"La caja {elemento} no existe en la tabla de la copia", 404)
        for campo, valor in (("titulo", titulo), ("ubicacion", ubicacion), ("vigencia", vigencia), ("cita", cita)):
            if not isinstance(valor, str) or not valor.strip():
                raise ErrorDominio(f"Indique {campo} del ancla")
        resultado = anclar_fragmento(self.repositorio.raiz, fragmento, cita)
        if resultado.get("estado") != "ANCLADO":
            raise ErrorDominio(f"La cita no se pudo anclar: {resultado.get('estado')}", 422)
        documento = self.contenido(codigo, identificador, "fuentes_visor")
        datos = json.loads(documento["texto"])
        entrada = {
            "titulo": titulo.strip(), "ruta": resultado["ruta"], "sha256": resultado["sha256"],
            "pagina": resultado["pagina"], "ubicacion": ubicacion.strip(),
            "fragmento": cita[:157] + ("…" if len(cita) > 157 else ""),
            "consulta": datetime.now(timezone.utc).date().isoformat(), "vigencia": vigencia.strip(),
            "rectangulos": resultado["rectangulos"], "metodo_ancla": "automatico-pdfminer",
        }  # fmt: skip
        if resultado.get("tramos"):
            entrada["tramos"] = resultado["tramos"]
        anclas = datos["elementos"].setdefault(elemento, [])
        misma = (entrada["ruta"], entrada["ubicacion"])
        anclas[:] = [a for a in anclas if (a.get("ruta"), a.get("ubicacion")) != misma]
        anclas.append(entrada)
        texto = json.dumps(datos, ensure_ascii=False, indent=2) + "\n"
        editado = self.editar(codigo, identificador, "fuentes_visor", texto, documento["revision"])
        return {**editado, "elemento": elemento, "pagina": entrada["pagina"], "anclas_del_elemento": len(anclas)}

    def retirar_anclas(
        self, codigo: str, identificador: str, elementos: list[str] | None = None, huerfanas: bool = False
    ) -> dict:
        """Retira anclas de las cajas indicadas y, si se pide, de las que ya no existen en la tabla de la copia."""
        documento = self.contenido(codigo, identificador, "fuentes_visor")
        datos = json.loads(documento["texto"])
        quitar = set(elementos or [])
        if huerfanas:
            vigentes = self._ids_tabla_copia(codigo, identificador)
            quitar |= {clave for clave in datos["elementos"] if clave not in vigentes}
        retiradas = sorted(clave for clave in quitar if clave in datos["elementos"])
        if not retiradas:
            return {"nombre": "fuentes_visor", "revision": documento["revision"], "retiradas": []}
        for clave in retiradas:
            datos["elementos"].pop(clave)
        texto = json.dumps(datos, ensure_ascii=False, indent=2) + "\n"
        editado = self.editar(codigo, identificador, "fuentes_visor", texto, documento["revision"])
        return {**editado, "retiradas": retiradas}

    def preparar(self, codigo: str, identificador: str, *, generar: bool = True, aceptar_hallazgos: str = "") -> dict:
        """Genera en la copia y guarda diff. Solo adopta hallazgos con justificación documentada en el sustento."""
        justificacion = validar_justificacion(aceptar_hallazgos) if aceptar_hallazgos.strip() else ""
        try:
            with self._bloqueo(codigo):
                carpeta = self._sesion(codigo, identificador)
                manifest = self._manifest(carpeta)
                if manifest["estado"] != "ABIERTA":
                    raise ErrorDominio("La sesión no está abierta", 409)
                self._renovar(codigo, manifest)
                tabla = carpeta / "copia" / manifest["archivos"]["tabla"]["nombre"]
                tabla_anterior = carpeta / "origen" / tabla.name
                tabla_modificada = tabla.read_bytes() != tabla_anterior.read_bytes()
                if justificacion:
                    sustento = manifest["archivos"]["sustento"]["nombre"]
                    if (carpeta / "copia" / sustento).read_bytes() == (carpeta / "origen" / sustento).read_bytes():
                        raise ErrorDominio("Documente en el sustento de la copia los hallazgos que acepta", 409)
                numeracion = None
                if generar and tabla_modificada:
                    programa = Path(__file__).resolve().parents[1] / "construir_modelos.py"
                    if not tabla.is_relative_to(self.repositorio.raiz):
                        raise ErrorDominio("La copia debe estar dentro del repositorio para regenerar", 409)
                    modulo = str(programa.parent)
                    if modulo not in sys.path:
                        sys.path.insert(0, modulo)
                    from numerar_modelos import numerar

                    total, nuevos = numerar(tabla)  # Números de referencia persistentes (DEC-044), como modelar.py.
                    numeracion = {"elementos": total, "nuevos": nuevos}
                    forzar = ["--forzar"] if justificacion else []
                    proceso = subprocess.run(
                        [sys.executable, str(programa), "--tabla", str(tabla), *forzar],
                        cwd=self.repositorio.raiz,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        check=False,
                    )
                    informe = {
                        "salida": proceso.stdout[-12000:],
                        "errores": proceso.stderr[-4000:],
                        "codigo": proceso.returncode,
                    }
                elif generar:
                    informe = {"salida": "Tabla sin cambios; se conserva el BPMN vigente.", "errores": "", "codigo": 0}
                else:
                    informe = {"salida": "Generador simulado en prueba", "errores": "", "codigo": 0}
                if generar and informe["codigo"] == 0:
                    try:
                        datos_visor(tabla, self._rutas(codigo)["html"], self.repositorio.raiz)
                    except (OSError, ValueError) as exc:
                        informe["codigo"] = 1
                        informe["errores"] = f"Metadatos de tabla o fuentes inválidos: {exc}"
                cambios = []
                partes = []
                for nombre in (*EDITABLES, *GENERADOS):
                    if nombre not in manifest["archivos"]:
                        continue
                    archivo = manifest["archivos"][nombre]["nombre"]
                    anterior_ruta = carpeta / "origen" / archivo
                    actual_ruta = carpeta / "copia" / archivo
                    anterior = anterior_ruta.read_bytes() if anterior_ruta.is_file() else b""
                    actual = actual_ruta.read_bytes() if actual_ruta.is_file() else b""
                    if anterior == actual or not actual_ruta.is_file():
                        continue
                    if (
                        nombre == "fuentes_visor"
                        and manifest["archivos"][nombre]["sha256"] is None
                        and actual == b'{"elementos": {}}\n'
                    ):
                        continue
                    cambios.append(nombre)
                    if nombre in EDITABLES:
                        partes.extend(
                            difflib.unified_diff(
                                anterior.decode("utf-8").splitlines(keepends=True),
                                actual.decode("utf-8").splitlines(keepends=True),
                                fromfile=f"origen/{archivo}",
                                tofile=f"copia/{archivo}",
                            )
                        )
                    else:
                        partes.append(f"Derivado actualizado: {archivo}\n")
                if ("tabla" in cambios or "fuentes_visor" in cambios or "bpmn" in cambios) and "html" not in cambios:
                    cambios.append("html")
                    partes.append("Vista HTML: se regenerará en la ruta del proceso al integrar.\n")
                preparacion = {
                    "revision_sesion": manifest["revision"],
                    "cambios": cambios,
                    "diff": "".join(partes),
                    "validacion": informe,
                    "aplicable": informe["codigo"] == 0 and bool(cambios),
                }
                if numeracion:
                    preparacion["numeracion"] = numeracion
                if justificacion:
                    preparacion["hallazgos_aceptados"] = {
                        "justificacion": justificacion,
                        "fecha": datetime.now(timezone.utc).isoformat(),
                    }
                manifest["preparacion"] = preparacion
                self._guardar_json(carpeta / "manifest.json", manifest)
                return preparacion
        except Timeout as exc:
            raise ErrorDominio("El proceso está ocupado", 409) from exc

    def integrar(self, codigo: str, identificador: str, revision_esperada: int) -> dict:
        """Integra solo cambios preparados, con detección de conflicto y rollback."""
        try:
            with self._bloqueo(codigo):
                carpeta = self._sesion(codigo, identificador)
                manifest = self._manifest(carpeta)
                preparacion = manifest.get("preparacion") or {}
                if manifest["estado"] != "ABIERTA" or manifest["revision"] != revision_esperada:
                    raise ErrorDominio("La sesión cambió; prepare de nuevo", 409)
                if not preparacion.get("aplicable") or preparacion.get("revision_sesion") != revision_esperada:
                    raise ErrorDominio("Falta preparación válida de la misma revisión", 409)
                if manifest.get("modo", "EDICION") == "EDICION":
                    self._renovar(codigo, manifest)
                else:
                    ocupante = self._ocupante(codigo)
                    if ocupante:
                        raise ErrorDominio(
                            f"El proceso está en edición por {ocupante.get('titular', 'otra sesión')}; "
                            "integre el borrador cuando quede libre",
                            409,
                        )
                rutas = self._rutas(codigo)
                for nombre, registrado in manifest["archivos"].items():
                    ruta = rutas[nombre]
                    esperado = registrado["sha256"]
                    actual = _hash(ruta.read_bytes()) if ruta.is_file() else None
                    if actual != esperado:
                        raise ErrorDominio(f"El destino {nombre} cambió desde la copia; no se integró", 409)
                for nombre in preparacion["cambios"]:
                    if nombre in EDITABLES and rutas[nombre].is_file() and _es_aprobado(rutas[nombre].read_bytes()):
                        raise ErrorDominio(f"El destino {nombre} fue aprobado; no se integró", 409)
                escritos = []
                try:
                    for nombre in preparacion["cambios"]:
                        ruta = rutas[nombre]
                        temporal = ruta.with_name(f".{ruta.name}.{uuid.uuid4().hex}.tmp")
                        try:
                            if nombre == "html":
                                modulo = Path(__file__).resolve().parents[1]
                                if str(modulo) not in sys.path:
                                    sys.path.insert(0, str(modulo))
                                from renderizar_bpmn import pagina_visor_enlazada

                                contenido = pagina_visor_enlazada(self._titulo(rutas["tabla"]), rutas["bpmn"], ruta)
                                temporal.write_bytes(contenido.encode("utf-8"))
                            else:
                                origen = carpeta / "copia" / manifest["archivos"][nombre]["nombre"]
                                temporal.write_bytes(origen.read_bytes())
                            os.replace(temporal, ruta)
                            escritos.append(nombre)
                        finally:
                            temporal.unlink(missing_ok=True)
                except (OSError, RuntimeError, ValueError) as exc:
                    for nombre in reversed(escritos):
                        ruta = rutas[nombre]
                        if manifest["archivos"][nombre]["sha256"] is None:
                            ruta.unlink(missing_ok=True)
                            continue
                        temporal = ruta.with_name(f".{ruta.name}.{uuid.uuid4().hex}.tmp")
                        try:
                            respaldo = carpeta / "origen" / manifest["archivos"][nombre]["nombre"]
                            temporal.write_bytes(respaldo.read_bytes())
                            os.replace(temporal, ruta)
                        finally:
                            temporal.unlink(missing_ok=True)
                    raise ErrorDominio(f"Integración falló; se restauraron los archivos: {exc}", 500) from exc
                manifest["estado"] = "INTEGRADA"
                manifest["integrada"] = _ahora().isoformat()
                self._guardar_json(carpeta / "manifest.json", manifest)
                if manifest.get("modo", "EDICION") == "EDICION":
                    (self._carpeta_proceso(codigo) / "activa.json").unlink(missing_ok=True)
                version = self._registrar_version(codigo, carpeta, manifest)
                resultado = {"sesion": identificador, "codigo": codigo, "estado": "INTEGRADA", "cambios": escritos}
                return {**resultado, "version": version} if version is not None else resultado
        except Timeout as exc:
            raise ErrorDominio("El proceso está ocupado", 409) from exc

    def _registrar_version(self, codigo: str, carpeta: Path, manifest: dict) -> int | None:
        """Numera la integración como versión y lo anota en la observación atendida.

        La integración ya quedó hecha: un fallo del registro se informa en el manifiesto, nunca la revierte."""
        from .observaciones import ServicioObservaciones
        from .versiones import ServicioVersiones

        try:
            version = ServicioVersiones(self.repositorio, sesiones=self.almacen).registrar(codigo, carpeta, manifest)
        except (ErrorDominio, OSError, KeyError) as exc:
            manifest["error_version"] = str(exc)[:500]
            self._guardar_json(carpeta / "manifest.json", manifest)
            return None
        manifest["version"] = version["numero"]
        self._guardar_json(carpeta / "manifest.json", manifest)
        if manifest.get("observacion"):
            try:
                ServicioObservaciones(self.repositorio).anotar_evento(
                    codigo,
                    manifest["observacion"],
                    {"accion": "VERSION_CREADA", "version": version["numero"], "sesion": manifest["sesion"],
                     "autor": manifest.get("titular") or ""},
                )  # fmt: skip
            except ErrorDominio:
                pass  # una observación inexistente no invalida la versión; el vínculo queda en la versión
        return version["numero"]

    @staticmethod
    def _titulo(tabla: Path) -> str:
        encontrado = re.search(r"(?m)^#\s+(.+)$", tabla.read_text(encoding="utf-8"))
        return encontrado.group(1).strip() if encontrado else tabla.stem

    def cerrar(self, codigo: str, identificador: str) -> dict:
        """Libera el editor sin borrar copia, diff ni instantánea."""
        try:
            with self._bloqueo(codigo):
                carpeta = self._sesion(codigo, identificador)
                manifest = self._manifest(carpeta)
                if manifest["estado"] != "ABIERTA":
                    return {**manifest, "detalle": "La sesión ya había terminado; no se modificó"}
                manifest["estado"] = "CERRADA"
                self._guardar_json(carpeta / "manifest.json", manifest)
                registro = self._leer_activa(codigo)
                if registro and registro["sesion"] == identificador:
                    (self._carpeta_proceso(codigo) / "activa.json").unlink(missing_ok=True)
                return manifest
        except Timeout as exc:
            raise ErrorDominio("El proceso está ocupado", 409) from exc
