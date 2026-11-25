---
tipo: informe
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
fecha_actualizacion: 2026-11-25
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Informe de auditoría S4.3.2.5

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3.2.5`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `C634D91B21338B8C`. Afirmaciones vigentes: 33 (INFERENCIA: 20, SUSTENTADA: 13).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| R-E1 | condicion | `SUSTENTADA` | El proceso inicia al identificarse una causa que impide continuar la obra. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-202.1` (p. 114, 115) |
| R-T1 | documento | `SUSTENTADA` | El residente registra y sustenta la causa en el cuaderno de incidencias. | reglamento-de-la-ley-general-de-contrataciones-p `art-188.3` (p. 104, 105) |
| R-F1 | existencia | `INFERENCIA` | Causa de suspension remitida (fin-mensaje). | — |
| S-E1 | existencia | `INFERENCIA` | Causa de suspension recibida (inicio-mensaje). | — |
| S-T1 | actor | `INFERENCIA` | El supervisor o inspector evalúa el impedimento y emite opinión. | reglamento-de-la-ley-general-de-contrataciones-p `art-186.1` (p. 101)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-188.3` (p. 104, 105) |
| S-F1 | existencia | `INFERENCIA` | Causa y opinion remitidas (fin-mensaje). | — |
| E-E1 | actor | `SUSTENTADA` | La OACGD recibe el expediente. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-T1 | accion | `SUSTENTADA` | La OACGD registra y deriva por el SGD. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-T2 | actor | `SUSTENTADA` | El coordinador de la SGGOS verifica y clasifica la figura. | reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49)<br>reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |
| E-G1 | decision | `SUSTENTADA` | Se decide si corresponde la suspensión contractual. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-202.1` (p. 114, 115) |
| E-T3 | accion | `SUSTENTADA` | La entidad coordina con el contratista las condiciones de la suspensión. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-202.1` (p. 114, 115)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59) |
| E-E2 | condicion | `SUSTENTADA` | La resolución de un contrato vinculado puede originar una suspensión acordada de la obra. | reglamento-de-la-ley-general-de-contrataciones-p `art-202.5` (p. 115) |
| E-M1 | existencia | `INFERENCIA` | Respuesta del ejecutor recibida (mensaje-recepcion). | — |
| E-G2 | decision | `SUSTENTADA` | La suspensión procede solo si hay acuerdo. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59) |
| E-T4 | existencia | `INFERENCIA` | Consolidar el acuerdo y elevarlo por SGD (tarea-usuario). | — |
| E-T5 | documento | `INFERENCIA` | La autoridad competente formaliza la suspensión mediante un acto. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59) |
| E-T5A | accion | `SUSTENTADA` | La entidad suspende el plazo de los contratos directamente vinculados, cuando corresponda. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.3` (p. 59) |
| E-T6 | existencia | `INFERENCIA` | Actualizar registros y coordinar la comunicacion (tarea-usuario). | — |
| E-F1 | existencia | `INFERENCIA` | Suspension de plazo formalizada y comunicada (fin-mensaje). | — |
| E-F2 | existencia | `INFERENCIA` | Suspension no formalizada comunicada (fin-mensaje). | — |
| C-E1 | existencia | `INFERENCIA` | Propuesta de suspension recibida (inicio-mensaje). | — |
| C-T1 | actor | `SUSTENTADA` | El contratista evalúa y responde la propuesta. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59) |
| C-F1 | existencia | `INFERENCIA` | Respuesta a la propuesta remitida (fin-mensaje). | — |
| E-R1 | condicion | `SUSTENTADA` | La reanudación inicia al verificarse el cese de la causa. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.2` (p. 59) |
| E-T7 | accion | `INFERENCIA` | Un especialista verifica las condiciones para reanudar. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.2` (p. 59) |
| E-T8 | existencia | `INFERENCIA` | Consolidar la verificacion y elevarla por SGD (tarea-usuario). | — |
| E-T9 | documento | `INFERENCIA` | La autoridad competente formaliza la reanudación del plazo. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.2` (p. 59)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-107.2` (p. 59) |
| E-T9A | documento | `SUSTENTADA` | Se suscribe el acta de reinicio de los contratos vinculados suspendidos. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.3` (p. 59) |
| E-F3 | entrada-salida | `INFERENCIA` | La reanudación formalizada se comunica. | reglamento-de-la-ley-general-de-contrataciones-p `art-202.2` (p. 115) |
| M:R-F1>S-E1 | entrada-salida | `INFERENCIA` | Causa y sustento (mensaje). | — |
| M:S-F1>E-E1 | entrada-salida | `INFERENCIA` | Causa y opinion (mensaje). | — |
| M:E-T3>C-E1 | entrada-salida | `INFERENCIA` | Propuesta de suspension (mensaje). | — |
| M:C-F1>E-M1 | entrada-salida | `INFERENCIA` | Respuesta del ejecutor (mensaje). | — |

## Contradicciones

Ninguna.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **R-F1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Aplicacion operativa del Reglamento, art. 202.1.
- **S-E1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Aplicacion operativa; validacion institucional pendiente.
- **S-T1 · actor.** La supervisión corresponde al supervisor o inspector (186.1); ninguna norma exige su opinión para acordar la suspensión: es práctica de control.
- **S-F1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Circuito propuesto sobre la fuente citada.
- **E-M1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, art. 202.1.
- **E-T4 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: No sustituye la decision formal; observacion del usuario, 2026-11-10.
- **E-T5 · documento.** El 107.1 exige un acuerdo escrito de las partes; un acto unilateral posterior es práctica institucional, no exigencia. El documento exacto sigue en EVIDENCIA-INSUFICIENTE.
- **E-T6 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Circuito interno pendiente de validacion.
- **E-F1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto propuesto.
- **E-F2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto alterno.
- **C-E1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, art. 202.1.
- **C-F1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, art. 202.1.
- **E-T7 · accion.** Paso de control interno sin exigencia literal.
- **E-T8 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Circuito interno pendiente de validacion; observacion del usuario, 2026-11-10.
- **E-T9 · documento.** El 107.2 exige un acta suscrita por las partes con la fecha de reinicio; solo sin acuerdo la entidad la determina. El modelo formaliza la reanudación de forma unilateral y sin el contratista.
- **E-F3 · entrada-salida.** El 202.2 exige comunicar al contratista el programa de ejecución y los calendarios actualizados; el fin no lo nombra ni tiene destinatario.
- **M:R-F1>S-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:S-F1>E-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-T3>C-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:C-F1>E-M1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| Acuerdo escrito de las partes ante un evento no atribuible | `REPRESENTADO` | E-G1, E-T3, C-T1, E-G2 | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59) |
| Sin mayores gastos, salvo los necesarios para viabilizar la suspensión | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59) |
| Los términos acordados incluyen la seguridad de la obra y de las personas | `REPRESENTADO` | E-T3, E-T4 | reglamento-de-la-ley-general-de-contrataciones-p `art-202.1` (p. 114, 115) |
| Acta de reinicio suscrita por las partes | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-107.2` (p. 59) |
| Sin acuerdo, la entidad determina la fecha de reinicio | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-107.2` (p. 59) |
| Suspensión de los contratos directamente vinculados | `REPRESENTADO` | E-T5A, E-T9A | reglamento-de-la-ley-general-de-contrataciones-p `art-107.3` (p. 59) |
| Comunicar al contratista el programa y los calendarios actualizados | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-202.2` (p. 115) |
| Suspensión por falta de pago de dos valorizaciones consecutivas | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-202.3` (p. 115) |
| El residente anota la suspensión por falta de pago y esta inicia al día siguiente | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-202.3` (p. 115) |
| Suspensión del contrato vinculado al resolverse el principal | `FUERA-DE-ALCANCE` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-202.4` (p. 115) |
| Suspensión del contrato principal al resolverse el vinculado | `REPRESENTADO` | E-E2, E-T3 | reglamento-de-la-ley-general-de-contrataciones-p `art-202.5` (p. 115) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 0.
- Obligaciones de la fuente no representadas: 6.
- Anclas del visor: {'VIGENTE': 37}.
