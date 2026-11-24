"""Adaptador local al MCP OCR; no persiste credenciales ni modifica PDF originales."""

from __future__ import annotations

import asyncio
import os
from pathlib import Path

import httpx2
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

from .repositorio import ErrorDominio

SERVIDOR = "http://127.0.0.1:18040/mcp"


def _contenido(resultado: object) -> dict:
    if getattr(resultado, "isError", False):
        raise ErrorDominio("El servicio OCR rechazó la solicitud")
    datos = getattr(resultado, "structuredContent", None)
    if isinstance(datos, dict):
        return datos
    import json

    bloques = getattr(resultado, "content", [])
    for bloque in bloques:
        if getattr(bloque, "type", "") == "text":
            return json.loads(bloque.text)
    raise ErrorDominio("El servicio OCR no devolvió datos estructurados")


async def _procesar(ruta: Path, titulo: str) -> dict:
    clave = os.getenv("OCR_MCP_KEY")
    if not clave:
        raise ErrorDominio("Falta OCR_MCP_KEY en el entorno local")
    async with httpx2.AsyncClient(headers={"Authorization": f"Bearer {clave}"}, timeout=120) as cliente:
        async with streamable_http_client(SERVIDOR, http_client=cliente) as (entrada, salida):
            async with ClientSession(entrada, salida) as sesion:
                await sesion.initialize()
                carga = _contenido(await sesion.call_tool("ocr_upload_link", {}))
                if ruta.stat().st_size > carga["max_bytes"]:
                    raise ErrorDominio("El lote PDF excede el máximo de OCR")
                async with httpx2.AsyncClient(timeout=300) as transferencia:
                    respuesta = await transferencia.put(carga["url"], content=ruta.read_bytes())
                    respuesta.raise_for_status()
                trabajo = _contenido(
                    await sesion.call_tool(
                        "ocr_submit", {"upload_id": carga["upload_id"], "artifacts": ["md"], "title": titulo}
                    )
                )
                identificador = trabajo["job_id"]
                for _ in range(120):
                    estado = _contenido(
                        await sesion.call_tool("ocr_status", {"job_id": identificador, "wait_seconds": 10})
                    )
                    valor = str(estado.get("status", estado.get("state", ""))).lower()
                    if valor in ("completed", "complete", "done", "succeeded", "success"):
                        break
                    if valor in ("failed", "error", "cancelled"):
                        raise ErrorDominio(f"OCR terminó con estado {valor}")
                else:
                    raise ErrorDominio("Tiempo de espera OCR agotado")
                paginas = []
                baja_confianza = []
                for numero in range(1, int(estado["pages"]) + 1):
                    resultado = _contenido(
                        await sesion.call_tool("ocr_read_markdown", {"job_id": identificador, "pages": str(numero)})
                    )
                    if resultado.get("truncated"):
                        raise ErrorDominio("OCR devolvió Markdown truncado")
                    paginas.append(resultado.get("markdown", ""))
                    if resultado.get("low_confidence_pages"):
                        baja_confianza.append(numero)
                return {
                    "job_id": identificador,
                    "estado": estado,
                    "paginas": paginas,
                    "baja_confianza": baja_confianza,
                }


def procesar_lote(ruta: Path, titulo: str) -> dict:
    """Procesa un PDF derivado; el resultado conserva su ID de trabajo para auditoría."""
    return asyncio.run(_procesar(ruta, titulo))
