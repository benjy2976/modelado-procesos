---
id: REF-RUBRICA-CALIDAD
tipo: guia
area: referencias
estado_documento: VIGENTE
clase_conocimiento: DECISION
proceso: []
fecha_creacion: 2026-10-15
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/referencias
---
# Rubrica de calidad documental

Cada recurso se evalua despues de descargarlo. Una pagina web localizada no demuestra que el archivo tenga OCR ni que sea la version vigente.

## Dimensiones

Cada dimension se puntua de 0 a 5.

| Dimension | 0 | 3 | 5 |
|---|---|---|---|
| Autoridad | Origen desconocido | Repositorio secundario confiable | Emisor oficial o diario oficial |
| Vigencia | Derogado o desconocido | Vigencia probable con dudas | Vigencia y modificatorias verificadas |
| Legibilidad automatica | Sin texto ni OCR | OCR parcial o con errores | Texto digital limpio y extraible |
| Estructura | Imagen desordenada | Titulos o tablas parcialmente recuperables | Articulos, titulos y tablas bien estructurados |
| Trazabilidad | Sin fecha ni identificador | Identificacion incompleta | Numero, fecha, emisor, URL y hash verificables |
| Aplicabilidad | No relacionada | Referencia complementaria | Regula directamente actividades del proceso |

## Resultado

- A: 26-30, fuente prioritaria y apta para agentes.
- B: 21-25, util con pequenas limitaciones.
- C: 16-20, requiere tratamiento o verificacion manual.
- D: 0-15, conservar como evidencia, pero no usar automaticamente sin correccion.

## Estado OCR

- `NATIVO`: contiene texto digital util.
- `OCR-BUENO`: imagen con OCR suficientemente confiable.
- `OCR-PARCIAL`: solo algunas paginas o zonas son utilizables.
- `SIN-OCR`: no contiene texto extraible.
- `NO-APLICA`: formato estructurado distinto de PDF.
- `PENDIENTE`: archivo aun no descargado o inspeccionado.

## Verificaciones tecnicas

1. Numero de paginas y paginas con texto.
2. Caracteres extraidos por pagina y porcentaje de paginas vacias.
3. Orden de lectura en columnas y tablas.
4. Busqueda de palabras de control.
5. Integridad visual mediante muestreo renderizado.
6. Presencia de firmas, anexos y sellos.
7. Hash SHA-256 y tamano.
8. Comparacion con la pagina oficial y sus modificatorias.
