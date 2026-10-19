---
id: GOV-EST-ARTEFACTOS-MODELAMIENTO
tipo: instruccion
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: DECISION
proceso:
  - S4.3
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-19
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - tema/automatizacion
---

# Estandar de artefactos para el modelamiento hibrido

Este estandar adopta un flujo hibrido: durante el levantamiento, todo flujo de proceso se construye en una tabla Markdown que genera BPMN (cadena BPMN, `DEC-025`, `DEC-026`); PlantUML se reserva para vistas que no son flujos de proceso; BPMN 2.0 XML es la fuente maestra desde la formalizacion; SVG, PNG, PDF, resumenes y reportes son derivados automaticos. Cada dato se modifica en una sola fuente autorizada. El mapa institucional de procesos Nivel 0 queda exceptuado en los terminos de la seccion siguiente.

## 0. Excepcion para el mapa de procesos Nivel 0

El mapa institucional de procesos Nivel 0 clasifica y relaciona macroprocesos de manera conceptual y lineal. No representa un flujo operativo BPMN y, por tanto:

- no requiere BPMN 2.0 XML;
- no requiere pools, lanes, eventos, tareas ni compuertas;
- no requiere PlantUML, manifiesto por modelo ni cadena completa de derivados;
- puede conservarse como tabla estructurada y vista Mermaid dentro de Markdown;
- debe continuar enlazando el original institucional, registrando version, calidad, fecha de consulta y discrepancias;
- mantiene nombres estables, historial Git y revision humana.

La excepcion aplica solo al mapa global Nivel 0 que organiza macroprocesos. No se extiende a la descomposicion e interacciones de S4, a S4.3 ni a los modelos AS-IS o TO-BE.

## 1. Principios obligatorios

1. Un mismo aspecto del modelo no puede tener dos fuentes maestras editables simultaneamente.
2. Markdown conserva las fichas NT, el sustento, las reglas, las decisiones y las relaciones.
3. La tabla del diagrama (`*-diagrama-proceso-tabla.md`) conserva el modelo logico de todo flujo de proceso mientras se encuentre en etapa conceptual; PlantUML solo se usa para vistas que no son flujos de proceso (seccion 7.2).
4. BPMN 2.0 XML conserva la semantica y disposicion del modelo formal.
5. SVG, PDF, PNG, resumenes y reportes se generan; no se editan manualmente.
6. AS-IS y TO-BE mantienen archivos y rutas separadas.
7. Los identificadores de participantes, actividades, eventos, compuertas, objetos y flujos son estables.
8. La generacion debe ser local, reproducible, determinista y verificable mediante hashes.
9. Una herramienta puede validar estructura, pero no otorgar aprobacion humana ni validar conocimiento normativo.
10. Git conserva el historial; los estados no se representan mediante copias o carpetas paralelas.

## 2. Clases de representacion

### 2.1 Vista institucional transcrita

Representa un mapa o diagrama recibido como evidencia institucional. Puede usar Markdown y, cuando corresponda, PlantUML para facilitar consulta, pero debe enlazar el original, indicar su calidad y conservar discrepancias. El mapa Nivel 0 usa la excepcion de la seccion 0. Ninguna transcripcion constituye por si sola un AS-IS operativo validado.

### 2.2 Modelo logico

Representa responsabilidades, actividades, decisiones y transferencias en una forma comprensible para especialistas e IA. Su fuente editable es `*-diagrama-proceso-tabla.md`, que genera un `.bpmn` validado y sus vistas `.svg` y `.png` (seccion 7.1). Las vistas que no son flujos de proceso usan `.puml` y `.svg` (seccion 7.2).

Un modelo logico:

- puede orientar entrevistas y talleres;
- debe distinguir observado, inferido y propuesto en su nota asociada;
- no se publica como BPMN ni sustituye la validacion del proceso;
- deja de ser fuente editable cuando el modelo se formaliza en BPMN.

### 2.3 Modelo formal

Representa el proceso mediante BPMN 2.0 XML. Su fuente maestra es `.bpmn`; su SVG, PDF y resumen Markdown son derivados.

Solo un modelo formal validado puede formar parte de una linea base BPMN. Las vistas derivadas deben corresponder al hash de su maestro.

## 3. Contrato de archivos

Cada proceso tiene su carpeta dentro de `02-procesos`, anidada bajo la de su proceso padre y nombrada con su codigo NT (`DEC-017`). Todos sus archivos empiezan por el codigo del proceso. Para S4.3 el patron es:

```text
02-procesos/S4-gestion-de-las-inversiones/S4-3-ejecucion-inversion/
|-- 00-S4-3-ejecucion-inversion.md             nota indice y portada
|-- S4-3-ficha-producto-proceso.md              Anexo 2; fuente del PDF
|-- S4-3-fichas-indicador.md                    Anexo 4; fuente del PDF
|-- S4-3-sustento.md                            fuentes, evidencias, historial; no se exporta
|-- S4-3-diagrama-proceso-modelo.yaml           configuracion del diagrama
|-- S4-3-diagrama-proceso-tabla.md             etapa logica: fuente del diagrama (DEC-025)
|-- S4-3-<vista>.puml y .svg                    solo vistas que no son flujos de proceso (DEC-026)
|-- S4-3-diagrama-proceso.bpmn                  generado en la etapa logica; maestro en la formal
|-- S4-3-diagrama-proceso.svg                   vista para Obsidian
|-- S4-3-diagrama-proceso.png                   vista para documentos
|-- S4-3-diagrama-proceso.html                  vista interactiva para el navegador
|-- S4-3-diagrama-proceso-resumen-generado.md
|-- S4-3-diagrama-proceso-manifest.json
|-- S4-3-diagrama-proceso-validacion.json
|-- S4-3-diagrama-proceso-validacion.md
`-- S4-3-n-<nombre>/                            subproceso Nivel 2, mismo patron
```

En el ultimo nivel se agregan, solo si el proceso cumple algun criterio del numeral 6.1.3 d de la NT, `<codigo>-procedimiento.md` (Anexo 7) y su diagrama de flujo `<codigo>-procedimiento-diagrama.bpmn` con su `.svg` (Anexo 8).

Una variacion de un documento aprobado se plantea en un unico archivo `<codigo>-<documento>-propuesta.md`, con la propiedad `modifica`. Al aprobarse, su contenido reemplaza al documento vigente en un solo commit y el archivo `-propuesta` se elimina.

El TO-BE aplica el mismo patron en `02-procesos/to-be/`, con la misma jerarquia y el sufijo `-to-be` en cada archivo. En esta etapa esta pendiente.

## 4. Funcion y autoridad de cada archivo

| Artefacto | Funcion | Autoridad | Modificacion |
|---|---|---|---|
| `*-ficha-producto-proceso.md` | Campos del Anexo 2 en orden fijo; referencia el SVG del diagrama | Fuente maestra del documento NT y de su PDF | Personas o IA, con el circuito de revision aplicable |
| `*-fichas-indicador.md` | Campos del Anexo 4 por indicador | Fuente maestra del documento NT y de su PDF | Personas o IA, con el circuito de revision aplicable |
| `*-procedimiento.md` | Campos del Anexo 7 | Fuente maestra del documento NT y de su PDF | Personas o IA, con el circuito de revision aplicable |
| `*-sustento.md` | Fuentes, evidencias, clase de cada afirmacion, vacios, discrepancias, BIM e historial de revision | Fuente maestra de trazabilidad | Personas o IA; el historial de conformidades solo personas |
| `*-propuesta.md` | Variacion de un documento aprobado | Propuesta; no reemplaza al vigente hasta su aprobacion | Personas o IA, con el circuito de revision aplicable |
| `*-modelo.yaml` | Declaracion de rutas, clase, estado y opciones de construccion | Configuracion del modelo | Personas o comando de inicializacion controlado |
| `*-diagrama-proceso-tabla.md` | Pools, carriles, elementos, flujos, mensajes, clase y fuente de cada elemento | Fuente del diagrama en la etapa logica; antecedente en la formal | Personas o IA antes de formalizar |
| `*.puml` | Vista que no es flujo de proceso (seccion 7.2) | Fuente de la vista | Personas o IA |
| `.svg` de un `.puml` | Vista del PlantUML | Derivado | Solo generador (`renderizar_plantuml.py`) |
| `*.bpmn` | Semantica y disposicion BPMN | Derivado de la tabla en la etapa logica; fuente maestra en la formal | `tabla_a_bpmn.py` en la etapa logica; editor BPMN o aplicacion controlada en la formal |
| `*.svg` | Vista del BPMN para Obsidian y revision | Derivado versionado | Solo generador (`renderizar_bpmn.py`) |
| `*.png` | Vista del BPMN para documentos e impresion | Derivado versionado | Solo generador (`renderizar_bpmn.py`) |
| `*-diagrama-proceso.html` | Vista interactiva del BPMN (zoom y desplazamiento); enlaza la copia versionada de bpmn-js | Derivado versionado | Solo generador (`construir_modelos.py`) |
| `*-resumen-generado.md` | Carriles, actividades, eventos, flujos y objetos extraidos | Derivado consultable | Solo generador |
| `*-manifest.json` | Versiones del generador y hashes de entradas/salidas | Evidencia tecnica derivada | Solo generador |
| `*-validacion.json` | Hallazgos estructurados | Derivado tecnico | Solo validador |
| `*-validacion.md` | Informe para revision humana | Derivado consultable | Solo validador |
| `*.pdf` | Exportacion de ficha, fichas de indicador o procedimiento, y artefactos de release | Derivado de publicacion | Solo generador |

Un archivo generado debe indicar `GENERADO - NO EDITAR` mediante comentario o metadato compatible con su formato.

## 5. Transicion del modelo logico a BPMN

### 5.1 Etapa logica

- `*-diagrama-proceso-tabla.md` es editable; el `.bpmn`, el `.svg` y el `.png` se generan desde ella y no se editan.
- Los modelos logicos iniciados en PlantUML se migran a la tabla; el `.puml` se retira y queda en el historial de Git (`DEC-026`).
- Las limitaciones semanticas se documentan en el sustento del proceso.

### 5.2 Formalizacion

- El equipo contrasta el modelo logico con evidencia, reglas y entrevistas.
- Se construye el `.bpmn` con identificadores estables: desde la tabla, el generado se adopta tal cual; desde PlantUML, se construye la tabla equivalente.
- La equivalencia se revisa; no se presupone conversion automatica completa.
- Se registra cualquier decision que altere alcance, responsables o convenciones.

### 5.3 Etapa formal

- El `.bpmn` es el unico maestro del diagrama.
- La tabla y, en su caso, el `.puml` se conservan como antecedentes de la etapa conceptual; no se siguen editando.
- Toda modificacion formal parte del BPMN o de una operacion aplicada por la herramienta al BPMN.
- Se regeneran SVG, resumen, manifiesto y validaciones.

## 6. Reglas para PlantUML

Aplican a las vistas que no son flujos de proceso (seccion 7.2) y a las vistas aprobadas ya transcritas en PlantUML.


1. El renderizado se ejecuta localmente; no se envian modelos institucionales a servidores externos.
2. La version del motor y su integridad se fijan en las dependencias del proyecto.
3. Los carriles representan participantes o unidades responsables, no estados documentales.
4. Las actividades conservan identificadores mediante alias o comentarios estables cuando la sintaxis lo permita.
5. El archivo incluye titulo, alcance y advertencia de que es un modelo logico, no BPMN.
6. El SVG usa nombre estable, texto legible y se incrusta desde la nota asociada.
7. Una vista PlantUML no puede introducir actividades, responsables o decisiones sin sustento registrado.

## 6.1 Subprocesos concurrentes

Regla adoptada en `DEC-024` para modelos logicos y formales:

1. La secuencia expresa que algo termina y otra cosa empieza. Si dos subprocesos coexisten e intercambian productos, no se dibujan en secuencia.
2. Dentro de un mismo proceso, un subproceso que debe permanecer activo va en una rama paralela; lo que entrega sin terminar se representa como evento que envia, y la rama que lo necesita espera ese evento.
3. Con participantes externos o procesos con su propio control, la relacion se representa con flujos de mensaje entre pools.
4. No se usan bucles para mantener vivo un proceso. Los sucesos que llegan mientras el proceso esta activo se modelan con subprocesos de evento sin interrupcion en el diagrama de detalle.
5. Se declara la instancia de cada subproceso (por ejemplo, una por inversion o una por contrato) y se marca la instancia multiple cuando corresponda.
6. En la cadena BPMN, lo que llega mientras un proceso esta activo se dibuja con eventos condicionales o de mensaje y con subprocesos de evento sin interrupcion contraidos. En una vista PlantUML, los eventos recibidos se dibujan como actividades de color `#FFF2CC` y los envios se indican en notas.

## 7. Reglas para BPMN

1. El archivo debe ser BPMN 2.0 XML valido y portable.
2. Pools y lanes representan participantes y responsabilidades confirmados.
3. Eventos, tareas, subprocesos, compuertas, flujos de secuencia y mensajes deben usarse conforme a su semantica.
4. Los elementos mantienen IDs estables aunque cambie su etiqueta.
5. La informacion grafica BPMN DI se conserva en el mismo XML maestro.
6. Un cambio de ubicacion visual modifica el BPMN DI y regenera el SVG; nunca se corrige directamente el SVG.
7. El modelo debe poder abrirse fuera de la futura aplicacion mediante una herramienta BPMN compatible.

### 7.1 Cadena BPMN

Regla adoptada en `DEC-025`:

1. La tabla se redacta con la [plantilla de diagrama en tabla](plantillas/modelamiento/diagrama-proceso-tabla.md); cada elemento declara su clase (observado, normativo, equipo o propuesta) y su fuente.
2. `tabla_a_bpmn.py` genera el `.bpmn`; antes de versionarlo, los controles D1 (esquema OMG), D2 (referencias), D3 (bloqueos) y D4 (trazado) no deben presentar hallazgos, o estos quedan explicados en el sustento.
3. El `.svg` y el `.png` se generan solo con `renderizar_bpmn.py`, con bpmn-js fijado por version y hash. La paleta de estilo Bizagi se aplica solo a los derivados.
4. La vista interactiva `.html` se versiona junto al SVG: lleva solo el diagrama y enlaza por ruta relativa la copia de bpmn-js versionada en `05-herramientas/gestor-modelos/vendor/`, verificada contra el hash del archivo de bloqueo, de modo que funciona sin internet. La copia para Bizagi es un producto de trabajo y no se versiona. Bizagi se usa solo para ajustes manuales; un `.bpmn` ajustado alli vuelve al repositorio validado y renderizado con las mismas herramientas.
5. `construir_modelos.py` construye o comprueba (`--check`) todos los diagramas en modelamiento: adopta el BPMN solo si la validacion no tiene hallazgos, genera el SVG, el PNG y la vista interactiva, y deja en `99-temporal/modelos/` las copias para Bizagi, los informes y una pagina indice.
6. En la etapa formal, el `.bpmn` versionado deja de llevar la marca de generacion y `construir_modelos.py` lo respeta como fuente maestra.

### 7.2 Cuando usar cada formato

Regla adoptada en `DEC-026`: la cadena BPMN se usa siempre que el contenido sea un flujo de proceso.

| Situacion | Formato |
|---|---|
| Diagrama de cualquier proceso en modelamiento, de cualquier nivel, que se muestra en su ficha (Anexos 2 y 3) | Cadena BPMN: tabla, `.bpmn`, `.svg`, `.png` y vista HTML |
| Diagrama de flujo del procedimiento (Anexo 8) | Cadena BPMN |
| Subprocesos de evento y sus detalles de nivel 3 | Cadena BPMN |
| Diagramas aprobados ya transcritos en PlantUML, como S4 | Se conservan; pasan a BPMN cuando se revise el documento aprobado |
| Vistas que no son flujos: mapas de relaciones, estructuras, arboles de decision, arquitectura de informacion | PlantUML |
| Mapa institucional Nivel 0 | Markdown y Mermaid (seccion 0) |

En el repositorio se versionan la tabla, el `.bpmn`, el `.svg` (Obsidian y fichas), el `.png` (documentos) y el `.html` (vista interactiva, enlazada desde la nota indice del proceso).

## 8. Automatizacion requerida

Comandos vigentes en `05-herramientas/gestor-modelos/`: `construir_modelos.py` (construccion y comprobacion de todos los diagramas BPMN), `tabla_a_bpmn.py` (con `_validar_bpmn.py`, `_revisar_trazado.py` y `_bpmn_a_bizagi.py`), `renderizar_bpmn.py` y `renderizar_plantuml.py`. Uso en el [gestor local de modelos](../05-herramientas/gestor-modelos/00-gestor-modelos.md).

El futuro gestor debe ofrecer como minimo:

```text
procesos build <modelo>
procesos build --changed
procesos build --all
procesos check <modelo>
procesos validate <modelo>
procesos export-ai <modelo>
procesos apply <modelo> <cambios.yaml>
procesos diff <modelo>
procesos release-check <modelo>
```

### 8.1 Construccion incremental

El gestor calcula hashes, identifica dependencias y regenera solo las salidas afectadas. Un fallo no debe reemplazar derivados previamente integros.

### 8.2 Control de integridad

`check` debe detectar:

- fuentes o salidas ausentes;
- derivados desactualizados;
- edicion manual de derivados;
- versiones de motor no autorizadas;
- enlaces rotos;
- IDs duplicados o referencias inexistentes.

### 8.3 Intercambio con IA

`export-ai` genera en `99-temporal/` una representacion compacta de carriles, actividades, eventos, flujos, reglas y pendientes. La IA propone operaciones estructuradas; `apply` valida y aplica esas operaciones al maestro correspondiente y despues regenera los derivados.

La IA no debe recibir imagenes para cambios ordinarios ni editar en paralelo BPMN, SVG y Markdown generado.

## 9. Generacion determinista

- La misma entrada y version del motor deben producir los mismos bytes, salvo campos expresamente excluidos.
- Los derivados versionados no incluyen horas o fechas variables de construccion.
- El orden del XML, YAML y JSON debe normalizarse cuando el formato lo permita.
- Los cambios se escriben de forma atomica.
- El manifiesto registra hash de fuentes, hash de salidas y version de cada motor.

## 10. Validacion y publicacion

Antes de revision:

- se ejecutan `build`, `check` y `validate`;
- la ficha, el sustento y la vista deben referirse al mismo modelo;
- AS-IS, analisis y TO-BE permanecen separados;
- los hallazgos abiertos son visibles.

Antes de una release:

- BPMN XML es la fuente maestra del modelo formal;
- SVG y PDF son reproducibles;
- las conformidades de cada nivel de revision estan registradas en el historial del sustento;
- las reglas normativas utilizadas cumplen el protocolo de conocimiento confiable;
- el manifiesto de release identifica maestros y derivados.

## 11. Relaciones

- [Iniciativa de modelamiento hibrido](iniciativas/iniciativa-modelamiento-hibrido.md)
- [Metodologia de modelamiento](metodologia-modelamiento.md)
- [Protocolo de versionado y releases](protocolo-versionado-y-releases.md)
- [Protocolo de trabajo con IA](protocolo-trabajo-con-ia.md)
- [Procesos](../02-procesos/00-PROCESOS.md)
- [Plantillas de procesos](plantillas/00-plantillas.md)
