---
id: INI-001
tipo: iniciativa
area: iniciativas
estado_documento: VIGENTE
estado_iniciativa: APROBADA
clase_conocimiento: DECISION
proceso:
  - S4
  - S4.3
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - tema/automatizacion
  - tema/ia
---

# INI-001 Modelamiento hibrido PlantUML y BPMN

La iniciativa implementara un camino inmediato de modelamiento logico con PlantUML y una solucion definitiva basada en BPMN 2.0 XML, derivados automaticos y una aplicacion local. El objetivo es que personas e IA modifiquen una sola fuente y que SVG, Markdown generado, validaciones y emisiones se mantengan sincronizados sin edicion archivo por archivo.

## 1. Problema y oportunidad

La vista Mermaid de las interacciones de S4 permite consultar relaciones, pero no reproduce adecuadamente piscinas, carriles y responsabilidades. Mantener manualmente una nota, un XML, un SVG y un PDF produciria duplicidad, errores y consumo innecesario de tiempo y tokens.

PlantUML ofrece una solucion textual inicial con carriles, facil de revisar en Git y de comunicar a IA. BPMN 2.0 XML ofrece la fidelidad semantica requerida para modelos formales. Una cadena automatizada permite usar ambos en momentos diferentes sin convertirlos en maestros paralelos.

## 2. Resultado esperado

El equipo dispondra de:

- una notacion logica textual para levantamiento y discusion;
- modelos BPMN formales con pools y lanes;
- SVG legibles dentro de Obsidian;
- resumenes Markdown generados para consulta humana y de IA;
- validaciones automaticas y reportes de inconsistencias;
- construccion incremental por hashes;
- intercambio compacto con IA mediante operaciones estructuradas;
- una interfaz web local construida sobre el mismo nucleo que la CLI.

## 3. Usuarios

- equipo de levantamiento y modelamiento;
- especialistas que revisan actividades y responsabilidades;
- responsables y duenos de proceso que validan las vistas;
- agentes de IA que analizan o proponen cambios;
- administradores del repositorio y futuras lineas base.

No se atribuyen funciones institucionales nuevas mediante esta lista.

## 4. Alcance

### Incluye

- contrato de archivos para modelos logicos y formales;
- renderizado local PlantUML a SVG;
- lectura, validacion y renderizado BPMN a SVG;
- resumen Markdown derivado;
- manifiestos, hashes y construccion incremental;
- CLI reproducible;
- formato compacto de intercambio con IA;
- aplicacion web local para visualizar, modificar y validar;
- integracion posterior con conocimiento normativo y requisitos BIM;
- comprobaciones previas a revision y release.

### No incluye inicialmente

- aprobacion automatica de modelos o reglas;
- sustitucion de entrevistas y validacion de especialistas;
- almacenamiento de expedientes o informacion sensible;
- colaboracion simultanea en tiempo real;
- publicacion en servicios externos;
- conversion automatica perfecta de PlantUML a BPMN;
- declaracion del repositorio como CDE institucional.
- conversion del mapa institucional de procesos Nivel 0 a PlantUML o BPMN; ese mapa conserva su representacion conceptual lineal en Markdown/Mermaid.

## 5. Decisiones rectoras

1. PlantUML se adopta como fuente editable del modelo logico durante el levantamiento.
2. BPMN 2.0 XML es la fuente maestra desde la formalizacion.
3. PlantUML y BPMN no permanecen como maestros editables simultaneos.
4. SVG, PDF, resumenes y reportes son derivados automaticos.
5. La ejecucion sera local y no enviara modelos institucionales a servidores externos.
6. La CLI se construira antes que la interfaz web.
7. La interfaz web reutilizara el mismo nucleo; no mantendra reglas exclusivas.
8. La IA propondra operaciones estructuradas y no editara manualmente todos los derivados.
9. El mapa institucional de procesos Nivel 0 queda exceptuado del flujo hibrido por no ser un modelo operativo BPMN.

Estas decisiones se formalizan en `DEC-012`, `DEC-013`, `DEC-014` y `DEC-015` del [registro de decisiones](../registro-decisiones.md).

## 6. Contrato de artefactos

La definicion obligatoria se encuentra en el [estandar de artefactos para el modelamiento hibrido](../estandar-artefactos-modelamiento.md).

El flujo general es:

```text
Etapa logica
narrativa.md + modelo-logico.puml
                    -> modelo-logico.svg

Formalizacion
narrativa contrastada + modelo-logico.puml
                    -> revision humana -> modelo.bpmn

Etapa formal
modelo.bpmn
    -> modelo.svg
    -> resumen-generado.md
    -> manifest.json
    -> validacion.json
    -> validacion.md
    -> PDF de release cuando corresponda
```

## 7. Reglas de modificacion

| Necesidad | Fuente que cambia | Salidas automaticas |
|---|---|---|
| Incorporar evidencia o alcance | Narrativa Markdown | Paquete de contexto |
| Ajustar flujo conceptual | PlantUML logico | SVG logico |
| Agregar o cambiar semantica BPMN | BPMN XML | SVG, resumen, manifiesto y validaciones |
| Cambiar disposicion visual formal | BPMN DI dentro del XML | SVG BPMN |
| Aplicar propuesta de IA | Operaciones YAML temporales aplicadas al maestro | Todos los derivados afectados |
| Emitir linea base | Tag y release sobre maestros aprobados | Manifiesto y derivados de publicacion |

Nunca se modifica una imagen para corregir el modelo.

## 8. Arquitectura prevista

### 8.1 Nucleo

Un paquete Python compatible con la politica del repositorio coordinara:

- descubrimiento de modelos y manifiestos;
- grafo de dependencias;
- calculo de hashes;
- construccion incremental;
- validadores;
- exportacion y aplicacion de operaciones para IA;
- comparacion y preparacion de release.

Ruta prevista: `05-herramientas/gestor-modelos/`.

### 8.2 Adaptador PlantUML

- ejecuta una version local fijada del motor;
- genera SVG sin acceso a servicios externos;
- captura errores de sintaxis;
- comprueba que la salida corresponda al hash del `.puml`;
- permite construir un modelo o todos los modificados.

### 8.3 Adaptador BPMN

- importa BPMN 2.0 XML;
- valida estructura e identificadores;
- conserva BPMN DI;
- genera SVG;
- extrae un resumen estructurado;
- prepara la vista para la futura web.

La alternativa tecnica preferente para visualizacion y edicion web es `bpmn-js`, sujeta a una prueba local de compatibilidad y reproducibilidad.

### 8.4 Interfaz de comandos

El primer producto operativo debe incluir:

```text
procesos init
procesos build [modelo|--changed|--all]
procesos check [modelo|--all]
procesos validate [modelo|--all]
procesos export-ai <modelo>
procesos apply <modelo> <cambios.yaml>
procesos diff <modelo>
procesos release-check <modelo>
```

### 8.5 Aplicacion web local

La web se construira despues de estabilizar la CLI y debe permitir:

- abrir modelos y derivados;
- ver pools, lanes, actividades, eventos y flujos;
- editar el BPMN maestro mediante controles validos;
- revisar operaciones propuestas por IA antes de aplicarlas;
- mostrar errores y relaciones con evidencia, reglas y BIM;
- comparar revisiones;
- reconstruir y verificar derivados;
- preparar paquetes de revision.

## 9. Requisitos funcionales

| ID | Requisito |
|---|---|
| RF-01 | Registrar cada modelo mediante un manifiesto estable. |
| RF-02 | Generar SVG local desde PlantUML. |
| RF-03 | Validar sintaxis PlantUML y reportar ubicacion del error. |
| RF-04 | Leer y validar BPMN 2.0 XML. |
| RF-05 | Generar SVG y resumen Markdown desde BPMN. |
| RF-06 | Detectar derivados ausentes, alterados o desactualizados. |
| RF-07 | Reconstruir solo dependencias afectadas. |
| RF-08 | Exportar contexto compacto para IA. |
| RF-09 | Aplicar operaciones estructuradas al maestro y rechazar cambios invalidos. |
| RF-10 | Comparar versiones por elementos e IDs, ademas del diff textual. |
| RF-11 | Ejecutar controles previos a revision y release. |
| RF-12 | Procesar por lote todos los modelos registrados. |
| RF-13 | Exportar fichas de producto y proceso, fichas de indicador y procedimientos a PDF con la maquetacion de los anexos de la NT 002-2025-PCM-SGP, incluido el diagrama referenciado (`DEC-017`). |
| RF-14 | Rechazar cambios a documentos con `estado_institucional: APROBADO` que no sigan el circuito del archivo `-propuesta` (`DEC-017`). |

## 10. Requisitos no funcionales

| ID | Requisito |
|---|---|
| RNF-01 | Operacion local y sin envio de modelos a servicios externos. |
| RNF-02 | Compatibilidad desde Python 3.11 estable. |
| RNF-03 | Resultados deterministas y dependencias fijadas. |
| RNF-04 | Escritura atomica: un fallo no reemplaza salidas integras. |
| RNF-05 | Nombres, rutas e IDs estables. |
| RNF-06 | Funcionamiento por CLI sin requerir interfaz visual. |
| RNF-07 | Mensajes de error accionables y reportes legibles. |
| RNF-08 | Pruebas unitarias, de integracion y de regresion visual. |
| RNF-09 | Ningun derivado puede convertirse en fuente maestra oculta. |
| RNF-10 | El conjunto minimo de contexto para IA evita cargar imagenes o XML completo cuando no sea necesario. |

## 11. Fases y entregables

### Fase 0 - Gobierno y contrato

Entregables:

- protocolo de iniciativas;
- estandar de artefactos hibridos;
- ficha INI-001;
- decisiones registradas;
- plantilla reutilizable.

Criterio de aceptacion: documentos enlazados, consistentes y sin notas huerfanas.

### Fase 1 - Piloto PlantUML

Entregables:

- dependencia PlantUML local y fijada;
- plantilla de carriles;
- comando inicial de renderizado y verificacion;
- reproduccion logica del diagrama de interacciones de S4;
- SVG incrustados en sus notas Markdown.

Criterios de aceptacion:

- un solo comando regenera los SVG;
- no se requiere servicio externo ni edicion de imagen;
- carriles, textos y conexiones son legibles;
- las vistas mantienen trazabilidad hacia los PDF originales;
- Git solo muestra cambios esperados.

### Fase 2 - Gestor incremental

Entregables:

- manifiesto por modelo;
- comandos `build`, `check` y `validate`;
- hashes de fuentes y salidas;
- deteccion de edicion manual;
- construccion `--changed` y `--all`.

Criterio de aceptacion: cambiar una fuente regenera exclusivamente sus dependencias y `check` detecta cualquier salida obsoleta.

### Fase 3 - Vertical BPMN

Entregables:

- un BPMN piloto con pools y lanes;
- validador estructural;
- SVG y resumen Markdown generados;
- comparacion del modelo logico con el formal;
- paquete de revision humana.

Criterio de aceptacion: el BPMN abre en una herramienta compatible, todos los derivados corresponden a su hash y ninguna perdida semantica queda oculta.

### Fase 4 - Intercambio con IA

Entregables:

- exportacion compacta;
- esquema de operaciones;
- aplicacion transaccional de cambios;
- pruebas de rechazo y recuperacion.

Criterio de aceptacion: una propuesta valida modifica solo el maestro y regenera las salidas; una propuesta invalida no altera el modelo vigente.

### Fase 5 - Aplicacion web local

Entregables:

- visor y editor BPMN;
- panel de validacion y comparacion;
- revision de operaciones de IA;
- relaciones con conocimiento, evidencia y BIM;
- integracion con la CLI.

Criterio de aceptacion: toda operacion de la web utiliza el mismo nucleo y puede verificarse desde CLI.

### Fase 6 - Integracion y releases

Entregables:

- controles automatizados previos a commit o release;
- generacion de paquete de publicacion;
- manual de operacion y mantenimiento;
- adopcion en mas procesos.

Criterio de aceptacion: una clonacion limpia puede reconstruir y verificar los modelos con instrucciones versionadas.

## 12. Estrategia de pruebas

- Unitarias: hashes, rutas, IDs, dependencias y operaciones.
- Integracion: PlantUML a SVG y BPMN a SVG/resumen.
- Regresion: comparacion normalizada de salidas.
- Visual: inspeccion de carriles, conexiones, fuentes y recortes.
- Compatibilidad: apertura del BPMN en otra herramienta.
- Fallos: sintaxis invalida, salida alterada, motor ausente y escritura interrumpida.
- Reproducibilidad: construccion desde clon limpio.
- Seguridad: confirmacion de operacion local y ausencia de datos sensibles en temporales.

## 13. Riesgos y mitigaciones

| Riesgo | Mitigacion |
|---|---|
| Mantener PlantUML y BPMN manualmente | PlantUML deja de ser editable al formalizar y `check` controla la etapa declarada |
| Conversion con perdida semantica | Formalizacion revisada, no conversion ciega |
| Diferencias Git ruidosas | IDs estables, serializacion normalizada y generacion determinista |
| Dependencia excesiva de una interfaz | Nucleo y CLI independientes de la web |
| Fuga de informacion | Motores locales y temporales excluidos de Git |
| Derivados alterados | Hashes y advertencia `GENERADO - NO EDITAR` |
| Automatizacion prematura de un metodo inestable | Piloto PlantUML y vertical BPMN antes de construir la web completa |
| Confusion entre validacion tecnica y aprobacion | Estados y evidencia humana separados de los resultados del validador |

## 14. Fuentes tecnicas de referencia

Consultadas el 2026-10-16:

- [PlantUML - diagramas de actividad y swimlanes](https://plantuml.com/activity-diagram-beta)
- [bpmn-js - toolkit de renderizado y modelamiento BPMN 2.0](https://bpmn.io/toolkit/bpmn-js/)
- [OMG - Business Process Model and Notation 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/)

Estas referencias sustentan la seleccion tecnica, no validan el contenido de ningun proceso institucional.

## 15. Siguiente hito

La implementacion tecnica de la Fase 1 esta completada: PlantUML 1.2026.8 y su artefacto Windows x64 estan fijados por hash, existe una plantilla de carriles, el comando local genera y comprueba SVG y la vista institucional S4 fue traducida. La aceptacion de la fase permanece pendiente hasta que el equipo revise su fidelidad contra la ficha aprobada. La vista Mermaid se conserva como control comparativo hasta esa conformidad. El mapa de procesos Nivel 0 no se convierte y permanece como representacion conceptual lineal en Markdown/Mermaid.

El siguiente hito es registrar la conformidad o las correcciones de la traduccion S4. Despues se elaborara el diagrama de S4.3 junto con su ficha, conforme a la estructura de `DEC-017`. La exportacion de fichas a PDF segun los anexos de la NT y el control de inmutabilidad de documentos aprobados se incorporan como capacidades de las fases 2 y 6.

## 16. Relaciones

- [Registro de iniciativas](00-iniciativas.md)
- [Estandar de artefactos para el modelamiento hibrido](../estandar-artefactos-modelamiento.md)
- [Registro de decisiones](../registro-decisiones.md)
- [Metodologia de modelamiento](../metodologia-modelamiento.md)
- [S4.3 Ejecucion de la inversion](../../02-procesos/s4-gestion-de-las-inversiones/s4-3-ejecucion-inversion/00-s4-3-ejecucion-inversion.md)
- [Herramientas](../../05-herramientas/00-herramientas.md)
