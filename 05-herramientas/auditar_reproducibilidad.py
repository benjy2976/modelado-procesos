#!/usr/bin/env python3
"""Audita que la base documental pueda reconstruirse sin incluir la cache publica en Git."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_PYTHON = (3, 11)
REGISTRO = ROOT / "01-referencias/00-catalogo/registro-descargas.csv"
CONFIG = ROOT / "05-herramientas/catalogador-documental/fuentes-descarga.json"
BINARIOS_LFS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".png", ".jpg", ".jpeg", ".tif", ".tiff", ".zip", ".7z",
    ".ifc", ".ifczip", ".bcf", ".bcfzip", ".rvt", ".nwd", ".nwc", ".dwg", ".dxf",
}
REQUERIDOS = (
    ".gitattributes",
    ".gitignore",
    "requirements.txt",
    "README.md",
    "AGENTS.md",
    "00-gobernanza/reproducibilidad.md",
    "01-referencias/00-catalogo/registro-descargas.csv",
    "05-herramientas/catalogador-documental/descargar_recursos.py",
    "05-herramientas/catalogador-documental/evaluar_calidad.py",
    "05-herramientas/catalogador-documental/fuentes-descarga.json",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def git(*args: str, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, input=input_bytes, capture_output=True, check=False
    )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for relative in REQUERIDOS:
        if not (ROOT / relative).is_file():
            errors.append(f"Falta archivo requerido: {relative}")

    if sys.version_info[:2] < MIN_PYTHON:
        errors.append(f"Python {sys.version.split()[0]} no cumple el minimo 3.11.")
    requirements = ROOT / "requirements.txt"
    if requirements.is_file():
        dependencies = [
            line.strip() for line in requirements.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        ]
        for dependency in dependencies:
            if "==" not in dependency:
                errors.append(f"Dependencia sin version exacta: {dependency}")

    try:
        json.loads(CONFIG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Configuracion de fuentes invalida: {exc}")

    try:
        with REGISTRO.open(encoding="utf-8-sig", newline="") as stream:
            rows = list(csv.DictReader(stream))
    except OSError as exc:
        errors.append(f"No se puede leer el indice: {exc}")
        rows = []

    paths: list[str] = []
    seen: set[str] = set()
    total_bytes = 0
    for number, row in enumerate(rows, start=2):
        relative_text = row.get("archivo", "").replace("\\", "/")
        relative = Path(relative_text)
        if not relative_text or relative.is_absolute() or ".." in relative.parts:
            errors.append(f"Fila {number}: ruta no relativa o insegura: {relative_text!r}")
            continue
        if relative_text in seen:
            errors.append(f"Fila {number}: ruta duplicada: {relative_text}")
        seen.add(relative_text)
        paths.append(relative_text)
        target = ROOT / relative
        if not target.is_file():
            errors.append(f"Falta recurso restaurado: {relative_text}")
            continue
        total_bytes += target.stat().st_size
        expected_size = row.get("tamano_bytes", "")
        if expected_size.isdigit() and target.stat().st_size != int(expected_size):
            errors.append(f"Tamano no coincide: {relative_text}")
        expected_hash = row.get("sha256", "").upper()
        if len(expected_hash) != 64 or sha256(target) != expected_hash:
            errors.append(f"SHA-256 no coincide: {relative_text}")
        url = row.get("url_solicitada", "")
        if not url.startswith(("https://", "http://")):
            errors.append(f"URL no valida en fila {number}: {url!r}")

    ignored_result = git("check-ignore", "--no-index", "--stdin", input_bytes=("\n".join(paths) + "\n").encode())
    ignored = {line.decode(errors="replace").replace("\\", "/") for line in ignored_result.stdout.splitlines()}
    for relative in paths:
        if relative not in ignored:
            errors.append(f"Recurso publico no ignorado por Git: {relative}")

    candidates_result = git("ls-files", "--cached", "--others", "--exclude-standard", "-z")
    candidates = [item.decode(errors="replace").replace("\\", "/") for item in candidates_result.stdout.split(b"\0") if item]
    for relative in candidates:
        if Path(relative).suffix.lower() not in BINARIOS_LFS:
            continue
        attribute = git("check-attr", "filter", "--", relative).stdout.decode(errors="replace").strip()
        if not attribute.endswith(": lfs"):
            errors.append(f"Binario sin filtro LFS: {relative}")

    if git("lfs", "version").returncode != 0:
        errors.append("Git LFS no esta disponible.")
    if not git("remote").stdout.strip():
        warnings.append("No hay remoto Git; no puede comprobarse clonacion ni transferencia LFS.")
    warnings.append("La disponibilidad futura de las URLs oficiales no puede garantizarse solo con hashes.")

    print(f"Recursos indexados: {len(rows)}")
    print(f"Recursos presentes y revisados: {sum((ROOT / Path(p)).is_file() for p in paths)}")
    print(f"Tamano de cache publica: {total_bytes / (1024 * 1024):.2f} MiB")
    print(f"Archivos versionables o candidatos: {len(candidates)}")
    print(f"Errores: {len(errors)}; advertencias: {len(warnings)}")
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"ADVERTENCIA: {item}")
    if errors:
        print("RESULTADO: NO APTO")
        return 1
    print("RESULTADO: APTO CON DEPENDENCIAS EXTERNAS DECLARADAS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
