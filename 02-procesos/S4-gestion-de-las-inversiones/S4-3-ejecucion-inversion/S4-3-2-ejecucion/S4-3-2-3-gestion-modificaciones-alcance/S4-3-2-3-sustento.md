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
fecha_actualizacion: 2026-11-05
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-3
---

# S4.3.2.3 Gestion de modificaciones de alcance - Sustento

Sube a: [S4.3.2.3 Gestion de modificaciones de alcance](00-S4-3-2-3-gestion-modificaciones-alcance.md)

## Resultado del realineamiento

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
