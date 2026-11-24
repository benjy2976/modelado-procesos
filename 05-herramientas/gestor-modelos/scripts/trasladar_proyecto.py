"""Empaqueta y restaura el trabajo local encima de un clon del mismo commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

EXCLUDED_DIRS = {
    ".git",
    ".mesa-local",
    ".venv",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".nuxt",
    ".output",
}
EXCLUDED_FILES = {".env", "id_rsa", "id_ed25519"}
EXCLUDED_SUFFIXES = {".pem", ".key", ".pfx", ".p12", ".pyc"}


def git(root: Path, *args: str) -> bytes:
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=True)
    return result.stdout


def git_paths(root: Path, *args: str) -> set[str]:
    return {part.decode("utf-8").replace("\\", "/") for part in git(root, *args).split(b"\0") if part}


def sha256_stream(stream: object) -> str:
    digest = hashlib.sha256()
    while chunk := stream.read(1024 * 1024):
        digest.update(chunk)
    return digest.hexdigest()


def safe_path(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    if (
        path.is_absolute()
        or not path.parts
        or "\\" in relative
        or ":" in relative
        or any(part in {".", ".."} for part in path.parts)
    ):
        raise ValueError(f"Ruta insegura en el paquete: {relative}")
    resolved = root.joinpath(*path.parts).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"Ruta fuera del repositorio: {relative}")
    return resolved


def excluded(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    name = parts[-1].lower()
    return (
        any(part.lower() in EXCLUDED_DIRS for part in parts[:-1])
        or name in EXCLUDED_FILES
        or (name.startswith(".env.") and name != ".env.example")
        or any(name.endswith(suffix) for suffix in EXCLUDED_SUFFIXES)
    )


def local_files(root: Path) -> set[str]:
    found: set[str] = set()
    for directory, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name.lower() not in EXCLUDED_DIRS]
        for name in files:
            path = Path(directory, name)
            relative = path.relative_to(root).as_posix()
            if not excluded(relative):
                if path.is_symlink():
                    raise ValueError(f"Enlace simbólico no admitido: {relative}")
                found.add(relative)
    return found


def exportar(root: Path, archive: Path) -> dict:
    root = root.resolve()
    archive = archive.resolve()
    if archive.is_relative_to(root):
        raise ValueError("Guarde el paquete fuera del repositorio")
    if archive.exists():
        raise FileExistsError(f"El paquete ya existe: {archive}")
    head = git(root, "rev-parse", "HEAD").decode().strip()
    tracked = git_paths(root, "ls-tree", "-r", "--name-only", "-z", "HEAD")
    changed = git_paths(root, "diff", "HEAD", "--no-renames", "--name-only", "-z", "--diff-filter=ACDMRTUXB")
    present = local_files(root)
    selected = sorted(((present - tracked) | changed) & present)
    deleted = sorted(path for path in ((changed - present) & tracked) if not excluded(path))
    manifest = {
        "formato": 1,
        "creado_utc": datetime.now(timezone.utc).isoformat(),
        "git_head": head,
        "archivos": [],
        "eliminados": deleted,
        "exclusiones": sorted(EXCLUDED_DIRS | EXCLUDED_FILES | EXCLUDED_SUFFIXES),
    }
    archive.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as zf:
            for relative in selected:
                source = safe_path(root, relative)
                with source.open("rb") as stream:
                    digest = sha256_stream(stream)
                size = source.stat().st_size
                zf.write(source, "files/" + relative)
                manifest["archivos"].append({"ruta": relative, "sha256": digest, "bytes": size})
            zf.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        verificar(archive)
    except BaseException:
        archive.unlink(missing_ok=True)
        raise
    return manifest


def verificar(archive: Path) -> dict:
    with zipfile.ZipFile(archive) as zf:
        manifest = json.loads(zf.read("manifest.json"))
        if manifest.get("formato") != 1:
            raise ValueError("Formato de paquete no compatible")
        expected = {"manifest.json"}
        seen: set[str] = set()
        for item in manifest["archivos"]:
            relative = item["ruta"]
            safe_path(Path.cwd(), relative)
            if excluded(relative):
                raise ValueError(f"Ruta excluida en el paquete: {relative}")
            if relative in seen:
                raise ValueError(f"Ruta duplicada: {relative}")
            seen.add(relative)
            entry = "files/" + relative
            expected.add(entry)
            with zf.open(entry) as stream:
                if sha256_stream(stream) != item["sha256"]:
                    raise ValueError(f"Hash incorrecto: {relative}")
            if zf.getinfo(entry).file_size != item["bytes"]:
                raise ValueError(f"Tamaño incorrecto: {relative}")
        for relative in manifest["eliminados"]:
            safe_path(Path.cwd(), relative)
            if excluded(relative):
                raise ValueError(f"Eliminación excluida en el paquete: {relative}")
        if len(zf.namelist()) != len(expected) or set(zf.namelist()) != expected:
            raise ValueError("El ZIP contiene entradas inesperadas o faltantes")
    return manifest


def restaurar(root: Path, archive: Path) -> dict:
    root = root.resolve()
    manifest = verificar(archive)
    head = git(root, "rev-parse", "HEAD").decode().strip()
    if head != manifest["git_head"]:
        raise ValueError("El clon debe estar en el mismo commit registrado en el paquete")
    if git(root, "status", "--porcelain", "--untracked-files=all").strip():
        raise ValueError("El clon de destino debe estar limpio antes de restaurar")
    tracked = git_paths(root, "ls-files", "-z")
    for item in manifest["archivos"]:
        target = safe_path(root, item["ruta"])
        if target.exists() and item["ruta"] not in tracked:
            raise ValueError(f"Archivo local ya presente en destino: {item['ruta']}")
    with zipfile.ZipFile(archive) as zf:
        for item in manifest["archivos"]:
            target = safe_path(root, item["ruta"])
            target.parent.mkdir(parents=True, exist_ok=True)
            fd, temporary = tempfile.mkstemp(prefix=".traslado-", dir=target.parent)
            try:
                with os.fdopen(fd, "wb") as output, zf.open("files/" + item["ruta"]) as source:
                    shutil.copyfileobj(source, output)
                os.replace(temporary, target)
            finally:
                Path(temporary).unlink(missing_ok=True)
        for relative in manifest["eliminados"]:
            safe_path(root, relative).unlink(missing_ok=True)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("accion", choices=("exportar", "verificar", "restaurar"))
    parser.add_argument("archivo", type=Path, help="ZIP de traslado, fuera del repositorio")
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[3])
    args = parser.parse_args()
    try:
        if args.accion == "exportar":
            result = exportar(args.repo, args.archivo)
        elif args.accion == "verificar":
            result = verificar(args.archivo)
        else:
            result = restaurar(args.repo, args.archivo)
    except (OSError, ValueError, KeyError, zipfile.BadZipFile, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(
        json.dumps(
            {
                "accion": args.accion,
                "git_head": result["git_head"],
                "archivos": len(result["archivos"]),
                "eliminados": len(result["eliminados"]),
                "zip": str(args.archivo.resolve()),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
