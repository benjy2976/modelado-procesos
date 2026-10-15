---
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# Manual operativo para construir y usar conocimiento

[Inicio](../00-inicio.md) · [Gobernanza](README.md)

## 1. Proposito

Este manual define la linea de trabajo comun para convertir documentos, evidencia institucional y aportes del equipo en conocimiento trazable; utilizar ese conocimiento en analisis, propuestas y modelos; y aplicar las validaciones humanas que correspondan antes de publicar una linea base.

Complementa, sin reemplazar, los siguientes documentos:

- [Protocolo de conocimiento confiable](protocolo-conocimiento-confiable.md): estados y controles de las reglas normativas.
- [Protocolo de trabajo con IA](protocolo-trabajo-con-ia.md): limites y forma de participacion de la IA.
- [Metodologia de modelamiento](metodologia-modelamiento.md): secuencia para AS-IS, analisis y TO-BE.
- [Versionado y releases](protocolo-versionado-y-releases.md): revision, aprobacion y publicacion con Git.

Cuando exista contradiccion, prevalecen las fuentes oficiales, las decisiones aprobadas y los protocolos especificos aplicables.

## 2. Principio rector

Ninguna afirmacion adquiere autoridad por estar bien redactada, aparecer en un Markdown, haber sido generada por IA o coincidir con la experiencia del equipo. Su uso depende de su tipo, evidencia, estado y validacion.

La cadena minima de trazabilidad es:

```text
FUENTE
  -> REGISTRO DOCUMENTAL Y HASH
  -> EXTRACCION TRAZABLE
  -> UNIDAD DE CONOCIMIENTO
  -> VALIDACION CORRESPONDIENTE
  -> PAQUETE DE CONTEXTO
  -> ANALISIS, PROPUESTA O MODELO
  -> REVISION INTEGRADA
  -> LINEA BASE / RELEASE
```

No se salta una etapa mediante copia manual. Los vinculos se mantienen con identificadores estables y rutas relativas.

## 3. Clases de informacion

Toda afirmacion relevante debe clasificarse antes de usarla.

| Clase | Que representa | Evidencia minima | Puede imponer una obligacion |
|---|---|---|---|
| `NORMATIVO` | Exigencia, permiso, prohibicion, condicion o definicion de una norma aplicable | Fuente oficial, ubicacion precisa, vigencia y regla validada | Si, solo cuando esta validada y resulta aplicable |
| `OBSERVADO` | Practica, actividad, problema o dato del funcionamiento real | Entrevista, registro, sistema, expediente anonimizado u otra evidencia AS-IS confirmada | No |
| `REFERENCIA` | Guia, estandar, manual, caso o buena practica | Documento identificado, calidad comprobada y alcance declarado | No, salvo que otra regla aplicable la incorpore expresamente |
| `INFERENCIA` | Conclusion obtenida al relacionar evidencia | Premisas citadas, razonamiento visible y revision analitica | No |
| `PROPUESTA` | Alternativa de diseno o mejora | Problema u objetivo, supuestos, impactos y criterios de evaluacion | No; requiere decision y aprobacion |
| `DECISION` | Eleccion adoptada por el equipo o autoridad competente | Registro de decision, responsable, fecha, alcance e impacto | Obliga al proyecto dentro del alcance aprobado |

Una misma fuente puede originar varias unidades de conocimiento. Cada unidad debe ser atomica: expresa una sola regla, observacion, referencia, inferencia, propuesta o decision comprobable.

## 4. Autoridad de las fuentes

La prioridad se evalua segun materia y aplicabilidad, no solo por el formato del archivo.

1. Norma vigente y fuente oficial aplicable.
2. Documento institucional aprobado dentro de su competencia y vigencia.
3. Evidencia institucional del AS-IS.
4. Estandar o guia tecnica adoptada o aplicable.
5. Referencia tecnica no adoptada, literatura o buena practica.
6. Aporte de especialista, inferencia o propuesta.
7. Salida de IA sin validacion.

Una fuente de menor nivel puede ayudar a interpretar o disenar, pero no contradecir ni sustituir una fuente aplicable de mayor autoridad. Si dos fuentes aparentemente aplicables entran en conflicto, se registra el conflicto y se suspende la conclusion hasta obtener revision competente.

## 5. Roles funcionales

Los siguientes son roles del flujo, no cargos organicos. Una persona puede desempeñar mas de uno cuando la segregacion y el riesgo lo permitan; la asignacion debe quedar registrada.

| Rol | Funcion en el flujo |
|---|---|
| Curador documental | Registra procedencia, hash, formato, calidad y extraccion |
| Proponente | Formula la unidad de conocimiento o la propuesta |
| Especialista tematico o normativo | Valida vigencia, interpretacion y aplicabilidad dentro de su especialidad |
| Referente operativo | Confirma que la descripcion AS-IS representa la practica real |
| Responsable metodologico | Revisa alcance, consistencia, separacion AS-IS/TO-BE y notacion BPMN |
| Especialista BIM | Revisa requisitos e intercambios de informacion BIM cuando correspondan |
| Responsable de aprobacion | Autoriza la linea base o decision segun la gobernanza que defina el proyecto |
| Agente IA | Extrae, estructura, compara y propone; nunca valida ni aprueba |

## 6. Flujo operativo

### 6.1 Ingresar y clasificar la fuente

1. Identificar la procedencia y obtenerla desde una fuente oficial o autorizada cuando corresponda.
2. Registrar URL, fecha de consulta, emisor, tipo, vigencia conocida y SHA-256.
3. Guardar el original sin modificar bajo `01-referencias/**/originales` o registrar su ubicacion reproducible.
4. Clasificarla como normativa, institucional, tecnica, evidencia AS-IS o referencia.
5. Registrar dudas de autenticidad, integridad, vigencia o alcance como pendientes; no completarlas por suposicion.

**Puerta F1 - Fuente utilizable:** identidad conocida, original preservado, hash registrado y procedencia verificable.

### 6.2 Evaluar calidad y producir la extraccion

1. Medir si el archivo contiene texto utilizable.
2. Aplicar OCR solo a una copia derivada cuando sea necesario.
3. Conservar marcadores de pagina y, cuando corresponda, articulo, numeral, tabla o anexo.
4. Comparar visualmente muestras criticas: encabezados, tablas, notas, formulas, firmas y paginas citadas.
5. Marcar la extraccion como `SIN-REVISAR`, `REVISADO-PARCIAL`, `REVISADO-COMPLETO` o `NO-CONFIABLE` de acuerdo con la evidencia disponible.

**Puerta F2 - Extraccion utilizable:** correspondencia comprobada con el original en los pasajes que se emplearan. El original siempre prevalece.

### 6.3 Formular unidades de conocimiento

1. Seleccionar un pasaje o evidencia concreta.
2. Clasificar la unidad segun la seccion 3.
3. Redactar una afirmacion atomica, sin ampliar lo que la fuente sostiene.
4. Registrar condiciones, excepciones, alcance, actores, objetos, plazos y evidencias solo si constan.
5. Vincular documento, hash, ubicacion precisa, extraccion y fecha de consulta.
6. Distinguir texto citado, parafrasis e interpretacion.
7. Si falta sustento, registrar `EVIDENCIA-INSUFICIENTE` y la accion necesaria.

Las reglas normativas usan `04-recursos-reutilizables/plantillas/regla-normativa.yaml`. Hasta disponer de plantillas especificas para las otras clases, estas se documentan en el artefacto de analisis con su clase visible, evidencia y estado de revision.

**Puerta F3 - Propuesta revisable:** campos obligatorios completos, fuente localizable, afirmacion atomica y estado inicial correcto (`BORRADOR-IA` o `BORRADOR-HUMANO`).

### 6.4 Aplicar la validacion correspondiente

No todas las afirmaciones requieren las mismas revisiones.

| Objeto | Validacion obligatoria | Resultado habilitado |
|---|---|---|
| Regla normativa | Calidad documental, vigencia, ubicacion, interpretacion y aplicabilidad por especialista | Uso normativo en modelos y publicaciones |
| Hecho AS-IS | Correspondencia con evidencia y confirmacion de referente operativo | Inclusion en narrativa y BPMN AS-IS |
| Referencia tecnica | Procedencia, calidad, alcance y pertinencia metodologica o tecnica | Uso como criterio de analisis, no como obligacion |
| Inferencia | Premisas completas, razonamiento y ausencia de contradiccion | Uso en analisis con etiqueta visible |
| Requisito o intercambio BIM | Fuente, aplicabilidad al caso y revision BIM; revision normativa adicional si se presenta como obligacion | Uso en analisis o TO-BE segun su clase |
| Propuesta TO-BE | Cumplimiento, factibilidad operativa, coherencia metodologica, impacto y decision del responsable | Incorporacion al modelo TO-BE aprobado |
| Elemento BPMN | Correspondencia con narrativa, semantica BPMN, reglas y evidencia vinculadas | Inclusion en el modelo revisado |
| Linea base | Integridad, trazabilidad, resolucion de observaciones y aprobacion registrada | Tag y release |

La validacion de un aspecto no valida los demas. Por ejemplo, una cita correcta no demuestra vigencia; una regla vigente no demuestra que el AS-IS la cumpla; y una propuesta tecnicamente atractiva no equivale a una decision aprobada.

**Puerta F4 - Conocimiento autorizado:** validacion humana registrada, alcance explicito y evento de revision disponible. Para reglas normativas se exige el estado `VALIDADO`.

### 6.5 Publicar en la base de conocimiento

1. Guardar las reglas en `04-recursos-reutilizables/conocimiento/reglas/`.
2. Registrar cada revision humana en `04-recursos-reutilizables/conocimiento/revisiones/`; los eventos no se reescriben.
3. Regenerar `catalogo-reglas.csv`; no editarlo manualmente.
4. Relacionar reemplazos, dependencias, procesos y actividades BPMN.
5. Confirmar que el commit conserva cambios legibles y no incluye originales publicos regenerables.

El catalogo es una vista de consulta. Los YAML y eventos son la fuente maestra del conocimiento estructurado; el original es la evidencia documental.

### 6.6 Preparar el paquete de contexto

Antes de una tarea de analisis o modelamiento se crea un paquete basado en `04-recursos-reutilizables/plantillas/paquete-contexto.yaml`.

El paquete incluye solo:

- ficha y limites del proceso;
- modelo vigente, si existe;
- reglas validadas aplicables;
- fuentes pendientes autorizadas, con su estado visible;
- evidencia AS-IS seleccionada;
- glosario pertinente;
- preguntas abiertas;
- archivos modificables y criterio de cierre.

Una fuente pendiente puede emplearse para investigar o formular una propuesta, pero no para afirmar cumplimiento ni justificar una linea base como si estuviera validada.

**Puerta F5 - Contexto autorizado:** contenido minimo, suficiente y aprobado para la tarea; no se carga la biblioteca completa.

### 6.7 Construir analisis, propuestas y modelos

1. Delimitar el problema y el producto esperado.
2. Separar en todo momento `OBSERVADO`, `NORMATIVO`, `REFERENCIA`, `INFERENCIA` y `PROPUESTA`.
3. Mantener AS-IS, analisis y TO-BE en artefactos separados.
4. Asignar identificadores estables a actividades, decisiones, reglas y propuestas.
5. Vincular cada elemento relevante con su evidencia o regla.
6. Registrar alternativas descartadas y la razon de la decision cuando afecten el alcance o el diseno.
7. Mantener BPMN 2.0 XML como fuente maestra; SVG y PDF son derivados.

**Puerta F6 - Producto revisable:** trazabilidad completa, supuestos visibles, preguntas abiertas identificadas y ausencia de afirmaciones normativas no autorizadas.

### 6.8 Revisar y aprobar el producto

La revision se ejecuta por dimensiones y conserva observaciones:

1. **Operativa:** flujo real, responsables, variantes y excepciones del AS-IS.
2. **Normativa:** reglas, vigencia, alcance, cumplimiento y conflictos.
3. **Metodologica:** limites, niveles, coherencia narrativa-BPMN y convenciones.
4. **BIM:** usos, informacion, intercambios, responsabilidades y requisitos aplicables.
5. **Consistencia:** correspondencia entre fichas, matrices, BPMN, indicadores y decisiones.
6. **Aprobacion:** aceptacion de la linea base por el responsable definido para el producto.

Una observacion se cierra con evidencia o decision registrada, no eliminandola sin explicacion.

**Puerta F7 - Publicable:** revisiones aplicables completadas, observaciones criticas cerradas, manifiesto preparado y aprobacion registrada. La publicacion se identifica mediante tag y release.

### 6.9 Mantener y revalidar

Un cambio de fuente, hash, vigencia, alcance, extraccion o decision activa el analisis de impacto. Las reglas afectadas pasan a `REVALIDACION-REQUERIDA` y dejan de sustentar nuevas publicaciones hasta completar la revision.

El impacto se rastrea en este orden:

```text
FUENTE CAMBIADA
  -> UNIDADES DE CONOCIMIENTO
  -> PAQUETES DE CONTEXTO
  -> ACTIVIDADES Y MODELOS BPMN
  -> ANALISIS Y PROPUESTAS
  -> LINEAS BASE PUBLICADAS
```

## 7. Criterios de uso segun el estado

| Estado o condicion | Analisis exploratorio | Modelo de trabajo | Linea base publicada |
|---|---:|---:|---:|
| Fuente pendiente claramente etiquetada | Si | Si, como pendiente | No |
| `BORRADOR-IA` o `BORRADOR-HUMANO` | Si | Si, con advertencia | No |
| `PROPUESTO` o `EN-REVISION` | Si | Si, con advertencia | No |
| Regla `VALIDADO` y aplicable | Si | Si | Si |
| Clase `OBSERVADO` confirmada | Si | Si en AS-IS | Si, si completa las revisiones del producto |
| `INFERENCIA` revisada | Si | Si, identificada | Solo como analisis, nunca como hecho o regla |
| `PROPUESTA` aprobada | Si | Si en TO-BE | Si |
| Estado de validacion `OBSERVADO`, `REVALIDACION-REQUERIDA` o `RETIRADO` | Solo para historial o correccion | No como sustento vigente | No |

## 8. Lista de comprobacion minima por tarea

Antes de iniciar:

- [ ] El objetivo y el producto esperado estan definidos.
- [ ] El paquete de contexto limita las fuentes y archivos modificables.
- [ ] Se conocen las validaciones aplicables.
- [ ] No se incluyeron datos personales, credenciales ni expedientes sensibles.

Antes de entregar a revision:

- [ ] Cada afirmacion relevante tiene clase, fuente y estado.
- [ ] Las citas incluyen ubicacion precisa y fecha de consulta.
- [ ] Las reglas usadas son validas para el alcance o estan marcadas como pendientes.
- [ ] AS-IS, analisis y TO-BE permanecen separados.
- [ ] Los vacios aparecen como preguntas o `EVIDENCIA-INSUFICIENTE`.
- [ ] Narrativa, BPMN y matrices usan identificadores consistentes.

Antes de publicar:

- [ ] Se completaron las revisiones operativa, normativa, metodologica y BIM que apliquen.
- [ ] No existen observaciones criticas abiertas.
- [ ] Las reglas normativas utilizadas estan `VALIDADO` y no requieren revalidacion.
- [ ] Existe aprobacion humana registrada.
- [ ] El manifiesto relaciona fuentes, reglas, decisiones y commit.
- [ ] El tag y la release identifican la linea base.

## 9. Uso con Obsidian, Git e IA

- La produccion de notas debe cumplir el [Estandar obligatorio de Obsidian](estandar-obligatorio-obsidian.md).
- Obsidian facilita navegacion, busqueda y enlaces; no crea una fuente de verdad adicional.
- Git conserva autoria, diferencias e historia; los nombres de archivo permanecen estables.
- Las ramas o solicitudes de cambio soportan revision; los tags y releases soportan publicacion.
- La IA recibe paquetes de contexto, no la biblioteca completa.
- Una respuesta de IA es borrador hasta que complete las validaciones humanas aplicables.
- Los datos sensibles permanecen fuera de prompts y servicios externos no autorizados.

## 10. Implantacion progresiva

1. Probar este manual con un conjunto pequeno de reglas de gestion por procesos.
2. Registrar dificultades, ambiguedades y tiempos de revision.
3. Ajustar plantillas y estados mediante decision registrada.
4. Implementar validaciones de esquema y generacion del catalogo.
5. Construir la consulta web y luego el flujo autenticado de validacion.
6. Aplicar el flujo al piloto S4.3 antes de extenderlo a otros procesos.

