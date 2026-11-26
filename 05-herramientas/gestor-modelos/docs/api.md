---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
---

# Contrato HTTP local

La API FastAPI de `mesa_modelamiento/api.py` expone consultas, observaciones y sesiones de edición recuperables. Es un contrato de desarrollo sin autenticación. El puerto de la API se publica solo en `127.0.0.1`; el acceso remoto solo se admite a través del frontend detrás de un proxy inverso con control de acceso, según [Entorno](entorno.md).

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

| Método y ruta | Tipo y propietario | Efecto |
|---|---|---|
| `GET /api/salud` | Consulta técnica, aplicación | Estado `ok` |
| `GET /api/arbol` | Proyección, procesos | Árbol desde Nivel 0 |
| `GET /api/procesos/{codigo}` | Consulta, procesos | Datos de tabla y revisión |
| `GET /api/procesos/{codigo}/bpmn` | Documento derivado, procesos | XML BPMN en línea |
| `GET /api/procesos/{codigo}/observaciones` | Colección, observaciones | Registros y revisión vigente |
| `POST /api/procesos/{codigo}/observaciones` | Creación, observaciones | Nueva observación o comentario |
| `PATCH /api/procesos/{codigo}/observaciones/{identificador}` | Cambio de estado, observaciones | `ABIERTA` o `RESUELTA` |

Las escrituras exigen `revision_esperada`; una revisión antigua devuelve `409`. `POST` admite `elemento`, `referencia`, `texto`, `autor` y `tipo`; `PATCH` admite `estado`. Los errores de dominio usan `{"error":{"code":...,"message":...}}`. El código NT limita el acceso a carpetas de proceso y no hay un endpoint para archivos arbitrarios. La implementación comprueba el origen en mutaciones, pero esta comprobación no sustituye identidad ni permisos.

`/openapi.json` es generado por FastAPI en ejecución y se conserva como [snapshot versionado](../contracts/openapi.json). `modelador-procesos contrato --check` detecta deriva; el frontend generará sus tipos a partir de ese JSON.

## Endpoints

Las rutas son locales y no incluyen autenticación. Las mutaciones verifican `Origin` cuando el cliente lo envía; esta medida no identifica usuarios. La implementación registrada en `mesa_modelamiento/api.py` es la evidencia del inventario.

| Método | Ruta | Acceso | Tipo | Rol | Ciclo | Recurso o concepto | Módulo propietario | Ruta canónica | Propósito | Decisión |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GET | /api/salud | public | consulta | canonica | sin ciclo | salud | mesa_modelamiento | /api/salud | Comprobar respuesta del servicio | Consulta técnica |
| GET | /api/arbol | public | proyeccion | canonica | derivado | árbol de procesos | mesa_modelamiento | /api/arbol | Leer jerarquía NT | Vista del repositorio institucional |
| GET | /api/procesos/{codigo} | public | recurso | canonica | externo | proceso | mesa_modelamiento | /api/procesos | Leer tabla y revisión del proceso | El proceso pertenece al repositorio institucional |
| GET | /api/procesos/{codigo}/bpmn | public | subrecurso | canonica | derivado | BPMN | mesa_modelamiento | /api/procesos | Leer XML BPMN disponible | Documento derivado del proceso |
| GET | /api/procesos/{codigo}/documentos/{tipo} | public | subrecurso | canonica | externo | documento del proceso | mesa_modelamiento | /api/procesos | Leer tabla o sustento Markdown en línea | `tipo` solo admite `tabla` y `sustento` |
| GET | /api/procesos/{codigo}/fuentes/{ref}/{indice} | public | subrecurso | contextual | externo | fuente registrada | mesa_modelamiento | /api/procesos | Leer fuente autorizada por caja e índice | El proceso y su metadata determinan el archivo; no se recibe una ruta arbitraria |
| GET | /api/procesos/{codigo}/fuentes/{ref}/{indice}/lectura | public | consulta | contextual | derivado | lectura de fuente | mesa_modelamiento | /api/procesos/{codigo}/fuentes | Extraer texto de fuente y página registrada | PDF sin página o sin texto se declara pendiente; no se aplica OCR |
| GET | /api/procesos/{codigo}/observaciones | public | recurso | canonica | propio | observación | mesa_modelamiento | /api/procesos/{codigo}/observaciones | Listar comentarios del proceso | El JSON local es autoridad de observaciones |
| POST | /api/procesos/{codigo}/observaciones | public | recurso | canonica | propio | observación | mesa_modelamiento | /api/procesos/{codigo}/observaciones | Crear observación | Requiere revisión esperada |
| POST | /api/procesos/{codigo}/observaciones/{identificador}/respuestas | public | subrecurso | contextual | propio | respuesta de observación | mesa_modelamiento | /api/procesos/{codigo}/observaciones | Responder una observación | La observación es la autoridad del historial; requiere revisión esperada |
| PATCH | /api/procesos/{codigo}/observaciones/{identificador} | public | recurso | canonica | propio | observación | mesa_modelamiento | /api/procesos/{codigo}/observaciones | Cambiar estado de observación | Requiere revisión esperada |
| POST | /api/procesos/{codigo}/sesiones | public | recurso | canonica | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Capturar instantánea y abrir copia con titular, motivo y modo `EDICION` o `BORRADOR` | `EDICION` toma el bloqueo del proceso (409 con titular y vencimiento si otro lo tiene); `BORRADOR` no bloquea (`DEC-069`) |
| GET | /api/procesos/{codigo}/bizagi | public | subrecurso | contextual | propio | exportación BPMN | mesa_modelamiento | /api/procesos/{codigo}/bpmn | BPMN vigente en el dialecto de Bizagi Modeler, generado al momento (`DEC-025`) | Solo lectura; no escribe archivos |
| GET | /api/procesos/{codigo}/versiones/{numero}/bizagi | public | subrecurso | contextual | propio | exportación BPMN | mesa_modelamiento | /api/procesos/{codigo}/versiones | BPMN de una versión en el dialecto de Bizagi | Solo lectura |
| GET | /api/observaciones/abiertas | public | consulta | contextual | propio | observación | mesa_modelamiento | /api/procesos/{codigo}/observaciones | Observaciones ABIERTAS por proceso para los contadores del árbol | Omite los procesos sin abiertas; un archivo ilegible se omite |
| GET | /api/procesos/{codigo}/edicion | public | consulta | contextual | propio | estado de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Estado `LIBRE`, `EN-EDICION` o `APROBADO`, bloqueo, borradores abiertos y `huella` del contenido (cambia al cambiar tabla, sustento, fuentes o BPMN) | Un bloqueo vencido se suelta al consultarlo y su sesión queda `VENCIDA` |
| GET | /api/procesos/{codigo}/versiones | public | consulta | contextual | propio | versión de modelo | mesa_modelamiento | /api/procesos/{codigo}/versiones | Versiones integradas, la más reciente primero, con conteo de cambios | Solo lectura; el registro vive fuera de Git |
| GET | /api/procesos/{codigo}/versiones/{numero} | public | recurso | canonica | propio | versión de modelo | mesa_modelamiento | /api/procesos/{codigo}/versiones | Cambio por caja y diff de tabla y sustento | 404 si la versión o su sesión no existen |
| GET | /api/procesos/{codigo}/versiones/{numero}/bpmn | public | subrecurso | contextual | propio | versión de modelo | mesa_modelamiento | /api/procesos/{codigo}/versiones | BPMN tal como quedó integrado | XML de la copia de la sesión |
| POST | /api/procesos/{codigo}/edicion/liberacion | public | accion | contextual | propio | estado de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Una persona libera el bloqueo con autor y motivo | La sesión queda `LIBERADA` con autor y motivo; no borra la copia |
| GET | /api/procesos/{codigo}/sesiones/activa | public | consulta | contextual | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Reanudar la sesión titular del bloqueo | Devuelve `null` si no existe o venció |
| GET | /api/procesos/{codigo}/sesiones/{identificador} | public | recurso | canonica | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Leer manifiesto y preparación | Solo el código e ID correspondientes |
| GET | /api/procesos/{codigo}/sesiones/{identificador}/documentos/{nombre} | public | subrecurso | contextual | propio | documento de copia | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Leer tabla, sustento o fuentes en copia | Nombres permitidos, sin ruta arbitraria |
| PUT | /api/procesos/{codigo}/sesiones/{identificador}/documentos/{nombre} | public | subrecurso | contextual | propio | documento de copia | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Editar copia por revisión esperada | Nunca edita documento aprobado |
| POST | /api/procesos/{codigo}/sesiones/{identificador}/preparacion | public | subrecurso | contextual | propio | preparación de sesión | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Regenerar copia, validar y calcular diff | No integra si hay hallazgos |
| POST | /api/procesos/{codigo}/sesiones/{identificador}/integracion | public | accion | contextual | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Integrar cambios preparados | Revisión de sesión y hashes de destino |
| POST | /api/procesos/{codigo}/sesiones/{identificador}/cierre | public | accion | contextual | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Cerrar sin integrar y liberar el bloqueo si lo tenía | Conserva instantánea y copia |
| POST | /api/procesos/{codigo}/observaciones/{identificador}/definicion | public | accion | contextual | propio | definición de resolución | mesa_modelamiento | /api/procesos/{codigo}/observaciones | Registrar la definición de una persona | `DEC-065`; rechaza el alias del agente; encola la aplicación (`DEC-068`) |
| GET | /api/observaciones/etapas | public | consulta | canonica | propio | observación | mesa_modelamiento | /api/observaciones/etapas | Listar observaciones por etapa en un proceso o en el árbol | `DEC-065`; resumen por defecto |
| POST | /api/procesos/{codigo}/observaciones/{identificador}/solicitud-analisis | public | accion | contextual | propio | trabajo de análisis | mesa_modelamiento | /api/procesos/{codigo}/observaciones | Encolar el análisis de la observación por el agente y despertarlo | `DEC-068`; responde 202; reanálisis en PROPUESTA exige nota |
| GET | /api/procesos/{codigo}/trabajos | public | consulta | contextual | propio | trabajo de agente | mesa_modelamiento | /api/trabajos | Listar trabajos del proceso | Estado operativo fuera de Git (`DEC-068`) |
| GET | /api/trabajos | public | recurso | canonica | propio | trabajo de agente | mesa_modelamiento | /api/trabajos | Listar la cola de trabajos con filtros | Solo lectura; tomar y completar son del agente por MCP |
| GET | /api/chat/estado | public | consulta | canonica | sin ciclo | chat con el agente | mesa_modelamiento | /api/chat/estado | Saber si el relevo está configurado | No expone URL ni token |
| POST | /api/procesos/{codigo}/chat | public | accion | contextual | sin ciclo | turno de chat | mesa_modelamiento | /api/procesos/{codigo}/chat | Enviar un turno al agente `mesa-chat` y recibir la respuesta en SSE | `DEC-068`; 503 sin relevo; el agente prepara y no aplica |

## Matriz de aplicabilidad CRUD

| Recurso o concepto | List | Create | Get | Update | Delete | Fuente de justificación |
| --- | --- | --- | --- | --- | --- | --- |
| proceso | no aplica: el árbol es una proyección | no permitida: se modela en la tabla institucional | aplica | aplica | no permitida: no existe operación de borrado | Actualización solo mediante sesión y preparación válida en `sesiones.py` |
| observación | aplica | aplica | no aplica: se entrega dentro de la colección | aplica | no permitida: se conservan observaciones y se cambia su estado | `observaciones.py` y `api.py` |
| respuesta de observación | no aplica: se entrega dentro de la observación | aplica | no aplica: se entrega dentro de la observación | no permitida: se conserva el historial | no permitida: se conserva el historial | `observaciones.py` y `api.py` |
| sesión de edición | no aplica: se consulta la activa por proceso | aplica | aplica | aplica | no permitida: se conserva el historial | Actualización por documentos, preparación, integración o cierre en `sesiones.py` |
| trabajo de agente | aplica | aplica | no aplica: se entrega en la colección | no permitida: lo toma y completa el agente por MCP o CLI | no permitida: se conserva con su historial | `trabajos.py`, `resolucion.py` y `api.py` (`DEC-068`) |
| documento de copia | no aplica: se consulta por nombre permitido | no aplica: se captura al iniciar sesión | aplica | aplica | no permitida: se conserva la copia | `sesiones.py`: tabla, sustento y fuentes con revisión de hash |
| preparación de sesión | no aplica: una preparación vigente por sesión | aplica | aplica | aplica | no permitida: la instantánea se conserva | Se lee dentro del manifiesto; `sesiones.py` regenera y actualiza diff y validación |
| lectura de fuente | no aplica: se consulta una entrada registrada | no permitida: es proyección de archivo | aplica | no permitida: no altera el documento | no permitida: no altera el documento | `documentos.py` limita a página registrada y devuelve hash y estado |

El servicio FastAPI registra estas rutas directamente en `app`; no hay routers anidados ni prefijos externos en el Compose actual. `GET /api/procesos/{codigo}/bpmn` devuelve XML en línea. El `POST` devuelve `201`; las lecturas y el `PATCH`, `200` en éxito. Los conflictos de revisión devuelven `409` mediante `ErrorDominio`. La validación automática de acceso no infiere la semántica de `comprobar_origen`; la revisión manual anterior no equivale a autenticación.

`GET /api/procesos/{codigo}/documentos/{tipo}` sirve únicamente la tabla o el sustento del mismo proceso como Markdown en línea. `GET /api/procesos/{codigo}/fuentes/{ref}/{indice}` resuelve la fuente desde `fuentes_visor` ya validado por `datos_visor`; `ref` e `indice` identifican una entrada registrada, no una ruta elegida por el cliente. Los faltantes devuelven `404`. El PDF se entrega como `application/pdf` en línea para PDF.js; las otras fuentes admitidas se presentan como texto. El detalle del modelo incluye `rectangulos`, `tramos` (página, rol `citado` o `antecedente` y rectángulos, para referencias de varias páginas) y `estado_ancla` por referencia; si el hash difiere, la API no entrega coordenadas para resaltar.

`POST /api/procesos/{codigo}/observaciones/{identificador}/definicion` registra la definición de una persona (`OPCION`, `OPCIONES`, `MANUAL` o `VINCULADA`) con revisión esperada; rechaza el alias del agente. `GET /api/observaciones/etapas?etapa=&codigo=` lista observaciones por etapa de resolución con su conteo. Las observaciones devuelven `etapa`, `resolucion` y `resoluciones_anteriores` cuando existen.

`POST .../observaciones/{identificador}/solicitud-analisis` recibe `{"autor", "nota"}`, encola un trabajo `ANALISIS` (sin duplicar uno activo) y responde `202` con el trabajo. Se admite en las etapas REGISTRADA, EN-ANALISIS y PROPUESTA; en PROPUESTA la nota (motivo del reanálisis) es obligatoria. Definir una resolución encola un trabajo `APLICACION` y devuelve su resumen en `trabajo`. `POST /api/procesos/{codigo}/chat` recibe `{"conversacion", "mensaje", "contexto"}`, antepone un bloque de contexto marcado como datos y retransmite el flujo SSE del relevo; la API solo conoce `MESA_RELEVO_URL` y `MESA_RELEVO_TOKEN`, nunca el token del Gateway.

`POST .../sesiones/{identificador}/preparacion` acepta un cuerpo opcional `{"aceptar_hallazgos": "..."}` con la justificación para adoptar hallazgos ya documentados en el sustento de la copia; la respuesta incluye `numeracion` y `hallazgos_aceptados` cuando corresponden.

La creación y la respuesta aceptan `formato`: `texto` (por defecto, hasta 4000 caracteres) o `html` (hasta 20000 caracteres de marcado y 4000 de texto visible). El HTML se guarda saneado por `contenido_enriquecido.py` con una lista blanca de etiquetas sin atributos: `h3`, `h4`, `p`, `br`, `strong`, `b`, `em`, `i`, `u`, `s`, `del`, `ul`, `ol`, `li` y `blockquote`. Los registros anteriores sin `formato` se leen como texto.

`POST /api/procesos/{codigo}/observaciones/{identificador}/respuestas` añade texto, autor declarado, fecha e historial de la observación y responde `201`. `PATCH` cambia solo entre `ABIERTA` y `RESUELTA`; si el estado ya coincide, devuelve el registro sin crear otro evento. Los cambios conservan revisión esperada y devuelven `409` ante desfase. `autor` no prueba identidad: el uso compartido exige autenticación antes de exposición remota.

La lectura de fuente entrega ruta registrada, SHA-256, metadatos, estado de extracción y hasta 12 000 caracteres. Para PDF extrae solo la página física registrada; sin página devuelve `PAGINA_NO_REGISTRADA` y sin texto devuelve `SIN_TEXTO_EXTRAIBLE`. No ejecuta OCR ni inventa un fragmento. `coincidencia_fragmento` indica una coincidencia textual simple y no valida el fundamento normativo.
