---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
---

# Adaptador MCP actual

El servidor MCP, por `stdio` o por HTTP (`streamable-http`), usa los mismos servicios de consulta, observaciones y sesiones de edición que la CLI y la API. La edición lógica se hace sobre la tabla y el sustento de una copia; el BPMN se regenera.

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

| Herramienta | Operación |
|---|---|
| `listar_procesos` | Árbol institucional |
| `leer_proceso` | Detalle por código NT |
| `listar_observaciones` | Registros y revisión vigente |
| `registrar_observacion` | Crea comentario u observación con revisión esperada; acepta `referencia` y `formato` (`texto` o `html`) |
| `responder_observacion` | Añade respuesta e historial con revisión esperada; acepta `formato` |
| `cambiar_estado_observacion` | Abre o resuelve una observación con revisión esperada |
| `leer_elemento` | Lee una caja o flujo por ID y sus fuentes registradas |
| `leer_fuente` | Lee texto acotado de una fuente y página registrada, con hash y estado de extracción |
| `redactar_observacion` | Mejora la redacción de una observación propia de Claudia (html o texto) sin cambiar su sentido; el texto anterior queda en el historial (`REDACTADA`) |
| `listar_versiones` | Versiones integradas del proceso, la más reciente primero, con titular, motivo, observación y conteo de cajas agregadas, modificadas y retiradas (plan B) |
| `leer_version` | Una versión con su cambio por caja (antes y después por campo, ID BPMN) y el diff de tabla y sustento |
| `estado_modelo` | Estado de edición del proceso: `LIBRE`, `EN-EDICION` (titular, motivo, vencimiento) o `APROBADO`, y borradores abiertos (`DEC-069`) |
| `iniciar_edicion` | Toma el bloqueo del proceso a nombre de Claudia (motivo, observación y trabajo) y abre una copia aislada; 409 si otro titular lo tiene vigente |
| `iniciar_borrador` | Abre una copia que no bloquea el proceso; solo se integra cuando el proceso está libre (`DEC-069`) |
| `leer_sesion` | Lee manifiesto, revisiones y preparación |
| `leer_documento_copia` | Lee tabla, sustento o fuentes de la copia |
| `editar_documento_copia` | Edita texto de la copia con hash esperado |
| `preparar_cambio` | Numera cajas nuevas, regenera BPMN/HTML en la copia y presenta diff y D1–D5; `aceptar_hallazgos` adopta hallazgos con justificación y sustento modificado |
| `aplicar_cambio` | Integra la preparación con revisión esperada y control de conflicto |
| `cerrar_edicion` | Cierra sin integrar y libera el bloqueo si la sesión lo tenía; conserva la copia. Tras `aplicar_cambio` no hace falta |
| `anclar_en_copia` | Ancla una cita literal verificada de un fragmento a una caja de la copia |
| `retirar_anclas_copia` | Retira anclas de cajas indicadas o huérfanas en la copia |
| `generar_modelo` | Genera o comprueba un modelo integrado; devuelve salida e informe D1–D5; `forzar` exige `justificacion` |
| `auditoria_inventariar` | Inventaría elementos, flujos, carriles y mensajes |
| `auditoria_registrar` | Registra afirmaciones con citas verificadas (lote atómico) |
| `auditoria_cobertura` | Reemplaza la cobertura fuente→modelo (lote atómico) |
| `auditoria_reconfirmar` | Reconfirma la auditoría tras un cambio de tabla sin perder lo vigente |
| `auditoria_correr` | Estado reanudable de la auditoría de un alcance |
| `auditoria_interfaces` | Candidatos de interfaz entre padre, hijos y hermanos |
| `auditoria_informe` | Informe de cobertura, resultados, citas y anclas |
| `buscar_fuentes` | Pasajes candidatos de la biblioteca, acotados y con ubicación |
| `contexto_fragmento` | Texto completo de un fragmento y sus vecinos |
| `anclar_cita` | Página y rectángulos de una cita en el PDF, sin escribir |
| `buscar_notas` y `leer_nota` | Notas de áreas autorizadas por propiedades y texto; lectura por tramos con enlaces |
| `listar_documentos`, `leer_documento` y `leer_texto_documento` | Inventario de la biblioteca, ficha y páginas del texto derivado |
| `listar_temas` | Vocabulario de temas de búsqueda |
| `listar_reglas` y `leer_regla` | Reglas normativas y sus eventos de revisión |
| `buscar_glosario` | Términos del glosario vivo |
| `buscar_decisiones` | Decisiones del registro por ID o texto |
| `revisar_etiquetas` | Revisión o recuento de etiquetas, sin escribir |
| `paquete_contexto` | Paquete de contexto de una tarea sobre un proceso: reglas propias y, aparte, las de procesos superiores; procesos relacionados con sus cajas; aviso si la auditoría no está vigente |
| `indice_documento` y `leer_articulos` | Índice de artículos de un documento y texto de un rango (hasta 40), para recorrer el capítulo de una figura |
| `leer_observacion` | Una observación completa con su resolución vigente y las anteriores |
| `registrar_analisis` y `registrar_propuesta` | Etapas de análisis (con hipótesis consideradas) y propuesta de una observación (`DEC-065`, `DEC-067`); reemplazar un análisis exige motivo y conserva el anterior |
| `observaciones_por_etapa` | Observaciones por etapa, en resumen por defecto; `detalle` agrega la resolución |
| `devolver_decision` | El agente no aplica una decisión ambigua: la devuelve con una pregunta, que queda como comentario, y la observación vuelve a decidirse; la decisión se conserva en `decisiones_devueltas` |
| `iniciar_correccion` y `registrar_aplicacion` | Corrección de una observación definida y cierre con evidencia o espera de evidencia |

Las escrituras del MCP firman con el alias del agente, **Claudia** (`DEC-064`). Un `ErrorDominio` llega como error de herramienta legible, con su código HTTP, no como fallo inesperado. Las escrituras de observaciones responden con una confirmación compacta (ID, referencia, etapa, estado, revisión y último evento); el registro completo se lee con `leer_observacion`.

No expone archivos arbitrarios, aprobación institucional ni validación normativa. El agente puede aplicar cambios sin una autorización por operación, conforme al [plan](../plan-mesa-modelamiento.md), pero la preparación y los hashes de destino impiden sustituciones silenciosas. La sesión no convierte una propuesta en regla `VALIDADO`.

## Conexión con Claude Code

El archivo `.mcp.json` de la raíz del repositorio registra el servidor `mesa-modelamiento`. Lo ejecuta dentro del contenedor `api`, que ya tiene el entorno instalado, con `docker compose exec -T --user 1000:1000 -e HOME=/tmp api modelador-procesos mcp --transporte stdio`. Requiere el compose levantado. El usuario `1000:1000` corresponde al equipo actual: en otro equipo se ajusta para que los archivos escritos conserven su propietario. El cliente carga el servidor al iniciar la sesión.

## Transporte HTTP y cola de trabajos (`DEC-068`)

El servicio `mcp-http` del compose sirve el mismo servidor con `modelador-procesos mcp --transporte streamable-http --host 0.0.0.0 --port 8768`, publicado solo en `127.0.0.1:8768/mcp`. La protección contra DNS rebinding admite únicamente las cabeceras Host de `MESA_MCP_HOSTS` (por defecto `127.0.0.1:8768,localhost:8768`); otra cabecera recibe 421. Lo usan los agentes de OpenClaw, que lo registran como `mesa-modelamiento` y filtran por agente las herramientas que ven ([agentes de OpenClaw](../openclaw/README.md)).

| Herramienta | Operación |
|---|---|
| `listar_trabajos` | Trabajos de la cola por estado, tipo o proceso, con conteo por estado |
| `tomar_trabajo` | Toma el trabajo pendiente más antiguo de un tipo (`ANALISIS` o `APLICACION`) y lo marca EN-CURSO a nombre de Claudia. La aplicación va de a una observación y solo de procesos libres, sin otra aplicación en curso (`DEC-069`) |
| `completar_trabajo` | Cierra un trabajo tomado como HECHO o ERROR con un resumen |

La cola vive en `.mesa-trabajos/cola.json`, fuera de Git, con bloqueo de archivo. Un trabajo EN-CURSO por más de 45 minutos vuelve a estar disponible. Definir una resolución encola su `APLICACION`; la web encola `ANALISIS` con el botón de análisis.

## Paridad con la CLI (2026-11-25)

La CLI tiene 66 comandos y el MCP 48 herramientas (tandas 1, 2A y 2B cerradas el 2026-11-25); con la cola de trabajos de `DEC-068` el MCP suma 51 y la CLI agrega los grupos `trabajos` y `relevo`; con el bloqueo de `DEC-069` el MCP suma 53 (`estado_modelo`, `iniciar_borrador`) y la CLI agrega `sesiones estado` y `sesiones liberar`; con las versiones livianas suma 55 (`listar_versiones`, `leer_version`) y la CLI agrega `versiones listar` y `versiones leer`; con `redactar_observacion` el MCP suma 56 y la CLI agrega `observaciones redactar`; con `devolver_decision` suma 57, y `registrar_aplicacion` acepta `resultado` (`ACLARADA`, `NO-PROCEDE`, `CAMBIO-MODELO`, `CAMBIO-SUSTENTO`). El MCP no tiene herramienta para definir: esa etapa es de una persona, por la web, la API o la CLI.

| Grupo de la CLI | En el MCP | Comentario |
|---|---|---|
| `arbol`, `proceso`, `fuente` | `listar_procesos`, `leer_proceso`, `leer_fuente` y además `leer_elemento` | Completo |
| `observaciones` (4) | Las 4 | Completo para el modelo actual de observaciones |
| `sesiones` (9, con `anclar` y `retirar-anclas`) | Las 9 | Completo |
| `modelo` | `generar_modelo` | Completo, con aceptación justificada de hallazgos |
| `auditoria` (7, con `reconfirmar`) | Las 7 | Completo |
| `fuentes buscar`, `fuentes contexto`, `fuentes anclar` | `buscar_fuentes`, `contexto_fragmento`, `anclar_cita` | Completo |
| Resto de `fuentes` (19) | No | Preparación de la biblioteca: extracción, OCR, segmentación, índice y bancos de prueba. Es administración, no edición; `temas comprobar` y `regimen` podrían exponerse como lectura |
| `api`, `mcp`, `contrato` | No aplica | Infraestructura |

Ya no faltan comandos de edición ni de auditoría. Las acciones de producto pendientes (tanda 2) se listan en la tabla siguiente.

## Canales de conocimiento (`DEC-066`, 2026-11-25)

El MCP debe ser el único canal de un agente hacia el repositorio, no solo hacia los modelos. Hasta ahora el agente lee el conocimiento directamente del disco. Esta tabla inventaría el conocimiento que ya existe, cómo se estructura y qué canal le falta.

| Conocimiento | Estructura actual | Canal hoy | Canal que falta |
|---|---|---|---|
| Biblioteca: catálogo de documentos | `01-referencias/00-catalogo/catalogo-documental.csv` (ID, ruta, hash, emisor, vigencia), `regimen-documental.json`, evaluación de calidad | CLI de preparación | Consultar un documento por ID o filtros: metadatos, vigencia, régimen, calidad y estado de extracción |
| Biblioteca: textos derivados | `09-derivados-texto/cache/`: Markdown paginado por documento, `00-indice.md`, fragmentos por artículo o numeral e índice FTS5 | `buscar_fuentes`, `contexto_fragmento`, `anclar_cita` | Leer el texto derivado de un documento por página o sección y recorrer el índice |
| Vocabulario de temas | `catalogo/temas-busqueda.json` y `temas-sugeridos.jsonl` | CLI `fuentes temas` | Comprobar y sugerir temas; listar términos de un tema |
| Guías de lectura de fuentes | 15 notas en `03-conocimiento/fuentes/` | Lectura directa | Listar y leer guías por documento o tema |
| Reglas normativas | 36 YAML en `03-conocimiento/reglas/` (`BORRADOR-IA`), eventos en `revisiones/` y `catalogo-reglas.csv` generado | Lectura directa | Listar y filtrar por proceso, dominio o estado; leer una regla con sus eventos; proponer una regla `BORRADOR-IA`, nunca validarla |
| Manual BPMN y paleta | 24 notas en `03-conocimiento/manual-bpmn/` y el catálogo de símbolos | Lectura directa | Leer notas y consultar la paleta permitida (`DEC-027`) |
| Actores y catálogos comunes | `03-conocimiento/actores-y-roles/` (3 notas); sistemas, documentos, riesgos y reglas de negocio vacíos | Lectura directa | Listar y leer |
| Glosario | `glosario.md` | Lectura directa | Buscar un término y devolver su definición |
| Decisiones | `00-gobernanza/registro-decisiones.md` (DEC-001 a DEC-066) | Lectura directa | Buscar y leer una decisión por ID, proceso o texto; registrar una nueva con control de revisión |
| Gobierno y método | Estándares, protocolos, convenciones, plantillas y `vocabulario-etiquetas.yaml` | Lectura directa | Leer por nombre; listar plantillas |
| Notas en general | Markdown con propiedades (`tipo`, `area`, `estado_documento`, `clase_conocimiento`, `tags`) y notas índice `00-*.md` | Lectura directa | Buscar notas por propiedades y texto, y leer una nota, dentro de una lista cerrada de áreas y nunca en `originales` |
| Etiquetas | `gestionar_etiquetas.py` (revisar, listar, aplicar, renombrar) | Script | Revisar y listar; aplicar y renombrar solo como escritura gobernada |
| Estado del proyecto y coordinación | `estado-del-proyecto.md`, reuniones, diario; Bases y Canvas como vistas | Lectura directa | Leer el estado y las actas |
| Paquete de contexto | Plantilla `paquete-contexto.yaml`; manual operativo, sección 6.6 | Armado manual | Armar el paquete de una tarea: ficha, modelo vigente, reglas del proceso, guías y glosario pertinentes, decisiones relacionadas, observaciones abiertas y estado de auditoría |
| Preparación documental | CLI `fuentes` (inventario, extracción, OCR, segmentación, índice, régimen, bancos de prueba) | CLI | Exponer como operaciones de administración, separadas de la consulta |

**Tanda 2A (2026-11-25).** Los canales de solo lectura de la tabla quedan disponibles en el servicio `conocimiento.py`, la CLI (`conocimiento ...`) y el MCP: notas, biblioteca, temas, reglas, glosario, decisiones, etiquetas y paquete de contexto. La consulta usa los manifiestos de preparación (242 documentos), no solo `catalogo-documental.csv`, que cubre 13. Para leer YAML se agregó la dependencia PyYAML. `gestionar_etiquetas.py` recorre el disco cuando no hay `git`, como en el contenedor del MCP. Quedan pendientes las escrituras (2C) y la preparación documental como administración (2D).

Las escrituras de conocimiento siguen el protocolo de conocimiento confiable: la IA solo propone (`BORRADOR-IA`) y ninguna herramienta valida ni atribuye conformidad. Canvas y Bases son vistas y no se exponen como fuente.

## Brechas para que un agente edite al nivel actual (2026-11-25)

Hasta el 2026-11-25 los diagramas de S4.3 se editaron con escritura directa y scripts auxiliares del agente, no por este MCP. El usuario decidió probar el producto editando solo por MCP. Esta tabla lista las acciones que el agente hacía por fuera y que el MCP todavía no cubre. La prioridad 1 bloquea el experimento.

| Prioridad | Acción del agente | Cómo se hacía | Situación en el MCP | Qué falta |
|---|---|---|---|---|
| Cerrada | Adoptar un modelo con hallazgos D3 o D4 ya documentados | `modelar.py <codigo> --forzar` | `preparar_cambio` deja el resultado en la copia y `aplicar_cambio` no lo integra | Aceptación explícita de hallazgos con justificación, registrada en la sesión y exigida en el sustento. Hoy bloquea S4.3.2.3 y S4.3.2.6 |
| Cerrada | Resolver observaciones por etapas (`DEC-065`) | No existía | Solo registrar, responder y cambiar entre `ABIERTA` y `RESUELTA` | Registrar análisis y opciones, listar las definidas por una persona, registrar la aplicación con sesión, diff y D1–D5. La definición la hace una persona por la API o la web |
| Cerrada | Registrar una observación sobre una caja por su ID de tabla | Script que traduce el ID de tabla al ID BPMN por el nombre | Exige el ID BPMN interno | Aceptar el ID de tabla o el número de caja y completar la referencia «Caja N (ID)» |
| 2 | Editar celdas, filas, mensajes, pools y columnas de la tabla | `tabla_edit.py` (operaciones estructuradas) | Solo se reescribe el texto completo del documento | Operaciones estructuradas con validación de columnas, IDs únicos y siguiente número libre (`DEC-044`) |
| 2 | Coordinar un cambio entre dos procesos (interfaz) | Edición directa de ambas tablas | Una sesión por proceso, sin vínculo | Sesiones vinculadas o integración conjunta, para que una interfaz no quede a medias |
| Cerrada | Reconfirmar la auditoría tras cambiar la tabla | `rehacer.py`: reinventariar, conservar lo vigente, marcar superadas y registrar nuevas | Sin herramientas de auditoría | Inventariar, registrar afirmaciones, registrar cobertura, informe con verificación y reconfirmación tras el cambio. La CLI ya tiene parte (`auditoria ...`) |
| Cerrada | Buscar pasajes en la biblioteca y leer un fragmento | `fuentes buscar` y `fuentes contexto` por CLI | `leer_fuente` solo lee anclas ya registradas | Búsqueda acotada y lectura por fragmento |
| Cerrada | Anclar o retirar citas del visor | `anclar_fragmento` y edición del JSON | Solo reescribir `fuentes-visor.json` completo | Anclar una cita a una caja y retirar anclas de cajas eliminadas |
| 2 | Registrar decisiones y actualizar documentos de gobierno | Edición directa de `registro-decisiones.md`, `estado-del-proyecto.md`, `alcance.md`, informes y notas índice | Solo tabla, sustento y fuentes del proceso | Agregar una decisión `DEC-NNN` con control de revisión. Los demás documentos, con una lista cerrada y la misma sesión recuperable |
| Cerrada | Recibir errores de dominio claros | — | Un `ErrorDominio` (conflicto, sesión terminada) llega como excepción inesperada con traza completa | Convertir `ErrorDominio` en error de herramienta con mensaje y código. Observado en la primera edición por MCP, el 2026-11-25 |
| Cerrada | Cerrar una sesión ya integrada | — | `aplicar_cambio` termina la sesión y `cerrar_edicion` responde «La sesión ya terminó» | Documentar que no hace falta cerrar tras aplicar, o que cerrar sea idempotente |
| 3 | Comprobación global y revisión de etiquetas | `construir_modelos.py --check` y `gestionar_etiquetas.py revisar` | No disponibles | Herramientas de solo lectura que devuelvan el resumen |
| 3 | Regenerar sin caché o exportar SVG y PNG por solicitud | `modelar.py --sin-cache` y `--exportar-imagenes` | No disponibles | Opciones de `preparar_cambio` |
| — | Commit, push, pruebas y cambios de herramientas | Git y pytest | Fuera del alcance del MCP | Siguen a cargo de una persona o de una tarea de desarrollo autorizada |

Las filas `Cerrada` quedaron resueltas en la tanda 1 (2026-11-25), en servicio, CLI y MCP con pruebas. También se agregó la numeración de cajas nuevas al preparar una sesión, que antes solo hacía `modelar.py`. La regla del experimento es que, desde la conexión del MCP, todo cambio de modelo se hace por sus herramientas. Cuando una acción falte, se registra aquí en lugar de resolverla por fuera.

## Brechas detectadas en la revisión de S4.3.2 (2026-11-26)

Ocho revisores (agentes que firman como Claudia) revisaron S4.3.2 y sus subprocesos solo con este MCP y registraron 70 observaciones. Encontraron estas fallas; ninguna impidió el trabajo, pero varias los obligaron a leer archivos por fuera del MCP.

| Prioridad | Falla | Efecto | Qué falta |
|---|---|---|---|
| 1 | `leer_proceso` omite los flujos marcados «por defecto» | Las compuertas parecen tener ramas sin salida (en S4.3.2.3, 81 secuencias frente a 84 de la auditoría); hubo que leer la tabla con `leer_nota` | Incluir el flujo por defecto con su marca |
| 1 | `leer_elemento` responde 404 con el ID de tabla (p. ej., `E-GREG`), aunque su descripción dice aceptarlo | Solo funciona con el ID BPMN interno | Resolver ID de tabla y número de caja, como `registrar_observacion` |
| 2 | `leer_proceso` de S4.3.2.3 supera el tamaño máximo de respuesta | El resultado se guarda en un archivo y el agente lo filtra por fuera | Paginación o lectura por carril o rango de cajas |
| 2 | `leer_articulos` falla con la huella del documento | Solo acepta el ID de catálogo (`CON-001`) | Aceptar también la huella |
| 2 | `listar_documentos` con texto («adicional», «Contraloría») no devuelve resultados | Hay que filtrar por área | Búsqueda por título y descripción |
| 2 | No se pueden vincular observaciones de procesos distintos | Las interfaces entre S4.3.2.5 y S4.3.2.6 solo se citan en el texto | Vínculo entre observaciones de procesos distintos |
| 3 | No hay herramienta para leer el estándar de artefactos (paleta 7.3 y carriles 7.4) | Se leyó con `grep`; `buscar_notas`/`leer_nota` sirven si la nota está indexada | Confirmar que el estándar se puede leer con `leer_nota` y documentarlo |
| 3 | `auditoria_interfaces` solo compara mensajes, no las anotaciones que prometen una interfaz | Una interfaz anotada sin mensaje (S4.3.2.3 → S4.3.2.8) no aparece como candidata | Revisar también las anotaciones |

## Hallazgos del primer experimento por MCP (2026-11-25)

Claudia analizó y propuso las 14 observaciones de S4.3.2.6 y S4.3.2.5 usando solo el MCP: paquete de contexto, guías, búsqueda y lectura de fuentes, comprobación del modelo y etapas de resolución. Funcionó sin leer el disco. El uso dejó estas brechas:

| Brecha | Efecto | Tanda sugerida |
|---|---|---|
| La selección múltiple no marca opciones excluyentes entre sí | Una persona puede acoger opciones contradictorias (por ejemplo, «mantener» y «cambiar») | 2B, ajuste |
| Al elegir opciones en la web no hay campo de comentario o dato complementario | Una opción que pide un dato (un plazo) obliga a usar «respuesta propia». El servicio ya acepta texto con las opciones | 2B, ajuste de la pantalla |
| El vínculo solo admite observaciones resueltas y del mismo proceso | No se puede declarar que una observación «sigue a» otra pendiente ni enlazar observaciones de procesos vecinos (interfaces) | 2B, ajuste |
| `observaciones_por_etapa` devuelve el análisis y la propuesta completos | Respuestas muy largas para el agente | Cerrada: resumen por defecto y confirmaciones compactas |
| El paquete de contexto trae términos de glosario genéricos y todas las reglas de los procesos ancestros | Ruido: 31 reglas, la mayoría de S4.3 en general | Cerrada: glosario cruzado solo con las cajas; reglas superiores aparte y compactas |
| La auditoría del paquete sale de la última corrida, aunque la tabla cambió | Puede mostrar un estado desactualizado sin advertirlo | Cerrada: `vigente` y advertencia |
| La búsqueda por palabras no encuentra artículos redactados con otros términos, y las cajas vecinas se citaban de memoria | 7 de 13 recomendaciones cambiaron en la revisión directa | Cerrada: índice y lectura por artículos, procesos relacionados y método `DEC-067` |
| No hay herramienta para incorporar un documento nuevo a la biblioteca | Las propuestas que necesitan la Directiva 005-2023-CG o el D.S. 072-2025-EF quedan en espera | 2D |
| No se pueden editar guías de lectura ni otras notas de conocimiento | Una propuesta que actualiza la guía de la Ley 31589 no puede aplicarse por MCP | 2C |
