---
tipo: decision
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: DECISION
confidencialidad: INTERNO
---

# Registro de decisiones

| ID | Fecha | Decision | Motivo | Impacto | Responsable |
|---|---|---|---|---|---|
| DEC-001 | 2026-10-14 | Adoptar estructura CDE simplificada: WIP, Compartido, Publicado y Archivo. | Integrar el trabajo de procesos con el aprendizaje BIM. | Toda informacion producida tendra estado controlado. | Equipo del proyecto |
| DEC-002 | 2026-10-14 | Usar Git para historial y no duplicar borradores. | Mantener trazabilidad y evitar copias ambiguas. | Los nombres de archivos seran estables. | Equipo del proyecto |
| DEC-003 | 2026-10-14 | Mantener las referencias externas fuera del flujo CDE de autoria. | Son fuentes recibidas, no informacion producida por el equipo. | Se catalogan y conservan como originales inmutables. | Equipo del proyecto |
| DEC-004 | 2026-10-15 | Gestionar con Git LFS los documentos binarios y formatos BIM/CAD; mantener en Git normal las fuentes textuales y BPMN XML. | Evitar inflar el historial ordinario y conservar diferencias legibles en Markdown, CSV, XML y codigo. | PDF, Office, imagenes y modelos binarios se almacenan mediante punteros LFS; cada equipo y remoto debe soportar Git LFS. | Equipo del proyecto |
| DEC-005 | 2026-10-15 | No versionar los binarios descargables de fuentes publicas; versionar su indice, hashes y automatizacion de descarga. | Los recursos publicos son reproducibles y ocuparian innecesariamente el repositorio y la cuota LFS. | Las areas publicas `01-referencias/02` a `08` se restauran localmente con el descargador; Git LFS queda para binarios institucionales o producidos que deban conservarse. | Equipo del proyecto |
| DEC-006 | 2026-10-15 | Sustituir la estructura de carpetas CDE por rutas estables de trabajo y gestionar publicaciones e historicos mediante tags y releases de Git. Esta decision reemplaza DEC-001. | Evitar duplicacion, movimientos de archivos y una segunda capa de versionado incompatible con Git. | Todo el repositorio se considera trabajo vigente; ramas/PR atienden la revision, releases identifican lineas base aprobadas y releases anteriores forman el archivo historico. | Equipo del proyecto |
| DEC-007 | 2026-10-15 | Establecer una cadena obligatoria de fuente, extraccion, regla propuesta, validacion especializada y paquete de contexto para todo conocimiento normativo usado por IA. | Impedir que una extraccion o respuesta plausible se confunda con conocimiento vigente y autorizado. | La IA no puede validar reglas; las lineas base solo pueden sustentarse en reglas trazables y validadas. | Equipo del proyecto |
| DEC-008 | 2026-10-15 | Incorporar como requisito del proyecto un catalogo de reglas y una aplicacion web interna de revision y validacion. | Permitir que el equipo de especialistas produzca conocimiento confiable con segregacion, auditoria y control de impacto. | Los YAML y eventos versionados son fuente maestra; el CSV y la web son vistas e interfaces controladas. | Equipo del proyecto |
| DEC-009 | 2026-10-15 | Adoptar un manual operativo unico para construir, validar y usar conocimiento en analisis, propuestas y modelos. | Aplicar controles proporcionales al tipo de afirmacion y mantener trazabilidad desde la fuente hasta la linea base. | Las afirmaciones se clasifican como normativas, observadas, referencias, inferencias, propuestas o decisiones; cada producto debe superar las puertas de validacion que le correspondan. | Equipo del proyecto |
| DEC-010 | 2026-10-15 | Organizar la boveda mediante un mapa de inicio, mapas de contenido por area y enlaces Markdown relativos. | Hacer explicita la jerarquia y las dependencias sin duplicar archivos ni depender exclusivamente de Obsidian. | Todo Markdown nuevo debe enlazarse desde el mapa de su area; los enlaces cruzados deben expresar una relacion real y verificable. | Equipo del proyecto |
| DEC-011 | 2026-10-15 | Establecer Obsidian como entorno obligatorio de produccion de conocimiento y adoptar un estandar comun de autoria. | Aprovechar propiedades, plantillas, reuniones, tareas, Canvas, Bases, enlaces y busqueda sin perder portabilidad, trazabilidad ni fuentes maestras. | Toda nota nueva debe cumplir el perfil aplicable; Canvas y Bases son vistas; la configuracion compartida se versiona y el estado personal se excluye. | Equipo del proyecto |
