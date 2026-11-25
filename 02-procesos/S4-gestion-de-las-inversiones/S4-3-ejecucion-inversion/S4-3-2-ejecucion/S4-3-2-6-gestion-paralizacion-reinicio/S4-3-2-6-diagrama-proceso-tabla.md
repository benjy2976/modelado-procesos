---
id: AP-S4-3-2-6-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.6
nivel_proceso: 3
perfil_trazado: zigzag-controlado
proceso:
  - S4.3.2.6
fecha_creacion: 2026-11-05
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-6
---

# S4.3.2.6 Gestion de paralizacion y reinicio

Sube a: [S4.3.2.6 Gestion de paralizacion y reinicio](00-S4-3-2-6-gestion-paralizacion-reinicio.md)

Modelo centrado en obras por contrata (`DEC-063`). Una instancia atiende un evento: la paralizacion, el cese de su causa o la paralizacion prolongada del regimen de reactivacion. En contrata el Reglamento de la Ley 32069 no regula la paralizacion como tramite propio; la trata como causal de ampliacion (198.1 a, S4.3.2.4) y, con acuerdo de las partes, como suspension (107, S4.3.2.5). El informe de la supervision, el acta de reinicio, el registro en INFOBRAS y la preferencia por la suspension son practica institucional informada por el usuario. La paralizacion prolongada sigue el TUO de la Ley 31589. La administracion directa se cita en el sustento como referencia (Directiva 017-2023-CG, num. 7.3.7) y no se diagrama.

Supervisor o inspector de obra es una abstraccion funcional ejercida alternativamente por supervisor contratado o inspector de la entidad, segun modalidad; no supone concurrencia ni identidad organizacional (`DEC-042`).

## Pools

| Pool | Carriles |
|---|---|
| Contratista | Residente de obra; Contratista o representante legal del contratista |
| Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad |
| Gobierno Regional Huanuco | OACGD — Registro documentario; SGGOS — Coordinador de obra; Especialista competente; UEI — Unidad Ejecutora de Inversiones; Titular de la entidad; OPMI — Oficina de Programacion Multianual de Inversiones |

## Elementos

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Anotacion | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|
| R-E1 | 1 | Contratista | Residente de obra | inicio-condicional | Hecho que impide continuar la ejecucion identificado | R-T1 |  |  | Contrato de obra vigente bajo la Ley 32069 | NORM | Reglamento, arts. 198.1 a y 200.1 a |
| R-T1 | 2 | Contratista | Residente de obra | tarea-usuario | Anotar el inicio de la causal en el Cuaderno de Incidencias | R-F1 | sale: Asiento de inicio de la causal |  |  | NORM | Reglamento, art. 200.1 a |
| R-F1 | 3 | Contratista | Residente de obra | fin-mensaje | Paralizacion anotada y comunicada |  |  |  |  | PROP | Practica institucional informada por el usuario, 2026-11-25 |
| R-E2 | 25 | Contratista | Residente de obra | inicio-condicional | Cese de la causa de paralizacion | R-T2 |  |  |  | NORM | Reglamento, art. 200.1 a |
| R-T2 | 26 | Contratista | Residente de obra | tarea-usuario | Anotar el fin de la causal en el Cuaderno de Incidencias | R-F2 | sale: Asiento de fin de la causal |  |  | NORM | Reglamento, art. 200.1 a |
| R-F2 | 27 | Contratista | Residente de obra | fin-mensaje | Fin de la causal comunicado |  |  |  | Desde el fin del hecho corren 10 dias habiles para solicitar la ampliacion (S4.3.2.4) | NORM | Reglamento, art. 200.1 a |
| C-E1 | 28 | Contratista | Contratista o representante legal del contratista | inicio-mensaje | Propuesta de continuidad recibida | C-T1 | entra: Propuesta de continuidad |  |  | NORM | TUO de la Ley 31589, art. 5.3 |
| C-T1 | 29 | Contratista | Contratista o representante legal del contratista | tarea | Comunicar la decision de continuar o no la ejecucion | C-F1 |  | 15 dias calendario desde el dia siguiente de la notificacion |  | NORM | TUO de la Ley 31589, art. 5.3 |
| C-F1 | 30 | Contratista | Contratista o representante legal del contratista | fin-mensaje | Decision comunicada a la entidad |  |  |  |  | NORM | TUO de la Ley 31589, art. 5.3 |
| S-E1 | 4 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Paralizacion comunicada recibida | S-T1 | entra: Asiento de inicio de la causal |  |  | PROP | Practica institucional informada por el usuario, 2026-11-25 |
| S-T1 | 5 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Verificar la paralizacion y su causa y emitir informe | S-F1 | sale: Informe de paralizacion |  |  | PROP | Practica institucional informada por el usuario, 2026-11-25 |
| S-F1 | 6 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Informe de paralizacion remitido |  |  |  |  | PROP | Practica institucional informada por el usuario, 2026-11-25 |
| S-E2 | 31 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Fin de la causal recibido | S-T2 | entra: Asiento de fin de la causal |  |  | PROP | Practica institucional informada por el usuario, 2026-11-25 |
| S-T2 | 32 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea-usuario | Suscribir con el contratista el acta de reinicio de los trabajos | S-F2 | sale: Acta de reinicio |  | Practica institucional; el Reglamento no la exige en contrata | PROP | Practica institucional informada por el usuario, 2026-11-25 |
| S-F2 | 33 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Acta de reinicio remitida |  |  |  |  | PROP | Practica institucional informada por el usuario, 2026-11-25 |
| E-E1 | 7 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Informe o acta recibido | E-T1 | entra: Informe de paralizacion o acta de reinicio |  |  | EQ | ROF, art. 20; DEC-041 |
| E-T1 | 8 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Registrar y derivar a SGGOS por SGD | E-T2 | sale: Registro y derivacion; almacen: SGD |  |  | EQ | ROF, art. 20; observacion del usuario, 2026-11-10 |
| E-T2 | 9 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Verificar integridad y clasificar el evento | E-G2 | entra: Expediente |  |  | EQ | ROF, arts. 97-98; DEC-041 |
| E-G2 | 12 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Que se gestiona? | E-G1 [Paralizacion]; E-T8 [Reinicio] |  |  |  | EQ | Separacion adoptada en DEC-041 |
| E-G1 | 10 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Requiere evaluacion tecnica especializada? | E-T3 [Si]; E-T4 [No] (por defecto) |  |  |  | EQ | El coordinador no sustituye al especialista; DEC-041 |
| E-T3 | 11 | Gobierno Regional Huanuco | Especialista competente | tarea | Evaluar la causa de la paralizacion | E-T4 | sale: Evaluacion especializada |  |  | PROP | Alcance de la evaluacion por confirmar |
| E-T4 | 34 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Evaluar la causa y si es atribuible al contratista | E-T5 | sale: Evaluacion de la paralizacion |  |  | PROP | Practica institucional informada por el usuario, 2026-11-25; Reglamento, art. 198.1 a |
| E-T5 | 35 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Registrar la paralizacion en INFOBRAS | E-G3 | almacen: INFOBRAS |  | Responsable y oportunidad por confirmar | PROP | Practica institucional informada por el usuario, 2026-11-25; Directiva 005-2023-CG: EVIDENCIA-INSUFICIENTE |
| E-G3 | 15 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Es atribuible al contratista? | E-F2 [Si]; E-F1 [No] (por defecto) |  |  |  | PROP | Practica institucional informada por el usuario, 2026-11-25 |
| E-F1 | 17 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Paralizacion derivada para acordar la suspension |  |  |  | Sin acuerdo, la paralizacion fundada sigue como causal de ampliacion (198.1 a) | PROP | Practica institucional informada por el usuario, 2026-11-25; Reglamento, arts. 107 y 198.1 a |
| E-F2 | 18 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Paralizacion atribuible comunicada al contratista |  |  |  | Se aplica el contrato; la resolucion queda diferida (DEC-061) | PROP | Practica institucional informada por el usuario, 2026-11-25 |
| E-T8 | 20 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Registrar el reinicio en INFOBRAS | E-F3 | entra: Acta de reinicio; almacen: INFOBRAS |  |  | PROP | Practica institucional informada por el usuario, 2026-11-25; Directiva 005-2023-CG: EVIDENCIA-INSUFICIENTE |
| E-F3 | 23 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin | Reinicio registrado |  |  |  | El contratista solicita la ampliacion conforme a S4.3.2.4 | PROP | Practica institucional informada por el usuario, 2026-11-25; Reglamento, art. 200.1 a |
| U-E1 | 36 | Gobierno Regional Huanuco | UEI — Unidad Ejecutora de Inversiones | inicio-condicional | Obra con avance de 40 % o mas y 6 meses o mas sin ejecucion fisica | U-T1 |  |  | Contrato vigente (2.1 i); el contrato resuelto o nulo (2.1 ii) queda diferido | NORM | TUO de la Ley 31589, art. 2.1 |
| U-T1 | 37 | Gobierno Regional Huanuco | UEI — Unidad Ejecutora de Inversiones | tarea-usuario | Registrar la obra en el inventario de obras paralizadas | T-T1 | almacen: Banco de Inversiones |  | Con el ultimo informe de avance, el cuaderno o un acta (3.2-3.4) | NORM | TUO de la Ley 31589, art. 3 |
| T-T1 | 38 | Gobierno Regional Huanuco | Titular de la entidad | tarea-usuario | Solicitar el informe de estado situacional | U-T2 |  |  |  | NORM | TUO de la Ley 31589, art. 4.1 |
| U-T2 | 39 | Gobierno Regional Huanuco | UEI — Unidad Ejecutora de Inversiones | tarea | Elaborar y registrar el informe de estado situacional | T-T2 | sale: Informe de estado situacional; almacen: Banco de Inversiones |  | Elaborado por la UEI, el supervisor o inspector, o contratado; es vinculante | NORM | TUO de la Ley 31589, arts. 4.1, 4.2 y 9.2 |
| T-T2 | 40 | Gobierno Regional Huanuco | Titular de la entidad | tarea-usuario | Aprobar la lista priorizada de obras paralizadas | O-T1 | sale: Resolucion de lista priorizada | A mas tardar el 31 de diciembre de cada año fiscal |  | NORM | TUO de la Ley 31589, art. 4.4 |
| O-T1 | 41 | Gobierno Regional Huanuco | OPMI — Oficina de Programacion Multianual de Inversiones | tarea-usuario | Registrar la resolucion en el Banco de Inversiones | T-G1 | almacen: Banco de Inversiones |  | Publicacion en el portal en 5 dias habiles (9.1) | NORM | TUO de la Ley 31589, arts. 4.4, 9.1 y 9.2 |
| T-G1 | 42 | Gobierno Regional Huanuco | Titular de la entidad | compuerta | ¿Que decide la entidad? | T-T3 [Proponer continuidad]; T-F4 [Resolver el contrato]; T-F2 [Obra no priorizada] (por defecto) |  |  |  | NORM | TUO de la Ley 31589, art. 5.2 |
| T-T3 | 43 | Gobierno Regional Huanuco | Titular de la entidad | tarea-usuario | Proponer al contratista la continuidad de la ejecucion | T-GE1 | sale: Propuesta de continuidad |  | Con las modificaciones contractuales que deriven del informe | NORM | TUO de la Ley 31589, art. 5.2 a |
| T-GE1 | 44 | Gobierno Regional Huanuco | Titular de la entidad | compuerta-eventos | ¿Que ocurre primero? | T-M1; T-R1 |  |  |  | NORM | TUO de la Ley 31589, art. 5.3 |
| T-M1 | 45 | Gobierno Regional Huanuco | Titular de la entidad | mensaje-recepcion | Decision del contratista recibida | T-G2 | entra: Decision del contratista |  |  | NORM | TUO de la Ley 31589, art. 5.3 |
| T-R1 | 46 | Gobierno Regional Huanuco | Titular de la entidad | temporizador | Vencio el plazo del contratista | T-F1 |  | 15 dias calendario desde el dia siguiente de la notificacion |  | NORM | TUO de la Ley 31589, art. 5.3 |
| T-G2 | 47 | Gobierno Regional Huanuco | Titular de la entidad | compuerta | ¿Decide continuar? | T-F3 [Si] (por defecto); T-F1 [No] |  |  |  | NORM | TUO de la Ley 31589, art. 5.3 |
| T-F3 | 48 | Gobierno Regional Huanuco | Titular de la entidad | fin | Continuidad de la obra acordada |  |  |  | Registro en el Formato 12-B y en INFOBRAS (9.3) | NORM | TUO de la Ley 31589, arts. 5.2 a y 9.3 |
| T-F1 | 49 | Gobierno Regional Huanuco | Titular de la entidad | fin | Contrato en causal de resolucion sin continuidad |  |  |  | Remite al evento Contrato resuelto de S4.3.2 | NORM | TUO de la Ley 31589, art. 5.3 |
| T-F4 | 50 | Gobierno Regional Huanuco | Titular de la entidad | fin | Contrato en causal de resolucion por decision de la entidad |  |  |  | Remite al evento Contrato resuelto de S4.3.2 | NORM | TUO de la Ley 31589, art. 5.2 b |
| T-F2 | 51 | Gobierno Regional Huanuco | Titular de la entidad | fin | Obra no incluida en la lista priorizada |  |  |  |  | PROP | Inferencia sobre el art. 4.4 del TUO de la Ley 31589 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| R-F1 | S-E1 | Asiento de inicio de la causal |
| S-F1 | E-E1 | Informe de paralizacion |
| R-F2 | S-E2 | Asiento de fin de la causal |
| S-F2 | E-E1 | Acta de reinicio |
| E-F1 | S4.3.2.5 Formalizacion de suspensiones de plazo | Paralizacion derivada para suspension |
| E-F2 | Contratista | Comunicacion de paralizacion atribuible |
| T-T3 | C-E1 | Propuesta de continuidad |
| C-F1 | T-M1 | Decision del contratista |
