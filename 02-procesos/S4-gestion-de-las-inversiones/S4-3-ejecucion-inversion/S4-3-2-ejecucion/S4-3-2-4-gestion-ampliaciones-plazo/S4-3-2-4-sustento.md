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
fecha_actualizacion: 2026-11-10
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

`DEC-042` ubica al residente dentro del contratista y distingue al supervisor contratado del inspector de la entidad. Por observacion del usuario del 2026-11-10, este diagrama usa los titulos funcionales **Contratista** y **Supervisor o inspector de obra**. El segundo titulo expresa alternativas segun modalidad, sin afirmar concurrencia ni pertenencia a una misma organizacion. La adscripcion del inspector al GORE sigue siendo una diferencia organizativa que el modelo unificado no detalla.

Cuaderno de Incidencias es la denominacion institucional uniforme adoptada por `DEC-041`, incluso para administracion directa; la Directiva 017-2023-CG usa "cuaderno de obra". La uniformidad terminologica no modifica el texto ni el sentido de la fuente.

## Fuentes utilizadas

| Fuente | Ubicacion precisa | Estado | Uso |
|---|---|---|---|
| Reglamento de la Ley 32069 | Arts. 198, 200 y 201, PDF pp. 112-114; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta; regla pendiente de validacion | Causal, procedimiento, opinion y decision en contrata |
| Directiva 017-2023-CG | Num. 7.3.7, PDF p. 18; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta; vigencia material pendiente de validacion | Ampliacion en administracion directa; la fuente usa cuaderno de obra |
| ROF GRH 2023 | Arts. 20, 44-45 y 92-98, PDF pp. 15, 24 y 46-48; consulta 2026-11-10; vigencia material pendiente de validacion | `EXIGENCIA-NORMATIVA` propuesta e `INFERENCIA` para el circuito | Funciones de registro documentario, GRAJ, GRI y SGGOS; no establece por si solo la secuencia interna descrita |
| Modelo anterior S4.3.2.3 | Variante `MOD-PLA-AMP` y matriz normativa | Antecedente en Git; propuesta no aprobada | Trazabilidad del contenido redistribuido |
| `DEC-041` | Registro de decisiones | `DECISION` | Codigo, nombre, limites y responsabilidades |
| Observaciones y aclaraciones del usuario | Mensajes de 2026-11-10 en esta conversacion | `EVIDENCIA-OBSERVADA` comunicada por el usuario; pendiente de contraste documental | Nombres funcionales, uso interno del SGD, secuencia coordinador-subgerente-GRI-GRAJ-decisor, proyecto de resolucion de GRAJ y decision mediante resolucion |

## Ajuste operativo propuesto el 2026-11-10

Paquete de contexto de esta revision: fase **conceptual**; fuentes textuales activas: ficha, tabla y sustento de S4.3.2.4, observacion y aclaracion del usuario, guia de lectura del ROF, ROF GRH 2023 y referencias normativas ya citadas en este sustento. BPMN XML, SVG, PNG y HTML generados quedan excluidos del contexto. No corresponde revision visual en este lote; la modificacion de herramientas no esta autorizada.

- **Evidencia comunicada por el usuario:** los registros y derivaciones internas del GORE se hacen mediante el Sistema de Gestion Documental (SGD). El coordinador evalua y eleva su informe al subgerente; este hace suyo el informe o emite opinion propia mediante informe tecnico y lo eleva a GRI; el gerente hace suyo el informe o emite criterio propio y remite el expediente con memorandum a GRAJ. El usuario preciso que GRAJ emite opinion legal, proyecta la resolucion y deriva al decisor, sin aprobar o denegar por si misma. La solicitud siempre se resuelve mediante resolucion, favorable o no favorable.
- **Representacion propuesta:** el SGD se dibuja con el almacen de datos BPMN de la paleta del proyecto y aparece en las tareas de registro o derivacion. Las tareas son de usuario cuando una persona registra o deriva; no se presume automatizacion de la evaluacion ni de la decision. GRAJ emite opinion legal y, en una tarea posterior, proyecta la resolucion y deriva el expediente por SGD. La autoridad competente resuelve mediante resolucion antes de la bifurcacion favorable o no favorable. Las tres cajas anteriores de evaluacion especializada, control contractual y consolidacion generica se retiran del flujo principal, que ahora asigna evaluacion e informes a los cargos comunicados.
- **Exigencia normativa distinguida:** el Reglamento de la Ley 32069, art. 200, y la Directiva 017-2023-CG, num. 7.3.7, se mantienen como fuentes propuestas para el procedimiento y la decision segun regimen. El ROF ubica funciones de las unidades, pero la secuencia entre cargos y el uso del SGD provienen de la observacion del usuario, no de esos articulos.
- **Inferencia y pendiente:** la autoridad exacta que firma el acto de aprobacion o denegacion y las delegaciones no estan acreditadas. Se conserva el carril funcional "Autoridad competente para resolver" y la marca `EVIDENCIA-INSUFICIENTE` hasta recibir el acto de delegacion o procedimiento aplicable. El supervisor contratado y el inspector de la entidad siguen siendo rutas alternativas cuya representacion organizativa separada requiere una variante posterior si el equipo la solicita.

### Propuesta local de titulos de carriles

Esta propuesta local fue extendida a S4.3.2 y sus seis hijos mediante `DEC-043` y la [convencion de la seccion 7.4 del estandar](../../../../../00-gobernanza/estandar-artefactos-modelamiento.md#74-convencion-de-carriles-y-sgd-en-s432). Los carriles externos se nombran por su interviniente y los internos con el patron **sigla de unidad — rol o funcion** cuando la unidad esta acreditada.

| Carril propuesto | Referente |
|---|---|
| Contratista | Participante que presenta la solicitud; incluye al residente en su organizacion |
| Supervisor o inspector de obra, segun modalidad | Responsabilidad alternativa de control de obra |
| OACGD — Registro documentario | Oficina de Atencion al Ciudadano y Gestion Documental |
| SGGOS — Coordinador de obra | Sub Gerencia de Gestion de Obras y Supervision, coordinador |
| SGGOS — Subgerente de Gestion de Obras y Supervision | Titular de la SGGOS; corresponde al "subgerente de obras" mencionado por el usuario |
| GRI — Gerente Regional de Infraestructura | Gerencia Regional de Infraestructura |
| GRAJ — Asesoria Juridica | Gerencia Regional de Asesoria Juridica |
| Autoridad competente para resolver | Cargo o delegacion concreta pendiente de acreditar |

## Elementos registrados

| Elemento | Contenido | Clase | Fuente |
|---|---|---|---|
| Disparador | Solicitud o causal de ampliacion | Normativo citado | Reglamento, arts. 198 y 200; Directiva, num. 7.3.7 |
| Instancia | Una por solicitud o causal | Decision del equipo | DEC-041 |
| Producto | Resolucion favorable o no favorable comunicada | Propuesta apoyada en observacion del usuario | Aclaracion del usuario, 2026-11-10 |
| Decision | Autoridad competente para resolver mediante resolucion, pendiente de identificar | Propuesta de modelamiento apoyada en observacion del usuario | DEC-041; aclaracion del usuario, 2026-11-10; delegacion concreta pendiente |

## Vacios de evidencia

| Vacio | Marca | Fuente o accion necesaria |
|---|---|---|
| Dueno, delegacion y contraste documental del circuito interno | `EVIDENCIA-INSUFICIENTE` | ROF complementado con delegaciones, procedimiento vigente y muestra no sensible del SGD |
| Soporte especializado para la evaluacion de ruta critica, si corresponde | `EVIDENCIA-INSUFICIENTE` | Asignacion funcional y validacion operativa; no se presupone un carril independiente |
| Criterios para controles presupuestal y juridico | `EVIDENCIA-INSUFICIENTE` | Matriz institucional por regimen |
| Plazos internos, documentos concretos, configuracion del SGD y notificacion | `EVIDENCIA-INSUFICIENTE` | Procedimiento y muestras no sensibles; el uso general del SGD fue comunicado por el usuario |
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
| Circuito interno y SGD | `ELABORACION` | 2026-11-10 | Propuesta ajustada con observacion del usuario; pendiente contraste operativo y competencia decisoria | Usuario y asistencia de IA | Observacion y aclaracion del usuario, 2026-11-10 |
| Proyecto y emision de resolucion | `ELABORACION` | 2026-11-10 | GRAJ proyecta la resolucion y la autoridad competente resuelve mediante ella; pendiente acreditar cargo y delegacion | Usuario y asistencia de IA | Aclaracion del usuario, 2026-11-10 |

## Relaciones

- [Sustento de S4.3.2.3](../S4-3-2-3-gestion-modificaciones-alcance/S4-3-2-3-sustento.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)

## Cambio de perfil de trazado ? 2026-11-06

Por indicacion del usuario se adopta `zigzag-controlado` para este subproceso. El cambio afecta la disposicion grafica; conserva actividades, participantes, secuencias y mensajes. Los registros anteriores de geometria corresponden a sus respectivas generaciones. Se regeneran los derivados mediante la tabla; no se realiza revision visual ni se atribuye conformidad institucional.

Resultado de los controles de esta generacion: D1, D2, D3 y D5 sin hallazgos. D4 registra 1 hallazgos geometricos (superposicion entre las etiquetas Opinion del responsable del control de obra y Solicitud y opinion). Se adopta el derivado de trabajo con `--forzar` para aplicar el perfil solicitado, sin cambiar el contenido del proceso. Estos hallazgos quedan pendientes de ajuste de disposicion y revision visual antes de una linea base; la exportacion no implica que el trazado este libre de defectos.

## Mejora del perfil zigzag-controlado ? 2026-11-06

Por solicitud del usuario se aplica la mejora general del perfil: compactacion de circuitos independientes y seleccion de corredores de mensajes con control de interferencias. Se conserva la semantica BPMN; no cambian actividades, responsables ni relaciones del proceso. D1, D2, D3 y D5 sin hallazgos. D4 conserva 1 hallazgos, del mismo tipo que los documentados en la generacion anterior; se mantiene la adopcion como derivado de trabajo con `--forzar`, con ajuste geometrico y revision visual pendientes.

## Control de la revision del 2026-11-10

La generacion focalizada de la tabla actual produjo BPMN, SVG, PNG y HTML sin usar `--forzar`. D1 (esquema), D2 (referencias), D3 (bloqueos), D4 (trazado) y D5 (notacion) no registran hallazgos. Se eliminaron de la vista objetos de datos redundantes que cruzaban etiquetas y un almacen de datos repetido junto a la transicion GRAJ-decisor; el registro en Cuaderno, la opinion del supervisor o inspector y la derivacion por SGD permanecen expresados en las actividades, mensajes y sustento. Los derivados se generaron con Chrome por un fallo local del proceso grafico de Edge en el primer intento. No se ha realizado revision visual ni se atribuye conformidad institucional.

La aclaracion posterior del usuario se incorporo en este mismo proceso: GRAJ emite opinion legal, proyecta la resolucion y deriva el expediente por SGD; la autoridad competente resuelve mediante resolucion tanto en la ruta favorable como en la no favorable. La generacion focalizada posterior actualizo BPMN, SVG, PNG y HTML sin `--forzar`. D1, D2, D3, D4 y D5 permanecen sin hallazgos. La identidad y delegacion de la autoridad competente siguen con `EVIDENCIA-INSUFICIENTE`; no se ha realizado revision visual ni se atribuye conformidad institucional.
