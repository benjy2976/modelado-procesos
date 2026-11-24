---
id: AP-S4-3-2-7-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.7
nivel_proceso: 3
tipo_proceso: APOYO
proceso_padre: S4.3.2
estado_institucional: PROPUESTA
nivel_revision: ELABORACION
proceso:
  - S4.3.2.7
fecha_creacion: 2026-11-18
fecha_actualizacion: 2026-11-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-7
---

# S4.3.2.7 Gestion de reducciones de prestaciones - Sustento

Sube a: [S4.3.2.7 Gestion de reducciones de prestaciones](00-S4-3-2-7-gestion-reducciones-prestaciones.md)

Registra la separacion de alcance y los limites del modelo de trabajo, sin validacion normativa ni aprobacion institucional.

## Fuentes utilizadas

[Reglamento local, art. 109.1-109.3, PDF p. 60](../../../../../01-referencias/04-contrataciones-publicas/ley-y-reglamento/reglamento-de-la-ley-general-de-contrataciones-publicas-con-modificaciones-posteriores-hasta-el-09-01-2026.pdf). Ruta de reduccion en obra con supervisor; conservar finalidad y verificar limite, oportunidad y efecto sobre plazo. La administracion directa y otros supuestos requieren ruta propia. El archivo local tiene SHA-256 `0ebe95b3e05661b80f73c060d6e6ce8dd17621ce34af9277c688dd67e5d99830`.

Consulta del PDF local: 2026-11-20. El enlace previo señalaba la página 95, que contiene el artículo 176, y no sustenta este proceso. El texto local está consolidado hasta el 09-01-2026; su vigencia posterior y aplicabilidad al contrato concreto siguen pendientes de control con la edición oficial actual. Conocimiento normativo propuesto, no `VALIDADO`.

## Piloto de auditoría por elemento — 2026-11-20

Esta prueba se limita a **S4.3.2.7** y al PDF local citado. Se comprobó que la página 60 contiene texto extraíble y se inspeccionó la página renderizada. Los anclajes de T1, T2, T4 y ST guardan rectángulos del pasaje en `S4-3-2-7-fuentes-visor.json`, ligados al hash y a la página. El visor solo proyecta esos rectángulos: no busca palabras al abrir el PDF. Como la vigencia posterior a enero de 2026 no está comprobada, las coincidencias con el texto local no equivalen a sustento normativo definitivo.

| ID | Resultado del contraste | Hallazgo o límite |
|---|---|---|
| E1 | `INFERENCIA` | El inicio por recepción de necesidad es una propuesta de flujo; falta identificar originador y medio institucional. |
| T1 | Cita local localizada; `EVIDENCIA-INSUFICIENTE` sobre vigencia | El art. 109.1 atribuye el sustento al área usuaria y enumera finalidad, prestaciones no ejecutadas/divisibles/cuantificables, oportunidad y límite del 25 %. El carril concreto sigue por confirmar. |
| G1 | `INFERENCIA` | La compuerta traduce las condiciones del art. 109.1; el cierre por falta de acreditación no es una denegación de fondo. |
| T2 | `CONTRADICCION` | El modelo solicita siempre opinión. El art. 109.1 d del texto local dice «de corresponder»; falta una condición que evite imponer esta ruta a todos los casos. |
| M1 | `INFERENCIA` | Recepción de opinión coherente solo cuando se activó T2; no hay fuente para un medio específico. |
| T3 | `EVIDENCIA-INSUFICIENTE` | Integración y controles internos propuestos; falta unidad responsable y procedimiento. |
| T4 | Cita local localizada; `EVIDENCIA-INSUFICIENTE` sobre vigencia | El art. 109.1-109.3 menciona resolución de la autoridad, decisión sobre efecto en plazo y publicación en Pladicop. «Notificar» requiere precisar la vía; no se debe inferir otra notificación obligatoria. |
| G2 | `INFERENCIA` | Separar la decisión favorable o no favorable es lógica de modelamiento, no un texto literal del artículo. |
| T5 | `EVIDENCIA-INSUFICIENTE` | La actualización de alcance y registros es propuesta operativa; la publicación en Pladicop sí aparece en el art. 109.3 local y debe reflejarse expresamente en la ruta favorable. |
| F1 | `INFERENCIA` | El cierre por comunicación es propuesto; medio y momento pendientes. |
| F2 | `INFERENCIA` | El cierre no favorable es propuesto; falta procedimiento institucional de comunicación. |
| F0 | `INFERENCIA` | Se mantiene como caso pendiente, no denegación de fondo; otras rutas siguen sin acreditar. |
| SE | `EVIDENCIA-INSUFICIENTE` | El art. 109.1 d menciona supervisor, «de corresponder»; no acredita por sí solo un inspector alternativo para esta opinión. |
| ST | `CONTRADICCION` parcial | La opinión del supervisor aparece en el texto local, pero el carril «supervisor o inspector» excede esa cita sin otra fuente que sustente al inspector. |
| SF | `INFERENCIA` | El envío de la opinión es una representación funcional de contar con ella; falta medio y plazo específico. |
| Mensaje T2→SE | `CONTRADICCION` heredada | El mensaje queda incondicional mientras T2 lo sea; debe depender de la condición «de corresponder». |
| Mensaje SF→M1 | `INFERENCIA` | Intercambio propuesto solo para la ruta con opinión; no se acredita un canal concreto. |

**Resultado del piloto:** 15 elementos y dos mensajes examinados; cuatro anclajes PDF preparados. La página errónea se corrigió en este sustento. No se ha cambiado la tabla ni se ha declarado conforme el modelo. Antes de modificar las rutas T2/ST y la publicación de T4/T5, se debe comprobar la edición oficial aplicable y el supuesto contractual; las discrepancias permanecen abiertas. El servicio de conversión PDF a searchable/Markdown ofrecido por el usuario aún no está disponible en esta sesión; el piloto usó el texto extraíble del original y su renderización local.

## Auditoría con herramientas — 2026-11-24

Segunda pasada del piloto con las herramientas de la fase 4 ([informe del piloto](../../../../../05-herramientas/gestor-modelos/docs/informe-piloto-auditoria-S4-3-2-7.md); [detalle generado](../../../../../05-herramientas/gestor-modelos/auditorias/S4-3-2-7/informe.md)). Hay 25 afirmaciones registradas con cita verificada: 6 `SUSTENTADA`, 13 `INFERENCIA`, 3 `EVIDENCIA-INSUFICIENTE` y 3 `CONTRADICCION`. Son propuestas de IA, sin validación normativa ni conformidad.

- Se mantienen las contradicciones de T2 y del mensaje T2→SE: el modelo pide siempre la opinión de supervisión y el Reglamento art. 109.1 d) dice «de corresponder». Se formula como contradicción la omisión en T5 de la publicación en la Pladicop exigida por el art. 109.3.
- Cambian SE (de `EVIDENCIA-INSUFICIENTE` a `INFERENCIA`) y ST con inspector (de `CONTRADICCION` parcial a `INFERENCIA`). El Reglamento art. 186.1, PDF p. 101, asigna la supervisión de obra «al supervisor o el inspector». La extensión al inspector de la opinión del 109.1 d) no es literal y requiere confirmación.
- Fuentes añadidas con ancla en el visor: Ley 32069 arts. 63.1, 63.3 y 64.1 (PDF pp. 30-31, texto local al 19-07-2026, SHA-256 `f14ffa37b824b8af…`); Reglamento arts. 19 c) (p. 11), 117.3-117.4 (p. 64), 186.1 (p. 101) y 257.1 (p. 141). Consulta: 2026-11-24. La vigencia posterior sigue pendiente.
- Hallazgo nuevo: con la reducción del monto, el contratista puede pedir la disminución proporcional de garantías (art. 117.3), con 10 días hábiles para la adecuación (art. 117.4). El modelo no muestra esa interfaz.
- Propuestas no aplicadas a la tabla: condicionar T2 y la ruta de supervisión; nombrar la publicación en la Pladicop en T4/T5; registrar la interfaz de garantías; documentar la variante con inspector. Requieren antes el control de vigencia y la evaluación del usuario.

## Elementos registrados

- OBSERVADO: el usuario acepta dividir el proceso y conserva tres casos en S4.3.2.3 (2026-11-18).
- DECISION de modelamiento: DEC-047 asigna S4.3.2.7 como hermano de nivel 3; no es una conformidad institucional.
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

Sin conformidades registradas. Documentos en ELABORACION. 2026-11-24: auditoría con herramientas registrada y anclas automáticas añadidas a `S4-3-2-7-fuentes-visor.json`; derivado HTML regenerado con D1-D5 sin hallazgos. La tabla no cambió.

## Relaciones

- Se rige por [decision de arquitectura](../../../../../00-gobernanza/registro-decisiones.md).
- Se separa de [S4.3.2.3](../S4-3-2-3-gestion-adicionales-deductivos-obra/00-S4-3-2-3-gestion-adicionales-deductivos-obra.md).
- Se integra en [S4.3.2](../00-S4-3-2-ejecucion.md).

## Control tecnico de la division

D1, D2 y D5 sin hallazgos. D3 sin bloqueos. D4: un cruce de mensaje con etiqueta (T6) al solicitar opinion de supervision. Se adoptan derivados de trabajo con --forzar para sincronizar la propuesta conceptual; no constituyen una linea base lista para publicacion. Revision visual y cierre de hallazgos pendientes. Informe reproducible: 99-temporal/modelos/S4-3-2-7-diagrama-proceso/validacion.txt.
