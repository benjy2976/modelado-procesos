---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
---

# Procedimientos de desarrollo y validación

Los controles actuales se ejecutan desde `05-herramientas/gestor-modelos/`. El lint y el formato aplican al paquete Python nuevo; los controles del generador se ejecutan sobre el repositorio completo al cerrar cambios en sus herramientas.

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

```powershell
uv sync --frozen
uv run ruff check mesa_modelamiento tests
uv run ruff format --check mesa_modelamiento tests
uv run pytest -q tests/test_mesa_modelamiento.py test_servidor_revision.py
uv run modelador-procesos arbol
uv run modelador-procesos contrato --check
docker compose up api
```

Para la primera pantalla Nuxt, desde `frontend/` ejecutar `npm ci`, `npm run generate:api`, `npm run lint`, `npm run typecheck` y `npm run build`. En desarrollo local arrancar la API en el puerto 8766 y `npm run dev -- --host 127.0.0.1 --port 8767`; Nuxt envía `/api` al backend. En contenedores, `docker compose up api frontend` usa el mismo contrato. La revisión visual de navegación y canvas se registra por separado de los controles de compilación.

Desde la raíz del repositorio, antes de proponer un commit que cambie diagramas o herramientas de modelamiento:

```powershell
.\.venv\Scripts\python.exe 05-herramientas\gestionar_etiquetas.py revisar
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\construir_modelos.py --check
```

Para cambios del perfil de trazado, ejecutar además `python -m unittest discover -s 05-herramientas/gestor-modelos -p test_zigzag.py`. El contrato OpenAPI actual se obtiene de FastAPI; aún falta fijarlo como artefacto generado y comparar su vigencia antes de crear el cliente Nuxt.

El estándar de memoria viva dispone del validador local `scripts/validate-project-memory`. Requiere shell POSIX y Python 3.10 o posterior. Ejecutarlo **directamente** desde la raíz de esta aplicación (por ejemplo con Git Bash en Windows), sin anteponer `python3`, y revisar hallazgos, confianza y cobertura. En un cierre global, ejecutar también Markdownlint con `.markdownlint-cli2.yaml`. El validador no sustituye los controles D1-D5 ni la revisión de hechos institucionales.

## Mantenimiento de memoria

Al cambiar una capacidad, leer el contexto funcional, la instrucción de capa y el contrato afectado; completar código y memoria en una ventana coherente. Al cerrar, revisar el diff y ejecutar el validador focalizado o global según alcance. Registrar `NOT_EVALUATED` de forma explícita. La revisión de rutas y accesos HTTP requiere cotejar `api.py`, pruebas y [API](api.md); los nombres de funciones por sí solos no prueban autorización.
