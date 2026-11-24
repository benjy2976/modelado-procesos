"""Corrida reanudable de auditoría sobre todos los procesos de un alcance (p. ej. S4.3).

La corrida no audita por sí misma: inventaría, detecta tablas cambiadas, contrasta interfaces de los padres
y resume el estado de cada proceso para que la auditoría por afirmación avance de uno en uno.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from .auditoria import AUDITORIAS, cargar_inventario, inventariar_elementos
from .auditoria_informe import informe
from .auditoria_interfaces import comparar_interfaces
from .fuentes_preparacion import _guardar, _sha256
from .repositorio import ErrorDominio, RepositorioProcesos


def _procesos(arbol: dict, alcance: str) -> list[tuple[str, bool]]:
    """Códigos del alcance en orden de árbol (padre antes que hijos) y si cada uno tiene hijos."""
    salida: list[tuple[str, bool]] = []

    def recorrer(nodo: dict, dentro: bool) -> None:
        dentro = dentro or nodo.get("codigo") == alcance
        if dentro:
            salida.append((nodo["codigo"], bool(nodo.get("hijos"))))
        for hijo in nodo.get("hijos", []):
            recorrer(hijo, dentro)

    recorrer(arbol, False)
    if not salida:
        raise ErrorDominio(f"Alcance {alcance} no encontrado", 404)
    return salida


def _estado(raiz: Path, codigo: str, padre: bool) -> dict:
    repositorio = RepositorioProcesos(raiz)
    tabla = repositorio.rutas(codigo)["tabla"]
    if not tabla.is_file():
        return {"estado": "SIN-MODELO"}
    revision = _sha256(tabla)
    try:
        inventario = cargar_inventario(raiz, codigo)
    except ErrorDominio:
        inventariar_elementos(raiz, codigo)
        inventario = cargar_inventario(raiz, codigo)
    if inventario["revision_tabla"] != revision:
        detalle = "La tabla cambió después del inventario; reinventariar y reconfirmar afirmaciones"
        return {"estado": "DESACTUALIZADO", "revision_tabla": revision, "detalle": detalle}
    datos = informe(raiz, codigo)
    if not datos["afirmaciones"]:
        estado = "PENDIENTE-AUDITORIA"
    elif datos["sin_resultado"] or not datos["cobertura_fuente"]:
        estado = "EN-CURSO"
    else:  # Auditoría completa en ambas direcciones; los hallazgos abiertos esperan decisión.
        estado = "COMPLETO" if datos["ok"] else "CON-HALLAZGOS"
    resumen = {
        "estado": estado,
        "revision_tabla": revision,
        "afirmaciones": datos["afirmaciones"],
        "resultados": datos["resultados"],
        "sin_resultado": len(datos["sin_resultado"]),
        "obligaciones": len(datos["cobertura_fuente"]),
        "no_representadas": datos["no_representadas"],
        "referencias_sin_ancla": len(datos["referencias_sin_ancla"]),
        "citas_con_problemas": len(datos["citas_con_problemas"]),
    }
    if padre:
        resumen["candidatos_interfaz"] = comparar_interfaces(raiz, codigo)["total"]
    return resumen


def _resumen_markdown(alcance: str, procesos: dict) -> str:
    lineas = [
        "---", "tipo: informe", "area: herramientas", "estado_documento: BORRADOR", "clase_conocimiento: OBSERVADO",
        "confidencialidad: INTERNO", "tags:", "  - tema/automatizacion", "  - tema/procesos", "---", "",
        f"# Corrida de auditoría {alcance}", "",
        "Sube a: [Plan de corrida documental y auditoría](../docs/plan-corrida-documental-y-auditoria.md).", "",
        f"Generado por `modelador-procesos auditoria correr --alcance {alcance}`; no editar a mano. Los resultados son "
        "propuestas del agente que audita: no constituyen validación normativa ni conformidad institucional.", "",
        "| Proceso | Estado | Afirmaciones | Obligaciones de la fuente | Candidatos de interfaz | Informe |",
        "|---|---|---|---|---|---|",
    ]  # fmt: skip
    for codigo, dato in procesos.items():
        carpeta = codigo.replace(".", "-")
        enlace = f"[ver]({carpeta}/informe.md)" if dato["estado"] not in ("SIN-MODELO", "DESACTUALIZADO") else "—"
        resultados = ", ".join(f"{k} {v}" for k, v in sorted(dato.get("resultados", {}).items())) or "—"
        lineas.append(f"| {codigo} | `{dato['estado']}` | {dato.get('afirmaciones', 0)} ({resultados}) | "
                      f"{dato.get('obligaciones', 0)} (no representadas: {dato.get('no_representadas', 0)}) | "
                      f"{dato.get('candidatos_interfaz', '—')} | {enlace} |")  # fmt: skip
    return "\n".join(lineas) + "\n"


def correr(raiz: Path, alcance: str, max_procesos: int | None = None) -> dict:
    """Actualiza el estado de cada proceso del alcance y lo guarda tras cada uno (reanudable)."""
    raiz = raiz.resolve()
    destino = raiz / AUDITORIAS / f"corrida-{alcance.replace('.', '-')}.json"
    previo = json.loads(destino.read_text(encoding="utf-8")) if destino.is_file() else {"procesos": {}}
    manifiesto = {"alcance": alcance, "procesos": previo.get("procesos", {})}
    procesados = 0
    for codigo, padre in _procesos(RepositorioProcesos(raiz).arbol(), alcance):
        if max_procesos is not None and procesados >= max_procesos:
            break
        manifiesto["procesos"][codigo] = {**_estado(raiz, codigo, padre),
                                          "actualizado": datetime.now(UTC).isoformat(timespec="seconds")}  # fmt: skip
        procesados += 1
        manifiesto["actualizado"] = datetime.now(UTC).isoformat(timespec="seconds")
        _guardar(destino, manifiesto)
    destino.with_suffix(".md").write_text(_resumen_markdown(alcance, manifiesto["procesos"]), encoding="utf-8")
    estados: dict[str, int] = {}
    for dato in manifiesto["procesos"].values():
        estados[dato["estado"]] = estados.get(dato["estado"], 0) + 1
    return {"alcance": alcance, "procesados": procesados, "estados": estados,
            "procesos": manifiesto["procesos"], "manifiesto": destino.relative_to(raiz).as_posix()}  # fmt: skip
