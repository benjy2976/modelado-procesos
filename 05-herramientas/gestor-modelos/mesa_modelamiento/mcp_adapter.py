"""Adaptador MCP local sobre los mismos servicios que utiliza la API."""

from __future__ import annotations

import functools
from collections.abc import Callable

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from . import auditoria, conocimiento, generacion
from . import fuentes_anclaje as anclaje
from . import fuentes_busqueda as busqueda
from .documentos import ServicioDocumentos
from .repositorio import ErrorDominio, RepositorioProcesos
from .resolucion import ServicioResolucion
from .sesiones import ServicioSesiones

# Alias con el que el agente de IA firma sus registros en el ciclo de retroalimentación (DEC-064).
AUTOR_AGENTE = "Claudia"


def _errores_de_dominio(funcion: Callable) -> Callable:
    """Entrega un ErrorDominio como error de herramienta legible, no como fallo inesperado con traza."""

    @functools.wraps(funcion)
    def envoltura(*args, **kwargs):  # noqa: ANN202
        try:
            return funcion(*args, **kwargs)
        except ErrorDominio as exc:
            raise ToolError(f"{exc} (HTTP {exc.codigo_http})") from exc

    return envoltura


def crear_servidor(repositorio: RepositorioProcesos | None = None) -> MCPServer:
    repositorio = repositorio or RepositorioProcesos.desde_entorno()
    observaciones = ServicioResolucion(repositorio)
    documentos = ServicioDocumentos(repositorio)
    sesiones = ServicioSesiones(repositorio)
    servidor = MCPServer(
        "mesa-modelamiento",
        instructions=(
            "Lee, edita en copia recuperable, genera y audita modelos de procesos; registra observaciones. "
            "No atribuyas validacion normativa, conformidad ni aprobacion institucional. Toda adopcion de "
            "hallazgos D1-D5 exige justificacion documentada en el sustento."
        ),
    )

    def herramienta() -> Callable:
        def decorar(funcion: Callable) -> Callable:
            return servidor.tool()(_errores_de_dominio(funcion))

        return decorar

    @herramienta()
    def listar_procesos() -> dict:
        """Lista el arbol de procesos, comenzando por el Nivel 0."""
        return repositorio.arbol()

    @herramienta()
    def leer_proceso(codigo: str) -> dict:
        """Lee detalle, cajas, flujos y fuentes registradas de un proceso por codigo NT."""
        return repositorio.leer_modelo(codigo)

    @herramienta()
    def listar_observaciones(codigo: str) -> dict:
        """Lee observaciones y revision vigente de un proceso."""
        return observaciones.listar(codigo)

    @herramienta()
    def registrar_observacion(
        codigo: str,
        elemento: str,
        texto: str,
        revision_esperada: str,
        tipo: str = "OBSERVACION",
        referencia: str = "",
        formato: str = "texto",
    ) -> dict:
        """Registra una observación sobre una caja (ID BPMN, ID de tabla o número) o el diagrama (elemento vacío).

        No altera el modelo. formato: texto o html. La referencia «Caja N (ID)» se completa sola."""
        return observaciones.agregar(
            codigo,
            elemento=elemento,
            texto=texto,
            autor=AUTOR_AGENTE,
            revision_esperada=revision_esperada,
            tipo=tipo,
            referencia=referencia,
            formato=formato,
        )

    @herramienta()
    def responder_observacion(
        codigo: str, identificador: str, texto: str, revision_esperada: str, formato: str = "texto"
    ) -> dict:
        """Añade respuesta a una observación existente sin alterar el modelo. formato: texto o html."""
        return observaciones.responder(codigo, identificador, texto, AUTOR_AGENTE, revision_esperada, formato)

    @herramienta()
    def cambiar_estado_observacion(codigo: str, identificador: str, estado: str, revision_esperada: str) -> dict:
        """Abre o resuelve una observación; no aprueba el proceso ni su sustento."""
        return observaciones.actualizar_estado(codigo, identificador, estado, revision_esperada, AUTOR_AGENTE)

    @herramienta()
    def registrar_analisis(
        codigo: str,
        identificador: str,
        texto: str,
        clase: str,
        revision_esperada: str,
        fuentes: list[str] | None = None,
        formato: str = "texto",
    ) -> dict:
        """Etapa EN-ANALISIS (DEC-065): qué entiende el agente, contexto consultado y clase del problema.

        clase: ERROR-MODELO, EXPLICACION-AUSENTE, DIFERENCIA-CRITERIO, FALTA-EVIDENCIA o FUERA-DE-ALCANCE.
        fuentes: rutas, IDs de documento, reglas o decisiones consultadas."""
        return observaciones.registrar_analisis(
            codigo, identificador, texto=texto, clase=clase, autor=AUTOR_AGENTE,
            revision_esperada=revision_esperada, fuentes=fuentes, formato=formato,
        )  # fmt: skip

    @herramienta()
    def registrar_propuesta(
        codigo: str, identificador: str, opciones: list[dict], revision_esperada: str, seleccion: str = "UNICA"
    ) -> dict:
        """Etapa PROPUESTA (DEC-065): 1 a 8 opciones para que una persona elija en la web.

        Cada opción: titulo, detalle, efecto (CAMBIO-MODELO, CAMBIO-SUSTENTO, DECISION, ACLARACION, NO-PROCEDE,
        PENDIENTE-EVIDENCIA), elementos, fuentes, recomendada y formato. seleccion: UNICA o MULTIPLE.
        El agente nunca define: la definición la hace una persona."""
        return observaciones.registrar_propuesta(
            codigo, identificador, opciones=opciones, autor=AUTOR_AGENTE, revision_esperada=revision_esperada,
            seleccion=seleccion,
        )  # fmt: skip

    @herramienta()
    def observaciones_por_etapa(etapa: str | None = None, codigo: str | None = None) -> dict:
        """Observaciones por etapa (REGISTRADA, EN-ANALISIS, PROPUESTA, DEFINIDA, EN-CORRECCION,
        PENDIENTE-EVIDENCIA, RESUELTA) en un proceso o en todo el árbol, con su resolución."""
        return observaciones.por_etapa(etapa, codigo)

    @herramienta()
    def iniciar_correccion(
        codigo: str, identificador: str, revision_esperada: str, confirmar_vigencia: bool = False
    ) -> dict:
        """Etapa EN-CORRECCION de una observación DEFINIDA. Si la tabla cambió desde la definición, confirme
        que la definición sigue aplicando o vuelva a analizar."""
        return observaciones.iniciar_correccion(
            codigo, identificador, autor=AUTOR_AGENTE, revision_esperada=revision_esperada,
            confirmar_vigencia=confirmar_vigencia,
        )  # fmt: skip

    @herramienta()
    def registrar_aplicacion(
        codigo: str,
        identificador: str,
        texto: str,
        revision_esperada: str,
        cerrar: bool = True,
        sesion: str = "",
        cambios: list[str] | None = None,
        validacion: str = "",
        decision: str = "",
        formato: str = "texto",
    ) -> dict:
        """Cierra una observación con evidencia de lo aplicado (sesión, cambios, D1-D5, decisión DEC-NNN).

        Con cerrar=False queda en PENDIENTE-EVIDENCIA. Un CAMBIO-MODELO exige la sesión que lo integró."""
        return observaciones.registrar_aplicacion(
            codigo, identificador, texto=texto, autor=AUTOR_AGENTE, revision_esperada=revision_esperada,
            cerrar=cerrar, sesion=sesion, cambios=cambios, validacion=validacion, decision=decision, formato=formato,
        )  # fmt: skip

    @herramienta()
    def leer_elemento(codigo: str, identificador: str) -> dict:
        """Lee una caja o flujo por ID, sin inventar fuente ni fundamento."""
        modelo = repositorio.leer_modelo(codigo)
        if identificador in modelo["elementos"]:
            return {
                "tipo": "elemento",
                "datos": modelo["elementos"][identificador],
                "fuentes": modelo["fuentes_visor"].get(modelo["elementos"][identificador]["ref"], []),
            }
        if identificador in modelo["flujos"]:
            return {"tipo": "flujo", "datos": modelo["flujos"][identificador]}
        raise ErrorDominio("Elemento no encontrado", 404)

    @herramienta()
    def leer_fuente(codigo: str, referencia: str, indice: int) -> dict:
        """Lee texto de una fuente registrada y solo la página PDF registrada, sin OCR."""
        return documentos.leer_fuente(codigo, referencia, indice)

    @herramienta()
    def iniciar_edicion(codigo: str) -> dict:
        """Captura una instantánea verificable y abre una copia aislada del proceso."""
        return sesiones.iniciar(codigo)

    @herramienta()
    def leer_sesion(codigo: str, sesion: str) -> dict:
        """Lee estado, revisiones y preparación de la sesión."""
        return sesiones.leer(codigo, sesion)

    @herramienta()
    def leer_documento_copia(codigo: str, sesion: str, nombre: str) -> dict:
        """Lee tabla, sustento o metadatos de fuentes de la copia editable."""
        return sesiones.contenido(codigo, sesion, nombre)

    @herramienta()
    def editar_documento_copia(codigo: str, sesion: str, nombre: str, texto: str, revision_esperada: str) -> dict:
        """Edita solo la copia con revisión esperada; no toca originales aprobados."""
        return sesiones.editar(codigo, sesion, nombre, texto, revision_esperada)

    @herramienta()
    def preparar_cambio(codigo: str, sesion: str, aceptar_hallazgos: str = "") -> dict:
        """Numera cajas nuevas, regenera la copia y devuelve diff y validación D1-D5.

        aceptar_hallazgos: justificación (mín. 20 caracteres) para adoptar hallazgos ya documentados en el
        sustento de la copia; sin ella, un resultado con hallazgos no es aplicable."""
        return sesiones.preparar(codigo, sesion, aceptar_hallazgos=aceptar_hallazgos)

    @herramienta()
    def anclar_en_copia(
        codigo: str, sesion: str, elemento: str, fragmento: str, cita: str, titulo: str, ubicacion: str, vigencia: str
    ) -> dict:
        """Ancla en la copia una cita literal de un fragmento de la biblioteca a una caja (ID de tabla)."""
        return sesiones.anclar(codigo, sesion, elemento, fragmento, cita, titulo, ubicacion, vigencia)

    @herramienta()
    def retirar_anclas_copia(
        codigo: str, sesion: str, elementos: list[str] | None = None, huerfanas: bool = False
    ) -> dict:
        """Retira anclas de las cajas indicadas y, con huerfanas, de las cajas que ya no existen en la copia."""
        return sesiones.retirar_anclas(codigo, sesion, elementos, huerfanas)

    @herramienta()
    def aplicar_cambio(codigo: str, sesion: str, revision_esperada: int) -> dict:
        """Integra cambios preparados con control de conflictos y instantánea recuperable."""
        return sesiones.integrar(codigo, sesion, revision_esperada)

    @herramienta()
    def cerrar_edicion(codigo: str, sesion: str) -> dict:
        """Cierra sin integrar; conserva la copia y libera el único editor. Tras aplicar_cambio no hace falta."""
        return sesiones.cerrar(codigo, sesion)

    @herramienta()
    def buscar_notas(
        area: str | None = None,
        tipo: str | None = None,
        estado: str | None = None,
        clase: str | None = None,
        etiqueta: str | None = None,
        proceso: str | None = None,
        texto: str | None = None,
        limite: int = 30,
        desplazamiento: int = 0,
    ) -> dict:
        """Busca notas Markdown por propiedades (tipo, estado_documento, clase_conocimiento, tags, proceso) y texto.

        area: gobernanza, referencias, procesos, conocimiento, coordinacion o herramientas. Devuelve rutas,
        títulos y extractos; lea el contenido con leer_nota."""
        return conocimiento.listar_notas(
            repositorio.raiz, area=area, tipo=tipo, estado=estado, clase=clase, etiqueta=etiqueta, proceso=proceso,
            texto=texto, limite=limite, desplazamiento=desplazamiento,
        )  # fmt: skip

    @herramienta()
    def leer_nota(ruta: str, desde: int = 0, max_caracteres: int = 20000) -> dict:
        """Lee una nota autorizada: propiedades, título, enlaces y un tramo del texto (use siguiente para continuar).

        Nunca lee originales, cachés ni carpetas temporales."""
        return conocimiento.leer_nota(repositorio.raiz, ruta, desde, max_caracteres)

    @herramienta()
    def listar_documentos(
        texto: str | None = None,
        area: str | None = None,
        formato: str | None = None,
        regimen: str | None = None,
        con_texto: bool | None = None,
        limite: int = 30,
        desplazamiento: int = 0,
    ) -> dict:
        """Inventario de la biblioteca (PDF y Office): ID, título, ruta, vigencia, régimen y texto derivado."""
        return conocimiento.listar_documentos(
            repositorio.raiz, texto=texto, area=area, formato=formato, regimen=regimen, con_texto=con_texto,
            limite=limite, desplazamiento=desplazamiento,
        )  # fmt: skip

    @herramienta()
    def leer_documento(identificador: str) -> dict:
        """Ficha de un documento de la biblioteca por ID de catálogo o ruta del original."""
        return conocimiento.leer_documento(repositorio.raiz, identificador)

    @herramienta()
    def leer_texto_documento(
        identificador: str, pagina_desde: int = 1, paginas: int = 3, max_caracteres: int = 12000
    ) -> dict:
        """Páginas del Markdown derivado de un documento (no del original), por ID o ruta."""
        return conocimiento.leer_texto_documento(repositorio.raiz, identificador, pagina_desde, paginas, max_caracteres)

    @herramienta()
    def listar_temas() -> dict:
        """Vocabulario de temas de búsqueda con sus términos y procesos."""
        return conocimiento.listar_temas(repositorio.raiz)

    @herramienta()
    def listar_reglas(
        proceso: str | None = None,
        dominio: str | None = None,
        estado: str | None = None,
        modalidad: str | None = None,
        texto: str | None = None,
    ) -> dict:
        """Reglas normativas desde sus YAML; proceso incluye ancestros y descendientes. BORRADOR-IA no es validada."""
        return conocimiento.listar_reglas(
            repositorio.raiz, proceso=proceso, dominio=dominio, estado=estado, modalidad=modalidad, texto=texto
        )

    @herramienta()
    def leer_regla(identificador: str) -> dict:
        """Regla normativa completa con sus eventos de revisión."""
        return conocimiento.leer_regla(repositorio.raiz, identificador)

    @herramienta()
    def buscar_glosario(texto: str | None = None) -> dict:
        """Términos del glosario vivo cuyo término o definición contiene el texto."""
        return conocimiento.buscar_glosario(repositorio.raiz, texto)

    @herramienta()
    def buscar_decisiones(texto: str | None = None, identificador: str | None = None, limite: int = 20) -> dict:
        """Decisiones del registro por ID (DEC-NNN) o texto; las más recientes primero."""
        return conocimiento.buscar_decisiones(repositorio.raiz, texto=texto, identificador=identificador, limite=limite)

    @herramienta()
    def revisar_etiquetas(accion: str = "revisar") -> dict:
        """Revisa o lista las etiquetas de las notas (solo lectura): accion revisar o listar."""
        return conocimiento.etiquetas(repositorio.raiz, accion)

    @herramienta()
    def paquete_contexto(codigo: str, tarea: str = "") -> dict:
        """Paquete de contexto de una tarea sobre un proceso: modelo vigente, notas, reglas aplicables, fuentes
        ancladas, guías de lectura, glosario, decisiones, observaciones abiertas, auditoría y sesión activa."""
        return conocimiento.paquete_contexto(repositorio, codigo, tarea)

    @herramienta()
    def generar_modelo(
        codigo: str,
        check: bool = False,
        exportar_imagenes: bool = False,
        sin_cache: bool = False,
        forzar: bool = False,
        justificacion: str = "",
    ) -> dict:
        """Genera o comprueba el BPMN y el HTML de una tabla ya integrada y devuelve el informe D1-D5.

        forzar adopta hallazgos y exige justificacion; esta debe constar en el sustento. Para cambiar la tabla
        use una sesión de edición."""
        return generacion.generar_modelo(
            repositorio, codigo, check=check, exportar_imagenes=exportar_imagenes, sin_cache=sin_cache,
            forzar=forzar, justificacion=justificacion,
        )  # fmt: skip

    @herramienta()
    def auditoria_inventariar(codigo: str) -> dict:
        """Inventaría elementos, flujos, carriles y mensajes con IDs de auditoría."""
        return auditoria.inventariar_elementos(repositorio.raiz, codigo)

    @herramienta()
    def auditoria_registrar(codigo: str, afirmaciones: list[dict]) -> dict:
        """Registra un lote de afirmaciones con citas verificadas; rechaza todo el lote ante un error."""
        return auditoria.registrar(repositorio.raiz, codigo, afirmaciones, AUTOR_AGENTE)

    @herramienta()
    def auditoria_cobertura(codigo: str, obligaciones: list[dict]) -> dict:
        """Reemplaza la cobertura fuente→modelo del proceso; rechaza todo el lote ante un error."""
        return auditoria.registrar_cobertura(repositorio.raiz, codigo, obligaciones)

    @herramienta()
    def auditoria_reconfirmar(
        codigo: str, afirmaciones: list[dict], motivo: str, cobertura: list[dict] | None = None
    ) -> dict:
        """Tras cambiar la tabla: reinventaría, conserva lo vigente, registra nuevas y rectifica superadas.

        cobertura: cambios por fragmento y comienzo de la obligación; con cita y sin coincidencia se agrega."""
        return auditoria.reconfirmar(repositorio.raiz, codigo, afirmaciones, cobertura, motivo, AUTOR_AGENTE)

    @herramienta()
    def auditoria_correr(alcance: str, max_procesos: int | None = None) -> dict:
        """Actualiza el estado reanudable de la auditoría de todos los procesos de un alcance."""
        from .auditoria_corrida import correr

        return correr(repositorio.raiz, alcance, max_procesos)

    @herramienta()
    def auditoria_interfaces(codigo: str) -> dict:
        """Candidatos de discrepancia de interfaz entre un padre, sus hijos y los hermanos."""
        from .auditoria_interfaces import comparar_interfaces

        return comparar_interfaces(repositorio.raiz, codigo)

    @herramienta()
    def auditoria_informe(codigo: str) -> dict:
        """Informe de cobertura, resultados, citas vigentes y anclas; ok indica si no hay hallazgos abiertos."""
        from .auditoria_informe import informe

        return informe(repositorio.raiz, codigo)

    @herramienta()
    def buscar_fuentes(
        consulta: str = "",
        modo: str = "flexible",
        tema: str | None = None,
        con_relacionados: bool = False,
        id_documento: str | None = None,
        archivo: str | None = None,
        tipo: str | None = None,
        area: str | None = None,
        articulo: str | None = None,
        regimen: str | None = None,
        limite: int = 8,
        max_caracteres: int = 6000,
    ) -> dict:
        """Busca pasajes candidatos en la biblioteca con ubicación verificable, acotados en cantidad y caracteres."""
        filtros = {"id_documento": id_documento, "archivo": archivo, "tipo": tipo, "area": area,
                   "articulo": articulo, "regimen": regimen}  # fmt: skip
        return busqueda.buscar_pasajes(
            repositorio.raiz, consulta, modo=modo, tema=tema, con_relacionados=con_relacionados, filtros=filtros,
            limite=limite, max_caracteres=max_caracteres,
        )  # fmt: skip

    @herramienta()
    def contexto_fragmento(fragmento: str, vecinos: int = 1, max_caracteres: int = 8000) -> dict:
        """Texto completo de un fragmento de la biblioteca y de sus vecinos."""
        return busqueda.contexto(repositorio.raiz, fragmento, vecinos, max_caracteres)

    @herramienta()
    def anclar_cita(cita: str, fragmento: str = "", archivo: str = "", pagina: int = 0) -> dict:
        """Calcula página y rectángulos de una cita en el PDF original, sin escribir en ningún proceso."""
        if fragmento:
            return anclaje.anclar_fragmento(repositorio.raiz, fragmento, cita)
        if not (archivo and pagina):
            raise ErrorDominio("Indique fragmento, o archivo y pagina")
        return anclaje.anclar(repositorio.raiz, archivo, pagina, cita)

    return servidor


def main() -> None:
    crear_servidor().run(transport="stdio")


if __name__ == "__main__":
    main()
