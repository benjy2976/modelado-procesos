---
id: GOV-EST-ARTEFACTOS-MODELAMIENTO
tipo: instruccion
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: DECISION
proceso:
  - S4.3
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - tema/automatizacion
---

# Estandar de artefactos para el modelamiento hibrido

Este estandar adopta un flujo hibrido: PlantUML permite construir y revisar modelos logicos durante el levantamiento; BPMN 2.0 XML es la fuente maestra desde la formalizacion; SVG, PDF, resumenes y reportes son derivados automaticos. Cada dato se modifica en una sola fuente autorizada. El mapa institucional de procesos Nivel 0 queda exceptuado en los terminos de la seccion siguiente.

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
2. Markdown conserva narrativa, evidencia, reglas, decisiones y relaciones.
3. PlantUML conserva el modelo logico mientras el artefacto se encuentre en etapa conceptual.
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

Representa responsabilidades, actividades, decisiones y transferencias en una forma comprensible para especialistas e IA. Su fuente editable es `.puml` y su vista es `.svg`.

Un modelo logico:

- puede orientar entrevistas y talleres;
- debe distinguir observado, inferido y propuesto en su nota asociada;
- no se publica como BPMN ni sustituye la validacion del proceso;
- deja de ser fuente editable cuando el modelo se formaliza en BPMN.

### 2.3 Modelo formal

Representa el proceso mediante BPMN 2.0 XML. Su fuente maestra es `.bpmn`; su SVG, PDF y resumen Markdown son derivados.

Solo un modelo formal validado puede formar parte de una linea base BPMN. Las vistas derivadas deben corresponder al hash de su maestro.

## 3. Contrato de archivos

Para el AS-IS de S4.3 se adopta como patron:

```text
03-modelamiento/procesos/s4-3-ejecucion-inversion/
|-- 01-levantamiento/
|   `-- s4-3-ejecucion-inversion-as-is-narrativa.md
|-- 02-modelos/as-is/
|   |-- s4-3-ejecucion-inversion-as-is-modelo.yaml
|   |-- s4-3-ejecucion-inversion-as-is-logico.puml
|   |-- s4-3-ejecucion-inversion-as-is-logico.svg
|   |-- s4-3-ejecucion-inversion-as-is.bpmn
|   |-- s4-3-ejecucion-inversion-as-is.svg
|   |-- s4-3-ejecucion-inversion-as-is-resumen-generado.md
|   `-- s4-3-ejecucion-inversion-as-is-manifest.json
`-- 05-validacion/
    |-- s4-3-ejecucion-inversion-as-is-validacion.json
    `-- s4-3-ejecucion-inversion-as-is-validacion.md
```

El TO-BE aplica el mismo patron en `02-modelos/to-be` y sustituye `as-is` por `to-be`.

## 4. Funcion y autoridad de cada archivo

| Artefacto | Funcion | Autoridad | Modificacion |
|---|---|---|---|
| `*-narrativa.md` | Alcance, evidencia, reglas, entradas, salidas y explicacion | Fuente maestra textual | Personas o IA, con revision aplicable |
| `*-modelo.yaml` | Declaracion de rutas, clase, estado y opciones de construccion | Configuracion del modelo | Personas o comando de inicializacion controlado |
| `*-logico.puml` | Flujo logico con carriles | Fuente conceptual temporal | Personas o IA antes de formalizar |
| `*-logico.svg` | Vista del PlantUML | Derivado | Solo generador |
| `*.bpmn` | Semantica y disposicion BPMN | Fuente maestra formal | Editor BPMN o aplicacion controlada |
| `*.svg` | Vista del BPMN para Obsidian y revision | Derivado versionado | Solo generador |
| `*-resumen-generado.md` | Carriles, actividades, eventos, flujos y objetos extraidos | Derivado consultable | Solo generador |
| `*-manifest.json` | Versiones del generador y hashes de entradas/salidas | Evidencia tecnica derivada | Solo generador |
| `*-validacion.json` | Hallazgos estructurados | Derivado tecnico | Solo validador |
| `*-validacion.md` | Informe para revision humana | Derivado consultable | Solo validador |
| `*.pdf` | Emision o artefacto de release | Derivado de publicacion | Solo generador de release |

Un archivo generado debe indicar `GENERADO - NO EDITAR` mediante comentario o metadato compatible con su formato.

## 5. Transicion de PlantUML a BPMN

### 5.1 Etapa logica

- `*-logico.puml` es editable.
- `*-logico.svg` se genera desde PlantUML.
- No es obligatorio que exista un `.bpmn`.
- Las limitaciones semanticas se documentan en la narrativa.

### 5.2 Formalizacion

- El equipo contrasta el modelo logico con evidencia, reglas y entrevistas.
- Se construye el `.bpmn` con identificadores estables.
- La equivalencia se revisa; no se presupone conversion automatica completa.
- Se registra cualquier decision que altere alcance, responsables o convenciones.

### 5.3 Etapa formal

- El `.bpmn` es el unico maestro del diagrama.
- El `.puml` se conserva como antecedente de la etapa conceptual o se regenera como resumen; no se sigue editando manualmente.
- Toda modificacion formal parte del BPMN o de una operacion aplicada por la herramienta al BPMN.
- Se regeneran SVG, resumen, manifiesto y validaciones.

## 6. Reglas para PlantUML

1. El renderizado se ejecuta localmente; no se envian modelos institucionales a servidores externos.
2. La version del motor y su integridad se fijan en las dependencias del proyecto.
3. Los carriles representan participantes o unidades responsables, no estados documentales.
4. Las actividades conservan identificadores mediante alias o comentarios estables cuando la sintaxis lo permita.
5. El archivo incluye titulo, alcance y advertencia de que es un modelo logico, no BPMN.
6. El SVG usa nombre estable, texto legible y se incrusta desde la nota asociada.
7. Una vista PlantUML no puede introducir actividades, responsables o decisiones sin sustento registrado.

## 7. Reglas para BPMN

1. El archivo debe ser BPMN 2.0 XML valido y portable.
2. Pools y lanes representan participantes y responsabilidades confirmados.
3. Eventos, tareas, subprocesos, compuertas, flujos de secuencia y mensajes deben usarse conforme a su semantica.
4. Los elementos mantienen IDs estables aunque cambie su etiqueta.
5. La informacion grafica BPMN DI se conserva en el mismo XML maestro.
6. Un cambio de ubicacion visual modifica el BPMN DI y regenera el SVG; nunca se corrige directamente el SVG.
7. El modelo debe poder abrirse fuera de la futura aplicacion mediante una herramienta BPMN compatible.

## 8. Automatizacion requerida

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
- la narrativa y la vista deben referirse al mismo modelo;
- AS-IS, analisis y TO-BE permanecen separados;
- los hallazgos abiertos son visibles.

Antes de una release:

- BPMN XML es la fuente maestra del modelo formal;
- SVG y PDF son reproducibles;
- las aprobaciones humanas estan registradas;
- las reglas normativas utilizadas cumplen el protocolo de conocimiento confiable;
- el manifiesto de release identifica maestros y derivados.

## 11. Relaciones

- [Iniciativa de modelamiento hibrido](iniciativas/iniciativa-modelamiento-hibrido.md)
- [Metodologia de modelamiento](metodologia-modelamiento.md)
- [Protocolo de versionado y releases](protocolo-versionado-y-releases.md)
- [Protocolo de trabajo con IA](protocolo-trabajo-con-ia.md)
- [Modelamiento](../03-modelamiento/README.md)
