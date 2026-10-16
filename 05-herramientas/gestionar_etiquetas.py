"""Gestiona las etiquetas de la boveda segun el vocabulario controlado (DEC-019).

El vocabulario vive en 00-gobernanza/vocabulario-etiquetas.yaml. Las etiquetas
`proceso/...` se derivan de las carpetas de 02-procesos o de la propiedad
`codigo_proceso`; las de `tema/...` deben pertenecer al vocabulario.

Uso, desde la raiz del repositorio:

    python 05-herramientas/gestionar_etiquetas.py revisar
    python 05-herramientas/gestionar_etiquetas.py aplicar
    python 05-herramientas/gestionar_etiquetas.py renombrar tema/viejo tema/nuevo
    python 05-herramientas/gestionar_etiquetas.py listar

`revisar` no modifica archivos y devuelve 1 si encuentra problemas. `aplicar`
aplica los renombres registrados, deriva la etiqueta de proceso y agrega el tema
por ruta cuando la nota no tiene ninguno; no elimina temas asignados a mano.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
VOCABULARIO = ROOT / "00-gobernanza" / "vocabulario-etiquetas.yaml"
PROCESOS = "02-procesos/"
CODIGO_CARPETA = re.compile(r"^([SEM]\d+(?:-\d+)*)-")
ETIQUETA_VALIDA = re.compile(r"^[a-z0-9-]+(?:/[a-z0-9-]+)*$")


# ---------------------------------------------------------------- vocabulario

def cargar_vocabulario() -> dict:
    return yaml.safe_load(VOCABULARIO.read_text(encoding="utf-8"))


def guardar_vocabulario(vocabulario: dict) -> None:
    texto = yaml.safe_dump(vocabulario, allow_unicode=True, sort_keys=False, width=100)
    VOCABULARIO.write_text(texto, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- notas

def notas(vocabulario: dict) -> list[str]:
    salida = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "*.md"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    excluir = tuple(vocabulario.get("excluir", []))
    return sorted(n for n in salida if (ROOT / n).is_file() and not n.startswith(excluir) and n not in excluir)


class Nota:
    """Nota Markdown con edicion minima del bloque de propiedades."""

    def __init__(self, rel: str) -> None:
        self.rel = rel
        with open(ROOT / rel, encoding="utf-8", newline="") as fh:
            self.texto = fh.read()
        self.nl = "\r\n" if "\r\n" in self.texto else "\n"
        lineas = self.texto.split(self.nl)
        self.propiedades: list[str] | None = None
        if lineas and lineas[0] == "---" and "---" in lineas[1:]:
            fin = lineas.index("---", 1)
            self.propiedades = lineas[1:fin]
            self.cuerpo = lineas[fin + 1:]

    def valor(self, clave: str) -> str | None:
        for linea in self.propiedades or []:
            if linea.startswith(clave + ":"):
                valor = linea.split(":", 1)[1].strip()
                return None if valor in ("", "null") else valor
        return None

    def etiquetas(self) -> list[str]:
        lineas = self.propiedades or []
        for i, linea in enumerate(lineas):
            if linea.startswith("tags:"):
                resto = linea[5:].strip()
                if resto.startswith("["):
                    return [e.strip().strip("'\"") for e in resto.strip("[]").split(",") if e.strip()]
                valores = []
                for siguiente in lineas[i + 1:]:
                    if siguiente.startswith(("  - ", "- ")):
                        valores.append(siguiente.split("- ", 1)[1].strip().strip("'\""))
                    else:
                        break
                return valores
        return []

    def fijar_etiquetas(self, valores: list[str]) -> None:
        lineas = self.propiedades
        assert lineas is not None
        nuevo = ["tags:"] + [f"  - {v}" for v in valores] if valores else ["tags: []"]
        for i, linea in enumerate(lineas):
            if linea.startswith("tags:"):
                fin = i + 1
                if not linea[5:].strip():
                    while fin < len(lineas) and (lineas[fin].startswith(("  - ", "- "))):
                        fin += 1
                lineas[i:fin] = nuevo
                return
        lineas.extend(nuevo)

    def guardar(self) -> bool:
        texto = self.nl.join(["---", *self.propiedades, "---", *self.cuerpo])
        if texto == self.texto:
            return False
        with open(ROOT / self.rel, "w", encoding="utf-8", newline="") as fh:
            fh.write(texto)
        self.texto = texto
        return True


# ---------------------------------------------------------------- derivacion

def cadena_desde_carpetas(rel: str) -> list[str]:
    if not rel.startswith(PROCESOS):
        return []
    codigos = []
    for parte in rel.split("/")[1:-1]:
        coincidencia = CODIGO_CARPETA.match(parte)
        if coincidencia:
            codigos.append(coincidencia.group(1))
    return codigos


def cadena_desde_codigo(codigo: str) -> list[str]:
    partes = codigo.strip().upper().split(".")
    return ["-".join(partes[: i + 1]) for i in range(len(partes))]


def etiqueta_proceso(cadena: list[str]) -> str | None:
    return "proceso/" + "/".join(c.lower() for c in cadena) if cadena else None


def etiquetas_de_proceso_existentes() -> set[str]:
    existentes = set()
    for carpeta in (ROOT / PROCESOS).rglob("*"):
        if carpeta.is_dir():
            rel = carpeta.relative_to(ROOT).as_posix() + "/x.md"
            etiqueta = etiqueta_proceso(cadena_desde_carpetas(rel))
            if etiqueta:
                existentes.add(etiqueta)
    return existentes


def proceso_esperado(nota: Nota) -> str | None:
    cadena = cadena_desde_carpetas(nota.rel)
    if not cadena and nota.valor("codigo_proceso"):
        cadena = cadena_desde_codigo(nota.valor("codigo_proceso"))
    return etiqueta_proceso(cadena)


def tema_por_ruta(rel: str, vocabulario: dict) -> str:
    for regla in vocabulario["temas_por_ruta"]:
        if rel.startswith(regla["prefijo"]):
            return "tema/" + regla["tema"]
    raise ValueError(rel)


# ---------------------------------------------------------------- comandos

def revisar(vocabulario: dict) -> int:
    temas = {"tema/" + t for t in vocabulario["espacios"]["tema"]["valores"]}
    renombres = vocabulario.get("renombres") or {}
    procesos = etiquetas_de_proceso_existentes()
    problemas = []
    for rel in notas(vocabulario):
        nota = Nota(rel)
        if nota.propiedades is None:
            problemas.append((rel, "sin propiedades YAML"))
            continue
        etiquetas = nota.etiquetas()
        for etiqueta in etiquetas:
            if etiqueta in renombres:
                problemas.append((rel, f"etiqueta renombrada pendiente de aplicar: {etiqueta} -> {renombres[etiqueta]}"))
            elif not ETIQUETA_VALIDA.match(etiqueta):
                problemas.append((rel, f"formato invalido (minusculas, numeros y guiones): {etiqueta}"))
            elif etiqueta.startswith("tema/") and etiqueta not in temas:
                problemas.append((rel, f"tema fuera del vocabulario: {etiqueta}"))
            elif etiqueta.startswith("proceso/") and etiqueta not in procesos:
                problemas.append((rel, f"proceso inexistente en 02-procesos: {etiqueta}"))
            elif etiqueta.split("/", 1)[0] not in vocabulario["espacios"]:
                problemas.append((rel, f"espacio de etiquetas no definido: {etiqueta}"))
        if not any(e.startswith("tema/") for e in etiquetas):
            problemas.append((rel, "sin etiqueta tema/"))
        de_proceso = [e for e in etiquetas if e.startswith("proceso/")]
        esperado = proceso_esperado(nota)
        if len(de_proceso) > 1:
            problemas.append((rel, f"mas de una etiqueta de proceso: {de_proceso}"))
        if esperado and de_proceso != [esperado]:
            problemas.append((rel, f"etiqueta de proceso esperada: {esperado}"))
        codigo = nota.valor("codigo_proceso")
        carpetas = cadena_desde_carpetas(rel)
        if codigo and carpetas and cadena_desde_codigo(codigo) != carpetas:
            problemas.append((rel, f"codigo_proceso {codigo} no coincide con las carpetas {'/'.join(carpetas)}"))
    for rel, problema in problemas:
        print(f"{rel}: {problema}")
    print(f"Notas revisadas: {len(notas(vocabulario))}; problemas: {len(problemas)}")
    return 1 if problemas else 0


def aplicar(vocabulario: dict) -> int:
    renombres = vocabulario.get("renombres") or {}
    modificadas = 0
    for rel in notas(vocabulario):
        nota = Nota(rel)
        if nota.propiedades is None:
            print(f"OMITIDA (sin propiedades): {rel}")
            continue
        etiquetas = [renombres.get(e, e) for e in nota.etiquetas()]
        esperado = proceso_esperado(nota)
        if esperado:
            etiquetas = [e for e in etiquetas if not e.startswith("proceso/")] + [esperado]
        if not any(e.startswith("tema/") for e in etiquetas):
            etiquetas.insert(0, tema_por_ruta(rel, vocabulario))
        unicas = list(dict.fromkeys(etiquetas))
        temas = [e for e in unicas if e.startswith("tema/")]
        resto = [e for e in unicas if not e.startswith("tema/")]
        nota.fijar_etiquetas(temas + resto)
        if nota.guardar():
            modificadas += 1
            print(f"actualizada: {rel}")
    print(f"Notas actualizadas: {modificadas}")
    return 0


def renombrar(vocabulario: dict, viejo: str, nuevo: str) -> int:
    for etiqueta in (viejo, nuevo):
        if not ETIQUETA_VALIDA.match(etiqueta) or "/" not in etiqueta:
            sys.exit(f"ERROR: etiqueta invalida: {etiqueta}")
    espacio_viejo, valor_viejo = viejo.split("/", 1)
    espacio_nuevo, valor_nuevo = nuevo.split("/", 1)
    if espacio_viejo == "tema":
        valores = vocabulario["espacios"]["tema"]["valores"]
        if valor_viejo not in valores:
            sys.exit(f"ERROR: {viejo} no esta en el vocabulario")
        if espacio_nuevo != "tema":
            sys.exit("ERROR: un tema solo puede renombrarse dentro del espacio tema/")
        vocabulario["espacios"]["tema"]["valores"] = {
            (valor_nuevo if k == valor_viejo else k): v for k, v in valores.items()
        }
        for regla in vocabulario["temas_por_ruta"]:
            if regla["tema"] == valor_viejo:
                regla["tema"] = valor_nuevo
    renombres = vocabulario.get("renombres") or {}
    renombres = {k: (nuevo if v == viejo else v) for k, v in renombres.items()}
    renombres[viejo] = nuevo
    vocabulario["renombres"] = renombres
    guardar_vocabulario(vocabulario)
    modificadas = 0
    for rel in notas(vocabulario):
        nota = Nota(rel)
        if nota.propiedades is None:
            continue
        etiquetas = [nuevo + e[len(viejo):] if e == viejo or e.startswith(viejo + "/") else e for e in nota.etiquetas()]
        nota.fijar_etiquetas(list(dict.fromkeys(etiquetas)))
        if nota.guardar():
            modificadas += 1
    print(f"Renombrada {viejo} -> {nuevo} en {modificadas} notas y registrada en el vocabulario.")
    return 0


def listar(vocabulario: dict) -> int:
    conteo = Counter()
    for rel in notas(vocabulario):
        nota = Nota(rel)
        conteo.update(nota.etiquetas())
    for etiqueta, cantidad in sorted(conteo.items()):
        print(f"{cantidad:4d}  {etiqueta}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="comando", required=True)
    sub.add_parser("revisar", help="comprueba etiquetas sin modificar archivos")
    sub.add_parser("aplicar", help="aplica renombres, deriva procesos y agrega temas por ruta")
    renombre = sub.add_parser("renombrar", help="renombra una etiqueta en el vocabulario y en todas las notas")
    renombre.add_argument("viejo")
    renombre.add_argument("nuevo")
    sub.add_parser("listar", help="cuenta las etiquetas en uso")
    args = parser.parse_args()
    vocabulario = cargar_vocabulario()
    if args.comando == "revisar":
        return revisar(vocabulario)
    if args.comando == "aplicar":
        return aplicar(vocabulario)
    if args.comando == "renombrar":
        return renombrar(vocabulario, args.viejo, args.nuevo)
    return listar(vocabulario)


if __name__ == "__main__":
    raise SystemExit(main())
