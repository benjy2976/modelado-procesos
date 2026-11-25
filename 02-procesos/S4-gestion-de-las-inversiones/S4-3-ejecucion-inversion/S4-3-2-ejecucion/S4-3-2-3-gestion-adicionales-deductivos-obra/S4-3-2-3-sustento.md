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

El modelo representa la ruta sin emergencia del art. 194.2. No habilita la via excepcional del art. 194.4; esta requiere su ruta especifica. Autoridades, delegaciones, controles presupuestales y participacion legal deben verificarse por caso. Los umbrales de la Ley se comprueban antes de remitir a la autoridad; no se presume que el coordinador puede aprobar.

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

Regeneracion derivada del ajuste visual de `zigzag-controlado` en S4.3.1, 2026-11-18: la tabla y la semantica de S4.3.2.3 no cambian. D4 conserva 23 hallazgos geometricos y D3 mantiene la limitacion del simulador ya documentada; D1, D2 y D5 no registran hallazgos. Se sincronizan BPMN, SVG, PNG y HTML de trabajo con `--forzar`, sin declarar esta vista lista para linea base.

## Recepcion institucional, encargo y secuencia de autorizacion - 2026-11-19

Paquete de contexto: fase conceptual con revision de la tabla y del sustento S4.3.2.3; interfaz textual S4.3.2.2, ROF y edicion oficial de Ley 32069 y Reglamento activas. Los derivados graficos y el BPMN XML se excluyen del analisis conceptual; la generacion focalizada se usa para mantenerlos sincronizados. No se autoriza cambiar el generador en este lote.

**EVIDENCIA-OBSERVADA:** el usuario precisa que el Subgerente de Gestion de Obras y Supervision recibe el sustento y lo deriva al coordinador antes de la caja 14; tambien senala que la comunicacion posterior a la consulta identifica el encargo de elaboracion. La tabla S4.3.2.2, cajas 52-53, ya representa la preparacion y emision de esa carta, condicionada a lo previsto en las bases. Se agrega la recepcion y derivacion SGGOS (caja 87), y se hace visible la asuncion del encargo por el elaborador (caja 88) tras la anotacion. No se modela una segunda autorizacion de elaboracion ni se atribuye al coordinador la potestad de designar a quien las bases no designan. La correspondencia exacta de cargos, proveidos y canales debe contrastarse con un expediente y el SGD de la entidad.

**EXIGENCIA-NORMATIVA propuesta:** [edicion oficial actualizada de Ley 32069 y Reglamento, El Peruano](https://diariooficial.elperuano.pe/Normas/obtenerDocumento?idNorma=25), consultada el **2026-11-19**, actualizada al **21-10-2026**: Reglamento art. 194.2 c-d, PDF pp. 121-122, fija en las bases al elaborador (entidad, contratista o supervisor) y establece la presentacion del expediente en quince dias desde el dia siguiente de la anotacion, con ratificacion de necesidad. Art. 194.2 e-g, pp. 121-122, situa el pronunciamiento de supervision cuando elabora el contratista, la opinion tecnica institucional o del proyectista y la resolucion. Ley art. 64.2-64.4, PDF p. 28, exige autorizacion previa de Contraloria para el adicional mayor de 30 % y hasta 50 %, calculado con el tratamiento legal del deductivo vinculado. La edicion consultada incluye la modificacion del art. 194.3 por DS 001-2026-EF; su aplicabilidad al contrato concreto y eventuales cambios posteriores requieren control especializado.

**INFERENCIA DE SECUENCIA:** la Ley exige autorizacion de Contraloria antes de que el titular autorice la ejecucion y el pago del adicional en ese umbral; no establece que deba obtenerse antes de presentar el expediente tecnico. En la propuesta se solicita despues de contar con expediente, opiniones y controles consolidados, y antes de la resolucion. No se llama «opinion de Contraloria»: el acto de esta rama es una **autorizacion**. El art. 194.2 f fija doce dias habiles para notificar la resolucion desde la opinion de supervision o el expediente elaborado por ella; la interaccion de este plazo con el tramite ante Contraloria permanece `EVIDENCIA-INSUFICIENTE` y requiere criterio juridico especifico, sin presumir suspension.

**PROPUESTA DE MODELAMIENTO:** la caja 52 se denomina ahora «Ley 32069, solo construccion, sin emergencia», porque «caso ordinario» confundia esa separacion con el umbral de Contraloria. La ruta de Contraloria sigue en la caja 38, despues de la presentacion del expediente (cajas 49-50 y 26), las opiniones (cajas 27-29 y 63-65) y el control consolidado (caja 37). El evento de recepcion 26 representa la espera del expediente; el elaborador puede trabajar desde la anotacion mientras llega la ratificacion, pero la caja 76 condiciona su presentacion a que esta haya sido comunicada. La caja 25 comunica la ratificacion y confirma el encargo existente, sin reiniciar los quince dias. La emergencia del art. 194.4 queda identificada para ruta especifica y no se niega por la caja 53 como cuestion de fondo.

Control de este lote: generacion focalizada con `--forzar` y comprobacion global `construir_modelos.py --check` correctas; D1, D2 y D5 sin hallazgos nuevos. D4 conserva 23 advertencias geometricas documentadas. D3 mantiene la limitacion preexistente del simulador de mensajes y compuertas inclusivas, sin que este lote agregue bucles en la tabla. Ocho pruebas del perfil `zigzag-controlado` correctas; `gestionar_etiquetas.py revisar`: 186 notas, cero problemas. Derivados de trabajo, sin validacion normativa ni conformidad institucional.

## Comunicacion al elaborador y salidas locales - 2026-11-19

Paquete de contexto: fase conceptual y revision visual expresamente solicitada; tabla y sustento S4.3.2.3, interfaz textual S4.3.2.2 y guia CON-010 activos. BPMN XML y PNG se usan solo para la geometria; el perfil `zigzag-controlado` ya estaba declarado en la tabla. La modificacion del generador queda limitada a detectar finales compartidos con muchas entradas; no cambia simbolos ni semantica.

**EVIDENCIA-OBSERVADA:** el usuario asigna al subgerente de SGGOS la comunicacion de la caja 17 y pide hacer reconocible al elaborador, el momento de inicio del computo y los avisos de anotacion y evaluacion. Se asigna la caja 17 a ese carril. El pool funcional del elaborador nombra las alternativas del art. 194.2 c —entidad contratante, contratista o supervisor— sin afirmar que concurren: solo una se determina por las bases de cada contrato. Falta un expediente concreto que permita sustituir la alternativa por una oficina, empresa o persona.

**EXIGENCIA-NORMATIVA propuesta:** [Ley 32069 y Reglamento, edicion oficial actualizada al 21-10-2026](https://diariooficial.elperuano.pe/Normas/obtenerDocumento?idNorma=25), consultada el **2026-11-19**: Reglamento art. 194.2 a-d, PDF pp. 121-122, hace partir los quince dias desde el dia siguiente de la anotacion de necesidad en el Cuaderno de Incidencias y atribuye a las bases la eleccion del elaborador. La [Opinion D000092-2026-OECE-DTN](../../../../../03-conocimiento/fuentes/guia-opinion-d000092-2026-oece-dtn.md), nums. 2.1-2.3 y 3.1-3.3, confirma que la respuesta de consulta y la ratificacion no desplazan ese hito; la nota 4 de la p. 2 indica comunicar la ratificacion al contratista u organo elaborador, segun corresponda. La resolucion se notifica conforme al art. 194.2 f; el aviso previo de evaluacion tecnica que se agrega aqui es una **propuesta operativa**, no un plazo o notificacion legal adicional acreditada.

**PROPUESTA DE MODELAMIENTO:** la caja 89 representa que SGGOS conoce la anotacion; la 90 comprueba si el elaborador ya la conoce; la 91 comunica la anotacion y antecedentes solo si hace falta. Si el contratista anoto y elabora, la anotacion conocida evita una segunda notificacion formal. Si anoto la supervision y elabora el contratista, o si elabora un organo de la entidad que aun no conoce el registro, SGGOS comunica. La caja 48 inicia la instancia de elaboracion; la 88 organiza el encargo comunicado segun bases; la 49 elabora durante el plazo que ya corre; la 76 espera la ratificacion para presentar. La caja 25 comunica la ratificacion, no una nueva orden que reinicie los quince dias. La caja 93 comunica el resultado tecnico al ejecutor y al elaborador como informacion previa a la decision, sin atribuirle efecto aprobatorio; canal, destinatario preciso y eventual tramite de observaciones quedan por contrastar.

La primera generacion de este lote revelo que enviar simultaneamente desde la anotacion y desde SGGOS al mismo evento de inicio podia duplicar instancias del elaborador. La fuente final elimina los mensajes directos a la caja 48: SGGOS recibe la anotacion y la compuerta 90 activa una sola alternativa por caso. Si el elaborador aun no la conoce, recibe el mensaje en la caja 48; si ya conoce su propia anotacion, se activa la caja condicional 97. Ambas rutas siguen a la 88 y conservan como unico hito legal la fecha del registro en el cuaderno. La correlacion del caso y la implementacion exacta de esa condicion requieren contraste en un motor BPMN y con la practica institucional; no se declara validacion operacional.

**REVISION VISUAL:** el fin unico 53 recibia cuatro causas distintas desde compuertas separadas por el pliegue del perfil y producia las flechas superpuestas mostradas por el usuario. Un intento de moverlo automaticamente aumento D4 y fue descartado. La fuente BPMN ahora conserva el fin 53 para regimen o emergencia y usa fines locales 94, 95 y 96 para falta de acreditacion inicial, elaborador no acreditado y deductivo puro pendiente de ruta. El perfil incorpora un aviso generico para futuros fines que reciban tres o mas ramas; no fabrica ni duplica finales porque esa distincion pertenece a la fuente maestra. Esta revision del modelo no equivale a conformidad institucional.

Resultado focal: el PNG se reviso en el bloque cuestionado. Las ramas de las cajas 24, 58 y 85 ahora llegan a finales propios y ya no confluyen en la 53. Las anotaciones extensas que se montaban sobre esas flechas se conservan en este sustento y en las fuentes de la tabla, no sobre el dibujo. D1, D2 y D5 sin hallazgos; D4 registra 19 advertencias (8 flujos superpuestos, 9 etiquetas montadas, 1 par de elementos superpuestos y 1 cruce de etiqueta), frente a 23 antes de este lote. D3 conserva advertencias del simulador de mensajes y compuertas inclusivas; los avisos se documentan como pendientes de contraste BPMN especializado y no se declaran validados. El canal de comunicacion de la evaluacion y el tratamiento de observaciones siguen `EVIDENCIA-INSUFICIENTE` para un procedimiento institucional.

Controles de cierre del lote: nueve pruebas de `test_zigzag.py` correctas, incluida la deteccion de un fin compartido; `construir_modelos.py --check` global correcto, `gestionar_etiquetas.py revisar` con 186 notas y cero problemas, y `git diff --check` sin errores de espacio. El test de la cadena terminal 45-46 comprueba alineacion y ausencia de descenso porque, con las nuevas actividades, ya ocupa la fila superior aun sin recolocacion. No se presenta el perfil ni el diagrama como linea base aprobada.

## Hito legal y avisos al elaborador - 2026-11-19

Paquete de contexto: fase conceptual; tabla y sustento S4.3.2.3, guia CON-010 y guia del ROF GRH 2023 activos. Derivados BPMN XML y graficos excluidos de la lectura conceptual; generacion focalizada al cerrar el lote. No se autoriza modificar herramientas.

**EVIDENCIA-OBSERVADA:** el usuario plantea que, si la entidad elabora mediante la SGE, esta podria recibir recien en la caja 25 la ratificacion y el encargo. Distingue las tres alternativas de elaboracion y advierte que el supervisor emite un informe tecnico de necesidad. Esta observacion revela un riesgo operativo: una comunicacion tardia al organo elaborador reduce el tiempo efectivo de trabajo sin desplazar el vencimiento legal.

**EXIGENCIA-NORMATIVA propuesta:** [Reglamento de la Ley 32069, edicion oficial actualizada al 21-10-2026](https://diariooficial.elperuano.pe/Normas/obtenerDocumento?idNorma=25), consultado el **2026-11-19**, art. 194.2 a-d, PDF pp. 121-122: la anotacion en el cuaderno es el hito; el supervisor remite a la entidad en hasta cinco dias desde el dia siguiente un informe tecnico sobre la necesidad y el riesgo; las bases eligen entre entidad, contratista y supervisor para elaborar; los quince dias para presentar se cuentan desde el dia siguiente de la anotacion, condicionados a la ratificacion de la necesidad. La [Opinion D000092-2026-OECE-DTN](../../../../../03-conocimiento/fuentes/guia-opinion-d000092-2026-oece-dtn.md), nums. 2.1-2.3 y 3.1-3.3, y su nota 4 en p. 2, confirma que la ratificacion no inicia ni suspende los quince dias y debe comunicarse al contratista o al organo elaborador, segun corresponda. No se presume que el contratista conozca el informe solo por participar en el cuaderno.

**INFERENCIA INSTITUCIONAL:** el [ROF GRH 2023](../../../../../03-conocimiento/fuentes/guia-rof-grh-2023.md), arts. 95-96, PDF p. 47, identifica a SGE como organo responsable de expedientes tecnicos; esto permite nombrarla como destino operativo **si las bases asignan la elaboracion a la entidad y esta encarga la tarea a SGE**. El ROF por si solo no prueba esa asignacion en un contrato concreto. La fecha efectiva de vigencia del ROF sigue pendiente de registrar en su guia, por lo que esta referencia institucional no se usa como regla validada de linea base.

**PROPUESTA DE MODELAMIENTO:** la caja 91 avisa oportunamente de la anotacion y el encargo al elaborador que aun no los conoce, expresamente a SGE en la alternativa institucional; la caja 25 comunica despues la ratificacion para permitir la presentacion. El supervisor conoce su propia posicion al emitir el informe; cuando elabora, no se agrega una notificacion formal redundante como requisito legal. El contratista solo puede omitir un aviso duplicado de la anotacion si ya la conoce por haberla realizado; la comunicacion de la ratificacion se conserva cuando le corresponde. Ninguno de esos avisos crea un plazo de quince dias nuevo. Si SGE recibe su primer aviso recien con la ratificacion, se documenta una demora operativa que requiere atencion institucional, sin alterar ficticiamente el computo.

Control del lote: generacion focalizada de BPMN, SVG, PNG y HTML correcta; D1 y D2 validos, D5 sin hallazgos, D4 conserva 19 advertencias geometricas preexistentes y D3 mantiene las limitaciones del simulador ya descritas. Revision de etiquetas: 186 notas, cero problemas. `git diff --check` no reporta errores de espacio. Los derivados se mantienen como propuesta de trabajo.

## Autor del expediente y ruta de evaluacion - 2026-11-19

Paquete de contexto: fase conceptual; tabla y sustento S4.3.2.3, guia CON-010 y texto del art. 194.2 activos. Derivados graficos y BPMN XML excluidos de la lectura conceptual; modificacion de herramientas no autorizada.

**EVIDENCIA-OBSERVADA:** el usuario observa que la antigua caja 58, formulada como nueva acreditacion del elaborador, confunde la evaluacion; en la practica institucional la mayoria de expedientes serian evaluados por la supervision. Solicita mostrar quien evalua cuando el supervisor elabora el expediente y el papel de la entidad. La frecuencia observada no sustituye la regla aplicable a cada autor del expediente.

**EXIGENCIA-NORMATIVA propuesta:** [Reglamento de Ley 32069, edicion oficial actualizada al 21-10-2026](https://diariooficial.elperuano.pe/Normas/obtenerDocumento?idNorma=25), consultado el **2026-11-19**, art. 194.2 c, e y g, PDF pp. 121-122: las bases definen quien elabora; cuando el contratista elabora, la supervision se pronuncia en diez dias desde el dia siguiente de la presentacion; antes de aprobar, la entidad pide opinion tecnica al proyectista u organo competente segun el supuesto. La [Opinion D000092-2026-OECE-DTN](../../../../../03-conocimiento/fuentes/guia-opinion-d000092-2026-oece-dtn.md), num. 2.9 A-C, PDF p. 6, y conclusiones 3.9-3.11, p. 10, precisa tres rutas: expediente del contratista, opinion de supervision y opinion tecnica previa en el mismo plazo de diez dias; expediente del supervisor, opinion tecnica previa de proyectista u organo competente sin autocontrol de supervision; expediente del organo de la entidad, opinion del supervisor en el «plazo correspondiente» y, si corresponde, opinion del proyectista. No fija un plazo autonomo de diez dias para toda evaluacion ni identifica a una persona de libre designacion como sustituto universal del supervisor. Vigencia e identidad del contrato concreto siguen sujetas a verificacion especializada; estas reglas no se marcan `VALIDADO`.

**PROPUESTA DE MODELAMIENTO:** la caja 58 pasa a «Identificar autor y ruta de evaluacion», sin segunda decision de acreditar al elaborador, porque esta se resolvio antes del encargo. La 59 selecciona las opiniones aplicables. La caja 64 explicita los diez dias solo cuando el contratista elaboro, y deja señalado el plazo pendiente de precisar cuando elaboro la entidad. La 27 identifica a quien emite la opinion tecnica previa; si elaboro el supervisor, esta es la evaluacion ajena al autor del expediente. La eventual designacion interna de una persona y su plazo de trabajo requieren base institucional o contractual adicional; `EVIDENCIA-INSUFICIENTE` para convertirlos en exigencia general.

Control del lote: regeneracion focalizada de BPMN, SVG, PNG y HTML correcta; D1 valido, D2 sin problemas, D5 sin hallazgos y D4 con 19 hallazgos geometricos, sin aumento respecto del lote anterior. D3 conserva las advertencias del simulador ya documentadas. Revision de etiquetas: 186 notas, cero problemas; `git diff --check` sin errores de espacio. No se atribuye conformidad institucional.

## Informe favorable de SGE y trazabilidad del visor - 2026-11-20

Paquete de contexto: fase conceptual para el flujo y fase de infraestructura para el visor; tabla y sustento S4.3.2.3 activos. BPMN XML y graficos excluidos de la lectura conceptual; generacion focalizada al cerrar el lote. Modificacion de herramientas autorizada por la solicitud expresa del usuario.

**EVIDENCIA-OBSERVADA:** el usuario precisa que SGE emite un informe incluso cuando la evaluacion tecnica de la caja 29 resulta favorable. La ruta previa pasaba directamente de esa compuerta a la comunicacion de SGGOS.

**PROPUESTA DE MODELAMIENTO:** la caja 98, en el carril de coordinacion de revision tecnica de SGE, elabora el informe favorable y lo entrega a la comunicacion posterior de SGGOS. La ruta desfavorable mantiene la caja 30 de integracion de observaciones. El informe no sustituye la resolucion ni acredita por si solo la opinion del proyectista o del supervisor. La forma documental y el circuito interno definitivo requieren contraste institucional; no se atribuye a esta caja un plazo autonomo.

**PROPUESTA DE INFRAESTRUCTURA:** el visor incorpora un arbol desde el mapa institucional Nivel 0, con enlaces a indices para niveles sin BPMN. La referencia textual de cada caja permanece visible; un archivo opcional de anclas documentales podra agregar ruta local, pagina fisica del PDF y fragmento. Mientras no se registren esas anclas, el panel indica expresamente que falta ubicacion precisa. Abrir un PDF en pagina concreta se soporta; el resaltado de su fragmento depende del visor PDF del navegador, mientras que los textos locales se resaltan en la vista servida. Ninguna ancla crea o valida una regla normativa.

**ANCLAS DOCUMENTALES INICIALES, 2026-11-20:** el [archivo de referencias del visor](S4-3-2-3-fuentes-visor.json) enlaza las cajas R-T1 y X-T1 con la p. 2 de la Opinion D000092-2026-OECE-DTN (num. 2.1 y transcripcion del art. 194.2 a y d), y S-T3 con la p. 6 (num. 2.9 A-C). Se cotejaron los tres terminos de busqueda con el texto de esas paginas del PDF local. La consulta y el estado de aplicabilidad provienen de la [guia de la opinion](../../../../../03-conocimiento/fuentes/guia-opinion-d000092-2026-oece-dtn.md). Estas anclas facilitan la lectura y no validan el contenido normativo ni acreditan que todas las cajas del modelo tengan ya una ubicacion precisa. El resto permanece pendiente de cotejo documental por elemento y flujo.

Control del lote: regeneracion focalizada y comprobacion global `construir_modelos.py --check` correctas. D1 y D2 sin problemas, D5 sin hallazgos. D4 conserva 18 interferencias geometricas y D3 mantiene las advertencias del simulador de mensajes y compuertas inclusivas ya documentadas; esta caja no las resuelve. Prueba de navegacion en Edge, API de arbol, visor de texto y diez pruebas del perfil correctas. Revision de etiquetas: 186 notas, cero problemas. Sin validacion normativa ni conformidad institucional.

## Puertos y corredores de las cajas 25, 29 y 62 - 2026-11-19

Paquete de contexto: fase de revision visual solicitada; fuente tabular, PNG y perfil `zigzag-controlado` activos. El BPMN XML se consulta solo para geometria y verificacion D1-D5; no se cambia el flujo conceptual. Modificacion de herramientas autorizada por la solicitud expresa de ajustar el perfil.

**EVIDENCIA-OBSERVADA:** el usuario indica que la ruta desde la caja 62 debe salir por la izquierda y llegar por arriba a la 29; la salida continua de la 25 debe abrir a la derecha, bajar, girar a la izquierda y volver a bajar sin discurrir junto al mensaje punteado. El PNG previo mostraba una entrada a la 29 desde su borde izquierdo y tramos verticales casi coincidentes junto a la 25.

**PROPUESTA DE TRAZADO:** el perfil prueba el puerto izquierdo de la 62 y el superior de la 29 cuando existe un corredor libre. Para la 25, separa la secuencia del mensaje mediante un rodeo exterior a su anotacion; la distancia horizontal de los tramos verticales es de 50 unidades BPMN-DI. No se altera la direccion semantica, los responsables ni los plazos. El PNG regenerado se inspecciono en ambos sectores y muestra los puertos y el corredor solicitados. D1 y D2 correctos, D5 sin hallazgos y D4 baja de 19 a 18 advertencias; D3 conserva las limitaciones del simulador ya documentadas. Diez pruebas del perfil pasan, incluida una regresion de estas conexiones. Los hallazgos D4 restantes y la conformidad institucional siguen pendientes.

## Auditoría por afirmación — 2026-11-24 (fase 5)

Auditoría con el formato de DEC-057 ([informe generado](../../../../../05-herramientas/gestor-modelos/auditorias/S4-3-2-3/informe.md)): 95 afirmaciones (29 `SUSTENTADA`, 66 `INFERENCIA`, sin contradicciones) y 14 obligaciones del Reglamento art. 194 (texto vigente) y de la Ley art. 64, de las que 3 no están representadas. Las 66 inferencias corresponden sobre todo a la ruta institucional (OACGD, SGGOS, SGE, controles de DEC-038) y a decisiones de modelamiento, sin norma literal que las sustente. Las anclas pasan de 3 a 75, calculadas desde el texto. Las 3 referencias previas a la Opinión D000092 no tienen coordenadas y quedan marcadas como tales. Son propuestas de IA, sin validación ni conformidad.

- **Bien representado:** el circuito del art. 194.2 a)-g), con sus plazos (5, 15, 10 y 12 días hábiles), la opinión técnica previa con el límite de un año del proyectista, y los límites y autorizaciones de la Ley 64.2-64.4 (15 %, 30 %, 50 % y 15 días hábiles de la Contraloría).
- **No representado:**
  - el **194.3 vigente**: la aprobación surte efecto con su publicación en la Pladicop, sin adenda, y **está prohibido aprobar adicionales por regularización**. E-T11 deja el canal «por confirmar» y no recoge la prohibición;
  - el **194.4**: en emergencia, la entidad autoriza a la supervisión a disponer la ejecución inmediata y regulariza después por el 194.2. E-GREG envía la emergencia a pendiente;
  - el **194.5**: si los adicionales superan el 50 % del contrato original, se resuelve el contrato. E-G8 no tiene rama para ese caso.
- **Interfaz:** E-FRED envía casos a S4.3.2.7 sin contraparte allí, y R-E1 recibe de S4.3.2.2 una respuesta que S4.3.2.2 no envía.
- **ROF:** el art. 98 (funciones de la SGGOS) quedó segmentado junto al art. 97 en el texto extraído; el ancla lo indica.
- **Propuestas no aplicadas:**
  - nombrar la Pladicop y la prohibición de regularizar en E-T11;
  - una ruta o anotación de emergencia conforme al 194.4;
  - una rama de E-G8 para el caso que supera el 50 %, con resolución del contrato.

