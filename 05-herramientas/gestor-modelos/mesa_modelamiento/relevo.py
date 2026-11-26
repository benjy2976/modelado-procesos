"""Relevo restringido hacia los agentes de OpenClaw de la mesa de modelamiento (DEC-068).

Sigue el patrón probado en modelador-bim (relevo del chat del visor). El token del Gateway de OpenClaw equivale a
una credencial de operador completa: este proceso es el ÚNICO que lo tiene; la API y el navegador no lo ven.
Solo permite:

- ``GET /salud``;
- ``POST /v1/turno {conversacion, mensaje}``: un turno de chat con el agente fijo ``mesa-chat``, sesión por
  conversación y streaming (SSE retransmitido tal cual);
- ``POST /v1/trabajo {tipo}``: despierta al agente fijo de ``ANALISIS`` o ``APLICACION`` para que procese la cola
  de trabajos por MCP. Responde 202 al instante; un solo despertar por tipo a la vez.

No acepta otro agente, modelo, ruta ni cabeceras del llamador. Se enlaza a una IP concreta, nunca a 0.0.0.0, y el
Gateway debe ser loopback. Variables: ``MESA_RELEVO_TOKEN``, ``OPENCLAW_GATEWAY_TOKEN`` y ``OPENCLAW_GATEWAY_URL``.
"""

from __future__ import annotations

import hmac
import json
import os
import re
import threading
import urllib.error
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

GATEWAY = "http://127.0.0.1:18789"
AGENTE_CHAT = "mesa-chat"
AGENTES_TRABAJO = {"ANALISIS": "mesa-analisis", "APLICACION": "mesa-aplicacion"}
MENSAJES_TRABAJO = {
    "ANALISIS": "Hay trabajos de ANALISIS pendientes en la mesa de modelamiento. Toma uno con "
    "tomar_trabajo(tipo='ANALISIS'), procésalo según tus instrucciones y ciérralo con completar_trabajo. "
    "Repite hasta que tomar_trabajo no devuelva trabajos.",
    # DEC-069: una observación por trabajo y por sesión, para que cada cambio sea una versión propia.
    "APLICACION": "Hay trabajos de APLICACION pendientes en la mesa de modelamiento. Toma uno con "
    "tomar_trabajo(tipo='APLICACION'): recibes una sola observación. Aplícala según tus instrucciones, en su "
    "propia sesión (iniciar_edicion con la observación y el trabajo), y cierra con completar_trabajo. Repite "
    "hasta que tomar_trabajo no devuelva trabajos.",
}
CONVERSACION = re.compile(r"^M-[0-9A-Za-z.-]{6,80}$")
MAX_MENSAJE = 16000
NO_PERMITIDOS = ("0.0.0.0", "::", "")
TIEMPO_TURNO = 600
TIEMPO_TRABAJO = 1800


def carga_turno(agente: str, sesion: str, mensaje: str, stream: bool) -> dict:
    """Cuerpo para el Gateway: agente fijo y sesión estable (continuidad por conversación o por trabajo)."""
    return {"model": f"openclaw/{agente}", "user": sesion, "stream": stream,
            "messages": [{"role": "user", "content": mensaje}]}  # fmt: skip


def validar_turno(cuerpo: object) -> tuple[str, str]:
    if not isinstance(cuerpo, dict) or set(cuerpo) - {"conversacion", "mensaje"}:
        raise ValueError("Solo se admiten «conversacion» y «mensaje»")
    conversacion, mensaje = cuerpo.get("conversacion", ""), cuerpo.get("mensaje", "")
    if not isinstance(conversacion, str) or not CONVERSACION.match(conversacion):
        raise ValueError("Conversación inválida")
    if not isinstance(mensaje, str) or not mensaje.strip() or len(mensaje) > MAX_MENSAJE:
        raise ValueError(f"Mensaje vacío o mayor de {MAX_MENSAJE} caracteres")
    return conversacion, mensaje


def validar_trabajo(cuerpo: object) -> str:
    if not isinstance(cuerpo, dict) or set(cuerpo) != {"tipo"} or cuerpo["tipo"] not in AGENTES_TRABAJO:
        raise ValueError(f"Solo se admite «tipo»: {sorted(AGENTES_TRABAJO)}")
    return cuerpo["tipo"]


class _Manejador(BaseHTTPRequestHandler):
    token: str | None = None
    gateway = GATEWAY
    gateway_token: str | None = None
    en_curso: dict[str, threading.Lock] = {}

    def do_GET(self) -> None:  # noqa: N802
        if self.path == "/salud":
            return self._json({"estado": "OK", "servicio": "relevo-mesa", "agentes":
                               [AGENTE_CHAT, *AGENTES_TRABAJO.values()]})  # fmt: skip
        self._json({"error": "Ruta no encontrada"}, 404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in ("/v1/turno", "/v1/trabajo"):
            return self._json({"error": "Ruta no encontrada"}, 404)
        recibido = self.headers.get("Authorization", "")
        if not self.token or not hmac.compare_digest(recibido.encode(), f"Bearer {self.token}".encode()):
            return self._json({"error": "No autorizado"}, 401)
        try:
            largo = int(self.headers.get("Content-Length") or 0)
            if largo > MAX_MENSAJE * 4:
                raise ValueError("Cuerpo demasiado grande")
            cuerpo = json.loads(self.rfile.read(largo) or b"{}")
            if self.path == "/v1/trabajo":
                return self._trabajo(validar_trabajo(cuerpo))
            conversacion, mensaje = validar_turno(cuerpo)
        except (ValueError, json.JSONDecodeError) as exc:
            return self._json({"error": str(exc)}, 400)
        self._turno(conversacion, mensaje)

    def _pedido(self, carga: dict, stream: bool) -> urllib.request.Request:
        aceptar = "text/event-stream" if stream else "application/json"
        return urllib.request.Request(
            self.gateway.rstrip("/") + "/v1/chat/completions", data=json.dumps(carga).encode(), method="POST",
            headers={"Content-Type": "application/json", "Accept": aceptar,
                     "Authorization": f"Bearer {self.gateway_token}"},
        )  # fmt: skip

    def _turno(self, conversacion: str, mensaje: str) -> None:
        pedido = self._pedido(carga_turno(AGENTE_CHAT, f"conv:{conversacion}", mensaje, True), True)
        try:
            respuesta = urllib.request.urlopen(pedido, timeout=TIEMPO_TURNO)  # noqa: S310 - Gateway loopback validado
        except urllib.error.HTTPError as exc:
            self.log_error("Gateway respondió %s", exc.code)
            return self._json({"error": f"El Gateway de OpenClaw respondió {exc.code}"}, 502)
        except urllib.error.URLError as exc:
            return self._json({"error": f"Gateway de OpenClaw no disponible: {exc.reason}"}, 502)
        with respuesta:
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            for linea in respuesta:  # SSE línea a línea, sin reinterpretar
                self.wfile.write(linea)
                self.wfile.flush()

    def _trabajo(self, tipo: str) -> None:
        candado = self.en_curso.setdefault(tipo, threading.Lock())
        if not candado.acquire(blocking=False):
            return self._json({"estado": "EN-CURSO", "detalle": "El agente ya está procesando la cola"}, 202)
        sesion = f"trabajo:{tipo.lower()}:{uuid.uuid4().hex}"
        pedido = self._pedido(carga_turno(AGENTES_TRABAJO[tipo], sesion, MENSAJES_TRABAJO[tipo], False), False)

        def ejecutar() -> None:
            try:
                with urllib.request.urlopen(pedido, timeout=TIEMPO_TRABAJO) as respuesta:  # noqa: S310
                    respuesta.read()
            except (urllib.error.URLError, OSError) as exc:
                self.log_error("Trabajo %s sin completar: %s", tipo, exc)
            finally:
                candado.release()

        threading.Thread(target=ejecutar, daemon=True).start()
        self._json({"estado": "DESPERTADO", "agente": AGENTES_TRABAJO[tipo], "sesion": sesion}, 202)

    def _json(self, datos: dict, codigo: int = 200) -> None:
        cuerpo = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(cuerpo)))
        self.end_headers()
        self.wfile.write(cuerpo)

    def log_message(self, formato: str, *args: object) -> None:
        if self.path != "/salud":
            super().log_message(formato, *args)


def servidor(host: str, puerto: int, token: str | None, gateway_token: str | None, gateway: str = GATEWAY):
    """Crea el servidor del relevo validando enlace, Gateway loopback y credenciales."""
    if host in NO_PERMITIDOS:
        raise SystemExit("El relevo debe enlazarse a una IP concreta (loopback o puente Docker), nunca a 0.0.0.0")
    if urlsplit(gateway).hostname not in ("127.0.0.1", "localhost", "::1"):
        raise SystemExit("El Gateway de OpenClaw debe ser loopback")
    if not token or not gateway_token:
        raise SystemExit("Faltan MESA_RELEVO_TOKEN u OPENCLAW_GATEWAY_TOKEN")
    atributos = {"token": token, "gateway": gateway, "gateway_token": gateway_token, "en_curso": {}}
    manejador = type("ManejadorRelevoMesa", (_Manejador,), atributos)
    return ThreadingHTTPServer((host, int(puerto)), manejador)


def servir(host: str = "127.0.0.1", puerto: int = 8769) -> None:
    server = servidor(host, puerto, os.environ.get("MESA_RELEVO_TOKEN"), os.environ.get("OPENCLAW_GATEWAY_TOKEN"),
                      os.environ.get("OPENCLAW_GATEWAY_URL", GATEWAY))  # fmt: skip
    print(f"Relevo de la mesa en http://{host}:{puerto} → {server.RequestHandlerClass.gateway}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
