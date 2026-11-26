---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
fecha_creacion: 2026-11-26
fecha_actualizacion: 2026-11-26
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Plan B: versiones livianas para la validación con especialistas

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

Estado: **implementado el 2026-11-26** (B1, B2 y B3; detalle vigente en [sesiones de edición](sesiones-edicion.md#versiones)). Además, la API pasó a correr con el usuario local, como el MCP, para que ambos puedan escribir el registro. Objetivo: que desde el inicio de la validación con
especialistas (2026-11-26) cada cambio integrado en un modelo quede numerado, explicado por elemento y
consultable, sin construir todavía el almacén definitivo (eso es del [sistema nuevo](plan-sistema-nuevo.md)).

## Principio: reutilizar lo que ya existe

Cada integración ya conserva en `.mesa-sesiones/<codigo>/<sesion>/` el estado anterior (`origen/`) y el nuevo
(`copia/`: tabla, sustento, fuentes y BPMN generado), y desde `DEC-069` el manifiesto sabe quién, para qué, qué
observación y qué trabajo. **Una versión es una sesión integrada**: basta con numerarla, calcular su cambio por
elemento y exponerla. No se copia contenido nuevo.

## Alcance

| Incluye | No incluye (queda para el sistema nuevo) |
|---|---|
| Número de versión por proceso (v1, v2…) al integrar | Base de datos |
| Cambio por elemento (agregado, modificado con campos antes/después, retirado) y marca de sustento o fuentes cambiados | Operaciones por elemento vía MCP |
| Consultar versiones por API, CLI, MCP y web | Comparar dos versiones arbitrarias |
| Ver el diagrama de una versión con sus cajas cambiadas resaltadas | Restaurar automáticamente una versión anterior |
| Evento «versión vN» en la observación atendida | Cambios hechos fuera de la aplicación (se ven en Git) |
| Respaldo diario de `.mesa-sesiones/` y del registro de versiones | |

Restaurar una versión, si hiciera falta, se hace abriendo una sesión y pegando la tabla de esa versión; queda
como una versión nueva.

## Contrato (fijado antes de repartir el trabajo)

Registro: `.mesa-versiones/<codigo>.jsonl`, una línea por versión, fuera de Git, escrito con candado de archivo.

```json
{
  "numero": 7,
  "codigo": "S4.3.2.6",
  "fecha": "2026-11-26T15:04:05+00:00",
  "sesion": "5f3c…",
  "titular": "Claudia",
  "motivo": "Aplicar OBS-12",
  "observacion": "OBS-12",
  "trabajo": "T-…",
  "documentos": {"tabla": true, "sustento": true, "fuentes_visor": false},
  "elementos": {
    "agregados": [{"id": "E-T9", "numero": "41", "nombre": "…"}],
    "retirados": [{"id": "E-T4", "numero": "11", "nombre": "…"}],
    "modificados": [{"id": "E-T3", "numero": "8", "campos": {"Nombre": ["antes", "después"]}}]
  },
  "hashes": {"tabla": "…", "sustento": "…", "bpmn": "…"}
}
```

| Superficie | Operación |
|---|---|
| API | `GET /api/procesos/{codigo}/versiones` (lista sin `elementos`), `GET /api/procesos/{codigo}/versiones/{numero}` (con `elementos` y diff de texto de tabla y sustento), `GET /api/procesos/{codigo}/versiones/{numero}/bpmn` (XML de la copia integrada) |
| MCP | `listar_versiones(codigo)`, `leer_version(codigo, numero)` |
| CLI | `versiones listar <codigo>`, `versiones leer <codigo> <numero>` |

## Paquetes de trabajo (paralelizables)

| Paquete | Agente | Archivos que posee | Depende de | Entregable y aceptación |
|---|---|---|---|---|
| **B1. Servicio y transporte** | Backend | `mesa_modelamiento/versiones.py` (nuevo), llamada desde `sesiones.integrar`, `api.py`, `esquemas.py`, `mcp_adapter.py`, `cli.py`, `contracts/openapi.json`, pruebas | Contrato de arriba | Integrar una sesión crea vN con el cambio por elemento correcto (prueba con agregado, retiro y modificación); las tres superficies responden; contrato OpenAPI vigente; evento en la observación si la sesión la declara |
| **B2. Pestaña «Historial»** | Frontend | `HistoryPanel.vue` (nuevo), `ModelWorkspace.vue` (pestaña), `BpmnCanvas.client.vue` (marcadores), `main.css`, tipos generados | Contrato (puede empezar con datos simulados) | Lista de versiones; al elegir una: cajas cambiadas con antes/después, clic selecciona la caja; «Ver diagrama de esta versión» carga su BPMN en solo lectura con verde (agregada), ámbar (modificada) y una lista de retiradas; lint y tipos |
| **B3. Operación y documentación** | Cualquiera | `docs/` (sesiones, API, MCP, CLI, modelo de datos, entorno), `scripts/respaldar-estado.sh` (nuevo), `estado-del-proyecto.md` | B1 terminado para documentar | Respaldo diario comprimido de `.mesa-sesiones/` y `.mesa-versiones/` a `~/respaldos/`; documentación sincronizada; validador de memoria y markdownlint |

Reglas de coordinación: cada paquete en su propia rama o worktree; nadie edita archivos que posee otro paquete;
un cambio de contrato se acuerda antes y se anota en este plan. Integración final: pruebas, contrato, lint y
tipos del frontend, revisión del usuario y un commit por paquete.

Esfuerzo estimado: B1 y B2 de 2 a 3 horas cada uno en paralelo; B3 una hora.

## Durante la validación

- Quien edite declara su nombre y el motivo (por ejemplo, «Reunión con especialistas SGGOS 2026-11-26»).
- Al cerrar cada jornada: commit de los procesos modificados (el estado vigente queda en Git) y respaldo de
  `.mesa-sesiones/` y `.mesa-versiones/` (el historial fino queda fuera de Git).
- Las versiones son evidencia de trabajo; ninguna equivale a conformidad o validación de los especialistas, que
  se registra en el sustento según las reglas del proyecto.
