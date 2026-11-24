---
tipo: mapa-de-contenido
area: derivados-texto
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
aliases:
  - Derivados de texto
tags:
  - tema/referencias
---

# Derivados de texto

Sube a: [Referencias](../00-REFERENCIAS.md)

El subdirectorio `cache/` se crea localmente para las extracciones Markdown reproducibles. Su contenido no se versiona y puede regenerarse desde los originales mediante el extractor documental previsto en `05-herramientas/extractor-documental/00-extractor-documental.md`.

La herramienta `modelador-procesos fuentes indice` genera `cache/00-indice.md`, una tabla por carpeta con enlaces al original y a su texto derivado. Los PDF se marcan por pagina fisica; los DOCX por parrafo y numeral; los PPTX por diapositiva. Los XLSX no se transcriben y solo tienen una ficha de inventario en `cache/preparacion-office.json`. La consulta acotada agrega `cache/segmentos/` (fragmentos por articulo, numeral o bloque), `cache/segmentacion.json`, el indice local `cache/indice-fuentes.sqlite` y las sugerencias de temas `cache/temas-sugeridos.jsonl`; todo es regenerable con la CLI.

Una extraccion facilita la busqueda y el trabajo con IA, pero no sustituye el original ni constituye conocimiento validado. Las reglas curadas se almacenan en `03-conocimiento/`.
