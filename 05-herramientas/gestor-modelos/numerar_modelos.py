"""Asigna numeros de referencia persistentes a los elementos de una tabla BPMN."""

from __future__ import annotations

import argparse
from pathlib import Path


def numerar(tabla: Path) -> tuple[int, int]:
    texto = tabla.read_text(encoding='utf-8')
    lineas = texto.splitlines(keepends=True)
    dentro = False
    encabezado = None
    columna = None
    maximo = 0
    filas = []
    for indice, linea in enumerate(lineas):
        if linea.strip() == '## Elementos':
            dentro = True
            continue
        if dentro and linea.startswith('## '):
            break
        if not dentro or not linea.startswith('|'):
            continue
        celdas = [c.strip() for c in linea.strip().strip('|').split('|')]
        if encabezado is None:
            encabezado = indice
            columna = celdas.index('Numero') if 'Numero' in celdas else None
            continue
        if celdas[0].startswith('---'):
            continue
        filas.append((indice, celdas))
        if columna is not None and len(celdas) > columna and celdas[columna].isdigit():
            maximo = max(maximo, int(celdas[columna]))
    if encabezado is None:
        raise ValueError(f'Falta la tabla Elementos: {tabla}')
    nuevo = 0
    if columna is None:
        columna = 1
        for indice, linea in enumerate(lineas):
            if indice == encabezado:
                lineas[indice] = linea.replace('| ID |', '| ID | Numero |', 1)
            elif indice == encabezado + 1:
                lineas[indice] = linea.replace('|---|', '|---|---|', 1)
    vistos = set()
    for indice, celdas in filas:
        if len(celdas) <= columna or not celdas[columna].isdigit() or 'Numero' not in texto.splitlines()[encabezado]:
            maximo += 1
            numero = str(maximo)
            nuevo += 1
            if 'Numero' in texto.splitlines()[encabezado]:
                celdas[columna] = numero
                lineas[indice] = '| ' + ' | '.join(celdas) + ' |\n'
            else:
                lineas[indice] = lineas[indice].replace('| ' + celdas[0] + ' |',
                                                        '| ' + celdas[0] + ' | ' + numero + ' |', 1)
        else:
            numero = celdas[columna]
        if numero in vistos:
            raise ValueError(f'Numero duplicado {numero} en {tabla}')
        vistos.add(numero)
    if nuevo:
        tabla.write_text(''.join(lineas), encoding='utf-8', newline='')
    return len(filas), nuevo


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tabla', type=Path)
    args = parser.parse_args()
    total, nuevos = numerar(args.tabla)
    print(f'Numeracion: {total} elementos, {nuevos} numeros nuevos')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
