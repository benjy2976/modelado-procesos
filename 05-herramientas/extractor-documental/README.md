---
tipo: guia
area: herramientas
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# Requisitos del extractor documental

[Inicio](../../00-inicio.md) · [Herramientas](../README.md)

## Objetivo

Generar una cache Markdown reproducible para busqueda, recuperacion de contexto y revision asistida, sin convertir el texto extraido en fuente oficial.

## Entrada y salida

- Entrada: documento identificado en `01-referencias/00-catalogo/registro-descargas.csv` o `catalogo-documental.csv`.
- Salida local: `01-referencias/09-derivados-texto/cache/<id-documento>/<sha256-corto>.md`.
- Metadatos: plantilla `00-gobernanza/plantillas/conocimiento/texto-extraido.md`.
- Fuente de verdad: el original cuyo SHA-256 aparece en el encabezado.

La cache completa no se versiona. Se regenera desde los originales restaurados. Las correcciones intelectuales, reglas y citas seleccionadas se conservan en el area de conocimiento versionada.

## Reglas de extraccion

1. Medir primero si el documento posee texto aprovechable.
2. Aplicar OCR solo a una copia derivada, nunca al original.
3. Conservar el orden de paginas y agregar `<!-- pagina_pdf: N -->`.
4. Registrar por separado la pagina impresa cuando pueda identificarse con certeza.
5. Marcar tablas, imagenes, formulas, notas o columnas cuyo orden no sea confiable.
6. No corregir silenciosamente el contenido; toda normalizacion debe declararse.
7. Registrar herramienta, version, fecha, hash del original y hash de la extraccion.
8. Permitir extraccion selectiva por paginas para no entregar documentos completos a una tarea de IA.
9. El resultado debe poder regenerarse de forma determinista en la medida permitida por el motor usado.

## Estados de calidad

- `SIN-REVISAR`: salida automatica.
- `REVISADO-PARCIAL`: se comprobaron las paginas usadas, no el documento completo.
- `REVISADO-COMPLETO`: se contrasto todo el texto con el original.
- `NO-CONFIABLE`: la estructura, OCR o contenido impide utilizar la extraccion sin lectura directa del original.

El estado se refiere a fidelidad de extraccion, no a vigencia ni interpretacion juridica.

La extraccion es una etapa del [Manual operativo del conocimiento](../../00-gobernanza/manual-operativo-del-conocimiento.md) y alimenta [Conocimiento estructurado](../../03-conocimiento/README.md).

## Criterios de aceptacion

- La extraccion identifica inequivocamente el original y su hash.
- Cada fragmento recuperado conserva pagina PDF.
- Una pagina con baja confianza puede localizarse rapidamente en el original.
- El extractor no modifica el catalogo normativo ni crea reglas `VALIDADO`.
- El mismo comando puede reconstruir una extraccion ausente despues de clonar y restaurar la biblioteca.
