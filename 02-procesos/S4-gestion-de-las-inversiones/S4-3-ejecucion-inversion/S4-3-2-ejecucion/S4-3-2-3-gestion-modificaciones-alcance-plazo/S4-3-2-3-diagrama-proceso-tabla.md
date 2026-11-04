---
id: AP-S4-3-2-3-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.3
nivel_proceso: 3
perfil_trazado: zigzag-amplio
proceso:
  - S4.3.2.3
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-04
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-3
---

# S4.3.2.3 Gestion de modificaciones de alcance o plazo

Sube a: [S4.3.2.3 Gestion de modificaciones de alcance o plazo](00-S4-3-2-3-gestion-modificaciones-alcance-plazo.md)

Propuesta de orquestacion reconstruida a partir del Bizagi de Consultas, la normativa vigente de contrataciones publicas y administracion directa, el ROF del Gobierno Regional Huanuco y las precisiones operativas del equipo. Los roles de residente y supervisor o inspector se modelan una sola vez porque intervienen en obra con independencia de la modalidad de ejecucion; el regimen se clasifica al ingresar el expediente a la entidad y determina los requisitos, la autoridad y el acto aplicables.

Notas que no se dibujan:

- La instancia es una por solicitud, necesidad o causal de modificacion.
- `MOD-*` identifica variantes internas de modelamiento y no codigos de nivel 4.
- En una obra interviene supervisor o inspector, segun corresponda; no ambos simultaneamente. El inspector puede pertenecer al GORE, pero se representa como participante funcional separado por la autonomia tecnica del rol de control en campo. Esto no le atribuye personalidad juridica independiente.
- Tanto en contrata como en administracion directa la necesidad o causal se registra o sustenta mediante el cuaderno de incidencias o cuaderno de obra aplicable.
- El tramite interno de la entidad sigue una columna vertebral comun. La modalidad y la figura seleccionan la regla sustantiva, los documentos, la autoridad y los plazos aplicables; no seleccionan actores de obra distintos.
- El monitor controla integridad, clasificacion, trazabilidad, plazos y consolidacion del expediente. El rol Monitor del Cuaderno de Incidencias solo visualiza informacion; no sustituye al supervisor, al elaborador ni al especialista que emite la opinion tecnica.
- La necesidad se define inicialmente por el sistema, funcion o desempeño afectado. La solucion detallada, partidas, metrados, planos y especificaciones se desarrollan en el expediente tecnico de la modificacion.
- En contrata se activa al elaborador definido en las bases conforme al articulo 194.2 c del Reglamento. En administracion directa la OAD designa al responsable conforme al numeral 7.3.6 de la Directiva 017-2023-CG.
- Quien elabora no emite la unica opinion que sustenta la aprobacion. SGE conduce una revision tecnica independiente mediante un especialista competente; si no dispone de la especialidad, debe obtener apoyo o revision externa antes de emitir su opinion institucional.
- Las intervenciones de control contractual y costos, Presupuesto y GRAJ son condicionales y pueden concurrir.
- Para adicionales de solo construccion: hasta 15 % decide la autoridad de la gestion administrativa; mas de 15 % y hasta 30 %, el titular; mas de 30 % y hasta 50 % requiere autorizacion previa de la Contraloria y decision del titular; por encima de 50 % corresponde resolver el contrato.
- En mayores metrados por contrata, la supervision o inspeccion autoriza la ejecucion en el cuaderno y la entidad autoriza el pago; no existe aprobacion previa de la entidad para ejecutar.
- En administracion directa, una modificacion aprobada puede originar la actualizacion del plan de abastecimiento y requerimientos de bienes o servicios tramitados por el residente y validados por el supervisor o inspector. Esa adquisicion es una interfaz posterior con el proceso de abastecimiento y queda fuera del limite de S4.3.2.3.
- El registro en Banco de Inversiones, INFOBRAS o Pladicop se realiza solo en el sistema y oportunidad aplicables.
- La comunicacion formal de salida puede canalizarse mediante la Oficina de Atencion al Ciudadano y Gestion Documental; en este nivel se integra con la actividad de registro y comunicacion coordinada por SGGOS para evitar representar el detalle documentario como una cadena adicional.
- El reinicio posterior a una suspension o paralizacion se modela como una nueva instancia disparada por la verificacion de sus condiciones, no como una espera que mantenga abierta indefinidamente la instancia que aprobo la modificacion.

## Pools

| Pool | Carriles |
|---|---|
| Residente de obra | Residente de obra |
| Supervision o inspeccion de obra | Supervisor o inspector de obra |
| Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental; SGGOS - Monitor o gestor del expediente; SGGOS - Control contractual y costos; SGE - Coordinacion de revision tecnica; SGE - Especialista tecnico competente; Subgerencia de Presupuesto Publico; Gerencia Regional de Asesoria Juridica; Gerencia Regional de Infraestructura; Autoridad competente segun regimen, figura, umbral y delegacion |
| Elaborador definido o designado | Equipo elaborador competente |
| Contraloria General de la Republica |  |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Grupo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R-E1 | Residente de obra | Residente de obra | inicio-condicional | Necesidad o causal identificada | R-T1 |  |  |  |  |  |  |  | NORM | Reglamento, arts. 194, 197 y 200; Directiva 017-2023-CG, nums. 7.3.6-7.3.7, PDF pp. 17-18 |
| R-T1 | Residente de obra | Residente de obra | tarea-usuario | Registrar y sustentar en el cuaderno | R-F1 |  |  |  |  |  |  |  | NORM | Reglamento, arts. 188.3, 194.2 a, 197.1 y 200.1 a; Directiva 017-2023-CG, nums. 7.3.2, 7.3.6 y 7.3.7 |
| R-F1 | Residente de obra | Residente de obra | fin-mensaje | Sustento remitido |  |  |  |  |  |  |  |  | NORM | Reglamento, arts. 194.2 y 200.1; Directiva 017-2023-CG, nums. 7.3.6-7.3.7 |
| S-E1 | Supervision o inspeccion de obra | Supervisor o inspector de obra | inicio-mensaje | Sustento del residente recibido | S-G1 |  |  |  |  |  |  |  | NORM | Reglamento, arts. 186.1, 194.2 b y 200.1 b; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6-7.3.7 |
| S-E2 | Supervision o inspeccion de obra | Supervisor o inspector de obra | inicio-condicional | Necesidad identificada por control | S-T0 |  |  |  |  |  |  |  | EQ | Precision operativa del equipo; el rol de control se sustenta en Reglamento, arts. 186-188, y Directiva 017-2023-CG, num. 6.8.3 |
| S-T0 | Supervision o inspeccion de obra | Supervisor o inspector de obra | tarea-usuario | Registrar la necesidad en el cuaderno | S-G1 |  |  |  |  |  |  |  | EQ | Precision operativa del equipo; uso del cuaderno sustentado en Reglamento, art. 188.3, y Directiva 017-2023-CG, nums. 7.3.2 y 7.3.6 |
| S-G1 | Supervision o inspeccion de obra | Supervisor o inspector de obra | compuerta |  | S-T1 |  |  |  |  |  |  |  | PROP | Convergencia de origenes |
| S-T1 | Supervision o inspeccion de obra | Supervisor o inspector de obra | tarea | Evaluar la necesidad y el riesgo para la ejecucion | S-G2 |  |  |  |  |  |  |  | NORM | Reglamento, arts. 187.1, 194.2 b, 197.1 y 200.1 b; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6-7.3.8 |
| S-G2 | Supervision o inspeccion de obra | Supervisor o inspector de obra | compuerta | ¿Ratifica la necesidad? | S-F1 [Si]; S-F2 [No] |  |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 b; Directiva 017-2023-CG, nums. 7.3.6-7.3.7 |
| S-F1 | Supervision o inspeccion de obra | Supervisor o inspector de obra | fin-mensaje | Necesidad ratificada y remitida al GORE |  |  |  |  |  |  |  |  | NORM | Reglamento, arts. 194.2 y 200.1; Directiva 017-2023-CG, nums. 7.3.6-7.3.8 |
| S-F2 | Supervision o inspeccion de obra | Supervisor o inspector de obra | fin | Necesidad no ratificada |  |  |  |  |  |  |  |  | PROP | Cierre propuesto cuando el primer control tecnico no ratifica la necesidad |
| E-E1 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | inicio-mensaje | Expediente recibido | E-T1 |  |  |  |  |  |  |  | EQ | ROF, art. 20; Bizagi de Consultas; DEC-032 |
| E-T1 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | tarea-usuario | Registrar y derivar a la SGGOS | E-T2 |  |  |  |  |  |  |  | NORM | ROF, art. 20 |
| E-T2 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | tarea-usuario | Revisar integridad y clasificar regimen y modalidad | E-T3 |  |  |  |  |  |  |  | EQ | ROF, arts. 97-98; Directiva 017-2025-OECE-CD, num. 10.3 C; precision operativa del equipo |
| E-T3 | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | tarea | Analizar alcance original, causal y figura posible | E-G0 |  |  |  |  |  |  |  | EQ | Ley 32069, arts. 63-64; Reglamento, arts. 158, 161, 194-197 y 210; ROF, arts. 97-98; precision operativa del equipo |
| E-G0 | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | compuerta | ¿Corresponde tramitar una modificacion? | E-G1 [Si]; E-T15 [No] |  |  |  |  |  |  |  | PROP | Separa obligacion original, valorizacion o mejora no admisible de una modificacion potencial; DEC-038 |
| E-T15 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | tarea-usuario | Notificar que no corresponde una modificacion | E-F3 |  |  |  |  |  |  |  | EQ | Resultado del control de admisibilidad contractual; precision operativa del equipo |
| E-F3 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | fin-mensaje | Caso clasificado fuera de modificacion |  |  |  |  |  |  |  |  | PROP | Puede corresponder exigir cumplimiento, tramitar valorizacion o derivar a otra figura |
| E-G1 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | compuerta | ¿Que modifica? | E-G2 [Alcance]; E-G3 [Plazo] |  |  |  |  |  |  |  | PROP | Agrupacion del proceso adoptada en DEC-032 |
| E-G2 | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | compuerta | ¿Que figura corresponde? | MOD-ALC-ADI [Adicional]; MOD-ALC-RED [Reduccion o deductivo]; MOD-ALC-MAY [Mayores cantidades] |  |  |  |  |  |  |  | NORM | Ley 32069, arts. 63-64; Reglamento, arts. 109 y 194-197; Directiva 017-2023-CG, num. 7.3.6 |
| MOD-ALC-ADI | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | tarea | Clasificar adicional o modificacion tecnica | E-G4 |  |  |  |  |  |  |  | EQ | Ley 32069, arts. 64.2-64.4; Reglamento, arts. 194-196; Directiva 017-2023-CG, num. 7.3.6; asignacion funcional propuesta |
| MOD-ALC-RED | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | tarea | Clasificar reduccion o deductivo | E-G4 |  |  |  |  |  |  |  | EQ | Reglamento, art. 109; Directiva 017-2023-CG, num. 7.3.6; asignacion funcional propuesta |
| MOD-ALC-MAY | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | tarea | Clasificar mayores metrados o cantidades | E-G4 |  |  |  |  |  |  |  | EQ | Reglamento, art. 197; Directiva 017-2023-CG, num. 7.3.6; asignacion funcional propuesta |
| E-G3 | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | compuerta | ¿Que figura de plazo corresponde? | MOD-PLA-AMP [Ampliacion]; MOD-PLA-SUS [Suspension o paralizacion]; MOD-PLA-INT [Intensificacion] |  |  |  |  |  |  |  | NORM | Reglamento, arts. 107, 191-192 y 198-202; Directiva 017-2023-CG, num. 7.3.7 |
| MOD-PLA-AMP | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | tarea | Clasificar ampliacion de plazo | E-G4 |  |  |  |  |  |  |  | EQ | Reglamento, arts. 198, 200 y 201; Directiva 017-2023-CG, num. 7.3.7; asignacion funcional propuesta |
| MOD-PLA-SUS | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | tarea | Clasificar suspension, paralizacion o reinicio | E-G4 |  |  |  |  |  |  |  | EQ | Reglamento, arts. 107 y 202; Directiva 017-2023-CG, num. 7.3.7; asignacion funcional propuesta |
| MOD-PLA-INT | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | tarea | Clasificar intensificacion del programa | E-G4 |  |  |  |  |  |  |  | EQ | Reglamento, arts. 191-192; aplica solo al regimen que contemple esta figura |
| E-G4 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | compuerta |  | E-G6 |  |  |  |  |  |  |  | PROP | Convergencia de variantes |
| E-G6 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | compuerta | ¿Requiere expediente tecnico? | E-T4 [Si]; E-G5 [No] (por defecto) |  |  |  |  |  |  |  | EQ | Reglamento, art. 194.2 c-g; Directiva 017-2023-CG, num. 7.3.6; depende del regimen y figura |
| E-T4 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | mensaje-envio | Activar elaborador | E-M2 |  |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 c; Directiva 017-2023-CG, num. 7.3.6 |
| E-M2 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | mensaje-recepcion | Expediente tecnico recibido | E-T5A |  |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 d-f; Directiva 017-2023-CG, num. 7.3.6 |
| E-T5A | Gobierno Regional Huanuco | SGE - Coordinacion de revision tecnica | tarea-usuario | Asignar u obtener revisor competente e independiente | E-T5 |  |  |  |  |  |  |  | EQ | ROF, arts. 95-96; Reglamento, art. 194.2 g; regla de independencia propuesta en DEC-038 |
| E-T5 | Gobierno Regional Huanuco | SGE - Especialista tecnico competente | tarea | Evaluar la solucion y emitir opinion tecnica | E-G7 |  |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 d-g; ROF, arts. 95-96; Directiva 017-2023-CG, num. 7.3.6 |
| E-G7 | Gobierno Regional Huanuco | SGE - Coordinacion de revision tecnica | compuerta | ¿La solucion tecnica es conforme? | E-G5 [Si]; E-T16 [No] |  |  |  |  |  |  |  | PROP | Segundo nivel de control tecnico independiente; DEC-038 |
| E-T16 | Gobierno Regional Huanuco | SGE - Coordinacion de revision tecnica | tarea-usuario | Emitir informe con observaciones | E-F2A |  |  |  |  |  |  |  | PROP | La subsanacion posterior inicia una nueva presentacion del expediente observado |
| E-F2A | Gobierno Regional Huanuco | SGE - Coordinacion de revision tecnica | fin-mensaje | Observaciones tecnicas notificadas |  |  |  |  |  |  |  |  | PROP | Producto alterno que permite una posterior subsanacion; la salida formal puede canalizarse por la OACGD |
| E-G5 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | compuerta-inclusiva | ¿Que controles requiere? | E-TC [C]; E-T6 [P]; E-T7 [J]; E-G5C (por defecto) |  |  |  |  |  |  |  | EQ | C: contractual y costos; P: presupuesto; J: juridico. Los controles pueden combinarse segun regimen, figura, impacto y riesgo; DEC-038 |
| E-TC | Gobierno Regional Huanuco | SGGOS - Control contractual y costos | tarea | Revisar metrados, precios, acumulados y consistencia contractual | E-G5C |  |  |  |  |  |  |  | EQ | Ley 32069, arts. 63-64; Reglamento, arts. 109, 194-197 y 210; ROF, arts. 97-98 |
| E-T6 | Gobierno Regional Huanuco | Subgerencia de Presupuesto Publico | tarea | Emitir certificacion o prevision | E-G5C |  |  |  |  |  |  |  | EQ | ROF, art. 51; Reglamento, art. 191.3; Directiva 017-2023-CG, num. 7.3.6 |
| E-T7 | Gobierno Regional Huanuco | Gerencia Regional de Asesoria Juridica | tarea | Emitir opinion o revisar el acto | E-G5C |  |  |  |  |  |  |  | EQ | ROF, arts. 44-45; Directiva 017-2023-CG, num. 7.3.6; Bizagi de Consultas |
| E-G5C | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | compuerta-inclusiva |  | E-T17 |  |  |  |  |  |  |  | PROP | Convergencia de controles activados |
| E-T17 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | tarea-usuario | Consolidar controles, responsables y discrepancias resueltas | E-G8 |  |  |  |  |  |  |  | PROP | Matriz de control propuesta en DEC-038; no sustituye las opiniones especializadas |
| E-G8 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | compuerta | ¿Requiere autorizacion de Contraloria? | E-T8 [Si]; E-T9 [No] (por defecto) |  |  |  |  |  |  |  | NORM | Clasificacion por regimen, figura y umbral; Ley 32069, arts. 64.3 b y 64.4 |
| E-T8 | Gobierno Regional Huanuco | Gerencia Regional de Infraestructura | tarea-usuario | Solicitar autorizacion a la Contraloria | E-M1 |  |  |  |  |  |  |  | EQ | Ley 32069, arts. 64.3 b y 64.4; unidad remitente pendiente de validar |
| E-M1 | Gobierno Regional Huanuco | Gerencia Regional de Infraestructura | mensaje-recepcion | Pronunciamiento recibido | E-G9 |  |  |  |  |  |  |  | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-G9 | Gobierno Regional Huanuco | Gerencia Regional de Infraestructura | compuerta | ¿Autorizada? | E-T9 [Si]; E-F2B (por defecto) |  |  |  |  |  |  |  | NORM | Ley 32069, arts. 64.3 b y 64.4 |
| E-F2B | Gobierno Regional Huanuco | Gerencia Regional de Infraestructura | fin-mensaje | No autorizacion comunicada |  |  |  |  |  |  |  |  | PROP | Cierre cuando no se obtiene la autorizacion externa exigible; la salida formal puede canalizarse por la OACGD |
| E-T9 | Gobierno Regional Huanuco | Gerencia Regional de Infraestructura | tarea | Integrar y elevar la propuesta | E-T10 |  |  |  |  |  |  |  | EQ | ROF, arts. 92-93; Bizagi de Consultas; la ruta concreta requiere validacion |
| E-T10 | Gobierno Regional Huanuco | Autoridad competente segun regimen, figura, umbral y delegacion | tarea-usuario | Resolver y emitir pronunciamiento | E-G10 |  |  |  |  |  |  |  | NORM | Incluye acordar o autorizar el pago cuando corresponda; Ley 32069, arts. 25 y 63-64; Reglamento, arts. 107, 109, 191, 197, 200 y 202; Directiva 017-2023-CG, nums. 7.3.6-7.3.7 |
| E-G10 | Gobierno Regional Huanuco | Autoridad competente segun regimen, figura, umbral y delegacion | compuerta | ¿Favorable? | E-T11 (por defecto); E-F2C [No] |  |  |  |  |  |  |  | PROP | La ruta favorable es la salida predeterminada despues de superar los controles. El Subgerente de SGGOS ocupa este rol solo si existe competencia o delegacion vigente |
| E-T11 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | tarea-usuario | Actualizar registros y coordinar la comunicacion | E-F1 |  |  |  |  |  |  |  | NORM | Directiva General de Invierte.pe, art. 33.2; ROF, art. 98 j-k; Reglamento, arts. 109.3, 194.3 y 198.4; Directiva 017-2023-CG, nums. 7.3.6-7.3.7 |
| E-F1 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | fin-mensaje | Modificacion comunicada |  |  |  |  |  |  |  |  | PROP | Producto propuesto del proceso; la salida formal puede canalizarse por la OACGD |
| E-F2C | Gobierno Regional Huanuco | Autoridad competente segun regimen, figura, umbral y delegacion | fin-mensaje | Decision no favorable comunicada |  |  |  |  |  |  |  |  | PROP | Producto alterno del proceso; la salida formal puede canalizarse por la OACGD |
| E-R1 | Gobierno Regional Huanuco | SGGOS - Monitor o gestor del expediente | inicio-condicional | Condiciones de reinicio verificadas | E-T13 |  |  |  |  |  |  |  | NORM | Nueva instancia posterior; Reglamento, arts. 107.2 y 202.2; Directiva 017-2023-CG, num. 7.3.7 |
| E-T13 | Gobierno Regional Huanuco | Autoridad competente segun regimen, figura, umbral y delegacion | tarea-usuario | Formalizar reinicio | E-F4 |  |  |  |  |  |  |  | NORM | Reglamento, arts. 107.2 y 202.2; Directiva 017-2023-CG, num. 7.3.7 |
| E-F4 | Gobierno Regional Huanuco | Autoridad competente segun regimen, figura, umbral y delegacion | fin-mensaje | Reinicio formalizado |  |  |  |  |  |  |  |  | PROP | Producto de la instancia posterior de reinicio |
| X-E1 | Elaborador definido o designado | Equipo elaborador competente | inicio-mensaje | Elaboracion o subsanacion solicitada | X-T1 |  |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 c-d; Directiva 017-2023-CG, num. 7.3.6 |
| X-T1 | Elaborador definido o designado | Equipo elaborador competente | tarea-usuario | Elaborar o subsanar el expediente tecnico | X-F1 |  |  |  |  |  |  |  | NORM | Reglamento, arts. 194.2 c-e y 196; Directiva 017-2023-CG, num. 7.3.6 |
| X-F1 | Elaborador definido o designado | Equipo elaborador competente | fin-mensaje | Expediente tecnico presentado |  |  |  |  |  |  |  |  | NORM | Reglamento, art. 194.2 d-f; Directiva 017-2023-CG, num. 7.3.6 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| R-F1 | S-E1 |  |
| S-F1 | E-E1 |  |
| E-T4 | X-E1 | Solicitud de elaboracion |
| X-F1 | E-M2 | Expediente tecnico |
| E-T8 | Contraloria General de la Republica | Solicitud de autorizacion |
| Contraloria General de la Republica | E-M1 | Pronunciamiento |
