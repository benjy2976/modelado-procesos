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
| `registrar_observacion` | Crea comentario u observación con revisión esperada |
| `responder_observacion` | Añade respuesta e historial con revisión esperada |
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

No expone archivos arbitrarios, aprobación institucional ni validación normativa. El agente puede aplicar cambios sin una autorización por operación, conforme al [plan](../plan-mesa-modelamiento.md), pero la preparación y los hashes de destino impiden sustituciones silenciosas. La sesión no convierte una propuesta en regla `VALIDADO`.
