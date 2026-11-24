"""Construye un solo modelo por codigo NT, con numeracion, tiempos y cache local."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from time import perf_counter

from numerar_modelos import numerar
from renderizar_plantuml import REPO_ROOT

AQUI = Path(__file__).resolve().parent
CACHE = REPO_ROOT / '99-temporal' / 'modelos' / 'cache-focalizado'


def localizar(codigo: str) -> Path:
    buscado = codigo.upper().replace('.', '-')
    candidatos = list((REPO_ROOT / '02-procesos').rglob(f'{buscado}-diagrama-proceso-tabla.md'))
    if len(candidatos) != 1:
        raise ValueError(f'{codigo}: se esperaban una tabla y se encontraron {len(candidatos)}')
    return candidatos[0]


def huella(tabla: Path) -> str:
    digest = hashlib.sha256()
    # El HTML incrusta las anclas del visor: un cambio en fuentes-visor.json debe invalidar la caché.
    visor = tabla.with_name(tabla.name.replace('-diagrama-proceso-tabla.md', '-fuentes-visor.json'))
    insumos = [tabla, *([visor] if visor.is_file() else []), *(AQUI.glob('*.py')), AQUI / 'bpmn-js.lock.json',
               AQUI / 'vendor' / 'bpmn-navigated-viewer-17.11.1.production.min.js']
    for ruta in sorted(insumos):
        digest.update(str(ruta.relative_to(REPO_ROOT)).encode('utf-8'))
        digest.update(ruta.read_bytes())
    return digest.hexdigest()


def productos(tabla: Path, imagenes: bool = False) -> list[Path]:
    base = tabla.name.removesuffix('-tabla.md')
    sufijos = ('.bpmn', '.html', '.svg', '.png') if imagenes else ('.bpmn', '.html')
    return [tabla.with_name(base + sufijo) for sufijo in sufijos]


def estado(tabla: Path, firma: str, imagenes: bool = False) -> dict:
    return {'firma': firma, 'productos': {str(p.relative_to(REPO_ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                                           for p in productos(tabla, imagenes)}}


def vigente(tabla: Path, guardado: dict, firma: str, imagenes: bool = False) -> bool:
    if guardado.get('firma') != firma:
        return False
    hashes = guardado.get('productos', {})
    for p in productos(tabla, imagenes):
        ruta = str(p.relative_to(REPO_ROOT))
        hash_esperado = hashes.get(ruta)
        if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != hash_esperado:
            return False
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('codigo', help='Codigo de proceso, p. ej. S4.3.2.4 o S4-3-2-4')
    parser.add_argument('--sin-cache', action='store_true')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--forzar', action='store_true', help='Adopta hallazgos ya justificados en el sustento')
    parser.add_argument('--exportar-imagenes', action='store_true', help='Genera SVG y PNG para publicacion')
    args = parser.parse_args()
    inicio = perf_counter()
    try:
        tabla = localizar(args.codigo)
        if not args.check:
            total, nuevos = numerar(tabla)
            print(f'Numeracion: {total} elementos, {nuevos} nuevos', flush=True)
        firma = huella(tabla)
        CACHE.mkdir(parents=True, exist_ok=True)
        archivo = CACHE / (tabla.stem + '.json')
        guardado = json.loads(archivo.read_text(encoding='utf-8')) if archivo.is_file() else {}
        if not args.check and not args.sin_cache and vigente(tabla, guardado, firma, args.exportar_imagenes):
            print(f'OK CACHE: {args.codigo} ({perf_counter() - inicio:.2f} s)')
            return 0
        comando = [sys.executable, str(AQUI / 'construir_modelos.py'), '--tabla', str(tabla)]
        if args.check:
            comando.append('--check')
        if args.forzar:
            comando.append('--forzar')
        if args.exportar_imagenes:
            comando.append('--exportar-imagenes')
        resultado = subprocess.run(comando, cwd=REPO_ROOT, check=False)
        if resultado.returncode:
            return resultado.returncode
        if not args.check:
            archivo.write_text(json.dumps(estado(tabla, firma, args.exportar_imagenes), indent=2) + '\n', encoding='utf-8')
        print(f'Tiempo total {args.codigo}: {perf_counter() - inicio:.2f} s')
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.exit(2, f'ERROR: {error}\n')


if __name__ == '__main__':
    raise SystemExit(main())
