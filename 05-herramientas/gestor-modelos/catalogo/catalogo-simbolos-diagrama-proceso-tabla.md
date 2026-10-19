---
id: HER-CATALOGO-SIMBOLOS-BPMN
tipo: nota-conocimiento
area: herramientas
estado_documento: VIGENTE
clase_conocimiento: DECISION
fecha_creacion: 2026-10-19
fecha_actualizacion: 2026-10-19
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
---

# Catálogo de símbolos de la paleta BPMN

<!-- Prueba de regresion de la cadena BPMN (DEC-027): contiene todos los simbolos de la paleta del proyecto. Se construye con construir_modelos.py; su vista interactiva y su copia para Bizagi permiten comparar cada simbolo con el manual BPMN y comprobar la importacion. No es un proceso del GRH. -->

Sube a: [Gestor local de modelos](../00-gestor-modelos.md)

Ejemplo generico con todos los simbolos de la paleta del proyecto (estandar de artefactos, seccion 7.3). Se regenera con cada cambio de la herramienta y debe pasar los controles D1 a D5. Sus vistas: [interactiva](catalogo-simbolos-diagrama-proceso.html), [SVG](catalogo-simbolos-diagrama-proceso.svg) y [PNG](catalogo-simbolos-diagrama-proceso.png).

## Pools

| Pool | Carriles |
|---|---|
| Catálogo 1: inicios, fines y tareas | Rol 1 |
| Catálogo 2: compuertas y eventos intermedios | Rol 2 |
| Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Marcador | Adjunto | Interrumpe | Disparador | Anotacion | Grupo |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E1-1 | Catálogo 1: inicios, fines y tareas | Rol 1 | inicio | Inicio | T1-1 | | | | | | | |
| T1-1 | Catálogo 1: inicios, fines y tareas | Rol 1 | tarea | Tarea | F1-1 | | | | | | | |
| F1-1 | Catálogo 1: inicios, fines y tareas | Rol 1 | fin | Fin | | | | | | | | |
| E1-2 | Catálogo 1: inicios, fines y tareas | Rol 1 | inicio-mensaje | Mensaje recibido | T1-2 | | | | | | | |
| T1-2 | Catálogo 1: inicios, fines y tareas | Rol 1 | tarea-usuario | Tarea de usuario | F1-2 | | | | | | | |
| F1-2 | Catálogo 1: inicios, fines y tareas | Rol 1 | fin-mensaje | Mensaje enviado | | | | | | | | |
| E1-3 | Catálogo 1: inicios, fines y tareas | Rol 1 | inicio-temporizador | Fecha alcanzada | T1-3 | | | | | | | |
| T1-3 | Catálogo 1: inicios, fines y tareas | Rol 1 | tarea-manual | Tarea manual | F1-3 | | | | | | | |
| F1-3 | Catálogo 1: inicios, fines y tareas | Rol 1 | fin-terminal | Fin terminal | | | | | | | | |
| E1-4 | Catálogo 1: inicios, fines y tareas | Rol 1 | inicio-senal | Señal recibida | T1-4 | | | | | | | |
| T1-4 | Catálogo 1: inicios, fines y tareas | Rol 1 | tarea-servicio | Tarea de servicio | F1-4 | | | | | | | |
| F1-4 | Catálogo 1: inicios, fines y tareas | Rol 1 | fin-senal | Señal emitida | | | | | | | | |
| E2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | inicio | Inicio | T2-1 | | | | | | | |
| T2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | tarea | Registrar solicitud | G2-1 | | | | | | | |
| G2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | compuerta | ¿Requiere revisión? | T2-2 [Sí]; T2-3 [No] (por defecto) | | | | | | | |
| T2-2 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | tarea | Revisar solicitud | G2-2 | | | | | | | |
| T2-3 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | tarea | Archivar solicitud | F2-2 | | | | | | | |
| G2-2 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | compuerta-paralela | | H2-1; S2-1; X2-1 | | | | | | | |
| H2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | hito | Hito alcanzado | G2-3 | | | | | | | |
| S2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | senal-envio | Señal emitida | G2-3 | | | | | | | |
| X2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | escalacion-envio | Escalación emitida | G2-3 | | | | | | | |
| G2-3 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | compuerta-paralela | | G2-4 | | | | | | | |
| G2-4 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | compuerta-eventos | ¿Qué ocurre primero? | M2-1; R2-1; C2-1; N2-1 | | | | | | | |
| M2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | mensaje-recepcion | Mensaje recibido | T2-4 | | | | | | | |
| R2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | temporizador | Plazo vencido | T2-4 | | | | | | | |
| C2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | condicional | Condición cumplida | T2-4 | | | | | | | |
| N2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | senal-recepcion | Señal recibida | T2-4 | | | | | | | |
| T2-4 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | tarea | Atender el suceso | G2-5 | | | | | | | |
| G2-5 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | compuerta-inclusiva | ¿Qué corresponde? | T2-5 [Opción 1]; T2-6 [Opción 2] | | | | | | | |
| T2-5 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | tarea | Atender opción 1 | G2-6 | | | | | | | |
| T2-6 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | tarea | Atender opción 2 | G2-6 | | | | | | | |
| G2-6 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | compuerta-inclusiva | | F2-1 | | | | | | | |
| F2-1 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | fin | Solicitud atendida | | | | | | | | |
| F2-2 | Catálogo 2: compuertas y eventos intermedios | Rol 2 | fin | Solicitud archivada | | | | | | | | |
| E3-1 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | inicio-condicional | Condición de inicio | S3-1 |  |  |  |  |  |  |  |
| S3-1 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | subproceso | Subproceso de llamada | T3-1 |  | multiple-paralelo |  |  |  |  |  |
| T3-1 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | tarea | Tarea con bucle | T3-2 | entra: Documento; almacén: Sistema | bucle |  |  |  |  | Grupo de tareas |
| T3-2 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | tarea | Tarea múltiple secuencial | T3-3 |  | multiple-secuencial |  |  |  |  | Grupo de tareas |
| T3-3 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | tarea | Registrar resultado | T3-4 | sale: Resultado |  |  |  |  | Anotación en una tarea |  |
| T3-4 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | tarea | Cerrar caso | F3-1 |  |  |  |  |  |  |  |
| F3-1 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | fin | Fin normal |  |  |  |  |  |  |  |  |
| B3-3 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | borde-mensaje | Aviso recibido | F3-4 |  |  | S3-1 | Sí |  |  |  |
| F3-4 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | fin | Atendido por aviso |  |  |  |  |  |  |  |  |
| B3-4 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | borde-condicional | Condición cumplida | F3-5 |  |  | S3-1 | No |  |  |  |
| F3-5 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | fin-senal | Señal emitida |  |  |  |  |  |  |  |  |
| B3-1 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | borde-temporizador | Plazo vencido | F3-2 |  |  | T3-2 | No |  |  |  |
| F3-2 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | fin-escalacion | Caso escalado |  |  |  |  |  |  |  |  |
| B3-2 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | borde-error | Error | F3-3 |  |  | T3-2 | Sí |  |  |  |
| F3-3 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | fin-error | Error notificado |  |  |  |  |  |  |  |  |
| B3-5 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | borde-senal | Señal recibida | F3-6 |  |  | T3-4 | Sí |  |  |  |
| F3-6 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | fin | Cancelado por señal |  |  |  |  |  |  |  |  |
| B3-6 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | borde-escalacion | Escalación recibida | F3-7 |  |  | T3-4 | No |  |  |  |
| F3-7 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | fin | Escalación atendida |  |  |  |  |  |  |  |  |
| V3-1 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | subproceso-evento-mensaje | Subproceso de evento de mensaje | | | | | | Mensaje recibido | Anotación en un subproceso de evento | Subprocesos de evento |
| V3-2 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | subproceso-evento-temporizador | Subproceso de evento de tiempo | | | | | | Cada mes | | Subprocesos de evento |
| V3-3 | Catálogo 3: marcadores, bordes, datos, artefactos y subprocesos de evento | Rol 3 | subproceso-evento-condicional | Subproceso de evento condicional | | | | | | Condición cumplida | | Subprocesos de evento |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
| Participante externo | E1-2 | Solicitud |
| F1-2 | Participante externo | Respuesta |
