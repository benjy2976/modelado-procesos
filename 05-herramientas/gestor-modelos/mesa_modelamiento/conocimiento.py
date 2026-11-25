"""Consulta del conocimiento estructurado del repositorio para CLI y MCP (DEC-066). Solo lectura.

El agente accede al conocimiento por estos canales y no por el disco: notas Markdown de áreas autorizadas,
catálogo y textos derivados de la biblioteca, temas, reglas y sus eventos, glosario, decisiones, etiquetas y el
paquete de contexto de una tarea. Nunca se leen originales ni carpetas temporales.
"""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path, PurePosixPath

import yaml

from .repositorio import ErrorDominio, RepositorioProcesos

AREAS = {
    "gobernanza": "00-gobernanza",
    "referencias": "01-referencias",
    "procesos": "02-procesos",
    "conocimiento": "03-conocimiento",
    "coordinacion": "04-coordinacion",
    "herramientas": "05-herramientas",
}
RAIZ_PERMITIDA = {"glosario.md", "estado-del-proyecto.md", "00-GESTION-POR-PROCESOS-GRH.md", "README.md", "AGENTS.md"}
EXCLUIDAS = {
    "originales",
    "node_modules",
    ".nuxt",
    ".output",
    "cache",
    ".mesa-sesiones",
    "salida",
    ".venv",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
}
CATALOGO = Path("01-referencias/00-catalogo/catalogo-documental.csv")
DERIVADOS = Path("01-referencias/09-derivados-texto/cache")
REGLAS = Path("03-conocimiento/reglas")
REVISIONES = Path("03-conocimiento/revisiones")
GLOSARIO = Path("glosario.md")
DECISIONES = Path("00-gobernanza/registro-decisiones.md")
GUIAS = Path("03-conocimiento/fuentes")
PAGINA = re.compile(r"<!-- pagina_pdf: (\d+)")
ENLACE = re.compile(r"\]\(([^)#]+\.md)(?:#[^)]*)?\)")
MAXIMO_LECTURA = 40000


def _normalizar(texto: str) -> str:
    plano = unicodedata.normalize("NFKD", str(texto or ""))
    return " ".join("".join(c for c in plano if not unicodedata.combining(c)).casefold().split())


def _fragmento(texto: str, consulta: str, ancho: int = 220) -> str:
    plano, buscado = _normalizar(texto), _normalizar(consulta)
    posicion = plano.find(buscado) if buscado else 0
    inicio = max(0, posicion - ancho // 3)
    return ("…" if inicio else "") + plano[inicio : inicio + ancho] + ("…" if inicio + ancho < len(plano) else "")


def ruta_permitida(raiz: Path, ruta: str) -> Path:
    """Valida una ruta relativa de nota Markdown dentro de las áreas autorizadas."""
    if not isinstance(ruta, str) or not ruta.strip():
        raise ErrorDominio("Indique la ruta relativa de la nota")
    relativa = PurePosixPath(ruta.strip().lstrip("/"))
    partes = relativa.parts
    if ".." in partes or relativa.suffix.lower() != ".md":
        raise ErrorDominio("Solo se leen notas Markdown con ruta relativa dentro del repositorio", 403)
    if len(partes) == 1:
        if partes[0] not in RAIZ_PERMITIDA:
            raise ErrorDominio(f"La nota {ruta} no está en la lista de notas de la raíz", 403)
    elif partes[0] not in AREAS.values() or EXCLUIDAS & set(partes):
        raise ErrorDominio(f"El área de {ruta} no está autorizada para consulta", 403)
    archivo = raiz / relativa
    if not archivo.is_file():
        raise ErrorDominio(f"No existe la nota {ruta}", 404)
    return archivo


def propiedades(texto: str) -> tuple[dict, str]:
    """Propiedades YAML del encabezado y cuerpo de una nota."""
    if texto.startswith("---"):
        fin = texto.find("\n---", 3)
        if fin != -1:
            try:
                datos = yaml.safe_load(texto[3:fin]) or {}
            except yaml.YAMLError:
                datos = {}
            return (datos if isinstance(datos, dict) else {}), texto[fin + 4 :].lstrip("\n")
    return {}, texto


def _titulo(cuerpo: str, archivo: Path) -> str:
    encontrado = re.search(r"(?m)^#\s+(.+)$", cuerpo)
    return encontrado.group(1).strip() if encontrado else archivo.stem


def _notas(raiz: Path, area: str | None) -> list[Path]:
    if area:
        if area not in AREAS:
            raise ErrorDominio(f"Área desconocida: {area}. Use {sorted(AREAS)}")
        bases = [raiz / AREAS[area]]
        sueltas: list[Path] = []
    else:
        bases = [raiz / carpeta for carpeta in AREAS.values()]
        sueltas = [raiz / nombre for nombre in sorted(RAIZ_PERMITIDA) if (raiz / nombre).is_file()]
    encontradas = [*sueltas]
    for base in bases:
        encontradas += [r for r in sorted(base.rglob("*.md")) if not EXCLUIDAS & set(r.relative_to(raiz).parts)]
    return encontradas


def listar_notas(
    raiz: Path,
    *,
    area: str | None = None,
    tipo: str | None = None,
    estado: str | None = None,
    clase: str | None = None,
    etiqueta: str | None = None,
    proceso: str | None = None,
    texto: str | None = None,
    limite: int = 30,
    desplazamiento: int = 0,
) -> dict:
    """Notas filtradas por propiedades y texto, con título y extracto; no devuelve el contenido completo."""
    limite = max(1, min(int(limite), 100))
    resultados = []
    for archivo in _notas(raiz, area):
        contenido = archivo.read_text(encoding="utf-8", errors="replace")
        datos, cuerpo = propiedades(contenido)
        etiquetas = [str(e) for e in datos.get("tags") or []]
        procesos = [str(p) for p in (datos.get("proceso") or [])] + [str(datos.get("codigo_proceso") or "")]
        if tipo and datos.get("tipo") != tipo:
            continue
        if estado and datos.get("estado_documento") != estado:
            continue
        if clase and datos.get("clase_conocimiento") != clase:
            continue
        if etiqueta and not any(e == etiqueta or e.startswith(etiqueta.rstrip("/") + "/") for e in etiquetas):
            continue
        if proceso and not any(p == proceso or p.startswith(proceso + ".") for p in procesos):
            continue
        if texto and _normalizar(texto) not in _normalizar(contenido):
            continue
        resultados.append(
            {
                "ruta": archivo.relative_to(raiz).as_posix(),
                "titulo": _titulo(cuerpo, archivo),
                "tipo": datos.get("tipo"),
                "area": datos.get("area"),
                "estado_documento": datos.get("estado_documento"),
                "clase_conocimiento": datos.get("clase_conocimiento"),
                "tags": etiquetas,
                "fecha_actualizacion": str(datos.get("fecha_actualizacion") or "") or None,
                **({"extracto": _fragmento(cuerpo, texto)} if texto else {}),
            }
        )
    pagina = resultados[desplazamiento : desplazamiento + limite]
    return {
        "total": len(resultados),
        "desplazamiento": desplazamiento,
        "resultados": pagina,
        "siguiente": desplazamiento + limite if desplazamiento + limite < len(resultados) else None,
    }


def leer_nota(raiz: Path, ruta: str, desde: int = 0, max_caracteres: int = 20000) -> dict:
    """Propiedades, título, enlaces y un tramo del cuerpo de una nota autorizada."""
    archivo = ruta_permitida(raiz, ruta)
    datos, cuerpo = propiedades(archivo.read_text(encoding="utf-8", errors="replace"))
    max_caracteres = max(500, min(int(max_caracteres), MAXIMO_LECTURA))
    desde = max(0, int(desde))
    enlaces = []
    for destino in dict.fromkeys(ENLACE.findall(cuerpo)):
        if "://" in destino:
            continue
        resuelto = (archivo.parent / destino).resolve()
        if resuelto.is_relative_to(raiz.resolve()):
            enlaces.append(resuelto.relative_to(raiz.resolve()).as_posix())
    fin = desde + max_caracteres
    return {
        "ruta": archivo.relative_to(raiz).as_posix(),
        "titulo": _titulo(cuerpo, archivo),
        "propiedades": json.loads(json.dumps(datos, default=str)),
        "total_caracteres": len(cuerpo),
        "desde": desde,
        "texto": cuerpo[desde:fin],
        "siguiente": fin if fin < len(cuerpo) else None,
        "enlaces": enlaces[:60],
    }


def _catalogo(raiz: Path) -> list[dict]:
    """Filas del catálogo documental (calificación de calidad); complementa el inventario de preparación."""
    ruta = raiz / CATALOGO
    if not ruta.is_file():
        return []
    with ruta.open(encoding="utf-8", newline="") as archivo:
        return list(csv.DictReader(archivo))


def inventario(raiz: Path) -> list[dict]:
    """Documentos de la biblioteca según los manifiestos de preparación PDF y Office, con régimen y calidad."""
    from .fuentes_office import MANIFIESTO_OFFICE
    from .fuentes_preparacion import MANIFIESTO
    from .fuentes_regimen import cargar_reglas, clasificar

    reglas = cargar_reglas(raiz)
    calidad = {f["id"]: f for f in _catalogo(raiz)}
    salida = []
    for manifiesto, formato in ((MANIFIESTO, "pdf"), (MANIFIESTO_OFFICE, "office")):
        archivo = raiz / manifiesto
        if not archivo.is_file():
            continue
        for entrada in json.loads(archivo.read_text(encoding="utf-8")).get("documentos", {}).values():
            extraccion = entrada.get("extraccion") or {}
            estado = entrada.get("estado") or (entrada.get("plan") or {}).get("estado")
            ficha = calidad.get(entrada.get("id") or "", {})
            salida.append(
                {
                    "id": entrada.get("id"),
                    "ruta": entrada.get("ruta"),
                    "formato": entrada.get("tipo") or formato,
                    "titulo": entrada.get("titulo") or ficha.get("titulo") or Path(entrada.get("ruta", "")).stem,
                    "vigencia": entrada.get("vigencia") or ficha.get("vigencia") or None,
                    "regimen": clasificar(reglas, entrada.get("ruta", ""))[0],
                    "estado_extraccion": estado,
                    "texto_derivado": extraccion.get("ruta"),
                    "catalogado": entrada.get("catalogado"),
                    "hash_coincide": entrada.get("hash_coincide"),
                    "calificacion": ficha.get("calificacion") or None,
                }
            )
    return salida


def listar_documentos(
    raiz: Path,
    *,
    texto: str | None = None,
    area: str | None = None,
    formato: str | None = None,
    regimen: str | None = None,
    con_texto: bool | None = None,
    limite: int = 30,
    desplazamiento: int = 0,
) -> dict:
    """Documentos de la biblioteca filtrados por texto, carpeta de 01-referencias, formato, régimen y texto derivado."""
    limite = max(1, min(int(limite), 100))
    salida = []
    for documento in inventario(raiz):
        buscable = " ".join(str(documento[k] or "") for k in ("id", "titulo", "ruta"))
        if texto and _normalizar(texto) not in _normalizar(buscable):
            continue
        if area and not str(documento["ruta"]).startswith(f"01-referencias/{area}"):
            continue
        if formato and formato.lower() not in (
            str(documento["formato"]).lower(),
            Path(str(documento["ruta"])).suffix[1:],
        ):
            continue
        if regimen and documento["regimen"] != regimen:
            continue
        if con_texto is not None and bool(documento["texto_derivado"]) != con_texto:
            continue
        salida.append(documento)
    return {"total": len(salida), "resultados": salida[desplazamiento : desplazamiento + limite]}


def leer_documento(raiz: Path, identificador: str) -> dict:
    """Ficha de un documento por ID de catálogo o ruta, con su fila de calidad si existe."""
    encontrados = [d for d in inventario(raiz) if identificador in (d["id"], d["ruta"])]
    if not encontrados:
        raise ErrorDominio(f"El documento {identificador} no está en el inventario de la biblioteca", 404)
    calidad = next((f for f in _catalogo(raiz) if f["id"] == encontrados[0]["id"]), None)
    return {"documentos": encontrados, "calidad": calidad}


def leer_texto_documento(
    raiz: Path, identificador: str, pagina_desde: int = 1, paginas: int = 3, max_caracteres: int = 12000
) -> dict:
    """Páginas del Markdown derivado de un documento (no el original), por ID o ruta del original."""
    documentos = [d for d in leer_documento(raiz, identificador)["documentos"] if d["texto_derivado"]]
    if not documentos:
        raise ErrorDominio(f"El documento {identificador} no tiene texto derivado", 404)
    if len(documentos) > 1 and identificador == documentos[0]["id"]:
        rutas = [d["ruta"] for d in documentos]
        raise ErrorDominio(f"El ID {identificador} tiene varios archivos; indique la ruta: {rutas}", 409)
    archivo = raiz / documentos[0]["texto_derivado"]
    if not archivo.is_file() or not archivo.resolve().is_relative_to((raiz / DERIVADOS).resolve()):
        raise ErrorDominio(f"El texto derivado de {identificador} no está disponible", 404)
    texto = archivo.read_text(encoding="utf-8", errors="replace")
    marcas = list(PAGINA.finditer(texto))
    metadatos = re.search(r"<!-- metadatos: (\{.*?\}) -->", texto)
    if not marcas:
        cuerpo, total, devueltas = texto, None, []
    else:
        total = int(marcas[-1].group(1))
        paginas = max(1, min(int(paginas), 20))
        tramos = [
            (int(m.group(1)), m.start(), marcas[i + 1].start() if i + 1 < len(marcas) else len(texto))
            for i, m in enumerate(marcas)
        ]
        elegidas = [t for t in tramos if pagina_desde <= t[0] < pagina_desde + paginas]
        devueltas = [t[0] for t in elegidas]
        cuerpo = "".join(texto[a:b] for _, a, b in elegidas)
    max_caracteres = max(500, min(int(max_caracteres), MAXIMO_LECTURA))
    return {
        "id": documentos[0]["id"],
        "ruta_original": documentos[0]["ruta"],
        "ruta": archivo.relative_to(raiz).as_posix(),
        "metadatos": json.loads(metadatos.group(1)) if metadatos else None,
        "paginas_total": total,
        "paginas": devueltas,
        "texto": cuerpo[:max_caracteres],
        "recortado": len(cuerpo) > max_caracteres,
    }


def listar_temas(raiz: Path) -> dict:
    from .fuentes_temas import cargar_vocabulario

    vocabulario = cargar_vocabulario(raiz)
    return {
        "temas": [
            {k: t.get(k) for k in ("id", "etiqueta", "procesos", "terminos", "relacionados")}
            for t in vocabulario.get("temas", [])
        ]
    }


def _reglas(raiz: Path) -> list[tuple[Path, dict]]:
    salida = []
    for archivo in sorted((raiz / REGLAS).glob("*.yaml")):
        try:
            datos = yaml.safe_load(archivo.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError as exc:
            raise ErrorDominio(f"Regla ilegible: {archivo.name}: {exc}", 500) from exc
        salida.append((archivo, datos))
    return salida


def _aplica(procesos: list[str], codigo: str) -> bool:
    return any(codigo == p or codigo.startswith(p + ".") or p.startswith(codigo + ".") for p in procesos)


def listar_reglas(
    raiz: Path,
    *,
    proceso: str | None = None,
    dominio: str | None = None,
    estado: str | None = None,
    modalidad: str | None = None,
    texto: str | None = None,
) -> dict:
    """Reglas normativas desde sus YAML (fuente maestra), filtradas; el proceso incluye ancestros y descendientes."""
    salida = []
    for archivo, datos in _reglas(raiz):
        aplicabilidad = datos.get("aplicabilidad") or {}
        procesos = [str(p) for p in aplicabilidad.get("procesos") or []]
        validacion = (datos.get("validacion") or {}).get("estado")
        if proceso and not _aplica(procesos, proceso):
            continue
        if dominio and datos.get("dominio") != dominio:
            continue
        if estado and validacion != estado:
            continue
        if modalidad and modalidad not in (aplicabilidad.get("modalidades") or []):
            continue
        if texto and _normalizar(texto) not in _normalizar(json.dumps(datos, ensure_ascii=False, default=str)):
            continue
        fuente = datos.get("fuente") or {}
        salida.append(
            {
                "id": datos.get("id_regla"),
                "titulo": datos.get("titulo"),
                "dominio": datos.get("dominio"),
                "tipo": datos.get("tipo_regla"),
                "estado_validacion": validacion,
                "vigencia": (datos.get("vigencia") or {}).get("estado"),
                "procesos": procesos,
                "modalidades": aplicabilidad.get("modalidades") or [],
                "documento": fuente.get("id_documento"),
                "ubicacion": fuente.get("articulo"),
                "archivo": archivo.relative_to(raiz).as_posix(),
            }
        )
    return {
        "total": len(salida),
        "reglas": salida,
        "advertencia": "Las reglas BORRADOR-IA no sustentan una línea base (protocolo de conocimiento confiable).",
    }


def leer_regla(raiz: Path, identificador: str) -> dict:
    """Regla completa y sus eventos de revisión, sin modificarlos."""
    encontrada = next(((a, d) for a, d in _reglas(raiz) if d.get("id_regla") == identificador), None)
    if encontrada is None:
        raise ErrorDominio(f"No existe la regla {identificador}", 404)
    archivo, datos = encontrada
    eventos = []
    for evento in sorted((raiz / REVISIONES).glob("*.yaml")):
        contenido = yaml.safe_load(evento.read_text(encoding="utf-8")) or {}
        if identificador in json.dumps(contenido, ensure_ascii=False, default=str):
            eventos.append({"archivo": evento.relative_to(raiz).as_posix(), **contenido})
    return {
        "archivo": archivo.relative_to(raiz).as_posix(),
        "regla": json.loads(json.dumps(datos, default=str)),
        "eventos": json.loads(json.dumps(eventos, default=str)),
    }


def _leer_si_existe(ruta: Path) -> str:
    return ruta.read_text(encoding="utf-8") if ruta.is_file() else ""


def _tabla_markdown(texto: str, primera_columna: str) -> list[dict[str, str]]:
    filas, encabezado = [], None
    for linea in texto.splitlines():
        if not linea.startswith("|"):
            encabezado = None if not linea.strip() else encabezado
            continue
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if celdas and celdas[0] == primera_columna:
            encabezado = celdas
        elif encabezado and not set("".join(celdas)) <= set("-: "):
            filas.append(dict(zip(encabezado, celdas, strict=False)))
    return filas


def buscar_glosario(raiz: Path, texto: str | None = None) -> dict:
    """Términos del glosario vivo cuyo término o definición contiene el texto (todos si no se indica)."""
    filas = _tabla_markdown(_leer_si_existe(raiz / GLOSARIO), "Termino")
    if texto:
        filas = [
            f
            for f in filas
            if _normalizar(texto) in _normalizar(f.get("Termino", "") + " " + f.get("Definicion de trabajo", ""))
        ]
    return {
        "total": len(filas),
        "terminos": [
            {
                "termino": f.get("Termino"),
                "definicion": f.get("Definicion de trabajo"),
                "fuente_pendiente": f.get("Fuente pendiente"),
            }
            for f in filas
        ],
    }


def buscar_decisiones(
    raiz: Path, *, texto: str | None = None, identificador: str | None = None, limite: int = 20
) -> dict:
    """Decisiones del registro por ID o texto; devuelve las más recientes primero."""
    texto_registro = _leer_si_existe(raiz / DECISIONES)
    encabezado = next((f for f in _tabla_markdown(texto_registro, "ID")[:1]), None)
    columnas = list(encabezado) if encabezado else ["ID", "Fecha", "Decision", "Motivo", "Impacto", "Responsable"]
    # Cada fila DEC se lee por sí misma: el registro tiene líneas en blanco que parten la tabla.
    filas = [
        dict(zip(columnas, [c.strip() for c in linea.strip().strip("|").split("|")], strict=False))
        for linea in texto_registro.splitlines()
        if re.match(r"\|\s*DEC-\d+\s*\|", linea)
    ]
    if identificador:
        filas = [f for f in filas if f.get("ID") == identificador]
        if not filas:
            raise ErrorDominio(f"No existe la decisión {identificador}", 404)
    elif texto:
        filas = [f for f in filas if _normalizar(texto) in _normalizar(" ".join(f.values()))]
    filas = list(reversed(filas))[: max(1, min(int(limite), 100))]
    return {
        "total": len(filas),
        "decisiones": [
            {
                "id": f.get("ID"),
                "fecha": f.get("Fecha"),
                "decision": f.get("Decision"),
                "motivo": f.get("Motivo"),
                "impacto": f.get("Impacto"),
                "responsable": f.get("Responsable"),
            }
            for f in filas
        ],
    }


def etiquetas(raiz: Path, operacion: str = "revisar") -> dict:
    """Revisión o recuento de etiquetas con 05-herramientas/gestionar_etiquetas.py, sin modificar notas."""
    if operacion not in {"revisar", "listar"}:
        raise ErrorDominio("Solo se permiten las operaciones de lectura revisar y listar")
    proceso = subprocess.run(
        [sys.executable, str(raiz / "05-herramientas" / "gestionar_etiquetas.py"), operacion],
        cwd=raiz,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    lineas = proceso.stdout.splitlines()
    return {
        "operacion": operacion,
        "codigo_salida": proceso.returncode,
        "resumen": lineas[-1] if lineas else "",
        "lineas": lineas[:300],
        "errores": proceso.stderr[-2000:],
    }


def paquete_contexto(repositorio: RepositorioProcesos, codigo: str, tarea: str = "") -> dict:
    """Paquete de contexto de una tarea (manual operativo, 6.6): rutas y resúmenes, no la biblioteca completa."""
    from .auditoria import AUDITORIAS
    from .observaciones import ServicioObservaciones
    from .sesiones import ServicioSesiones

    raiz = repositorio.raiz
    rutas = repositorio.rutas(codigo)
    carpeta = repositorio.carpeta(codigo)
    rutas = {
        **rutas,
        "fuentes_visor": rutas["tabla"].with_name(
            rutas["tabla"].name.replace("-diagrama-proceso-tabla.md", "-fuentes-visor.json")
        ),
    }
    documentos = {nombre: ruta.relative_to(raiz).as_posix() for nombre, ruta in rutas.items() if ruta.is_file()}
    notas = sorted(p.relative_to(raiz).as_posix() for p in carpeta.glob("*.md"))
    texto_modelo = " ".join(
        (raiz / documentos[n]).read_text(encoding="utf-8", errors="replace")
        for n in ("tabla", "sustento")
        if n in documentos
    )
    plano = _normalizar(texto_modelo)
    glosario = [t for t in buscar_glosario(raiz)["terminos"] if t["termino"] and _normalizar(t["termino"]) in plano]
    visor = (
        json.loads((raiz / documentos["fuentes_visor"]).read_text(encoding="utf-8"))
        if "fuentes_visor" in documentos
        else {}
    )
    rutas_fuente = {a.get("ruta") for anclas in visor.get("elementos", {}).values() for a in anclas}
    ids_fuente = sorted({d["id"] for d in inventario(raiz) if d["ruta"] in rutas_fuente and d["id"]})
    guias = []
    for guia in sorted((raiz / GUIAS).glob("guia-*.md")):
        contenido = guia.read_text(encoding="utf-8", errors="replace")
        if any(i in contenido for i in ids_fuente):
            guias.append(
                {"ruta": guia.relative_to(raiz).as_posix(), "titulo": _titulo(propiedades(contenido)[1], guia)}
            )
    decisiones = buscar_decisiones(raiz, texto=codigo, limite=15)["decisiones"]
    try:
        abiertas = [
            o for o in ServicioObservaciones(repositorio).listar(codigo)["observaciones"] if o["estado"] == "ABIERTA"
        ]
    except ErrorDominio:
        abiertas = []
    auditoria = None
    for corrida in sorted((raiz / AUDITORIAS).glob("corrida-*.json")):
        procesos = json.loads(corrida.read_text(encoding="utf-8")).get("procesos", {})
        if codigo in procesos:
            auditoria = {"corrida": corrida.relative_to(raiz).as_posix(), **procesos[codigo]}
    return {
        "esquema": "paquete-contexto-v1",
        "proceso": codigo,
        "tarea": tarea or "pendiente",
        "fase_trabajo": "conceptual",
        "modelo_vigente": documentos,
        "notas_del_proceso": notas,
        "reglas_aplicables": listar_reglas(raiz, proceso=codigo)["reglas"],
        "fuentes_ancladas": ids_fuente,
        "guias_de_lectura": guias,
        "glosario_aplicable": glosario,
        "decisiones_relacionadas": [
            {k: d[k] for k in ("id", "fecha")} | {"decision": (d["decision"] or "")[:220]} for d in decisiones
        ],
        "observaciones_abiertas": [
            {"id": o["id"], "referencia": o.get("referencia"), "tipo": o.get("tipo"), "texto": o["texto"][:220]}
            for o in abiertas
        ],
        "auditoria": auditoria,
        "sesion_activa": ServicioSesiones(repositorio).activa(codigo),
        "artefactos_excluidos_del_contexto": ["*.bpmn", "*.svg", "*.png", "*.html"],
        "restricciones": [
            "No usar conocimiento general para afirmaciones normativas.",
            "Registrar EVIDENCIA-INSUFICIENTE cuando las fuentes no sostengan una conclusion.",
            "Las reglas BORRADOR-IA no sustentan una linea base.",
        ],
    }
