---
tipo: especificacion-herramienta
area: herramientas
estado_documento: VIGENTE
clase_conocimiento: DECISION
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-11-06
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
aliases:
  - Gestor local de modelos
---

# Gestor local de modelos

Este directorio implementa la [iniciativa de modelamiento hibrido](../../00-gobernanza/iniciativas/iniciativa-modelamiento-hibrido.md) con dos cadenas locales, sin servicios externos al renderizar:

- **Cadena BPMN** (`DEC-025`, `DEC-026`), para todo flujo de proceso en modelamiento: tabla en Markdown, BPMN 2.0 generado y validado, y vistas SVG, PNG y HTML producidas con bpmn-js.
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
                                                           |-- renderizar_bpmn.py --> .svg (Obsidian) y .png
                                                           `-- copia para Bizagi (opcional, edicion manual)
```

| Archivo | Funcion |
|---|---|
| `construir_modelos.py` | Construye o comprueba todos los diagramas en modelamiento: BPMN, SVG, PNG y vista interactiva HTML, con una pagina indice en `99-temporal/modelos/` |
| `tabla_a_bpmn.py` | Lee la tabla o lista, calcula el trazado, genera el `.bpmn`, lo valida, produce la copia para Bizagi y una vista HTML local |
| `_validar_bpmn.py` | D1 esquema oficial de la OMG, D2 referencias, D3 bloqueos y elementos inalcanzables (juego de tokens) |
| `_revisar_notacion.py` | D5: paleta del proyecto (estandar, seccion 7.3) y buenas practicas del manual BPMN |
| `catalogo/` | [Catalogo de simbolos](catalogo/catalogo-simbolos-diagrama-proceso-tabla.md): todos los simbolos de la paleta, prueba de regresion |
| `_revisar_trazado.py` | D4: flujos que atraviesan elementos, etiquetas o grupos ajenos, flujos superpuestos, mensajes que cruzan pools ajenos, etiquetas montadas |
| `_bpmn_a_bizagi.py` | Copia en el dialecto que importa Bizagi Modeler; agrega el proceso vacio que Bizagi exige en los pools cerrados |
| `renderizar_bpmn.py` | SVG, PNG y vista interactiva HTML con bpmn-js en Edge o Chrome sin ventana; colores de estilo Bizagi solo en los derivados |
| `bpmn-js.lock.json` | Version, URL, SHA-256 y ubicacion de bpmn-js |
| `vendor/` | Copia versionada de bpmn-js 17.11.1 y su licencia; la usan las vistas interactivas y el renderizador |
| `xsd_bpmn20/` | Esquemas oficiales BPMN 2.0 de la OMG |

### Uso

Desde la raiz del repositorio:

```powershell
# Construir todos los diagramas en modelamiento: BPMN, SVG, PNG, vista interactiva e indice
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\construir_modelos.py

# Comprobar, sin escribir, que todos los BPMN, SVG y HTML versionados estan al dia
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\construir_modelos.py --check

# Construir o comprobar una tabla concreta de trabajo, incluso antes de ubicarla en 02-procesos
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\construir_modelos.py --tabla ruta\<id>-diagrama-proceso-tabla.md
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\construir_modelos.py --tabla ruta\<id>-diagrama-proceso-tabla.md --check
```

`construir_modelos.py` busca `02-procesos/**/<codigo>-diagrama-proceso-tabla.md`. `--tabla` permite indicar una o mas tablas concretas de trabajo del repositorio, sin alterar el conjunto del control global. En la etapa logica regenera `<codigo>-diagrama-proceso.bpmn` solo si la validacion no tiene hallazgos (con `--forzar`, aunque los tenga; deben explicarse en el sustento). En la etapa formal, cuando el `.bpmn` ya no lleva la marca de generacion, lo respeta como fuente maestra. La vista interactiva `<codigo>-diagrama-proceso.html` se escribe junto al SVG y se versiona; la nota indice del proceso la enlaza. Las copias para Bizagi y los informes quedan en `99-temporal/modelos/`, con `index.html`, y no se versionan.

### Ciclo conceptual por lotes

Con `DEC-040`, la generacion y la revision visual se tratan como operaciones distintas:

1. La IA modifica la tabla y el sustento con el paquete de contexto autorizado.
2. Al cerrar un lote conceptual coherente se ejecuta `construir_modelos.py --tabla <ruta>` para mantener actualizados BPMN, SVG, PNG y HTML.
3. Al contexto vuelven solo el estado de la construccion y los hallazgos D1-D5 accionables. Los archivos generados no se abren ni se buscan para cambios ordinarios.
4. La misma tabla no se edita mientras esa generacion esta en curso.
5. El HTML o SVG se inspecciona cuando el contenido entra expresamente a revision visual, cuando una fuente no esta transcrita o cuando un fallo no puede resolverse con el informe textual.
6. `construir_modelos.py --check` sin `--tabla` se reserva para el cierre o para cambios en las herramientas.

El comando es local y determinista: ejecutar Python y bpmn-js no consume razonamiento de IA. No se implementa un observador permanente ni edicion concurrente del mismo modelo; si esa necesidad aparece, antes se incorporaran hashes de origen y descarte de resultados obsoletos.

Pasos individuales, para un modelo:

```powershell
# 1. Generar y validar el BPMN desde la tabla
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\tabla_a_bpmn.py `
  02-procesos\...\<codigo>-diagrama-proceso-tabla.md 99-temporal\modelos\<codigo>

# 2. Generar las vistas versionadas
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_bpmn.py `
  02-procesos\...\<codigo>-diagrama-proceso.bpmn `
  --output 02-procesos\...\<codigo>-diagrama-proceso.svg `
  --png 02-procesos\...\<codigo>-diagrama-proceso.png `
  --html 02-procesos\...\<codigo>-diagrama-proceso.html --titulo "<codigo> <nombre>"

# 3. Comprobar que el SVG versionado esta al dia, sin sobrescribirlo
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_bpmn.py `
  02-procesos\...\<codigo>-diagrama-proceso.bpmn `
  --output 02-procesos\...\<codigo>-diagrama-proceso.svg --check
```

`tabla_a_bpmn.py` escribe en la carpeta indicada `<nombre>.bpmn`, `validacion.txt`, `bizagi/<nombre>_bizagi.bpmn` y `<nombre>_visor.html`. El `.bpmn` que se versiona en la carpeta del proceso se copia desde ahi con el nombre `<codigo>-diagrama-proceso.bpmn`, una vez que la validacion no presenta hallazgos o estos quedan explicados en el sustento. Sin carpeta de salida, los resultados van a `salida/`, que Git ignora.

### Entrada

La fuente se redacta con la [plantilla de diagrama en tabla](../../00-gobernanza/plantillas/modelamiento/diagrama-proceso-tabla.md): tablas `## Pools`, `## Elementos` y `## Mensajes`. Las columnas adicionales, como `Clase` y `Fuente`, no se dibujan y sostienen la trazabilidad. Tambien se admite el formato de lista (`## Pool: X`, `### Carril`, `- ID (tipo) Nombre -> siguientes`).

Tipos admitidos: los de la paleta del proyecto, listados con su pagina del manual en la seccion 7.3 del [estandar de artefactos](../../00-gobernanza/estandar-artefactos-modelamiento.md) (`DEC-027`). Columnas opcionales: `Marcador` en actividades; `Adjunto` e `Interrumpe` en eventos de borde (a lo sumo dos por actividad, a los costados del marcador; la rama de excepcion baja recta bajo el evento); `Disparador` en subprocesos de evento; `Anotacion` y `Grupo` en cualquier elemento. Flujo por defecto: `T-3 [No] (por defecto)` en `Siguiente`.

Los subprocesos de evento son sin interrupcion y se dibujan expandidos, con su evento de inicio y el icono del disparador (manual, fig. 2.90, p. 97), en una zona bajo el flujo principal de su carril. No llevan `Siguiente`; admiten las columnas `Disparador` (lo que los activa, que se anota como "Se activa: ..."), `Anotacion` (texto al costado) y `Grupo` (marco que reune varios). Los identificadores del BPMN se derivan del nombre del archivo y del ID de cada elemento, de modo que cambiar el titulo no los altera.

### Trazado

Columnas por orden del flujo; una fila por rama de cada compuerta dentro del carril; flujos en angulo recto que esquivan cajas, etiquetas, anotaciones y grupos ajenos; puertos de mensaje repartidos; pools externos cerrados en bandas, los que envian arriba y los que reciben abajo, junto al elemento con el que se comunican (un pool que recibe va arriba si su mensaje sale de un nodo intermedio situado sobre la zona de subprocesos de evento); etiquetas dimensionadas segun su texto. El control D4 informa cualquier superposicion restante.

La fuente tabular admite el campo opcional `perfil_trazado: equilibrado`. Este perfil conserva el tamaño de los simbolos, pero alinea en una misma etapa visual los extremos de cada flujo de mensaje entre pools, calcula la separacion horizontal segun el ancho real de cada columna y reduce moderadamente filas y separaciones entre pools. El perfil `normal` sigue siendo el valor predeterminado y conserva la geometria anterior. El perfil equilibrado debe aplicarse primero como piloto y solo se adopta para un modelo cuando D1-D5 no presentan hallazgos y la inspeccion visual confirma que las etiquetas siguen siendo legibles (`DEC-034`).

El perfil experimental `zigzag-controlado` agrega un pliegue serpentino a las secuencias extensas (`DEC-035`). Primero elimina por pool las etapas en las que el participante no actua; si aun supera 16 columnas, baja a un nuevo tramo y alterna el sentido horizontal. Las ramas conservan filas propias dentro de cada tramo, los pools pueden tener anchos diferentes y los mensajes de ida y vuelta usan corredores separados entre participantes. El cambio es exclusivamente BPMN-DI. Se aplica solo cuando la fuente lo declara y, como los demas perfiles no predeterminados, exige D1-D5 sin hallazgos e inspeccion visual humana antes de extenderse.

La mejora del 2026-11-06, solicitada a partir de S4.3.2.5, se limita a `zigzag-controlado`: compacta a la izquierda los componentes conectados por secuencias dentro de cada pool, conserva sus distancias internas y reserva una columna entre circuitos que comparten carril. Los mensajes no imponen un reloj horizontal comun. El enrutador compara corredores entre pools, penaliza invasiones de participantes intermedios, tramos compartidos y cruces, elimina rodeos colineales y ubica las etiquetas considerando formas y rutas ya trazadas. Es una heuristica: D4 y la revision visual siguen siendo necesarios; no garantiza eliminar todo cruce de cualquier modelo.

Regresion reproducible: `.venv/Scripts/python.exe -m unittest discover -s 05-herramientas/gestor-modelos -p test_zigzag.py`. Las pruebas verifican semantica BPMN sin cambios, determinismo, limite de hallazgos D4 en los seis subprocesos de S4.3.2 y compactacion del piloto sin aumentar su altura. En la comparacion contra el generador previo, `normal`, `equilibrado` y `zigzag-amplio` producen XML identico para esos seis modelos.

`zigzag-amplio` aplica el mismo algoritmo con tramos de 28 columnas (`DEC-036`). Se reserva para modelos con muchas alternativas y convergencias, en los que el pliegue de 16 columnas produce cruces o un crecimiento vertical desproporcionado. En pools con numerosos carriles comprime, dentro de cada carril, las filas de fase que no contienen ningun elemento; conserva el orden y la separacion de todas las celdas ocupadas (`DEC-039`). No sustituye al perfil corto: la fuente elige el menor tramo que supere D1-D5 y conserve una lectura visual razonable.

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

## Relaciones

- [Estandar de artefactos de modelamiento](../../00-gobernanza/estandar-artefactos-modelamiento.md)
- [Plantilla de diagrama en tabla](../../00-gobernanza/plantillas/modelamiento/diagrama-proceso-tabla.md)
- [Plantilla de modelo logico con carriles](../../00-gobernanza/plantillas/modelamiento/modelo-logico-carriles.puml)
- [Registro de decisiones](../../00-gobernanza/registro-decisiones.md)
- [S4 Gestion de las inversiones](../../02-procesos/S4-gestion-de-las-inversiones/S4-ficha-producto-proceso.md)
