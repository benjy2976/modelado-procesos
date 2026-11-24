---
id: AP-S4-3-1-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S4.3.1
nivel_proceso: 2
proceso:
  - S4.3.1
fecha_creacion: 2026-11-18
fecha_actualizacion: 2026-11-18
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-1
---

# S4.3.1 Inicio de ejecucion - Sustento

Sube a: [S4.3.1 Inicio de ejecucion](00-S4-3-1-inicio-de-ejecucion.md)

Registra la procedencia y la revision preliminar del modelo recibido de Bizagi. El archivo es un **insumo observado**, no el diagrama formal ni una linea base de S4.3.1.

## Fuentes utilizadas

| Fuente | Ubicacion precisa | Estado | Uso |
|---|---|---|---|
| Exportacion Bizagi recibida | [Copia intacta](S4-3-1-insumo-modelo-bizagi.bpmn); origen local `99-temporal/modelos/sggos-2026-11-02-bpmn/inicio-ejecucion-bizagi.bpmn`; SHA-256 `E0F50BD0A6FD3FF6C0C79FDB27BD93627E2280FC7F43340D291257916D61AD9E` | `OBSERVADO`, copia verificada el 2026-11-18; no aprobada | Insumo para el levantamiento de S4.3.1 |
| [Modelo de S4.3](../00-S4-3-ejecucion-inversion.md) | Descomposicion de nivel 1, `DEC-028` | `PROPUESTA` en `ELABORACION` | Ubicar S4.3.1 antes de S4.3.2 |
| [Ley 32069, PDF OECE](../../../../01-referencias/04-contrataciones-publicas/ley-y-reglamento/ley-general-de-contrataciones-publicas-con-modificaciones-posteriores-hasta-el-19-07-2026.pdf) | Arts. 3.2 c, pagina PDF 2, y 62.4-62.5, pagina PDF 30 | Texto consolidado hasta el 19-07-2026, consultado el 2026-11-18; aplicabilidad al contrato concreto pendiente | Gobierno regional comprendido como entidad contratante; alternativa de inspector |
| [ROF del Gobierno Regional Huanuco](../../../../01-referencias/01-institucionales-grh/originales/reglamento-organizacion-funciones-grh-2023.pdf) | Arts. 20, pagina PDF 14; 24-25, paginas PDF 15-16; 29-30, paginas PDF 17-18; 92-94, paginas PDF 46-47; 97-98, paginas PDF 47-48 | Aprobado por Ordenanza Regional 013-2023-GRH-CR; [publicacion institucional](https://datos.regionhuanuco.gob.pe/publico/Rof-web.html) cotejada el 2026-11-18; modificaciones posteriores no descartadas exhaustivamente | Funciones de OACGD, GRA, Abastecimiento, GRI y SGGOS; no acredita itinerario concreto ni acto de designacion |
| Precision del usuario, 2026-11-18 | Mensaje de esta iteracion: GORE o ejecutoras; SGGOS usual; notificacion y designacion antes del coordinador | `EVIDENCIA-OPERATIVA-DECLARADA`, pendiente de respaldo documental | Ajuste de la frontera y ruta previa al coordinador |
| Precision del usuario, 2026-11-18, sobre condiciones pendientes | Mensaje de esta iteracion: si falta supervision, esperar su contratacion o gestionar inspeccion si procede; las otras condiciones generan hechos que permiten retomar la verificacion | `EVIDENCIA-OPERATIVA-DECLARADA`, pendiente de respaldo documental | Eliminar el fin por condiciones pendientes y representar eventos de reanudacion |
| [Reglamento de la Ley 32069, PDF OECE](../../../../01-referencias/04-contrataciones-publicas/ley-y-reglamento/reglamento-de-la-ley-general-de-contrataciones-publicas-con-modificaciones-posteriores-hasta-el-09-01-2026.pdf) | Arts. 176.1-176.9, paginas PDF 93-96; arts. 186.1-186.4, pagina PDF 101; art. 188.3, pagina PDF 104 | Texto consolidado al 09-01-2026, consultado el 2026-11-18; modificacion DS 001-2026-EF vigente desde el 14-01-2026; interpretacion `BORRADOR-IA` | Contraste normativo inicial, no validacion humana |
| [Compendio oficial OECE](https://www.gob.pe/institucion/oece/colecciones/45029-ley-n-32069-ley-general-de) | Reglamento actualizado y vigencia del DS 001-2026-EF | Consultado el 2026-11-18 | Verificacion oficial de version y entrada en vigor |
| [DS 222-2026-EF, El Peruano](https://busquedas.elperuano.pe/dispositivo/EX/2567159-1) | Art. 3, modifica solo la decimocuarta disposicion complementaria final | Publicado el 21-10-2026; consultado el 2026-11-18 | Comprobacion focalizada de que no cambia los arts. 176 ni 186 |

Las referencias al Reglamento corresponden al texto oficial OECE consolidado al 09-01-2026 y a la entrada en vigor de la modificacion del DS 001-2026-EF. La busqueda oficial identifico el DS 222-2026-EF de octubre, que no altera los articulos de inicio y supervision aqui usados. No se acredita una revision exhaustiva de todas las normas posteriores ni de la aplicabilidad del regimen al contrato concreto. Ninguna regla se marca `VALIDADO`.

## Revision del insumo

El BPMN declara tres participantes: un pool «Proceso principal», «Inicio de ejecucion contractual - SOLO CONSTRUCCION» y «Gerencia Regional de Administracion». Contiene tres carriles, 23 tareas, cuatro compuertas exclusivas, dos paralelas, un inicio condicional, dos esperas de tiempo, un fin, 35 flujos de secuencia y dos mensajes. Se observan rutas de contrato de obra, supervision o inspeccion y gestion de equipo complementario. Estas son **descripciones del archivo**, no roles, condiciones ni plazos acreditados para el GORE.

La copia conserva exactamente los bytes de la exportacion. No se corrige el XML recibido. El validador local informa D1 **esquema BPMN valido**, D2 **33 nodos sin asignacion semantica a un carril** (los tres carriles se ven en la imagen, pero no incluyen referencias `flowNodeRef` a sus nodos) y D3 **bloqueo en una compuerta paralela**, un participante sin evento de inicio y dos compuertas que ningun escenario alcanza. Los 35 flujos de secuencia y los dos de mensaje tienen identificadores de origen y destino existentes; esto no resuelve los hallazgos de D2 y D3. No se usa esta copia como `<codigo>-diagrama-proceso.bpmn`.

## Elementos registrados

| Elemento | Contenido | Clase | Fuente |
|---|---|---|---|
| Alcance declarado | Inicio de ejecucion contractual, solo construccion | `OBSERVADO` | Nombre del participante del exportado Bizagi |
| Secuencia de nivel 1 | S4.3.1 antecede a S4.3.2 Ejecucion | `DECISION` de modelamiento, pendiente de aprobacion institucional | `DEC-028`; mapa de S4.3 |
| Actividades y participantes | Los nombres del exportado son hipotesis para el contraste posterior | `REFERENCIA` | Exportado Bizagi recibido |

## Vacios de evidencia

| Vacio | Marca | Accion necesaria |
|---|---|---|
| Itinerario documental del contrato, acto y firmante de designacion del coordinador, comunicacion interna y delegaciones | `EVIDENCIA-INSUFICIENTE` | Cotejar expediente de contratacion, SGD, designacion, bases y contrato concretos; el ROF solo establece funciones generales |
| Otras oficinas y unidades ejecutoras que contratan o ejecutan obras | `EVIDENCIA-INSUFICIENTE` | Identificar entidad/UEI y sus instrumentos de competencia y operacion; preparar variante sin imponer la ruta GRA-GRI-SGGOS de la sede |
| Alcance de S4.3.1 fuera de solo construccion | `EVIDENCIA-INSUFICIENTE` | Revisar contrata, administracion directa y otros supuestos pertinentes sin extrapolar el BPMN recibido |
| Resultado del proceso y enlace con S4.3.2 | `EVIDENCIA-INSUFICIENTE` | Definir producto y hito de transferencia con el equipo |

## Discrepancias

| Hallazgo | Tratamiento |
|---|---|
| El archivo recibido contiene rutas y roles aun no contrastados y problemas D2/D3 | Conservar como evidencia intacta; reconstruir la tabla conceptual y generar el modelo de trabajo por la cadena BPMN del proyecto |
| El nombre del participante restringe el BPMN a solo construccion, mientras el proceso S4.3.1 puede tener mayor alcance | Registrar como limite del insumo; resolver el alcance durante la revision normativa y operativa |
| La primera tabla comenzaba en el carril del coordinador y rotulaba otro carril como entidad contratante no identificada | La entidad principal es el Gobierno Regional Huanuco; el coordinador es personal de SGGOS y recibe el contrato despues del tramite y su designacion. Se corrige la entrada y la pertenencia organizativa, sin presumir el documento que formaliza la designacion |

## Informacion BIM

`EVIDENCIA-INSUFICIENTE`. No se atribuyen requisitos BIM al archivo recibido.

## Contraste del Bizagi con el Reglamento

| Elemento observado en Bizagi | Exigencia normativa o ausencia de respaldo | Resultado para la tabla inicial |
|---|---|---|
| Inicia con recepcion del contrato y verificacion generica de condiciones | Art. 176.1: el inicio del **plazo** rige cuando se cumplen las condiciones aplicables; art. 176.3: la entidad inicia gestiones dentro de veintidos dias desde la firma, sin exigir que todas culminen entonces | Se conserva como disparador operativo y se explicitan las condiciones; no se equipara recepcion del contrato con inicio del plazo |
| Pregunta si cuenta con supervision; si no, designa equipo inspector | Ley, art. 62.4-62.5, y Reglamento, arts. 176.1 b y 186.1-186.4: debe comunicarse al contratista quien supervisa; si la obra requiere supervisor, un inspector o equipo de inspectores puede cubrir temporalmente solo con procedimiento de seleccion del supervisor convocado y hasta el umbral de valorizacion del art. 186.3 | Se reemplaza la comprobacion de mera capacidad interna por comprobacion de habilitacion legal; la ruta y controles de inspector se detallaran al obtener evidencia contractual |
| Preve designacion y contratacion de equipo complementario | Los arts. 176 y 186 examinados no hacen de ese equipo una condicion general del inicio | Se conserva como interfaz de contratacion por investigar; no se incorpora como requisito del flujo legal |
| Culmina con comunicacion al contratista para el inicio | Art. 176.1 b exige identificar al responsable de supervision en una comunicacion; el inicio del plazo depende de todas las condiciones aplicables. No se identifico en el art. 176 una obligacion general de acta de inicio | Se mantiene comunicacion como salida operativa propuesta, su forma y firma pendientes; no se afirma que el acta sea obligatoria |
| No muestra la actualizacion del expediente, adelanto, JPRD ni terreno como controles especificos | Art. 176.1 a, c, d y e, segun supuestos de aplicacion | Se agregan verificaciones explicitas; no se presume que todos los supuestos ocurren en cada contrato |
| Dos esperas de contratos y compuertas paralelas con bloqueo tecnico | El art. 176.7-176.9 permite diferir el inicio por acuerdo en supuestos tasados; el art. 176.4 regula consecuencias ante incumplimiento | Se reconstruyen esperas y reanudaciones sin bloqueo paralelo: contratacion de supervision o inspeccion transitoria habilitada, y acreditacion de las demas condiciones. El diferimiento y los efectos del incumplimiento siguen pendientes de modelamiento especifico |
| El diagrama padre S4.3 propone «Acta de inicio de obra» como salida de S4.3.1 | El art. 176 revisado no establece un acta general como condicion de inicio; puede existir exigencia en bases o procedimiento institucional no examinados | Se registra discrepancia con el padre para resolver al revisar bases y contrato; no se convierte el acta en requisito normativo de esta tabla |

**Inferencia de modelamiento:** concentrar en S4.3.1 la comprobacion de habilitacion y el hito de inicio, y dejar la adquisicion de equipo complementario como interfaz con S3.2. Requiere confirmacion del equipo. No es exigencia textual del Reglamento.

## Tratamiento de condiciones pendientes y reanudacion

| Situacion | Exigencia normativa | Propuesta logica y limite |
|---|---|---|
| No se cuenta con quien supervise | Reglamento, art. 176.1 b: comunicar al contratista quien supervisa; Ley, art. 62.5 y Reglamento, art. 186.4: inspeccion transitoria solo en el supuesto y limites previstos | Si no procede o no se opta por inspeccion, esperar la acreditacion del contrato de supervision y volver a verificar. Si procede gestionarla, el primer hecho acreditado entre contratacion de supervisor y designacion habilitada del inspector permite volver a verificar. Competencia y acto de designacion requieren evidencia institucional |
| Falta documentacion tecnica actualizada, adelanto directo, contrato JPRD o entrega de terreno | Reglamento, art. 176.1 a, c, d y e, segun aplicabilidad; el literal e corresponde a solo construccion | Coordinar con las unidades competentes y esperar la acreditacion del requisito aplicable. Cada hecho reabre la verificacion del conjunto; una sola acreditacion no implica que todas las condiciones esten cumplidas. Las rutas de cumplimiento de cada unidad son interfaces aun no levantadas |
| Persiste incumplimiento de condiciones | Reglamento, art. 176.4: consecuencias vinculadas al pedido del contratista y al plazo del numeral; art. 176.7-176.9: diferimiento por acuerdo y supuestos delimitados | El flujo de espera no representa por si mismo un diferimiento, una suspension ni una renuncia a remedios contractuales. Estos eventos y decisiones requieren un lote propio con expediente y competencia acreditados; la tabla actual no los da por ocurridos |

La antigua caja 12 (`F0`, fin por «condiciones pendientes») se retira: era una interrupcion logica improcedente para el alcance indicado por el usuario. Los numeros 1-11 y 13-17 conservan sus referencias; las nuevas cajas comienzan en 18. Los eventos condicionales representan hechos acreditados, no plazos nuevos ni decisiones automaticas. Su implementacion y la eventual concurrencia de requisitos necesitan revision del equipo.

## Cotejo institucional y ruta previa al coordinador

| Afirmacion | Clase | Evidencia y limite |
|---|---|---|
| El Gobierno Regional Huanuco puede ser entidad contratante para sus obras | Exigencia normativa propuesta | Ley 32069, art. 3.2 c; no convierte a la SGGOS en persona contratante separada |
| La GRA tiene funcion de suscribir contratos de ejecucion de obras en su ambito; Abastecimiento gestiona la obtencion de obras requeridas | Exigencia normativa propuesta | ROF, arts. 25 d y 29-30; para una unidad ejecutora distinta debe comprobarse su propio instrumento de competencia |
| La OACGD registra, deriva y tramita documentos y genera notificacion y archivo de contratos | Exigencia normativa propuesta | ROF, art. 20; la aplicacion exacta al contrato concreto y su canal documental siguen pendientes |
| La GRI monitorea proyectos de infraestructura y la SGGOS, dependiente de ella, controla y sigue obras | Exigencia normativa propuesta | ROF, arts. 92-94 y 97-98; justifica su participacion, no determina por si solo que GRI derive cada contrato a SGGOS |
| El contrato se notifica y se designa coordinador antes de que este lo tramite | Evidencia operativa declarada por el usuario | Precisado el 2026-11-18; el ROF no identifica al cargo coordinador ni fija instrumento, firmante o plazo de designacion |
| GRA remite, OACGD registra y notifica a GRI, GRI deriva a SGGOS y el subgerente designa y comunica al coordinador | Propuesta de modelamiento | Cajas 13-17 de la tabla. La secuencia es plausible por funciones y jerarquia, pero requiere expediente y trazas del SGD; no se declara regla normativa ni AS-IS confirmado |

La denominacion **UEI** identifica una responsabilidad en Invierte.pe y no prueba por si misma quien suscribe un contrato. La [orientacion oficial del MEF](https://www.mef.gob.pe/es/?Itemid=100674&id=6015&lang=es-ES&language=es-ES&option=com_content&view=article), consultada el 2026-11-18, admite que la UEI coincida con una unidad ejecutora presupuestal o sea una unidad de organizacion con competencias. Por ello, la ruta de este modelo corresponde a la sede y la SGGOS; para otra ejecutora se identificaran la unidad contratante y el organo encargado de la obra en el caso concreto.

**Limite de alcance:** la tabla cubre solo construccion. El art. 176 distingue ademas diseño y construccion, consultorias, ejecucion rapida y diferimiento. Estas variantes quedan pendientes; no se extrapola la ruta del Bizagi. El umbral de obligatoriedad del supervisor depende tambien de la Ley de Presupuesto del año fiscal correspondiente (art. 186.3), que no se contrasto en este lote.

## Generacion y revision del primer modelo

La [tabla editable](S4-3-1-diagrama-proceso-tabla.md) genero BPMN 2.0 XML, SVG, PNG y HTML interactivo el 2026-11-18. Tras incorporar las esperas y los retornos, la comprobacion focalizada D1-D5 no informa hallazgos. El PNG se reviso visualmente: las rutas de supervision/inspeccion y las cuatro acreditaciones se distinguen. La validacion es **tecnica del archivo generado**, no conformidad normativa, operativa o institucional. El BPMN de Bizagi permanece intacto y separado.

En la revision visual de la caja 3 se observo que tres retornos llegaban por arriba, comprimidos contra el borde del carril. El perfil `zigzag-controlado` ahora prueba dos entradas separadas por abajo para los hechos de supervisor contratado e inspector designado que provienen de la fila inferior; el retorno que nace en la fila principal sigue arriba y la primera entrada conserva el lado izquierdo. Se retiraron dos anotaciones redundantes bajo las cajas 3 y 6 para dejar libre el corredor; sus condiciones siguen en las notas de la tabla y en este sustento (arts. 176.1 a y 186.4 del Reglamento). El cambio es solo de disposicion, no una nueva regla del proceso.

La segunda revision visual detecto dos flechas de retorno apiladas sobre la caja 6 y los eventos 25-28 en una unica columna vertical. Se incorpora la caja 30 (`G4`), compuerta exclusiva de convergencia, para reunir las cuatro alternativas de acreditacion antes de volver a verificar los documentos tecnicos. Cada evento conserva su disparador y su numero; la compuerta no afirma que el cumplimiento de un solo requisito baste para iniciar el plazo. El perfil distribuye esas cuatro esperas en una fila horizontal cuando comparten carril y destino y hay celdas libres. El PNG pasa de 5250 x 4976 a 5610 x 3548 pixeles: 28,7 % menos altura, con 6,9 % mas ancho. D1-D5 quedan sin hallazgos. La convergencia y la colocacion son propuestas de modelamiento, pendientes de revision del equipo.

## Historial de revision

No se registran conformidades de `REVISION-EQUIPO`, `OPINION-TECNICA` ni `APROBACION`. Esta lectura inicial no valida el flujo.

## Paquete de contexto y relaciones

Fase logica conceptual con revision visual expresamente solicitada. Fuentes textuales activas: indice y sustento de S4.3, tabla S4.3.1, elementos del Bizagi recibido y articulos 176 y 186 del Reglamento y 62 de la Ley. El XML Bizagi es insumo observado; el BPMN generado no es fuente de reglas. La revision del PNG y la modificacion del perfil de trazado responden a la solicitud de corregir entradas, altura e intersecciones. Fuentes insuficientes para validar adscripciones institucionales, aplicabilidad contractual, gestion especifica del diferimiento/incumplimiento y alcance fuera de solo construccion.

- Se ubica bajo [S4.3 Ejecucion de la inversion](../00-S4-3-ejecucion-inversion.md).
- Entregara a [S4.3.2 Ejecucion](../S4-3-2-ejecucion/00-S4-3-2-ejecucion.md) el hito que se defina en el modelamiento posterior.

## Auditoría por afirmación — 2026-11-24 (fase 5)

Auditoría con el formato de DEC-057 ([informe generado](../../../../05-herramientas/gestor-modelos/auditorias/S4-3-1/informe.md)): 30 afirmaciones (17 `SUSTENTADA`, 13 `INFERENCIA`, sin contradicciones) y 15 obligaciones de los arts. 176, 179 y 186.4 del Reglamento, la Ley art. 62.5 y el ROF (arts. 20, 25, 93 y 97). Hay 6 obligaciones no representadas. Se crearon 41 anclas del visor calculadas desde el texto en `S4-3-1-fuentes-visor.json`. Son propuestas de IA, sin validación ni conformidad.

- **Condiciones del art. 176.1 a)-e):** todas representadas (T2-T6, C3-C6), así como la ruta del inspector temporal (Ley 62.5; Reglamento 186.4, texto vigente).
- **No representado:**
  - el plazo para iniciar las gestiones del 176.1: **22 días** desde la suscripción del contrato según el texto vigente del 176.3 (20 en el original);
  - las consecuencias del 176.4 cuando, requerida por el contratista, la entidad no cumple en 10 días: resarcimiento de hasta 0,05 % diario con tope del 3 %, o resolución;
  - el **diferimiento del inicio por acuerdo** (176.7), con suspensión del adelanto (176.8) y su formalización mediante acta de diferimiento y acta de reinicio publicadas en la Pladicop (176.9);
  - el plazo de 7 días para entregar el adelanto directo (179.2).
- **Acta de inicio:** práctica institucional en contrata que formaliza el cumplimiento de las condiciones (OBSERVADO, informado por el usuario el 2026-11-24). T7 comunica el cumplimiento sin acta, y F1 no la envía a S4.3.2, que la espera. Es un candidato de interfaz.
- **Ruta documental inicial** (GRA, OACGD, GRI, SGGOS, de E1 a T0E): coherente con las funciones del ROF, pero la secuencia concreta sigue siendo inferencia hasta cotejarla con un expediente y con el SGD. La designación del coordinador no figura en el ROF.
- **C1 y C1B** tienen el mismo nombre («Supervisor contratado») en ramas distintas; conviene distinguirlos.
- **Propuestas no aplicadas:**
  - T7 como «Suscribir acta de inicio» y F1 enviándola a S4.3.2;
  - anotar el plazo de 22 días en T1;
  - una ruta de diferimiento por acuerdo con sus actas;
  - una anotación sobre el requerimiento del contratista y sus consecuencias.

