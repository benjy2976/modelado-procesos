---
tipo: mapa-de-contenido
area: proyecto
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# Inicio de la boveda

Este es el punto de entrada a la documentacion del proyecto. Los enlaces expresan la jerarquia y las dependencias principales; las carpetas conservan la separacion fisica de los artefactos.

## Situacion actual

- [Estado del proyecto](estado-del-proyecto.md)
- [README y puesta en marcha](README.md)
- [Glosario](glosario.md)
- [Instrucciones para agentes](AGENTS.md)

## Areas

1. [Gobernanza](00-gobernanza/README.md): alcance, decisiones, metodo, conocimiento, IA, versiones y reproducibilidad.
2. [Referencias](01-referencias/README.md): fuentes originales, catalogos, calidad y derivados de texto.
3. [Arquitectura de procesos](02-arquitectura-procesos/README.md): niveles aprobados e inventario de procesos.
4. [Modelamiento](03-modelamiento/README.md): levantamiento, AS-IS, analisis, TO-BE, BIM y validacion.
5. [Recursos reutilizables](04-recursos-reutilizables/README.md): conocimiento estructurado, plantillas y componentes comunes.
6. [Herramientas](05-herramientas/README.md): descarga, extraccion, validacion y auditoria.
7. [Coordinacion](06-coordinacion/README.md): reuniones, diario, Canvas y Bases transversales.
8. [Bandeja de entrada](90-bandeja-entrada/README.md): material aun no clasificado ni verificado.
9. [Temporal](99-temporal/README.md): salidas regenerables que no constituyen evidencia.

## Recorrido de trabajo

```text
Gobernanza
  -> Referencias
  -> Conocimiento estructurado
  -> Paquete de contexto
  -> Arquitectura y modelamiento
  -> Validacion
  -> Tag y release
```

- La linea completa esta en el [Manual operativo del conocimiento](00-gobernanza/manual-operativo-del-conocimiento.md).
- El piloto se desarrolla en [S4.3 Ejecucion de la inversion](03-modelamiento/procesos/s4-3-ejecucion-inversion/README.md).
- Las reglas curadas se administran en [Conocimiento estructurado](04-recursos-reutilizables/conocimiento/README.md).
- La biblioteca se controla desde el [Catalogo documental](01-referencias/00-catalogo/plan-descargas.md).

## Navegacion

Cada area mantiene un `README.md` como mapa de contenido. Todo documento nuevo debe quedar enlazado desde el mapa de su area y, cuando exista una dependencia real, desde el documento relacionado. Las reglas se encuentran en [Arquitectura de informacion y enlaces](00-gobernanza/arquitectura-de-informacion.md).

La redaccion y el uso de propiedades, plantillas, reuniones, tareas, Canvas y Bases se rigen por el [Estandar obligatorio de Obsidian](00-gobernanza/estandar-obligatorio-obsidian.md).

