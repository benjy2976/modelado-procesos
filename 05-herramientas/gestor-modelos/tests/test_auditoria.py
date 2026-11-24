"""Inventario, registro e informe de auditoría y anclaje de citas en PDF sintéticos."""

import json
from pathlib import Path

import pytest
from test_fuentes_consulta import _biblioteca

from mesa_modelamiento.auditoria import carpeta_auditoria, eventos, inventariar_elementos, registrar
from mesa_modelamiento.auditoria_informe import informe
from mesa_modelamiento.fuentes_anclaje import anclar, rectangulo_valido, verificar_anclas
from mesa_modelamiento.fuentes_busqueda import buscar, indexar
from mesa_modelamiento.fuentes_fragmentos import segmentar
from mesa_modelamiento.repositorio import ErrorDominio

TABLA = """# S4.3.2.7 Prueba

## Pools

| Pool | Carriles |
| --- | --- |
| Entidad | Area usuaria; Autoridad |
| Supervisor | Supervisor |

## Elementos

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Clase | Fuente |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | Entidad | Area usuaria | inicio | Necesidad | T1 | PROP | DEC |
| T1 | 2 | Entidad | Area usuaria | tarea | Sustentar reduccion | G1 | NORM | Art. 2 |
| G1 | 3 | Entidad | Autoridad | compuerta | ¿Procede? | F1 [Si]; F0 [No] | PROP | DEC |
| F1 | 4 | Entidad | Autoridad | fin | Reducida |  | PROP | DEC |
| F0 | 5 | Entidad | Autoridad | fin | Pendiente |  | PROP | DEC |

## Mensajes

| Desde | Hacia | Nombre |
| --- | --- | --- |
| T1 | F1 | Aviso |
"""


def _pdf(lineas: list[str]) -> bytes:
    """PDF de una página con un renglón Helvetica por elemento, legible por pdfminer."""
    flujo = "BT /F1 12 Tf 72 700 Td 14 TL " + " ".join(f"({t}) Tj T*" for t in lineas) + " ET"
    objetos = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R "
        "/Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(flujo)} >>\nstream\n{flujo}\nendstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    salida, posiciones = "%PDF-1.4\n", []
    for numero, objeto in enumerate(objetos, 1):
        posiciones.append(len(salida))
        salida += f"{numero} 0 obj\n{objeto}\nendobj\n"
    inicio = len(salida)
    salida += f"xref\n0 {len(objetos) + 1}\n0000000000 65535 f \n"
    salida += "".join(f"{p:010d} 00000 n \n" for p in posiciones)
    salida += f"trailer\n<< /Size {len(objetos) + 1} /Root 1 0 R >>\nstartxref\n{inicio}\n%%EOF\n"
    return salida.encode("latin-1")


def test_anclar_renglones_guion_y_estados(tmp_path: Path) -> None:
    ruta = "01-referencias/04-contrataciones-publicas/prueba.pdf"
    archivo = tmp_path / ruta
    archivo.parent.mkdir(parents=True)
    archivo.write_bytes(_pdf(["Primera linea del texto.", "La reduccion implica una dismi-", "nucion del monto."]))
    uno = anclar(tmp_path, ruta, 1, "primera linea del texto")
    assert uno["estado"] == "ANCLADO" and len(uno["rectangulos"]) == 1 and rectangulo_valido(uno["rectangulos"][0])
    x0, y0, x1, y1 = uno["rectangulos"][0]
    assert 0.11 < x0 < 0.13 and 0.08 < y0 < 0.13 and y1 - y0 < 0.03
    dos = anclar(tmp_path, ruta, 1, "implica una disminución del monto")
    assert dos["estado"] == "ANCLADO" and len(dos["rectangulos"]) == 2
    assert dos["rectangulos"][0][1] < dos["rectangulos"][1][1]
    assert anclar(tmp_path, ruta, 1, "texto ausente")["estado"] == "CITA-NO-HALLADA"
    assert anclar(tmp_path, ruta, 2, "primera")["estado"] == "PAGINA-INEXISTENTE"
    assert anclar(tmp_path, ruta, 1, "primera", sha256="0" * 64)["estado"] == "HASH-DISTINTO"
    with pytest.raises(ErrorDominio):
        anclar(tmp_path, "02-procesos/otro.pdf", 1, "x")
    assert not rectangulo_valido([0.5, 0.2, 0.4, 0.3]) and not rectangulo_valido([0, 0, 1.2, 1])

    visor = tmp_path / "fuentes-visor.json"
    base = {"ruta": ruta, "sha256": uno["sha256"], "pagina": 1}
    visor.write_text(json.dumps({"elementos": {
        "T1": [{**base, "rectangulos": uno["rectangulos"]}, {**base, "pagina": 3, "rectangulos": uno["rectangulos"]}],
        "T2": [{**base, "rectangulos": [[0.5, 0.2, 0.4, 0.3]]}, {**base, "sha256": "0" * 64, "rectangulos": []}],
    }}), encoding="utf-8")  # fmt: skip
    estados = [a["estado"] for a in verificar_anclas(tmp_path, visor)]
    assert estados == ["VIGENTE", "PAGINA-INEXISTENTE", "RECTANGULO-INVALIDO", "HASH-DISTINTO"]


def _proceso(raiz: Path) -> Path:
    _biblioteca(raiz)
    carpeta = raiz / "02-procesos" / "S4-3-2-7-gestion-reducciones"
    tabla = carpeta / "S4-3-2-7-diagrama-proceso-tabla.md"
    tabla.write_text(TABLA, encoding="utf-8")
    original = raiz / "01-referencias/04-contrataciones-publicas/NOR-001/norma.pdf"
    original.parent.mkdir(parents=True, exist_ok=True)
    original.write_bytes(b"norma")  # Sus bytes producen el hash registrado por la biblioteca sintética.
    segmentar(raiz)
    indexar(raiz)
    return tabla


def test_inventario_registro_idempotente_e_informe(tmp_path: Path) -> None:
    tabla = _proceso(tmp_path)
    inventario = inventariar_elementos(tmp_path, "S4.3.2.7")
    assert inventario["por_clase"] == {"carril": 3, "elemento": 5, "flujo": 4, "mensaje": 1}
    fragmento = buscar(tmp_path, "adenda")["resultados"][0]["id"]
    entrada = {"elemento": "T1", "aspecto": "accion", "afirmacion": "La reducción no requiere adenda.",
               "resultado": "SUSTENTADA", "clase": "EXIGENCIA-NORMATIVA", "razonamiento": "El 2.2 lo dice.",
               "fuentes": [{"fragmento": fragmento, "cita": "No se requiere adenda"}]}  # fmt: skip
    assert registrar(tmp_path, "S4.3.2.7", [entrada])["registrados"] == 1
    assert registrar(tmp_path, "S4.3.2.7", [entrada])["repetidos"] == 1
    cambio = registrar(tmp_path, "S4.3.2.7", [{**entrada, "resultado": "INFERENCIA"}])
    assert cambio["rectificaciones"] == 1 and len(eventos(tmp_path, "S4.3.2.7")) == 2

    malos = [
        {**entrada, "elemento": "T9"},
        {**entrada, "fuentes": [{"fragmento": fragmento, "cita": "texto que no está"}]},
        {**entrada, "resultado": "VALIDADO"},
        {**entrada, "resultado": "CONTRADICCION", "fuentes": []},
    ]
    with pytest.raises(ErrorDominio) as error:
        registrar(tmp_path, "S4.3.2.7", malos)
    for codigo in ("ID-AUSENTE", "CITA-INVALIDA", "RESULTADO", "SIN-FUENTE"):
        assert codigo in str(error.value)
    assert len(eventos(tmp_path, "S4.3.2.7")) == 2

    parcial = informe(tmp_path, "S4.3.2.7")
    assert not parcial["ok"] and parcial["sin_resultado"] == ["E1", "G1", "F1", "F0", "M:T1>F1"]
    resto = [{**entrada, "elemento": e, "resultado": "INFERENCIA", "fuentes": [], "afirmacion": f"Paso {e}"}
             for e in ("E1", "G1", "F1", "F0", "M:T1>F1")]  # fmt: skip
    registrar(tmp_path, "S4.3.2.7", resto)
    completo = informe(tmp_path, "S4.3.2.7")
    assert completo["ok"] and completo["resultados"] == {"INFERENCIA": 6}
    texto = (tmp_path / completo["informe"]).read_text(encoding="utf-8")
    assert "| T1 | accion | `INFERENCIA` |" in texto and "tags:" in texto

    tabla.write_text(TABLA.replace("Necesidad", "Necesidad recibida"), encoding="utf-8")
    with pytest.raises(ErrorDominio):
        registrar(tmp_path, "S4.3.2.7", [entrada])
    assert informe(tmp_path, "S4.3.2.7")["inventario_desactualizado"]
    assert carpeta_auditoria(tmp_path, "S4.3.2.7").name == "S4-3-2-7"
