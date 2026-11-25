---
id: AP-S4-3-2-5-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.5
nivel_proceso: 3
perfil_trazado: zigzag-controlado
proceso:
  - S4.3.2.5
fecha_creacion: 2026-11-05
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-5
---

# S4.3.2.5 Formalizacion de suspensiones de plazo

Sube a: [S4.3.2.5 Formalizacion de suspensiones de plazo](00-S4-3-2-5-formalizacion-suspensiones-plazo.md)

Modelo inicial extraido de la anterior variante agrupada de suspension. La ruta normativa sustentada corresponde a la suspension contractual. La figura equivalente en administracion directa permanece como `EVIDENCIA-INSUFICIENTE` y no se presume.

Residente de obra y contratista o representante legal pertenecen al mismo participante Contratista y se mantienen en carriles distintos por sus responsabilidades tecnica y contractual. Supervisor o inspector de obra es una abstraccion funcional ejercida alternativamente por supervisor contratado o inspector de la entidad; no supone concurrencia ni identidad organizacional (`DEC-042`).

## Pools

| Pool | Carriles |
|---|---|
| Contratista | Residente de obra; Contratista o representante legal del contratista, solo contrata |
| Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad |
| Gobierno Regional Huanuco | OACGD — Registro documentario; SGGOS — Coordinador de obra; Especialista competente; Titular de la competencia o autoridad delegada |

## Elementos

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Anotacion | Clase | Fuente |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-E1 | 1 | Contratista | Residente de obra | inicio-condicional | Causa que impide continuar identificada | R-T1 |  |  |  | NORM | Reglamento, art. 202.1 |
| R-T1 | 2 | Contratista | Residente de obra | tarea-usuario | Registrar y sustentar la causa en el Cuaderno de Incidencias | R-F1 | sale: Registro y sustento |  |  | NORM | Reglamento, arts. 188.3 y 202.1 |
| R-F1 | 3 | Contratista | Residente de obra | fin-mensaje | Causa de suspension remitida |  |  |  |  | PROP | Aplicacion operativa del Reglamento, art. 202.1 |
| S-E1 | 4 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Causa de suspension recibida | S-T1 | entra: Registro y sustento |  |  | PROP | Aplicacion operativa; validacion institucional pendiente |
| S-T1 | 5 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Evaluar el impedimento y emitir opinion | S-F1 | sale: Opinion |  |  | NORM | Reglamento, arts. 186-188 y 202.1 |
| S-F1 | 6 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Causa y opinion remitidas |  |  |  |  | PROP | Circuito propuesto sobre la fuente citada |
| E-E1 | 7 | Gobierno Regional Huanuco | OACGD — Registro documentario | inicio-mensaje | Expediente de suspension recibido | E-T1 | entra: Causa y opinion |  |  | EQ | ROF, art. 20; DEC-041 |
| E-T1 | 8 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Registrar y derivar a SGGOS por SGD | E-T2 | sale: Registro y derivacion; almacen: SGD |  |  | EQ | ROF, art. 20; observacion del usuario, 2026-11-10 |
| E-T2 | 9 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Verificar integridad y clasificar la figura | E-G1 | entra: Expediente |  |  | EQ | ROF, arts. 97-98; DEC-041 |
| E-G1 | 10 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Corresponde suspension contractual? | E-T3 [Si]; E-F2 [No] |  |  |  | NORM | Reglamento, art. 202.1; AD: EVIDENCIA-INSUFICIENTE |
| E-T3 | 11 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Coordinar las condiciones de suspension con el contratista o su representante legal | E-M1 |  |  |  | NORM | Reglamento, art. 202.1: acuerdo de las partes |
| E-E2 | 29 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | inicio-condicional | Contrato directamente vinculado resuelto | E-T3 |  |  | Las partes pueden acordar suspender el plazo de la obra hasta perfeccionar un nuevo contrato vinculado | NORM | Reglamento, art. 202.5 |
| E-E3 | 30 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | inicio-mensaje | Paralizacion derivada para suspension recibida | E-T3 | entra: Paralizacion derivada |  | Proviene de S4.3.2.6 cuando la paralizacion no es atribuible al contratista | PROP | Practica institucional informada por el usuario, 2026-11-25; Reglamento, art. 202.1 |
| E-M1 | 12 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | mensaje-recepcion | Respuesta del ejecutor recibida | E-G2 | entra: Respuesta del contratista o su representante legal |  |  | NORM | Reglamento, art. 202.1 |
| E-G2 | 13 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Existe acuerdo de suspension? | E-T4 [Si]; E-F2 [No] |  |  |  | NORM | Reglamento, art. 202.1 |
| E-T4 | 14 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Consolidar el acuerdo y elevarlo por SGD | E-T5 | sale: Acuerdo consolidado; almacen: SGD |  |  | PROP | No sustituye la decision formal; observacion del usuario, 2026-11-10 |
| E-T5 | 15 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Formalizar la suspension de plazo | E-T5A | entra: Acuerdo consolidado; sale: Acto de suspension |  |  | NORM | Reglamento, arts. 107 y 202 |
| E-T5A | 27 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Suspender el plazo de los contratos vinculados, cuando corresponda | E-T6 |  |  |  | NORM | Reglamento, art. 107.3 |
| E-T6 | 16 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Actualizar registros y coordinar la comunicacion | E-F1 | sale: Registros y comunicacion |  |  | PROP | Circuito interno pendiente de validacion |
| E-F1 | 17 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Suspension de plazo formalizada y comunicada |  |  |  |  | PROP | Producto propuesto |
| E-F2 | 18 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Suspension no formalizada comunicada |  |  |  |  | PROP | Producto alterno |
| C-E1 | 19 | Contratista | Contratista o representante legal del contratista, solo contrata | inicio-mensaje | Propuesta de suspension recibida | C-T1 |  |  |  | NORM | Reglamento, art. 202.1 |
| C-T1 | 20 | Contratista | Contratista o representante legal del contratista, solo contrata | tarea | Evaluar y responder la propuesta | C-F1 | sale: Respuesta |  |  | NORM | Reglamento, art. 202.1 |
| C-F1 | 21 | Contratista | Contratista o representante legal del contratista, solo contrata | fin-mensaje | Respuesta a la propuesta remitida |  |  |  |  | NORM | Reglamento, art. 202.1 |
| E-R1 | 22 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | inicio-condicional | Cese de la causa de suspension verificado | E-T7 |  |  |  | NORM | Reglamento, arts. 107.2 y 202.2 |
| E-T7 | 23 | Gobierno Regional Huanuco | Especialista competente | tarea | Verificar condiciones para reanudar el plazo | E-T8 | sale: Verificacion |  |  | NORM | Reglamento, arts. 107.2 y 202.2 |
| E-T8 | 24 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Consolidar la verificacion y elevarla por SGD | E-T9 | sale: Sustento de reanudacion; almacen: SGD |  |  | PROP | Circuito interno pendiente de validacion; observacion del usuario, 2026-11-10 |
| E-T9 | 25 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Formalizar la reanudacion del plazo suspendido | E-T9A | sale: Acto de reanudacion |  |  | NORM | Reglamento, arts. 107.2 y 202.2 |
| E-T9A | 28 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Suscribir acta de reinicio de los contratos vinculados suspendidos | E-F3 |  |  |  | NORM | Reglamento, art. 107.3 |
| E-F3 | 26 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | Reanudacion del plazo formalizada |  |  |  |  | PROP | Producto de la instancia posterior |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| R-F1 | S-E1 | Causa y sustento |
| S-F1 | E-E1 | Causa y opinion |
| E-T3 | C-E1 | Propuesta de suspension |
| C-F1 | E-M1 | Respuesta del ejecutor |
| S4.3.2.6 Gestion de paralizacion y reinicio | E-E3 | Paralizacion derivada para suspension |
