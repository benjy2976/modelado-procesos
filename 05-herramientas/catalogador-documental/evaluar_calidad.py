#!/usr/bin/env python3
"""Evalua integridad y aptitud tecnica de los recursos descargados.

No modifica originales ni aplica OCR. Los resultados son indicadores para
catalogacion; la vigencia juridica debe confirmarse mediante revision humana.
"""

from __future__ import annotations

import csv
import hashlib
import sys
import zipfile
from collections import Counter
from datetime import date
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
REGISTRO = ROOT / "01-referencias/00-catalogo/registro-descargas.csv"
SALIDA = ROOT / "01-referencias/00-catalogo/evaluacion-calidad-documental.csv"
RESUMEN = ROOT / "01-referencias/00-catalogo/resumen-calidad-documental.md"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def magic_ok(path: Path) -> tuple[bool, str]:
    head = path.read_bytes()[:8]
    ext = path.suffix.lower()
    if ext == ".pdf":
        return head.startswith(b"%PDF-"), "PDF"
    if ext in {".docx", ".xlsx", ".pptx"}:
        return head.startswith(b"PK"), "ZIP-OOXML"
    if ext == ".doc":
        return head.startswith(bytes.fromhex("D0CF11E0A1B11AE1")), "OLE-DOC"
    if ext == ".xls":
        return head.startswith(bytes.fromhex("D0CF11E0A1B11AE1")), "OLE-XLS"
    return len(head) > 0, "OTRO"


def eval_pdf(path: Path) -> dict[str, object]:
    reader = PdfReader(str(path), strict=False)
    pages = len(reader.pages)
    counts: list[int] = []
    errors = 0
    for page in reader.pages:
        try:
            counts.append(len((page.extract_text() or "").strip()))
        except Exception:
            counts.append(0)
            errors += 1
    text_pages = sum(n >= 20 for n in counts)
    chars = sum(counts)
    coverage = text_pages / pages if pages else 0
    avg = chars / pages if pages else 0
    if text_pages == 0:
        text_state, legibility, structure = "SIN-TEXTO_REQUIERE-OCR", 1, 1
    elif coverage < 0.80:
        text_state, legibility, structure = "TEXTO-PARCIAL_REVISAR-OCR", 2, 2
    elif avg < 150:
        text_state, legibility, structure = "TEXTO-ESCASO_REVISAR", 3, 3
    elif avg < 600:
        text_state, legibility, structure = "TEXTO-EXTRAIBLE", 4, 4
    else:
        text_state, legibility, structure = "TEXTO-EXTRAIBLE", 5, 4
    return {
        "paginas": pages,
        "paginas_con_texto": text_pages,
        "cobertura_texto_pct": round(coverage * 100, 1),
        "caracteres_extraidos": chars,
        "estado_texto": text_state,
        "legibilidad_0_5": legibility,
        "estructura_0_5": structure,
        "detalle_tecnico": f"errores_extraccion={errors}; promedio_caracteres_pagina={avg:.0f}",
    }


def eval_ooxml(path: Path) -> dict[str, object]:
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        names = archive.namelist()
        if bad:
            raise ValueError(f"entrada ZIP corrupta: {bad}")
    ext = path.suffix.lower()
    markers = {
        ".docx": "word/document.xml",
        ".xlsx": "xl/workbook.xml",
        ".pptx": "ppt/presentation.xml",
    }
    marker_ok = markers[ext] in names
    return {
        "paginas": "",
        "paginas_con_texto": "",
        "cobertura_texto_pct": "",
        "caracteres_extraidos": "",
        "estado_texto": "EDITABLE-OFFICE" if marker_ok else "OOXML-NO-RECONOCIDO",
        "legibilidad_0_5": 5 if marker_ok else 1,
        "estructura_0_5": 5 if marker_ok else 1,
        "detalle_tecnico": f"contenedor_zip=integro; entradas={len(names)}; marcador={marker_ok}",
    }


def vigencia_indicativa(source_id: str, filename: str) -> tuple[int, str]:
    """Puntaje documental, no dictamen juridico."""
    lower = filename.lower()
    if "consolid" in lower or "actualiz" in lower:
        return 4, "FECHA-DE-CORTE-IDENTIFICABLE_REVISAR-MODIFICATORIAS-POSTERIORES"
    if source_id.startswith("PRES-"):
        return 5, "EJERCICIO-2026_REVISAR-NORMAS-COMPLEMENTARIAS"
    if source_id.startswith("TEC-"):
        return 3, "COLECCION-TECNICA_REVISAR-MODIFICATORIAS-Y-TIPOLOGIA"
    return 4, "FUENTE-OFICIAL_VIGENCIA-JURIDICA-POR-CONFIRMAR"


def grade(total: int, usable: bool) -> str:
    if not usable:
        return "D-NO-UTILIZABLE"
    if total >= 27:
        return "A-ALTA"
    if total >= 23:
        return "B-ADECUADA"
    if total >= 18:
        return "C-CONDICIONADA"
    return "D-BAJA"


def main() -> int:
    rows = list(csv.DictReader(REGISTRO.open(encoding="utf-8-sig", newline="")))
    results: list[dict[str, object]] = []
    for source in rows:
        source_path = Path(source["archivo"])
        path = source_path if source_path.is_absolute() else ROOT / source_path
        flags: list[str] = []
        exists = path.exists()
        integrity, kind = (False, "AUSENTE")
        hash_match = False
        detail: dict[str, object] = {
            "paginas": "", "paginas_con_texto": "", "cobertura_texto_pct": "",
            "caracteres_extraidos": "", "estado_texto": "NO-EVALUADO",
            "legibilidad_0_5": 0, "estructura_0_5": 0, "detalle_tecnico": "",
        }
        if not exists:
            flags.append("ARCHIVO-AUSENTE")
        else:
            integrity, kind = magic_ok(path)
            if not integrity:
                flags.append("FORMATO-NO-COINCIDE")
            hash_match = sha256(path) == source["sha256"].upper()
            if not hash_match:
                flags.append("HASH-NO-COINCIDE")
            try:
                if integrity and path.suffix.lower() == ".pdf":
                    detail = eval_pdf(path)
                elif integrity and path.suffix.lower() in {".docx", ".xlsx", ".pptx"}:
                    detail = eval_ooxml(path)
                elif integrity:
                    detail.update({
                        "estado_texto": "FORMATO-BINARIO-NO-ANALIZADO",
                        "legibilidad_0_5": 2,
                        "estructura_0_5": 2,
                        "detalle_tecnico": "integridad superficial; requiere aplicacion especializada",
                    })
            except Exception as exc:
                flags.append("ERROR-LECTURA")
                detail["detalle_tecnico"] = f"{type(exc).__name__}: {exc}"
            if path.stat().st_size < 10_000:
                flags.append("ARCHIVO-MUY-PEQUENO_REVISAR")
        if "REQUIERE-OCR" in str(detail["estado_texto"]):
            flags.append("OCR-REQUERIDO-EN-DERIVADO")
        elif "REVISAR-OCR" in str(detail["estado_texto"]):
            flags.append("OCR-PARCIAL-A-EVALUAR")

        current_score, current_state = vigencia_indicativa(source["id_fuente"], path.name)
        authority = 5
        traceability = 5 if source["url_final"] and source["sha256"] else 2
        applicability = int(source["aplicabilidad_0_5"] or 0)
        total = authority + current_score + int(detail["legibilidad_0_5"]) + int(detail["estructura_0_5"]) + traceability + applicability
        usable = exists and integrity and hash_match and "ERROR-LECTURA" not in flags
        results.append({
            "fecha_evaluacion": date.today().isoformat(),
            "id_fuente": source["id_fuente"],
            "archivo": path.resolve().relative_to(ROOT).as_posix(),
            "extension": path.suffix.lower(),
            "tamano_bytes": source["tamano_bytes"],
            "formato_detectado": kind,
            "integridad_formato": "OK" if integrity else "FALLA",
            "hash_coincide": "SI" if hash_match else "NO",
            **detail,
            "autoridad_0_5": authority,
            "vigencia_indicativa_0_5": current_score,
            "estado_vigencia": current_state,
            "trazabilidad_0_5": traceability,
            "aplicabilidad_0_5": applicability,
            "puntaje_total_30": total,
            "calificacion": grade(total, usable),
            "alertas": " | ".join(flags),
            "url_oficial": source["url_final"],
            "sha256": source["sha256"],
        })

    fields = list(results[0].keys()) if results else []
    with SALIDA.open("w", encoding="utf-8-sig", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    grades = Counter(str(r["calificacion"]) for r in results)
    states = Counter(str(r["estado_texto"]) for r in results)
    integrity_failures = [r for r in results if r["integridad_formato"] != "OK" or r["hash_coincide"] != "SI"]
    unreadable = [r for r in results if "OCR-REQUERIDO" in str(r["alertas"])]
    partial = [r for r in results if "OCR-PARCIAL" in str(r["alertas"])]
    report = [
        "# Resumen de calidad documental",
        "",
        f"- Fecha de evaluacion: {date.today().isoformat()}",
        f"- Archivos evaluados: {len(results)}",
        f"- Fallas de integridad o hash: {len(integrity_failures)}",
        f"- PDF sin texto que requieren OCR en copia derivada: {len(unreadable)}",
        f"- PDF con texto parcial que requieren revision: {len(partial)}",
        "- Alcance: evaluacion automatica de integridad, extraccion de texto y trazabilidad; no constituye dictamen de vigencia juridica ni revision visual exhaustiva.",
        "",
        "## Calificaciones",
        "",
    ]
    report.extend(f"- {key}: {value}" for key, value in sorted(grades.items()))
    report += ["", "## Estado de texto", ""]
    report.extend(f"- {key}: {value}" for key, value in sorted(states.items()))
    report += ["", "## Archivos que requieren OCR", ""]
    if unreadable:
        report.extend(f"- `{r['archivo']}`" for r in unreadable)
    else:
        report.append("- Ninguno.")
    report += ["", "## Archivos con texto parcial", ""]
    if partial:
        report.extend(f"- `{r['archivo']}`" for r in partial)
    else:
        report.append("- Ninguno.")
    report += ["", "## Fallas de integridad", ""]
    if integrity_failures:
        report.extend(f"- `{r['archivo']}`: {r['alertas']}" for r in integrity_failures)
    else:
        report.append("- Ninguna.")
    report += [
        "", "## Criterio de uso", "",
        "Los puntajes permiten priorizar revision. Antes de citar una obligacion se debe confirmar vigencia, modificatorias y ubicacion precisa en la fuente oficial. El OCR, cuando corresponda, debe aplicarse solo a una copia ubicada en `derivados/`.",
        "",
    ]
    RESUMEN.write_text("\n".join(report), encoding="utf-8")
    print(f"Evaluados: {len(results)}")
    print(f"Integridad/hash con fallas: {len(integrity_failures)}")
    print(f"Sin texto/OCR: {len(unreadable)}")
    print(f"Texto parcial: {len(partial)}")
    print(f"CSV: {SALIDA}")
    print(f"Resumen: {RESUMEN}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
