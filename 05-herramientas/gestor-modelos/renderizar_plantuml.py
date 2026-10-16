"""Renderiza fuentes PlantUML con una version local fijada y verificada."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[2]
LOCK_PATH = Path(__file__).with_name("plantuml.lock.json")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_lock() -> dict[str, object]:
    data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    required = {"version", "artifacts"}
    missing = required.difference(data)
    if missing:
        raise RuntimeError(f"Faltan campos en {LOCK_PATH}: {sorted(missing)}")
    return data


def download_verified(url: str, destination: Path, expected: str) -> Path:
    if destination.exists() and sha256(destination) == expected.lower():
        return destination
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=destination.parent, delete=False) as temporary:
        temporary_path = Path(temporary.name)
    try:
        print(f"Descargando {url}...", file=sys.stderr)
        urllib.request.urlretrieve(url, temporary_path)
        obtained = sha256(temporary_path)
        if obtained != expected.lower():
            raise RuntimeError(
                "La descarga no coincide con el SHA-256 fijado: "
                f"esperado={expected}, obtenido={obtained}"
            )
        os.replace(temporary_path, destination)
    finally:
        temporary_path.unlink(missing_ok=True)
    return destination


def ensure_native_windows(lock: dict[str, object]) -> Path:
    artifact = lock["artifacts"]["windows_x64_native"]
    archive = REPO_ROOT / artifact["archive_cache_path"]
    executable = REPO_ROOT / artifact["executable_cache_path"]
    expected_executable = artifact["executable_sha256"].lower()
    if executable.exists() and sha256(executable) == expected_executable:
        return executable

    download_verified(artifact["url"], archive, artifact["sha256"])
    destination = executable.parent
    destination.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            if Path(member.filename).name != member.filename:
                raise RuntimeError(f"Ruta no permitida en el ZIP: {member.filename}")
        bundle.extractall(destination)
    if not executable.exists() or sha256(executable) != expected_executable:
        raise RuntimeError("El ejecutable nativo extraido no coincide con el hash fijado.")
    return executable


def java_major(java: str) -> int:
    result = subprocess.run(
        [java, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    text = (result.stderr or result.stdout).decode("utf-8", errors="replace")
    quoted = text.split('"', 2)
    if len(quoted) < 2:
        return 0
    first = quoted[1].split(".")[0]
    if first == "1":
        return int(quoted[1].split(".")[1])
    return int(first)


def plantuml_command(lock: dict[str, object]) -> list[str]:
    machine = platform.machine().lower()
    if platform.system() == "Windows" and machine in {"amd64", "x86_64"}:
        return [str(ensure_native_windows(lock))]

    artifact = lock["artifacts"]["java_jar"]
    jar = download_verified(
        artifact["url"], REPO_ROOT / artifact["cache_path"], artifact["sha256"]
    )
    java = shutil.which("java")
    if not java:
        raise RuntimeError("No se encontro Java para ejecutar PlantUML en esta plataforma.")
    minimum = int(artifact["minimum_java"])
    detected = java_major(java)
    if detected < minimum:
        raise RuntimeError(f"PlantUML requiere Java {minimum}+; se detecto Java {detected}.")
    return [java, "-Djava.awt.headless=true", "-jar", str(jar)]


def render(source: Path, output_format: str) -> bytes:
    lock = load_lock()
    command = plantuml_command(lock) + [
        "-charset",
        "UTF-8",
        "-nometadata",
        "-failfast2",
        f"-t{output_format}",
        "-pipe",
    ]
    result = subprocess.run(
        command,
        input=source.read_bytes(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"PlantUML no pudo renderizar {source}: {message}")
    if not result.stdout:
        raise RuntimeError(f"PlantUML no produjo una salida para {source}.")

    if output_format == "svg":
        rendered = result.stdout.replace(b"\r\n", b"\n")
        if b"<svg" not in rendered:
            raise RuntimeError("La salida no contiene un SVG valido.")
        marker = b"<!-- GENERADO - NO EDITAR. Fuente: PlantUML fijado por el proyecto. -->\n"
        if not rendered.startswith(marker):
            rendered = marker + rendered
        return rendered
    return result.stdout


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Renderiza PlantUML localmente con version y hash fijados."
    )
    parser.add_argument("source", type=Path, help="Archivo .puml de entrada")
    parser.add_argument("--output", type=Path, required=True, help="Archivo de salida")
    parser.add_argument("--format", choices=("svg", "png"), default="svg")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Comprueba que la salida vigente coincide sin sobrescribirla.",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    output = args.output.resolve()
    if not source.is_file():
        parser.error(f"No existe la fuente: {source}")
    if source.suffix.lower() != ".puml":
        parser.error("La fuente debe tener extension .puml")

    try:
        rendered = render(source, args.format)
        if args.check:
            if not output.exists():
                print(f"DESACTUALIZADO: falta {output}", file=sys.stderr)
                return 1
            if output.read_bytes() != rendered:
                print(f"DESACTUALIZADO: {output}", file=sys.stderr)
                return 1
            print(f"OK: {output}")
            return 0

        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as temporary:
            temporary.write(rendered)
            temporary_path = Path(temporary.name)
        os.replace(temporary_path, output)
        print(f"GENERADO: {output}")
        return 0
    except (OSError, RuntimeError, urllib.error.URLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
