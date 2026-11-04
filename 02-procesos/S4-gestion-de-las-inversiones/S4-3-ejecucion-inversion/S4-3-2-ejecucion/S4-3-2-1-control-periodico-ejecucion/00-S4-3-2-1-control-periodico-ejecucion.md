---
tipo: mapa-de-contenido
area: S4-3-2-1-control-periodico-ejecucion
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
codigo_proceso: S4.3.2.1
nivel_proceso: 3
proceso_padre: S4.3.2
alcance_proyecto: EN-ALCANCE
aliases:
  - S4.3.2.1 Control periodico de la ejecucion
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-1
---

# S4.3.2.1 Control periodico de la ejecucion

Sube a: [S4.3.2 Ejecucion](../00-S4-3-2-ejecucion.md)

Proceso de nivel 3 adoptado mediante `DEC-032`. Su desarrollo inicial toma del modelo Bizagi de Ejecucion el circuito de valorizacion periodica. La expresion "Control periodico" conserva un alcance mayor, pero no se incorporan otros controles hasta contar con evidencia operativa.

## Ubicacion

Mapa de procesos institucional > S4 Gestion de las inversiones > S4.3 Ejecucion de la inversion > S4.3.2 Ejecucion > **S4.3.2.1 Control periodico de la ejecucion** (Nivel 3).

## Que hace

Verifica periodicamente la informacion de avance, atiende observaciones y produce un expediente de valorizacion aprobado para el tramite que corresponda. Objetivo y alcance pendientes de validacion del dueno del proceso.

## Interacciones

| Sentido | Contraparte | Elemento observado |
|---|---|---|
| Recibe | S4.3.2 Ejecucion | Cierre del periodo y avance ejecutado |
| Envia | Proceso de pago por determinar | Expediente de valorizacion aprobado para tramite de pago |
| Envia | S4.3.3 Recepcion | La ultima valorizacion es una señal observada en Bizagi; su relacion formal con la recepcion esta pendiente de definir |

## Documentos del proceso

| Documento | Archivo | Estado |
|---|---|---|
| Ficha de producto y proceso | [S4-3-2-1-ficha-producto-proceso.md](S4-3-2-1-ficha-producto-proceso.md) | `PROPUESTA` en `ELABORACION` |
| Fichas de indicador | [S4-3-2-1-fichas-indicador.md](S4-3-2-1-fichas-indicador.md) | `EVIDENCIA-INSUFICIENTE` |
| Diagrama del proceso | Fuente [S4-3-2-1-diagrama-proceso-tabla.md](S4-3-2-1-diagrama-proceso-tabla.md); genera BPMN, SVG, PNG y HTML | `PROPUESTA` en `ELABORACION` |
| Sustento | [S4-3-2-1-sustento.md](S4-3-2-1-sustento.md) | Vigente para trazabilidad |
| Procedimiento | No creado | Pendiente determinar si cumple los criterios del numeral 6.1.3 d de la NT |

## Subprocesos

No se han adoptado procesos de nivel 4. La valorizacion es el nucleo operativo inicial del proceso, no un proceso codificado por separado.

## Pendientes

- Confirmar que controles distintos de la valorizacion integran este proceso.
- Confirmar el dueno y las unidades responsables.
- Identificar el proceso receptor del expediente aprobado para pago.
- Definir la relacion entre la ultima valorizacion, la culminacion de obra y S4.3.3 Recepcion.

## Relaciones

- [Sustento de S4.3.2](../S4-3-2-sustento.md)
- [Modelo Bizagi de Ejecucion](../../../../../99-temporal/modelos/sggos-2026-11-02-bpmn/ejecucion-bizagi.bpmn)

