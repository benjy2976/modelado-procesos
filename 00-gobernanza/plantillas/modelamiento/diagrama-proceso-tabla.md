---
id: pendiente
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: pendiente
nivel_proceso: pendiente
proceso: []
fecha_creacion: "{{date:YYYY-MM-DD}}"
fecha_actualizacion: "{{date:YYYY-MM-DD}}"
responsable: pendiente
confidencialidad: INTERNO
tags:
  - tema/procesos
---

# [codigo] [nombre del proceso]

<!-- Fuente editable del diagrama en la etapa logica (DEC-025, DEC-026). Guardar como <codigo>-diagrama-proceso-tabla.md en la carpeta del proceso y enlazarla desde su nota indice. El titulo de nivel 1 es el nombre del diagrama. Generar el BPMN, el SVG y el PNG con 05-herramientas/gestor-modelos/construir_modelos.py. -->
<!-- Reglas: ID unico sin espacios; un nombre de carril no puede contener ";"; "Siguiente" solo dentro del mismo pool, con condiciones entre corchetes: G-1 [Si]; T-2 [No]. Entre pools se usa la tabla "Mensajes"; un pool que solo aparece alli se dibuja cerrado. -->
<!-- Solo se usan los tipos de la paleta del proyecto (estandar de artefactos, seccion 7.3; DEC-027); el control D5 rechaza cualquier otro. -->
<!-- Tipos: inicio, inicio-mensaje, inicio-temporizador, inicio-condicional, inicio-senal; mensaje-recepcion, temporizador, condicional, senal-recepcion; mensaje-envio, senal-envio, escalacion-envio, hito; fin, fin-mensaje, fin-terminal, fin-senal, fin-escalacion, fin-error; borde-temporizador, borde-mensaje, borde-condicional, borde-senal, borde-escalacion, borde-error; tarea, tarea-usuario, tarea-manual, tarea-servicio, subproceso; subproceso-evento-mensaje, subproceso-evento-temporizador, subproceso-evento-condicional; compuerta, compuerta-paralela, compuerta-inclusiva, compuerta-eventos. -->
<!-- Columnas opcionales: Marcador (multiple-paralelo, multiple-secuencial, bucle) en actividades; Adjunto (ID de la actividad) e Interrumpe (Si o No) en eventos de borde, con a lo sumo dos por actividad; Disparador en subprocesos de evento, que no llevan "Siguiente"; Anotacion y Grupo en cualquier elemento. Flujo por defecto: "T-3 [No] (por defecto)" en Siguiente. -->
<!-- Clase: OBS (observado en fuente institucional), NORM (exigencia normativa), EQ (equipo), PROP (propuesta). Fuente: regla, articulo o evidencia del sustento. Ambas columnas no se dibujan; sostienen la trazabilidad. -->

Sube a: <!-- enlace a la nota indice del proceso -->

## Pools

| Pool | Carriles |
|---|---|
| [codigo] [nombre del proceso] | Unidad o rol 1; Unidad o rol 2 |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| E-1 | [codigo] [nombre del proceso] | Unidad o rol 1 | inicio-mensaje | Solicitud recibida | T-1 | | | OBS | |
| T-1 | [codigo] [nombre del proceso] | Unidad o rol 1 | tarea | Revisar solicitud | G-1 | entra: Solicitud | | OBS | |
| G-1 | [codigo] [nombre del proceso] | Unidad o rol 1 | compuerta | ¿Procede? | T-2 [Si]; F-2 [No] | | | OBS | |
| T-2 | [codigo] [nombre del proceso] | Unidad o rol 2 | tarea | Atender solicitud | F-1 | sale: Respuesta | | OBS | |
| F-1 | [codigo] [nombre del proceso] | Unidad o rol 2 | fin-mensaje | Respuesta enviada | | | | OBS | |
| F-2 | [codigo] [nombre del proceso] | Unidad o rol 1 | fin | Solicitud no procede | | | | OBS | |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| Proceso o actor externo | E-1 | Solicitud |
| F-1 | Proceso o actor externo | Respuesta |
