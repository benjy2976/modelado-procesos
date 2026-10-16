---
id: GOV-CONVENCIONES-NOMBRES
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: DECISION
proceso: []
fecha_creacion: 2026-10-15
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/gobernanza
  - tema/obsidian
---

# Convenciones de nombres y versiones

## Archivos de trabajo

- Sin tildes y con guiones como separador.
- El estado y la version se registran en metadatos y Git, no en cadenas como `final-final2`.
- Sufijos reservados: `-propuesta` para la unica variacion de un documento aprobado y `-to-be` para los documentos del arbol TO-BE.

## Mayusculas para enfatizar

Las mayusculas marcan tres niveles visuales (`DEC-019`); fuera de ellos todo nombre va en minusculas.

| Nivel | Regla | Ejemplos |
|---|---|---|
| 1. Entrada y areas | Nota indice completa en mayusculas | `00-GESTION-POR-PROCESOS-GRH.md`, `00-PROCESOS.md`, `00-GOBERNANZA.md` |
| 2. Procesos | Codigo NT en mayusculas, con guion en lugar de punto; el resto en minusculas | Carpetas `S4-gestion-de-las-inversiones/`, `S4-3-ejecucion-inversion/`; indice `00-S4-3-ejecucion-inversion.md`; documentos `S4-3-ficha-producto-proceso.md`, `S4-3-fichas-indicador.md`, `S4-3-sustento.md`, `S4-3-diagrama-proceso.bpmn` |
| 3. Contenido | Minusculas | `registro-decisiones.md`, `00-bases.md` |

- Las carpetas de area conservan su nombre en minusculas (`02-procesos/`); solo su nota indice va en mayusculas.
- Los indices de subareas que no son procesos van en minusculas.
- Dos archivos no pueden diferir solo en mayusculas: Windows no los distingue y GitHub si.
- En Windows, un cambio solo de mayusculas se hace con `git mv` en dos pasos, pasando por un nombre temporal, y se comprueba que la carpeta en disco quede igual que en Git.
- Los enlaces deben coincidir exactamente en mayusculas con el nombre del archivo.
- Las etiquetas y los nombres de propiedades van siempre en minusculas.

## Versionado

- `0.x`: borradores y revisiones previas a la primera aprobacion.
- `1.0`: primera linea base publicada.
- `1.x`: ajustes compatibles sin cambio sustancial de alcance.
- `2.0`: cambio sustancial de alcance, flujo o producto.

## Etiquetas Git sugeridas

- `s4.3-v0.9.0-rc.1`: candidato distribuido para revision.
- `s4.3-v1.0.0`: primera linea base aprobada de los documentos de S4.3.
- `s4.3-v1.1.0`: actualizacion compatible aprobada.
- `s4.3-v2.0.0`: cambio sustancial aprobado.
- `s4.3-to-be-v1.0.0`: primera linea base del TO-BE, cuando se desarrolle.

Los estados no se agregan al nombre de los archivos ni se representan con carpetas duplicadas. Un tag sin sufijo `rc` identifica una linea base publicada; las publicaciones anteriores constituyen el historial archivado.

## Commits sugeridos

- `docs:` documentacion y fuentes.
- `feat(s4.3):` nueva parte del modelo.
- `fix(s4.3):` correccion del modelo.
- `review(s4.3):` observaciones aplicadas.
- `publish(s4.3):` establecimiento de linea base.
