---
id: HER-MESA-MODELAMIENTO-METODOLOGIA-REVISION
tipo: propuesta
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
proceso: []
fecha_creacion: 2026-11-20
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/ia
  - tema/procesos
---

# Metodología de auditoría y atención de observaciones

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

Esta es una **propuesta de método**, no una corrida completa ni una validación normativa. Ordena dos ciclos: primero, probar la auditoría en un modelo pequeño y, tras evaluar su resultado, auditar y enriquecer el sustento de los demás modelos de S4.3; después, someterlos a comentarios y atender cada observación con trazabilidad. Usa la [tabla estructurada](../plan-mesa-modelamiento.md) y el sustento como instrumentos de trabajo en la fase lógica. El BPMN y el visor se regeneran al cerrar cada lote conceptual. La consola será una vista de los registros, no una fuente paralela de decisiones.

## 1. Corrida previa de sustento en S4.3

### Alcance y punto de partida

El inventario actual contiene **11 tablas**: S4.3, S4.3.1, S4.3.2 y S4.3.2.1 a S4.3.2.8. S4.3.3 tiene carpeta, pero no tabla/modelo: se registra como `SIN-MODELO`, sin inferir su contenido. Antes de ejecutar, el inventario se recalcula desde el árbol y se guardan código, ruta, revisión de la tabla y del sustento, y hash de las fuentes consultadas. Se procesan solo documentos dentro del alcance y régimen aplicable a cada proceso; no se extiende una regla de obra bajo contrata a administración directa o a otro régimen por semejanza de nombres.

Cada corrida toma un [paquete de contexto](../../../00-gobernanza/plantillas/conocimiento/paquete-contexto.yaml) por proceso: fase, límites, tabla y sustento vigentes, ficha, glosario, fuentes textuales necesarias, reglas validadas disponibles y preguntas abiertas. Los derivados gráficos y el XML generado quedan fuera del contexto conceptual, salvo error técnico o revisión visual programada.

### Unidad de análisis y clasificación

Se revisa **cada caja, evento, compuerta, flujo, carril e interfaz con otro proceso**. Para cada elemento se separan las afirmaciones comprobables: actor, acción, condición, plazo, documento, entrada/salida, decisión y excepción. Un elemento puede requerir varias fuentes o combinar un requisito normativo con una decisión institucional; no se le asigna una sola cita global que oculte esa diferencia.

| Resultado por afirmación | Significado y acción |
|---|---|
| `SUSTENTADA` | La fuente localizada respalda exactamente la afirmación y su ámbito. Se registra la clase: exigencia normativa, evidencia institucional observada o decisión del proyecto. |
| `INFERENCIA` | La conclusión se deduce de fuentes identificadas, pero no está expresamente ordenada por ellas. Se explica el razonamiento y queda visible como propuesta. |
| `CONTRADICCION` | La tabla o el sustento difiere de la fuente aplicable, o dos fuentes discrepan. Se abre hallazgo y se propone corrección o delimitación. |
| `EVIDENCIA-INSUFICIENTE` | Falta fuente, página, vigencia, ámbito o hecho institucional verificable. No se completa por conocimiento general. |
| `NO-APLICA` | Hay justificación explícita de por qué la afirmación o fuente no corresponde a este caso. |

La auditoría busca activamente omisiones: requisitos previos, rutas de rechazo y retorno, notificaciones, competencia para decidir, plazos, documentos, excepciones, interfaces entre procesos y coherencia entre niveles. También contrasta el sustento con la tabla y los límites definidos en las notas índice. Los controles D1–D5 detectan problemas técnicos y geométricos; **no prueban corrección jurídica ni operativa**.

### Prueba de cada referencia

Para cada fuente se registra identificador del catálogo, ruta al original, hash, emisor, título, fecha de consulta, vigencia comprobada o pendiente, artículo/numeral, página física del PDF y fragmento breve que permite identificar el pasaje. **Al enlazar la referencia** se selecciona el párrafo o los renglones concretos y se guardan sus rectángulos de página (puede haber varios), cotejados visualmente con el original. Las coordenadas se expresan como proporciones de la página renderizada, con origen arriba a la izquierda, de modo que el mismo pasaje se marque a cualquier zoom. Quedan ligadas al hash del PDF y a la página física. Si cambia el PDF o no se pudo ubicar el pasaje, el visor abre la página sin resaltado y muestra el motivo. **Al abrir el visor no se busca texto**: solo proyecta las coordenadas guardadas. El fragmento textual sirve como cita y control de identidad, no como instrucción de búsqueda. El resaltado tampoco sustituye la cita ni la validación normativa.

El recorrido puede usar un servicio de conversión PDF a **PDF con texto buscable y Markdown paginado** para localizar y leer pasajes más rápido, especialmente cuando el original carece de texto. Se mide primero si el PDF ya tiene capa textual; solo si falta, se solicita OCR sobre una copia derivada. La extracción conserva marcadores de página y hash del original, y declara qué páginas provienen de OCR. El agente compara cada pasaje candidato y sus coordenadas con el PDF original antes de enlazarlo; ni el PDF convertido ni el Markdown sustituyen la evidencia original. El MCP OCR local quedó probado el 2026-11-20 con un PDF sintético de una página: carga, procesamiento y lectura del Markdown paginado completados. Su configuración y credencial son locales, fuera de Git; la prueba no equivale a validar su fidelidad en documentos normativos.

### Preparación documental antes de la auditoría

No se ejecuta OCR indiscriminado sobre toda la biblioteca. El inventario local del 2026-11-20 cuenta 181 PDF, mientras que la [última evaluación automatizada](../../../01-referencias/00-catalogo/resumen-calidad-documental.md), del 2026-10-16, encontró cinco PDF sin texto entre 230 archivos de varios formatos. Son cortes y universos distintos: primero se recalcula la cobertura de texto de los PDF vigentes. El reglamento utilizado en el piloto S4.3.2.7 ya tiene texto extraíble; repetirlo con OCR no mejora ese caso.

La corrida preparatoria produce un **manifiesto reanudable**, no citas automáticas: identificador del catálogo, ruta del original, SHA-256, páginas, cobertura de texto por página, pertinencia para S4.3, método elegido y estado del derivado. Se conservan los resultados aunque se interrumpa la corrida; un cambio de hash invalida solo los derivados de esa fuente. El orden es:

1. Medir todos los PDF disponibles y cruzarlos con catálogo y fuentes citadas por los procesos de S4.3; señalar faltantes, duplicados por hash y archivos cuya vigencia esté pendiente.
2. Priorizar las fuentes que realmente sustentan el piloto y la siguiente ronda. Para PDF con texto aprovechable, extraer Markdown paginado directamente; para páginas sin texto o inutilizables, enviar una copia derivada al MCP OCR y pedir Markdown, JSONL y PDF buscable solo si cada artefacto aporta a la revisión.
3. Guardar los derivados en la caché local prevista en [el extractor documental](../../extractor-documental/00-extractor-documental.md), vinculados al hash del original y al método usado. Registrar fallos, páginas de baja confianza y costos/tiempos; no versionar copias masivas ni modificar originales.
4. Comprobar en una muestra de páginas, y siempre en las páginas finalmente citadas, texto, numeración y orden de lectura contra el original. Solo entonces iniciar o continuar la auditoría de afirmaciones. Los rectángulos de resaltado se seleccionan en el original; no se infieren del Markdown OCR.

La medición global puede hacerse en una sola corrida; la conversión se ejecuta por lotes de fuentes pertinentes y se amplía conforme avanza la auditoría. Así se evita procesar normas que no intervienen en S4.3 o regenerar documentos que ya son buscables.

### Consulta acotada de la biblioteca: propuesta para la corrida

La biblioteca completa no entra en el contexto de un agente. La extracción paginada alimentará un índice local regenerable; el original, su catálogo y las citas cotejadas conservarán sus funciones separadas. Cada unidad recuperable conservará el ID y SHA-256 del documento, la página PDF, el artículo/numeral y sus encabezados superiores cuando se reconozcan con fiabilidad, el método de extracción y una referencia estable al fragmento. Un artículo que cruza páginas puede formar una unidad lógica con varias ubicaciones; un bloque que mezcle obligaciones distintas se divide sin perder el vínculo con su artículo. El índice no se versiona como fuente de conocimiento.

La propuesta de búsqueda tiene tres capas progresivas:

1. **Estructura y filtros obligatorios.** Acotar por proceso, modalidad, entidad emisora, tipo documental, régimen y fecha aplicable cuando estén acreditados; navegar por documento, capítulo, artículo y numeral. Una vigencia desconocida queda visible como pendiente y no se convierte en vigente por aparecer en la búsqueda.
2. **Búsqueda léxica y temas.** Indexar el texto por fragmento y mantener un vocabulario de temas, sinónimos y relaciones. Por ejemplo, «paralización» puede recuperar términos relacionados, pero «suspensión» no se trata automáticamente como equivalente jurídico. Las etiquetas sugeridas por IA son pistas de recuperación con procedencia y confianza, no reglas ni clasificación normativa validada. Conservar también búsquedas por artículo y frases exactas.
3. **Recuperación semántica opcional.** Comparar sobre un conjunto de preguntas reales la búsqueda anterior con vectores, combinación léxica-semántica y reordenación de candidatos. Adoptar cada componente solo si mejora la recuperación de pasajes pertinentes, el costo y la latencia. Los resúmenes sirven para orientar, nunca para citar en lugar del pasaje original.

La consulta para una caja descompone sus afirmaciones en actor, acción, condición, plazo, documento y excepción. Solicita candidatos al índice con filtros de ámbito; amplía los artículos vecinos, las remisiones y las modificatorias pertinentes; elimina duplicados y entrega al agente un paquete pequeño de pasajes con ubicación y estado de extracción. El agente coteja cada candidato con el PDF original, busca evidencia en contra y registra `EVIDENCIA-INSUFICIENTE` si no puede sostener la afirmación. Las relaciones entre fuente, regla propuesta, afirmación y elemento del modelo se guardan explícitamente; una etiqueta temática no constituye ese vínculo.

El mismo servicio de consulta deberá alimentar CLI, API y MCP, con operaciones de lectura acotadas: buscar fragmentos, obtener artículo y páginas contiguas, seguir remisiones y recuperar el paquete de evidencia de un elemento. El visor recibe solo referencias verificadas y rectángulos enlazados al hash del original; no ejecuta una búsqueda al abrir el PDF. Antes de ampliar la auditoría se medirá, con preguntas extraídas del piloto S4.3.2.7, si los pasajes correctos aparecen entre los primeros resultados, si se recuperan condiciones y excepciones, los errores de OCR, el costo, la latencia y la exactitud de las citas. Los fallos se incorporarán al conjunto de prueba antes de reindexar.

El agente puede proponer reglas y correcciones, pero no declarar una regla `VALIDADO`, una conformidad institucional ni un modelo `APROBADO`. Se aplica el [protocolo de conocimiento confiable](../../../00-gobernanza/protocolo-conocimiento-confiable.md): una regla aún no validada queda identificada como propuesta y no sustenta por sí sola una línea base publicada. Si la vigencia no puede comprobarse, se marca pendiente aunque el PDF exista.

### Secuencia de la corrida

1. **Preparar fuentes e inventariar modelos.** Completar la preparación documental selectiva anterior; detectar las 11 tablas, los sustentos y el caso `SIN-MODELO`, y anotar los hashes iniciales. El manifiesto permite reanudar sin repetir procesos ni sobrescribir cambios de otro editor.
2. **Probar un solo modelo pequeño.** Auditar S4.3.2.7 (reducciones de prestaciones, 15 elementos y dos mensajes). Entregar su matriz de afirmaciones, citas con página y rectángulos, vista del pasaje resaltado mediante metadatos, discrepancias y cambios en copia si proceden. Detener la expansión al resto hasta que el usuario evalúe este resultado; la prueba no implica conformidad del modelo.
3. **Recorrer los otros diez modelos, un proceso por vez, una vez evaluado el piloto.** Primero los procesos padre S4.3 y S4.3.2 para fijar interfaces; después S4.3.1 y S4.3.2.1 a .6 y .8. Comparar entradas y salidas con el padre y los hermanos. Un cambio de tabla no corre en paralelo con su generación.
4. **Contrastar y corregir.** Incorporar referencias precisas y hallazgos en el sustento; registrar anclajes verificados en `fuentes-visor.json`. Si una discrepancia exige cambiar el flujo, editar tabla y sustento en una copia, preparar diff, regenerar BPMN/HTML, ejecutar D1–D5 e integrar solo si no hay conflicto de revisión. Conservar la versión anterior. Si no hay base suficiente, mantener el hallazgo abierto en lugar de forzar una ruta.
5. **Verificar cobertura y emitir informe.** Releer los pasajes citados, revisar que cada afirmación tenga clase y resultado, comprobar enlaces y revisar muestras cruzadas entre procesos. El informe indica conteos y vacíos por proceso; `SIN-MODELO` y `EVIDENCIA-INSUFICIENTE` permanecen visibles. Solo entonces se habilita la revisión de usuarios sobre esa versión identificada.

El resumen durable de la auditoría y las discrepancias vive en el **sustento de cada proceso**; la tabla conserva la lógica modelada y `fuentes-visor.json` solo localiza pasajes para el visor. Un manifiesto operativo puede guardar progreso, hashes y resultados por elemento para reanudar y alimentar la consola, pero no reemplaza esos maestros ni se presenta como validación. La corrida debe ser repetible: mismo alcance y mismos hashes no crean citas ni cambios duplicados; una fuente o modelo modificado dispara revisión de los resultados afectados.

**Criterio de cierre de la corrida:** todos los modelos inventariados tienen resultado registrado; cada afirmación revisada tiene clase y localización comprobable o vacío explícito; los cambios integrados tienen diff e informe D1–D5; las contradicciones pendientes se muestran como pendientes. Esto declara *cobertura de análisis*, no exactitud normativa certificada.

## 2. Atención individual de comentarios y observaciones

Cada comentario conserva su ID, texto original, autor declarado, fecha, proceso, revisión del modelo observada y elemento BPMN opcional. Puede dirigirse a una caja, flujo, diagrama completo o documento. **No se fusiona, borra ni cierra automáticamente** por parecerse a otro. Una corrección puede atender varias observaciones, pero cada una recibe su propia interpretación, evaluación y vínculo al mismo cambio.

El agente toma una observación a la vez dentro de un modelo. Primero reformula qué entiende y qué se pide; si hay ambigüedad, registra hipótesis y evidencia faltante. Luego consulta tabla, sustento, historial y fuentes pertinentes; distingue un error del modelo, una explicación ausente, una diferencia de criterio y una solicitud fuera de alcance. Finalmente registra una propuesta de atención con justificación y referencias. No atribuye su interpretación al autor como si fuera confirmada.

| Tipo de atención | Evidencia mínima para cerrarla |
|---|---|
| `CAMBIO-MODELO` | ID de sesión, diff de tabla/sustento, elementos afectados, hashes anterior/nuevo, resultado de generación y D1–D5, explicación del efecto. |
| `CAMBIO-SUSTENTO` | Diff y referencia precisa añadida o corregida; indicación expresa de que el flujo no cambió. |
| `ACLARACION` | Respuesta razonada que señala el elemento y el pasaje existente que ya atiende la cuestión. |
| `VINCULADA-A-CAMBIO` | ID de otra observación/cambio, explicación específica de cómo ese cambio resuelve esta observación y revisión en que quedó integrado. |
| `NO-PROCEDE` | Motivo concreto, límite de alcance o fuente aplicable; no equivale a ignorar el comentario. |
| `PENDIENTE-EVIDENCIA` | Qué fuente, dato o decisión falta y qué parte del modelo permanece incierta; no se marca resuelta. |

El registro de atención añade eventos inmutables: recepción, interpretación, fuentes consultadas, propuesta, sesión/diff, validación técnica, integración o conflicto, respuesta y eventual reapertura. Cada evento tiene fecha, actor (agente o persona), revisión esperada y resultado. Una rectificación es un evento nuevo. El historial permite reconstruir **qué dijo el autor, qué entendió el agente, qué cambió, por qué y en qué versión**. El autor o editor puede reabrir una resolución sin perder la anterior.

El estado actual del [modelo de datos](modelo-datos.md) solo conserva `ABIERTA`/`RESUELTA`, respuestas e historial básico. Los tipos de atención, vínculos a cambios, etapas `EN-ANALISIS`/`EN-CORRECCION` y reapertura detallada son **ampliaciones por implementar** en el mismo servicio de dominio, expuestas a CLI, API y MCP. La escritura requiere revisión esperada. Varios usuarios pueden aportar observaciones; un único editor activo modifica la copia del modelo. Un conflicto de revisión suspende esa integración y obliga a recalcular la atención sobre la versión vigente.

La resolución por agente no constituye revisión humana ni validación de una regla. El agente puede aplicar un cambio mediante el [MCP existente](mcp.md) y la [sesión recuperable](sesiones-edicion.md) dentro de los controles técnicos ya autorizados; el registro debe distinguir `PROPUESTO`, `INTEGRADO` y `VERIFICADO-POR-PERSONA` cuando exista tal intervención, sin inventarla.

### Objetivo del ciclo de retroalimentación (`DEC-064`)

Definido por el usuario el 2026-11-25:

1. **Observar.** Cada usuario puede observar o comentar el diagrama completo o una caja concreta, sobre la versión que está viendo.
2. **Revisar.** El equipo revisa los registros abiertos de uno en uno, con la tabla, el sustento y las fuentes.
3. **Resolver y documentar.** Cada registro se cierra con su atención documentada. La atención puede producir un cambio del diagrama o del sustento, o una **decisión** que se registra en el [registro de decisiones](../../../00-gobernanza/registro-decisiones.md) y se vincula al registro que la originó.
4. **Claudia como actor.** El agente de IA participa con el alias **Claudia**: registra dudas y observaciones propias, propone atenciones y aplica cambios autorizados. Sus registros quedan identificados con ese alias. No sustituye la revisión humana ni marca conformidades.

Primer experimento: S4.3.2.6 y S4.3.2.5, con 14 registros de Claudia. Las limitaciones que revele el uso se anotan como requisitos de M4 y M5. Las primeras son:
- para observar una caja nueva hay que adoptar antes el BPMN;
- el elemento se identifica por el ID interno del BPMN y no por el de la tabla;
- solo hay estados `ABIERTA` y `RESUELTA`;
- no se guarda la revisión del modelo observada;
- el autor no distingue persona de agente;
- no hay campo para distinguir una duda de una observación;
- el texto era solo plano (atendido el 2026-11-25: formato `html` saneado, editor sencillo, formulario plegable y panel redimensionable);
- una caja retirada deja su registro sin aviso.

### Etapas de resolución de cada observación (`DEC-065`)

Definidas por el usuario el 2026-11-25. Toda observación, la registre una persona o Claudia, recorre estas etapas. Funciona como las preguntas que el agente hace en el chat, pero en la web y con trazabilidad.

| Etapa | Quién actúa | Qué queda registrado |
|---|---|---|
| 1. `REGISTRADA` | Usuario o Claudia | Texto, autor, caja o diagrama y revisión del modelo observada. |
| 2. `EN-ANALISIS` | Agente (Claudia) | Qué entiende del problema, contexto consultado (tabla, sustento, fuentes, decisiones) y clase: error del modelo, explicación ausente, diferencia de criterio, falta de evidencia o fuera de alcance. |
| 3. `PROPUESTA` | Agente (Claudia) | Una o varias opciones de solución. Cada una tiene título, detalle, efecto previsto (cambio del modelo, cambio del sustento, decisión, no procede o pendiente de evidencia), cajas afectadas, fuentes y si es la recomendada. Se indica si admite elegir una o varias. |
| 4. `DEFINIDA` | Persona | La persona acoge una opción, varias compatibles o una opción manual escrita por ella, o vincula la observación a otra ya resuelta. Se registran el autor, la fecha y, si corresponde, la decisión del registro de decisiones. |
| 5. `EN-CORRECCION` | Agente, 100 % IA por MCP | En otra pasada, el agente aplica lo definido: edita la tabla, el sustento u otro documento en una sesión recuperable, regenera el modelo y ejecuta D1–D5. |
| 6. `RESUELTA` | Agente, con evidencia | Sesión, diff, hashes anterior y nuevo, resultado de D1–D5 y decisión vinculada. La persona puede verificarla o reabrirla sin perder el historial. |

Reglas:
- El agente propone, pero nunca elige por la persona: solo una persona puede pasar una observación a `DEFINIDA`.
- La pasada de corrección solo toma observaciones `DEFINIDA` y aplica exactamente la opción acogida. Si la revisión del modelo cambió desde la definición, se detiene y vuelve a análisis.
- Una observación vinculada hereda la resolución de la otra, pero conserva su propio registro y su motivo.
- `ABIERTA` y `RESUELTA` se conservan como estado resumido para compatibilidad. La etapa detallada es un campo nuevo.
- Ninguna etapa equivale a revisión de equipo, opinión técnica ni aprobación.

Implementado el 2026-11-25 (tanda 2B): `resolucion.py` en servicio, CLI, API y MCP, y la definición en la web. Si la tabla cambió desde la definición, la corrección exige confirmar que la definición sigue aplicando (`confirmar_vigencia`) o volver a analizar; así una corrección no bloquea las demás observaciones del mismo modelo. Un cambio de modelo se cierra con la sesión que lo integró.

### Método de análisis de Claudia (`DEC-067`)

La evaluación del 2026-11-25 comparó las 14 propuestas hechas por MCP con una revisión directa de los documentos. En 7 de 13 cuestiones la recomendación cambió o le faltaba una opción. Todas las omisiones tuvieron la misma causa: no se leyó un documento que sí estaba en la biblioteca. Una búsqueda por palabras no encontró un artículo redactado con otros términos, y una caja vecina se citó de memoria. Por eso, antes de registrar una propuesta, Claudia sigue estos pasos con las herramientas del MCP:

1. **Releer, no recordar.** Lee las cajas propias y las de los procesos relacionados (`paquete_contexto`, `procesos_relacionados`) antes de citarlas. Nunca nombra una caja vecina de memoria.
2. **Recorrer el capítulo de la figura.** Con `indice_documento` revisa los títulos del capítulo de la norma rectora (por ejemplo, Reglamento arts. 176-212 para la ejecución de obras) y lee con `leer_articulos` los que podrían aplicar. La búsqueda por palabras complementa, no sustituye.
3. **Formular hipótesis alternativas y buscarlas.** Para cada recomendación registra en `hipotesis` las alternativas consideradas y por qué se descartan o se ofrecen. Incluye al menos:
   - otra figura regulada que resuelva lo mismo (por ejemplo, intervención económica frente a resolución);
   - una figura análoga en un proceso vecino (por ejemplo, el acta de reinicio del art. 107.2 para el acta de una paralización);
   - otro responsable posible.
4. **Buscar responsables por función, no por nombre.** En el ROF se buscan los verbos de la función: registrar en el Banco de Inversiones, suscribir contratos, controlar la supervisión. Antes de proponer una unidad nueva se revisan las convenciones de carriles de los procesos hermanos.
5. **Revisión adversarial.** Antes de registrar, para la opción recomendada se pregunta qué fuente la contradiría y se busca. El resultado queda en `hipotesis`.
6. **Declarar lo no revisado.** Si un documento pertinente no está en la biblioteca, el análisis lo dice y propone incorporarlo, en lugar de suplirlo.

Un análisis que reemplaza a otro conserva el anterior y su propuesta, con el motivo (`resoluciones_anteriores`). Así se ve qué se propuso antes y por qué cambió.

**Objetivo de la consola de observaciones (M5, por planificar).** Una vista que liste todas las observaciones de todos los procesos con su estado, como pendiente, en análisis, pendiente de evidencia, vinculada a otra, resuelta o no procede. Debe permitir filtrar por proceso, caja, autor y estado, y abrir la línea de tiempo de cada registro hasta el cambio o la decisión que lo cerró. Su diseño se planificará más adelante; este objetivo fija el alcance esperado.

## 3. Consola y orden de implementación

La consola mostrará dos colas relacionadas: **auditorías de sustento** por proceso y **observaciones** por modelo/elemento. Permitirá filtrar por proceso, estado, clase de hallazgo, fuente pendiente y revisión; abrirá la línea de tiempo de cada observación, el diff, la tabla y la página citada. Indicará qué revisión del modelo está viendo y si una cita quedó desactualizada. Las cifras agregadas enlazan a registros individuales; no convierten un porcentaje de cobertura en conformidad.

| Corte | Producto verificable |
|---|---|
| M1. Contrato de auditoría y anclaje | Esquema de afirmación/hallazgo, metadatos de rectángulos ligados a hash/página, manifiesto reanudable e inventario S4.3; visor sin búsqueda textual al abrir una referencia. Inventario PDF y preparación selectiva: extracción nativa o adaptador del MCP OCR ya probado localmente. |
| M2. Un piloto pequeño | S4.3.2.7: matriz de sus 15 elementos y dos mensajes, citas cotejadas y resaltado por metadatos, discrepancias y cambios en copia cuando procedan. El usuario evalúa el resultado antes de ampliar la corrida. |
| M3. Corrida completa posterior | Los otros diez modelos con sustento enriquecido o vacío declarado, interfaces cruzadas, informe consolidado y versiones identificadas para revisión. S4.3.3 figura `SIN-MODELO`. |
| M4. Atención trazable | Ampliación compatible de observaciones, vínculo a sesión/diff, resolución individual, reapertura y pruebas por CLI/API/MCP. |
| M5. Consola de revisión | Filtros y líneas de tiempo de todos los procesos; lectura de evidencia y comparación de versiones. Desde aquí se invita a comentar sobre la versión auditada. |

La división evita mezclar una corrida de búsqueda de evidencia con el tratamiento de opiniones de usuarios: primero se hace explícita la base y sus vacíos; después cada comentario se evalúa contra una versión conocida. M1 y M2 prueban el contrato y el costo real en **un** modelo antes de ejecutar los otros diez; M3 aporta la base revisable; M4 y M5 convierten el historial en un flujo consultable sin crear otra fuente maestra.
