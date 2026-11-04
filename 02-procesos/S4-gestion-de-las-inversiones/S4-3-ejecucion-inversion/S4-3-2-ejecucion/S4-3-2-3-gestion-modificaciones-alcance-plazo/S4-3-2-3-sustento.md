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
fecha_actualizacion: 2026-11-04
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-3
---

# S4.3.2.3 Gestion de modificaciones de alcance o plazo - Sustento

Sube a: [S4.3.2.3 Gestion de modificaciones de alcance o plazo](00-S4-3-2-3-gestion-modificaciones-alcance-plazo.md)

## Resultado del analisis

El modelo propuesto no reproduce literalmente el Bizagi recibido. Conserva como evidencia observada su circuito de recepcion, evaluacion tecnica, evaluacion presupuestal, revision legal, decision y notificacion, pero corrige diez problemas:

1. modela al residente y al supervisor o inspector como roles comunes de obra, sin duplicarlos por modalidad;
2. usa una entrada comun a la entidad y clasifica el regimen y la figura dentro de SGGOS;
3. distingue las reglas sustantivas de contrata y administracion directa sin convertirlas en dos circuitos administrativos completos;
4. sustituye la regla historica de remitir a la Contraloria al superar 15 % por los umbrales vigentes de la Ley 32069;
5. separa la validacion inicial de la necesidad, la elaboracion del expediente y la revision tecnica institucional independiente;
6. limita al monitor o gestor a integridad, clasificacion, trazabilidad, plazos y consolidacion, sin atribuirle una conformidad tecnica para la que puede no tener especialidad;
7. identifica primero si el hecho ya estaba comprendido en el alcance original, es valorizacion o constituye una modificacion potencial;
8. activa al elaborador definido en las bases de contrata o designado por la OAD en administracion directa;
9. incorpora segregacion entre quien elabora, quien revisa tecnicamente y quien decide, con acceso a un especialista competente distinto del elaborador;
10. representa los controles contractual y de costos, presupuestal y juridico como rutas independientes y combinables, no como una secuencia obligatoria para todos los casos.

La instancia del proceso es una solicitud, necesidad o causal de modificacion. Por ello, cada caso se tramita y cierra de manera independiente, aunque la obra continue ejecutandose. La formalizacion posterior de un reinicio constituye otra instancia disparada cuando se verifican sus condiciones; no mantiene abierta indefinidamente la instancia que decidio la modificacion.

## Fuentes utilizadas

| ID o fuente | Ubicacion precisa | Consulta y vigencia | Clase y uso |
|---|---|---|---|
| Ley 32069 consolidada | Arts. 63-64, PDF pp. 30-31; [archivo](../../../../../01-referencias/04-contrataciones-publicas/ley-y-reglamento/ley-general-de-contrataciones-publicas-con-modificaciones-posteriores-hasta-el-19-07-2026.pdf) | Consulta 2026-11-04; texto consolidado con modificaciones hasta 2026-07-19 | `EXIGENCIA-NORMATIVA` propuesta: tipos de modificacion, autoridades y umbrales de adicionales de obra |
| Reglamento de la Ley 32069 | Arts. 107, 109, 186, 188 y 191-202, PDF pp. 59-60 y 101-115; [archivo](../../../../../01-referencias/04-contrataciones-publicas/ley-y-reglamento/reglamento-de-la-ley-general-de-contrataciones-publicas-con-modificaciones-posteriores-hasta-el-09-01-2026.pdf) | Consulta 2026-11-04; texto consolidado al 2026-01-09. La vigencia de las modificaciones del DS 001-2026-EF se verifico para esta propuesta desde 2026-01-14 mediante la [RD 001-2026-EF/54.01](https://www.gob.pe/institucion/mef/normas-legales/7614342-001-2026-ef-54-01) y el [compendio oficial del OECE](https://www.gob.pe/institucion/oece/colecciones/45029-ley-n-32069-ley-general-de-contrataciones-publicas-y-su-reglamento) | `EXIGENCIA-NORMATIVA` propuesta: supervisor o inspector, cuaderno de incidencias, suspension, reduccion, intensificacion, adicionales, mayores metrados, ampliacion y reinicio |
| Directiva 017-2023-CG/GMPL | Nums. 6.8.2-6.8.3, 7.2.3, 7.3.2 y 7.3.6-7.3.8, PDF pp. 9-10 y 14-18; [archivo](../../../../../01-referencias/05-control-gubernamental/administracion-directa/directiva-n-017-2023-cg-gmpl.pdf) | Consulta 2026-11-04; vigencia material y modificatorias pendientes de validacion especializada | `EXIGENCIA-NORMATIVA` propuesta: residente, inspector o supervisor, cuaderno de obra, abastecimiento y modificaciones de alcance, costo y plazo en administracion directa |
| Directiva 017-2025-OECE-CD | Num. 10.3, literal C, y num. 10.4.9, PDF pp. 6-8; [archivo](../../../../../01-referencias/04-contrataciones-publicas/cuaderno-incidencias/directiva-n-017-2025-oece-cd-directiva-de-disposiciones-sobre-el-uso-del-cuaderno-de-incidencias.pdf) | Consulta 2026-11-04; vigente desde 2025-10-12 segun la [resolucion y ficha oficial](https://www.gob.pe/institucion/oece/normas-legales/7281401-017-2025-oece-cd) | `EXIGENCIA-NORMATIVA` propuesta: el rol Monitor del Cuaderno de Incidencias visualiza la informacion para seguimiento; no se le atribuye evaluacion tecnica |
| ROF del Gobierno Regional Huanuco | Arts. 20, 44-45, 51 y 92-98; [guia de lectura](../../../../../03-conocimiento/fuentes/guia-rof-grh-2023.md) | Consulta 2026-11-04; aprobado en 2023; publicacion efectiva y modificatorias posteriores pendientes de control de vigencia | `EXIGENCIA-NORMATIVA` propuesta para competencias; `INFERENCIA` para el circuito interno |
| Directiva General de Invierte.pe | Art. 33.2; regla `REG-INV-EJEC-004` | Fuente ya registrada; estado de validacion no modificado | Registro de modificaciones durante la ejecucion fisica cuando corresponda |
| Exportacion Bizagi de Consultas | `99-temporal/modelos/sggos-2026-11-02-bpmn/consultas-bizagi.bpmn`, ramas de suspension, adicional y reduccion | Observada 2026-11-04; XML no valido y con codificacion inconsistente | `EVIDENCIA-OBSERVADA`: actividades, documentos y unidades que deben contrastarse; no es linea base |
| `DEC-032` | [Registro de decisiones](../../../../../00-gobernanza/registro-decisiones.md) | Vigente en el proyecto | Codigo, nombre, nivel 3 y tratamiento de las figuras como variantes internas sin codigo de nivel 4 |

Las reglas normativas de esta nota son propuestas de conocimiento preparadas por IA. No tienen estado `VALIDADO` ni acreditan conformidad de una unidad organica.

## Arquitectura del proceso propuesta

| Bloque | Contenido | Justificacion |
|---|---|---|
| 1. Originar y validar la necesidad | El residente sustenta o el supervisor o inspector identifica la necesidad; el rol de control de obra evalua necesidad, efecto y riesgo y decide si la ratifica | Es un control de primera linea sobre necesidad y constructibilidad. No equivale a elaborar ni aprobar la solucion tecnica |
| 2. Registrar, verificar integridad y clasificar | OACGD registra y deriva. El monitor o gestor verifica integridad, regimen, modalidad y trazabilidad | El ROF sustenta el circuito documental y de seguimiento; la Directiva 017-2025-OECE-CD no convierte al monitor en evaluador tecnico |
| 3. Controlar admisibilidad contractual | SGGOS contrasta la propuesta con alcance original, planos, especificaciones, metrados, modalidad de pago y causal | Separa obligaciones ya contratadas, errores de valorizacion y mejoras no indispensables de una modificacion potencial. En suma alzada, una omision de metrado no convierte por si sola una prestacion prevista en adicional |
| 4. Clasificar figura y definir elaborador | Se identifica la figura de alcance o plazo y, si requiere expediente tecnico, se activa al elaborador definido en las bases o designado por la OAD | El Reglamento, art. 194.2 c, distribuye la elaboracion en contrata; la Directiva 017-2023-CG regula la designacion en administracion directa |
| 5. Revisar tecnicamente con independencia | SGE asigna u obtiene un especialista competente distinto del elaborador; este verifica necesidad, alternativa, compatibilidad, prestaciones, normas, metrados e interfaces y emite opinion | No duplica la evaluacion de supervision: aplica un control institucional independiente sobre el expediente ya desarrollado. Si SGE no dispone de la especialidad, el modelo exige obtener apoyo antes de opinar |
| 6. Obtener controles complementarios | Segun regimen, figura, impacto y riesgo se activan control contractual y de costos, presupuesto y/o revision juridica | Los controles son combinables. Quien consolida no sustituye la responsabilidad del autor de cada opinion |
| 7. Consolidar y autorizar externamente | El monitor arma la matriz de controles, responsables, discrepancias y pendientes; solo se solicita autorizacion de Contraloria cuando la norma lo exige | El control de completitud y segregacion antecede a la decision; evita conservar el umbral historico de 15 % del Bizagi |
| 8. Decidir, registrar y comunicar | La autoridad competente resuelve segun regimen, figura, umbral y delegacion; SGGOS actualiza registros y coordina la comunicacion formal | El Subgerente de SGGOS solo ocupa el rol decisor si existe competencia o delegacion vigente. El canal documentario puede involucrar OACGD sin agregar una segunda cadena al nivel mostrado |

## Matriz normativa de variantes y reglas por regimen

| ID interno | Figura agrupada | Contrata | Administracion directa | Producto o decision |
|---|---|---|---|---|
| `MOD-ALC-ADI` | Adicional o modificacion tecnica | Aplica el calculo neto, los umbrales y el procedimiento de la Ley y el Reglamento | Aplica el sustento y aprobacion de la modificacion del expediente tecnico previstos por la directiva | Aprobacion, denegacion, reformulacion o resolucion, segun el regimen y umbral |
| `MOD-ALC-RED` | Reduccion o deductivo | La reduccion contractual tiene limite, condiciones y resolucion propios; el deductivo vinculado integra el calculo del adicional | El expediente modificado puede contener deductivos y debe seguir el tramite tecnico, legal y presupuestal aplicable | Acto de aprobacion o denegacion y actualizacion del expediente o contrato |
| `MOD-ALC-MAY` | Mayores metrados o cantidades | El supervisor o inspector autoriza la ejecucion en el cuaderno; la entidad autoriza el pago | El inspector o supervisor puede aprobar cambios no significativos y mayores metrados dentro de los limites de la directiva | Autorizacion, registro y pago cuando corresponda |
| `MOD-PLA-AMP` | Ampliacion de plazo | Se acredita afectacion de ruta critica y se sigue el procedimiento contractual | Se acredita causal y afectacion de ruta critica; residente solicita, inspector o supervisor valida y la entidad decide | Ampliacion aprobada o denegada y cronograma actualizado |
| `MOD-PLA-SUS` | Suspension, paralizacion o reinicio | Se aplica el acuerdo de suspension contractual y el reinicio conforme al Reglamento | Se aplican las causales, validacion y autorizacion de paralizacion y reinicio de la directiva | Documento de suspension o paralizacion y documento de reinicio |
| `MOD-PLA-INT` | Intensificacion del programa | Figura prevista por los arts. 191-192 del Reglamento | No se presume figura equivalente; requiere confirmar aplicabilidad | Acuerdo y programa intensificado cuando corresponda |

Fuentes precisas: Ley, arts. 63-64; Reglamento, arts. 107, 109 y 191-202; Directiva 017-2023-CG/GMPL, nums. 7.3.6-7.3.7, PDF pp. 17-18.

## Aplicacion al Gobierno Regional Huanuco

| Participante o carril | Fundamento | Tratamiento en el modelo |
|---|---|---|
| Residente de obra | Reglamento, art. 188.3; Directiva 017-2023-CG, nums. 6.8.2, 7.3.6-7.3.7 | Rol de campo comun a ambas modalidades; identifica, registra y sustenta la necesidad en el cuaderno |
| Supervisor o inspector de obra | Reglamento, arts. 186.1 y 188.3; Directiva 017-2023-CG, nums. 6.8.3 y 7.3.6-7.3.8 | Rol de control comun a ambas modalidades. El inspector es servidor designado y el supervisor es contratado; no actuan simultaneamente. Se modelan en un pool funcional separado por su autonomia tecnica, sin negar la vinculacion organica del inspector con el GORE |
| OACGD | ROF, art. 20 | Recibe, registra, clasifica, deriva y notifica documentos. No evalua el fondo de la modificacion |
| SGGOS - Monitor o gestor | ROF, arts. 97-98; Directiva 017-2025-OECE-CD, num. 10.3 C | Revisa integridad, clasifica regimen y modalidad, controla trazabilidad y plazos y consolida opiniones. No emite conformidad tecnica por defecto ni reemplaza al especialista |
| SGGOS - Control contractual y costos | Ley 32069, arts. 63-64; Reglamento, arts. 158, 161, 194-197 y 210; ROF, arts. 97-98 | Contrasta alcance original, causal, modalidad de pago, metrados, precios y acumulados. Distingue obligacion original, valorizacion, mejora no necesaria y modificacion admisible |
| Elaborador definido o designado | Reglamento, art. 194.2 c-f; Directiva 017-2023-CG, num. 7.3.6 | Desarrolla planos, especificaciones, memoria, metrados, costos y demas contenido del expediente. No se presume que pueda revisar institucionalmente su propio producto |
| SGE - Coordinacion de revision tecnica | Reglamento, art. 194.2 g; ROF, arts. 95-96 | Asigna u obtiene un revisor competente e independiente. Si no existe especialidad interna suficiente, debe gestionarse apoyo o revision externa antes del pronunciamiento institucional |
| SGE - Especialista tecnico competente | Reglamento, art. 194.2 d-g; ROF, arts. 95-96 | Revisa la solucion desarrollada contra necesidad, prestaciones, normas, compatibilidad, cantidades e interfaces y sustenta la opinion tecnica. Es un control institucional distinto de la supervision y del elaborador |
| Subgerencia de Presupuesto Publico | ROF, art. 51 | Emite certificacion o prevision cuando la variante genera incidencia presupuestal y la norma lo exige |
| Gerencia Regional de Asesoria Juridica | ROF, art. 45 | Emite opinion o revisa el acto cuando corresponde; el Bizagi observado no basta para hacer obligatoria su intervencion universal |
| Gerencia Regional de Infraestructura | ROF, arts. 92-93 | Integra y eleva la propuesta en el circuito planteado. Debe validarse que sea la unidad que remite formalmente cada solicitud externa |
| Autoridad competente | Ley, arts. 25 y 63-64; Reglamento, arts. 107, 109, 191, 197, 200 y 202; Directiva 017-2023-CG | Se mantiene como rol generico porque la fuente revisada no contiene la delegacion vigente del GORE para cada figura. No se atribuye universalmente la decision al Subgerente de SGGOS |
| Contraloria | Ley, art. 64.3 b y 64.4 | Participante externo solo en adicionales que superan 30 % y no exceden 50 %, conforme al calculo normativo aplicable |

## Segregacion y control frente a una evaluacion deficiente

La revision institucional no se considera una repeticion de la supervision. Cada control responde una pregunta diferente:

| Control | Pregunta principal | Evidencia esperada |
|---|---|---|
| Supervisor o inspector | ¿La necesidad existe en campo y afecta la ejecucion, seguridad, funcionalidad o plazo? | Asiento, informe de necesidad, riesgos y recomendacion |
| Elaborador | ¿Como se resuelve tecnicamente la necesidad ratificada? | Expediente con memoria, planos, especificaciones, metrados, costos y cronograma que correspondan |
| Especialista tecnico de SGE | ¿La solucion propuesta es necesaria, compatible, suficiente y conforme a la especialidad? | Informe tecnico independiente que identifica verificaciones, observaciones y conclusion |
| Control contractual y de costos | ¿La prestacion ya estaba incluida, la figura es admisible y el costo y acumulados son consistentes? | Matriz de alcance original, causal, modalidad de pago, metrados, precios y umbrales |
| Monitor o gestor | ¿El expediente contiene los controles exigibles, conserva trazabilidad y resolvio discrepancias? | Lista de verificacion y matriz de responsables; no una nueva opinion tecnica |
| Autoridad competente | ¿Corresponde adoptar el acto dentro de su competencia y con sustento suficiente? | Pronunciamiento, acuerdo, resolucion o autorizacion, segun la figura |

Como propuesta de control interno (`DEC-038`), quien elaboro el expediente no debe emitir la unica opinion tecnica que sustenta su aprobacion; las discrepancias entre supervision, elaborador, especialista, costos, presupuesto o asesoria juridica deben quedar identificadas y resueltas antes de elevar el caso. Son alertas para revision reforzada: cambio de solucion sin necesidad demostrada, sustitucion por una prestacion inferior o mas costosa, omision de una obligacion ya prevista en planos o especificaciones, metrados que solo corrigen una valorizacion, mejora no indispensable, fraccionamiento, acumulados cercanos a umbrales y ausencia de especialista competente. Estas alertas son una propuesta operativa pendiente de validacion institucional, no una presuncion de responsabilidad ni una regla normativa validada.

## Discrepancias con el Bizagi observado

| Hallazgo observado | Evaluacion | Tratamiento propuesto |
|---|---|---|
| Una compuerta pregunta si el monto acumulado neto adicional supera 15 % y, si la respuesta es afirmativa, remite a Contraloria | Regla incompatible con los umbrales vigentes de la Ley 32069 | Se reemplaza por clasificacion segun figura y umbral: Contraloria solo para el tramo mayor de 30 % y hasta 50 % |
| Adicional y reduccion comparten una misma rama | Son figuras con requisitos, limites y actos distintos | Se modelan como variantes independientes |
| Suspension o paralizacion aparece junto con continuidad de trabajos | La suspension contractual y la paralizacion en administracion directa tienen reglas diferentes, pero comparten actores de campo y una ruta institucional semejante | Se agrupan como variante de plazo; SGGOS clasifica el regimen antes de aplicar la regla |
| Presupuesto, asesoria juridica y autorizacion externa aparecen como pasos casi lineales | No todas las figuras requieren las mismas intervenciones | Se utiliza una compuerta inclusiva para evaluaciones combinables y una decision separada para Contraloria |
| Participantes institucionales antiguos o genericos | El ROF vigente usa OACGD, SGGOS, SGE, Presupuesto, GRAJ y GRI | Se actualizan los carriles y se conserva como brecha la autoridad delegada |
| El monitor parece recibir y evaluar tecnicamente expedientes de cualquier especialidad | El rol Monitor del Cuaderno de Incidencias es de visualizacion y seguimiento; el ROF no demuestra competencia tecnica universal | Se limita al monitor a integridad, clasificacion, trazabilidad, plazos y consolidacion, y se asigna la revision a un especialista competente |
| No queda segregado quien elabora del que revisa el adicional | La fuente permite distintos elaboradores y exige opinion del organo especializado de la entidad en los supuestos aplicables | Se crea un participante elaborador y un segundo control tecnico institucional independiente conducido por SGE |

## Decisiones de visualizacion

- El diagrama muestra la orquestacion comun y las variantes como actividades internas, no como procesos de nivel 4.
- Se eliminan los carriles exclusivos de residente e inspector de administracion directa. Los dos roles de campo se muestran como participantes funcionales comunes y la modalidad deja de condicionar la estructura de actores.
- Las evaluaciones combinables se dibujan con compuerta inclusiva. Esta excepcion a la preferencia por compuertas exclusivas evita tres decisiones binarias sucesivas y expresa mejor que pueden activarse una, varias o ninguna.
- El elaborador se muestra como participante separado. El pool expresa independencia funcional del acto de elaboracion, aunque en un caso concreto el responsable sea una unidad del GORE, el contratista, la supervision u otro sujeto definido por las bases o designado por la OAD.
- La salida favorable integra registro y coordinacion de la comunicacion en SGGOS; OACGD permanece como canal documentario posible sin extender el nivel principal con una segunda cadena de salida.
- El reinicio se muestra como una instancia posterior iniciada por evento condicional. Asi se evita mantener abierta la instancia que resolvio la modificacion durante un tiempo indeterminado.
- Se usa el perfil experimental `zigzag-amplio`: compacta por participante y solo pliega despues de 28 columnas. El tramo de 16 columnas empleado en S4.3.2.2 genera 24 hallazgos D4 en este modelo ramificado. `DEC-039` elimina dentro de cada carril las filas de fase sin elementos y reduce la altura del PNG de 9870 a 7260 px (26,4 %) sin cambiar la semantica.
- La disposicion visual no altera la semantica. D1, D2, D3 y D5 no presentan hallazgos. D4 conserva dos advertencias `T4`: los rotulos `P` y `J` de la compuerta inclusiva se montan entre si, y `No` se monta sobre `¿Favorable?`. Se adopta forzadamente el derivado porque las tareas, carriles y rutas siguen siendo distinguibles y eliminar las condiciones ocultaria responsabilidades; queda pendiente ajustar el algoritmo BPMN-DI y realizar revision visual humana antes de cualquier linea base.

## Vacios y preguntas para validacion

| Vacio | Marca | Evidencia o decision necesaria |
|---|---|---|
| Autoridad de la gestion administrativa y delegaciones vigentes del GORE por figura | `EVIDENCIA-INSUFICIENTE` | Resolucion o acto de delegacion vigente |
| Unidad que remite formalmente a la Contraloria y sus documentos | `EVIDENCIA-INSUFICIENTE` | Procedimiento interno y validacion de GRI, SGGOS y OACGD |
| Criterios exactos para activar SGE, Presupuesto y GRAJ en cada variante | `EVIDENCIA-INSUFICIENTE` | Matriz institucional validada por responsables |
| Responsable interno de control contractual y costos y su matriz de revision por modalidad de pago | `EVIDENCIA-INSUFICIENTE` | Perfiles, asignacion funcional, directiva interna y lista de verificacion aprobada |
| Mecanismo para obtener especialista independiente cuando SGE no dispone de la especialidad | `EVIDENCIA-INSUFICIENTE` | Definir encargo, apoyo interorganico o contratacion, requisitos de independencia, entregable y plazo |
| Regla institucional de impedimentos y segregacion entre elaborador, revisor y decisor | `EVIDENCIA-INSUFICIENTE` | Politica de integridad o control interno validada; el modelo solo registra la propuesta `maker-checker` |
| Momento de registro en Banco de Inversiones frente a mayores metrados autorizados por el supervisor | `DISCREPANCIA-PENDIENTE` | Criterio de Invierte.pe y practica institucional documentada |
| Interfaz con adquisiciones cuando una modificacion de administracion directa cambia bienes o servicios requeridos | `EVIDENCIA-INSUFICIENTE` | Definir la salida hacia el proceso de abastecimiento y los documentos que preparan el residente y valida el supervisor o inspector. No se incorpora la adquisicion dentro de S4.3.2.3 |
| Inclusion definitiva de intensificacion, propuesta de cambio de ingenieria de valor y modificacion por hecho sobreviniente | `EVIDENCIA-INSUFICIENTE` | Decision de alcance y revision de arts. 110 y 191-192 del Reglamento |
| Formularios, plazos internos, firma y medio de notificacion de cada variante | `EVIDENCIA-INSUFICIENTE` | Procedimientos, TUPA interno si aplica y validacion operativa |
| Vigencia material de la Directiva 017-2023-CG y del ROF frente a modificatorias posteriores | `VALIDACION-PENDIENTE` | Control normativo especializado |

## Informacion BIM

`EVIDENCIA-INSUFICIENTE`. Una modificacion puede afectar modelos o requisitos de informacion, pero no se asigna ningun requisito BIM sin fuente y validacion especificas.

## Historial de revision

| Documento | Nivel | Fecha | Resultado | Rol o unidad | Evidencia |
|---|---|---|---|---|---|
| Juego inicial S4.3.2.3 | `ELABORACION` | 2026-11-03 | Propuesta creada | Equipo del proyecto con asistencia de IA | `DEC-032`; Bizagi; catalogo de eventos |
| Reconstruccion normativa y contextual | `ELABORACION` | 2026-11-04 | Regimenes, variantes, umbrales y carriles GORE replanteados; pendiente validacion | IA; sin atribuir revision humana | Ley 32069; Reglamento; Directiva 017-2023-CG; ROF; Bizagi observado |
| Unificacion de actores de obra | `ELABORACION` | 2026-11-04 | Residente y supervisor o inspector modelados como roles comunes; regimen clasificado dentro de la entidad | Precision operativa expresa del equipo, contrastada con las fuentes; sin atribuir validacion normativa | `DEC-037`; Reglamento, arts. 186 y 188; Directiva 017-2023-CG, nums. 6.8.2-6.8.3 y 7.3.2-7.3.8 |
| Segregacion de elaboracion y controles | `ELABORACION` | 2026-11-04 | Monitor limitado a gestion del expediente; elaborador, revision tecnica competente, control contractual y decision separados | Propuesta IA basada en fuentes y precisiones del equipo; pendiente validacion institucional | `DEC-038`; Ley, arts. 25-28 y 63-64; Reglamento, arts. 158 y 194-197; Directivas 017-2023-CG y 017-2025-OECE-CD; ROF |
| Compactacion del trazado amplio | `ELABORACION` | 2026-11-04 | Filas de fase sin elementos eliminadas por carril; altura reducida 26,4 % | Refinamiento tecnico del generador; pendiente valoracion visual humana | `DEC-039`; controles D1-D5 y comparacion de dimensiones |

## Relaciones

- [S4.3.2.2 Atencion de consultas](../S4-3-2-2-atencion-consultas-obra/00-S4-3-2-2-atencion-consultas-obra.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)
- [Guia del Reglamento de la Ley 32069](../../../../../03-conocimiento/fuentes/guia-reglamento-ley-32069.md)
- [Guia del ROF del Gobierno Regional Huanuco](../../../../../03-conocimiento/fuentes/guia-rof-grh-2023.md)
- [Modelo Bizagi de Consultas](../../../../../99-temporal/modelos/sggos-2026-11-02-bpmn/consultas-bizagi.bpmn)
