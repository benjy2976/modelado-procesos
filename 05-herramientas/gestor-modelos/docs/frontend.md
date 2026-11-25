---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Frontend de la mesa de modelamiento

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

## Organización del frontend

`frontend/` contiene una aplicación Nuxt 4 con Vue y TypeScript. `app/app.vue` presenta la ruta Nuxt y `ModelWorkspace.vue` coordina el proceso activo, la ruta de navegación, el canvas, el inspector y el modal documental. La barra de navegación reúne en una línea el código y nombre del proceso, sin repetirlos en otro encabezado. La URL `/procesos/<código>` identifica el proceso y permite recargarlo o volver mediante el historial del navegador; `/` presenta Nivel 0. `ProcessTree.vue` presenta una jerarquía plegable que abre la rama activa al navegar o recargar. `BpmnCanvas.client.vue` importa el XML con `bpmn-js` y emite el ID del elemento seleccionado. El canvas solo selecciona: el enlace a un proceso interior se muestra en el inspector.

El árbol lateral puede ocultarse y recuperarse desde la cabecera para ampliar el espacio de lectura del diagrama. La mesa ocupa el alto de la ventana: cuando la rama abierta supera el espacio disponible, solo se desplaza la lista «Explorar», mientras su encabezado, el diagrama y el inspector conservan sus áreas. El visor aplica en memoria la paleta BPMN del HTML anterior (eventos verdes y rojos, actividades azules y compuertas amarillas), las etiquetas negras, la numeración de la tabla y el marcador del disparador en subprocesos de evento contraídos. El XML BPMN almacenado no se modifica por ese estilo de presentación.

La rueda amplía o reduce el BPMN alrededor de la posición del cursor dentro del canvas; los botones `+` y `−` mantienen el zoom centrado y «Ajustar» encuadra el diagrama completo.

`DocumentModal.client.vue` renderiza Markdown con HTML de origen deshabilitado y saneamiento adicional; los documentos de proceso se abren en el modal. `PdfReader.client.vue` usa PDF.js para dibujar la página física registrada, navegar páginas y ampliar. Proyecta los rectángulos normalizados ya guardados al enlazar la fuente; **no busca texto al abrir el PDF**. El backend retira las coordenadas si cambió el hash del documento. Si la referencia aún no tiene ancla, se abre la página sin resaltado y se indica ese límite. El resaltado ayuda a leer el pasaje, no valida el fundamento. Una referencia con `tramos` abarca varias páginas: el lector las muestra juntas, con el pasaje citado en amarillo y el antecedente necesario para entenderlo en azul. Al navegar con «Anterior» o «Siguiente» vuelve al modo de una página.

La sección «Documentación del proceso» (tabla y sustento) aparece solo en la pestaña «Detalle y sustento». `ResolutionPanel.vue` muestra en cada tarjeta la etapa, las hipótesis del análisis, las propuestas anteriores reemplazadas, el análisis del agente y sus opciones; una persona elige una o varias (según la propuesta), escribe una respuesta propia o vincula la observación a otra ya resuelta, y ve después la definición y la aplicación. El filtro de la lista incluye «Por definir» y «Definidas». `ObservationsPanel.vue` muestra el formulario de nueva observación plegado tras un botón y recuerda en el navegador el autor o equipo. El texto y las respuestas se escriben con `RichTextEditor.vue` (título, párrafo, negrita, cursiva, subrayado, tachado, viñetas, numeración, cita y quitar formato; el pegado entra como texto plano) y se envían con `formato: html`; al mostrarse se sanean de nuevo con DOMPurify y la misma lista blanca. El panel derecho se redimensiona arrastrando su borde izquierdo o con las flechas del teclado sobre el separador (Mayús para pasos largos, doble clic para restablecer); el ancho se guarda en el navegador y no aplica en pantallas angostas. `ObservationsPanel.vue` ofrece formularios para observación del diagrama o del elemento seleccionado, filtros, respuestas, cambio de estado e historial. Envía la revisión vigente en cada escritura y recarga la lista tras un conflicto `409`; no modifica el modelo. El campo autor es declarado por quien escribe y aún no está ligado a identidad autenticada.

`ModelEditPanel.vue` abre o reanuda la única sesión activa del proceso. Permite editar tabla, sustento y metadatos de fuentes en texto UTF-8, guardar solo en la copia, preparar diff y D1–D5, integrar una preparación válida o cerrar conservando la copia. El panel bloquea el cambio de documento y la preparación si hay texto sin guardar. La versión anterior permanece en `.mesa-sesiones/`; el diagrama se recarga después de integrar.

Los tipos de transporte se generan desde [OpenAPI](../contracts/openapi.json) mediante `npm run generate:api`; no son la fuente de reglas de negocio. `app/assets/main.css` define el contraste y los límites visibles de árbol, diagrama e inspector. La ruta Nitro `server/routes/api/[...path].ts` actúa como proxy local de la API Python, con destino privado configurado por `NUXT_API_TARGET`.

### Revisión de módulos frontend

La primera pantalla reúne navegación, BPMN, lectura documental y observaciones en un coordinador que comparte selección y proceso activo. No hay carpetas `app/modules/` ni coordinadores por módulo que justifiquen dividirla artificialmente. Si la edición del modelo agrega flujos propios, separar sus coordinadores y subflujos. Conservar la selección de caja en el estado de la mesa; ninguna subvista debe navegar automáticamente al hacer clic en una caja.

El frontend no escribe archivos del repositorio directamente. Las observaciones y ediciones se ejecutan mediante contratos de la API que comparten servicios con CLI y MCP. La revisión visual de la pantalla requiere un navegador accesible; compilación, tipos y rutas HTTP no sustituyen esa comprobación.
