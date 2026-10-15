# Instrucciones para agentes

## Antes de trabajar

1. Leer `estado-del-proyecto.md` y el README del area afectada.
2. Revisar `git status` y preservar cualquier cambio existente.
3. Consultar solo las fuentes necesarias para la tarea.

## Reglas obligatorias

- Cumplir `00-gobernanza/estandar-obligatorio-obsidian.md` al crear o modificar notas de conocimiento.
- Enlazar todo Markdown nuevo desde el mapa de contenido de su area; no dejar notas huerfanas.
- Tratar Canvas y Bases como vistas: ninguna regla, decision o conclusion durable puede existir solo en ellos.
- No modificar originales ubicados en `01-referencias/**/originales`.
- No sobrescribir informacion publicada o aprobada.
- Mantener separados AS-IS, analisis y TO-BE.
- No inventar actividades, responsables, plazos, articulos ni requisitos BIM.
- Toda afirmacion normativa debe registrar fuente oficial, fecha de consulta, vigencia y ubicacion precisa.
- La IA solo puede proponer conocimiento normativo. Nunca debe marcar una regla como `VALIDADO` ni atribuir una validacion a una persona.
- Para usar una regla como sustento normativo de una linea base debe cumplir `00-gobernanza/protocolo-conocimiento-confiable.md`.
- Distinguir expresamente evidencia observada, exigencia normativa, inferencia y propuesta.
- Si las fuentes autorizadas son insuficientes, registrar `EVIDENCIA-INSUFICIENTE` en vez de completar el vacio.
- BPMN 2.0 XML es la fuente maestra de los diagramas; SVG y PDF son derivados.
- Usar nombres estables. El historial se conserva con Git, no agregando `final`, `final2` o fechas al nombre de cada borrador.
- No duplicar ni mover archivos entre carpetas de estado. El trabajo vigente permanece en su ruta estable y las lineas base se gestionan segun `00-gobernanza/protocolo-versionado-y-releases.md`.
- Para PDF, medir primero si posee texto; aplicar OCR solo a una copia derivada.
- Registrar decisiones que cambien alcance, limites, codigos o convenciones.
- No incluir datos personales, credenciales o expedientes sensibles en prompts o servicios externos.

## Eficiencia de contexto

Para una tarea de modelamiento usar un paquete basado en `04-recursos-reutilizables/plantillas/paquete-contexto.yaml`: ficha del proceso, modelo vigente, reglas aplicables, glosario relevante, evidencias seleccionadas y estado actual. No cargar la biblioteca completa.
