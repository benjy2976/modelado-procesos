# Convenciones de nombres y versiones

## Archivos de trabajo

- Minusculas, sin tildes, separados por guiones.
- Codigo de proceso al inicio cuando corresponda.
- El estado y la version se registran en metadatos y Git, no en cadenas como `final-final2`.

- Las carpetas de proceso usan el codigo NT con guiones y una denominacion corta: `s4-gestion-de-las-inversiones/`, `s4-3-ejecucion-inversion/`.
- Los documentos del proceso usan nombres fijos precedidos por el codigo: `s4-3-ficha-producto-proceso.md`, `s4-3-fichas-indicador.md`, `s4-3-sustento.md`, `s4-3-diagrama-proceso.bpmn`.
- Sufijos reservados: `-propuesta` para la unica variacion de un documento aprobado y `-to-be` para los documentos del arbol TO-BE.

Ejemplo: `s4-3-diagrama-proceso.bpmn`.

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
