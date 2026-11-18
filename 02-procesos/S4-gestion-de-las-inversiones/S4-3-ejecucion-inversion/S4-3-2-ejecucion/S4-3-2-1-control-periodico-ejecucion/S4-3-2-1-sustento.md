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
fecha_actualizacion: 2026-11-17
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
| Descripcion del tramite regular por el usuario | Instruccion recibida el 2026-11-17: cajas 7, 10 y 14 y secuencia de recepcion, revision, informe, conformidad para tramite de pago u observaciones | `PROPUESTA` operativa del usuario; pendiente de contraste institucional | Precision de carriles y dos rutas posteriores a la revision de la valorizacion |

## Delimitacion aplicada

El Bizagi de Ejecucion mezcla adelantos, compatibilidad del expediente tecnico, valorizaciones y una salida hacia recepcion. Para este proceso solo se utiliza el circuito recurrente de valorizacion. Los adelantos y la compatibilidad se analizaran en S4.3.1; la recepcion corresponde a S4.3.3.

`DEC-042` distingue pertenencia y responsabilidad: el residente actua dentro del Ejecutor de obra; el control corresponde alternativamente al supervisor contratado o al inspector de la entidad. Este modelo de trabajo conserva un solo proceso con carriles; las etiquetas compuestas no afirman que todos los actores pertenezcan a una misma organizacion. El usuario identifica al monitor de obras de SGGOS como responsable de la revision institucional de la valorizacion (caja 7), a Atencion al Ciudadano como receptor y derivador inicial, y al subgerente de SGGOS como quien recibe y deriva al monitor. La adscripcion concreta de Atencion al Ciudadano y la funcion que actua en GRI requieren confirmacion documental; los carriles son funcionales.

## Elementos registrados

| Elemento | Contenido | Clase | Fuente |
|---|---|---|---|
| Disparador | Cierre del periodo de valorizacion | `NORMATIVO` citado | Reglamento, art. 210.1 |
| Instancia | Una por periodo de control o valorizacion | `PROPUESTA` | DEC-032 y analisis del flujo |
| Nucleo | Elaborar, revisar, observar, subsanar y aprobar la valorizacion | `OBSERVADO` reorganizado | ejecucion-bizagi.bpmn |
| Producto | Valorizacion remitida por GRI a Administracion para tramite de pago, o carta de observaciones notificada directamente al contratista | `PROPUESTA` operativa | Descripcion del usuario, 2026-11-17; pasos internos de pago pendientes |

## Tramite regular descrito el 2026-11-17

El usuario indico la secuencia institucional: Atencion al Ciudadano recepciona la valorizacion y la deriva a SGGOS; el subgerente la recepciona y deriva al monitor de obras; el monitor la revisa en la caja 7. Si cumple, el monitor elabora su informe y proyecta el informe del subgerente; el expediente se envia a la Gerencia de Infraestructura, que lo tramita a Administracion para pago. Si esta observado, el monitor elabora su informe y proyecta la carta del subgerente, quien notifica directamente al contratista. Estas son instrucciones de modelamiento del usuario, no una conformidad institucional ni una regla normativa validada.

La precision del usuario del 2026-11-17 establece que, en la caja 10, el monitor verifica los calculos de penalidad, amortizacion, retenciones y demas conceptos que correspondan e incorpora esa informacion y el monto propuesto para pagar en su informe. Se conserva la preparacion del proyecto de informe del subgerente. En la caja 14, el subgerente revisa y emite su propio informe otorgando conformidad; con esa conformidad se tramitara el pago por la ruta hacia GRI y Administracion. Esta precision sustituye la inferencia anterior sobre la actuacion del subgerente y se registra como `PROPUESTA` operativa del usuario, pendiente de contraste institucional. La conformidad descrita es un acto del proceso modelado, no una conformidad de revision ni aprobacion de estos documentos. La firma o mecanismo de emision, el canal de notificacion directa al contratista, la adscripcion de Atencion al Ciudadano, el cargo que tramita en GRI y el circuito posterior dentro de Administracion quedan en `EVIDENCIA-INSUFICIENTE`; el modelo no les asigna plazos. El bucle previo de observaciones del supervisor o inspector permanece como antecedente del modelo y no se confunde con la observacion emitida por el monitor.

La generacion focalizada previa a la precision de las cajas 10 y 14 del 2026-11-17 deja D1, D2, D3, D4 y D5 sin hallazgos. Las etiquetas de documentos que causaban cruces D4 se retiraron del dibujo; el informe del monitor, los proyectos del subgerente y la carta permanecen identificados aqui y en la ficha. Los dos finales conservan como mensajes el tramite hacia Administracion y la notificacion al contratista. La revision institucional del contenido sigue pendiente.

## Paquete de contexto de la precision de cajas 10 y 14

- Fase: conceptual; proceso S4.3.2.1; modalidad conservada segun regimen.
- Fuentes textuales activas: indice, ficha, tabla y sustento del proceso; instruccion del usuario del 2026-11-17.
- Evidencia activa: descripcion operativa del usuario; no se incorpora una exigencia normativa nueva ni una regla validada.
- Glosario aplicable: monitor de obras, subgerente de SGGOS, GRI y Administracion, con el sentido funcional ya registrado.
- Archivos modificables: tabla, sustento y ficha; generacion focalizada al cerrar el lote.
- Derivados excluidos del contexto: BPMN XML, SVG, PNG y HTML; revision visual no requerida en esta tarea.
- Modificacion de herramientas: no autorizada. Cierre: precisiones incorporadas y derivados actualizados, con hallazgos D1-D5 registrados si aparecen.

Resultado del lote de precision de cajas 10 y 14 (2026-11-17): BPMN, SVG, PNG y HTML actualizados; D1-D5 sin hallazgos. Se conserva la etiqueta breve "Informe del subgerente" en la entrada de la caja 15 para evitar un cruce D4; su naturaleza de informe propio de conformidad queda explicita en la caja 14, las notas de la tabla y la ficha. Sin revision visual ni conformidad institucional.

## Vacios de evidencia

| Vacio | Marca | Fuente o accion necesaria |
|---|---|---|
| Controles periodicos distintos de la valorizacion | `EVIDENCIA-INSUFICIENTE` | Levantamiento con el equipo y fuentes aplicables |
| Dueno del proceso y adscripcion formal de los actores identificados | `EVIDENCIA-INSUFICIENTE` | ROF, MOP u opinion del responsable de procesos; el usuario identifico funciones operativas, no al dueno |
| Detalle del proceso de pago en Administracion | `EVIDENCIA-INSUFICIENTE` | Confirmar su articulacion con S2.1 u otro proceso y los actos posteriores |
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

## Convencion de carriles y SGD

Se aplica la [convencion de carriles y SGD](../../../../../00-gobernanza/estandar-artefactos-modelamiento.md#74-convencion-de-carriles-y-sgd-en-s432) de `DEC-043`. En este modelo preliminar de un solo pool, los carriles identifican por nombre la responsabilidad del residente, del supervisor o inspector y de la unidad institucional aun no acreditada. La derivacion interna del informe para tramite de pago se expresa como tarea de usuario y `almacen: SGD`. La adscripcion de la unidad receptora sigue con `EVIDENCIA-INSUFICIENTE`; el uso de SGD no identifica al destinatario del pago. El titulo Ejecutor de obra, segun regimen conserva la diferencia entre contrata y administracion directa sin atribuir un contratista a esta ultima.

La generacion focalizada de esta normalizacion dejo D1-D5 sin hallazgos en su fecha. Se regeneraron BPMN, SVG, PNG y HTML. No se atribuye conformidad institucional.

## Interfaz con mayores metrados - DEC-047

S4.3.2.8 entrega el sustento del periodo y la autorizacion de ejecucion de mayores metrados. Esta ultima no equivale a autorizar el pago: verificar la autorizacion de la autoridad de gestion administrativa conforme al art. 197.2 antes de tramitarlo. El detalle de esta interfaz y la ubicacion documental del control de pago requieren evidencia operativa; no se modifica en este lote la secuencia vigente de valorizacion. Fuente, consulta y vigencia en el [sustento de S4.3.2.8](../S4-3-2-8-gestion-mayores-metrados/S4-3-2-8-sustento.md).
