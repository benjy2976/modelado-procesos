---
tipo: instruccion
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: NO-APLICA
tags:
  - tema/automatizacion
applyTo: "compose.yaml,Dockerfile*,*.dockerfile"
---

# Contenedores de la aplicación

El [entorno](../../docs/entorno.md) documenta servicios, puertos, variables y montajes. `compose.yaml` monta el repositorio institucional como datos; no trasladar fuentes ni originales al código de la aplicación. Mantener el puerto de desarrollo ligado a `127.0.0.1` y no ampliar acceso de escritura sin documentar el contrato operativo.

Verificar `docker compose config` al cambiar la composición. Registrar en [arquitectura](../../docs/arquitectura.md) cualquier servicio nuevo o cambio de frontera.
