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
fecha_actualizacion: 2026-11-06
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-6
---

# S4.3.2.6 Gestion de paralizacion y reinicio

Sube a: [S4.3.2.6 Gestion de paralizacion y reinicio](00-S4-3-2-6-gestion-paralizacion-reinicio.md)

Modelo inicial extraido de la anterior variante agrupada. Una instancia atiende un evento de paralizacion o de reinicio; despues de la validacion comun, los actos y cierres se mantienen separados. No existe una espera indefinida entre ambos eventos.

Ejecutor de obra agrupa al residente y los demas roles del ejecutor cuando intervengan. Control de obra es una abstraccion funcional ejercida alternativamente por supervisor contratado o inspector de la entidad, segun modalidad; no supone concurrencia ni identidad organizacional (`DEC-042`).

## Pools

| Pool | Carriles |
|---|---|
| Ejecutor de obra | Residente de obra |
| Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad |
| Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental; SGGOS — Coordinador de obra; Especialista competente; Titular de la competencia o autoridad delegada |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| R-E1 | Ejecutor de obra | Residente de obra | inicio-condicional | Evento de paralizacion o reinicio identificado | R-T1 |  |  | NORM | Ley 31589, art. 2; Directiva 017-2023-CG, num. 7.3.7 |
| R-T1 | Ejecutor de obra | Residente de obra | tarea-usuario | Registrar y sustentar el evento en el Cuaderno de Incidencias | R-F1 | sale: Causal de paralizacion o solicitud de reinicio |  | NORM | Directiva 017-2023-CG, num. 7.3.7; Reglamento, art. 188.3 cuando corresponda |
| R-F1 | Ejecutor de obra | Residente de obra | fin-mensaje | Evento y sustento remitidos |  |  |  | PROP | Aplicacion operativa de las fuentes citadas |
| S-E1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | inicio-mensaje | Evento y sustento recibidos | S-T1 | entra: Causal o solicitud |  | NORM | Directiva 017-2023-CG, num. 7.3.7 |
| S-T1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | tarea | Validar la causal o las condiciones de reinicio | S-F1 | sale: Validacion y opinion |  | NORM | Directiva 017-2023-CG, num. 7.3.7; Ley 31589, art. 5.2 en su ambito |
| S-F1 | Control de obra | Supervisor contratado o inspector de la entidad, segun modalidad | fin-mensaje | Evento validado y remitido |  |  |  | PROP | Circuito propuesto sobre las fuentes citadas |
| E-E1 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | inicio-mensaje | Expediente recibido | E-T1 | entra: Evento, sustento y opinion |  | EQ | ROF, art. 20; DEC-041 |
| E-T1 | Gobierno Regional Huanuco | Oficina de Atencion al Ciudadano y Gestion Documental | tarea-usuario | Registrar y derivar a la SGGOS | E-T2 | sale: Registro y derivacion |  | NORM | ROF, art. 20 |
| E-T2 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Verificar integridad y clasificar regimen y evento | E-G1 | entra: Expediente |  | EQ | ROF, arts. 97-98; DEC-041 |
| E-G1 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Requiere evaluacion tecnica especializada? | E-T3 [Si]; E-G2 [No] (por defecto) |  |  | EQ | El coordinador no sustituye al especialista; DEC-041 |
| E-T3 | Gobierno Regional Huanuco | Especialista competente | tarea | Evaluar causal o condiciones tecnicas | E-G2 | sale: Evaluacion especializada |  | PROP | Alcance exacto pendiente por regimen |
| E-G2 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Que se gestiona? | E-T4 [Paralizacion]; E-T7 [Reinicio] |  |  | EQ | Separacion adoptada en DEC-041 |
| E-T4 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Consolidar el expediente de paralizacion | E-T5 | sale: Expediente consolidado |  | PROP | No sustituye opiniones especializadas |
| E-T5 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Resolver sobre la paralizacion | E-G3 | entra: Expediente consolidado; sale: Pronunciamiento |  | NORM | Ley 31589, art. 5.2; Directiva 017-2023-CG, num. 7.3.7 |
| E-G3 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | compuerta | ¿Favorable? | E-T6 [Si] (por defecto); E-F2 [No] |  |  | PROP | Rutas de decision; tratamiento completo por regimen pendiente |
| E-T6 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Actualizar registros y coordinar la comunicacion | E-F1 | sale: Registros y comunicacion |  | PROP | Circuito interno pendiente de validacion |
| E-F1 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Paralizacion formalizada y comunicada |  |  |  | PROP | Producto propuesto |
| E-F2 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | Paralizacion no formalizada comunicada |  |  |  | PROP | Producto alterno |
| E-T7 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Consolidar el sustento de reinicio | E-T8 | sale: Sustento consolidado |  | PROP | No sustituye evaluaciones especializadas |
| E-T8 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | tarea-usuario | Formalizar el reinicio | E-G4 | entra: Sustento consolidado; sale: Pronunciamiento |  | NORM | Directiva 017-2023-CG, num. 7.3.7; contrata: EVIDENCIA-INSUFICIENTE |
| E-G4 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | compuerta | ¿Favorable? | E-T9 [Si] (por defecto); E-F4 [No] |  |  | PROP | Rutas de decision |
| E-T9 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea-usuario | Actualizar registros y coordinar la comunicacion | E-F3 | sale: Registros y comunicacion |  | PROP | Circuito interno pendiente de validacion |
| E-F3 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Reinicio formalizado y comunicado |  |  |  | PROP | Producto propuesto |
| E-F4 | Gobierno Regional Huanuco | Titular de la competencia o autoridad delegada | fin-mensaje | Reinicio no formalizado comunicado |  |  |  | PROP | Producto alterno |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| R-F1 | S-E1 | Evento y sustento |
| S-F1 | E-E1 | Evento validado y opinion |
