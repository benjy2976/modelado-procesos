---
id: HER-MESA-MODELAMIENTO-INFORME-AUDITORIA-FASE-5-S4-3
tipo: informe
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
proceso:
  - S4.3
fecha_creacion: 2026-11-25
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Informe consolidado de la auditoría de S4.3 (fase 5)

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md). Procedimiento en el [plan de corrida](plan-corrida-documental-y-auditoria.md). Estado vivo por proceso en el [resumen de la corrida S4.3](../auditorias/corrida-S4-3.md). Antecedente: [informe del piloto S4.3.2.7](informe-piloto-auditoria-S4-3-2-7.md).

Las clasificaciones son propuestas de un agente de IA con el formato aprobado en DEC-057. No validan normas, no atribuyen conformidad y no cambian el estado de ningún modelo, que siguen en `ELABORACION`. Las tablas de las secciones siguientes son las de la auditoría inicial. El 2026-11-25 el usuario pidió aplicar las propuestas de interfaces y de Pladicop, plazos y silencio (DEC-058); su resultado está en la sección «Aplicación de propuestas — 2026-11-25». Las demás propuestas esperan decisión.

## Resultado por proceso

| Proceso | Afirmaciones | `SUSTENTADA` | `INFERENCIA` | `CONTRADICCION` | Obligaciones | No representadas | Anclas |
|---|---|---|---|---|---|---|---|
| S4.3 | 11 | 6 | 5 | 0 | 9 | 5 (interacciones de la ficha) | vigentes |
| S4.3.1 | 30 | 17 | 13 | 0 | 15 | 6 | vigentes |
| S4.3.2 | 20 | 11 | 7 | 2 | 11 | 1 | vigentes |
| S4.3.2.1 | 20 | 12 | 7 | 1 | 10 | 6 | vigentes |
| S4.3.2.2 | 64 | 36 | 28 | 0 | 12 | 2 (y 1 fuera de alcance) | vigentes |
| S4.3.2.3 | 95 | 29 | 66 | 0 | 14 | 3 | 75 |
| S4.3.2.4 | 23 | 15 | 8 | 0 | 11 | 8 | 22 |
| S4.3.2.5 | 30 | 10 | 20 | 0 | 11 | 8 (y 1 fuera de alcance) | 34 |
| S4.3.2.6 | 26 | 5 | 21 | 0 | 12 | 7 | 18 |
| S4.3.2.7 | 33 | 13 | 11 | 0 | 15 | 0 | 16 |
| S4.3.2.8 | 20 | 6 | 14 | 0 | 8 | 3 | 12 |
| S4.3.3 | — | — | — | — | — | — | `SIN-MODELO` |

La corrida deja 10 procesos `CON-HALLAZGOS`, 1 `COMPLETO` (S4.3.2.7) y 1 `SIN-MODELO` (S4.3.3).

**Integridad (5.C2).** El control `auditoria informe --check` ya comprueba elementos sin resultado, citas que no aparecen en su fragmento, inventarios con hash desactualizado, anclas no vigentes y referencias sin ancla. En los 11 procesos con modelo todas estas comprobaciones pasan. El `--check` falla solo por las obligaciones no representadas, que son hallazgos abiertos y no defectos de integridad. S4.3.2.7 pasa por completo.

## Contradicciones (corregidas el 2026-11-25, DEC-059)

- **S4.3.2, F-3 y su mensaje a S4.3.3.** El modelo deja «por definir» el tratamiento tras la nulidad. El art. 111.3 lo define para obras: si la nulidad no es atribuible al contratista, corresponde la constatación física e inventario, igual que tras una resolución.
- **S4.3.2.1, F-2.** Con observaciones, el proceso termina sin pago. El art. 210.4 otorga plazo de subsanación, revisa la respuesta en 2 días hábiles y, aunque no se subsane, paga el monto no cuestionado.

Ambas se corrigieron por instrucción del usuario. F-3 envía el contrato a constatación e inventario cuando la nulidad no es atribuible al contratista; el caso atribuible queda sin tratamiento normativo identificado. En S4.3.2.1 se retiró F-2 y se modeló el ciclo de subsanación con pago del monto no cuestionado. No quedan contradicciones abiertas en S4.3.

El acta de inicio (S4.3.1 y S4.3.2 E-1) dejó de ser contradicción: el usuario aclaró que es una práctica institucional en obras por contrata para formalizar el inicio cuando se cumplen las condiciones, no una exigencia legal. Las afirmaciones se rectificaron a `INFERENCIA` y `EVIDENCIA-OBSERVADA`.

## Patrones transversales

1. **La Pladicop no figura como canal.** Los arts. 109.3, 194.3, 198.4 y 200.1 d) hacen surtir efecto a reducciones, adicionales y ampliaciones con su publicación en la Pladicop, sin adenda. Los modelos registran en el SGD y solo S4.3.2.7 nombra la Pladicop, tras la puerta 4.P.
2. **Faltan plazos y efectos del silencio.** Están en la norma pero no en el modelo: los 10, 5 y 10 días hábiles del 200.1, la aprobación ficta del 200.1 d) y el plazo de 22 días del 176.3. El circuito institucional de cinco instancias (OACGD, SGGOS, GRI, GRAJ y decisor) tiene que caber en esos plazos, y ningún modelo lo muestra.
3. **Las excepciones de cierre no tienen ruta.** Por ejemplo, la resolución del contrato al superar el 50 % (194.5 y 197.4), la emergencia (194.4) y la suspensión por falta de pago (202.3).
4. **Contratos vinculados.** Ampliar o suspender la obra amplía o suspende de oficio el contrato de supervisión (200.4 y 107.3). No se representa en ningún modelo.
5. **Las inferencias son sobre todo institucionales.** La ruta interna (OACGD, SGGOS, GRI, GRAJ) se apoya en el ROF y en la observación del usuario del 2026-11-10. Su adscripción y la delegación de la autoridad siguen en `EVIDENCIA-INSUFICIENTE`.
6. **Ámbito de las fuentes en S4.3.2.6.** La Ley 31589 regula la reactivación de obras inventariadas como paralizadas, no el evento ordinario. En contrata, el Reglamento trata la paralización como causal de ampliación (198.1 a) o como suspensión acordada (107). La Directiva 017-2023-CG solo aplica a administración directa.

## Interfaces (5.E2)

**Candidatos deterministas.** `comparar-interfaces` sobre S4.3 y S4.3.2 produce 8:

| Padre | Tipo | Hijo | Detalle |
|---|---|---|---|
| S4.3 | `SALIDA-NO-REPRESENTADA` | S4.3.1 | El padre declara «Acta de inicio de obra»; S4.3.1 termina en «Inicio del plazo comunicado». |
| S4.3 | `SECUENCIA-SIN-CORRESPONDENCIA` | S4.3.2 | El fin de S4.3.1 no corresponde al inicio «Acta de inicio de obra recibida». |
| S4.3 | `MENSAJE-SIN-CONTRAPARTE` | S4.3.2 | S4.3.2 recibe el acta de S4.3.1, que no la envía. |
| S4.3 | `HIJO-SIN-MODELO` | S4.3.3 | Sin tabla. |
| S4.3.2 | `TIPO-DE-DISPARO` | S4.3.2.7 | El padre lo dispara por condición y el hijo inicia por mensaje. |
| S4.3.2 | `MENSAJE-SIN-CONTRAPARTE` | S4.3.2.3 | Recibe de S4.3.2.2 una respuesta que S4.3.2.2 no envía. |
| S4.3.2 | `MENSAJE-SIN-CONTRAPARTE` | S4.3.2.3 | Envía a S4.3.2.7 un sustento reclasificado que S4.3.2.7 no recibe. |
| S4.3.2 | `MENSAJE-SIN-CONTRAPARTE` | S4.3.2.8 | Envía a S4.3.2.1 el sustento para valorización, que S4.3.2.1 no recibe. |

Como el acta de inicio es práctica institucional, los tres primeros se resuelven alineando nombres: S4.3.1 termina con el acta de inicio que S4.3.2 recibe. No es una corrección normativa.

**Interfaces que solo muestra la cobertura fuente → modelo.** Ningún modelo tiene un mensaje para ellas, por lo que el contraste determinista no puede verlas:

- Adicionales (S4.3.2.3) y mayores metrados (S4.3.2.8) son causales de ampliación de plazo (198.1 b y c) hacia S4.3.2.4. Los mayores gastos generales se pagan por el art. 201 (197.3).
- La paralización en contrata (S4.3.2.6) se tramita como ampliación (S4.3.2.4) o como suspensión (S4.3.2.5).
- Si la supervisión o la entidad no absuelven las consultas, el contratista puede pedir ampliación por la demora (S4.3.2.2, art. 190.4), hacia S4.3.2.4.
- La falta de pago de dos valorizaciones (S4.3.2.1) suspende el plazo por anotación del residente (202.3, S4.3.2.5).
- La resolución del contrato (194.5, 197.4 y 202.4-202.5) no tiene proceso destino en el árbol S4.3.

## Propuestas pendientes de decisión (5.E3)

Las propuestas de cada proceso están en la sección «Auditoría por afirmación — 2026-11-24 (fase 5)» de su sustento. En resumen:

| Proceso | Propuestas principales |
|---|---|
| S4.3 | Representar las 5 interacciones de la ficha que faltan. |
| S4.3.1 | Reflejar el plazo de 22 días (176.3), el 176.4, el diferimiento de actas (176.7-176.9) y el 179.2; alinear el fin con el acta de inicio. |
| S4.3.2 | Corregir F-3 conforme al 111.3; alinear el disparo de S4.3.2.7. |
| S4.3.2.1 | Corregir F-2 conforme al 210.4; recibir el sustento de S4.3.2.8; derivar el 202.3. |
| S4.3.2.2 | Representar el 190.4 y el 190.5; enviar la respuesta que espera S4.3.2.3. |
| S4.3.2.3 | Nombrar la Pladicop y la prohibición de regularizar (194.3); emergencia (194.4); rama de resolución al superar el 50 % (194.5). |
| S4.3.2.4 | Solicitud a la entidad y a la supervisión en 10 días hábiles, con extemporaneidad; plazos de 5 y 10 días hábiles; falta de opinión y aprobación ficta; Pladicop; contratos vinculados. |
| S4.3.2.5 | Acta de reinicio con el contratista y ruta sin acuerdo; comunicar el programa actualizado (202.2); regla de costos; contratos vinculados; decidir dónde va el 202.3. |
| S4.3.2.6 | Decidir el alcance por régimen. Para administración directa: tres fechas en el cuaderno, cronograma en 2 días calendario y registro en el SNPMGI y el INFOBRAS. Para la Ley 31589, si se mantiene, una variante. |
| S4.3.2.7 | Ninguna; se recibe el sustento de S4.3.2.3 si se acepta la interfaz. |
| S4.3.2.8 | Salida a resolución (197.4); interfaz con S4.3.2.4 (198.1 c y 197.3). |

## Aplicación de propuestas — 2026-11-25 (DEC-058)

Se aplicaron las propuestas de interfaces y de los patrones 1 y 2 en seis tablas. Las auditorías se reconfirmaron sobre la nueva revisión (detalle en la sección «Cambios aplicados» de cada sustento):

| Proceso | Cambio | Resultado tras reconfirmar |
|---|---|---|
| S4.3.1 | Acta de inicio como salida, con mensaje a S4.3.2; plazo de 22 días del 176.3 en T1 | 32 afirmaciones vigentes (18 `SUSTENTADA`, 14 `INFERENCIA`) y 2 superadas; no representadas: 6 → 5 |
| S4.3.2.1 | T-1 recibe el sustento de S4.3.2.8 (210.1) | no representadas: 6 → 5 (luego 3 con DEC-059) |
| S4.3.2.2 | E-F1 envía la respuesta como antecedente a S4.3.2.3 | sin cambio en obligaciones |
| S4.3.2.3 | E-T11 publica en la Pladicop y anota la prohibición de regularizar (194.3) | no representadas: 3 → 2 |
| S4.3.2.4 | Causales con su origen; solicitud a entidad y supervisión con plazo y extemporaneidad; 5 días del supervisor con compuerta basada en eventos y vencimiento; 10 días y silencio en E-T9; Pladicop en E-T10, E-F1 y E-F2 | 31 afirmaciones vigentes (25 `SUSTENTADA`, 6 `INFERENCIA`) y 8 superadas (`NO-APLICA`); no representadas: 8 → 3 |
| S4.3.2.7 | Inicio condicional propio (E0) y recepción desde S4.3.2.3 | sigue `COMPLETO` |

**Interfaces.** `comparar-interfaces` baja de 8 candidatos a 1: S4.3.3 `SIN-MODELO`. Las anclas de los seis procesos están vigentes y no hay referencias sin ancla.

**Conteos.** Las primeras cifras de este lote contaban también afirmaciones superadas. Se corrigieron rectificándolas a `NO-APLICA`; las de esta tabla son las vigentes.

**Generación.** D4 deja 2 hallazgos geométricos nuevos en S4.3.2.4, adoptados con `--forzar` y documentados. S4.3.2.3 conserva los 18 ya documentados. Los demás modelos quedan sin hallazgos.

**Siguen pendientes:**
- el alcance de S4.3.2.6 y el destino del 202.3;
- los plazos del 210.2-210.3, el 176.4, el 179.2 y el diferimiento.

## Rutas de resolución, emergencia y contratos vinculados — 2026-11-25 (DEC-060)

| Proceso | Cambio | Resultado |
|---|---|---|
| S4.3.2.3 | Ruta de emergencia (194.4) y rama de resolución al superar el 50 % (194.5) | `COMPLETO`: 14/14 obligaciones; D4 sube de 18 a 30 hallazgos (`--forzar`, revisión visual pendiente) |
| S4.3.2.4 | Ampliación de oficio de los contratos vinculados (200.4) | no representadas: 3 → 2 |
| S4.3.2.5 | Suspensión y acta de reinicio de contratos vinculados (107.3); inicio por resolución del vinculado (202.5) | no representadas: 8 → 6 |
| S4.3.2.8 | Comunicación de la causal de resolución al superar el 50 % (197.4) | no representadas: 3 → 2 |

La corrida queda con 9 procesos `CON-HALLAZGOS`, 2 `COMPLETO` (S4.3.2.3 y S4.3.2.7) y 1 `SIN-MODELO` (S4.3.3). Los fines de resolución remiten al evento Contrato resuelto (B-1) de S4.3.2. El trámite de la resolución (arts. 122-123) no tiene proceso en el árbol.

## Limitaciones

- **Directiva 017-2023-CG.** No se segmenta por numerales: el «artículo 3» de la resolución aprobatoria absorbe la directiva. Las citas se verifican dentro de un fragmento amplio y las anclas caen en la página correcta. Conviene corregir la segmentación cuando se autorice trabajar en la herramienta.
- **Espacios espurios.** La verificación de citas exige el texto tal como se extrajo. Las citas eligen tramos sin espacios espurios, como «qu e», «d iez» o las ligaduras de El Peruano.
- **Vigencia por confirmar.** La Ley 31589 (TUO) y la Directiva 017-2023-CG tienen la vigencia jurídica por confirmar según el catálogo; las anclas lo declaran.
- **Límites del contraste de interfaces.** Solo compara nombres, disparos y mensajes declarados. Las interfaces implícitas en la norma se detectan por la cobertura y las interpreta el agente.
- **Revisión de especialistas.** La revisión jurídica de vigencia, ámbito y sentido corresponde a especialistas.

## Decisión solicitada

1. Qué propuestas aplicar y en qué orden. Se sugiere empezar por las interfaces (acta de inicio, mensajes sin contraparte) y por los patrones 1 y 2 (Pladicop, plazos y silencio), que afectan a varios modelos.
2. El alcance por régimen de S4.3.2.6 y el destino del 202.3 (S4.3.2.1 o S4.3.2.5).
3. Si se crea o asigna un proceso destino para la resolución del contrato, y si se modela S4.3.3.

**Decisión del 2026-11-25 (`DEC-061`).** La etapa se cierra con los procesos ya definidos. El proceso de resolución del contrato, el tratamiento de la nulidad atribuible al contratista y una eventual variante en diagrama propio de S4.3.2.6 para la Ley 31589 quedan como ampliaciones diferidas en [Alcance](../../../00-gobernanza/alcance.md#ampliaciones-de-alcance-diferidas). S4.3.3 ya figura en el árbol, pero también se difiere por decisión del usuario (`DEC-062`); el candidato de interfaz `HIJO-SIN-MODELO` se explica por esa decisión.

El silencio o las métricas no equivalen a conformidad.
