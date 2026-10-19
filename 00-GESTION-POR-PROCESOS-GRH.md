---
tipo: mapa-de-contenido
area: proyecto
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
aliases:
  - Inicio
  - Inicio de la boveda
tags:
  - tema/gobernanza
---

# Gestion por procesos del GRH

Punto de entrada a la boveda de gestion por procesos del Gobierno Regional de Huanuco. Organiza la documentacion de procesos conforme a la NT 002-2025-PCM-SGP y puede acoger cualquier proceso de la entidad; el alcance actual es S4.3 Ejecucion de la inversion. Los enlaces expresan la jerarquia y las dependencias principales; las carpetas conservan la separacion fisica de los artefactos.

## Situacion actual

- [Estado del proyecto](estado-del-proyecto.md)
- [README y puesta en marcha](README.md)
- [Glosario](glosario.md)
- [Instrucciones para agentes](AGENTS.md)
- [Instrucciones para Claude](CLAUDE.md): importa `AGENTS.md`

## Empezar por el proceso

- **Foco actual:** [S4.3 Ejecucion de la inversion](02-procesos/S4-gestion-de-las-inversiones/S4-3-ejecucion-inversion/00-S4-3-ejecucion-inversion.md): situacion y siguiente documento a elaborar.
- **Proceso padre aprobado:** [S4 Gestion de las inversiones](02-procesos/S4-gestion-de-las-inversiones/00-S4-gestion-de-las-inversiones.md): ficha, indicadores y diagrama.
- **Como leer los procesos:** [Procesos](02-procesos/00-PROCESOS.md): niveles, codigos, documentos y niveles de revision.

## Areas

1. [Gobernanza](00-gobernanza/00-GOBERNANZA.md): alcance, decisiones, metodo, plantillas, IA, versiones y reproducibilidad.
2. [Referencias](01-referencias/00-REFERENCIAS.md): fuentes originales, catalogos, calidad y derivados de texto.
3. [Procesos](02-procesos/00-PROCESOS.md): mapa institucional, procesos jerarquizados por codigo con su ficha, indicadores, diagrama y sustento, y arbol TO-BE pendiente.
4. [Conocimiento](03-conocimiento/00-CONOCIMIENTO.md): reglas normativas curadas, eventos de revision y catalogos comunes.
5. [Coordinacion](04-coordinacion/00-COORDINACION.md): reuniones, diario, Canvas y Bases transversales.
6. [Herramientas](05-herramientas/00-HERRAMIENTAS.md): descarga, extraccion, renderizado, validacion y auditoria.
7. [Bandeja de entrada](90-bandeja-entrada/00-BANDEJA-ENTRADA.md): material aun no clasificado ni verificado.
8. [Temporal](99-temporal/00-TEMPORAL.md): salidas regenerables que no constituyen evidencia.

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
- Las reglas curadas se administran en [Conocimiento estructurado](03-conocimiento/00-CONOCIMIENTO.md).
- La biblioteca se controla desde el [Catalogo documental](01-referencias/00-catalogo/plan-descargas.md).

## Navegacion

Cada area mantiene una nota indice `00-<nombre>.md` como mapa de contenido. Todo documento nuevo debe quedar enlazado desde el mapa de su area y, cuando exista una dependencia real, desde el documento relacionado. Las reglas se encuentran en [Arquitectura de informacion y enlaces](00-gobernanza/arquitectura-de-informacion.md).

La redaccion y el uso de propiedades, plantillas, reuniones, tareas, Canvas y Bases se rigen por el [Estandar obligatorio de Obsidian](00-gobernanza/estandar-obligatorio-obsidian.md).

