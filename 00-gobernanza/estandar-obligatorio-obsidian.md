---
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
fecha_creacion: 2026-10-15
fecha_actualizacion: 2026-10-15
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/obsidian
---

# Estandar obligatorio de produccion de conocimiento en Obsidian

[Inicio](../00-inicio.md) · [Gobernanza](README.md)

## 1. Condicion obligatoria

Obsidian es el entorno principal de autoria, navegacion y consulta del conocimiento del proyecto. Todo integrante o agente que cree o modifique notas debe cumplir este estandar.

Git sigue siendo el sistema de versionado y publicacion. Los archivos del repositorio siguen siendo las fuentes maestras; Obsidian no introduce una base de datos paralela ni reemplaza los controles definidos en el [Manual operativo del conocimiento](manual-operativo-del-conocimiento.md).

En este documento:

- **DEBE** y **NO DEBE** expresan requisitos obligatorios.
- **PUEDE** expresa una funcion permitida cuando aporta valor y cumple los controles aplicables.
- Una funcion visual o automatica de Obsidian no otorga validez, vigencia ni aprobacion al contenido.

## 2. Fuentes maestras y vistas

| Artefacto | Funcion | Condicion |
|---|---|---|
| Markdown `.md` | Narrativa, actas, analisis, mapas de contenido y documentacion | Fuente maestra textual cuando corresponda |
| YAML `.yaml` | Reglas, eventos y paquetes de contexto estructurados | Fuente maestra del dato definido por su esquema |
| BPMN `.bpmn` | Modelo de proceso | Fuente maestra del diagrama |
| Canvas `.canvas` | Exploracion y representacion espacial | Vista de trabajo; no puede ser el unico lugar de una conclusion |
| Base `.base` | Consulta, filtro, agrupacion y tablero | Vista regenerable sobre archivos y propiedades |
| PDF o archivo original | Evidencia documental | Original inmutable, sujeto al catalogo y a su hash |
| SVG, PNG o PDF derivado | Revision, intercambio o publicacion | Derivado; no sustituye su fuente editable |
| `.obsidian/*.json` seleccionado | Configuracion portable de la boveda | Se versiona solo cuando beneficia a todo el equipo |

## 3. Perfil minimo de una nota

Toda nota de conocimiento nueva, excepto README, instrucciones, plantillas y extracciones regenerables, DEBE comenzar con propiedades YAML.

```yaml
---
id: pendiente
tipo: nota-conocimiento
area: pendiente
estado_documento: BORRADOR
clase_conocimiento: pendiente
proceso: []
fecha_creacion: YYYY-MM-DD
fecha_actualizacion: YYYY-MM-DD
responsable: pendiente
confidencialidad: INTERNO
tags: []
---
```

### 3.1 Perfil reducido

Los mapas de contenido, README, guias, instrucciones y plantillas cuya funcion sea inequivoca pueden omitir identificador, fechas, responsable y etiquetas. Como minimo declaran:

```yaml
---
tipo: mapa-de-contenido
area: nombre-estable
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---
```

### 3.2 Vocabularios iniciales

- `tipo`: `mapa-de-contenido`, `nota-conocimiento`, `reunion`, `diario`, `analisis`, `propuesta`, `decision`, `evidencia`, `guia`, `estado-proyecto`, `plantilla` o `instruccion`.
- `estado_documento`: `BORRADOR`, `EN-REVISION`, `VIGENTE`, `CERRADO` o `RETIRADO`.
- `clase_conocimiento`: `NORMATIVO`, `OBSERVADO`, `REFERENCIA`, `INFERENCIA`, `PROPUESTA`, `DECISION` o `NO-APLICA`.
- `confidencialidad`: `PUBLICO`, `INTERNO` o `RESTRINGIDO`.

`estado_documento` describe la madurez editorial de la nota y NO DEBE confundirse con `validacion.estado` de una regla normativa. Una nota `VIGENTE` no convierte una regla en `VALIDADO`.

Las fechas usan ISO `YYYY-MM-DD`. `responsable` registra rol o identificador institucional autorizado, nunca datos personales innecesarios. Si la confidencialidad es `RESTRINGIDO`, el repositorio solo conserva una referencia segura y no el contenido sensible.

## 4. Estructura de redaccion

Una nota DEBE:

1. Tener un unico titulo de nivel 1 (`#`).
2. Explicar en el primer parrafo su proposito o conclusion principal.
3. Usar encabezados jerarquicos sin saltar niveles.
4. Separar hechos, normas, referencias, inferencias y propuestas.
5. Identificar las fuentes en la seccion donde se utilizan.
6. Terminar con relaciones, pendientes o decisiones cuando correspondan.
7. Usar lenguaje directo y una afirmacion principal por parrafo.

No se copia contenido entre notas para simular relaciones. Se enlaza la fuente maestra o, si se necesita contexto visible, se incrusta una seccion controlada.

## 5. Enlaces, bloques e incrustaciones

1. El formato predeterminado es el enlace Markdown relativo: `[Titulo](ruta/archivo.md)`.
2. Toda nota DEBE estar enlazada desde el mapa de contenido de su area.
3. Los enlaces cruzados DEBEN indicar la relacion: se rige por, se sustenta en, produce, implementa, valida o relacionado.
4. Los enlaces a encabezados DEBEN apuntar a secciones estables.
5. Los enlaces a bloques y la sintaxis `![[...]]` PUEDEN usarse cuando una referencia precisa o incrustacion aporta valor y no existe equivalente portable razonable.
6. Una incrustacion es una vista del contenido original; NO DEBE editarse como si fuera una copia independiente.
7. Antes de publicar no debe haber enlaces no resueltos, salvo pendientes expresamente documentados.

La jerarquia y las relaciones se detallan en [Arquitectura de informacion y enlaces](arquitectura-de-informacion.md).

## 6. Propiedades, etiquetas y alias

- Las propiedades guardan datos atomicos para busqueda y Bases; no contienen parrafos ni justificaciones.
- Los nombres de propiedades son estables, en minusculas y con guion bajo.
- Los estados, aprobaciones y clasificaciones obligatorias se registran en propiedades o esquemas, no solo mediante etiquetas.
- Las etiquetas se reservan para facetas tematicas transversales. Formato recomendado: `tema/bim`, `tema/contrataciones`, `tema/invierte-pe`.
- Los alias se usan para siglas, nombres alternativos o denominaciones anteriores; no reemplazan el identificador estable.
- Un cambio masivo de nombre o tipo de propiedad requiere decision registrada y comprobacion de impacto en Bases, busquedas y plantillas.

## 7. Mapas, enlaces entrantes, grafo y busqueda

- El mapa raiz es [Inicio de la boveda](../00-inicio.md).
- Cada area mantiene un `README.md` como mapa de contenido.
- Los enlaces entrantes ayudan a descubrir dependencias, pero no reemplazan el enlace desde el mapa padre.
- El grafo es una herramienta diagnostica; su posicion visual, color o proximidad NO constituye una relacion formal.
- Las busquedas reutilizables que afecten al equipo se documentan en Markdown o en una Base; no deben depender solo del historial local de busqueda.
- Los marcadores personales y la disposicion de paneles son estado local y no se versionan.

## 8. Plantillas

Las notas repetibles DEBEN originarse en las plantillas de `04-recursos-reutilizables/plantillas/obsidian/`.

Plantillas iniciales:

- `nota-conocimiento.md` para conocimiento no cubierto por un esquema YAML especializado.
- `reunion.md` para sesiones de levantamiento, revision o decision.
- `diario.md` para captura diaria transitoria.
- `propuesta.md` para alternativas TO-BE o de mejora.
- `mapa-de-contenido.md` para nuevas areas o subareas.

Modificar una plantilla requiere revisar las notas futuras que dependen de ella. Las plantillas se editan en modo fuente para evitar que el editor transforme variables como `{{date}}` o `{{title}}`.

## 9. Reuniones

Las reuniones se registran bajo `06-coordinacion/reuniones/<anio>/` mediante la plantilla obligatoria.

El acta DEBE contener:

- objetivo, fecha, modalidad y alcance;
- participantes por rol o identificador institucional autorizado;
- evidencia revisada;
- hechos observados y puntos por confirmar;
- decisiones, desacuerdos y preguntas abiertas;
- tareas con responsable, plazo y enlace al artefacto afectado;
- relacion con procesos, reglas, propuestas o modelos.

Una afirmacion recogida en una reunion comienza como `OBSERVADO` pendiente de confirmacion, salvo que se adjunte evidencia suficiente. Una decision que cambie alcance, codigos, convenciones o metodo DEBE promoverse al [Registro de decisiones](registro-decisiones.md). El acta no sustituye esa formalizacion.

No se almacenan grabaciones, transcripciones con datos personales ni expedientes sensibles sin autorizacion y almacenamiento institucional apropiado.

## 10. Notas diarias y captura rapida

Las notas diarias se guardan en `06-coordinacion/diario/YYYY/MM/` y usan la plantilla `diario.md`.

- Sirven para captura temporal, bitacora y tareas personales del proyecto.
- No constituyen evidencia validada ni reemplazan actas, decisiones, reglas o productos.
- Todo conocimiento durable DEBE promoverse a su area antes de cerrar la semana o la actividad relacionada.
- Las notas diarias no se crean en la raiz de la boveda.

## 11. Tareas

Las tareas usan la sintaxis Markdown `- [ ]` y deben estar dentro de la nota que proporciona su contexto.

Formato recomendado:

```markdown
- [ ] Descripcion verificable — responsable: ROL — vence: YYYY-MM-DD
```

Una tarea cerrada conserva `- [x]` como evidencia de seguimiento. Las tareas no reemplazan el sistema institucional que se defina para compromisos oficiales. Una tarea que modifica un producto DEBE enlazarlo.

## 12. Canvas

Canvas PUEDE usarse para:

- explorar descomposiciones de procesos;
- preparar talleres y ordenar evidencia;
- visualizar relaciones entre fuentes, reglas, actividades y propuestas;
- comparar AS-IS y TO-BE manteniendolos en grupos separados;
- representar el flujo de produccion de conocimiento.

Reglas obligatorias:

1. Los Canvas se guardan junto al proceso correspondiente o en `06-coordinacion/canvas/` si son transversales.
2. Se versiona el archivo `.canvas`, que utiliza el formato abierto JSON Canvas.
3. Una tarjeta de texto con conocimiento durable DEBE convertirse en nota Markdown y enlazarse desde el Canvas.
4. Las conexiones importantes DEBEN tener etiqueta semantica.
5. Una aprobacion, requisito normativo o decision NO PUEDE existir solo en un Canvas.
6. AS-IS, analisis y TO-BE deben quedar visualmente y conceptualmente separados.
7. Una imagen exportada del Canvas es un derivado, no la fuente editable.

## 13. Bases

Bases PUEDE utilizarse para catalogos, tableros y consultas sobre propiedades.

1. Los archivos `.base` son vistas versionables y se guardan en el area a la que sirven o en `06-coordinacion/bases/` si son transversales.
2. Una Base NO DEBE ser la unica ubicacion de un dato; consulta propiedades de archivos fuente.
3. Los filtros y formulas deben usar propiedades del vocabulario aprobado.
4. Toda Base compartida debe explicar su objetivo, alcance y criterio de inclusion en el mapa de contenido que la enlaza.
5. Una formula es un dato derivado y no reemplaza la evidencia ni la validacion humana.
6. Cambiar una propiedad usada por una Base exige actualizar y probar sus consultas.

## 14. Callouts, tablas, comentarios y codigo

- Los callouts se usan con proposito consistente: `[!info]` para contexto, `[!question]` para preguntas, `[!warning]` para riesgos, `[!todo]` para acciones y `[!example]` para ejemplos.
- Un callout no cambia el estado de validacion de su contenido.
- Las tablas se usan para comparaciones estables y pequenas; los conjuntos de datos mantenibles se guardan en CSV, YAML o Base segun corresponda.
- Los comentarios `%% ... %%` solo contienen notas editoriales no esenciales; la evidencia y decisiones permanecen visibles y versionadas.
- Los bloques de codigo declaran lenguaje cuando sea posible.

## 15. Adjuntos y archivos incrustados

- Los adjuntos se almacenan en el area que corresponda y siguen las reglas de Git, LFS y reproducibilidad.
- Los originales en `01-referencias/**/originales` no se modifican.
- Los PDF publicos regenerables no se agregan al repositorio; se enlazan mediante catalogo e identificador.
- Las imagenes de una nota deben tener nombre estable, texto alternativo y procedencia.
- No se incrustan recursos remotos que requieran credenciales o expongan informacion institucional.

## 16. Plugins, temas y servicios

El perfil base utiliza plugins oficiales incluidos en Obsidian: enlaces entrantes y salientes, busqueda, propiedades, plantillas, notas diarias, Canvas, Bases, esquema y recuperacion de archivos.

- Los plugins de comunidad permanecen en modo restringido hasta evaluacion y aprobacion.
- Una propuesta de plugin debe registrar finalidad, version, licencia, permisos, datos tratados, trafico externo, mantenimiento, portabilidad y alternativa sin plugin.
- Un plugin no puede introducir una fuente maestra oculta ni escribir fuera de las rutas autorizadas.
- Obsidian Sync y Publish no se habilitan por defecto: Git y las releases gobiernan este proyecto. Cualquier servicio adicional requiere decision y analisis de seguridad.
- Los temas, hotkeys, paneles, grafo y espacios de trabajo personales no deben alterar el significado de la documentacion.
- La recuperacion local de archivos complementa, pero no sustituye, Git.

## 17. Uso de IA y CLI

- La IA DEBE respetar este estandar, `AGENTS.md` y el paquete de contexto de la tarea.
- La IA no valida propiedades de aprobacion ni conocimiento normativo.
- Las operaciones automatizadas deben usar rutas exactas desde la raiz de la boveda.
- El CLI puede crear, leer, buscar, consultar Bases, administrar tareas y revisar enlaces; las acciones destructivas requieren comprobacion previa.
- No se usa control visual de Obsidian para las tareas de este proyecto salvo solicitud expresa del usuario.

Comandos de control:

```powershell
obsidian vault info=path
obsidian properties counts
obsidian tags counts
obsidian unresolved total
obsidian orphans
obsidian deadends
obsidian tasks todo verbose
obsidian bases
```

## 18. Revision, Git y publicacion

Antes de un commit de conocimiento:

- verificar propiedades y estructura;
- comprobar enlaces y fuentes;
- revisar que no existan datos sensibles;
- confirmar separacion AS-IS, analisis y TO-BE;
- inspeccionar el `git diff` y excluir estado visual local.

Antes de una release:

- ejecutar las validaciones del [Manual operativo del conocimiento](manual-operativo-del-conocimiento.md);
- resolver enlaces no intencionales y Markdown huerfano;
- comprobar que Canvas y Bases no contienen conocimiento exclusivo;
- identificar commit, reglas, decisiones y aprobaciones utilizadas.

## 19. Cumplimiento y transicion

- Toda nota nueva creada despues de `DEC-011` debe cumplir este estandar desde su creacion.
- Toda nota existente debe adoptar el perfil aplicable cuando se modifique materialmente y, en cualquier caso, antes de formar parte de una linea base.
- Los mapas de contenido, README, plantillas, instrucciones y caches pueden usar un perfil reducido si su funcion es inequivoca.
- Una desviacion requiere justificacion, responsable, alcance y plazo de regularizacion.
- El futuro auditor de la boveda verificara propiedades, enlaces, ubicacion, plantillas y archivos de configuracion permitidos.

## 20. Fuentes oficiales de la herramienta

Consultadas el 2026-10-15:

- [Propiedades](https://obsidian.md/help/properties)
- [Enlazar notas](https://obsidian.md/help/link-notes)
- [Sintaxis Markdown](https://obsidian.md/help/syntax)
- [Plantillas](https://obsidian.md/help/plugins/templates)
- [Notas diarias](https://obsidian.md/help/plugins/daily-notes)
- [Canvas](https://obsidian.md/help/plugins/canvas)
- [Sintaxis de Bases](https://obsidian.md/help/bases/syntax)
- [CLI](https://obsidian.md/help/cli)

