---
id: AP-S4-3-2-2-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.2
nivel_proceso: 3
perfil_trazado: zigzag-corredores
proceso:
  - S4.3.2.2
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-2
---

# S4.3.2.2 Atencion de consultas de obra

Sube a: [S4.3.2.2 Atencion de consultas de obra](00-S4-3-2-2-atencion-consultas-obra.md)

Modelo reconstruido a partir de las actividades de consulta del BPMN exportado de Bizagi, el articulo 190 del Reglamento de la Ley 32069, el ROF del Gobierno Regional Huanuco y las precisiones operativas del equipo. Las ramas de alcance, ampliacion, suspension y paralizacion o reinicio se trasladan a S4.3.2.3 a S4.3.2.6 y no se duplican en este flujo.

Notas que no se dibujan:

- La instancia es una por consulta.
- El pool Contratista contiene al residente y al equipo especialista del ejecutor; estos roles no constituyen participantes independientes.
- El pool Supervision contratada representa exclusivamente la variante con supervisor externo. Cuando interviene un inspector de la entidad, sus actividades deben trasladarse al pool del Gobierno Regional Huanuco en la variante correspondiente.
- El informe del especialista del contratista o de la supervision se incorpora cuando la naturaleza de la consulta y la composicion de su personal clave lo requieren. Si la consulta del contratista conlleva modificar el expediente tecnico, el informe tecnico es obligatorio conforme al articulo 190.2.
- La SGE conserva la responsabilidad de absolver la consulta aun cuando venza el plazo del proyectista sin opinion. Los especialistas elaboran el informe tecnico de absolucion y el Subgerente de Estudios firma la respuesta, conforme a `DEC-033`.
- Cuando la consulta requiere la opinion de un especialista de la supervision, este revisa y se pronuncia antes de que el supervisor decida si puede absolverla o debe elevarla. El supervisor hace suyo el pronunciamiento y anota en el Cuaderno de Incidencias tanto la absolucion como la elevacion que corresponda.

- La consulta del contratista que modifica el expediente tecnico exige su informe tecnico (art. 190.2). S-G6 verifica su presencia antes de elevar; E-G5 evita que la entidad continue la atencion si recibe una consulta de ese supuesto sin informe. La opinion del supervisor no sustituye ese informe. La consulta propia de la supervision mantiene su ruta excepcional, sin atribuirla al art. 190.2. Trazabilidad y vigencia: [sustento](S4-3-2-2-sustento.md).

- Antes de toda elevacion, el supervisor emite su informe tecnico (caja 59), que contiene la evaluacion y opinion sobre la viabilidad de la consulta. Es necesario para la entidad aunque no intervenga un especialista de supervision. El informe del especialista, cuando exista, es insumo de este informe; no lo sustituye. Precision operativa del usuario, 2026-11-17, desarrollada en el [sustento](S4-3-2-2-sustento.md).

- En la caja 52, el monitor prepara la carta de respuesta al contratista. Si corresponde un adicional, la carta comunica a quien corresponde elaborarlo segun las bases de contratacion aplicables. No se presume un responsable ni se aprueba el adicional en este proceso. Precision operativa del usuario, 2026-11-18; ver [sustento](S4-3-2-2-sustento.md).

## Pools

| Pool | Carriles |
|---|---|
| Contratista | Residente de obra; Equipo especialista del ejecutor |
| Supervision contratada | Supervisor de obra; Equipo especialista de la supervision |
| Gobierno Regional Huanuco | OACGD — Registro documentario; SGGOS — Monitor de obras; SGGOS — Subgerente de Gestion de Obras y Supervision; SGE — Especialistas tecnicos; SGE — Subgerente de Estudios |
| Proyectista | Proyectista |

## Elementos

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Grupo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C-E1 | 1 | Contratista | Residente de obra | inicio | Necesidad de consulta identificada | C-G1 |  |  |  |  |  |  |  | EQ | Descripcion operativa del equipo; Reglamento, art. 190.1 |
| C-G1 | 2 | Contratista | Residente de obra | compuerta | ¿Modifica expediente o requiere informe? | C-T1 [Si]; C-G2 [No] (por defecto) |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.2; precision operativa del equipo |
| C-T1 | 3 | Contratista | Equipo especialista del ejecutor | tarea | Elaborar informe tecnico de especialidad | C-G2 |  |  | sale: Informe tecnico de especialidad |  |  |  |  | EQ | Precision operativa del equipo |
| C-G2 | 4 | Contratista | Residente de obra | compuerta |  | C-T2 |  |  |  |  |  |  |  | PROP | Convergencia de rutas |
| C-T2 | 5 | Contratista | Residente de obra | tarea-usuario | Registrar la consulta en el Cuaderno de Incidencias | C-F1 |  |  | sale: Consulta y antecedentes; sale: Informe tecnico cuando corresponda |  |  |  |  | NORM | Reglamento, arts. 188 y 190.1-190.2 |
| C-F1 | 6 | Contratista | Residente de obra | fin-mensaje | Consulta remitida al supervisor |  |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.1 |
| C-E2 | 7 | Contratista | Residente de obra | inicio-mensaje | Respuesta a la consulta recibida | C-T3 |  |  | entra: Respuesta a la consulta |  |  |  |  | OBS | Flujo Bizagi y precision operativa del equipo |
| C-T3 | 8 | Contratista | Residente de obra | tarea-usuario | Tomar conocimiento y registrar la respuesta | C-F2 |  |  | sale: Registro de respuesta |  |  |  |  | PROP | Cierre operativo de la consulta |
| C-F2 | 9 | Contratista | Residente de obra | fin | Consulta atendida para el ejecutor |  |  |  |  |  |  |  |  | PROP | Producto del proceso |
| S-E1 | 10 | Supervision contratada | Supervisor de obra | inicio-mensaje | Consulta del ejecutor recibida | S-T1 |  |  | entra: Consulta y antecedentes |  |  |  |  | NORM | Reglamento, art. 190.1 |
| S-T1 | 11 | Supervision contratada | Supervisor de obra | tarea | Revisar la consulta y el expediente tecnico | S-G5 |  |  | entra: Consulta; entra: Informe tecnico cuando corresponda |  |  |  |  | OBS | Flujo Bizagi; Reglamento, art. 190 |
| S-G1 | 12 | Supervision contratada | Supervisor de obra | compuerta | ¿Modifica el expediente tecnico? | S-G6 [Si]; S-T2 [No] (por defecto) |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.1 |
| S-T2 | 13 | Supervision contratada | Supervisor de obra | tarea-usuario | Absolver y anotar en el Cuaderno de Incidencias | S-T5 |  |  |  |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17; Reglamento, art. 190.1 |
| S-E2 | 14 | Supervision contratada | Supervisor de obra | inicio |  | S-T0 |  |  |  |  |  |  |  | EQ | Consulta originada por la supervision; precision operativa del equipo |
| S-T0 | 15 | Supervision contratada | Supervisor de obra | tarea | Identificar consulta propia | S-G2 |  |  | sale: Antecedentes de la supervision |  |  |  |  | EQ | Precision operativa del equipo |
| S-G2 | 16 | Supervision contratada | Supervisor de obra | compuerta | ¿Especialista? | S-T3 [Si]; S-G3 [No] (por defecto) |  |  |  |  |  |  |  | EQ | Precision operativa del equipo |
| S-T3 | 17 | Supervision contratada | Equipo especialista de la supervision | tarea | Elaborar informe tecnico de especialidad | S-G3 |  |  | sale: Informe tecnico de especialidad |  |  |  |  | EQ | Precision operativa del equipo |
| S-G3 | 18 | Supervision contratada | Supervisor de obra | compuerta |  | S-T8 |  |  |  |  |  |  |  | PROP | Convergencia de rutas |
| S-T4 | 19 | Supervision contratada | Supervisor de obra | tarea-usuario | Anotar y elevar consulta con informes | S-F1 |  |  | entra: Informe tecnico de supervision; sale: Consulta elevada; sale: Informe tecnico de supervision; sale: Informe tecnico del contratista si modifica expediente | 5 dias desde la anotacion cuando aplica el art. 190.3 |  |  |  | EQ | Precision operativa del usuario, 2026-11-17; Reglamento, art. 190.3; flujo Bizagi |
| S-F1 | 20 | Supervision contratada | Supervisor de obra | fin-mensaje | Consulta elevada a la entidad |  |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.3 |
| S-T5 | 23 | Supervision contratada | Supervisor de obra | tarea | Comunicar la respuesta al ejecutor | S-F2 |  |  | sale: Respuesta comunicada |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17 |
| S-F2 | 24 | Supervision contratada | Supervisor de obra | fin-mensaje | Respuesta comunicada al ejecutor |  |  |  |  |  |  |  |  | PROP | Producto del proceso |
| E-E1 | 25 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Consulta recibida por Mesa de Partes | E-T1 |  |  | entra: Consulta elevada; entra: Informe tecnico de supervision; entra: Informe tecnico del contratista cuando corresponde |  |  |  |  | EQ | Precision operativa del equipo; ROF, art. 20 |
| E-T1 | 26 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Registrar y derivar la consulta a la SGGOS por SGD | E-T2 |  |  | sale: Registro y proveido de derivacion; almacen: SGD |  |  |  |  | OBS | Flujo Bizagi; precision operativa del equipo; observacion del usuario, 2026-11-10 |
| E-T2 | 27 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea-usuario | Recibir consulta y derivarla al monitor por SGD | E-T3 |  |  | entra: Consulta y antecedentes; almacen: SGD |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17 |
| E-T3 | 28 | Gobierno Regional Huanuco | SGGOS — Monitor de obras | tarea | Revisar antecedentes y preparar tramite a la SGE | E-G5 |  |  | sale: Consulta preparada para derivacion |  |  |  |  | PROP | Tramite del monitor descrito parcialmente por el usuario, 2026-11-17; documento proyectado pendiente de precisar |
| E-T4 | 29 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | tarea | Evaluar la consulta y definir si interviene el proyectista | E-G1 |  |  | entra: Consulta; entra: Informe tecnico de supervision; entra: Opinion del proyectista cuando este integrada |  |  |  |  | NORM | ROF, art. 96.i; Reglamento, art. 190.3 |
| E-G1 | 30 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | compuerta | ¿Aplica? | E-T8 [No] (por defecto); E-T5 [Si] |  |  |  |  |  |  |  | NORM | Solicitud de opinion al proyectista; Reglamento, art. 190.3 |
| E-T5 | 31 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | tarea | Elaborar solicitud de opinion al proyectista | E-T6 |  |  | sale: Solicitud de opinion; sale: Antecedentes tecnicos |  |  |  |  | EQ | ROF, art. 96.i; flujo Bizagi |
| E-T6 | 32 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Remitir la consulta al proyectista | E-G2 |  |  |  | Al dia siguiente cuando aplica el art. 190.3 a |  |  |  | NORM | Reglamento, art. 190.3 a; flujo Bizagi |
| E-G2 | 33 | Gobierno Regional Huanuco | OACGD — Registro documentario | compuerta-eventos | ¿Que ocurre primero? | E-M1; E-R1 |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.3 a |
| E-M1 | 34 | Gobierno Regional Huanuco | OACGD — Registro documentario | mensaje-recepcion | Opinion del proyectista recibida | E-T7 |  |  | entra: Informe tecnico del proyectista |  |  |  |  | NORM | Reglamento, arts. 190.3 a y 190.6 |
| E-R1 | 35 | Gobierno Regional Huanuco | OACGD — Registro documentario | temporizador | Vencio el plazo del proyectista | E-T8 |  |  |  | 10 dias cuando aplica el art. 190.3 a |  |  |  | NORM | Reglamento, art. 190.3 a |
| E-T7 | 36 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | tarea | Evaluar la opinion del proyectista | E-T8 |  |  | entra: Informe tecnico del proyectista |  |  |  |  | NORM | Reglamento, art. 190.3 a; ROF, art. 96.i |
| E-T8 | 37 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | tarea | Elaborar informe tecnico de absolucion | E-T9 |  |  | sale: Informe tecnico de absolucion; sale: Proyecto de respuesta | 5 dias desde la opinion aplicable o el vencimiento correspondiente |  |  |  | EQ | Reglamento, art. 190.3; ROF, art. 96.i; DEC-033 |
| E-T9 | 38 | Gobierno Regional Huanuco | SGE — Subgerente de Estudios | tarea-usuario | Revisar y firmar la respuesta a la consulta | E-G3 |  |  | entra: Informe tecnico de absolucion; sale: Respuesta firmada |  |  |  |  | EQ | Precision operativa del equipo; DEC-033 |
| E-G3 | 39 | Gobierno Regional Huanuco | SGE — Subgerente de Estudios | compuerta | ¿Identifica modificacion? | E-T10 [Si]; E-G4 [No] (por defecto) |  |  |  |  |  |  |  | OBS | Flujo Bizagi; separacion adoptada en DEC-032 |
| E-T10 | 40 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | tarea | Comunicar causal de modificacion a SGGOS | E-G4 |  |  |  |  |  |  |  | PROP | S4.3.2.3 a S4.3.2.6 segun DEC-041 |
| E-G4 | 41 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | compuerta |  | E-T11 |  |  |  |  |  |  |  | PROP | Convergencia de rutas |
| E-T11 | 42 | Gobierno Regional Huanuco | SGE — Subgerente de Estudios | tarea-usuario | Notificar respuesta firmada a la SGGOS | E-T13 |  |  |  |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17 |
| E-F1 | 43 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | fin-mensaje | Respuesta comunicada al contratista |  |  |  |  |  |  | Antecedente para S4.3.2.3 cuando la respuesta identifica un adicional (E-G3) |  | EQ | Precision operativa del usuario, 2026-11-17 |
| P-E1 | 44 | Proyectista | Proyectista | inicio-mensaje | Solicitud de opinion recibida | P-T1 |  |  | entra: Solicitud y antecedentes tecnicos |  |  |  |  | NORM | Reglamento, arts. 190.3 a y 190.6 |
| P-T1 | 45 | Proyectista | Proyectista | tarea | Evaluar la consulta y el expediente tecnico | P-T2 |  |  | entra: Solicitud y antecedentes tecnicos |  |  |  |  | NORM | Reglamento, arts. 190.3 a y 190.6 |
| P-T2 | 46 | Proyectista | Proyectista | tarea | Elaborar y remitir opinion tecnica | P-F1 |  |  | sale: Informe tecnico del proyectista | 10 dias cuando aplica el art. 190.3 a |  |  |  | NORM | Reglamento, arts. 190.3 a y 190.6 |
| P-F1 | 47 | Proyectista | Proyectista | fin-mensaje | Opinion tecnica remitida |  |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.3 a |
| S-G5 | 48 | Supervision contratada | Supervisor de obra | compuerta | ¿Requiere opinion especializada? | S-T6 [Si]; S-G1 [No] (por defecto) |  |  |  |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17 |
| S-T6 | 49 | Supervision contratada | Equipo especialista de la supervision | tarea | Revisar consulta y emitir pronunciamiento | S-T7 |  |  |  |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17 |
| S-T7 | 50 | Supervision contratada | Supervisor de obra | tarea | Hacer suyo el pronunciamiento del especialista | S-G1 |  |  |  |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17 |
| E-T12 | 51 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea-usuario | Tramitar consulta a la SGE por SGD | E-T4 |  |  | sale: Consulta derivada a SGE; almacen: SGD |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17 |
| E-T13 | 52 | Gobierno Regional Huanuco | SGGOS — Monitor de obras | tarea | Preparar carta e indicar quien elabora el adicional segun bases, si corresponde | E-T14 |  |  |  |  |  |  |  | PROP | Secuencia inferida de la instruccion del usuario, 2026-11-17; confirmar alcance de «el monitor proyecta» |
| E-T14 | 53 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea | Revisar y emitir carta al contratista | E-F1 |  |  |  |  |  |  |  | PROP | Secuencia inferida de la instruccion del usuario, 2026-11-17 |
| C-E3 | 54 | Contratista | Residente de obra | inicio-mensaje | Carta de respuesta de la SGGOS recibida | C-T3 |  |  | entra: Carta y respuesta firmada de la SGE |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17 |
| S-G6 | 55 | Supervision contratada | Supervisor de obra | compuerta | ¿Adjunta informe del contratista? | S-T8 [Si]; S-F3 [No] (por defecto) |  |  |  |  |  |  |  | PROP | Propuesta de control del art. 190.2; sustento, 2026-11-17 |
| S-F3 | 56 | Supervision contratada | Supervisor de obra | fin | No atendida por falta de informe |  |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.2; regla propuesta pendiente de validacion |
| E-G5 | 57 | Gobierno Regional Huanuco | SGGOS — Monitor de obras | compuerta | ¿Falta informe exigido por art. 190.2? | E-F2 [Si]; E-T12 [No] (por defecto) |  |  |  |  |  |  |  | PROP | Propuesta de control del art. 190.2; sustento, 2026-11-17 |
| E-F2 | 58 | Gobierno Regional Huanuco | SGGOS — Monitor de obras | fin | No atendida por falta de informe |  |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.2; regla propuesta pendiente de validacion |
| S-T8 | 59 | Supervision contratada | Supervisor de obra | tarea | Emitir informe tecnico de supervision | S-T4 |  |  | sale: Informe tecnico de supervision |  |  |  |  | EQ | Precision operativa del usuario, 2026-11-17; ver sustento |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| C-F1 | S-E1 | Consulta e informe tecnico cuando corresponde |
| S-T5 | C-E2 | Respuesta a la consulta |
| S-F1 | E-E1 | Consulta e informes tecnicos de sustento |
| E-T6 | P-E1 | Solicitud de opinion y antecedentes tecnicos |
| P-F1 | E-M1 | Informe tecnico del proyectista |
| E-F1 | C-E3 | Carta de respuesta al contratista |
| E-F1 | S4.3.2.3 Gestion de adicionales y deductivos de obra | Respuesta notificada como antecedente |
