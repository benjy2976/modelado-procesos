"""Comprueba el traslado de cambios locales sobre un clon del mismo commit."""

from __future__ import annotations

import json
import subprocess
import sys
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "trasladar_proyecto.py"


def run(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, check=True)


def test_exporta_y_restaura_cache_y_cambios_sin_credenciales(tmp_path: Path) -> None:
    source = tmp_path / "origen"
    source.mkdir()
    run("git", "init", "-q", str(source))
    run("git", "config", "user.name", "Prueba", cwd=source)
    run("git", "config", "user.email", "prueba@example.invalid", cwd=source)
    (source / ".gitignore").write_text("cache/\n.mesa-local/\n", encoding="utf-8")
    (source / "modelo.md").write_text("original", encoding="utf-8")
    (source / "eliminar.md").write_text("fuera", encoding="utf-8")
    run("git", "add", ".", cwd=source)
    run("git", "commit", "-qm", "base", cwd=source)
    target = tmp_path / "destino"
    run("git", "clone", "-q", str(source), str(target))

    (source / "modelo.md").write_text("revisado", encoding="utf-8")
    (source / "eliminar.md").unlink()
    run("git", "add", "-u", cwd=source)
    (source / "nuevo.md").write_text("avance", encoding="utf-8")
    (source / "cache").mkdir()
    (source / "cache" / "ocr.md").write_text("resultado OCR", encoding="utf-8")
    (source / ".mesa-local").mkdir()
    (source / ".mesa-local" / "token.txt").write_text("secreto", encoding="utf-8")
    archive = tmp_path / "traslado.zip"

    exported = json.loads(run(sys.executable, str(SCRIPT), "exportar", str(archive), "--repo", str(source)).stdout)
    assert exported["archivos"] == 3
    with zipfile.ZipFile(archive) as zf:
        assert "files/cache/ocr.md" in zf.namelist()
        assert all("token" not in name for name in zf.namelist())
    run(sys.executable, str(SCRIPT), "restaurar", str(archive), "--repo", str(target))
    assert (target / "modelo.md").read_text(encoding="utf-8") == "revisado"
    assert (target / "nuevo.md").read_text(encoding="utf-8") == "avance"
    assert (target / "cache" / "ocr.md").read_text(encoding="utf-8") == "resultado OCR"
    assert not (target / "eliminar.md").exists()
    assert not (target / ".mesa-local").exists()


def test_rechaza_clon_con_cambios_antes_de_restaurar(tmp_path: Path) -> None:
    source = tmp_path / "origen"
    source.mkdir()
    run("git", "init", "-q", str(source))
    run("git", "config", "user.name", "Prueba", cwd=source)
    run("git", "config", "user.email", "prueba@example.invalid", cwd=source)
    (source / "modelo.md").write_text("original", encoding="utf-8")
    run("git", "add", ".", cwd=source)
    run("git", "commit", "-qm", "base", cwd=source)
    target = tmp_path / "destino"
    run("git", "clone", "-q", str(source), str(target))
    (source / "modelo.md").write_text("revisado", encoding="utf-8")
    archive = tmp_path / "traslado.zip"
    run(sys.executable, str(SCRIPT), "exportar", str(archive), "--repo", str(source))
    (target / "modelo.md").write_text("cambio local", encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "restaurar", str(archive), "--repo", str(target)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "limpio" in result.stderr
    assert (target / "modelo.md").read_text(encoding="utf-8") == "cambio local"
