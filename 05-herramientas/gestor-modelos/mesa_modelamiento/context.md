---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
---

# Contexto: mesa de modelamiento

Sube a: [Guía de IA](../docs/guia_IA.md).

## Propósito

Permite consultar procesos, registrar observaciones y editar modelos lógicos en copia recuperable. Presenta las mismas operaciones por CLI, API y MCP sin crear otra fuente maestra de modelos.

## Alcance y límites

`fuentes_preparacion` y `fuentes_extraccion` preparan PDF de la biblioteca mediante la misma CLI. El manifiesto reanudable y el Markdown paginado son caché local ignorada por Git; se enlazan al SHA-256 del original. El diagnóstico usa un umbral explícito de texto por página y no acredita fidelidad. `fuentes_ocr` usa el MCP OCR local solo para copias derivadas de fuentes con URL pública HTTPS y hash coincidente; los demás PDF se señalan como pendientes. `fuentes_office` convierte DOCX y PPTX con `fuentes_docx`, `fuentes_numeracion` y `fuentes_ooxml`: el ancla de un DOCX es el párrafo del cuerpo y su numeral reconstruido, no una página; los XLSX solo se fichan. `fuentes_indice` genera el índice legible de la caché desde ambos manifiestos. El cotejo visual, la interpretación normativa y la validación institucional siguen siendo pasos distintos.

`RepositorioProcesos` localiza un proceso por código NT, lee la tabla y entrega el BPMN disponible. `ServicioObservaciones` mantiene un archivo JSON por proceso con revisión esperada y escritura atómica. `ServicioSesiones` conserva el árbol de trabajo en una instantánea y permite una copia editable por proceso. La autorización multiusuario y el bloqueo distribuido de un editor único siguen pendientes.

## Vocabulario y estados

Una **observación** puede asociarse a un elemento BPMN o al diagrama. Sus estados actuales son `ABIERTA` y `RESUELTA`. La **revisión** es el hash del documento JSON y se compara antes de escribir; `409` indica conflicto de revisión en HTTP. No representa aprobación técnica o institucional del proceso.

Una **respuesta** permanece dentro de la observación con autor declarado y fecha. El historial conserva creación, respuestas y cambios de estado; responder o resolver no modifica el BPMN ni valida el fundamento.

## Actores

El servicio local no autentica personas. El campo `autor` es un dato declarado por el cliente, no una identidad verificada. El origen de las mutaciones se comprueba en el adaptador HTTP; por ello el despliegue actual debe permanecer local. El plan separa comentarios de varios usuarios y edición única posterior.

## Reglas

Un código NT válido es la única llave para localizar procesos. La revisión esperada evita sobreescrituras silenciosas de observaciones; el reemplazo atómico protege cada archivo local. El registro de una observación no cambia el estado institucional del modelo.

Los registros antiguos sin respuestas o historial se leen sin migración destructiva; las nuevas colecciones se agregan cuando se responde o cambia el estado. Un cambio al mismo estado es idempotente.

## Flujo

CLI, API y MCP llaman a los mismos servicios. Una lectura resuelve código NT, carpeta y artefacto; una escritura de observación verifica revisión, bloquea el archivo, actualiza el JSON y devuelve la nueva revisión. La generación BPMN continúa a cargo de `modelar.py` y los scripts vigentes.

`ServicioDocumentos` ofrece solo tabla, sustento y fuentes ya registradas para la caja consultada. El visor no convierte un pasaje en conocimiento validado: la fuente, página, fecha y vigencia permanecen en los metadatos del proceso y en su sustento.

Los anclajes PDF opcionales incluyen hash y rectángulos normalizados de la página, cotejados al enlazar la fuente. `datos_visor` entrega las coordenadas solo si el archivo conserva el mismo hash; `HASH_DISTINTO` obliga a revisar el enlace. La búsqueda textual puede apoyar la auditoría, pero el visor no la ejecuta al abrir el PDF.

La sesión captura bytes del árbol de trabajo, incluso sin commit. `editar` requiere el hash de la copia; `preparar` regenera derivados y entrega diff y hallazgos; `integrar` exige la revisión preparada y los hashes originales de todos los destinos. Si alguno cambió, no escribe. `cerrar` conserva la instantánea. Los documentos `APROBADO` y originales no son editables. Las acciones están descritas en [sesiones de edición](../docs/sesiones-edicion.md).

## Evidencia y contratos

La semántica anterior se apoya en `repositorio.py`, `observaciones.py` y `api.py`. El transporte y sus rutas están en [API](../docs/api.md), la persistencia en [modelo de datos](../docs/modelo-datos.md), los comandos en [CLI](../docs/cli.md), y el alcance evolutivo en [el plan](../plan-mesa-modelamiento.md). Revisar este contexto cuando cambien estados, reglas de concurrencia, actores o capacidad de edición.
