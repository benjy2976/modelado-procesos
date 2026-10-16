# Instrucciones para agentes

## Antes de trabajar

1. Leer `estado-del-proyecto.md` y la nota indice `00-<nombre>.md` del area afectada.
2. Revisar `git status` y preservar cualquier cambio existente.
3. Consultar solo las fuentes necesarias para la tarea.

## Reglas obligatorias

- Cumplir `00-gobernanza/estandar-obligatorio-obsidian.md` al crear o modificar notas de conocimiento.
- Enlazar todo Markdown nuevo desde el mapa de contenido de su area; no dejar notas huerfanas.
- Seguir `00-gobernanza/convenciones-nombres.md` (mayusculas en tres niveles) y el vocabulario de etiquetas `00-gobernanza/vocabulario-etiquetas.yaml`; ejecutar `05-herramientas/gestionar_etiquetas.py revisar` antes de proponer un commit.
- Tratar Canvas y Bases como vistas: ninguna regla, decision o conclusion durable puede existir solo en ellos.
- No modificar originales ubicados en `01-referencias/**/originales`.
- No sobrescribir informacion publicada o aprobada. Un documento con `estado_institucional: APROBADO` no se edita; una variacion se plantea en un unico archivo `<codigo>-<documento>-propuesta.md`.
- Organizar cada proceso en su carpeta por codigo NT dentro de `02-procesos`, con el juego de documentos de `00-gobernanza/estandar-artefactos-modelamiento.md`. Las fichas siguen exactamente los campos de los anexos de la NT 002-2025-PCM-SGP; fuentes, evidencias y discrepancias van en el sustento del proceso.
- Mantener separados el arbol principal de procesos y el arbol TO-BE (`02-procesos/to-be/`); el analisis de brechas acompana al TO-BE.
- No registrar, presumir ni atribuir conformidades de los niveles de revision (`REVISION-EQUIPO`, `OPINION-TECNICA`, `APROBACION`) ni asignar el estado `APROBADO`.
- No inventar actividades, responsables, plazos, articulos ni requisitos BIM.
- Toda afirmacion normativa debe registrar fuente oficial, fecha de consulta, vigencia y ubicacion precisa.
- La IA solo puede proponer conocimiento normativo. Nunca debe marcar una regla como `VALIDADO` ni atribuir una validacion a una persona.
- Para usar una regla como sustento normativo de una linea base debe cumplir `00-gobernanza/protocolo-conocimiento-confiable.md`.
- Distinguir expresamente evidencia observada, exigencia normativa, inferencia y propuesta.
- Si las fuentes autorizadas son insuficientes, registrar `EVIDENCIA-INSUFICIENTE` en vez de completar el vacio.
- BPMN 2.0 XML es la fuente maestra de los modelos formales; SVG y PDF son derivados. Se exceptua unicamente el mapa institucional de procesos Nivel 0, que es una representacion conceptual lineal de macroprocesos y puede mantenerse en Markdown/Mermaid sin BPMN ni carriles.
- Usar nombres estables. El historial se conserva con Git, no agregando `final`, `final2` o fechas al nombre de cada borrador.
- No duplicar ni mover archivos entre carpetas de estado. El trabajo vigente permanece en su ruta estable y las lineas base se gestionan segun `00-gobernanza/protocolo-versionado-y-releases.md`.
- Para PDF, medir primero si posee texto; aplicar OCR solo a una copia derivada.
- Registrar decisiones que cambien alcance, limites, codigos o convenciones.
- No incluir datos personales, credenciales o expedientes sensibles en prompts o servicios externos.

## Eficiencia de contexto

Para una tarea de modelamiento usar un paquete basado en `00-gobernanza/plantillas/conocimiento/paquete-contexto.yaml`: ficha del proceso, modelo vigente, reglas aplicables, glosario relevante, evidencias seleccionadas y estado actual. No cargar la biblioteca completa.
