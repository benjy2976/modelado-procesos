---
tipo: mapa-de-contenido
area: procesos
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
aliases:
  - Procesos
tags:
  - tema/procesos
---

# Procesos

Sube a: [Gestion por procesos del GRH](../00-GESTION-POR-PROCESOS-GRH.md)

Esta area reune la documentacion de cada proceso tal como la organiza la Norma Tecnica de gestion por procesos (NT 002-2025-PCM-SGP): por niveles, con codigo y con su juego de documentos. El alcance actual es **S4.3 Ejecucion de la inversion**.

## Como leer el arbol

```mermaid
flowchart TD
    MAPA["Mapa de procesos institucional<br/>Nivel 0"] --> S4["S4 Gestion de las inversiones<br/>Nivel 0"]
    S4 --> S43["S4.3 Ejecucion de la inversion<br/>Nivel 1 - alcance actual"]
    S43 --> S431["S4.3.n<br/>Nivel 2 - se crean al aprobar la descomposicion"]
    S431 --> PROC["Ultimo nivel<br/>procedimiento cuando corresponda"]
```

1. **Cada carpeta es un proceso.** Su nombre empieza por el codigo NT en mayusculas, con guion en lugar de punto (`S4`, `S4-3`, `S4-3-1`). Los subprocesos son subcarpetas.
   - Los procesos **en alcance** tienen su documentacion completa (`alcance_proyecto: EN-ALCANCE`).
   - Los procesos **relacionados** fuera de alcance son nodos de referencia: solo una nota indice con su identificacion y fuente (`alcance_proyecto: REFERENCIA`). Permiten ver en el grafo el modelo de procesos y sus interacciones (`DEC-019`).
2. **Cada proceso tiene el mismo juego de documentos**, siempre con el codigo al inicio del nombre:

| Documento | Archivo | Referencia NT |
|---|---|---|
| Portada (nota indice) | `00-<carpeta>.md`, por ejemplo `00-S4-3-ejecucion-inversion.md` | - |
| Ficha de producto y proceso | `<codigo>-ficha-producto-proceso.md` | Numeral 6.1.3 a; Anexo 2 |
| Fichas de indicador | `<codigo>-fichas-indicador.md` | Numeral 6.1.3 b; Anexo 4 |
| Diagrama del proceso | `<codigo>-diagrama-proceso-tabla.md`, que genera `<codigo>-diagrama-proceso.bpmn`, `.svg`, `.png` y la vista interactiva `.html` (`DEC-026`) | Anexo 3 |
| Procedimiento | `<codigo>-procedimiento.md`, solo en el ultimo nivel y si cumple los criterios | Numeral 6.1.3 d; Anexos 7 y 8 |
| Sustento | `<codigo>-sustento.md`: fuentes, evidencias, discrepancias e historial de revision; no se exporta | Control del proyecto |
| Variacion de un documento aprobado | `<codigo>-<documento>-propuesta.md` | Control del proyecto |

3. **El estado esta en los metadatos de cada archivo**, no en carpetas. Todo lo no aprobado es `PROPUESTA` y avanza por niveles de revision:

| Nivel de revision | Quien otorga la conformidad para avanzar |
|---|---|
| `ELABORACION` | Quien elabora el documento lo remite a revision del equipo |
| `REVISION-EQUIPO` | Un integrante del equipo como representante del equipo (declarativa) |
| `OPINION-TECNICA` | Sub Gerencia de Modernizacion y Transformacion Digital |
| `APROBACION` | Dueno del proceso |

Un documento `APROBADO` no se edita: para variarlo se crea su archivo `-propuesta`. La IA nunca registra conformidades ni asigna el estado `APROBADO`.

4. **El TO-BE vive en un arbol separado** con la misma jerarquia. En esta etapa esta pendiente.

Las reglas completas estan en el [estandar de artefactos](../00-gobernanza/estandar-artefactos-modelamiento.md) y en la decision `DEC-017` del [registro de decisiones](../00-gobernanza/registro-decisiones.md).

## Contenido

- [Mapa de procesos institucional](mapa-de-procesos-institucional/00-mapa-de-procesos-institucional.md): mapa Nivel 0 e inventario de productos y procesos.
- [S4 Gestion de las inversiones](S4-gestion-de-las-inversiones/00-S4-gestion-de-las-inversiones.md): proceso Nivel 0 aprobado.
  - [S4.3 Ejecucion de la inversion](S4-gestion-de-las-inversiones/S4-3-ejecucion-inversion/00-S4-3-ejecucion-inversion.md): alcance actual del proyecto.
- [S2 Gestion contable y financiera](S2-gestion-contable-y-financiera/00-S2-gestion-contable-y-financiera.md): nodo de referencia, contraparte de S4.3 mediante S2.1.
- [S3 Gestion de bienes y servicios](S3-gestion-de-bienes-y-servicios/00-S3-gestion-de-bienes-y-servicios.md): nodo de referencia, contraparte de S4.3 mediante S3.1 y S3.2.
- [TO-BE](to-be/00-to-be.md): rediseno futuro, pendiente.

## Vistas del modelo

- En el grafo, la vista `modelo-procesos` muestra solo procesos y actores con su jerarquia e interacciones; la vista `proceso` muestra una rama completa. Se aplican con `05-herramientas/configurar_grafo_obsidian.py`.
- La [Base de procesos](../04-coordinacion/bases/procesos.base) lista los nodos de proceso y los documentos NT con sus estados.

## Fuentes y metodo

- [Fuentes institucionales aprobadas](../01-referencias/01-institucionales-grh/originales/00-originales-institucionales-grh.md)
- [Norma tecnica de gestion por procesos](../01-referencias/02-gestion-por-procesos/originales/00-originales-gestion-por-procesos.md)
- [Metodologia de modelamiento](../00-gobernanza/metodologia-modelamiento.md)
- [Plantillas de procesos](../00-gobernanza/plantillas/00-plantillas.md)
