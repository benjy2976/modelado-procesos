---
tipo: propuesta
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
fecha_creacion: 2026-11-20
fecha_actualizacion: 2026-11-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Ruta hacia la revisión por áreas usuarias

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

Este documento fija el estado y las condiciones de salida del trabajo actual. La meta es que personal de las áreas usuarias pueda examinar cada modelo, entender su sustento y sus vacíos, registrar observaciones y seguir la respuesta sin perder el historial. La revisión de usuarios enriquece el modelo; no equivale a validación normativa, conformidad de los niveles de revisión ni aprobación institucional.

## Lo que ya existe y su límite

| Capacidad | Estado al 2026-11-20 | Límite que impide declararla lista para áreas usuarias |
|---|---|---|
| Núcleo Python, CLI, API, MCP y contrato OpenAPI (E1) | Implementado y probado localmente según el [plan](../plan-mesa-modelamiento.md). | No representa todavía un servicio compartido con identidad. |
| Visor Nuxt, árbol y canvas BPMN (E2) | Código y rutas de lectura implementados; se corrigieron navegación, selección y zoom. | Falta recorrido visual e interactivo completo en los procesos representativos. |
| Visores Markdown/PDF y anclajes (E3) | Infraestructura y anclajes por hash/página en piloto S4.3.2.7. | Faltan prueba visual, cobertura de fuentes por proceso y cotejo de citas; ausencia de ancla debe quedar visible. |
| Observaciones (E4) | Formularios, historial básico, API y MCP con pruebas locales. | Falta prueba de uso de extremo a extremo y ampliar la atención trazable por observación. |
| Edición en copia y agente (E5–E6) | Sesiones, diff, conflicto e integración parcial probados. | Falta una edición de tabla con regeneración válida, recuperación y prueba interactiva completa. |
| Auditoría de sustento | Piloto S4.3.2.7: 15 elementos y dos mensajes examinados, cuatro anclajes preparados; discrepancias explícitas. | Vigencia y supuesto contractual pendientes; no se han auditado los otros modelos ni se ha evaluado el piloto con el usuario. |
| OCR local | MCP conectado y probado con PDF sintético sin texto. | Falta inventario actualizado y control de fidelidad en las fuentes efectivamente usadas; no justifica OCR masivo. |

Los cambios locales aún no confirmados en Git se preservan. Esta tabla es un corte de trabajo, no una declaración de que todas las entregas están cerradas.

En este corte pasaron el `--check` global del generador (D1–D5), 15 pruebas Python, Ruff, ESLint, Nuxt typecheck, Markdownlint y la revisión de etiquetas. El validador de memoria viva reportó cero errores y cero advertencias, pero dejó tres asuntos `NOT_EVALUATED` —versión del estándar, semántica de recursos API y cobertura semántica de CLI— que requieren contraste posterior. Ninguno de estos controles sustituye la prueba visual interactiva ni la revisión de las fuentes.

## Puertas de salida, en orden

| Puerta | Trabajo pendiente y producto auditable | Evidencia de cierre |
|---|---|---|
| P1. Base documental | Recalcular inventario PDF, hash, páginas y cobertura textual; extraer Markdown paginado de fuentes pertinentes y aplicar OCR solo donde falte texto aprovechable. Registrar método, fallos y páginas de baja confianza. | Manifiesto reanudable y caché vinculada al original; una muestra cotejada con el PDF. |
| P2. Piloto de sustento | Completar el caso S4.3.2.7: revisar fuente oficial, vigencia y ámbito contractual; verificar cada afirmación y ancla; conservar contradicciones y `EVIDENCIA-INSUFICIENTE`. Presentar resultado al usuario antes de ampliar la corrida. | Matriz por elemento, citas exactas, páginas y rectángulos comprobados, hallazgos y versión del modelo. La valoración del usuario sobre el piloto queda registrada como decisión, no se presume. |
| P3. Auditoría de S4.3 | Recorrer los otros diez modelos y sus interfaces, un proceso por vez; registrar sustento o vacío, cambios de tabla/sustento en copia, diffs y controles D1–D5. S4.3.3 se identifica `SIN-MODELO` hasta tener contenido propio. | Informe de cobertura por proceso, fuentes y discrepancias; versiones recuperables. Cobertura no significa exactitud jurídica certificada. |
| P4. Visor verificable | Cerrar E2–E3 con navegación completa, selección sin salto de página, Markdown renderizado, PDF en página registrada y resaltado solo por coordenadas cotejadas y hash vigente. Mostrar claramente fuente ausente, cita sin página y ancla inválida. | Recorrido interactivo grabado o reproducible en procesos padre/hijo y un conjunto de referencias válidas e inválidas. |
| P5. Atención trazable | Completar E4–E6 y M4: cada observación conserva texto, autor declarado, versión, elemento, interpretación, fuentes, respuesta, cambio/diff o motivo de no proceder; permite reapertura. Probar edición de tabla en copia, regeneración, conflicto y recuperación mediante CLI/API/MCP. | Prueba de extremo a extremo: observación → análisis → cambio o justificación → versión resultante, con historial íntegro. El agente no atribuye revisión humana. |
| P6. Mesa de revisión guiada | Construir la consola M5 con filtros, cola por proceso, lectura de evidencia y línea de tiempo. Preparar un paquete de revisión por proceso: modelo identificado, alcance, responsables propuestos, sustento por elemento, fuentes localizables, vacíos y observaciones. | Una persona invitada puede recorrer el paquete en sesión local guiada y registrar una observación que otro agente/editor lee y atiende sin perderla. Se registran dificultades de uso. |
| P7. Apertura compartida | Cerrar E8: identidad y roles, almacenamiento transaccional para múltiples observadores, un editor activo, respaldo/restauración, auditoría de operaciones y despliegue controlado. | Prueba con dos observadores simultáneos y dos intentos de edición; comentarios íntegros, segunda edición bloqueada, recuperación demostrada y acceso limitado. |

P1–P6 permiten una **evaluación guiada en el entorno local** cuando sus evidencias existan. Para que personal de varias áreas acceda y comente por su cuenta se requiere también P7. La comparación tabla→BPMN frente a edición directa (E7) puede realizarse en copias en paralelo y no bloquea el primer ciclo de revisión: la tabla sigue siendo el método vigente mientras no haya una decisión documentada.

## Experiencia mínima del usuario revisor

El revisor entra por el árbol al proceso y ve el código, alcance, estado de elaboración y revisión identificada. Selecciona una caja o flujo para leer descripción, tipo de afirmación, fuente, artículo/numeral y página; abre el documento en el visor propio y ve solo el pasaje previamente anclado. Si la fuente o la vigencia faltan, la interfaz lo expresa. Puede registrar una observación de la caja, flujo o modelo completo y después consultar su ID, estado, interpretación, respuesta y cambio vinculado. Un mismo cambio puede atender varios comentarios, pero cada comentario conserva su historial. La pantalla no muestra `VALIDADO` ni `APROBADO` por una operación del agente.

## Decisiones que harán falta antes de P7

El equipo deberá fijar dónde se alojará el servicio, cómo se identificarán los usuarios, quién tendrá rol de editor, quién administrará respaldos y cuánto tiempo se conservarán observaciones e historial. Se pueden diseñar y probar componentes locales sin esas definiciones; no se inventa una política institucional ni se abre acceso compartido antes de resolverlas.

La secuencia detallada de auditoría y de atención individual está en la [metodología](metodologia-auditoria-y-observaciones.md). Las entregas técnicas E1–E8 y sus criterios permanecen en el [plan de la mesa](../plan-mesa-modelamiento.md). Esta ruta enlaza ambas cadenas y define el punto en que el producto será comprobable por usuarios de las áreas.
