"""Adaptador MCP local sobre los mismos servicios que utiliza la API."""

from __future__ import annotations

from mcp.server import MCPServer

from .documentos import ServicioDocumentos
from .observaciones import ServicioObservaciones
from .repositorio import RepositorioProcesos
from .sesiones import ServicioSesiones

# Alias con el que el agente de IA firma sus registros en el ciclo de retroalimentación (DEC-064).
AUTOR_AGENTE = "Claudia"


def crear_servidor(repositorio: RepositorioProcesos | None = None) -> MCPServer:
    repositorio = repositorio or RepositorioProcesos.desde_entorno()
    observaciones = ServicioObservaciones(repositorio)
    documentos = ServicioDocumentos(repositorio)
    sesiones = ServicioSesiones(repositorio)
    servidor = MCPServer(
        "mesa-modelamiento",
        instructions=(
            "Lee modelos y registra observaciones de borrador. No atribuyas validacion normativa, "
            "conformidad ni aprobacion institucional. Usa IDs de proceso y BPMN existentes."
        ),
    )

    @servidor.tool()
    def listar_procesos() -> dict:
        """Lista el arbol de procesos, comenzando por el Nivel 0."""
        return repositorio.arbol()

    @servidor.tool()
    def leer_proceso(codigo: str) -> dict:
        """Lee detalle, cajas, flujos y fuentes registradas de un proceso por codigo NT."""
        return repositorio.leer_modelo(codigo)

    @servidor.tool()
    def listar_observaciones(codigo: str) -> dict:
        """Lee observaciones y revision vigente de un proceso."""
        return observaciones.listar(codigo)

    @servidor.tool()
    def registrar_observacion(
        codigo: str,
        elemento: str,
        texto: str,
        revision_esperada: str,
        tipo: str = "OBSERVACION",
        referencia: str = "",
        formato: str = "texto",
    ) -> dict:
        """Registra una observacion o comentario sobre un ID BPMN; no altera el modelo. formato: texto o html."""
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

    @servidor.tool()
    def responder_observacion(
        codigo: str, identificador: str, texto: str, revision_esperada: str, formato: str = "texto"
    ) -> dict:
        """Añade respuesta a una observación existente sin alterar el modelo. formato: texto o html."""
        return observaciones.responder(codigo, identificador, texto, AUTOR_AGENTE, revision_esperada, formato)

    @servidor.tool()
    def cambiar_estado_observacion(codigo: str, identificador: str, estado: str, revision_esperada: str) -> dict:
        """Abre o resuelve una observación; no aprueba el proceso ni su sustento."""
        return observaciones.actualizar_estado(codigo, identificador, estado, revision_esperada, AUTOR_AGENTE)

    @servidor.tool()
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
        from .repositorio import ErrorDominio

        raise ErrorDominio("Elemento no encontrado", 404)

    @servidor.tool()
    def leer_fuente(codigo: str, referencia: str, indice: int) -> dict:
        """Lee texto de una fuente registrada y solo la página PDF registrada, sin OCR."""
        return documentos.leer_fuente(codigo, referencia, indice)

    @servidor.tool()
    def iniciar_edicion(codigo: str) -> dict:
        """Captura una instantánea verificable y abre una copia aislada del proceso."""
        return sesiones.iniciar(codigo)

    @servidor.tool()
    def leer_sesion(codigo: str, sesion: str) -> dict:
        """Lee estado, revisiones y preparación de la sesión."""
        return sesiones.leer(codigo, sesion)

    @servidor.tool()
    def leer_documento_copia(codigo: str, sesion: str, nombre: str) -> dict:
        """Lee tabla, sustento o metadatos de fuentes de la copia editable."""
        return sesiones.contenido(codigo, sesion, nombre)

    @servidor.tool()
    def editar_documento_copia(codigo: str, sesion: str, nombre: str, texto: str, revision_esperada: str) -> dict:
        """Edita solo la copia con revisión esperada; no toca originales aprobados."""
        return sesiones.editar(codigo, sesion, nombre, texto, revision_esperada)

    @servidor.tool()
    def preparar_cambio(codigo: str, sesion: str) -> dict:
        """Regenera la copia y devuelve diff y validación D1-D5 para revisar."""
        return sesiones.preparar(codigo, sesion)

    @servidor.tool()
    def aplicar_cambio(codigo: str, sesion: str, revision_esperada: int) -> dict:
        """Integra cambios preparados con control de conflictos y instantánea recuperable."""
        return sesiones.integrar(codigo, sesion, revision_esperada)

    @servidor.tool()
    def cerrar_edicion(codigo: str, sesion: str) -> dict:
        """Cierra sin integrar; conserva la copia y libera el único editor."""
        return sesiones.cerrar(codigo, sesion)

    return servidor


def main() -> None:
    crear_servidor().run(transport="stdio")


if __name__ == "__main__":
    main()
