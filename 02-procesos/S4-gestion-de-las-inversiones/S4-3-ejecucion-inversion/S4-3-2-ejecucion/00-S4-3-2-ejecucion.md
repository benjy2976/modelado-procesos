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

Modelo de trabajo actualizado mediante `DEC-041`: una instancia de larga duracion permanece activa hasta la culminacion de la obra o una terminacion por resolucion o nulidad. Mientras esta activa pueden iniciarse repetidas veces y en paralelo seis procesos de nivel 3, todos como subprocesos de evento no interruptivos. La actividad principal "Ejecutar la obra conforme al expediente tecnico" permanece sin codigo de proceso independiente y no se usa un bucle para mantener viva la ejecucion.

Los seis hijos permanecen en el mismo nivel. En la vista padre se agrupan para lectura como Control periodico, Atencion de incidencias, Modificaciones de alcance y Modificaciones de plazo. Los antecedentes se conservan en Git y en el respaldo existente de `99-temporal/modelos/comparacion-s4-3-2/`; no se crean copias adicionales.

## Ubicacion

Mapa de procesos institucional > S4 Gestion de las inversiones > S4.3 Ejecucion de la inversion > **S4.3.2** (Nivel 2).

## Documentos del proceso

| Documento | Archivo | Estado |
|---|---|---|
| Ficha de producto y proceso | `S4-3-2-ficha-producto-proceso.md` | `PENDIENTE` |
| Diagrama del proceso | Fuente [S4-3-2-diagrama-proceso-tabla.md](S4-3-2-diagrama-proceso-tabla.md); genera [S4-3-2-diagrama-proceso.bpmn](S4-3-2-diagrama-proceso.bpmn), su [SVG](S4-3-2-diagrama-proceso.svg), su [PNG](S4-3-2-diagrama-proceso.png) y su [vista interactiva](S4-3-2-diagrama-proceso.html) | `PROPUESTA` en `ELABORACION`: seis subprocesos de evento concurrentes |
| Sustento | [S4-3-2-sustento.md](S4-3-2-sustento.md) | Vigente |
| Insumo del equipo | [S4-3-2-insumo-modelo-ejecucion-equipo.png](S4-3-2-insumo-modelo-ejecucion-equipo.png) | `PROPUESTA` del equipo, evaluada en el sustento |

## Subprocesos

| Codigo | Proceso | Situacion |
|---|---|---|
| S4.3.2.1 | [Control periodico de la ejecucion](S4-3-2-1-control-periodico-ejecucion/00-S4-3-2-1-control-periodico-ejecucion.md) | Desarrollo inicial en `ELABORACION`; el flujo de valorizacion es el nucleo observado |
| S4.3.2.2 | [Atencion de consultas de obra](S4-3-2-2-atencion-consultas-obra/00-S4-3-2-2-atencion-consultas-obra.md) | Modelo detallado en `ELABORACION`; puede originar casos de S4.3.2.3 a S4.3.2.6 |
| S4.3.2.3 | [Gestion de modificaciones de alcance](S4-3-2-3-gestion-modificaciones-alcance/00-S4-3-2-3-gestion-modificaciones-alcance.md) | Realineado a adicional, reduccion o deductivo y mayores cantidades como variantes internas sin nivel 4 |
| S4.3.2.4 | [Gestion de ampliaciones de plazo](S4-3-2-4-gestion-ampliaciones-plazo/00-S4-3-2-4-gestion-ampliaciones-plazo.md) | Juego inicial en `ELABORACION`; una instancia por solicitud o causal |
| S4.3.2.5 | [Formalizacion de suspensiones de plazo](S4-3-2-5-formalizacion-suspensiones-plazo/00-S4-3-2-5-formalizacion-suspensiones-plazo.md) | Juego inicial en `ELABORACION`; suspension contractual y posterior reanudacion separadas por instancia |
| S4.3.2.6 | [Gestion de paralizacion y reinicio](S4-3-2-6-gestion-paralizacion-reinicio/00-S4-3-2-6-gestion-paralizacion-reinicio.md) | Juego inicial en `ELABORACION`; paralizacion y reinicio separados por instancia |

## Relaciones

- Recibe de [S4.3.1 Inicio de ejecucion](../S4-3-1-inicio-de-ejecucion/00-S4-3-1-inicio-de-ejecucion.md) el acta de inicio de obra.
- Envia a [S4.3.3 Recepcion](../S4-3-3-recepcion/00-S4-3-3-recepcion.md) la obra culminada o el contrato resuelto o nulo.
- [Estandar de artefactos, seccion 6.1](../../../../00-gobernanza/estandar-artefactos-modelamiento.md)
- [Convencion de carriles y SGD para S4.3.2, seccion 7.4](../../../../00-gobernanza/estandar-artefactos-modelamiento.md#74-convencion-de-carriles-y-sgd-en-s432)

## Criterio de trazado ? 2026-11-06

Por indicacion del usuario, los seis subprocesos usan `perfil_trazado: zigzag-controlado`; los futuros trabajos dentro de esta carpeta mantendran ese perfil. El diagrama padre S4.3.2 no se redibuja en este lote; el perfil se aplicara cuando se retome su trazado. Los resultados de generacion y pendientes geometricos se registran en el sustento de cada subproceso.
