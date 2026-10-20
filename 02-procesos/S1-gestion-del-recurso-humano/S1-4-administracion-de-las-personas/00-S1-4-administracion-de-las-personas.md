---
tipo: mapa-de-contenido
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S1.4
nivel_proceso: 1
proceso_padre: S1
alcance_proyecto: REFERENCIA
aliases:
  - S1.4 Administracion de las personas
tags:
  - tema/procesos
  - proceso/s1/s1-4
---

# S1.4 Administracion de las personas

Sube a: [S1 Gestion del recurso humano](../00-S1-gestion-del-recurso-humano.md)

La ficha institucional de S1 ubica en **S1.4** el producto «Informes y resoluciones de procedimientos disciplinarios». Por ello, S1.4 es el **proceso padre identificado** para el modelamiento del PAD. La intervencion de otros organos y participantes son interfaces del caso; no hay evidencia de que el PAD sea un proceso transversal con varios padres de Nivel 1.

## Identificacion y limite

| Clase | Dato | Fuente |
|---|---|---|
| Evidencia observada | S1.4 se denomina «Administracion de las personas» en el inventario Nivel 1. | [Mapa institucional aprobado, paginas PDF 21 y 25](../../mapa-de-procesos-institucional/mapa-procesos-nivel-1-s1.md) |
| Evidencia observada | La ficha de S1 incluye en la fila S1.4 los «Informes y resoluciones de procedimientos disciplinarios» y los receptores «PAD / SERVIR / CONTRALORIA». | [Mapa institucional aprobado, paginas PDF 110-111](../../../01-referencias/01-institucionales-grh/originales/mapa-procesos-grh-oficial.pdf) |
| Evidencia observada del borrador | El numeral 5.4.1 denomina «Gestion del Regimen Disciplinario y Procedimiento Administrativo Sancionador» a un subproceso. | [Revision del proyecto de directiva PAD](../../../90-bandeja-entrada/revision-proyecto-directiva-pad.md), PDF recibido, pagina 9 |
| Inferencia de arquitectura | El PAD candidato se descompone bajo S1.4, no bajo S1.8 ni como rama independiente de Nivel 0. | Contraste de las fuentes anteriores |
| EVIDENCIA-INSUFICIENTE | Codigo, nombre institucional, dueno y descomposicion aprobada del eventual hijo PAD; delimitacion de sus interfaces con archivo, registro, control y recursos. | Fuentes revisadas hasta 2026-10-20 |

## Modelos asociados

- [Paquete PAD en trabajo](modelos-pad/00-modelos-pad.md): cinco BPMN, cinco fichas candidatas del Anexo 2, inventario, indicadores y evaluacion de procedimientos. Sus identificadores `pad-trabajo-*` **no son codigos NT** ni convierten los modelos en el diagrama aprobado de S1.4.
- [Propuesta inicial de modelamiento](../../../90-bandeja-entrada/propuesta-modelamiento-pad.md): campos candidatos, vacios y decisiones pendientes.

El paquete se mantiene como **trabajo asociado a S1.4**. Cuando se documente el codigo y limite del hijo PAD, sus artefactos se ajustaran a ese proceso dentro de esta rama. No se atribuye al proceso S1.4 completo el flujo particular de un caso PAD.
