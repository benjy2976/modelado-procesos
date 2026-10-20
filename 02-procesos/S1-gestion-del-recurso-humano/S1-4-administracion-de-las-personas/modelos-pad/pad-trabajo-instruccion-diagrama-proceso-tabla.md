---
id: BAN-PAD-MOD-INSTRUCCION
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

# Fase instructiva - modelo de trabajo

Sube a: [Modelos BPMN de trabajo para el PAD](00-modelos-pad.md)

`OBS` significa texto observado en el borrador; `PROP`, representacion propuesta. La notificacion del acto marca el inicio formal del PAD segun el propio borrador (6.8.9); la actividad previa de evaluar el informe no se rotula como PAD iniciado.

## Pools

| Pool | Carriles |
|---|---|
| Fase instructiva | Organo Instructor; Secretaria Tecnica |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|
| E-1 | Fase instructiva | Organo Instructor | inicio | Informe de precalificacion recibido | G-1 | entra: Informe de precalificacion | OBS | 6.5.2 b y 6.5.3, p. 20 |
| G-1 | Fase instructiva | Organo Instructor | compuerta | ¿Se dispone iniciar el PAD? | T-2 [Si]; T-1 [No] |  | PROP | 6.5.3-6.5.4, p. 20 |
| T-1 | Fase instructiva | Organo Instructor | tarea | Motivar el pronunciamiento de no inicio | F-1 | sale: Pronunciamiento motivado | OBS | 6.5.3-6.5.4, p. 20 |
| F-1 | Fase instructiva | Organo Instructor | fin | Inicio no dispuesto |  |  | PROP | 6.5.3-6.5.4, p. 20 |
| T-2 | Fase instructiva | Organo Instructor | tarea | Emitir acto de inicio | T-3 | sale: Acto de inicio | OBS | 6.8.9-6.8.10, p. 24; anexo 7, p. 46 |
| T-3 | Fase instructiva | Secretaria Tecnica | tarea | Notificar el acto de inicio | T-4 | sale: Constancia de notificacion | OBS | 6.8.9, p. 24; 6.1.8 n, p. 17 |
| T-4 | Fase instructiva | Organo Instructor | tarea | Recibir y evaluar descargos | T-5 | entra: Descargos o constancia de vencimiento | OBS | 6.8.11-6.8.14, pp. 24-25 |
| T-5 | Fase instructiva | Organo Instructor | tarea | Emitir informe de instruccion | F-2 |  | OBS | 6.8.14, p. 25; anexo 8, p. 47 |
| F-2 | Fase instructiva | Organo Instructor | fin | Informe remitido al organo sancionador |  |  | OBS | 6.8.14, p. 25 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| Secretaria Tecnica de precalificacion | E-1 | Informe de precalificacion |
| T-3 | Servidor o ex servidor | Acto de inicio notificado |
| Servidor o ex servidor | T-4 | Descargos, si se presentan |
| T-5 | Organo Sancionador | Informe de instruccion |
