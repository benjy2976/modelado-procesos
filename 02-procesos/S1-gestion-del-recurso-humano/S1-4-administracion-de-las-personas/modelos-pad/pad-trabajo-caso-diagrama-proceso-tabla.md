---
id: BAN-PAD-MOD-CASO
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

# Gestion del caso disciplinario - modelo de trabajo

Sube a: [Modelos BPMN de trabajo para el PAD](00-modelos-pad.md)

Vista de fases del borrador. `OBS` significa texto observado en el **borrador**, no practica AS-IS ni regla normativa validada; `PROP` identifica una decision de representacion pendiente de revision. Las actividades de llamada resumen los diagramas de esta carpeta y no afirman que sean procesos institucionales codificados.

## Pools

| Pool | Carriles |
|---|---|
| Gestion del caso disciplinario | Secretaria Tecnica; Organo Instructor; Organo Sancionador |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|
| E-1 | Gestion del caso disciplinario | Secretaria Tecnica | inicio | Caso conocido | SP-1 | entra: Denuncia, reporte o informe de control | OBS | PDF directiva propuesta, 6.8.1, pp. 22-23 |
| SP-1 | Gestion del caso disciplinario | Secretaria Tecnica | subproceso | Investigar y precalificar | G-1 | sale: Proveido o informe de precalificacion | OBS | 6.5 y 6.8.1, pp. 19-23 |
| G-1 | Gestion del caso disciplinario | Secretaria Tecnica | compuerta | ¿Se recomienda iniciar PAD? | SP-2 [Si]; F-1 [No] |  | PROP | 6.5.2, pp. 19-20 |
| F-1 | Gestion del caso disciplinario | Secretaria Tecnica | fin | No ha lugar y archivo |  | sale: Proveido de no ha lugar | OBS | 6.4 y 6.5.2, pp. 19-20 |
| SP-2 | Gestion del caso disciplinario | Organo Instructor | subproceso | Tramitar fase instructiva | G-2 | sale: Pronunciamiento o informe de instruccion | OBS | 6.5.3-6.5.4 y 6.8.2-6.8.14, pp. 20, 23-25 |
| G-2 | Gestion del caso disciplinario | Organo Instructor | compuerta | ¿Se dispuso el inicio del PAD? | SP-3 [Si]; F-2 [No] |  | PROP | 6.5.3-6.5.4 y 6.8.9, pp. 20, 24 |
| F-2 | Gestion del caso disciplinario | Organo Instructor | fin | Inicio no dispuesto |  | sale: Pronunciamiento motivado | OBS | 6.5.3-6.5.4, p. 20 |
| SP-3 | Gestion del caso disciplinario | Organo Sancionador | subproceso | Resolver fase sancionadora | G-3 |  | OBS | 6.8.15-6.8.23, pp. 25-27 |
| G-3 | Gestion del caso disciplinario | Organo Sancionador | compuerta | ¿Resultado de la decision? | F-3 [Sancion]; F-4 [Archivo] |  | PROP | 6.8.15 y 6.8.23, pp. 25-27 |
| F-3 | Gestion del caso disciplinario | Organo Sancionador | fin | Sancion decidida |  | sale: Acto de sancion | OBS | 6.8.23, p. 27; anexo 9, p. 48 |
| F-4 | Gestion del caso disciplinario | Organo Sancionador | fin | Archivo decidido |  | sale: Acto de archivo | OBS | 6.8.23, p. 27; anexo 10, p. 49 |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| Denunciante o area informante | E-1 | Denuncia o reporte |
| SP-3 | Servidor o ex servidor | Decision final comunicada |
