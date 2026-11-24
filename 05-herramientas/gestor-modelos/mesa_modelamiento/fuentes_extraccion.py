"""Extracción paginada de PDF y controles de calidad para la biblioteca local."""

from __future__ import annotations

import hashlib
import json
import logging
import re
from collections import Counter
from datetime import UTC, datetime
from html import escape
from pathlib import Path
from tempfile import TemporaryDirectory

from pypdf import PdfReader, PdfWriter

from .fuentes_preparacion import REFERENCIAS, _sha256, cargar_manifiesto, guardar_manifiesto
from .repositorio import ErrorDominio

logging.getLogger("pypdf").setLevel(logging.ERROR)
BASE = REFERENCIAS / "09-derivados-texto" / "cache"


def _destino(raiz: Path, dato: dict) -> Path:
    identificador = re.sub(r"[^A-Za-z0-9-]", "-", dato["id"])
    ruta_hash = hashlib.sha256(dato["ruta"].encode("utf-8")).hexdigest()[:8]
    return raiz / BASE / identificador / f"{dato['sha256'][:16].lower()}-{ruta_hash}.md"


def _carpeta_ocr(raiz: Path, dato: dict) -> Path:
    """Aísla páginas intermedias incluso cuando varios PDF comparten ID y hash."""
    return (raiz / dato["extraccion"]["ruta"]).with_suffix(".ocr")


def aislar_paginas_ocr(raiz: Path) -> dict:
    """Reconstruye sidecars únicos desde Markdown final ya verificado."""
    manifiesto = cargar_manifiesto(raiz)
    reconstruidas = 0
    for dato in manifiesto["documentos"].values():
        if dato.get("ocr_estado") != "COMPLETO":
            continue
        texto = (raiz / dato["extraccion"]["ruta"]).read_text(encoding="utf-8")
        partes = re.split(r"<!-- pagina_pdf: \d+; pagina_impresa: NO-DETERMINADA -->", texto)[1:]
        if len(partes) != dato["extraccion"]["paginas"]:
            raise ErrorDominio(f"Paginación inconsistente en {dato['id']}")
        carpeta = _carpeta_ocr(raiz, dato)
        carpeta.mkdir(parents=True, exist_ok=True)
        for numero, (metodo, cuerpo) in enumerate(zip(dato["extraccion"]["metodos"], partes, strict=True), 1):
            if metodo != "ocr":
                continue
            salida = carpeta / f"p{numero}.md"
            if not salida.is_file():
                salida.write_text(cuerpo.strip() + "\n", encoding="utf-8")
                reconstruidas += 1
    return {"paginas_ocr_aisladas": reconstruidas}


def resolver_colisiones_cache(raiz: Path) -> dict:
    """Separa derivados que compartían ID y hash aunque tenían rutas documentales distintas."""
    manifiesto = cargar_manifiesto(raiz)
    por_cache = {}
    for dato in manifiesto["documentos"].values():
        extraccion = dato.get("extraccion")
        if extraccion:
            por_cache.setdefault(extraccion["ruta"], []).append(dato)
    separados = 0
    for relativa, grupo in por_cache.items():
        if len(grupo) < 2:
            continue
        primera, resto = (raiz / relativa).read_text(encoding="utf-8").split("\n", 1)
        for dato in grupo:
            metadatos = json.loads(primera.removeprefix("<!-- metadatos: ").removesuffix(" -->"))
            metadatos["pdf_original"] = dato["ruta"]
            destino = _destino(raiz, dato)
            destino.parent.mkdir(parents=True, exist_ok=True)
            destino.write_text(
                "<!-- metadatos: " + json.dumps(metadatos, ensure_ascii=False) + " -->\n" + resto,
                encoding="utf-8",
            )
            dato["extraccion"]["ruta"] = destino.relative_to(raiz).as_posix()
            dato["extraccion"]["sha256_texto"] = _sha256(destino)
            separados += 1
    if separados:
        guardar_manifiesto(raiz, manifiesto)
    return {"derivados_separados": separados}


def _escribir(raiz: Path, dato: dict, paginas: list[str], metodos: list[str], estado: str) -> dict:
    encabezado = {
        "esquema": "texto-pdf-paginado-v1",
        "id_documento": dato["id"],
        "pdf_original": dato["ruta"],
        "sha256_original": dato["sha256"],
        "fuente_url": dato["url"],
        "metodo_por_pagina": metodos,
        "herramienta": "modelador-procesos/pypdf-6",
        "fecha_extraccion": datetime.now(UTC).isoformat(timespec="seconds"),
        "estado_calidad": estado,
        "pagina_impresa": "NO-DETERMINADA",
    }
    bloques = [f"<!-- metadatos: {json.dumps(encabezado, ensure_ascii=False)} -->\n"]
    for numero, contenido in enumerate(paginas, 1):
        bloques.append(f"\n<!-- pagina_pdf: {numero}; pagina_impresa: NO-DETERMINADA -->\n\n{contenido.strip()}\n")
    texto = "".join(bloques)
    ruta = _destino(raiz, dato)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_suffix(".tmp")
    temporal.write_text(texto, encoding="utf-8")
    temporal.replace(ruta)
    return {
        "ruta": ruta.relative_to(raiz).as_posix(),
        "sha256_texto": _sha256(ruta),
        "estado": estado,
        "paginas": len(paginas),
        "metodos": metodos,
    }


def _sincronizar_cabeceras(raiz: Path, manifiesto: dict) -> int:
    """Alinea el encabezado del Markdown con los métodos OCR ya registrados."""
    cambios = 0
    for dato in manifiesto["documentos"].values():
        if dato.get("ocr_estado") != "COMPLETO":
            continue
        extraccion = dato["extraccion"]
        ruta = raiz / extraccion["ruta"]
        texto = ruta.read_text(encoding="utf-8")
        primera, resto = texto.split("\n", 1)
        prefijo = "<!-- metadatos: "
        if not primera.startswith(prefijo) or not primera.endswith(" -->"):
            raise ErrorDominio(f"Encabezado de extracción inválido para {dato['id']}")
        metadatos = json.loads(primera[len(prefijo) : -4])
        if (
            metadatos["metodo_por_pagina"] == extraccion["metodos"]
            and metadatos["estado_calidad"] == extraccion["estado"]
        ):
            continue
        metadatos["metodo_por_pagina"] = extraccion["metodos"]
        metadatos["estado_calidad"] = extraccion["estado"]
        nuevo = prefijo + json.dumps(metadatos, ensure_ascii=False) + " -->\n" + resto
        ruta.write_text(nuevo, encoding="utf-8")
        extraccion["sha256_texto"] = _sha256(ruta)
        cambios += 1
    return cambios


def extraer_nativo(raiz: Path, max_documentos: int | None = None) -> dict:
    """Extrae texto existente; deja páginas OCR como marcadores pendientes."""
    manifiesto = cargar_manifiesto(raiz)
    procesados = 0
    errores = 0
    for dato in manifiesto["documentos"].values():
        plan = dato.get("plan", {})
        if plan.get("estado") in (None, "PENDIENTE-DIAGNOSTICO", "NO-CONFIABLE"):
            continue
        if dato.get("extraccion", {}).get("sha256_original") == dato["sha256"]:
            continue
        if max_documentos is not None and procesados >= max_documentos:
            break
        try:
            lector = PdfReader(raiz / dato["ruta"], strict=False)
            ocr = set(plan["ocr"])
            paginas = [
                "[OCR PENDIENTE: página sin texto nativo suficiente]" if i in ocr else (pagina.extract_text() or "")
                for i, pagina in enumerate(lector.pages, 1)
            ]
            metodos = ["ocr-pendiente" if i in ocr else "nativo" for i in range(1, len(paginas) + 1)]
            estado = "OCR-PENDIENTE" if ocr else "EXTRAIDO-NATIVO-PENDIENTE-COTEJO"
            dato["extraccion"] = _escribir(raiz, dato, paginas, metodos, estado)
            dato["extraccion"]["sha256_original"] = dato["sha256"]
        except Exception as exc:
            dato["extraccion_error"] = f"{type(exc).__name__}: {exc}"[:300]
            errores += 1
        procesados += 1
        guardar_manifiesto(raiz, manifiesto)
    return {
        "procesados": procesados,
        "errores": errores,
        "pendientes": sum(
            "extraccion" not in d and bool(d.get("plan", {}).get("nativas")) for d in manifiesto["documentos"].values()
        ),
    }


def extraer_ocr(raiz: Path, max_documentos: int | None = None, permitir_ids_sin_url: list[str] | None = None) -> dict:
    """Completa OCR por lotes; una excepción sin URL exige un ID explícito en CLI."""
    from .fuentes_ocr import procesar_lote

    manifiesto = cargar_manifiesto(raiz)
    documentos = 0
    paginas = 0
    errores = 0
    ids_permitidos = set(permitir_ids_sin_url or [])
    for dato in sorted(manifiesto["documentos"].values(), key=lambda d: d.get("prioridad") != "CITADA"):
        pendientes = [p for p in dato.get("plan", {}).get("ocr", []) if str(p) not in dato.get("ocr_lotes", {})]
        if not pendientes:
            continue
        if (not dato["url"].startswith("https://") and dato["id"] not in ids_permitidos) or not dato.get(
            "hash_coincide"
        ):
            dato["ocr_estado"] = "OMITIDO-SIN-URL-PUBLICA-O-HASH"
            continue
        if max_documentos is not None and documentos >= max_documentos:
            break
        if "extraccion" not in dato:
            dato["ocr_estado"] = "PENDIENTE-EXTRACCION-NATIVA"
            continue
        documentos += 1
        try:
            lector = PdfReader(raiz / dato["ruta"], strict=False)
            for inicio in range(0, len(pendientes), 20):
                lote = pendientes[inicio : inicio + 20]
                with TemporaryDirectory(dir=raiz / BASE) as temporal:
                    ruta_lote = Path(temporal) / "lote.pdf"
                    escritor = PdfWriter()
                    for numero in lote:
                        escritor.add_page(lector.pages[numero - 1])
                    with ruta_lote.open("wb") as salida:
                        escritor.write(salida)
                    for intento in range(3):
                        try:
                            resultado = procesar_lote(ruta_lote, f"{dato['id']} páginas {lote[0]}-{lote[-1]}")
                            break
                        except Exception:
                            if intento == 2:
                                raise
                if len(resultado["paginas"]) != len(lote):
                    raise ErrorDominio("OCR devolvió una paginación diferente")
                carpeta = _carpeta_ocr(raiz, dato)
                carpeta.mkdir(parents=True, exist_ok=True)
                for numero, texto in zip(lote, resultado["paginas"], strict=True):
                    (carpeta / f"p{numero}.md").write_text(texto, encoding="utf-8")
                    dato.setdefault("ocr_lotes", {})[str(numero)] = resultado["job_id"]
                    paginas += 1
                dato.setdefault("ocr_baja_confianza", []).extend(lote[i - 1] for i in resultado["baja_confianza"])
                guardar_manifiesto(raiz, manifiesto)
            original = (raiz / dato["extraccion"]["ruta"]).read_text(encoding="utf-8")
            partes = re.split(r"(<!-- pagina_pdf: \d+; pagina_impresa: NO-DETERMINADA -->)", original)
            for indice in range(1, len(partes), 2):
                numero = int(re.search(r"pagina_pdf: (\d+)", partes[indice]).group(1))
                archivo = _carpeta_ocr(raiz, dato) / f"p{numero}.md"
                if archivo.is_file():
                    partes[indice + 1] = "\n\n" + archivo.read_text(encoding="utf-8").strip() + "\n"
            completo = "".join(partes)
            ruta = raiz / dato["extraccion"]["ruta"]
            ruta.write_text(completo, encoding="utf-8")
            dato["extraccion"].update(
                estado="EXTRAIDO-CON-OCR-PENDIENTE-COTEJO",
                sha256_texto=_sha256(ruta),
            )
            dato["extraccion"]["metodos"] = [
                "ocr" if str(i) in dato.get("ocr_lotes", {}) else metodo
                for i, metodo in enumerate(dato["extraccion"]["metodos"], 1)
            ]
            dato["ocr_estado"] = "COMPLETO"
        except Exception as exc:
            dato["ocr_estado"] = "ERROR"
            dato["ocr_error"] = str(exc)[:300] if isinstance(exc, ErrorDominio) else type(exc).__name__
            errores += 1
        guardar_manifiesto(raiz, manifiesto)
    for dato in manifiesto["documentos"].values():
        if dato.get("ocr_estado") == "COMPLETO" and dato["extraccion"]["estado"] == "EXTRAIDO-MIXTO-PENDIENTE-COTEJO":
            dato["extraccion"]["estado"] = "EXTRAIDO-CON-OCR-PENDIENTE-COTEJO"
    cabeceras = _sincronizar_cabeceras(raiz, manifiesto)
    if cabeceras:
        guardar_manifiesto(raiz, manifiesto)
    return {
        "documentos_intentados": documentos,
        "paginas_ocr": paginas,
        "errores": errores,
        "cabeceras_sincronizadas": cabeceras,
    }


def evaluar_extraccion(raiz: Path) -> dict:
    """Contrasta paginación, presencia de texto y estado OCR; nunca valida contenido normativo."""
    manifiesto = cargar_manifiesto(raiz)
    conteo: Counter[str] = Counter()
    paginas_pendientes = 0
    paginas_baja_confianza = 0
    paginas_tabla_candidatas = 0
    paginas_texto_escaso = 0
    hashes_crlf_migrados = 0
    hallazgos = []
    for dato in manifiesto["documentos"].values():
        extraccion = dato.get("extraccion")
        diag = dato.get("diagnostico", {})
        ruta_texto = raiz / extraccion["ruta"] if extraccion else None
        if extraccion and ruta_texto.is_file():
            bytes_cache = ruta_texto.read_bytes()
            hash_real = hashlib.sha256(bytes_cache).hexdigest().upper()
            hash_lf = hashlib.sha256(bytes_cache.replace(b"\r\n", b"\n")).hexdigest().upper()
            if hash_real != extraccion["sha256_texto"] and hash_lf == extraccion["sha256_texto"]:
                extraccion["sha256_texto"] = hash_real
                hashes_crlf_migrados += 1
        if not extraccion:
            estado = "SIN-EXTRACCION"
        elif not ruta_texto.is_file():
            estado = "CACHE-FALTANTE"
        elif _sha256(raiz / dato["ruta"]) != dato["sha256"]:
            estado = "ORIGINAL-CAMBIO"
        elif extraccion["paginas"] != diag.get("total"):
            estado = "PAGINACION-DISTINTA"
        elif _sha256(ruta_texto) != extraccion["sha256_texto"]:
            estado = "CACHE-ALTERADA"
        elif (
            len(
                re.findall(
                    r"<!-- pagina_pdf: \d+; pagina_impresa: NO-DETERMINADA -->", ruta_texto.read_text(encoding="utf-8")
                )
            )
            != extraccion["paginas"]
        ):
            estado = "MARCADORES-DISTINTOS"
        else:
            estado = extraccion["estado"]
        conteo[estado] += 1
        if estado in (
            "CACHE-FALTANTE",
            "ORIGINAL-CAMBIO",
            "PAGINACION-DISTINTA",
            "CACHE-ALTERADA",
            "MARCADORES-DISTINTOS",
        ):
            hallazgos.append({"id": dato["id"], "estado": estado})
        paginas_pendientes += extraccion.get("metodos", []).count("ocr-pendiente") if extraccion else 0
        paginas_baja_confianza += len(dato.get("ocr_baja_confianza", []))
        if extraccion and ruta_texto.is_file():
            partes = re.split(
                r"<!-- pagina_pdf: \d+; pagina_impresa: NO-DETERMINADA -->",
                ruta_texto.read_text(encoding="utf-8"),
            )[1:]
            candidatos = []
            for numero, cuerpo in enumerate(partes, 1):
                if numero > len(extraccion["metodos"]):
                    break
                if numero in dato.get("ocr_baja_confianza", []):
                    candidatos.append({"pagina": numero, "motivo": "OCR-BAJA-CONFIANZA"})
                if extraccion["metodos"][numero - 1] == "ocr" and len(cuerpo.strip()) < 80:
                    candidatos.append({"pagina": numero, "motivo": "OCR-TEXTO-ESCASO"})
                    paginas_texto_escaso += 1
                filas = sum(bool(re.search(r"\S\s{3,}\S", linea)) for linea in cuerpo.splitlines())
                if filas >= 5:
                    candidatos.append({"pagina": numero, "motivo": "POSIBLE-TABLA-O-COLUMNAS"})
                    paginas_tabla_candidatas += 1
            dato["cotejo_candidatos"] = candidatos
        dato["evaluacion_extraccion"] = estado
    guardar_manifiesto(raiz, manifiesto)
    return {
        "estados": dict(sorted(conteo.items())),
        "paginas_ocr_pendientes": paginas_pendientes,
        "paginas_ocr_baja_confianza": paginas_baja_confianza,
        "paginas_ocr_texto_escaso": paginas_texto_escaso,
        "paginas_posible_tabla_o_columnas": paginas_tabla_candidatas,
        "hashes_crlf_migrados": hashes_crlf_migrados,
        "hallazgos": hallazgos[:30],
    }


def preparar_cotejo(raiz: Path, identificador: str, pagina: int, archivo: str | None = None) -> dict:
    """Prepara una vista local en paralelo del PDF original y la página extraída."""
    manifiesto = cargar_manifiesto(raiz)
    candidatos = [
        d
        for d in manifiesto["documentos"].values()
        if d["id"] == identificador and (archivo is None or d["ruta"] == archivo)
    ]
    if len(candidatos) != 1:
        raise ErrorDominio("El ID no identifica un PDF único; use un documento no duplicado")
    dato = candidatos[0]
    extraccion = dato.get("extraccion", {})
    if not extraccion or not 1 <= pagina <= extraccion["paginas"]:
        raise ErrorDominio("Página no extraída o fuera de rango")
    texto = (raiz / extraccion["ruta"]).read_text(encoding="utf-8")
    marcador = f"<!-- pagina_pdf: {pagina}; pagina_impresa: NO-DETERMINADA -->"
    cuerpo = texto.split(marcador, 1)[1].split("<!-- pagina_pdf:", 1)[0]
    pdf = (raiz / dato["ruta"]).as_uri() + f"#page={pagina}"
    html = (
        '<!doctype html><html lang="es"><meta charset="utf-8"><title>Cotejo PDF</title>'
        "<style>body{margin:0;font:15px sans-serif}header{padding:12px;background:#17324d;color:white}"
        "main{display:grid;grid-template-columns:1fr 1fr;height:calc(100vh - 55px)}"
        "iframe{width:100%;height:100%;border:0}pre{overflow:auto;white-space:pre-wrap;padding:24px}</style>"
        f"<header>{escape(identificador)} · página PDF {pagina} · cotejo visual pendiente</header>"
        f'<main><iframe src="{escape(pdf, quote=True)}"></iframe><pre>{escape(cuerpo)}</pre></main></html>'
    )
    nombre_seguro = re.sub(r"[^A-Za-z0-9-]", "-", identificador)
    nombre_seguro += "-" + hashlib.sha256(dato["ruta"].encode("utf-8")).hexdigest()[:8]
    salida = raiz / BASE / "cotejos" / f"{nombre_seguro}-p{pagina}.html"
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(html, encoding="utf-8")
    return {"vista": salida.relative_to(raiz).as_posix(), "estado": "PENDIENTE-COTEJO-VISUAL"}
