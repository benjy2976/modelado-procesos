"""Inventario, registro e informe de auditoría y anclaje de citas en PDF sintéticos."""

import json
from pathlib import Path

import pytest
from test_fuentes_consulta import _biblioteca

from mesa_modelamiento.auditoria import carpeta_auditoria, eventos, inventariar_elementos, registrar
from mesa_modelamiento.auditoria_informe import informe
from mesa_modelamiento.fuentes_anclaje import anclar, anclar_entre_paginas, rectangulo_valido, verificar_anclas
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


def _pdf(lineas: list[str], *otras: list[str]) -> bytes:
    """PDF con una página por lista de renglones Helvetica, legible por pdfminer."""
    paginas = [lineas, *otras]
    fuente = 3 + 2 * len(paginas)
    objetos = ["<< /Type /Catalog /Pages 2 0 R >>",
               f"<< /Type /Pages /Kids [{' '.join(f'{3 + 2 * n} 0 R' for n in range(len(paginas)))}] "
               f"/Count {len(paginas)} >>"]  # fmt: skip
    for n, renglones in enumerate(paginas):
        flujo = "BT /F1 12 Tf 72 700 Td 14 TL " + " ".join(f"({t}) Tj T*" for t in renglones) + " ET"
        objetos += [
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents {4 + 2 * n} 0 R "
            f"/Resources << /Font << /F1 {fuente} 0 R >> >> >>",
            f"<< /Length {len(flujo)} >>\nstream\n{flujo}\nendstream",
        ]
    objetos.append("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
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
    assert anclar(tmp_path, ruta, 1, "primeralinea del  tex to")["estado"] == "ANCLADO"  # Espacios de composición.
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
        "T3": [{"ruta": ruta, "pagina": 1, "ubicacion": "sin coordenadas"}],
    }}), encoding="utf-8")  # fmt: skip
    estados = [a["estado"] for a in verificar_anclas(tmp_path, visor)]
    assert estados == ["VIGENTE", "PAGINA-INEXISTENTE", "RECTANGULO-INVALIDO", "HASH-DISTINTO", "SIN-COORDENADAS"]
    tramo = {"pagina": 1, "rol": "citado", "rectangulos": uno["rectangulos"]}
    visor.write_text(json.dumps({"elementos": {"T1": [
        {**base, "rectangulos": uno["rectangulos"], "tramos": [tramo, {**tramo, "rol": "antecedente"}]},
        {**base, "rectangulos": uno["rectangulos"], "tramos": [tramo, {**tramo, "pagina": 2}]},
    ]}}), encoding="utf-8")  # fmt: skip
    assert [a["estado"] for a in verificar_anclas(tmp_path, visor)] == ["VIGENTE", "PAGINA-INEXISTENTE"]


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
               "fuentes": [{"fragmento": fragmento, "cita": "No se requiere adenda", "ambito": "reducción en ejecución",
                            "relacion": "directa"}]}  # fmt: skip
    assert registrar(tmp_path, "S4.3.2.7", [entrada])["registrados"] == 1
    assert registrar(tmp_path, "S4.3.2.7", [entrada])["repetidos"] == 1
    cambio = registrar(tmp_path, "S4.3.2.7", [{**entrada, "resultado": "INFERENCIA"}])
    assert cambio["rectificaciones"] == 1 and len(eventos(tmp_path, "S4.3.2.7")) == 2

    malos = [
        {**entrada, "elemento": "T9"},
        {**entrada, "fuentes": [{"fragmento": fragmento, "cita": "texto que no está"}]},
        {**entrada, "resultado": "VALIDADO"},
        {**entrada, "resultado": "CONTRADICCION", "fuentes": []},
        {**entrada, "fuentes": [{**entrada["fuentes"][0], "relacion": "antecedente"}]},
        {**entrada, "fuentes": [{"fragmento": fragmento, "cita": "No se requiere adenda"}]},
    ]
    with pytest.raises(ErrorDominio) as error:
        registrar(tmp_path, "S4.3.2.7", malos)
    for codigo in ("ID-AUSENTE", "CITA-INVALIDA", "RESULTADO", "SIN-FUENTE", "SIN-FUENTE-DIRECTA", "CONTEXTO-CITA"):
        assert codigo in str(error.value)
    assert len(eventos(tmp_path, "S4.3.2.7")) == 2

    parcial = informe(tmp_path, "S4.3.2.7")
    assert not parcial["ok"] and parcial["sin_resultado"] == ["E1", "G1", "F1", "F0", "M:T1>F1"]
    resto = [{**entrada, "elemento": e, "resultado": "INFERENCIA", "fuentes": [], "afirmacion": f"Paso {e}"}
             for e in ("E1", "G1", "F1", "F0", "M:T1>F1")]  # fmt: skip
    registrar(tmp_path, "S4.3.2.7", resto)
    con_mencion = informe(tmp_path, "S4.3.2.7")
    assert con_mencion["referencias_sin_ancla"] == [{"elemento": "T1", "articulo": 2}] and not con_mencion["ok"]
    from mesa_modelamiento.auditoria import registrar_cobertura

    cobertura = [
        {"fragmento": fragmento, "cita": "No se requiere adenda", "obligacion": "Sin adenda", "estado": "REPRESENTADO",
         "elementos": ["T1"], "razonamiento": "T1 lo recoge."},
        {"fragmento": fragmento, "cita": "basta la publicación de la resolución", "obligacion": "Publicar",
         "estado": "NO-REPRESENTADO", "elementos": [], "razonamiento": "Falta."},
    ]  # fmt: skip
    resumen = registrar_cobertura(tmp_path, "S4.3.2.7", cobertura)
    assert resumen["por_estado"] == {"REPRESENTADO": 1, "NO-REPRESENTADO": 1}
    with pytest.raises(ErrorDominio):
        registrar_cobertura(tmp_path, "S4.3.2.7", [{**cobertura[0], "elementos": ["T9"]}])
    assert informe(tmp_path, "S4.3.2.7")["no_representadas"] == 1
    tabla.write_text(TABLA.replace("| NORM | Art. 2 |", "| NORM | DEC |"), encoding="utf-8")
    inventariar_elementos(tmp_path, "S4.3.2.7")
    registrar(tmp_path, "S4.3.2.7", [{**entrada, "resultado": "INFERENCIA"}, *resto])
    registrar_cobertura(tmp_path, "S4.3.2.7", [cobertura[0], {**cobertura[1], "estado": "FUERA-DE-ALCANCE"}])
    completo = informe(tmp_path, "S4.3.2.7")
    assert completo["ok"] and completo["resultados"] == {"INFERENCIA": 6} and not completo["referencias_sin_ancla"]
    texto = (tmp_path / completo["informe"]).read_text(encoding="utf-8")
    assert "| T1 | accion | `INFERENCIA` |" in texto and "tags:" in texto

    retirado = TABLA.replace("| NORM | Art. 2 |", "| NORM | DEC |").replace("F0", "FX")
    tabla.write_text(retirado, encoding="utf-8")
    inventariar_elementos(tmp_path, "S4.3.2.7")
    sin_f0 = informe(tmp_path, "S4.3.2.7")
    assert sin_f0["afirmaciones_de_elementos_retirados"] == ["F0"] and sin_f0["sin_resultado"] == ["FX"]
    assert sin_f0["afirmaciones"] == 5

    tabla.write_text(
        TABLA.replace("| NORM | Art. 2 |", "| NORM | DEC |").replace("Necesidad", "Nueva"), encoding="utf-8"
    )
    with pytest.raises(ErrorDominio):
        registrar(tmp_path, "S4.3.2.7", [entrada])
    assert informe(tmp_path, "S4.3.2.7")["inventario_desactualizado"]
    assert carpeta_auditoria(tmp_path, "S4.3.2.7").name == "S4-3-2-7"


def test_cita_que_cruza_el_salto_de_pagina(tmp_path: Path) -> None:
    ruta = "01-referencias/04-contrataciones-publicas/dos.pdf"
    archivo = tmp_path / ruta
    archivo.parent.mkdir(parents=True)
    archivo.write_bytes(_pdf(["Texto previo.", "La entidad puede reducir prestaciones hasta"],
                             ["por el mismo porcentaje del contrato.", "Otro numeral."]))  # fmt: skip
    cita = "puede reducir prestaciones hasta por el mismo porcentaje"
    assert anclar(tmp_path, ruta, 1, cita)["estado"] == "CITA-NO-HALLADA"
    cruzada = anclar_entre_paginas(tmp_path, ruta, [1, 2], cita)
    assert cruzada["estado"] == "ANCLADO" and [t["pagina"] for t in cruzada["tramos"]] == [1, 2]
    assert all(len(t["rectangulos"]) == 1 and t["rol"] == "citado" for t in cruzada["tramos"])
    assert anclar_entre_paginas(tmp_path, ruta, [1, 2], "texto que no existe en ninguna")["estado"] == "CITA-NO-HALLADA"
    assert anclar_entre_paginas(tmp_path, ruta, [1, 2], cita, sha256="0" * 64)["estado"] == "HASH-DISTINTO"


def test_reconfirmar_conserva_vigentes_y_rectifica_superadas(tmp_path: Path) -> None:
    from mesa_modelamiento.auditoria import cargar_cobertura, reconfirmar, registrar_cobertura, vigentes

    tabla = _proceso(tmp_path)
    inventariar_elementos(tmp_path, "S4.3.2.7")
    fragmento = buscar(tmp_path, "adenda")["resultados"][0]["id"]
    base = {"aspecto": "existencia", "resultado": "INFERENCIA", "clase": "DECISION-PROYECTO", "fuentes": [],
            "razonamiento": "Paso del modelo."}  # fmt: skip
    registrar(tmp_path, "S4.3.2.7", [{**base, "elemento": e, "afirmacion": f"Paso {e}"} for e in ("T1", "E1", "F0")])
    registrar_cobertura(tmp_path, "S4.3.2.7", [
        {"fragmento": fragmento, "cita": "No se requiere adenda", "obligacion": "Sin adenda",
         "estado": "NO-REPRESENTADO",
         "elementos": [], "razonamiento": "Falta."}])  # fmt: skip
    tabla.write_text(TABLA.replace("F0", "FX"), encoding="utf-8")
    with pytest.raises(ErrorDominio, match="motivo"):
        reconfirmar(tmp_path, "S4.3.2.7", [], motivo=" ")
    resultado = reconfirmar(
        tmp_path, "S4.3.2.7",
        [{**base, "elemento": "T1", "afirmacion": "Paso T1 revisado"}, {**base, "elemento": "FX", "afirmacion": "Fin"}],
        [{"fragmento": fragmento, "obligacion": "Sin adenda", "estado": "REPRESENTADO", "elementos": ["T1"],
          "razonamiento": "T1 lo recoge."},
         {"fragmento": fragmento, "cita": "basta la publicación de la resolución", "obligacion": "Publicar",
          "estado": "NO-REPRESENTADO", "elementos": [], "razonamiento": "Falta."}],
        motivo="Prueba de cambio de tabla",
    )  # fmt: skip
    assert resultado["conservadas"] == 1 and resultado["nuevas"] == 2 and resultado["superadas"] == 1
    assert resultado["descartadas_por_elemento_retirado"] == ["F0"] and resultado["obligaciones_nuevas"] == 1
    actuales = {(r["elemento"], r["afirmacion"]): r["resultado"] for r in vigentes(tmp_path, "S4.3.2.7").values()}
    assert actuales[("T1", "Paso T1")] == "NO-APLICA" and actuales[("T1", "Paso T1 revisado")] == "INFERENCIA"
    estados = [o["estado"] for o in cargar_cobertura(tmp_path, "S4.3.2.7")["obligaciones"]]
    assert estados == ["REPRESENTADO", "NO-REPRESENTADO"]
    with pytest.raises(ErrorDominio, match="ID-AUSENTE"):
        reconfirmar(tmp_path, "S4.3.2.7", [{**base, "elemento": "F0", "afirmacion": "x"}], motivo="Prueba")
