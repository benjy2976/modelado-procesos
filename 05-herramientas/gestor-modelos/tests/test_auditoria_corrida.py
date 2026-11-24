"""Corrida por alcance y contraste de interfaces con un árbol sintético."""

from pathlib import Path

from mesa_modelamiento.auditoria_corrida import correr
from mesa_modelamiento.auditoria_interfaces import comparar_interfaces

ENCABEZADO = (
    "| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Documentos |\n|---|---|---|---|---|---|---|---|\n"
)


def _tabla(carpeta: Path, prefijo: str, filas: list[str], mensajes: list[str] = ()) -> Path:
    carpeta.mkdir(parents=True, exist_ok=True)
    texto = "# Modelo\n\n## Pools\n\n| Pool | Carriles |\n|---|---|\n| P | C |\n\n## Elementos\n\n" + ENCABEZADO
    texto += "".join(f"| {f} |\n" for f in filas)
    texto += "\n## Mensajes\n\n| Desde | Hacia | Nombre |\n|---|---|---|\n" + "".join(f"| {m} |\n" for m in mensajes)
    ruta = carpeta / f"{prefijo}-diagrama-proceso-tabla.md"
    ruta.write_text(texto, encoding="utf-8")
    return ruta


def _arbol(raiz: Path) -> dict[str, Path]:
    base = raiz / "02-procesos" / "S4-3-ejecucion"
    padre = _tabla(base, "S4-3", [
        "E-1 | 1 | P | C | inicio | Inicio | S-1 | ",
        "S-1 | 2 | P | C | subproceso | S4.3.1 Inicio de ejecucion | S-2 | sale: Acta de inicio de obra",
        "S-2 | 3 | P | C | subproceso | S4.3.2 Ejecucion | S-3 | ",
        "S-3 | 4 | P | C | subproceso | S4.3.3 Recepcion | F-1 | ",
        "F-1 | 5 | P | C | fin | Fin |  | ",
    ])  # fmt: skip
    hijo1 = _tabla(base / "S4-3-1-inicio", "S4-3-1", [
        "E1 | 1 | P | C | inicio | Contrato suscrito | F1 | ",
        "F1 | 2 | P | C | fin-mensaje | Plazo comunicado |  | ",
    ])  # fmt: skip
    _tabla(base / "S4-3-2-ejecucion", "S4-3-2", [
        "E-1 | 1 | P | C | inicio-mensaje | Acta de obra recibida | T-1 | ",
        "T-1 | 2 | P | C | tarea | Ejecutar | F-1 | ",
        "F-1 | 3 | P | C | fin | Obra culminada |  | ",
        "CP | 4 | P | C | subproceso-evento-temporizador | S4.3.2.1 Control periodico |  | ",
    ], ["S4.3.1 Inicio de ejecucion | E-1 | Acta de inicio"])  # fmt: skip
    _tabla(base / "S4-3-2-ejecucion" / "S4-3-2-1-control", "S4-3-2-1", [
        "E-1 | 1 | P | C | inicio-mensaje | Valorizacion recibida | F-1 | ",
        "F-1 | 2 | P | C | fin | Valorizacion remitida |  | ",
    ])  # fmt: skip
    (base / "S4-3-2-ejecucion" / "S4-3-2-9-otro").mkdir()
    (base / "S4-3-3-recepcion").mkdir()
    return {"padre": padre, "hijo1": hijo1}


def test_interfaces_detectan_cada_tipo_de_candidato(tmp_path: Path) -> None:
    _arbol(tmp_path)
    s43 = comparar_interfaces(tmp_path, "S4.3")
    tipos = {(c["tipo"], c["hijo"]) for c in s43["candidatos"]}
    assert ("SALIDA-NO-REPRESENTADA", "S4.3.1") in tipos
    assert ("HIJO-SIN-MODELO", "S4.3.3") in tipos
    assert ("SECUENCIA-SIN-CORRESPONDENCIA", "S4.3.2") in tipos
    assert ("MENSAJE-SIN-CONTRAPARTE", "S4.3.2") in tipos
    s432 = {(c["tipo"], c["hijo"]) for c in comparar_interfaces(tmp_path, "S4.3.2")["candidatos"]}
    assert s432 == {("TIPO-DE-DISPARO", "S4.3.2.1"), ("HIJO-SIN-ELEMENTO", "S4.3.2.9")}
    assert (tmp_path / "05-herramientas/gestor-modelos/auditorias/S4-3/interfaces.json").is_file()
    from mesa_modelamiento.auditoria import cargar_inventario, inventariar_elementos

    inventariar_elementos(tmp_path, "S4.3")
    flujos = {i["id"] for i in cargar_inventario(tmp_path, "S4.3")["items"] if i["clase"] == "flujo"}
    assert flujos == {"F:E-1>S-1", "F:S-1>S-2", "F:S-2>S-3", "F:S-3>F-1"}


def test_corrida_reanudable_y_cambio_de_tabla(tmp_path: Path) -> None:
    rutas = _arbol(tmp_path)
    parcial = correr(tmp_path, "S4.3", max_procesos=2)
    assert parcial["procesados"] == 2 and set(parcial["procesos"]) == {"S4.3", "S4.3.1"}
    completa = correr(tmp_path, "S4.3")
    assert completa["procesados"] == 6
    assert completa["estados"] == {"PENDIENTE-AUDITORIA": 4, "SIN-MODELO": 2}
    assert completa["procesos"]["S4.3"]["candidatos_interfaz"] >= 4
    resumen = (tmp_path / completa["manifiesto"]).with_suffix(".md").read_text(encoding="utf-8")
    assert "| S4.3.3 | `SIN-MODELO`" in resumen and "[ver](S4-3-1/informe.md)" in resumen
    rutas["hijo1"].write_text(rutas["hijo1"].read_text(encoding="utf-8").replace("Plazo", "Acta"), encoding="utf-8")
    assert correr(tmp_path, "S4.3")["procesos"]["S4.3.1"]["estado"] == "DESACTUALIZADO"
