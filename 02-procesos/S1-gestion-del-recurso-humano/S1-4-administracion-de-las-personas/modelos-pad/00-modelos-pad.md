---
tipo: mapa-de-contenido
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
tags:
  - tema/procesos
  - proceso/s1/s1-4
---

# Modelos BPMN de trabajo para el PAD

Sube a: [S1.4 Administracion de las personas](../00-S1-4-administracion-de-las-personas.md)

Estos cinco modelos son **propuestas de lectura del borrador de directiva**, no AS-IS observado, reglas validadas ni diagramas institucionales aprobados. Se agrupan bajo `S1.4`, el proceso padre identificado por el producto disciplinario de la ficha S1. El hijo PAD carece de codigo NT. `pad-trabajo-*` identifica archivos de trabajo y **no es un codigo de proceso**. Cuando se defina la jerarquia, las tablas se trasladaran a la carpeta del hijo con los nombres NT; los BPMN y vistas se regeneraran.

## Diagramas de proceso, Anexo 3, en trabajo

| Modelo de trabajo | Fuente BPMN | Diagrama | Vista |
|---|---|---|---|
| Gestion del caso disciplinario | [Tabla](pad-trabajo-caso-diagrama-proceso-tabla.md) | [BPMN](pad-trabajo-caso-diagrama-proceso.bpmn) | [SVG](pad-trabajo-caso-diagrama-proceso.svg) · [HTML](pad-trabajo-caso-diagrama-proceso.html) |
| Investigacion preliminar y precalificacion | [Tabla](pad-trabajo-precalificacion-diagrama-proceso-tabla.md) | [BPMN](pad-trabajo-precalificacion-diagrama-proceso.bpmn) | [SVG](pad-trabajo-precalificacion-diagrama-proceso.svg) · [HTML](pad-trabajo-precalificacion-diagrama-proceso.html) |
| Fase instructiva | [Tabla](pad-trabajo-instruccion-diagrama-proceso-tabla.md) | [BPMN](pad-trabajo-instruccion-diagrama-proceso.bpmn) | [SVG](pad-trabajo-instruccion-diagrama-proceso.svg) · [HTML](pad-trabajo-instruccion-diagrama-proceso.html) |
| Fase sancionadora | [Tabla](pad-trabajo-decision-diagrama-proceso-tabla.md) | [BPMN](pad-trabajo-decision-diagrama-proceso.bpmn) | [SVG](pad-trabajo-decision-diagrama-proceso.svg) · [HTML](pad-trabajo-decision-diagrama-proceso.html) |
| Derivacion de recursos | [Tabla](pad-trabajo-recursos-diagrama-proceso-tabla.md) | [BPMN](pad-trabajo-recursos-diagrama-proceso.bpmn) | [SVG](pad-trabajo-recursos-diagrama-proceso.svg) · [HTML](pad-trabajo-recursos-diagrama-proceso.html) |

## Fichas y formatos NT en elaboracion

| Unidad modelada | Ficha de producto y proceso, Anexo 2 |
|---|---|
| Caso PAD | [Ficha candidata](pad-trabajo-caso-ficha-producto-proceso.md) |
| Investigacion preliminar y precalificacion | [Ficha candidata](pad-trabajo-precalificacion-ficha-producto-proceso.md) |
| Fase instructiva | [Ficha candidata](pad-trabajo-instruccion-ficha-producto-proceso.md) |
| Fase sancionadora | [Ficha candidata](pad-trabajo-decision-ficha-producto-proceso.md) |
| Derivacion de recursos | [Ficha candidata](pad-trabajo-recursos-ficha-producto-proceso.md) |

- [Inventario candidato de productos y procesos, Anexo 1](pad-trabajo-inventario-productos-procesos.md).
- [Fichas de indicador candidatas, Anexo 4](pad-trabajo-fichas-indicador.md).
- [Sustento de campos, fuentes y discrepancias](pad-trabajo-sustento.md).
- [Aplicabilidad de procedimientos, Anexos 7 y 8](pad-trabajo-aplicabilidad-procedimientos.md): decision pendiente de ultimo nivel y criterio; no se emite aun un procedimiento NT.

Estas cinco fichas permiten revisar el contenido de cada diagrama **sin afirmar que existan cinco procesos institucionales**. Codigo, nivel, dueno, indicadores y productos NT se confirmaran al decidir la descomposicion de S1.4.

## Limites de uso

- Las secuencias y compuertas son propuestas de modelamiento. La columna `Fuente` de cada tabla apunta al numeral y pagina PDF del borrador.
- No se dibujan plazos como temporizadores, porque su aplicabilidad y vigencia no han sido validadas con fuentes oficiales.
- La segunda instancia se representa solo hasta la derivacion del recurso; el borrador no permite modelar las actuaciones internas de la autoridad que resuelve.
- Medidas cautelares, prescripcion, notificacion especial y custodia requieren modelos de detalle cuando el equipo confirme sus limites y reglas.
- La [revision documental](../../../../90-bandeja-entrada/revision-proyecto-directiva-pad.md) registra discrepancias que impiden adoptar estos diagramas como linea base.

## Construccion y verificacion

Las tablas se construyen con `construir_modelos.py --tabla <ruta>`; la comprobacion usa el mismo comando con `--check`, ademas del control global `--check`. Los cinco modelos pasaron D1 a D5 sin hallazgos y su comprobacion individual `--check`. El control global tambien paso; las vistas HTML preexistentes usan CRLF en Windows, ahora admitido por el comparador sin cambiar su contenido.

## Relaciones

- Se sustenta en: [Revision del borrador](../../../../90-bandeja-entrada/revision-proyecto-directiva-pad.md).
- Implementa: [Propuesta de modelamiento](../../../../90-bandeja-entrada/propuesta-modelamiento-pad.md).
- Se rige por: [Estandar de artefactos](../../../../00-gobernanza/estandar-artefactos-modelamiento.md).
