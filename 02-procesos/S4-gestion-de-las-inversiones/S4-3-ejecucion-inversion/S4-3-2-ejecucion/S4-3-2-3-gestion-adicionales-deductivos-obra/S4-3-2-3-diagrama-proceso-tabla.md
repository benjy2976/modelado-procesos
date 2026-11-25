---
id: AP-S4-3-2-3-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.3
nivel_proceso: 3
perfil_trazado: zigzag-controlado
proceso:
  - S4.3.2.3
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-3
---

# S4.3.2.3 Gestion de adicionales y deductivos de obra

Sube a: [S4.3.2.3 Gestion de adicionales y deductivos de obra](00-S4-3-2-3-gestion-adicionales-deductivos-obra.md)

Division mediante `DEC-047`: este proceso comprende adicional, deductivo puro y adicional con deductivo vinculante. Reducciones de prestaciones y mayores metrados se desarrollan en S4.3.2.7 y S4.3.2.8. El deductivo puro tiene clasificacion propia; su procedimiento autonomo permanece con EVIDENCIA-INSUFICIENTE.

Notas que no se dibujan:

- La instancia es una por solicitud, necesidad o causal de modificacion de alcance.
- `MOD-ALC-*` identifica variantes internas de modelamiento, no codigos de nivel 4.
- Cuaderno de Incidencias es la denominacion institucional uniforme adoptada para este modelo, incluso en administracion directa; las fuentes de esa modalidad pueden denominarlo cuaderno de obra.
- Ejecutor de obra, segun regimen agrupa al residente y, cuando una actividad contractual lo exige, al contratista o su representante legal. Supervisor o inspector de obra es una abstraccion funcional ejercida alternativamente por supervisor contratado o inspector de la entidad; no los convierte en una misma organizacion ni supone que concurran.
- El pool funcional del elaborador identifica las tres alternativas del art. 194.2 c: entidad contratante, contratista o supervisor. Solo una se activa por expediente, segun las bases; el pool no convierte a los tres en una organizacion ni atribuye adscripcion no acreditada.
- SGGOS — Coordinador de obra puede verificar integridad y realizar la clasificacion inicial del alcance original, la causal y la figura cuando no se requiere juicio tecnico especializado.
- Cuando la materia excede su competencia, interviene el especialista competente. El coordinador no sustituye la revision tecnica de especialidad, el control contractual y de costos ni la decision formal.
- El carril Titular de la competencia o autoridad delegada evita fijar una autoridad que dependa de delegaciones variables.
- Quien elabora no emite la unica opinion tecnica que sustenta la decision.

- Los plazos de 15 y 10 dias se aplican exclusivamente al supuesto del art. 194 indicado en cada tarea; no reinician con la carta de encargo ni con una subsanacion. Los 10 dias de opinion del supervisor estan expresos cuando elabora el contratista. Si elabora la entidad, la Opinion D000092 exige opinion del supervisor en el plazo correspondiente, sin dar alli un numero autonomo. Si elabora el supervisor, no revisa su propio expediente: interviene el proyectista o el organo tecnico competente para la opinion previa.
- El detalle de este lote corresponde a Ley 32069, solo construccion. La emergencia sigue la ruta del art. 194.4 (E-TEMER) y se regulariza por este mismo procedimiento. Otros regimenes y sistemas de entrega se identifican y quedan pendientes de desarrollo especifico, sin aplicarles estos plazos por analogia.
- Fuentes, vigencia, condiciones y limites de la propuesta: [Sustento](S4-3-2-3-sustento.md#replanteamiento-del-circuito-de-alcance---2026-11-18).

- La respuesta de consultas ingresa antes de la anotacion especifica de necesidad. Si ya existe una anotacion valida, se conserva su fecha; no se repite para reiniciar el computo. La elaboracion transcurre mientras se tramita la ratificacion; solo la presentacion efectiva queda condicionada a esta (Opinion D000092, 2.1-2.3).

## Pools

| Pool | Carriles |
|---|---|
| Ejecutor de obra, segun regimen | Residente de obra |
| Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad |
| Gobierno Regional Huanuco | OACGD — Registro documentario; SGGOS — Subgerente de Gestion de Obras y Supervision; SGGOS — Coordinador de obra; SGGOS — Control contractual y costos; SGE — Coordinacion de revision tecnica; SGE — Especialista tecnico competente; Subgerencia de Presupuesto Publico — Control presupuestal; GRAJ — Asesoria Juridica; Titular de la competencia o autoridad delegada |
| Elaborador del adicional segun bases: entidad, contratista o supervisor | Responsable de elaborar el expediente (una alternativa por caso) |
| Contraloria General de la Republica |  |
| S4.3.2.2 Atencion de consultas de obra |  |
| Proyectista |  |
| S4.3.2.7 Gestion de reducciones de prestaciones |  |

## Elementos

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Clase | Fuente |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-E1 | 1 | Ejecutor de obra, segun regimen | Residente de obra | inicio-mensaje | Respuesta de consulta recibida | R-T1 |  |  | entra: Respuesta S4.3.2.2 |  |  |  | EQ | Usuario 2026-11-18; Opinion D000083, 2.2.1 y 3.3 |
| R-T1 | 2 | Ejecutor de obra, segun regimen | Residente de obra | tarea-usuario | Anotar necesidad del adicional en cuaderno | R-F1 |  |  | entra: Respuesta de consulta; sale: Anotacion de necesidad |  |  | Hito del computo de 5 y 15 dias: dia siguiente de esta anotacion; conservar fecha si ya existe | NORM | Reglamento, art. 194.2 a; Opinion D000092, 2.1-2.3 y 3.1-3.3 |
| R-F1 | 3 | Ejecutor de obra, segun regimen | Residente de obra | fin-mensaje | Anotacion y antecedentes remitidos |  |  |  |  |  |  |  | NORM | Reglamento, arts. 194.2 y 197.1; Directiva 017-2023-CG, num. 7.3.6 |
| S-E1 | 4 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Sustento del residente recibido | S-G1 |  |  | entra: Registro y sustento de necesidad |  |  |  | NORM | Reglamento, arts. 186.1 y 194.2 b; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6 |
| S-E2 | 5 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-condicional | Necesidad identificada por supervision | S-T0 |  |  |  |  |  | Origen alternativo del art. 194; consulta previa si existe. No duplicar anotacion ya valida | EQ | Precision operativa del equipo; Reglamento, arts. 186-188 |
| S-T0 | 6 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea-usuario | Registrar la necesidad en el Cuaderno de Incidencias | S-G1 |  |  | sale: Registro de necesidad |  |  | Comunicar anotacion al elaborador definido en bases; inicia computo sin esperar ratificacion | EQ | Precision operativa del equipo; Reglamento, art. 188.3; Directiva 017-2023-CG, nums. 7.3.2 y 7.3.6 |
| S-G1 | 7 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | compuerta |  | S-T1 |  |  |  |  |  | Convergencia exclusiva: residente o supervision. No aprueba ni espera ambos origenes | PROP | Convergencia de origenes |
| S-T1 | 8 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Sustentar posicion tecnica sobre necesidad y riesgo | S-G2 |  |  |  | Informe a entidad en 5 dias desde el dia siguiente de la anotacion (art. 194.2 b) |  | El informe fundamenta si ratifica o no; no extender este plazo a reducciones ni administracion directa | NORM | Reglamento, arts. 187.1, 194.2 b y 197.1; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6 |
| S-G2 | 9 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | compuerta | ¿Ratifica la necesidad? | S-F1 [Si]; S-F2 [No] |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 b; Directiva 017-2023-CG, num. 7.3.6 |
| S-F1 | 10 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Necesidad ratificada y remitida |  |  |  | sale: Informe de necesidad |  |  |  | NORM | Reglamento, art. 194.2; Directiva 017-2023-CG, num. 7.3.6 |
| S-F2 | 11 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin | Necesidad no ratificada |  |  |  |  |  |  |  | PROP | Cierre propuesto para el control inicial |
| E-E1 | 12 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Sustento de necesidad recibido | E-T1 |  |  | entra: Informe de necesidad |  |  |  | EQ | ROF, art. 20; DEC-037 |
| E-T1 | 13 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Registrar y derivar a SGGOS por SGD | E-TSG |  |  | sale: Registro y derivacion; almacen: SGD |  |  |  | EQ | ROF, art. 20; observacion del usuario, 2026-11-10 |
| E-TSG | 87 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea-usuario | Recibir sustento y derivarlo al coordinador por SGD | E-T2 |  |  | almacen: SGD |  |  |  | OBS | Precision institucional del usuario, 2026-11-19; circuito analogo documentado en S4.3.2.2 |
| E-T2 | 14 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Verificar integridad, regimen, sistema de entrega y supuesto | E-GREG |  |  | entra: Expediente |  |  |  | EQ | ROF, arts. 97-98; DEC-041 |
| E-T3 | 15 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Clasificar alcance original, causal y figura inicial | E-G0 |  |  |  |  |  | Si requiere juicio tecnico especializado, deriva al especialista competente | EQ | Precision del equipo registrada en DEC-041 |
| E-G0 | 16 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Corresponde adicional o deductivo de obra? | E-G2 [Si]; E-T15 [No] |  |  |  |  |  |  | PROP | Separa obligacion original, valorizacion y modificacion potencial |
| E-T15 | 17 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea-usuario | Comunicar clasificacion y proceso de destino | E-F3 |  |  | sale: Comunicacion |  |  | Reducciones: S4.3.2.7; mayores metrados: S4.3.2.8. No aprueba la figura derivada | OBS | Precision institucional del usuario, 2026-11-19; DEC-041 |
| E-F3 | 18 | Gobierno Regional Huanuco | OACGD — Registro documentario | fin-mensaje | Caso clasificado fuera del proceso |  |  |  |  |  |  |  | PROP | Puede corresponder exigir cumplimiento, valorizar o derivar a otro proceso |
| E-G2 | 19 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Que caso corresponde? | MOD-ALC-ADI [Adicional]; E-TVIN [Adicional con deductivo vinculante]; E-TDP [Deductivo puro] |  |  |  |  |  |  | PROP | DEC-047; tres casos solicitados por el usuario |
| MOD-ALC-ADI | 20 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Identificar adicional sin deductivo vinculado | E-G6 |  |  |  |  |  |  | EQ | Ley 32069, art. 64.2-64.3; Reglamento, art. 194; DEC-046 |
| E-G6 | 24 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Necesidad ratificada, causal y elaborador acreditados? | E-T4 [Si]; E-FNEC [No] |  |  |  |  |  |  | PROP | Reglamento, art. 194.1 y 194.2 a-d; bases del contrato; detalle en sustento |
| E-T4 | 25 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | mensaje-envio | Comunicar ratificacion a quien elabora | E-M2 |  |  | sale: Ratificacion de necesidad |  |  | A contratista u organo elaborador (SGE si corresponde), segun bases; supervisor ya conoce su informe. Es segundo aviso para SGE si recibio la anotacion; permite presentar, pero no inicia ni reinicia los 15 dias | PROP | Opinion D000092, 2.1 nota 4, 2.2 y 3.2; Reglamento, art. 194.2 b-d; interfaz S4.3.2.2 |
| E-M2 | 26 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-recepcion | Expediente del adicional presentado a evaluacion | E-GEL |  |  | entra: Expediente tecnico |  |  |  | NORM | Reglamento, art. 194.2 d-f; Directiva 017-2023-CG, num. 7.3.6 |
| E-T5A | 27 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | tarea-usuario | Determinar quien emite opinion tecnica previa | E-GPRO |  |  |  |  |  | Proyectista en primera instancia si no transcurrio mas de un anio; en defecto organo competente. Cuando elaboro el supervisor, esta es la evaluacion tecnica ajena al autor del expediente | PROP | Reglamento, art. 194.2 g; Opinion D000092, 2.8-2.9 y 3.8-3.11 |
| E-T5 | 28 | Gobierno Regional Huanuco | SGE — Especialista tecnico competente | tarea | Emitir opinion del organo competente | E-GJOIN |  |  | sale: Opinion tecnica | Si elaboro contratista: mismo plazo de supervision |  |  | PROP | Opinion D000092, 2.8 y 2.9 A-B; DEC-038 |
| E-G7 | 29 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | compuerta | ¿Evaluacion tecnica favorable? | E-TINF [Si]; E-T16 [No] |  |  |  |  |  | Resultado favorable requiere informe de SGE; resultado desfavorable tambien se eleva para decision | PROP | Precision operativa del usuario, 2026-11-20; DEC-038 |
| E-TINF | 98 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | tarea-usuario | Elaborar informe de evaluacion tecnica favorable | E-TNEV |  |  | sale: Informe de evaluacion tecnica |  |  | Recoge y fundamenta la evaluacion favorable; se remite para el tramite de decision. No equivale a aprobar el adicional | OBS | Precision operativa del usuario, 2026-11-20; Reglamento, art. 194.2 g para opinion tecnica |
| E-T16 | 30 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | tarea-usuario | Integrar observaciones para decision | E-TNEV |  |  | sale: Observaciones tecnicas |  |  | Subsanacion y efecto sobre plazos pendientes; no se reinicia automaticamente el plazo normativo | PROP | Propuesta operativa; Reglamento, art. 194.2 f; no sustituir resolucion por informe |
| E-TNEV | 93 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | mensaje-envio | Comunicar evaluacion tecnica | E-G5 |  |  | sale: Resultado tecnico comunicado |  |  | Al ejecutor y al elaborador, segun corresponda; no es aprobacion del adicional; canal por confirmar | PROP | Precision del usuario, 2026-11-19; art. 194.2 e-g para secuencia de opiniones |
| E-G5 | 32 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva | ¿Que controles requiere? | E-TC [C]; E-T6 [P]; E-T7 [J] |  |  |  |  |  | C siempre; P y J segun figura. Controles no amplian el plazo legal | EQ | DEC-038; control contractual obligatorio en esta propuesta |
| E-TC | 33 | Gobierno Regional Huanuco | SGGOS — Control contractual y costos | tarea | Verificar monto, precios, deductivo vinculado y acumulados | E-G5C |  |  | sale: Control contractual y de costos |  |  | No descontar una reduccion independiente como deductivo vinculado sin sustento | EQ | Ley 32069, arts. 63-64; Reglamento, arts. 109 y 194-197; ROF, arts. 97-98 |
| E-T6 | 34 | Gobierno Regional Huanuco | Subgerencia de Presupuesto Publico — Control presupuestal | tarea | Emitir certificacion o prevision cuando corresponda | E-G5C |  |  | sale: Control presupuestal |  |  |  | EQ | ROF, art. 51; Directiva 017-2023-CG, num. 7.3.6 |
| E-T7 | 35 | Gobierno Regional Huanuco | GRAJ — Asesoria Juridica | tarea | Emitir opinion o revisar el acto cuando corresponda | E-G5C |  |  | sale: Control juridico |  |  |  | EQ | ROF, arts. 44-45; Directiva 017-2023-CG, num. 7.3.6 |
| E-G5C | 36 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva |  | E-T17 |  |  |  |  |  |  | PROP | Convergencia de controles activados |
| E-T17 | 37 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Consolidar controles, responsables y discrepancias resueltas | E-G8 |  |  | sale: Expediente consolidado |  |  |  | PROP | Matriz de control propuesta en DEC-038; no sustituye opiniones especializadas |
| E-G8 | 38 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Que limite alcanza el adicional acumulado? | E-T8 [Mayor de 30 % y hasta 50 %]; E-FRES [Mayor de 50 %]; E-T10 [Hasta 30 %] (por defecto) |  |  |  |  |  | Se verifica luego de integrar expediente y opiniones, antes de resolver; no es opinion sobre la necesidad ni requisito previo a la presentacion del expediente | NORM | Ley 32069, arts. 64.2, 64.3 b y 64.4; Reglamento, art. 194.5 |
| E-T8 | 39 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Solicitar autorizacion a la Contraloria | E-M1 |  |  | sale: Solicitud de autorizacion |  |  | Unidad remitente interna pendiente de confirmar | EQ | Ley 32069, arts. 64.3 b y 64.4; EVIDENCIA-INSUFICIENTE sobre circuito interno |
| E-M1 | 40 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | mensaje-recepcion | Pronunciamiento de Contraloria recibido | E-G9 |  |  | entra: Pronunciamiento |  |  |  | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-G9 | 41 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | compuerta | ¿Autorizada? | E-T10 [Si]; E-F2B [No] |  |  |  |  |  |  | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-F2B | 42 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | No autorizacion comunicada |  |  |  |  |  |  |  | PROP | Cierre cuando no se obtiene la autorizacion externa exigible |
| E-T10 | 43 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Emitir y notificar resolucion del adicional | E-G10 |  |  | entra: Expediente consolidado; sale: Pronunciamiento | Art. 194.2 f: 12 dias habiles desde opinion del supervisor o expediente elaborado por este |  | 12 dias habiles del tramite institucional, desde dia siguiente de opinion del supervisor o expediente elaborado por este; no aplica a reduccion | NORM | Reglamento, art. 194.2 f; Opinion D000092, 2.9 y 3.9-3.11 |
| E-G10 | 44 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | compuerta | ¿Favorable? | E-T11 [Si] (por defecto); E-F2C [No] |  |  |  |  |  |  | PROP | Rutas de decision |
| E-T11 | 45 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Publicar la aprobacion en la Pladicop y actualizar registros | E-F1 |  |  | sale: Registros y comunicacion; almacen: Pladicop |  |  | Surte efecto con su publicacion en la Pladicop, sin adenda. Prohibido aprobar adicionales por regularizacion. Unidad que publica por confirmar | NORM | Reglamento, art. 194.3 (texto vigente); Opinion D000092, 2.11 y 3.14-3.15; registros de inversion aplicables |
| E-F1 | 46 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Aprobacion del adicional publicada |  |  |  |  |  |  |  | PROP | Reglamento, art. 194.3 (texto vigente) |
| E-F2C | 47 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | Decision no favorable comunicada |  |  |  |  |  |  |  | PROP | Producto alterno |
| X-E1 | 48 | Elaborador del adicional segun bases: entidad, contratista o supervisor | Responsable de elaborar el expediente (una alternativa por caso) | inicio-mensaje | Anotacion comunicada al elaborador | X-TENC |  |  | entra: Anotacion de necesidad; entra: Respuesta de consulta y comunicacion del elaborador segun bases |  |  | Solo si el elaborador no conocia la anotacion; el aviso no inicia los 15 dias | PROP | Reglamento, art. 194.2 c-d; Opinion D000092, 2.1-2.3; interfaz S4.3.2.2 |
| X-E2 | 97 | Elaborador del adicional segun bases: entidad, contratista o supervisor | Responsable de elaborar el expediente (una alternativa por caso) | inicio-condicional | Anotacion propia conocida por elaborador | X-TENC |  |  |  |  |  | Alternativa exclusiva de X-E1 cuando el elaborador ya conoce el registro del cuaderno | PROP | Reglamento, art. 194.2 a-d; precision del usuario, 2026-11-19 |
| X-TENC | 88 | Elaborador del adicional segun bases: entidad, contratista o supervisor | Responsable de elaborar el expediente (una alternativa por caso) | tarea-usuario | Asumir encargo y organizar elaboracion del expediente | X-T1 |  |  |  |  |  | Comprobar elaborador de las bases y alcance de la respuesta; no esperar la ratificacion para empezar ni iniciar nuevo plazo | PROP | Reglamento, art. 194.2 c-d; Opinion D000092, 2.1-2.3; respuesta S4.3.2.2 |
| X-T1 | 49 | Elaborador del adicional segun bases: entidad, contratista o supervisor | Responsable de elaborar el expediente (una alternativa por caso) | tarea-usuario | Elaborar expediente del adicional y deductivo vinculado | X-MR |  |  | sale: Expediente tecnico | 15 dias calendario desde el dia siguiente de la anotacion; necesidad ratificada |  | Elaboracion dentro del computo iniciado; presentacion condicionada a ratificacion; plazo adicional solo otorgado con sustento | NORM | Reglamento, art. 194.2 c-d; Opinion D000092, 2.1-2.7 |
| X-F1 | 50 | Elaborador del adicional segun bases: entidad, contratista o supervisor | Responsable de elaborar el expediente (una alternativa por caso) | fin-mensaje | Expediente tecnico presentado |  |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 d-f; Directiva 017-2023-CG, num. 7.3.6 |
| E-GREG | 52 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Que supuesto corresponde? | E-T3 [Ley 32069, solo construccion] (por defecto); E-TEMER [Emergencia]; E-FPEND [Otro regimen] |  |  |  |  |  | Emergencia: riesgo para el ambiente, la poblacion, los trabajadores o la obra (194.4) | PROP | Reglamento, arts. 194.1-194.4; DEC-046 |
| E-FPEND | 53 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin | Caso de otro regimen pendiente de ruta especifica |  |  |  |  |  |  |  | PROP | DEC-046; EVIDENCIA-INSUFICIENTE, no es decision de fondo |
| E-TEMER | 99 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Autorizar a la supervision la ejecucion inmediata del adicional | E-T3 |  |  |  |  |  | Regularizacion por el 194.2 desde E-T3 | NORM | Reglamento, art. 194.4 |
| E-FRES | 100 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin | Contrato en causal de resolucion por superar el 50 % |  |  |  |  |  |  | Activa la resolucion del contrato (S4.3.2, B-1) | NORM | Reglamento, art. 194.5 |
| E-FNEC | 94 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin | Necesidad o elaborador pendiente de acreditar |  |  |  |  |  |  |  | PROP | Salida local de E-G6; no es decision de fondo |
| E-FDP | 96 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin | Deductivo puro pendiente de ruta |  |  |  |  |  |  |  | PROP | DEC-047; EVIDENCIA-INSUFICIENTE sobre ruta autonoma |
| E-GEL | 58 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Identificar autor y ruta de evaluacion | E-GPAR |  |  |  |  |  | El elaborador ya se acredito antes del encargo. Contratista o entidad: opinion de supervision y opinion tecnica previa. Supervisor: opinion tecnica previa del proyectista u organo competente, sin autoevaluacion | PROP | Reglamento, art. 194.2 c-g; Opinion D000092, 2.9 A-C y 3.9-3.11 |
| E-GPAR | 59 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva | ¿Que opiniones corresponden? | E-TSUP [Elaboro contratista o entidad]; E-T5A [Opinion tecnica previa] |  |  |  |  |  | Si elaboro el supervisor, solo opinion tecnica previa del proyectista u organo competente. Si elaboro el contratista, la opinion tecnica previa se emite en el mismo plazo de diez dias de supervision | PROP | Reglamento, art. 194.2 e-g; Opinion D000092, 2.8-2.9 |
| E-TSUP | 60 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-envio | Coordinar presentacion a supervision | E-MSUP |  |  | sale: Expediente presentado |  |  | Presentacion a entidad y supervision cuando elabora contratista; si elabora entidad, remite al supervisor | PROP | Opinion D000092, 2.4 nota 5; 2.9 A y C |
| E-MSUP | 61 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-recepcion | Opinion de supervision recibida | E-GJOIN |  |  | entra: Opinion de supervision |  |  |  | PROP | DEC-046 |
| E-GJOIN | 62 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva |  | E-G7 |  |  |  |  |  | Reune opiniones activadas segun elaborador; no abre un nuevo plazo | PROP | DEC-046 |
| S-E3 | 63 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Expediente para evaluacion recibido | S-T3 |  |  | entra: Expediente presentado |  |  |  | PROP | Opinion D000092, 2.9 A y C |
| S-T3 | 64 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Evaluar expediente ajeno y emitir opinion | S-F3 |  |  |  | Si elaboro contratista: 10 dias desde el dia siguiente de presentacion (art. 194.2 e); si elaboro entidad: plazo correspondiente por precisar |  | Supervisor opina cuando elaboro contratista o entidad; no revisa expediente elaborado por el mismo | NORM | Reglamento, art. 194.2 e; Opinion D000092, 2.9 A y C |
| S-F3 | 65 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Opinion de supervision remitida |  |  |  | sale: Opinion de supervision |  |  |  | PROP | Reglamento, art. 194.2 e-f |
| X-MR | 76 | Elaborador del adicional segun bases: entidad, contratista o supervisor | Responsable de elaborar el expediente (una alternativa por caso) | mensaje-recepcion | Ratificacion comunicada para presentar | X-F1 |  |  | entra: Ratificacion de necesidad |  |  | Condicion de presentacion; no nuevo inicio del computo | PROP | Opinion D000092, 2.1 nota 4, 2.2-2.3 |
| E-ENOT | 89 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | inicio-mensaje | Anotacion comunicada a SGGOS | E-GNOT |  |  | entra: Anotacion; entra: Identificacion del elaborador segun bases |  |  | La recepcion no modifica la fecha legal de la anotacion | PROP | Precision del usuario, 2026-11-19; Reglamento, art. 194.2 a-d |
| E-GNOT | 90 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | compuerta | ¿Elaborador conoce la anotacion? | E-FNOT [Si]; E-TNOT [No] |  |  |  |  |  | Verificar bases: si anoto el contratista y elabora este, no hay segunda notificacion; si anoto supervision y elabora contratista, comunicarle | PROP | Reglamento, art. 194.2 c; precision del usuario, 2026-11-19 |
| E-TNOT | 91 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | mensaje-envio | Avisar anotacion y encargo al elaborador | E-FNOT |  |  | sale: Anotacion y antecedentes |  |  | Avisar de inmediato a SGE si las bases asignan elaboracion a la entidad, o a otro elaborador que desconozca la anotacion; este aviso no inicia ni suspende los 15 dias | PROP | Reglamento, art. 194.2 a-d; Opinion D000092, 2.1-2.3; ROF GRH, arts. 95-96 |
| E-FNOT | 92 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | fin | Inicio comunicado o conocido |  |  |  |  |  |  |  | PROP | Cierre del aviso operativo; no es aprobacion |
| E-GPRO | 77 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | compuerta | ¿Corresponde opinion del proyectista? | E-TPRO [Si]; E-GEX [No] |  |  |  |  |  | No mas de un anio desde conformidad del expediente original | PROP | Opinion D000092, 2.8-2.9 |
| E-TPRO | 78 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | mensaje-envio | Solicitar opinion al proyectista | E-MPRO |  |  | sale: Expediente del adicional |  |  |  | PROP | Opinion D000092, 2.8-2.9 |
| E-MPRO | 79 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | mensaje-recepcion | Opinion del proyectista recibida | E-GJOIN |  |  | entra: Opinion del proyectista |  |  |  | PROP | Opinion D000092, 2.8-2.9 |
| E-GEX | 80 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | compuerta | ¿El expediente lo elaboro la entidad? | E-TEX [Si]; E-T5 [No] |  |  |  |  |  |  | PROP | Opinion D000092, 2.8-2.9 |
| E-TEX | 81 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | tarea-usuario | Documentar supuesto de opinion inoficiosa | E-GJOIN |  |  |  |  |  | No auto-revisar: supuesto 2.8; conservar supervision. Controles independientes de DEC-038 segun riesgo | PROP | Opinion D000092, 2.8-2.9 |
| E-EDP | 82 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Sustento de deductivo puro recibido | E-T1 |  |  | entra: Sustento y respuesta de consulta cuando exista |  |  |  | PROP | DEC-047 |
| E-TVIN | 83 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Identificar adicional y deductivo vinculante | E-G6 |  |  |  |  |  | Evaluacion conjunta; acreditar vinculo de sustitucion. No restar reducciones independientes | PROP | DEC-047 |
| E-TDP | 84 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Precisar naturaleza y sustento del deductivo puro | E-GDP |  |  |  |  |  | EVIDENCIA-INSUFICIENTE sobre ruta autonoma; no aplicar plazos 15 y 10 por analogia | PROP | DEC-047 |
| E-GDP | 85 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Corresponde reduccion de prestaciones? | E-FRED [Si]; E-FDP [No o no acreditado] |  |  |  |  |  |  | PROP | DEC-047 |
| E-FRED | 86 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Caso clasificado para S4.3.2.7 |  |  |  | sale: Sustento y clasificacion; sin decision de fondo |  |  |  | PROP | DEC-047 |

## Mensajes

| Desde | Hacia | Nombre |
| --- | --- | --- |
| R-F1 | S-E1 | Sustento de necesidad |
| S-F1 | E-E1 | Necesidad ratificada |
| R-F1 | E-ENOT | Anotacion de necesidad comunicada a SGGOS |
| S-T0 | E-ENOT | Anotacion de supervision comunicada a SGGOS |
| E-TNOT | X-E1 | Anotacion y encargo comunicados al elaborador distinto del anotante |
| E-T4 | X-MR | Ratificacion comunicada |
| X-F1 | E-M2 | Expediente tecnico |
| E-T8 | Contraloria General de la Republica | Solicitud de autorizacion |
| Contraloria General de la Republica | E-M1 | Pronunciamiento |
| S4.3.2.2 Atencion de consultas de obra | R-E1 | Respuesta notificada como antecedente |
| E-TSUP | S-E3 | Expediente presentado para pronunciamiento |
| S-F3 | E-MSUP | Opinion de supervision |
| E-TNEV | Elaborador del adicional segun bases: entidad, contratista o supervisor | Resultado de evaluacion tecnica preliminar |
| E-TNEV | Ejecutor de obra, segun regimen | Resultado de evaluacion tecnica preliminar |
| E-TPRO | Proyectista | Solicitud de opinion previa |
| Proyectista | E-MPRO | Opinion tecnica |
| E-FRED | S4.3.2.7 Gestion de reducciones de prestaciones | Sustento reclasificado como reduccion |
| E-TEMER | Supervisor o inspector de obra | Autorizacion de ejecucion inmediata |
