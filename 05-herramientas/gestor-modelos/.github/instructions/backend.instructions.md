---
tipo: instruccion
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: NO-APLICA
tags:
  - tema/automatizacion
applyTo: "mesa_modelamiento/**/*.py,tests/**/*.py,*.py"
---

# Capa Python

La API, CLI y MCP son adaptadores. Colocar las reglas compartidas en `mesa_modelamiento` y documentar su semántica en [el contexto del módulo](../../mesa_modelamiento/context.md). Mantener acceso a archivos del repositorio detrás de `RepositorioProcesos`; validar código NT antes de resolver rutas y conservar revisiones esperadas en escrituras.

Usar tipos, Ruff y pruebas enfocadas según [procedimientos](../../docs/procedimientos.md). Si cambia una ruta HTTP, sincronizar [API](../../docs/api.md); si cambia un comando, sincronizar [CLI](../../docs/cli.md); si cambia el JSON persistido, sincronizar [modelo de datos](../../docs/modelo-datos.md).
