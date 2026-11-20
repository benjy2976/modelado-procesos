---
tipo: instruccion
area: herramientas
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
tags:
  - tema/automatizacion
---

# Instrucciones de la aplicación de modelamiento

Estas instrucciones complementan el `AGENTS.md` de la raíz del repositorio. La raíz de esta aplicación es `05-herramientas/gestor-modelos/`; los procesos, referencias y notas de gobierno situados fuera son datos o reglas del repositorio institucional, no código interno de la aplicación.

Antes de modificar la aplicación, leer [el índice técnico](docs/00-documentacion-aplicacion.md), el [plan](plan-mesa-modelamiento.md) y el documento que gobierne la capacidad afectada. Conservar la tabla, el sustento y el BPMN según la etapa declarada en el estándar institucional; no atribuir aprobación o validación humana.

- CLI, API y MCP llaman a los mismos servicios del paquete `mesa_modelamiento`; no duplicar reglas en los adaptadores.
- Cada escritura conserva revisión esperada y resultado recuperable. No aceptar rutas arbitrarias ni escribir en `01-referencias/**/originales`.
- Para código Python nuevo o migrado, aplicar las [convenciones](docs/convenciones.md), Ruff y las pruebas cercanas. Los scripts heredados se migran por caso de uso, sin reformateos masivos.
- La interfaz Nuxt en `frontend/` aplica [su instrucción de capa](.github/instructions/frontend.instructions.md), ESLint y tipos generados desde OpenAPI. Ejecutar sus controles al cambiar la pantalla.
- El índice de documentación distingue capacidades implementadas de decisiones previstas. Actualizar el contrato correspondiente al cambiar rutas, comandos, datos o contenedores.
- La aplicación adoptó el estándar portable de `gestionar-memoria-viva-proyecto` 1.9.0. Su registro e índice están en [docs/guia_IA.md](docs/guia_IA.md); las referencias y el validador locales permiten aplicarlo sin acceso al paquete externo.
- Al modificar código, contratos o contenedores, sincronizar la memoria afectada en la misma ventana de trabajo. Consultar el `context.md` del módulo funcional y la instrucción de la capa correspondiente.
- En este equipo, la configuración y prueba del MCP OCR se documentan localmente en `.mesa-local/00-configuracion-local.md` cuando exista. Esa carpeta y las credenciales no se versionan.
- En un checkpoint global ejecutar `scripts/validate-project-memory` directamente desde la raíz de esta aplicación, revisar cobertura y hallazgos, y ejecutar Markdownlint. Registrar `NOT_EVALUATED` como límite, no como conformidad.
