"""Banco de preguntas de recuperación y métricas reproducibles sobre el índice local.

El banco declara pasajes esperados (casos positivos) o pasajes que no deben aparecer (casos
negativos). Medir no interpreta normas: solo indica si la búsqueda entrega los pasajes ya cotejados.
"""

from __future__ import annotations

import json
import re
import time
from collections import Counter
from contextlib import closing
from datetime import UTC, datetime
from pathlib import Path

from .fuentes_busqueda import _conectar, buscar
from .fuentes_extraccion import BASE
from .fuentes_preparacion import _guardar, _sha256
from .fuentes_temas import terminos_de
from .repositorio import ErrorDominio

BANCOS = Path("05-herramientas/gestor-modelos/bancos-prueba")
RESULTADOS = BASE / "pruebas"
CORTES = (1, 3, 5, 10)
TIPOS = {"POSITIVA", "NEGATIVA"}
CARACTERES_POR_TOKEN = 4  # Estimación gruesa para comparar costos entre variantes, no para facturar.


def _ruta_banco(raiz: Path, nombre: str) -> Path:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]*", nombre):
        raise ErrorDominio("Nombre de banco inválido")
    ruta = raiz / BANCOS / f"{nombre}.json"
    if not ruta.is_file():
        raise ErrorDominio(f"Banco inexistente: {nombre}", 404)
    return ruta


def _resolver(base, referencia: dict) -> str | None:
    fila = base.execute(
        "SELECT id FROM fragmentos WHERE ruta = ? AND substr(id, instr(id, ':') + 1) = ?",
        (referencia["ruta"], referencia["clave"]),
    ).fetchone()
    return fila[0] if fila else None


def preparar(raiz: Path, nombre: str) -> dict:
    """Valida el banco y resuelve cada pasaje esperado a un fragmento vigente del índice."""
    raiz = raiz.resolve()
    banco = json.loads(_ruta_banco(raiz, nombre).read_text(encoding="utf-8"))
    hallazgos = []
    if banco.get("estado") in (None, "VALIDADO"):
        hallazgos.append({"codigo": "ESTADO", "detalle": "El banco declara un estado provisional, nunca VALIDADO"})
    identificadores = [p.get("id") for p in banco.get("preguntas", [])]
    for repetido in [i for i, n in Counter(identificadores).items() if n > 1]:
        hallazgos.append({"codigo": "ID-REPETIDO", "detalle": repetido})
    resueltas = []
    base, desactualizado = _conectar(raiz)
    with closing(base):
        for pregunta in banco.get("preguntas", []):
            if pregunta.get("tipo") not in TIPOS:
                hallazgos.append({"codigo": "TIPO", "detalle": pregunta.get("id")})
            if not (pregunta.get("consulta") or pregunta.get("tema") or pregunta.get("filtros")):
                hallazgos.append({"codigo": "CONSULTA-VACIA", "detalle": pregunta.get("id")})
            clave = "esperados" if pregunta.get("tipo") == "POSITIVA" else "no_esperados"
            referencias = pregunta.get(clave) or []
            if not referencias:
                hallazgos.append({"codigo": "SIN-REFERENCIAS", "detalle": f"{pregunta.get('id')}: falta {clave}"})
            fragmentos = []
            for referencia in referencias:
                fragmento = _resolver(base, referencia)
                if fragmento is None:
                    hallazgos.append({"codigo": "PASAJE-INEXISTENTE", "detalle": f"{pregunta.get('id')}: {referencia}"})
                fragmentos.append(fragmento)
            resueltas.append({**pregunta, "fragmentos": fragmentos})
    return {
        "banco": nombre,
        "preguntas": len(resueltas),
        "positivas": sum(p.get("tipo") == "POSITIVA" for p in resueltas),
        "negativas": sum(p.get("tipo") == "NEGATIVA" for p in resueltas),
        "hallazgos": hallazgos,
        "indice_desactualizado": desactualizado,
        "resueltas": resueltas,
    }


def _ejecutar(raiz: Path, pregunta: dict, limite: int, con_temas: bool, modo: str | None) -> tuple[list[str], int, int]:
    terminos: list[str] = []
    if con_temas and pregunta.get("tema"):
        terminos, _ = terminos_de(raiz, pregunta["tema"], pregunta.get("con_relacionados", False))
    inicio = time.perf_counter()
    resultado = buscar(
        raiz, pregunta.get("consulta", ""), modo=modo or pregunta.get("modo", "todas"), terminos=terminos,
        filtros=pregunta.get("filtros"), limite=limite, max_caracteres=10**9,
    )  # fmt: skip
    milisegundos = round((time.perf_counter() - inicio) * 1000)
    paquete = sum(len(r["extracto"]) for r in resultado["resultados"][:5])
    return [r["id"] for r in resultado["resultados"]], milisegundos, paquete


def medir(raiz: Path, nombre: str, con_temas: bool = True, limite: int = 10, modo: str | None = None) -> dict:
    """Ejecuta el banco y calcula aciertos por posición, MRR, limpieza de negativos, latencia y tamaño."""
    raiz = raiz.resolve()
    preparado = preparar(raiz, nombre)
    if preparado["hallazgos"]:
        raise ErrorDominio("El banco tiene hallazgos; ejecute 'fuentes pruebas preparar' y corríjalos")
    detalle, latencias, paquetes = [], [], []
    for pregunta in preparado["resueltas"]:
        obtenidos, milisegundos, paquete = _ejecutar(raiz, pregunta, limite, con_temas, modo)
        latencias.append(milisegundos)
        paquetes.append(paquete)
        posiciones = [obtenidos.index(f) + 1 for f in pregunta["fragmentos"] if f in obtenidos]
        fila = {
            "id": pregunta["id"],
            "tipo": pregunta["tipo"],
            "elemento": pregunta.get("elemento"),
            "ms": milisegundos,
        }
        if pregunta["tipo"] == "POSITIVA":
            fila["primera_posicion"] = min(posiciones) if posiciones else None
            fila["esperados_hallados"] = f"{len(posiciones)}/{len(pregunta['fragmentos'])}"
        else:
            fila["intrusos_top5"] = sum(p <= 5 for p in posiciones)
        detalle.append(fila)
    positivas = [d for d in detalle if d["tipo"] == "POSITIVA"]
    negativas = [d for d in detalle if d["tipo"] == "NEGATIVA"]
    metricas = {
        f"acierto@{k}": round(sum((d["primera_posicion"] or 99) <= k for d in positivas) / len(positivas), 3)
        for k in CORTES
        if positivas
    }
    if positivas:
        metricas["mrr"] = round(
            sum(1 / d["primera_posicion"] for d in positivas if d["primera_posicion"]) / len(positivas), 3
        )
    if negativas:
        metricas["negativas_limpias"] = round(sum(d["intrusos_top5"] == 0 for d in negativas) / len(negativas), 3)
    latencias.sort()
    resultado = {
        "banco": nombre,
        "variante": f"{modo or 'banco'}-{'temas' if con_temas else 'sin-temas'}",
        "fecha": datetime.now(UTC).isoformat(timespec="seconds"),
        "sha256_banco": _sha256(_ruta_banco(raiz, nombre)),
        "preguntas": len(detalle),
        "metricas": metricas,
        "latencia_ms": {"mediana": latencias[len(latencias) // 2], "maxima": latencias[-1]},
        "paquete_top5_caracteres_promedio": round(sum(paquetes) / len(paquetes)),
        "paquete_top5_tokens_estimados": round(sum(paquetes) / len(paquetes) / CARACTERES_POR_TOKEN),
        "detalle": detalle,
    }
    destino = raiz / RESULTADOS / f"{nombre}-{resultado['variante']}.json"
    _guardar(destino, resultado)
    return {**resultado, "archivo": destino.relative_to(raiz).as_posix()}
