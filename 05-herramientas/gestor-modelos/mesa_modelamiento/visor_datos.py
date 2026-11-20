"""Datos de revision del visor, derivados de la tabla sin editar el BPMN."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

from .identificadores import gid


def _filas(texto: str, titulo: str) -> list[list[str]]:
    seccion = texto.split(f"## {titulo}\n", 1)
    if len(seccion) < 2:
        return []
    bloque = seccion[1].split("\n## ", 1)[0]
    filas = []
    for linea in bloque.splitlines():
        if not linea.startswith("|") or re.match(r"^\|\s*-", linea):
            continue
        filas.append([celda.strip() for celda in linea.strip().strip("|").split("|")])
    return filas


def datos_visor(tabla: Path, html: Path, raiz: Path) -> dict:
    tabla, html, raiz = tabla.resolve(), html.resolve(), raiz.resolve()
    texto = tabla.read_text(encoding="utf-8")
    semilla = tabla.name.removesuffix(".md")
    codigo = re.search(r"^codigo_proceso:\s*(\S+)", texto, re.MULTILINE)
    padre = re.search(r"^proceso_padre:\s*(\S+)", texto, re.MULTILINE)
    elementos: dict[str, dict] = {}
    flujos: dict[str, dict] = {}
    filas_elementos = _filas(texto, "Elementos")
    cabecera = filas_elementos[0] if filas_elementos else []
    for fila in filas_elementos[1:]:
        columnas = dict(zip(cabecera, fila, strict=False))
        ref = columnas.get("ID", "")
        if not ref:
            continue
        numero, pool, carril = (columnas.get(c, "") for c in ("Numero", "Pool", "Carril"))
        tipo, nombre, siguientes = (columnas.get(c, "") for c in ("Tipo", "Nombre", "Siguiente"))
        datos = {
            "ref": ref,
            "numero": numero,
            "pool": pool,
            "carril": carril,
            "tipo": tipo,
            "nombre": nombre,
            "documentos": columnas.get("Documentos", ""),
            "plazo": columnas.get("Plazo", ""),
            "disparador": columnas.get("Disparador", ""),
            "anotacion": columnas.get("Anotacion", ""),
            "clase": columnas.get("Clase", ""),
            "fuente": columnas.get("Fuente", ""),
        }
        if tipo.startswith("subproceso"):
            codigo_hijo = re.match(r"^(S\d+(?:\.\d+)+)\b", nombre)
            if codigo_hijo:
                prefijo = codigo_hijo.group(1).replace(".", "-")
                carpeta_hija = next(
                    (
                        p
                        for p in (raiz / "02-procesos").rglob(f"{prefijo}-*")
                        if p.is_dir() and re.match(rf"^{re.escape(prefijo)}-(?!\d)", p.name)
                    ),
                    None,
                )
                if carpeta_hija:
                    modelo_hijo = carpeta_hija / f"{prefijo}-diagrama-proceso.html"
                    indice_hijo = next(iter(sorted(carpeta_hija.glob("00-*.md"))), None)
                    destino = modelo_hijo if modelo_hijo.is_file() else indice_hijo
                    if destino:
                        datos["destino"] = "/" + destino.relative_to(raiz).as_posix()
                        datos["destino_tipo"] = "diagrama" if destino == modelo_hijo else "indice"
        elementos[gid(semilla, "nodo", ref)] = datos
        for siguiente in siguientes.split(";"):
            m = re.match(r"\s*([^\s\[]+)(?:\s*\[(.*?)\])?\s*$", siguiente)
            if not m:
                continue
            destino, condicion = m.group(1), m.group(2) or ""
            flujos[gid(semilla, "flujo", ref, destino)] = {
                "tipo": "secuencia",
                "origen": ref,
                "destino": destino,
                "condicion": condicion,
                "fuente": "",
            }
    for k, fila in enumerate(_filas(texto, "Mensajes")[1:]):
        if len(fila) < 3:
            continue
        origen, destino, nombre = fila[:3]
        flujos[gid(semilla, "msj", origen, destino, str(k))] = {
            "tipo": "mensaje",
            "origen": origen,
            "destino": destino,
            "nombre": nombre,
            "fuente": "",
        }
    enlace_padre = ""
    codigo_actual = codigo.group(1) if codigo else ""
    codigo_padre = (
        padre.group(1) if padre and padre.group(1) not in ("null", "None") else codigo_actual.rpartition(".")[0]
    )
    if codigo_padre:
        base_padre = codigo_padre.replace(".", "-") + "-diagrama-proceso.html"
        for carpeta in html.parents:
            candidato = carpeta / base_padre
            if candidato.is_file() and candidato != html:
                enlace_padre = os.path.relpath(candidato, html.parent).replace(os.sep, "/")
                break
            if carpeta == raiz:
                break
        if not enlace_padre:
            for carpeta in html.parents:
                indice = next(iter(sorted(carpeta.glob("00-*.md"))), None)
                if indice and carpeta != html.parent:
                    enlace_padre = os.path.relpath(indice, html.parent).replace(os.sep, "/")
                    break
                if carpeta == raiz:
                    break
    referencias = tabla.with_name(tabla.name.replace("-diagrama-proceso-tabla.md", "-fuentes-visor.json"))
    fuentes_visor = {}
    hashes_fuentes: dict[Path, str] = {}
    if referencias.is_file():
        contenido = json.loads(referencias.read_text(encoding="utf-8"))
        if not isinstance(contenido, dict) or not isinstance(contenido.get("elementos"), dict):
            raise ValueError(f"Metadatos de fuentes invalidos: {referencias}")
        for ref, entradas in contenido["elementos"].items():
            if ref not in {e["ref"] for e in elementos.values()} or not isinstance(entradas, list):
                raise ValueError(f"Referencia de elemento invalida: {ref}")
            fuentes_visor[ref] = []
            for entrada in entradas:
                ruta = entrada.get("ruta", "")
                if not isinstance(ruta, str):
                    raise ValueError(f"Ruta de fuente invalida: {ruta}")
                archivo = (raiz / ruta).resolve()
                if (
                    not archivo.is_relative_to(raiz)
                    or not archivo.is_file()
                    or archivo.suffix.lower() not in {".pdf", ".md", ".txt", ".html"}
                    or not ruta.startswith(("01-referencias/", "03-conocimiento/"))
                ):
                    raise ValueError(f"Ruta de fuente invalida: {ruta}")
                pagina = entrada.get("pagina")
                if pagina is not None and (
                    not isinstance(pagina, int) or pagina < 1 or archivo.suffix.lower() != ".pdf"
                ):
                    raise ValueError(f"Pagina de fuente invalida: {ruta}")
                rectangulos = entrada.get("rectangulos", [])
                huella_registrada = entrada.get("sha256", "")
                if rectangulos and (
                    pagina is None
                    or not isinstance(huella_registrada, str)
                    or not re.fullmatch(r"[0-9a-fA-F]{64}", huella_registrada)
                    or not isinstance(rectangulos, list)
                    or any(
                        not isinstance(rect, list)
                        or len(rect) != 4
                        or any(not isinstance(v, (int, float)) or isinstance(v, bool) for v in rect)
                        or not (0 <= rect[0] < rect[2] <= 1 and 0 <= rect[1] < rect[3] <= 1)
                        for rect in rectangulos
                    )
                ):
                    raise ValueError(f"Ancla PDF invalida: {ruta}")
                estado_ancla = "SIN_COORDENADAS"
                if rectangulos:
                    if archivo not in hashes_fuentes:
                        with archivo.open("rb") as lectura:
                            hashes_fuentes[archivo] = hashlib.file_digest(lectura, "sha256").hexdigest()
                    estado_ancla = (
                        "DISPONIBLE" if hashes_fuentes[archivo] == huella_registrada.lower() else "HASH_DISTINTO"
                    )
                fuentes_visor[ref].append(
                    {
                        "ruta": ruta,
                        "pagina": pagina,
                        "fragmento": str(entrada.get("fragmento", "")),
                        "titulo": str(entrada.get("titulo", archivo.name)),
                        "ubicacion": str(entrada.get("ubicacion", "")),
                        "consulta": str(entrada.get("consulta", "")),
                        "vigencia": str(entrada.get("vigencia", "")),
                        "sha256": huella_registrada,
                        "rectangulos": rectangulos if estado_ancla == "DISPONIBLE" else [],
                        "estado_ancla": estado_ancla,
                    }
                )
    return {
        "codigo": codigo_actual,
        "modelo": html.relative_to(raiz).as_posix(),
        "padre": enlace_padre,
        "tabla": tabla.name,
        "sustento": tabla.name.replace("-diagrama-proceso-tabla.md", "-sustento.md"),
        "elementos": elementos,
        "flujos": flujos,
        "fuentes_visor": fuentes_visor,
    }
