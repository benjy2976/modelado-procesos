# Protocolo de versionado y releases

## Principio

El arbol de trabajo contiene la version vigente en elaboracion. No se crean carpetas paralelas para WIP, Compartido, Publicado o Archivo. Git conserva el historial y las lineas base se inmovilizan con tags anotados y releases.

Este repositorio apoya la gestion de informacion BIM, pero no se declara por si mismo como el Entorno Comun de Datos institucional. Si en el futuro se adopta un CDE institucional, su relacion con este repositorio se documentara como un mecanismo externo de emision y aprobacion.

## Jerarquia de estados

| Situacion | Mecanismo | Regla |
|---|---|---|
| Trabajo en curso | Arbol de trabajo y commits | El archivo conserva una ruta y un nombre estables. |
| Revision o coordinacion | Rama y solicitud de cambio; opcionalmente pre-release `-rc.N` | Debe indicar alcance, proposito, revisores y observaciones pendientes. |
| Linea base publicada | Tag anotado y release | Requiere evidencia de revision y aprobacion, manifiesto y artefactos derivados. |
| Historico o reemplazado | Release anterior e historial Git | Es inmutable; la release sucesora indica a cual reemplaza. |

## Versiones

- `0.x`: borradores y candidatos previos a la primera aprobacion.
- `1.0.0`: primera linea base aprobada.
- `1.x`: cambios compatibles que no alteran sustancialmente alcance, flujo o producto.
- `2.0.0`: cambio sustancial de alcance, flujo o producto.

Ejemplos: `s4.3-as-is-v0.9.0-rc.1`, `s4.3-as-is-v1.0.0` y `s4.3-to-be-v1.0.0`.

## Contenido minimo de una release

1. Tag y commit exactos.
2. Alcance, proposito de uso y version.
3. Personas o instancias que elaboraron, revisaron y aprobaron.
4. Fecha y evidencia de aprobacion.
5. Fuentes maestras incluidas y derivados emitidos.
6. Decisiones abiertas, limitaciones y relacion con la version reemplazada.
7. Manifiesto basado en `04-recursos-reutilizables/plantillas/manifiesto-release.yaml`.
8. Identificadores y revisiones de las reglas validadas que sustentan afirmaciones normativas.

## Publicacion

Antes de crear una release se valida que BPMN 2.0 XML sea la fuente maestra, que SVG/PDF sean derivados reproducibles, que AS-IS y TO-BE esten separados y que todas las afirmaciones normativas tengan trazabilidad hacia reglas en estado `VALIDADO`. El tag debe ser anotado y no debe moverse despues de publicado.

Ejemplo local, solo despues de contar con aprobacion registrada:

```powershell
git tag -a s4.3-as-is-v1.0.0 -m "Linea base aprobada del AS-IS de S4.3"
git push origin s4.3-as-is-v1.0.0
```

La creacion de la release en GitHub, GitLab u otra forja se realiza a partir de ese tag. No debe publicarse solo porque los archivos esten completos tecnicamente.
