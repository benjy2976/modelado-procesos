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

# Informe de auditoría S4.3.2.3

Sube a: [Plan de corrida documental y auditoría](../../docs/plan-corrida-documental-y-auditoria.md).

Generado por `modelador-procesos auditoria informe S4.3.2.3`; no editar a mano. Los resultados son propuestas
del agente que registró cada afirmación: no constituyen validación normativa ni conformidad institucional.

Revisión de la tabla: `4B27170A34348F86`. Afirmaciones vigentes: 97 (INFERENCIA: 66, SUSTENTADA: 31).

## Afirmaciones por elemento

| Elemento | Aspecto | Resultado | Afirmación | Fuentes |
|---|---|---|---|---|
| R-E1 | existencia | `INFERENCIA` | Respuesta de consulta recibida (inicio-mensaje). | — |
| R-T1 | documento | `SUSTENTADA` | El residente anota la necesidad del adicional en el cuaderno. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-188.1` (p. 104) |
| R-F1 | existencia | `INFERENCIA` | Anotacion y antecedentes remitidos (fin-mensaje). | — |
| S-E1 | existencia | `INFERENCIA` | Sustento del residente recibido (inicio-mensaje). | — |
| S-E2 | existencia | `INFERENCIA` | Necesidad identificada por supervision (inicio-condicional). | — |
| S-T0 | documento | `SUSTENTADA` | La supervisión registra la necesidad en el cuaderno. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| S-G1 | existencia | `INFERENCIA` | S-G1 (compuerta). | — |
| S-T1 | plazo | `SUSTENTADA` | El supervisor sustenta su posición técnica sobre necesidad y riesgo en 5 días. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| S-G2 | decision | `SUSTENTADA` | El supervisor ratifica o no la necesidad. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| S-F1 | entrada-salida | `SUSTENTADA` | La necesidad ratificada se remite a la entidad. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| S-F2 | existencia | `INFERENCIA` | Necesidad no ratificada (fin). | — |
| E-E1 | actor | `SUSTENTADA` | La OACGD recibe el sustento. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-T1 | accion | `SUSTENTADA` | La OACGD registra y deriva por el SGD. | reglamento-organizacion-funciones-grh-2023 `art-20` (p. 14) |
| E-TSG | existencia | `INFERENCIA` | Recibir sustento y derivarlo al coordinador por SGD (tarea-usuario). | — |
| E-T2 | accion | `INFERENCIA` | El coordinador verifica integridad, régimen, sistema de entrega y supervisión. | reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49)<br>reglamento-organizacion-funciones-grh-2023 `art-97` (p. 47, 48, 49) |
| E-T3 | existencia | `INFERENCIA` | Clasificar alcance original, causal y figura inicial (tarea). | — |
| E-G0 | existencia | `INFERENCIA` | ¿Corresponde adicional o deductivo de obra? (compuerta). | — |
| E-T15 | existencia | `INFERENCIA` | Comunicar clasificacion y proceso de destino (tarea-usuario). | — |
| E-F3 | existencia | `INFERENCIA` | Caso clasificado fuera del proceso (fin-mensaje). | — |
| E-G2 | existencia | `INFERENCIA` | ¿Que caso corresponde? (compuerta). | — |
| MOD-ALC-ADI | decision | `SUSTENTADA` | Se identifica un adicional sin deductivo vinculado. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.1` (p. 109)<br>ley-general-de-contrataciones-publicas-con-modif `art-64.2` (p. 31) |
| E-G6 | condicion | `SUSTENTADA` | Se acreditan la necesidad ratificada, la causal y el elaborador. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.1` (p. 109)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-T4 | condicion | `SUSTENTADA` | Se comunica la ratificación a quien elabora el expediente. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-M2 | existencia | `INFERENCIA` | Expediente del adicional presentado a evaluacion (mensaje-recepcion). | — |
| E-T5A | actor | `SUSTENTADA` | Se determina quién emite la opinión técnica previa. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-T5 | accion | `SUSTENTADA` | El órgano competente emite opinión técnica. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-G7 | existencia | `INFERENCIA` | ¿Evaluacion tecnica favorable? (compuerta). | — |
| E-TINF | existencia | `INFERENCIA` | Elaborar informe de evaluacion tecnica favorable (tarea-usuario). | — |
| E-T16 | existencia | `INFERENCIA` | Integrar observaciones para decision (tarea-usuario). | — |
| E-TNEV | existencia | `INFERENCIA` | Comunicar evaluacion tecnica (mensaje-envio). | — |
| E-G5 | existencia | `INFERENCIA` | ¿Que controles requiere? (compuerta-inclusiva). | — |
| E-TC | accion | `SUSTENTADA` | El control contractual verifica monto, precios, deductivo vinculado y acumulado. | ley-general-de-contrataciones-publicas-con-modif `art-64.2` (p. 31)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-194.5` (p. 110) |
| E-T6 | actor | `SUSTENTADA` | La Subgerencia de Presupuesto emite certificación o previsión. | reglamento-organizacion-funciones-grh-2023 `art-51` (p. 26, 27) |
| E-T7 | actor | `SUSTENTADA` | Asesoría Jurídica emite opinión o revisa el acto. | reglamento-organizacion-funciones-grh-2023 `art-45-parte1` (p. 24, 25, 26)<br>reglamento-organizacion-funciones-grh-2023 `art-44` (p. 24) |
| E-G5C | existencia | `INFERENCIA` | E-G5C (compuerta-inclusiva). | — |
| E-T17 | existencia | `INFERENCIA` | Consolidar controles, responsables y discrepancias resueltas (tarea-usuario). | — |
| E-G8 | decision | `SUSTENTADA` | Se verifica si se requiere autorización previa de la Contraloría (más de 30 % y hasta 50 %). | ley-general-de-contrataciones-publicas-con-modif `art-64.3` (p. 31)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-194.5` (p. 110) |
| E-T8 | accion | `SUSTENTADA` | Se solicita autorización a la Contraloría. | ley-general-de-contrataciones-publicas-con-modif `art-64.3` (p. 31) |
| E-M1 | plazo | `SUSTENTADA` | Se recibe el pronunciamiento de la Contraloría. | ley-general-de-contrataciones-publicas-con-modif `art-64.4` (p. 31) |
| E-G9 | decision | `SUSTENTADA` | Se distingue si la Contraloría autorizó. | ley-general-de-contrataciones-publicas-con-modif `art-64.4` (p. 31) |
| E-F2B | existencia | `INFERENCIA` | No autorizacion comunicada (fin-mensaje). | — |
| E-T10 | plazo | `SUSTENTADA` | El titular emite y notifica la resolución del adicional en 12 días hábiles. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.1` (p. 109)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-G10 | existencia | `INFERENCIA` | ¿Favorable? (compuerta). | — |
| E-T11 | documento | `INFERENCIA` | Se actualizan registros y la comunicación, con el canal de publicación por confirmar. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.3` (p. 110) |
| E-T11 | documento | `SUSTENTADA` | La aprobación se publica en la Pladicop, sin adenda, y no procede aprobar por regularización. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.3` (p. 110)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-194.3` (p. 110) |
| E-F1 | entrada-salida | `SUSTENTADA` | El proceso termina con la aprobación publicada. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.3` (p. 110) |
| E-F1 | existencia | `INFERENCIA` | Decision del adicional comunicada (fin-mensaje). | — |
| E-F2C | existencia | `INFERENCIA` | Decision no favorable comunicada (fin-mensaje). | — |
| X-E1 | existencia | `INFERENCIA` | Anotacion comunicada al elaborador (inicio-mensaje). | — |
| X-E2 | existencia | `INFERENCIA` | Anotacion propia conocida por elaborador (inicio-condicional). | — |
| X-TENC | existencia | `INFERENCIA` | Asumir encargo y organizar elaboracion del expediente (tarea-usuario). | — |
| X-T1 | plazo | `SUSTENTADA` | El elaborador presenta el expediente en 15 días desde la anotación. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| X-F1 | entrada-salida | `SUSTENTADA` | El expediente técnico queda presentado. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-GREG | decision | `INFERENCIA` | Solo sigue la ruta si es Ley 32069, solo construcción y sin emergencia. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.4` (p. 110) |
| E-FPEND | existencia | `INFERENCIA` | Caso pendiente de completar sustento o ruta especifica (fin). | — |
| E-FNEC | existencia | `INFERENCIA` | Necesidad o elaborador pendiente de acreditar (fin). | — |
| E-FDP | existencia | `INFERENCIA` | Deductivo puro pendiente de ruta (fin). | — |
| E-GEL | existencia | `INFERENCIA` | Identificar autor y ruta de evaluacion (tarea-usuario). | — |
| E-GPAR | existencia | `INFERENCIA` | ¿Que opiniones corresponden? (compuerta-inclusiva). | — |
| E-TSUP | existencia | `INFERENCIA` | Coordinar presentacion a supervision (mensaje-envio). | — |
| E-MSUP | existencia | `INFERENCIA` | Opinion de supervision recibida (mensaje-recepcion). | — |
| E-GJOIN | existencia | `INFERENCIA` | E-GJOIN (compuerta-inclusiva). | — |
| S-E3 | existencia | `INFERENCIA` | Expediente para evaluacion recibido (inicio-mensaje). | — |
| S-T3 | plazo | `SUSTENTADA` | La supervisión se pronuncia sobre el expediente del contratista en 10 días. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| S-F3 | entrada-salida | `SUSTENTADA` | La opinión de supervisión queda remitida. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| X-MR | existencia | `INFERENCIA` | Ratificacion comunicada para presentar (mensaje-recepcion). | — |
| E-ENOT | existencia | `INFERENCIA` | Anotacion comunicada a SGGOS (inicio-mensaje). | — |
| E-GNOT | decision | `SUSTENTADA` | Se verifica si el elaborador conoce la anotación. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-TNOT | accion | `SUSTENTADA` | Se avisa la anotación y el encargo al elaborador. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110)<br>reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-FNOT | existencia | `INFERENCIA` | Inicio comunicado o conocido (fin). | — |
| E-GPRO | condicion | `SUSTENTADA` | Corresponde opinión del proyectista si no pasó más de un año desde la conformidad. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-TPRO | accion | `SUSTENTADA` | Se solicita opinión al proyectista. | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| E-MPRO | existencia | `INFERENCIA` | Opinion del proyectista recibida (mensaje-recepcion). | — |
| E-GEX | existencia | `INFERENCIA` | ¿El expediente lo elaboro la entidad? (compuerta). | — |
| E-TEX | existencia | `INFERENCIA` | Documentar supuesto de opinion inoficiosa (tarea-usuario). | — |
| E-EDP | existencia | `INFERENCIA` | Sustento de deductivo puro recibido (inicio-mensaje). | — |
| E-TVIN | decision | `SUSTENTADA` | Se identifica el adicional con su deductivo vinculante. | ley-general-de-contrataciones-publicas-con-modif `art-64.2` (p. 31) |
| E-TDP | existencia | `INFERENCIA` | Precisar naturaleza y sustento del deductivo puro (tarea). | — |
| E-GDP | decision | `INFERENCIA` | Un deductivo puro se evalúa como posible reducción de prestaciones. | reglamento-de-la-ley-general-de-contrataciones-p `art-109.1` (p. 60) |
| E-FRED | entrada-salida | `INFERENCIA` | El caso se clasifica y se envía a S4.3.2.7. | reglamento-de-la-ley-general-de-contrataciones-p `art-109.1` (p. 60) |
| M:R-F1>S-E1 | entrada-salida | `INFERENCIA` | Sustento de necesidad (mensaje). | — |
| M:S-F1>E-E1 | entrada-salida | `INFERENCIA` | Necesidad ratificada (mensaje). | — |
| M:R-F1>E-ENOT | entrada-salida | `INFERENCIA` | Anotacion de necesidad comunicada a SGGOS (mensaje). | — |
| M:S-T0>E-ENOT | entrada-salida | `INFERENCIA` | Anotacion de supervision comunicada a SGGOS (mensaje). | — |
| M:E-TNOT>X-E1 | entrada-salida | `INFERENCIA` | Anotacion y encargo comunicados al elaborador distinto del anotante (mensaje). | — |
| M:E-T4>X-MR | entrada-salida | `INFERENCIA` | Ratificacion comunicada (mensaje). | — |
| M:X-F1>E-M2 | entrada-salida | `INFERENCIA` | Expediente tecnico (mensaje). | — |
| M:E-T8>Contraloria General de la Republica | entrada-salida | `INFERENCIA` | Solicitud de autorizacion (mensaje). | — |
| M:Contraloria General de la Republica>E-M1 | entrada-salida | `INFERENCIA` | Pronunciamiento (mensaje). | — |
| M:S4.3.2.2 Atencion de consultas de obra>R-E1 | entrada-salida | `INFERENCIA` | Respuesta notificada como antecedente (mensaje). | — |
| M:E-TSUP>S-E3 | entrada-salida | `INFERENCIA` | Expediente presentado para pronunciamiento (mensaje). | — |
| M:S-F3>E-MSUP | entrada-salida | `INFERENCIA` | Opinion de supervision (mensaje). | — |
| M:E-TNEV>Elaborador del adicional segun bases: entidad, contratista o supervisor | entrada-salida | `INFERENCIA` | Resultado de evaluacion tecnica preliminar (mensaje). | — |
| M:E-TNEV>Ejecutor de obra, segun regimen | entrada-salida | `INFERENCIA` | Resultado de evaluacion tecnica preliminar (mensaje). | — |
| M:E-TPRO>Proyectista | entrada-salida | `INFERENCIA` | Solicitud de opinion previa (mensaje). | — |
| M:Proyectista>E-MPRO | entrada-salida | `INFERENCIA` | Opinion tecnica (mensaje). | — |
| M:E-FRED>S4.3.2.7 Gestion de reducciones de prestaciones | entrada-salida | `INFERENCIA` | Sustento reclasificado como reduccion (mensaje). | — |

## Contradicciones

Ninguna.

## Evidencia insuficiente

Ninguna.

## Inferencias

- **R-E1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Usuario 2026-11-18; Opinion D000083, 2.2.1 y 3.3.
- **R-F1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, arts. 194.2 y 197.1; Directiva 017-2023-CG, num. 7.3.6.
- **S-E1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, arts. 186.1 y 194.2 b; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6.
- **S-E2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del equipo; Reglamento, arts. 186-188.
- **S-G1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Convergencia de origenes.
- **S-F2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Cierre propuesto para el control inicial.
- **E-TSG · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision institucional del usuario, 2026-11-19; circuito analogo documentado en S4.3.2.2.
- **E-T2 · accion.** Funciones de la SGGOS; la verificación concreta es propuesta (DEC-041).
- **E-T3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision del equipo registrada en DEC-041.
- **E-G0 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Separa obligacion original, valorizacion y modificacion potencial.
- **E-T15 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision institucional del usuario, 2026-11-19; DEC-041.
- **E-F3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Puede corresponder exigir cumplimiento, valorizar o derivar a otro proceso.
- **E-G2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047; tres casos solicitados por el usuario.
- **E-M2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, art. 194.2 d-f; Directiva 017-2023-CG, num. 7.3.6.
- **E-G7 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-20; DEC-038.
- **E-TINF · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision operativa del usuario, 2026-11-20; Reglamento, art. 194.2 g para opinion tecnica.
- **E-T16 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Propuesta operativa; Reglamento, art. 194.2 f; no sustituir resolucion por informe.
- **E-TNEV · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision del usuario, 2026-11-19; art. 194.2 e-g para secuencia de opiniones.
- **E-G5 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-038; control contractual obligatorio en esta propuesta.
- **E-G5C · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Convergencia de controles activados.
- **E-T17 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Matriz de control propuesta en DEC-038; no sustituye opiniones especializadas.
- **E-F2B · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Cierre cuando no se obtiene la autorizacion externa exigible.
- **E-G10 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Rutas de decision.
- **E-T11 · documento.** El 194.3 vigente fija la publicación en la Pladicop, sin adenda, y prohíbe aprobar adicionales por regularización; E-T11 deja el canal por confirmar y no recoge la prohibición.
- **E-F1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto propuesto; canal formal por confirmar.
- **E-F2C · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Producto alterno.
- **X-E1 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, art. 194.2 c-d; Opinion D000092, 2.1-2.3; interfaz S4.3.2.2.
- **X-E2 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, art. 194.2 a-d; precision del usuario, 2026-11-19.
- **X-TENC · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, art. 194.2 c-d; Opinion D000092, 2.1-2.3; respuesta S4.3.2.2.
- **E-GREG · decision.** La emergencia tiene procedimiento propio en el 194.4 (ejecución inmediata autorizada a la supervisión y regularización posterior) que el modelo deja pendiente.
- **E-FPEND · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-046; EVIDENCIA-INSUFICIENTE, no es decision de fondo.
- **E-FNEC · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Salida local de E-G6; no es decision de fondo.
- **E-FDP · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047; EVIDENCIA-INSUFICIENTE sobre ruta autonoma.
- **E-GEL · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, art. 194.2 c-g; Opinion D000092, 2.9 A-C y 3.9-3.11.
- **E-GPAR · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Reglamento, art. 194.2 e-g; Opinion D000092, 2.8-2.9.
- **E-TSUP · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Opinion D000092, 2.4 nota 5; 2.9 A y C.
- **E-MSUP · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-046.
- **E-GJOIN · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-046.
- **S-E3 · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Opinion D000092, 2.9 A y C.
- **X-MR · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Opinion D000092, 2.1 nota 4, 2.2-2.3.
- **E-ENOT · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Precision del usuario, 2026-11-19; Reglamento, art. 194.2 a-d.
- **E-FNOT · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Cierre del aviso operativo; no es aprobacion.
- **E-MPRO · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Opinion D000092, 2.8-2.9.
- **E-GEX · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Opinion D000092, 2.8-2.9.
- **E-TEX · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: Opinion D000092, 2.8-2.9.
- **E-EDP · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047.
- **E-TDP · existencia.** Paso operativo o de modelamiento; procedencia declarada en la tabla: DEC-047.
- **E-GDP · decision.** DEC-047; la distinción entre deductivo puro y reducción requiere evidencia técnica y contractual.
- **E-FRED · entrada-salida.** S4.3.2.7 no registra la recepción de este caso (candidato de interfaz).
- **M:R-F1>S-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:S-F1>E-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:R-F1>E-ENOT · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:S-T0>E-ENOT · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-TNOT>X-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-T4>X-MR · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:X-F1>E-M2 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-T8>Contraloria General de la Republica · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:Contraloria General de la Republica>E-M1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:S4.3.2.2 Atencion de consultas de obra>R-E1 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-TSUP>S-E3 · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:S-F3>E-MSUP · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-TNEV>Elaborador del adicional segun bases: entidad, contratista o supervisor · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-TNEV>Ejecutor de obra, segun regimen · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-TPRO>Proyectista · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:Proyectista>E-MPRO · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.
- **M:E-FRED>S4.3.2.7 Gestion de reducciones de prestaciones · entrada-salida.** Paso operativo o de modelamiento; procedencia declarada en la tabla: mensaje del modelo.

## Cobertura de la fuente

| Obligación de la fuente | Estado | Elementos | Fuente |
|---|---|---|---|
| Resolución previa por causal: deficiencias del expediente o causas no previsibles | `REPRESENTADO` | E-G6, MOD-ALC-ADI, E-T10 | reglamento-de-la-ley-general-de-contrataciones-p `art-194.1` (p. 109) |
| Anotación de la necesidad por residente o supervisión | `REPRESENTADO` | R-T1, S-T0 | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| Informe técnico del supervisor en 5 días | `REPRESENTADO` | S-T1 | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| Elaborador del expediente según bases | `REPRESENTADO` | E-GNOT, E-TNOT, E-G6 | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| Presentación en 15 días desde la anotación si hay ratificación; plazo adicional por complejidad | `REPRESENTADO` | X-T1, E-T4 | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| Pronunciamiento de supervisión en 10 días si elaboró el contratista | `REPRESENTADO` | S-T3 | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| Resolución notificada en 12 días hábiles | `REPRESENTADO` | E-T10 | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| Opinión técnica previa del órgano competente o del proyectista (un año) | `REPRESENTADO` | E-T5A, E-GPRO, E-TPRO, E-T5 | reglamento-de-la-ley-general-de-contrataciones-p `art-194.2` (p. 109, 110) |
| Publicación en la Pladicop sin adenda y prohibición de aprobar por regularización | `REPRESENTADO` | E-T11, E-F1 | reglamento-de-la-ley-general-de-contrataciones-p `art-194.3` (p. 110) |
| Adicionales de emergencia: ejecución inmediata autorizada y regularización posterior | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-194.4` (p. 110) |
| Más del 50 % del contrato original: resolución del contrato | `NO-REPRESENTADO` | — | reglamento-de-la-ley-general-de-contrataciones-p `art-194.5` (p. 110) |
| Hasta 15 % por la autoridad de la gestión administrativa, restando deductivos vinculados | `REPRESENTADO` | E-TC, E-TVIN, MOD-ALC-ADI | ley-general-de-contrataciones-publicas-con-modif `art-64.2` (p. 31) |
| Más de 15 % hasta 30 % por el titular; más de 30 % hasta 50 % con autorización de la Contraloría | `REPRESENTADO` | E-G8, E-T8, E-T10 | ley-general-de-contrataciones-publicas-con-modif `art-64.3` (p. 31) |
| Pronunciamiento de la Contraloría en 15 días hábiles | `REPRESENTADO` | E-M1 | ley-general-de-contrataciones-publicas-con-modif `art-64.4` (p. 31) |

## Controles

- Elementos o mensajes sin resultado: ninguno.
- Citas con problemas: 0.
- Referencias mencionadas sin ancla: 0.
- Obligaciones de la fuente no representadas: 2.
- Anclas del visor: {'SIN-COORDENADAS': 3, 'VIGENTE': 74}.
