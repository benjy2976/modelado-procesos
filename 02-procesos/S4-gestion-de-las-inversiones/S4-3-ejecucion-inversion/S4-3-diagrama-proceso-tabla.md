---
id: AP-S4-3-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3
nivel_proceso: 1
proceso:
  - S4.3
fecha_creacion: 2026-10-19
fecha_actualizacion: 2026-11-02
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3
---

# S4.3 Ejecución de la inversión

<!-- Fuente editable del diagrama en la etapa lógica (DEC-025, DEC-026). Genera S4-3-diagrama-proceso.bpmn, .svg, .png y .html con 05-herramientas/gestor-modelos/construir_modelos.py. -->

Sube a: [S4.3 Ejecución de la inversión](00-S4-3-ejecucion-inversion.md)

Propuesta de nivel 1 actualizada por el equipo el 2026-11-02: S4.3 se representa mediante tres subprocesos secuenciales —Inicio de ejecución, Ejecución y Recepción—. La entrada de Adquisiciones se identifica expresamente como el contrato de ejecución de inversión. El detalle de cada subproceso permanece pendiente de análisis.

Clase de cada elemento: `OBS` observado en la ficha aprobada de S4; `EQ` planteamiento del equipo; `PROP` propuesta de modelamiento. Fuentes, diferencias y pendientes en [S4-3-sustento.md](S4-3-sustento.md).

Notas que no se dibujan:

- La denominación S4.3.1 Inicio de ejecución y su alcance detallado están pendientes de análisis; no constituyen una línea base aprobada.
- La ficha aprobada de S4 denomina la entrada de S3.2 como "Servicio contratado / bien adquirido / consultoría y obra contratada". "Contrato de ejecución de inversión" es la especificación propuesta por el equipo para este diagrama.
- La compuerta ubicada antes del fin en el boceto no se incorpora porque solo tiene una entrada y una salida y no representa una decisión, división ni convergencia BPMN.
- Los productos intermedios se representan como objetos de datos de salida del subproceso que los genera; habilitan el subproceso siguiente y su detalle documental debe confirmarse al modelar cada nivel 2.

## Pools

| Pool | Carriles |
|---|---|
| S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Marcador | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| E-1 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | inicio | Inicio | S-1 |  |  |  | PROP | Propuesta del equipo, 2026-11-02 |
| S-1 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso | S4.3.1 Inicio de ejecución | S-2 | sale: Acta de inicio de obra | Detalle pendiente de análisis |  | EQ | Propuesta del equipo, 2026-11-02; ficha S4, páginas impresas 120-121 |
| S-2 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso | S4.3.2 Ejecución | S-3 | sale: Obra concluida o con contrato resuelto | Instancia de larga duración con seis procesos de eventos concurrentes; unidad exacta pendiente |  | EQ | DEC-030; DEC-041 |
| S-3 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso | S4.3.3 Recepción | F-1 [Obra recepcionada] |  | Detalle pendiente de desarrollo posterior |  | EQ | Propuesta del equipo, 2026-11-02; ficha S4, páginas impresas 120-121 |
| F-1 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | fin | Fin |  |  |  |  | PROP | Propuesta del equipo, 2026-11-02 |

## Mensajes

| Desde | Hacia | Nombre | Clase |
|---|---|---|---|
| S4.2 Elaboración del expediente técnico o documento equivalente | S-1 | Expediente técnico o documento equivalente | EQ |
| S3.2 Contratación de bienes y servicios (Adquisiciones) | S-1 | Contrato de ejecución de inversión | EQ |
| S-3 | S4.4 Liquidación, transferencia y cierre de inversión | Información técnico y financiera de liquidación de la inversión | EQ |
