---
id: BAN-PAD-MOD-RECURSOS
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

# Derivacion de recursos - modelo de trabajo

Sube a: [Modelos BPMN de trabajo para el PAD](00-modelos-pad.md)

`OBS` significa texto observado en el borrador; `PROP`, representacion propuesta. La vista llega hasta la resolucion de la reconsideracion o la elevacion de la apelacion; no dibuja una segunda instancia cuyo detalle no consta en la fuente.

## Pools

| Pool | Carriles |
|---|---|
| Derivacion de recursos | Secretaria Tecnica; Organo Sancionador |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|
| E-1 | Derivacion de recursos | Secretaria Tecnica | inicio | Recurso recibido | G-1 | entra: Recurso presentado | OBS | 6.16.1, p. 31 |
| G-1 | Derivacion de recursos | Secretaria Tecnica | compuerta | ¿Es reconsideracion? | T-1 [Si]; G-2 [No] |  | PROP | 6.16.1, p. 31 |
| T-1 | Derivacion de recursos | Organo Sancionador | tarea | Resolver reconsideracion | F-1 | sale: Decision de reconsideracion | OBS | 6.16.1, p. 31 |
| F-1 | Derivacion de recursos | Organo Sancionador | fin | Reconsideracion resuelta |  |  | PROP | 6.16.1, p. 31 |
| G-2 | Derivacion de recursos | Secretaria Tecnica | compuerta | ¿Apelacion de amonestacion escrita? | T-2 [Si]; T-3 [No] |  | PROP | 6.16.2, p. 31 |
| T-2 | Derivacion de recursos | Secretaria Tecnica | tarea | Derivar apelacion a Recursos Humanos | F-2 | sale: Expediente de apelacion | OBS | 6.16.2, p. 31 |
| F-2 | Derivacion de recursos | Secretaria Tecnica | fin | Apelacion derivada a Recursos Humanos |  |  | PROP | 6.16.2, p. 31 |
| T-3 | Derivacion de recursos | Secretaria Tecnica | tarea | Elevar apelacion al Tribunal | F-3 | sale: Expediente de apelacion | OBS | 6.16.2 y 6.18.4, pp. 31-32 |
| F-3 | Derivacion de recursos | Secretaria Tecnica | fin | Apelacion elevada al Tribunal |  |  | PROP | 6.16.2 y 6.18.4, pp. 31-32 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| Servidor o ex servidor | E-1 | Recurso presentado |
| T-1 | Servidor o ex servidor | Decision de reconsideracion |
| T-2 | Recursos Humanos | Apelacion |
| T-3 | Tribunal del Servicio Civil | Apelacion |
