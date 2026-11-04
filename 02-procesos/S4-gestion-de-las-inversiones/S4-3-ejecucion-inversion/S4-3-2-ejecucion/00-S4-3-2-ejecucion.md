---
tipo: mapa-de-contenido
area: S4-3-2-ejecucion
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
codigo_proceso: S4.3.2
nivel_proceso: 2
proceso_padre: S4.3
alcance_proyecto: EN-ALCANCE
aliases:
  - S4.3.2 Ejecucion
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2
---

# S4.3.2 Ejecucion

Sube a: [S4.3 Ejecucion de la inversion](../00-S4-3-ejecucion-inversion.md)

Modelo de trabajo actualizado por el equipo (`DEC-030` a `DEC-032`): una instancia de larga duracion permanece activa hasta la culminacion de la obra o hasta una terminacion por resolucion o nulidad. Durante esa instancia pueden activarse repetidas veces y en paralelo tres procesos de nivel 3: Control periodico de la ejecucion, Atencion de consultas de obra y Gestion de modificaciones de alcance o plazo. En el diagrama de S4.3.2 se muestran como subprocesos de evento contraidos con su disparador; su detalle se desarrolla en carpetas propias.

El modelo anterior y el respaldo integral inmediatamente previo al reemplazo se conservan en `99-temporal/modelos/comparacion-s4-3-2/`. La evaluacion BPMN, el detalle de los eventos agrupados y los pendientes estan en el [sustento](S4-3-2-sustento.md).

## Ubicacion

Mapa de procesos institucional > S4 Gestion de las inversiones > S4.3 Ejecucion de la inversion > **S4.3.2** (Nivel 2).

## Documentos del proceso

| Documento | Archivo | Estado |
|---|---|---|
| Ficha de producto y proceso | `S4-3-2-ficha-producto-proceso.md` | `PENDIENTE` |
| Diagrama del proceso | Fuente [S4-3-2-diagrama-proceso-tabla.md](S4-3-2-diagrama-proceso-tabla.md); genera [S4-3-2-diagrama-proceso.bpmn](S4-3-2-diagrama-proceso.bpmn), su [SVG](S4-3-2-diagrama-proceso.svg), su [PNG](S4-3-2-diagrama-proceso.png) y su [vista interactiva](S4-3-2-diagrama-proceso.html) | `PROPUESTA` en `ELABORACION`: tres bloques de eventos concurrentes |
| Sustento | [S4-3-2-sustento.md](S4-3-2-sustento.md) | Vigente |
| Insumo del equipo | [S4-3-2-insumo-modelo-ejecucion-equipo.png](S4-3-2-insumo-modelo-ejecucion-equipo.png) | `PROPUESTA` del equipo, evaluada en el sustento |

## Subprocesos

| Codigo | Proceso | Situacion |
|---|---|---|
| S4.3.2.1 | [Control periodico de la ejecucion](S4-3-2-1-control-periodico-ejecucion/00-S4-3-2-1-control-periodico-ejecucion.md) | Desarrollo inicial en `ELABORACION`; el flujo de valorizacion es el nucleo observado |
| S4.3.2.2 | [Atencion de consultas de obra](S4-3-2-2-atencion-consultas-obra/00-S4-3-2-2-atencion-consultas-obra.md) | Modelo detallado en `ELABORACION`: contratista, supervision, OACGD, SGGOS, SGE y proyectista; firma del Subgerente de Estudios (`DEC-033`) |
| S4.3.2.3 | [Gestion de modificaciones de alcance o plazo](S4-3-2-3-gestion-modificaciones-alcance-plazo/00-S4-3-2-3-gestion-modificaciones-alcance-plazo.md) | Modelo propuesto en `ELABORACION`: actores de obra comunes, control de alcance original, elaborador definido o designado, revision tecnica competente e independiente, controles complementarios y decision segregados (`DEC-037`, `DEC-038`); pendiente validacion operativa |

## Relaciones

- Recibe de [S4.3.1 Inicio de ejecucion](../S4-3-1-inicio-de-ejecucion/00-S4-3-1-inicio-de-ejecucion.md) el acta de inicio de obra.
- Envia a [S4.3.3 Recepcion](../S4-3-3-recepcion/00-S4-3-3-recepcion.md) la obra culminada o el contrato resuelto o nulo.
- [Estandar de artefactos, seccion 6.1](../../../../00-gobernanza/estandar-artefactos-modelamiento.md)
