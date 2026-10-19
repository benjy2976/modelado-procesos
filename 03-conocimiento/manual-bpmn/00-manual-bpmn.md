---
tipo: mapa-de-contenido
area: manual-bpmn
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
aliases:
  - Galeria de diagramas del manual BPMN
tags:
  - tema/conocimiento
  - tema/procesos
---

# Manual BPMN: galeria de diagramas

Sube a: [Conocimiento](../00-CONOCIMIENTO.md)

**Estado: planteamiento.** La estructura de carpetas fue aceptada por el equipo del proyecto el 2026-10-19. Los diagramas aun no se desarrollan; este documento detalla lo que se hara.

## Objetivo

Transcribir con la cadena BPMN (`DEC-025`, `DEC-026`) los diagramas del [manual BPMN 2.0](../../01-referencias/02-gestion-por-procesos/originales/bpmn-2-manual-referencia-guia-practica.pdf) (`LOC-004`; Freund, Rucker y Hitpass, 4.a edicion, 2014), un diagrama por figura, ordenados como el PDF. La galeria sirve como referencia de patrones para el modelamiento del GRH y como prueba amplia de la herramienta. Cada diagrama reproduce la semantica de la figura, no su disposicion: el trazado es automatico.

## Condicion previa: derechos de uso

El manual es una obra de terceros y el catalogo no registra su licencia ni permisos de uso (`EVIDENCIA-INSUFICIENTE`). El repositorio es publico, por lo que cada transcripcion seria una reproduccion derivada publicada. Antes de la etapa 2 se debe confirmar la licencia o el permiso, o decidir una alternativa: mantener la galeria fuera de Git (`99-temporal`) o reemplazar los ejemplos del libro por ejemplos propios del GRH para cada patron. La etapa 1 solo registra numeros, paginas y titulos de figuras.

## Inventario

El PDF tiene 266 paginas y 199 imagenes incrustadas; la numeracion llega a unas 197 figuras y se identificaron 185 titulos. Distribucion por seccion (asignacion por pagina, aproximada):

| Seccion | Tema | Pagina inicial (PDF) | Figuras | Carpeta |
|---|---|---:|---:|---|
| 1 | BPM y BPMN | 1 | 5 | Sin carpeta: se registra en el inventario |
| 2.1 | Entender BPMN | 28 | 1 | Sin carpeta: se registra en el inventario |
| 2.2 | Actividades simples y eventos indefinidos | 33 | 1 | [cap-2-notacion/2-2-actividades-y-eventos-simples](cap-2-notacion/2-2-actividades-y-eventos-simples/00-2-2-actividades-y-eventos-simples.md) |
| 2.3 | Flujo de procesos con gateways | 35 | 13 | [cap-2-notacion/2-3-gateways](cap-2-notacion/2-3-gateways/00-2-3-gateways.md) |
| 2.4 | Flujo de procesos sin gateways | 47 | 4 | [cap-2-notacion/2-4-flujo-sin-gateways](cap-2-notacion/2-4-flujo-sin-gateways/00-2-4-flujo-sin-gateways.md) |
| 2.5 | Lanes | 50 | 4 | [cap-2-notacion/2-5-lanes](cap-2-notacion/2-5-lanes/00-2-5-lanes.md) |
| 2.6 | Eventos | 53 | 37 | [cap-2-notacion/2-6-eventos](cap-2-notacion/2-6-eventos/00-2-6-eventos.md) |
| 2.7 | Actividades especiales | 77 | 6 | [cap-2-notacion/2-7-actividades-especiales](cap-2-notacion/2-7-actividades-especiales/00-2-7-actividades-especiales.md) |
| 2.8 | Subprocesos | 84 | 16 | [cap-2-notacion/2-8-subprocesos](cap-2-notacion/2-8-subprocesos/00-2-8-subprocesos.md) |
| 2.9 | Pools y flujos de mensajes | 99 | 12 | [cap-2-notacion/2-9-pools-y-mensajes](cap-2-notacion/2-9-pools-y-mensajes/00-2-9-pools-y-mensajes.md) |
| 2.10 | Objetos de datos | 108 | 2 | [cap-2-notacion/2-10-objetos-de-datos](cap-2-notacion/2-10-objetos-de-datos/00-2-10-objetos-de-datos.md) |
| 2.11 | Artefactos | 110 | 1 | [cap-2-notacion/2-11-artefactos](cap-2-notacion/2-11-artefactos/00-2-11-artefactos.md) |
| 2.12 | Modelos de coreografia y conversacion | 113 | 3 | Sin carpeta: se registra en el inventario |
| 2.13 | BPMN comparado con otras notaciones | 117 | 7 | Sin carpeta: se registra en el inventario |
| 3.1 | Nivel descriptivo: sobre este nivel | 134 | 2 | Sin carpeta: se registra en el inventario |
| 3.2 | Caso de estudio: contratacion de personal | 140 | 1 | [cap-3-nivel-descriptivo/3-2-caso-contratacion-de-personal](cap-3-nivel-descriptivo/3-2-caso-contratacion-de-personal/00-3-2-caso-contratacion-de-personal.md) |
| 3.3 | Restriccion de la simbologia en el nivel descriptivo | 142 | 10 | [cap-3-nivel-descriptivo/3-3-simbologia-nivel-descriptivo](cap-3-nivel-descriptivo/3-3-simbologia-nivel-descriptivo/00-3-3-simbologia-nivel-descriptivo.md) |
| 3.4 | Reflexiones sobre el analisis en el primer nivel | 155 | 2 | Sin carpeta: se registra en el inventario |
| 3.5 | Primer nivel y BPMN 2.0 (conversacion y coreografia) | 159 | 2 | Sin carpeta: se registra en el inventario |
| 4.1 | Nivel operativo: sobre este nivel | 162 | 2 | Sin carpeta: se registra en el inventario |
| 4.2 | Del nivel 1 al nivel 2 | 167 | 2 | [cap-4-nivel-operativo/4-2-del-nivel-1-al-nivel-2](cap-4-nivel-operativo/4-2-del-nivel-1-al-nivel-2/00-4-2-del-nivel-1-al-nivel-2.md) |
| 4.3 | Procesos de los participantes | 170 | 4 | [cap-4-nivel-operativo/4-3-procesos-de-los-participantes](cap-4-nivel-operativo/4-3-procesos-de-los-participantes/00-4-3-procesos-de-los-participantes.md) |
| 4.4 | Preparacion de la automatizacion | 174 | 8 | [cap-4-nivel-operativo/4-4-preparacion-de-la-automatizacion](cap-4-nivel-operativo/4-4-preparacion-de-la-automatizacion/00-4-4-preparacion-de-la-automatizacion.md) |
| 4.5 | Recomendaciones practicas para el nivel 2 | 185 | 10 | [cap-4-nivel-operativo/4-5-recomendaciones-practicas](cap-4-nivel-operativo/4-5-recomendaciones-practicas/00-4-5-recomendaciones-practicas.md) |
| 4.6 | Filtros y frecuencia de uso de objetos | 198 | 2 | Sin carpeta: se registra en el inventario |
| 5.1 | Nivel tecnico: sobre este modelo | 202 | 1 | Sin carpeta: se registra en el inventario |
| 5.2 | Fundamentos | 205 | 2 | Sin carpeta: se registra en el inventario |
| 5.3 | Automatizacion de procesos con BPMN 2.0 | 210 | 3 | [cap-5-nivel-tecnico/5-3-automatizacion-con-bpmn](cap-5-nivel-tecnico/5-3-automatizacion-con-bpmn/00-5-3-automatizacion-con-bpmn.md) |
| 5.4 | Semantica de ejecucion | 217 | 16 | [cap-5-nivel-tecnico/5-4-semantica-de-ejecucion](cap-5-nivel-tecnico/5-4-semantica-de-ejecucion/00-5-4-semantica-de-ejecucion.md) |
| 6 | Mejora de procesos | 235 | 6 | Sin carpeta: se registra en el inventario |

Las secciones sin carpeta contienen figuras conceptuales, tablas de simbolos, otras notaciones, coreografias o conversaciones, que quedan fuera de la paleta (`DEC-027`), o figuras que se evaluaran mas adelante (capitulo 6).

## Clasificacion de cada figura

| Clase | Tratamiento |
|---|---|
| Reproducible con la paleta del proyecto | Se transcribe y debe pasar los controles D1 a D5 |
| Requiere simbolos previstos para la fase 2 | Se registra en el inventario; se transcribe cuando la paleta los incorpore |
| Ejemplo incorrecto a proposito ("uso incorrecto", "no recomendado") | No se genera: el control D5 lo rechaza; se cita con su pagina |
| No es un diagrama de proceso BPMN | No se genera; se cita con su pagina |

## Convenciones

- Carpetas por capitulo (`cap-<n>-<tema>`) y por seccion (`<n>-<m>-<tema>`), cada una con su nota indice `00-<carpeta>.md`.
- Nombre de cada figura: `fig-<capitulo>-<numero de dos digitos>-<tema-corto>`, tomado de su titulo; por ejemplo `fig-2-03-gateway-exclusivo` y `fig-2-07-ensalada-y-plato-de-fondo`.
- Por figura: `<nombre>-diagrama-proceso-tabla.md` (fuente, con la cita de figura y pagina), `.bpmn`, `.svg` y `.html`. No se generan `.png` para ahorrar espacio en LFS.
- Solo simbolos de la [paleta del proyecto](../../00-gobernanza/estandar-artefactos-modelamiento.md) (seccion 7.3); la columna `Fuente` de cada elemento cita la figura y la pagina.
- La galeria no va en `02-procesos`; `construir_modelos.py` la construira con una opcion propia (`--manual`, pendiente de implementar) para no mezclarla con los procesos del GRH.

## Etapas

| Etapa | Contenido | Tokens estimados |
|---|---|---:|
| 1a. Inventario a partir de los titulos | Las 199 figuras con numero, pagina, titulo, nombre propuesto, carpeta y clase preliminar | 40.000-70.000 |
| 1b. Verificacion visual de la clasificacion | Mirar cada figura para confirmar su clase | 180.000-250.000 |
| 2. Piloto | 5 figuras de categorias distintas, elegidas al azar entre las reproducibles | 60.000-80.000 |
| 3. Desarrollo | Todas las reproducibles (100-115) o un subconjunto priorizado (unas 30, de mayor utilidad para el GRH) | 1.200.000-1.800.000, o unas 400.000 |
| 3b. Fase 2 de la paleta | Ampliar la herramienta y transcribir las figuras que lo requieren (unas 30) | 400.000-600.000 |

Cada etapa se ejecuta por decision del equipo, despues de revisar la anterior. La etapa 3 conviene hacerla por capitulo, en sesiones separadas.

## Relaciones

- [Guia de lectura del manual BPMN](../fuentes/guia-manual-bpmn.md)
- [Gestor local de modelos](../../05-herramientas/gestor-modelos/00-gestor-modelos.md)
- [Catalogo de simbolos de la paleta](../../05-herramientas/gestor-modelos/catalogo/catalogo-simbolos-diagrama-proceso-tabla.md)
