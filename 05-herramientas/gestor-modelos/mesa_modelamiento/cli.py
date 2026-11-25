"""Entrada unica para los casos de uso disponibles de la mesa de modelamiento."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .documentos import ServicioDocumentos
from .repositorio import ErrorDominio, RepositorioProcesos
from .resolucion import ServicioResolucion
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
    tareas_fuentes.add_parser("regimen", help="Comprobar las reglas de régimen y resumir la clasificación")
    buscar = tareas_fuentes.add_parser("buscar", help="Buscar pasajes candidatos con ubicación verificable")
    buscar.add_argument("consulta", nargs="?", default="")
    buscar.add_argument("--modo", choices=["todas", "alguna", "frase", "flexible"], default="flexible")
    buscar.add_argument("--tema", help="Restringir a los términos de un tema del vocabulario")
    buscar.add_argument("--con-relacionados", action="store_true", help="Incluir temas relacionados (no equivalentes)")
    buscar.add_argument("--id", dest="id_documento", help="ID de catálogo")
    buscar.add_argument("--archivo", help="Parte de la ruta del original")
    buscar.add_argument("--tipo", choices=["pdf", "docx", "pptx"])
    buscar.add_argument("--area", help="Carpeta de primer nivel de 01-referencias")
    buscar.add_argument("--articulo")
    buscar.add_argument(
        "--regimen", help="CONTRATA-LEY-32069, OBRAS-POR-IMPUESTOS, ADMINISTRACION-DIRECTA, TRANSVERSAL..."
    )
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
    anclar = tareas_fuentes.add_parser("anclar", help="Rectángulos de una cita en el PDF original")
    anclar.add_argument("--fragmento", help="ID de fragmento; se prueban sus páginas en orden")
    anclar.add_argument("--archivo", help="Ruta del PDF original registrada")
    anclar.add_argument("--pagina", type=int)
    anclar.add_argument("--cita", required=True)
    pruebas = tareas_fuentes.add_parser("pruebas", help="Banco de preguntas de recuperación")
    tareas_pruebas = pruebas.add_subparsers(dest="accion_pruebas", required=True)
    tareas_pruebas.add_parser("preparar").add_argument("banco")
    medir = tareas_pruebas.add_parser("medir")
    medir.add_argument("banco")
    medir.add_argument("--sin-temas", action="store_true", help="Medir solo la búsqueda léxica")
    medir.add_argument("--modo", choices=["todas", "alguna", "frase", "flexible"], help="Sustituye el modo del banco")
    tareas_fuentes.add_parser("resolver-colisiones-cache")
    tareas_fuentes.add_parser("aislar-paginas-ocr")
    cotejo = tareas_fuentes.add_parser("preparar-cotejo")
    cotejo.add_argument("--id", required=True)
    cotejo.add_argument("--pagina", required=True, type=int)
    cotejo.add_argument("--archivo", help="Ruta relativa registrada para distinguir IDs repetidos")
    conocimiento = grupos.add_parser("conocimiento", help="Consultar conocimiento estructurado (solo lectura)")
    consultas = conocimiento.add_subparsers(dest="operacion", required=True)
    notas = consultas.add_parser("notas", help="Buscar notas por propiedades y texto")
    for opcion in ("area", "tipo", "estado", "clase", "etiqueta", "proceso", "texto"):
        notas.add_argument(f"--{opcion}")
    notas.add_argument("--limite", type=int, default=30)
    notas.add_argument("--desplazamiento", type=int, default=0)
    nota = consultas.add_parser("nota", help="Leer una nota autorizada")
    nota.add_argument("ruta")
    nota.add_argument("--desde", type=int, default=0)
    nota.add_argument("--max-caracteres", type=int, default=20000)
    documentos_c = consultas.add_parser("documentos", help="Inventario de la biblioteca")
    for opcion in ("texto", "area", "formato", "regimen"):
        documentos_c.add_argument(f"--{opcion}")
    documentos_c.add_argument("--con-texto", choices=["si", "no"])
    documentos_c.add_argument("--limite", type=int, default=30)
    documentos_c.add_argument("--desplazamiento", type=int, default=0)
    consultas.add_parser("documento", help="Ficha de un documento por ID o ruta").add_argument("identificador")
    texto_doc = consultas.add_parser("texto-documento", help="Páginas del texto derivado de un documento")
    texto_doc.add_argument("identificador")
    texto_doc.add_argument("--pagina", type=int, default=1)
    texto_doc.add_argument("--paginas", type=int, default=3)
    texto_doc.add_argument("--max-caracteres", type=int, default=12000)
    indice = consultas.add_parser("indice", help="Índice de artículos de un documento")
    indice.add_argument("identificador")
    indice.add_argument("--archivo")
    indice.add_argument("--desde", type=int)
    indice.add_argument("--hasta", type=int)
    articulos = consultas.add_parser("articulos", help="Texto de un rango de artículos (hasta 40)")
    articulos.add_argument("identificador")
    articulos.add_argument("desde", type=int)
    articulos.add_argument("hasta", type=int)
    articulos.add_argument("--archivo")
    articulos.add_argument("--max-caracteres", type=int, default=30000)
    consultas.add_parser("temas", help="Vocabulario de temas de búsqueda")
    reglas = consultas.add_parser("reglas", help="Reglas normativas filtradas")
    for opcion in ("proceso", "dominio", "estado", "modalidad", "texto"):
        reglas.add_argument(f"--{opcion}")
    consultas.add_parser("regla", help="Regla con sus eventos de revisión").add_argument("identificador")
    consultas.add_parser("glosario", help="Términos del glosario").add_argument("texto", nargs="?")
    decisiones = consultas.add_parser("decisiones", help="Decisiones del registro")
    decisiones.add_argument("--texto")
    decisiones.add_argument("--id", dest="identificador")
    decisiones.add_argument("--limite", type=int, default=20)
    consultas.add_parser("etiquetas", help="Revisar o listar etiquetas").add_argument(
        "accion", choices=["revisar", "listar"], nargs="?", default="revisar"
    )
    paquete = consultas.add_parser("paquete", help="Paquete de contexto de una tarea sobre un proceso")
    paquete.add_argument("codigo")
    paquete.add_argument("--tarea", default="")
    auditoria = grupos.add_parser("auditoria", help="Auditar afirmaciones de un modelo contra fuentes")
    tareas_auditoria = auditoria.add_subparsers(dest="operacion", required=True)
    tareas_auditoria.add_parser("inventariar-elementos").add_argument("codigo")
    lote = tareas_auditoria.add_parser("registrar")
    lote.add_argument("codigo")
    lote.add_argument("--archivo", type=Path, required=True, help="JSON con una lista de afirmaciones")
    cobertura = tareas_auditoria.add_parser("cobertura", help="Obligaciones de la fuente y elemento que las representa")
    cobertura.add_argument("codigo")
    cobertura.add_argument("--archivo", type=Path, required=True, help="JSON con la lista de obligaciones")
    corrida = tareas_auditoria.add_parser("correr", help="Estado reanudable de la auditoría de un alcance")
    corrida.add_argument("--alcance", required=True, help="Código raíz, p. ej. S4.3")
    corrida.add_argument("--max-procesos", type=int)
    tareas_auditoria.add_parser("comparar-interfaces", help="Candidatos de interfaz padre-hijos").add_argument("codigo")
    reconfirmacion = tareas_auditoria.add_parser(
        "reconfirmar", help="Reconfirmar la auditoría tras cambiar la tabla, conservando lo vigente"
    )
    reconfirmacion.add_argument("codigo")
    reconfirmacion.add_argument(
        "--archivo", type=Path, required=True, help="JSON con afirmaciones, cobertura (opcional) y motivo"
    )
    reporte = tareas_auditoria.add_parser("informe")
    reporte.add_argument("codigo")
    reporte.add_argument("--check", action="store_true", help="Terminar con código 1 si hay pendientes")
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
    agregar.add_argument("--referencia", default="", help="Se completa sola si --elemento es un ID de tabla o número")
    agregar.add_argument("--formato", choices=["texto", "html"], default="texto")
    responder = operaciones.add_parser("responder")
    responder.add_argument("codigo")
    responder.add_argument("identificador")
    responder.add_argument("--texto", required=True)
    responder.add_argument("--autor", required=True)
    responder.add_argument("--revision", required=True)
    responder.add_argument("--formato", choices=["texto", "html"], default="texto")
    estado = operaciones.add_parser("estado")
    estado.add_argument("codigo")
    estado.add_argument("identificador")
    estado.add_argument("--valor", choices=["ABIERTA", "RESUELTA"], required=True)
    estado.add_argument("--revision", required=True)
    estado.add_argument("--autor", default="")
    for operacion, ayuda in (
        ("analizar", "Etapa EN-ANALISIS (agente)"),
        ("proponer", "Etapa PROPUESTA con opciones (agente)"),
        ("definir", "Etapa DEFINIDA (persona)"),
        ("corregir", "Etapa EN-CORRECCION (agente)"),
        ("aplicar", "Cierre con evidencia o espera de evidencia (agente)"),
    ):
        etapa_cli = operaciones.add_parser(operacion, help=ayuda)
        etapa_cli.add_argument("codigo")
        etapa_cli.add_argument("identificador")
        etapa_cli.add_argument("--autor", required=True)
        etapa_cli.add_argument("--revision", required=True)
        if operacion != "corregir":
            etapa_cli.add_argument(
                "--archivo", type=Path, required=operacion != "definir",
                help="JSON con los campos de la etapa (texto, clase, fuentes, opciones, seleccion, etc.)",
            )  # fmt: skip
        if operacion == "definir":
            etapa_cli.add_argument("--tipo", choices=["OPCION", "OPCIONES", "MANUAL", "VINCULADA"], required=True)
            etapa_cli.add_argument("--opcion", action="append", default=[])
            etapa_cli.add_argument("--texto", default="")
            etapa_cli.add_argument("--vinculada-a", default="")
        if operacion == "corregir":
            etapa_cli.add_argument("--confirmar-vigencia", action="store_true")
    por_etapa = operaciones.add_parser("etapas", help="Observaciones por etapa en un proceso o en todo el árbol")
    por_etapa.add_argument("--etapa")
    por_etapa.add_argument("--codigo")
    por_etapa.add_argument("--resumen", action="store_true", help="Sin el análisis ni la propuesta completos")
    modelo = grupos.add_parser("modelo", help="Ejecutar el generador vigente sin cambiar su contrato")
    modelo.add_argument("codigo")
    modelo.add_argument("--check", action="store_true")
    modelo.add_argument("--exportar-imagenes", action="store_true")
    modelo.add_argument("--sin-cache", action="store_true")
    modelo.add_argument("--forzar", action="store_true", help="Adopta hallazgos D1-D5 ya documentados en el sustento")
    modelo.add_argument("--justificacion", default="", help="Obligatoria con --forzar")
    api = grupos.add_parser("api", help="Servir la API local")
    api.add_argument("--host", default="127.0.0.1")
    api.add_argument("--port", type=int, default=8000)
    trabajos = grupos.add_parser("trabajos", help="Cola de trabajos de los agentes (DEC-068)")
    tareas_trabajos = trabajos.add_subparsers(dest="operacion", required=True)
    listar_t = tareas_trabajos.add_parser("listar")
    for opcion in ("estado", "tipo", "codigo"):
        listar_t.add_argument(f"--{opcion}")
    encolar_t = tareas_trabajos.add_parser("encolar")
    encolar_t.add_argument("tipo", choices=["ANALISIS", "APLICACION"])
    encolar_t.add_argument("codigo")
    encolar_t.add_argument("observacion")
    encolar_t.add_argument("--solicitante", required=True)
    encolar_t.add_argument("--nota", default="")
    tomar_t = tareas_trabajos.add_parser("tomar")
    tomar_t.add_argument("tipo", choices=["ANALISIS", "APLICACION"])
    tomar_t.add_argument("--agente", required=True)
    tomar_t.add_argument("--codigo")
    tomar_t.add_argument("--lote", action="store_true", help="Solo ANALISIS; la aplicación va de a una (DEC-069)")
    completar_t = tareas_trabajos.add_parser("completar")
    completar_t.add_argument("identificador")
    completar_t.add_argument("--agente", required=True)
    completar_t.add_argument("--resultado", required=True)
    completar_t.add_argument("--estado", choices=["HECHO", "ERROR"], default="HECHO")
    cancelar_t = tareas_trabajos.add_parser("cancelar")
    cancelar_t.add_argument("identificador")
    cancelar_t.add_argument("--autor", required=True)
    cancelar_t.add_argument("--motivo", required=True)
    relevo = grupos.add_parser("relevo", help="Servir el relevo hacia los agentes de OpenClaw (DEC-068)")
    relevo.add_argument("--host", required=True, help="IP concreta: loopback o puerta de enlace de la red Docker")
    relevo.add_argument("--port", type=int, default=8769)
    mcp = grupos.add_parser("mcp", help="Servir herramientas MCP")
    mcp.add_argument("--transporte", choices=["stdio", "streamable-http"], default="stdio")
    mcp.add_argument("--host", default="127.0.0.1", help="Solo con streamable-http")
    mcp.add_argument("--port", type=int, default=8768, help="Solo con streamable-http")
    contrato = grupos.add_parser("contrato", help="Exportar o comprobar el OpenAPI generado")
    contrato.add_argument("--check", action="store_true", help="Comprobar que el archivo versionado esté vigente")
    sesiones = grupos.add_parser("sesiones", help="Editar un modelo en copia recuperable")
    acciones = sesiones.add_subparsers(dest="operacion", required=True)
    for operacion in ("iniciar", "leer", "documento", "editar", "preparar", "integrar", "cerrar", "anclar",
                      "retirar-anclas", "estado", "liberar"):  # fmt: skip
        accion = acciones.add_parser(operacion)
        accion.add_argument("codigo")
        if operacion not in ("iniciar", "estado", "liberar"):
            accion.add_argument("sesion")
        if operacion == "iniciar":
            accion.add_argument("--titular", default="persona", help="Quién toma el modelo (persona o agente)")
            accion.add_argument("--motivo", default="", help="Para qué se edita (observación, ajuste, etc.)")
            accion.add_argument("--modo", choices=["EDICION", "BORRADOR"], default="EDICION")
            accion.add_argument("--observacion", default=None, help="Observación que atiende la edición")
        if operacion == "liberar":
            accion.add_argument("--autor", required=True)
            accion.add_argument("--motivo", required=True, help="Por qué se libera el bloqueo (mín. 10 caracteres)")
        if operacion in ("documento", "editar"):
            accion.add_argument("nombre", choices=["tabla", "sustento", "fuentes_visor"])
        if operacion == "editar":
            accion.add_argument("--archivo", type=Path, required=True, help="Archivo UTF-8 con el nuevo contenido")
            accion.add_argument("--revision", required=True)
        if operacion == "integrar":
            accion.add_argument("--revision", type=int, required=True)
        if operacion == "preparar":
            accion.add_argument(
                "--aceptar-hallazgos", default="", help="Justificación para adoptar hallazgos ya documentados"
            )
        if operacion == "anclar":
            for campo in ("elemento", "fragmento", "cita", "titulo", "ubicacion", "vigencia"):
                accion.add_argument(f"--{campo}", required=True)
        if operacion == "retirar-anclas":
            accion.add_argument("--elemento", action="append", default=[], help="Caja cuyas anclas se retiran")
            accion.add_argument("--huerfanas", action="store_true", help="Retira anclas de cajas que ya no existen")
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
    if args.operacion == "regimen":
        from .fuentes_office import cargar_manifiesto_office
        from .fuentes_preparacion import MANIFIESTO
        from .fuentes_regimen import comprobar

        rutas = (
            list(json.loads((raiz / MANIFIESTO).read_text(encoding="utf-8"))["documentos"])
            if (raiz / MANIFIESTO).is_file()
            else []
        )
        return comprobar(raiz, rutas + list(cargar_manifiesto_office(raiz)["documentos"]))
    if args.operacion == "anclar":
        from . import fuentes_anclaje as anclaje

        if args.fragmento:
            return anclaje.anclar_fragmento(raiz, args.fragmento, args.cita)
        if not (args.archivo and args.pagina):
            raise ErrorDominio("Indique --fragmento, o --archivo y --pagina")
        return anclaje.anclar(raiz, args.archivo, args.pagina, args.cita)
    if args.operacion == "pruebas":
        from . import fuentes_pruebas as pruebas

        if args.accion_pruebas == "preparar":
            return pruebas.preparar(raiz, args.banco)
        return pruebas.medir(raiz, args.banco, con_temas=not args.sin_temas, modo=args.modo)
    if args.operacion == "temas":
        return temas.comprobar(raiz) if args.accion_temas == "comprobar" else temas.sugerir(raiz, args.proceso)
    filtros = {k: getattr(args, k) for k in ("id_documento", "archivo", "tipo", "area", "articulo", "regimen")}
    return busqueda.buscar_pasajes(
        raiz, args.consulta, modo=args.modo, tema=args.tema, con_relacionados=args.con_relacionados,
        filtros=filtros, limite=args.limite, max_caracteres=args.max_caracteres,
    )  # fmt: skip


def _etapa_observacion(observaciones: ServicioResolucion, args: argparse.Namespace) -> object:
    comunes = {"autor": args.autor, "revision_esperada": args.revision}
    if args.operacion == "corregir":
        return observaciones.iniciar_correccion(
            args.codigo, args.identificador, **comunes, confirmar_vigencia=args.confirmar_vigencia
        )
    datos = json.loads(args.archivo.read_text(encoding="utf-8")) if getattr(args, "archivo", None) else {}
    if args.operacion == "analizar":
        return observaciones.registrar_analisis(args.codigo, args.identificador, **comunes, **datos)
    if args.operacion == "proponer":
        return observaciones.registrar_propuesta(args.codigo, args.identificador, **comunes, **datos)
    if args.operacion == "definir":
        return observaciones.definir(
            args.codigo, args.identificador, **comunes, tipo=args.tipo, opciones=args.opcion or datos.get("opciones"),
            texto=args.texto or datos.get("texto", ""), formato=datos.get("formato", "texto"),
            vinculada_a=args.vinculada_a or datos.get("vinculada_a", ""),
        )  # fmt: skip
    return observaciones.registrar_aplicacion(args.codigo, args.identificador, **comunes, **datos)


def _conocimiento(repositorio: RepositorioProcesos, args: argparse.Namespace) -> object:
    from . import conocimiento as c

    raiz = repositorio.raiz
    operacion = args.operacion
    if operacion == "notas":
        filtros = {k: getattr(args, k) for k in ("area", "tipo", "estado", "clase", "etiqueta", "proceso", "texto")}
        return c.listar_notas(raiz, **filtros, limite=args.limite, desplazamiento=args.desplazamiento)
    if operacion == "nota":
        return c.leer_nota(raiz, args.ruta, args.desde, args.max_caracteres)
    if operacion == "documentos":
        con_texto = None if args.con_texto is None else args.con_texto == "si"
        return c.listar_documentos(
            raiz, texto=args.texto, area=args.area, formato=args.formato, regimen=args.regimen, con_texto=con_texto,
            limite=args.limite, desplazamiento=args.desplazamiento,
        )  # fmt: skip
    if operacion == "documento":
        return c.leer_documento(raiz, args.identificador)
    if operacion == "texto-documento":
        return c.leer_texto_documento(raiz, args.identificador, args.pagina, args.paginas, args.max_caracteres)
    if operacion == "indice":
        return c.indice_documento(raiz, args.identificador, archivo=args.archivo, desde=args.desde, hasta=args.hasta)
    if operacion == "articulos":
        return c.leer_articulos(
            raiz, args.identificador, args.desde, args.hasta, archivo=args.archivo, max_caracteres=args.max_caracteres
        )
    if operacion == "temas":
        return c.listar_temas(raiz)
    if operacion == "reglas":
        filtros = {k: getattr(args, k) for k in ("proceso", "dominio", "estado", "modalidad", "texto")}
        return c.listar_reglas(raiz, **filtros)
    if operacion == "regla":
        return c.leer_regla(raiz, args.identificador)
    if operacion == "glosario":
        return c.buscar_glosario(raiz, args.texto)
    if operacion == "decisiones":
        return c.buscar_decisiones(raiz, texto=args.texto, identificador=args.identificador, limite=args.limite)
    if operacion == "etiquetas":
        return c.etiquetas(raiz, args.accion)
    return c.paquete_contexto(repositorio, args.codigo, args.tarea)


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
        if args.operacion in ("segmentar", "indexar", "buscar", "contexto", "temas", "pruebas", "anclar", "regimen"):
            return _consulta(repositorio.raiz, args)
        resultado = operaciones[args.operacion]()
        if args.operacion in CAMBIAN_CACHE:
            resultado["indice"] = generar_indice(repositorio.raiz)["indice"]
        return resultado
    if args.grupo == "conocimiento":
        return _conocimiento(repositorio, args)
    if args.grupo == "auditoria":
        from . import auditoria
        from .auditoria_informe import informe

        if args.operacion == "inventariar-elementos":
            return auditoria.inventariar_elementos(repositorio.raiz, args.codigo)
        if args.operacion == "registrar":
            entradas = json.loads(args.archivo.read_text(encoding="utf-8"))
            return auditoria.registrar(repositorio.raiz, args.codigo, entradas)
        if args.operacion == "correr":
            from .auditoria_corrida import correr

            return correr(repositorio.raiz, args.alcance, args.max_procesos)
        if args.operacion == "comparar-interfaces":
            from .auditoria_interfaces import comparar_interfaces

            return comparar_interfaces(repositorio.raiz, args.codigo)
        if args.operacion == "cobertura":
            entradas = json.loads(args.archivo.read_text(encoding="utf-8"))
            return auditoria.registrar_cobertura(repositorio.raiz, args.codigo, entradas)
        if args.operacion == "reconfirmar":
            datos = json.loads(args.archivo.read_text(encoding="utf-8"))
            return auditoria.reconfirmar(
                repositorio.raiz, args.codigo, datos.get("afirmaciones", []), datos.get("cobertura"),
                datos.get("motivo", ""),
            )  # fmt: skip
        resultado = informe(repositorio.raiz, args.codigo)
        if args.check and not resultado["ok"]:
            print(json.dumps(resultado, ensure_ascii=False, indent=2))
            return 1
        return resultado
    observaciones = ServicioResolucion(repositorio)
    documentos = ServicioDocumentos(repositorio)
    sesiones = ServicioSesiones(repositorio)
    if args.grupo == "sesiones":
        if args.operacion == "iniciar":
            return sesiones.iniciar(args.codigo, args.titular, args.motivo, args.modo, args.observacion)
        if args.operacion == "estado":
            return sesiones.estado(args.codigo)
        if args.operacion == "liberar":
            return sesiones.liberar(args.codigo, args.autor, args.motivo)
        if args.operacion == "leer":
            return sesiones.leer(args.codigo, args.sesion)
        if args.operacion == "documento":
            return sesiones.contenido(args.codigo, args.sesion, args.nombre)
        if args.operacion == "editar":
            return sesiones.editar(
                args.codigo, args.sesion, args.nombre, args.archivo.read_text(encoding="utf-8"), args.revision
            )
        if args.operacion == "preparar":
            return sesiones.preparar(args.codigo, args.sesion, aceptar_hallazgos=args.aceptar_hallazgos)
        if args.operacion == "anclar":
            return sesiones.anclar(
                args.codigo, args.sesion, args.elemento, args.fragmento, args.cita, args.titulo, args.ubicacion,
                args.vigencia,
            )  # fmt: skip
        if args.operacion == "retirar-anclas":
            return sesiones.retirar_anclas(args.codigo, args.sesion, args.elemento, args.huerfanas)
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
        if args.operacion == "etapas":
            return observaciones.por_etapa(args.etapa, args.codigo, not args.resumen)
        if args.operacion in ("analizar", "proponer", "definir", "corregir", "aplicar"):
            return _etapa_observacion(observaciones, args)
        if args.operacion == "responder":
            return observaciones.responder(
                args.codigo, args.identificador, args.texto, args.autor, args.revision, args.formato
            )
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
            referencia=args.referencia,
            formato=args.formato,
        )
    if args.grupo == "modelo":
        from .generacion import generar_modelo

        resultado = generar_modelo(
            repositorio, args.codigo, check=args.check, exportar_imagenes=args.exportar_imagenes,
            sin_cache=args.sin_cache, forzar=args.forzar, justificacion=args.justificacion,
        )  # fmt: skip
        if resultado["codigo_salida"]:
            print(json.dumps(resultado, ensure_ascii=False, indent=2))
            return resultado["codigo_salida"]
        return resultado
    if args.grupo == "trabajos":
        from .trabajos import ServicioTrabajos

        servicio = ServicioTrabajos(repositorio)
        if args.operacion == "listar":
            return servicio.listar(estado=args.estado, tipo=args.tipo, codigo=args.codigo)
        if args.operacion == "encolar":
            return servicio.encolar(args.tipo, args.codigo, args.observacion, args.solicitante, nota=args.nota)
        if args.operacion == "tomar":

            def ocupado(codigo: str) -> bool:
                return sesiones.estado(codigo)["estado"] != "LIBRE"

            return servicio.tomar(args.tipo, args.agente, args.codigo, args.lote, ocupado=ocupado)
        if args.operacion == "completar":
            return servicio.completar(args.identificador, args.agente, args.resultado, args.estado)
        return servicio.cancelar(args.identificador, args.autor, args.motivo)
    if args.grupo == "relevo":
        from .relevo import servir

        servir(args.host, args.port)
        return None
    if args.grupo == "api":
        import uvicorn

        uvicorn.run("mesa_modelamiento.api:app", host=args.host, port=args.port)
        return None
    from .mcp_adapter import main as servir_mcp

    servir_mcp(args.transporte, args.host, args.port)
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
