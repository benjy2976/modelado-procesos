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

Subproceso de nivel 2 propuesto en `DEC-023`: una instancia por contrato o frente de ejecucion. Inicia cuando S4.3.1 entrega las condiciones de inicio y termina con la obra culminada o con el contrato resuelto o declarado nulo. Los sucesos que ocurren en cualquier momento de la ejecucion (valorizaciones, consultas, adicionales, ampliaciones, suspensiones, paralizaciones) se modelan como subprocesos de evento sin interrupcion (`DEC-024`). En este nivel aparecen contraidos [+]; cada uno se detallara en su propio diagrama de nivel 3, con los codigos propuestos en el sustento.

## Ubicacion

Mapa de procesos institucional > S4 Gestion de las inversiones > S4.3 Ejecucion de la inversion > **S4.3.2** (Nivel 2).

## Documentos del proceso

| Documento | Archivo | Estado |
|---|---|---|
| Ficha de producto y proceso | `S4-3-2-ficha-producto-proceso.md` | `PENDIENTE` |
| Diagrama del proceso | [S4-3-2-diagrama-proceso-logico.puml](S4-3-2-diagrama-proceso-logico.puml) y su [SVG](S4-3-2-diagrama-proceso-logico.svg); luego `S4-3-2-diagrama-proceso.bpmn` | `PROPUESTA` en `ELABORACION`: modelo logico |
| Sustento | [S4-3-2-sustento.md](S4-3-2-sustento.md) | Vigente |
| Insumo del equipo | [S4-3-2-insumo-modelo-ejecucion-equipo.png](S4-3-2-insumo-modelo-ejecucion-equipo.png) | `PROPUESTA` del equipo, evaluada en el sustento |

## Relaciones

- Recibe de [S4.3.1 Gestion de la ejecucion](../S4-3-1-gestion-de-la-ejecucion/00-S4-3-1-gestion-de-la-ejecucion.md) las condiciones de inicio, y le envia valorizaciones, requerimientos y modificaciones.
- Envia a [S4.3.3 Recepcion](../S4-3-3-recepcion/00-S4-3-3-recepcion.md) la obra culminada o el contrato resuelto o nulo.
- [Estandar de artefactos, seccion 6.1](../../../../00-gobernanza/estandar-artefactos-modelamiento.md)
