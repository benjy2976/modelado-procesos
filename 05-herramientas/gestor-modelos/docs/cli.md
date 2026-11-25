---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
---

# CLI de la aplicación

`modelador-procesos` es la entrada común del paquete Python. Las lecturas y observaciones comparten servicios con API y MCP; el comando `modelo` delega aún en el generador vigente.

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

## Comandos

La preparación documental de las fases 1 y 2 usa `fuentes inventariar`, `fuentes diagnosticar-texto [--max-documentos N]`, `fuentes planificar-extraccion`, `fuentes priorizar --proceso S4.3.2`, `fuentes extraer --metodo nativo|ocr [--max-documentos N]`, `fuentes evaluar-extraccion` y `fuentes preparar-cotejo --id <ID> --pagina N [--archivo <ruta-registrada>]`. `--archivo` distingue un ID usado por varios PDF. `fuentes resolver-colisiones-cache` separa derivados históricos que compartían ID y hash pese a corresponder a rutas distintas; `fuentes aislar-paginas-ocr` reconstruye páginas OCR intermedias en una carpeta propia por PDF. Ninguno cambia los originales.

`fuentes extraer-office [--max-documentos N]` convierte DOCX y PPTX a Markdown y deja una ficha de inventario de cada XLSX en `preparacion-office.json`, sin transcribir hojas. Un DOCX no tiene páginas fijas: cada párrafo del cuerpo lleva `<!-- parrafo: N; ... -->` con el numeral automático reconstruido desde `numbering.xml` y `styles.xml` (`numeral`), el numeral escrito a mano si lo hay (`numeral_texto`), la sección detectada y, si Word dejó marcas de su última paginación, `pagina_word_aprox`, que es solo orientativa. Las tablas se conservan en HTML con celdas combinadas y las notas al pie al final. Cada PPTX se marca por `diapositiva`. La conversión es reanudable: no repite un archivo con el mismo hash y versión del conversor.

`fuentes indice` reescribe `cache/00-indice.md`, una tabla legible por carpeta que enlaza cada original con su texto derivado, su tamaño, método y estado. Se regenera automáticamente después de `extraer`, `evaluar-extraccion`, `resolver-colisiones-cache`, `aislar-paginas-ocr` y `extraer-office`.

La consulta acotada de la fase 3 usa `fuentes segmentar`, `fuentes indexar`, `fuentes buscar` y `fuentes contexto`. `segmentar` divide cada texto derivado en fragmentos con ID estable `<hash-documento>-<hash-ruta>:<clave>`: los PDF normativos por artículo y numeral (`art-109.1`), los demás PDF por bloques de página (`p12-b2`), los DOCX por numeral o sección (`par-795`), las tablas (`tabla-66`) y las diapositivas. Omite cabeceras y pies repetidos en la mitad o más de las páginas y adjudica títulos y capítulos al artículo que los sigue. Una clave repetida en el mismo documento se marca `clave_repetida`; en textos consolidados suele indicar un numeral modificado cuya versión vigente debe verificarse. Una entrada de índice de contenido queda como `ENCABEZADO-SIN-CUERPO`. `indexar` reconstruye un índice SQLite FTS5 local, sin tildes ni mayúsculas, a partir de la segmentación vigente.

`fuentes buscar "<consulta>" [--modo todas|alguna|frase] [--tema <id> [--con-relacionados]] [--id <ID>] [--archivo <parte-de-ruta>] [--tipo pdf|docx|pptx] [--area <carpeta>] [--articulo N] [--limite N] [--max-caracteres N]` devuelve pasajes candidatos con documento, hash, ubicación (páginas PDF, párrafos DOCX o diapositiva), artículo, numeral, encabezados, método de extracción y estado de cotejo. Cada palabra se cita, de modo que el usuario no puede inyectar operadores FTS. `--archivo` busca una parte de la ruta: una cadena común a dos nombres incluye ambos documentos. Sin consulta, un filtro como `--articulo` lista los fragmentos en orden. `fuentes contexto <fragmento> [--vecinos N] [--max-caracteres N]` entrega el texto completo y los fragmentos contiguos del mismo documento. La salida advierte `indice_desactualizado` si la segmentación cambió después de indexar.

`fuentes buscar --regimen <valor>` limita la búsqueda a un régimen de ejecución asignado por carpeta y excepciones en `01-referencias/00-catalogo/regimen-documental.json`; cada resultado declara el régimen de su documento. `fuentes indexar` aplica las reglas vigentes al reconstruir el índice.

`fuentes buscar` usa por defecto el modo `flexible`: omite palabras vacías, busca por raíz con prefijo («sustenta» halla «sustente») y, si con todas las raíces hay menos resultados que el límite, completa con coincidencias parciales marcadas `relajado`. `todas`, `alguna` y `frase` conservan la coincidencia exacta.

La fase 4 agrega `fuentes pruebas`, `fuentes anclar` y el grupo `auditoria`. `fuentes anclar` normaliza página y cita de la misma forma (sin tildes, mayúsculas ni puntuación y uniendo palabras partidas con guion) y devuelve un rectángulo por renglón con origen arriba a la izquierda. Una página sin capa de texto o una cita que la capa ordena distinto devuelve `SIN-CAPA-TEXTO` o `CITA-NO-HALLADA`; nunca un resaltado aproximado. `auditoria registrar` valida cada ID contra el inventario vigente y cada cita contra el texto del fragmento; un evento idéntico no se repite y un cambio de resultado se guarda como rectificación. Los resultados admitidos son `SUSTENTADA`, `INFERENCIA`, `CONTRADICCION`, `EVIDENCIA-INSUFICIENTE` y `NO-APLICA`; `VALIDADO` se rechaza.

Formato ampliado (DEC-057, 2026-11-24): cada cita declara `ambito` (de qué trata el pasaje: adicionales o reducción, selección o ejecución, bienes u obras, régimen) y `relacion` con la afirmación (`directa`, `antecedente` o `analogia`). Una afirmación `SUSTENTADA` necesita al menos una cita directa. `auditoria cobertura` recorre la fuente hacia el modelo: cada obligación del pasaje rector queda representada por elementos, declarada no representada o fuera de alcance, con cita verificada. `auditoria informe --check` falla si hay obligaciones no representadas, si la cobertura corresponde a otra revisión de la tabla o si un elemento menciona en su nombre, anotación o fuente un artículo que ninguna de sus anclas muestra (`REFERENCIA-SIN-ANCLA`). Una referencia del visor puede tener `tramos` de varias páginas, cada uno con rol `citado` o `antecedente`; `fuentes anclar` compara sin espacios para tolerar ligaduras partidas (por ejemplo, «fi nalidad») en las ediciones de El Peruano. Con `--fragmento`, si la cita no está entera en una página y el fragmento abarca varias, la herramienta detecta en el texto el punto de corte (el prefijo más largo presente en una página cuyo resto empieza en la siguiente) y devuelve un tramo `citado` por página. Asignar el rol `antecedente` a un tramo es una decisión de quien registra la referencia.

`fuentes temas comprobar` valida `catalogo/temas-busqueda.json`: esquema, IDs, procesos existentes, relaciones y ausencia de equivalencias o del estado `VALIDADO`. `fuentes temas sugerir [--proceso S4.3]` asigna temas candidatos a fragmentos por coincidencia de términos, con procedencia y confianza `BAJA` o `MEDIA`, en `cache/temas-sugeridos.jsonl`. Un tema relacionado amplía la búsqueda, pero no afirma equivalencia jurídica.

Estos comandos producen un manifiesto y Markdown paginado en `01-referencias/09-derivados-texto/cache/`, excluida de Git. El umbral inicial de 80 caracteres por página decide si se intenta OCR; no acredita fidelidad ni vigencia. OCR requiere `OCR_MCP_KEY` en el entorno local y procesa copias derivadas de PDF con URL pública HTTPS registrada y hash coincidente. Para un documento sin URL cuya procedencia se haya revisado, `fuentes extraer --metodo ocr --permitir-id-sin-url <ID>` habilita solo ese ID; el argumento puede repetirse. Los demás quedan pendientes. El PDF original no se altera.

| Comando | Resultado |
|---|---|
| `arbol` | Árbol institucional en JSON |
| `proceso S4.3.2.3` | Datos y revisión de un proceso en JSON |
| `fuente <codigo> <referencia> <indice>` | Texto acotado de la fuente y página registrada, con hash y estado |
| `fuentes` | Grupo de preparación documental; requiere una operación |
| `fuentes inventariar` | Reconciliación de PDF, catálogo, hashes y duplicados |
| `fuentes diagnosticar-texto [--max-documentos N]` | Medición de texto nativo por página |
| `fuentes planificar-extraccion` | Cola de extracción nativa y OCR selectivo |
| `fuentes priorizar --proceso <codigo>` | Prioridad provisional según citas en tablas y sustentos |
| `fuentes extraer --metodo nativo\|ocr [--max-documentos N]` | Markdown paginado o OCR sobre copias derivadas |
| `fuentes evaluar-extraccion` | Integridad, paginación y señales de cotejo |
| `fuentes preparar-cotejo --id <ID> --pagina N [--archivo <ruta-registrada>]` | Vista local de original y texto |
| `fuentes resolver-colisiones-cache` | Separa derivados históricos con procedencia diferente |
| `fuentes aislar-paginas-ocr` | Aísla páginas OCR intermedias de cada PDF |
| `fuentes extraer-office [--max-documentos N]` | DOCX/PPTX a Markdown anclado por párrafo o diapositiva; ficha de XLSX |
| `fuentes indice` | Índice Markdown legible de la caché con enlaces a originales y textos |
| `fuentes segmentar [--max-documentos N]` | Fragmentos por artículo, numeral, bloque, tabla o diapositiva, con ubicación |
| `fuentes indexar` | Índice léxico SQLite FTS5 regenerable |
| `fuentes buscar ...` | Pasajes candidatos filtrados y acotados en cantidad y caracteres |
| `fuentes contexto <fragmento>` | Texto completo del fragmento y sus vecinos |
| `fuentes temas comprobar\|sugerir` | Validación del vocabulario y sugerencias léxicas con procedencia |
| `fuentes regimen` | Comprueba `regimen-documental.json` y resume la clasificación de los documentos |
| `fuentes pruebas preparar\|medir <banco> [--modo M] [--sin-temas]` | Banco de recuperación de `bancos-prueba/` y métricas acierto@k, MRR, negativas, latencia y tamaño |
| `fuentes anclar (--fragmento <id> \| --archivo <pdf> --pagina N) --cita "<texto>"` | Rectángulos por renglón de una cita en el PDF original |
| `auditoria inventariar-elementos <codigo>` | Elementos, flujos, carriles y mensajes con IDs de auditoría |
| `auditoria registrar <codigo> --archivo <lote.json>` | Registro inmutable de afirmaciones con cita verificada; rechaza todo el lote ante un error |
| `auditoria cobertura <codigo> --archivo <obligaciones.json>` | Obligaciones de la fuente rectora y elemento que las representa (`REPRESENTADO`, `NO-REPRESENTADO`, `FUERA-DE-ALCANCE`) |
| `auditoria correr --alcance <codigo> [--max-procesos N]` | Estado reanudable por proceso: `SIN-MODELO`, `PENDIENTE-AUDITORIA`, `EN-CURSO`, `CON-HALLAZGOS`, `COMPLETO` o `DESACTUALIZADO`; escribe `auditorias/corrida-<alcance>.json` y su resumen Markdown |
| `auditoria comparar-interfaces <padre>` | Candidatos de interfaz: hijo sin modelo o sin elemento, tipo de disparo, salida declarada no representada, secuencia entre hijos y mensajes sin contraparte entre hermanos |
| `auditoria informe <codigo> [--check]` | Cobertura, resultados, citas vigentes y anclas del visor; Markdown en `auditorias/<codigo>/`. Solo cuenta afirmaciones de elementos presentes en el inventario; las de elementos retirados se listan en `afirmaciones_de_elementos_retirados` y permanecen en el registro |
| `observaciones listar S4.3.2.3` | Registros y revisión vigente |
| `observaciones agregar <codigo> --texto ... --autor ... --revision ... [--elemento ...] [--tipo ...]` | Registro con ID y nueva revisión |
| `observaciones responder <codigo> <id> --texto ... --autor ... --revision ...` | Respuesta e historial con nueva revisión |
| `observaciones estado <codigo> <id> --valor ABIERTA\|RESUELTA --revision ... [--autor ...]` | Cambio de estado trazado |
| `modelo <codigo> [--check] [--exportar-imagenes]` | Salida y código de `modelar.py` |
| `api [--host 127.0.0.1] [--port 8000]` | Servidor HTTP local |
| `mcp [--transporte stdio]` | Servidor MCP local |
| `contrato [--check]` | Exporta `contracts/openapi.json` o comprueba que coincide con FastAPI |
| `sesiones iniciar <codigo>` | Captura árbol de trabajo y abre copia recuperable |
| `sesiones leer <codigo> <sesion>` | Manifiesto y preparación de la copia |
| `sesiones documento <codigo> <sesion> tabla\|sustento\|fuentes_visor` | Texto y hash de revisión |
| `sesiones editar <codigo> <sesion> <nombre> --archivo <ruta> --revision <hash>` | Sustituye solo el texto de la copia |
| `sesiones preparar <codigo> <sesion>` | Regenera copia, devuelve diff y D1–D5 |
| `sesiones integrar <codigo> <sesion> --revision <numero>` | Integra cambios preparados si el destino no cambió |
| `sesiones cerrar <codigo> <sesion>` | Libera editor; conserva instantánea y copia |

Se ejecuta desde la carpeta de la aplicación con `uv run modelador-procesos ...`. Un error de dominio se imprime en JSON en `stderr` y termina con código `1`; el comando `modelo` conserva el código de salida del generador. Los argumentos mal formados se rigen por `argparse`.

`contrato --check` devuelve `0` si el snapshot coincide con el schema generado y `1` si está desfasado. `contrato` sin `--check` sobrescribe únicamente el contrato generado, sin modificar procesos ni observaciones.
