---
tipo: estado-proyecto
area: proyecto
estado_documento: VIGENTE
clase_conocimiento: OBSERVADO
fecha_actualizacion: 2026-11-04
confidencialidad: INTERNO
tags:
  - tema/gobernanza
---

# Estado del proyecto

- Fecha de actualizacion: 2026-11-04
- Fase: estructura centrada en procesos implementada (`DEC-017`); traduccion S4 lista para revision humana de fidelidad; propuesta de nivel 1 de S4.3 actualizada a la secuencia S4.3.1 Inicio de ejecucion, S4.3.2 Ejecucion y S4.3.3 Recepcion, con entrada contractual desde S3.2 Adquisiciones (`DEC-028`)
- Ambito inicial: S4.3 Ejecucion de la inversion
- Estado de los procesos: mapa Nivel 0 y ficha S4 confirmados como lineas base institucionales aprobadas; la nota S4 se dividio en ficha de producto y proceso, fichas de indicador y sustento, pendientes de conformidad humana de fidelidad; S4.3 delimitado (`DEC-020`) con modelo logico y ficha borrador en `ELABORACION`; su diagrama principal refleja la propuesta lineal de `DEC-028`; S4.3.1 fue renombrado a Inicio de ejecucion y conserva solo una nota indice pendiente de detalle; la propuesta anterior de S4.3.1 y los respaldos anterior e inmediatamente previo al reemplazo de S4.3.2 se guardaron en `99-temporal/modelos/` (`DEC-029`, `DEC-030`); S4.3.2 tiene un modelo logico de larga duracion y tres procesos de nivel 3 (`DEC-032`); S4.3.2.2 ya cuenta con modelo detallado de contratista, supervision, OACGD, SGGOS, SGE y proyectista, con informe tecnico de especialistas y firma del Subgerente de Estudios (`DEC-033`); S4.3.2.3 separa actores de obra, monitor, control contractual y costos, elaborador, revision tecnica competente e independiente, controles complementarios y decisor (`DEC-037`, `DEC-038`), pendiente de validacion institucional; S4.3.3 queda pendiente de desarrollo; 12 guias de lectura de fuentes, 32 reglas normativas y un paquete de conocimientos BPMN `BORRADOR-IA` pendientes de validacion humana; TO-BE pendiente para una etapa posterior
- Estado BIM: aprendizaje y adopcion progresiva; la informacion se organizara con rutas estables y trazabilidad Git, sin declarar el repositorio como CDE institucional
- Descargas: 231 recursos publicos indexados; la auditoria del 2026-10-19 encontro 204 presentes y verificados por hash en esta copia local y 27 pendientes de restauracion. El Formato 08-A del MEF, actualizado al 18-02-2026, se incorporo como XLSX (`INV-005A`) con integridad y hash comprobados, pendiente de revision visual y de aplicabilidad por el equipo. La Ley 29783 requiere OCR en copia derivada.
- Git: estrategia hibrida configurada; repositorio inicial publicado en remoto, recursos publicos regenerables fuera de Git y LFS reservado para binarios no reproducibles
- Obsidian: boveda independiente operativa mediante CLI; notas indice `00-<nombre>.md` en lugar de `README.md`, navegacion `Sube a:` hacia el indice inmediato y grupos de color comunes del grafo (`DEC-018`); entrada `00-GESTION-POR-PROCESOS-GRH.md`, mayusculas en tres niveles, etiquetas controladas `tema/` y `proceso/`, nodos de referencia, actores e interacciones enlazadas para la vista del modelo de procesos (`DEC-019`); estandar obligatorio de autoria, mapas, propiedades, plantillas, reuniones, Canvas y Bases definidos; estado visual excluido de Git
- Conocimiento: manual operativo y protocolo obligatorio definidos; catalogo, plantillas y requisitos del validador web preparados; implementacion pendiente
- Reproducibilidad: dependencias fijadas, auditor automatizado aprobado, `origin` sincronizado y cuatro objetos LFS recuperados e integros; falta validar la clonacion completa desde otro equipo
- Modelamiento: cadena BPMN adoptada (`DEC-025`) y aplicada a todo flujo de proceso en modelamiento (`DEC-026`): el diagrama principal S4.3 refleja la propuesta de `DEC-028`; S4.3.2 fue reemplazado por la propuesta agrupada de `DEC-030`, refinado en notacion por `DEC-031` y desagregado formalmente por `DEC-032`; S4.3.2.2 fue regenerado con cuatro pools, carriles institucionales y el tratamiento de la opinion del proyectista o el vencimiento de su plazo (`DEC-033`); el piloto visual de S4.3.2.2 usa `zigzag-controlado` (`DEC-035`) y S4.3.2.3 usa `zigzag-amplio` para el flujo ramificado (`DEC-036`) con segregacion de responsabilidades (`DEC-038`) y compresion de filas inactivas por carril (`DEC-039`); D1, D2, D3 y D5 quedan sin hallazgos en este ultimo modelo y D4 conserva dos superposiciones menores de rotulos documentadas en su sustento; PlantUML queda para vistas que no son flujos y para S4 aprobado; paleta BPMN del proyecto y control de notacion D5 adoptados (`DEC-027`), con catalogo de simbolos como prueba de regresion
- PAD: el mapa institucional Nivel 1 y la ficha S1 ubican el producto disciplinario en S1.4 Administracion de las personas. Cinco BPMN y cinco fichas candidatas del Anexo 2, inventario del Anexo 1, tres fichas de indicador candidatas del Anexo 4 y evaluacion de procedimientos estan agrupados bajo S1.4; no representan AS-IS observado ni una linea base aprobada. Codigo, nombre y descomposicion del eventual hijo PAD siguen pendientes; otras areas participan como interfaces sin cambiar la pertenencia principal identificada.
- Entorno ampliado: politica abierta desde Python estable 3.11; `.venv` local operativo con CPython 3.14.7 x64, dependencias universales con hashes y controles de instalacion y funcionamiento; guia propuesta en [Herramientas](05-herramientas/guia-entorno.md)

## Completado

- Inventario inicial de cuatro PDF.
- Estructura documental de trabajo y protocolo de versionado mediante tags/releases.
- Criterios iniciales de calidad documental.
- Descarga trazable desde fuentes oficiales de PCM MEF OECE Contraloria y MVCS.
- Incorporacion del DS 140-2026-EF como Reglamento vigente de Invierte.pe y de las bases estandar 2026 de la Ley 32069.
- Registro de URL hash SHA-256 formato e indicadores de legibilidad/OCR por archivo.
- Revision visual de una muestra critica y correccion del enlace de la Guia Nacional BIM 2023.
- Configuracion de atributos Git LFS para documentos binarios y futuros formatos BIM/CAD.
- Definicion del flujo de trabajo con IA, conocimiento normativo confiable y validacion humana.
- Modelo de datos inicial para reglas, eventos de revision, catalogo y paquetes de contexto.
- Requisitos funcionales y criterios de aceptacion del validador web interno.
- Documento y auditor automatizado de reproducibilidad con limites externos declarados.
- Configuracion portable de la boveda Obsidian y verificacion de acceso mediante CLI.
- Manual operativo para clasificar conocimiento y aplicar validaciones desde la fuente hasta la linea base.
- Arquitectura inicial de navegacion con mapas de contenido y relaciones portables entre areas.
- Estandar obligatorio de produccion en Obsidian, configuracion compartida de plantillas y notas diarias, y area de coordinacion.
- Transcripcion trazable del mapa de procesos Nivel 0 y de la ficha S4, incluidos intercambios, vista de relaciones, indicadores y discrepancias pendientes de conformidad o decision humana.
- Protocolo y plantilla para documentar iniciativas con alcance, arquitectura, fases, pruebas, riesgos y criterios de aceptacion.
- Iniciativa INI-001 y estandar de artefactos aprobados para el modelamiento hibrido PlantUML/BPMN y su futura automatizacion.
- Excepcion expresa del mapa institucional Nivel 0, que permanece como representacion conceptual lineal en Markdown/Mermaid.
- Adopcion expresa del mapa Nivel 0 y la ficha S4 como lineas base institucionales oficiales y aprobadas, manteniendo pendiente la identificacion del acto y la fecha formal no visibles en los PDF.
- Piloto PlantUML local y reproducible: version fijada, ejecutable nativo Windows verificado, plantilla de carriles, comando de renderizado/comprobacion y vista S4 generada.
- Estructura centrada en procesos conforme a la NT 002-2025-PCM-SGP aprobada (`DEC-017`) e implementada: procesos jerarquizados por codigo en `02-procesos`, documentos y plantillas segun los Anexos 2, 4 y 7, niveles de revision en metadatos, sustento por proceso y arbol TO-BE reservado.

## Siguiente hito

Recibir el detalle de S4.3.1 Inicio de ejecucion; confirmar la unidad de instancia de S4.3.2; revisar con el equipo S4.3.2.1; validar el modelo detallado de S4.3.2.2 y completar su variante con inspector, denominaciones documentales e indicadores; validar en S4.3.2.3 la autoridad y delegaciones por figura, la asignacion del control contractual y de costos, los criterios de intervencion de SGE, Presupuesto y GRAJ, el mecanismo para obtener especialistas independientes, la remision a Contraloria y el alcance de intensificacion; corregir las dos superposiciones menores BPMN-DI antes de una linea base; desarrollar posteriormente S4.3.3 Recepcion. En paralelo, revisar la fidelidad de la ficha y los intercambios de S4.3 contra las fuentes institucionales, sin atribuir conformidad ni aprobacion.
