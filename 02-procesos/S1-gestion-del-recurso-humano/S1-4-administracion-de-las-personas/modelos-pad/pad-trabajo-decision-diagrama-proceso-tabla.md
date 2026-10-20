---
id: BAN-PAD-MOD-DECISION
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
proceso: []
fecha_creacion: 2026-10-20
fecha_actualizacion: 2026-10-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s1/s1-4
---

# Fase sancionadora - modelo de trabajo

Sube a: [Modelos BPMN de trabajo para el PAD](00-modelos-pad.md)

`OBS` significa texto observado en el borrador; `PROP`, representacion propuesta. La posible omision motivada del informe oral y las variantes de notificacion requieren revision juridica y de operacion.

## Pools

| Pool | Carriles |
|---|---|
| Fase sancionadora | Organo Sancionador |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|
| E-1 | Fase sancionadora | Organo Sancionador | inicio | Informe de instruccion recibido | T-1 | entra: Informe de instruccion | OBS | 6.8.15, p. 25 |
| T-1 | Fase sancionadora | Organo Sancionador | tarea | Comunicar la recepcion del informe | T-2 |  | OBS | 6.8.17, p. 26 |
| T-2 | Fase sancionadora | Organo Sancionador | subproceso | Gestionar oportunidad de informe oral | T-3 |  | PROP | 6.8.17-6.8.18, p. 26; detalle pendiente |
| T-3 | Fase sancionadora | Organo Sancionador | tarea | Evaluar el caso y emitir decision final | G-3 | sale: Decision final | OBS | 6.8.19-6.8.23, pp. 26-27 |
| G-3 | Fase sancionadora | Organo Sancionador | compuerta | ¿Cual es la decision? | T-4 [Sancion]; T-5 [Archivo] |  | PROP | 6.8.15 y 6.8.23, pp. 25-27 |
| T-4 | Fase sancionadora | Organo Sancionador | tarea | Emitir y notificar acto de sancion | F-1 | sale: Acto de sancion y constancia | OBS | 6.8.23, p. 27; anexo 9, p. 48 |
| F-1 | Fase sancionadora | Organo Sancionador | fin | Sancion comunicada |  |  | PROP | 6.8.23 y IX, pp. 27, 33-36 |
| T-5 | Fase sancionadora | Organo Sancionador | tarea | Emitir y notificar acto de archivo | F-2 |  | OBS | 6.8.23, p. 27; anexo 10, p. 49 |
| F-2 | Fase sancionadora | Organo Sancionador | fin | Archivo comunicado |  |  | PROP | 6.8.23 y IX, pp. 27, 33-36 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| Organo Instructor | E-1 | Informe de instruccion |
| T-1 | Servidor o ex servidor | Comunicacion de recepcion del informe |
| Servidor o ex servidor | T-2 | Solicitud de informe oral, si se presenta |
| T-4 | Servidor o ex servidor | Acto de sancion notificado |
| T-5 | Servidor o ex servidor | Acto de archivo notificado |
