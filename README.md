---
tipo: mapa-de-contenido
area: proyecto
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# Modelamiento de procesos - Ejecucion de inversiones

Repositorio de trabajo para documentar, contrastar, modelar y mejorar los procesos de gestion de inversiones del Gobierno Regional de Huanuco, con enfasis inicial en S4.3 Ejecucion de la inversion y con adopcion progresiva de BIM.

Entrada de navegacion: [Inicio de la boveda](00-inicio.md).

## Puesta en marcha despues de clonar

Para el entorno ampliado de trabajo documental y desarrollo, seguir la [guia de instalacion y propuesta de herramientas](05-herramientas/guia-entorno.md). Incluye preparacion automatica con Python estable 3.11 o posterior, dependencias fijadas con hashes y comprobacion funcional. Los pasos siguientes conservan el perfil minimo del catalogador.

Requisitos:

- Git y Git LFS.
- Python estable 3.11 o posterior. El comando concreto puede ser `python`, `python3` o `py -3.x`, segun el equipo.
- Acceso a internet o espejos institucionales para instalar dependencias y reconstruir la biblioteca publica.

```powershell
git clone <URL-DEL-REPOSITORIO>
cd ejecucion
git lfs install --local
python3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/descargar_recursos.py --modo restaurar
.\.venv\Scripts\python.exe 05-herramientas/auditar_reproducibilidad.py
```

`restaurar` lee el indice versionado `01-referencias/00-catalogo/registro-descargas.csv`, descarga solamente los archivos ausentes y comprueba su hash SHA-256. No modifica el indice. Los PDF y otros binarios publicos descargables son una cache local ignorada por Git, por lo que `git status` debe permanecer limpio.

El resultado de la sincronizacion queda en `99-temporal/registro-ultima-sincronizacion.csv`. Si algun recurso no puede recuperarse o no coincide con el hash registrado, se informa alli como alerta y no debe darse por valido.

## Actualizar las fuentes publicas

```powershell
# Busca adjuntos nuevos desde las paginas oficiales configuradas.
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/descargar_recursos.py --modo descubrir

# Comprueba si cambio el contenido de recursos ya registrados.
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/descargar_recursos.py --modo actualizar
```

`actualizar` nunca sobrescribe un original. Cuando detecta contenido diferente, guarda el candidato en `99-temporal/actualizaciones-documentales/` para revision humana. Solo despues de verificar fuente, vigencia, integridad y calidad se actualizan y confirman en Git el indice o la configuracion de fuentes. Para agregar una familia documental se edita `05-herramientas/catalogador-documental/fuentes-descarga.json` y se ejecuta `descubrir`.

La evaluacion tecnica de PDF es opcional y requiere `pypdf`:

```powershell
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/evaluar_calidad.py
```

En Linux o macOS se usa `.venv/bin/python` en lugar de `.\.venv\Scripts\python.exe`. La guia detallada, los limites de la garantia y las reglas de inmutabilidad estan en `00-gobernanza/reproducibilidad.md`, `01-referencias/README.md` y `01-referencias/00-catalogo/plan-descargas.md`.

## Lectura inicial

1. [Estado del proyecto](estado-del-proyecto.md)
2. [Instrucciones para agentes](AGENTS.md)
3. [Alcance](00-gobernanza/alcance.md)
4. [Manual operativo del conocimiento](00-gobernanza/manual-operativo-del-conocimiento.md)
5. [Estandar obligatorio de Obsidian](00-gobernanza/estandar-obligatorio-obsidian.md)
6. [Protocolo de trabajo con IA](00-gobernanza/protocolo-trabajo-con-ia.md)
7. [Protocolo de conocimiento confiable](00-gobernanza/protocolo-conocimiento-confiable.md)
8. [Versionado y releases](00-gobernanza/protocolo-versionado-y-releases.md)
9. [Plan de descargas](01-referencias/00-catalogo/plan-descargas.md)

## Estructura

- [Gobernanza](00-gobernanza/README.md): reglas, metodo, decisiones y plan de trabajo.
- [Referencias](01-referencias/README.md): fuentes externas e institucionales; los originales son inmutables.
- [Arquitectura de procesos](02-arquitectura-procesos/README.md): mapas aprobados e inventario de procesos.
- [Modelamiento](03-modelamiento/README.md): trabajo vigente organizado por proceso y tipo de artefacto.
- [Recursos reutilizables](04-recursos-reutilizables/README.md): plantillas, glosarios, actores, controles y componentes comunes.
- [Herramientas](05-herramientas/README.md): utilidades de catalogacion, OCR, BPMN y trazabilidad.
- [Coordinacion](06-coordinacion/README.md): reuniones, diario, Canvas y Bases transversales.
- [Bandeja de entrada](90-bandeja-entrada/README.md): archivos recibidos pendientes de clasificacion.
- [Temporal](99-temporal/README.md): salidas transitorias que no deben versionarse.

## Fuentes maestras

- Conocimiento y fichas: Markdown con metadatos YAML.
- Datos tabulares: CSV o XLSX segun el uso.
- Diagramas: BPMN 2.0 XML (`.bpmn`).
- Intercambio BIM: formatos abiertos cuando sean aplicables, especialmente IFC y BCF.
- PDF y SVG: salidas de revision o publicacion, no fuentes editables.

## Conocimiento normativo y apoyo de IA

La IA puede extraer, proponer, relacionar y revisar, pero no validar conocimiento normativo. Cada regla confiable debe vincularse con un original, hash, ubicacion precisa, vigencia y evento de validacion humana. Las reglas YAML son la fuente maestra; `04-recursos-reutilizables/conocimiento/catalogo-reglas.csv` es una vista regenerable.

Cada tarea de IA usa un paquete de contexto limitado. No se carga la biblioteca completa ni se aceptan afirmaciones normativas basadas en memoria general del modelo. El equipo validara las reglas mediante el flujo definido en `00-gobernanza/protocolo-conocimiento-confiable.md` y, progresivamente, mediante la aplicacion requerida en `05-herramientas/validador-conocimiento/README.md`.

La linea de trabajo completa, desde el ingreso de una fuente hasta la aprobacion de una propuesta o modelo, se encuentra en `00-gobernanza/manual-operativo-del-conocimiento.md`. El manual clasifica cada afirmacion como normativa, observada, referencia, inferencia, propuesta o decision y determina las validaciones aplicables a cada clase.

## Versiones y publicaciones

El repositorio completo es el espacio de trabajo vigente: no existen copias paralelas `WIP`, `Compartido`, `Publicado` o `Archivo`. Git conserva cada cambio. Las ramas y solicitudes de cambio sirven para revision; las lineas base aprobadas se identifican con tags anotados y releases. Una publicacion reemplazada permanece recuperable como release historico y no se copia a otra carpeta.
