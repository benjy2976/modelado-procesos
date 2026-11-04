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
fecha_actualizacion: 2026-11-04
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

## Delimitacion aplicada

El Bizagi de Consultas contiene tambien suspension y aprobacion de adicionales o reducciones. Esas ramas no forman parte del producto "consulta absuelta": se utilizan como insumo de S4.3.2.3. Este proceso termina al notificar la respuesta y, cuando corresponda, al comunicar la solicitud o causal de modificacion.

## Elementos registrados

| Elemento | Contenido | Clase | Fuente |
|---|---|---|---|
| Disparador | Consulta anotada en el cuaderno de obra | `NORMATIVO` citado | Reglamento, art. 190 |
| Instancia | Una por consulta | `DECISION` | DEC-032 |
| Participantes | Contratista o residente, supervisor o inspector, SGGOS, SGE y proyectista cuando corresponda | `OBSERVADO` y `NORMATIVO` citado | Bizagi; Reglamento, art. 190; ROF, arts. 95-98 |
| Responsable de la absolucion tecnica en el GORE Huanuco | Sub Gerencia de Estudios (SGE) | `NORMATIVO-INSTITUCIONAL` propuesto | ROF, art. 96, lit. i |
| Seguimiento y canalizacion institucional | Sub Gerencia de Gestion de Obras y Supervision (SGGOS) | `NORMATIVO-INSTITUCIONAL` propuesto e `INFERENCIA` de modelamiento | ROF, arts. 97-98; el circuito documental exacto requiere evidencia operativa |
| Elaboracion del sustento de la respuesta | Especialistas de la SGE elaboran el informe tecnico de absolucion | `OBSERVADO` y `DECISION` | Descripcion del equipo; DEC-033 |
| Firma de la respuesta | El Subgerente de Estudios revisa y firma siempre la respuesta a la consulta | `OBSERVADO` y `DECISION` | Descripcion del equipo; DEC-033 |
| Consulta originada por la supervision | Puede elevarse sin consulta previa del contratista | `OBSERVADO` | Descripcion del equipo; caso excepcional |
| Producto principal | Consulta absuelta y notificada | `PROPUESTA` | Analisis del flujo observado |
| Producto alterno | Respuesta y causal comunicadas a S4.3.2.3 | `PROPUESTA` | DEC-032 |

## Vacios de evidencia

| Vacio | Marca | Fuente o accion necesaria |
|---|---|---|
| Nombre, serie documental, custodia y medio exacto de notificacion | `EVIDENCIA-INSUFICIENTE` | Procedimiento documentario o muestra no sensible del tramite real |
| Criterio exacto para involucrar al proyectista | `EVIDENCIA-INSUFICIENTE` | Fuente contractual, expediente y validacion del equipo |
| Variante con inspector perteneciente a la entidad | `EVIDENCIA-INSUFICIENTE` | Levantamiento del circuito interno aplicable |
| Indicador, meta y fuente de datos | `EVIDENCIA-INSUFICIENTE` | Definicion del dueno del proceso |

## Discrepancias

| Hallazgo | Tratamiento |
|---|---|
| El Bizagi no tiene evento de inicio general y contiene enlaces sin pareja | No se copia el XML; se adopta como inicio el mensaje de consulta anotada y se reconstruye el flujo |
| El Bizagi mezcla consulta con suspension y adicional | Se separan mediante el limite entre S4.3.2.2 y S4.3.2.3 |
| El Bizagi representa a la entidad sin distinguir sus unidades internas | El rediseño debe separar al menos SGGOS y SGE: SGGOS recibe, sigue y canaliza; SGE analiza y absuelve tecnicamente conforme al ROF |

## Criterio para el rediseño institucional

La exigencia nacional de que la entidad absuelva la consulta se concreta, para el Gobierno Regional Huanuco, mediante la competencia asignada a la SGE por el articulo 96, literal i, del ROF. Por tanto, el modelo no debe dejar la absolucion sustantiva en una actividad generica de la entidad ni atribuirla al rol Monitor.

La SGGOS conserva un papel diferenciado de control, seguimiento, recepcion y canalizacion del tramite. Cuando se requiera opinion del proyectista, la SGE conduce el analisis tecnico y continua hasta producir la absolucion institucional aun si el proyectista no se pronuncia dentro del plazo aplicable. El modelo utiliza una compuerta basada en eventos para esperar la opinion o el vencimiento del plazo, rutas que convergen en la elaboracion del informe tecnico de absolucion.

`DEC-033` cierra el vacio operativo de autoria y firma: los especialistas de la SGE elaboran el informe tecnico y el Subgerente de Estudios revisa y firma siempre la respuesta. Esta precision proviene del equipo y no se presenta como una exigencia extraida del ROF. La OACGD registra la entrada y canaliza la notificacion; la denominacion y serie exactas de los documentos permanecen pendientes.

El diagrama base representa supervision contratada como participante externo. Si la obra cuenta con inspector, este pertenece a la entidad y sus actividades deben reubicarse en el pool del GORE Huanuco; no se lo representa como un participante externo equivalente al supervisor.

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

## Relaciones

- [S4.3.2.3 Gestion de modificaciones](../S4-3-2-3-gestion-modificaciones-alcance-plazo/00-S4-3-2-3-gestion-modificaciones-alcance-plazo.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)

