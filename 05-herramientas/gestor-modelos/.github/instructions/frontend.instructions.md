---
tipo: instruccion
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: NO-APLICA
tags:
  - tema/automatizacion
applyTo: "frontend/**/*.{vue,ts,css,mjs,json}"
---

# Capa Nuxt/Vue

La [memoria del frontend](../../docs/frontend.md) describe sus módulos y flujo. Consumir la API por el proxy local y generar los tipos desde `contracts/openapi.json`; no escribir otra versión manual del contrato. Las cajas BPMN emiten selección y el inspector ofrece la navegación al hijo.

Conservar límites visibles entre árbol, canvas e inspector, contraste legible y controles de teclado. Ejecutar ESLint, TypeScript y build antes de cerrar una pantalla. No declarar revisión visual si el navegador no estuvo disponible. Un cambio de endpoint exige actualizar [API](../../docs/api.md) y el snapshot OpenAPI.
