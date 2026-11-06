---
id: AP-S4-3-2-4-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.4
nivel_proceso: 3
proceso:
  - S4.3.2.4
fecha_creacion: 2026-11-05
fecha_actualizacion: 2026-11-05
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-4
---

# S4.3.2.4 Gestion de ampliaciones de plazo

Sube a: [S4.3.2.4 Gestion de ampliaciones de plazo](00-S4-3-2-4-gestion-ampliaciones-plazo.md)

Modelo inicial extraido de la variante `MOD-PLA-AMP` del anterior S4.3.2.3. La instancia es una por solicitud o causal de ampliacion. Cuaderno de Incidencias es la denominacion institucional uniforme; las fuentes de administracion directa pueden usar cuaderno de obra.

Ejecutor de obra agrupa al residente y los demas roles del ejecutor cuando intervengan. Control de obra es una abstraccion funcional ejercida alternativamente por supervisor contratado o inspector de la entidad, segun modalidad; no supone concurrencia ni identidad organizacional (`DEC-042`).

## Pools

| Pool | Carriles |
|---|---|
| Ejecutor de obra | Residente de obra |
| Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad |
| Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental; SGGOS — Coordinador de obra; Especialista competente; SGGOS — Control contractual y costos; Titular de la competencia o autoridad delegada |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| R-E1 | Ejecutor de obra | Residente de obra | inicio-condicional | Causal de ampliacion identificada | R-T1 |  |  | NORM | Reglamento, arts. 198 y 200; Directiva 017-2023-CG, num. 7.3.7 |
| R-T1 | Ejecutor de obra | Residente de obra | tarea-usuario | Registrar y sustentar la causal en el Cuaderno de Incidencias | R-F1 | sale: Solicitud y sustento |  | NORM | Reglamento, art. 200.1 a; Directiva 017-2023-CG, num. 7.3.7 |
| R-F1 | Ejecutor de obra | Residente de obra | fin-mensaje | Solicitud de ampliacion remitida |  |  |  | NORM | Reglamento, art. 200.1; Directiva 017-2023-CG, num. 7.3.7 |
| S-E1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | inicio-mensaje | Solicitud de ampliacion recibida | S-T1 | entra: Solicitud y sustento |  | NORM | Reglamento, art. 200.1 b; Directiva 017-2023-CG, num. 7.3.7 |
| S-T1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | tarea | Evaluar la causal y emitir opinion | S-F1 | sale: Opinion del responsable del control de obra |  | NORM | Reglamento, arts. 198 y 200.1 b; Directiva 017-2023-CG, num. 7.3.7 |
| S-F1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | fin-mensaje | Solicitud y opinion remitidas al GORE |  |  |  | NORM | Reglamento, art. 200.1; Directiva 017-2023-CG, num. 7.3.7 |
| E-E1 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | inicio-mensaje | Expediente de ampliacion recibido | E-T1 | entra: Solicitud y opinion |  | EQ | ROF, art. 20; DEC-041 |
| E-T1 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | tarea-usuario | Registrar y derivar a la SGGOS | E-T2 | sale: Registro y derivacion |  | NORM | ROF, art. 20 |
| E-T2 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Verificar integridad y clasificar regimen y causal | E-G1 | entra: Expediente de ampliacion |  | EQ | ROF, arts. 97-98; DEC-041 |
| E-G1 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Requiere evaluacion tecnica especializada? | E-T3 [Si]; E-T4 [No] (por defecto) |  |  | EQ | El coordinador no sustituye al especialista; DEC-041 |
| E-T3 | Gobierno Regional Huanuco | Especialista competente | tarea | Evaluar causal y afectacion de la ruta critica | E-T4 | sale: Evaluacion especializada |  | NORM | Reglamento, arts. 198 y 200; Directiva 017-2023-CG, num. 7.3.7 |
| E-T4 | Gobierno Regional Huanuco | SGGOS — Control contractual y costos | tarea | Revisar procedimiento y efectos contractuales | E-T5 | sale: Control contractual |  | EQ | Reglamento, arts. 198, 200 y 201; ROF, arts. 97-98 |
| E-T5 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Consolidar y elevar el expediente | E-T6 | sale: Expediente consolidado |  | PROP | DEC-041; no sustituye opiniones especializadas |
| E-T6 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Resolver la solicitud de ampliacion | E-G4 | entra: Expediente consolidado; sale: Pronunciamiento |  | NORM | Reglamento, art. 200; Directiva 017-2023-CG, num. 7.3.7 |
| E-G4 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | compuerta | ¿Favorable? | E-T7 [Si] (por defecto); E-F2 [No] |  |  | PROP | Rutas de decision |
| E-T7 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Actualizar registros y coordinar la comunicacion | E-F1 | sale: Plazo y cronograma actualizados cuando corresponda |  | NORM | Reglamento, art. 198.4; Directiva 017-2023-CG, num. 7.3.7 |
| E-F1 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Ampliacion de plazo comunicada |  |  |  | PROP | Producto propuesto |
| E-F2 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | Decision no favorable comunicada |  |  |  | PROP | Producto alterno |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| R-F1 | S-E1 | Solicitud y sustento |
| S-F1 | E-E1 | Solicitud y opinion |

