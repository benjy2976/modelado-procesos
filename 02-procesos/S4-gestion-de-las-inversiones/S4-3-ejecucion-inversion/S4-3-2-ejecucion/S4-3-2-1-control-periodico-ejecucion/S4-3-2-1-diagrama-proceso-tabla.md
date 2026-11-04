---
id: AP-S4-3-2-1-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.1
nivel_proceso: 3
proceso:
  - S4.3.2.1
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-03
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-1
---

# S4.3.2.1 Control periodico de la ejecucion

Sube a: [S4.3.2.1 Control periodico de la ejecucion](00-S4-3-2-1-control-periodico-ejecucion.md)

Modelo inicial reconstruido a partir del circuito de valorizacion del BPMN exportado de Bizagi. No se copian sus conexiones defectuosas: cada actividad se reubica en un flujo verificable y conserva su clase y fuente en el sustento.

Notas que no se dibujan:

- La instancia propuesta es una por periodo de control o valorizacion dentro de una ejecucion activa.
- El cierre mensual es normativo para valorizaciones; otros controles periodicos no se agregan sin evidencia.
- El destino institucional del expediente para pago esta pendiente de determinar.
- Contratista y residente son alternativas segun modalidad; supervisor e inspector tambien lo son.

## Pools

| Pool | Carriles |
|---|---|
| S4.3.2.1 Control periodico de la ejecucion | Contratista o residente; Supervisor o inspector; Entidad |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Grupo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E-1 | S4.3.2.1 Control periodico de la ejecucion | Contratista o residente | inicio-temporizador | Cierre del periodo de valorizacion | T-1 |  |  |  | Cierre de cada mes |  | Una instancia por periodo |  | NORM | Reglamento de la Ley 32069, art. 210.1; Directiva 017-2023-CG, num. 7.3.4 |
| T-1 | S4.3.2.1 Control periodico de la ejecucion | Contratista o residente | tarea | Elaborar y presentar la valorizacion | T-2 |  |  | sale: Informe de valorizacion |  |  |  |  | OBS | ejecucion-bizagi.bpmn, tareas de elaboracion y remision de valorizacion |
| T-2 | S4.3.2.1 Control periodico de la ejecucion | Supervisor o inspector | tarea | Revisar la valorizacion | G-1 |  |  | entra: Informe de valorizacion |  |  |  |  | OBS | ejecucion-bizagi.bpmn, revisar y aprobar la valorizacion |
| G-1 | S4.3.2.1 Control periodico de la ejecucion | Supervisor o inspector | compuerta | ¿La valorizacion cumple las condiciones tecnicas? | T-3 [Si]; T-4 [No] |  |  |  |  |  |  |  | PROP | Reconstruccion del flujo observado; pendiente validar criterios |
| T-4 | S4.3.2.1 Control periodico de la ejecucion | Supervisor o inspector | tarea | Comunicar observaciones de la supervision | T-5 |  |  | sale: Observaciones |  |  |  |  | OBS | ejecucion-bizagi.bpmn, informe de observaciones |
| T-5 | S4.3.2.1 Control periodico de la ejecucion | Contratista o residente | tarea | Subsanar la valorizacion | T-2 |  |  | entra: Observaciones; sale: Valorizacion subsanada |  |  |  |  | PROP | Inferencia necesaria para cerrar el ciclo de observaciones observado |
| T-3 | S4.3.2.1 Control periodico de la ejecucion | Entidad | tarea | Recibir y revisar la valorizacion | G-2 |  |  | entra: Valorizacion revisada |  |  |  |  | OBS | ejecucion-bizagi.bpmn, recibir y revisar la valorizacion |
| G-2 | S4.3.2.1 Control periodico de la ejecucion | Entidad | compuerta | ¿Existen observaciones de la entidad? | T-6 [Si]; T-7 [No] |  |  |  |  |  |  |  | OBS | ejecucion-bizagi.bpmn, compuerta de observaciones |
| T-6 | S4.3.2.1 Control periodico de la ejecucion | Entidad | tarea | Comunicar observaciones de la entidad | T-5 |  |  | sale: Informe de observaciones |  |  |  |  | OBS | ejecucion-bizagi.bpmn, derivar informe de observaciones |
| T-7 | S4.3.2.1 Control periodico de la ejecucion | Entidad | tarea | Elaborar informe para tramite de pago | F-1 |  |  | sale: Expediente de valorizacion aprobado |  |  |  |  | OBS | ejecucion-bizagi.bpmn, realizar y derivar informe de pago |
| F-1 | S4.3.2.1 Control periodico de la ejecucion | Entidad | fin-mensaje | Expediente de valorizacion aprobado para tramite de pago |  |  |  |  |  |  |  |  | PROP | Producto propuesto; receptor pendiente de confirmar |

