---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: DECISION
tags:
  - tema/automatizacion
---

# Convenciones de código y comentarios

El código nuevo del paquete Python se organiza por capacidad real y mantiene delgados los adaptadores CLI, API y MCP. Una regla de proceso o una decisión institucional se documenta en el sustento o en `00-gobernanza/`; el comentario de código explica únicamente un motivo técnico que no resulta evidente.

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

- Preferir nombres que expresen responsabilidad, tipos explícitos y funciones acotadas. No crear capas, interfaces ni carpetas vacías para capacidades futuras.
- Comentar el **porqué** de un límite, una excepción o una decisión (`DEC-...`); evitar repetir lo que ya dice la instrucción y no conservar código comentado.
- Usar docstrings breves para módulos y operaciones públicas. Los pendientes remiten a una entrega o decisión del [plan](../plan-mesa-modelamiento.md).
- Formatear el paquete nuevo con Ruff; su configuración vigente está en `pyproject.toml` (Python 3.11, longitud 120; reglas E, F, I y B). Mantener pruebas cerca de cada cambio funcional.
- No aplicar todavía al generador heredado los límites adicionales de complejidad y tamaño del proyecto de referencia: sus archivos actuales superan esas medidas. Se evaluarán al extraer cada caso de uso, sin un reformateo masivo.
- Para capacidades nuevas, usar como objetivo los límites del ejemplo: archivo recomendado de hasta 250 líneas, función de hasta 60 líneas y complejidad ciclomática máxima de 12. La comprobación exploratoria del paquete actual con las reglas ampliadas encuentra cinco hallazgos: dos fechas `datetime.UTC`, un exceso de argumentos y complejidad y tamaño de `datos_visor`. Por ello esas reglas todavía no son un control obligatorio que pase; E1 debe refactorizar esos puntos antes de activarlas.
- Cuando exista `frontend/`, adoptar ESLint con TypeScript y Vue, formato único en el IDE, comprobación de tipos y pruebas. Su configuración se ajustará al código Nuxt real y excluirá contratos generados; hoy no existe un `eslint.config.mjs` ejecutable en esta aplicación.

Estas pautas se adaptan de `modelador-bim-main/docs/conventions.md` y `normatividad-main/docs/convenciones.md`, consultados localmente el 2026-11-20. El estándar portable completo de `gestionar-memoria-viva-proyecto` 1.9.0 se adoptó posteriormente y está registrado en [la guía de IA](guia_IA.md).

## Diseño HTTP orientado a recursos

`/api/procesos/{codigo}` representa el proceso institucional identificado por código NT. El árbol es una proyección de esa colección; el BPMN es un documento derivado. Las observaciones son recursos propios del proceso y su colección JSON local es la autoridad de escritura. Las rutas no ofrecen una segunda autoridad para editar tablas ni BPMN. El inventario, las omisiones CRUD y las decisiones de cada ruta están en [API](api.md); los estados de observación pertenecen al [contexto funcional](../mesa_modelamiento/context.md).
