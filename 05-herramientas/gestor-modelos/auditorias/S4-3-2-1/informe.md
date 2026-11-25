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

# Informe de auditoría S4.3.2.1

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3.2.1`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `C4D41E45B6430525`. Afirmaciones vigentes: 20 (CONTRADICCION: 1, INFERENCIA: 7, SUSTENTADA: 12).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| C:S4.3.2.1 Control periodico de la ejecucion/Supervisor o inspector de obra, segun modalidad | actor | `SUSTENTADA` | El supervisor o inspector revisa la valorización. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.2` (p. 118) |
| E-1 | decision | `SUSTENTADA` | El control se dispara al cierre de cada mes, una instancia por periodo. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.1` (p. 118) |
| T-1 | accion | `SUSTENTADA` | El ejecutor elabora y presenta la valorización. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.2` (p. 118)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-210.2` (p. 118) |
| T-2 | accion | `SUSTENTADA` | El supervisor o inspector revisa la valorización. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.2` (p. 118) |
| G-1 | decision | `INFERENCIA` | El supervisor decide si la valorización cumple las condiciones técnicas. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.2` (p. 118) |
| T-4 | accion | `INFERENCIA` | El control de obra devuelve observaciones al ejecutor. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.2` (p. 118) |
| T-5 | accion | `INFERENCIA` | El ejecutor subsana y vuelve a presentar al supervisor. | — |
| T-3 | accion | `INFERENCIA` | El monitor de obras revisa la valorización. | reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |
| G-2 | decision | `SUSTENTADA` | La entidad decide si la valorización cumple. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| T-6 | accion | `SUSTENTADA` | El monitor informa observaciones y proyecta la carta al contratista. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| T-7 | accion | `SUSTENTADA` | Se verifican los cálculos y se informa el monto a pagar. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.6` (p. 119)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| F-1 | entrada-salida | `SUSTENTADA` | El proceso termina con la valorización remitida a Administración para pago. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| T-8 | accion | `SUSTENTADA` | Atención al Ciudadano recepciona la valorización revisada y la deriva a SGGOS. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| T-9 | accion | `INFERENCIA` | El subgerente de la SGGOS deriva la valorización al monitor de obras. | reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |
| T-10 | accion | `INFERENCIA` | El subgerente emite su propio informe de conformidad. | — |
| T-11 | accion | `INFERENCIA` | La GRI tramita la valorización para pago ante Administración. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| T-12 | accion | `SUSTENTADA` | El subgerente notifica directamente al contratista las observaciones. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| F-2 | entrada-salida | `CONTRADICCION` | Con observaciones, el proceso termina sin pago. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.4` (p. 118)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| M:F-1>Administracion | entrada-salida | `SUSTENTADA` | La valorización se envía a Administración para el trámite de pago. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| M:F-2>Contratista | entrada-salida | `SUSTENTADA` | Se envía la carta de observaciones al contratista. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |

## Contradicciones

- **F-2 · entrada-salida.** El Reglamento otorga plazo de subsanación, revisa la respuesta en 2 días hábiles y, aunque no se subsane, paga el monto no cuestionado (210.4). Terminar en F-2 omite la subsanación y el pago parcial.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **G-1 · decision.** Reconstruido del Bizagi observado; el Reglamento prevé que el supervisor informe a la entidad, no un ciclo de devolución al contratista.
- **T-4 · accion.** Práctica observada (Bizagi); debe compatibilizarse con el plazo de 5 días del 210.2.
- **T-5 · accion.** Inferido para cerrar el ciclo observado.
- **T-9 · accion.** Trámite regular descrito por el usuario el 2026-11-17.
- **T-3 · accion.** Trámite regular descrito por el usuario el 2026-11-17. La figura del monitor no figura en el ROF.
- **T-10 · accion.** Trámite regular descrito por el usuario el 2026-11-17. Precisión de la caja 14.
- **T-11 · accion.** Trámite regular descrito por el usuario el 2026-11-17.

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| Valorización mensual o en el periodo que fijen las bases | `REPRESENTADO` | E-1 | reglamento-de-la-ley-general-de-contrataciones-p `art-210.1` (p. 118) |
| Las valorizaciones incluyen adicionales y mayores metrados | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-210.1` (p. 118) |
| Revisión conjunta de metrados entre residente y supervisor | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-210.2` (p. 118) |
| Presentación al supervisor y a la entidad en los primeros 3 días | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-210.2` (p. 118) |
| Informe del supervisor a la entidad en 5 días | `REPRESENTADO` | T-2, T-8 | reglamento-de-la-ley-general-de-contrataciones-p `art-210.2` (p. 118) |
| La entidad evalúa y paga hasta el último día del mes de presentación | `REPRESENTADO` | G-2, T-7, F-1 | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| Observaciones comunicadas al supervisor y al contratista con plazo | `REPRESENTADO` | T-6, T-12 | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| Revisión de la subsanación en 2 días hábiles | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-210.3` (p. 118) |
| Pago del monto no cuestionado si no se subsana | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-210.4` (p. 118) |
| En la última valorización, planos post construcción o suspensión del pago | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-210.10` (p. 119) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 0.
- Obligaciones de la fuente no representadas: 6.
- Anclas del visor: {'VIGENTE': 14}.
