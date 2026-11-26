---
tipo: informe
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
fecha_actualizacion: 2026-11-26
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Informe de auditoría S4.3.2

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3.2`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `F0F27A5E72CE1D1C`. Afirmaciones vigentes: 22 (INFERENCIA: 7, NO-APLICA: 2, SUSTENTADA: 13).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| C:S4.3.2 Ejecucion/Ejecucion, control y gestion institucional de la obra | actor | `INFERENCIA` | Un solo carril agrupa ejecución, control y gestión institucional de la obra. | — |
| E-1 | entrada-salida | `INFERENCIA` | La ejecución empieza al recibir el acta de inicio de obra. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| T-1 | accion | `SUSTENTADA` | La ejecución registra sus ocurrencias en el cuaderno de incidencias. | reglamento-de-la-ley-general-de-contrataciones-p `art-188.1` (p. 104) |
| F-1 | secuencia | `SUSTENTADA` | La obra culminada pasa a recepción. | reglamento-de-la-ley-general-de-contrataciones-p `art-212.1` (p. 120) |
| B-1 | condicion | `SUSTENTADA` | La resolución del contrato interrumpe la ejecución. | reglamento-de-la-ley-general-de-contrataciones-p `art-122.1` (p. 66, 67)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-123.4` (p. 67, 68) |
| B-2 | condicion | `SUSTENTADA` | La declaración de nulidad interrumpe la ejecución. | ley-general-de-contrataciones-publicas-con-modif `art-71.1` (p. 35)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-111.1` (p. 61) |
| F-2 | entrada-salida | `SUSTENTADA` | Tras la resolución se realiza la constatación física e inventario. | reglamento-de-la-ley-general-de-contrataciones-p `art-123.4` (p. 67, 68)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-122.1` (p. 66, 67) |
| F-3 | entrada-salida | `NO-APLICA` | El tratamiento posterior a la nulidad está por definir. | — |
| F-3 | entrada-salida | `SUSTENTADA` | Tras la nulidad no atribuible al contratista corresponden la constatación física y el inventario; si es atribuible, el 111.3 no fija tratamiento. | reglamento-de-la-ley-general-de-contrataciones-p `art-111.3` (p. 61)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-111.2` (p. 61) |
| CP | decision | `SUSTENTADA` | El control periódico se dispara al cierre de cada mes. | reglamento-de-la-ley-general-de-contrataciones-p `art-210.1` (p. 118) |
| CO | decision | `SUSTENTADA` | La atención de consultas se dispara por una consulta registrada en el cuaderno. | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106) |
| MA | existencia | `INFERENCIA` | Los adicionales y deductivos se gestionan como proceso por evento. | — |
| AP | existencia | `SUSTENTADA` | Las ampliaciones de plazo se gestionan por causal o solicitud. | reglamento-de-la-ley-general-de-contrataciones-p `art-198.1` (p. 112, 113)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-200.1` (p. 114)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-201.1` (p. 114) |
| SP | existencia | `SUSTENTADA` | Las suspensiones del plazo se formalizan por evento. | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-202.1` (p. 114, 115) |
| PR | existencia | `INFERENCIA` | La paralización y el reinicio tienen tratamiento diferenciado por régimen. | — |
| RP | decision | `INFERENCIA` | La reducción de prestaciones se dispara por una condición. | — |
| MM | existencia | `INFERENCIA` | Los mayores metrados se gestionan como proceso por evento. | — |
| M:S4.3.1 Inicio de ejecucion>E-1 | entrada-salida | `INFERENCIA` | S4.3.1 envía el acta de inicio de obra. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| M:F-1>S4.3.3 Recepcion | entrada-salida | `SUSTENTADA` | La obra culminada se entrega a recepción. | reglamento-de-la-ley-general-de-contrataciones-p `art-212.1` (p. 120) |
| M:F-2>S4.3.3 Recepcion | entrada-salida | `SUSTENTADA` | El contrato resuelto pasa a constatación e inventario. | reglamento-de-la-ley-general-de-contrataciones-p `art-123.4` (p. 67, 68) |
| M:F-3>S4.3.3 Recepcion | entrada-salida | `NO-APLICA` | El contrato nulo pasa a recepción con tratamiento por definir. | — |
| M:F-3>S4.3.3 Recepcion | entrada-salida | `SUSTENTADA` | El contrato nulo pasa a S4.3.3 para constatación física e inventario. | reglamento-de-la-ley-general-de-contrataciones-p `art-111.3` (p. 61) |

## Contradicciones

Ninguna.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **C:S4.3.2 Ejecucion/Ejecucion, control y gestion institucional de la obra · actor.** Simplificación del nivel 2 (DEC-030); los actores se detallan en los hijos (DEC-042).
- **E-1 · entrada-salida.** Práctica institucional informada por el usuario el 2026-11-24: en obras por contrata, el GORE Huánuco formaliza con un acta de inicio que se cumplieron las condiciones del art. 176.1, para que la fecha de inicio no dependa de una apreciación subjetiva. La ley no exige el acta, pero tampoco la contradice: el acta documenta el hecho del que depende el inicio del plazo. En administración directa el acta también aparece en la Directiva 017-2023-CG.
- **MA · existencia.** DEC-047; su sustento se audita en S4.3.2.3.
- **PR · existencia.** Apoyado en reglas BORRADOR-IA del sustento; se audita en S4.3.2.6.
- **RP · decision.** Candidato de interfaz: S4.3.2.7 empieza por mensaje («Necesidad de reducción recibida») y además recibe casos reclasificados desde S4.3.2.3. Debe alinearse el tipo de disparo.
- **MM · existencia.** DEC-047; su sustento se audita en S4.3.2.8.
- **M:S4.3.1 Inicio de ejecucion>E-1 · entrada-salida.** Práctica institucional informada por el usuario el 2026-11-24: en obras por contrata, el GORE Huánuco formaliza con un acta de inicio que se cumplieron las condiciones del art. 176.1, para que la fecha de inicio no dependa de una apreciación subjetiva. La ley no exige el acta, pero tampoco la contradice: el acta documenta el hecho del que depende el inicio del plazo. S4.3.1 aún no registra este envío (candidato de interfaz).

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| El plazo de ejecución rige al cumplirse las condiciones de inicio | `REPRESENTADO` | E-1, M:S4.3.1 Inicio de ejecucion>E-1 | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| Las ocurrencias se registran en el cuaderno de incidencias | `REPRESENTADO` | T-1 | reglamento-de-la-ley-general-de-contrataciones-p `art-188.1` (p. 104) |
| Las consultas se formulan mediante el cuaderno de incidencias | `REPRESENTADO` | CO | reglamento-de-la-ley-general-de-contrataciones-p `art-190.1` (p. 106) |
| Valorizaciones mensuales o en el periodo que fijen las bases | `REPRESENTADO` | CP | reglamento-de-la-ley-general-de-contrataciones-p `art-210.1` (p. 118) |
| La recepción sigue a la culminación | `REPRESENTADO` | F-1, M:F-1>S4.3.3 Recepcion | reglamento-de-la-ley-general-de-contrataciones-p `art-212.1` (p. 120) |
| La resolución sigue su procedimiento | `REPRESENTADO` | B-1 | reglamento-de-la-ley-general-de-contrataciones-p `art-122.1` (p. 66, 67) |
| Tras la resolución, constatación física e inventario | `REPRESENTADO` | F-2, M:F-2>S4.3.3 Recepcion | reglamento-de-la-ley-general-de-contrataciones-p `art-123.4` (p. 67, 68) |
| La autoridad de la gestión administrativa puede declarar la nulidad | `REPRESENTADO` | B-2 | ley-general-de-contrataciones-publicas-con-modif `art-71.1` (p. 35) |
| Tras la nulidad no atribuible al contratista, constatación física e inventario | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-111.3` (p. 61) |
| El contratista puede solicitar ampliación por causales | `REPRESENTADO` | AP | reglamento-de-la-ley-general-de-contrataciones-p `art-198.1` (p. 112, 113) |
| Las partes pueden acordar la suspensión del plazo | `REPRESENTADO` | SP | reglamento-de-la-ley-general-de-contrataciones-p `art-107.1` (p. 59) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 0.
- Obligaciones de la fuente no representadas: 1.
- Anclas del visor: {'VIGENTE': 18}.
