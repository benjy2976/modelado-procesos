"""Entrada unica para los casos de uso disponibles de la mesa de modelamiento."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from .documentos import ServicioDocumentos
from .observaciones import ServicioObservaciones
from .repositorio import ErrorDominio, RepositorioProcesos
from .sesiones import ServicioSesiones


def _argumentos() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="modelador-procesos")
    grupos = parser.add_subparsers(dest="grupo", required=True)
    grupos.add_parser("arbol", help="Leer el arbol institucional")
    proceso = grupos.add_parser("proceso", help="Leer un modelo por codigo")
    proceso.add_argument("codigo")
    fuente = grupos.add_parser("fuente", help="Leer una fuente registrada y su página")
    fuente.add_argument("codigo")
    fuente.add_argument("referencia")
    fuente.add_argument("indice", type=int)
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
    responder = operaciones.add_parser("responder")
    responder.add_argument("codigo")
    responder.add_argument("identificador")
    responder.add_argument("--texto", required=True)
    responder.add_argument("--autor", required=True)
    responder.add_argument("--revision", required=True)
    estado = operaciones.add_parser("estado")
    estado.add_argument("codigo")
    estado.add_argument("identificador")
    estado.add_argument("--valor", choices=["ABIERTA", "RESUELTA"], required=True)
    estado.add_argument("--revision", required=True)
    estado.add_argument("--autor", default="")
    modelo = grupos.add_parser("modelo", help="Ejecutar el generador vigente sin cambiar su contrato")
    modelo.add_argument("codigo")
    modelo.add_argument("--check", action="store_true")
    modelo.add_argument("--exportar-imagenes", action="store_true")
    api = grupos.add_parser("api", help="Servir la API local")
    api.add_argument("--host", default="127.0.0.1")
    api.add_argument("--port", type=int, default=8000)
    mcp = grupos.add_parser("mcp", help="Servir herramientas MCP")
    mcp.add_argument("--transporte", choices=["stdio"], default="stdio")
    contrato = grupos.add_parser("contrato", help="Exportar o comprobar el OpenAPI generado")
    contrato.add_argument("--check", action="store_true", help="Comprobar que el archivo versionado esté vigente")
    sesiones = grupos.add_parser("sesiones", help="Editar un modelo en copia recuperable")
    acciones = sesiones.add_subparsers(dest="operacion", required=True)
    for operacion in ("iniciar", "leer", "documento", "editar", "preparar", "integrar", "cerrar"):
        accion = acciones.add_parser(operacion)
        accion.add_argument("codigo")
        if operacion != "iniciar":
            accion.add_argument("sesion")
        if operacion in ("documento", "editar"):
            accion.add_argument("nombre", choices=["tabla", "sustento", "fuentes_visor"])
        if operacion == "editar":
            accion.add_argument("--archivo", type=Path, required=True, help="Archivo UTF-8 con el nuevo contenido")
            accion.add_argument("--revision", required=True)
        if operacion == "integrar":
            accion.add_argument("--revision", type=int, required=True)
    return parser


def ejecutar(args: argparse.Namespace) -> object:
    if args.grupo == "contrato":
        from .contrato import sincronizar_contrato

        vigente = sincronizar_contrato(comprobar=args.check)
        if not vigente:
            print("El contrato OpenAPI está desfasado; ejecute 'modelador-procesos contrato'.", file=sys.stderr)
        return 0 if vigente else 1
    repositorio = RepositorioProcesos.desde_entorno()
    observaciones = ServicioObservaciones(repositorio)
    documentos = ServicioDocumentos(repositorio)
    sesiones = ServicioSesiones(repositorio)
    if args.grupo == "sesiones":
        if args.operacion == "iniciar":
            return sesiones.iniciar(args.codigo)
        if args.operacion == "leer":
            return sesiones.leer(args.codigo, args.sesion)
        if args.operacion == "documento":
            return sesiones.contenido(args.codigo, args.sesion, args.nombre)
        if args.operacion == "editar":
            return sesiones.editar(
                args.codigo, args.sesion, args.nombre, args.archivo.read_text(encoding="utf-8"), args.revision
            )
        if args.operacion == "preparar":
            return sesiones.preparar(args.codigo, args.sesion)
        if args.operacion == "integrar":
            return sesiones.integrar(args.codigo, args.sesion, args.revision)
        return sesiones.cerrar(args.codigo, args.sesion)
    if args.grupo == "arbol":
        return repositorio.arbol()
    if args.grupo == "proceso":
        return repositorio.leer_modelo(args.codigo)
    if args.grupo == "fuente":
        return documentos.leer_fuente(args.codigo, args.referencia, args.indice)
    if args.grupo == "observaciones":
        if args.operacion == "listar":
            return observaciones.listar(args.codigo)
        if args.operacion == "responder":
            return observaciones.responder(args.codigo, args.identificador, args.texto, args.autor, args.revision)
        if args.operacion == "estado":
            return observaciones.actualizar_estado(
                args.codigo, args.identificador, args.valor, args.revision, args.autor
            )
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
