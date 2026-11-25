"""Informe de auditoría: cobertura, resultados, citas vigentes y anclas del visor de un proceso."""

from __future__ import annotations

import json
import re
from collections import Counter
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from .auditoria import _tabla, cargar_cobertura, cargar_inventario, carpeta_auditoria, vigentes
from .fuentes_anclaje import verificar_anclas
from .fuentes_busqueda import _conectar
from .fuentes_preparacion import _sha256
from .repositorio import RepositorioProcesos

OBLIGATORIOS = {"elemento", "mensaje"}
MENCION = re.compile(r"\bart(?:[íi]culos?|s)?\.?\s*(\d+(?:\.\d+)?(?:\s*(?:,|y|-)\s*\d+(?:\.\d+)?)*)", re.I)


def _referencias_sin_ancla(tabla: Path, fuentes_visor: Path) -> list[dict]:
    """Elementos cuyo nombre, anotación o fuente mencionan un artículo que ninguna de sus anclas muestra."""
    anclas = (
        json.loads(fuentes_visor.read_text(encoding="utf-8")).get("elementos", {}) if fuentes_visor.is_file() else {}
    )
    hallazgos = []
    for fila in _tabla(tabla.read_text(encoding="utf-8"), "Elementos"):
        texto = " ".join(fila.get(c, "") for c in ("Nombre", "Anotacion", "Fuente"))
        mencionados = {
            int(n.split(".")[0]) for m in MENCION.finditer(texto) for n in re.findall(r"\d+(?:\.\d+)?", m.group(1))
        }
        ubicaciones = " ".join(a.get("ubicacion", "") for a in anclas.get(fila["ID"], []))
        anclados = {int(n) for n in re.findall(r"(?<![\d.])(\d+)(?:\.\d+)?", ubicaciones)}
        for articulo in sorted(mencionados - anclados):
            hallazgos.append({"elemento": fila["ID"], "articulo": articulo})
    return hallazgos


ENCABEZADO = """---
tipo: informe
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
fecha_actualizacion: {fecha}
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Informe de auditoría {codigo}

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe {codigo}`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.
"""


def _citas(raiz: Path, registros: list[dict]) -> list[dict]:
    """Citas cuyo fragmento ya no está en el índice o cuyo original cambió de hash."""
    if not any(r["fuentes"] for r in registros):
        return []
    base, _ = _conectar(raiz)
    problemas, hashes = [], {}
    with closing(base):
        for registro in registros:
            for fuente in registro["fuentes"]:
                if base.execute("SELECT 1 FROM fragmentos WHERE id = ?", (fuente["fragmento"],)).fetchone() is None:
                    problemas.append({"elemento": registro["elemento"], "fragmento": fuente["fragmento"],
                                      "estado": "FRAGMENTO-AUSENTE"})  # fmt: skip
                    continue
                archivo = raiz / fuente["ruta"]
                if fuente["ruta"] not in hashes:
                    hashes[fuente["ruta"]] = _sha256(archivo) if archivo.is_file() else ""
                if hashes[fuente["ruta"]] != fuente["sha256"]:
                    problemas.append({"elemento": registro["elemento"], "fragmento": fuente["fragmento"],
                                      "estado": "HASH-DISTINTO"})  # fmt: skip
    return problemas


def _ubicacion(fuente: dict) -> str:
    ubicacion = fuente["ubicacion"]
    lugar = f"p. {', '.join(map(str, ubicacion['paginas']))}" if "paginas" in ubicacion else ubicacion.get("tipo", "")
    return f"{Path(fuente['ruta']).stem[:48]} `{fuente['fragmento'].split(':')[1]}` ({lugar})"


def _markdown(codigo: str, datos: dict, items: list[dict], registros: list[dict]) -> str:
    lineas = [ENCABEZADO.format(codigo=codigo, fecha=datos["fecha"][:10])]
    resumen = ", ".join(f"{k}: {v}" for k, v in sorted(datos["resultados"].items()))
    lineas += [
        f"Revisión de la tabla: `{datos['revision_tabla'][:16]}`. Afirmaciones vigentes: {len(registros)} ({resumen}).",
        "", "## Afirmaciones por elemento", "",
        "| Elemento | Aspecto | Resultado | Afirmación | Fuentes |", "|---|---|---|---|---|",
    ]  # fmt: skip
    orden = {item["id"]: n for n, item in enumerate(items)}
    for r in sorted(registros, key=lambda r: (orden.get(r["elemento"], 999), r["aspecto"])):
        fuentes = "<br>".join(_ubicacion(f) for f in r["fuentes"]) or "—"
        lineas.append(f"| {r['elemento']} | {r['aspecto']} | `{r['resultado']}` | {r['afirmacion']} | {fuentes} |")
    secciones = (("Contradicciones", "CONTRADICCION"), ("Evidencia insuficiente", "EVIDENCIA-INSUFICIENTE"),
                 ("Inferencias", "INFERENCIA"))  # fmt: skip
    for titulo, resultado in secciones:
        seleccion = [r for r in registros if r["resultado"] == resultado]
        lineas += ["", f"## {titulo}", ""] + (
            [f"- **{r['elemento']} · {r['aspecto']}.** {r['razonamiento']}" for r in seleccion] or ["Ninguna."]
        )
    cobertura = datos["cobertura_fuente"]
    if cobertura:
        lineas += ["", "## Cobertura de la fuente", "", "| Obligación de la fuente | Estado | Elementos | Fuente |",
                   "|---|---|---|---|"]  # fmt: skip
        for c in cobertura:
            lineas.append(
                f"| {c['obligacion']} | `{c['estado']}` | {', '.join(c['elementos']) or '—'} | {_ubicacion(c)} |"
            )
    pendientes = ", ".join(datos["sin_resultado"]) or "ninguno"
    lineas += ["", "## Controles", "", f"- Elementos o mensajes sin resultado: {pendientes}.",
               f"- Citas con problemas: {len(datos['citas_con_problemas'])}.",
               f"- Referencias mencionadas sin ancla: {len(datos['referencias_sin_ancla'])}.",
               f"- Obligaciones de la fuente no representadas: {datos['no_representadas']}.",
               f"- Anclas del visor: {dict(Counter(a['estado'] for a in datos['anclas']))}."]  # fmt: skip
    return "\n".join(lineas) + "\n"


def informe(raiz: Path, codigo: str) -> dict:
    """Concilia inventario, registro, índice y anclas; escribe el informe Markdown del proceso."""
    raiz = raiz.resolve()
    inventario = cargar_inventario(raiz, codigo)
    rutas = RepositorioProcesos(raiz).rutas(codigo)
    registros = list(vigentes(raiz, codigo).values())
    con_resultado = {r["elemento"] for r in registros}
    items = inventario["items"]
    sin_resultado = [i["id"] for i in items if i["clase"] in OBLIGATORIOS and i["id"] not in con_resultado]
    visor = rutas["tabla"].parent / f"{codigo.replace('.', '-')}-fuentes-visor.json"
    anclas = verificar_anclas(raiz, visor)
    cobertura = cargar_cobertura(raiz, codigo)
    datos = {
        "codigo": codigo,
        "fecha": datetime.now(UTC).isoformat(timespec="seconds"),
        "revision_tabla": inventario["revision_tabla"],
        "inventario_desactualizado": _sha256(raiz / inventario["tabla"]) != inventario["revision_tabla"],
        "resultados_de_otra_revision": sum(r["revision_tabla"] != inventario["revision_tabla"] for r in registros),
        "afirmaciones": len(registros),
        "resultados": dict(Counter(r["resultado"] for r in registros)),
        "items": dict(Counter(i["clase"] for i in items)),
        "items_con_resultado": len(con_resultado & {i["id"] for i in items}),
        "sin_resultado": sin_resultado,
        "citas_con_problemas": _citas(raiz, registros),
        "anclas": anclas,
        "referencias_sin_ancla": _referencias_sin_ancla(rutas["tabla"], visor),
        "cobertura_fuente": cobertura["obligaciones"],
        "cobertura_de_otra_revision": bool(cobertura["obligaciones"])
        and cobertura.get("revision_tabla") != inventario["revision_tabla"],
        "no_representadas": sum(c["estado"] == "NO-REPRESENTADO" for c in cobertura["obligaciones"]),
    }
    datos["ok"] = not (
        sin_resultado or datos["citas_con_problemas"] or datos["inventario_desactualizado"]
        or any(a["estado"] not in ("VIGENTE", "SIN-COORDENADAS") for a in anclas) or datos["referencias_sin_ancla"]
        or datos["no_representadas"] or datos["cobertura_de_otra_revision"]
    )  # fmt: skip
    destino = carpeta_auditoria(raiz, codigo) / "informe.md"
    destino.write_text(_markdown(codigo, datos, items, registros), encoding="utf-8")
    return {**datos, "informe": destino.relative_to(raiz).as_posix()}
