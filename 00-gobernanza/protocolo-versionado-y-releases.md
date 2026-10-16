---
id: GOV-PROT-VERSIONADO-RELEASES
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
proceso: []
fecha_creacion: 2026-10-15
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/git
---

# Protocolo de versionado y releases

## Principio

El arbol de trabajo contiene la version vigente en elaboracion. No se crean carpetas paralelas para WIP, Compartido, Publicado o Archivo. Git conserva el historial y las lineas base se inmovilizan con tags anotados y releases.

Este repositorio apoya la gestion de informacion BIM, pero no se declara por si mismo como el Entorno Comun de Datos institucional. Si en el futuro se adopta un CDE institucional, su relacion con este repositorio se documentara como un mecanismo externo de emision y aprobacion.

## Jerarquia de estados

| Situacion | Mecanismo | Regla |
|---|---|---|
| Trabajo en curso | Arbol de trabajo y commits | El archivo conserva una ruta y un nombre estables. |
| Documento de proceso en circuito de revision | Propiedades `estado_institucional: PROPUESTA` y `nivel_revision` | Avanza por `ELABORACION`, `REVISION-EQUIPO`, `OPINION-TECNICA` y `APROBACION`; cada conformidad se registra en el sustento del proceso. |
| Revision o coordinacion | Rama y solicitud de cambio; opcionalmente pre-release `-rc.N` | Debe indicar alcance, proposito, revisores y observaciones pendientes. |
| Linea base publicada | Tag anotado y release | Requiere evidencia de revision y aprobacion, manifiesto y artefactos derivados. |
| Historico o reemplazado | Release anterior e historial Git | Es inmutable; la release sucesora indica a cual reemplaza. |
| Variacion de un documento aprobado | Unico archivo `<codigo>-<documento>-propuesta.md` con la propiedad `modifica` | El documento aprobado no se edita; al aprobarse la variacion, su contenido lo reemplaza en un solo commit, se elimina el archivo `-propuesta` y se crea un nuevo tag. |

## Versiones

- `0.x`: borradores y candidatos previos a la primera aprobacion.
- `1.0.0`: primera linea base aprobada.
- `1.x`: cambios compatibles que no alteran sustancialmente alcance, flujo o producto.
- `2.0.0`: cambio sustancial de alcance, flujo o producto.

Ejemplos: `s4.3-v0.9.0-rc.1`, `s4.3-v1.0.0` y `s4.3-to-be-v1.0.0`.

## Contenido minimo de una release

1. Tag y commit exactos.
2. Alcance, proposito de uso y version.
3. Personas o instancias que elaboraron, revisaron y aprobaron.
4. Fecha y evidencia de aprobacion.
5. Fuentes maestras incluidas y derivados emitidos.
6. Decisiones abiertas, limitaciones y relacion con la version reemplazada.
7. Manifiesto basado en `00-gobernanza/plantillas/conocimiento/manifiesto-release.yaml`.
8. Identificadores y revisiones de las reglas validadas que sustentan afirmaciones normativas.

## Publicacion

Antes de crear una release de un modelo formal se valida que BPMN 2.0 XML sea la fuente maestra, que SVG/PDF sean derivados reproducibles, que AS-IS y TO-BE esten separados y que todas las afirmaciones normativas tengan trazabilidad hacia reglas en estado `VALIDADO`. El mapa institucional de procesos Nivel 0 aplica la excepcion definida en el [estandar de artefactos para el modelamiento hibrido](estandar-artefactos-modelamiento.md). El tag debe ser anotado y no debe moverse despues de publicado.

Ejemplo local, solo despues de contar con aprobacion registrada:

```powershell
git tag -a s4.3-v1.0.0 -m "Linea base aprobada de los documentos de S4.3"
git push origin s4.3-v1.0.0
```

La creacion de la release en GitHub, GitLab u otra forja se realiza a partir de ese tag. No debe publicarse solo porque los archivos esten completos tecnicamente.
