---
id: AP-S4-3-2-1-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S4.3.2.1
nivel_proceso: 3
proceso:
  - S4.3.2.1
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-06
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-1
---

# S4.3.2.1 Control periodico de la ejecucion - Sustento

Sube a: [S4.3.2.1 Control periodico de la ejecucion](00-S4-3-2-1-control-periodico-ejecucion.md)

## Fuentes utilizadas

| Fuente | Ubicacion precisa | Estado | Uso |
|---|---|---|---|
| Exportacion Bizagi de Ejecucion | `99-temporal/modelos/sggos-2026-11-02-bpmn/ejecucion-bizagi.bpmn`, participante "S4.3.P2 Emision de Valorizacion" | `OBSERVADO`; BPMN invalido por flujos de mensaje incompletos | Actividades y decisiones del circuito de valorizacion |
| Reglamento de la Ley 32069 | Art. 210.1 | `NORMATIVO` citado; regla pendiente de validacion | Periodicidad y valorizacion de obra |
| Directiva 017-2023-CG | Num. 7.3.4 | `NORMATIVO` citado; regla pendiente de validacion | Valorizacion en administracion directa |
| Decision del equipo | `DEC-032` | `DECISION` | Codigo, nombre y adopcion como nivel 3 |

## Delimitacion aplicada

El Bizagi de Ejecucion mezcla adelantos, compatibilidad del expediente tecnico, valorizaciones y una salida hacia recepcion. Para este proceso solo se utiliza el circuito recurrente de valorizacion. Los adelantos y la compatibilidad se analizaran en S4.3.1; la recepcion corresponde a S4.3.3.

`DEC-042` distingue pertenencia y responsabilidad: el residente actua dentro del Ejecutor de obra; el control corresponde alternativamente al supervisor contratado o al inspector de la entidad. Como este modelo inicial usa un solo proceso con carriles, las etiquetas compuestas expresan esas responsabilidades sin afirmar que todos pertenezcan a una misma organizacion. La unidad institucional que recibe la valorizacion permanece como `EVIDENCIA-INSUFICIENTE`.

## Elementos registrados

| Elemento | Contenido | Clase | Fuente |
|---|---|---|---|
| Disparador | Cierre del periodo de valorizacion | `NORMATIVO` citado | Reglamento, art. 210.1 |
| Instancia | Una por periodo de control o valorizacion | `PROPUESTA` | DEC-032 y analisis del flujo |
| Nucleo | Elaborar, revisar, observar, subsanar y aprobar la valorizacion | `OBSERVADO` reorganizado | ejecucion-bizagi.bpmn |
| Producto | Expediente de valorizacion aprobado para tramite de pago | `PROPUESTA` | Salida observada en Bizagi; receptor pendiente |

## Vacios de evidencia

| Vacio | Marca | Fuente o accion necesaria |
|---|---|---|
| Controles periodicos distintos de la valorizacion | `EVIDENCIA-INSUFICIENTE` | Levantamiento con el equipo y fuentes aplicables |
| Dueno y unidades responsables | `EVIDENCIA-INSUFICIENTE` | ROF, MOP u opinion del responsable de procesos |
| Proceso receptor del expediente para pago | `EVIDENCIA-INSUFICIENTE` | Confirmar articulacion con S2.1 u otro proceso |
| Criterios de observacion y subsanacion | `EVIDENCIA-INSUFICIENTE` | Validacion operativa y normativa |
| Indicador, meta y fuente de datos | `EVIDENCIA-INSUFICIENTE` | Definicion del dueno del proceso |

## Discrepancias

| Hallazgo | Tratamiento |
|---|---|
| El Bizagi usa la denominacion "S4.3.P2 Emision de Valorizacion" | Se conserva como antecedente; `DEC-032` adopta el codigo S4.3.2.1 y un alcance provisionalmente mayor |
| El Bizagi tiene dos flujos de mensaje sin destino | No se copia el XML; se reconstruye el flujo desde la tabla y se valida con la cadena BPMN |
| El modelo anterior enviaba la valorizacion a la antigua S4.3.1 | Se retira esa relacion porque S4.3.1 ahora es Inicio de ejecucion; el receptor queda pendiente |

## Informacion BIM

`EVIDENCIA-INSUFICIENTE`. No se atribuyen requisitos BIM a la valorizacion sin fuente aplicable y validacion del equipo.

## Historial de revision

| Documento | Nivel | Fecha | Resultado | Rol o unidad | Evidencia |
|---|---|---|---|---|---|
| Juego inicial S4.3.2.1 | `ELABORACION` | 2026-11-03 | Propuesta creada; pendiente revision | Equipo del proyecto con asistencia de IA | DEC-032; exportacion Bizagi |
| Precision de participantes | `ELABORACION` | 2026-11-05 | Residente ubicado en Ejecutor de obra y control de obra expresado como responsabilidad alternativa | Equipo del proyecto con asistencia de IA | `DEC-042` |

## Relaciones

- [Sustento de S4.3.2](../S4-3-2-sustento.md)
- [Paquete de conocimientos sobre subprocesos de evento](../../../../../03-conocimiento/manual-bpmn/cap-2-notacion/2-8-subprocesos/conocimientos-propuestos-subprocesos-evento.md)


## Cambio de perfil de trazado ? 2026-11-06

Por indicacion del usuario se adopta `zigzag-controlado` para este subproceso. El cambio afecta la disposicion grafica; conserva actividades, participantes, secuencias y mensajes. Los registros anteriores de geometria corresponden a sus respectivas generaciones. Se regeneran los derivados mediante la tabla; no se realiza revision visual ni se atribuye conformidad institucional.

Resultado de los controles de esta generacion: D1, D2, D3 y D5 sin hallazgos. D4 sin superposiciones.

## Mejora del perfil zigzag-controlado ? 2026-11-06

Por solicitud del usuario se aplica la mejora general del perfil: compactacion de circuitos independientes y seleccion de corredores de mensajes con control de interferencias. Se conserva la semantica BPMN; no cambian actividades, responsables ni relaciones del proceso. D1, D2, D3 y D5 sin hallazgos. D4 sin hallazgos.
