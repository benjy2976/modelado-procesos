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

## Documentos Office

La biblioteca contiene además 29 DOCX, 27 XLSX y 1 PPTX. No requieren OCR porque su texto es digital. La corrida del 24 de noviembre de 2026 con `fuentes extraer-office` convirtió los 29 DOCX y el PPTX a Markdown (`EXTRAIDO-ESTRUCTURADO-PENDIENTE-COTEJO`) y fichó los 27 XLSX (`FICHADO`), sin errores. Todos están catalogados y sus hashes coinciden con el registro. El único Office registrado y ausente en esta copia es el Formato 08-A (`formato-08-a.xlsx`, `INV-005A`). El estado y los resúmenes por documento están en `cache/preparacion-office.json`, fuera de Git.

Las hojas de cálculo no se transcriben: un agente puede leerlas directamente. Su ficha registra hojas, estado visible u oculto, rango, filas con datos, fórmulas, celdas combinadas y primera fila con datos, para localizarlas y citarlas por hoja y celdas junto con el hash del archivo.

Un DOCX no tiene paginación fija. El ancla citable es el número de párrafo del cuerpo y el numeral. Word no guarda en el texto los numerales automáticos, de modo que se reconstruyen desde las definiciones de lista. En las bases estándar coexisten numerales escritos a mano (por ejemplo, 4.4.1.) y automáticos (por ejemplo, 3.3.10 y los literales). Las 19 bases estándar comparten el ID `CON-003A`, por lo que solo la ruta o el hash identifican cuál se cita.

**Cotejo de numeración.** La base de licitación pública de obras se abrió con LibreOffice en un contenedor desechable y se comparó su texto renderizado con el Markdown. En la sección de adicionales, el render muestra la misma secuencia 3.3.1 a 3.3.12, incluido «3.3.10 ELABORACIÓN DEL EXPEDIENTE TÉCNICO DE PRESTACIONES ADICIONALES» con su nota 39. En el documento completo, los 175 numerales automáticos de párrafos del cuerpo se localizaron en el render con el mismo numeral; ninguno difiere. Trece casos requirieron revisión individual porque el título se repetía o una llamada de nota interrumpía el texto, y también coincidieron. No se cotejaron uno por uno los numerales dentro de celdas de tabla. LibreOffice paginó el documento en 154 páginas frente a unas 180 de la última paginación de Word: `pagina_word_aprox` es orientativa y no sirve como cita. Las mayúsculas aplicadas por formato no se reflejan en el texto derivado.

Este cotejo comprueba la conversión, no el contenido normativo: las bases siguen siendo plantillas cuyo uso en un contrato concreto depende de las bases efectivamente aprobadas.

## Publicaciones oficiales del Reglamento — 2026-11-24

Se incorporaron la separata especial de El Peruano del 22-01-2025 con el D.S. 009-2025-EF (`CON-001P`, aportada por el usuario, 196 páginas con capa de texto; 2 páginas de portada sin texto quedan sin OCR porque no tienen contenido normativo) y las publicaciones de El Peruano del D.S. 001-2026-EF (`CON-001M1`) y del D.S. 222-2026-EF (`CON-001M2`), obtenidas de copias alojadas en lpderecho.pe cuyos metadatos corresponden a la publicación oficial de Editora Perú. Las ediciones de El Peruano extraen la ligadura «fi» con un espacio («efi cientes») e intercalan cabeceras de columna; por eso el anclaje compara sin espacios. Una comparación automática por artículo entre la edición original y el texto consolidado todavía tiene ruido de extracción. Los numerales usados en S4.3.2.7 se verificaron uno por uno.

## Fase 3: consulta acotada

**Segmentación (3.C1–3.E1).** Los 211 textos derivados (181 PDF, 29 DOCX y 1 PPTX) se dividieron en 22 849 fragmentos con cobertura de texto del 100 % en todos los documentos. 83 PDF se reconocieron como normas con artículos, 98 se segmentaron por bloques de página y 30 por estructura Office. La primera versión solo reconocía «Artículo N.» y dejaba en bloques a normas técnicas del RNE y decretos que usan «Artículo N.-»; el patrón se amplió exigiendo que el título empiece en mayúscula, para no confundir citas con encabezados. Las entradas de índices de contenido (130) quedan como `ENCABEZADO-SIN-CUERPO` y no alteran la jerarquía de capítulos.

El cotejo visual de las páginas 60 y 61 del Reglamento de la Ley 32069 confirma los límites: el artículo 109 completo está en la página 60 y el artículo 110 empieza al pie de la página 60 y continúa en la 61, tal como lo registra el fragmento `art-110.1`. El mismo cotejo explica las claves repetidas del Reglamento: el texto consolidado contiene el numeral original, una nota «(\*) Numeral modificado por el Artículo 2 del Decreto Supremo Nº 001-2026-EF…» y el texto nuevo. Esos fragmentos (`clave_repetida`) exigen determinar la versión vigente antes de citarlos; la herramienta no lo decide.

Los IDs de fragmento combinan el hash del documento con el de su ruta, porque cuatro pares de PDF tienen bytes idénticos en carpetas distintas y producían identificadores duplicados.

**Índice y consultas (3.C2–3.E3).** El índice SQLite FTS5 local contiene los 22 849 fragmentos y se reconstruye en un segundo. Doce consultas de control sobre hechos ya verificados pasaron con el criterio del plan (pasaje correcto entre los primeros resultados): art. 109.1 en la página 60 entre los tres primeros para «reducción de prestaciones»; filtro por artículo 109 con 109.1–109.3 en orden; numeral 3.3.10 de las bases de obra; art. 110.1 con páginas 60–61; contexto 108.4, 109.1 y 109.2; método OCR declarado en `LOC-001`; presupuesto de caracteres, resultado vacío y neutralización de operadores FTS. El orden interno de los primeros resultados sigue a BM25 y favorece fragmentos breves; su calidad se medirá con el banco de preguntas de la fase 4. Dos fallos iniciales correspondieron a los casos de control y no a la herramienta: el filtro `--archivo` busca una parte de la ruta y la cadena elegida era común a la Ley y al Reglamento.

**Temas (3.C3–3.E4).** El vocabulario `catalogo/temas-busqueda.json` (`BORRADOR-IA`) contiene once temas derivados de los nombres de los procesos S4.3, con relaciones no equivalentes. La sugerencia léxica para S4.3 asignó 945 temas candidatos a 741 fragmentos de 77 documentos. En una muestra de 22 sugerencias revisada por IA, unas 8 eran pertinentes, 7 pertinentes pero de otro régimen o tangenciales (obras por impuestos, administración directa, servicios) y 7 falsos positivos por homonimia o etapa distinta («valorización de residuos sólidos», «absolución de consultas a las bases», «paralización del funcionamiento»). La confianza `MEDIA` apenas reduce ese ruido. Los temas sirven para ampliar la recuperación, no para seleccionar sustento; la fase 4 necesita filtrar por régimen y ámbito antes de proponer citas.

