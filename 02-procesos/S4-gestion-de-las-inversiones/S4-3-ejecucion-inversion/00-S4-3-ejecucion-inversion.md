---
tipo: mapa-de-contenido
area: S4-3-ejecucion-inversion
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
codigo_proceso: S4.3
nivel_proceso: 1
proceso_padre: S4
alcance_proyecto: EN-ALCANCE
aliases:
  - S4.3 Ejecucion de la inversion
tags:
  - tema/procesos
  - proceso/s4/s4-3
---

# S4.3 Ejecucion de la inversion

Sube a: [S4 Gestion de las inversiones](../00-S4-gestion-de-las-inversiones.md)

Proceso en alcance del proyecto. Aun no cuenta con documentacion NT propia: su primer producto es la ficha de producto y proceso, que debe elaborarse y recorrer el circuito de revision.

## Ubicacion

Mapa de procesos institucional > S4 Gestion de las inversiones > **S4.3** (Nivel 1).

## Lo que ya se conoce

Datos observados en la [ficha aprobada de S4](../S4-ficha-producto-proceso.md); su detalle y clasificacion estan en el [sustento de S4.3](S4-3-sustento.md).

- **Responsable consignado:** Sub Gerencia de Gestion de Obras y Supervision; unidades ejecutoras que pertenecen al GRH.

## Interacciones

Entradas y productos de S4.3 tal como figuran en la ficha aprobada de S4 (paginas impresas 120-121). Cada contraparte enlaza a su nodo de proceso o actor.

| Sentido | Contraparte | Elemento observado |
|---|---|---|
| Entrada | [S4.2 Elaboracion del expediente tecnico](../S4-2-elaboracion-del-expediente-tecnico/00-S4-2-elaboracion-del-expediente-tecnico.md) | Expediente tecnico, documento equivalente aprobado y/o EETT |
| Entrada | [Gobiernos Nacional, Regional y Local](../../../03-conocimiento/actores-y-roles/gobiernos-nacional-regional-y-local.md) | Convenios |
| Entrada | [S3.2 Contratacion de bienes y servicios](../../S3-gestion-de-bienes-y-servicios/S3-2-contratacion-de-bienes-y-servicios/00-S3-2-contratacion-de-bienes-y-servicios.md) | Servicio contratado / bien adquirido / consultoria y obra contratada |
| Salida | [S3.1 Programacion de bienes y servicios](../../S3-gestion-de-bienes-y-servicios/S3-1-programacion-de-bienes-y-servicios/00-S3-1-programacion-de-bienes-y-servicios.md) | Designacion de personal y/o requerimiento de contratacion de consultoria de obra/bienes y servicios |
| Salida | [MEF / INFOBRAS](../../../03-conocimiento/actores-y-roles/mef-infobras.md) | Reporte de inversiones ejecutadas |
| Salida | [S2.1 Gestion Contable](../../S2-gestion-contable-y-financiera/S2-1-gestion-contable/00-S2-1-gestion-contable.md) | Expediente para pagos |
| Salida | [S4.4 Liquidacion, transferencia y cierre de inversion](../S4-4-liquidacion-transferencia-y-cierre/00-S4-4-liquidacion-transferencia-y-cierre.md) | Informacion tecnico y financiero para liquidacion ET |
| Salida | [S4.2 Elaboracion del expediente tecnico](../S4-2-elaboracion-del-expediente-tecnico/00-S4-2-elaboracion-del-expediente-tecnico.md) | Informe de estado situacional del Proyecto/programa o IOARR por saldo de obra |

## Documentos del proceso

| Documento | Archivo | Estado |
|---|---|---|
| Ficha de producto y proceso | [S4-3-ficha-producto-proceso.md](S4-3-ficha-producto-proceso.md) | `PROPUESTA` en `ELABORACION`: primer borrador; dueno y objetivo pendientes |
| Fichas de indicador | `S4-3-fichas-indicador.md` | `PENDIENTE` |
| Diagrama del proceso | [S4-3-diagrama-proceso-logico.puml](S4-3-diagrama-proceso-logico.puml) y su [SVG](S4-3-diagrama-proceso-logico.svg); luego `S4-3-diagrama-proceso.bpmn` | `PROPUESTA` en `ELABORACION`: modelo logico |
| Sustento | [S4-3-sustento.md](S4-3-sustento.md) | Vigente |
| Procedimiento | - | Se determinara al aprobar la descomposicion: solo aplica en el ultimo nivel |

## Subprocesos Nivel 2

Propuestos en `DEC-023` y `DEC-024`, pendientes de aprobar con la descomposicion de S4.3:

| Codigo | Subproceso | Instancia | Estado |
|---|---|---|---|
| S4.3.1 | [Gestion de la ejecucion](S4-3-1-gestion-de-la-ejecucion/00-S4-3-1-gestion-de-la-ejecucion.md) | Una por inversion, transversal | Sin documentos |
| S4.3.2 | [Ejecucion](S4-3-2-ejecucion/00-S4-3-2-ejecucion.md) | Una por contrato o frente | Modelo logico y sustento en `ELABORACION` |
| S4.3.3 | [Recepcion](S4-3-3-recepcion/00-S4-3-3-recepcion.md) | Una por ejecucion concluida o resuelta | Sin documentos |

## Pendientes

- Responder las preguntas P7 a P10 del [sustento](S4-3-sustento.md) y revisar el modelo logico y la ficha borrador.
- Incorporar fuentes de Obras por Impuestos y del Sistema Nacional de Abastecimiento a la biblioteca.

- Recibir los levantamientos del equipo y el documento interno para elaborar fichas; se registraran como insumos en el sustento.
- Elaborar la ficha de producto y proceso de S4.3 conforme al Anexo 2.
- Definir la descomposicion en procesos Nivel 2.
- El rediseno TO-BE queda pendiente para una etapa posterior: ver [TO-BE](../../to-be/00-to-be.md).

## Relaciones

- [Ficha de producto y proceso de S4](../S4-ficha-producto-proceso.md)
- [Inventario de productos y procesos](../../mapa-de-procesos-institucional/inventario-productos-procesos.md)
- [Estandar de artefactos](../../../00-gobernanza/estandar-artefactos-modelamiento.md)
- [Iniciativa de modelamiento hibrido](../../../00-gobernanza/iniciativas/iniciativa-modelamiento-hibrido.md)
- [Plantillas de procesos](../../../00-gobernanza/plantillas/00-plantillas.md)
