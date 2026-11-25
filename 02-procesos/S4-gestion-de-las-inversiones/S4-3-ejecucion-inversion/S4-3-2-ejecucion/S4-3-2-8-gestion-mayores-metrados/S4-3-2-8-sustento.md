---
id: AP-S4-3-2-8-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.8
nivel_proceso: 3
tipo_proceso: APOYO
proceso_padre: S4.3.2
estado_institucional: PROPUESTA
nivel_revision: ELABORACION
proceso:
  - S4.3.2.8
fecha_creacion: 2026-11-18
fecha_actualizacion: 2026-11-18
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-8
---

# S4.3.2.8 Gestion de mayores metrados - Sustento

Sube a: [S4.3.2.8 Gestion de mayores metrados](00-S4-3-2-8-gestion-mayores-metrados.md)

Registra la separacion de alcance y los limites del modelo de trabajo, sin validacion normativa ni aprobacion institucional.

## Fuentes utilizadas

[Reglamento, art. 197.1-197.4, PDF p. 123; art. 210](https://diariooficial.elperuano.pe/Normas/obtenerDocumento?idNorma=25). Detalle limitado a precios unitarios y sistemas de entrega comprendidos en art. 197. No exige aprobacion previa de ejecucion por la entidad; autorizacion de pago se controla en S4.3.2.1. No se extiende por analogia a administracion directa.

Consulta oficial: 2026-11-18. Edicion de El Peruano actualizada al 21-10-2026; aplicabilidad al contrato y modificatorias posteriores pendientes de control especializado. Conocimiento normativo propuesto, no VALIDADO.

## Elementos registrados

- OBSERVADO: el usuario acepta dividir el proceso y conserva tres casos en S4.3.2.3 (2026-11-18).
- DECISION de modelamiento: DEC-047 asigna S4.3.2.8 como hermano de nivel 3; no es una conformidad institucional.
- PROPUESTA: objetivo, productos e interfaces de la ficha; unidades internas y propietario pendientes. El tipo Apoyo se hereda provisionalmente de S4.3.2.3.
- EXIGENCIA NORMATIVA propuesta: condiciones indicadas en la fuente y en las filas NORM; no se trasladan los plazos del art. 194.

## Paquete de contexto

Fase conceptual; fuentes textuales activas: indice, ficha, tabla y sustento del padre, S4.3.2.3 y este proceso; Reglamento en los articulos citados. Reglas validadas: ninguna. BPMN XML, SVG, PNG y HTML excluidos del contexto; revision visual diferida. Modificacion de herramientas no autorizada. Glosario: adicional, deductivo vinculado, deductivo puro, reduccion y mayor metrado no son sinonimos automaticos.

## Vacios de evidencia

EVIDENCIA-INSUFICIENTE: dueno, adscripciones, delegaciones, objetivo estrategico, indicadores, caso contractual y modalidades distintas de las expresamente descritas. Los cierres por evidencia pendiente no equivalen a denegacion. La distincion entre deductivo puro y reduccion requiere evidencia tecnica y contractual; un caso no se tramita dos veces.

## Discrepancias

La ruta se separa de S4.3.2.3; no existe secuencia obligatoria entre hermanos. La numeracion nueva pertenece a este modelo; la numeracion retirada de S4.3.2.3 no se reutiliza.

## Informacion BIM

EVIDENCIA-INSUFICIENTE. No se incorporan requisitos BIM.

## Historial de revision

Sin conformidades registradas. Documentos en ELABORACION.

## Relaciones

- Se rige por [decision de arquitectura](../../../../../00-gobernanza/registro-decisiones.md).
- Se separa de [S4.3.2.3](../S4-3-2-3-gestion-adicionales-deductivos-obra/00-S4-3-2-3-gestion-adicionales-deductivos-obra.md).
- Se integra en [S4.3.2](../00-S4-3-2-ejecucion.md).

## Control tecnico de la division

D1, D2 y D5 sin hallazgos. D3 sin bloqueos. D4: dos interferencias: mensaje a valorizacion atraviesa anotacion (T1) y comunicacion a entidad cruza etiqueta (T6). Se adoptan derivados de trabajo con --forzar para sincronizar la propuesta conceptual; no constituyen una linea base lista para publicacion. Revision visual y cierre de hallazgos pendientes. Informe reproducible: 99-temporal/modelos/S4-3-2-8-diagrama-proceso/validacion.txt.

## Auditoría por afirmación — 2026-11-24 (fase 5)

Auditoría con el formato de DEC-057 ([informe generado](../../../../../05-herramientas/gestor-modelos/auditorias/S4-3-2-8/informe.md)): 20 afirmaciones (6 `SUSTENTADA`, 14 `INFERENCIA`, sin contradicciones) y 8 obligaciones del Reglamento arts. 197 y 198.1 c) (texto vigente; el art. 197 no tiene modificaciones en el texto consolidado), de las que 3 no están representadas. Se calcularon 12 anclas desde el texto, todas vigentes. Esta generación deja D1-D5 sin hallazgos: las dos interferencias D4 registradas antes ya no aparecen. Son propuestas de IA, sin validación ni conformidad.

- **Bien representado:** el núcleo del 197.1 y 197.2. El contratista solicita en el cuaderno de incidencias, solo en contratos a precios unitarios. El supervisor autoriza en el mismo medio si no se supera el límite acumulado (mayores metrados más adicionales, menos deductivos). La ejecución no requiere aprobación previa de la entidad, pero el pago sí, y se tramita en la valorización del periodo (interfaz con S4.3.2.1).
- **Inferencias relevantes:**
  - que el inspector autorice: el 197.1 nombra al supervisor y el 186.1 asigna la supervisión al supervisor o al inspector;
  - comunicar la autorización a la entidad (S3) no es exigencia literal;
  - S4 documenta el exceso del límite sin derivar la consecuencia del 197.4.
- **No representado:**
  - **197.4:** si se supera el 50 % del componente obra, se procede a la resolución del contrato;
  - **197.3 y 198.1 c):** los mayores metrados son causal de ampliación de plazo, y sus mayores gastos generales se pagan por el art. 201. No hay interfaz con S4.3.2.4.
- **Interfaz:** RF envía el sustento a S4.3.2.1, que no registra ese mensaje (candidato ya detectado en S4.3.2).
- **Propuestas no aplicadas:**
  - en S4, una salida o anotación hacia la resolución del contrato cuando se supera el 50 % (197.4);
  - un mensaje o anotación hacia S4.3.2.4 cuando los mayores metrados afectan la ruta crítica (198.1 c y 197.3);
  - la recepción correspondiente en S4.3.2.1.
