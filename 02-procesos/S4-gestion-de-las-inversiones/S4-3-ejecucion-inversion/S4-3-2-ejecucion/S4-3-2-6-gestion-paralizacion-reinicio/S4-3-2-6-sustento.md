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
fecha_actualizacion: 2026-11-10
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

## Cambio de perfil de trazado ? 2026-11-06

Por indicacion del usuario se adopta `zigzag-controlado` para este subproceso. El cambio afecta la disposicion grafica; conserva actividades, participantes, secuencias y mensajes. Los registros anteriores de geometria corresponden a sus respectivas generaciones. Se regeneran los derivados mediante la tabla; no se realiza revision visual ni se atribuye conformidad institucional.

Resultado de los controles de esta generacion: D1, D2, D3 y D5 sin hallazgos. D4 registra 6 hallazgos geometricos (superposiciones de flujos y etiquetas y un cruce de flujo con etiqueta). Se adopta el derivado de trabajo con `--forzar` para aplicar el perfil solicitado, sin cambiar el contenido del proceso. Estos hallazgos quedan pendientes de ajuste de disposicion y revision visual antes de una linea base; la exportacion no implica que el trazado este libre de defectos.

## Mejora del perfil zigzag-controlado ? 2026-11-06

Por solicitud del usuario se aplica la mejora general del perfil: compactacion de circuitos independientes y seleccion de corredores de mensajes con control de interferencias. Se conserva la semantica BPMN; no cambian actividades, responsables ni relaciones del proceso. D1, D2, D3 y D5 sin hallazgos. D4 conserva 6 hallazgos, del mismo tipo que los documentados en la generacion anterior; se mantiene la adopcion como derivado de trabajo con `--forzar`, con ajuste geometrico y revision visual pendientes.

## Convencion de carriles y SGD

Se aplica la [convencion de carriles y SGD](../../../../../00-gobernanza/estandar-artefactos-modelamiento.md#74-convencion-de-carriles-y-sgd-en-s432) de `DEC-043`. El pool funcional antes titulado Control de obra se muestra como Supervisor o inspector de obra, segun modalidad; no se presume una misma organizacion. OACGD usa la etiqueta uniforme. El registro y la derivacion inicial a SGGOS se modelan con tarea de usuario y `almacen: SGD`. Otras actividades de consolidacion no se declaran derivaciones por SGD sin evidencia de su tramite. El pool Ejecutor de obra, segun regimen es una abstraccion provisional mientras se contrasta la organizacion por modalidad.

La generacion focalizada de esta normalizacion deja D1, D2, D3 y D5 sin hallazgos. D4 registra 6 hallazgos geometricos (un tramo compartido, etiquetas montadas y un cruce con etiqueta) en las rutas de paralizacion y reinicio; no afectan las referencias ni la terminacion. Se adoptaron BPMN, SVG, PNG y HTML de trabajo con `--forzar`, con revision visual y ajuste de disposicion pendientes antes de una linea base. No se atribuye conformidad institucional.

Regeneracion derivada del ajuste visual de `zigzag-controlado` en S4.3.1, 2026-11-18: la tabla y la semantica de S4.3.2.6 no cambian. D1, D2, D3 y D5 permanecen sin hallazgos; D4 baja de dos a un hallazgo geometrico. Se sincronizan BPMN, SVG, PNG y HTML de trabajo con `--forzar`; el hallazgo pendiente sigue sujeto a revision de disposicion antes de una linea base.

## Auditoría por afirmación — 2026-11-24 (fase 5)

Auditoría con el formato de DEC-057 ([informe generado](../../../../../05-herramientas/gestor-modelos/auditorias/S4-3-2-6/informe.md)). Comprende 26 afirmaciones (5 `SUSTENTADA`, 21 `INFERENCIA`, sin contradicciones) y 12 obligaciones del num. 7.3.7 de la Directiva 017-2023-CG, del TUO de la Ley 31589 (arts. 2 y 5) y del Reglamento art. 198.1 a). De ellas, 7 no están representadas. Se calcularon 18 anclas desde el texto, todas vigentes. Ambas fuentes tienen la vigencia jurídica por confirmar según el catálogo; el ancla lo indica. D4 mantiene el hallazgo geométrico ya documentado y se regeneró con `--forzar`. Son propuestas de IA, sin validación ni conformidad.

- **Bien representado (administración directa):** el residente informa la paralización o el reinicio por el cuaderno de obra; el supervisor o inspector la valida y emite un informe aprobatorio para el reinicio; un acto resolutivo aprueba la modificación de plazo y la OAD autoriza el reinicio (7.3.7).
- **Ámbito de las fuentes (inferencia principal):**
  - la Ley 31589 regula un **régimen especial** de reactivación de obras inventariadas como paralizadas: en contrata, avance ≥ 40 % y 6 meses sin ejecución o contrato resuelto o nulo; en administración directa, ≥ 50 %. No regula el evento ordinario de paralización. Citarla en R-E1, S-T1 y E-T5 es un antecedente, no una fuente directa;
  - en contrata el Reglamento no tiene una figura propia de paralización: la trata como causal de ampliación (198.1 a) o, con acuerdo, como suspensión (107, S4.3.2.5). Esto coincide con el vacío `EVIDENCIA-INSUFICIENTE` ya registrado para contrata.
- **No representado:**
  - la anotación de tres fechas en el cuaderno: solicitud de paralización, paralización real y reinicio (7.3.7);
  - el cronograma actualizado que el residente entrega en 2 días calendario tras el reinicio, para el acto resolutivo (7.3.7);
  - el registro previo de la modificación de plazo en el SNPMGI y el INFOBRAS (7.3.7);
  - en el régimen de la Ley 31589: su ámbito (2.1), la decisión de proponer la continuidad o resolver (5.2) y la respuesta del contratista en 15 días calendario (5.3);
  - la interfaz de contrata con S4.3.2.4 (198.1 a).
- **Limitación de herramienta:** el texto extraído de la Directiva 017-2023-CG no se segmenta por numerales. El «artículo 3» de la resolución aprobatoria absorbe la directiva (pp. 3-30) y las citas se resuelven dentro de un fragmento amplio. Las anclas caen en la p. 18, que es la correcta.
- **Propuestas no aplicadas:**
  - decidir con el equipo si S4.3.2.6 queda solo para administración directa y, en contrata, se deriva la paralización a S4.3.2.4 o S4.3.2.5;
  - si se mantiene el régimen de la Ley 31589, modelarlo como variante con la propuesta de continuidad o resolución y el plazo de 15 días calendario;
  - nombrar en R-T1 las tres fechas y en E-T9 el cronograma actualizado y el registro en el SNPMGI y el INFOBRAS.

## Enfoque en contrata — 2026-11-25 (DEC-063)

Por decisión del usuario, S4.3.2.6 se centra en obras por contrata, la modalidad que más ejecuta el GORE. En administración directa el procedimiento ya está regulado por la Directiva 017-2023-CG (num. 7.3.7: tres fechas en el cuaderno, cronograma actualizado en 2 días calendario, registro en el SNPMGI y el INFOBRAS y acto resolutivo), que se conserva aquí como referencia y no se diagrama.

| Tramo | Contenido | Clase |
|---|---|---|
| Paralización | El contratista anota el inicio de la causal en el cuaderno de incidencias (Reglamento, art. 200.1 a) | Exigencia normativa |
| Paralización | La supervisión verifica e informa; la entidad evalúa la causa y la atribución, registra en INFOBRAS y, si no es atribuible, deriva a S4.3.2.5 para acordar la suspensión | Práctica institucional informada por el usuario |
| Paralización | Sin acuerdo, la paralización fundada sigue como causal de ampliación (198.1 a, S4.3.2.4) | Exigencia normativa |
| Reinicio | El contratista anota el fin de la causal (200.1 a); desde ahí corren los 10 días hábiles para solicitar la ampliación | Exigencia normativa |
| Reinicio | Acta de reinicio suscrita por la supervisión y el contratista; registro en INFOBRAS | Práctica institucional informada por el usuario |
| Paralización prolongada | TUO de la Ley 31589: inventario de la UEI (3), informe de estado situacional (4.1-4.2), lista priorizada al 31 de diciembre (4.4), publicación en 5 días hábiles (9.1), propuesta de continuidad o resolución (5.2) y respuesta del contratista en 15 días calendario (5.3) | Exigencia normativa; vigencia por confirmar |
| Obra no priorizada | Fin «Obra no incluida en la lista priorizada» | Inferencia |

El registro en INFOBRAS queda con `EVIDENCIA-INSUFICIENTE` normativa: la Directiva 005-2023-CG no está en la biblioteca. El contrato resuelto o nulo de la Ley 31589 (2.1 ii) y el trámite de resolución quedan diferidos (`DEC-061`).

Las dudas y pendientes de este cambio están registrados como observaciones de Claudia en `S4-3-2-6-observaciones.json` (`DEC-064`, `DEC-065`) y se resolverán una por una.

**Generación.** D1, D2, D3 y D5 sin hallazgos. D4 registra 5 hallazgos geométricos: 3 flujos superpuestos (el corredor común de R-F1→S-E1 y T-T3→C-E1, y las salidas de T-G1 hacia T-F4 y T-F2 sobre la entrada desde O-T1) y 2 etiquetas de documentos montadas sobre anotaciones (U-T2 y T-T3). Se adoptó con `--forzar` para poder observar las cajas nuevas en el módulo de observaciones; quedan pendientes de revisión visual del usuario y de ajuste de disposición. No afectan referencias ni terminación.

**Auditoría.** La auditoría por afirmación y la cobertura siguen sobre la revisión anterior de la tabla; varias anclas del visor corresponden al contenido previo. Se reconfirmarán al cerrar las observaciones que cambian el flujo. No se atribuye validación ni conformidad.
