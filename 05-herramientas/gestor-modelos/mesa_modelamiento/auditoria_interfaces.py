"""Contraste determinista de interfaces entre un proceso padre, sus hijos y los hermanos entre sí.

Produce candidatos a discrepancia, no conclusiones: si una diferencia de nombres o de disparo es material
lo decide quien audita, con el contexto del modelo y de las fuentes.
"""

from __future__ import annotations

import re
import unicodedata
from datetime import UTC, datetime
from pathlib import Path

from .auditoria import _tabla, carpeta_auditoria
from .fuentes_preparacion import _guardar, _sha256
from .repositorio import ErrorDominio, RepositorioProcesos

CODIGO_EN_NOMBRE = re.compile(r"^(S\d+(?:\.\d+)+)\b")
DISPARO = {"subproceso-evento-temporizador": "inicio-temporizador", "subproceso-evento-mensaje": "inicio-mensaje",
           "subproceso-evento-condicional": "inicio-condicional"}  # fmt: skip
VACIAS = set("a al con de del el en la las lo los o para por que se su sus un una y segun".split())


def _raices(texto: str) -> set[str]:
    """Raíces de cinco letras de las palabras con contenido, para comparar nombres de eventos."""
    plano = "".join(c for c in unicodedata.normalize("NFKD", texto) if not unicodedata.combining(c)).casefold()
    return {p[:5] for p in re.findall(r"[a-z0-9]+", plano) if len(p) > 3 and p not in VACIAS}


def _corresponde(a: set[str], b: set[str]) -> bool:
    """Coinciden al menos la mitad de las raíces del nombre más corto; una palabra genérica no basta."""
    if not a or not b:
        return False
    return len(a & b) >= max(1, -(-min(len(a), len(b)) // 2))


def _modelo(repositorio: RepositorioProcesos, codigo: str) -> dict | None:
    tabla = repositorio.rutas(codigo)["tabla"]
    if not tabla.is_file():
        return None
    texto = tabla.read_text(encoding="utf-8")
    elementos = _tabla(texto, "Elementos")
    return {
        "tabla": tabla,
        "elementos": elementos,
        "mensajes": _tabla(texto, "Mensajes"),
        "inicios": [e for e in elementos if e.get("Tipo", "").startswith("inicio")],
        "fines": [e for e in elementos if e.get("Tipo", "").startswith("fin")],
    }


def _hijos(repositorio: RepositorioProcesos, codigo: str) -> list[str]:
    def buscar(nodo: dict) -> dict | None:
        if nodo.get("codigo") == codigo:
            return nodo
        return next((h for h in (buscar(n) for n in nodo.get("hijos", [])) if h), None)

    nodo = buscar(repositorio.arbol())
    if nodo is None:
        raise ErrorDominio(f"Proceso {codigo} no encontrado en el árbol", 404)
    return [h["codigo"] for h in nodo.get("hijos", [])]


def _candidato(tipo: str, hijo: str, detalle: str, **extra) -> dict:
    return {"tipo": tipo, "hijo": hijo, "detalle": detalle, **extra}


def _salidas(elemento: dict, hijo: str, modelo: dict) -> list[dict]:
    salida = re.search(r"sale:\s*([^;|]+)", elemento.get("Documentos", ""))
    if not salida or any(_corresponde(_raices(salida.group(1)), _raices(f.get("Nombre", ""))) for f in modelo["fines"]):
        return []
    fines = [f.get("Nombre", "") for f in modelo["fines"]]
    return [_candidato("SALIDA-NO-REPRESENTADA", hijo, f"El padre declara la salida «{salida.group(1).strip()}»; "
                       f"ningún fin del hijo la nombra: {fines}")]  # fmt: skip


def _secuencia(padre: dict, modelos: dict, por_id: dict) -> list[dict]:
    """Entre hijos consecutivos del padre, el fin de uno debería corresponder a un inicio del siguiente."""
    candidatos = []
    for origen, hijo_a in por_id.items():
        siguientes = re.findall(
            r"([A-Za-z0-9-]+)", next(e for e in padre["elementos"] if e["ID"] == origen)["Siguiente"]
        )
        for destino in (s for s in siguientes if s in por_id):
            hijo_b = por_id[destino]
            a, b = modelos.get(hijo_a), modelos.get(hijo_b)
            if not a or not b:
                continue
            parejas = [(f, i) for f in a["fines"] for i in b["inicios"]]
            if not any(_corresponde(_raices(f.get("Nombre", "")), _raices(i.get("Nombre", ""))) for f, i in parejas):
                candidatos.append(_candidato(
                    "SECUENCIA-SIN-CORRESPONDENCIA", hijo_b,
                    f"Fines de {hijo_a}: {[f.get('Nombre') for f in a['fines']]}; inicios de {hijo_b}: "
                    f"{[i.get('Nombre') for i in b['inicios']]}", origen=hijo_a,
                ))  # fmt: skip
    return candidatos


def _reciprocidad(modelos: dict) -> list[dict]:
    """Un mensaje que un hijo dirige a un hermano (o recibe de él) debería figurar también en el hermano."""
    candidatos = []
    for hijo, modelo in modelos.items():
        if not modelo:
            continue
        for mensaje in modelo["mensajes"]:
            for extremo in ("Desde", "Hacia"):
                otro = CODIGO_EN_NOMBRE.match(mensaje.get(extremo, ""))
                if not otro or otro.group(1) not in modelos or not modelos[otro.group(1)]:
                    continue
                contraparte = modelos[otro.group(1)]
                if not any(hijo in m.get("Desde", "") + m.get("Hacia", "") for m in contraparte["mensajes"]):
                    sentido = "recibe de" if extremo == "Desde" else "envía a"
                    candidatos.append(_candidato(
                        "MENSAJE-SIN-CONTRAPARTE", hijo,
                        f"{hijo} {sentido} {otro.group(1)} «{mensaje.get('Nombre', '')}», pero {otro.group(1)} "
                        f"no registra ese intercambio", hermano=otro.group(1),
                    ))  # fmt: skip
    return candidatos


def comparar_interfaces(raiz: Path, codigo: str) -> dict:
    """Candidatos a discrepancia entre el padre y sus hijos; se guardan junto a la auditoría del padre."""
    raiz = raiz.resolve()
    repositorio = RepositorioProcesos(raiz)
    padre = _modelo(repositorio, codigo)
    if padre is None:
        raise ErrorDominio(f"{codigo} no tiene tabla de modelo (SIN-MODELO)", 404)
    hijos = _hijos(repositorio, codigo)
    modelos = {h: _modelo(repositorio, h) for h in hijos}
    por_id = {}
    candidatos = []
    for elemento in padre["elementos"]:
        if not elemento.get("Tipo", "").startswith("subproceso"):
            continue
        codigo_hijo = CODIGO_EN_NOMBRE.match(elemento.get("Nombre", ""))
        if not codigo_hijo:
            continue
        hijo = codigo_hijo.group(1)
        por_id[elemento["ID"]] = hijo
        modelo = modelos.get(hijo)
        if hijo not in modelos:
            candidatos.append(
                _candidato("ELEMENTO-SIN-HIJO", hijo, f"{elemento['ID']} nombra un proceso que no es hijo")
            )
            continue
        if modelo is None:
            candidatos.append(
                _candidato("HIJO-SIN-MODELO", hijo, "El hijo no tiene tabla; su interfaz no se contrasta")
            )
            continue
        esperado = DISPARO.get(elemento["Tipo"])
        if esperado and not any(i.get("Tipo") == esperado for i in modelo["inicios"]):
            tipos = sorted({i.get("Tipo") for i in modelo["inicios"]})
            candidatos.append(_candidato("TIPO-DE-DISPARO", hijo, f"El padre lo dispara como {elemento['Tipo']}; "
                                         f"el hijo no tiene {esperado} (inicios: {tipos})"))  # fmt: skip
        candidatos += _salidas(elemento, hijo, modelo)
    for hijo in hijos:
        if hijo not in por_id.values():
            candidatos.append(
                _candidato("HIJO-SIN-ELEMENTO", hijo, "El hijo existe en el árbol pero el padre no lo modela")
            )
    candidatos += _secuencia(padre, modelos, por_id)
    candidatos += _reciprocidad(modelos)
    resultado = {
        "codigo": codigo,
        "revision_tabla": _sha256(padre["tabla"]),
        "revisiones_hijos": {h: _sha256(m["tabla"]) for h, m in modelos.items() if m},
        "fecha": datetime.now(UTC).isoformat(timespec="seconds"),
        "hijos": hijos,
        "candidatos": candidatos,
    }
    _guardar(carpeta_auditoria(raiz, codigo) / "interfaces.json", resultado)
    return {**resultado, "total": len(candidatos)}
