---
id: CON-PROP-BPMN-EVSUB-001
tipo: propuesta
area: 2-8-subprocesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
proceso:
  - S4.3.2
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-03
responsable: equipo-proyecto
confidencialidad: INTERNO
aliases:
  - Paquete de validacion de subprocesos de evento
tags:
  - tema/conocimiento
  - tema/procesos
---

# Conocimientos propuestos sobre subprocesos de evento

Sube a: [2.8 Subprocesos](00-2-8-subprocesos.md)

Este paquete convierte el analisis realizado para S4.3.2 en unidades de conocimiento atomicas, trazables y reutilizables. Todas tienen origen IA y estado `BORRADOR-IA`: pueden usarse para revision o modelamiento exploratorio, pero no constituyen conocimiento validado ni una exigencia institucional aprobada.

## Fuentes y autoridad

| Fuente | Clase | Autoridad para este paquete | Ubicacion principal |
|---|---|---|---|
| `LOC-005`, especificacion BPMN 2.0.2 de OMG | REFERENCIA tecnica primaria | Define semantica y notacion BPMN | Seccion 10.2.5, p. impresa 174; tabla 10.86, pp. 241-244 |
| `LOC-004`, Manual de referencia y guia practica BPMN | REFERENCIA tecnica secundaria | Explica y ejemplifica la notacion | Seccion 2.8.6, pp. PDF 96-98; figuras 2.90 y 2.91 |
| `PROC-001`, NT 002-2025-PCM-SGP | NORMATIVO pendiente de validacion | Regula niveles y documentacion de procesos; recomienda BPMN | Numerales 6.1.2 y 6.1.3, pp. PDF 11-12; glosario p. 22 |
| `DEC-031` | DECISION del proyecto | Define la aplicacion provisional en S4.3.2 | Registro de decisiones del proyecto |

La identificacion, URL, hash y alerta de la especificacion oficial se encuentran en la [guia de BPMN 2.0.2](../../../fuentes/guia-especificacion-bpmn-2-0-2.md). El manual `LOC-004` tiene SHA-256 `9F9504BF6431F9F34AB10BD8876755221A36D46CB8E15D2FF82DBB55FF41CEEA`; la NT `PROC-001`, `16225C398C24D45B601EFEEF20C9E456EF81F0217BBB0A35E8A41BF2F4B60254`.

## Unidades tecnicas propuestas

| ID | Clase | Enunciado atomico propuesto | Fuente y ubicacion |
|---|---|---|---|
| `REF-BPMN-EVSUB-001` | REFERENCIA | Un subproceso de evento se ejecuta dentro del alcance de un proceso o subproceso contenedor; puede iniciarse cada vez que ocurre su disparador mientras ese contenedor permanece activo. | `LOC-005`, sec. 10.2.5, p. impresa 174 / PDF 204; `LOC-004`, sec. 2.8.6, PDF 96-97 |
| `REF-BPMN-EVSUB-002` | REFERENCIA | Un subproceso de evento no forma parte del flujo normal del proceso padre y no debe tener flujos de secuencia entrantes ni salientes. | `LOC-005`, sec. 10.2.5, p. impresa 174 / PDF 204 |
| `REF-BPMN-EVSUB-003` | REFERENCIA | Un subproceso de evento debe tener exactamente un evento de inicio y ese evento debe declarar un disparador. | `LOC-005`, sec. 10.2.5, p. impresa 174 / PDF 204; tabla 10.86, PDF 271 |
| `REF-BPMN-EVSUB-004` | REFERENCIA | Si el evento de inicio es no interruptivo, el proceso contenedor no se cancela y pueden ejecutarse concurrentemente varias instancias del subproceso de evento. | `LOC-005`, tabla 10.87, p. impresa 244 / PDF 274; `LOC-004`, sec. 2.8.6, PDF 96 |
| `REF-BPMN-EVSUB-005` | REFERENCIA | Un subproceso de evento contraido se representa con rectangulo de esquinas redondeadas y borde fino punteado, marcador `+` de colapso y el evento de inicio como marcador en la esquina superior izquierda. | `LOC-005`, sec. 10.2.5, pp. impresas 173-175 / PDF 203-205; `LOC-004`, fig. 2.91, PDF 97 |
| `REF-BPMN-EVSUB-006` | REFERENCIA | Los disparadores de mensaje, temporizador y condicion se reconocen por los marcadores de sobre, reloj y hoja con lineas; un aro discontinuo identifica el inicio no interruptivo. | `LOC-005`, tabla 10.86, pp. impresas 241-243 / PDF 271-273 |
| `REF-BPMN-DES-001` | REFERENCIA | Contraer un subproceso permite reducir la complejidad visual del diagrama superior sin eliminar su detalle interno, que puede revisarse en un nivel de modelamiento mas detallado. | `LOC-005`, sec. 10.2.5, pp. impresas 171-172 / PDF 201-202; `LOC-004`, sec. 2.8, PDF 84-85 |

## Inferencia metodologica propuesta

| ID | Clase | Enunciado | Premisas | Limite |
|---|---|---|---|---|
| `INF-GPP-BPMN-001` | INFERENCIA | La presencia de un subproceso o subproceso de evento en un diagrama BPMN no determina automaticamente la creacion de un proceso formal de nivel inferior en la arquitectura institucional. | BPMN define un objeto de flujo y su semantica; la NT dispone que los dueños determinan los procesos de nivel 1 hasta el ultimo nivel y que los procesos determinados se documentan con ficha e indicador (`REG-GPP-NIV-001`). | Debe validarla el responsable metodologico y el especialista en gestion por procesos; no reemplaza una decision sobre la desagregacion concreta. |

Esta inferencia corrige la lectura demasiado amplia de que todo simbolo de subproceso BPMN equivale necesariamente a un proceso de nivel inferior con ficha propia. Puede existir coincidencia cuando el equipo determina y documenta formalmente ese proceso, pero la equivalencia no nace del simbolo por si solo.

## Aplicacion actual, no generalizable sin revision

En S4.3.2, `DEC-031` aplica provisionalmente `REF-BPMN-EVSUB-001` a `006` para Control periodico, Consultas de obra y Gestionar modificaciones de alcance o plazo. La seleccion concreta de temporizador, mensaje y condicion sigue siendo una propuesta de modelamiento que debe contrastarse con los disparadores operativos reales.

No se propone como conocimiento general que toda ejecucion de inversion deba tener exactamente esos tres bloques, ni que la unidad de instancia sea siempre una inversion. Esos puntos permanecen pendientes de evidencia operativa.

## Resultado de validacion solicitado

| Revision | Responsable funcional | Resultado pendiente |
|---|---|---|
| Correspondencia con la especificacion y el manual | Responsable metodologico BPMN | Confirmar, observar o corregir `REF-BPMN-EVSUB-001` a `006` y `REF-BPMN-DES-001` |
| Interpretacion de niveles y documentos | Especialista en gestion por procesos | Confirmar, observar o corregir `INF-GPP-BPMN-001` y las reglas `REG-GPP-*` relacionadas |
| Aplicacion a S4.3.2 | Dueño o referente operativo del proceso | Confirmar los disparadores, la unidad de instancia y la no interrupcion de cada bloque |

Para cada unidad deben registrarse: resultado, comentario, rol o especialidad, fecha, fuente y hash comprobados. La IA no puede cambiar su estado a `VALIDADO` ni atribuir la revision a una persona.

## Relaciones

- Se sustenta en: [Guia de la especificacion BPMN 2.0.2](../../../fuentes/guia-especificacion-bpmn-2-0-2.md).
- Complementa: [Guia del manual BPMN](../../../fuentes/guia-manual-bpmn.md).
- Se aplica provisionalmente en: [Sustento de S4.3.2](../../../../02-procesos/S4-gestion-de-las-inversiones/S4-3-ejecucion-inversion/S4-3-2-ejecucion/S4-3-2-sustento.md).
- Se rige por: [Protocolo de conocimiento confiable](../../../../00-gobernanza/protocolo-conocimiento-confiable.md).

