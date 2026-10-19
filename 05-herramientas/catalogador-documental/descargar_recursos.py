from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import mimetypes
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".pptx", ".doc", ".xls"}
USER_AGENT = "Mozilla/5.0 (compatible; GRH-documental/2.0; public-records)"
REGISTRY_FIELDS = [
    "id_fuente", "archivo", "url_solicitada", "url_final", "estado",
    "tamano_bytes", "sha256", "tipo_contenido", "aplicabilidad_0_5",
    "fecha_consulta", "etag", "ultima_modificacion", "error",
]


def fetch(url: str, retries: int = 3) -> tuple[bytes, str, dict[str, str]]:
    last_error: Exception | None = None
    parsed = urllib.parse.urlparse(url)
    # El MEF devuelve una pagina HTML de bloqueo para sus XLSX con el agente
    # identificador del catalogador. La cabecera generica entrega el archivo.
    user_agent = "Mozilla/5.0" if parsed.hostname == "mef.gob.pe" and parsed.path.lower().endswith(".xlsx") else USER_AGENT
    for attempt in range(retries):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": user_agent})
            with urllib.request.urlopen(request, timeout=90) as response:
                headers = {
                    "tipo_contenido": response.headers.get("Content-Type", ""),
                    "etag": response.headers.get("ETag", ""),
                    "ultima_modificacion": response.headers.get("Last-Modified", ""),
                }
                return response.read(), response.geturl(), headers
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1.5 * (attempt + 1))
    assert last_error is not None
    raise last_error


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def extension_from_url(url: str) -> str:
    return Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).suffix.lower()


def safe_name(url: str) -> str:
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    name = Path(path).name or "documento"
    name = re.sub(r"^\d{6,}-", "", name)
    return re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-.").lower()


def relative_path(root: Path, value: str | Path) -> str:
    path = Path(str(value).replace("\\", "/"))
    if path.is_absolute():
        path = path.resolve().relative_to(root)
    return path.as_posix()


def links_from_landing_page(page_url: str) -> list[str]:
    body, final_url, _ = fetch(page_url)
    source = html.unescape(body.decode("utf-8", errors="replace"))
    candidates = re.findall(
        r'''(?:href|src)=["']([^"']+)["']''', source, flags=re.IGNORECASE
    )
    links: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        absolute = urllib.parse.urljoin(final_url, candidate)
        if "preview_" in absolute.lower() or extension_from_url(absolute) not in ALLOWED_EXTENSIONS:
            continue
        if absolute not in seen:
            links.append(absolute)
            seen.add(absolute)
    return links


def load_registry(root: Path, registry: Path) -> dict[str, dict[str, str]]:
    if not registry.exists():
        return {}
    result: dict[str, dict[str, str]] = {}
    for row in csv.DictReader(registry.open(encoding="utf-8-sig", newline="")):
        try:
            row["archivo"] = relative_path(root, row["archivo"])
        except (ValueError, OSError):
            continue
        result[row["archivo"]] = row
    return result


def discover_tasks(config: dict[str, object]) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    tasks: list[dict[str, object]] = []
    errors: list[dict[str, str]] = []
    for page in config["landing_pages"]:  # type: ignore[index]
        try:
            for link in links_from_landing_page(page["url"]):
                tasks.append({
                    "id": page["id"], "url": link,
                    "destino": (Path(page["destino"]) / safe_name(link)).as_posix(),
                    "aplicabilidad": int(page["aplicabilidad"]),
                })
        except Exception as exc:  # noqa: BLE001
            errors.append({"id": str(page["id"]), "url": str(page["url"]), "error": str(exc)})
    for item in config["direct_downloads"]:  # type: ignore[index]
        tasks.append({
            "id": item["id"], "url": item["url"], "destino": item["destino"],
            "aplicabilidad": int(item["aplicabilidad"]),
        })
    return list({str(task["destino"]): task for task in tasks}.values()), errors


def tasks_from_registry(previous: dict[str, dict[str, str]]) -> list[dict[str, object]]:
    return [
        {
            "id": row["id_fuente"], "url": row.get("url_final") or row["url_solicitada"],
            "destino": path, "aplicabilidad": int(row.get("aplicabilidad_0_5") or 0),
        }
        for path, row in previous.items()
    ]


def base_row(task: dict[str, object], path: str) -> dict[str, str | int]:
    return {
        "id_fuente": str(task["id"]), "archivo": path,
        "url_solicitada": str(task["url"]), "url_final": str(task["url"]), "estado": "",
        "tamano_bytes": 0, "sha256": "", "tipo_contenido": "",
        "aplicabilidad_0_5": int(task["aplicabilidad"]),
        "fecha_consulta": date.today().isoformat(), "etag": "", "ultima_modificacion": "", "error": "",
    }


def candidate_path(root: Path, relative: str, digest: str) -> Path:
    original = Path(relative)
    filename = f"{original.stem}--candidato-{digest[:8]}{original.suffix}"
    return root / "99-temporal" / "actualizaciones-documentales" / original.parent / filename


def process_task(
    root: Path, task: dict[str, object], previous: dict[str, str] | None, refresh: bool,
) -> dict[str, str | int]:
    relative = relative_path(root, str(task["destino"]))
    target = root / relative
    row = base_row(task, relative)
    expected = (previous or {}).get("sha256", "").upper()
    if target.exists() and target.stat().st_size > 0:
        local_data = target.read_bytes()
        local_hash = sha256(local_data)
        row.update({
            "tamano_bytes": len(local_data), "sha256": local_hash,
            "tipo_contenido": mimetypes.guess_type(target.name)[0] or "",
        })
        if expected and local_hash != expected:
            row["estado"] = "alerta-local-modificado"
            row["error"] = f"Hash esperado {expected}; hash local {local_hash}. No se modifica el archivo."
            return row
        if not refresh:
            row["estado"] = "verificado-local"
            if previous:
                row["url_final"] = previous.get("url_final") or str(task["url"])
                row["etag"] = previous.get("etag", "")
                row["ultima_modificacion"] = previous.get("ultima_modificacion", "")
            return row
    try:
        remote_data, final_url, headers = fetch(str(task["url"]))
        remote_hash = sha256(remote_data)
        row.update({
            "url_final": final_url, "tipo_contenido": headers["tipo_contenido"],
            "etag": headers["etag"], "ultima_modificacion": headers["ultima_modificacion"],
        })
        if target.exists():
            if remote_hash == str(row["sha256"]):
                row["estado"] = "sin-cambios-remotos"
                return row
            candidate = candidate_path(root, relative, remote_hash)
            candidate.parent.mkdir(parents=True, exist_ok=True)
            candidate.write_bytes(remote_data)
            row["estado"] = "cambio-remoto-detectado"
            row["error"] = (
                f"El origen cambio a SHA-256 {remote_hash}. Candidato guardado en "
                f"{candidate.relative_to(root).as_posix()}; requiere revision antes de sustituir."
            )
            return row
        if expected and remote_hash != expected:
            candidate = candidate_path(root, relative, remote_hash)
            candidate.parent.mkdir(parents=True, exist_ok=True)
            candidate.write_bytes(remote_data)
            row.update({
                "estado": "hash-remoto-no-coincide", "sha256": expected,
                "error": (
                    f"Hash esperado {expected}; origen actual {remote_hash}. Candidato guardado en "
                    f"{candidate.relative_to(root).as_posix()}."
                ),
            })
            return row
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(remote_data)
        row.update({"estado": "descargado", "tamano_bytes": len(remote_data), "sha256": remote_hash})
        return row
    except Exception as exc:  # noqa: BLE001
        row["estado"] = "error"
        row["error"] = str(exc)
        return row


def write_csv(path: Path, rows: list[dict[str, str | int]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=REGISTRY_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Restaura, descubre o comprueba actualizaciones de la biblioteca publica."
    )
    parser.add_argument("--config", default="05-herramientas/catalogador-documental/fuentes-descarga.json")
    parser.add_argument("--root", default=".")
    parser.add_argument(
        "--modo", choices=("restaurar", "descubrir", "actualizar"), default="restaurar",
        help=(
            "restaurar descarga solo ausentes usando el indice; descubrir consulta las fichas y agrega recursos; "
            "actualizar vuelve a consultar y detecta cambios sin sobrescribir originales"
        ),
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()
    registry = root / "01-referencias/00-catalogo/registro-descargas.csv"
    runtime_report = root / "99-temporal/registro-ultima-sincronizacion.csv"
    previous = load_registry(root, registry)
    discovery_errors: list[dict[str, str]] = []
    if args.modo == "restaurar":
        if not previous:
            print("No existe un indice de descargas. Ejecute --modo descubrir.", file=sys.stderr)
            return 2
        tasks = tasks_from_registry(previous)
    else:
        config = json.loads((root / args.config).read_text(encoding="utf-8"))
        tasks, discovery_errors = discover_tasks(config)
        discovered_paths = {relative_path(root, str(task["destino"])) for task in tasks}
        tasks.extend(task for task in tasks_from_registry(previous) if str(task["destino"]) not in discovered_paths)
    rows: list[dict[str, str | int]] = []
    refresh = args.modo == "actualizar"
    for index, task in enumerate(tasks, start=1):
        rel = relative_path(root, str(task["destino"]))
        print(f"[{index}/{len(tasks)}] {task['id']} -> {rel}", flush=True)
        rows.append(process_task(root, task, previous.get(rel), refresh))
    write_csv(runtime_report, rows)
    blocking_states = {
        "error", "alerta-local-modificado", "hash-remoto-no-coincide", "cambio-remoto-detectado"
    }
    blocked = [row for row in rows if row["estado"] in blocking_states]
    if discovery_errors:
        for error in discovery_errors:
            print(f"Error de descubrimiento {error['id']}: {error['error']}", file=sys.stderr)
    if not blocked and not discovery_errors and args.modo != "restaurar":
        write_csv(registry, rows)
        print(f"Indice actualizado: {registry}")
    elif not blocked and not discovery_errors:
        print(f"Restauracion verificada; indice sin cambios: {registry}")
    else:
        print("El indice versionado no se modifico porque existen alertas.", file=sys.stderr)
    print(f"Recursos procesados: {len(rows)}; alertas: {len(blocked) + len(discovery_errors)}")
    print(f"Reporte de ejecucion: {runtime_report}")
    return 1 if blocked or discovery_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
