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
| POST | /api/procesos/{codigo}/sesiones | public | recurso | canonica | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Capturar instantánea y abrir copia | Una sesión activa por proceso |
| GET | /api/procesos/{codigo}/sesiones/activa | public | consulta | contextual | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Reanudar sesión activa | Devuelve `null` si no existe |
| GET | /api/procesos/{codigo}/sesiones/{identificador} | public | recurso | canonica | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Leer manifiesto y preparación | Solo el código e ID correspondientes |
| GET | /api/procesos/{codigo}/sesiones/{identificador}/documentos/{nombre} | public | subrecurso | contextual | propio | documento de copia | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Leer tabla, sustento o fuentes en copia | Nombres permitidos, sin ruta arbitraria |
| PUT | /api/procesos/{codigo}/sesiones/{identificador}/documentos/{nombre} | public | subrecurso | contextual | propio | documento de copia | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Editar copia por revisión esperada | Nunca edita documento aprobado |
| POST | /api/procesos/{codigo}/sesiones/{identificador}/preparacion | public | subrecurso | contextual | propio | preparación de sesión | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Regenerar copia, validar y calcular diff | No integra si hay hallazgos |
| POST | /api/procesos/{codigo}/sesiones/{identificador}/integracion | public | accion | contextual | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Integrar cambios preparados | Revisión de sesión y hashes de destino |
| POST | /api/procesos/{codigo}/sesiones/{identificador}/cierre | public | accion | contextual | propio | sesión de edición | mesa_modelamiento | /api/procesos/{codigo}/sesiones | Liberar editor sin integrar | Conserva instantánea y copia |

## Matriz de aplicabilidad CRUD

| Recurso o concepto | List | Create | Get | Update | Delete | Fuente de justificación |
| --- | --- | --- | --- | --- | --- | --- |
| proceso | no aplica: el árbol es una proyección | no permitida: se modela en la tabla institucional | aplica | aplica | no permitida: no existe operación de borrado | Actualización solo mediante sesión y preparación válida en `sesiones.py` |
| observación | aplica | aplica | no aplica: se entrega dentro de la colección | aplica | no permitida: se conservan observaciones y se cambia su estado | `observaciones.py` y `api.py` |
| respuesta de observación | no aplica: se entrega dentro de la observación | aplica | no aplica: se entrega dentro de la observación | no permitida: se conserva el historial | no permitida: se conserva el historial | `observaciones.py` y `api.py` |
| sesión de edición | no aplica: se consulta la activa por proceso | aplica | aplica | aplica | no permitida: se conserva el historial | Actualización por documentos, preparación, integración o cierre en `sesiones.py` |
| documento de copia | no aplica: se consulta por nombre permitido | no aplica: se captura al iniciar sesión | aplica | aplica | no permitida: se conserva la copia | `sesiones.py`: tabla, sustento y fuentes con revisión de hash |
| preparación de sesión | no aplica: una preparación vigente por sesión | aplica | aplica | aplica | no permitida: la instantánea se conserva | Se lee dentro del manifiesto; `sesiones.py` regenera y actualiza diff y validación |
| lectura de fuente | no aplica: se consulta una entrada registrada | no permitida: es proyección de archivo | aplica | no permitida: no altera el documento | no permitida: no altera el documento | `documentos.py` limita a página registrada y devuelve hash y estado |

El servicio FastAPI registra estas rutas directamente en `app`; no hay routers anidados ni prefijos externos en el Compose actual. `GET /api/procesos/{codigo}/bpmn` devuelve XML en línea. El `POST` devuelve `201`; las lecturas y el `PATCH`, `200` en éxito. Los conflictos de revisión devuelven `409` mediante `ErrorDominio`. La validación automática de acceso no infiere la semántica de `comprobar_origen`; la revisión manual anterior no equivale a autenticación.

`GET /api/procesos/{codigo}/documentos/{tipo}` sirve únicamente la tabla o el sustento del mismo proceso como Markdown en línea. `GET /api/procesos/{codigo}/fuentes/{ref}/{indice}` resuelve la fuente desde `fuentes_visor` ya validado por `datos_visor`; `ref` e `indice` identifican una entrada registrada, no una ruta elegida por el cliente. Los faltantes devuelven `404`. El PDF se entrega como `application/pdf` en línea para PDF.js; las otras fuentes admitidas se presentan como texto. El detalle del modelo incluye `rectangulos`, `tramos` (página, rol `citado` o `antecedente` y rectángulos, para referencias de varias páginas) y `estado_ancla` por referencia; si el hash difiere, la API no entrega coordenadas para resaltar.

`POST /api/procesos/{codigo}/observaciones/{identificador}/respuestas` añade texto, autor declarado, fecha e historial de la observación y responde `201`. `PATCH` cambia solo entre `ABIERTA` y `RESUELTA`; si el estado ya coincide, devuelve el registro sin crear otro evento. Los cambios conservan revisión esperada y devuelven `409` ante desfase. `autor` no prueba identidad: el uso compartido exige autenticación antes de exposición remota.

La lectura de fuente entrega ruta registrada, SHA-256, metadatos, estado de extracción y hasta 12 000 caracteres. Para PDF extrae solo la página física registrada; sin página devuelve `PAGINA_NO_REGISTRADA` y sin texto devuelve `SIN_TEXTO_EXTRAIBLE`. No ejecuta OCR ni inventa un fragmento. `coincidencia_fragmento` indica una coincidencia textual simple y no valida el fundamento normativo.
