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
| `mesa-aplicacion.AGENTS.md` | Aplicación de lo definido, una observación por sesión (`DEC-069`), con controles y evidencia |
| `mesa-chat.AGENTS.md` | Asistente conversacional: prepara cambios, nunca los integra |
| `preparar_instalacion.py` | Genera el parche de configuración, `agentes.tsv` y los `AGENTS.md` combinados para el script 217 |

## Flujos

| Flujo | Disparo | Agente y modelo propuesto | Resultado |
|---|---|---|---|
| Análisis | Botón «Solicitar análisis a Claudia» (o reanálisis con motivo) encola `ANALISIS` y despierta al agente por el relevo | `mesa-analisis`, GPT-6.2 Sol | Análisis y propuesta registrados en la observación (etapa PROPUESTA) |
| Aplicación | Definir una resolución encola `APLICACION`; la automatización de OpenClaw despierta al agente cada 10 min | `mesa-aplicacion`, GPT-6.1 Terra | Cada observación se aplica en su propia sesión de edición con bloqueo (`DEC-069`); al integrar queda una versión ligada a la observación, la aplicación registrada y el trabajo cerrado |
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
- **Modelos.** OpenClaw 2026.11.6 no admitía asignar `gpt-6.1-terra` ni `gpt-6.2-*` («Unknown model»); desde
  2026.11.10 sí. Se restableció el plan: `gpt-6.2-sol` para análisis y `gpt-6.1-terra` para aplicación y chat.
- **Code Mode desactivado.** Con Code Mode el agente recibe una herramienta `exec` de JavaScript que corre en el
  proceso del Gateway, sin frontera de seguridad. Como los agentes reciben texto de la web pública, cada modelo de
  agente declara `codeMode: false` (lo genera `preparar_instalacion.py`). Se comprueba pidiendo al agente la lista de
  sus herramientas: no debe aparecer `exec`.
- **Entradas de modelos sobrantes.** `openclaw doctor` puede agregar entradas heredadas (`gpt-5.6-*`) a cada
  agente. Cada agente `mesa-*` debe declarar solo su modelo; las demás se retiran con
  `openclaw config unset 'agents.entries.<id>.models["openai/<modelo>"]'`, probando antes con `--dry-run`.
- **Actualizar OpenClaw.** `openclaw update` reinstala el servicio del Gateway y exige resolver
  `OPENCLAW_GATEWAY_TOKEN`; en esta instalación el servicio lo recibe por `EnvironmentFile` en un archivo
  complementario de systemd, y la reinstalación falla y deja el Gateway detenido. Tras actualizar se comprueba
  `systemctl --user is-active openclaw-gateway.service` y, si está detenido, se arranca. Antes de actualizar:
  `openclaw backup create --verify` y `openclaw update --dry-run`.
