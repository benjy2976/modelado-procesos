# Protocolo de conocimiento confiable

## Objetivo

Convertir fuentes oficiales y evidencia institucional en conocimiento estructurado, trazable y validado por especialistas. Este protocolo es un requisito del proyecto y constituye una puerta de control previa al uso normativo de una regla en modelos publicados.

## Capas de informacion

| Capa | Fuente maestra | Uso |
|---|---|---|
| Evidencia | PDF u otro original inmutable | Prueba documental |
| Extraccion | Markdown derivado con marcadores de pagina | Busqueda y lectura asistida |
| Regla propuesta | YAML individual | Analisis y revision del especialista |
| Regla validada | YAML aprobado y eventos de revision | Conocimiento autorizado para modelamiento |
| Catalogo | CSV generado desde los YAML | Consulta, filtros e interfaz web |
| Paquete de contexto | YAML por tarea | Entrega minima de conocimiento a personas o IA |

El Markdown extraido nunca sustituye al original. Si difieren, prevalece el original y la extraccion debe corregirse o marcarse como no confiable.

Las extracciones se generan bajo `01-referencias/09-derivados-texto/cache/` segun `05-herramientas/extractor-documental/README.md`. Son cache reproducible y no se versionan de forma masiva. Las reglas, revisiones y decisiones curadas si se versionan.

## Flujo obligatorio

```text
FUENTE-VERIFICADA
    -> TEXTO-EXTRAIDO
    -> EXTRACCION-REVISADA
    -> BORRADOR-IA o BORRADOR-HUMANO
    -> PROPUESTO
    -> EN-REVISION
    -> VALIDADO u OBSERVADO
    -> REVALIDACION-REQUERIDA o RETIRADO
```

- `BORRADOR-IA`: contenido generado o transformado por un modelo; no es utilizable como regla confiable.
- `BORRADOR-HUMANO`: formulacion inicial de un integrante del equipo.
- `PROPUESTO`: contiene todos los campos y citas obligatorias.
- `EN-REVISION`: asignado a un especialista competente.
- `VALIDADO`: el especialista confirmo texto, vigencia, aplicabilidad e interpretacion.
- `OBSERVADO`: requiere correccion y conserva las observaciones.
- `REVALIDACION-REQUERIDA`: una dependencia cambio y suspende su uso como regla confiable.
- `RETIRADO`: ya no debe usarse; se conserva por trazabilidad.

Solo una persona autorizada puede establecer `VALIDADO`. La aplicacion y los agentes deben impedir que un modelo de IA ejecute esa transicion.

## Contenido minimo de una regla

Cada regla se basa en `00-gobernanza/plantillas/conocimiento/regla-normativa.yaml` e incluye:

1. Identificador estable.
2. Enunciado atomico y tipo: obligacion, prohibicion, permiso, condicion, definicion o recomendacion.
3. Actor, accion, objeto, condiciones, excepciones, plazo y evidencia cuando existan.
4. Ambito de aplicacion: proceso, etapa, modalidad y tipologia.
5. Documento, hash, articulo o numeral, pagina PDF y fecha de consulta.
6. Estado de vigencia separado del estado de validacion.
7. Origen humano o IA y nivel de revision de la extraccion.
8. Historial de observaciones y eventos de validacion.

No se inventan campos ausentes en la fuente; se usa `null`, lista vacia o `EVIDENCIA-INSUFICIENTE` segun corresponda.

## Puertas de control

Una regla solo puede pasar a `VALIDADO` cuando:

- el archivo original coincide con el hash registrado;
- la cita existe en la ubicacion indicada;
- tablas, notas, anexos y referencias cruzadas necesarias fueron revisadas visualmente;
- la vigencia y modificatorias se comprobaron en fuente oficial;
- el alcance y las condiciones de aplicacion estan expresos;
- las inferencias estan diferenciadas del contenido normativo;
- el especialista registra identificador, especialidad, fecha y resultado;
- existe un evento de revision inmutable.

## Revalidacion automatica

Toda regla vinculada cambia a `REVALIDACION-REQUERIDA` cuando ocurra al menos uno de estos eventos:

- cambia el SHA-256 del documento fuente;
- se incorpora una modificatoria o derogacion relacionada;
- cambia la ubicacion del articulo, numeral o anexo;
- se corrige una extraccion que afecte el sentido;
- cambia la modalidad, tipologia o alcance del proceso donde se aplica;
- el especialista retira su validacion justificadamente.

## Segregacion y auditoria

Cuando sea viable, quien valida no debe ser la unica persona que propuso la regla. Cada aprobacion, observacion, retiro o revalidacion genera un evento basado en `00-gobernanza/plantillas/conocimiento/evento-revision.yaml`. Los eventos no se reescriben; una rectificacion se registra como un evento nuevo.

## Uso en modelos

Las releases de procesos deben relacionar las reglas validadas utilizadas. Una regla no validada puede aparecer en analisis con su estado visible, pero no sustentar por si sola una afirmacion normativa de una linea base publicada.
