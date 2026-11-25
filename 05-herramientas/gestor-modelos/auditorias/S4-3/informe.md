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

# Informe de auditoría S4.3

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `BCCC169B7ECF1242`. Afirmaciones vigentes: 11 (INFERENCIA: 5, SUSTENTADA: 6).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| C:S4.3 Ejecución de la inversión/Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | actor | `SUSTENTADA` | La Sub Gerencia de Gestión de Obras y Supervisión y las unidades ejecutoras del GRH son responsables de S4.3. | s4-gestion-inversion `p2` (p. 2) |
| E-1 | existencia | `INFERENCIA` | El proceso tiene un inicio genérico. | — |
| S-1 | entrada-salida | `INFERENCIA` | S4.3.1 entrega un acta de inicio de obra a S4.3.2. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| S-1 | existencia | `INFERENCIA` | S4.3 empieza con el inicio de ejecución (S4.3.1). | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93) |
| S-2 | entrada-salida | `INFERENCIA` | La ejecución termina con la obra concluida o con el contrato resuelto. | — |
| S-2 | secuencia | `SUSTENTADA` | La ejecución sigue al inicio y precede a la recepción. | reglamento-de-la-ley-general-de-contrataciones-p `art-176.1` (p. 93)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-212.1` (p. 120) |
| S-3 | existencia | `SUSTENTADA` | La recepción es una etapa propia tras la ejecución. | reglamento-de-la-ley-general-de-contrataciones-p `art-212.1` (p. 120) |
| F-1 | existencia | `INFERENCIA` | El proceso termina con la obra recepcionada. | — |
| M:S4.2 Elaboración del expediente técnico o documento equivalente>S-1 | entrada-salida | `SUSTENTADA` | S4.2 entrega a S4.3 el expediente técnico o documento equivalente. | s4-gestion-inversion `p2` (p. 2) |
| M:S3.2 Contratación de bienes y servicios (Adquisiciones)>S-1 | entrada-salida | `SUSTENTADA` | S3.2 entrega a S4.3 el contrato de ejecución. | s4-gestion-inversion `p2` (p. 2) |
| M:S-3>S4.4 Liquidación, transferencia y cierre de inversión | entrada-salida | `SUSTENTADA` | S4.3 entrega a S4.4 la información técnica y financiera para la liquidación. | s4-gestion-inversion `p2` (p. 2) |

## Contradicciones

Ninguna.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **E-1 · existencia.** Evento de modelamiento; las entradas reales llegan como mensajes a S-1.
- **S-1 · existencia.** DEC-028 separa la etapa previa al inicio; el 176.1 confirma que en contrata el plazo depende de condiciones previas. La etapa equivalente en administración directa no está modelada.
- **S-1 · entrada-salida.** Práctica institucional informada por el usuario el 2026-11-24: en obras por contrata, el GORE Huánuco formaliza con un acta de inicio que se cumplieron las condiciones del art. 176.1, para que la fecha de inicio no dependa de una apreciación subjetiva. La ley no exige el acta, pero tampoco la contradice: el acta documenta el hecho del que depende el inicio del plazo. Queda pendiente que S4.3.1 la represente: hoy termina en «Inicio del plazo comunicado».
- **S-2 · entrada-salida.** Salidas definidas por DEC-030/DEC-041; S4.3.2 también contempla la nulidad, que la salida del padre no nombra.
- **F-1 · existencia.** Cierre de modelamiento; los casos de contrato resuelto o nulo sin recepción no tienen fin propio en el padre.

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| Responsable: SGGOS y unidades ejecutoras | `REPRESENTADO` | C:S4.3 Ejecución de la inversión/Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | s4-gestion-inversion `p2` (p. 2) |
| Entrada: expediente técnico desde S4.2 | `REPRESENTADO` | M:S4.2 Elaboración del expediente técnico o documento equivalente>S-1 | s4-gestion-inversion `p2` (p. 2) |
| Entrada: bien, servicio, consultoría u obra contratada desde S3.2 | `REPRESENTADO` | M:S3.2 Contratación de bienes y servicios (Adquisiciones)>S-1 | s4-gestion-inversion `p2` (p. 2) |
| Entrada: convenios desde gobiernos nacional, regional y local | `NO-REPRESENTADO` | — | s4-gestion-inversion `p2` (p. 2) |
| Producto: designación de personal o requerimiento de contratación hacia S3.1 | `NO-REPRESENTADO` | — | s4-gestion-inversion `p2` (p. 2) |
| Producto: reporte de inversiones ejecutadas al MEF / INFOBRAS | `NO-REPRESENTADO` | — | s4-gestion-inversion `p2` (p. 2) |
| Producto: expediente para pagos hacia S2.1 | `NO-REPRESENTADO` | — | s4-gestion-inversion `p2` (p. 2) |
| Producto: información para liquidación hacia S4.4 | `REPRESENTADO` | M:S-3>S4.4 Liquidación, transferencia y cierre de inversión | s4-gestion-inversion `p2` (p. 2) |
| Producto: informe de estado situacional por saldo de obra hacia S4.2 | `NO-REPRESENTADO` | — | s4-gestion-inversion `p2` (p. 2) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 0.
- Obligaciones de la fuente no representadas: 5.
- Anclas del visor: {}.
