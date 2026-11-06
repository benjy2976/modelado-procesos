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
fecha_actualizacion: 2026-11-06
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-3
---

# S4.3.2.3 Gestion de modificaciones de alcance

Sube a: [S4.3.2.3 Gestion de modificaciones de alcance](00-S4-3-2-3-gestion-modificaciones-alcance.md)

Propuesta realineada mediante `DEC-041`. Conserva del modelo anterior solo el circuito comun y las variantes de alcance. Ampliacion, suspension y paralizacion o reinicio se trasladan a S4.3.2.4, S4.3.2.5 y S4.3.2.6.

Notas que no se dibujan:

- La instancia es una por solicitud, necesidad o causal de modificacion de alcance.
- `MOD-ALC-*` identifica variantes internas de modelamiento, no codigos de nivel 4.
- Cuaderno de Incidencias es la denominacion institucional uniforme adoptada para este modelo, incluso en administracion directa; las fuentes de esa modalidad pueden denominarlo cuaderno de obra.
- Ejecutor de obra agrupa al residente y, cuando una actividad contractual lo exige, al contratista o su representante legal. Control de obra es una abstraccion funcional ejercida alternativamente por supervisor contratado o inspector de la entidad; no los convierte en una misma organizacion ni supone que concurran.
- Elaboracion del expediente tecnico conserva un pool funcional mientras no se confirme si el equipo elaborador pertenece al ejecutor, al GORE o a un tercero. Esa adscripcion es `EVIDENCIA-INSUFICIENTE`; el pool no atribuye independencia juridica.
- SGGOS — Coordinador de obra puede verificar integridad y realizar la clasificacion inicial del alcance original, la causal y la figura cuando no se requiere juicio tecnico especializado.
- Cuando la materia excede su competencia, interviene el especialista competente. El coordinador no sustituye la revision tecnica de especialidad, el control contractual y de costos ni la decision formal.
- El carril Titular de la competencia o autoridad delegada evita fijar una autoridad que dependa de delegaciones variables.
- Quien elabora no emite la unica opinion tecnica que sustenta la decision.

## Pools

| Pool | Carriles |
|---|---|
| Ejecutor de obra | Residente de obra |
| Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad |
| Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental; SGGOS — Coordinador de obra; SGGOS — Control contractual y costos; SGE — Coordinacion de revision tecnica; SGE — Especialista tecnico competente; Subgerencia de Presupuesto Publico; Gerencia Regional de Asesoria Juridica; Titular de la competencia o autoridad delegada |
| Elaboracion del expediente tecnico | Equipo elaborador competente; adscripcion pendiente de confirmar |
| Contraloria General de la Republica |  |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R-E1 | Ejecutor de obra | Residente de obra | inicio-condicional | Necesidad de modificar el alcance identificada | R-T1 |  |  |  |  |  |  | NORM | Reglamento, arts. 194 y 197; Directiva 017-2023-CG, num. 7.3.6 |
| R-T1 | Ejecutor de obra | Residente de obra | tarea-usuario | Registrar y sustentar la necesidad en el Cuaderno de Incidencias | R-F1 |  |  | sale: Registro y sustento de necesidad |  |  |  | NORM | Reglamento, arts. 188.3, 194.2 a y 197.1; Directiva 017-2023-CG, nums. 7.3.2 y 7.3.6 |
| R-F1 | Ejecutor de obra | Residente de obra | fin-mensaje | Sustento remitido |  |  |  |  |  |  |  | NORM | Reglamento, arts. 194.2 y 197.1; Directiva 017-2023-CG, num. 7.3.6 |
| S-E1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | inicio-mensaje | Sustento del residente recibido | S-G1 |  |  | entra: Registro y sustento de necesidad |  |  |  | NORM | Reglamento, arts. 186.1 y 194.2 b; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6 |
| S-E2 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | inicio-condicional | Necesidad identificada por el control de obra | S-T0 |  |  |  |  |  |  | EQ | Precision operativa del equipo; Reglamento, arts. 186-188 |
| S-T0 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | tarea-usuario | Registrar la necesidad en el Cuaderno de Incidencias | S-G1 |  |  | sale: Registro de necesidad |  |  |  | EQ | Precision operativa del equipo; Reglamento, art. 188.3; Directiva 017-2023-CG, nums. 7.3.2 y 7.3.6 |
| S-G1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | compuerta |  | S-T1 |  |  |  |  |  |  | PROP | Convergencia de origenes |
| S-T1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | tarea | Evaluar la necesidad y el riesgo para la ejecucion | S-G2 |  |  |  |  |  |  | NORM | Reglamento, arts. 187.1, 194.2 b y 197.1; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6 |
| S-G2 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | compuerta | ¿Ratifica la necesidad? | S-F1 [Si]; S-F2 [No] |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 b; Directiva 017-2023-CG, num. 7.3.6 |
| S-F1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | fin-mensaje | Necesidad ratificada y remitida |  |  |  | sale: Informe de necesidad |  |  |  | NORM | Reglamento, art. 194.2; Directiva 017-2023-CG, num. 7.3.6 |
| S-F2 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | fin | Necesidad no ratificada |  |  |  |  |  |  |  | PROP | Cierre propuesto para el control inicial |
| E-E1 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | inicio-mensaje | Expediente recibido | E-T1 |  |  | entra: Informe de necesidad |  |  |  | EQ | ROF, art. 20; DEC-037 |
| E-T1 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | tarea-usuario | Registrar y derivar a la SGGOS | E-T2 |  |  | sale: Registro y derivacion |  |  |  | NORM | ROF, art. 20 |
| E-T2 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Verificar integridad y clasificar regimen y modalidad | E-T3 |  |  | entra: Expediente |  |  |  | EQ | ROF, arts. 97-98; DEC-041 |
| E-T3 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Clasificar alcance original, causal y figura inicial | E-G0 |  |  |  |  |  | Si requiere juicio tecnico especializado, deriva al especialista competente | EQ | Precision del equipo registrada en DEC-041 |
| E-G0 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Corresponde una modificacion de alcance? | E-G2 [Si]; E-T15 [No] |  |  |  |  |  |  | PROP | Separa obligacion original, valorizacion y modificacion potencial |
| E-T15 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | tarea-usuario | Comunicar que no corresponde una modificacion de alcance | E-F3 |  |  | sale: Comunicacion |  |  |  | PROP | Resultado de clasificacion inicial; DEC-041 |
| E-F3 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | fin-mensaje | Caso clasificado fuera del proceso |  |  |  |  |  |  |  | PROP | Puede corresponder exigir cumplimiento, valorizar o derivar a otro proceso |
| E-G2 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Que figura de alcance corresponde? | MOD-ALC-ADI [Adicional]; MOD-ALC-RED [Reduccion o deductivo]; MOD-ALC-MAY [Mayores cantidades] |  |  |  |  |  |  | NORM | Ley 32069, arts. 63-64; Reglamento, arts. 109 y 194-197; Directiva 017-2023-CG, num. 7.3.6 |
| MOD-ALC-ADI | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Clasificar adicional o modificacion tecnica | E-G4 |  |  |  |  |  |  | EQ | Ley 32069, arts. 64.2-64.4; Reglamento, arts. 194-196; Directiva 017-2023-CG, num. 7.3.6 |
| MOD-ALC-RED | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Clasificar reduccion o deductivo | E-G4 |  |  |  |  |  |  | EQ | Reglamento, art. 109; Directiva 017-2023-CG, num. 7.3.6 |
| MOD-ALC-MAY | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Clasificar mayores metrados o cantidades | E-G4 |  |  |  |  |  |  | EQ | Reglamento, art. 197; Directiva 017-2023-CG, num. 7.3.6 |
| E-G4 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta |  | E-G6 |  |  |  |  |  |  | PROP | Convergencia de variantes |
| E-G6 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Requiere expediente tecnico? | E-T4 [Si]; E-G5 [No] (por defecto) |  |  |  |  |  |  | EQ | Reglamento, art. 194.2 c-g; Directiva 017-2023-CG, num. 7.3.6 |
| E-T4 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-envio | Activar al elaborador definido o designado | E-M2 |  |  | sale: Solicitud de elaboracion |  |  |  | NORM | Reglamento, art. 194.2 c; Directiva 017-2023-CG, num. 7.3.6 |
| E-M2 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-recepcion | Expediente tecnico recibido | E-T5A |  |  | entra: Expediente tecnico |  |  |  | NORM | Reglamento, art. 194.2 d-f; Directiva 017-2023-CG, num. 7.3.6 |
| E-T5A | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | tarea-usuario | Asignar u obtener revisor competente e independiente | E-T5 |  |  |  |  |  |  | EQ | ROF, arts. 95-96; Reglamento, art. 194.2 g; DEC-038 |
| E-T5 | Gobierno Regional Huanuco | SGE — Especialista tecnico competente | tarea | Evaluar la solucion y emitir opinion tecnica | E-G7 |  |  | sale: Opinion tecnica |  |  |  | NORM | Reglamento, art. 194.2 d-g; ROF, arts. 95-96; Directiva 017-2023-CG, num. 7.3.6 |
| E-G7 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | compuerta | ¿La solucion tecnica es conforme? | E-G5 [Si]; E-T16 [No] |  |  |  |  |  |  | PROP | Control tecnico independiente; DEC-038 |
| E-T16 | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | tarea-usuario | Emitir informe con observaciones | E-F2A |  |  | sale: Observaciones tecnicas |  |  |  | PROP | La subsanacion inicia una nueva presentacion |
| E-F2A | Gobierno Regional Huanuco | SGE — Coordinacion de revision tecnica | fin-mensaje | Observaciones tecnicas comunicadas |  |  |  |  |  |  |  | PROP | Producto alterno; canal documentario por confirmar |
| E-G5 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva | ¿Que controles requiere? | E-TC [C]; E-T6 [P]; E-T7 [J]; E-G5C (por defecto) |  |  |  |  |  |  | EQ | Controles combinables segun regimen, figura, impacto y riesgo; DEC-038 |
| E-TC | Gobierno Regional Huanuco | SGGOS — Control contractual y costos | tarea | Revisar metrados, precios, acumulados y consistencia contractual | E-G5C |  |  | sale: Control contractual y de costos |  |  |  | EQ | Ley 32069, arts. 63-64; Reglamento, arts. 109 y 194-197; ROF, arts. 97-98 |
| E-T6 | Gobierno Regional Huanuco | Subgerencia de Presupuesto Publico | tarea | Emitir certificacion o prevision cuando corresponda | E-G5C |  |  | sale: Control presupuestal |  |  |  | EQ | ROF, art. 51; Directiva 017-2023-CG, num. 7.3.6 |
| E-T7 | Gobierno Regional Huanuco | Gerencia Regional de Asesoria Juridica | tarea | Emitir opinion o revisar el acto cuando corresponda | E-G5C |  |  | sale: Control juridico |  |  |  | EQ | ROF, arts. 44-45; Directiva 017-2023-CG, num. 7.3.6 |
| E-G5C | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-inclusiva |  | E-T17 |  |  |  |  |  |  | PROP | Convergencia de controles activados |
| E-T17 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Consolidar controles, responsables y discrepancias resueltas | E-G8 |  |  | sale: Expediente consolidado |  |  |  | PROP | Matriz de control propuesta en DEC-038; no sustituye opiniones especializadas |
| E-G8 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Requiere autorizacion de Contraloria? | E-T8 [Si]; E-T10 [No] (por defecto) |  |  |  |  |  |  | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-T8 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Solicitar autorizacion a la Contraloria | E-M1 |  |  | sale: Solicitud de autorizacion |  |  | Unidad remitente interna pendiente de confirmar | EQ | Ley 32069, arts. 64.3 b y 64.4; EVIDENCIA-INSUFICIENTE sobre circuito interno |
| E-M1 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | mensaje-recepcion | Pronunciamiento de Contraloria recibido | E-G9 |  |  | entra: Pronunciamiento |  |  |  | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-G9 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | compuerta | ¿Autorizada? | E-T10 [Si]; E-F2B [No] |  |  |  |  |  |  | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-F2B | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | No autorizacion comunicada |  |  |  |  |  |  |  | PROP | Cierre cuando no se obtiene la autorizacion externa exigible |
| E-T10 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Resolver y emitir pronunciamiento | E-G10 |  |  | entra: Expediente consolidado; sale: Pronunciamiento |  |  |  | NORM | Ley 32069, arts. 25 y 63-64; Reglamento, arts. 109, 194 y 197; Directiva 017-2023-CG, num. 7.3.6 |
| E-G10 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | compuerta | ¿Favorable? | E-T11 [Si] (por defecto); E-F2C [No] |  |  |  |  |  |  | PROP | Rutas de decision |
| E-T11 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Actualizar registros y coordinar la comunicacion | E-F1 |  |  | sale: Registros y comunicacion |  |  |  | NORM | Directiva General de Invierte.pe, art. 33.2; ROF, art. 98 j-k; Reglamento, arts. 109.3 y 194.3; Directiva 017-2023-CG, num. 7.3.6 |
| E-F1 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Modificacion de alcance comunicada |  |  |  |  |  |  |  | PROP | Producto propuesto; canal formal por confirmar |
| E-F2C | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | Decision no favorable comunicada |  |  |  |  |  |  |  | PROP | Producto alterno |
| X-E1 | Elaboracion del expediente tecnico | Equipo elaborador competente; adscripcion pendiente de confirmar | inicio-mensaje | Elaboracion o subsanacion solicitada | X-T1 |  |  | entra: Solicitud de elaboracion |  |  |  | NORM | Reglamento, art. 194.2 c-d; Directiva 017-2023-CG, num. 7.3.6 |
| X-T1 | Elaboracion del expediente tecnico | Equipo elaborador competente; adscripcion pendiente de confirmar | tarea-usuario | Elaborar o subsanar el expediente tecnico | X-F1 |  |  | sale: Expediente tecnico |  |  |  | NORM | Reglamento, arts. 194.2 c-e y 196; Directiva 017-2023-CG, num. 7.3.6 |
| X-F1 | Elaboracion del expediente tecnico | Equipo elaborador competente; adscripcion pendiente de confirmar | fin-mensaje | Expediente tecnico presentado |  |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 d-f; Directiva 017-2023-CG, num. 7.3.6 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| R-F1 | S-E1 | Sustento de necesidad |
| S-F1 | E-E1 | Necesidad ratificada |
| E-T4 | X-E1 | Solicitud de elaboracion |
| X-F1 | E-M2 | Expediente tecnico |
| E-T8 | Contraloria General de la Republica | Solicitud de autorizacion |
| Contraloria General de la Republica | E-M1 | Pronunciamiento |


