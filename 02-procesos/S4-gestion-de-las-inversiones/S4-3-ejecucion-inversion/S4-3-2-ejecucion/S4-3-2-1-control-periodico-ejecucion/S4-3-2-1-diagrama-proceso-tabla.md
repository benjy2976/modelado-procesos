---
id: AP-S4-3-2-1-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.1
nivel_proceso: 3
perfil_trazado: zigzag-controlado
proceso:
  - S4.3.2.1
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-1
---

# S4.3.2.1 Control periodico de la ejecucion

Sube a: [S4.3.2.1 Control periodico de la ejecucion](00-S4-3-2-1-control-periodico-ejecucion.md)

Modelo de valorizacion actualizado con el tramite regular descrito por el usuario el 2026-11-17. La caja 7 conserva su numero y representa la revision del monitor de obras de SGGOS. La ruta institucional comienza con la recepcion por Atencion al Ciudadano y termina con el tramite a Administracion o la notificacion directa de observaciones al contratista.

Notas que no se dibujan:

- Caja 10: el monitor verifica los calculos de penalidad, amortizacion, retenciones y demas conceptos que correspondan; incorpora esa informacion y el monto propuesto para pagar en su informe y conserva la preparacion del proyecto de informe del subgerente.
- Caja 14: el subgerente revisa el informe del monitor, emite su propio informe otorgando conformidad y eleva la valorizacion a GRI; esa conformidad sustenta el tramite de pago de la caja 15.
- La instancia propuesta es una por periodo de control o valorizacion dentro de una ejecucion activa.
- El cierre mensual es normativo para valorizaciones; otros controles periodicos no se agregan sin evidencia.
- La Gerencia Regional de Infraestructura tramita la valorizacion hacia Administracion para pago; el proceso interno de pago y sus actos posteriores no se detallan aqui.
- El participante ejecutor contiene al residente; la intervencion formal del contratista o su representante se agrega solo cuando una actividad la exige.
- Supervisor o inspector de obra expresa una responsabilidad funcional alternativa: la ejerce el supervisor contratado o el inspector de la entidad, segun la modalidad y la asignacion aplicable.
- Atencion al Ciudadano se identifica por la funcion descrita por el usuario; su adscripcion a una unidad especifica no esta acreditada.

## Pools

| Pool | Carriles |
|---|---|
| S4.3.2.1 Control periodico de la ejecucion | Ejecutor de obra, segun regimen — Residente de obra; Supervisor o inspector de obra, segun modalidad; Atencion al Ciudadano — Recepcion documentaria; SGGOS — Subgerente de Gestion de Obras y Supervision; SGGOS — Monitor de obras; GRI — Tramite de valorizacion |

## Elementos

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Grupo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E-1 | 1 | S4.3.2.1 Control periodico de la ejecucion | Ejecutor de obra, segun regimen — Residente de obra | inicio-temporizador | Cierre del periodo de valorizacion | T-1 |  |  |  | Cierre de cada mes |  | Una instancia por periodo |  | NORM | Reglamento de la Ley 32069, art. 210.1; Directiva 017-2023-CG, num. 7.3.4 |
| T-1 | 2 | S4.3.2.1 Control periodico de la ejecucion | Ejecutor de obra, segun regimen — Residente de obra | tarea | Elaborar y presentar la valorizacion | T-2 |  |  | entra: Sustento de mayores metrados del periodo, si los hay; sale: Informe de valorizacion |  |  |  |  | OBS | ejecucion-bizagi.bpmn, tareas de elaboracion y remision de valorizacion; Reglamento de la Ley 32069, arts. 197.2 y 210.1 |
| T-2 | 3 | S4.3.2.1 Control periodico de la ejecucion | Supervisor o inspector de obra, segun modalidad | tarea | Revisar la valorizacion | G-1 |  |  | entra: Informe de valorizacion |  |  |  |  | OBS | ejecucion-bizagi.bpmn, revisar y aprobar la valorizacion |
| G-1 | 4 | S4.3.2.1 Control periodico de la ejecucion | Supervisor o inspector de obra, segun modalidad | compuerta | ¿La valorizacion cumple las condiciones tecnicas? | T-8 [Si]; T-4 [No] |  |  |  |  |  |  |  | PROP | Reconstruccion del flujo observado; pendiente validar criterios |
| T-4 | 5 | S4.3.2.1 Control periodico de la ejecucion | Supervisor o inspector de obra, segun modalidad | tarea | Comunicar observaciones del control de obra | T-5 |  |  | sale: Observaciones |  |  |  |  | OBS | ejecucion-bizagi.bpmn, informe de observaciones |
| T-5 | 6 | S4.3.2.1 Control periodico de la ejecucion | Ejecutor de obra, segun regimen — Residente de obra | tarea | Subsanar la valorizacion | T-2 |  |  | entra: Observaciones; sale: Valorizacion subsanada |  |  |  |  | PROP | Inferencia necesaria para cerrar el ciclo de observaciones observado |
| T-3 | 7 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Monitor de obras | tarea | Revisar la valorizacion | G-2 |  |  | entra: Valorizacion derivada por el subgerente |  |  |  |  | EQ | Descripcion del tramite regular por el usuario, 2026-11-17; caja 7 |
| G-2 | 8 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Monitor de obras | compuerta | ¿La valorizacion cumple? | T-7 [Si]; T-6 [No] |  |  |  |  |  |  |  | EQ | Descripcion del tramite regular por el usuario, 2026-11-17 |
| T-6 | 9 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Monitor de obras | tarea | Elaborar informe de observaciones y proyectar carta del subgerente | T-12 |  |  |  |  |  |  |  | EQ | Descripcion del tramite regular por el usuario, 2026-11-17 |
| T-7 | 10 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Monitor de obras | tarea | Verificar calculos e informar monto propuesto para pago | T-10 |  |  |  |  |  | Si las observaciones no se subsanan o no se responden en plazo, el monto propuesto es el no cuestionado |  | EQ | Descripcion del tramite regular por el usuario, 2026-11-17; Reglamento de la Ley 32069, arts. 210.3 y 210.4 |
| F-1 | 11 | S4.3.2.1 Control periodico de la ejecucion | GRI — Tramite de valorizacion | fin-mensaje | Valorizacion remitida a Administracion para pago |  |  |  |  |  |  |  |  | EQ | Descripcion del tramite regular por el usuario, 2026-11-17 |
| T-8 | 12 | S4.3.2.1 Control periodico de la ejecucion | Atencion al Ciudadano — Recepcion documentaria | tarea | Recepcionar valorizacion y derivar a SGGOS | T-9 |  |  | entra: Valorizacion revisada; sale: Valorizacion derivada |  |  |  |  | EQ | Descripcion del tramite regular por el usuario, 2026-11-17 |
| T-9 | 13 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea | Recepcionar valorizacion y derivar al monitor de obras | T-3 |  |  | entra: Valorizacion derivada por Atencion al Ciudadano |  |  |  |  | EQ | Descripcion del tramite regular por el usuario, 2026-11-17 |
| T-10 | 14 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea | Revisar y emitir informe propio de conformidad para tramite de pago | T-11 |  |  |  |  |  |  |  | EQ | Precision del usuario, 2026-11-17; caja 14 |
| T-11 | 15 | S4.3.2.1 Control periodico de la ejecucion | GRI — Tramite de valorizacion | tarea | Tramitar valorizacion para pago ante Administracion | F-1 |  |  | entra: Informe del subgerente; sale: Valorizacion para pago |  |  |  |  | EQ | Descripcion del tramite regular por el usuario, 2026-11-17 |
| T-12 | 16 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea | Emitir carta y notificar observaciones con plazo de subsanacion | GE-1 |  |  |  |  |  | Se comunican tambien al supervisor |  | EQ | Descripcion del tramite regular por el usuario, 2026-11-17; Reglamento de la Ley 32069, art. 210.3 |
| GE-1 | 18 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Subgerente de Gestion de Obras y Supervision | compuerta-eventos | ¿Que ocurre primero? | M-1; R-1 |  |  |  |  |  |  |  | NORM | Reglamento de la Ley 32069, arts. 210.3 y 210.4 |
| M-1 | 19 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Subgerente de Gestion de Obras y Supervision | mensaje-recepcion | Subsanacion recibida | T-13 |  |  | entra: Subsanacion de observaciones |  |  |  |  | NORM | Reglamento de la Ley 32069, art. 210.3 |
| T-13 | 20 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Monitor de obras | tarea | Revisar la subsanacion | T-7 |  |  |  | 2 dias habiles desde el dia siguiente de recibida |  |  |  | NORM | Reglamento de la Ley 32069, art. 210.3; revision por el monitor inferida de T-3 |
| R-1 | 21 | S4.3.2.1 Control periodico de la ejecucion | SGGOS — Subgerente de Gestion de Obras y Supervision | temporizador | Vencio el plazo de subsanacion | T-7 |  |  |  | Plazo otorgado en la carta |  |  |  | NORM | Reglamento de la Ley 32069, art. 210.4 |

## Mensajes

| Desde | Hacia | Nombre | Clase |
|---|---|---|---|
| F-1 | Administracion | Valorizacion para tramite de pago | EQ |
| S4.3.2.8 Gestion de mayores metrados | T-1 | Sustento de mayores metrados del periodo | PROP |
| T-12 | Contratista | Carta de observaciones con plazo de subsanacion | EQ |
| Contratista | M-1 | Subsanacion de observaciones | NORM |

