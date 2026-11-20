---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
---

# Arquitectura de la aplicación

La aplicación reside en `05-herramientas/gestor-modelos/`. Su paquete instalable `mesa_modelamiento` ofrece consultas y acciones compartidas a la CLI, FastAPI y MCP. El generador BPMN heredado sigue en esta misma carpeta mientras se migra por capacidades.

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

## Stack

Python 3.11 o posterior, FastAPI y Pydantic para HTTP, `argparse` para CLI, MCP para herramientas de agente, Nuxt 4/Vue/TypeScript y `bpmn-js` para la pantalla de revisión, y Docker Compose para el entorno local.

## Componentes

El paquete `mesa_modelamiento` contiene servicios y adaptadores. `frontend/` contiene la interfaz y un proxy Nitro local hacia la API. El generador BPMN vigente sigue como scripts vecinos. Las carpetas institucionales son repositorios de datos y autoridad documental, no módulos de aplicación.

## Frontera actual

| Ubicación | Función | Autoridad |
|---|---|---|
| `mesa_modelamiento/` | Acceso a procesos, observaciones y adaptadores | Código de aplicación |
| `construir_modelos.py` y herramientas vecinas | Generación y controles D1-D5 | Código del generador vigente |
| `compose.yaml`, `pyproject.toml`, `uv.lock` | Servicios y entorno reproducible | Configuración de aplicación |
| `02-procesos/` | Tablas, sustento, BPMN y observaciones | Repositorio de procesos |
| `01-referencias/` | Fuentes y catálogos documentales | Repositorio de evidencias; originales inmutables |
| `00-gobernanza/` | Reglas y decisiones institucionales | Repositorio de conocimiento |

El código resuelve la raíz de datos mediante `PROCESOS_REPO_ROOT`; no presupone que `02-procesos` esté dentro del paquete. La CLI `modelo` delega todavía en `modelar.py`. Los HTML actuales son vistas derivadas. El contrato OpenAPI se genera desde FastAPI y se guarda en `contracts/openapi.json`; el frontend genera de allí sus tipos TypeScript.

## Flujo global

1. `RepositorioProcesos` localiza un código NT y lee la tabla o el BPMN correspondiente.
2. API, CLI y MCP presentan esas consultas sin crear una segunda fuente maestra. Nuxt consume la API mediante un proxy local y muestra el BPMN; el clic en una caja solo selecciona. Las rutas documentales resuelven tabla, sustento y fuentes registradas sin aceptar rutas arbitrarias.
3. `ServicioObservaciones` registra comentarios en JSON del proceso, con revisión esperada, bloqueo local y reemplazo atómico.
4. El generador conserva su propio ciclo tabla → BPMN → HTML; SVG y PNG se exportan cuando se solicitan.

La copia aislada para edición y el editor único multiusuario están **planificados**, no implementados. Sus límites se describen en el [plan](../plan-mesa-modelamiento.md).
