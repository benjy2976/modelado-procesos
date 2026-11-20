"""Entrada unica para los casos de uso disponibles de la mesa de modelamiento."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .observaciones import ServicioObservaciones
from .repositorio import ErrorDominio, RepositorioProcesos


def _argumentos() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="modelador-procesos")
    grupos = parser.add_subparsers(dest="grupo", required=True)
    grupos.add_parser("arbol", help="Leer el arbol institucional")
    proceso = grupos.add_parser("proceso", help="Leer un modelo por codigo")
    proceso.add_argument("codigo")
    observaciones = grupos.add_parser("observaciones", help="Consultar o registrar observaciones")
    operaciones = observaciones.add_subparsers(dest="operacion", required=True)
    listar = operaciones.add_parser("listar")
    listar.add_argument("codigo")
    agregar = operaciones.add_parser("agregar")
    agregar.add_argument("codigo")
    agregar.add_argument("--texto", required=True)
    agregar.add_argument("--autor", required=True)
    agregar.add_argument("--revision", required=True)
    agregar.add_argument("--elemento", default="")
    agregar.add_argument("--tipo", choices=["OBSERVACION", "COMENTARIO"], default="OBSERVACION")
    modelo = grupos.add_parser("modelo", help="Ejecutar el generador vigente sin cambiar su contrato")
    modelo.add_argument("codigo")
    modelo.add_argument("--check", action="store_true")
    modelo.add_argument("--exportar-imagenes", action="store_true")
    api = grupos.add_parser("api", help="Servir la API local")
    api.add_argument("--host", default="127.0.0.1")
    api.add_argument("--port", type=int, default=8000)
    mcp = grupos.add_parser("mcp", help="Servir herramientas MCP")
    mcp.add_argument("--transporte", choices=["stdio"], default="stdio")
    return parser


def ejecutar(args: argparse.Namespace) -> object:
    repositorio = RepositorioProcesos.desde_entorno()
    observaciones = ServicioObservaciones(repositorio)
    if args.grupo == "arbol":
        return repositorio.arbol()
    if args.grupo == "proceso":
        return repositorio.leer_modelo(args.codigo)
    if args.grupo == "observaciones":
        if args.operacion == "listar":
            return observaciones.listar(args.codigo)
        return observaciones.agregar(
            args.codigo,
            elemento=args.elemento,
            texto=args.texto,
            autor=args.autor,
            revision_esperada=args.revision,
            tipo=args.tipo,
        )
    if args.grupo == "modelo":
        repositorio.carpeta(args.codigo)
        programa = Path(__file__).resolve().parents[1] / "modelar.py"
        comando = [sys.executable, str(programa), args.codigo]
        if args.check:
            comando.append("--check")
        if args.exportar_imagenes:
            comando.append("--exportar-imagenes")
        return subprocess.run(comando, check=False).returncode
    if args.grupo == "api":
        import uvicorn

        uvicorn.run("mesa_modelamiento.api:app", host=args.host, port=args.port)
        return None
    from .mcp_adapter import main as servir_mcp

    servir_mcp()
    return None


def main() -> None:
    args = _argumentos().parse_args()
    try:
        resultado = ejecutar(args)
    except ErrorDominio as exc:
        print(json.dumps({"error": {"code": exc.codigo_http, "message": str(exc)}}), file=sys.stderr)
        raise SystemExit(1) from exc
    if isinstance(resultado, int):
        raise SystemExit(resultado)
    if resultado is not None:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
