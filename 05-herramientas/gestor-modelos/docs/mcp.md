---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
---

# Adaptador MCP actual

El servidor MCP por `stdio` usa los mismos servicios de consulta, observaciones y sesiones de edición que la CLI y la API. La edición lógica se hace sobre la tabla y el sustento de una copia; el BPMN se regenera.

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
| `iniciar_edicion` | Conserva instantánea y abre copia aislada |
| `leer_sesion` | Lee manifiesto, revisiones y preparación |
| `leer_documento_copia` | Lee tabla, sustento o fuentes de la copia |
| `editar_documento_copia` | Edita texto de la copia con hash esperado |
| `preparar_cambio` | Regenera BPMN/HTML en copia y presenta diff y D1–D5 |
| `aplicar_cambio` | Integra la preparación con revisión esperada y control de conflicto |
| `cerrar_edicion` | Libera el editor sin borrar la copia |

Las escrituras del MCP firman con el alias del agente, **Claudia** (`DEC-064`).

No expone archivos arbitrarios, aprobación institucional ni validación normativa. El agente puede aplicar cambios sin una autorización por operación, conforme al [plan](../plan-mesa-modelamiento.md), pero la preparación y los hashes de destino impiden sustituciones silenciosas. La sesión no convierte una propuesta en regla `VALIDADO`.

## Conexión con Claude Code

El archivo `.mcp.json` de la raíz del repositorio registra el servidor `mesa-modelamiento`. Lo ejecuta dentro del contenedor `api`, que ya tiene el entorno instalado, con `docker compose exec -T --user 1000:1000 -e HOME=/tmp api modelador-procesos mcp --transporte stdio`. Requiere el compose levantado. El usuario `1000:1000` corresponde al equipo actual: en otro equipo se ajusta para que los archivos escritos conserven su propietario. El cliente carga el servidor al iniciar la sesión.

## Paridad con la CLI (2026-11-25)

La CLI tiene 43 comandos y el MCP 15 herramientas.

| Grupo de la CLI | En el MCP | Comentario |
|---|---|---|
| `arbol`, `proceso`, `fuente` | `listar_procesos`, `leer_proceso`, `leer_fuente` y además `leer_elemento` | Completo |
| `observaciones` (4) | Las 4 | Completo para el modelo actual de observaciones |
| `sesiones` (7) | Las 7 | Completo |
| `modelo` | No | Falta: generación focalizada, `--check` y exportación de imágenes. `preparar_cambio` genera solo dentro de una sesión |
| `auditoria` (6) | No | Faltan los 6: inventariar, registrar, cobertura, correr, comparar interfaces e informe |
| `fuentes buscar`, `fuentes contexto`, `fuentes anclar` | No | Faltan: el agente los necesita para sustentar y anclar |
| Resto de `fuentes` (19) | No | Preparación de la biblioteca: extracción, OCR, segmentación, índice y bancos de prueba. Es administración, no edición; `temas comprobar` y `regimen` podrían exponerse como lectura |
| `api`, `mcp`, `contrato` | No aplica | Infraestructura |

Faltan 10 comandos que sí intervienen en la edición y la auditoría. Además, algunas acciones no existen ni en la CLI ni en el MCP; se listan en la tabla siguiente.

## Brechas para que un agente edite al nivel actual (2026-11-25)

Hasta el 2026-11-25 los diagramas de S4.3 se editaron con escritura directa y scripts auxiliares del agente, no por este MCP. El usuario decidió probar el producto editando solo por MCP. Esta tabla lista las acciones que el agente hacía por fuera y que el MCP todavía no cubre. La prioridad 1 bloquea el experimento.

| Prioridad | Acción del agente | Cómo se hacía | Situación en el MCP | Qué falta |
|---|---|---|---|---|
| 1 | Adoptar un modelo con hallazgos D3 o D4 ya documentados | `modelar.py <codigo> --forzar` | `preparar_cambio` deja el resultado en la copia y `aplicar_cambio` no lo integra | Aceptación explícita de hallazgos con justificación, registrada en la sesión y exigida en el sustento. Hoy bloquea S4.3.2.3 y S4.3.2.6 |
| 1 | Resolver observaciones por etapas (`DEC-065`) | No existía | Solo registrar, responder y cambiar entre `ABIERTA` y `RESUELTA` | Registrar análisis y opciones, listar las definidas por una persona, registrar la aplicación con sesión, diff y D1–D5. La definición la hace una persona por la API o la web |
| 1 | Registrar una observación sobre una caja por su ID de tabla | Script que traduce el ID de tabla al ID BPMN por el nombre | Exige el ID BPMN interno | Aceptar el ID de tabla o el número de caja y completar la referencia «Caja N (ID)» |
| 2 | Editar celdas, filas, mensajes, pools y columnas de la tabla | `tabla_edit.py` (operaciones estructuradas) | Solo se reescribe el texto completo del documento | Operaciones estructuradas con validación de columnas, IDs únicos y siguiente número libre (`DEC-044`) |
| 2 | Coordinar un cambio entre dos procesos (interfaz) | Edición directa de ambas tablas | Una sesión por proceso, sin vínculo | Sesiones vinculadas o integración conjunta, para que una interfaz no quede a medias |
| 2 | Reconfirmar la auditoría tras cambiar la tabla | `rehacer.py`: reinventariar, conservar lo vigente, marcar superadas y registrar nuevas | Sin herramientas de auditoría | Inventariar, registrar afirmaciones, registrar cobertura, informe con verificación y reconfirmación tras el cambio. La CLI ya tiene parte (`auditoria ...`) |
| 2 | Buscar pasajes en la biblioteca y leer un fragmento | `fuentes buscar` y `fuentes contexto` por CLI | `leer_fuente` solo lee anclas ya registradas | Búsqueda acotada y lectura por fragmento |
| 2 | Anclar o retirar citas del visor | `anclar_fragmento` y edición del JSON | Solo reescribir `fuentes-visor.json` completo | Anclar una cita a una caja y retirar anclas de cajas eliminadas |
| 2 | Registrar decisiones y actualizar documentos de gobierno | Edición directa de `registro-decisiones.md`, `estado-del-proyecto.md`, `alcance.md`, informes y notas índice | Solo tabla, sustento y fuentes del proceso | Agregar una decisión `DEC-NNN` con control de revisión. Los demás documentos, con una lista cerrada y la misma sesión recuperable |
| 1 | Recibir errores de dominio claros | — | Un `ErrorDominio` (conflicto, sesión terminada) llega como excepción inesperada con traza completa | Convertir `ErrorDominio` en error de herramienta con mensaje y código. Observado en la primera edición por MCP, el 2026-11-25 |
| 3 | Cerrar una sesión ya integrada | — | `aplicar_cambio` termina la sesión y `cerrar_edicion` responde «La sesión ya terminó» | Documentar que no hace falta cerrar tras aplicar, o que cerrar sea idempotente |
| 3 | Comprobación global y revisión de etiquetas | `construir_modelos.py --check` y `gestionar_etiquetas.py revisar` | No disponibles | Herramientas de solo lectura que devuelvan el resumen |
| 3 | Regenerar sin caché o exportar SVG y PNG por solicitud | `modelar.py --sin-cache` y `--exportar-imagenes` | No disponibles | Opciones de `preparar_cambio` |
| — | Commit, push, pruebas y cambios de herramientas | Git y pytest | Fuera del alcance del MCP | Siguen a cargo de una persona o de una tarea de desarrollo autorizada |

La regla del experimento es que, desde la conexión del MCP, todo cambio de modelo se hace por sus herramientas. Cuando una acción falte, se registra aquí en lugar de resolverla por fuera.
