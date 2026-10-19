---
tipo: mapa-de-contenido
area: herramientas
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
aliases:
  - Herramientas previstas
tags:
  - tema/automatizacion
---

# Herramientas previstas

Sube a: [Gestion por procesos del GRH](../00-GESTION-POR-PROCESOS-GRH.md)

1. Catalogador y verificador de hashes.
2. Detector de texto y calidad OCR.
3. Extractor de texto con referencia de pagina.
4. Validador BPMN 2.0: esquema OMG, referencias, bloqueos y trazado (`_validar_bpmn.py`, `_revisar_trazado.py`; `DEC-025`).
5. Generador de matrices de trazabilidad.
6. Generador de paquetes de publicacion.
7. Extractor PDF a Markdown con marcadores de pagina y hash de origen.
8. Generador y validador del catalogo de reglas.
9. Aplicacion web interna para revision especializada del conocimiento.
10. Auditor de reproducibilidad del repositorio y la cache documental.
11. Gestor local de modelos PlantUML/BPMN, derivados, validaciones e intercambio compacto con IA. Vigentes: renderizado PlantUML y cadena BPMN de tabla a BPMN, SVG y PNG (`tabla_a_bpmn.py`, `renderizar_bpmn.py`; `DEC-025`).
12. Configurador local del grafo de Obsidian con los grupos de color y vistas comunes (`configurar_grafo_obsidian.py`).
13. Gestor del vocabulario de etiquetas: revisar, aplicar, renombrar y listar (`gestionar_etiquetas.py`).

Las especificaciones son `extractor-documental/00-extractor-documental.md` y `validador-conocimiento/00-validador-conocimiento.md`. La aplicacion debe conservar YAML y eventos de revision como fuentes maestras versionadas.

## Especificaciones

- [Guia de instalacion y propuesta de herramientas](guia-entorno.md): entorno ampliado, utilidad, versiones y comprobaciones al clonar.
- [Extractor documental](extractor-documental/00-extractor-documental.md)
- [Validador de conocimiento](validador-conocimiento/00-validador-conocimiento.md)
- [Gestor local de modelos](gestor-modelos/00-gestor-modelos.md)
- [Iniciativa del gestor de modelos](../00-gobernanza/iniciativas/iniciativa-modelamiento-hibrido.md)
- [Estandar de artefactos de modelamiento](../00-gobernanza/estandar-artefactos-modelamiento.md)
- [Referencias y catalogos](../01-referencias/00-REFERENCIAS.md)
- [Conocimiento estructurado](../03-conocimiento/00-CONOCIMIENTO.md)

## Grafo de Obsidian

```powershell
# Aplica los grupos de color comunes; conserva el resto de la configuracion personal.
.\.venv\Scripts\python.exe 05-herramientas/configurar_grafo_obsidian.py --vista conocimiento
.\.venv\Scripts\python.exe 05-herramientas/configurar_grafo_obsidian.py --vista modelo-procesos
.\.venv\Scripts\python.exe 05-herramientas/configurar_grafo_obsidian.py --vista proceso --codigo S4.3
```

Los grupos y vistas se describen en el [estandar de Obsidian](../00-gobernanza/estandar-obligatorio-obsidian.md), seccion 7.1.

## Etiquetas

```powershell
# Comprueba que todas las notas cumplen el vocabulario de etiquetas
.\.venv\Scripts\python.exe 05-herramientas/gestionar_etiquetas.py revisar
```

El vocabulario y el resto de comandos se describen en el [estandar de Obsidian](../00-gobernanza/estandar-obligatorio-obsidian.md), seccion 6.1.

## Biblioteca publica reproducible

El indice versionado es `01-referencias/00-catalogo/registro-descargas.csv`. Sus rutas deben ser relativas al repositorio.

```powershell
# Despues de clonar: descarga solo archivos ausentes, verifica su SHA-256 y no modifica el indice.
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/descargar_recursos.py --modo restaurar

# Consulta las fichas oficiales y agrega adjuntos nuevos al indice.
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/descargar_recursos.py --modo descubrir

# Vuelve a consultar los recursos y detecta cambios de contenido.
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/descargar_recursos.py --modo actualizar
```

`actualizar` nunca sobrescribe un original. Si el contenido remoto cambia, deja un candidato en `99-temporal/actualizaciones-documentales/` y mantiene intacto el indice versionado hasta su revision.

El reporte de cada ejecucion se genera en `99-temporal/registro-ultima-sincronizacion.csv`.

## Auditoria previa a commit o release

```powershell
.\.venv\Scripts\python.exe 05-herramientas/auditar_reproducibilidad.py
```

El resultado `APTO CON DEPENDENCIAS EXTERNAS DECLARADAS` confirma integridad local, exclusiones y LFS. Las advertencias recuerdan los limites que no puede resolver el repositorio por si solo, como la permanencia de URLs publicas o un remoto aun no configurado.
