# Reproducibilidad del repositorio

## Alcance de la garantia

La base del proyecto es reconstruible y verificable con tres mecanismos:

1. Git conserva fuentes textuales, configuracion, indices, reglas y modelos editables.
2. Git LFS conserva binarios institucionales o no reproducibles que deban formar parte del repositorio.
3. Los recursos publicos se restauran desde `registro-descargas.csv` y se aceptan solo si su SHA-256 coincide.

La reproducibilidad no equivale a preservacion externa indefinida. Si una entidad retira una URL publica, el hash permite detectar la ausencia o un reemplazo, pero no recuperar por si solo el archivo. Para eliminar ese riesgo seria necesario un espejo institucional autorizado o un paquete de preservacion fuera del repositorio ordinario.

## Entorno minimo

- Git.
- Git LFS 3 o posterior.
- Python 3.10 o posterior.
- Dependencias fijadas en `requirements.txt` para la evaluacion documental.
- Acceso a las URLs oficiales registradas y a un indice de paquetes Python o espejo institucional.
- Un remoto con soporte Git LFS para compartir los cuatro binarios locales del commit inicial.

## Reconstruccion

```powershell
git clone <URL-DEL-REPOSITORIO>
cd ejecucion
git lfs install --local
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/descargar_recursos.py --modo restaurar
.\.venv\Scripts\python.exe 05-herramientas/auditar_reproducibilidad.py
```

En Linux o macOS se sustituye `.\.venv\Scripts\python.exe` por `.venv/bin/python`.

## Evidencias de reproducibilidad

- El indice usa rutas relativas y contiene URL, tamano y SHA-256.
- `restaurar` no modifica el indice versionado.
- Los binarios publicos descargados estan ignorados por Git.
- Los binarios no reproducibles incluidos se gestionan mediante punteros LFS.
- Las extracciones Markdown masivas son cache regenerable.
- Las reglas curadas, revisiones y paquetes de contexto se conservan como texto versionable.
- Las versiones de dependencias ejecutables estan fijadas.

## Auditoria antes de publicar

Ejecutar:

```powershell
python 05-herramientas/auditar_reproducibilidad.py
```

La auditoria verifica archivos, tamanos, hashes, rutas, reglas de exclusion, atributos LFS, configuracion JSON y archivos minimos. No comprueba que todas las URLs sigan disponibles; esa comprobacion corresponde a `--modo actualizar` y puede detectar contenido nuevo sin sobrescribir originales.

## Limites actuales

- Todavia no existe un remoto configurado; por ello no se ha probado un clon desde otra maquina ni la transferencia LFS.
- El extractor Markdown y el validador web estan especificados, pero aun no implementados.
- La vigencia juridica no se deduce de la reproducibilidad tecnica y requiere validacion especializada.
- El manual BPMN aportado localmente y los tres PDF institucionales dependen del remoto LFS; antes de publicarlos en un remoto externo debe confirmarse autorizacion y licencia.

Con estos limites, el commit inicial puede declararse tecnicamente auditable y reconstruible, pero no todavia preservado de forma independiente de las fuentes oficiales.
