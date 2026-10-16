---
id: GOV-PROP-IDENTIDAD-ETIQUETAS-VISTAS
tipo: propuesta
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: DECISION
proceso: []
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/gobernanza
  - tema/obsidian
---

# Propuesta de identidad, mayusculas, etiquetas y vistas del modelo de procesos

Sube a: [Gobernanza](00-GOBERNANZA.md)

Completa `DEC-018` con cuatro reglas: nombre de la nota de entrada, uso de mayusculas para enfatizar, uso obligatorio de etiquetas y vistas filtrables, entre ellas una del modelo de procesos con sus relaciones. Aprobada por el equipo del proyecto el 2026-10-16 (`DEC-019`) con estos ajustes: la nota de entrada se llama `00-GESTION-POR-PROCESOS-GRH.md`, generica para cualquier proceso del Gobierno Regional; el vocabulario de etiquetas es dinamico y se mantiene en `vocabulario-etiquetas.yaml` con el script `gestionar_etiquetas.py`; los actores externos creados se limitan a los que interactuan con S4.3; se agregaron los temas `referencias` y `coordinacion`.

## 1. Situacion actual

| Medida | Valor |
|---|---:|
| Notas Markdown | 77 |
| Notas sin etiquetas | 49 |
| Etiquetas de proceso | 2, planas (`proceso/s4`, `proceso/s4-3`) |
| Relaciones entre procesos como enlaces | 0: las interacciones de S4.3 con S4.2, S3.2, S2.1 o MEF figuran solo como texto en tablas |

Consecuencia: el grafo no puede mostrar el modelo de procesos, porque las relaciones entre procesos no son enlaces y la mayoria de los procesos relacionados no tiene una nota que los represente.

## 2. Nombre de la nota de entrada

`00-inicio.md` no dice que contiene la boveda. Se propone que su nombre exprese el objeto del proyecto:

| Opcion | Nombre | Comentario |
|---|---|---|
| A | `00-MODELO-PROCESOS-INVERSIONES-GRH.md` | Expresa el producto: el modelo de procesos de inversiones del Gobierno Regional de Huanuco. **Recomendada** |
| B | `00-MODELAMIENTO-PROCESOS-INVERSIONES.md` | Expresa la actividad; omite la entidad |
| C | `00-GESTION-PROCESOS-S4-3.md` | Centrado en el alcance actual; quedaria desactualizado al ampliar el alcance |

La nota conserva `aliases: [Inicio]` para que siga encontrandose como "Inicio".

## 3. Mayusculas para enfatizar

Hoy la convencion exige minusculas en todos los nombres. Se propone usar mayusculas solo para marcar tres niveles visuales, de modo que el explorador y el grafo distingan de inmediato que tipo de nodo es cada uno:

| Nivel | Regla | Ejemplos |
|---|---|---|
| 1. Entrada y areas | Nota indice completa en mayusculas | `00-MODELO-PROCESOS-INVERSIONES-GRH.md`, `00-PROCESOS.md`, `00-GOBERNANZA.md` |
| 2. Procesos | El codigo NT en mayusculas, como lo escribe la norma (`S4`, `S4.3`); el resto en minusculas | Carpetas `S4-gestion-de-las-inversiones/`, `S4-3-ejecucion-inversion/`; indice `00-S4-3-ejecucion-inversion.md`; documentos `S4-3-ficha-producto-proceso.md` |
| 3. Contenido | Minusculas | `arquitectura-de-informacion.md`, `registro-decisiones.md` |

Reglas complementarias:

1. Las carpetas de area conservan su nombre actual en minusculas (`02-procesos/`); solo cambia su nota indice.
2. Los indices de subareas que no son procesos usan minusculas (`00-bases.md`, `00-plantillas.md`).
3. Se mantienen la ausencia de tildes y los guiones como separador. El punto del codigo NT se escribe como guion (`S4.3` -> `S4-3`).
4. Las etiquetas se escriben siempre en minusculas, porque Obsidian no distingue mayusculas en etiquetas.
5. Dos archivos no pueden diferir solo en mayusculas: Windows no los distingue y GitHub si.

Riesgos y control:

- En Windows un cambio solo de mayusculas requiere `git mv`; un renombrado manual puede no registrarse.
- Un enlace con mayusculas incorrectas funciona en Windows y falla en GitHub o Linux. El verificador de enlaces comparara mayusculas exactas.

Alternativa sin mayusculas: conservar minusculas y enfatizar solo con el prefijo `00-` y los colores del grafo. Es mas simple, pero no responde al pedido de enfasis visual en el explorador.

## 4. Regla de etiquetas

Se mantiene el principio vigente del estandar de Obsidian: estados, aprobaciones y clasificaciones van en propiedades; las etiquetas sirven para facetas de filtrado. Se proponen dos espacios obligatorios, siempre en minusculas:

### 4.1 `proceso/` jerarquico

Reproduce la jerarquia de procesos con etiquetas anidadas:

```text
proceso/s4
proceso/s4/s4-3
proceso/s4/s4-3/s4-3-1
```

- Es obligatoria en toda nota de `02-procesos` y en toda nota que trate de un proceso concreto (reglas, reuniones, decisiones).
- Una busqueda por una etiqueta incluye sus anidadas: `tag:#proceso/s4` devuelve S4 y todos sus subprocesos; `tag:#proceso/s4/s4-3` devuelve solo la rama de S4.3.
- Cada nota lleva solo la etiqueta del proceso mas especifico al que pertenece.

### 4.2 `tema/` con vocabulario cerrado

Toda nota lleva al menos una etiqueta de tema:

| Etiqueta | Uso |
|---|---|
| `tema/procesos` | Arquitectura, fichas, modelos y documentos de proceso |
| `tema/gobernanza` | Reglas, decisiones, planes y protocolos del proyecto |
| `tema/conocimiento` | Reglas normativas, revisiones y catalogos |
| `tema/obsidian` | Boveda, notas, enlaces y vistas |
| `tema/automatizacion` | Herramientas y scripts |
| `tema/ia` | Trabajo con inteligencia artificial |
| `tema/git` | Versionado y releases |
| `tema/iniciativas` | Iniciativas del proyecto |
| `tema/glosario` | Terminologia |
| `tema/invierte-pe` | Sistema Nacional de Programacion Multianual y Gestion de Inversiones |
| `tema/contrataciones` | Contrataciones publicas |
| `tema/control-gubernamental` | Control gubernamental |
| `tema/presupuesto` | Presupuesto y administracion |
| `tema/normativa-tecnica` | Normativa tecnica sectorial |
| `tema/bim` | BIM y gestion de la informacion |

Agregar una etiqueta de tema requiere actualizar esta lista mediante decision. Las etiquetas libres o en mayusculas no se admiten.

## 5. Modelo de procesos y sus relaciones en el grafo

Para que el grafo muestre procesos relacionados entre si se necesitan dos condiciones: que cada proceso relacionado tenga una nota y que las interacciones sean enlaces.

### 5.1 Nodos de proceso

- **Procesos en alcance** (S4, S4.3 y sus subprocesos): carpeta completa con su documentacion, como hoy.
- **Procesos relacionados fuera de alcance** (S4.1, S4.2, S4.4, S4.5, S3.1, S3.2, S2.1): solo una nota indice de referencia en su lugar de la jerarquia, por ejemplo `02-procesos/S3-gestion-de-bienes-y-servicios/S3-2-contratacion-de-bienes-y-servicios/00-S3-2-contratacion-de-bienes-y-servicios.md`. Contiene codigo, nombre, nivel, fuente y la indicacion "fuera de alcance". No se documenta su ficha.
- **Actores externos** (MEF / INFOBRAS, Ministerios, PCM, Gobiernos Nacional, Regional y Local, Poblacion, Unidad productora): una nota por actor en `03-conocimiento/actores-y-roles/`, con la fuente donde se observa.

Esto ajusta el principio 6 de `DEC-017` ("solo los procesos en alcance tienen carpeta"): los procesos relacionados tendran un nodo de referencia, no documentacion.

Una propiedad nueva distingue ambos casos para colorearlos y filtrarlos:

```yaml
alcance_proyecto: EN-ALCANCE   # EN-ALCANCE | REFERENCIA
```

### 5.2 Interacciones como enlaces

- La nota indice de cada proceso en alcance incluye una seccion `Interacciones` con una fila por entrada o producto observado y un enlace a la nota de la contraparte (proceso o actor).
- Las fichas aprobadas no se modifican: los enlaces viven en las notas indice, que no son documentos NT.
- Cada fila conserva el texto literal de la ficha y su fuente esta en el sustento del proceso.

Resultado: la vista del modelo de procesos muestra la jerarquia (S4 -> S4.3 -> S4.3.n) y las interacciones laterales (S4.3 <- S4.2, S4.3 -> S2.1, S4.3 -> MEF / INFOBRAS).

## 6. Grupos y vistas filtrables

El script `configurar_grafo_obsidian.py` incorporara vistas predefinidas, ademas de las dos actuales:

| Vista | Filtro | Que muestra |
|---|---|---|
| `navegacion` | Sin filtro | Arbol completo |
| `conocimiento` | Excluye notas indice y plantillas | Conocimiento y sus relaciones |
| `modelo-procesos` | `(path:02-procesos [tipo:mapa-de-contenido] -path:02-procesos/to-be) OR path:03-conocimiento/actores-y-roles` | Solo nodos de proceso y actores, con jerarquia e interacciones |
| `proceso` con `--codigo S4.3` | `tag:#proceso/s4/s4-3` | Todos los documentos de un proceso y sus subprocesos |

Grupos de color nuevos, antes de los actuales:

| Grupo | Consulta | Color |
|---|---|---|
| Procesos en alcance | `[alcance_proyecto:EN-ALCANCE]` | Naranja |
| Procesos de referencia | `[alcance_proyecto:REFERENCIA]` | Gris claro |
| Actores externos | `path:03-conocimiento/actores-y-roles` | Amarillo |

Otras formas de ver el modelo, complementarias y sin plugins:

- **Base `procesos.base`:** tabla de todos los nodos de proceso con codigo, nivel, alcance, estado de su ficha y proceso padre.
- **Diagrama de interacciones PlantUML:** sigue siendo la vista formal; el grafo es una vista de exploracion.

## 7. Impactos

- Renombrado de `00-inicio.md`, 8 indices de area, 2 carpetas de proceso y sus documentos (los que llevan codigo NT), con `git mv` y el script de rutas.
- Actualizacion de convenciones de nombres, arquitectura de informacion, estandar de Obsidian (secciones 6 y 7.1), estandar de artefactos, `AGENTS.md`, `DEC-017` y plantillas.
- Etiquetas agregadas o normalizadas en las 77 notas.
- Creacion de 7 nodos de proceso de referencia, de 2 indices de proceso Nivel 0 (S2 y S3) y de unas 7 notas de actores, todos con su fuente.
- Ampliacion del script del grafo y del verificador de enlaces (comparacion exacta de mayusculas).

## 8. Decisiones requeridas

1. Nombre de la nota de entrada: opcion A, B, C u otra.
2. Regla de mayusculas en tres niveles o alternativa sin mayusculas.
3. Etiquetas `proceso/` jerarquicas y `tema/` con vocabulario cerrado.
4. Nodos de referencia para procesos relacionados y notas de actores externos, ajustando el principio 6 de `DEC-017`.
5. Vistas y grupos nuevos del grafo, y la Base `procesos.base`.

## Relaciones

- Continua: [propuesta de notas indice y grafo](propuesta-notas-indice-y-grafo.md) (`DEC-018`).
- Modifica: [convenciones de nombres](convenciones-nombres.md) y [estandar obligatorio de Obsidian](estandar-obligatorio-obsidian.md).
