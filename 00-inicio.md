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

## Empezar por el proceso

- **Foco actual:** [S4.3 Ejecucion de la inversion](02-procesos/s4-gestion-de-las-inversiones/s4-3-ejecucion-inversion/README.md): situacion y siguiente documento a elaborar.
- **Proceso padre aprobado:** [S4 Gestion de las inversiones](02-procesos/s4-gestion-de-las-inversiones/README.md): ficha, indicadores y diagrama.
- **Como leer los procesos:** [Procesos](02-procesos/README.md): niveles, codigos, documentos y niveles de revision.

## Areas

1. [Gobernanza](00-gobernanza/README.md): alcance, decisiones, metodo, plantillas, IA, versiones y reproducibilidad.
2. [Referencias](01-referencias/README.md): fuentes originales, catalogos, calidad y derivados de texto.
3. [Procesos](02-procesos/README.md): mapa institucional, procesos jerarquizados por codigo con su ficha, indicadores, diagrama y sustento, y arbol TO-BE pendiente.
4. [Conocimiento](03-conocimiento/README.md): reglas normativas curadas, eventos de revision y catalogos comunes.
5. [Coordinacion](04-coordinacion/README.md): reuniones, diario, Canvas y Bases transversales.
6. [Herramientas](05-herramientas/README.md): descarga, extraccion, renderizado, validacion y auditoria.
7. [Bandeja de entrada](90-bandeja-entrada/README.md): material aun no clasificado ni verificado.
8. [Temporal](99-temporal/README.md): salidas regenerables que no constituyen evidencia.

## Recorrido de trabajo

```text
Gobernanza
  -> Referencias
  -> Conocimiento estructurado
  -> Paquete de contexto
  -> Documentos del proceso (ficha, indicadores, diagrama, sustento)
  -> Circuito de revision
  -> Tag y release
```

- La linea completa esta en el [Manual operativo del conocimiento](00-gobernanza/manual-operativo-del-conocimiento.md).
- Las reglas curadas se administran en [Conocimiento estructurado](03-conocimiento/README.md).
- La biblioteca se controla desde el [Catalogo documental](01-referencias/00-catalogo/plan-descargas.md).

## Navegacion

Cada area mantiene un `README.md` como mapa de contenido. Todo documento nuevo debe quedar enlazado desde el mapa de su area y, cuando exista una dependencia real, desde el documento relacionado. Las reglas se encuentran en [Arquitectura de informacion y enlaces](00-gobernanza/arquitectura-de-informacion.md).

La redaccion y el uso de propiedades, plantillas, reuniones, tareas, Canvas y Bases se rigen por el [Estandar obligatorio de Obsidian](00-gobernanza/estandar-obligatorio-obsidian.md).

