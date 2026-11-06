---
id: AP-S4-3-2-4-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S4.3.2.4
nivel_proceso: 3
proceso:
  - S4.3.2.4
fecha_creacion: 2026-11-05
fecha_actualizacion: 2026-11-06
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-4
---

# S4.3.2.4 Gestion de ampliaciones de plazo - Sustento

Sube a: [S4.3.2.4 Gestion de ampliaciones de plazo](00-S4-3-2-4-gestion-ampliaciones-plazo.md)

## Delimitacion y trazabilidad

Este proceso recibe la variante `MOD-PLA-AMP` y las actividades de ampliacion que formaban parte del anterior S4.3.2.3. `DEC-041` reconoce que su causal, evaluacion de ruta critica, coordinacion inicial, pronunciamiento y cierre son distintos de los de alcance, suspension y paralizacion.

`DEC-042` ubica al residente dentro del Ejecutor de obra. Control de obra representa una responsabilidad alternativa: supervisor contratado en la supervision externa o inspector perteneciente a la entidad, segun modalidad; no afirma identidad organizacional ni concurrencia.

Cuaderno de Incidencias es la denominacion institucional uniforme adoptada por `DEC-041`, incluso para administracion directa; la Directiva 017-2023-CG usa "cuaderno de obra". La uniformidad terminologica no modifica el texto ni el sentido de la fuente.

## Fuentes utilizadas

| Fuente | Ubicacion precisa | Estado | Uso |
|---|---|---|---|
| Reglamento de la Ley 32069 | Arts. 198, 200 y 201, PDF pp. 112-114; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta; regla pendiente de validacion | Causal, procedimiento, opinion y decision en contrata |
| Directiva 017-2023-CG | Num. 7.3.7, PDF p. 18; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta; vigencia material pendiente de validacion | Ampliacion en administracion directa; la fuente usa cuaderno de obra |
| ROF GRH 2023 | Arts. 20 y 97-98; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta e `INFERENCIA` para el circuito | Registro documentario y seguimiento de SGGOS |
| Modelo anterior S4.3.2.3 | Variante `MOD-PLA-AMP` y matriz normativa | Antecedente en Git; propuesta no aprobada | Trazabilidad del contenido redistribuido |
| `DEC-041` | Registro de decisiones | `DECISION` | Codigo, nombre, limites y responsabilidades |

## Elementos registrados

| Elemento | Contenido | Clase | Fuente |
|---|---|---|---|
| Disparador | Solicitud o causal de ampliacion | Normativo citado | Reglamento, arts. 198 y 200; Directiva, num. 7.3.7 |
| Instancia | Una por solicitud o causal | Decision del equipo | DEC-041 |
| Producto | Ampliacion aprobada o decision no favorable comunicada | Propuesta | Analisis del flujo |
| Decision | Titular de la competencia o autoridad delegada | Decision del equipo | DEC-041; delegacion concreta pendiente |

## Vacios de evidencia

| Vacio | Marca | Fuente o accion necesaria |
|---|---|---|
| Dueno, delegacion y circuito interno | `EVIDENCIA-INSUFICIENTE` | ROF complementado con delegaciones y procedimiento vigente |
| Unidad y perfil que evalua la ruta critica | `EVIDENCIA-INSUFICIENTE` | Asignacion funcional y validacion operativa |
| Criterios para controles presupuestal y juridico | `EVIDENCIA-INSUFICIENTE` | Matriz institucional por regimen |
| Plazos internos, documentos, sistemas y notificacion | `EVIDENCIA-INSUFICIENTE` | Procedimiento y muestras no sensibles |
| Indicador, meta y fuente de datos | `EVIDENCIA-INSUFICIENTE` | Definicion del dueno del proceso |

## Informacion BIM

`EVIDENCIA-INSUFICIENTE`.

## Control de trazado

La generacion focalizada del 2026-11-05 deja D1, D2, D3, D4 y D5 sin hallazgos. La convergencia vacia posterior a la evaluacion especializada se retiro porque ambas rutas pueden llegar directamente al control contractual sin cambiar la semantica. No se modifico el generador en esta tarea.

## Historial de revision

| Documento | Nivel | Fecha | Resultado | Rol o unidad | Evidencia |
|---|---|---|---|---|---|
| Juego inicial S4.3.2.4 | `ELABORACION` | 2026-11-05 | Propuesta creada; pendiente revision | Equipo del proyecto con asistencia de IA | `DEC-041`; fuentes citadas |
| Precision de participantes | `ELABORACION` | 2026-11-05 | Residente integrado en Ejecutor de obra y control de obra declarado como responsabilidad alternativa | Equipo del proyecto con asistencia de IA | `DEC-042` |

## Relaciones

- [Sustento de S4.3.2.3](../S4-3-2-3-gestion-modificaciones-alcance/S4-3-2-3-sustento.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)

## Cambio de perfil de trazado ? 2026-11-06

Por indicacion del usuario se adopta `zigzag-controlado` para este subproceso. El cambio afecta la disposicion grafica; conserva actividades, participantes, secuencias y mensajes. Los registros anteriores de geometria corresponden a sus respectivas generaciones. Se regeneran los derivados mediante la tabla; no se realiza revision visual ni se atribuye conformidad institucional.

Resultado de los controles de esta generacion: D1, D2, D3 y D5 sin hallazgos. D4 registra 1 hallazgos geometricos (superposicion entre las etiquetas Opinion del responsable del control de obra y Solicitud y opinion). Se adopta el derivado de trabajo con `--forzar` para aplicar el perfil solicitado, sin cambiar el contenido del proceso. Estos hallazgos quedan pendientes de ajuste de disposicion y revision visual antes de una linea base; la exportacion no implica que el trazado este libre de defectos.

## Mejora del perfil zigzag-controlado ? 2026-11-06

Por solicitud del usuario se aplica la mejora general del perfil: compactacion de circuitos independientes y seleccion de corredores de mensajes con control de interferencias. Se conserva la semantica BPMN; no cambian actividades, responsables ni relaciones del proceso. D1, D2, D3 y D5 sin hallazgos. D4 conserva 1 hallazgos, del mismo tipo que los documentados en la generacion anterior; se mantiene la adopcion como derivado de trabajo con `--forzar`, con ajuste geometrico y revision visual pendientes.
