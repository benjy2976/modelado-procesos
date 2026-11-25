---
id: AP-S4-3-2-2-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S4.3.2.2
nivel_proceso: 3
proceso:
  - S4.3.2.2
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-18
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-2
---

# S4.3.2.2 Atencion de consultas de obra - Sustento

Sube a: [S4.3.2.2 Atencion de consultas de obra](00-S4-3-2-2-atencion-consultas-obra.md)

## Fuentes utilizadas

| Fuente | Ubicacion precisa | Estado | Uso |
|---|---|---|---|
| Exportacion Bizagi de Consultas | `99-temporal/modelos/sggos-2026-11-02-bpmn/consultas-bizagi.bpmn`, participantes Eventualidades de Obra y Proyectista | `OBSERVADO`; BPMN invalido por flujo de mensaje incompleto, referencia grafica rota y nodos no alcanzados | Actividades de recepcion, evaluacion, opinion y notificacion de consultas |
| Reglamento de la Ley 32069 | Art. 190 | `NORMATIVO` citado; regla pendiente de validacion | Tratamiento de consultas de obra |
| Directiva 017-2023-CG | Num. 7.3.7 b | `NORMATIVO` citado; regla pendiente de validacion | Consulta como posible causal de ampliacion en administracion directa |
| ROF del Gobierno Regional Huanuco 2023 | Arts. 95-98; en especial art. 96, lit. i, PDF pp. 47-48 (numeracion impresa pp. 46-47) | `NORMATIVO-INSTITUCIONAL` propuesto; pendiente validacion humana | Competencia de SGE para absolver consultas y de SGGOS para controlar y seguir la ejecucion |
| Decision del equipo | `DEC-032` | `DECISION` | Codigo, nombre, limites y adopcion como nivel 3 |
| Decision del equipo | `DEC-033` | `DECISION` y evidencia operativa | Especialistas de la SGE elaboran el informe tecnico; el Subgerente de Estudios firma siempre la respuesta; carriles institucionales del modelo |
| Precision operativa del usuario | Instruccion recibida el 2026-11-17 sobre intervencion condicional del especialista de supervision, anotacion en el Cuaderno de Incidencias y tramite SGGOS–SGE–SGGOS | `PROPUESTA` operativa, pendiente de contraste institucional | Reordenar las rutas del supervisor y la comunicacion de la respuesta firmada |

## Delimitacion aplicada

El Bizagi de Consultas contiene tambien suspension y aprobacion de adicionales o reducciones. Esas ramas no forman parte del producto "consulta absuelta": se utilizan como insumo de S4.3.2.3 a S4.3.2.6, segun la figura. Este proceso termina al notificar la respuesta y, cuando corresponda, al comunicar la solicitud o causal.

## Elementos registrados

| Elemento | Contenido | Clase | Fuente |
|---|---|---|---|
| Disparador | Consulta registrada en el Cuaderno de Incidencias | `NORMATIVO` citado | Reglamento, art. 190; terminologia institucional DEC-041 |
| Instancia | Una por consulta | `DECISION` | DEC-032 |
| Participantes | Ejecutor de obra por contrata, supervision contratada, GORE Huanuco y proyectista cuando corresponda | `OBSERVADO` y `NORMATIVO` citado | Bizagi; Reglamento, art. 190; ROF, arts. 95-98; DEC-042 |
| Responsable de la absolucion tecnica en el GORE Huanuco | Sub Gerencia de Estudios (SGE) | `NORMATIVO-INSTITUCIONAL` propuesto | ROF, art. 96, lit. i |
| Seguimiento y canalizacion institucional | Sub Gerencia de Gestion de Obras y Supervision (SGGOS) | `NORMATIVO-INSTITUCIONAL` propuesto e `INFERENCIA` de modelamiento | ROF, arts. 97-98; el circuito documental exacto requiere evidencia operativa |
| Elaboracion del sustento de la respuesta | Especialistas de la SGE elaboran el informe tecnico de absolucion | `OBSERVADO` y `DECISION` | Descripcion del equipo; DEC-033 |
| Firma de la respuesta | El Subgerente de Estudios revisa y firma siempre la respuesta a la consulta | `OBSERVADO` y `DECISION` | Descripcion del equipo; DEC-033 |
| Consulta originada por la supervision | Puede elevarse sin consulta previa del contratista | `OBSERVADO` | Descripcion del equipo; caso excepcional |
| Producto principal | Consulta absuelta y notificada | `PROPUESTA` | Analisis del flujo observado |
| Producto alterno | Respuesta y causal comunicadas a S4.3.2.3, .4, .5 o .6 | `PROPUESTA` | DEC-041 |

## Precision operativa del 2026-11-17

El usuario indico que el supervisor anota en el Cuaderno de Incidencias tanto la absolucion como la elevacion de la consulta a la entidad. Si la materia requiere opinion del especialista de la supervision, este revisa y se pronuncia antes de decidir si el supervisor puede absolver; el supervisor hace suyo ese pronunciamiento. La intervencion del especialista es condicional, no un paso obligatorio de toda consulta.

En el tramo institucional, el subgerente de SGGOS recibe y tramita la consulta a SGE, con intervencion del monitor de obras. Despues de la caja 39, SGE comunica a SGGOS la respuesta firmada; SGGOS prepara la carta dirigida al contratista. La frase del usuario termino en «el monitor proyecta» sin identificar el documento. Como `INFERENCIA` provisional, la tabla asigna al monitor el proyecto de esa carta y al subgerente su emision; ambos pasos quedan pendientes de precision del usuario. El canal de notificacion, la firma concreta de la carta y la remision de la causal a los procesos S4.3.2.3–S4.3.2.6 permanecen por confirmar. La ruta anterior SGE → supervisor → contratista se reemplazo por la comunicacion SGE → SGGOS → contratista en esta propuesta.

La caja 39 y los demas numeros vigentes se conservaron. Las cajas 21 y 22, de la antigua recepcion de respuesta por la supervision, se retiraron sin reutilizar sus numeros. Los elementos nuevos reciben los numeros 48–54. La consulta propia de la supervision conserva su ruta excepcional; la precision actual se concentra en la consulta recibida del ejecutor.

## Vacios de evidencia

| Vacio | Marca | Fuente o accion necesaria |
|---|---|---|
| Nombre, serie documental, custodia y medio exacto de notificacion | `EVIDENCIA-INSUFICIENTE` | Procedimiento documentario o muestra no sensible del tramite real |
| Criterio exacto para involucrar al proyectista | `EVIDENCIA-INSUFICIENTE` | Fuente contractual, expediente y validacion del equipo |
| Acto de emision de la carta de SGGOS y responsable concreto de elaborar el adicional | `EVIDENCIA-INSUFICIENTE` | Verificar el circuito de emision y las bases de contratacion aplicables; la instruccion del 2026-11-18 precisa que el monitor prepara la carta |
| Variante con inspector perteneciente a la entidad | `EVIDENCIA-INSUFICIENTE` | Levantamiento del circuito interno aplicable |
| Indicador, meta y fuente de datos | `EVIDENCIA-INSUFICIENTE` | Definicion del dueno del proceso |

## Discrepancias

| Hallazgo | Tratamiento |
|---|---|
| El Bizagi no tiene evento de inicio general y contiene enlaces sin pareja | No se copia el XML; se adopta como inicio el mensaje de consulta anotada y se reconstruye el flujo |
| El Bizagi mezcla consulta con suspension y adicional | Se separan mediante los limites entre S4.3.2.2 y S4.3.2.3 a S4.3.2.6 |
| El Bizagi representa a la entidad sin distinguir sus unidades internas | El rediseño debe separar al menos SGGOS y SGE: SGGOS recibe, sigue y canaliza; SGE analiza y absuelve tecnicamente conforme al ROF |

## Criterio para el rediseño institucional

La exigencia nacional de que la entidad absuelva la consulta se concreta, para el Gobierno Regional Huanuco, mediante la competencia asignada a la SGE por el articulo 96, literal i, del ROF. Por tanto, el modelo no debe dejar la absolucion sustantiva en una actividad generica de la entidad ni atribuirla al rol Monitor.

La SGGOS conserva un papel diferenciado de control, seguimiento, recepcion y canalizacion del tramite. Cuando se requiera opinion del proyectista, la SGE conduce el analisis tecnico y continua hasta producir la absolucion institucional aun si el proyectista no se pronuncia dentro del plazo aplicable. El modelo utiliza una compuerta basada en eventos para esperar la opinion o el vencimiento del plazo, rutas que convergen en la elaboracion del informe tecnico de absolucion.

`DEC-033` cierra el vacio operativo de autoria y firma: los especialistas de la SGE elaboran el informe tecnico y el Subgerente de Estudios revisa y firma siempre la respuesta. Esta precision proviene del equipo y no se presenta como una exigencia extraida del ROF. La OACGD registra la entrada y canaliza la notificacion; la denominacion y serie exactas de los documentos permanecen pendientes.

El diagrama base representa supervision contratada como participante externo. Si la obra cuenta con inspector, este pertenece a la entidad y sus actividades deben reubicarse en el pool del GORE Huanuco; no se lo representa como un participante externo equivalente al supervisor.

`DEC-042` precisa ademas que el pool Ejecutor de obra por contrata contiene al residente y a su equipo especialista como carriles internos, no como participantes independientes. El pool Supervision contratada representa solo al supervisor externo. La variante de administracion directa y el circuito con inspector de la entidad siguen como `EVIDENCIA-INSUFICIENTE` hasta levantar el flujo institucional correspondiente.

Fuente de lectura: [Guia del ROF del Gobierno Regional Huanuco 2023](../../../../../03-conocimiento/fuentes/guia-rof-grh-2023.md).

## Pilotos de visualizacion

La primera generacion valida ocupaba 6940 x 2821 px en SVG. La evidencia observada fue un desplazamiento horizontal acumulativo: cada flujo de mensaje entre participantes agregaba una columna, aun cuando el receptor iniciaba la etapa que el emisor acababa de cerrar. Tambien existian separaciones uniformes mayores que las requeridas por varios elementos.

Como propuesta tecnica (`DEC-034`), este modelo activa `perfil_trazado: equilibrado`. El perfil no cambia nodos, secuencias, mensajes, carriles ni productos; modifica solamente las coordenadas BPMN-DI. Emisor y receptor de un mensaje comparten etapa visual, el ancho entre columnas se calcula segun los simbolos y sus etiquetas, y se reducen moderadamente los espacios verticales. Los simbolos conservan su tamaño.

El derivado equilibrado mide 5226 x 2514 px en SVG: 24,7 % menos ancho y 10,9 % menos alto que la primera generacion, con D1-D5 sin hallazgos. La apreciacion visual posterior considero que todavia desperdiciaba demasiado espacio horizontal; se conserva como antecedente temporal y no como solucion aceptada.

La segunda propuesta tecnica (`DEC-035`) activa `perfil_trazado: zigzag-controlado`. El perfil elimina por participante las etapas sin actividad y pliega la secuencia solamente cuando supera 16 columnas. El tramo siguiente baja y cambia de sentido; los mensajes de ida y vuelta se conducen por niveles separados entre pools. Las pruebas intermedias con limites de 8 y 12 columnas fueron descartadas porque producian una composicion excesivamente vertical.

El nuevo derivado mide 2568 x 2923 px en SVG. Frente al perfil equilibrado reduce 50,9 % el ancho y 42,9 % el area, con un aumento de 16,3 % en la altura; frente a la primera generacion reduce 63,0 % el ancho y 61,7 % el area. D1-D5 no presentan hallazgos. Es evidencia tecnica de un piloto pendiente de apreciacion visual del equipo; no constituye conformidad ni aprobacion del contenido del proceso.

## Informacion BIM

`EVIDENCIA-INSUFICIENTE`. La posible consulta sobre modelos o informacion BIM requiere fuentes y requisitos expresos antes de modelarse.

## Historial de revision

| Documento | Nivel | Fecha | Resultado | Rol o unidad | Evidencia |
|---|---|---|---|---|---|
| Juego inicial S4.3.2.2 | `ELABORACION` | 2026-11-03 | Propuesta creada; pendiente revision | Equipo del proyecto con asistencia de IA | DEC-032; exportacion Bizagi |
| Rediseño institucional S4.3.2.2 | `ELABORACION` | 2026-11-03 | Pools, carriles, opinion del proyectista, informe tecnico y firma incorporados; pendiente revision | Equipo del proyecto con asistencia de IA | DEC-033; ROF, arts. 95-98; Reglamento, art. 190 |
| Piloto de visualizacion equilibrada | `ELABORACION` | 2026-11-03 | Geometria compactada; D1-D5 sin hallazgos; pendiente apreciacion visual | Equipo del proyecto con asistencia de IA | DEC-034; informe de validacion del gestor |
| Piloto de visualizacion zigzag controlado | `ELABORACION` | 2026-11-04 | Geometria replegada a 16 columnas; D1-D5 sin hallazgos; pendiente apreciacion visual | Equipo del proyecto con asistencia de IA | DEC-035; informe de validacion del gestor |
| Precision de participantes | `ELABORACION` | 2026-11-05 | Ejecutor de obra por contrata confirmado como participante que contiene residente y especialistas; variante con inspector permanece pendiente | Equipo del proyecto con asistencia de IA | `DEC-042` |

## Relaciones

- [S4.3.2.3 Gestion de modificaciones de alcance](../S4-3-2-3-gestion-adicionales-deductivos-obra/00-S4-3-2-3-gestion-adicionales-deductivos-obra.md)
- [S4.3.2.4 Gestion de ampliaciones de plazo](../S4-3-2-4-gestion-ampliaciones-plazo/00-S4-3-2-4-gestion-ampliaciones-plazo.md)
- [S4.3.2.5 Formalizacion de suspensiones de plazo](../S4-3-2-5-formalizacion-suspensiones-plazo/00-S4-3-2-5-formalizacion-suspensiones-plazo.md)
- [S4.3.2.6 Gestion de paralizacion y reinicio](../S4-3-2-6-gestion-paralizacion-reinicio/00-S4-3-2-6-gestion-paralizacion-reinicio.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)


## Mejora del perfil zigzag-controlado ? 2026-11-06

Por solicitud del usuario se aplica la mejora general del perfil: compactacion de circuitos independientes y seleccion de corredores de mensajes con control de interferencias. Se conserva la semantica BPMN; no cambian actividades, responsables ni relaciones del proceso. D1, D2, D3 y D5 sin hallazgos. D4 sin hallazgos.

## Convencion de carriles y SGD

Se aplica la [convencion de carriles y SGD](../../../../../00-gobernanza/estandar-artefactos-modelamiento.md#74-convencion-de-carriles-y-sgd-en-s432) de `DEC-043`. El pool de contrata se titula Contratista y conserva carriles separados para residente y especialistas; Supervision contratada conserva su pool externo. OACGD, SGGOS y SGE usan el patron unidad y funcion. El registro y las asignaciones o derivaciones internas de la consulta se representan con tareas humanas y `almacen: SGD`. La ruta con inspector de la entidad no se infiere de esta variante y permanece pendiente.

La generacion focalizada de la normalizacion de 2026-11-10 dejo D1-D5 sin hallazgos en esa fecha. No se atribuye conformidad institucional.

En la propuesta del 2026-11-17, D1, D2, D3 y D5 no presentan hallazgos. D4 detecta 15 interferencias geometricas (un flujo que atraviesa una forma, seis tramos superpuestos, cinco etiquetas montadas y dos cruces de flujo con etiquetas); se redujeron desde 17 al acortar rotulos y retirar documentos graficos redundantes. Es un pendiente de disposicion visual, no una conformidad del contenido. La fuente tabular conserva la secuencia; el informe reproducible queda en `99-temporal/modelos/S4-3-2-2-diagrama-proceso/validacion.txt`.

## Aplicacion del articulo 190 - 2026-11-17

**Paquete de contexto del lote conceptual:** S4.3.2.2, variante por contrata con supervision externa. Fuentes textuales activas: indice, ficha, tabla y este sustento; guia local CON-001 y numerales 190.1-190.3 del Reglamento. Glosario: informe tecnico del contratista, opinion tecnica del supervisor y expediente tecnico son objetos distintos. Se preserva la evidencia operativa previa. No hay reglas validadas incorporadas por este lote. BPMN, SVG, PNG y HTML quedan excluidos del contexto; se regeneran al cierre. No corresponde revision visual en esta tarea ni esta autorizada la modificacion de herramientas. Se mantienen codigo, alcance y participantes.

**Exigencia normativa propuesta, pendiente de validacion humana:** el art. 190.1 permite la respuesta directa del supervisor cuando la consulta no implica modificar el expediente tecnico. El art. 190.2 exige que la anotacion del contratista que implique esa modificacion incluya un informe tecnico y dispone su no atencion si falta. El informe del contratista es distinto de la opinion del supervisor prevista para la elevacion en el art. 190.3.

**Fuente oficial y vigencia:** consulta del 2026-11-17 al [texto actualizado de El Peruano](https://diariooficial.elperuano.pe/Normas/obtenerDocumento?idNorma=25), Reglamento aprobado por DS 009-2025-EF, art. 190, numerales 190.1, 190.2 y 190.3; referencia local CON-001, pagina PDF 105, identificada en la [guia de lectura](../../../../../03-conocimiento/fuentes/guia-reglamento-ley-32069.md). El numeral 190.1 fue modificado por el [DS 001-2026-EF, articulo 2](https://busquedas.elperuano.pe/dispositivo/NL/2474920-3), vigente desde el 2026-01-14 segun el [compendio del OECE](https://www.gob.pe/institucion/oece/colecciones/45029-ley-n-32069-ley-general-de-contrataciones-publicas-y-su-reglamento). La modificatoria no sustituye el numeral 190.2. Aplicabilidad al contrato concreto y validacion humana pendientes; no se constituye linea base normativa.

**Propuesta de modelamiento:** la caja 2 hace obligatorio preparar el informe si se modifica el expediente. La caja 12 pregunta expresamente por esa modificacion: No permite absolver; Si conduce a la caja 55, que comprueba el informe antes de elevar. Su ausencia termina en la caja 56 sin absolucion. La caja 57 controla el mismo supuesto al revisar antecedentes en SGGOS: solo si es consulta del contratista, modifica el expediente y carece del informe termina en la caja 58 sin atencion; en los demas casos continua el tramite. Esta ubicacion del control en el monitor es una propuesta operativa, no una competencia asignada expresamente por el art. 190.2. Se conservan todos los numeros anteriores.

**Limites y vacios:** la no atencion no equivale a denegacion de fondo ni aprobacion de una modificacion. No se inventan plazo de subsanacion, acto de rechazo ni canal de comunicacion: `EVIDENCIA-INSUFICIENTE`. La consulta propia de la supervision conserva su ruta excepcional y no se confunde con la anotacion del contratista regulada en el numeral 190.2. La especialidad que elabora el informe y la opinion interna de supervision conservan su condicion operativa previa.

**Control del lote del articulo 190:** D1, D2, D3 y D5 sin hallazgos. D4 registra 17 interferencias: T1 (1), T2 (5), T4 (7) y T6 (4). Afectan el ramal de falta de informe del supervisor, etiquetas y mensajes cercanos y el tramo de comunicacion SGE-SGGOS ya observado. Se conservan como pendientes de disposicion visual; no alteran las conexiones verificadas por D2-D3. Se usa `--forzar` exclusivamente para actualizar los derivados del borrador con estos hallazgos documentados, sin modificar herramientas ni atribuir conformidad. Antes de una linea base deben resolverse en revision visual. Detalle reproducible: `99-temporal/modelos/S4-3-2-2-diagrama-proceso/validacion.txt`.

## Informe tecnico de supervision para la entidad

Precision operativa recibida del usuario el 2026-11-17: la consulta requiere el informe del contratista en el supuesto ya delimitado y, para elevarla a la entidad, el supervisor debe emitir ademas su propio informe tecnico con la evaluacion y opinion sobre su viabilidad. Se incorpora como `PROPUESTA` operativa en `ELABORACION`, sin atribuir validacion normativa ni conformidad institucional.

Se mantiene el paquete conceptual del lote anterior, sus fuentes textuales y exclusiones de derivados; no se autoriza modificar herramientas ni se realiza revision visual. La nueva caja 59, S-T8, es obligatoria antes de la elevacion S-T4, tanto para la consulta del contratista que pasa el control del informe como para la consulta propia de la supervision. No depende de que intervenga un especialista. Su pronunciamiento, si existe, alimenta la evaluacion que el supervisor asume y formaliza en su informe. Los numeros anteriores se conservan.

La entidad recibe el informe tecnico de supervision junto con la consulta y el informe del contratista cuando corresponde. El monitor verifica esos antecedentes y SGE los utiliza para evaluar la consulta. Son documentos distintos: el contratista sustenta su consulta; la supervision evalua y emite su opinion tecnica; SGE produce el informe institucional de absolucion.

La denominacion documental y el paso explicito de emision provienen de esta instruccion del usuario. La referencia normativa del art. 190.3 a la opinion tecnica conserva la fuente, fecha de consulta y vigencia documentadas en la seccion anterior; no se le atribuye una exigencia literal adicional. La opinion sobre viabilidad no se modela como aprobacion de una modificacion ni se presume siempre favorable. El tratamiento documental de un informe de supervision omitido permanece como `EVIDENCIA-INSUFICIENTE`; no se extiende automaticamente la consecuencia del art. 190.2 a otro documento.

Control de este lote: D1, D2, D3 y D5 sin hallazgos; D4 registra 14 interferencias geometricas pendientes de revision visual. Se retiraron anotaciones graficas redundantes conservando su contenido en las notas textuales y este sustento. Se regeneran los derivados con `--forzar` bajo la misma justificacion del lote anterior: mantener el borrador sincronizado, sin conformidad visual ni linea base. El detalle actualizado permanece en `99-temporal/modelos/S4-3-2-2-diagrama-proceso/validacion.txt`.


## Carta de respuesta y revision del trazado - 2026-11-18

**Paquete de contexto:** fase conceptual y disposicion visual solicitada expresamente por el usuario para S4.3.2.2. Fuentes textuales activas: indice, ficha, tabla y sustento del proceso; estandar de artefactos y documentacion del gestor. Evidencia activa: instruccion del usuario sobre la caja 52 y las flechas. No se incorporan reglas normativas nuevas. Glosario: comunicar quien elabora el adicional no equivale a elaborarlo ni aprobarlo. BPMN, SVG, PNG y HTML del proceso se incluyen solo para comprobar la geometria; los derivados de otros procesos quedan excluidos del contexto. Se mantienen alcance, participantes, IDs, numeros y conexiones.

**Precision operativa del usuario:** el monitor prepara la carta de respuesta al contratista en la caja 52. Si corresponde un adicional, la carta debe comunicar a quien corresponde elaborarlo segun las bases de contratacion. Esta instruccion resuelve la inferencia provisional sobre el documento de salida del monitor registrada el 2026-11-17. Se incorpora como propuesta operativa en `ELABORACION`, sin atribuir aprobacion institucional ni validacion normativa. La firma y el acto de emision siguen pendientes de corroboracion.

**EVIDENCIA-INSUFICIENTE:** no se han aportado las bases del contrato concreto; no se identifica ni presume el elaborador del adicional. Su determinacion requiere consultar esas bases. La elaboracion y tramitacion del adicional permanecen fuera de este proceso de consultas, vinculadas a S4.3.2.3.

**Bloqueo tecnico observado:** antes del ajuste, D4 reporto 14 interferencias con `zigzag-controlado`, 11 con `zigzag-amplio` y 18 con `equilibrado`; todos conservaron un flujo atravesando una forma. El enrutador elegia un candidato con interferencias cuando no encontraba ruta libre y no reservaba las etiquetas de documentos como obstaculos. Esto justifica la intervencion minima en el generador para satisfacer la solicitud de rodear las cajas.

**Propuesta tecnica acotada:** perfil optativo `zigzag-corredores`, basado en `zigzag-controlado`, aplicado solo a este proceso. Compara entradas y salidas por los cuatro lados, reserva documentos y sus etiquetas, penaliza tramos compartidos y separa puertos de mensajes y secuencias. Conserva los perfiles anteriores y la semantica BPMN. No representa una nueva notacion ni una conformidad humana. La generacion focalizada y la revision visual verifican el resultado; el control global comprueba que los demas modelos siguen sincronizados.

**Resultado verificado:** la generacion focalizada del 2026-11-18 termina sin hallazgos D1-D5; D4 informa sin superposiciones. Se inspecciono la imagen generada, incluidos el ramal de falta de informe, la comunicacion de respuesta y la caja 52. Se mantienen posibles cruces perpendiculares entre flujos en una colaboracion con varios carriles; no equivalen a atravesar cajas ni a compartir tramos. Perfil documentado en `DEC-045`; revision humana y aprobacion institucional no atribuidas.

**Comprobaciones de cierre:** cuatro pruebas de regresion del trazado superadas, comprobacion global `construir_modelos.py --check` correcta y 172 notas revisadas por `gestionar_etiquetas.py revisar`, sin problemas. Los hallazgos historicos de otros procesos no se modifican ni se declaran resueltos.

## Auditoría por afirmación — 2026-11-24 (fase 5)

Auditoría con el formato de DEC-057 ([informe generado](../../../../../05-herramientas/gestor-modelos/auditorias/S4-3-2-2/informe.md)): 64 afirmaciones (36 `SUSTENTADA`, 28 `INFERENCIA`, sin contradicciones) y 12 obligaciones del Reglamento art. 190 (texto vigente) y del ROF art. 96. Se crearon 41 anclas del visor calculadas desde el texto. Son propuestas de IA, sin validación ni conformidad.

- **Bien representado:** la ruta de solo construcción del art. 190: consulta por cuaderno, respuesta directa del supervisor sin modificación, informe técnico obligatorio con su control doble, opinión del proyectista en 10 días y absolución en 5. La Sub Gerencia de Estudios absuelve conforme al ROF art. 96.
- **No representado:**
  - el 190.4: si la consulta no se absuelve en plazo, el contratista puede pedir ampliación de plazo, y no hay vínculo con S4.3.2.4;
  - la exigencia de anticipación del 190.5.
- **Plazos y condiciones por anotar:**
  - los 5 días del supervisor para elevar la consulta con su opinión (190.3 a);
  - el límite de un año desde la conformidad del expediente para consultar al proyectista, que la compuerta E-G1 («¿Aplica?») no nombra.
- **Interfaz:** E-T10 comunica una causal de modificación sin mensaje hacia S4.3.2.3-S4.3.2.6. S4.3.2.3 declara recibir de este proceso una «respuesta notificada como antecedente» que aquí no se envía.
- **La ruta de diseño y construcción** (190.3 b) queda fuera del alcance modelado.
- **Propuestas no aplicadas:**
  - un evento o anotación para la ampliación de plazo del 190.4;
  - el plazo de 5 días en S-T4;
  - la condición del año en E-G1;
  - un mensaje explícito hacia los procesos de modificación.

## Cambios aplicados — 2026-11-25 (DEC-058)

- **Interfaz con S4.3.2.3.** E-F1 envía además la respuesta como antecedente a S4.3.2.3, que la recibe en R-E1. Una anotación precisa que solo es relevante cuando la respuesta identifica un adicional (E-G3).
- **Causal de ampliación (190.4).** Se anota en el inicio de S4.3.2.4, no aquí; la obligación queda pendiente de una salida explícita si el equipo lo decide.
- **Generación.** D1-D5 sin hallazgos nuevos.

La auditoría se reconfirmó sobre la nueva revisión de la tabla ([informe generado](../../../../../05-herramientas/gestor-modelos/auditorias/S4-3-2-2/informe.md)). Son propuestas de IA; no se atribuye validación ni conformidad y el proceso sigue en `ELABORACION`.
