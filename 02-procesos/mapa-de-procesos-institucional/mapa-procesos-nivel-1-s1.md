---
id: AP-MAPA-NIVEL-1-S1
tipo: nota-conocimiento
area: mapa-de-procesos-institucional
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
proceso: []
fecha_creacion: 2026-10-20
fecha_actualizacion: 2026-10-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
---

# S1 en el mapa institucional Nivel 1

Sube a: [Mapa de procesos institucional](00-mapa-de-procesos-institucional.md)

Esta nota transcribe la rama S1 del mapa institucional aprobado para ubicar el proyecto de directiva PAD. La ficha de S1 coloca los productos de procedimientos disciplinarios en **S1.4 Administracion de las personas**. No se observa un codigo de Nivel 2 para el PAD en las paginas revisadas.

## Identificacion de la fuente

| Campo | Valor |
|---|---|
| Original inmutable | [Mapa de Procesos GRH - Oficial](../../01-referencias/01-institucionales-grh/originales/mapa-procesos-grh-oficial.pdf) |
| Version observada | 3.0; hoja de verificacion de cambios, pagina PDF 3 |
| SHA-256 | `92B61519CA6D15087BDB870E52D5586D4546789E0728C6947593DBF552C3C851` |
| Ubicacion precisa | Mapa Nivel 1: pagina PDF 21; inventario: pagina PDF 25; ficha S1: paginas PDF 110-111; vista institucional del proceso S1: pagina PDF 112 |
| Fecha de consulta | 2026-10-20 |
| Estado de la fuente | El usuario identifica este mapa como aprobado. Las paginas muestran sellos y firmas; no se atribuyen conformidades personales a esta transcripcion |
| Vigencia formal | EVIDENCIA-INSUFICIENTE para acto y fecha de aprobacion formal y para descartar una version posterior |
| Legibilidad | PDF escaneado sin capa de texto; lectura visual de las paginas indicadas, sin OCR sobre el original |

## Procesos de S1 Nivel 1

Las denominaciones siguen el inventario institucional de la pagina PDF 25; la pagina 21 ofrece la vista de la misma rama.

| Codigo | Denominacion observada |
|---|---|
| S1 | Gestion del recurso humano |
| S1.1 | Planificacion de Recursos Humanos |
| S1.2 | Organizacion y distribucion del trabajo |
| S1.3 | Gestion de la incorporacion |
| **S1.4** | **Administracion de las personas** |
| S1.5 | Gestion de la compensacion |
| S1.6 | Gestion del rendimiento |
| S1.7 | Gestion del desarrollo y la capacitacion |
| S1.8 | Gestion de relaciones humanas y sociales |

## Ubicacion del PAD

| Clase | Hallazgo | Ubicacion |
|---|---|---|
| Evidencia observada | La ficha de S1 clasifica S1 como proceso de **Apoyo** y registra a la Sub Gerencia de Gestion de Recursos Humanos como dueno de S1. | Pagina PDF 110, encabezado de la ficha |
| Evidencia observada | En la fila S1.4, «Administracion de las personas», figura el producto «Informes y resoluciones de procedimientos disciplinarios» y el receptor «PAD / SERVIR / CONTRALORIA». | Pagina PDF 110, tabla de descripcion del proceso; la fila continua en la pagina 111 |
| Evidencia observada | La fila S1.8 se refiere a relaciones humanas y sociales y lista productos de relaciones colectivas, seguridad y salud, bienestar y clima. No ubica alli el producto disciplinario. | Pagina PDF 111, tabla de descripcion del proceso |
| Inferencia de arquitectura | El modelamiento del PAD debe examinarse **bajo S1.4** y mantener el producto de S1.4 como interfaz del proceso padre. Esto no determina por si solo el nombre, codigo ni cantidad de procesos de Nivel 2. | Contrastacion de paginas PDF 25 y 110-111 con el proyecto de directiva, numeral 5.4.1, pagina PDF 9 |
| Evidencia insuficiente | No hay codigo `S1.4.n`, ficha de Nivel 1 propia de S1.4 ni descomposicion aprobada de su componente disciplinario en las paginas revisadas. | Paginas PDF 21, 25 y 110-112 |

La [propuesta de directiva PAD](../../90-bandeja-entrada/revision-proyecto-directiva-pad.md) denomina el subproceso «Gestion del Regimen Disciplinario y Procedimiento Administrativo Sancionador» en su numeral 5.4.1. Esa denominacion pertenece al **borrador** y no sustituye «S1.4 Administracion de las personas» del mapa aprobado.

## Uso en el modelamiento

- Conservar S1 y S1.4 como codigos y nombres de la fuente institucional recibida.
- Formular la eventual descomposicion del PAD por debajo de S1.4 sin asignar un codigo Nivel 2 hasta contar con decision institucional documentada.
- No editar ni reemplazar la ficha institucional aprobada de S1. Cualquier nueva ficha o modelo se tramita como propuesta del nivel que corresponda.
- Contrastar el flujo de la directiva propuesta con evidencia de ejecucion actual antes de llamarlo AS-IS.

## Relaciones

- Se sustenta en: [Mapa de Procesos GRH - Oficial](../../01-referencias/01-institucionales-grh/originales/mapa-procesos-grh-oficial.pdf).
- Alimenta: [Revision del proyecto de directiva PAD](../../90-bandeja-entrada/revision-proyecto-directiva-pad.md).
- Alimenta: [Propuesta de modelamiento PAD](../../90-bandeja-entrada/propuesta-modelamiento-pad.md).
- Ubica: [S1.4 Administracion de las personas](../S1-gestion-del-recurso-humano/S1-4-administracion-de-las-personas/00-S1-4-administracion-de-las-personas.md).
