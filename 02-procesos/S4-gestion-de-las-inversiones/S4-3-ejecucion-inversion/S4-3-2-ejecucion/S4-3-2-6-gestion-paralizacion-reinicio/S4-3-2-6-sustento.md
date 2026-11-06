---
id: AP-S4-3-2-6-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S4.3.2.6
nivel_proceso: 3
proceso:
  - S4.3.2.6
fecha_creacion: 2026-11-05
fecha_actualizacion: 2026-11-05
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-6
---

# S4.3.2.6 Gestion de paralizacion y reinicio - Sustento

Sube a: [S4.3.2.6 Gestion de paralizacion y reinicio](00-S4-3-2-6-gestion-paralizacion-reinicio.md)

## Delimitacion y trazabilidad

Este proceso recibe del anterior S4.3.2.3 la paralizacion y el reinicio. `DEC-041` los separa de la suspension contractual porque las causales, la coordinacion inicial, los actos y el cierre son distintos. Paralizacion y reinicio se modelan como instancias independientes; no se mantiene una espera indefinida entre ambas.

`DEC-042` ubica al residente dentro del Ejecutor de obra. Control de obra representa una responsabilidad alternativa: supervisor contratado en la supervision externa o inspector perteneciente a la entidad, segun modalidad; no afirma identidad organizacional ni concurrencia.

Cuaderno de Incidencias es la denominacion institucional uniforme. La Directiva 017-2023-CG usa "cuaderno de obra"; la estandarizacion terminologica no modifica la cita.

## Fuentes utilizadas

| Fuente | Ubicacion precisa | Estado | Uso |
|---|---|---|---|
| TUO de la Ley 31589 | Arts. 2 y 5.2, PDF pp. 2-3; consulta registrada en la guia local | `EXIGENCIA-NORMATIVA` propuesta | Definicion de obra publica paralizada y continuidad o resolucion en su ambito |
| Directiva 017-2023-CG | Num. 7.3.7, PDF p. 18; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta; vigencia material pendiente de validacion | Paralizacion y reinicio en administracion directa; la fuente usa cuaderno de obra |
| Reglamento de la Ley 32069 | Arts. 186-188; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta | Roles de control y Cuaderno de Incidencias cuando corresponda |
| ROF GRH 2023 | Arts. 20 y 97-98; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta e `INFERENCIA` | Registro y seguimiento interno |
| Modelo anterior S4.3.2.3 | Variante agrupada `MOD-PLA-SUS` y ruta de reinicio | Antecedente en Git; propuesta no aprobada | Trazabilidad del contenido redistribuido |
| `DEC-041` | Registro de decisiones | `DECISION` | Codigo, nombre, limites y responsabilidades |

## Elementos registrados

| Elemento | Contenido | Clase | Fuente |
|---|---|---|---|
| Disparadores | Causal de paralizacion; condiciones o solicitud de reinicio | Normativo citado | Ley 31589; Directiva 017-2023-CG, num. 7.3.7 |
| Instancias | Una por paralizacion y otra por reinicio | Decision del equipo | DEC-041 |
| Productos | Paralizacion formalizada; reinicio formalizado; decisiones no favorables | Propuesta | Analisis del flujo |
| Decision | Titular de la competencia o autoridad delegada | Decision del equipo | DEC-041; delegacion concreta pendiente |

## Vacios de evidencia

| Vacio | Marca | Fuente o accion necesaria |
|---|---|---|
| Procedimiento completo de paralizacion y reinicio en contrata | `EVIDENCIA-INSUFICIENTE` | Fuente aplicable y validacion especializada; solo se reviso la Ley 31589 |
| Interfaz entre continuidad, resolucion y el termino de S4.3.2 | `EVIDENCIA-INSUFICIENTE` | Criterio juridico y operativo documentado |
| Dueno, delegacion y unidad que prepara los actos | `EVIDENCIA-INSUFICIENTE` | ROF, delegaciones y procedimiento vigente |
| Criterios y especialista para evaluar causal y reinicio | `EVIDENCIA-INSUFICIENTE` | Matriz por regimen y asignacion funcional |
| Documentos, plazos, registros y notificacion | `EVIDENCIA-INSUFICIENTE` | Procedimiento y muestras no sensibles |
| Indicador, meta y fuente de datos | `EVIDENCIA-INSUFICIENTE` | Definicion del dueno |

## Informacion BIM

`EVIDENCIA-INSUFICIENTE`.

## Control de trazado

La generacion focalizada del 2026-11-05 deja D1, D2, D3 y D5 sin hallazgos. D4 conserva dos advertencias exclusivamente geometricas: dos flujos consecutivos comparten un tramo de 205 px entre la evaluacion especializada y la seleccion de paralizacion o reinicio, y las etiquetas "Si" y "No" de una decision se montan. Se adopta el derivado de trabajo con `--forzar`; queda pendiente revision visual humana y ajuste BPMN-DI antes de una linea base. No se modifica el generador en esta tarea.

## Historial de revision

| Documento | Nivel | Fecha | Resultado | Rol o unidad | Evidencia |
|---|---|---|---|---|---|
| Juego inicial S4.3.2.6 | `ELABORACION` | 2026-11-05 | Propuesta creada; pendiente revision | Equipo del proyecto con asistencia de IA | `DEC-041`; fuentes citadas |
| Precision de participantes | `ELABORACION` | 2026-11-05 | Residente integrado en Ejecutor de obra y control de obra declarado como responsabilidad alternativa | Equipo del proyecto con asistencia de IA | `DEC-042` |

## Relaciones

- [S4.3.2.5 Formalizacion de suspensiones de plazo](../S4-3-2-5-formalizacion-suspensiones-plazo/00-S4-3-2-5-formalizacion-suspensiones-plazo.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)
