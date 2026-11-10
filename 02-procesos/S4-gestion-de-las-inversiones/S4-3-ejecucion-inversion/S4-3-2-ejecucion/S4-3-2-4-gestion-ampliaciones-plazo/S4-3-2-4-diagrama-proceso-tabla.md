---
id: AP-S4-3-2-4-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.4
nivel_proceso: 3
perfil_trazado: zigzag-controlado
proceso:
  - S4.3.2.4
fecha_creacion: 2026-11-05
fecha_actualizacion: 2026-11-10
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-4
---

# S4.3.2.4 Gestion de ampliaciones de plazo

Sube a: [S4.3.2.4 Gestion de ampliaciones de plazo](00-S4-3-2-4-gestion-ampliaciones-plazo.md)

Modelo inicial extraido de la variante `MOD-PLA-AMP` del anterior S4.3.2.3. La instancia es una por solicitud o causal de ampliacion. Cuaderno de Incidencias es la denominacion institucional uniforme; las fuentes de administracion directa pueden usar cuaderno de obra.

Esta revision representa al Contratista y al Supervisor o inspector de obra segun la modalidad. El segundo nombre es una alternativa funcional: el supervisor contratado y el inspector de la entidad no actuan simultaneamente ni pertenecen a la misma organizacion. Los registros y derivaciones internas del Gobierno Regional se realizan mediante el Sistema de Gestion Documental (SGD), representado como almacen de datos BPMN; su uso no implica una decision automatica.

## Pools

| Pool | Carriles |
|---|---|
| Contratista | Contratista |
| Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad |
| Gobierno Regional Huanuco | OACGD — Registro documentario; SGGOS — Coordinador de obra; SGGOS — Subgerente de Gestion de Obras y Supervision; GRI — Gerente Regional de Infraestructura; GRAJ — Asesoria Juridica; Autoridad competente para resolver |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| R-E1 | Contratista | Contratista | inicio-condicional | Causal de ampliacion identificada | R-T1 |  |  | NORM | Reglamento, arts. 198 y 200; Directiva 017-2023-CG, num. 7.3.7 |
| R-T1 | Contratista | Contratista | tarea-usuario | Registrar causal en Cuaderno y presentar solicitud | R-F1 | sale: Solicitud y sustento |  | NORM | Reglamento, art. 200.1 a; Directiva 017-2023-CG, num. 7.3.7 |
| R-F1 | Contratista | Contratista | fin-mensaje | Solicitud de ampliacion remitida |  |  |  | NORM | Reglamento, art. 200.1; Directiva 017-2023-CG, num. 7.3.7 |
| S-E1 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Solicitud de ampliacion recibida | S-T1 | entra: Solicitud y sustento |  | NORM | Reglamento, art. 200.1 b; Directiva 017-2023-CG, num. 7.3.7 |
| S-T1 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Evaluar la causal y emitir opinion | S-F1 |  |  | NORM | Reglamento, arts. 198 y 200.1 b; Directiva 017-2023-CG, num. 7.3.7 |
| S-F1 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Solicitud y opinion remitidas al GORE |  |  |  | NORM | Reglamento, art. 200.1; Directiva 017-2023-CG, num. 7.3.7 |
| E-E1 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Expediente de ampliacion recibido | E-T1 | entra: Solicitud y opinion |  | EQ | ROF, art. 20; observacion del usuario, 2026-11-10 |
| E-T1 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Registrar expediente y derivar a SGGOS por SGD | E-T2 | sale: Registro y derivacion; almacen: SGD |  | EQ | ROF, art. 20; observacion del usuario, 2026-11-10 |
| E-T2 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Evaluar solicitud y sustento de ampliacion | E-T3 | entra: Expediente de ampliacion; sale: Evaluacion del coordinador |  | EQ | Observacion del usuario, 2026-11-10; ROF, arts. 97-98 |
| E-T3 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Emitir informe y elevar expediente al subgerente por SGD | E-T4 | sale: Informe del coordinador; almacen: SGD |  | EQ | Observacion del usuario, 2026-11-10 |
| E-T4 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea | Hacer suyo o emitir informe tecnico de procedencia | E-T5 | entra: Informe del coordinador; sale: Informe tecnico de SGGOS |  | EQ | Observacion del usuario, 2026-11-10; ROF, arts. 97-98 |
| E-T5 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea-usuario | Elevar informe tecnico y expediente a GRI por SGD | E-T6 | sale: Derivacion a GRI; almacen: SGD |  | EQ | Observacion del usuario, 2026-11-10 |
| E-T6 | Gobierno Regional Huanuco | GRI — Gerente Regional de Infraestructura | tarea | Evaluar procedencia y hacer suyo o emitir criterio propio | E-T7 | entra: Informe tecnico de SGGOS; sale: Criterio del gerente |  | EQ | Observacion del usuario, 2026-11-10; ROF, arts. 92-93 |
| E-T7 | Gobierno Regional Huanuco | GRI — Gerente Regional de Infraestructura | tarea-usuario | Remitir expediente con memorandum a GRAJ por SGD | E-T8 | sale: Memorandum y expediente; almacen: SGD |  | EQ | Observacion del usuario, 2026-11-10 |
| E-T8 | Gobierno Regional Huanuco | GRAJ — Asesoria Juridica | tarea | Emitir opinion legal sobre la ampliacion | E-T8A | entra: Memorandum y expediente; sale: Opinion legal |  | EQ | Aclaraciones del usuario, 2026-11-10; ROF, arts. 44-45 |
| E-T8A | Gobierno Regional Huanuco | GRAJ — Asesoria Juridica | tarea-usuario | Proyectar resolucion y derivar expediente al decisor por SGD | E-T9 | sale: Proyecto de resolucion y expediente; almacen: SGD |  | EQ | Aclaracion del usuario, 2026-11-10 |
| E-T9 | Gobierno Regional Huanuco | Autoridad competente para resolver | tarea-usuario | Resolver la solicitud mediante resolucion | E-G1 | entra: Expediente, opinion legal y proyecto de resolucion; sale: Resolucion; almacen: SGD |  | EQ | Aclaracion del usuario, 2026-11-10; Reglamento, art. 200; Directiva 017-2023-CG, num. 7.3.7; autoridad concreta pendiente |
| E-G1 | Gobierno Regional Huanuco | Autoridad competente para resolver | compuerta | ¿Se aprueba la ampliacion? | E-T10 [Si]; E-F2 [No] |  |  | PROP | Dos resultados posibles de la decision |
| E-T10 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Actualizar plazo y cronograma y registrar decision en SGD | E-F1 | sale: Plazo y cronograma actualizados cuando corresponda; almacen: SGD |  | EQ | Reglamento, art. 198.4; observacion del usuario, 2026-11-10 |
| E-F1 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Resolucion favorable comunicada |  |  |  | PROP | Producto propuesto; aclaracion del usuario, 2026-11-10 |
| E-F2 | Gobierno Regional Huanuco | Autoridad competente para resolver | fin-mensaje | Resolucion no favorable comunicada |  |  |  | PROP | Producto alterno; aclaracion del usuario, 2026-11-10 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| R-F1 | S-E1 | Solicitud y sustento |
| S-F1 | E-E1 | Solicitud y opinion |

