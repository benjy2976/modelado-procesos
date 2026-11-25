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

# Informe de auditoría S4.3.2.2

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3.2.2`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `B995646E7BDF8BBF`. Afirmaciones vigentes: 65 (INFERENCIA: 29, SUSTENTADA: 36).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| C:Gobierno Regional Huanuco/SGE — Especialistas tecnicos | actor | `SUSTENTADA` | La Sub Gerencia de Estudios absuelve las consultas de obra. | reglamento-organizacion-funciones-grh-2023 `art-96` (p. 47) |
| C-E1 | decision | `SUSTENTADA` | El contratista identifica una consulta que formula por el cuaderno. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106) |
| C-G1 | decision | `SUSTENTADA` | Se distingue si la consulta modifica el expediente y requiere informe técnico. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.2` (p. 106) |
| C-T1 | documento | `SUSTENTADA` | El ejecutor elabora el informe técnico de especialidad. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.2` (p. 106) |
| C-G2 | existencia | `INFERENCIA` | C-G2 (compuerta). | — |
| C-T2 | documento | `SUSTENTADA` | La consulta se registra en el cuaderno de incidencias. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-188.1` (p. 104) |
| C-F1 | entrada-salida | `SUSTENTADA` | La consulta queda dirigida al supervisor. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106) |
| C-E2 | existencia | `INFERENCIA` | Respuesta a la consulta recibida (inicio-mensaje). | — |
| C-T3 | existencia | `INFERENCIA` | Tomar conocimiento y registrar la respuesta (tarea-usuario). | — |
| C-F2 | existencia | `INFERENCIA` | Consulta atendida para el ejecutor (fin). | — |
| S-E1 | entrada-salida | `SUSTENTADA` | El supervisor recibe la consulta. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106) |
| S-T1 | existencia | `INFERENCIA` | Revisar la consulta y el expediente tecnico (tarea). | — |
| S-G1 | decision | `SUSTENTADA` | El supervisor distingue si la consulta modifica el expediente. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106) |
| S-T2 | accion | `SUSTENTADA` | El supervisor absuelve y anota en el cuaderno. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-188.1` (p. 104) |
| S-E2 | existencia | `INFERENCIA` | S-E2 (inicio). | — |
| S-T0 | existencia | `INFERENCIA` | Identificar consulta propia (tarea). | — |
| S-G2 | existencia | `INFERENCIA` | ¿Especialista? (compuerta). | — |
| S-T3 | existencia | `INFERENCIA` | Elaborar informe tecnico de especialidad (tarea). | — |
| S-G3 | existencia | `INFERENCIA` | S-G3 (compuerta). | — |
| S-T4 | plazo | `SUSTENTADA` | El supervisor eleva la consulta con su opinión a la entidad. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| S-F1 | entrada-salida | `SUSTENTADA` | La consulta queda elevada a la entidad. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| S-T5 | existencia | `INFERENCIA` | Comunicar la respuesta al ejecutor (tarea). | — |
| S-F2 | existencia | `INFERENCIA` | Respuesta comunicada al ejecutor (fin-mensaje). | — |
| E-E1 | actor | `SUSTENTADA` | Mesa de Partes (OACGD) recibe la consulta. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-T1 | accion | `SUSTENTADA` | La OACGD registra y deriva la consulta a la SGGOS por el SGD. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-T2 | existencia | `INFERENCIA` | Recibir consulta y derivarla al monitor por SGD (tarea-usuario). | — |
| E-T3 | existencia | `INFERENCIA` | Revisar antecedentes y preparar tramite a la SGE (tarea). | — |
| E-T4 | actor | `SUSTENTADA` | La Sub Gerencia de Estudios evalúa la consulta. | reglamento-organizacion-funciones-grh-2023 `art-96` (p. 47) |
| E-G1 | decision | `SUSTENTADA` | Se decide si la consulta se remite al proyectista. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| E-T5 | documento | `SUSTENTADA` | Se prepara la solicitud de opinión al proyectista. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106)<br>reglamento-organizacion-funciones-grh-2023 `art-96` (p. 47) |
| E-T6 | plazo | `SUSTENTADA` | La consulta se remite al proyectista al día siguiente. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| E-G2 | decision | `SUSTENTADA` | Se espera la opinión o el vencimiento del plazo del proyectista. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| E-M1 | entrada-salida | `SUSTENTADA` | Se recibe la opinión del proyectista. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| E-R1 | plazo | `SUSTENTADA` | Vence el plazo de 10 días del proyectista. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| E-T7 | accion | `SUSTENTADA` | La Sub Gerencia de Estudios evalúa la opinión del proyectista. | reglamento-organizacion-funciones-grh-2023 `art-96` (p. 47)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| E-T8 | plazo | `SUSTENTADA` | Se elabora el informe de absolución en 5 días. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106)<br>reglamento-organizacion-funciones-grh-2023 `art-96` (p. 47) |
| E-T9 | existencia | `INFERENCIA` | Revisar y firmar la respuesta a la consulta (tarea-usuario). | — |
| E-G3 | existencia | `INFERENCIA` | ¿Identifica modificacion? (compuerta). | — |
| E-T10 | entrada-salida | `INFERENCIA` | Si se identifica una modificación, se comunica la causal a la SGGOS. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.4` (p. 106) |
| E-G4 | existencia | `INFERENCIA` | E-G4 (compuerta). | — |
| E-T11 | existencia | `INFERENCIA` | Notificar respuesta firmada a la SGGOS (tarea-usuario). | — |
| E-F1 | entrada-salida | `SUSTENTADA` | La respuesta se comunica al contratista. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| P-E1 | entrada-salida | `SUSTENTADA` | El proyectista recibe la solicitud. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.6` (p. 106) |
| P-T1 | accion | `SUSTENTADA` | El proyectista evalúa la consulta. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.6` (p. 106) |
| P-T2 | plazo | `SUSTENTADA` | El proyectista remite su opinión en 10 días. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-190.6` (p. 106) |
| P-F1 | entrada-salida | `SUSTENTADA` | La opinión del proyectista queda remitida. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| S-G5 | existencia | `INFERENCIA` | ¿Requiere opinion especializada? (compuerta). | — |
| S-T6 | existencia | `INFERENCIA` | Revisar consulta y emitir pronunciamiento (tarea). | — |
| S-T7 | existencia | `INFERENCIA` | Hacer suyo el pronunciamiento del especialista (tarea). | — |
| E-T12 | existencia | `INFERENCIA` | Tramitar consulta a la SGE por SGD (tarea-usuario). | — |
| E-T13 | existencia | `INFERENCIA` | Preparar carta e indicar quien elabora el adicional segun bases, si corresponde (tarea). | — |
| E-T14 | existencia | `INFERENCIA` | Revisar y emitir carta al contratista (tarea). | — |
| C-E3 | existencia | `INFERENCIA` | Carta de respuesta de la SGGOS recibida (inicio-mensaje). | — |
| S-G6 | condicion | `SUSTENTADA` | Si modifica el expediente, se verifica que adjunte el informe del contratista. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.2` (p. 106) |
| S-F3 | excepcion | `SUSTENTADA` | Sin el informe, la consulta no se atiende. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.2` (p. 106) |
| E-G5 | condicion | `SUSTENTADA` | La SGGOS verifica que la consulta traiga el informe exigido. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.2` (p. 106) |
| E-F2 | excepcion | `SUSTENTADA` | Sin el informe exigido, la consulta no se atiende. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.2` (p. 106) |
| S-T8 | documento | `SUSTENTADA` | El supervisor emite su informe técnico (opinión). | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| M:C-F1>S-E1 | entrada-salida | `SUSTENTADA` | La consulta e informe llegan al supervisor. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106) |
| M:S-T5>C-E2 | entrada-salida | `INFERENCIA` | Respuesta a la consulta (mensaje). | — |
| M:S-F1>E-E1 | entrada-salida | `SUSTENTADA` | La consulta y los informes llegan a la entidad. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| M:E-T6>P-E1 | entrada-salida | `SUSTENTADA` | La solicitud de opinión llega al proyectista. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| M:P-F1>E-M1 | entrada-salida | `SUSTENTADA` | La opinión llega a la entidad. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| M:E-F1>C-E3 | entrada-salida | `INFERENCIA` | Carta de respuesta al contratista (mensaje). | — |
| M:E-F1>S4.3.2.3 Gestion de adicionales y deductivos de obra | entrada-salida | `INFERENCIA` | La respuesta a la consulta pasa como antecedente a S4.3.2.3 cuando identifica un adicional. | — |

## Contradicciones

Ninguna.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **C-G2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Convergencia de rutas.
- **C-E2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Flujo Bizagi y precision operativa del equipo.
- **C-T3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Cierre operativo de la consulta.
- **C-F2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto del proceso.
- **S-T1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Flujo Bizagi; Reglamento, art. 190.
- **S-E2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Consulta originada por la supervision; precision operativa del equipo.
- **S-T0 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del equipo.
- **S-G2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del equipo.
- **S-T3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del equipo.
- **S-G3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Convergencia de rutas.
- **S-T5 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-17.
- **S-F2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto del proceso.
- **E-T2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-17.
- **E-T3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Tramite del monitor descrito parcialmente por el usuario, 2026-11-17; documento proyectado pendiente de precisar.
- **E-T9 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del equipo; DEC-033.
- **E-G3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Flujo Bizagi; separacion adoptada en DEC-032.
- **E-T10 · entrada-salida.** Derivación a S4.3.2.3-S4.3.2.6 (DEC-041) sin mensaje hacia esos procesos. Falta además la consecuencia del 190.4: sin absolución, el contratista puede pedir ampliación de plazo (S4.3.2.4).
- **E-G4 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Convergencia de rutas.
- **E-T11 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-17.
- **S-G5 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-17.
- **S-T6 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-17.
- **S-T7 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-17.
- **E-T12 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-17.
- **E-T13 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Secuencia inferida de la instruccion del usuario, 2026-11-17; confirmar alcance de «el monitor proyecta».
- **E-T14 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Secuencia inferida de la instruccion del usuario, 2026-11-17.
- **C-E3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-17.
- **M:S-T5>C-E2 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-F1>C-E3 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-F1>S4.3.2.3 Gestion de adicionales y deductivos de obra · entrada-salida.** Interfaz recíproca con S4.3.2.3 (R-E1); opinión D000083 citada en S4.3.2.3.

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| El contratista consulta mediante el cuaderno | `REPRESENTADO` | C-E1, C-T2 | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106) |
| El supervisor responde directamente si no se modifica el expediente | `REPRESENTADO` | S-G1, S-T2 | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106) |
| Informe técnico obligatorio cuando hay modificación; sin él no se atiende | `REPRESENTADO` | C-G1, C-T1, S-G6, S-F3, E-G5, E-F2 | reglamento-de-la-ley-general-de-contrataciones-p `art-190.2` (p. 106) |
| El supervisor eleva consulta y opinión en 5 días | `REPRESENTADO` | S-T8, S-T4, S-F1 | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| Remisión al proyectista al día siguiente si no pasó más de un año de la conformidad | `REPRESENTADO` | E-G1, E-T6 | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| Opinión del proyectista en 10 días | `REPRESENTADO` | E-R1, P-T2 | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| La entidad absuelve en 5 días desde la opinión o el vencimiento | `REPRESENTADO` | E-T8 | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| Diseño y construcción: la opinión del proyectista se integra al informe del contratista | `FUERA-DE-ALCANCE` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-190.3` (p. 106) |
| Sin absolución, el contratista puede pedir ampliación de plazo | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-190.4` (p. 106) |
| El contratista debe consultar con anticipación suficiente | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-190.5` (p. 106) |
| El proyectista debe atender las consultas según su contrato | `REPRESENTADO` | P-T1, P-T2 | reglamento-de-la-ley-general-de-contrataciones-p `art-190.6` (p. 106) |
| La Sub Gerencia de Estudios absuelve las consultas de obra | `REPRESENTADO` | C:Gobierno Regional Huanuco/SGE — Especialistas tecnicos | reglamento-organizacion-funciones-grh-2023 `art-96` (p. 47) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 0.
- Obligaciones de la fuente no representadas: 2.
- Anclas del visor: {'VIGENTE': 41}.
