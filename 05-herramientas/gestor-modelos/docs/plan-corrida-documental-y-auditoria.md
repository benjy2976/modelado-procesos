---
id: HER-MESA-MODELAMIENTO-PLAN-CORRIDA-DOCUMENTAL
tipo: propuesta
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
proceso: []
fecha_creacion: 2026-11-24
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/ia
  - tema/procesos
---

# Plan de corrida documental y auditoría de modelos

Este plan descompone la [metodología de auditoría](metodologia-auditoria-y-observaciones.md) en entregas ordenadas. Cada fila de **construcción** termina con una CLI probada; solo una fila posterior de **corrida** la usa sobre documentos o modelos reales. El producto final es una versión de S4.3 en la que cada afirmación comprobable de cajas y flujos tenga evidencia localizada o un vacío explícito. La automatización no atribuye validación normativa ni conformidad institucional.

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

## Alcance, comandos y punto de parada

La primera pasada diagnostica los 181 PDF actualmente presentes. La extracción nativa cubre páginas con texto aprovechable; el MCP OCR local procesa solo copias derivadas de páginas que lo necesiten. Los derivados masivos y el índice quedan en caché local. Los originales, el catálogo, las citas cotejadas, el sustento y las decisiones conservan sus funciones distintas.

Los subcomandos `fuentes` de las fases 1 y 2 ya se implementaron en la [CLI](cli.md); los restantes `fuentes` y `auditoria` siguen propuestos. `modelo`, `sesiones` y las lecturas/observaciones actuales ya existen. Los servicios Python serán comunes a CLI, API y un eventual MCP: no se duplican reglas. Cada CLI nueva acepta IDs de catálogo o códigos de proceso, emite JSON acotado y códigos de salida, evita rutas arbitrarias de escritura y conserva un manifiesto reanudable para operaciones largas.

**C** = construir herramienta y probarla con datos de prueba, sin iniciar la corrida real. **E** = ejecutar una herramienta ya terminada. **D** = control determinístico; **IA** = propuesta o análisis semántico; **H** = cotejo o decisión humana. La columna de autonomía indica si puedo completar la fila sin una nueva respuesta del usuario. Un servicio externo caído o un documento institucional restringido se registra como pendiente y no detiene trabajo independiente.

**Punto desatendido concreto:** puedo avanzar por las fases 1–3 y terminar la fase 4 con el piloto S4.3.2.7, sus citas resaltables, métricas, discrepancias e informe. Allí entrego el resultado para la evaluación del usuario ya acordada; la expansión a los otros modelos de la fase 5 espera esa evaluación. No hay pregunta indispensable antes de iniciar este tramo: la biblioteca pública local, el MCP OCR de este equipo, el método de tabla y el piloto están definidos. Se excluyen del envío a OCR los documentos sensibles o restringidos sin autorización institucional.

## Fase 1. Inventariar y decidir qué extraer

| Orden | Tipo | Trabajo y herramienta | Resultado y verificación | ¿Autónomo? |
|---|---|---|---|---|
| 1.C1 | C | Implementar `fuentes inventariar`: catálogo, registro, rutas, SHA-256, faltantes y duplicados. | CLI probada con catálogo de prueba, duplicados y archivo ausente; **D**. | Sí |
| 1.E1 | E | Ejecutar `fuentes inventariar` sobre la biblioteca. | Manifiesto de originales por ID/hash; recuentos reconciliados con catálogo; **D**. | Sí; faltantes quedan señalados |
| 1.C2 | C | Implementar `fuentes diagnosticar-texto` por página, con errores y reanudación. | CLI probada con PDF textual, escaneado y mixto; **D**. | Sí |
| 1.E2 | E | Ejecutar `fuentes diagnosticar-texto` sobre el manifiesto 1.E1. | Páginas, cobertura textual y fallos por PDF; **D** más muestra visual de utilidad del texto. | Sí |
| 1.C3 | C | Implementar `fuentes planificar-extraccion` y `fuentes priorizar`, con umbrales y cruce S4.3. | CLI probadas con casos límite y fuentes sin ID; **D**. | Sí |
| 1.E3 | E | Ejecutar planificación y prioridad con resultados 1.E2. | Cola `NATIVO`, `OCR-PARCIAL`, `OCR-INTEGRAL`, `NO-CONFIABLE` o `FALTANTE`; prioridad del piloto; **D**. La **IA** puede proponer fuentes adicionales, sin declarar vigencia. | Sí |

La fase termina cuando todo PDF presente tiene un estado y cada decisión de OCR puede explicarse con una medición. No se construye MCP nuevo para este lote.

## Fase 2. Extraer y comprobar fidelidad

| Orden | Tipo | Trabajo y herramienta | Resultado y verificación | ¿Autónomo? |
|---|---|---|---|---|
| 2.C1 | C | Implementar `fuentes extraer --metodo nativo\|ocr`: extracción paginada, copia derivada, adaptador al MCP OCR, reintentos y caché por hash. | CLI probada con PDF de prueba y trabajo interrumpido; **D**. El original no cambia. | Sí; el servicio OCR responde actualmente |
| 2.E1 | E | Ejecutar extracción nativa para la cola 1.E3. | Markdown con página PDF, herramienta, fecha y hashes; **D** para integridad y paginación. | Sí |
| 2.E2 | E | Ejecutar OCR selectivo con la misma CLI ya construida. | Markdown OCR; JSONL/PDF buscable solo si aporta; trabajos reanudables; **D** para estado y artefactos. | Sí, salvo caída del MCP o fuente restringida |
| 2.C2 | C | Implementar `fuentes evaluar-extraccion` y `fuentes preparar-cotejo`. | CLI probadas con página vacía, corte y texto alterado; **D**. | Sí |
| 2.E3 | E | Ejecutar evaluación de extracción. | Señales de baja confianza, tablas/columnas dudosas y páginas por revisar; **D** e **IA** para anomalías no codificadas. | Sí |
| 2.E4 | E | Preparar y cotejar muestra, y después toda página que llegue a citarse. | Estado de fidelidad con hash, página y registro de cotejo; **H o agente con inspección visual** frente al original. | Sí para el cotejo de trabajo; validación normativa humana posterior |
| 2.C3 | C | Implementar `fuentes extraer-office`: DOCX a Markdown con marcadores de párrafo y sección y numeración reconstruida; PPTX por diapositiva; ficha de inventario para XLSX. Implementar `fuentes indice`. | CLI probada con DOCX sintético con listas multinivel, reinicio de subniveles, numeración por estilo, tabla combinada, salto de página, nota al pie y texto eliminado; **D**. | Sí |
| 2.E5 | E | Ejecutar sobre los Office de la biblioteca y cotejar los numerales reconstruidos de una muestra contra el documento abierto. | Markdown de DOCX/PPTX, fichas XLSX e índice; cotejo **D** contra el render de un procesador de textos. | Sí |

La caché sigue los [requisitos del extractor](../../extractor-documental/00-extractor-documental.md) y no se versiona en masa. La indisponibilidad del OCR deja pendientes reanudables; no bloquea la extracción nativa.

**Estado al 24 de noviembre de 2026:** las filas 1.C1–1.E3 y 2.C1–2.E5 se ejecutaron; 2.C3 y 2.E5 amplían la fase a DOCX, PPTX y XLSX. El [informe de preparación PDF](informe-preparacion-biblioteca-pdf.md) registra la corrida de 181 PDF y 603 páginas OCR, los controles determinísticos y los límites del cotejo visual. El mismo informe registra la corrida Office: 29 DOCX y 1 PPTX con texto anclado, 27 XLSX fichados y el cotejo de numerales. La revisión normativa de cajas y flujos aún no comenzó; corresponde a las fases 3 y 4.

## Fase 3. Construir la consulta acotada

| Orden | Tipo | Trabajo y herramienta | Resultado y verificación | ¿Autónomo? |
|---|---|---|---|---|
| 3.C1 | C | Implementar `fuentes segmentar`: documento, encabezados, artículo/numeral y páginas, con estructura incierta explícita. | CLI probada con artículo entre dos páginas y varias obligaciones en una página; **D**. | Sí |
| 3.E1 | E | Segmentar los textos extraídos. | Fragmentos estables enlazados al original; **D** para cobertura y **IA/inspección visual** de una muestra de límites. | Sí |
| 3.C2 | C | Implementar `fuentes indexar`, `fuentes buscar` y `fuentes contexto`: búsqueda léxica, filtros, páginas vecinas y límite de salida. | CLI probadas con filtros, cita exacta, resultado vacío y presupuesto de caracteres; **D**. | Sí |
| 3.E2 | E | Construir índice local con `fuentes indexar`. | Índice regenerable por hash, separado de originales y sustento; **D**. | Sí |
| 3.E3 | E | Ejecutar consultas de control con `fuentes buscar/contexto`. | Paquetes de pocos pasajes con ID, página, método y estado; **D** para límites y filtros. | Sí |
| 3.C3 | C | Implementar `fuentes temas comprobar` y, si mejora la recuperación, `fuentes temas sugerir` para etiquetas candidatas. | CLI probadas con vocabulario permitido, sinónimos no equivalentes y procedencia de sugerencia; **D**. | Sí |
| 3.E4 | E | Etiquetar inicialmente solo fragmentos pertinentes a S4.3. | Etiquetas de búsqueda con procedencia; **IA** propone, **D** verifica esquema; equivalencias jurídicas quedan sin validar. | Sí |

**Estado al 24 de noviembre de 2026:** las filas 3.C1–3.E4 se ejecutaron; resultados y hallazgos en el [informe](informe-preparacion-biblioteca-pdf.md#fase-3-consulta-acotada). Para la fase 4 conviene registrar en el catálogo el régimen de cada documento (contratación pública, obras por impuestos, administración directa u otro) como filtro obligatorio: esa clasificación es una decisión humana.

La estructura y la búsqueda textual funcionan antes de aplicar IA a etiquetas. `Paralización` puede conducir a pasajes sobre `suspensión`, pero el índice no afirma que sean equivalentes. Los vectores y un MCP propio de consulta se posponen hasta medir el piloto.

## Fase 4. Medir y auditar un modelo pequeño

| Orden | Tipo | Trabajo y herramienta | Resultado y verificación | ¿Autónomo? |
|---|---|---|---|---|
| 4.C1 | C | Implementar `fuentes pruebas preparar/medir`: casos positivos y negativos, pasajes esperados, métricas y costo. | CLI probadas con resultados conocidos; **D**. | Sí |
| 4.E1 | E | Preparar banco provisional de preguntas de S4.3.2.7 y cotejar respuestas con originales. | Banco versionado con citas y casos de excepción; **IA/inspección visual**; su carácter provisional queda visible. | Sí |
| 4.E2 | E | Medir recuperación léxica/temática con `fuentes pruebas medir`. | Recuperación entre primeros resultados, precisión, latencia y tamaño del paquete; cálculo **D** sobre banco 4.E1. | Sí |
| 4.C2 | C | Si 4.E2 muestra fallos que la semántica podría resolver, implementar `fuentes indexar-semantico` con modelo local y la misma prueba. | Comparación reproducible y costo medido; **D**. No se usa servicio externo sin autorización. | Condicional; puede omitirse sin bloquear el piloto |
| 4.E3 | E | Si se construyó 4.C2, ejecutar comparación semántica y decidir por métricas si se conserva. | Mismas preguntas e igual presupuesto; **D** y análisis de errores por **IA**. | Condicional; no bloquea el piloto |
| 4.C3 | C | Implementar `auditoria inventariar-elementos` y `auditoria registrar`: lectura de tabla y registro por afirmación, fuente y revisión. | CLI probadas con ID ausente, cita inválida y evento repetido; **D**. | Sí |
| 4.E4 | E | Inventariar cajas, eventos, compuertas, flujos, carriles e interfaces del piloto. | Todos los IDs con estado inicial; cobertura **D**. | Sí |
| 4.E5 | E | Auditar afirmaciones del piloto con búsqueda acotada y registrarlas. | Matriz de actor, acción, condición, plazo, documento y excepción; **IA** propone sustento, contradicción o vacío; **D** verifica ID/hash/página. | Sí; sin marcar regla `VALIDADO` |
| 4.C4 | C | Implementar `fuentes anclar` y ampliar `auditoria informe` para leer matriz y anclajes. | CLI probadas con hash cambiado, página inexistente y rectángulo inválido; **D**. | Sí |
| 4.E6 | E | Anclar y cotejar pasajes usados sobre el PDF original. | Página y rectángulos normalizados en fuentes del visor; **D** para geometría/hash y **IA visual** para coincidencia real. | Sí |
| 4.E7 | E | Emitir informe del piloto. | Matriz completa, evidencia, vacíos, discrepancias, resaltados y costo; conciliación **D**. | Sí |
| 4.P | Puerta | Presentar el piloto al usuario antes de extender la auditoría. | El usuario evalúa calidad y ajustes. No se atribuye conformidad por silencio ni por métricas. | Requiere respuesta para entrar a fase 5 |

**Estado al 24 de noviembre de 2026:** se ejecutaron 4.C1, 4.E1, 4.E2, 4.C3, 4.E4, 4.E5, 4.C4, 4.E6 y 4.E7. Se omitieron 4.C2 y 4.E3: los fallos de recuperación eran léxicos y se resolvieron con el modo `flexible`. El usuario resolvió la puerta 4.P el mismo día (DEC-057): aprobó el formato, se aplicaron los cambios a S4.3.2.7 y se incorporó el régimen documental como filtro. La fase 5 queda habilitada; resultados en el [informe del piloto](informe-piloto-auditoria-S4-3-2-7.md).

La herramienta de auditoría se construye **antes** de aplicarse incluso al piloto. Una buena búsqueda no prueba por sí misma la interpretación normativa.

## Fase 5. Ampliar a los demás modelos

| Orden | Tipo | Trabajo y herramienta | Resultado y verificación | ¿Autónomo? |
|---|---|---|---|---|
| 5.C1 | C | Implementar `auditoria correr --alcance S4.3` y `auditoria comparar-interfaces` reutilizando servicios probados en el piloto. | CLI probadas con interrupción, reanudación y cambio de hash; **D**. | Sí, tras 4.P |
| 5.E1 | E | Recorrer un proceso por vez, con entrada y resultado por elemento. | Auditoría reanudable de otros modelos; **D** para cobertura y **IA** para interpretación. | Sí, tras 4.P |
| 5.E2 | E | Contrastar entradas, salidas y actores padre-hijos. | Candidatos a discrepancia; **D** para referencias, **IA** para materialidad. | Sí, tras 4.P |
| 5.E3 | E | Atender hallazgos en copia mediante `sesiones` y regenerar con `modelo --check`, herramientas ya existentes. | Diff de tabla/sustento, BPMN/HTML actualizados y D1–D5; **D** para integridad, **IA** para propuesta conceptual. | Sí, tras 4.P |
| 5.C2 | C | Ampliar `auditoria informe --check` para elementos sin resultado, citas huérfanas y hashes desactualizados. | CLI probada con omisión y referencia rota; **D**. | Sí, tras 4.P |
| 5.E4 | E | Comprobar toda la corrida. | Informe consolidado y vacíos explícitos; S4.3.3 queda `SIN-MODELO` mientras no exista tabla. | Sí, tras 4.P |

**Estado al 25 de noviembre de 2026:**
- 5.C1 implementada: `auditoria correr` y `auditoria comparar-interfaces`, probadas con interrupción, reanudación y cambio de tabla.
- 5.E1 completada el 2026-11-25: los 11 procesos con modelo de S4.3 quedan auditados en ambas direcciones. S4.3.2.7 está `COMPLETO` y los otros 10, `CON-HALLAZGOS`.
- 5.E2 completada: 8 candidatos deterministas e interfaces implícitas detectadas por la cobertura.
- 5.C2: el `--check` ya cubre los elementos sin resultado, las citas, los hashes y las anclas. Todos los procesos pasan esas comprobaciones de integridad.
- 5.E4: [informe consolidado de la fase 5](informe-auditoria-fase-5-S4-3.md). S4.3.3 sigue `SIN-MODELO`.
- 5.E3 en curso: el 2026-11-25 se aplicaron las propuestas de interfaces y de Pladicop, plazos y silencio (DEC-058) en seis tablas, con las auditorías reconfirmadas. Luego se corrigieron las contradicciones de S4.3.2 y S4.3.2.1 (DEC-059). Las demás propuestas esperan decisión.
- El estado vivo está en el [resumen de la corrida S4.3](../auditorias/corrida-S4-3.md).

La revisión jurídica de vigencia, ámbito y sentido corresponde a especialistas. El agente deja propuestas y evidencia rastreable, sin atribuir su criterio a una persona.

## Fase 6. Preparar el producto de revisión

| Orden | Tipo | Trabajo y herramienta | Resultado y verificación | ¿Autónomo? |
|---|---|---|---|---|
| 6.C1 | C | Implementar `auditoria cobertura` y `fuentes verificar-anclajes`. | CLI probadas con conteos discordantes, hash distinto y página inexistente; **D**. | Sí, tras 4.P |
| 6.E1 | E | Calcular cobertura y verificar todos los enlaces. | Informe por proceso y cola de anclajes defectuosos; **D**, con muestra visual de citas decisivas. | Sí, tras 4.P |
| 6.C2 | C | Ampliar visor/consola para mostrar afirmación, pasaje, discrepancia e historial usando las salidas CLI. | Pruebas de navegación, estados vacíos y resaltado sin búsqueda al abrir PDF. | Sí, tras 4.P |
| 6.E2 | E | Probar recorrido caja → afirmación → fuente/hallazgo → PDF original. | Vista navegable; **D** para enlaces y pruebas de UI, inspección visual de presentación. | Sí, tras 4.P |
| 6.C3 | C | Implementar `auditoria preparar-revision` para fijar hashes/commit, D1–D5 y pendientes sin declarar aprobación. | CLI probada con documento modificado durante la preparación; **D**. | Sí, tras 4.P |
| 6.E3 | E | Generar paquete de revisión para áreas usuarias. | Versión identificada, cobertura, vacíos, enlaces y controles técnicos; **D**. | Sí, tras 4.P |
| 6.P | Puerta | Distribuir y recibir revisión formal de personal competente. | Observaciones atribuibles y eventual validación humana según protocolo. | Requiere personas y acceso institucional |

## Política CLI, MCP y habilidades reutilizables

Toda capacidad se construye primero como servicio Python y CLI verificable. La CLI es suficiente para inventarios, OCR por lotes, indexación, métricas y reportes: exponer el mismo JSON por MCP no reduce automáticamente tokens. El MCP OCR ya disponible se usa como dependencia de `fuentes extraer --metodo ocr` y no obliga a crear otro servidor OCR.

En 4.E7 se miden llamadas, tokens, latencia y errores del trabajo real. Solo si una consulta por caja se repite mucho y puede devolver menos contexto mediante IDs, límites y caché del servidor se añade `buscar_pasajes` u `obtener_contexto` al MCP de la aplicación; la CLI continúa disponible. La escritura de auditoría por MCP se evalúa después, con el mismo criterio. Una habilidad futura documentará la secuencia de llamadas, estados y controles, pero invocará los mismos servicios en vez de guardar otra lógica o credenciales.

Las comprobaciones determinísticas cubren integridad, paginación, cobertura, hashes, anclajes, repetibilidad y D1–D5. La IA propone interpretación y busca omisiones. La persona competente valida vigencia, ámbito, interpretación y fidelidad operativa para una publicación, conforme al [protocolo de conocimiento confiable](../../../00-gobernanza/protocolo-conocimiento-confiable.md).
