---
id: HER-MESA-MODELAMIENTO-INFORME-PILOTO-S4-3-2-7
tipo: informe
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
proceso:
  - S4.3.2.7
fecha_creacion: 2026-11-24
fecha_actualizacion: 2026-11-24
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-7
---

# Informe del piloto de auditoría S4.3.2.7 (fase 4)

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md). Procedimiento en el [plan de corrida](plan-corrida-documental-y-auditoria.md); el detalle por afirmación está en el [informe generado de la auditoría](../auditorias/S4-3-2-7/informe.md).

Este informe presenta el piloto para la evaluación del usuario (puerta 4.P). Las clasificaciones son propuestas de un agente de IA. No validan normas, no atribuyen conformidad y no cambian el estado del modelo, que sigue en `ELABORACION`.

## Qué se hizo

1. **Banco de recuperación (4.C1–4.E2).** Se preparó un banco provisional de 13 preguntas positivas y 2 negativas a partir de la tabla y el sustento de S4.3.2.7 ([banco](../bancos-prueba/S4-3-2-7.json)). Los pasajes esperados se cotejaron con el render del PDF original: Ley 32069, pp. 30-31; Reglamento, pp. 60, 64 y 101. Las negativas comprueban dos riesgos señalados en el sustento: confundir la reducción contractual con la reducción negociada en la selección (arts. 132.2 y 167.2) y trasladar los plazos de adicionales (arts. 193-194).
2. **Auditoría por afirmación (4.C3–4.E5).** Se inventariaron 34 ítems del modelo: 15 elementos, 2 mensajes, 13 flujos y 4 carriles. Se registraron 25 afirmaciones con fuente, cita literal verificada contra el fragmento y razonamiento.
3. **Anclaje y cotejo (4.C4–4.E6).** Se anclaron automáticamente 11 pasajes nuevos en el visor, junto a los 4 manuales del 2026-11-20. Las anclas se dibujaron sobre el PDF renderizado para comprobar que caen sobre el texto citado.

## Recuperación

| Variante | acierto@1 | acierto@3 | acierto@5 | MRR | Negativas limpias | Latencia mediana | Paquete top-5 |
|---|---|---|---|---|---|---|---|
| Léxica, todas las palabras | 0,62 | 0,69 | 0,69 | 0,65 | 2/2 | 1-2 ms | ≈123 tokens |
| Léxica flexible (raíces y sin palabras vacías) | 0,92 | 1,00 | 1,00 | 0,95 | 2/2 | 9 ms | ≈353 tokens |

Los cuatro fallos del modo estricto se debían a la flexión («sustenta» y «sustente») y a palabras vacías exigidas («sobre», «sin»). Se añadió el modo `flexible`, ahora predeterminado en la CLI. Los temas de búsqueda no cambiaron ninguna métrica. La búsqueda semántica (4.C2-4.E3) se omitió porque los fallos eran léxicos. **Advertencia:** el modo flexible se ajustó con este mismo banco. Su rendimiento debe confirmarse con preguntas nuevas de otros procesos antes de darlo por bueno.

## Resultado de la auditoría

| Resultado | Afirmaciones |
|---|---|
| `SUSTENTADA` | 6 |
| `INFERENCIA` | 13 |
| `EVIDENCIA-INSUFICIENTE` | 3 |
| `CONTRADICCION` | 3 |

Todos los elementos y mensajes tienen al menos un resultado. Las 15 anclas del visor están vigentes y ninguna cita tiene problemas de hash o de fragmento.

**Contradicciones que se mantienen o aparecen**

- **T2 y mensaje T2→SE.** El modelo solicita siempre la opinión de supervisión, pero el art. 109.1 d) la exige «de corresponder». Confirma el piloto manual.
- **T5 (nueva como formulación expresa).** El art. 109.3 dispone que la resolución se publique en la Pladicop sin adenda, y ningún elemento lo nombra. El piloto manual lo había señalado como pendiente.

**Cambios frente al piloto manual del 2026-11-20**

- **SE pasa de `EVIDENCIA-INSUFICIENTE` a `INFERENCIA`.** **ST con inspector pasa de `CONTRADICCION` parcial a `INFERENCIA`.** El art. 186.1 del Reglamento asigna la supervisión de obra «al supervisor o el inspector», de forma excluyente. Que el inspector emita la opinión del 109.1 d) es una inferencia razonable, no un texto literal: conviene confirmarla con el equipo o con una opinión del OECE.
- **T1 suma la base legal del límite del 25 %:** art. 64.1 de la Ley («puede reducir bienes, servicios, consultorías u obras hasta por el mismo porcentaje»). **T4 suma la Ley 63.1 y el Reglamento 19 c)** para la competencia de la autoridad de la gestión administrativa.
- **T4 «notificar» se precisa como inferencia.** El 109.3 y el 257.1 hacen de la publicación en la Pladicop el acto con valor legal. Ninguna fuente exige otra notificación.
- **Hallazgo nuevo en T5:** según el art. 117.3, el contratista puede pedir la disminución proporcional de garantías cuando se reduce el monto, y el 117.4 fija 10 días hábiles para adecuarlas. Es una interfaz que el modelo no muestra.

**Evidencia insuficiente:** adscripción del área usuaria (T1), unidad y controles de integración (T3) y vigencia posterior del texto consolidado al 09-01-2026 (T1).

## Propuestas para el modelo (no aplicadas)

Ninguna se aplicó a la tabla. El sustento exige comprobar antes la edición oficial vigente y el supuesto contractual.

1. Condicionar T2, el mensaje T2→SE y la ruta del supervisor a que «corresponda» la opinión.
2. Nombrar en T4 o T5 la publicación de la resolución en la Pladicop como acto de cierre favorable y reemplazar «notificar» por esa publicación, salvo evidencia de otro canal.
3. Registrar en T5 o en el sustento la interfaz de adecuación de garantías (117.3 y 117.4).
4. Documentar la variante con inspector apoyada en el 186.1, como inferencia pendiente de confirmación.

## Calidad de las herramientas y límites

- **Anclaje automático:** reproduce las 8 y 2 anclas manuales de T1 y T2 con el mismo número de renglones y diferencias de 0,6-0,7 % de la página, que corresponden al margen aplicado a mano. Cuando la capa de texto del PDF omite o reordena un renglón, devuelve `CITA-NO-HALLADA` en vez de resaltar texto equivocado. Ocurrió en el 117.4, que quedó con ancla parcial declarada.
- **Páginas OCR:** no se anclan automáticamente porque no tienen capa de texto en el original.
- **Numerales modificados:** el texto consolidado del Reglamento repite algunos numerales con su versión modificada por el D.S. 001-2026-EF, cuya entrada en vigor está condicionada. La herramienta marca esas claves y no decide cuál está vigente. El art. 109 no está entre ellas.
- **Temas de búsqueda:** en la muestra revisada su precisión fue baja. El catálogo necesita un atributo de régimen (contratación pública, obras por impuestos, administración directa) para filtrar fuentes, y esa clasificación es una decisión humana.
- **Costo:** cada consulta devuelve un paquete de unos 350 tokens en los cinco primeros resultados y cada contexto de artículo, entre 1000 y 2500 caracteres. No se midieron los tokens totales de la sesión del agente; queda pendiente para la fase 5, si se decide exponer la búsqueda por MCP.
- **Inventario y evidencia institucional:** los flujos y carriles se inventarian, pero no tienen cobertura obligatoria. Ninguna fuente institucional del GORE Huánuco (ROF, MOF, expedientes) se usó para adscribir unidades.

## Decisión solicitada (4.P)

Se solicita al usuario evaluar la calidad del piloto y decidir:

1. Si el formato de auditoría (afirmación, cita, resultado, razonamiento) y el nivel de detalle son adecuados para extenderlos a los otros diez modelos de S4.3 (fase 5).
2. Qué propuestas aplicar a la tabla de S4.3.2.7, y si antes se comprueba la vigencia del texto consolidado.
3. Si se incorpora el atributo de régimen al catálogo documental.

Sin esa respuesta no se inicia la fase 5. El silencio o las métricas no equivalen a conformidad.

## Resolución de la puerta 4.P — 2026-11-24

El usuario aprobó el formato, pidió aplicar las cuatro propuestas e incorporar el régimen al catálogo (DEC-057). Resultados:

- **Tabla S4.3.2.7.** Se agregó la compuerta G3 y se modificaron T4, T5, F1 y ST, según el [sustento](../../../02-procesos/S4-gestion-de-las-inversiones/S4-3-ejecucion-inversion/S4-3-2-ejecucion/S4-3-2-7-gestion-reducciones-prestaciones/S4-3-2-7-sustento.md). D1-D5 sin hallazgos. La auditoría rehecha no deja contradicciones abiertas: 11 `SUSTENTADA`, 12 `INFERENCIA`, 3 `EVIDENCIA-INSUFICIENTE` y 6 `NO-APLICA` por rectificación. Hay 16 anclas vigentes.
- **Régimen.** `01-referencias/00-catalogo/regimen-documental.json` clasifica los 239 documentos: 34 `CONTRATA-LEY-32069`, 5 `OBRAS-POR-IMPUESTOS`, 15 `ADMINISTRACION-DIRECTA`, 184 `TRANSVERSAL` y 1 `NO-DETERMINADO` (D.S. 206-2024-EF). El filtro reduce «valorización» de 223 a 146 coincidencias y elimina homónimos ajenos a la contratación. Las métricas del banco no cambian.
- **Defecto detectado (corregido después).** La caché de `modelar.py` no consideraba `fuentes-visor.json`: un cambio de anclas no regenera el HTML hasta usar `--sin-cache`. Se corrigió con autorización expresa del usuario: la huella de la caché incluye ahora ese archivo.

## Validación ampliada tras la revisión del usuario — 2026-11-24

El usuario señaló que auditar del modelo hacia las fuentes no basta para validar el modelo. G1 preguntaba por el art. 109 sin ninguna referencia a ese artículo, y la Ley art. 64 regula adicionales, no reducción. Se aceptaron las observaciones y se amplió el formato (DEC-057):

- **Dirección fuente → modelo.** Las 15 obligaciones de los pasajes rectores (Reglamento 109.1-109.3, 117.3-117.4 y 186.1; Ley 63.1 y 64.1) se mapearon a elementos. Todas quedan representadas.
- **Contexto de cada cita.** Cada fuente declara su ámbito y su relación. En T1, la Ley 64.1 pasa a ser una sola referencia de dos páginas: la última oración (p. 31), que trata la reducción, es la cita directa, y el 25 % de la primera oración (p. 30), que trata adicionales, es el antecedente que le da contenido. La fuente operativa sigue siendo el Reglamento 109.1. La Ley 63.3 y el 186.1 quedan como antecedentes.
- **G1** pasa a «¿Se acreditan las condiciones de la reducción?», con fuente y ancla en el 109.1. El nuevo control `REFERENCIA-SIN-ANCLA` impide que un elemento mencione un artículo sin mostrarlo.
- **Vigencia.** Se incorporaron la publicación oficial del Reglamento (El Peruano, 22-01-2025, `CON-001P`), el D.S. 001-2026-EF (`CON-001M1`, en vigor desde el 14-01-2026 tras la R.D. 0001-2026-EF/54.01) y el D.S. 222-2026-EF (`CON-001M2`, que solo modifica la Decimocuarta DCF). Los numerales usados por el piloto son idénticos en la publicación original y no fueron modificados. La afirmación de vigencia de T1 pasa a `SUSTENTADA` al 2026-11-24. Como el texto consolidado es más actual, el visor sigue mostrando ese texto; la edición original queda en la biblioteca sin mostrarse.

Resultado vigente: 33 afirmaciones (13 `SUSTENTADA`, 11 `INFERENCIA`, 2 `EVIDENCIA-INSUFICIENTE`, 7 `NO-APLICA`), sin contradicciones, 15/15 obligaciones representadas, 16 anclas vigentes y ninguna referencia sin ancla.
