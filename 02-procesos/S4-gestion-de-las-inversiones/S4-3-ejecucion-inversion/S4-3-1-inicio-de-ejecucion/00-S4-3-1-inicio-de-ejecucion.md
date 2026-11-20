---
tipo: mapa-de-contenido
area: S4-3-1-inicio-de-ejecucion
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
codigo_proceso: S4.3.1
nivel_proceso: 2
proceso_padre: S4.3
alcance_proyecto: EN-ALCANCE
aliases:
  - S4.3.1 Inicio de ejecucion
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-1
---

# S4.3.1 Inicio de ejecucion

Sube a: [S4.3 Ejecucion de la inversion](../00-S4-3-ejecucion-inversion.md)

Se incorporo una copia exacta del BPMN exportado de Bizagi como insumo observado. Su alcance declarado es **inicio de ejecucion contractual, solo construccion**. El primer modelo logico representa la ruta principal de la sede del Gobierno Regional Huanuco: contrato suscrito, tramite y notificacion a GRI/SGGOS, designacion del coordinador y verificacion de condiciones de inicio conforme a los articulos 176 y 186 del Reglamento de la Ley 32069. Es una propuesta en elaboracion, sin validacion normativa humana ni conformidad institucional. Las variantes de otras oficinas o unidades ejecutoras, las modalidades fuera de solo construccion y la ficha de producto y proceso quedan pendientes.

La propuesta anterior denominada "S4.3.1 Gestion de la ejecucion" fue retirada de la ruta activa el 2026-11-02. Se conserva en el historial de Git y, para la comparacion de trabajo, en `99-temporal/modelos/comparacion-s4-3-1/gestion-de-la-ejecucion-anterior/` (`DEC-029`).

## Documentos e insumos

| Documento | Archivo | Estado |
|---|---|---|
| Modelo Bizagi recibido | [S4-3-1-insumo-modelo-bizagi.bpmn](S4-3-1-insumo-modelo-bizagi.bpmn) | Copia fiel; evidencia observada, sin validacion del flujo |
| Sustento del proceso | [S4-3-1-sustento.md](S4-3-1-sustento.md) | Contraste normativo inicial, discrepancias y vacios de evidencia |
| Tabla editable del modelo logico | [S4-3-1-diagrama-proceso-tabla.md](S4-3-1-diagrama-proceso-tabla.md) | `BORRADOR`, solo construccion |
| BPMN generado | [S4-3-1-diagrama-proceso.bpmn](S4-3-1-diagrama-proceso.bpmn) | Derivado de la tabla, no linea base |
| Vista SVG | [S4-3-1-diagrama-proceso.svg](S4-3-1-diagrama-proceso.svg) | Derivado generado |
| Vista PNG | [S4-3-1-diagrama-proceso.png](S4-3-1-diagrama-proceso.png) | Derivado generado |
| Vista interactiva HTML | [S4-3-1-diagrama-proceso.html](S4-3-1-diagrama-proceso.html) | Derivado generado |
| Ficha de producto y proceso | - | `PENDIENTE` |
| Fichas de indicador | - | `PENDIENTE` |

## Pendientes

- Cotejar con un expediente y registros del SGD la ruta GRA-OACGD-GRI-SGGOS, el acto de designacion del coordinador, las bases y el contrato concreto.
- Identificar las variantes de otras oficinas o unidades ejecutoras competentes, sin asumir la ruta de la sede central.
- Distinguir este supuesto de solo construccion de otras modalidades que corresponda cubrir en S4.3.1.
- Mantener el BPMN Bizagi como insumo intacto; el modelo logico nuevo reemplaza sus rutas tecnicamente problematicas sin afirmar validacion de aquel archivo. Ver el [sustento](S4-3-1-sustento.md).

