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
fecha_creacion: 2026-10-19
fecha_actualizacion: 2026-10-19
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-1
---

# S4.3.1 Gestion de la ejecucion - Sustento

Sube a: [S4.3.1 Gestion de la ejecucion](00-S4-3-1-gestion-de-la-ejecucion.md)

Registra los insumos, las fuentes, la clase de cada dato y los vacios que sustentan la [ficha](S4-3-1-ficha-producto-proceso.md) y el [diagrama](S4-3-1-diagrama-proceso-tabla.md) de S4.3.1. No se exporta a PDF. La delimitacion de S4.3 en tres subprocesos y las respuestas del equipo P1-P14 estan en el [sustento de S4.3](../S4-3-sustento.md); aqui solo se citan.

## Insumos

| Insumo | Fecha | Clase | Uso |
|---|---|---|---|
| Delimitacion de S4.3.1 en `DEC-023` y `DEC-024` | 2026-10-16 | `DECISION` del equipo | Alcance, inicio, termino y relacion con S4.3.2 y S4.3.3 |
| Ficha aprobada de S4, fila S4.3 | Aprobada (`DEC-016`) | `OBSERVADO` | Entradas, productos, proveedores, receptores y responsable |
| Respuestas del equipo P2, P4, P5, P6 y P11-P14 | 2026-10-16 | `DECISION` del equipo y `OBSERVADO` | Modalidades, procura, componente de gestion, saldo de obra |
| Modelo 1 del equipo "Inicio de ejecucion contractual - solo construccion" | 2026-10-19 | `PROPUESTA` del equipo | Secuencia de inicio y carriles; la imagen se compartio en la conversacion de trabajo y no esta en el repositorio |
| Diagrama de S4.3.2 | 2026-10-19 | `PROPUESTA` | Mensajes que S4.3.2 envia a S4.3.1 |

## Modelo 1 del equipo

Contenido observado en el insumo (`OBSERVADO`):

- Carriles: GRI, SGOS y coordinador de proyecto.
- Secuencia: recibir el contrato; verificar las condiciones de inicio; compuerta "¿cuenta con supervision?"; si no, designar al inspector; conformar el equipo complementario mediante un tramite de GRI a GRA; comunicar al contratista el inicio.

Evaluacion (`INFERENCIA`):

| Aspecto | Resultado | Fuente |
|---|---|---|
| Compuerta de supervision | Se conserva: la supervision la ejerce el supervisor o el inspector, nunca ambos a la vez; si la obra requiere supervisor, puede designarse un inspector o un equipo de inspectores para iniciar mientras se contrata | Reglamento de la Ley 32069, art. 186.1 y 186.4, PDF p. 101 |
| Verificacion de condiciones | Se conserva y se ubica despues de designar la supervision, porque la comunicacion del supervisor o inspector es una de las condiciones del art. 176.1 | `REG-CON-OBRA-002` |
| Comunicacion al contratista | Se representa como el mensaje "Condiciones de inicio cumplidas" a S4.3.2, que inicia con el acta de inicio | `DEC-024`; diagrama de S4.3.2 |
| Equipo complementario por GRI y GRA | Se resume en "Asignar el rol de Monitor y conformar el equipo de gestion"; el tramite entre gerencias corresponde al nivel 3 | `REG-CON-CDI-002`; practica del equipo |
| Alcance "solo construccion" | Se amplia a todas las modalidades con anotaciones, como en S4.3.2 | Respuestas P2 y P3 |
| Carriles GRI, SGOS y coordinador | No se adoptan todavia: falta la evidencia de funciones (ROF o MOF) que los sustente | `EVIDENCIA-INSUFICIENTE` |

## Fuentes de cada elemento del diagrama

Clase `NORMATIVO` citado salvo indicacion. Reglas en `03-conocimiento/reglas/`, todas en estado `BORRADOR-IA`, por lo que no constituyen sustento de linea base hasta cumplir el protocolo de conocimiento confiable. Fecha de consulta: 2026-10-19.

| Elemento | Fuente y ubicacion | Clase |
|---|---|---|
| Inicio por expediente tecnico aprobado; una instancia por inversion | Ficha S4, p. impresas 120-121; `DEC-023` | `OBSERVADO`; `DECISION` |
| Planificar la ejecucion de la inversion | `REG-INV-EJEC-002` (Reglamento del Invierte.pe, art. 3.24, PDF p. 4): gobernanza, recursos, contrataciones, cronograma, riesgos y controles; respuesta P5: la planificacion a cargo de la entidad va en la gestion | `NORMATIVO`; `DECISION` |
| Convenios como entrada | Ficha S4; respuesta P2: condicion del proyecto, no modalidad | `OBSERVADO` |
| Requerir las contrataciones y la designacion de personal | Instructivo del Formato 08-A, p. 20: preparar terminos de referencia y actuar como area usuaria; AD: `REG-CGR-AD-003` (plan de abastecimiento), `REG-CGR-AD-004` (adquisiciones de los primeros treinta dias); diseno y construccion: `REG-CON-OBRA-001` | `REFERENCIA`; `NORMATIVO` |
| Contratos y adquisiciones recibidos | Ficha S4: entrada desde S3.2 | `OBSERVADO` |
| ¿Cuenta con supervisor contratado? / Designar al inspector o al equipo de inspectores | Reglamento de la Ley 32069, art. 186.1 y 186.4, PDF p. 101 (texto modificado por el DS 001-2026-EF); modelo 1 del equipo | `NORMATIVO`; `PROPUESTA` del equipo |
| Asignar el rol de Monitor y conformar el equipo de gestion | `REG-CON-CDI-002`; Instructivo del Formato 08-A, p. 19-20; practica del equipo (respuesta P11) | `NORMATIVO`; `REFERENCIA`; `OBSERVADO` |
| Verificar las condiciones de inicio | `REG-CON-OBRA-002` (Reglamento, art. 176.1, PDF p. 93-94); AD: Directiva 017-2023-CG, num. 7.3.1 | `NORMATIVO` |
| ¿Condiciones de inicio cumplidas? / Gestionar las condiciones pendientes | Consecuencia de la verificacion; el detalle de cada condicion corresponde al nivel 3 | `PROPUESTA` |
| Condiciones de inicio comunicadas | `DEC-024`; mensaje de inicio de S4.3.2 | `PROPUESTA` |
| Todas las ejecuciones recibidas o constatadas | `DEC-023`: S4.3.1 termina cuando todas las ejecuciones fueron recibidas o constatadas; se cumple con los mensajes de S4.3.3 | `PROPUESTA` |
| Consolidar la informacion para la liquidacion | Ficha S4: producto a S4.4; respuesta P4: la liquidacion ocurre en S4.4 | `OBSERVADO`; `DECISION` |
| ¿Contrato resuelto con saldo por ejecutar? / Informe de estado situacional | Respuesta P6; ficha S4: producto a S4.2 | `DECISION`; `OBSERVADO` |
| Seguimiento mensual de la ejecucion | `REG-INV-EJEC-005` (vigilancia permanente del avance); `REG-INV-EJEC-006` (Formato 12-B en los primeros diez dias habiles del mes siguiente); ficha S4: reporte a MEF / INFOBRAS | `NORMATIVO`; `OBSERVADO` |
| Tramite del expediente para pagos | Ficha S4: producto a S2.1; diagrama de S4.3.2: la valorizacion aprobada se envia a S4.3.1 | `PROPUESTA` |
| Actualizacion por modificaciones de la ejecucion | `REG-INV-EJEC-002`; los registros en el Banco de Inversiones (`REG-INV-EJEC-004`) quedan dentro de cada subproceso de S4.3.2 | `PROPUESTA` |
| Provision de bienes, servicios y personal | `DEC-023` (la provision continua pasa a S4.3.1); `REG-CGR-AD-003`; Directiva 017-2023-CG, num. 7.3.3, p. 15-16; componente de gestion (respuesta P11) | `DECISION`; `NORMATIVO`; `OBSERVADO` |
| Registro de obra publica paralizada | `REG-CON-PARAL-001`; TUO de la Ley 31589, art. 3.1 (inventario en el Banco de Inversiones) y art. 4.1 (informe de estado situacional), p. 2 | `NORMATIVO` |

## Entradas y productos de la ficha

| Dato | Clase | Fuente |
|---|---|---|
| Entradas desde S4.2, Gobiernos y S3.2; productos a S3.1, MEF / INFOBRAS, S2.1, S4.4 y S4.2 | `OBSERVADO`, texto literal de la fila S4.3 | Ficha S4, p. impresas 120-121 |
| Asignacion de esos intercambios a S4.3.1 | `PROPUESTA` | `DEC-023`: S4.3.1 planifica, contrata, provee y hace el seguimiento |
| Producto a S4.3.2: condiciones de inicio cumplidas | `PROPUESTA` | `DEC-024` |
| Entradas desde S4.3.2: valorizacion aprobada, modificaciones y requerimientos | `PROPUESTA` | Diagrama de S4.3.2 y `DEC-023` |
| Entrada desde S4.3.3: recepcion o constatacion concluida | `PROPUESTA` | `DEC-023` |

## Discrepancias y vacios

| N | Tema | Situacion | Clase |
|---|---|---|---|
| D1 | Expediente para pagos | El diagrama de S4.3 lo envia desde S4.3.2 a S2.1; el de S4.3.1 lo tramita desde S4.3.1. Debe confirmarse una sola ruta y alinear el diagrama de S4.3 | `PROPUESTA` |
| D2 | Carriles por unidad de organizacion | Un solo carril con el responsable de S4.3 en la ficha S4 | `EVIDENCIA-INSUFICIENTE` |
| D3 | Obras por Impuestos | `INV-006`, `INV-006A` e `INV-006B` pendientes de lectura | `EVIDENCIA-INSUFICIENTE` |
| D4 | Varios contratos o frentes | La verificacion y la comunicacion de condiciones se repiten por cada uno; falta definir su representacion | `PROPUESTA` |
| D5 | Programa de mantenimiento | `REG-INV-EJEC-009`: la UEI lo elabora durante la ejecucion fisica; falta ubicarlo entre S4.3.1 y S4.3.3 | `PROPUESTA` |
| D6 | Formato 09, seccion B | `REG-INV-EJEC-007`; pregunta P8 del sustento de S4.3 | `EVIDENCIA-INSUFICIENTE` |
| D7 | Supervision en diseno y construccion | Pregunta P7 del sustento de S4.3 | `EVIDENCIA-INSUFICIENTE` |
| D8 | Condiciones de inicio en administracion directa | Se cita el num. 7.3.1 de la Directiva 017-2023-CG; falta transcribirlas en una regla | `PROPUESTA` |
| D9 | Equipo de proteccion del personal de la entidad | Ley 29783 y su reglamento pendientes de lectura | `EVIDENCIA-INSUFICIENTE` |

## Preguntas para el equipo

| N | Pregunta |
|---|---|
| Q1 | ¿El expediente para pagos se tramita desde S4.3.1 (con la valorizacion aprobada en S4.3.2) o lo envia directamente S4.3.2 a S2.1? |
| Q2 | ¿Se confirman los cinco subprocesos de evento como procesos de nivel 3, y con que codigos? |
| Q3 | ¿Que unidad cumple cada rol del modelo 1 (GRI, SGOS, coordinador de proyecto) y que documento lo establece? |
| Q4 | ¿Donde se elabora el programa de mantenimiento: en S4.3.1 durante la ejecucion o en S4.3.3 con la recepcion? |
| Q5 | Con varios contratos o frentes, ¿la preparacion se modela una vez por contrato dentro de S4.3.1? |

## Diagrama en BPMN

El diagrama se genero con la cadena BPMN (`DEC-025`, `DEC-026`) y paso los controles D1-D5 el 2026-10-19. Para que los mensajes hacia S3.1 y S4.3.2 no cruzaran la zona de subprocesos de evento, `tabla_a_bpmn.py` ubica arriba un pool cerrado que recibe cuando su mensaje sale de un nodo intermedio situado sobre esa zona; los diagramas de S4.3, S4.3.2 y el catalogo no cambiaron.
