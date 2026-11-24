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

# Operaciones que escriben textos derivados; tras ellas el índice legible se regenera.
CAMBIAN_CACHE = {"extraer", "evaluar-extraccion", "resolver-colisiones-cache", "aislar-paginas-ocr", "extraer-office"}


def _argumentos() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="modelador-procesos")
    grupos = parser.add_subparsers(dest="grupo", required=True)
    grupos.add_parser("arbol", help="Leer el arbol institucional")
    fuentes = grupos.add_parser("fuentes", help="Preparar la biblioteca documental para consulta y cotejo")
    tareas_fuentes = fuentes.add_subparsers(dest="operacion", required=True)
    tareas_fuentes.add_parser("inventariar")
    diagnosticar = tareas_fuentes.add_parser("diagnosticar-texto")
    diagnosticar.add_argument("--max-documentos", type=int)
    tareas_fuentes.add_parser("planificar-extraccion")
    prioridad = tareas_fuentes.add_parser("priorizar")
    prioridad.add_argument("--proceso", required=True)
    extraer = tareas_fuentes.add_parser("extraer")
    extraer.add_argument("--metodo", choices=["nativo", "ocr"], required=True)
    extraer.add_argument("--max-documentos", type=int)
    extraer.add_argument("--permitir-id-sin-url", action="append", default=[])
    tareas_fuentes.add_parser("evaluar-extraccion")
    office = tareas_fuentes.add_parser("extraer-office", help="DOCX/PPTX a Markdown anclado y ficha de XLSX")
    office.add_argument("--max-documentos", type=int)
    tareas_fuentes.add_parser("indice", help="Regenerar el índice legible de la caché")
    segmentar = tareas_fuentes.add_parser("segmentar", help="Dividir textos derivados en fragmentos ubicados")
    segmentar.add_argument("--max-documentos", type=int)
    tareas_fuentes.add_parser("indexar", help="Reconstruir el índice léxico local de fragmentos")
    buscar = tareas_fuentes.add_parser("buscar", help="Buscar pasajes candidatos con ubicación verificable")
    buscar.add_argument("consulta", nargs="?", default="")
    buscar.add_argument("--modo", choices=["todas", "alguna", "frase"], default="todas")
    buscar.add_argument("--tema", help="Restringir a los términos de un tema del vocabulario")
    buscar.add_argument("--con-relacionados", action="store_true", help="Incluir temas relacionados (no equivalentes)")
    buscar.add_argument("--id", dest="id_documento", help="ID de catálogo")
    buscar.add_argument("--archivo", help="Parte de la ruta del original")
    buscar.add_argument("--tipo", choices=["pdf", "docx", "pptx"])
    buscar.add_argument("--area", help="Carpeta de primer nivel de 01-referencias")
    buscar.add_argument("--articulo")
    buscar.add_argument("--limite", type=int, default=8)
    buscar.add_argument("--max-caracteres", type=int, default=6000)
    contexto = tareas_fuentes.add_parser("contexto", help="Texto completo de un fragmento y sus vecinos")
    contexto.add_argument("fragmento")
    contexto.add_argument("--vecinos", type=int, default=1)
    contexto.add_argument("--max-caracteres", type=int, default=8000)
    temas = tareas_fuentes.add_parser("temas", help="Vocabulario de temas de búsqueda")
    tareas_temas = temas.add_subparsers(dest="accion_temas", required=True)
    tareas_temas.add_parser("comprobar")
    sugerir = tareas_temas.add_parser("sugerir")
    sugerir.add_argument("--proceso", help="Prefijo de código de proceso, p. ej. S4.3")
    tareas_fuentes.add_parser("resolver-colisiones-cache")
    tareas_fuentes.add_parser("aislar-paginas-ocr")
    cotejo = tareas_fuentes.add_parser("preparar-cotejo")
    cotejo.add_argument("--id", required=True)
    cotejo.add_argument("--pagina", required=True, type=int)
    cotejo.add_argument("--archivo", help="Ruta relativa registrada para distinguir IDs repetidos")
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


def _consulta(raiz: Path, args: argparse.Namespace) -> object:
    from . import fuentes_busqueda as busqueda
    from . import fuentes_temas as temas
    from .fuentes_fragmentos import segmentar

    if args.operacion == "segmentar":
        return segmentar(raiz, args.max_documentos)
    if args.operacion == "indexar":
        return busqueda.indexar(raiz)
    if args.operacion == "contexto":
        return busqueda.contexto(raiz, args.fragmento, args.vecinos, args.max_caracteres)
    if args.operacion == "temas":
        return temas.comprobar(raiz) if args.accion_temas == "comprobar" else temas.sugerir(raiz, args.proceso)
    terminos, usados = temas.terminos_de(raiz, args.tema, args.con_relacionados) if args.tema else ([], [])
    filtros = {k: getattr(args, k) for k in ("id_documento", "archivo", "tipo", "area", "articulo")}
    resultado = busqueda.buscar(
        raiz, args.consulta, modo=args.modo, terminos=terminos, filtros=filtros,
        limite=args.limite, max_caracteres=args.max_caracteres,
    )  # fmt: skip
    return {**resultado, "temas_usados": usados}


def ejecutar(args: argparse.Namespace) -> object:
    if args.grupo == "contrato":
        from .contrato import sincronizar_contrato

        vigente = sincronizar_contrato(comprobar=args.check)
        if not vigente:
            print("El contrato OpenAPI está desfasado; ejecute 'modelador-procesos contrato'.", file=sys.stderr)
        return 0 if vigente else 1
    repositorio = RepositorioProcesos.desde_entorno()
    if args.grupo == "fuentes":
        from . import fuentes_extraccion as extraccion
        from . import fuentes_preparacion as preparacion
        from .fuentes_indice import generar_indice
        from .fuentes_office import extraer_office

        operaciones = {
            "inventariar": lambda: preparacion.inventariar(repositorio.raiz),
            "diagnosticar-texto": lambda: preparacion.diagnosticar_texto(repositorio.raiz, args.max_documentos),
            "planificar-extraccion": lambda: preparacion.planificar_extraccion(repositorio.raiz),
            "priorizar": lambda: preparacion.priorizar(repositorio.raiz, args.proceso),
            "extraer": lambda: (
                extraccion.extraer_nativo(repositorio.raiz, args.max_documentos)
                if args.metodo == "nativo"
                else extraccion.extraer_ocr(repositorio.raiz, args.max_documentos, args.permitir_id_sin_url)
            ),
            "evaluar-extraccion": lambda: extraccion.evaluar_extraccion(repositorio.raiz),
            "resolver-colisiones-cache": lambda: extraccion.resolver_colisiones_cache(repositorio.raiz),
            "aislar-paginas-ocr": lambda: extraccion.aislar_paginas_ocr(repositorio.raiz),
            "preparar-cotejo": lambda: extraccion.preparar_cotejo(repositorio.raiz, args.id, args.pagina, args.archivo),
            "extraer-office": lambda: extraer_office(repositorio.raiz, args.max_documentos),
            "indice": lambda: generar_indice(repositorio.raiz),
        }
        if args.operacion in ("segmentar", "indexar", "buscar", "contexto", "temas"):
            return _consulta(repositorio.raiz, args)
        resultado = operaciones[args.operacion]()
        if args.operacion in CAMBIAN_CACHE:
            resultado["indice"] = generar_indice(repositorio.raiz)["indice"]
        return resultado
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
