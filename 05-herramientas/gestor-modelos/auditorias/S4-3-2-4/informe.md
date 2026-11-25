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

# Informe de auditoría S4.3.2.4

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3.2.4`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `1B8B1E88B30B6B43`. Afirmaciones vigentes: 23 (INFERENCIA: 8, SUSTENTADA: 15).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| R-E1 | condicion | `SUSTENTADA` | El proceso inicia al identificarse una causal de ampliación. | reglamento-de-la-ley-general-de-contrataciones-p `art-198.1` (p. 112, 113) |
| R-T1 | plazo | `SUSTENTADA` | El contratista registra la causal y presenta la solicitud. | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| R-F1 | entrada-salida | `SUSTENTADA` | La solicitud se remite. | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| S-E1 | entrada-salida | `SUSTENTADA` | El supervisor recibe la solicitud. | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| S-T1 | plazo | `SUSTENTADA` | El supervisor evalúa la causal y emite opinión. | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-198.3` (p. 113) |
| S-F1 | entrada-salida | `SUSTENTADA` | La solicitud y la opinión llegan al GORE. | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| E-E1 | actor | `SUSTENTADA` | La OACGD recibe el expediente. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-T1 | accion | `SUSTENTADA` | La OACGD registra y deriva por el SGD. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-T2 | existencia | `INFERENCIA` | Evaluar solicitud y sustento de ampliacion (tarea). | — |
| E-T3 | existencia | `INFERENCIA` | Emitir informe y elevar expediente al subgerente por SGD (tarea-usuario). | — |
| E-T4 | actor | `SUSTENTADA` | El subgerente de la SGGOS emite el informe técnico de procedencia. | reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |
| E-T5 | existencia | `INFERENCIA` | Elevar informe tecnico y expediente a GRI por SGD (tarea-usuario). | — |
| E-T6 | actor | `SUSTENTADA` | La GRI evalúa la procedencia. | reglamento-organizacion-funciones-grh-2023 `art-89-parte2` (p. 44, 45, 46, 47) |
| E-T7 | existencia | `INFERENCIA` | Remitir expediente con memorandum a GRAJ por SGD (tarea-usuario). | — |
| E-T8 | actor | `SUSTENTADA` | Asesoría Jurídica emite opinión legal. | reglamento-organizacion-funciones-grh-2023 `art-45-parte1` (p. 24, 25, 26)<br>reglamento-organizacion-funciones-grh-2023 `art-44` (p. 24) |
| E-T8A | existencia | `INFERENCIA` | Proyectar resolucion y derivar expediente al decisor por SGD (tarea-usuario). | — |
| E-T9 | plazo | `SUSTENTADA` | La autoridad competente resuelve la solicitud. | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| E-G1 | decision | `SUSTENTADA` | La ampliación se aprueba o no. | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| E-T10 | documento | `INFERENCIA` | Se actualizan el plazo y el cronograma y se registra la decisión en el SGD. | reglamento-de-la-ley-general-de-contrataciones-p `art-198.4` (p. 113) |
| E-F1 | entrada-salida | `SUSTENTADA` | La resolución favorable se comunica. | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| E-F2 | entrada-salida | `SUSTENTADA` | La resolución no favorable se comunica. | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| M:R-F1>S-E1 | entrada-salida | `INFERENCIA` | Solicitud y sustento (mensaje). | — |
| M:S-F1>E-E1 | entrada-salida | `INFERENCIA` | Solicitud y opinion (mensaje). | — |

## Contradicciones

Ninguna.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **E-T2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Observacion del usuario, 2026-11-10; ROF, arts. 97-98.
- **E-T3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Observacion del usuario, 2026-11-10.
- **E-T5 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Observacion del usuario, 2026-11-10.
- **E-T7 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Observacion del usuario, 2026-11-10.
- **E-T8A · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Aclaracion del usuario, 2026-11-10.
- **E-T10 · documento.** El 198.4 hace surtir efecto a la ampliación con su publicación en la Pladicop, sin adenda; el modelo registra en el SGD pero no nombra la Pladicop.
- **M:R-F1>S-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:S-F1>E-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| Causales que afectan la ruta crítica | `REPRESENTADO` | R-E1 | reglamento-de-la-ley-general-de-contrataciones-p `art-198.1` (p. 112, 113) |
| Se privilegia el criterio técnico sobre las formalidades | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-198.3` (p. 113) |
| Publicación en la Pladicop sin adenda | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-198.4` (p. 113) |
| Solicitud a la entidad y a la supervisión en 10 días hábiles, con prórroga de 10 | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| Las solicitudes extemporáneas se tienen por no presentadas | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| Opinión del supervisor en 5 días hábiles | `REPRESENTADO` | S-T1, S-F1 | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| Sin opinión del supervisor, la entidad responde igual | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| Resolución notificada por la Pladicop en 10 días hábiles | `REPRESENTADO` | E-T9, E-G1, E-F1, E-F2 | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| Silencio de la entidad: se aprueba lo informado o lo solicitado | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114) |
| Ampliación parcial si la causal no tiene fin previsto | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-200.2` (p. 114) |
| Ampliación de oficio de los contratos vinculados | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-200.4` (p. 114) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 0.
- Obligaciones de la fuente no representadas: 8.
- Anclas del visor: {'VIGENTE': 22}.
