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

# Informe de auditoría S4.3.2.6

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3.2.6`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `2B254AD775A38733`. Afirmaciones vigentes: 26 (INFERENCIA: 21, SUSTENTADA: 5).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| R-E1 | condicion | `INFERENCIA` | El proceso inicia con un evento de paralización o de reinicio. | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)<br>ds206_2024ef `art-2.2` (p. 2)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-198.1` (p. 112, 113) |
| R-T1 | documento | `SUSTENTADA` | El residente registra y sustenta el evento en el cuaderno. | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)<br>directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-188.3` (p. 104, 105) |
| R-F1 | existencia | `INFERENCIA` | Evento y sustento remitidos (fin-mensaje). | — |
| S-E1 | existencia | `INFERENCIA` | Evento y sustento recibidos (inicio-mensaje). | — |
| S-T1 | actor | `SUSTENTADA` | El supervisor o inspector valida la causal o las condiciones de reinicio. | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)<br>directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| S-F1 | existencia | `INFERENCIA` | Evento validado y remitido (fin-mensaje). | — |
| E-E1 | actor | `SUSTENTADA` | La OACGD recibe el expediente. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-T1 | accion | `SUSTENTADA` | La OACGD registra y deriva por el SGD. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-T2 | actor | `SUSTENTADA` | El coordinador de la SGGOS verifica y clasifica régimen y evento. | reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49)<br>reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |
| E-G1 | existencia | `INFERENCIA` | ¿Requiere evaluacion tecnica especializada? (compuerta). | — |
| E-T3 | existencia | `INFERENCIA` | Evaluar causal o condiciones tecnicas (tarea). | — |
| E-G2 | existencia | `INFERENCIA` | ¿Que se gestiona? (compuerta). | — |
| E-T4 | existencia | `INFERENCIA` | Consolidar el expediente de paralizacion (tarea-usuario). | — |
| E-T5 | actor | `INFERENCIA` | La autoridad competente resuelve sobre la paralización. | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)<br>ds206_2024ef `art-5.2` (p. 3) |
| E-G3 | existencia | `INFERENCIA` | ¿Favorable? (compuerta). | — |
| E-T6 | existencia | `INFERENCIA` | Actualizar registros y coordinar la comunicacion (tarea-usuario). | — |
| E-F1 | existencia | `INFERENCIA` | Paralizacion formalizada y comunicada (fin-mensaje). | — |
| E-F2 | existencia | `INFERENCIA` | Paralizacion no formalizada comunicada (fin-mensaje). | — |
| E-T7 | existencia | `INFERENCIA` | Consolidar el sustento de reinicio (tarea-usuario). | — |
| E-T8 | actor | `INFERENCIA` | La autoridad competente formaliza el reinicio. | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| E-G4 | existencia | `INFERENCIA` | ¿Favorable? (compuerta). | — |
| E-T9 | documento | `INFERENCIA` | Se actualizan registros tras el reinicio. | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30)<br>directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| E-F3 | existencia | `INFERENCIA` | Reinicio formalizado y comunicado (fin-mensaje). | — |
| E-F4 | existencia | `INFERENCIA` | Reinicio no formalizado comunicado (fin-mensaje). | — |
| M:R-F1>S-E1 | entrada-salida | `INFERENCIA` | Evento y sustento (mensaje). | — |
| M:S-F1>E-E1 | entrada-salida | `INFERENCIA` | Evento validado y opinion (mensaje). | — |

## Contradicciones

Ninguna.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **R-E1 · condicion.** En administración directa el 7.3.7 regula la paralización y el reinicio. La Ley 31589 define la «obra pública paralizada» de su régimen especial (avance ≥ 40 % o ≥ 50 % y 6 meses sin ejecución), no el evento ordinario de paralización. En contrata, el Reglamento no tiene una figura propia de paralización: la trata como causal de ampliación (198.1 a) o, si hay acuerdo, como suspensión (107).
- **R-F1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Aplicacion operativa de las fuentes citadas.
- **S-E1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Directiva 017-2023-CG, num. 7.3.7.
- **S-F1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Circuito propuesto sobre las fuentes citadas.
- **E-G1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: El coordinador no sustituye al especialista; DEC-041.
- **E-T3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Alcance exacto pendiente por regimen.
- **E-G2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Separacion adoptada en DEC-041.
- **E-T4 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: No sustituye opiniones especializadas.
- **E-T5 · actor.** En AD la paralización se formaliza como modificación de plazo, aprobada por acto resolutivo del funcionario competente (7.3.7). El 5.2 de la Ley 31589 (continuar o resolver el contrato) solo aplica a obras inventariadas como paralizadas en su régimen especial, no a la decisión sobre una paralización.
- **E-G3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Rutas de decision; tratamiento completo por regimen pendiente.
- **E-T6 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Circuito interno pendiente de validacion.
- **E-F1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto propuesto.
- **E-F2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto alterno.
- **E-T7 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: No sustituye evaluaciones especializadas.
- **E-T8 · actor.** En AD «la OAD de la entidad autorizará el reinicio»; que la OAD sea el titular de la competencia no está acreditado. En contrata, EVIDENCIA-INSUFICIENTE según el sustento.
- **E-G4 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Rutas de decision.
- **E-T9 · documento.** El 7.3.7 exige el cronograma actualizado del residente en 2 días calendario y el registro en el SNPMGI e INFOBRAS antes de la ampliación; el modelo no los nombra.
- **E-F3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto propuesto.
- **E-F4 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto alterno.
- **M:R-F1>S-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:S-F1>E-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| El residente informa al supervisor o inspector por el cuaderno de obra para su validación | `REPRESENTADO` | R-T1, R-F1, S-E1, S-T1 | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| El residente comunica el reinicio al supervisor o inspector | `REPRESENTADO` | R-T1, S-T1 | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| Informe aprobatorio del supervisor o inspector para el reinicio | `REPRESENTADO` | S-T1, S-F1 | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| La OAD autoriza el reinicio | `REPRESENTADO` | E-T8 | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| Anotar en el cuaderno la fecha de la solicitud, la fecha real de paralización y la de reinicio | `NO-REPRESENTADO` | — | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| Cronograma actualizado en 2 días calendario tras el reinicio, para el acto resolutivo | `NO-REPRESENTADO` | — | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| La modificación de plazo se aprueba por acto resolutivo del funcionario competente | `REPRESENTADO` | E-T5 | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| Registro previo en el SNPMGI e INFOBRAS | `NO-REPRESENTADO` | — | directiva-n-017-2023-cg-gmpl `art-3-parte16` (p. 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30) |
| Ámbito del régimen especial: avance ≥ 40 % y 6 meses sin ejecución, o contrato resuelto o nulo | `NO-REPRESENTADO` | — | ds206_2024ef `art-2.1` (p. 2) |
| Obra inventariada con contrato vigente: proponer la continuidad o resolver | `NO-REPRESENTADO` | — | ds206_2024ef `art-5.2` (p. 3) |
| El contratista responde la propuesta de continuidad en 15 días calendario | `NO-REPRESENTADO` | — | ds206_2024ef `art-5.3` (p. 3) |
| En contrata, la paralización no atribuible es causal de ampliación de plazo | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-198.1` (p. 112, 113) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 29.
- Obligaciones de la fuente no representadas: 7.
- Anclas del visor: {'VIGENTE': 16}.
