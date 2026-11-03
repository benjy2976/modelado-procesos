---
id: CON-GUIA-BPMN-2-0-2
tipo: nota-conocimiento
area: conocimiento
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
proceso: []
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-03
responsable: equipo-proyecto
confidencialidad: INTERNO
aliases:
  - Guia de la especificacion BPMN 2.0.2
tags:
  - tema/conocimiento
  - tema/procesos
---

# Guia de lectura: especificacion BPMN 2.0.2

Sube a: [Guias de lectura de fuentes](00-fuentes.md)

La especificacion BPMN 2.0.2 de OMG es la fuente tecnica primaria para la semantica y la notacion BPMN. Es una referencia tecnica para el proyecto; no constituye por si misma una obligacion juridica nacional. La Norma Tecnica 002-2025-PCM-SGP permite a cada entidad elegir la metodologia de diagramacion y recomienda BPMN.

## Identificacion

| Campo | Valor |
|---|---|
| Catalogo | `LOC-005` |
| Titulo | Business Process Model and Notation (BPMN), Version 2.0.2 |
| Emisor | Object Management Group (OMG) |
| Version | 2.0.2, enero de 2014 |
| Pagina oficial | [Especificacion BPMN](https://www.omg.org/spec/BPMN/) |
| PDF oficial | [BPMN 2.0.2](https://www.omg.org/spec/BPMN/2.0.2/PDF) |
| SHA-256 verificado | `D3D9258A70BF808C11AC52BECEA4CE645540A8B881117535F60A56FBF13E22F2` |
| Extension | 532 paginas PDF; 530 con texto extraible |
| Fecha de consulta | 2026-11-03 |

La copia usada para comprobar el hash y las paginas se conserva solo en `99-temporal/bpmn-2-0-2-especificacion-oficial.pdf`; el original es reproducible desde la URL oficial y no se incorpora como nuevo binario versionado.

## Mapa de lectura aplicable

| Tema | Ubicacion impresa | Pagina PDF |
|---|---:|---:|
| Subprocesos y marcadores de subproceso | Seccion 10.2.5, pp. 172-176 | 202-206 |
| Semantica del subproceso de evento | Seccion 10.2.5, p. 174 | 204 |
| Representacion contraida y expandida | Figuras 10.30 y 10.31, p. 175 | 205 |
| Eventos de inicio de subprocesos de evento | Seccion 10.5.2, tabla 10.86, pp. 241-244 | 271-274 |
| Atributo `isInterrupting` | Tabla 10.87, p. 244 | 274 |

## Afirmaciones tecnicas directamente sustentadas

- El subproceso de evento es un subproceso especializado contenido en un proceso o subproceso y se identifica en XML mediante `triggeredByEvent="true"`.
- No forma parte del flujo normal del proceso padre y no puede tener flujos de secuencia entrantes ni salientes.
- Debe tener exactamente un evento de inicio con disparador definido.
- Puede iniciarse cada vez que ocurre su disparador mientras el proceso padre esta activo.
- Si el evento de inicio no es interruptivo, el proceso contenedor continua y pueden existir varias instancias concurrentes.
- Su borde es una linea fina punteada. Cuando esta contraido, el evento de inicio se representa como marcador en la esquina superior izquierda.
- Mensaje, temporizador y condicion usan, respectivamente, los marcadores de sobre, reloj y hoja con lineas. El aro discontinuo identifica la variante no interruptiva.

## Alerta de consistencia de la fuente

El texto normativo de la pagina impresa 174 exige que el evento de inicio aparezca en la esquina superior izquierda del subproceso contraido. Sin embargo, la figura 10.30 de la pagina siguiente no lo dibuja. OMG mantiene este problema registrado como `BPMN21-369`. Para esta regla grafica se usa el texto de la especificacion y se contrasta con la tabla 10.86 y con la figura 2.91 del manual `LOC-004`, que si muestra el marcador.

## Uso en el proyecto

Las unidades atomicas propuestas para validacion se encuentran en [Conocimientos propuestos sobre subprocesos de evento](../manual-bpmn/cap-2-notacion/2-8-subprocesos/conocimientos-propuestos-subprocesos-evento.md). Su estado inicial es `BORRADOR-IA` y no deben presentarse como conocimiento validado hasta que se registre la revision humana correspondiente.

