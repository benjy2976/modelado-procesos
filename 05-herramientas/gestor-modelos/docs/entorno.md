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

Compose define `api`, `frontend` y un servicio `mcp` optativo bajo perfil. La API se publica solo en la interfaz de bucle local. El frontend se publica en `127.0.0.1` por defecto o en la interfaz que indique `MODELOS_UI_BIND`. Usa un proxy Nitro interno para `/api`, cuyo destino dentro de Compose es `http://api:8000`; por eso no hace falta exponer la API para usar la interfaz. En Compose, el frontend se compila para producción (`npm run build`, que ejecuta antes lint y typecheck) y se sirve con el servidor Nitro (`node .output/server/index.mjs`); el servidor de desarrollo de Nuxt queda para el trabajo local sin contenedor.

Para los agentes de OpenClaw (`DEC-068`) Compose agrega `mcp-http`, que sirve el MCP por HTTP en `127.0.0.1:${MODELOS_MCP_PORT:-8768}` con el usuario local, y `relevo` bajo el perfil `openclaw`. El relevo usa la red del anfitrión para llegar al Gateway en `127.0.0.1:18789` y escucha solo en la puerta de enlace de la red del compose (`MESA_RELEVO_IP`, por defecto `192.168.80.1`, puerto `8769`). Por eso la red `default` tiene subred fija `192.168.80.0/20`. Sus credenciales viven fuera del repositorio, en `~/.config/mesa-relevo/` con modo `600`: `relevo.env` (`MESA_RELEVO_TOKEN`, `OPENCLAW_GATEWAY_TOKEN`, `OPENCLAW_GATEWAY_URL`) y `api.env` (`MESA_RELEVO_URL`, `MESA_RELEVO_TOKEN`), que la API carga si existe. Los crea el script 218 de ia-familiar; sin `api.env` el chat y el despertar quedan inactivos. Se levanta con `docker compose --profile openclaw up -d relevo`.

## Montaje actual

`compose.yaml` define `api`, `frontend` y un perfil opcional `mcp`. Los servicios Python usan la misma imagen y montan `${PROCESOS_REPO_HOST:-../..}` en `/workspace`; como Compose resuelve la ruta desde la carpeta del proyecto, el valor predeterminado apunta a la raíz de este repositorio. El directorio de trabajo Python es `/workspace/05-herramientas/gestor-modelos`. `PROCESOS_REPO_ROOT=/workspace` indica dónde leer `02-procesos`, `01-referencias` y las notas de gobierno. La API publica `127.0.0.1:${MODELOS_API_PORT:-8766}`; Nuxt publica `${MODELOS_UI_BIND:-127.0.0.1}:${MODELOS_UI_PORT:-8767}` y monta `node_modules` en volumen propio para no reutilizar binarios de Windows dentro de Linux.

## Variables

| Variable | Función | Valor actual en Compose |
|---|---|---|
| `PROCESOS_REPO_HOST` | Ruta del repositorio institucional en el anfitrión | `../..` |
| `PROCESOS_REPO_ROOT` | Raíz visible para el paquete Python | `/workspace` |
| `MODELOS_API_PORT` | Puerto local publicado | `8766` |
| `MODELOS_UI_PORT` | Puerto local del frontend | `8767` |
| `MODELOS_UI_BIND` | Interfaz del anfitrión donde se publica el frontend | `127.0.0.1` |
| `NUXT_API_TARGET` | Destino privado del proxy Nuxt | `http://api:8000` en Compose; `http://127.0.0.1:8766` en desarrollo sin contenedor |
| `UV_PROJECT_ENVIRONMENT` | Entorno Python interno | `/tmp/mesa-venv` |
| `UV_CACHE_DIR` | Caché de dependencias | `/tmp/uv-cache` |
| `MODELOS_MCP_PORT` | Puerto local del MCP por HTTP | `8768` |
| `MESA_MCP_HOSTS` | Cabeceras Host admitidas por el MCP HTTP | `127.0.0.1:8768,localhost:8768` |
| `MESA_RELEVO_IP` | IP donde escucha el relevo | `192.168.80.1` |
| `MESA_RELEVO_URL`, `MESA_RELEVO_TOKEN` | Acceso de la API al relevo (`api.env`) | Fuera del repositorio |
| `OPENCLAW_GATEWAY_TOKEN`, `OPENCLAW_GATEWAY_URL` | Acceso del relevo al Gateway (`relevo.env`) | Fuera del repositorio |

Los valores propios de cada equipo se declaran en `.env`, junto a `compose.yaml`, que Compose lee automáticamente. Se crea copiando la plantilla versionada `.env.example` y ajustando los puertos a otros libres si los predeterminados están ocupados. `.env` está excluido de Git y del paquete de traslado. Con él, el arranque no necesita variables en la línea de comandos:

```bash
cp .env.example .env
docker compose up -d api frontend
```

`api` y `frontend` usan `restart: unless-stopped`: vuelven a arrancar tras un fallo o un reinicio del equipo o de Docker, salvo que se hayan detenido expresamente con `docker compose stop` o `down`. El perfil `mcp` no tiene política de reinicio porque se lanza por stdio a demanda.

El montaje completo es una integración **local y transitoria**: el mismo volumen contiene código y datos, y el servicio puede escribir las observaciones autorizadas. Cuando se independicen repositorios, se configurarán montajes diferenciados de código, procesos, referencias y gobierno, con permisos de solo lectura donde corresponda. Ese cambio requiere adaptar primero las rutas del generador y probar lectura y escritura; no se simula con enlaces simbólicos dependientes de Windows.

El proxy Nitro solo simplifica el consumo desde el navegador. La aplicación no tiene autenticación, identidad de usuarios ni control multiusuario, y el proxy Nitro sustituye la cabecera `Origin`, de modo que la comprobación de origen de la API no filtra a quien entra por la interfaz. No publicar este servicio como si ofreciera control multiusuario.

## Publicación detrás de un proxy inverso

Para acceder desde otra red, el frontend puede publicarse con `MODELOS_UI_BIND` (por ejemplo `0.0.0.0` o la IP de la red privada por la que llega el proxy) y servirse a través de un proxy inverso con HTTPS. Es un despliegue operativo de cada equipo: el dominio, las IP y las credenciales se configuran en `.env` y en el proxy, nunca en archivos versionados.

Condiciones mínimas:

- El proxy inverso exige control de acceso (por ejemplo, autenticación básica mediante una lista de acceso) antes de llegar a la aplicación. Sin él, cualquiera podría leer las referencias y crear observaciones, editar sesiones e integrar cambios en las tablas de `02-procesos`.
- `MODELOS_API_PORT` sigue ligado a `127.0.0.1`; el proxy apunta solo al puerto del frontend.
- Con `0.0.0.0` el frontend también queda accesible desde la red local del anfitrión sin pasar por el proxy; limitarlo con el cortafuegos del anfitrión si esa red no es de confianza.
- El control de acceso del proxy no identifica autores: el campo `autor` de las observaciones sigue siendo declarado.
