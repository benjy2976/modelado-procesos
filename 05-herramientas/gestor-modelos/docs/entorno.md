---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
---

# Entorno y contenedores

La aplicación se instala desde su propia carpeta. Los datos institucionales permanecen por ahora en el repositorio padre y se suministran al contenedor mediante un montaje explícito.

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

## Requisitos

Para desarrollo local: Python compatible con `pyproject.toml`, `uv` y el repositorio institucional accesible. Para contenedores: Docker Compose. El validador de memoria viva requiere además shell POSIX y Python 3.10 o posterior.

## Servicios

Compose define `api`, `frontend` y un servicio `mcp` optativo bajo perfil. API y frontend se publican solo en la interfaz de bucle local. El frontend usa un proxy Nitro interno para `/api`; su destino dentro de Compose es `http://api:8000`.

## Montaje actual

`compose.yaml` define `api`, `frontend` y un perfil opcional `mcp`. Los servicios Python usan la misma imagen y montan `${PROCESOS_REPO_HOST:-../..}` en `/workspace`; como Compose resuelve la ruta desde la carpeta del proyecto, el valor predeterminado apunta a la raíz de este repositorio. El directorio de trabajo Python es `/workspace/05-herramientas/gestor-modelos`. `PROCESOS_REPO_ROOT=/workspace` indica dónde leer `02-procesos`, `01-referencias` y las notas de gobierno. La API publica `127.0.0.1:${MODELOS_API_PORT:-8766}`; Nuxt publica `127.0.0.1:${MODELOS_UI_PORT:-8767}` y monta `node_modules` en volumen propio para no reutilizar binarios de Windows dentro de Linux.

## Variables

| Variable | Función | Valor actual en Compose |
|---|---|---|
| `PROCESOS_REPO_HOST` | Ruta del repositorio institucional en el anfitrión | `../..` |
| `PROCESOS_REPO_ROOT` | Raíz visible para el paquete Python | `/workspace` |
| `MODELOS_API_PORT` | Puerto local publicado | `8766` |
| `MODELOS_UI_PORT` | Puerto local del frontend | `8767` |
| `NUXT_API_TARGET` | Destino privado del proxy Nuxt | `http://api:8000` en Compose; `http://127.0.0.1:8766` en desarrollo sin contenedor |
| `UV_PROJECT_ENVIRONMENT` | Entorno Python interno | `/tmp/mesa-venv` |
| `UV_CACHE_DIR` | Caché de dependencias | `/tmp/uv-cache` |

El montaje completo es una integración **local y transitoria**: el mismo volumen contiene código y datos, y el servicio puede escribir las observaciones autorizadas. Cuando se independicen repositorios, se configurarán montajes diferenciados de código, procesos, referencias y gobierno, con permisos de solo lectura donde corresponda. Ese cambio requiere adaptar primero las rutas del generador y probar lectura y escritura; no se simula con enlaces simbólicos dependientes de Windows.

El proxy Nitro solo simplifica el consumo local desde el navegador. El acceso compartido, la autenticación y un proxy institucional no están implementados. No publicar este servicio como si ofreciera control multiusuario.
