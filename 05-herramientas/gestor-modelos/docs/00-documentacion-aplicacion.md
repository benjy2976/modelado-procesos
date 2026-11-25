---
tipo: mapa-de-contenido
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: NO-APLICA
tags:
  - tema/automatizacion
---

# Documentación de la aplicación de modelamiento

Esta carpeta describe la aplicación alojada en `05-herramientas/gestor-modelos/`. El [índice de la herramienta](../00-gestor-modelos.md) conserva las instrucciones del generador vigente y el [plan de la mesa](../plan-mesa-modelamiento.md) conserva las entregas y decisiones aún no implementadas.

| Pregunta | Fuente de la aplicación |
|---|---|
| ¿Qué componentes existen y dónde termina la aplicación? | [Arquitectura](arquitectura.md) |
| ¿Qué lee y monta cada contenedor? | [Entorno](entorno.md) |
| ¿Cómo se escribe y comenta el código? | [Convenciones](convenciones.md) |
| ¿Cómo se ejecutan los controles? | [Procedimientos](procedimientos.md) |
| ¿Qué rutas HTTP existen? | [API](api.md) |
| ¿Qué comandos existen? | [CLI](cli.md) |
| ¿Qué datos conserva hoy? | [Modelo de datos](modelo-datos.md) |
| ¿Cómo se organiza la pantalla Nuxt? | [Frontend](frontend.md) |
| ¿Qué puede hacer hoy un agente? | [MCP](mcp.md) |
| ¿Cómo se edita e integra una copia recuperable? | [Sesiones de edición](sesiones-edicion.md) |
| ¿Cómo se audita el sustento de S4.3 y se atiende cada observación? | [Metodología de auditoría y observaciones](metodologia-auditoria-y-observaciones.md) |
| ¿Qué pasos, herramientas y verificaciones requiere la corrida documental? | [Plan de corrida documental y auditoría](plan-corrida-documental-y-auditoria.md) |
| ¿Qué produjo la preparación de la biblioteca PDF? | [Informe de preparación PDF](informe-preparacion-biblioteca-pdf.md) |
| ¿Qué resultó del piloto de auditoría de S4.3.2.7? | [Informe del piloto S4.3.2.7](informe-piloto-auditoria-S4-3-2-7.md) |
| ¿Qué resultó de la auditoría de todo S4.3 (fase 5)? | [Informe consolidado de la fase 5](informe-auditoria-fase-5-S4-3.md) |
| ¿Cómo se traslada el trabajo local, PDF y caché OCR a otro equipo? | [Traslado entre equipos](traslado-entre-equipos.md) |
| ¿Qué falta para abrir la revisión por áreas usuarias? | [Ruta hacia la revisión por áreas usuarias](ruta-revision-areas-usuarias.md) |
| ¿Hacia dónde podría crecer la plataforma (gestión documental al estilo drive)? | [Planteamiento a futuro de gestión documental](vision-gestion-documental.md) |
| ¿Qué instrucciones de IA y skills están disponibles? | [Guía de IA](guia_IA.md) |
| ¿Qué estándar portable se adoptó? | [Memoria viva](memoria-viva/00-memoria-viva.md) y [plantilla de contexto](context-template.md) |

Las [instrucciones locales para agentes](../AGENTS.md) complementan las de la raíz institucional.

Otros puntos de entrada al mismo protocolo: [CLAUDE.md](../CLAUDE.md), [Copilot](../.github/copilot-instructions.md) y [prompts locales](../.github/prompts/base_universal.prompt.md), [código](../.github/prompts/codigo.prompt.md), [inicialización](../.github/prompts/inicializar_proyecto.prompt.md), [memoria](../.github/prompts/memoria.prompt.md), [módulo](../.github/prompts/modulo.prompt.md), [reporte](../.github/prompts/reporte.prompt.md) y [revisión](../.github/prompts/revision.prompt.md).

Las reglas de procesos y de conocimiento institucional siguen en `00-gobernanza/` y en el sustento de cada proceso. La documentación de esta aplicación describe su implementación y sus contratos; no duplica las normas de contratación ni convierte un modelo en aprobado.
