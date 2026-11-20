---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/ia
  - tema/automatizacion
---

# Guía de IA de la aplicación

El agente que trabaje en esta aplicación sigue primero el `AGENTS.md` de la raíz institucional y después las [instrucciones locales](../AGENTS.md). Las fuentes técnicas se distribuyen por contrato en el [índice documental](00-documentacion-aplicacion.md); el plan registra capacidades futuras sin presentarlas como implementadas.

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

Se adoptó el estándar portable de la skill `gestionar-memoria-viva-proyecto` **1.9.0** el **2026-11-20**, a partir del paquete local proporcionado por el usuario en `C:\Users\72121555.REGIONHUANUCO\Downloads\gestionar-memoria-viva-proyecto`. La versión anterior de esta aplicación era una adaptación parcial sin skill. Esta línea registra la versión adoptada; la fuente normativa de la versión de la skill permanece en su `SKILL.md`.

## Adopción del estándar

- Skill: `gestionar-memoria-viva-proyecto`.
- Versión adoptada: `1.9.0`
- Fecha de revisión: 2026-11-20.
- Versión anterior: no aplica; había una adaptación parcial sin versión declarada.

El estándar vive en esta aplicación mediante las [referencias locales](memoria-viva/00-memoria-viva.md), las [instrucciones de agentes](../AGENTS.md), los prompts y el [validador portable](../scripts/validate-project-memory). La guía institucional de Obsidian, el sustento de cada proceso y los controles D1-D5 siguen siendo autoridades distintas y prevalecen en sus materias.

## Contextos de módulos

| Módulo | Responsabilidad |
| --- | --- |
| [Mesa de modelamiento](../mesa_modelamiento/context.md) | Consulta de procesos y observaciones locales compartidas por CLI, API y MCP |

## Instrucciones por capa

| Capa | Instrucción |
| --- | --- |
| Python | [Backend](../.github/instructions/backend.instructions.md) |
| Contenedores | [Infraestructura](../.github/instructions/infra.instructions.md) |
| Nuxt/Vue | [Frontend](../.github/instructions/frontend.instructions.md) |

El [frontend](frontend.md) es una capa real desde E2. La herramienta no atribuye conformidad institucional al ejecutar controles automáticos.
