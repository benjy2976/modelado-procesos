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

# Informe de auditoría S4.3.2.8

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3.2.8`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `0DDE10A7FBB3485A`. Afirmaciones vigentes: 20 (INFERENCIA: 14, SUSTENTADA: 6).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| R1 | condicion | `SUSTENTADA` | El proceso inicia al identificarse la necesidad de mayores metrados. | reglamento-de-la-ley-general-de-contrataciones-p `art-197.1` (p. 112) |
| R2 | documento | `SUSTENTADA` | El residente solicita los mayores metrados en el cuaderno. | reglamento-de-la-ley-general-de-contrataciones-p `art-197.1` (p. 112) |
| R3 | existencia | `INFERENCIA` | Remitir solicitud a supervision (mensaje-envio). | — |
| R4 | existencia | `INFERENCIA` | Pronunciamiento de supervision recibido (mensaje-recepcion). | — |
| RG | existencia | `INFERENCIA` | ¿Ejecucion autorizada? (compuerta). | — |
| R5 | documento | `SUSTENTADA` | El residente ejecuta y sustenta los mayores metrados del periodo. | reglamento-de-la-ley-general-de-contrataciones-p `art-197.2` (p. 112) |
| RF | entrada-salida | `SUSTENTADA` | El sustento pasa a valorización y la autoridad de gestión administrativa autoriza el pago. | reglamento-de-la-ley-general-de-contrataciones-p `art-197.2` (p. 112) |
| RF0 | existencia | `INFERENCIA` | Ejecucion no habilitada por esta ruta (fin). | — |
| S1 | existencia | `INFERENCIA` | Solicitud en cuaderno recibida (inicio-mensaje). | — |
| S2 | decision | `SUSTENTADA` | El supervisor verifica la figura, la modalidad y los acumulados. | reglamento-de-la-ley-general-de-contrataciones-p `art-197.1` (p. 112)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-197.1` (p. 112)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-197.4` (p. 112) |
| SG | decision | `SUSTENTADA` | El supervisor decide si autoriza. | reglamento-de-la-ley-general-de-contrataciones-p `art-197.1` (p. 112) |
| S3 | actor | `INFERENCIA` | El supervisor o inspector autoriza en el cuaderno y comunica a la entidad. | reglamento-de-la-ley-general-de-contrataciones-p `art-197.1` (p. 112)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-186.1` (p. 101)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-197.2` (p. 112) |
| SF1 | existencia | `INFERENCIA` | Autorizacion de ejecucion remitida (fin-mensaje). | — |
| S4 | excepcion | `INFERENCIA` | Si se excede el límite se aplica el 197.4 y no se habilita la ejecución. | reglamento-de-la-ley-general-de-contrataciones-p `art-197.4` (p. 112) |
| SF0 | existencia | `INFERENCIA` | Pronunciamiento sin autorizacion remitido (fin-mensaje). | — |
| M:R3>S1 | entrada-salida | `INFERENCIA` | Solicitud de mayores metrados (mensaje). | — |
| M:SF1>R4 | entrada-salida | `INFERENCIA` | Autorizacion (mensaje). | — |
| M:SF0>R4 | entrada-salida | `INFERENCIA` | Pronunciamiento sin autorizacion (mensaje). | — |
| M:S3>Gobierno Regional Huanuco | entrada-salida | `INFERENCIA` | Comunicacion de autorizacion (mensaje). | — |
| M:RF>S4.3.2.1 Control periodico de la ejecucion | entrada-salida | `INFERENCIA` | Sustento para valorizacion y autorizacion de pago (mensaje). | — |

## Contradicciones

Ninguna.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **R3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047.
- **R4 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047.
- **RG · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047.
- **RF0 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047.
- **S1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047.
- **S3 · actor.** El 197.1 atribuye la autorización al supervisor; el inspector la ejerce por el 186.1, lo que es una inferencia. Comunicar a la entidad no es exigencia literal, y la entidad no aprueba la ejecución (197.2).
- **SF1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047.
- **S4 · excepcion.** El 197.4 manda resolver el contrato si se supera el 50 % del componente obra. El modelo solo documenta el impedimento y no deriva la resolución.
- **SF0 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047.
- **M:R3>S1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:SF1>R4 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:SF0>R4 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:S3>Gobierno Regional Huanuco · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:RF>S4.3.2.1 Control periodico de la ejecucion · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| Solo en contratos a precios unitarios | `REPRESENTADO` | S2 | reglamento-de-la-ley-general-de-contrataciones-p `art-197.1` (p. 112) |
| Solicitud por anotación en el cuaderno de incidencias | `REPRESENTADO` | R2, R3 | reglamento-de-la-ley-general-de-contrataciones-p `art-197.1` (p. 112) |
| El supervisor autoriza en el cuaderno si no se supera el límite acumulado | `REPRESENTADO` | S2, SG, S3 | reglamento-de-la-ley-general-de-contrataciones-p `art-197.1` (p. 112) |
| Sin aprobación previa de la entidad para ejecutar, pero sí para pagar | `REPRESENTADO` | RF | reglamento-de-la-ley-general-de-contrataciones-p `art-197.2` (p. 112) |
| Los mayores metrados se presentan en la valorización del periodo | `REPRESENTADO` | R5, RF | reglamento-de-la-ley-general-de-contrataciones-p `art-197.2` (p. 112) |
| Si generan ampliación de plazo, los mayores gastos generales se pagan por el art. 201 | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-197.3` (p. 112) |
| Los mayores metrados son causal de ampliación de plazo | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-198.1` (p. 112, 113) |
| Si se supera el 50 % del componente obra, se resuelve el contrato | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-197.4` (p. 112) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 0.
- Obligaciones de la fuente no representadas: 3.
- Anclas del visor: {'VIGENTE': 12}.
