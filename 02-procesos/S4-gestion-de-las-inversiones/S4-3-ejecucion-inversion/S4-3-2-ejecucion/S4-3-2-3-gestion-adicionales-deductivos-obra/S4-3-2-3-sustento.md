---
id: AP-S4-3-2-3-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S4.3.2.3
nivel_proceso: 3
proceso:
  - S4.3.2.3
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-18
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-3
---

# S4.3.2.3 Gestion de adicionales y deductivos de obra - Sustento

Sube a: [S4.3.2.3 Gestion de adicionales y deductivos de obra](00-S4-3-2-3-gestion-adicionales-deductivos-obra.md)

## Alcance vigente

DEC-047 divide este proceso: S4.3.2.3 conserva adicionales, deductivos puros y adicionales con deductivos vinculantes; reducciones y mayores metrados pasan a S4.3.2.7 y S4.3.2.8. La seccion final documenta la division y sus limites. Los apartados DEC-041 y DEC-046 siguientes son antecedentes, no la arquitectura vigente.

## Antecedente del realineamiento DEC-041

`DEC-041` limita este proceso a adicional o modificacion tecnica, reduccion o deductivo y mayores metrados o cantidades. Las variantes de plazo del modelo anterior se trasladan, con su trazabilidad, a S4.3.2.4, S4.3.2.5 y S4.3.2.6. No se crean codigos de nivel 4.

El circuito conserva la segregacion adoptada por `DEC-038`: necesidad en campo, clasificacion inicial, elaboracion, revision tecnica independiente, controles complementarios, consolidacion y decision. La denominacion anterior del rol de gestion se retira y se usa **SGGOS — Coordinador de obra**. El **Monitor del Cuaderno de Incidencias** solo seria pertinente si se modelara el acceso o visualizacion del sistema, lo que no ocurre en este flujo.

## Definicion institucional de terminologia

Por decision del equipo (`DEC-041`), los modelos usan de manera uniforme **Cuaderno de Incidencias**, incluida administracion directa. Esta es una definicion institucional de estandarizacion terminologica y no altera las citas: la Directiva 017-2023-CG emplea "cuaderno de obra". Cuando se transcribe literalmente una fuente, prevalece su denominacion original.

`DEC-042` ubica al residente dentro del Ejecutor de obra. Control de obra conserva en este modelo un pool funcional porque supervisor contratado e inspector realizan la misma etapa alternativa con control propio; la etiqueta no afirma que pertenezcan a una misma organizacion ni que actuen simultaneamente. La funcion Elaboracion del expediente tecnico permanece separada solo para mostrar su intercambio; su adscripcion al ejecutor, al GORE o a un tercero es `EVIDENCIA-INSUFICIENTE` y debe reubicarse cuando se confirme.

## Fuentes utilizadas

| ID o fuente | Ubicacion precisa | Consulta y vigencia | Clase y uso |
|---|---|---|---|
| Ley 32069 consolidada | Arts. 63-64, PDF pp. 30-31 | Consulta 2026-11-04; texto consolidado con modificaciones hasta 2026-07-19 | `EXIGENCIA-NORMATIVA` propuesta: tipos de modificacion, autoridades y umbrales |
| Reglamento de la Ley 32069 | Arts. 109, 186, 188 y 194-197, PDF pp. 59-60 y 101-112 | Consulta 2026-11-04; texto consolidado al 2026-01-09 | `EXIGENCIA-NORMATIVA` propuesta: supervisor o inspector, Cuaderno de Incidencias, reduccion, adicionales y mayores metrados |
| Directiva 017-2023-CG/GMPL | Nums. 6.8.2-6.8.3, 7.3.2 y 7.3.6, PDF pp. 9-10, 14 y 17 | Consulta 2026-11-04; vigencia material y modificatorias pendientes de validacion especializada | `EXIGENCIA-NORMATIVA` propuesta para administracion directa; la fuente usa "cuaderno de obra" |
| Directiva 017-2025-OECE-CD | Num. 10.3 C, PDF pp. 6-8 | Consulta 2026-11-04; vigente desde 2025-10-12 segun fuente oficial ya citada | `EXIGENCIA-NORMATIVA` propuesta: el Monitor del Cuaderno de Incidencias visualiza informacion; no se lo usa como coordinador |
| ROF del Gobierno Regional Huanuco | Arts. 20, 44-45, 51 y 92-98 | Consulta 2026-11-04; publicacion efectiva y modificatorias posteriores pendientes de control | `EXIGENCIA-NORMATIVA` propuesta para competencias; `INFERENCIA` para el circuito interno |
| Directiva General de Invierte.pe | Art. 33.2; regla `REG-INV-EJEC-004` | Fuente ya registrada; estado de validacion no modificado | Registro de modificaciones durante la ejecucion fisica cuando corresponda |
| Exportacion Bizagi de Consultas | Ramas de adicional y reduccion del archivo observado | Observada 2026-11-04; no es linea base | `EVIDENCIA-OBSERVADA` para actividades y documentos que requieren contraste |
| `DEC-037`, `DEC-038`, `DEC-041` y `DEC-042` | [Registro de decisiones](../../../../../00-gobernanza/registro-decisiones.md) | Vigentes en el proyecto | Roles comunes de obra, pertenencia de participantes, segregacion de controles y nuevo alcance y codificacion |

Las reglas normativas de esta nota son propuestas de conocimiento preparadas por IA. No tienen estado `VALIDADO` ni acreditan conformidad institucional.

## Distribucion del contenido anterior

| Contenido del modelo anterior | Ubicacion vigente | Tratamiento |
|---|---|---|
| `MOD-ALC-ADI`, `MOD-ALC-RED`, `MOD-ALC-MAY` | S4.3.2.3 | Variantes internas sin nivel 4 |
| `MOD-PLA-AMP` | S4.3.2.4 | Proceso separado para ampliaciones de plazo |
| Suspension contractual y reinicio posterior | S4.3.2.5 | Ciclo de formalizacion de suspension y reanudacion del plazo suspendido |
| Paralizacion y reinicio | S4.3.2.6 | Proceso separado por causal y cierre propios |
| Intensificacion del programa | Sin asignacion definitiva | `EVIDENCIA-INSUFICIENTE`; no se incorpora por inferencia a ninguno de los seis procesos |

## Responsabilidades separadas

| Control | Pregunta principal | Clase |
|---|---|---|
| Control de obra, mediante supervisor contratado o inspector de la entidad segun modalidad | ¿La necesidad existe en campo y afecta la ejecucion? | Exigencia normativa propuesta y evidencia operativa |
| SGGOS — Coordinador de obra | ¿El expediente esta integro y cual es la clasificacion inicial del alcance original, la causal y la figura? | Decision del equipo; no incluye juicio tecnico especializado |
| Elaborador | ¿Como se resuelve tecnicamente la necesidad ratificada? | Exigencia normativa propuesta segun figura |
| Especialista tecnico competente | ¿La solucion es necesaria, compatible, suficiente y conforme a la especialidad? | Propuesta de control independiente basada en `DEC-038` |
| Control contractual y de costos | ¿La prestacion estaba incluida y los metrados, precios y acumulados son consistentes? | Propuesta institucional basada en fuentes citadas |
| Presupuesto y GRAJ | ¿Corresponden controles presupuestales o legales? | Condicional; criterios exactos pendientes |
| Titular de la competencia o autoridad delegada | ¿Corresponde adoptar el acto dentro de su competencia? | Carril estable; delegacion concreta pendiente |

## Vacios y preguntas para validacion

| Vacio | Marca | Evidencia o decision necesaria |
|---|---|---|
| Delegaciones vigentes por figura | `EVIDENCIA-INSUFICIENTE` | Resolucion o acto de delegacion vigente |
| Unidad que remite formalmente a Contraloria | `EVIDENCIA-INSUFICIENTE` | Procedimiento interno y validacion de las unidades involucradas |
| Criterios para activar SGE, Presupuesto y GRAJ | `EVIDENCIA-INSUFICIENTE` | Matriz institucional validada |
| Responsable de control contractual y de costos | `EVIDENCIA-INSUFICIENTE` | Perfiles, asignacion funcional y lista de verificacion |
| Mecanismo para obtener especialista independiente | `EVIDENCIA-INSUFICIENTE` | Definir encargo, apoyo o contratacion y requisitos de independencia |
| Registro en Banco de Inversiones frente a mayores metrados | `DISCREPANCIA-PENDIENTE` | Criterio de Invierte.pe y practica institucional documentada |
| Interfaz con abastecimiento en administracion directa | `EVIDENCIA-INSUFICIENTE` | Definir salida y documentos sin incorporar la adquisicion dentro del proceso |
| Formularios, plazos internos y medio de notificacion | `EVIDENCIA-INSUFICIENTE` | Procedimientos y validacion operativa |

## Decisiones de visualizacion

El modelo realineado vuelve al perfil predeterminado porque la reduccion a variantes de alcance ya no requiere el pliegue amplio del modelo anterior. La generacion focalizada del 2026-11-05 deja D1, D2, D3 y D5 sin hallazgos. D4 registra diez advertencias exclusivamente geometricas: un mensaje atraviesa el fin "Necesidad no ratificada"; los dos mensajes con Contraloria atraviesan los pools Ejecutor de obra y Control de obra; y cuatro pares de etiquetas se montan (conformidad tecnica/observaciones, solicitud/anotacion, necesidad ratificada/no ratificada y condiciones P/J). Se adopta el derivado de trabajo con `--forzar` porque el informe no identifica bloqueos, referencias rotas ni notacion invalida. Queda pendiente revision visual humana y ajuste BPMN-DI antes de una linea base; no se modifica el generador en esta tarea.

## Informacion BIM

`EVIDENCIA-INSUFICIENTE`. No se asignan requisitos BIM sin fuente y validacion especificas.

## Historial de revision

| Documento | Nivel | Fecha | Resultado | Rol o unidad | Evidencia |
|---|---|---|---|---|---|
| Juego inicial S4.3.2.3 | `ELABORACION` | 2026-11-03 | Propuesta creada | Equipo del proyecto con asistencia de IA | `DEC-032`; Bizagi; catalogo de eventos |
| Segregacion de elaboracion y controles | `ELABORACION` | 2026-11-04 | Responsabilidades separadas; pendiente validacion | Propuesta IA basada en fuentes y precisiones del equipo | `DEC-038` |
| Realineamiento a modificaciones de alcance | `ELABORACION` | 2026-11-05 | Variantes de plazo trasladadas a S4.3.2.4-.6; pendiente revision | Equipo del proyecto con asistencia de IA | `DEC-041` |
| Precision de participantes | `ELABORACION` | 2026-11-05 | Residente integrado en Ejecutor de obra; control de obra y adscripcion del elaborador explicitados | Equipo del proyecto con asistencia de IA | `DEC-042` |

## Relaciones

- [S4.3.2.4 Gestion de ampliaciones de plazo](../S4-3-2-4-gestion-ampliaciones-plazo/00-S4-3-2-4-gestion-ampliaciones-plazo.md)
- [S4.3.2.5 Formalizacion de suspensiones de plazo](../S4-3-2-5-formalizacion-suspensiones-plazo/00-S4-3-2-5-formalizacion-suspensiones-plazo.md)
- [S4.3.2.6 Gestion de paralizacion y reinicio](../S4-3-2-6-gestion-paralizacion-reinicio/00-S4-3-2-6-gestion-paralizacion-reinicio.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)
- [Guia del Reglamento de la Ley 32069](../../../../../03-conocimiento/fuentes/guia-reglamento-ley-32069.md)
- [Guia del ROF del Gobierno Regional Huanuco](../../../../../03-conocimiento/fuentes/guia-rof-grh-2023.md)

## Cambio de perfil de trazado ? 2026-11-06

Por indicacion del usuario se adopta `zigzag-controlado` para este subproceso. El cambio afecta la disposicion grafica; conserva actividades, participantes, secuencias y mensajes. Los registros anteriores de geometria corresponden a sus respectivas generaciones. Se regeneran los derivados mediante la tabla; no se realiza revision visual ni se atribuye conformidad institucional.

Resultado de los controles de esta generacion: D1, D2, D3 y D5 sin hallazgos. D4 registra 18 hallazgos geometricos (superposiciones de flujos y etiquetas y cruces de flujos con etiquetas). Se adopta el derivado de trabajo con `--forzar` para aplicar el perfil solicitado, sin cambiar el contenido del proceso. Estos hallazgos quedan pendientes de ajuste de disposicion y revision visual antes de una linea base; la exportacion no implica que el trazado este libre de defectos.

## Mejora del perfil zigzag-controlado ? 2026-11-06

Por solicitud del usuario se aplica la mejora general del perfil: compactacion de circuitos independientes y seleccion de corredores de mensajes con control de interferencias. Se conserva la semantica BPMN; no cambian actividades, responsables ni relaciones del proceso. D1, D2, D3 y D5 sin hallazgos. D4 conserva 18 hallazgos, del mismo tipo que los documentados en la generacion anterior; se mantiene la adopcion como derivado de trabajo con `--forzar`, con ajuste geometrico y revision visual pendientes.

## Convencion de carriles y SGD

Se aplica la [convencion de carriles y SGD](../../../../../00-gobernanza/estandar-artefactos-modelamiento.md#74-convencion-de-carriles-y-sgd-en-s432) de `DEC-043`. El pool funcional antes titulado Control de obra se muestra como Supervisor o inspector de obra, segun modalidad, sin afirmar identidad organizacional ni concurrencia. OACGD y GRAJ usan las etiquetas uniformes. El registro y la derivacion inicial a SGGOS se modelan con tarea de usuario y `almacen: SGD`. No se presume el medio de las comunicaciones externas ni de otros registros. El pool Ejecutor de obra, segun regimen es una abstraccion provisional de las rutas de contrata y administracion directa.

La generacion focalizada de esta normalizacion deja D1, D2, D3 y D5 sin hallazgos. D4 registra 18 hallazgos geometricos en el circuito de autorizacion y convergencia (flujos compartidos, etiquetas montadas y cruces con etiquetas); no afectan las referencias ni la terminacion. Se adoptaron BPMN, SVG, PNG y HTML de trabajo con `--forzar`, con revision visual y ajuste de disposicion pendientes antes de una linea base. No se atribuye conformidad institucional.

## Replanteamiento del circuito de alcance - 2026-11-18

**Resultado propuesto:** se conservan codigo, carpeta y variantes de `DEC-041`, pero se deja de imponer un circuito unico. El adicional incorpora su presupuesto deductivo vinculado; la reduccion independiente tiene su propio control de procedencia; los mayores metrados se autorizan en obra y se enlazan con valorizacion. `DEC-046` registra esta precision. No se crean procesos nuevos ni se presume aceptada su futura separacion.

### Paquete de contexto del lote

- Fase: conceptual. Objetivo: corregir la secuencia consulta-elaboracion-evaluacion-decision y distinguir las figuras.
- Fuentes textuales activas: indice, ficha, tabla y sustento S4.3.2.3; secciones de interfaz de S4.3.2.2; guia CON-001; articulos 105.3, 109, 190, 194, 196 y 197 del Reglamento y art. 64 de la Ley; decisiones DEC-038, DEC-041 a DEC-044.
- Evidencia observada: instruccion del usuario del 2026-11-18 sobre consulta previa y plazos; no se aportaron bases ni expediente de un contrato concreto.
- Glosario: consulta absuelta, encargo de elaboracion, expediente del adicional, opinion de supervision y resolucion aprobatoria son objetos distintos. Deductivo vinculado no se usa como sinonimo de reduccion independiente. Reduccion de metas es una denominacion operativa cuya correspondencia contractual debe acreditarse.
- Reglas validadas incorporadas: ninguna. Conocimiento normativo en propuesta, pendiente de validacion humana y aplicabilidad contractual.
- Archivos modificables: juego textual S4.3.2.3, registro de decisiones y estado del proyecto; derivados mediante generacion focalizada.
- Derivados excluidos del contexto: BPMN XML, SVG, PNG y HTML. Revision visual no requerida en este lote; pendiente al estabilizar contenido. Modificacion de herramientas no autorizada.
- Limites: detalle ordinario de solo construccion bajo Ley 32069. Otros sistemas, regimen anterior, administracion directa y emergencia conservan su pertenencia al proceso, pero se cierran como ruta pendiente de especificacion; no se les aplican los plazos de este lote por analogia.

### Evidencia y contraste normativo

**EVIDENCIA-OBSERVADA:** el usuario describe la consulta de obra como antecedente para adicional, deductivo y adicional-deductivo vinculante, seguida de autorizacion de elaboracion, 15 dias de elaboracion, 10 de supervision y tramite de aprobacion. Se incorpora la consulta como interfaz operativa con S4.3.2.2; la respuesta y la carta ya modeladas alli se reciben sin volver a tramitar la consulta completa. Confirmar el encargo no supone emitir una segunda autorizacion.

**EXIGENCIA-NORMATIVA propuesta:** el hito inicial de los 15 dias es la anotacion, no una carta posterior. El art. 194 no establece que toda necesidad de adicional deba tener una consulta independiente previa; esa secuencia se conserva como evidencia operativa del usuario y debe compatibilizarse con los plazos. La precision posterior de este lote recibe la respuesta antes de la anotacion y conserva el origen alternativo del art. 194; no impone una consulta a toda necesidad ni reinicia un computo ya iniciado.

Fuentes oficiales consultadas el **2026-11-18**:

| Fuente | Ubicacion precisa | Vigencia y uso |
|---|---|---|
| [Ley y Reglamento actualizados, El Peruano](https://diariooficial.elperuano.pe/Normas/obtenerDocumento?idNorma=25) | Ley art. 64.2-64.4, PDF p. 28; Reglamento art. 109.1-109.3, p. 95; art. 194.1-194.5, pp. 121-122; art. 197.1-197.4, p. 123 | Edicion oficial actualizada al 21-10-2026. Consulta del texto disponible; aplicabilidad y modificatorias posteriores pendientes de control especializado. Se corroboran plazos, roles y diferencia entre figuras; no se declara regla validada. |
| [Reglamento consolidado OECE](https://cdn.www.gob.pe/uploads/document/file/9295551/6444155-ref-reglamento-de-la-ley-de-contrataciones-del-estado-con-modificaciones-posteriores-hasta-08-ene-2026-2-v2.pdf?v=1768513235) | Art. 105.3; art. 109, p. 60; arts. 194-197, pp. 108-112; referencia local CON-001 en la guia enlazada | Consolidado al 09-01-2026, contrastado con la edicion de El Peruano. Dias calendario salvo indicacion expresa de habiles. |
| [DS 001-2026-EF, El Peruano](https://busquedas.elperuano.pe/dispositivo/NL/2474920-3) | Art. 2, modificacion del numeral 194.3; disposicion de vigencia | Modifica publicacion y prohibicion de regularizacion; no sustituye 194.2 d-g. Vigencia desde 14-01-2026 segun compendio OECE ya registrado en la guia CON-001. |

### Condiciones y computo que conserva la tabla

| Tramo | Regla propuesta y condicion | Representacion |
|---|---|---|
| Necesidad | Art. 194.1: adicional indispensable por deficiencias del expediente o causas no previsibles no imputables al contratista. Art. 194.2 a-b: anotacion e informe del supervisor en 5 dias desde el dia siguiente de aquella | Control de causal y antecedentes antes de encargar; no basta una carta favorable |
| Elaborador | Art. 194.2 c: las bases determinan entidad, contratista o supervisor | Se comprueban las bases; no se asigna automaticamente al contratista |
| Elaboracion | Art. 194.2 d: 15 dias calendario desde el dia siguiente de la anotacion, con necesidad ratificada. El plazo adicional por complejidad, permisos, autorizaciones o sofisticacion tecnica exige otorgamiento de la entidad; no es automatico | Caja 49 muestra plazo e hito; encargo o subsanacion no reinician el computo |
| Supervision | Art. 194.2 e: 10 dias calendario desde el dia siguiente de la presentacion cuando elaboro el contratista | Rama especifica, cajas 63-65; si elaboro el supervisor, no se impone una revision de su propio expediente por otros 10 dias |
| Opinion institucional | Art. 194.2 g: opinion del organo competente o del proyectista bajo la condicion temporal prevista, dentro del plazo del literal e | Control institucional concurrente cuando elaboro el contratista; SGE es la propuesta organizativa conservada de DEC-038, sin inventar adscripciones |
| Decision | Art. 194.2 f: notificacion en 12 dias habiles desde el dia siguiente de recibir opinion del supervisor o expediente elaborado por este, segun corresponda | Plazo total institucional, no 12 dias adicionales por cada revision. Incluye tramitacion y notificacion. Interaccion del computo con autorizacion CGR requiere precision especializada |
| Elaboracion por entidad | Opinion D000092, 2.9 C y 3.11: presentacion a supervision, opinion y decision de entidad; proyectista cuando corresponde | Ruta incorporada; se precisa el computo de decision. La opinion no explicita en ese apartado un numero autonomo de dias para supervision: precision pendiente |

El modelo representa un caso ordinario. No habilita regularizacion de adicionales; la emergencia del art. 194.4 requiere su ruta especifica. Autoridades, delegaciones, controles presupuestales y participacion legal deben verificarse por caso. Los umbrales de la Ley se comprueban antes de remitir a la autoridad; no se presume que el coordinador puede aprobar.

### Diferencias entre tramites y posible separacion

| Figura | Tratamiento en esta propuesta | ¿Comparte 15 + 10 dias? | Recomendacion de arquitectura |
|---|---|---|---|
| Adicional sin deductivo vinculado | Consulta como antecedente operativo, necesidad ratificada, elaboracion, opiniones y decision | Solo bajo las condiciones de 194.2 d-e; no son 25 dias desde la carta | Conservar como nucleo de S4.3.2.3 |
| Adicional con deductivo vinculado | Un expediente que identifica y sustenta ambas partes y el efecto neto aplicable; verificar vinculo, no solo restar importes | Sigue el tramite del adicional | Mantener junto al adicional; separarlo fragmentaria su evaluacion |
| Deductivo independiente o reduccion de metas | Determinar si corresponde a reduccion de prestaciones del art. 109. No basta la denominacion; requiere sustento del area usuaria, finalidad preservada, prestaciones no ejecutadas, divisibles y cuantificables, opinion de supervision cuando corresponda, limite del 25 % y oportunidad anterior a recepcion | No se trasladan los plazos del art. 194 | Candidato a proceso propio de reducciones; por ahora rama interna. Efecto sobre plazo se decide en la misma resolucion, art. 109.2 |
| Mayores metrados | Precios unitarios y supuesto art. 197: solicitud y autorizacion en cuaderno, control de acumulados, ejecucion y sustento para valorizacion; el pago requiere autorizacion de la autoridad de gestion administrativa | No | Es el candidato mas claro a proceso separado, enlazado con valorizaciones/control periodico; no necesita aprobacion previa de ejecucion por la entidad |

**INFERENCIA de modelamiento:** el deductivo vinculado se mantiene unido al adicional porque incide en su presupuesto y umbral (Ley, art. 64.2-64.3). El termino coloquial «adicional deductivo vinculante» no se convierte en un quinto procedimiento autonomo. La vinculacion concreta requiere evidencia tecnica y contractual.

**PROPUESTA pendiente de decision:** separar posteriormente Gestion de adicionales y deductivos vinculados, Gestion de reducciones de prestaciones y Gestion de mayores metrados como hijos directos de S4.3.2, sin nivel 4. No se asignan codigos, no se renombra el padre ni se retiran variantes durante este lote. Antes de adoptar esa arquitectura deben definirse producto, dueno e interfaces, actualizar DEC-041 y regenerar el padre. S4.3.2.2 conservaria su salida de consulta; S4.3.2.1 debe recibir el sustento para valorizacion y distinguir autorizacion de pago; S4.3.2.4 solo interviene ante una solicitud de ampliacion aplicable, no automaticamente por toda modificacion.

### Pendientes de este lote

- Bases, regimen temporal y sistema de entrega del contrato concreto: EVIDENCIA-INSUFICIENTE.
- Acto de encargo y adscripcion del elaborador: EVIDENCIA-INSUFICIENTE. Ruta de elaboracion por entidad precisada mediante CON-010; plazo numerico de supervision en esa variante pendiente de validacion.
- Precisar con el equipo si «deductivo» se usa para sustitucion vinculada, reduccion independiente u otro ajuste; no inferir equivalencia.
- Subsanaciones y efectos sobre computos, autorizacion CGR y controles presupuestales de cada supuesto: pendientes de desarrollo especializado; no se inventan suspensiones ni reinicios de plazo.
- Desarrollo detallado de administracion directa, otros sistemas y emergencia, y decision de separar procesos: pendientes; el cierre de ruta pendiente no equivale a denegacion.
- La autorizacion de pago de mayores metrados queda como requisito explicito de la interfaz con valorizacion; no se representa como aprobacion previa de su ejecucion.

### Incorporacion de opiniones OECE y ajuste de entrada

El usuario aporta la Opinion D000092-2026-OECE-DTN y precisa que la respuesta de la consulta precede a la anotacion de necesidad. Se incorpora el PDF oficial como **CON-010**, junto con **CON-011 / Opinion D000083-2026-OECE-DTN**, que fundamenta la independencia entre consultas y adicionales. Consulta: 2026-11-18; archivos, fuentes oficiales, SHA-256, vigencia, paginas y reglas BORRADOR-IA en las [guia D000092](../../../../../03-conocimiento/fuentes/guia-opinion-d000092-2026-oece-dtn.md) y [guia D000083](../../../../../03-conocimiento/fuentes/guia-opinion-d000083-2026-oece-dtn.md). Estas guias amplian el paquete textual del lote; no se cargan derivados del modelo ni se modifican herramientas.

**Cambio aplicado:** S4.3.2.2 entrega su respuesta al ejecutor como antecedente. La caja 2 anota la necesidad especifica del adicional; el dia siguiente inicia los computos de 5 y 15 dias. La anotacion se comunica a supervision y elaborador: el trabajo de elaboracion puede transcurrir mientras se tramita la ratificacion. La caja 76 exige recibir esta antes de presentar el expediente. No se suman 5 dias mas 15 ni se cuentan estos desde la carta de respuesta.

**Precision sobre la expresion del usuario:** «aprobacion de la necesidad como respuesta a la consulta» se registra como respuesta tecnica que motiva iniciar el adicional. No se atribuye a esa respuesta la ratificacion del supervisor del art. 194.2 b ni la aprobacion del expediente mediante resolucion. Tampoco se ordena repetir una anotacion de necesidad ya valida: su fecha original sigue rigiendo. El escenario encadenado consulta-anotacion es aplicable cuando la respuesta revela esa necesidad; la Opinion D000083 no vuelve obligatoria la consulta previa en todos los casos.

**Otros ajustes derivados de CON-010:** se incorpora la ruta de elaboracion por entidad; se prioriza la opinion del proyectista bajo el supuesto temporal y, en defecto, del organo competente, incluido el supuesto inoficioso del numeral 2.8. La opinion institucional corre junto con supervision cuando elabora contratista (2.9 A). La opinion desfavorable se integra para que la entidad resuelva; no se cierra el expediente solo con un informe tecnico. Los deductivos vinculados se consideran en la incidencia neta y las reducciones independientes no se descuentan de ella (2.10 y 3.12-3.13). La notificacion requiere verificar el canal vigente, pues la situacion de SEACE descrita por la opinion es temporal (2.11).

**Trazabilidad de numeracion:** se conservan los numeros anteriores; se retira el fin tecnico 31 porque la opinion no sustituye la decision. Los numeros de pasos intermedios retirados de esta misma iteracion no se reutilizan. No cambia la arquitectura de seis procesos ni se atribuye aprobacion o validacion.

### Control del lote con opiniones OECE

D1, D2, D3 y D5 sin hallazgos: esquema valido, referencias consistentes y escenarios sin bloqueos. D4 informa 80 interferencias geometricas: T1=16, T2=22, T3=3, T4=32 y T6=5; afectan anotaciones, intercambios con elaborador, proyectista y Contraloria y convergencias. Se regeneran los derivados de trabajo con --forzar exclusivamente para mantenerlos sincronizados con la fuente conceptual, no como trazado listo para publicar. El informe reproducible queda en 99-temporal/modelos/S4-3-2-3-diagrama-proceso/validacion.txt. Se requiere ajuste de disposicion y revision visual antes de linea base; no se modificaron herramientas ni se atribuye conformidad.

Comprobacion de cierre 2026-11-18: construir_modelos.py --check correcto para todos los modelos; gestionar_etiquetas.py revisar: 174 notas, 0 problemas. Integridad SHA-256 de CON-010 y CON-011 comprobada; enlaces locales de ambas guias sin roturas; 36 reglas con identificadores unicos. Estos controles no eliminan los hallazgos geometricos D4 ni validan las reglas.

## Division adoptada para el modelo de trabajo - DEC-047

Esta seccion sustituye la recomendacion pendiente de separacion del lote DEC-046. Por instruccion del usuario del 2026-11-18, S4.3.2.3 se denomina Gestion de adicionales y deductivos de obra y comprende tres casos: adicional, deductivo puro y adicional con deductivo vinculante. La ruta estable se conserva; las nuevas carpetas corresponden a procesos hermanos, no a copias de estado.

Reducciones se trasladan a [S4.3.2.7](../S4-3-2-7-gestion-reducciones-prestaciones/00-S4-3-2-7-gestion-reducciones-prestaciones.md); mayores metrados a [S4.3.2.8](../S4-3-2-8-gestion-mayores-metrados/00-S4-3-2-8-gestion-mayores-metrados.md). Los tres aparecen como cajas independientes en S4.3.2. No hay nivel 4 ni cadena obligatoria entre ellos.

**Evidencia observada:** el usuario distingue deductivo puro de reduccion de metas. **EVIDENCIA-INSUFICIENTE:** no se aporto aun el supuesto tecnico-contractual que acredita una ruta autonoma del deductivo puro. **Propuesta:** entrada propia, clasificacion y remision a S4.3.2.7 si es reduccion de prestaciones; de lo contrario el detalle queda pendiente. No se exige ratificacion ni se aplican 15/10 dias del adicional por analogia. La respuesta de consulta puede integrar sus antecedentes; no equivale a un expediente aprobado.

La caja 7 es convergencia exclusiva de dos origenes alternativos (residente y supervision). Se conserva con anotacion aclaratoria; no decide, aprueba ni sincroniza ambos origenes. Ahora conecta directamente con caja 8. Se retiran los numeros 21, 22, 23, 51, 56, 57 y 66-75; no se reutilizan. Las nuevas cajas 82-86 identifican y clasifican los casos de deductivo puro y adicional vinculado. Los nuevos procesos tienen numeracion local propia.

Paquete conceptual: ficha, indice, tabla y sustento de S4.3.2 y .3, nuevos .7/.8, fuentes ya citadas y plantillas NT. Se mantienen limites normativos del lote anterior. Derivados excluidos del contexto, revision visual diferida, herramientas sin cambios. No existen conformidades institucionales nuevas.

## Control tecnico de la division

D1, D2 y D5 sin hallazgos. D4: 93 hallazgos geometricos (T1=19, T2=27, T3=3, T4=29, T5=1, T6=10). D3 reporta acumulacion en seis escenarios. Se comprobo que el grafo combinado de secuencias y mensajes entre nodos es aciclico. El simulador simplificado convierte mensajes en flujos de tokens y consume cada entrada de eventos de recepcion e inclusivas por separado (_validar_bpmn.py, grafo y juego_tokens); no modela la espera correlacionada del mensaje ni la reunion inclusiva. Al restaurar la continuidad de la tabla Mensajes, antes cortada por una linea vacia, estos intercambios pasan a ser evaluados. El aviso de ciclo/acumulacion no prueba un ciclo real; se mantiene como limitacion pendiente de contraste BPMN especializado, sin alterar ni omitir mensajes para silenciarlo. No se modifican herramientas ni se declara D3 conforme. Se adoptan derivados de trabajo con --forzar para sincronizar la propuesta conceptual; no constituyen una linea base lista para publicacion. Revision visual y cierre de hallazgos pendientes. Informe reproducible: 99-temporal/modelos/S4-3-2-3-diagrama-proceso/validacion.txt.


Precision de DEC-047, 2026-11-18: por indicacion expresa del usuario se renombra la carpeta y su nota indice a `S4-3-2-3-gestion-adicionales-deductivos-obra`. Esta precision sustituye la conservacion de la ruta anterior indicada en el lote inicial. Se actualizan los enlaces; el codigo S4.3.2.3 y el contenido del flujo se conservan.

## Compactacion visual - DEC-048

Paquete de contexto: fase de disposicion visual, tabla y sustento S4.3.2.3, generador y pruebas de trazado; BPMN-DI y PNG autorizados para medir y revisar la geometria. Modificacion de herramientas autorizada por el usuario. Se activa compactacion en zigzag-controlado sin cambiar sus 16 columnas. La suma de alturas de pools baja de 7866 a 4966 unidades (36,9 %), sin cambiar cajas ni anchos de carril. La comparacion usa el mismo contenido y distingue el efecto geometrico de la validacion normativa. No se atribuye conformidad institucional.

Resultado de la primera iteracion: PNG de 5624 x 16966 a 5624 x 11166 pixeles (34,2 % menos altura total). Vista general inspeccionada: carriles de una actividad compactados; persisten recorridos largos y cruces, especialmente en controles y mensajes. Cinco pruebas correctas, con comparacion de ocho hijos; D1, D2 y D5 sin hallazgos; D4 conserva 93 hallazgos (19/27/3/29/1/10 por T1-T6), sin aumento; D3 conserva la limitacion ya documentada. Derivados de trabajo sincronizados con --forzar; no es trazado definitivo ni linea base publicable. Etiquetas: 184 notas, cero problemas.

## Corredores y recolocacion de terminales - DEC-049

Trabajo visual solicitado expresamente por el usuario. Se autoriza lectura de geometria BPMN, PNG y modificacion del generador y sus pruebas; se conserva el paquete textual del lote DEC-048. No se cambia la tabla, los responsables, las conexiones ni los numeros.

Las cajas 45 y 46 se recolocan como cadena terminal en una fila superior del mismo carril, sin reglas particulares por ID. Se corrigen rutas invasivas mediante corredores ortogonales; el origen y destino dejan de estar excluidos de la comprobacion interior y los mensajes rodean pools ajenos.

D1, D2 y D5 sin hallazgos; D3 conserva la limitacion del simulador ya documentada. D4 baja de 93 a 23: T1=0, T2=10, T3=0, T4=8, T5=1, T6=4. Los pendientes corresponden a corredores compartidos, etiquetas sobre anotaciones, una superposicion de anotaciones y cuatro cruces de etiquetas. Se adoptan derivados de trabajo con --forzar para sincronizar el modelo; no es linea base publicable. La reduccion de avisos no constituye validacion normativa ni conformidad institucional.

Revision visual de la vista general regenerada realizada: 45-46 aparecen juntas arriba en el carril del coordinador; el tramo 39-44 rodea las actividades en vez de atravesarlas. PNG actual: 5832 x 10578 pixeles frente a 5624 x 11166 de DEC-048; el margen lateral aumenta para alojar corredores externos. Siete pruebas correctas, incluyendo recorrido alrededor de barreras, rechazo de extremos encerrados, ausencia de penetracion de cajas y conservacion semantica de los ocho hijos. Etiquetas: 184 notas, cero problemas.
