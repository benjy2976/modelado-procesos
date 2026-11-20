"""Lectura de documentos del proceso y fuentes ya registradas por elemento."""

from __future__ import annotations

import hashlib
from pathlib import Path

from pypdf import PdfReader

from .repositorio import ErrorDominio, RepositorioProcesos


class ServicioDocumentos:
    def __init__(self, repositorio: RepositorioProcesos):
        self.repositorio = repositorio

    def documento_proceso(self, codigo: str, tipo: str) -> Path:
        if tipo not in {"tabla", "sustento"}:
            raise ErrorDominio("Tipo de documento no permitido", 404)
        ruta = self.repositorio.rutas(codigo)[tipo]
        if not ruta.is_file():
            raise ErrorDominio(f"El proceso {codigo} aun no tiene {tipo}", 404)
        return ruta

    def fuente(self, codigo: str, ref: str, indice: int) -> Path:
        referencias = self.repositorio.leer_modelo(codigo)["fuentes_visor"].get(ref)
        if referencias is None or indice < 0 or indice >= len(referencias):
            raise ErrorDominio("Fuente no registrada para el elemento", 404)
        ruta = referencias[indice]["ruta"]
        archivo = (self.repositorio.raiz / ruta).resolve()
        if (
            not archivo.is_relative_to(self.repositorio.raiz)
            or not ruta.startswith(("01-referencias/", "03-conocimiento/"))
            or not archivo.is_file()
            or archivo.suffix.lower() not in {".pdf", ".md", ".txt", ".html"}
        ):
            raise ErrorDominio("Fuente no disponible", 404)
        return archivo

    def leer_fuente(self, codigo: str, ref: str, indice: int) -> dict:
        """Extrae solo la página registrada; una página ausente queda pendiente."""
        archivo = self.fuente(codigo, ref, indice)
        registro = self.repositorio.leer_modelo(codigo)["fuentes_visor"][ref][indice]
        pagina = registro.get("pagina")
        texto = ""
        estado = "TEXTO_DISPONIBLE"
        if archivo.suffix.lower() == ".pdf":
            if pagina is None:
                estado = "PAGINA_NO_REGISTRADA"
            else:
                try:
                    lector = PdfReader(str(archivo), strict=False)
                    if pagina > len(lector.pages):
                        raise ErrorDominio("Página registrada fuera del PDF", 422)
                    texto = lector.pages[pagina - 1].extract_text() or ""
                    if not texto.strip():
                        estado = "SIN_TEXTO_EXTRAIBLE"
                except ErrorDominio:
                    raise
                except Exception as exc:
                    raise ErrorDominio("No se pudo leer la página PDF", 422) from exc
        else:
            texto = archivo.read_text(encoding="utf-8", errors="replace")
        fragmento = registro.get("fragmento", "")
        with archivo.open("rb") as lectura:
            huella = hashlib.file_digest(lectura, "sha256").hexdigest()
        return {
            "ruta": registro["ruta"],
            "titulo": registro.get("titulo", archivo.name),
            "pagina": pagina,
            "ubicacion": registro.get("ubicacion", ""),
            "fragmento": fragmento,
            "consulta": registro.get("consulta", ""),
            "vigencia": registro.get("vigencia", ""),
            "sha256": huella,
            "rectangulos": registro.get("rectangulos", []),
            "estado_ancla": registro.get("estado_ancla", "SIN_COORDENADAS"),
            "estado": estado,
            "coincidencia_fragmento": bool(fragmento and fragmento.casefold() in texto.casefold()),
            "texto": texto[:12000],
            "truncado": len(texto) > 12000,
        }
