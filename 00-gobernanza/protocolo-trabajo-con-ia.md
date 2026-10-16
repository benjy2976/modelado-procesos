# Protocolo de trabajo con inteligencia artificial

## Proposito

La inteligencia artificial se usa como apoyo para localizar, extraer, estructurar, contrastar, modelar y revisar informacion. No sustituye la interpretacion del especialista, la validacion del dueno del proceso ni la aprobacion institucional.

Toda tarea asistida por IA debe poder reconstruirse a partir de fuentes identificadas, instrucciones explicitas y salidas versionadas.

## Principios obligatorios

1. La IA trabaja solo con el paquete de contexto autorizado para la tarea.
2. Ninguna afirmacion normativa se sustenta en memoria general del modelo.
3. Se distinguen siempre evidencia observada, exigencia normativa, inferencia y propuesta.
4. Si la evidencia es insuficiente se registra `EVIDENCIA-INSUFICIENTE`; no se completa el vacio por plausibilidad.
5. La IA puede proponer reglas, relaciones y modelos, pero no asignarles estado `VALIDADO`.
6. AS-IS, analisis y TO-BE permanecen separados.
7. Una obligacion normativa no demuestra por si misma que una actividad ocurra en el AS-IS.
8. Una practica observada no se presenta como obligatoria sin fuente normativa.
9. Las salidas deben conservar identificadores estables y referencias precisas.
10. No se remiten datos personales, credenciales ni expedientes sensibles a servicios externos.

## Funciones de apoyo

| Funcion | Puede realizar la IA | Requiere decision humana |
|---|---|---|
| Biblioteca | Detectar texto, extraer, indexar y señalar defectos | Aceptar calidad y correspondencia con el original |
| Analisis normativo | Identificar pasajes y proponer reglas atomicas | Confirmar vigencia, aplicabilidad e interpretacion |
| Levantamiento | Estructurar notas y detectar vacios | Confirmar que representan la practica real |
| Modelamiento | Proponer narrativa, relaciones y BPMN | Validar alcance, flujo, responsables y excepciones |
| Revision | Detectar inconsistencias y trazabilidad incompleta | Resolver conflictos y aprobar correcciones |
| Publicacion | Preparar manifiesto y lista de comprobacion | Autorizar la linea base y la release |

## Paquete de contexto

Cada tarea debe declarar un archivo basado en `00-gobernanza/plantillas/conocimiento/paquete-contexto.yaml`. Como minimo contiene:

- objetivo y producto esperado;
- proceso, modalidad y limites;
- archivos que la IA puede consultar;
- reglas validadas aplicables;
- fuentes pendientes permitidas para analisis;
- evidencia AS-IS seleccionada;
- restricciones y preguntas abiertas;
- archivos que pueden modificarse;
- criterio de cierre.

No se carga la biblioteca completa. Si durante el trabajo aparece una dependencia no incluida, se registra como pregunta o solicitud de contexto.

## Contrato minimo de una solicitud

```markdown
## Objetivo
## Producto esperado
## Contexto autorizado
## Fuentes normativas
## Restricciones
## Trazabilidad requerida
## Formato de salida
## Preguntas abiertas
## Criterio de cierre
```

Toda solicitud normativa debe incluir esta regla:

> No utilices conocimiento general para formular afirmaciones normativas. Si las fuentes autorizadas no sostienen una conclusion, registra EVIDENCIA-INSUFICIENTE e identifica la fuente o validacion faltante.

## Forma de respuesta

Las afirmaciones relevantes se clasifican como:

- `OBSERVADO`: respaldado por evidencia del funcionamiento real.
- `NORMATIVO`: respaldado por una regla validada o por una fuente citada pendiente de validacion.
- `INFERENCIA`: conclusion analitica que debe contrastarse.
- `PROPUESTA`: alternativa de diseno TO-BE.

Cuando la respuesta use una fuente aun no curada debe indicar documento, articulo o numeral, pagina PDF, fecha de consulta y estado de vigencia. No puede presentarla como conocimiento confiable hasta completar `00-gobernanza/protocolo-conocimiento-confiable.md`.

## Revision independiente

Los productos de riesgo alto se revisan en una segunda pasada separada de la generacion. El revisor, humano o asistido por otro modelo, busca omisiones, contradicciones, citas incorrectas, supuestos y divergencias entre narrativa, BPMN, matrices y reglas. La coincidencia entre modelos no equivale a validacion humana.
