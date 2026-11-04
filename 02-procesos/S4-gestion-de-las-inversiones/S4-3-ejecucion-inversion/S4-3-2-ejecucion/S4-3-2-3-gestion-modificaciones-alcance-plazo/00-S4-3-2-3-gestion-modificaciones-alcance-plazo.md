---
tipo: mapa-de-contenido
area: S4-3-2-3-gestion-modificaciones-alcance-plazo
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
codigo_proceso: S4.3.2.3
nivel_proceso: 3
proceso_padre: S4.3.2
alcance_proyecto: EN-ALCANCE
aliases:
  - S4.3.2.3 Gestion de modificaciones de alcance o plazo
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-3
---

# S4.3.2.3 Gestion de modificaciones de alcance o plazo

Sube a: [S4.3.2 Ejecucion](../00-S4-3-2-ejecucion.md)

Proceso de nivel 3 adoptado mediante `DEC-032`. Agrupa el tratamiento comun de las modificaciones que pueden surgir durante la ejecucion; sus variantes no reciben codigos de nivel 4 en esta etapa.

## Ubicacion

Mapa de procesos institucional > S4 Gestion de las inversiones > S4.3 Ejecucion de la inversion > S4.3.2 Ejecucion > **S4.3.2.3 Gestion de modificaciones de alcance o plazo** (Nivel 3).

## Que hace

Gestiona una instancia por cada solicitud, necesidad o causal registrada en obra. El residente y el supervisor o inspector participan como roles comunes con independencia de la modalidad. Cuando el expediente ingresa al GORE, el monitor controla integridad, clasificacion y trazabilidad sin reemplazar la evaluacion especializada; el control contractual distingue una obligacion original de una modificacion potencial; el elaborador definido o designado desarrolla la solucion; SGE obtiene una revision tecnica competente e independiente; y la autoridad que corresponda decide segun regimen, figura, umbral y delegacion.

La propuesta no usa un unico circuito de aprobacion. Adicionales, reducciones, mayores metrados, ampliaciones, suspensiones e intensificacion tienen reglas y productos diferentes. Tampoco trata la revision institucional como una repeticion de la supervision: separa necesidad en campo, elaboracion, revision tecnica independiente, control contractual y de costos, consolidacion y decision. El [sustento](S4-3-2-3-sustento.md) contiene la matriz normativa, las responsabilidades, los controles frente a una evaluacion deficiente y las discrepancias frente al Bizagi observado.

## Interacciones

| Sentido | Contraparte | Elemento observado |
|---|---|---|
| Recibe | S4.3.2.2 Atencion de consultas de obra | Respuesta que origina una solicitud o causal de modificacion |
| Recibe | Residente y supervisor o inspector de obra | Asiento en el cuaderno, solicitud, necesidad o causal e informe tecnico |
| Tramita con | OACGD, monitor o gestor, control contractual y costos, SGE, Presupuesto, GRAJ, GRI y autoridad competente | Registro, clasificacion, controles independientes y decision segun la figura |
| Solicita a | Elaborador definido en las bases o designado por la OAD | Expediente tecnico de la modificacion cuando la figura lo requiere |
| Solicita | Contraloria General de la Republica | Autorizacion previa solo cuando la Ley 32069 la exige |
| Envia | Participantes de la ejecucion | Decision favorable, improcedencia o denegacion comunicada |
| Registra | Banco de Inversiones, INFOBRAS o Pladicop | Actualizacion en el sistema y oportunidad que correspondan |

## Documentos del proceso

| Documento | Archivo | Estado |
|---|---|---|
| Ficha de producto y proceso | [S4-3-2-3-ficha-producto-proceso.md](S4-3-2-3-ficha-producto-proceso.md) | `PROPUESTA` en `ELABORACION` |
| Fichas de indicador | [S4-3-2-3-fichas-indicador.md](S4-3-2-3-fichas-indicador.md) | `EVIDENCIA-INSUFICIENTE` |
| Diagrama del proceso | Fuente [S4-3-2-3-diagrama-proceso-tabla.md](S4-3-2-3-diagrama-proceso-tabla.md); genera BPMN, SVG, PNG y HTML | `PROPUESTA` en `ELABORACION` |
| Sustento | [S4-3-2-3-sustento.md](S4-3-2-3-sustento.md) | Vigente para trazabilidad |
| Procedimiento | No creado | Pendiente determinar si el flujo comun o alguna variante cumple los criterios del numeral 6.1.3 d de la NT |

## Variantes internas sin codigo de proceso

| ID de modelamiento | Variante |
|---|---|
| `MOD-ALC-ADI` | Adicional o modificacion tecnica, con regla diferenciada por regimen |
| `MOD-ALC-RED` | Reduccion o deductivo, con regla diferenciada por regimen |
| `MOD-ALC-MAY` | Mayores metrados o cantidades, con regla diferenciada por regimen |
| `MOD-PLA-AMP` | Ampliacion de plazo |
| `MOD-PLA-SUS` | Suspension, paralizacion o reinicio |
| `MOD-PLA-INT` | Intensificacion del programa; aplicabilidad pendiente fuera del regimen contractual |

## Pendientes

- Identificar la autoridad de la gestion administrativa y las delegaciones vigentes del GORE para cada figura.
- Validar la unidad que remite formalmente solicitudes a la Contraloria y los documentos del expediente.
- Confirmar por variante cuando intervienen SGE, Presupuesto y GRAJ.
- Definir la unidad y los perfiles responsables del control contractual y de costos y aprobar su matriz de revision por modalidad de pago.
- Definir como se obtiene un especialista competente e independiente cuando SGE no dispone de la especialidad requerida.
- Validar la segregacion propuesta entre elaborador, revisor tecnico, controles complementarios, consolidacion y decisor.
- Resolver la relacion entre el registro previo de Invierte.pe y los mayores metrados autorizados por la supervision.
- Definir la interfaz posterior con el proceso de abastecimiento cuando una modificacion aprobada en administracion directa cambia los bienes o servicios requeridos.
- Decidir si intensificacion, cambio de ingenieria de valor y modificaciones por hechos sobrevinientes quedan dentro del alcance.
- Desarrollar el flujo interno de cada variante solo con evidencia suficiente.

## Relaciones

- [S4.3.2.2 Atencion de consultas](../S4-3-2-2-atencion-consultas-obra/00-S4-3-2-2-atencion-consultas-obra.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)
- [Guia del Reglamento de la Ley 32069](../../../../../03-conocimiento/fuentes/guia-reglamento-ley-32069.md)
- [Guia del ROF del Gobierno Regional Huanuco](../../../../../03-conocimiento/fuentes/guia-rof-grh-2023.md)
- [Modelo Bizagi de Consultas](../../../../../99-temporal/modelos/sggos-2026-11-02-bpmn/consultas-bizagi.bpmn)

