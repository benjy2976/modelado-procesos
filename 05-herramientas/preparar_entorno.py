#!/usr/bin/env python3
"""Instala el perfil ampliado en .venv, sin activar scripts ni tocar Python global."""

import subprocess
import sys
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_PYTHON = (3, 11)


def main() -> int:
    if (
        sys.implementation.name != "cpython"
        or sys.version_info[:2] < MIN_PYTHON
        or sys.version_info.releaselevel != "final"
    ):
        print(
            "Usar una version estable de Python 3.11 o posterior: "
            "<python-compatible> 05-herramientas/preparar_entorno.py"
        )
        return 1
    target = ROOT / ".venv"
    executable = target / (
        "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
    )
    if not target.exists():
        venv.EnvBuilder(with_pip=True).create(target)
    if not executable.is_file():
        print(".venv existe pero no contiene Python; revisarlo manualmente.")
        return 1
    try:
        subprocess.run(
            [
                str(executable),
                "-c",
                (
                    "import sys; assert sys.implementation.name == 'cpython'; "
                    "assert sys.version_info[:2] >= (3, 11); "
                    "assert sys.version_info.releaselevel == 'final'"
                ),
            ],
            check=True,
        )
        subprocess.run(
            [
                str(executable),
                "-m",
                "pip",
                "install",
                "--require-hashes",
                "-r",
                str(ROOT / "requirements-herramientas.txt"),
            ],
            cwd=ROOT,
            check=True,
        )
        return subprocess.run(
            [str(executable), str(ROOT / "05-herramientas/verificar_entorno.py")],
            cwd=ROOT,
            check=False,
        ).returncode
    except subprocess.CalledProcessError as exc:
        print(
            f"Preparacion interrumpida (codigo {exc.returncode}); revisar salida anterior."
        )
        return exc.returncode


if __name__ == "__main__":
    sys.exit(main())
