---
tipo: mapa-de-contenido
area: herramientas
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# Herramientas previstas

[Inicio](../00-inicio.md)

1. Catalogador y verificador de hashes.
2. Detector de texto y calidad OCR.
3. Extractor de texto con referencia de pagina.
4. Validador BPMN 2.0.
5. Generador de matrices de trazabilidad.
6. Generador de paquetes de publicacion.
7. Extractor PDF a Markdown con marcadores de pagina y hash de origen.
8. Generador y validador del catalogo de reglas.
9. Aplicacion web interna para revision especializada del conocimiento.
10. Auditor de reproducibilidad del repositorio y la cache documental.
11. Gestor local de modelos PlantUML/BPMN, derivados, validaciones e intercambio compacto con IA.

Las especificaciones son `extractor-documental/README.md` y `validador-conocimiento/README.md`. La aplicacion debe conservar YAML y eventos de revision como fuentes maestras versionadas.

## Especificaciones

- [Guia de instalacion y propuesta de herramientas](guia-entorno.md): entorno ampliado, utilidad, versiones y comprobaciones al clonar.
- [Extractor documental](extractor-documental/README.md)
- [Validador de conocimiento](validador-conocimiento/README.md)
- [Gestor local de modelos](gestor-modelos/README.md)
- [Iniciativa del gestor de modelos](../00-gobernanza/iniciativas/iniciativa-modelamiento-hibrido.md)
- [Estandar de artefactos de modelamiento](../00-gobernanza/estandar-artefactos-modelamiento.md)
- [Referencias y catalogos](../01-referencias/README.md)
- [Conocimiento estructurado](../04-recursos-reutilizables/conocimiento/README.md)

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
