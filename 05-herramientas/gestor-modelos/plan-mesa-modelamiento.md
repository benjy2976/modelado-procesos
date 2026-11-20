---
id: HER-MESA-MODELAMIENTO-PLAN
tipo: propuesta
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
proceso: []
fecha_creacion: 2026-11-20
fecha_actualizacion: 2026-11-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/ia
  - tema/procesos
---

# Plan de la mesa de modelamiento

Sube a: [Gestor local de modelos](00-gestor-modelos.md)

## Objetivo y limites

Construir una aplicacion de revision y modelamiento con interfaz Nuxt/Vue y backend Python. La API web y el futuro servidor MCP consumen los mismos servicios de dominio. El repositorio conserva la autoridad sobre fichas, tabla, sustento, BPMN formal y fuentes. La aplicacion no atribuye validacion normativa ni conformidad institucional.

La organizacion toma como referencia local `C:\Users\72121555.REGIONHUANUCO\Downloads\modelador-bim-main`: modulos por capacidad, acciones y consultas reutilizadas por CLI/API/MCP, contrato OpenAPI para el frontend y Compose para los servicios. Se adapta a la autoridad documental y a la cadena BPMN ya vigentes en este repositorio; no se importan reglas BIM ni se copia su almacén de proyectos.

La tabla estructurada sigue siendo el metodo vigente para convertir instrucciones e ideas en BPMN; no se retira por incorporar un editor grafico. En etapa logica, las ediciones de contenido se hacen sobre la tabla y el sustento, y el BPMN y el HTML se generan mediante `construir_modelos.py`. Antes de cambiar ese metodo se compararan, con el mismo caso, costo de edicion, estabilidad de IDs y fuentes, validacion D1-D5, calidad visual y tiempo de regeneracion frente a editar BPMN directamente. En etapa formal, el estandar actual reconoce el XML BPMN como fuente maestra; la tabla puede seguir como insumo de estructuracion. Los SVG, PNG y PDF siguen siendo derivados bajo demanda. Los HTML actuales permanecen como exportaciones de consulta mientras se migra el visor.

## Componentes

| Componente | Responsabilidad | Fuente que utiliza |
|---|---|---|
| Nuxt/Vue | Arbol, canvas BPMN, formularios, inspector, PDF.js y observaciones | API Python; no escribe archivos directamente |
| Dominio Python | Resolver codigos e IDs, validar operaciones, controlar revisiones, guardar observaciones y preparar cambios | Archivos del repositorio |
| CLI unica | Operaciones para personas, automatizaciones y mantenimiento | Las mismas consultas y acciones del dominio |
| API FastAPI | Contratos HTTP para la interfaz y documentos; misma capa de dominio que MCP | Dominio Python |
| Adaptador MCP Python | Recursos acotados y herramientas con esquemas por operacion | Dominio Python |
| Generador existente | Construccion y controles D1-D5; imagenes solo bajo solicitud | Tabla o BPMN formal segun etapa |

La primera ejecucion es local. La API se enlaza a `127.0.0.1`, sin CORS abierto. Docker monta el repositorio mediante una ruta configurable y publica solo el puerto local. El JSON de observaciones se serializa con un bloqueo de archivo y revision esperada; este mecanismo se limita a procesos que comparten el mismo sistema de archivos y no reemplaza una base de datos. El uso compartido tendra muchos autores de observaciones y **un solo editor activo**; no se planifica coedicion simultanea del modelo. Antes de habilitar acceso remoto se requieren identidad, permisos, almacenamiento transaccional y auditoria de operaciones.

## Organizacion del codigo y migracion

`05-herramientas/gestor-modelos/` es la raiz de la aplicacion de modelamiento. `mesa_modelamiento/` es el paquete Python instalable; `pyproject.toml` y `uv.lock` fijan su entorno. `compose.yaml` arranca la API y permite lanzar el MCP por stdio usando el mismo paquete. Cuando se implemente el frontend se agregaran `frontend/` (Nuxt), `contracts/` (OpenAPI generado y tipos TypeScript) e `infrastructure/` (proxy/configuracion) con archivos reales, sin directorios vacios. El conjunto de `05-herramientas` mantiene otras capacidades documentales que se integraran por etapas a la misma CLI si sus casos de uso lo requieren.

La [documentacion propia de la aplicacion](docs/00-documentacion-aplicacion.md) separa arquitectura, entorno, API, CLI, datos, MCP, convenciones y procedimientos. El 2026-11-20 se recibió el paquete completo de la skill `gestionar-memoria-viva-proyecto` 1.9.0 y se adoptó su estándar portable local; el registro y sus límites están en [la guía de IA](docs/guia_IA.md). Ruff comprueba el paquete Python nuevo; ESLint se configurará al crear el frontend Nuxt real.

El Compose actual monta la raiz del repositorio institucional en `/workspace` y fija `PROCESOS_REPO_ROOT=/workspace`. Asi el codigo de la aplicacion puede leer procesos, gobierno y referencias sin moverlos ahora. La separacion futura de repositorios se hara con montajes y rutas configuradas y probadas, no por una copia implicita de datos al contenedor.

El paquete Python se organiza por capacidad: `procesos` (arbol y localizacion), `modelos` (tabla, BPMN y validacion), `observaciones` (registro y revision), `fuentes` (documentos y anclajes) y `conocimiento` (reglas y sustento). Cada capacidad separara consultas de acciones de escritura cuando ambas existan. `api.py`, `cli.py` y `mcp_adapter.py` son adaptadores delgados: no duplican las reglas. La extraccion solo ocurre al migrar un caso de uso real; no se crean interfaces de repositorio ni carpetas de relleno.

| Codigo vigente | Destino previsto | Transicion segura |
|---|---|---|
| `visor_datos.py` | `mesa_modelamiento/visor_datos.py` y luego modulo `procesos` | El archivo anterior queda como adaptador de compatibilidad para los HTML y pruebas actuales. |
| `modelar.py`, `construir_modelos.py`, `numerar_modelos.py` | Acciones del modulo `modelos` | La CLI unica delega inicialmente a `modelar.py`; se conserva el comando historico hasta igualar sus salidas y controles. |
| `tabla_a_bpmn.py`, validadores D1-D5 y `renderizar_bpmn.py` | Motor del modulo `modelos` | Migrar por funciones probadas, mantener los mismos IDs y perfil; no cambiar el trazado como efecto lateral. |
| `servidor_revision.py`, `visor_revision.js/css` | API Python y frontend Nuxt | Mantener el visor actual hasta que arbol, seleccion, documentos y observaciones tengan paridad. |
| `catalogador-documental/`, `gestionar_etiquetas.py`, `auditar_reproducibilidad.py` | Modulos `fuentes`, `conocimiento` y `mantenimiento` segun cada caso | No mover en bloque: conservar comandos y formatos, extraer servicios reutilizables cuando entren a API o MCP. |

No habra dos rutas de escritura para el mismo recurso: cada mutacion tendra una accion canonica, revision esperada, validacion, escritura atomica y registro de resultado. El XML BPMN no se editara como fuente principal mientras sea derivado de la tabla; los experimentos de edicion directa se haran en una copia aislada. Las notas aprobadas y los originales de referencias permanecen fuera de las operaciones de escritura.

## Contratos y contenedores

- CLI `modelador-procesos`: `arbol`, `proceso <codigo>`, `observaciones listar/agregar`, `modelo <codigo> [--check] [--exportar-imagenes]`, `api` y `mcp`. Las entradas de lectura y observaciones llaman al dominio compartido; `modelo` es un puente temporal al generador vigente.
- HTTP local: `GET /api/arbol`, `GET /api/procesos/{codigo}`, `GET /api/procesos/{codigo}/bpmn` y recurso de observaciones (`GET`, `POST`, `PATCH`). Respuestas de error: `error.code` y `error.message`; las escrituras requieren `revision_esperada` y un desfase responde `409`.
- MCP local por stdio: arbol, proceso, observaciones y registro de observaciones. No expone rutas arbitrarias, aprobacion, validacion normativa ni edicion semantica. El transporte HTTP y el acceso remoto esperan autenticacion y control de hosts.
- Compose inicial: servicio `api` y perfil opcional `mcp`, ambos con la misma imagen Python y el repositorio montado en `/workspace`; puerto API ligado a `127.0.0.1`. El servicio Nuxt y el proxy se agregaran con la primera pantalla funcional. El frontend consumira OpenAPI generado, no tipos escritos a mano.
- Despliegue compartido posterior: Nuxt, API, MCP y proxy independientes; un solo propietario de cada escritura, base de datos transaccional para observaciones multiusuario, identidad/roles y trazabilidad. La generacion de modelos se aislara como trabajo con estado y resultados verificables.

Arranque local desde `05-herramientas/gestor-modelos/`:

```powershell
uv sync --frozen
uv run modelador-procesos arbol
uv run modelador-procesos proceso S4.3.2.3
uv run modelador-procesos api
docker compose up api
```

## Datos y operaciones

- Fichas y sustento: Markdown vigente, respetando campos de anexos NT y la regla de no editar documentos `APROBADO`.
- Modelo logico: `*-diagrama-proceso-tabla.md`; ID de caja y flujo estables.
- Observaciones: conservar inicialmente `<codigo>-observaciones.json` por proceso y el esquema existente. Ampliar de forma compatible para tipo, alcance, respuestas y revision; usar escritura atomica y revision esperada. Cuando exista concurrencia real, migrar el registro operativo a una base de datos y conservar exportaciones auditables.
- Fuentes: identificador de catalogo, hash del documento, pagina fisica, ubicacion, fragmento y coordenadas de los renglones cotejados al enlazar. El visor proyecta esas coordenadas sin buscar texto al abrir el PDF; un hash distinto desactiva el resaltado. Los metadatos de visor no sustituyen el sustento. El [piloto previo a la corrida](docs/metodologia-auditoria-y-observaciones.md) se limita a S4.3.2.7; el MCP OCR local ya fue probado y la preparación documental selectiva queda pendiente.
- Operaciones de edicion: antes de editar se conserva una instantanea verificable del estado actual, incluidos cambios no confirmados en Git, y se crea una copia de trabajo aislada por proceso. CLI, API y MCP pueden editar esa copia mediante las mismas operaciones, sin una aprobacion humana intermedia impuesta por MCP. `preparar_cambio` muestra diff y controles; `aplicar_cambio` puede actualizar la copia o integrar el resultado en la ruta vigente con revision esperada y registro del resultado. Una copia con hallazgos permanece disponible para corregirse; la integracion no borra la version previa. No se exponen rutas fuera de la copia o del proceso correspondiente.

El MCP ofrecera primero lectura de arbol, proceso, caja/flujo, sustento, fuentes y observaciones, ademas de registrar observaciones. Cuando `preparar_cambio` y `aplicar_cambio` tengan pruebas, el agente podra usarlos para editar e integrar cambios sin solicitar una aprobacion por operacion; el usuario controla al agente. Los controles tecnicos preservan la copia anterior, la identidad de cada proceso y la trazabilidad, pero no son una puerta de autorizacion humana del MCP. Los recursos y herramientas no podran declarar `VALIDADO`, `APROBADO` ni conformidades humanas.

### Copia recuperable y comparacion de metodos

La primera sesion de edicion de un proceso capturara una instantanea inmutable de sus maestros y metadatos desde el **arbol de trabajo real**, no solo desde `HEAD`; asi se conserva tambien lo que aun no esta en un commit. La copia editable tendra identificador de sesion, hashes de origen y registro de cambios. Una integracion conserva la instantanea anterior y comprueba si el destino cambio desde que se copio; si cambio, presenta el conflicto sin sustituirlo silenciosamente. El almacenamiento de sesiones sera persistente y separado de `99-temporal/`. El mecanismo concreto se probara con cambios simultaneos y recuperacion antes de habilitar la integracion de E5.

Para E7 se ejecutaran los **mismos tres cambios** en dos copias del piloto: renombrar una actividad con sustento, insertar actividad y flujo, y corregir disposicion/ruta de una flecha. En una copia se editara la tabla y se regenerara; en la otra se usara un editor BPMN sobre XML. Se mediran tiempo de trabajo, numero de operaciones manuales, tamaño y legibilidad del diff, estabilidad de IDs y referencias, resultados D1-D5, calidad visual y tiempo de recuperacion ante error. El editor de [bpmn-js](https://bpmn.io/toolkit/bpmn-js/walkthrough/) admite importar, editar y exportar BPMN XML; esa posibilidad tecnica no demuestra por si sola menor costo para nuestros modelos. La recomendacion final se basara en los resultados y mantendra la tabla como habilidad de estructuracion aunque la edicion grafica resulte conveniente para algunos ajustes.

## Entregas y criterios de aceptacion

La [ruta hacia la revisión por áreas usuarias](docs/ruta-revision-areas-usuarias.md) relaciona estas entregas técnicas con la auditoría de sustento, la atención trazable y las pruebas necesarias para una evaluación guiada local o una apertura compartida. No se declara terminado un corte solo porque exista su código.

Los intervalos siguientes son **cortes funcionales**, no fechas ni autorizaciones para publicar. Cada uno termina con un producto utilizable, pruebas y un registro de limites. La entrega siguiente usa el contrato estable de la anterior. Se trabaja primero con S4.3.2.3, sin alterar su contenido normativo, y despues se prueba la navegacion con S4.3.2.2 y S4.3.1.

| Entrega | Productos verificables | Criterio de cierre | Por que termina aqui | Avance autonomo seguro y decision pendiente |
|---|---|---|---|---|
| **E1. Nucleo Python** (implementada; controles pasados) | Paquete instalable, CLI unica, API, MCP local, `compose.yaml`, lectura de arbol/modelo/BPMN, observaciones con revision y pruebas. | CLI, API y MCP leen el mismo proceso; un conflicto de revision devuelve 409; el chequeo global D1-D5 sigue pasando; visor HTML antiguo funciona. | Fija la identidad de procesos e IDs y un solo lugar para reglas antes de construir otra interfaz. | Contrato OpenAPI versionado, prueba de API/MCP compartidos, Ruff y pruebas locales completados el 2026-11-20. |
| **E2. Mesa de revision** (implementación en curso) | Aplicacion Nuxt/Vue, contrato OpenAPI generado, tipos TS, contenedor frontend y proxy Nitro local, arbol desde Nivel 0, canvas BPMN, zoom con rueda, arrastre, inspector y enlace al proceso hijo solo desde el panel. | Se recorre Nivel 0 → S4 → S4.3 → S4.3.2 → S4.3.2.3 y se vuelve sin pagina en blanco; clic en caja solo selecciona; el limite entre diagrama y panel es legible. | Valida primero navegacion, maquetacion y contrato API sin mezclar problemas documentales o escrituras del modelo. | Código, compilación y rutas de lectura implementados; revisión visual y recorrido interactivo pendientes porque el navegador automatizado local no estuvo disponible en esta sesión. |
| **E3. Evidencia y documentos** (implementación en curso) | Visor Markdown renderizado, PDF.js integrado, API de documentos por identificador permitido, anclajes de página y rectángulos por hash, panel de fuente y cotejo junto al elemento. | Un enlace abre modal; PDF abre la página registrada y resalta solo las coordenadas verificadas al enlazar, sin búsqueda textual durante la lectura; hash distinto o falta de ancla desactiva el resaltado. | La lectura de evidencia es requisito para revisar y corregir cajas; un único modelo pequeño permite probar primero precisión y costo de anclaje. | El visor y contrato se adaptaron a coordenadas; el piloto S4.3.2.7 y la comprobación visual quedan como control de cierre. Las citas faltantes no se completan sin página verificada. |
| **E4. Ciclo de observaciones** (implementado; revisión visual pendiente) | Formularios de observacion para caja, flujo o diagrama; listado, filtro, respuesta, estado e historial; exportacion estructurada para agente; API/MCP con las mismas operaciones permitidas. | Una observacion creada en la interfaz puede leerse por CLI y MCP con ID estable; una revision vieja no pisa otra; cerrar una observacion no cambia el BPMN. | Se obtiene una herramienta de revision util antes de editar el modelo; las observaciones permiten priorizar cambios reales. | Servicio, formularios y contratos locales implementados; pruebas de revisión, historial y compatibilidad con JSON anterior pasan. La interacción visual completa sigue pendiente. |
| **E5. Edicion logica en copia** (implementación en curso) | Sesion con copia verificable del proceso, formularios para tabla, sustento y referencias; diff, revision esperada, regeneracion focalizada, resultados D1-D5 e integracion recuperable. | Una edicion de prueba conserva la version de partida y los IDs, modifica la copia y genera derivados; la integracion deja rastro y permite recuperar el estado anterior. Un documento `APROBADO` y los originales permanecen intactos. | Se aisla la primera escritura del modelo del trabajo vigente; los errores en una copia no destruyen el avance. | Copia, formulario, diff, conflicto e integración de sustento probados. La tabla actual de S4.3.2.3 reproduce hallazgos D3/D4; la herramienta bloquea su integración tras una edición hasta corregirlos. Falta prueba visual y de regeneración exitosa con un modelo piloto sin hallazgos. |
| **E6. Agente de modelamiento** (implementación en curso) | Herramientas MCP para leer caja/flujo/fuente, editar la copia, preparar diff, integrar cambios, regenerar y registrar resultado; esquemas y pruebas de recuperacion. | El agente aplica un cambio piloto mediante MCP sin aprobacion por operacion; la version previa y el diff son recuperables; no se atribuye `VALIDADO` ni `APROBADO`. | La IA usa exactamente las acciones ya probadas por la interfaz; se evita una segunda implementacion de las reglas. | MCP comparte sesiones y lectura de fuentes registradas con API/CLI; pruebas de integración de sustento, conservación del BPMN y extracción acotada de texto pasan. Falta una edición de tabla con regeneración válida en un modelo piloto. |
| **E7. Comparacion y BPMN formal** | Ensayo equivalente tabla→BPMN frente a edicion directa de XML con editor BPMN; mediciones, recomendacion, y solo despues un prototipo de transicion de autoridad y exportaciones. | Se documentan tiempo y pasos, estabilidad de IDs y citas, validacion D1-D5, calidad visual y recuperacion para los mismos cambios. La tabla permanece disponible como metodo de estructuracion. | El editor grafico es una alternativa posible, no una decision tomada; separar el ensayo evita sustituir una metodologia util por intuicion. | **Puedo medir y recomendar en copias.** Cambiar la fuente maestra de un proceso real sigue requiriendo una decision posterior conforme al estandar vigente. |
| **E8. Uso compartido** | Identidad, registro transaccional de observaciones, editor unico con bloqueo de sesion, auditoria, copias de seguridad, proxy y despliegue controlado. | Varios usuarios con acceso registran observaciones concurrentemente; solo un editor modifica el modelo; nadie pierde comentarios o cambios y ningun borrador obtiene conformidad automatica. | El patron muchos observadores/un editor evita construir coedicion en tiempo real innecesaria. | **Puedo diseñar y probar localmente.** El despliegue real aun necesita ubicacion, red, identidad y retencion institucionales. |

**Las decisiones del usuario permiten avanzar hasta E6 en el entorno local**, en secuencia y con una copia recuperable antes de la primera escritura del agente. E7 puede medirse en copias; la transicion real de fuente maestra y el despliegue institucional de E8 quedan para decisiones posteriores. E2-E4 forman el **visor de revision** utilizable. E5-E6 forman el **modelador logico asistido**. No se fijan duraciones en dias hasta medir la primera entrega Nuxt y el inventario real de metadatos de fuentes; las puertas de cierre son comportamientos comprobables, no tiempo transcurrido.

## Decisiones predeterminadas para trabajo desatendido

Estas son propuestas operativas, no validaciones institucionales. El usuario puede cambiarlas antes o durante una entrega; si no las cambia, se aplican a los trabajos tecnicos ya autorizados.

| Clave | Decision predeterminada | Consecuencia |
|---|---|---|
| D-A | Piloto S4.3.2.3; S4.3.2.2 y S4.3.1 para probar arbol y enlaces. | Permite comprobar un caso complejo con fuentes registradas y dos procesos vecinos. |
| D-B | Nuxt/Vue/TypeScript con componentes reutilizables, contraste accesible y layout de tres zonas: arbol, canvas, inspector. | La caja selecciona; la navegacion al hijo se inicia solo en el inspector. |
| D-C | Uso local en `127.0.0.1` durante E2-E6; el acceso compartido se prepara, pero no se publica todavia. | Permite desarrollar sin simular identidad ni seguridad multiusuario inexistentes. |
| D-D | Observaciones en JSON compatible con el visor actual durante el piloto local; para uso compartido se migran a almacenamiento transaccional. | Varios observadores podran registrar comentarios sin disputar la unica sesion de edicion. |
| D-E | Los PDF y Markdown se leen desde rutas registradas y permitidas; no se exponen rutas arbitrarias. | La evidencia se abre en visor propio con pagina exacta; un fragmento no verificado no se resalta. |
| D-F | El agente puede preparar y aplicar cambios en la copia mediante MCP cuando E5-E6 esten probadas; el MCP no impone aprobacion humana por operacion. | El usuario dirige al agente; la aplicacion conserva versiones, revisiones y resultados tecnicos. |
| D-G | No crear commits ni publicar, aprobar o desplegar fuera de la maquina local como efecto automatico de un formulario o herramienta MCP. | Los cambios quedan revisables en Git y las decisiones institucionales siguen siendo humanas. |
| D-H | **Decidida:** conservar instantanea verificable del estado actual y editar una copia aislada antes de integrar; el agente puede corregir libremente esa copia. | El avance previo, incluso no confirmado en Git, queda recuperable. La copia no se guarda unicamente en `99-temporal/`, que se trata como regenerable. |
| D-I | **Decidida:** el agente puede aplicar e integrar cambios mediante MCP sin una autorizacion adicional por cada operacion. | La CLI, API y MCP invocan las mismas acciones; se conserva version previa, diff, revision y reporte de validacion. No se atribuye conformidad institucional. |
| D-J | **Decidida en cuanto al metodo:** la tabla continua como herramienta de estructuracion. **Pendiente:** medir tabla/regeneracion frente a edicion directa del BPMN antes de cambiar el flujo formal o declarar otra fuente maestra. | Una capacidad grafica nueva no elimina el metodo de modelamiento ni crea dos fuentes maestras simultaneas. |
| D-K | **Decidida en cuanto al uso:** todos los usuarios con acceso pueden registrar observaciones; solo uno edita el modelo a la vez, sin coedicion en tiempo real. **Pendiente para despliegue:** identidad, red, ubicacion, respaldo y retencion. | El almacenamiento compartido debe aceptar observaciones concurrentes y bloquear una segunda sesion de edicion. |

Con estas decisiones, el tramo tecnico puede ejecutarse desde E1 hasta E6 en local, respetando sus criterios de cierre y sin pedir permiso por cada accion del MCP. La comparacion de E7 tambien puede hacerse sobre copias. La transicion de un proceso real a fuente BPMN y el despliegue compartido se deciden cuando existan resultados medidos y un entorno institucional definido. Si una afirmacion normativa no esta sustentada, se registra `EVIDENCIA-INSUFICIENTE` y se continua con componentes independientes. Una entrega se cierra solo cuando cumple sus criterios; no se declara completa por tiempo o por haber generado archivos.

## Estado de la primera entrega

`mesa_modelamiento/` contiene el repositorio de procesos, el servicio de observaciones y los adaptadores CLI, FastAPI y MCP. `compose.yaml` arranca API y frontend con el repositorio montado. OpenAPI se genera desde FastAPI y se comprueba con `modelador-procesos contrato --check`; la primera pantalla Nuxt consume tipos generados desde ese contrato. E1 no habilita formularios que modifiquen fichas, tablas o sustento. El cierre visual de E2 se verifica por separado.
