---
id: AP-S4-3-2-2-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.2
nivel_proceso: 3
perfil_trazado: zigzag-controlado
proceso:
  - S4.3.2.2
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-10
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

## Pools

| Pool | Carriles |
|---|---|
| Contratista | Residente de obra; Equipo especialista del ejecutor |
| Supervision contratada | Supervisor de obra; Equipo especialista de la supervision |
| Gobierno Regional Huanuco | OACGD — Registro documentario; SGGOS — Coordinador de obra; SGE — Especialistas tecnicos; SGE — Subgerente de Estudios |
| Proyectista | Proyectista |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Grupo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C-E1 | Contratista | Residente de obra | inicio | Necesidad de consulta identificada | C-G1 |  |  |  |  |  |  |  | EQ | Descripcion operativa del equipo; Reglamento, art. 190.1 |
| C-G1 | Contratista | Residente de obra | compuerta | ¿La consulta requiere informe tecnico? | C-T1 [Si]; C-G2 [No] (por defecto) |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.2; precision operativa del equipo |
| C-T1 | Contratista | Equipo especialista del ejecutor | tarea | Elaborar informe tecnico de especialidad | C-G2 |  |  | sale: Informe tecnico de especialidad |  |  |  |  | EQ | Precision operativa del equipo |
| C-G2 | Contratista | Residente de obra | compuerta |  | C-T2 |  |  |  |  |  |  |  | PROP | Convergencia de rutas |
| C-T2 | Contratista | Residente de obra | tarea-usuario | Registrar la consulta en el Cuaderno de Incidencias | C-F1 |  |  | sale: Consulta y antecedentes; sale: Informe tecnico cuando corresponda |  |  |  |  | NORM | Reglamento, arts. 188 y 190.1-190.2 |
| C-F1 | Contratista | Residente de obra | fin-mensaje | Consulta remitida al supervisor |  |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.1 |
| C-E2 | Contratista | Residente de obra | inicio-mensaje | Respuesta a la consulta recibida | C-T3 |  |  | entra: Respuesta a la consulta |  |  |  |  | OBS | Flujo Bizagi y precision operativa del equipo |
| C-T3 | Contratista | Residente de obra | tarea-usuario | Tomar conocimiento y registrar la respuesta | C-F2 |  |  | sale: Registro de respuesta |  |  |  |  | PROP | Cierre operativo de la consulta |
| C-F2 | Contratista | Residente de obra | fin | Consulta atendida para el ejecutor |  |  |  |  |  |  |  |  | PROP | Producto del proceso |
| S-E1 | Supervision contratada | Supervisor de obra | inicio-mensaje | Consulta del ejecutor recibida | S-T1 |  |  | entra: Consulta y antecedentes |  |  |  |  | NORM | Reglamento, art. 190.1 |
| S-T1 | Supervision contratada | Supervisor de obra | tarea | Revisar la consulta y el expediente tecnico | S-G1 |  |  | entra: Consulta; entra: Informe tecnico cuando corresponda |  |  |  |  | OBS | Flujo Bizagi; Reglamento, art. 190 |
| S-G1 | Supervision contratada | Supervisor de obra | compuerta | ¿Puede absolver sin modificar? | S-T2 [Si]; S-G2 [No] (por defecto) |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.1 |
| S-T2 | Supervision contratada | Supervisor de obra | tarea | Absolver la consulta dentro de su competencia | S-G4 |  |  | sale: Respuesta del supervisor |  |  |  |  | NORM | Reglamento, art. 190.1 |
| S-E2 | Supervision contratada | Supervisor de obra | inicio |  | S-T0 |  |  |  |  |  |  |  | EQ | Consulta originada por la supervision; precision operativa del equipo |
| S-T0 | Supervision contratada | Supervisor de obra | tarea | Identificar consulta propia | S-G2 |  |  | sale: Antecedentes de la supervision |  |  |  |  | EQ | Precision operativa del equipo |
| S-G2 | Supervision contratada | Supervisor de obra | compuerta | ¿Especialista? | S-T3 [Si]; S-G3 [No] (por defecto) |  |  |  |  |  |  |  | EQ | Precision operativa del equipo |
| S-T3 | Supervision contratada | Equipo especialista de la supervision | tarea | Elaborar informe tecnico de especialidad | S-G3 |  |  | sale: Informe tecnico de especialidad |  |  |  |  | EQ | Precision operativa del equipo |
| S-G3 | Supervision contratada | Supervisor de obra | compuerta |  | S-T4 |  |  |  |  |  |  |  | PROP | Convergencia de rutas |
| S-T4 | Supervision contratada | Supervisor de obra | tarea | Elaborar opinion tecnica y elevar la consulta a la entidad | S-F1 |  |  | sale: Consulta elevada; sale: Opinion tecnica del supervisor | 5 dias desde la anotacion cuando aplica el art. 190.3 |  |  |  | NORM | Reglamento, art. 190.3; flujo Bizagi |
| S-F1 | Supervision contratada | Supervisor de obra | fin-mensaje | Consulta elevada a la entidad |  |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.3 |
| S-E3 | Supervision contratada | Supervisor de obra | inicio-mensaje | Respuesta de la entidad recibida | S-G4 |  |  | entra: Respuesta firmada |  |  |  |  | OBS | Flujo Bizagi y precision operativa del equipo |
| S-G4 | Supervision contratada | Supervisor de obra | compuerta |  | S-T5 |  |  |  |  |  |  |  | PROP | Convergencia de respuestas |
| S-T5 | Supervision contratada | Supervisor de obra | tarea-usuario | Registrar la respuesta y comunicarla al ejecutor | S-F2 |  |  | sale: Respuesta comunicada |  |  |  |  | OBS | Flujo Bizagi; practica descrita por el equipo |
| S-F2 | Supervision contratada | Supervisor de obra | fin-mensaje | Respuesta comunicada al ejecutor |  |  |  |  |  |  |  |  | PROP | Producto del proceso |
| E-E1 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Consulta recibida por Mesa de Partes | E-T1 |  |  | entra: Consulta elevada; entra: Opinion tecnica del supervisor |  |  |  |  | EQ | Precision operativa del equipo; ROF, art. 20 |
| E-T1 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Registrar y derivar la consulta a la SGGOS por SGD | E-T2 |  |  | sale: Registro y proveido de derivacion; almacen: SGD |  |  |  |  | OBS | Flujo Bizagi; precision operativa del equipo; observacion del usuario, 2026-11-10 |
| E-T2 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Recibir y asignar la consulta para su seguimiento por SGD | E-T3 |  |  | entra: Consulta y antecedentes; almacen: SGD |  |  |  |  | EQ | ROF, arts. 97-98; precision operativa del equipo; observacion del usuario, 2026-11-10 |
| E-T3 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Verificar antecedentes y canalizar la consulta a la SGE por SGD | E-T4 |  |  | sale: Consulta canalizada; almacen: SGD |  |  |  |  | EQ | ROF, arts. 97-98; flujo Bizagi; DEC-033; observacion del usuario, 2026-11-10 |
| E-T4 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | tarea | Evaluar la consulta y definir si interviene el proyectista | E-G1 |  |  | entra: Consulta; entra: Opinion del supervisor; entra: Opinion del proyectista cuando este integrada |  |  |  |  | NORM | ROF, art. 96.i; Reglamento, art. 190.3 |
| E-G1 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | compuerta | ¿Aplica? | E-T8 [No] (por defecto); E-T5 [Si] |  |  |  |  |  |  |  | NORM | Solicitud de opinion al proyectista; Reglamento, art. 190.3 |
| E-T5 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | tarea | Elaborar solicitud de opinion al proyectista | E-T6 |  |  | sale: Solicitud de opinion; sale: Antecedentes tecnicos |  |  |  |  | EQ | ROF, art. 96.i; flujo Bizagi |
| E-T6 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Remitir la consulta al proyectista | E-G2 |  |  |  | Al dia siguiente cuando aplica el art. 190.3 a |  |  |  | NORM | Reglamento, art. 190.3 a; flujo Bizagi |
| E-G2 | Gobierno Regional Huanuco | OACGD — Registro documentario | compuerta-eventos | ¿Que ocurre primero? | E-M1; E-R1 |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.3 a |
| E-M1 | Gobierno Regional Huanuco | OACGD — Registro documentario | mensaje-recepcion | Opinion del proyectista recibida | E-T7 |  |  | entra: Informe tecnico del proyectista |  |  |  |  | NORM | Reglamento, arts. 190.3 a y 190.6 |
| E-R1 | Gobierno Regional Huanuco | OACGD — Registro documentario | temporizador | Vencio el plazo del proyectista | E-T8 |  |  |  | 10 dias cuando aplica el art. 190.3 a |  |  |  | NORM | Reglamento, art. 190.3 a |
| E-T7 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | tarea | Evaluar la opinion del proyectista | E-T8 |  |  | entra: Informe tecnico del proyectista |  |  |  |  | NORM | Reglamento, art. 190.3 a; ROF, art. 96.i |
| E-T8 | Gobierno Regional Huanuco | SGE — Especialistas tecnicos | tarea | Elaborar informe tecnico de absolucion | E-T9 |  |  | sale: Informe tecnico de absolucion; sale: Proyecto de respuesta | 5 dias desde la opinion aplicable o el vencimiento correspondiente |  |  |  | EQ | Reglamento, art. 190.3; ROF, art. 96.i; DEC-033 |
| E-T9 | Gobierno Regional Huanuco | SGE — Subgerente de Estudios | tarea-usuario | Revisar y firmar la respuesta a la consulta | E-G3 |  |  | entra: Informe tecnico de absolucion; sale: Respuesta firmada |  |  |  |  | EQ | Precision operativa del equipo; DEC-033 |
| E-G3 | Gobierno Regional Huanuco | SGE — Subgerente de Estudios | compuerta | ¿Identifica modificacion? | E-T10 [Si]; E-G4 [No] (por defecto) |  |  |  |  |  |  |  | OBS | Flujo Bizagi; separacion adoptada en DEC-032 |
| E-T10 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-envio | Derivar causal | E-G4 |  |  | sale: Causal y antecedentes de modificacion |  |  |  |  | PROP | S4.3.2.3 a S4.3.2.6 segun DEC-041 |
| E-G4 | Gobierno Regional Huanuco | OACGD — Registro documentario | compuerta |  | E-T11 |  |  |  |  |  |  |  | PROP | Convergencia de rutas |
| E-T11 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Notificar la respuesta firmada al supervisor | E-F1 |  |  | sale: Respuesta notificada |  |  |  |  | EQ | Flujo Bizagi; precision operativa del equipo; DEC-033 |
| E-F1 | Gobierno Regional Huanuco | OACGD — Registro documentario | fin-mensaje | Respuesta institucional notificada |  |  |  |  |  |  |  |  | PROP | Producto del proceso |
| P-E1 | Proyectista | Proyectista | inicio-mensaje | Solicitud de opinion recibida | P-T1 |  |  | entra: Solicitud y antecedentes tecnicos |  |  |  |  | NORM | Reglamento, arts. 190.3 a y 190.6 |
| P-T1 | Proyectista | Proyectista | tarea | Evaluar la consulta y el expediente tecnico | P-T2 |  |  | entra: Solicitud y antecedentes tecnicos |  |  |  |  | NORM | Reglamento, arts. 190.3 a y 190.6 |
| P-T2 | Proyectista | Proyectista | tarea | Elaborar y remitir opinion tecnica | P-F1 |  |  | sale: Informe tecnico del proyectista | 10 dias cuando aplica el art. 190.3 a |  |  |  | NORM | Reglamento, arts. 190.3 a y 190.6 |
| P-F1 | Proyectista | Proyectista | fin-mensaje | Opinion tecnica remitida |  |  |  |  |  |  |  |  | NORM | Reglamento, art. 190.3 a |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| C-F1 | S-E1 | Consulta e informe tecnico |
| S-T5 | C-E2 | Respuesta a la consulta |
| S-F1 | E-E1 | Consulta elevada y opinion tecnica del supervisor |
| E-T6 | P-E1 | Solicitud de opinion y antecedentes tecnicos |
| P-F1 | E-M1 | Informe tecnico del proyectista |
| E-T11 | S-E3 | Respuesta firmada por el Subgerente de Estudios |
