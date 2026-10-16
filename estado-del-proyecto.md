---
tipo: estado-proyecto
area: proyecto
estado_documento: VIGENTE
clase_conocimiento: OBSERVADO
fecha_actualizacion: 2026-10-16
confidencialidad: INTERNO
tags:
  - tema/gobernanza
---

# Estado del proyecto

- Fecha de actualizacion: 2026-10-16
- Fase: estructura centrada en procesos implementada (`DEC-017`); traduccion S4 lista para revision humana de fidelidad; S4.3 a la espera de insumos para elaborar su ficha
- Ambito inicial: S4.3 Ejecucion de la inversion
- Estado de los procesos: mapa Nivel 0 y ficha S4 confirmados como lineas base institucionales aprobadas; la nota S4 se dividio en ficha de producto y proceso, fichas de indicador y sustento, pendientes de conformidad humana de fidelidad; S4.3 delimitado (`DEC-020`) con modelo logico y ficha borrador en `ELABORACION` a partir de la propuesta del equipo; 9 guias de lectura de fuentes y 24 reglas `BORRADOR-IA` pendientes de validacion humana; TO-BE pendiente para una etapa posterior
- Estado BIM: aprendizaje y adopcion progresiva; la informacion se organizara con rutas estables y trazabilidad Git, sin declarar el repositorio como CDE institucional
- Descargas: lote base oficial de 219 archivos completado y evaluado tecnicamente
- Git: estrategia hibrida configurada; repositorio inicial publicado en remoto, recursos publicos regenerables fuera de Git y LFS reservado para binarios no reproducibles
- Obsidian: boveda independiente operativa mediante CLI; notas indice `00-<nombre>.md` en lugar de `README.md`, navegacion `Sube a:` hacia el indice inmediato y grupos de color comunes del grafo (`DEC-018`); entrada `00-GESTION-POR-PROCESOS-GRH.md`, mayusculas en tres niveles, etiquetas controladas `tema/` y `proceso/`, nodos de referencia, actores e interacciones enlazadas para la vista del modelo de procesos (`DEC-019`); estandar obligatorio de autoria, mapas, propiedades, plantillas, reuniones, Canvas y Bases definidos; estado visual excluido de Git
- Conocimiento: manual operativo y protocolo obligatorio definidos; catalogo, plantillas y requisitos del validador web preparados; implementacion pendiente
- Reproducibilidad: dependencias fijadas, auditor automatizado aprobado, `origin` sincronizado y cuatro objetos LFS recuperados e integros; falta validar la clonacion completa desde otro equipo
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

Revisar con el equipo la fidelidad de la ficha, las fichas de indicador y el diagrama de S4 contra el PDF aprobado y registrar la conformidad en su sustento. En paralelo, recibir los levantamientos del equipo y el documento interno para elaborar fichas, registrarlos en el sustento de S4.3 y elaborar la ficha de producto y proceso de S4.3.
