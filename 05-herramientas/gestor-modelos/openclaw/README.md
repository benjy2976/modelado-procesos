---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: NO-APLICA
proceso: []
fecha_creacion: 2026-11-25
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/ia
---

# Agentes de OpenClaw de la mesa de modelamiento

Sube a: [Documentación de la aplicación](../docs/00-documentacion-aplicacion.md).

Configuración versionada de los tres agentes fijos de `DEC-068`. La instalación en OpenClaw la hace el operador
con los scripts de `ia-familiar/tmp/openclaw-diag/` (217 y 218), que usan los archivos generados desde esta carpeta.

| Archivo | Uso |
|---|---|
| `agentes.json` | Por agente: nombre, modelo y lista exacta de herramientas MCP (`mesa-modelamiento__<herramienta>`) |
| `comun.md` | Reglas comunes; se agrega como sección tras las instrucciones de cada agente |
| `mesa-analisis.AGENTS.md` | Análisis y propuesta con el método `DEC-067` |
| `mesa-aplicacion.AGENTS.md` | Aplicación por lote de lo definido, con sesión, controles y evidencia |
| `mesa-chat.AGENTS.md` | Asistente conversacional: prepara cambios, nunca los integra |
| `preparar_instalacion.py` | Genera el parche de configuración, `agentes.tsv` y los `AGENTS.md` combinados para el script 217 |

## Flujos

| Flujo | Disparo | Agente y modelo propuesto | Resultado |
|---|---|---|---|
| Análisis | Botón «Solicitar análisis a Claudia» (o reanálisis con motivo) encola `ANALISIS` y despierta al agente por el relevo | `mesa-analisis`, GPT-6.2 Sol | Análisis y propuesta registrados en la observación (etapa PROPUESTA) |
| Aplicación | Definir una resolución encola `APLICACION`; la automatización de OpenClaw despierta al agente cada 10 min | `mesa-aplicacion`, GPT-6.1 Terra | Cambios aplicados por lote de proceso en una sesión de edición, aplicación registrada y trabajo cerrado |
| Chat | Pestaña «Asistente» del espacio de trabajo | `mesa-chat`, GPT-6.1 Terra | Respuesta en streaming; las variaciones quedan preparadas en una copia que la persona revisa y aplica |

Los modelos se confirman con la prueba sobre las cuestiones de S4.3.2.6 (comparación con una revisión directa).

## Componentes y puertos

| Componente | Dirección | Credencial |
|---|---|---|
| MCP por HTTP (`mcp-http`) | `127.0.0.1:8768/mcp`, cabecera Host restringida | Ninguna; solo loopback |
| Relevo (`relevo`, perfil `openclaw`) | `192.168.80.1:8769` (puente de la red del compose) | `MESA_RELEVO_TOKEN`; es el único con `OPENCLAW_GATEWAY_TOKEN` (`~/.config/mesa-relevo/relevo.env`) |
| API | Llama al relevo con `MESA_RELEVO_URL` y `MESA_RELEVO_TOKEN` (`~/.config/mesa-relevo/api.env`) | Nunca ve el token del Gateway |
| Cola de trabajos | `.mesa-trabajos/cola.json`, fuera de Git | Estado operativo; la trazabilidad durable queda en la observación |

## Operación

1. Con el stack levantado, generar los archivos del 217:
   `python3 openclaw/preparar_instalacion.py ~/ia-familiar/tmp/openclaw-diag/217-registrar-mcp-y-agentes-mesa`.
2. El operador ejecuta el 217 (MCP y agentes; reinicia el Gateway) y luego el 218 (entorno del relevo, compose y
   automatización).
3. Un cambio de estos archivos no llega solo a OpenClaw: se regenera y se vuelve a ejecutar el 217. Si los agentes
   ya existen, solo se actualizan el parche y los `AGENTS.md`.

## Credenciales y herramientas

Lecciones de la puesta en marcha del 2026-11-25:

- **Solo suscripción.** OpenClaw usa únicamente el perfil OAuth de la suscripción de ChatGPT
  (`auth.order.openai`). La clave de API se retiró de la instalación.
- **Orden de credenciales por agente.** Un agente creado con `openclaw agents add` puede traer un orden propio
  (`models auth order`) que prevalece sobre el global; los agentes `mesa-*` lo trajeron con solo la clave de API y
  fallaban con «billing issue». Tras crear o recrear un agente se revisa con
  `openclaw models auth order get --provider openai --agent <id>` y se limpia con `order clear`. Ambos comandos
  requieren el Gateway detenido.
- **Perfil de herramientas.** El perfil `minimal` no carga `bundle-mcp` y deja al agente sin herramientas MCP
  («No callable tools remain after resolving explicit tool allowlist»). Se usa `messaging`, que sí lo carga, con la
  lista explícita de herramientas MCP y la negación de las nativas (`browser`, `edit`, `exec`, `read`, `write` y
  otras), como el agente `cse-bim` de la misma instalación. `preparar_instalacion.py` ya genera esa forma.
- **Modelos.** El catálogo permitido de la instalación aún no incluye `gpt-6.1-terra` ni `gpt-6.2-sol`
  («Unknown model» al fijarlos). `mesa-chat` funciona temporalmente con `gpt-6-luna`; queda pendiente actualizar el
  catálogo (`openclaw doctor`) y retirar los modelos GPT-5 antes de la prueba con S4.3.2.6.
