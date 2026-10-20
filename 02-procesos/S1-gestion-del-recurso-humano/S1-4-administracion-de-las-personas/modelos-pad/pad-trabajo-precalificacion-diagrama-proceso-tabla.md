---
id: BAN-PAD-MOD-PRECALIFICACION
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
proceso: []
fecha_creacion: 2026-10-20
fecha_actualizacion: 2026-10-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s1/s1-4
---

# Investigacion preliminar y precalificacion - modelo de trabajo

Sube a: [Modelos BPMN de trabajo para el PAD](00-modelos-pad.md)

`OBS` significa texto observado en el borrador; `PROP`, representacion propuesta. El detalle de nuevas evaluaciones, denuncias anonimas, prescripcion y requerimientos sin respuesta queda en el sustento documental, pendiente de aclaracion.

## Pools

| Pool | Carriles |
|---|---|
| Investigacion preliminar y precalificacion | Secretaria Tecnica |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|
| E-1 | Investigacion preliminar y precalificacion | Secretaria Tecnica | inicio | Hecho presuntamente irregular conocido | T-1 | entra: Denuncia, reporte o informe de control | OBS | 6.1.8 y 6.8.1, pp. 16-17, 22 |
| T-1 | Investigacion preliminar y precalificacion | Secretaria Tecnica | tarea | Recibir y registrar el caso | T-2 | sale: Registro del caso | OBS | 6.1.8 a y 6.8.1, pp. 16-17, 22 |
| T-2 | Investigacion preliminar y precalificacion | Secretaria Tecnica | tarea | Realizar investigacion preliminar | T-3 | entra: Antecedentes y medios probatorios | OBS | 6.5.1 y 6.8.1, pp. 19, 22 |
| T-3 | Investigacion preliminar y precalificacion | Secretaria Tecnica | tarea | Precalificar los hechos | G-1 |  | OBS | 6.1.8 d y 6.8.1, pp. 17, 22 |
| G-1 | Investigacion preliminar y precalificacion | Secretaria Tecnica | compuerta | ¿Hay sustento para recomendar inicio? | T-5 [Si]; T-4 [No] |  | PROP | 6.5.2 y 6.8.1, pp. 19-20, 22-23 |
| T-4 | Investigacion preliminar y precalificacion | Secretaria Tecnica | tarea | Emitir proveido de no ha lugar | F-1 | sale: Proveido de no ha lugar | OBS | 6.4.1 y 6.5.2 a, pp. 19-20; anexo 5, p. 44 |
| F-1 | Investigacion preliminar y precalificacion | Secretaria Tecnica | fin | Caso archivado sin PAD |  |  | OBS | 6.5.2 a, p. 20 |
| T-5 | Investigacion preliminar y precalificacion | Secretaria Tecnica | tarea | Emitir informe de precalificacion | F-2 | sale: Informe de precalificacion | OBS | 6.1.8 f y 6.5.2 b, pp. 17, 20; anexo 6, p. 45 |
| F-2 | Investigacion preliminar y precalificacion | Secretaria Tecnica | fin | Informe remitido al organo instructor |  |  | OBS | 6.5.2 b, p. 20 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| Denunciante o area informante | E-1 | Denuncia o reporte |
| T-5 | Organo Instructor | Informe de precalificacion |
