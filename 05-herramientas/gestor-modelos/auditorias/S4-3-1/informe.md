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

# Informe de auditoría S4.3.1

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3.1`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `37A2FC2D2201BD9B`. Afirmaciones vigentes: 34 (INFERENCIA: 16, SUSTENTADA: 18).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| C:Gobierno Regional Huanuco/SGGOS — Subgerente de Gestion de Obras y Supervision | actor | `SUSTENTADA` | La SGGOS conduce el inicio de la ejecución. | reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |
| E1 | actor | `SUSTENTADA` | El proceso inicia con el contrato de obra suscrito por la GRA. | reglamento-organizacion-funciones-grh-2023 `art-25` (p. 15, 16) |
| T0A | secuencia | `INFERENCIA` | La GRA remite el contrato para su registro documentario. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| T0B | accion | `INFERENCIA` | La OACGD registra el contrato y lo notifica a la GRI. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| T0C | accion | `INFERENCIA` | La GRI deriva el contrato a la SGGOS. | reglamento-organizacion-funciones-grh-2023 `art-89-parte2` (p. 44, 45, 46, 47)<br>reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |
| T0D | accion | `INFERENCIA` | La SGGOS designa un coordinador de obra. | reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |
| T0E | accion | `INFERENCIA` | La SGGOS notifica la designación y remite el contrato al coordinador. | — |
| T1 | accion | `SUSTENTADA` | La entidad revisa e inicia las gestiones para cumplir las condiciones de inicio. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.3` (p. 94) |
| T1 | plazo | `SUSTENTADA` | Las gestiones de entrega de los documentos de 176.1 y 176.2 se inician en no más de 22 días desde la suscripción. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.3` (p. 94) |
| T2 | condicion | `SUSTENTADA` | Se verifica si hay supervisión contratada o inspección habilitada. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93)<br>ley-general-de-contrataciones-publicas-con-modif `art-62.5` (p. 30) |
| G1 | decision | `SUSTENTADA` | Se distingue si existe supervisor contratado. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-186.4` (p. 101) |
| G3 | decision | `SUSTENTADA` | Sin supervisor se evalúa si procede la inspección temporal. | reglamento-de-la-ley-general-de-contrataciones-p `art-186.4` (p. 101)<br>ley-general-de-contrataciones-publicas-con-modif `art-62.5` (p. 30) |
| T8 | accion | `SUSTENTADA` | La SGGOS gestiona la designación de un inspector. | reglamento-de-la-ley-general-de-contrataciones-p `art-186.4` (p. 101) |
| GE1 | decision | `INFERENCIA` | Se espera lo que ocurra primero: supervisor contratado o inspector designado. | — |
| C1B | existencia | `INFERENCIA` | El supervisor contratado habilita la verificación. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| C1 | existencia | `INFERENCIA` | El supervisor contratado habilita la verificación (rama sin inspector). | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| C2 | existencia | `SUSTENTADA` | La designación del inspector habilita la verificación. | reglamento-de-la-ley-general-de-contrataciones-p `art-186.4` (p. 101) |
| T3 | accion | `SUSTENTADA` | Se comunica al contratista quién supervisa la obra. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| T4 | condicion | `SUSTENTADA` | Se verifica la entrega de la documentación técnica actualizada. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| T5 | condicion | `SUSTENTADA` | Se verifica la entrega del adelanto directo y la suscripción del contrato de la JPRD. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-179.2` (p. 97) |
| T6 | condicion | `SUSTENTADA` | Se verifica la entrega total o parcial del terreno. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| G2 | decision | `SUSTENTADA` | El inicio procede cuando se cumplen todas las condiciones. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| T9 | accion | `INFERENCIA` | Si faltan condiciones, se coordinan los requisitos pendientes. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.4` (p. 94, 95)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-176.7` (p. 95) |
| GE2 | decision | `INFERENCIA` | Se espera la acreditación de cada requisito pendiente. | — |
| C3 | existencia | `SUSTENTADA` | Se acredita la documentación técnica actualizada. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| C4 | existencia | `SUSTENTADA` | Se acredita la entrega del adelanto directo. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| C5 | existencia | `SUSTENTADA` | Se acredita la suscripción del contrato de la JPRD. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| C6 | existencia | `SUSTENTADA` | Se acredita la entrega del terreno. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| G4 | secuencia | `INFERENCIA` | Cada requisito acreditado vuelve a la verificación. | — |
| T7 | documento | `INFERENCIA` | Se comunica el cumplimiento de las condiciones de inicio, sin acta. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-176.9` (p. 96) |
| T7 | documento | `INFERENCIA` | El inicio se formaliza mediante un acta de inicio de obra. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| F1 | entrada-salida | `INFERENCIA` | El proceso termina con el inicio del plazo comunicado. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| F1 | entrada-salida | `INFERENCIA` | S4.3.1 termina con el acta de inicio de obra emitida. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| M:F1>S4.3.2 Ejecucion | entrada-salida | `INFERENCIA` | El acta de inicio de obra pasa a S4.3.2. | — |

## Contradicciones

Ninguna.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **T0A · secuencia.** Ruta operativa propuesta; falta cotejo con un expediente y con el SGD.
- **T0B · accion.** El art. 20 asigna a la OACGD registrar y derivar documentos; la notificación a la GRI en particular es la secuencia propuesta.
- **T0C · accion.** La GRI monitorea la ejecución y la SGGOS depende de ella y controla las obras; la derivación concreta es inferida.
- **T0D · accion.** Práctica informada por el usuario (DEC-042); el ROF no menciona la figura del coordinador ni el instrumento de designación.
- **T0E · accion.** Paso operativo sin fuente documental.
- **GE1 · decision.** Patrón de compuerta basada en eventos propuesto por el usuario (2026-11-18).
- **C1B · existencia.** Evento de espera propuesto.
- **C1 · existencia.** Dos eventos con el mismo nombre en ramas distintas (C1 y C1B); conviene distinguirlos.
- **T9 · accion.** El modelo no representa las consecuencias del 176.4 (requerimiento del contratista, resarcimiento, resolución) ni el diferimiento por acuerdo del 176.7-176.9, aunque los cita.
- **GE2 · decision.** Disposición BPMN propuesta.
- **G4 · secuencia.** Disposición BPMN propuesta.
- **T7 · documento.** Práctica institucional informada por el usuario el 2026-11-24: en contrata, el GORE formaliza con un acta de inicio el cumplimiento de las condiciones. T7 no la representa. El Reglamento prevé actas, publicadas en la Pladicop, para diferir y reiniciar el inicio (176.9).
- **F1 · entrada-salida.** S4.3 declara como salida el acta de inicio y S4.3.2 espera recibirla; F1 no la envía (candidato de interfaz).
- **T7 · documento.** Práctica institucional en obras por contrata indicada por el usuario el 2026-11-24 para formalizar el inicio al cumplirse las condiciones; el Reglamento no la exige.
- **F1 · entrada-salida.** Salida declarada por S4.3 y recibida por S4.3.2; práctica institucional.
- **M:F1>S4.3.2 Ejecucion · entrada-salida.** Interfaz alineada con el inicio de S4.3.2 (E-1); práctica institucional.

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| a) Documentación técnica actualizada, si cambió en la selección | `REPRESENTADO` | T4, C3 | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| b) Comunicar al contratista quién supervisa | `REPRESENTADO` | T2, T3 | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| c) Adelanto directo entregado, si se solicitó | `REPRESENTADO` | T5, C4 | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| d) Contrato tripartito de la JPRD, de corresponder | `REPRESENTADO` | T5, C5 | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| e) Entrega total o parcial del terreno | `REPRESENTADO` | T6, C6 | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| La entidad inicia las gestiones en no más de 22 días desde la suscripción | `REPRESENTADO` | T1 | reglamento-de-la-ley-general-de-contrataciones-p `art-176.3` (p. 94) |
| Si no cumple en 10 días del requerimiento, el contratista puede pedir resarcimiento o resolver | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-176.4` (p. 94, 95) |
| Diferimiento del inicio por acuerdo (estacionalidad, errores del expediente, imposibilidad b o d) | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-176.7` (p. 95) |
| Al diferir se suspende la entrega del adelanto y se reanuda 15 días antes | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-176.8` (p. 95) |
| Acta de diferimiento y acta de reinicio publicadas en la Pladicop | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-176.9` (p. 96) |
| Entrega del adelanto directo en 7 días desde la garantía | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-179.2` (p. 97) |
| Inspector temporal mientras se contrata al supervisor | `REPRESENTADO` | G3, T8, C2 | reglamento-de-la-ley-general-de-contrataciones-p `art-186.4` (p. 101) |
| La GRA suscribe contratos de obras | `REPRESENTADO` | E1 | reglamento-organizacion-funciones-grh-2023 `art-25` (p. 15, 16) |
| La OACGD registra y deriva documentos | `REPRESENTADO` | T0B | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| La SGGOS controla y sigue la ejecución de obras | `REPRESENTADO` | C:Gobierno Regional Huanuco/SGGOS — Subgerente de Gestion de Obras y Supervision | reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 0.
- Obligaciones de la fuente no representadas: 5.
- Anclas del visor: {'VIGENTE': 41}.
