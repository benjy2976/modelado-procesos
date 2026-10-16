---
id: AP-S4-3-2-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S4.3.2
nivel_proceso: 2
proceso:
  - S4.3.2
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2
---

# S4.3.2 Ejecucion - Sustento

Sube a: [S4.3.2 Ejecucion](00-S4-3-2-ejecucion.md)

Registra los insumos, la evaluacion, las fuentes y los vacios que sustentan el modelo logico de S4.3.2. No se exporta a PDF. La delimitacion de S4.3 en tres subprocesos esta en el [sustento de S4.3](../S4-3-sustento.md).

## Insumos recibidos

| Insumo | Fecha | Clase | Autor | Archivo |
|---|---|---|---|---|
| Modelo BPMN de S4.3.2 Ejecucion con bucle de eventos | 2026-10-16 | `PROPUESTA` | Equipo del proyecto | [S4-3-2-insumo-modelo-ejecucion-equipo.png](S4-3-2-insumo-modelo-ejecucion-equipo.png), SHA-256 `72334CEBE26B3AD471F799F3E4FBE95B177F8BC77BB4BF26EFEC6307390F0CBB` |

## Modelo observado del equipo

Clase `OBSERVADO` en el insumo:

- Pools separados para Contratista y Supervisor, que envian flujos de mensaje a la tarea "recepcionar evento" del pool S4.3.2 Ejecucion.
- Flujo: inicio de obra, evento de temporizador "Esperar evento", tarea "recepcionar evento" y compuerta "tiene conformidad tecnica o resolucion de contrato o nulidad de contrato?". Si la respuesta es si, termina; si es no, una compuerta paralela y una inclusiva distribuyen a las ramas de evento, que convergen en otra compuerta inclusiva y regresan a "Esperar evento".
- Ramas de evento: S4.3.2.1 Valorizacion (subproceso, con almacen de datos), S4.3.2.2 Adicional de obra (subproceso), Adicional deductivo vinculante, Suspension de obra, Ampliacion de plazo, Consulta de obra (con flecha hacia ampliacion de plazo), Paralizacion de obra, Reduccion de obra, Mayores y menores metrados y una rama "Consulta a la..." cortada en la imagen.
- Nota con la lista de eventos: Valorizacion, Adicional de obra, Modificacion contractual (sin completar), Consulta.
- Preguntas abiertas del equipo sobre el evento final y el documento de finalizacion de obra.

## Aclaraciones del equipo

Respuestas del equipo del proyecto del 2026-10-16 (clase `DECISION` del equipo) y su contraste (`NORMATIVO` citado):

| Aclaracion | Contraste | Fuente |
|---|---|---|
| La paralizacion de obra es una figura distinta de la suspension | Coherente: la suspension de plazo se acuerda entre las partes (Reglamento, art. 202 y art. 107); la obra publica paralizada es una situacion definida por ley especial, y en administracion directa la paralizacion se informa y sustenta para modificar el plazo | `REG-CON-PARAL-001`; `REG-CGR-AD-005`; Reglamento de la Ley 32069, art. 202.1, PDF p. 114-115 |
| El adicional aumenta el alcance y la reduccion es lo opuesto | Coherente: la Ley 32069 permite ordenar adicionales y reducir prestaciones hasta por el mismo porcentaje | `REG-CON-ADIC-001` |
| Adicional y deductivo vinculado son dos acciones de una misma accion | Coherente: el limite del adicional de obra se calcula restandole los presupuestos deductivos vinculados | `REG-CON-ADIC-002` |
| En administracion directa las figuras son distintas pero parecidas y aplican adicionales y paralizacion | Coherente: la directiva de la CGR trata adicionales, deductivos, mayores metrados y partidas nuevas como modificaciones (num. 7.3.6) y la paralizacion como causal de modificacion de plazo (num. 7.3.7) | `REG-CGR-AD-005`; Directiva 017-2023-CG, num. 7.3.6, PDF p. 17 |
| El modelo del equipo se usara, por lo que se conserva | Se guarda como insumo | Esta nota |

## Evaluacion del modelo del equipo

Clase `INFERENCIA`, con base en el manual BPMN (`REFERENCIA`) y la NT 002-2025-PCM-SGP (`NORMATIVO`).

### Aciertos

- Identifica que los eventos pueden ocurrir en cualquier momento y en cualquier orden durante la ejecucion.
- Separa las condiciones de termino (conformidad tecnica, resolucion, nulidad) de los eventos que no terminan la ejecucion.
- Trata la valorizacion y el adicional como subprocesos con detalle propio.
- Relaciona la consulta con la ampliacion de plazo: la demora en absolver consultas es causal de ampliacion en administracion directa (Directiva 017-2023-CG, num. 7.3.7 b, PDF p. 18).

### Observaciones

| Codigo | Observacion | Efecto | Fuente |
|---|---|---|---|
| E1 | El bucle procesa un evento por vuelta | Mientras se tramita un adicional, que puede tomar semanas, el proceso no puede atender la valorizacion del mes siguiente ni una consulta, aunque en la realidad ocurren a la vez | Manual BPMN, sec. 2.8.6, p. 96-97 |
| E2 | El evento de temporizador "Esperar evento" no espera eventos: espera una fecha o un plazo | Su significado BPMN es distinto del que se quiere representar | Manual BPMN, sec. 2.6.3, p. 60-61 |
| E3 | La compuerta paralela recibe el regreso del "no" y luego una inclusiva elige ramas | Una compuerta paralela de union espera todas sus entradas; la inclusiva decide por condiciones sobre datos, no por el suceso que llego | Manual BPMN, sec. 2.3.2 y 2.3.3, p. 38-43 |
| E4 | Los mensajes llegan a una tarea generica "recepcionar evento" | Se pierde que suceso llego y quien lo envio; cada suceso debe tener su propio disparador (mensaje, tiempo o condicion) | Manual BPMN, sec. 2.6.2, p. 58; sec. 2.6.3, p. 60; sec. 2.6.5, p. 63 |
| E5 | Pools separados para contratista y supervisor | Es valido en BPMN, pero la NT pide un proceso con carriles por rol; ademas, en administracion directa no hay contratista sino residente | NT, Anexo 3, p. 27 |
| E6 | Adicional y adicional deductivo vinculante en ramas separadas | Segun la aclaracion del equipo y la Ley, son una sola accion | `REG-CON-ADIC-002` |
| E7 | La conformidad tecnica se evalua dentro de la ejecucion | La conformidad y la recepcion corresponden a S4.3.3; la ejecucion termina con la obra culminada | `REG-CON-OBRA-003`; `DEC-023` |
| E8 | "Mayores y menores metrados" | El reglamento regula los mayores metrados (art. 197); no se encontro la figura de menores metrados | `EVIDENCIA-INSUFICIENTE` |

### Propuesta

Clase `PROPUESTA`, conforme a `DEC-024` y al estandar de artefactos, seccion 6.1:

1. Flujo principal corto: condiciones de inicio recibidas, acta de inicio, ejecucion de la obra y forma de termino.
2. Cada figura es un subproceso de evento sin interrupcion con su propio disparador. Puede ocurrir muchas veces y a la vez que otras, mientras la ejecucion siga activa, sin bucle.
3. La valorizacion se dispara con un temporizador mensual; las demas, por una condicion o por un mensaje anotado en el cuaderno de obra.
4. La ejecucion termina por obra culminada, por resolucion del contrato o por nulidad. En el BPMN formal, la resolucion y la nulidad pueden modelarse como eventos de borde con interrupcion sobre la ejecucion, o el termino como compuerta basada en eventos (manual BPMN, sec. 2.6.14, p. 74).
5. Un solo diagrama para contrata y administracion directa, con las diferencias anotadas por modalidad, porque las figuras son parecidas segun la aclaracion del equipo. Queda por confirmar si se prefiere un diagrama por modalidad.
6. Roles normativos (contratista o residente, supervisor o inspector, entidad) indicados en cada actividad. En el BPMN formal seran carriles; su correspondencia con unidades de organizacion del GRH es `EVIDENCIA-INSUFICIENTE`.
7. Separacion por niveles (observacion del equipo del 2026-10-16): el diagrama de S4.3.2 muestra solo la vida de la ejecucion y cada subproceso de evento contraido [+], con su disparador y sus relaciones con el flujo principal y con S4.3.1 y S4.3.3. El detalle de cada subproceso se modelara en su propio diagrama de nivel 3, como S4.3 hace con sus subprocesos de nivel 2 (NT, Anexo 3, p. 27).

### Codigos propuestos para el nivel 3

Los codigos S4.3.2.1 y S4.3.2.2 figuran en el modelo del equipo (`OBSERVADO` en el insumo). Los demas siguen el orden de las ramas del insumo y son `PROPUESTA` hasta que el equipo los confirme; al confirmarse se registrara la decision y se crearan sus carpetas.

| Codigo | Subproceso de evento | Disparador | Origen del codigo |
|---|---|---|---|
| S4.3.2.1 | Valorizacion | Temporizador: cierre de cada mes | Insumo del equipo |
| S4.3.2.2 | Adicional de obra con deductivo vinculado | Prestacion indispensable no prevista | Insumo del equipo; integra la rama de deductivo vinculante |
| S4.3.2.3 | Suspension de plazo | Causa que impide continuar | `PROPUESTA` |
| S4.3.2.4 | Ampliacion de plazo | Causal que afecta la ruta critica | `PROPUESTA` |
| S4.3.2.5 | Consulta de obra | Consulta anotada en el cuaderno | `PROPUESTA` |
| S4.3.2.6 | Paralizacion de obra | Supuesto de paralizacion | `PROPUESTA` |
| S4.3.2.7 | Reduccion de prestaciones | Prestacion que deja de ser necesaria | `PROPUESTA` |
| S4.3.2.8 | Mayores metrados | Mayor metrado en contrato a precios unitarios | `PROPUESTA` |

### Esbozo de actividades por subproceso de evento

Insumo para los diagramas de nivel 3, clase `PROPUESTA` construida sobre las fuentes del catalogo de eventos (`NORMATIVO` citado). No reemplaza el levantamiento con el equipo.

| Codigo | Actividades esbozadas (rol) | Envia | Base |
|---|---|---|---|
| S4.3.2.1 | Formular la valorizacion con los metrados ejecutados (contratista o residente); revisar y aprobar la valorizacion (supervisor o inspector) | S4.3.1: valorizacion aprobada para el expediente de pago `PROPUESTA` | Reglamento, art. 210.1; Directiva 017-2023-CG, num. 7.3.4 |
| S4.3.2.2 | Elaborar el expediente del adicional y de su deductivo vinculado; aprobar el adicional restando el deductivo vinculado (autoridad competente); registrar la modificacion en el Banco de Inversiones antes de ejecutarla (UEI) | S4.3.1: modificacion aprobada | `REG-CON-ADIC-002`; Reglamento, arts. 194 y 196; num. 7.3.6; `REG-INV-EJEC-004` |
| S4.3.2.3 | Acordar la suspension del plazo (entidad y contratista); al cesar la causa, reiniciar el plazo | S4.3.1: suspension y reinicio | Reglamento, art. 202; AD: `EVIDENCIA-INSUFICIENTE` |
| S4.3.2.4 | Solicitar y sustentar la ampliacion (contratista o residente); opinar (supervisor o inspector); resolver (entidad); en AD, registro previo en el Banco de Inversiones | S4.3.1: plazo modificado | Reglamento, arts. 198, 200 y 201; num. 7.3.7 |
| S4.3.2.5 | Si no modifica el expediente tecnico, absolver la consulta (supervisor o inspector); si lo modifica, elevarla a la entidad | Puede originar S4.3.2.4 | Reglamento, art. 190; num. 7.3.7 b |
| S4.3.2.6 | Informar la paralizacion en el cuaderno (contratista o residente); validarla (supervisor o inspector); en AD, sustentar y solicitar la modificacion del plazo con fechas de paralizacion y reinicio; en contrata, obra publica paralizada: continuidad o resolucion | S4.3.1: paralizacion y reinicio `PROPUESTA`; puede derivar en resolucion | `REG-CGR-AD-005`; `REG-CON-PARAL-001`; Ley 31589, art. 5.2 |
| S4.3.2.7 | Aprobar la reduccion hasta el limite legal (autoridad competente); registrar la modificacion en el Banco de Inversiones | S4.3.1: modificacion aprobada | `REG-CON-ADIC-001`; `REG-INV-EJEC-004` |
| S4.3.2.8 | Solicitar el mayor metrado en el cuaderno (contratista o residente); autorizarlo dentro del limite de adicionales (supervisor; en AD, segun num. 7.3.6) | S4.3.1: mayor metrado autorizado | Reglamento, art. 197; num. 7.3.6 |

## Catalogo de eventos

Clase `NORMATIVO` citado. Las ubicaciones del Reglamento corresponden al texto consolidado del Reglamento de la Ley 32069 (`CON-001`), y las de administracion directa (AD) a la Directiva 017-2023-CG (`CTRL-001`). Fecha de consulta: 2026-10-16.

| Evento | Disparador | Contrata | Administracion directa | Envia a |
|---|---|---|---|---|
| Valorizacion | Temporizador: cierre de cada mes | Reglamento, art. 210.1, PDF p. 118 | Num. 7.3.4, PDF p. 16 | S4.3.1: valorizacion aprobada para el expediente de pago `PROPUESTA` |
| Consulta de obra | Mensaje: consulta anotada en el cuaderno | Reglamento, art. 190, PDF p. 105 | Num. 7.3.7 b, PDF p. 18, como causal de ampliacion | Entidad, si modifica el expediente tecnico (art. 190.2) |
| Adicional de obra con deductivo vinculado | Condicion: prestacion indispensable no prevista | Ley 32069, art. 64.2-64.3, PDF p. 31 (`REG-CON-ADIC-002`); Reglamento, arts. 194 y 196, PDF p. 109-112 | Num. 7.3.6, PDF p. 17 | S4.3.1: modificacion aprobada |
| Reduccion de prestaciones | Condicion: prestacion que deja de ser necesaria | Ley 32069, art. 64.1, PDF p. 30-31 (`REG-CON-ADIC-001`) | Num. 7.3.6 (toda modificacion de alcance), `INFERENCIA` | S4.3.1: modificacion aprobada |
| Mayores metrados | Condicion: mayor metrado en contrato a precios unitarios | Reglamento, art. 197, PDF p. 112 | Num. 7.3.6, PDF p. 17 | S4.3.1: mayor metrado autorizado |
| Ampliacion de plazo | Condicion: causal que afecta la ruta critica | Reglamento, arts. 198, 200 y 201, PDF p. 112-114 | Num. 7.3.7, PDF p. 18, con registro previo en el Banco de Inversiones | S4.3.1: plazo modificado |
| Suspension de plazo | Condicion: evento que impide continuar, por acuerdo de partes | Reglamento, art. 202, PDF p. 114-115 | `EVIDENCIA-INSUFICIENTE` | S4.3.1: plazo suspendido y reinicio |
| Paralizacion de obra | Condicion: supuestos de paralizacion | Ley 31589, TUO, art. 2, PDF p. 2 (`REG-CON-PARAL-001`): obra publica paralizada; con contrato vigente, la entidad propone la continuidad o resuelve el contrato (art. 5.2, PDF p. 3) | Num. 7.3.7, PDF p. 18 (`REG-CGR-AD-005`) | S4.3.1: paralizacion y reinicio `PROPUESTA` |
| Registro de modificaciones | Toda modificacion durante la ejecucion fisica | Directiva de Invierte.pe, art. 33.2 (`REG-INV-EJEC-004`) | Igual | - |

Formas de termino:

| Termino | Fuente | Continua en |
|---|---|---|
| Obra culminada | Reglamento, art. 212, PDF p. 119 (`REG-CON-OBRA-003`); AD: num. 7.4 (`REG-CGR-AD-002`) | S4.3.3: recepcion o culminacion |
| Contrato resuelto | Reglamento, arts. 122 y 123, PDF p. 66-67 (`REG-CON-OBRA-004`) | S4.3.3: constatacion fisica e inventario |
| Contrato declarado nulo | Ley 32069, art. 71, PDF p. 35; Reglamento, art. 111, PDF p. 61 | S4.3.3: `EVIDENCIA-INSUFICIENTE` sobre el tratamiento posterior |

Figuras candidatas, no dibujadas hasta que el equipo confirme si se modelan (`PROPUESTA`):

| Figura | Fuente |
|---|---|
| Modificacion contractual por intensificacion del programa de ejecucion; la nota del equipo menciona "Modificacion contractual" sin completar | Reglamento, art. 191, PDF p. 106 |
| Actualizacion del programa de ejecucion | Reglamento, art. 206, PDF p. 116 |
| Monitoreo y control de obras | Reglamento, art. 207, PDF p. 116-117 |
| Intervencion economica de la obra (solo contrata) | Reglamento, art. 208, PDF p. 117 |
| Reajustes | Reglamento, art. 209, PDF p. 118 |

## Vacios de evidencia

| Vacio | Estado | Se cubre con |
|---|---|---|
| Figura de "menores metrados" | `EVIDENCIA-INSUFICIENTE` | Aclaracion del equipo o fuente que la regule |
| Suspension de plazo en administracion directa | `EVIDENCIA-INSUFICIENTE` | Fuente aplicable a AD |
| Tratamiento posterior a la nulidad del contrato de obra | `EVIDENCIA-INSUFICIENTE` | Lectura del art. 111 del Reglamento |
| Procedimiento de paralizacion en contrata dentro de la Ley 32069 y su reglamento | `EVIDENCIA-INSUFICIENTE`; solo se reviso la Ley 31589 | Ubicacion precisa indicada por el equipo |
| Rama "Consulta a la..." cortada en el insumo | `EVIDENCIA-INSUFICIENTE` | Imagen completa del modelo del equipo |
| Unidades de organizacion por rol | `EVIDENCIA-INSUFICIENTE` | Dueno del proceso |

## Preguntas abiertas

1. Se modela un solo diagrama para contrata y administracion directa, con diferencias anotadas, o uno por modalidad?
2. Se incorporan como eventos la intensificacion del programa, la intervencion economica, el monitoreo y control, y los reajustes?
3. Que significa "menores metrados" en la practica del GRH: un deductivo, una valorizacion por metrado real u otra figura?
4. Que figura completa la rama "Consulta a la..." del modelo del equipo?
5. Se confirman los codigos de nivel 3 propuestos y la creacion de sus carpetas?

## Historial de revision

| Fecha | Cambio | Autor |
|---|---|---|
| 2026-10-16 | Creacion: insumo del equipo, evaluacion, catalogo de eventos y modelo logico | Equipo del proyecto con asistencia de IA |
| 2026-10-16 | Modelo logico reducido al nivel 2 (subprocesos de evento contraidos); detalle trasladado al esbozo de actividades para el nivel 3 | Equipo del proyecto con asistencia de IA |

## Relaciones

- [Modelo logico de S4.3.2](S4-3-2-diagrama-proceso-logico.puml) y su [SVG](S4-3-2-diagrama-proceso-logico.svg)
- [Sustento de S4.3](../S4-3-sustento.md)
- [Guia del manual BPMN](../../../../03-conocimiento/fuentes/guia-manual-bpmn.md)
- [Guia del TUO de la Ley 31589](../../../../03-conocimiento/fuentes/guia-ley-31589-obras-paralizadas.md)
- [Guia del Reglamento de la Ley 32069](../../../../03-conocimiento/fuentes/guia-reglamento-ley-32069.md)
- [Guia de la Directiva de administracion directa](../../../../03-conocimiento/fuentes/guia-directiva-cgr-administracion-directa.md)
