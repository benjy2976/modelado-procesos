---
tipo: especificacion-herramienta
area: herramientas
estado_documento: VIGENTE
clase_conocimiento: DECISION
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-11-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
aliases:
  - Gestor local de modelos
---

# Gestor local de modelos

La [documentación de la aplicación](docs/00-documentacion-aplicacion.md) describe su arquitectura, contratos, entorno y controles. Este índice conserva el uso del generador vigente y enlaza el [plan de la mesa de modelamiento](plan-mesa-modelamiento.md).

Las [instrucciones locales para agentes](AGENTS.md) delimitan el trabajo sobre esta aplicación.

Este directorio implementa la [iniciativa de modelamiento hibrido](../../00-gobernanza/iniciativas/iniciativa-modelamiento-hibrido.md) con dos cadenas locales, sin servicios externos al renderizar:

- **Cadena BPMN** (`DEC-025`, `DEC-026`, `DEC-051`), para todo flujo de proceso en modelamiento: tabla en Markdown, BPMN 2.0 generado y validado, visor HTML y exportaciones SVG/PNG bajo demanda.
- **PlantUML**, solo para vistas que no son flujos de proceso y para diagramas aprobados ya transcritos (estandar de artefactos, seccion 7.2).

Ninguna herramienta modifica la semantica del modelo por su cuenta ni otorga aprobacion humana.

## Dependencias

- Python 3.11 o posterior, con `lxml` (fijado en `requirements-herramientas.txt`).
- PlantUML: Windows x64, o Java 11 o posterior en otras plataformas.
- Cadena BPMN: Microsoft Edge o Google Chrome instalado. Otra ruta se indica en la variable `BPMN_NAVEGADOR`.
- Acceso a internet solo la primera vez, para descargar los artefactos fijados en `plantuml.lock.json` y `bpmn-js.lock.json`. Se comprueban por SHA-256 y se guardan en `99-temporal/herramientas/` (no se versionan).

## Cadena BPMN

```text
<codigo>-diagrama-proceso-tabla.md --tabla_a_bpmn.py--> <codigo>-diagrama-proceso.bpmn
                                                           |-- validacion D1-D3 y trazado D4
                                                           |-- visor HTML --> carga el .bpmn por HTTP local
                                                           |-- --exportar-imagenes --> .svg y .png
                                                           `-- copia para Bizagi (opcional, edicion manual)
```

| Archivo | Funcion |
|---|---|
| `construir_modelos.py` | Construye o comprueba BPMN y HTML; exporta SVG/PNG por opcion expresa y genera una pagina indice en `99-temporal/modelos/` |
| `modelar.py` | Resuelve un codigo NT a una sola tabla, conserva la numeracion, mide las etapas y omite la construccion si el cache coincide |
| `numerar_modelos.py` | Asigna el siguiente numero de referencia libre a elementos nuevos, sin renumerar los existentes |
| `tabla_a_bpmn.py` | Lee la tabla o lista, calcula el trazado, genera el `.bpmn`, lo valida, produce la copia para Bizagi y una vista HTML local |
| `_validar_bpmn.py` | D1 esquema oficial de la OMG, D2 referencias, D3 bloqueos y elementos inalcanzables (juego de tokens) |
| `_revisar_notacion.py` | D5: paleta del proyecto (estandar, seccion 7.3) y buenas practicas del manual BPMN |
| `catalogo/` | [Catalogo de simbolos](catalogo/catalogo-simbolos-diagrama-proceso-tabla.md): todos los simbolos de la paleta, prueba de regresion |
| `_revisar_trazado.py` | D4: flujos que atraviesan elementos, etiquetas o grupos ajenos, flujos superpuestos, mensajes que cruzan pools ajenos, etiquetas montadas |
| `_bpmn_a_bizagi.py` | Copia en el dialecto que importa Bizagi Modeler; agrega el proceso vacio que Bizagi exige en los pools cerrados |
| `renderizar_bpmn.py` | SVG y PNG opcionales con bpmn-js en Edge o Chrome; plantilla HTML que importa el BPMN hermano por HTTP local |
| `bpmn-js.lock.json` | Version, URL, SHA-256 y ubicacion de bpmn-js |
| `markdown-it.lock.json` | Version, origen y SHA-256 del motor Markdown local del visor documental |
| `vendor/` | Copia versionada de bpmn-js 17.11.1 y su licencia; la usan las vistas interactivas y el renderizador |
| `xsd_bpmn20/` | Esquemas oficiales BPMN 2.0 de la OMG |

### Uso

Desde la raiz del repositorio:

```powershell
# Uso rapido en reunion: solo un modelo
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\modelar.py S4.3.2.4

# Comprobacion focalizada sin escribir; --sin-cache fuerza una construccion completa
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\modelar.py S4.3.2.4 --check

# Construir todos los diagramas en modelamiento: BPMN, HTML e indice
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\construir_modelos.py

# Comprobar, sin escribir, que BPMN y HTML estan al dia
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\construir_modelos.py --check

# Exportar SVG y PNG solo cuando se preparen documentos o publicacion
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\modelar.py S4.3.2.1 --exportar-imagenes

# Construir o comprobar una tabla concreta de trabajo, incluso antes de ubicarla en 02-procesos
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\construir_modelos.py --tabla ruta\<id>-diagrama-proceso-tabla.md
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\construir_modelos.py --tabla ruta\<id>-diagrama-proceso-tabla.md --check
```

`construir_modelos.py` busca `02-procesos/**/<codigo>-diagrama-proceso-tabla.md`. `--tabla` permite indicar una o mas tablas concretas de trabajo del repositorio, sin alterar el conjunto del control global. En la etapa logica regenera `<codigo>-diagrama-proceso.bpmn` solo si la validacion no tiene hallazgos (con `--forzar`, aunque los tenga; deben explicarse en el sustento). En la etapa formal, cuando el `.bpmn` ya no lleva la marca de generacion, lo respeta como fuente maestra. La vista interactiva `<codigo>-diagrama-proceso.html` se versiona junto al BPMN y lo carga como archivo separado. Las copias para Bizagi y los informes quedan en `99-temporal/modelos/`, con `index.html`, y no se versionan. Los SVG y PNG existentes no se actualizan durante el modelamiento ordinario; se comprueban o regeneran solo al solicitar `--exportar-imagenes`.

Para S4.3 se usa `modelar.py <codigo>` durante la reunion (`DEC-044`). El comando completa la columna `Numero` de la tabla y muestra el numero como texto de referencia en HTML y, cuando se exportan, SVG y PNG. Los numeros existentes no cambian al insertar, mover o renombrar una fila. El cache comprueba la huella de la tabla y herramientas y los hashes de BPMN y HTML; cuando se pide `--exportar-imagenes`, incluye SVG y PNG. Si todo coincide, informa `OK CACHE` sin abrir el navegador. El cache se guarda en `99-temporal/modelos/cache-focalizado/` y es regenerable. `--sin-cache` fuerza el ciclo completo; `--check` comprueba el modelo sin escribir. `--forzar` solo se usa para hallazgos D1-D5 ya justificados en el sustento.

### Ciclo conceptual por lotes

Con `DEC-040`, la generacion y la revision visual se tratan como operaciones distintas:

1. La IA modifica la tabla y el sustento con el paquete de contexto autorizado.
2. Al cerrar un lote conceptual coherente se ejecuta `construir_modelos.py --tabla <ruta>` para mantener actualizados BPMN y HTML.
3. Al contexto vuelven solo el estado de la construccion y los hallazgos D1-D5 accionables. Los archivos generados no se abren ni se buscan para cambios ordinarios.
4. La misma tabla no se edita mientras esa generacion esta en curso.
5. El HTML se inspecciona cuando el contenido entra expresamente a revision visual, cuando una fuente no esta transcrita o cuando un fallo no puede resolverse con el informe textual. SVG/PNG quedan para exportacion expresa.
6. `construir_modelos.py --check` sin `--tabla` se reserva para el cierre o para cambios en las herramientas.

El comando es local y determinista: ejecutar Python y bpmn-js no consume razonamiento de IA. No se implementa un observador permanente ni edicion concurrente del mismo modelo; si esa necesidad aparece, antes se incorporaran hashes de origen y descarte de resultados obsoletos.

Pasos individuales, para un modelo:

```powershell
# 1. Generar y validar el BPMN desde la tabla
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\tabla_a_bpmn.py `
  02-procesos\...\<codigo>-diagrama-proceso-tabla.md 99-temporal\modelos\<codigo>

# 2. Exportar imagenes desde el BPMN vigente, solo cuando se necesiten
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_bpmn.py `
  02-procesos\...\<codigo>-diagrama-proceso.bpmn `
  --output 02-procesos\...\<codigo>-diagrama-proceso.svg `
  --png 02-procesos\...\<codigo>-diagrama-proceso.png

# 3. Comprobar que el SVG versionado esta al dia, sin sobrescribirlo
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_bpmn.py `
  02-procesos\...\<codigo>-diagrama-proceso.bpmn `
  --output 02-procesos\...\<codigo>-diagrama-proceso.svg --check
```

`tabla_a_bpmn.py` escribe en la carpeta indicada `<nombre>.bpmn`, `validacion.txt` y `bizagi/<nombre>_bizagi.bpmn`. Solo `--visor-autonomo` crea `<nombre>_visor.html` con XML incrustado para consulta aislada; no forma parte del ciclo normal. El `.bpmn` que se versiona en la carpeta del proceso se copia desde ahi con el nombre `<codigo>-diagrama-proceso.bpmn`, una vez que la validacion no presenta hallazgos o estos quedan explicados en el sustento. Sin carpeta de salida, los resultados van a `salida/`, que Git ignora.

### Entrada

La fuente se redacta con la [plantilla de diagrama en tabla](../../00-gobernanza/plantillas/modelamiento/diagrama-proceso-tabla.md): tablas `## Pools`, `## Elementos` y `## Mensajes`. Las columnas adicionales, como `Clase` y `Fuente`, no se dibujan y sostienen la trazabilidad. Tambien se admite el formato de lista (`## Pool: X`, `### Carril`, `- ID (tipo) Nombre -> siguientes`).

Tipos admitidos: los de la paleta del proyecto, listados con su pagina del manual en la seccion 7.3 del [estandar de artefactos](../../00-gobernanza/estandar-artefactos-modelamiento.md) (`DEC-027`). Columnas opcionales: `Marcador` en actividades; `Adjunto` e `Interrumpe` en eventos de borde (a lo sumo dos por actividad, a los costados del marcador; la rama de excepcion baja recta bajo el evento); `Disparador` en subprocesos de evento; `Anotacion` y `Grupo` en cualquier elemento. Flujo por defecto: `T-3 [No] (por defecto)` en `Siguiente`.

Los subprocesos de evento son sin interrupcion y se dibujan expandidos, con su evento de inicio y el icono del disparador (manual, fig. 2.90, p. 97), en una zona bajo el flujo principal de su carril. No llevan `Siguiente`; admiten las columnas `Disparador` (lo que los activa, que se anota como "Se activa: ..."), `Anotacion` (texto al costado) y `Grupo` (marco que reune varios). Los identificadores del BPMN se derivan del nombre del archivo y del ID de cada elemento, de modo que cambiar el titulo no los altera.

### Trazado

Columnas por orden del flujo; una fila por rama de cada compuerta dentro del carril; flujos en angulo recto que esquivan cajas, etiquetas, anotaciones y grupos ajenos; puertos de mensaje repartidos; pools externos cerrados en bandas, los que envian arriba y los que reciben abajo, junto al elemento con el que se comunican (un pool que recibe va arriba si su mensaje sale de un nodo intermedio situado sobre la zona de subprocesos de evento); etiquetas dimensionadas segun su texto. El control D4 informa cualquier superposicion restante.

La fuente tabular admite el campo opcional `perfil_trazado: equilibrado`. Este perfil conserva el tamaño de los simbolos, pero alinea en una misma etapa visual los extremos de cada flujo de mensaje entre pools, calcula la separacion horizontal segun el ancho real de cada columna y reduce moderadamente filas y separaciones entre pools. El perfil `normal` sigue siendo el valor predeterminado y conserva la geometria anterior. El perfil equilibrado debe aplicarse primero como piloto y solo se adopta para un modelo cuando D1-D5 no presentan hallazgos y la inspeccion visual confirma que las etiquetas siguen siendo legibles (`DEC-034`).

El perfil experimental `zigzag-controlado` agrega un pliegue serpentino a las secuencias extensas (`DEC-035`). Primero elimina por pool las etapas en las que el participante no actua; si aun supera 16 columnas, baja a un nuevo tramo y alterna el sentido horizontal. Las ramas conservan filas propias dentro de cada tramo, los pools pueden tener anchos diferentes y los mensajes de ida y vuelta usan corredores separados entre participantes. El cambio es exclusivamente BPMN-DI. Se aplica solo cuando la fuente lo declara y, como los demas perfiles no predeterminados, exige D1-D5 sin hallazgos e inspeccion visual humana antes de extenderse.

En convergencias con retornos desde filas inferiores del mismo carril, el perfil prueba entradas distribuidas por el borde inferior de la actividad y corredores separados; conserva la ruta previa si los obstaculos no permiten esa distribucion. La busqueda de posiciones de las etiquetas de condicion tambien prueba puntos adicionales de cada tramo para separar rotulos de ramas cercanas. Este ajuste de disposicion no cambia la secuencia BPMN y requiere comprobar D4 y el PNG del modelo afectado.

En `zigzag-controlado`, una compuerta que continua hacia otra situada bastante mas abajo y a la izquierda puede salir por su puerto izquierdo y entrar por arriba a la destinataria, siempre que el corredor este libre. Cuando la secuencia de un evento de mensaje baja junto a su propio flujo punteado y una anotacion impide el descenso directo, el trazado abre primero a la derecha, rodea la anotacion y usa un corredor vertical separado. Estas reglas afectan solo BPMN-DI; D4 y la inspeccion visual comprueban el resultado.

Si una compuerta basada en eventos abre tres o cuatro esperas del mismo carril y todas convergen en una misma verificacion o compuerta exclusiva, el perfil prueba colocarlas en una fila horizontal de columnas libres. Cuando existe compuerta de convergencia, la situa al final de esa fila. Solo cambia coordenadas; la compuerta, si se necesita para simplificar retornos, debe constar expresamente en la tabla fuente. Se conserva la distribucion vertical cuando faltan celdas libres.

La mejora del 2026-11-06, solicitada a partir de S4.3.2.5, se limita a `zigzag-controlado`: compacta a la izquierda los componentes conectados por secuencias dentro de cada pool, conserva sus distancias internas y reserva una columna entre circuitos que comparten carril. Los mensajes no imponen un reloj horizontal comun. El enrutador compara corredores entre pools, penaliza invasiones de participantes intermedios, tramos compartidos y cruces, elimina rodeos colineales y ubica las etiquetas considerando formas y rutas ya trazadas. Es una heuristica: D4 y la revision visual siguen siendo necesarios; no garantiza eliminar todo cruce de cualquier modelo.

Regresion reproducible: `.venv/Scripts/python.exe -m unittest discover -s 05-herramientas/gestor-modelos -p test_zigzag.py`. Las pruebas verifican semantica BPMN sin cambios, determinismo, limite de hallazgos D4 en los seis subprocesos de S4.3.2 y compactacion del piloto sin aumentar su altura. En la comparacion contra el generador previo, `normal`, `equilibrado` y `zigzag-amplio` producen XML identico para esos seis modelos.

`zigzag-amplio` aplica el mismo algoritmo con tramos de 28 columnas (`DEC-036`). Se reserva para modelos con muchas alternativas y convergencias, en los que el pliegue de 16 columnas produce cruces o un crecimiento vertical desproporcionado. En pools con numerosos carriles comprime, dentro de cada carril, las filas de fase que no contienen ningun elemento; conserva el orden y la separacion de todas las celdas ocupadas (`DEC-039`). No sustituye al perfil corto: la fuente elige el menor tramo que supere D1-D5 y conserve una lectura visual razonable.

El perfil optativo `zigzag-corredores` conserva la distribucion de `zigzag-controlado` y agrega busqueda de corredores por los cuatro lados, reserva de etiquetas de documentos y separacion de puertos de mensajes. Se aplica inicialmente solo en S4.3.2.2 por el bloqueo geometrico documentado en su [sustento](../../02-procesos/S4-gestion-de-las-inversiones/S4-3-ejecucion-inversion/S4-3-2-ejecucion/S4-3-2-2-atencion-consultas-obra/S4-3-2-2-sustento.md). Los perfiles anteriores no cambian. D4 y la inspeccion visual siguen siendo necesarios.

### Vistas SVG y PNG

`renderizar_bpmn.py` carga el BPMN en bpmn-js (`bpmn-navigated-viewer` 17.11.1) dentro de Edge o Chrome sin ventana, con un perfil temporal propio, y obtiene el SVG mediante la exportacion oficial de bpmn-js. El PNG es una captura de ese SVG (escala 2 por defecto). Los colores de estilo Bizagi y las etiquetas en negro se aplican a una copia en memoria: el `.bpmn` fuente no cambia. El SVG lleva la marca `GENERADO - NO EDITAR` y numera las flechas en orden fijo, de modo que la misma entrada produce los mismos bytes en el mismo equipo. La ubicacion del texto depende de las fuentes instaladas: `--check` debe ejecutarse en el entorno de referencia del proyecto.

La vista interactiva lleva solo el diagrama coloreado y enlaza `vendor/bpmn-navigated-viewer-17.11.1.production.min.js` por ruta relativa: pesa unos 30 KB, funciona sin internet desde que se clona el repositorio y se abre con doble clic o desde el enlace de la nota indice (Obsidian la abre en el navegador). `renderizar_bpmn.py` usa la copia de `vendor/` si coincide con el hash del archivo de bloqueo; si falta, descarga la de la URL fijada al cache.

La licencia de bpmn-js (`vendor/LICENSE-bpmn-js.txt`, MIT con clausula de marca de agua) exige no retirar ni alterar la marca de agua de bpmn.io en aplicaciones o sitios. El proyecto no modifica la biblioteca y la vista interactiva conserva la marca; solo oculta el boton para entrar a los subprocesos contraidos, cuyo interior esta vacio en ese nivel.

### Bizagi

La copia `bizagi/<nombre>_bizagi.bpmn` se importa en Bizagi Modeler (Archivo > Importar > BPMN). Importacion probada con Bizagi Modeler 4.2 el 2026-10-19. Bizagi recorta etiquetas largas: la herramienta avisa cuando un nombre de evento o compuerta supera 40 caracteres o un mensaje supera 50. El camino de vuelta desde Bizagi (`.bpm` a BPMN) esta pendiente de adaptar.

### Limites

- Los simbolos previstos para la segunda fase (seccion 7.3 del estandar) aun no se generan; el control D5 los rechaza.
- Un grupo reune elementos del flujo o subprocesos de evento, no ambos; la herramienta avisa si un elemento ajeno queda dentro del marco.
- Los documentos de una actividad con eventos de borde pueden superponerse a ellos; el control D4 lo informa.
- Un nombre de carril no puede contener ";".
- En la etapa formal, el `.bpmn` pasa a ser la fuente maestra y la tabla queda como antecedente (estandar de artefactos, seccion 5).

### Procedencia de los esquemas

Copias identicas, verificadas el 2026-10-19, de los esquemas publicados por la OMG en `https://www.omg.org/spec/BPMN/20100501/`:

| Archivo | SHA-256 |
|---|---|
| `BPMN20.xsd` | `A07C159CB0594573DD7C97B1370DD116112378F377E43C89A8BF512AC5030705` |
| `BPMNDI.xsd` | `F0DFF1CD559D1514D8EBFC8C646F58402BCACED27EC22E2AA6456C2DCC80B038` |
| `DC.xsd` | `A2F90E5AD9BB48C6915E4E034B4E27AC838264A1D4F27BFC70DBDFC69351312D` |
| `DI.xsd` | `8220B179C175572DF74E08A51BFFABE957867962035CEE7B5FEE0B6ACB4C4498` |
| `Semantic.xsd` | `C4318842F7D2BBC262D7954C9452C501DB16F0868EAC0B8732EC5D7FB384D9A7` |

El validador y la herramienta provienen del proyecto de la directiva SGE; el trazado, el control D4 y el conversor para Bizagi se rehicieron en este proyecto (`DEC-025`).

## PlantUML

En Windows x64 se usa la [distribucion nativa oficial de PlantUML 1.2026.8](https://github.com/plantuml/plantuml/releases/tag/v1.2026.8), sin depender del Java global. En otras plataformas se usa el JAR con Java 11 o posterior. Los binarios se almacenan en `99-temporal/herramientas/plantuml/`.

```powershell
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_plantuml.py `
  02-procesos\S4-gestion-de-las-inversiones\S4-diagrama-proceso-logico.puml `
  --output 02-procesos\S4-gestion-de-las-inversiones\S4-diagrama-proceso-logico.svg

# Comprobar sin sobrescribir
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_plantuml.py `
  02-procesos\S4-gestion-de-las-inversiones\S4-diagrama-proceso-logico.puml `
  --output 02-procesos\S4-gestion-de-las-inversiones\S4-diagrama-proceso-logico.svg --check
```

La descarga falla si el contenido remoto no coincide con el hash fijado. La salida se escribe de forma atomica y `--check` devuelve un codigo distinto de cero cuando falta o difiere el SVG.

## Visor de revisión y observaciones

Cada `*-diagrama-proceso.html` generado muestra el BPMN a la izquierda y un panel de detalle a la derecha (debajo en pantallas estrechas). El panel deriva ID, nombre, responsable, documentos, plazo, anotación, clase y fuente de la tabla maestra. Al seleccionar una caja o una flecha muestra su información; el enlace al proceso superior aparece cuando existe su HTML. La rueda acerca o aleja alrededor del puntero; el arrastre mueve el lienzo. Los enlaces a la tabla y al sustento permiten consultar la explicación completa.

El HTML carga el `.bpmn` hermano; el navegador exige servir ambos por HTTP local. Para consultar el diagrama y registrar observaciones, desde la raíz del repositorio ejecutar:

```powershell
python 05-herramientas/gestor-modelos/servidor_revision.py
```

Abrir `http://127.0.0.1:8765/`: la portada enumera los procesos con HTML disponible. La API local crea un archivo `<codigo>-observaciones.json` junto al modelo al guardar la primera observación. Cada registro conserva el ID BPMN del elemento, una referencia legible, el texto, autor o equipo, fecha y estado `ABIERTA` o `RESUELTA`. La observación del diagrama completo usa ID vacío. El botón **Exportar abiertas para IA** descarga un JSON que incluye las observaciones abiertas y los datos actuales de sus elementos. Resolver una observación solo indica seguimiento editorial; no equivale a validación normativa ni aprobación institucional.

La tabla y el sustento siguen siendo las fuentes de las afirmaciones del proceso. El JSON de observaciones no modifica el BPMN ni se borra al regenerar HTML, SVG o PNG. Si cambia un ID BPMN, la observación permanece y requiere reconciliación manual antes de aplicar correcciones. El servidor escucha únicamente en `127.0.0.1`; cerrar con `Ctrl+C`.

## Relaciones

La portada del servidor comienza en el mapa institucional Nivel 0 y presenta el arbol de carpetas de procesos. En cada visor, **Arbol de procesos** permite saltar entre diagramas; cuando un nivel no tiene BPMN, su enlace conduce a la nota indice. El enlace al padre usa su HTML si existe y, en caso contrario, su indice.

Las cajas BPMN de tipo subproceso con codigo de hijo (por ejemplo, `S4.3.2.2`) muestran **Abrir diagrama del proceso interior** en el panel. Cualquier clic en la caja, incluido el marcador `+`, solo la selecciona y muestra su detalle. La navegacion al hijo requiere activar expresamente el enlace del panel derecho; si el hijo aun no tiene HTML, el enlace abre su nota indice. Este enlace entre modelos no anade un flujo de secuencia BPMN.

El visor oculta la flecha diagonal externa que agrega bpmn-js a los subprocesos contraidos: ese control intenta abrir contenido BPMN interno y puede mostrar un lienzo vacio cuando el proceso hijo esta en otro archivo.

El panel muestra la fuente textual registrada en la tabla y avisa si falta su ubicacion precisa. Para habilitar **Abrir documento** por caja, crear junto a la tabla un archivo opcional `<codigo>-fuentes-visor.json` con rutas relativas al repositorio. Ejemplo de estructura, sin atribuir estas ubicaciones a un caso real:

```json
{"elementos":{"ID-DE-TABLA":[{"titulo":"Fuente documental","ruta":"01-referencias/ruta/documento.pdf","pagina":2,"ubicacion":"numeral 2.1","fragmento":"termino de busqueda","consulta":"2026-11-18","vigencia":"aplicabilidad pendiente"}]}}
```

`pagina` es la pagina fisica del PDF (base 1), no la numeracion impresa. `ubicacion` identifica numeral o apartado; `consulta` y `vigencia` muestran el estado de la referencia. El visor abre el PDF en esa pagina y transmite `fragmento` al buscador nativo del navegador; el termino tambien aparece encima del documento. El resaltado dentro del PDF depende del visor instalado. Las fuentes Markdown, incluida la tabla y el sustento, se renderizan localmente con `markdown-it` 15.0.3, con HTML de origen deshabilitado: se muestran encabezados, tablas, listas, citas, enlaces e indice de secciones; el frontmatter se pliega como metadatos y el primer fragmento coincidente se resalta. TXT y HTML locales se muestran como texto escapado. Los `.md` se abren en el mismo modal, sin descargarse; fuera del servidor el visor documental no esta disponible. Las rutas de anclas solo admiten archivos locales bajo `01-referencias/` o `03-conocimiento/`; para la tabla y el sustento se admiten notas Markdown bajo `02-procesos/`. Si no se registra el ancla, el visor no presume pagina ni pasaje. Los metadatos son enlaces de lectura, no sustituyen la tabla, el sustento ni la validacion de reglas.

- [Estandar de artefactos de modelamiento](../../00-gobernanza/estandar-artefactos-modelamiento.md)
- [Plantilla de diagrama en tabla](../../00-gobernanza/plantillas/modelamiento/diagrama-proceso-tabla.md)
- [Plantilla de modelo logico con carriles](../../00-gobernanza/plantillas/modelamiento/modelo-logico-carriles.puml)
- [Registro de decisiones](../../00-gobernanza/registro-decisiones.md)
- [S4 Gestion de las inversiones](../../02-procesos/S4-gestion-de-las-inversiones/S4-ficha-producto-proceso.md)

## Compactacion de carriles en zigzag-controlado

DEC-048, 2026-11-18: el perfil conserva 16 columnas por tramo y elimina las filas vacias de cada carril despues del plegado. Conserva el orden de filas ocupadas y usa el calculo existente de altura para documentos, anotaciones y margenes. No modifica actividades, conexiones, numeros ni dimensiones de las cajas. El ancho comun dentro de cada pool se mantiene. zigzag-corredores conserva su configuracion previa para evitar extender este cambio a otra variante.

La regresion compara los ocho hijos de S4.3.2 con la compactacion desactivada: semantica, determinismo y cantidad de hallazgos D4 por tipo. La compactacion no resuelve los cruces previos ni convierte el perfil en definitivo; la siguiente iteracion debera abordar el enrutamiento.

## Corredores y cadenas terminales - DEC-049

zigzag-controlado reubica cadenas terminales completas de dos o tres nodos, sin bifurcaciones ni entradas adicionales a sus nodos posteriores, en celdas libres de filas superiores del mismo carril. Se reserva una columna de separacion lateral; el calculo de altura sigue incluyendo documentos y anotaciones. La regla no depende del codigo del proceso ni de los numeros 45-46.

Las rutas que invaden cajas se recalculan sobre una malla ortogonal con busqueda A*, penalizando quiebres. Las cajas de origen y destino tambien son obstaculos: solo se permite tocar sus bordes. Los mensajes consideran los pools ajenos como barreras. Primero se intenta evitar tambien documentos y anotaciones; si no existe paso, se conserva la prohibicion de atravesar nodos, dejando los conflictos documentales al control D4. Si tampoco existe paso entre nodos se detiene la generacion con un error, sin adoptar una flecha invasiva. Los eventos de borde exceptuan su actividad anfitriona por su union BPMN. Los rotulos se recolocan despues sobre las conexiones definitivas.

No se garantiza aun ausencia de solapes entre conexiones ni entre anotaciones: permanecen como hallazgos de D4. La prueba de regresion verifica la semantica, determinismo y ausencia de aumento por tipo de hallazgo en los ocho hijos.

Cuando `zigzag-controlado` encuentra un fin BPMN que recibe tres o mas rutas del mismo pool, emite un aviso para revisar si los motivos deben terminar en fines distintos. Un fin compartido por excepciones situadas en varios tramos puede forzar corredores superpuestos aunque el enrutador evite atravesar cajas. El perfil no cambia la topologia del proceso ni crea finales por su cuenta; la separacion, cuando proceda, se hace en la tabla maestra y se fundamenta en el sustento.
