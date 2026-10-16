---
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
fecha_creacion: 2026-10-15
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/obsidian
---

# Estandar obligatorio de produccion de conocimiento en Obsidian

Sube a: [Gobernanza](00-GOBERNANZA.md)

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
| PlantUML `.puml` | Modelo logico durante levantamiento | Fuente conceptual temporal; deja de ser editable al formalizar BPMN |
| BPMN `.bpmn` | Modelo formal de proceso | Fuente maestra formal; se exceptua el mapa institucional Nivel 0 |
| Canvas `.canvas` | Exploracion y representacion espacial | Vista de trabajo; no puede ser el unico lugar de una conclusion |
| Base `.base` | Consulta, filtro, agrupacion y tablero | Vista regenerable sobre archivos y propiedades |
| PDF o archivo original | Evidencia documental | Original inmutable, sujeto al catalogo y a su hash |
| SVG, PNG o PDF derivado | Revision, intercambio o publicacion | Derivado; no sustituye su fuente editable |
| `.obsidian/*.json` seleccionado | Configuracion portable de la boveda | Se versiona solo cuando beneficia a todo el equipo |

## 3. Perfil minimo de una nota

Toda nota de conocimiento nueva, excepto notas indice, instrucciones, plantillas y extracciones regenerables, DEBE comenzar con propiedades YAML.

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

Los mapas de contenido (notas indice `00-`), guias, instrucciones y plantillas cuya funcion sea inequivoca pueden omitir identificador, fechas, responsable y etiquetas. Como minimo declaran:

```yaml
---
tipo: mapa-de-contenido
area: nombre-estable
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---
```

### 3.2 Vocabularios iniciales

- `tipo`: `mapa-de-contenido`, `nota-conocimiento`, `reunion`, `diario`, `analisis`, `propuesta`, `iniciativa`, `decision`, `evidencia`, `guia`, `estado-proyecto`, `plantilla` o `instruccion`.
- `estado_documento`: `BORRADOR`, `EN-REVISION`, `VIGENTE`, `CERRADO` o `RETIRADO`.
- `clase_conocimiento`: `NORMATIVO`, `OBSERVADO`, `REFERENCIA`, `INFERENCIA`, `PROPUESTA`, `DECISION` o `NO-APLICA`.
- `confidencialidad`: `PUBLICO`, `INTERNO` o `RESTRINGIDO`.

### 3.3 Propiedades de los documentos de proceso

Los documentos de cada proceso en `02-procesos` agregan, segun corresponda (`DEC-017`):

| Propiedad | Valores | Uso |
|---|---|---|
| `codigo_proceso` | Codigo NT, por ejemplo `S4.3` | Todos los documentos y portadas del proceso |
| `nivel_proceso` | `0`, `1`, `2`... | Todos los documentos y portadas del proceso |
| `tipo_proceso` | `MISIONAL`, `ESTRATEGICO` o `APOYO` | Documentos NT |
| `proceso_padre` | Codigo NT del proceso padre o `null` | Documentos NT |
| `documento_nt` | `inventario`, `mapa`, `ficha-producto-proceso`, `ficha-indicador` o `procedimiento` | Documentos NT |
| `anexo_nt` | Numero de anexo de la NT | Documentos NT |
| `estado_institucional` | `PROPUESTA` o `APROBADO` | Documentos NT |
| `nivel_revision` | `ELABORACION`, `REVISION-EQUIPO`, `OPINION-TECNICA`, `APROBACION` o `null` si esta aprobado | Documentos NT en propuesta |
| `modifica` | Archivo aprobado que se busca variar o `null` | Archivos `-propuesta` |
| `alcance_proyecto` | `EN-ALCANCE` o `REFERENCIA` | Notas indice de proceso (`DEC-019`) |

`estado_institucional` y `nivel_revision` describen el circuito institucional del documento y no sustituyen a `estado_documento`. Solo una persona, con evidencia registrada en el sustento, puede cambiar el nivel de revision o marcar `APROBADO`.

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
- Las etiquetas se reservan para facetas de filtrado y siguen la seccion 6.1.
- Los alias se usan para siglas, nombres alternativos o denominaciones anteriores; no reemplazan el identificador estable.
- Un cambio masivo de nombre o tipo de propiedad requiere decision registrada y comprobacion de impacto en Bases, busquedas y plantillas.

### 6.1 Etiquetas obligatorias

El vocabulario controlado vive en [vocabulario-etiquetas.yaml](vocabulario-etiquetas.yaml), que es su fuente maestra (`DEC-019`). Toda nota con propiedades, salvo plantillas, lleva:

1. **Al menos una etiqueta `tema/`** del vocabulario. Si una nota no tiene ninguna, se le asigna la que corresponde a su ruta; las demas se agregan a mano cuando aportan.
2. **Una etiqueta `proceso/` jerarquica** si pertenece a un proceso: `proceso/s4`, `proceso/s4/s4-3`, `proceso/s4/s4-3/s4-3-1`. Se deriva de las carpetas de `02-procesos` o de la propiedad `codigo_proceso`; no se escribe a mano. Una busqueda por la etiqueta padre incluye a sus anidadas.

Las etiquetas van en minusculas, con numeros y guiones; no se admiten etiquetas libres ni espacios fuera del vocabulario.

El vocabulario es dinamico. Para ajustarlo:

```powershell
# Comprobar todas las notas sin modificar nada
.\.venv\Scripts\python.exe 05-herramientas/gestionar_etiquetas.py revisar

# Aplicar renombres registrados, derivar procesos y asignar temas por ruta
.\.venv\Scripts\python.exe 05-herramientas/gestionar_etiquetas.py aplicar

# Renombrar una etiqueta en el vocabulario y en todas las notas
.\.venv\Scripts\python.exe 05-herramientas/gestionar_etiquetas.py renombrar tema/viejo tema/nuevo

# Ver cuantas notas usan cada etiqueta
.\.venv\Scripts\python.exe 05-herramientas/gestionar_etiquetas.py listar
```

Agregar un tema consiste en anadirlo a `espacios.tema.valores` y, si corresponde, a `temas_por_ruta`. Los renombres quedan registrados en `renombres` para que `aplicar` corrija etiquetas antiguas. Un cambio de vocabulario que altere el significado de una faceta se registra como decision.

## 7. Mapas, enlaces entrantes, grafo y busqueda

- El mapa raiz es [Gestion por procesos del GRH](../00-GESTION-POR-PROCESOS-GRH.md).
- Cada area y subarea mantiene una nota indice `00-<nombre>.md` como mapa de contenido, segun la [arquitectura de informacion](arquitectura-de-informacion.md), seccion "Notas indice".
- Los enlaces entrantes ayudan a descubrir dependencias, pero no reemplazan el enlace desde el mapa padre.
- El grafo es una herramienta diagnostica; su posicion visual, color o proximidad NO constituye una relacion formal.
- Las busquedas reutilizables que afecten al equipo se documentan en Markdown o en una Base; no deben depender solo del historial local de busqueda.
- Los marcadores personales y la disposicion de paneles son estado local y no se versionan.

### 7.1 Lectura comun del grafo

Para que el grafo muestre el conocimiento y el modelo de procesos, el equipo usa los mismos grupos de color y vistas (`DEC-018` y `DEC-019`). El orden importa: Obsidian aplica el primer grupo que coincide.

| Grupo | Consulta | Color |
|---|---|---|
| Procesos en alcance | `[alcance_proyecto:EN-ALCANCE]` | Naranja |
| Procesos de referencia | `[alcance_proyecto:REFERENCIA]` | Gris claro |
| Actores externos | `path:03-conocimiento/actores-y-roles` | Amarillo |
| Notas indice | `[tipo:mapa-de-contenido]` | Gris |
| Documentos NT | `[documento_nt:ficha-producto-proceso] OR [documento_nt:ficha-indicador] OR [documento_nt:procedimiento] OR [documento_nt:inventario] OR [documento_nt:mapa]` | Azul |
| Sustentos | `file:sustento` | Turquesa |
| Conocimiento | `path:03-conocimiento` | Verde |
| Referencias | `path:01-referencias` | Marron |
| Gobernanza | `path:00-gobernanza` | Morado |

| Vista | Filtro | Uso |
|---|---|---|
| `navegacion` | Sin filtro | Recorrer el arbol de areas y procesos |
| `conocimiento` | `-[tipo:mapa-de-contenido] -file:00-GESTION-POR-PROCESOS-GRH -file:README -path:00-gobernanza/plantillas` | Ver solo el conocimiento y sus relaciones |
| `modelo-procesos` | `(path:02-procesos [tipo:mapa-de-contenido] -path:02-procesos/to-be) OR path:03-conocimiento/actores-y-roles` | Ver procesos y actores con su jerarquia e interacciones |
| `proceso --codigo S4.3` | `tag:#proceso/s4/s4-3` | Ver todos los documentos de un proceso y sus subprocesos |

`.obsidian/graph.json` no se versiona porque Obsidian reescribe en el el zoom y otros valores en cada uso. Cada persona aplica la configuracion comun con `python 05-herramientas/configurar_grafo_obsidian.py --vista <vista>`; el script conserva el resto de su configuracion personal. La [Base de procesos](../04-coordinacion/bases/procesos.base) ofrece la misma informacion en forma de tabla. Para trabajar en un proceso tambien sirve el grafo local de su nota indice con profundidad 2.

## 8. Plantillas

Las notas repetibles DEBEN originarse en las plantillas de `00-gobernanza/plantillas/`, indexadas en su [mapa de plantillas](plantillas/00-plantillas.md). Obsidian las ofrece desde esa carpeta.

Los documentos de cada proceso usan las plantillas `nt-002/` (ficha de producto y proceso, fichas de indicador y procedimiento) y `procesos/` (portada y sustento), conforme al [estandar de artefactos](estandar-artefactos-modelamiento.md).

Plantillas de notas en `obsidian/`:

- `nota-conocimiento.md` para conocimiento no cubierto por un esquema YAML especializado.
- `reunion.md` para sesiones de levantamiento, revision o decision.
- `diario.md` para captura diaria transitoria.
- `propuesta.md` para alternativas TO-BE o de mejora.
- `iniciativa.md` para capacidades, herramientas o cambios metodologicos que requieren construccion progresiva.
- `mapa-de-contenido.md` para nuevas areas o subareas.

Modificar una plantilla requiere revisar las notas futuras que dependen de ella. Las plantillas se editan en modo fuente para evitar que el editor transforme variables como `{{date}}` o `{{title}}`.

## 9. Reuniones

Las reuniones se registran bajo `04-coordinacion/reuniones/<anio>/` mediante la plantilla obligatoria.

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

Las notas diarias se guardan en `04-coordinacion/diario/YYYY/MM/` y usan la plantilla `diario.md`.

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

1. Los Canvas se guardan junto al proceso correspondiente o en `04-coordinacion/canvas/` si son transversales.
2. Se versiona el archivo `.canvas`, que utiliza el formato abierto JSON Canvas.
3. Una tarjeta de texto con conocimiento durable DEBE convertirse en nota Markdown y enlazarse desde el Canvas.
4. Las conexiones importantes DEBEN tener etiqueta semantica.
5. Una aprobacion, requisito normativo o decision NO PUEDE existir solo en un Canvas.
6. AS-IS, analisis y TO-BE deben quedar visualmente y conceptualmente separados.
7. Una imagen exportada del Canvas es un derivado, no la fuente editable.

## 13. Bases

Bases PUEDE utilizarse para catalogos, tableros y consultas sobre propiedades.

1. Los archivos `.base` son vistas versionables y se guardan en el area a la que sirven o en `04-coordinacion/bases/` si son transversales.
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
- Los mapas de contenido, plantillas, instrucciones y caches pueden usar un perfil reducido si su funcion es inequivoca.
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

