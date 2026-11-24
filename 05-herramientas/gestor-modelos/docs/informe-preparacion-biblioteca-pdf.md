---
id: HER-MESA-MODELAMIENTO-INFORME-PREPARACION-PDF
tipo: informe
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
proceso: []
fecha_creacion: 2026-11-24
fecha_actualizacion: 2026-11-24
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Preparación de la biblioteca PDF: fases 1 y 2

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md). El procedimiento y las fases posteriores constan en el [plan de corrida](plan-corrida-documental-y-auditoria.md).

## Inventario y diagnóstico

La corrida del 24 de noviembre de 2026 encontró 181 PDF, 9383 páginas y cero errores de apertura o extracción en el diagnóstico. Todos los archivos presentes tienen entrada en el catálogo documental o en el registro de descargas; los hashes registrados coinciden y no hay rutas catalogadas faltantes. El inventario detectó cuatro pares de archivos con SHA-256 idéntico pese a estar guardados bajo nombres distintos. Esto es una alerta de catalogación, no una deduplicación automática.

Con el umbral inicial de 80 caracteres nativos por página, 132 PDF se clasificaron `NATIVO`, 43 `OCR-PARCIAL` y 6 `OCR-INTEGRAL`. Hay 603 páginas candidatas a OCR. La medición solo decide el método de extracción: una página con texto puede tener errores de orden de lectura, tablas o contenido incompleto.

Los cuatro pares con bytes idénticos son `TEC-001` E.031/E.040, `TEC-001` E.050/EM.020, `BIM-005`/`BIM-005A` y `BIM-002`/`BIM-002A`. En los dos primeros, nombres de normas diferentes apuntan al mismo contenido; requieren cotejo de catálogo antes de usarse como sustento. `TEC-001` también identifica varios PDF y no basta por sí solo para seleccionar uno. La prioridad textual provisional de S4.3.2 marcó cinco archivos citados en 18 tablas y sustentos, pero un ID repetido como `CON-001` tampoco distingue por sí solo la ley del reglamento.

## Extracción y límites

La extracción nativa produjo Markdown paginado para los 181 PDF. El manifiesto y los textos masivos están en `01-referencias/09-derivados-texto/cache/`, fuera de Git; se regeneran con la CLI. Cada texto conserva ID, ruta y hash del original, método, fecha y marcador de página física. Los originales no se modificaron.

La cola OCR usa una copia derivada de cada lote de páginas y el MCP local del equipo. Por defecto se envían archivos con URL pública HTTPS registrada y hash coincidente. Para `LOC-001` (221 páginas candidatas), `LOC-003` (1) y `LOC-004` (12), sin URL registrada, se aplicó una excepción explícita por ID tras revisar su ficha y la naturaleza de los documentos. La excepción permite la extracción local; no subsana la procedencia, vigencia ni idoneidad de la cita. Esos puntos continúan pendientes antes del uso normativo.

La muestra visual de la página 88 de `CON-007` confirmó que OCR puede interpretar mal letras de una imagen aunque el servicio no marque baja confianza. Por eso `EXTRAIDO-CON-OCR-PENDIENTE-COTEJO` no equivale a texto fiel: toda página que se vaya a citar debe cotejarse con el PDF antes de anclar un pasaje.

## Resultado de la corrida OCR

El OCR completó las 603 páginas candidatas de los 49 PDF que lo requerían: 369 páginas en fuentes con URL pública registrada y 234 páginas en los tres ID habilitados expresamente. No quedó ninguna página OCR pendiente ni se registraron errores de trabajo. La evaluación final verificó los hashes de los originales y de los textos, la cantidad de páginas y los marcadores físicos: 132 documentos quedaron `EXTRAIDO-NATIVO-PENDIENTE-COTEJO` y 49 `EXTRAIDO-CON-OCR-PENDIENTE-COTEJO`, sin hallazgos de integridad.

El control dejó 72 páginas OCR señaladas por baja confianza, 11 con texto OCR escaso y 83 con posible tabla o columnas según una regla heurística. Las categorías pueden coincidir en una misma página. Se prepararon vistas de cotejo para `CON-007`, página PDF 88, y `LOC-001`, página PDF 1. Una comparación visual de esas muestras mostró que la portada y los elementos gráficos pueden perder palabras o cambiar letras en OCR, incluso sin aviso de baja confianza. Las páginas usadas como evidencia en una futura caja o flujo requieren cotejo individual; ninguna cita normativa ni modelo se marcó como validado en estas dos fases.

Los cuatro derivados que inicialmente compartían archivo por tener el mismo ID y hash se separaron por ruta documental. También se aislaron las 603 páginas OCR intermedias por PDF para permitir una reanudación sin mezclas; el control final quedó sin cachés alteradas. La localización de página impresa y los anclajes de pasajes se construirán en las fases siguientes. El manifiesto y los textos derivados permanecen fuera de Git; este informe y las herramientas sí quedan en el repositorio.

La caché local ocupa aproximadamente 30,8 MB, incluidos 512 archivos OCR intermedios de la disposición anterior. La herramienta actual no los consulta y Git los ignora. Su retirada fue rechazada por el control automático de ejecución de comandos; queda como limpieza local pendiente, sin efecto en la integridad del manifiesto ni de los Markdown finales.
