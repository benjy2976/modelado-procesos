"""Inventario y diagnóstico reproducible de PDF de la biblioteca documental."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import time
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from pypdf import PdfReader

from .repositorio import ErrorDominio

REFERENCIAS = Path("01-referencias")
MANIFIESTO = REFERENCIAS / "09-derivados-texto" / "cache" / "preparacion-pdf.json"
UMBRAL_TEXTO = 80
ID_VALIDO = re.compile(r"[A-Za-z][A-Za-z0-9-]*\Z")


def _marca_tiempo() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _sha256(ruta: Path) -> str:
    resumen = hashlib.sha256()
    with ruta.open("rb") as archivo:
        for bloque in iter(lambda: archivo.read(1024 * 1024), b""):
            resumen.update(bloque)
    return resumen.hexdigest().upper()


def _guardar(ruta: Path, datos: dict) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_suffix(".tmp")
    temporal.write_text(json.dumps(datos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for intento in range(10):
        try:
            temporal.replace(ruta)
            break
        except PermissionError:
            if intento == 9:
                raise
            time.sleep(0.1)


def _cargar(raiz: Path) -> dict:
    ruta = raiz / MANIFIESTO
    if not ruta.is_file():
        raise ErrorDominio("Falta el manifiesto; ejecute 'fuentes inventariar' primero")
    return json.loads(ruta.read_text(encoding="utf-8"))


def _registros_csv(ruta: Path) -> list[dict[str, str]]:
    if not ruta.is_file():
        return []
    with ruta.open(encoding="utf-8-sig", newline="") as archivo:
        return list(csv.DictReader(archivo))


def _catalogo(raiz: Path) -> tuple[dict[str, dict], list[dict]]:
    directorio = raiz / REFERENCIAS / "00-catalogo"
    documentos = _registros_csv(directorio / "catalogo-documental.csv")
    descargas = _registros_csv(directorio / "registro-descargas.csv")
    indice: dict[str, dict] = {}
    for fila in descargas:
        ruta = fila.get("archivo", "").replace("\\", "/")
        if ruta and ruta not in indice:
            indice[ruta] = {
                "id": fila.get("id_fuente", ""),
                "url": fila.get("url_final") or fila.get("url_solicitada") or "",
                "sha256_registrado": fila.get("sha256", ""),
                "origen": "registro-descargas",
            }
    for fila in documentos:
        ruta = fila.get("ubicacion", "").replace("\\", "/")
        if ruta:
            previo = indice.get(ruta, {})
            indice[ruta] = {
                "id": fila.get("id") or previo.get("id", ""),
                "url": fila.get("fuente_url") or previo.get("url", ""),
                "sha256_registrado": fila.get("sha256") or previo.get("sha256_registrado", ""),
                "origen": "catalogo-documental",
                "titulo": fila.get("titulo", ""),
                "vigencia": fila.get("vigencia", ""),
            }
    return indice, documentos


def inventariar(raiz: Path) -> dict:
    """Reconcilia PDF presentes con el catálogo sin modificar los originales."""
    raiz = raiz.resolve()
    indice, documentos = _catalogo(raiz)
    anterior = {}
    if (raiz / MANIFIESTO).is_file():
        anterior = _cargar(raiz).get("documentos", {})
    encontrados: dict[str, dict] = {}
    for ruta in sorted((raiz / REFERENCIAS).rglob("*.pdf")):
        relativa = ruta.relative_to(raiz).as_posix()
        if relativa.startswith("01-referencias/09-derivados-texto/"):
            continue
        sha = _sha256(ruta)
        ficha = indice.get(relativa, {})
        identificador = ficha.get("id") or f"PENDIENTE-{sha[:12]}"
        previo = anterior.get(relativa, {})
        dato = {
            "id": identificador,
            "ruta": relativa,
            "sha256": sha,
            "bytes": ruta.stat().st_size,
            "catalogado": relativa in indice,
            "hash_coincide": not ficha.get("sha256_registrado") or sha == ficha["sha256_registrado"].upper(),
            "url": ficha.get("url", ""),
            "origen_registro": ficha.get("origen", ""),
            "titulo": ficha.get("titulo", ""),
            "vigencia": ficha.get("vigencia", ""),
        }
        if previo.get("sha256") == sha:
            for clave in (
                "diagnostico",
                "plan",
                "extraccion",
                "prioridad",
                "ocr_lotes",
                "ocr_estado",
                "ocr_baja_confianza",
                "evaluacion_extraccion",
                "cotejo_candidatos",
                "extraccion_error",
            ):
                if clave in previo:
                    dato[clave] = previo[clave]
        encontrados[relativa] = dato
    hashes: dict[str, list[str]] = defaultdict(list)
    for relativa, dato in encontrados.items():
        hashes[dato["sha256"]].append(relativa)
    faltantes = sorted(ruta for ruta in indice if ruta.lower().endswith(".pdf") and ruta not in encontrados)
    manifiesto = {
        "esquema": "preparacion-pdf-v1",
        "actualizado": _marca_tiempo(),
        "umbral_texto": UMBRAL_TEXTO,
        "documentos": encontrados,
        "faltantes_catalogo": faltantes,
        "duplicados_sha256": [rutas for rutas in hashes.values() if len(rutas) > 1],
    }
    _guardar(raiz / MANIFIESTO, manifiesto)
    return {
        "pdf_presentes": len(encontrados),
        "catalogados": sum(d["catalogado"] for d in encontrados.values()),
        "sin_catalogo": sum(not d["catalogado"] for d in encontrados.values()),
        "hash_distinto": sum(not d["hash_coincide"] for d in encontrados.values()),
        "faltantes_catalogo": len(faltantes),
        "duplicados_sha256": len(manifiesto["duplicados_sha256"]),
        "filas_catalogo_documental": len(documentos),
        "manifiesto": MANIFIESTO.as_posix(),
    }


def diagnosticar_texto(raiz: Path, max_documentos: int | None = None) -> dict:
    """Mide texto por página y conserva progreso después de cada PDF."""
    manifiesto = _cargar(raiz)
    procesados = 0
    errores = 0
    paginas = 0
    for dato in manifiesto["documentos"].values():
        if "diagnostico" in dato:
            continue
        if max_documentos is not None and procesados >= max_documentos:
            break
        try:
            lector = PdfReader(raiz / dato["ruta"], strict=False)
            medidas = []
            for pagina in lector.pages:
                try:
                    texto = pagina.extract_text() or ""
                    medidas.append({"caracteres": len(texto.strip()), "error": ""})
                except Exception as exc:  # El PDF de origen puede ser defectuoso.
                    medidas.append({"caracteres": 0, "error": type(exc).__name__})
            dato["diagnostico"] = {"paginas": medidas, "total": len(medidas), "error": ""}
            paginas += len(medidas)
        except Exception as exc:
            dato["diagnostico"] = {"paginas": [], "total": 0, "error": f"{type(exc).__name__}: {exc}"[:300]}
            errores += 1
        procesados += 1
        manifiesto["actualizado"] = _marca_tiempo()
        _guardar(raiz / MANIFIESTO, manifiesto)
    pendientes = sum("diagnostico" not in d for d in manifiesto["documentos"].values())
    return {"procesados": procesados, "paginas_medidas": paginas, "errores": errores, "pendientes": pendientes}


def planificar_extraccion(raiz: Path) -> dict:
    """Decide páginas nativas y candidatas a OCR por umbral explícito."""
    manifiesto = _cargar(raiz)
    conteo: Counter[str] = Counter()
    for dato in manifiesto["documentos"].values():
        diag = dato.get("diagnostico")
        if not diag:
            plan = {"estado": "PENDIENTE-DIAGNOSTICO", "nativas": [], "ocr": []}
        elif diag["error"] or not diag["paginas"]:
            plan = {"estado": "NO-CONFIABLE", "nativas": [], "ocr": []}
        else:
            nativas = [i for i, p in enumerate(diag["paginas"], 1) if p["caracteres"] >= UMBRAL_TEXTO]
            ocr = [i for i, p in enumerate(diag["paginas"], 1) if p["caracteres"] < UMBRAL_TEXTO]
            estado = "OCR-INTEGRAL" if not nativas else "OCR-PARCIAL" if ocr else "NATIVO"
            plan = {"estado": estado, "nativas": nativas, "ocr": ocr}
        dato["plan"] = plan
        conteo[plan["estado"]] += 1
    manifiesto["actualizado"] = _marca_tiempo()
    _guardar(raiz / MANIFIESTO, manifiesto)
    return {"estados": dict(sorted(conteo.items())), "manifiesto": MANIFIESTO.as_posix()}


def priorizar(raiz: Path, codigo: str) -> dict:
    """Marca fuentes citadas textualmente en tablas y sustentos del proceso."""
    if not re.fullmatch(r"S\d+(?:\.\d+)*", codigo):
        raise ErrorDominio("Código de proceso inválido")
    manifiesto = _cargar(raiz)
    procesos = raiz / "02-procesos"
    prefijo = codigo.replace(".", "-")
    textos = []
    for ruta in procesos.rglob("*.md"):
        if ruta.name.endswith(("-sustento.md", "-diagrama-proceso-tabla.md")) and prefijo in ruta.as_posix():
            textos.append(ruta.read_text(encoding="utf-8"))
    corpus = "\n".join(textos)
    citados = 0
    for dato in manifiesto["documentos"].values():
        identificador = dato["id"]
        dato["prioridad"] = "CITADA" if ID_VALIDO.fullmatch(identificador) and identificador in corpus else "BIBLIOTECA"
        citados += dato["prioridad"] == "CITADA"
    _guardar(raiz / MANIFIESTO, manifiesto)
    return {"codigo": codigo, "documentos_citados": citados, "textos_revisados": len(textos)}


def cargar_manifiesto(raiz: Path) -> dict:
    """Lee el estado local para otros servicios sin exponer rutas arbitrarias."""
    return _cargar(raiz)


def guardar_manifiesto(raiz: Path, datos: dict) -> None:
    """Persiste el estado local con reemplazo atómico."""
    datos["actualizado"] = _marca_tiempo()
    _guardar(raiz / MANIFIESTO, datos)
