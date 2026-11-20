"""Adaptador MCP local sobre los mismos servicios que utiliza la API."""

from __future__ import annotations

from mcp.server import MCPServer

from .observaciones import ServicioObservaciones
from .repositorio import RepositorioProcesos


def crear_servidor(repositorio: RepositorioProcesos | None = None) -> MCPServer:
    repositorio = repositorio or RepositorioProcesos.desde_entorno()
    observaciones = ServicioObservaciones(repositorio)
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
        codigo: str, elemento: str, texto: str, revision_esperada: str, tipo: str = "OBSERVACION"
    ) -> dict:
        """Registra una observacion o comentario sobre un ID BPMN; no altera el modelo."""
        return observaciones.agregar(
            codigo,
            elemento=elemento,
            texto=texto,
            autor="Agente IA",
            revision_esperada=revision_esperada,
            tipo=tipo,
        )

    return servidor


def main() -> None:
    crear_servidor().run(transport="stdio")


if __name__ == "__main__":
    main()
