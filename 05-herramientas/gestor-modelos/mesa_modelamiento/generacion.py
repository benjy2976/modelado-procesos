"""Generación focalizada de un modelo con el generador vigente, compartida por CLI y MCP.

Envuelve `modelar.py` sin cambiar su contrato y devuelve la salida y el informe D1–D5. Adoptar un modelo con
hallazgos (`forzar`) exige una justificación explícita, que debe quedar además documentada en el sustento.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .repositorio import ErrorDominio, RepositorioProcesos

PROGRAMA = Path(__file__).resolve().parents[1] / "modelar.py"
MINIMO_JUSTIFICACION = 20


def validar_justificacion(justificacion: str) -> str:
    texto = " ".join((justificacion or "").split())
    if len(texto) < MINIMO_JUSTIFICACION:
        raise ErrorDominio(
            f"Para adoptar hallazgos indique una justificación de al menos {MINIMO_JUSTIFICACION} caracteres "
            "y documéntela en el sustento"
        )
    return texto


def informe_validacion(raiz: Path, tabla: Path, limite: int = 12000) -> str | None:
    """Texto del informe D1–D5 que el generador deja en 99-temporal/modelos/<tabla>/validacion.txt."""
    carpeta = tabla.name.removesuffix("-tabla.md")
    archivo = raiz / "99-temporal" / "modelos" / carpeta / "validacion.txt"
    return archivo.read_text(encoding="utf-8", errors="replace")[-limite:] if archivo.is_file() else None


def generar_modelo(
    repositorio: RepositorioProcesos,
    codigo: str,
    *,
    check: bool = False,
    exportar_imagenes: bool = False,
    sin_cache: bool = False,
    forzar: bool = False,
    justificacion: str = "",
) -> dict:
    """Genera o comprueba un modelo y devuelve salida, código y validación D1–D5."""
    tabla = repositorio.rutas(codigo)["tabla"]
    if not tabla.is_file():
        raise ErrorDominio(f"El proceso {codigo} aun no tiene tabla", 404)
    opciones = [("--check", check), ("--exportar-imagenes", exportar_imagenes), ("--sin-cache", sin_cache)]
    if forzar:
        justificacion = validar_justificacion(justificacion)
        opciones.append(("--forzar", True))
    banderas = [bandera for bandera, activa in opciones if activa]
    proceso = subprocess.run(
        [sys.executable, str(PROGRAMA), codigo, *banderas],
        cwd=repositorio.raiz,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    resultado = {
        "codigo": codigo,
        "opciones": banderas,
        "codigo_salida": proceso.returncode,
        "adoptado": proceso.returncode == 0 and not check,
        "salida": proceso.stdout[-8000:],
        "errores": proceso.stderr[-4000:],
        "validacion": informe_validacion(repositorio.raiz, tabla),
    }
    if forzar:
        resultado["hallazgos_aceptados"] = {
            "justificacion": justificacion,
            "recordatorio": "La justificación debe constar en el sustento del proceso (AGENTS.md).",
        }
    return resultado
