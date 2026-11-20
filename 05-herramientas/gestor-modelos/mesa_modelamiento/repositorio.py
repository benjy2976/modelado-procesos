"""Acceso acotado a los procesos y sus derivados de lectura."""

from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path

from .visor_datos import datos_visor

CODIGO = re.compile(r"S\d+(?:\.\d+)*\Z")
CARPETA = re.compile(r"^(S\d+(?:-\d+)*)-(.+)$")


class ErrorDominio(Exception):
    """Error controlado que los adaptadores pueden presentar al usuario."""

    def __init__(self, mensaje: str, codigo_http: int = 400):
        super().__init__(mensaje)
        self.codigo_http = codigo_http


class RepositorioProcesos:
    def __init__(self, raiz: Path):
        self.raiz = raiz.resolve()
        self.procesos = self.raiz / "02-procesos"

    @classmethod
    def desde_entorno(cls) -> RepositorioProcesos:
        predeterminada = Path(__file__).resolve().parents[3]
        return cls(Path(os.environ.get("PROCESOS_REPO_ROOT", predeterminada)))

    def carpeta(self, codigo: str) -> Path:
        if not isinstance(codigo, str) or not CODIGO.fullmatch(codigo):
            raise ErrorDominio("Codigo de proceso invalido")
        clave = codigo.replace(".", "-")
        encontradas = []
        for ruta in self.procesos.rglob(f"{clave}-*"):
            identidad = CARPETA.fullmatch(ruta.name)
            if (
                ruta.is_dir()
                and identidad
                and identidad.group(1) == clave
                and "to-be" not in ruta.relative_to(self.procesos).parts
            ):
                encontradas.append(ruta)
        if len(encontradas) != 1:
            raise ErrorDominio(f"Proceso {codigo} no encontrado o ambiguo", 404)
        return encontradas[0]

    def rutas(self, codigo: str) -> dict[str, Path]:
        carpeta = self.carpeta(codigo)
        prefijo = codigo.replace(".", "-")
        return {
            nombre: carpeta / f"{prefijo}-{sufijo}"
            for nombre, sufijo in {
                "tabla": "diagrama-proceso-tabla.md",
                "bpmn": "diagrama-proceso.bpmn",
                "html": "diagrama-proceso.html",
                "sustento": "sustento.md",
                "observaciones": "observaciones.json",
            }.items()
        }

    def arbol(self) -> dict:
        def nodo(carpeta: Path) -> dict:
            identidad = CARPETA.fullmatch(carpeta.name)
            codigo = identidad.group(1).replace("-", ".")
            prefijo = identidad.group(1)
            indice = next(iter(sorted(carpeta.glob("00-*.md"))), None)
            bpmn = carpeta / f"{prefijo}-diagrama-proceso.bpmn"
            hijos = [nodo(p) for p in sorted(carpeta.iterdir()) if p.is_dir() and CARPETA.fullmatch(p.name)]
            return {
                "codigo": codigo,
                "nombre": identidad.group(2).replace("-", " ").capitalize(),
                "indice": indice.relative_to(self.raiz).as_posix() if indice else None,
                "bpmn": f"/api/procesos/{codigo}/bpmn" if bpmn.is_file() else None,
                "hijos": hijos,
            }

        mapa = self.procesos / "mapa-de-procesos-institucional" / "mapa-procesos-nivel-0.md"
        return {
            "codigo": "Nivel 0",
            "nombre": "Mapa de procesos institucional",
            "indice": mapa.relative_to(self.raiz).as_posix() if mapa.is_file() else None,
            "bpmn": None,
            "hijos": [nodo(p) for p in sorted(self.procesos.iterdir()) if p.is_dir() and CARPETA.fullmatch(p.name)],
        }

    def leer_modelo(self, codigo: str) -> dict:
        rutas = self.rutas(codigo)
        tabla = rutas["tabla"]
        if not tabla.is_file():
            raise ErrorDominio(f"El proceso {codigo} aun no tiene tabla", 404)
        datos = datos_visor(tabla, rutas["html"], self.raiz)
        datos["revision_tabla"] = hashlib.sha256(tabla.read_bytes()).hexdigest()
        datos["bpmn_url"] = f"/api/procesos/{codigo}/bpmn" if rutas["bpmn"].is_file() else None
        return datos

    def bpmn(self, codigo: str) -> Path:
        ruta = self.rutas(codigo)["bpmn"]
        if not ruta.is_file():
            raise ErrorDominio(f"El proceso {codigo} aun no tiene BPMN", 404)
        return ruta
