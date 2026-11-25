"""Cola de trabajos y relevo hacia OpenClaw (DEC-068), con un Gateway falso local."""

import json
import threading
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest

from mesa_modelamiento import relevo
from mesa_modelamiento.repositorio import ErrorDominio, RepositorioProcesos
from mesa_modelamiento.resolucion import ServicioResolucion
from mesa_modelamiento.trabajos import ServicioTrabajos


@pytest.fixture
def repositorio(tmp_path: Path) -> RepositorioProcesos:
    for codigo, carpeta in (("S4.3", "S4-3-ejecucion"), ("S4.4", "S4-4-liquidacion")):
        destino = tmp_path / "02-procesos" / "S4-prueba" / carpeta
        destino.mkdir(parents=True)
        prefijo = codigo.replace(".", "-")
        (destino / f"{prefijo}-diagrama-proceso.bpmn").write_text(
            '<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"><process id="P"/></definitions>',
            encoding="utf-8",
        )
        (destino / f"{prefijo}-diagrama-proceso-tabla.md").write_text(
            f"---\ncodigo_proceso: {codigo}\n---\n\n## Elementos\n\n"
            "| ID | Numero | Tipo | Nombre |\n|---|---|---|---|\n",
            encoding="utf-8",
        )
        (destino / f"{prefijo}-sustento.md").write_text("# Sustento\n", encoding="utf-8")
    return RepositorioProcesos(tmp_path)


def test_cola_no_duplica_toma_de_a_una_y_cierra(repositorio: RepositorioProcesos) -> None:
    """DEC-069: la aplicación se toma de a una observación y nunca dos del mismo proceso en paralelo."""
    cola = ServicioTrabajos(repositorio)
    primero = cola.encolar("APLICACION", "S4.3", "obs-1", "Equipo")
    assert cola.encolar("APLICACION", "S4.3", "obs-1", "Equipo")["duplicado"] is True
    cola.encolar("APLICACION", "S4.4", "obs-2", "Equipo")
    cola.encolar("APLICACION", "S4.3", "obs-3", "Equipo")
    with pytest.raises(ErrorDominio, match="de a una"):
        cola.tomar("APLICACION", "Claudia", lote=True)
    tomado = cola.tomar("APLICACION", "Claudia")
    assert [t["observacion"] for t in tomado["tomados"]] == ["obs-1"]
    siguiente = cola.tomar("APLICACION", "Claudia")
    assert siguiente["codigo"] == "S4.4", "S4.3 ya tiene una aplicación en curso"
    assert cola.tomar("APLICACION", "Claudia")["tomados"] == []
    with pytest.raises(ErrorDominio, match="resultado"):
        cola.completar(primero["id"], "Claudia", " ")
    cerrado = cola.completar(primero["id"], "Claudia", "Aplicado en sesión abc")
    assert cerrado["estado"] == "HECHO" and [e["accion"] for e in cerrado["historial"]] == [
        "ENCOLADO",
        "TOMADO",
        "HECHO",
    ]
    assert cola.tomar("APLICACION", "Claudia", ocupado=lambda codigo: codigo == "S4.3")["tomados"] == []
    assert cola.tomar("APLICACION", "Claudia")["tomados"][0]["observacion"] == "obs-3"
    with pytest.raises(ErrorDominio):
        cola.encolar("OTRO", "S4.3", "obs-9", "Equipo")


def test_trabajo_vencido_vuelve_a_estar_disponible(repositorio: RepositorioProcesos) -> None:
    cola = ServicioTrabajos(repositorio)
    trabajo = cola.encolar("ANALISIS", "S4.3", "obs-1", "Equipo")
    cola.tomar("ANALISIS", "Claudia")
    datos = json.loads(cola._archivo.read_text(encoding="utf-8"))
    datos["trabajos"][0]["tomado_en"] = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
    cola._archivo.write_text(json.dumps(datos), encoding="utf-8")
    assert cola.listar()["por_estado"] == {"PENDIENTE": 1}
    assert cola.tomar("ANALISIS", "Claudia")["tomados"][0]["id"] == trabajo["id"]


def test_definir_encola_aplicacion_y_solicitud_de_analisis(repositorio: RepositorioProcesos) -> None:
    servicio = ServicioResolucion(repositorio)
    revision = servicio.listar("S4.3")["revision"]
    obs = servicio.agregar("S4.3", elemento="", texto="Duda", autor="Equipo", revision_esperada=revision)
    analisis = servicio.solicitar_analisis("S4.3", obs["id"], "Equipo")
    assert analisis["tipo"] == "ANALISIS" and analisis["estado"] == "PENDIENTE"
    definida = servicio.definir(
        "S4.3", obs["id"], tipo="MANUAL", texto="Hágase así", autor="Equipo",
        revision_esperada=servicio.listar("S4.3")["revision"],
    )  # fmt: skip
    assert definida["trabajo"]["tipo"] == "APLICACION"
    with pytest.raises(ErrorDominio, match="etapa DEFINIDA"):
        servicio.solicitar_analisis("S4.3", obs["id"], "Equipo")
    pendientes = ServicioTrabajos(repositorio).listar(estado="PENDIENTE")
    assert sorted(t["tipo"] for t in pendientes["trabajos"]) == ["ANALISIS", "APLICACION"]


class _GatewayFalso(BaseHTTPRequestHandler):
    recibidos: list = []

    def do_POST(self) -> None:  # noqa: N802
        cuerpo = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        self.recibidos.append({"cuerpo": cuerpo, "auth": self.headers.get("Authorization")})
        self.send_response(200)
        if cuerpo.get("stream"):
            self.send_header("Content-Type", "text/event-stream")
            self.end_headers()
            self.wfile.write(b'data: {"choices":[{"delta":{"content":"Hola"}}]}\n\n')
            self.wfile.write(b"data: [DONE]\n\n")
        else:
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"choices":[{"message":{"content":"listo"}}]}')

    def log_message(self, *args: object) -> None:
        pass


def _levantar(servidor) -> int:
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    return servidor.server_address[1]


def _post(url: str, cuerpo: dict, token: str) -> tuple[int, bytes]:
    pedido = urllib.request.Request(url, data=json.dumps(cuerpo).encode(), method="POST",
                                    headers={"Content-Type": "application/json",
                                             "Authorization": f"Bearer {token}"})  # fmt: skip
    try:
        with urllib.request.urlopen(pedido, timeout=10) as respuesta:
            return respuesta.status, respuesta.read()
    except urllib.error.HTTPError as exc:
        return exc.code, exc.read()


def test_relevo_agentes_fijos_streaming_y_autorizacion() -> None:
    _GatewayFalso.recibidos = []
    gateway = ThreadingHTTPServer(("127.0.0.1", 0), _GatewayFalso)
    puerto_gateway = _levantar(gateway)
    servidor = relevo.servidor("127.0.0.1", 0, "token-relevo", "token-gateway", f"http://127.0.0.1:{puerto_gateway}")
    base = f"http://127.0.0.1:{_levantar(servidor)}"
    try:
        assert _post(base + "/v1/turno", {"conversacion": "M-S4.3-abc123", "mensaje": "hola"}, "malo")[0] == 401
        assert _post(base + "/v1/turno", {"conversacion": "M-S4.3-abc123", "mensaje": "hola", "model": "x"},
                     "token-relevo")[0] == 400  # fmt: skip
        codigo, cuerpo = _post(base + "/v1/turno", {"conversacion": "M-S4.3-abc123", "mensaje": "hola"}, "token-relevo")
        assert codigo == 200 and b"Hola" in cuerpo
        chat = _GatewayFalso.recibidos[0]
        assert chat["cuerpo"]["model"] == "openclaw/mesa-chat" and chat["cuerpo"]["user"] == "conv:M-S4.3-abc123"
        assert chat["auth"] == "Bearer token-gateway"
        assert _post(base + "/v1/trabajo", {"tipo": "OTRO"}, "token-relevo")[0] == 400
        codigo, cuerpo = _post(base + "/v1/trabajo", {"tipo": "ANALISIS"}, "token-relevo")
        assert codigo == 202 and json.loads(cuerpo)["agente"] == "mesa-analisis"
        for _ in range(50):
            if len(_GatewayFalso.recibidos) == 2:
                break
            time.sleep(0.05)
        trabajo = _GatewayFalso.recibidos[1]["cuerpo"]
        assert trabajo["model"] == "openclaw/mesa-analisis" and trabajo["stream"] is False
        assert trabajo["user"].startswith("trabajo:analisis:")
    finally:
        servidor.shutdown()
        gateway.shutdown()
    with pytest.raises(SystemExit):
        relevo.servidor("0.0.0.0", 0, "a", "b")
    with pytest.raises(SystemExit):
        relevo.servidor("127.0.0.1", 0, "a", "b", "http://10.0.0.5:18789")
