"""Regresión del vínculo estable entre elementos BPMN y observaciones."""
import importlib.util
import json
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from visor_datos import datos_visor


RUTA = Path(__file__).with_name("servidor_revision.py")
spec = importlib.util.spec_from_file_location("servidor_revision", RUTA)
modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(modulo)


class RevisionLocal(unittest.TestCase):
    def test_subproceso_enlaza_al_diagrama_o_indice_del_hijo(self):
        with tempfile.TemporaryDirectory() as carpeta:
            raiz = Path(carpeta)
            padre = raiz / "02-procesos" / "S4-padre"
            hijo = padre / "S4-3-hijo"
            hijo.mkdir(parents=True)
            tabla = padre / "S4-diagrama-proceso-tabla.md"
            html = padre / "S4-diagrama-proceso.html"
            tabla.write_text(
                "codigo_proceso: S4\n\n## Elementos\n\n"
                "| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente |\n"
                "|---|---|---|---|---|---|---|\n"
                "| H1 | 1 | P | C | subproceso | S4.3 Ejecucion | |\n",
                encoding="utf-8",
            )
            indice = hijo / "00-S4-3-hijo.md"
            indice.write_text("# Hijo\n", encoding="utf-8")
            nodo = next(iter(datos_visor(tabla, html, raiz)["elementos"].values()))
            self.assertEqual(nodo["destino_tipo"], "indice")
            (hijo / "S4-3-diagrama-proceso.html").write_text("", encoding="utf-8")
            nodo = next(iter(datos_visor(tabla, html, raiz)["elementos"].values()))
            self.assertEqual(nodo["destino_tipo"], "diagrama")
            self.assertTrue(nodo["destino"].endswith("/S4-3-diagrama-proceso.html"))

    def test_guardar_y_resolver_observacion_de_elemento(self):
        with tempfile.TemporaryDirectory() as carpeta:
            raiz = Path(carpeta)
            proceso = raiz / "02-procesos" / "S4-prueba"
            proceso.mkdir(parents=True)
            html = proceso / "X-diagrama-proceso.html"
            html.write_text("<html></html>", encoding="utf-8")
            html.with_suffix(".bpmn").write_text(
                '<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL">'
                '<task id="T1"/></definitions>', encoding="utf-8"
            )
            with patch.object(modulo, "RAIZ", raiz):
                self.assertEqual(modulo.modelo_valido("02-procesos/S4-prueba/X-diagrama-proceso.html"), html.resolve())
                servidor = ThreadingHTTPServer(("127.0.0.1", 0), modulo.Manejador)
                hilo = threading.Thread(target=servidor.serve_forever, daemon=True)
                hilo.start()
                try:
                    base = f"http://127.0.0.1:{servidor.server_port}"
                    modelo = "02-procesos/S4-prueba/X-diagrama-proceso.html"
                    with urlopen(base + "/") as respuesta:
                        self.assertIn(modelo, respuesta.read().decode("utf-8"))
                    with urlopen(base + "/api/arbol") as respuesta:
                        arbol = json.load(respuesta)
                        self.assertEqual(arbol["hijos"][0]["codigo"], "S4")
                        self.assertEqual(arbol["hijos"][0]["modelo"], "/" + modelo)
                    fuente = raiz / "03-conocimiento" / "fuentes" / "prueba.md"
                    fuente.parent.mkdir(parents=True)
                    fuente.write_text("---\ntipo: prueba\n---\n# Titulo\n\nAntes. Pasaje verificable. Despues.\n\n| A | B |\n|---|---|\n| 1 | 2 |\n", encoding="utf-8")
                    with urlopen(base + "/ver-fuente?ruta=03-conocimiento/fuentes/prueba.md&fragmento=Pasaje%20verificable") as respuesta:
                        pagina = respuesta.read().decode("utf-8")
                        self.assertIn("markdown-it.umd.min.js", pagina)
                        self.assertIn("<pre>tipo: prueba</pre>", pagina)
                        self.assertIn('id="contenido"', pagina)
                        self.assertIn("Pasaje verificable", pagina)
                    tabla = proceso / "X-diagrama-proceso-tabla.md"
                    tabla.write_text("# Tabla de prueba\n", encoding="utf-8")
                    with urlopen(base + "/ver-fuente?ruta=02-procesos/S4-prueba/X-diagrama-proceso-tabla.md") as respuesta:
                        self.assertIn("# Tabla de prueba", respuesta.read().decode("utf-8"))
                        self.assertIn("text/html", respuesta.headers["Content-Type"])
                    with self.assertRaises(HTTPError) as denegado:
                        urlopen(base + "/ver-fuente?ruta=../../estado-del-proyecto.md")
                    self.assertEqual(denegado.exception.code, 400)
                    def pedir(metodo, datos):
                        peticion = Request(
                            base + "/api/observaciones",
                            json.dumps(datos).encode("utf-8"),
                            {"Content-Type": "application/json"}, method=metodo
                        )
                        try:
                            with urlopen(peticion) as respuesta:
                                return respuesta.status, json.load(respuesta)
                        except HTTPError as error:
                            self.fail(f"HTTP {error.code}: {error.read().decode('utf-8')}")
                    estado, obs = pedir("POST", {
                        "modelo": modelo, "elemento": "T1", "referencia": "7",
                        "texto": "Corregir esta actividad", "autor": "Equipo"
                    })
                    self.assertEqual(estado, 201)
                    self.assertEqual(obs["estado"], "ABIERTA")
                    with urlopen(base + "/api/observaciones?modelo=" + modelo) as respuesta:
                        self.assertEqual(len(json.load(respuesta)["observaciones"]), 1)
                    estado, obs = pedir("PATCH", {"modelo": modelo, "id": obs["id"], "estado": "RESUELTA"})
                    self.assertEqual((estado, obs["estado"]), (200, "RESUELTA"))
                    guardado = json.loads(modulo.archivo_observaciones(html).read_text(encoding="utf-8"))
                    self.assertEqual(guardado["observaciones"][0]["elemento"], "T1")
                finally:
                    servidor.shutdown()
                    servidor.server_close()
                    hilo.join()


if __name__ == "__main__":
    unittest.main()
