"""Versiones livianas de los modelos: cada sesión integrada es una versión numerada por proceso.

No copia contenido: la versión apunta a la sesión, cuya carpeta conserva el estado anterior (``origen/``) y el
integrado (``copia/``). Al integrar se calcula una sola vez el cambio por elemento de la tabla y se agrega una
línea al registro ``.mesa-versiones/<codigo>.jsonl`` (fuera de Git). Ver ``docs/plan-versiones-validacion.md``.
"""

from __future__ import annotations

import difflib
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from filelock import FileLock, Timeout

from .auditoria import _tabla
from .identificadores import gid
from .repositorio import ErrorDominio, RepositorioProcesos

DOCUMENTOS = ("tabla", "sustento", "fuentes_visor")
SECCIONES = ("Pools", "Mensajes")


def _texto(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8") if ruta.is_file() else ""


def _seccion(texto: str, titulo: str) -> list[dict[str, str]]:
    return _tabla(texto, titulo) if texto else []


def cambios_elementos(anterior: str, nuevo: str) -> dict:
    """Compara las filas de la sección «Elementos» por ID: agregadas, retiradas y modificadas campo a campo."""
    antes = {f["ID"]: f for f in _seccion(anterior, "Elementos") if f.get("ID")}
    despues = {f["ID"]: f for f in _seccion(nuevo, "Elementos") if f.get("ID")}

    def resumen(fila: dict) -> dict:
        return {"id": fila["ID"], "numero": fila.get("Numero", ""), "nombre": fila.get("Nombre", "")}

    modificados = []
    for identificador in [i for i in despues if i in antes]:
        a, d = antes[identificador], despues[identificador]
        campos = {c: [a.get(c, ""), d.get(c, "")] for c in sorted(set(a) | set(d)) if a.get(c, "") != d.get(c, "")}
        if campos:
            modificados.append({**resumen(d), "campos": campos})
    return {
        "agregados": [resumen(despues[i]) for i in despues if i not in antes],
        "retirados": [resumen(antes[i]) for i in antes if i not in despues],
        "modificados": modificados,
    }


class ServicioVersiones:
    """Registro de versiones por proceso; solo agrega líneas y nunca reescribe versiones anteriores."""

    def __init__(self, repositorio: RepositorioProcesos, almacen: Path | None = None, sesiones: Path | None = None):
        self.repositorio = repositorio
        base = repositorio.raiz / "05-herramientas" / "gestor-modelos"
        self.sesiones = (sesiones or base / ".mesa-sesiones").resolve()
        self.almacen = (almacen or self.sesiones.with_name(".mesa-versiones")).resolve()

    def _registro(self, codigo: str) -> Path:
        self.repositorio.carpeta(codigo)
        return self.almacen / f"{codigo}.jsonl"

    def _bloqueo(self, codigo: str) -> FileLock:
        self.almacen.mkdir(parents=True, exist_ok=True)
        return FileLock(str(self.almacen / f".{codigo}.lock"), timeout=10)

    def _leer_todas(self, codigo: str) -> list[dict]:
        registro = self._registro(codigo)
        if not registro.is_file():
            return []
        versiones = []
        for numero, linea in enumerate(registro.read_text(encoding="utf-8").splitlines(), start=1):
            if not linea.strip():
                continue
            try:
                versiones.append(json.loads(linea))
            except json.JSONDecodeError as exc:
                raise ErrorDominio(f"Registro de versiones ilegible en la línea {numero}", 500) from exc
        return versiones

    def registrar(self, codigo: str, carpeta_sesion: Path, manifest: dict) -> dict:
        """Crea la versión siguiente a partir de una sesión recién integrada."""
        origen, copia = carpeta_sesion / "origen", carpeta_sesion / "copia"
        archivos = manifest["archivos"]
        nombre = {clave: archivos[clave]["nombre"] for clave in archivos}
        tabla_antes, tabla_despues = _texto(origen / nombre["tabla"]), _texto(copia / nombre["tabla"])
        documentos = {
            clave: (origen / nombre[clave]).read_bytes() != (copia / nombre[clave]).read_bytes()
            if (copia / nombre[clave]).is_file()
            else False
            for clave in DOCUMENTOS
            if clave in nombre
        }
        secciones = {titulo: _seccion(tabla_antes, titulo) != _seccion(tabla_despues, titulo) for titulo in SECCIONES}
        hashes = {}
        for clave in ("tabla", "sustento", "bpmn"):
            ruta = copia / nombre.get(clave, "")
            existe = clave in nombre and ruta.is_file()
            hashes[clave] = hashlib.sha256(ruta.read_bytes()).hexdigest() if existe else None
        try:
            with self._bloqueo(codigo):
                anteriores = self._leer_todas(codigo)
                version = {
                    "numero": (anteriores[-1]["numero"] + 1) if anteriores else 1,
                    "codigo": codigo,
                    "fecha": datetime.now(timezone.utc).isoformat(),
                    "sesion": manifest["sesion"],
                    "modo": manifest.get("modo", "EDICION"),
                    "titular": manifest.get("titular"),
                    "motivo": manifest.get("motivo"),
                    "observacion": manifest.get("observacion"),
                    "trabajo": manifest.get("trabajo"),
                    "documentos": documentos,
                    "secciones": secciones,
                    "elementos": cambios_elementos(tabla_antes, tabla_despues),
                    "hashes": hashes,
                }
                with self._registro(codigo).open("a", encoding="utf-8") as registro:
                    registro.write(json.dumps(version, ensure_ascii=False) + "\n")
                return version
        except Timeout as exc:
            raise ErrorDominio("El registro de versiones está ocupado", 409) from exc

    def listar(self, codigo: str) -> dict:
        """Versiones del proceso, de la más reciente a la más antigua, con conteos en lugar del detalle."""
        versiones = []
        for version in reversed(self._leer_todas(codigo)):
            elementos = version.get("elementos", {})
            resumen = {k: v for k, v in version.items() if k != "elementos"}
            claves = ("agregados", "retirados", "modificados")
            resumen["conteo"] = {clave: len(elementos.get(clave, [])) for clave in claves}
            versiones.append(resumen)
        return {"codigo": codigo, "versiones": versiones}

    def _version(self, codigo: str, numero: int) -> dict:
        version = next((v for v in self._leer_todas(codigo) if v.get("numero") == numero), None)
        if version is None:
            raise ErrorDominio("Versión no encontrada", 404)
        return version

    def _carpeta(self, codigo: str, version: dict) -> tuple[Path, dict]:
        carpeta = self.sesiones / codigo / version["sesion"]
        try:
            manifest = json.loads((carpeta / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ErrorDominio("La sesión de esta versión ya no está disponible", 404) from exc
        return carpeta, manifest

    def leer(self, codigo: str, numero: int) -> dict:
        """Versión con su cambio por elemento y el diff de texto de tabla y sustento."""
        version = self._version(codigo, numero)
        carpeta, manifest = self._carpeta(codigo, version)
        diferencias = {}
        for clave in ("tabla", "sustento"):
            nombre = manifest["archivos"][clave]["nombre"]
            antes = _texto(carpeta / "origen" / nombre).splitlines(keepends=True)
            despues = _texto(carpeta / "copia" / nombre).splitlines(keepends=True)
            diferencias[clave] = "".join(
                difflib.unified_diff(antes, despues, f"v{numero - 1}/{nombre}", f"v{numero}/{nombre}")
            )
        # El ID BPMN se deriva del nombre de la tabla y del ID de fila, como en el visor (identificadores.gid).
        semilla = manifest["archivos"]["tabla"]["nombre"].removesuffix(".md")
        elementos = {
            clave: [{**e, "bpmn_id": gid(semilla, "nodo", e["id"])} for e in lista]
            for clave, lista in version.get("elementos", {}).items()
        }
        return {**version, "elementos": elementos, "diff": diferencias}

    def bpmn(self, codigo: str, numero: int) -> bytes:
        """BPMN tal como quedó integrado en la versión."""
        version = self._version(codigo, numero)
        carpeta, manifest = self._carpeta(codigo, version)
        ruta = carpeta / "copia" / manifest["archivos"]["bpmn"]["nombre"]
        if not ruta.is_file():
            raise ErrorDominio("La versión no conserva BPMN", 404)
        return ruta.read_bytes()
