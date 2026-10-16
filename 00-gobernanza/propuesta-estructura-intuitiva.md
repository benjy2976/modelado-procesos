---
id: GOV-PROP-ESTRUCTURA-INTUITIVA
tipo: propuesta
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: DECISION
proceso:
  - S4
  - S4.3
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/gobernanza
  - tema/obsidian
  - tema/procesos
---

# Propuesta de estructura intuitiva centrada en procesos

Version 3, aprobada por el equipo del proyecto el 2026-10-16 y registrada como `DEC-017`. Organiza el repositorio para que cada proceso se lea como lo pide la Norma Tecnica de gestion por procesos: por niveles jerarquizados en carpetas, con codigo y con su juego de documentos. La ficha de producto y proceso es el documento central y la fuente de los PDF que se aprobaran.

La migracion se ejecuto el 2026-10-16. En la seccion 8, la columna "Ruta actual" corresponde a la estructura anterior y se conserva como registro de la correspondencia aplicada.

## 1. Criterios acordados

1. **Los procesos se modelan directamente.** No hay carpetas por etapa de trabajo (alcance, levantamiento, analisis, validacion).
2. **La jerarquia son carpetas.** S4 contiene a S4.3, S4.3 contiene a S4.3.1 y asi sucesivamente, a medida que avanza el trabajo.
3. **Cada proceso agrupa sus documentos en su carpeta.** El estado se registra en los metadatos de cada archivo, nunca mediante carpetas.
4. **Todo lo no aprobado es propuesta.** Lo que cambia es su nivel de revision. Lo aprobado no se modifica directamente.
5. **La ficha sigue exactamente el Anexo 2 de la NT.** Contiene los datos de la ficha y referencia el SVG del diagrama. Es la fuente desde la que se exportara el PDF a aprobar.
6. **Las fichas de indicador van en archivo propio** (Anexo 4), tambien en S4.
7. **El sustento va aparte.** Fuentes, evidencias, discrepancias y pendientes se registran en un archivo de sustento por proceso, que no se exporta.
8. **El TO-BE se mantiene en un arbol separado**, con la misma jerarquia. En esta etapa solo se documenta como pendiente y no se desarrolla.

## 2. Lo que pide la norma tecnica

Fuente: Norma Tecnica N 002-2025-PCM-SGP, aprobada por Resolucion de Secretaria de Gestion Publica N 002-2025-PCM-SGP del 21-02-2025. Original: [norma tecnica](../01-referencias/02-gestion-por-procesos/originales/nt-002-2025-pcm-sgp/norma-tecnica-n-002-2025-pcm-sgp-f-f.pdf), registro `PROC-001`. Fecha de consulta: 2026-10-16. Vigencia juridica: por confirmar segun el catalogo documental.

> [!warning] Clase de conocimiento
> Las afirmaciones de esta seccion son `NORMATIVO` citado y pendiente de validacion; aun no existe una regla curada en el catalogo. Orientan el diseno de carpetas, pero no sustentan una linea base hasta cumplir el [protocolo de conocimiento confiable](protocolo-conocimiento-confiable.md).

| Elemento normativo | Ubicacion precisa | Consecuencia para la estructura |
|---|---|---|
| El nivel 0 (macroproceso) se desagrega en nivel 1, nivel 2 hasta el ultimo nivel n | Glosario, pagina PDF 22 | Las carpetas de procesos se anidan por nivel |
| Codigo con letra M, E o S mas numeracion por nivel (`M1`, `M1.2`, `M1.2.4`) | Anexo 1, pagina PDF 25 | El codigo encabeza cada carpeta y cada archivo |
| La documentacion se compone de ficha de producto y proceso (incluye diagrama), ficha de indicador, mapa de procesos institucional y procedimiento | Numeral 6.1.3, pagina PDF 11 | Un juego fijo de documentos por proceso |
| Los duenos de proceso determinan los niveles 1 en adelante, elaborando y aprobando las fichas y sus fichas de indicador | Numeral 6.1.2, paso 3, pagina PDF 11 | La ficha de S4.3 y las de sus subprocesos son productos que deben elaborarse |
| El mapa de procesos institucional corresponde al nivel 0 y lo aprueba la maxima autoridad administrativa | Numeral 6.1.3 c, pagina PDF 13; Anexo 6, pagina PDF 30 | El mapa queda en un area propia |
| El procedimiento solo aplica a procesos de ultimo nivel, como maximo uno por proceso y solo si cumple algun criterio | Numeral 6.1.3 d, pagina PDF 13 | El procedimiento existe solo en las hojas del arbol que lo justifiquen |
| Riesgos y registros se consignan en la ficha de ultimo nivel | Anexo 2, pagina PDF 26 | La plantilla activa esos campos segun el nivel |
| Ficha, ficha de indicador y procedimiento: elaboracion y aprobacion del dueno del proceso, opinion tecnica de la unidad responsable de gestion por procesos | Numeral 6.1.4, Tabla 1, pagina PDF 14 | Los niveles de revision siguen ese circuito |
| Se recomienda BPMN para los diagramas | Nota 8, pagina PDF 12 | Confirma BPMN 2.0 XML como maestro formal |

## 3. Verificacion del insumo: fichas de S4.3

Fuente revisada: [s4-gestion-inversion.pdf](../01-referencias/01-institucionales-grh/originales/s4-gestion-inversion.pdf), con capa de texto, SHA-256 `F86C31E6...1F83`.

| Contenido de la fuente | Situacion en el repositorio |
|---|---|
| Ficha del proceso Nivel 0 S4: objetivo, tipo, duenos, objetivo estrategico | Transcrita; fidelidad pendiente de revision humana |
| Descomposicion Nivel 1 con proveedor, entrada, producto, receptor y responsable, incluida la fila S4.3 | Transcrita; fidelidad pendiente |
| Diagrama de interacciones de S4 | Transcrito en PlantUML/SVG; fidelidad pendiente |
| Fichas de indicador S4-IND-1 a S4-IND-3 | Transcritas dentro de la nota S4; pasaran a archivo propio |
| Ficha de producto y proceso propia de S4.3 (Nivel 1) | `EVIDENCIA-INSUFICIENTE`: no existe en las fuentes recibidas |
| Procesos Nivel 2 de S4.3 y sus procedimientos | `EVIDENCIA-INSUFICIENTE`: no existen en las fuentes recibidas |

Lo recibido sobre S4.3 esta transcrito y solo falta su conformidad humana. La ficha de S4.3 y sus niveles inferiores deben elaborarse conforme al numeral 6.1.2, paso 3. Los levantamientos del equipo y el documento interno para elaborar fichas, aun no aprobado, se incorporaran como insumos en el sustento de S4.3 cuando se compartan.

## 4. Arbol objetivo

```text
/
|-- 00-inicio.md                      puerta de entrada y ruta de lectura
|-- README.md  AGENTS.md  estado-del-proyecto.md  glosario.md
|-- 00-gobernanza/                    reglas, decisiones, iniciativas
|   `-- plantillas/                   antes 04-recursos-reutilizables/plantillas
|       |-- nt-002/                   NUEVO: ficha, indicador, procedimiento, inventario
|       |-- procesos/                 NUEVO: portada y sustento de proceso
|       |-- obsidian/
|       |-- modelamiento/
|       `-- conocimiento/             regla, evento de revision, paquete de contexto, manifiesto
|-- 01-referencias/                   sin cambios
|-- 02-procesos/                      NUEVO: une 02-arquitectura-procesos y 03-modelamiento
|   |-- README.md                     como leer niveles, codigos, estados y documentos
|   |-- mapa-de-procesos-institucional/            Nivel 0 (NT 6.1.3 c, Anexos 1, 5 y 6)
|   |   |-- README.md
|   |   |-- mapa-procesos-nivel-0.md                excepcion DEC-015
|   |   `-- inventario-productos-procesos.md        formato Anexo 1, ramas en alcance
|   |-- s4-gestion-de-las-inversiones/              S4 - Nivel 0
|   |   |-- README.md                               portada
|   |   |-- s4-ficha-producto-proceso.md            transcripcion fiel del original aprobado
|   |   |-- s4-fichas-indicador.md                  S4-IND-1 a 3
|   |   |-- s4-diagrama-proceso-logico.puml         vista transcrita
|   |   |-- s4-diagrama-proceso-logico.svg          derivado
|   |   |-- s4-diagrama-proceso-modelo.yaml
|   |   |-- s4-sustento.md                          fuente, calidad, fidelidad, discrepancias
|   |   `-- s4-3-ejecucion-inversion/               S4.3 - Nivel 1 (alcance del proyecto)
|   |       |-- README.md
|   |       |-- s4-3-ficha-producto-proceso.md      Anexo 2 (a elaborar)
|   |       |-- s4-3-fichas-indicador.md            Anexo 4 (a elaborar)
|   |       |-- s4-3-diagrama-proceso-logico.puml   maestro mientras es modelo logico
|   |       |-- s4-3-diagrama-proceso.bpmn          maestro desde la formalizacion
|   |       |-- s4-3-diagrama-proceso.svg           derivado; la ficha lo referencia
|   |       |-- s4-3-sustento.md
|   |       `-- s4-3-1-<nombre>/                    S4.3.1 - Nivel 2, mismo patron
|   |           `-- s4-3-1-procedimiento.md         solo si es ultimo nivel y cumple criterios
|   `-- to-be/                                      PENDIENTE: no se desarrolla en esta etapa
|       `-- README.md                               proposito, alcance futuro y reglas
|-- 03-conocimiento/                  antes 04-recursos-reutilizables (sin plantillas)
|-- 04-coordinacion/                  antes 06-coordinacion
|-- 05-herramientas/                  sin cambios
|-- 90-bandeja-entrada/
`-- 99-temporal/
```

Las subcarpetas de nivel 2 se crean solo cuando se apruebe la descomposicion de S4.3. Dentro de S4 solo se desarrolla S4.3: S4.1, S4.2, S4.4 y S4.5 aparecen como filas en la portada de S4 y en el inventario, sin carpeta.

## 5. Documentos de cada proceso

| Archivo | Contenido | Se exporta a PDF | Cuando existe |
|---|---|---|---|
| `README.md` | Portada: ubicacion, objetivo, estado de cada documento, subprocesos y pendientes | No | Siempre |
| `<codigo>-ficha-producto-proceso.md` | Campos del Anexo 2, en su orden y con titulos fijos | Si | Siempre |
| `<codigo>-fichas-indicador.md` | Una seccion por indicador con los campos del Anexo 4 | Si | Cuando el dueno define indicadores |
| `<codigo>-diagrama-proceso-logico.puml` / `.bpmn` | Fuente maestra del diagrama, segun la etapa | No (derivado SVG/PDF) | Siempre |
| `<codigo>-diagrama-proceso.svg` | Vista generada; la ficha la referencia en "Actividades del proceso" | Incrustado en la ficha | Siempre |
| `<codigo>-procedimiento.md` | Campos del Anexo 7; diagrama de flujo del Anexo 8 como BPMN y SVG | Si | Solo en el ultimo nivel y si cumple los criterios del numeral 6.1.3 d |
| `<codigo>-sustento.md` | Fuentes con pagina, evidencias, clase de cada afirmacion, discrepancias, revisiones y `EVIDENCIA-INSUFICIENTE` | No | Siempre |
| `<codigo>-<documento>-propuesta.md` | Variacion de un documento aprobado | Si, como borrador | Solo cuando se plantea variar un documento aprobado |

### 5.1 Ficha conforme al Anexo 2

```markdown
## Nombre del proceso
## Tipo de proceso
## Dueno del proceso
## Objetivo del proceso
## Objetivo estrategico
## Proveedor | Elementos de entrada | Producto | Receptor del producto   (tabla)
## Actividades del proceso      -> referencia al SVG del diagrama
## Riesgos                      (solo ultimo nivel)
## Registros                    (solo ultimo nivel)
## Elaborado por | Revisado por | Aprobado por
```

Los titulos fijos permiten que una herramienta lea la ficha y genere el PDF con la maquetacion del Anexo 2, incluido el diagrama. El PDF es un derivado; la ficha Markdown es la unica fuente.

La ficha de S4 conserva la estructura y el contenido del original aprobado (formato institucional version 3.0), porque no puede modificarse. Las fichas nuevas siguen el Anexo 2.

## 6. Estados y niveles de revision

Todo documento no aprobado es una propuesta. Su avance se expresa con el nivel de revision, alineado con el circuito del numeral 6.1.4:

```yaml
codigo_proceso: S4.3
nivel_proceso: 1
tipo_proceso: APOYO              # MISIONAL | ESTRATEGICO | APOYO
proceso_padre: S4
documento_nt: ficha-producto-proceso   # inventario | mapa | ficha-producto-proceso | ficha-indicador | procedimiento
anexo_nt: 2
estado_institucional: PROPUESTA  # PROPUESTA | APROBADO
nivel_revision: ELABORACION      # ELABORACION | REVISION-EQUIPO | OPINION-TECNICA | APROBACION
modifica: null                   # solo en archivos -propuesta: documento aprobado que se busca variar
```

Cada nivel concluye con una conformidad distinta, otorgada por personas o instancias distintas:

| Nivel de revision | Que ocurre | Quien otorga la conformidad para avanzar | Forma | Campo de la ficha | Referencia |
|---|---|---|---|---|---|
| `ELABORACION` | El documento se construye | Quien elabora lo remite a revision del equipo | Remision registrada | Elaborado por | NT 6.1.4, Tabla 1; Anexo 2 |
| `REVISION-EQUIPO` | Revision interna del proyecto | Un integrante del equipo como representante del equipo | Declarativa | No figura en la ficha | Control propio del proyecto |
| `OPINION-TECNICA` | Revision tecnica conforme a la NT | Sub Gerencia de Modernizacion y Transformacion Digital | Opinion tecnica documentada | Revisado por | NT 6.1.4, Tabla 1; Anexo 2 |
| `APROBACION` | Decision final sobre el documento | Dueno del proceso | Aprobacion documentada | Aprobado por | NT 6.1.4, Tabla 1; Anexo 2 |

La denominacion de la Sub Gerencia proviene de la transcripcion del [mapa de procesos Nivel 0](../02-procesos/mapa-de-procesos-institucional/mapa-procesos-nivel-0.md). Su funcion como unidad responsable de la opinion tecnica fue indicada por el equipo del proyecto el 2026-10-16 y debe sustentarse con el documento de organizacion vigente cuando se disponga de el.

Una observacion en cualquier nivel devuelve el documento a `ELABORACION`. El dueno de cada proceso se toma de su ficha o de la ficha del proceso padre aprobada; si no puede determinarse, se registra `EVIDENCIA-INSUFICIENTE`.

El sustento de cada proceso mantiene un historial de revision con una fila por paso: documento, nivel, fecha, resultado (conforme u observado), rol o unidad que lo otorga y evidencia (declaracion, informe, memorando o acta). Se registran roles y unidades, no datos personales adicionales.

Reglas:

1. Cada conformidad la registra una persona con la evidencia correspondiente. La IA no registra, presume ni atribuye conformidades, y nunca asigna el estado `APROBADO`.
2. Un documento `APROBADO` no se edita. Se marca su version con un tag Git.
3. Para variarlo se crea un unico archivo `-propuesta`, con nombre fijo y el campo `modifica`. Nunca se usan `final`, numeros de copia ni fechas en el nombre.
4. Al aprobarse la variacion, su contenido reemplaza al documento vigente en un solo commit, se elimina el archivo `-propuesta` y se crea un nuevo tag. Git conserva el historial.
5. Un control automatico rechazara cambios a documentos `APROBADO` que no sigan este circuito.

## 7. Arbol TO-BE

`02-procesos/to-be/` reservara el rediseno futuro con la misma jerarquia del arbol principal (por ejemplo `to-be/s4-gestion-de-las-inversiones/s4-3-ejecucion-inversion/`). Los archivos llevaran el sufijo `-to-be` (por ejemplo `s4-3-ficha-producto-proceso-to-be.md`) para no confundirse con los del arbol principal en busquedas y enlaces.

En esta etapa solo existira su `README.md`, que documentara proposito, relacion con el arbol principal y condiciones para iniciarlo. El analisis de brechas y oportunidades se desarrollara junto con el TO-BE.

## 8. Correspondencia de rutas

| Ruta actual | Ruta propuesta | Operacion |
|---|---|---|
| `02-arquitectura-procesos/README.md` | `02-procesos/00-procesos.md` | mover y reescribir |
| `02-arquitectura-procesos/mapa-procesos-nivel-0.md` | `02-procesos/mapa-de-procesos-institucional/mapa-procesos-nivel-0.md` | mover |
| `02-arquitectura-procesos/inventario-procesos.md` | `02-procesos/mapa-de-procesos-institucional/inventario-productos-procesos.md` | mover y adaptar al Anexo 1 con productos de la ficha S4 |
| `02-arquitectura-procesos/s4-gestion-de-las-inversiones.md` | `02-procesos/s4-gestion-de-las-inversiones/` dividido en `s4-ficha-producto-proceso.md`, `s4-fichas-indicador.md` y `s4-sustento.md` | mover y dividir sin alterar el contenido transcrito |
| `02-arquitectura-procesos/s4-gestion-de-las-inversiones-logico.puml`, `.svg` y `-modelo.yaml` | `02-procesos/s4-gestion-de-las-inversiones/s4-diagrama-proceso-logico.*` y `s4-diagrama-proceso-modelo.yaml` | mover y regenerar SVG |
| `03-modelamiento/README.md` | integrado en `02-procesos/00-procesos.md` | eliminar despues de integrar |
| `03-modelamiento/procesos/s4-3-ejecucion-inversion/README.md` | `02-procesos/s4-gestion-de-las-inversiones/s4-3-ejecucion-inversion/00-s4-3-ejecucion-inversion.md` | mover y reescribir como portada |
| `03-modelamiento/.../00-alcance`, `01-levantamiento`, `02-modelos/as-is`, `03-analisis`, `05-validacion` | se retiran (vacias); su funcion pasa a la ficha, el diagrama y el sustento | eliminar |
| `03-modelamiento/.../02-modelos/to-be` | `02-procesos/to-be/` | reemplazar por README de pendiente |
| `03-modelamiento/.../04-bim/README.md` | criterios BIM dentro de la plantilla de sustento, hasta que se defina su tratamiento | integrar |
| `04-recursos-reutilizables/plantillas/` | `00-gobernanza/plantillas/` | mover; YAML de conocimiento a `plantillas/conocimiento/` |
| `04-recursos-reutilizables/conocimiento/*` y carpetas de actores, sistemas, documentos, riesgos y reglas de negocio | `03-conocimiento/` | mover |
| `04-recursos-reutilizables/indicadores`, `componentes-bpmn` | se retiran (vacias) | los indicadores viven en cada proceso |
| `06-coordinacion/` | `04-coordinacion/` | mover |

## 9. Ajustes a reglas vigentes

La aprobacion de esta propuesta requiere registrar una decision (`DEC-017`) y ajustar:

- `AGENTS.md`: la separacion AS-IS, analisis y TO-BE pasa de carpetas de trabajo a dos arboles (principal y `to-be/`); el analisis acompanara al TO-BE. Tambien cambia la ruta del paquete de contexto.
- [Metodologia de modelamiento](metodologia-modelamiento.md): pasos alineados a las fases de la NT y a los documentos por proceso.
- [Estandar de artefactos](estandar-artefactos-modelamiento.md), seccion 3: nuevo contrato de archivos por proceso.
- [Estandar obligatorio de Obsidian](estandar-obligatorio-obsidian.md): propiedades `codigo_proceso`, `nivel_proceso`, `documento_nt`, `estado_institucional`, `nivel_revision` y `modifica`.

## 10. Impactos tecnicos

- Enlaces Markdown: 24 notas citan rutas de `02-arquitectura-procesos`, `03-modelamiento` o `04-recursos-reutilizables`.
- Configuracion Obsidian versionada: `.obsidian/templates.json` y `.obsidian/daily-notes.json`.
- Vistas: `06-coordinacion/bases/documentacion.base` y `06-coordinacion/canvas/flujo-del-conocimiento.canvas`.
- Especificaciones del validador y del extractor que citan rutas de conocimiento y plantillas.
- El renderizador PlantUML recibe rutas por argumento y no requiere cambios.
- Herramientas nuevas para mas adelante: exportador de fichas a PDF segun los Anexos 2, 4 y 7, y control de inmutabilidad de documentos `APROBADO`.

## 11. Migracion propuesta

1. Aprobacion general de esta propuesta y registro de `DEC-017`.
2. Confirmar en un commit propio el trabajo pendiente actual, para partir de una base limpia.
3. Ejecutar todos los movimientos con `git mv` en un unico commit, sin copias.
4. Reescribir enlaces y configuraciones mediante un script verificable.
5. Dividir la nota S4 en ficha, fichas de indicador y sustento, conservando paginas y discrepancias.
6. Adaptar el inventario al Anexo 1.
7. Crear las plantillas `nt-002` y `procesos`, las portadas de `02-procesos`, S4 y S4.3 y el README de `to-be/`.
8. Ajustar `AGENTS.md`, la metodologia y los estandares segun la seccion 9.
9. Verificar: auditoria de reproducibilidad, `--check` del SVG regenerado, cero enlaces rotos, cero notas huerfanas y ninguna ruta antigua activa.
10. Integrar mediante rama y solicitud de cambio.

Criterio de aceptacion: una persona sin conocer la arquitectura del repositorio encuentra desde `00-inicio.md`, en no mas de tres clics, la ficha de S4, la situacion de S4.3 y el siguiente documento a elaborar.

## 12. Estado de las decisiones

| Tema | Situacion |
|---|---|
| Jerarquia de procesos en carpetas por codigo | Aprobado |
| Sin carpetas de etapas de trabajo | Aprobado |
| Ficha conforme al Anexo 2 como fuente del PDF | Aprobado |
| Fichas de indicador en archivo propio, incluida S4 | Aprobado |
| Archivo de sustento por proceso | Aprobado |
| Arbol TO-BE separado y pendiente | Aprobado |
| Renumeracion de conocimiento (`03`) y coordinacion (`04`) | Aprobado |
| Niveles de revision y responsables de cada conformidad | Aprobado |
| Circuito de archivos `-propuesta` para variar documentos aprobados | Aprobado |
| Criterios BIM dentro de la plantilla de sustento | Aprobado |
| Aprobacion general de esta propuesta | Aprobada el 2026-10-16 (`DEC-017`) |

## Relaciones

- [Arquitectura de informacion vigente](arquitectura-de-informacion.md)
- [Estandar obligatorio de Obsidian](estandar-obligatorio-obsidian.md)
- [Estandar de artefactos para el modelamiento hibrido](estandar-artefactos-modelamiento.md)
- [Protocolo de versionado y releases](protocolo-versionado-y-releases.md)
- [Registro de decisiones](registro-decisiones.md)
- [Procesos](../02-procesos/00-PROCESOS.md)
