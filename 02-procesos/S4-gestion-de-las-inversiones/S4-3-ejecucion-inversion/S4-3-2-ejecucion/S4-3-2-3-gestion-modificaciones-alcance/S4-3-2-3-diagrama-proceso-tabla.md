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
fecha_actualizacion: 2026-11-18
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-3
---

# S4.3.2.3 Gestion de modificaciones de alcance

Sube a: [S4.3.2.3 Gestion de modificaciones de alcance](00-S4-3-2-3-gestion-modificaciones-alcance.md)

Propuesta replanteada mediante `DEC-046`: adicional con su deductivo vinculado, reduccion independiente y mayores metrados tienen rutas diferenciadas. La consulta S4.3.2.2 es antecedente del circuito operativo de adicionales; no equivale a aprobacion del expediente. Se conserva el alcance de `DEC-041`. Ampliacion, suspension y paralizacion o reinicio se trasladan a S4.3.2.4, S4.3.2.5 y S4.3.2.6.

Notas que no se dibujan:

- La instancia es una por solicitud, necesidad o causal de modificacion de alcance.
- `MOD-ALC-*` identifica variantes internas de modelamiento, no codigos de nivel 4.
- Cuaderno de Incidencias es la denominacion institucional uniforme adoptada para este modelo, incluso en administracion directa; las fuentes de esa modalidad pueden denominarlo cuaderno de obra.
- Ejecutor de obra, segun regimen agrupa al residente y, cuando una actividad contractual lo exige, al contratista o su representante legal. Supervisor o inspector de obra es una abstraccion funcional ejercida alternativamente por supervisor contratado o inspector de la entidad; no los convierte en una misma organizacion ni supone que concurran.
- Elaboracion del expediente tecnico conserva un pool funcional mientras no se confirme si el equipo elaborador pertenece al ejecutor, al GORE o a un tercero. Esa adscripcion es `EVIDENCIA-INSUFICIENTE`; el pool no atribuye independencia juridica.
- SGGOS — Coordinador de obra puede verificar integridad y realizar la clasificacion inicial del alcance original, la causal y la figura cuando no se requiere juicio tecnico especializado.
- Cuando la materia excede su competencia, interviene el especialista competente. El coordinador no sustituye la revision tecnica de especialidad, el control contractual y de costos ni la decision formal.
- El carril Titular de la competencia o autoridad delegada evita fijar una autoridad que dependa de delegaciones variables.
- Quien elabora no emite la unica opinion tecnica que sustenta la decision.

- Los plazos de 15 y 10 dias se aplican exclusivamente al supuesto del art. 194 indicado en cada tarea; no reinician con la carta de encargo ni con una subsanacion. La Opinion D000092 precisa tambien la secuencia para elaboracion por entidad; se conserva pendiente la precision del plazo numerico de supervision en esa variante.
- El detalle de este lote corresponde a Ley 32069, solo construccion, procedimiento ordinario. Otros regimenes, sistemas de entrega y emergencia se identifican y quedan pendientes de desarrollo especifico, sin aplicarles estos plazos por analogia.
- Fuentes, vigencia, condiciones y limites de la propuesta: [Sustento](S4-3-2-3-sustento.md#replanteamiento-del-circuito-de-alcance---2026-11-18).

- La respuesta de consultas ingresa antes de la anotacion especifica de necesidad. Si ya existe una anotacion valida, se conserva su fecha; no se repite para reiniciar el computo. La elaboracion transcurre mientras se tramita la ratificacion; solo la presentacion efectiva queda condicionada a esta (Opinion D000092, 2.1-2.3).

## Pools

| Pool | Carriles |
|---|---|
| Ejecutor de obra, segun regimen | Residente de obra |
| Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad |
| Gobierno Regional Huanuco | OACGD — Registro documentario; SGGOS — Coordinador de obra; SGGOS — Control contractual y costos; SGE — Coordinacion de revision tecnica; SGE — Especialista tecnico competente; Subgerencia de Presupuesto Publico — Control presupuestal; GRAJ — Asesoria Juridica; Titular de la competencia o autoridad delegada |
| Elaboracion del expediente tecnico | Equipo elaborador competente (adscripcion pendiente) |
| Contraloria General de la Republica |  |
| S4.3.2.2 Atencion de consultas de obra |  |
| Proyectista |  |

## Elementos
| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R-E1 | 1 | Ejecutor de obra, segun regimen | Residente de obra | inicio-mensaje | Respuesta de consulta recibida | R-T1 |  |  | entra: Respuesta S4.3.2.2 |  |  |  | EQ | Usuario 2026-11-18; Opinion D000083, 2.2.1 y 3.3 |
| R-T1 | 2 | Ejecutor de obra, segun regimen | Residente de obra | tarea-usuario | Anotar necesidad del adicional en cuaderno | R-F1 |  |  | entra: Respuesta de consulta; sale: Anotacion de necesidad |  |  | Hito del computo de 5 y 15 dias: dia siguiente de esta anotacion; conservar fecha si ya existe | NORM | Reglamento, art. 194.2 a; Opinion D000092, 2.1-2.3 y 3.1-3.3 |
| R-F1 | 3 | Ejecutor de obra, segun regimen | Residente de obra | fin-mensaje | Anotacion y antecedentes remitidos |  |  |  |  |  |  |  | NORM | Reglamento, arts. 194.2 y 197.1; Directiva 017-2023-CG, num. 7.3.6 |
| S-E1 | 4 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Sustento del residente recibido | S-G1 |  |  | entra: Registro y sustento de necesidad |  |  |  | NORM | Reglamento, arts. 186.1 y 194.2 b; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6 |
| S-E2 | 5 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-condicional | Necesidad identificada por supervision | S-T0 |  |  |  |  |  | Origen alternativo del art. 194; consulta previa si existe. No duplicar anotacion ya valida | EQ | Precision operativa del equipo; Reglamento, arts. 186-188 |
| S-T0 | 6 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea-usuario | Registrar la necesidad en el Cuaderno de Incidencias | S-G1 |  |  | sale: Registro de necesidad |  |  | Comunicar anotacion al elaborador definido en bases; inicia computo sin esperar ratificacion | EQ | Precision operativa del equipo; Reglamento, art. 188.3; Directiva 017-2023-CG, nums. 7.3.2 y 7.3.6 |
| S-G1 | 7 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | compuerta |  | S-GFIG |  |  |  |  |  |  | PROP | Convergencia de origenes |
| S-T1 | 8 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Evaluar la necesidad y el riesgo para la ejecucion | S-G2 |  |  |  | Adicional art. 194.2 b: informe en 5 dias calendario desde el dia siguiente de la anotacion |  | No extender este plazo a reducciones ni administracion directa | NORM | Reglamento, arts. 187.1, 194.2 b y 197.1; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6 |
| S-G2 | 9 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | compuerta | ¿Ratifica la necesidad? | S-F1 [Si]; S-F2 [No] |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 b; Directiva 017-2023-CG, num. 7.3.6 |
| S-F1 | 10 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Necesidad ratificada y remitida |  |  |  | sale: Informe de necesidad |  |  |  | NORM | Reglamento, art. 194.2; Directiva 017-2023-CG, num. 7.3.6 |
| S-F2 | 11 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin | Necesidad no ratificada |  |  |  |  |  |  |  | PROP | Cierre propuesto para el control inicial |
| E-E1 | 12 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Sustento de necesidad recibido | E-T1 |  |  | entra: Informe de necesidad |  |  |  | EQ | ROF, art. 20; DEC-037 |
| E-T1 | 13 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Registrar y derivar a SGGOS por SGD | E-T2 |  |  | sale: Registro y derivacion; almacen: SGD |  |  |  | EQ | ROF, art. 20; observacion del usuario, 2026-11-10 |
| E-T2 | 14 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Verificar integridad, regimen, sistema de entrega y supuesto | E-GREG |  |  | entra: Expediente |  |  |  | EQ | ROF, arts. 97-98; DEC-041 |
| E-T3 | 15 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Clasificar alcance original, causal y figura inicial | E-G0 |  |  |  |  |  | Si requiere juicio tecnico especializado, deriva al especialista competente | EQ | Precision del equipo registrada en DEC-041 |
| E-G0 | 16 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Corresponde una modificacion de alcance? | E-G2 [Si]; E-T15 [No] |  |  |  |  |  |  | PROP | Separa obligacion original, valorizacion y modificacion potencial |
| E-T15 | 17 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Comunicar que no corresponde una modificacion de alcance | E-F3 |  |  | sale: Comunicacion |  |  |  | PROP | Resultado de clasificacion inicial; DEC-041 |
| E-F3 | 18 | Gobierno Regional Huanuco | OACGD — Registro documentario | fin-mensaje | Caso clasificado fuera del proceso |  |  |  |  |  |  |  | PROP | Puede corresponder exigir cumplimiento, valorizar o derivar a otro proceso |
| E-G2 | 19 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Que figura de alcance corresponde? | MOD-ALC-ADI [Adicional con o sin deductivo vinculado]; MOD-ALC-RED [Reduccion independiente]; MOD-ALC-MAY [Mayores metrados] |  |  |  |  |  |  | NORM | Ley 32069, arts. 63-64; Reglamento, arts. 109 y 194-197; Directiva 017-2023-CG, num. 7.3.6 |
| MOD-ALC-ADI | 20 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Identificar adicional y su deductivo vinculado | E-G4 |  |  |  |  |  |  | EQ | Ley 32069, art. 64.2-64.3; Reglamento, art. 194; DEC-046 |
| MOD-ALC-RED | 21 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Verificar sustento de reduccion independiente | E-GRED |  |  |  |  |  | Area usuaria: finalidad conservada, prestaciones no ejecutadas, divisibles y cuantificables; opinion del supervisor; limite 25 %; antes de recepcion | EQ | Reglamento, art. 109.1; responsable interno del sustento pendiente |
| MOD-ALC-MAY | 22 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Derivar solicitud de mayores metrados al control de obra | E-FMAY |  |  |  |  |  |  | PROP | Reglamento, art. 197.1-197.2; no es aprobacion previa de la entidad |
| E-G4 | 23 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta |  | E-G6 |  |  |  |  |  |  | PROP | Convergencia de variantes |
| E-G6 | 24 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Necesidad ratificada, causal y elaborador acreditados? | E-T4 [Si]; E-FPEND [No] |  |  |  |  |  | Causal indispensable; anotacion e informe; confirmar elaborador segun bases y evitar duplicar el encargo de consultas | PROP | Reglamento, art. 194.1 y 194.2 a-d; bases del contrato |
| E-T4 | 25 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-envio | Comunicar ratificacion al elaborador | E-M2 |  |  | sale: Ratificacion y confirmacion del elaborador |  |  | No reinicia los 15 dias; encargo segun bases y antecedente de consulta | NORM | Opinion D000092, 2.1 nota 4, 2.2 y 3.2 |
| E-M2 | 26 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-recepcion | Expediente del adicional presentado a evaluacion | E-GEL |  |  | entra: Expediente tecnico |  |  |  | NORM | Reglamento, art. 194.2 d-f; Directiva 017-2023-CG, num. 7.3.6 |
| E-T5A | 27 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | tarea-usuario | Determinar opinion tecnica aplicable | E-GPRO |  |  |  |  |  | Proyectista en primera instancia si no transcurrio mas de un anio; en defecto organo competente | EQ | Opinion D000092, 2.8-2.9 y 3.8-3.11 |
| E-T5 | 28 | Gobierno Regional Huanuco | SGE — Especialista tecnico competente | tarea | Emitir opinion del organo competente | E-GJOIN |  |  | sale: Opinion tecnica | Si elaboro contratista: mismo plazo de supervision |  |  | PROP | Opinion D000092, 2.8 y 2.9 A-B; DEC-038 |
| E-G7 | 29 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | compuerta | ¿Evaluacion tecnica favorable? | E-G5 [Si]; E-T16 [No] |  |  |  |  |  | Resultado desfavorable tambien se eleva para decision; no terminar solo en opinion | PROP | Control tecnico independiente; DEC-038 |
| E-T16 | 30 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | tarea-usuario | Integrar observaciones para decision | E-G5 |  |  | sale: Observaciones tecnicas |  |  | Subsanacion y efecto sobre plazos pendientes; no se reinicia automaticamente el plazo normativo | PROP | Propuesta operativa; Reglamento, art. 194.2 f; no sustituir resolucion por informe |
| E-G5 | 32 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva | ¿Que controles requiere? | E-TC [C]; E-T6 [P]; E-T7 [J] |  |  |  |  |  | C siempre; P y J segun figura. Controles no amplian el plazo legal | EQ | DEC-038; control contractual obligatorio en esta propuesta |
| E-TC | 33 | Gobierno Regional Huanuco | SGGOS — Control contractual y costos | tarea | Verificar monto, precios, deductivo vinculado y acumulados | E-G5C |  |  | sale: Control contractual y de costos |  |  | No descontar una reduccion independiente como deductivo vinculado sin sustento | EQ | Ley 32069, arts. 63-64; Reglamento, arts. 109 y 194-197; ROF, arts. 97-98 |
| E-T6 | 34 | Gobierno Regional Huanuco | Subgerencia de Presupuesto Publico — Control presupuestal | tarea | Emitir certificacion o prevision cuando corresponda | E-G5C |  |  | sale: Control presupuestal |  |  |  | EQ | ROF, art. 51; Directiva 017-2023-CG, num. 7.3.6 |
| E-T7 | 35 | Gobierno Regional Huanuco | GRAJ — Asesoria Juridica | tarea | Emitir opinion o revisar el acto cuando corresponda | E-G5C |  |  | sale: Control juridico |  |  |  | EQ | ROF, arts. 44-45; Directiva 017-2023-CG, num. 7.3.6 |
| E-G5C | 36 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva |  | E-T17 |  |  |  |  |  |  | PROP | Convergencia de controles activados |
| E-T17 | 37 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Consolidar controles, responsables y discrepancias resueltas | E-G8 |  |  | sale: Expediente consolidado |  |  |  | PROP | Matriz de control propuesta en DEC-038; no sustituye opiniones especializadas |
| E-G8 | 38 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Adicional sujeto a autorizacion de Contraloria? | E-T8 [Si]; E-T10 [No] (por defecto) |  |  |  |  |  | Reduccion independiente no sigue esta rama; verificar autoridad y umbral del adicional | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-T8 | 39 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Solicitar autorizacion a la Contraloria | E-M1 |  |  | sale: Solicitud de autorizacion |  |  | Unidad remitente interna pendiente de confirmar | EQ | Ley 32069, arts. 64.3 b y 64.4; EVIDENCIA-INSUFICIENTE sobre circuito interno |
| E-M1 | 40 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | mensaje-recepcion | Pronunciamiento de Contraloria recibido | E-G9 |  |  | entra: Pronunciamiento |  |  |  | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-G9 | 41 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | compuerta | ¿Autorizada? | E-T10 [Si]; E-F2B [No] |  |  |  |  |  |  | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-F2B | 42 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | No autorizacion comunicada |  |  |  |  |  |  |  | PROP | Cierre cuando no se obtiene la autorizacion externa exigible |
| E-T10 | 43 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Emitir y notificar resolucion segun figura | E-G10 |  |  | entra: Expediente consolidado; sale: Pronunciamiento | Art. 194.2 f: 12 dias habiles desde opinion del supervisor o expediente elaborado por este |  | 12 dias habiles del tramite institucional, desde dia siguiente de opinion del supervisor o expediente elaborado por este; no aplica a reduccion | NORM | Reglamento, art. 194.2 f; Opinion D000092, 2.9 y 3.9-3.11 |
| E-G10 | 44 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | compuerta | ¿Favorable? | E-T11 [Si] (por defecto); E-F2C [No] |  |  |  |  |  |  | PROP | Rutas de decision |
| E-T11 | 45 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Actualizar registros y coordinar la comunicacion | E-F1 |  |  | sale: Registros y comunicacion |  |  | Verificar canal vigente SEACE/Pladicop o transitorio contractual; no presumir implementacion actual | NORM | Opinion D000092, 2.11 y 3.14-3.15; Reglamento, art. 109.3; registros de inversion aplicables |
| E-F1 | 46 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Modificacion de alcance comunicada |  |  |  |  |  |  |  | PROP | Producto propuesto; canal formal por confirmar |
| E-F2C | 47 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | Decision no favorable comunicada |  |  |  |  |  |  |  | PROP | Producto alterno |
| X-E1 | 48 | Elaboracion del expediente tecnico | Equipo elaborador competente (adscripcion pendiente) | inicio-mensaje | Anotacion y antecedentes recibidos | X-T1 |  |  | entra: Anotacion de necesidad; entra: Respuesta de consulta y bases |  |  |  | NORM | Opinion D000092, 2.1-2.3; propuesta de intercambio con elaborador |
| X-T1 | 49 | Elaboracion del expediente tecnico | Equipo elaborador competente (adscripcion pendiente) | tarea-usuario | Elaborar expediente del adicional y deductivo vinculado | X-MR |  |  | sale: Expediente tecnico | 15 dias calendario desde el dia siguiente de la anotacion; necesidad ratificada |  | Elaboracion dentro del computo iniciado; presentacion condicionada a ratificacion; plazo adicional solo otorgado con sustento | NORM | Reglamento, art. 194.2 c-d; Opinion D000092, 2.1-2.7 |
| X-F1 | 50 | Elaboracion del expediente tecnico | Equipo elaborador competente (adscripcion pendiente) | fin-mensaje | Expediente tecnico presentado |  |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 d-f; Directiva 017-2023-CG, num. 7.3.6 |
| E-E2 | 51 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Sustento de reduccion recibido | E-T1 |  |  | entra: Sustento de reduccion independiente |  |  |  | PROP | Reglamento, art. 109; entrada alternativa propuesta |
| E-GREG | 52 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Ley 32069, solo construccion y caso ordinario? | E-T3 [Si]; E-FPEND [Otro regimen o supuesto] |  |  |  |  |  |  | PROP | DEC-046 |
| E-FPEND | 53 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin | Caso pendiente de completar sustento o ruta especifica |  |  |  |  |  |  | EVIDENCIA-INSUFICIENTE; no es aprobacion ni denegacion de fondo | PROP | DEC-046 |
| E-GRED | 56 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Sustento de reduccion completo? | E-G5 [Si]; E-FPEND [No] |  |  |  |  |  |  | PROP | Reglamento, art. 109.1; propuesta de control documental |
| E-FMAY | 57 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Solicitud derivada sin aprobar ejecucion |  |  |  | sale: Solicitud de mayores metrados |  |  |  | PROP | Reglamento, art. 197.1-197.2 |
| E-GEL | 58 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Elaborador acreditado segun bases? | E-GPAR [Si]; E-FPEND [No] |  |  |  |  |  | No imponer al supervisor diez dias para revisar su propio expediente | PROP | Opinion D000092, 2.9 A-C y 3.9-3.11 |
| E-GPAR | 59 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva | ¿Que opiniones corresponden? | E-TSUP [Contratista o entidad]; E-T5A [Siempre: verificar opinion previa] |  |  |  |  |  | Seleccion por elaborador; cuando es contratista, ambas opiniones tienen el mismo plazo | PROP | Opinion D000092, 2.8-2.9 |
| E-TSUP | 60 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-envio | Coordinar presentacion a supervision | E-MSUP |  |  | sale: Expediente presentado |  |  | Presentacion a entidad y supervision cuando elabora contratista; si elabora entidad, remite al supervisor | PROP | Opinion D000092, 2.4 nota 5; 2.9 A y C |
| E-MSUP | 61 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-recepcion | Opinion de supervision recibida | E-GJOIN |  |  | entra: Opinion de supervision |  |  |  | PROP | DEC-046 |
| E-GJOIN | 62 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva |  | E-G7 |  |  |  |  |  | Reune opiniones activadas segun elaborador; no abre un nuevo plazo | PROP | DEC-046 |
| S-E3 | 63 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Expediente para evaluacion recibido | S-T3 |  |  | entra: Expediente presentado |  |  |  | PROP | Opinion D000092, 2.9 A y C |
| S-T3 | 64 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Evaluar expediente y emitir pronunciamiento | S-F3 |  |  |  | Contratista: 10 dias calendario desde el dia siguiente de presentacion; entidad: plazo correspondiente por precisar |  | No se omite pronunciamiento por elaboracion de entidad | NORM | Reglamento, art. 194.2 e; Opinion D000092, 2.9 A y C |
| S-F3 | 65 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Opinion de supervision remitida |  |  |  | sale: Opinion de supervision |  |  |  | PROP | Reglamento, art. 194.2 e-f |
| S-GFIG | 66 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | compuerta | ¿Solicitud de mayores metrados del art. 197? | S-TMM [Si]; S-T1 [No] |  |  |  |  |  | Solo precios unitarios y sistemas del art. 197; no generalizar a administracion directa | PROP | DEC-046 |
| S-EMM | 67 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Solicitud de mayores metrados derivada | S-TMM |  |  | entra: Solicitud de mayores metrados |  |  |  | PROP | DEC-046 |
| S-TMM | 68 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Verificar mayores metrados, modalidad y acumulados | S-GMM |  |  |  |  |  |  | NORM | Reglamento, art. 197.1 |
| S-GMM | 69 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | compuerta | ¿Corresponde autorizar mayores metrados? | S-AMM [Si]; S-FNMM [No] |  |  |  |  |  |  | PROP | Reglamento, art. 197.1 y 197.4 |
| S-AMM | 70 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea-usuario | Autorizar ejecucion en Cuaderno de Incidencias | S-FMM |  |  | sale: Autorizacion de mayores metrados |  |  |  | NORM | Reglamento, art. 197.1 |
| S-FMM | 71 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Mayores metrados autorizados para ejecucion |  |  |  |  |  |  | No equivale a autorizacion de pago | PROP | Reglamento, art. 197.1-197.2 |
| S-FNMM | 72 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin | Solicitud no autorizada o pendiente de reclasificar |  |  |  |  |  |  | Si supera limite, aplicar art. 197.4; no habilitar ejecucion por esta ruta | PROP | DEC-046 |
| R-EMM | 73 | Ejecutor de obra, segun regimen | Residente de obra | inicio-mensaje | Autorizacion de mayores metrados recibida | R-TMM |  |  |  |  |  |  | PROP | DEC-046 |
| R-TMM | 74 | Ejecutor de obra, segun regimen | Residente de obra | tarea | Ejecutar y sustentar mayores metrados del periodo | R-FMM |  |  | sale: Sustento para valorizacion |  |  |  | NORM | Reglamento, art. 197.2 |
| R-FMM | 75 | Ejecutor de obra, segun regimen | Residente de obra | fin-mensaje | Mayores metrados remitidos a valorizacion |  |  |  |  |  |  | Interfaz con control periodico; el pago requiere autorizacion de la autoridad de gestion administrativa | PROP | Reglamento, arts. 197.2 y 210 |
| X-MR | 76 | Elaboracion del expediente tecnico | Equipo elaborador competente (adscripcion pendiente) | mensaje-recepcion | Ratificacion comunicada para presentar | X-F1 |  |  | entra: Ratificacion de necesidad |  |  | Condicion de presentacion; no nuevo inicio del computo | PROP | Opinion D000092, 2.1 nota 4, 2.2-2.3 |
| E-GPRO | 77 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | compuerta | ¿Corresponde opinion del proyectista? | E-TPRO [Si]; E-GEX [No] |  |  |  |  |  | No mas de un anio desde conformidad del expediente original | PROP | Opinion D000092, 2.8-2.9 |
| E-TPRO | 78 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | mensaje-envio | Solicitar opinion al proyectista | E-MPRO |  |  | sale: Expediente del adicional |  |  |  | PROP | Opinion D000092, 2.8-2.9 |
| E-MPRO | 79 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | mensaje-recepcion | Opinion del proyectista recibida | E-GJOIN |  |  | entra: Opinion del proyectista |  |  |  | PROP | Opinion D000092, 2.8-2.9 |
| E-GEX | 80 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | compuerta | ¿El expediente lo elaboro la entidad? | E-TEX [Si]; E-T5 [No] |  |  |  |  |  |  | PROP | Opinion D000092, 2.8-2.9 |
| E-TEX | 81 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | tarea-usuario | Documentar supuesto de opinion inoficiosa | E-GJOIN |  |  |  |  |  | No auto-revisar: supuesto 2.8; conservar supervision. Controles independientes de DEC-038 segun riesgo | PROP | Opinion D000092, 2.8-2.9 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| R-F1 | S-E1 | Sustento de necesidad |
| S-F1 | E-E1 | Necesidad ratificada |
| R-F1 | X-E1 | Anotacion y antecedentes para elaboracion |
| S-T0 | X-E1 | Anotacion de necesidad identificada por supervision |
| E-T4 | X-MR | Ratificacion comunicada |
| X-F1 | E-M2 | Expediente tecnico |
| E-T8 | Contraloria General de la Republica | Solicitud de autorizacion |
| Contraloria General de la Republica | E-M1 | Pronunciamiento |

| S4.3.2.2 Atencion de consultas de obra | R-E1 | Respuesta notificada como antecedente |
| E-TSUP | S-E3 | Expediente presentado para pronunciamiento |
| S-F3 | E-MSUP | Opinion de supervision |
| E-FMAY | S-EMM | Solicitud de mayores metrados |
| S-FMM | R-EMM | Autorizacion de ejecucion de mayores metrados |
| E-TPRO | Proyectista | Solicitud de opinion previa |
| Proyectista | E-MPRO | Opinion tecnica |
