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
fecha_actualizacion: 2026-11-25
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

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Anotacion | Clase | Fuente |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-E1 | 1 | Contratista | Contratista | inicio-condicional | Causal de ampliacion identificada | R-T1 |  |  | Causales del 198.1: a) atrasos o paralizaciones no atribuibles, incluida la consulta no absuelta (S4.3.2.2, art. 190.4) y la paralizacion en contrata (S4.3.2.6); b) adicional (S4.3.2.3); c) mayores metrados (S4.3.2.8). Siempre que modifiquen la ruta critica | NORM | Reglamento, arts. 190.4, 198.1 y 200 |
| R-T1 | 2 | Contratista | Contratista | tarea-usuario | Registrar causal en Cuaderno y notificar solicitud a la entidad y a la supervision | R-F1 | sale: Solicitud y sustento | 10 dias habiles desde la aprobacion del adicional o el fin del hecho generador, prorrogables hasta 10; fuera de plazo se tiene por no presentada |  | NORM | Reglamento, art. 200.1 a |
| R-F1 | 3 | Contratista | Contratista | fin-mensaje | Solicitud de ampliacion notificada |  |  |  |  | NORM | Reglamento, art. 200.1 a |
| S-E1 | 4 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Solicitud de ampliacion recibida | S-T1 | entra: Solicitud y sustento |  |  | NORM | Reglamento, art. 200.1 b; Directiva 017-2023-CG, num. 7.3.7 |
| S-T1 | 5 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Evaluar la causal y emitir opinion | S-F1 |  | 5 dias habiles desde la notificacion de la solicitud |  | NORM | Reglamento, arts. 198 y 200.1 b |
| S-F1 | 6 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Opinion tecnica notificada a la entidad |  |  |  |  | NORM | Reglamento, art. 200.1 b |
| E-E1 | 7 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Solicitud de ampliacion recibida | E-T1 | entra: Solicitud y sustento |  |  | EQ | Reglamento, art. 200.1 a; ROF, art. 20; observacion del usuario, 2026-11-10 |
| E-T1 | 8 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Registrar expediente y derivar a SGGOS por SGD | E-GE1 | sale: Registro y derivacion; almacen: SGD |  |  | EQ | ROF, art. 20; observacion del usuario, 2026-11-10 |
| E-GE1 | 22 | Gobierno Regional Huanuco | OACGD — Registro documentario | compuerta-eventos | ¿Que ocurre primero? | E-M1; E-R1 |  |  |  | NORM | Reglamento, art. 200.1 b-c |
| E-M1 | 23 | Gobierno Regional Huanuco | OACGD — Registro documentario | mensaje-recepcion | Opinion del supervisor recibida | E-T2 | entra: Opinion tecnica |  |  | NORM | Reglamento, art. 200.1 b |
| E-R1 | 24 | Gobierno Regional Huanuco | OACGD — Registro documentario | temporizador | Vencio el plazo del supervisor | E-T2 |  | 5 dias habiles desde la notificacion de la solicitud | La entidad resuelve sin el pronunciamiento del supervisor | NORM | Reglamento, art. 200.1 c |
| E-T2 | 9 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Evaluar solicitud y sustento de ampliacion | E-T3 | entra: Expediente de ampliacion; sale: Evaluacion del coordinador |  |  | EQ | Observacion del usuario, 2026-11-10; ROF, arts. 97-98 |
| E-T3 | 10 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Emitir informe y elevar expediente al subgerente por SGD | E-T4 | sale: Informe del coordinador; almacen: SGD |  |  | EQ | Observacion del usuario, 2026-11-10 |
| E-T4 | 11 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea | Hacer suyo o emitir informe tecnico de procedencia | E-T5 | entra: Informe del coordinador; sale: Informe tecnico de SGGOS |  |  | EQ | Observacion del usuario, 2026-11-10; ROF, arts. 97-98 |
| E-T5 | 12 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea-usuario | Elevar informe tecnico y expediente a GRI por SGD | E-T6 | sale: Derivacion a GRI; almacen: SGD |  |  | EQ | Observacion del usuario, 2026-11-10 |
| E-T6 | 13 | Gobierno Regional Huanuco | GRI — Gerente Regional de Infraestructura | tarea | Evaluar procedencia y hacer suyo o emitir criterio propio | E-T7 | entra: Informe tecnico de SGGOS; sale: Criterio del gerente |  |  | EQ | Observacion del usuario, 2026-11-10; ROF, arts. 92-93 |
| E-T7 | 14 | Gobierno Regional Huanuco | GRI — Gerente Regional de Infraestructura | tarea-usuario | Remitir expediente con memorandum a GRAJ por SGD | E-T8 | sale: Memorandum y expediente; almacen: SGD |  |  | EQ | Observacion del usuario, 2026-11-10 |
| E-T8 | 15 | Gobierno Regional Huanuco | GRAJ — Asesoria Juridica | tarea | Emitir opinion legal sobre la ampliacion | E-T8A | entra: Memorandum y expediente; sale: Opinion legal |  |  | EQ | Aclaraciones del usuario, 2026-11-10; ROF, arts. 44-45 |
| E-T8A | 16 | Gobierno Regional Huanuco | GRAJ — Asesoria Juridica | tarea-usuario | Proyectar resolucion y derivar expediente al decisor por SGD | E-T9 | sale: Proyecto de resolucion y expediente; almacen: SGD |  |  | EQ | Aclaracion del usuario, 2026-11-10 |
| E-T9 | 17 | Gobierno Regional Huanuco | Autoridad competente para resolver | tarea-usuario | Resolver la solicitud mediante resolucion | E-G1 | entra: Expediente, opinion legal y proyecto de resolucion; sale: Resolucion; almacen: SGD | 10 dias habiles desde la opinion del supervisor o el vencimiento de su plazo; incluye el circuito interno desde E-T2 | Si no se notifica en plazo, se tiene por aprobado lo informado por el supervisor o, sin informe, lo solicitado por el contratista | EQ | Reglamento, art. 200.1 d; aclaracion del usuario, 2026-11-10; autoridad concreta pendiente |
| E-G1 | 18 | Gobierno Regional Huanuco | Autoridad competente para resolver | compuerta | ¿Se aprueba la ampliacion? | E-T10 [Si]; E-F2 [No] |  |  |  | PROP | Dos resultados posibles de la decision |
| E-T10 | 19 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Publicar la resolucion en la Pladicop y actualizar plazo y cronograma | E-F1 | sale: Resolucion publicada; sale: Plazo y cronograma actualizados; almacen: Pladicop; almacen: SGD |  |  | EQ | Reglamento, arts. 198.4 y 200.1 d; observacion del usuario, 2026-11-10 |
| E-F1 | 20 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Resolucion favorable notificada por la Pladicop |  |  |  |  | PROP | Reglamento, art. 200.1 d |
| E-F2 | 21 | Gobierno Regional Huanuco | Autoridad competente para resolver | fin-mensaje | Resolucion no favorable notificada por la Pladicop |  |  |  |  | PROP | Reglamento, art. 200.1 d; canal de la autoridad por confirmar |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| R-F1 | S-E1 | Solicitud y sustento |
| R-F1 | E-E1 | Solicitud y sustento |
| S-F1 | E-M1 | Opinion tecnica |
| E-F1 | Contratista | Resolucion notificada por la Pladicop |
| E-F2 | Contratista | Resolucion notificada por la Pladicop |

