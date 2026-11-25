---
tipo: propuesta
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
proceso: []
fecha_creacion: 2026-11-25
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/conocimiento
---

# Planteamiento a futuro: gestión documental con conocimiento estructurado

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

Planteamiento del usuario del 2026-11-25. Es una dirección de crecimiento de la plataforma, **no un alcance aprobado ni una tarea en curso**. Primero se hará funcionar el MCP como canal único (`DEC-066`); la reestructuración se pensará después.

## Situación actual

1. El conocimiento se obtiene de archivos PDF y de documentos de Office conservados en `01-referencias`.
2. Las herramientas de preparación documental y el MCP los convierten en Markdown paginado, fragmentos por artículo e índice de búsqueda.
3. Desde ese Markdown se construye lo demás: guías de lectura, reglas, auditorías, sustentos y modelos, consultables por el MCP.

## Planteamiento

- **Módulo de administración de archivos, al estilo de un drive.** El usuario podrá cargar documentos, administrar el inventario de descargas y consultar los documentos, con conocimiento estructurado asociado a cada uno.
- **El agente como organizador.** El agente podrá proponer la estructura de carpetas, mover documentos y reorganizar el inventario, por los mismos canales gobernados del MCP.
- **Lectura fácil como regla.** Todo documento incorporado se convertirá a Markdown con las herramientas de la plataforma. Desde ese punto rige el flujo actual: fragmentos, índice, guías, reglas, auditoría y modelos.

## Condiciones que conviene conservar cuando se diseñe

- Los originales se preservan sin modificar, con hash, procedencia y fecha de consulta. El Markdown es un derivado regenerable.
- Mover o renombrar un documento no debe romper sus anclas, citas ni referencias de catálogo. El identificador estable del catálogo es la llave, no la ruta.
- Las propuestas del agente sobre la estructura se aplican como cambios revisables, con la misma lógica de propuesta, definición por una persona y aplicación que las observaciones (`DEC-065`).

## Relaciones

- [MCP: canales de conocimiento](mcp.md#canales-de-conocimiento-dec-066-2026-11-25)
- [Informe de preparación de la biblioteca PDF](informe-preparacion-biblioteca-pdf.md)
- [Metodología de auditoría y observaciones](metodologia-auditoria-y-observaciones.md)
