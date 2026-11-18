---
tipo: mapa-de-contenido
area: S4-3-2-2-atencion-consultas-obra
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
codigo_proceso: S4.3.2.2
nivel_proceso: 3
proceso_padre: S4.3.2
alcance_proyecto: EN-ALCANCE
aliases:
  - S4.3.2.2 Atencion de consultas de obra
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-2
---

# S4.3.2.2 Atencion de consultas de obra

Sube a: [S4.3.2 Ejecucion](../00-S4-3-2-ejecucion.md)

Proceso de nivel 3 adoptado mediante `DEC-032`. Su modelo inicial separa la atencion y absolucion de una consulta de los tramites de modificacion que esta pueda originar.

## Ubicacion

Mapa de procesos institucional > S4 Gestion de las inversiones > S4.3 Ejecucion de la inversion > S4.3.2 Ejecucion > **S4.3.2.2 Atencion de consultas de obra** (Nivel 3).

## Que hace

Atiende una consulta originada por el contratista o, excepcionalmente, por la supervision. Cuando la materia lo requiere, el especialista de la supervision se pronuncia y el supervisor hace suyo ese pronunciamiento antes de absolver o elevar la consulta; ambas decisiones se anotan en el Cuaderno de Incidencias. En la entidad, el subgerente de SGGOS tramita la consulta a SGE con intervencion del monitor de obras. Los especialistas de SGE elaboran el informe tecnico y el Subgerente de Estudios firma la respuesta. Despues de la caja 39, SGE la comunica a SGGOS para que el monitor prepare la carta al contratista; si corresponde un adicional, indica a quien corresponde elaborarlo segun las bases de contratacion. La causal puede dar lugar a S4.3.2.3, .4, .5 o .6, segun corresponda.

El supervisor solo absuelve directamente si la consulta no modifica el expediente tecnico. Si lo modifica, la consulta del contratista debe acompanarse de su informe tecnico; sin este, no se atiende. La elevacion requiere ademas el informe tecnico de supervision, emitido por el supervisor con su evaluacion y opinion sobre la viabilidad de la consulta, conforme a la precision operativa del usuario. Vease la [trazabilidad del articulo 190](S4-3-2-2-sustento.md).

## Interacciones

| Sentido | Contraparte | Elemento observado |
|---|---|---|
| Recibe | Contratista, mediante el residente | Consulta registrada en el Cuaderno de Incidencias |
| Recibe | Supervisor de obra | Consulta originada por la supervision o consulta del contratista elevada con informe tecnico de supervision |
| Canaliza | SGGOS, mediante el subgerente y el monitor de obras | Consulta y antecedentes para su atencion tecnica |
| Elabora | Especialistas de la SGE | Informe tecnico de absolucion y proyecto de respuesta |
| Firma | Subgerente de Estudios | Respuesta institucional a la consulta |
| Solicita | Proyectista, cuando corresponda | Opinion tecnica sobre el expediente tecnico |
| Envia | Contratista | Absolucion anotada por el supervisor o carta de SGGOS con respuesta institucional |
| Envia | S4.3.2.3 a S4.3.2.6 | Respuesta que origina una solicitud o causal de alcance, ampliacion, suspension o paralizacion/reinicio |

## Documentos del proceso

| Documento | Archivo | Estado |
|---|---|---|
| Ficha de producto y proceso | [S4-3-2-2-ficha-producto-proceso.md](S4-3-2-2-ficha-producto-proceso.md) | `PROPUESTA` en `ELABORACION` |
| Fichas de indicador | [S4-3-2-2-fichas-indicador.md](S4-3-2-2-fichas-indicador.md) | `EVIDENCIA-INSUFICIENTE` |
| Diagrama del proceso | Fuente [S4-3-2-2-diagrama-proceso-tabla.md](S4-3-2-2-diagrama-proceso-tabla.md); genera BPMN, SVG, PNG y HTML | `PROPUESTA` en `ELABORACION` |
| Sustento | [S4-3-2-2-sustento.md](S4-3-2-2-sustento.md) | Vigente para trazabilidad |
| Procedimiento | No creado | Pendiente determinar si cumple los criterios del numeral 6.1.3 d de la NT |

Vista para revision: [Diagrama interactivo](S4-3-2-2-diagrama-proceso.html).

## Subprocesos

No se han adoptado procesos de nivel 4.

## Pendientes

- Confirmar el nombre, serie documental, custodia y medio de notificacion de la respuesta firmada.
- Confirmar el acto de emision de la carta de SGGOS y consultar las bases aplicables para identificar al elaborador del adicional cuando corresponda.
- Desarrollar la variante con inspector de obra perteneciente a la entidad.
- Confirmar los indicadores, metas y fuentes de datos del proceso.

## Relaciones

- [S4.3.2.3 Gestion de modificaciones de alcance](../S4-3-2-3-gestion-adicionales-deductivos-obra/00-S4-3-2-3-gestion-adicionales-deductivos-obra.md)
- [S4.3.2.4 Gestion de ampliaciones de plazo](../S4-3-2-4-gestion-ampliaciones-plazo/00-S4-3-2-4-gestion-ampliaciones-plazo.md)
- [S4.3.2.5 Formalizacion de suspensiones de plazo](../S4-3-2-5-formalizacion-suspensiones-plazo/00-S4-3-2-5-formalizacion-suspensiones-plazo.md)
- [S4.3.2.6 Gestion de paralizacion y reinicio](../S4-3-2-6-gestion-paralizacion-reinicio/00-S4-3-2-6-gestion-paralizacion-reinicio.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)
- [Modelo Bizagi de Consultas](../../../../../99-temporal/modelos/sggos-2026-11-02-bpmn/consultas-bizagi.bpmn)

