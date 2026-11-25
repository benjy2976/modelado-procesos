---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Sesiones de edición recuperables

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

`ServicioSesiones` conserva en `.mesa-sesiones/<codigo>/<id>/` dos carpetas: `origen/` con los bytes del árbol de trabajo al iniciar, y `copia/` con tabla, sustento, metadatos de fuentes y derivados editables. El manifiesto guarda hash SHA-256 de cada origen, revisión de sesión, estado y resultado de preparación. El almacén persiste fuera de `99-temporal` y está excluido de Git porque puede contener trabajo no confirmado; **no se borra al integrar o cerrar**. El editor debe respaldar ese almacén junto con el repositorio si necesita recuperación entre equipos.

Cada proceso tiene un estado de edición (`DEC-069`): `LIBRE`, `EN-EDICION` o `APROBADO`. Una sesión en modo `EDICION` toma el bloqueo del proceso: `activa.json` registra titular, motivo, observación, trabajo, inicio y vencimiento. Solo hay un titular por proceso; otra solicitud recibe 409 con quién lo tiene y hasta cuándo. Cada edición o preparación renueva el vencimiento (`MESA_BLOQUEO_MINUTOS`, 30 por defecto); si vence, el bloqueo se suelta al consultarlo y la sesión queda `VENCIDA`, sin perder su copia. Una persona puede liberar un bloqueo con autor y motivo (sesión `LIBERADA`). Integrar o cerrar libera el bloqueo. Las sesiones en modo `BORRADOR`, que abre el asistente, no bloquean y solo se integran cuando el proceso está libre y sin cambios desde la copia. El candado de archivo serializa las operaciones locales. No hay coedición distribuida ni identidad autenticada: el titular es el nombre que declara la persona o el agente. Si la tabla o el sustento declaran `estado_institucional: APROBADO`, no se abre la sesión. Los originales en `01-referencias/**/originales` nunca forman parte de la copia editable.

La edición acepta `tabla`, `sustento` y `fuentes_visor` mediante texto UTF-8 completo y hash de revisión del documento. El visor ofrece un formulario de texto para cada uno; un agente usa la misma acción por MCP. `preparar_cambio` numera las cajas nuevas con el mismo criterio de `modelar.py` (`DEC-044`), ejecuta `construir_modelos.py --tabla` sobre la copia y devuelve diff y hallazgos. Con `aceptar_hallazgos` (justificación de al menos 20 caracteres) adopta un resultado con hallazgos, como `--forzar`, solo si el sustento de la copia también cambió; la justificación queda en la preparación. `anclar` y `retirar_anclas` editan `fuentes-visor.json` de la copia con citas verificadas o quitando anclas de cajas retiradas. `cerrar` sobre una sesión ya integrada o cerrada no cambia nada. SVG y PNG no se generan. Un resultado con hallazgos permanece en la copia para corregirse; la aplicación no lo integra. El generador sigue escribiendo su informe operativo en `99-temporal/modelos/`.

`aplicar_cambio` exige la revisión de sesión preparada y comprueba que **todos** los archivos de destino conservan los hashes capturados al iniciar. Si otra edición, incluso sin commit, cambió un archivo, devuelve `409` sin escribir. La integración reemplaza solo los archivos que difieren; ante fallo de escritura intenta restaurar desde la instantánea. La instantánea permanece disponible para recuperación manual y comparación posterior. El resultado queda en el árbol de trabajo para revisión con Git; ninguna acción crea commits ni atribuye aprobación institucional.

La prueba local cubre copia de cambios no confirmados, el bloqueo con titular, vencimiento y liberación, los borradores que no bloquean, conflicto de documento, conflicto de destino, preservación del origen, integración de sustento por MCP y exclusión de un documento `APROBADO`. La prueba focalizada con S4.3.2.3 reprodujo hallazgos D3 de ciclos con acumulación de tokens y D4 de trazado en la tabla actual; por eso una modificación de esa tabla no se puede integrar automáticamente mientras esos hallazgos permanezcan. La sesión cerrada de prueba conserva su instantánea; no modificó el proceso. Si la tabla no cambió, `preparar` conserva el BPMN vigente y permite integrar solo sustento o metadatos válidos. La revisión visual del formulario sigue pendiente mientras no esté disponible un navegador para QA.
