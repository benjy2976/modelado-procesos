---
tipo: estado-proyecto
area: proyecto
estado_documento: VIGENTE
clase_conocimiento: OBSERVADO
fecha_actualizacion: 2026-11-18
confidencialidad: INTERNO
tags:
  - tema/gobernanza
---

# Estado del proyecto

- Fecha de actualizacion: 2026-11-18
- Fase: estructura centrada en procesos implementada (`DEC-017`); traduccion S4 lista para revision humana de fidelidad; propuesta de nivel 1 de S4.3 actualizada a la secuencia S4.3.1 Inicio de ejecucion, S4.3.2 Ejecucion y S4.3.3 Recepcion, con entrada contractual desde S3.2 Adquisiciones (`DEC-028`)
- Ambito inicial: S4.3 Ejecucion de la inversion
- Estado de los procesos: mapa Nivel 0 y ficha S4 confirmados como lineas base institucionales aprobadas; la nota S4 se dividio en ficha de producto y proceso, fichas de indicador y sustento, pendientes de conformidad humana de fidelidad; S4.3 delimitado (`DEC-020`) con modelo logico y ficha borrador en `ELABORACION`; su diagrama principal refleja la propuesta lineal de `DEC-028`; S4.3.1 fue renombrado a Inicio de ejecucion y conserva solo una nota indice pendiente de detalle; la propuesta anterior de S4.3.1 y los respaldos de S4.3.2 se conservan en `99-temporal/modelos/` (`DEC-029`, `DEC-030`); S4.3.2 tiene un modelo logico de larga duracion y seis procesos hijos directos (`DEC-041`): control periodico, consultas, alcance, ampliaciones, suspensiones y paralizacion/reinicio. La pertenencia de residente, contratista o representante legal, control de obra e inspector se precisa en `DEC-042`: la pertenencia organizativa se conserva y los titulos funcionales de los modelos se precisan en `DEC-043`. S4.3.2.3 queda limitado a alcance con variantes internas sin nivel 4; S4.3.2.4 a S4.3.2.6 tienen juegos iniciales en `ELABORACION`; S4.3.3 queda pendiente de desarrollo; 14 guias de lectura de fuentes, 36 reglas normativas y un paquete de conocimientos BPMN `BORRADOR-IA` pendientes de validacion humana; TO-BE pendiente para una etapa posterior
- Estado BIM: aprendizaje y adopcion progresiva; la informacion se organizara con rutas estables y trazabilidad Git, sin declarar el repositorio como CDE institucional
- Descargas: 233 recursos publicos indexados; la auditoria del 2026-10-19 encontro 204 presentes y verificados por hash en esta copia local y 27 pendientes de restauracion. El Formato 08-A del MEF, actualizado al 18-02-2026, se incorporo como XLSX (`INV-005A`) con integridad y hash comprobados, pendiente de revision visual y de aplicabilidad por el equipo. La Ley 29783 requiere OCR en copia derivada.
- Git: estrategia hibrida configurada; repositorio inicial publicado en remoto, recursos publicos regenerables fuera de Git y LFS reservado para binarios no reproducibles
- Obsidian: boveda independiente operativa mediante CLI; notas indice `00-<nombre>.md` en lugar de `README.md`, navegacion `Sube a:` hacia el indice inmediato y grupos de color comunes del grafo (`DEC-018`); entrada `00-GESTION-POR-PROCESOS-GRH.md`, mayusculas en tres niveles, etiquetas controladas `tema/` y `proceso/`, nodos de referencia, actores e interacciones enlazadas para la vista del modelo de procesos (`DEC-019`); estandar obligatorio de autoria, mapas, propiedades, plantillas, reuniones, Canvas y Bases definidos; estado visual excluido de Git
- Conocimiento: manual operativo y protocolo obligatorio definidos; catalogo, plantillas y requisitos del validador web preparados; implementacion pendiente
- Reproducibilidad: dependencias fijadas, auditor automatizado aprobado, `origin` sincronizado y cuatro objetos LFS recuperados e integros; falta validar la clonacion completa desde otro equipo
- Modelamiento: cadena BPMN adoptada (`DEC-025`) y aplicada a todo flujo de proceso en modelamiento (`DEC-026`), con ciclo textual por lotes para IA (`DEC-040`): la tabla y el sustento concentran las iteraciones conceptuales, la generacion focalizada mantiene los derivados actualizados sin incorporarlos al contexto y la revision visual se reserva para una puerta expresa. El diagrama principal S4.3 refleja la propuesta de `DEC-028`; S4.3.2 conserva la instancia de larga duracion de `DEC-030`, la notacion de `DEC-031` y muestra seis subprocesos de evento no interruptivos conforme a `DEC-041`, sin bucle ni nivel 4. Los seis modelos hijos usan `zigzag-controlado`. `DEC-042` integra residente, contratista o representante legal y especialistas propios dentro del Ejecutor de obra, y declara Control de obra como abstraccion funcional alternativa para supervisor contratado o inspector de la entidad. Cuaderno de Incidencias y SGGOS — Coordinador de obra permanecen como denominaciones comunes; los demas titulos de carril y la notacion SGD siguen `DEC-043`. La generacion focalizada del 2026-11-05 deja D1, D2, D3 y D5 sin hallazgos en los modelos afectados; D4 conserva diez advertencias geometricas en S4.3.2.3, seis en S4.3.2.5 y dos en S4.3.2.6, documentadas como pendientes de revision visual antes de una linea base. PlantUML queda para vistas que no son flujos y para S4 aprobado; paleta BPMN y control D5 adoptados (`DEC-027`)
- Controles de cierre S4.3.2: `construir_modelos.py --check` finaliza correctamente para todos los modelos y `gestionar_etiquetas.py revisar` informa 172 notas revisadas y 0 problemas al 2026-11-10.
- Operacion para reuniones (`DEC-044`): los ocho diagramas existentes de S4.3 tienen numeros de referencia persistentes en sus tablas y derivados; `modelar.py <codigo>` construye solo el modelo indicado, mide cada etapa y usa cache local por contenido y productos. La comprobacion global del 2026-11-17 finaliza correctamente. Los hallazgos D4 ya documentados de S4.3.2.3 (18) y S4.3.2.6 (6) siguen pendientes de revision visual.
- Convencion S4.3.2 del 2026-11-10 (`DEC-043`): la seccion 7.4 del estandar fija titulos de participantes y carriles y representa el SGD como almacen de datos BPMN junto a tareas humanas de registro o derivacion interna. Se aplico en las seis tablas hijas; los modelos mixtos conservan la distincion por regimen. S4.3.2.3 y S4.3.2.6 mantienen respectivamente 18 y 6 hallazgos geometricos D4 documentados y revision visual pendiente.
- PAD: el mapa institucional Nivel 1 y la ficha S1 ubican el producto disciplinario en S1.4 Administracion de las personas. Cinco BPMN y cinco fichas candidatas del Anexo 2, inventario del Anexo 1, tres fichas de indicador candidatas del Anexo 4 y evaluacion de procedimientos estan agrupados bajo S1.4; no representan AS-IS observado ni una linea base aprobada. Codigo, nombre y descomposicion del eventual hijo PAD siguen pendientes; otras areas participan como interfaces sin cambiar la pertenencia principal identificada.
- Entorno ampliado: politica abierta desde Python estable 3.11; `.venv` local operativo con CPython 3.14.7 x64, dependencias universales con hashes y controles de instalacion y funcionamiento; guia propuesta en [Herramientas](05-herramientas/guia-entorno.md)

- S4.3.2.2, 2026-11-18: caja 52 precisa que la carta identifica al elaborador del adicional segun las bases cuando corresponda, sin presumirlo. Perfil optativo `zigzag-corredores` (`DEC-045`) aplicado por solicitud de revision visual: D1-D5 sin hallazgos, imagen inspeccionada, cuatro pruebas de regresion correctas y comprobacion global satisfactoria. Bases del contrato concreto y acto de emision pendientes; permanece en `ELABORACION`.

- S4.3.2.3, 2026-11-18: replanteamiento conceptual DEC-046 diferencia adicional con deductivo vinculado, reduccion independiente y mayores metrados; incorpora interfaz de consultas, 15 dias desde anotacion y 10 dias de supervision cuando elabora contratista, con opinion institucional concurrente. Se mantiene el alcance y los codigos; separacion en procesos propios pendiente. CON-010 y CON-011 incorporan las opiniones OECE D000092 y D000083 con guias y cuatro reglas BORRADOR-IA: la respuesta de consulta precede a la anotacion especifica; el computo no se suspende por demora de ratificacion. Elaboracion por entidad tiene ruta precisada; otros regimenes y plazos pendientes requieren completar evidencia. Sin validacion normativa ni conformidad institucional.

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
- Adopcion del ciclo conceptual por lotes para IA, con generacion focalizada de derivados y revision visual diferida (`DEC-040`).
- Reestructuracion de S4.3.2 en seis hijos directos, con alcance y tres figuras de plazo separadas, sin nivel 4 (`DEC-041`).
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

Recibir el detalle de S4.3.1 Inicio de ejecucion; confirmar la unidad de instancia de S4.3.2; revisar con el equipo S4.3.2.1; validar S4.3.2.2 y su variante con inspector; validar los modelos de S4.3.2.3 a S4.3.2.6, en especial duenos, delegaciones, control contractual, especialistas competentes, controles presupuestales y juridicos, actos, registros y diferencias por regimen; decidir la ubicacion de intensificacion, que permanece con `EVIDENCIA-INSUFICIENTE`; desarrollar posteriormente S4.3.3 Recepcion. En paralelo, revisar la fidelidad de la ficha y los intercambios de S4.3 contra las fuentes institucionales, sin atribuir conformidad ni aprobacion.

## Actualizacion de alcance - 2026-11-18

DEC-047: division iniciada y modelada con S4.3.2.3 Gestion de adicionales y deductivos de obra (tres casos), S4.3.2.7 Gestion de reducciones de prestaciones y S4.3.2.8 Gestion de mayores metrados. El padre presenta ocho hijos de nivel 3. Limite deductivo puro/reduccion pendiente de evidencia; no se atribuye aprobacion institucional. Los nuevos indices y juegos documentales estan enlazados desde S4.3.2.

DEC-048, 2026-11-18: primera mejora de zigzag-controlado, con compactacion de filas por carril manteniendo 16 columnas. S4.3.2.3 reduce 34,2 % la altura del PNG; cinco pruebas correctas, sin aumento de D4. Revision visual general realizada; cruces y enrutamiento pendientes antes de considerar definitivo el perfil.

DEC-049, 2026-11-18: segunda mejora de zigzag-controlado, con corredores que rodean cajas y pools ajenos y recolocacion de cadenas terminales cortas. En S4.3.2.3 las cajas 45-46 suben juntas; D4 baja de 93 a 23, con T1 y T3 en cero. Persisten solapes y etiquetas; no se declara perfil definitivo.
