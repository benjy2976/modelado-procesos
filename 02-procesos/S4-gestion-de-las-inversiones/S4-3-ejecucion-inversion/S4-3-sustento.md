---
id: AP-S4-3-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S4.3
nivel_proceso: 1
proceso:
  - S4.3
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3
---

# S4.3 Ejecucion de la inversion - Sustento

Sube a: [S4.3 Ejecucion de la inversion](00-S4-3-ejecucion-inversion.md)

Registra las fuentes, evidencias, vacios e historial de revision que sustentan los documentos de S4.3. No se exporta a PDF.

## Fuentes utilizadas

| Fuente | Ubicacion precisa | Estado | Uso |
|---|---|---|---|
| [Ficha institucional S4](../../../01-referencias/01-institucionales-grh/originales/s4-gestion-inversion.pdf), SHA-256 `F86C31E6A6BDFFBDBF7D5186BFD21E1FD58522BC546E0127296BD8C461931F83` | Paginas PDF 1-4; paginas impresas 120-123; fila S4.3 | Aprobada (`DEC-016`); transcripcion pendiente de conformidad de fidelidad | Responsable, entradas y productos de S4.3 |
| [NT 002-2025-PCM-SGP](../../../01-referencias/02-gestion-por-procesos/originales/nt-002-2025-pcm-sgp/norma-tecnica-n-002-2025-pcm-sgp-f-f.pdf) | Numerales 6.1.2 a 6.1.4; Anexos 1 a 8 | Vigencia juridica por confirmar; regla no curada | Estructura y contenido minimo de los documentos |

## Elementos observados

Clase: `OBSERVADO` en la fuente institucional aprobada. Se transcriben tal como figuran en la [ficha de S4](../S4-ficha-producto-proceso.md).

| Elemento | Texto observado | Contraparte |
|---|---|---|
| Responsable consignado | Sub Gerencia de Gestion de Obras y Supervision; unidades ejecutoras que pertenecen al GRH | - |
| Entrada | Expediente tecnico, documento equivalente aprobado y/o EETT | S4.2 Elaboracion del expediente tecnico |
| Entrada | Convenios | Gobiernos Nacional, Regional y Local |
| Entrada | Servicio contratado / bien adquirido / consultoria y obra contratada | S3.2 Contratacion de bienes y servicios |
| Producto | Designacion de personal y/o requerimiento de contratacion de consultoria de obra/bienes y servicios | S3.1 Programacion de bienes y servicios |
| Producto | Reporte de inversiones ejecutadas | MEF / INFOBRAS |
| Producto | Expediente para pagos | S2.1 Gestion Contable |
| Producto | Informacion tecnico y financiero para liquidacion ET | S4.4 Liquidacion, transferencia y cierre de inversion |
| Producto | Informe de estado situacional del Proyecto/programa o IOARR por saldo de obra | S4.2 Elaboracion del expediente tecnico |

## Vacios de evidencia

| Vacio | Marca | Fuente o accion necesaria |
|---|---|---|
| Ficha de producto y proceso propia de S4.3 | `EVIDENCIA-INSUFICIENTE` | No existe en las fuentes recibidas; debe elaborarse conforme al numeral 6.1.2, paso 3 de la NT |
| Objetivo del proceso S4.3 | `EVIDENCIA-INSUFICIENTE` | Definicion del dueno del proceso |
| Condicion del responsable consignado como dueno del proceso S4.3 | `EVIDENCIA-INSUFICIENTE` | Confirmacion del dueno o documento de organizacion vigente |
| Procesos Nivel 2 y sus procedimientos | `EVIDENCIA-INSUFICIENTE` | Descomposicion aprobada de S4.3 |
| Indicadores propios de S4.3 | `EVIDENCIA-INSUFICIENTE` | Definicion del dueno del proceso |

## Insumos recibidos

| Insumo | Fecha | Clase | Autor | Archivo |
|---|---|---|---|---|
| Propuesta de descomposicion de S4.3 en tres subprocesos (diagrama BPMN) | 2026-10-16 | `PROPUESTA` | Equipo del proyecto | [S4-3-insumo-propuesta-descomposicion-equipo.png](S4-3-insumo-propuesta-descomposicion-equipo.png) |

Pendientes de recibir:

- Levantamientos del equipo sobre S4.3. Se registraran como insumos con su clase de conocimiento, no como fuentes aprobadas.
- Documento interno para elaborar fichas, aun no aprobado. Se registrara como referencia de trabajo.

## Evaluacion de la propuesta de descomposicion del equipo

Evaluacion preparada por IA el 2026-10-16. Clase `INFERENCIA`: contrasta la propuesta con reglas en estado `BORRADOR-IA` y con buenas practicas BPMN; requiere validacion humana. Las fuentes se resumen en las [guias de lectura](../../../03-conocimiento/fuentes/00-fuentes.md).

### Propuesta observada

| Elemento | Contenido del diagrama |
|---|---|
| Pool principal | S4.3 Ejecucion de la inversion, sin carriles |
| Pools externos | S4.2 Elaboracion del expediente tecnico; S4.4 Liquidacion, transferencia y cierre |
| Flujo | Inicio -> compuerta "Obra?" (solo salida Si) -> compuerta "Solo construccion?" -> Si: S4.3.1 Procura -> "Acta de inicio de obra" -> S4.3.2 Ejecucion -> "Obra concluida o con contrato resuelto" -> S4.3.3 Recepcion -> "Obra recepcionada" -> compuerta -> Fin. No: va directo a S4.3.2 Ejecucion |
| Mensajes | Desde S4.2 hacia Procura: expediente tecnico o documento equivalente. Desde Recepcion hacia S4.4: informacion tecnico y financiera de liquidacion de la inversion |
| Alcance declarado por el equipo | Procura: todo lo previo al acta de inicio de obra o su equivalente. Ejecucion: la ejecucion propiamente dicha. Recepcion: recepcion de obra concluida o cierre con contrato resuelto; luego pasa a S4.4 |

### Coincidencias con la normativa

| Hallazgo | Sustento |
|---|---|
| Los tres subprocesos corresponden a etapas reconocidas: preparacion previa al inicio, ejecucion fisica y culminacion | `REG-INV-EJEC-001`; `REG-CGR-AD-001` (fases de administracion directa) |
| El acta de inicio es un limite adecuado entre S4.3.1 y S4.3.2: el plazo de obra rige al cumplirse condiciones previas definidas | `REG-CON-OBRA-002`; Directiva 017-2023-CG num. 7.3.1 |
| La entrada desde S4.2 y la salida hacia S4.4 coinciden con las interacciones aprobadas de la ficha S4 | Ficha S4, paginas impresas 120-121 |
| La pregunta "Solo construccion?" corresponde a un sistema de entrega normado | `REG-CON-OBRA-001` |

### Observaciones

| N | Observacion | Sustento | Sugerencia |
|---|---|---|---|
| O1 | Faltan interacciones aprobadas en la ficha S4: S3.1 (requerimiento de contratacion), S3.2 (obra o servicio contratado), S2.1 (expediente para pagos), MEF / INFOBRAS (reporte), Gobiernos (convenios) y S4.2 (estado situacional por saldo de obra) | Ficha S4, p. 120-121; seccion Interacciones de la portada de S4.3 | Agregarlas como flujos de mensaje; S3.1 y S3.2 son el nucleo de la procura |
| O2 | La compuerta "Obra?" solo tiene la salida "Si": no indica que ocurre con inversiones que no son obra (IOARR de equipamiento, bienes o servicios), aunque la fase de Ejecucion aplica a proyectos e IOARR | `REG-INV-EJEC-001`; manual BPMN p. 36 | Declarar que S4.3 se limita a obras o agregar la rama "No" |
| O3 | La salida "No" de "Solo construccion?" salta la procura, pero en diseno y construccion tambien hay contratacion y condiciones de inicio; ademas no se representa la administracion directa, que tiene su propia preparacion | `REG-CON-OBRA-001`; `REG-CON-OBRA-002`; `REG-INV-EJEC-008`; Directiva 017-2023-CG num. 7.2 | Distinguir primero la modalidad (contrata o administracion directa) y luego el sistema de entrega; ver pregunta P3 |
| O4 | "Recepcion" no aplica al contrato resuelto: la norma preve constatacion fisica e inventario y luego liquidacion; el saldo de obra genera el informe de estado situacional hacia S4.2 | `REG-CON-OBRA-003`; `REG-CON-OBRA-004`; ficha S4 | Nombrar S4.3.3 de forma que cubra ambos casos (por ejemplo "Culminacion de la ejecucion fisica") con dos finales: obra recibida y obra con contrato resuelto |
| O5 | La frontera con S4.4 difiere por modalidad: en contrata la liquidacion del contrato es posterior a la recepcion; en administracion directa culminacion y liquidacion son una sola fase. Tampoco esta asignado el registro de la culminacion (Formato 09, seccion B, 60 dias) | `REG-CON-OBRA-005`; `REG-CGR-AD-002`; `REG-INV-EJEC-007` | Decidir y registrar donde termina S4.3 en cada modalidad |
| O6 | El Reglamento vigente agrega la "planificacion de la ejecucion" como componente de la fase; el mapa institucional no la ubica | `REG-INV-EJEC-001`; `REG-INV-EJEC-002` | Decidir si forma parte de S4.3.1, de S4.2 o de un proceso propio |
| O7 | No se ven obligaciones permanentes de la ejecucion: registro previo de modificaciones, vigilancia del avance, seguimiento mensual (Formato 12-B), programa de mantenimiento y expediente para pagos | `REG-INV-EJEC-004` a `REG-INV-EJEC-006`; `REG-INV-EJEC-009` | Ubicarlas dentro de S4.3.2 o en un subproceso transversal de seguimiento y control |
| O8 | Notacion BPMN: codigo "S43.1" en lugar de "S4.3.1"; textos de estado sobre flujos de secuencia; compuerta final con una entrada y una salida; un solo evento de fin para resultados distintos; pool sin carriles | Manual BPMN p. 35-37 y 147; NT num. 6.1.3 a | Corregir el codigo; usar eventos intermedios u objetos de datos para actas y estados; eliminar la union innecesaria; usar dos eventos de fin; agregar carriles al detallar el nivel 2 |
| O9 | El mensaje hacia S4.4 usa una tercera redaccion ("informacion tecnico y financiera de liquidacion de la inversion") distinta de las dos de la ficha S4 | Sustento de S4, discrepancias | Conservar el texto de la ficha o registrar la decision de unificarlo |

### Preguntas abiertas iniciales

| N | Pregunta |
|---|---|
| P1 | S4.3 cubre solo obras o tambien IOARR y otras inversiones sin obra? |
| P2 | Que modalidades usa el Gobierno Regional: contrata, administracion directa, convenios, Obras por Impuestos u otras? |
| P3 | Que significa la salida "No" de "Solo construccion?": diseno y construccion, administracion directa u otro caso? |
| P4 | Quien liquida los contratos de obra y quien registra la culminacion en el Formato 09: S4.3 o S4.4? |
| P5 | Donde se ubica la planificacion de la ejecucion del Reglamento vigente? |
| P6 | Como continua un contrato resuelto con saldo de obra: vuelve a S4.2 y luego a una nueva ejecucion? |

### Respuestas del equipo y contraste normativo

Respuestas del equipo del proyecto del 2026-10-16 a las preguntas P1-P6. Clase `DECISION` del equipo; el contraste es `INFERENCIA` sobre reglas `BORRADOR-IA`.

| N | Respuesta del equipo | Contraste con las fuentes | Efecto en el modelo |
|---|---|---|---|
| P1 | S4.3 abarca todas las inversiones, no solo obras | Coherente: la fase de Ejecucion rige para proyectos e IOARR (`REG-INV-EJEC-001`). Para bienes y servicios la conformidad la otorga el area usuaria y la recepcion de bienes se rige por el Sistema Nacional de Abastecimiento (`REG-CON-BYS-001`); esa normativa no esta en la biblioteca: `EVIDENCIA-INSUFICIENTE` | Se elimina la compuerta "Obra?"; S4.3.3 cubre recepcion de obra y conformidad de bienes y servicios |
| P2 | Modalidades en uso: contrata, administracion directa y Obras por Impuestos. Los convenios son, en general, para que el GORE ejecute; son una condicion del proyecto, no una modalidad | Contrata: Reglamento de la Ley 32069. Administracion directa: `REG-CGR-AD-001` y justificacion previa `REG-INV-EJEC-008`. Obras por Impuestos (Ley 29230 y su reglamento): sin fuentes en la biblioteca, `EVIDENCIA-INSUFICIENTE` | S4.3.1 cubre contratacion, preparacion por administracion directa y Obras por Impuestos; convenios como entrada |
| P3 | La salida "No" de "Solo construccion?" es diseno y construccion: el contrato existe desde S4.2, por lo que no hay procura | Coherente: en diseno y construccion el contratista elabora el expediente y ejecuta la obra (`REG-CON-OBRA-001`); el contrato puede terminarse durante el diseno (Reglamento Ley 32069, art. 175.2, p. 93). Las condiciones de inicio del art. 176.1 aplican tambien a este sistema (`REG-CON-OBRA-002`). Queda por confirmar en que proceso se contrata la supervision | Compuerta C1: "Diseno y construccion con contrato vigente desde S4.2?" |
| P4 | La liquidacion ocurre en S4.4 | En contrata la liquidacion sigue a la recepcion o a la resolucion consentida (`REG-CON-OBRA-005`). En administracion directa un mismo Comite de Culminacion y Liquidacion actua en S4.3 y S4.4 (`REG-CGR-AD-002`). El registro de la culminacion en el Formato 09, seccion B (`REG-INV-EJEC-007`), sigue sin asignar | S4.3 termina con la recepcion o constatacion y entrega informacion a S4.4 |
| P5 | La planificacion de la ejecucion que realiza la entidad va en la procura; la demas planificacion la hacen los especialistas de obra | Parcialmente coherente: la definicion reglamentaria incluye la planificacion para el expediente tecnico y para la ejecucion fisica (`REG-INV-EJEC-002`). Si se ubica en S4.3.1, la planificacion previa al expediente debe quedar cubierta en S4.2 | S4.3.1 incluye la planificacion de la ejecucion fisica a cargo de la entidad; pendiente confirmar la de S4.2 |
| P6 | Un contrato resuelto puede continuar por saldo de obra: vuelve a S4.2 para elaborar el expediente de saldo y reinicia el ciclo | Coherente con la ficha S4 (salida de S4.3 a S4.2: informe de estado situacional por saldo de obra) y con el uso de diseno y construccion para saldos (`REG-CON-OBRA-001`). La obra con contrato resuelto tambien se liquida (`REG-CON-OBRA-004`) | Compuerta C2: con saldo, salen el informe a S4.2 y la informacion a S4.4 |

### Situacion de las observaciones

| N | Situacion |
|---|---|
| O1 | Incorporada: intercambios de la ficha S4 en el modelo logico |
| O2 | Resuelta por P1 |
| O3 | Resuelta por P2 y P3; queda la supervision en diseno y construccion |
| O4 | Incorporada: S4.3.3 cubre constatacion por resolucion; saldo hacia S4.2 |
| O5 | Resuelta en parte por P4; queda asignar el registro del Formato 09, seccion B |
| O6 | Resuelta en parte por P5; queda la planificacion previa al expediente |
| O7 | Incorporada como contenido propuesto de S4.3.2 |
| O8 | Se aplicara al formalizar en BPMN |
| O9 | El modelo logico usa la redaccion literal de la ficha S4 |

### Preguntas abiertas tras las respuestas

| N | Pregunta |
|---|---|
| P7 | En diseno y construccion, la supervision de la obra se contrata en S4.2 o en S4.3? |
| P8 | Quien registra la culminacion de la ejecucion fisica en el Formato 09, seccion B: S4.3 o S4.4? |
| P9 | La planificacion previa a la elaboracion del expediente se realiza en S4.2? |
| P10 | Quien es el dueno de S4.3 y cual es su objetivo? |

### Elementos de la ficha borrador

| Campo de la ficha | Contenido | Clase | Fuente |
|---|---|---|---|
| Nombre | S4.3 Ejecucion de la inversion | `OBSERVADO` | Ficha S4, p. 120-121 |
| Tipo de proceso | Apoyo | `INFERENCIA` | Tipo de S4 en su ficha aprobada y codigo `S` (NT 002-2025-PCM-SGP, Anexo 1) |
| Entradas y productos | Texto literal de las filas de S4.3 | `OBSERVADO` | Ficha S4, p. 120-121 |
| Subprocesos | S4.3.1 Procura, S4.3.2 Ejecucion, S4.3.3 Recepcion | `PROPUESTA` | Propuesta del equipo y respuestas P1-P6 |
| Dueno, objetivo y objetivo estrategico | Pendientes | `EVIDENCIA-INSUFICIENTE` | P10 |

## Informacion BIM

Para cada actividad relevante se registraran, cuando exista evidencia:

- uso BIM;
- requisito de informacion;
- contenedor recibido y producido;
- formato de intercambio;
- proposito de uso y estado de revision/aprobacion;
- autor, revisor y aprobador;
- control de calidad;
- evidencia de aceptacion;
- relacion con EIR, BEP, MIDP, TIDP y matriz de responsabilidades.

El repositorio gestiona las fuentes y su versionado. Cualquier emision hacia un CDE institucional futuro se registrara como una integracion externa. Referencias: [biblioteca BIM](../../../01-referencias/08-bim/00-bim.md).

## Historial de revision

| Documento | Nivel | Fecha | Resultado | Rol o unidad | Evidencia |
|---|---|---|---|---|---|
| - | - | - | Sin documentos remitidos a revision | - | - |

## Relaciones

- [Portada de S4.3](00-S4-3-ejecucion-inversion.md)
- [Sustento de S4](../S4-sustento.md)
- [Manual operativo del conocimiento](../../../00-gobernanza/manual-operativo-del-conocimiento.md)
