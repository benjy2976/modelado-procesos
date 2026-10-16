---
id: CON-GUIA-MANUAL-BPMN
tipo: nota-conocimiento
area: conocimiento
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
proceso: []
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
aliases:
  - Guia del manual BPMN
tags:
  - tema/conocimiento
  - tema/procesos
---

# Guia de lectura: BPMN 2.0, Manual de Referencia y Guia Practica

Sube a: [Guias de lectura de fuentes](00-fuentes.md)

Manual de Freund, Rucker y Hitpass (4.a edicion en espanol, 2014). Es una **referencia tecnica**, no una norma: sus recomendaciones son buenas practicas para modelar y revisar diagramas BPMN; no imponen obligaciones.

## Identificacion

| Campo | Valor |
|---|---|
| Catalogo | `LOC-004` |
| Original | [bpmn-2-manual-referencia-guia-practica.pdf](../../01-referencias/02-gestion-por-procesos/originales/bpmn-2-manual-referencia-guia-practica.pdf) (266 paginas; 10 sin texto) |
| SHA-256 | `9F9504BF6431F9F34AB10BD8876755221A36D46CB8E15D2FF82DBB55FF41CEEA` |
| Fecha de consulta | 2026-10-16 |

## Mapa de lectura

| Tema | Ubicacion | Pagina PDF |
|---|---|---:|
| Notacion basica: actividades, eventos, gateways | Seccion 2.2 | 33-37 |
| Pools y lanes | Seccion 2.9 | 99 en adelante |
| Subprocesos | Seccion 2.8 | 84 en adelante |
| Nivel 1: modelo descriptivo | Capitulo 3 | 134-161 |
| Pools y lanes en el nivel descriptivo | Seccion 3.3.1 | 142-144 |
| Gateways en el nivel descriptivo | Seccion 3.3.3 | 147 |
| Nivel 2: modelo operacional | Capitulo 4 | 162 en adelante |

## Buenas practicas aplicables

| Practica | Ubicacion |
|---|---|
| Nombrar las actividades con verbo y sustantivo ("comprar alimentos") | p. 34 |
| Nombrar los eventos con objeto y participio ("orden recibida") | p. 35 |
| Si se usa evento de inicio, usar tambien evento de fin; se recomienda siempre usarlos | p. 35 |
| Escribir la pregunta sobre el gateway y nombrar las respuestas en los flujos de salida | p. 36 |
| No mezclar los dos simbolos equivalentes del XOR-gateway | p. 37 |
| Un proceso puede tener varios eventos de fin para mostrar distintos estados de termino | p. 37 |
| Cada participante con su propio dirigente va en su propio pool; la comunicacion entre pools es por flujo de mensaje | p. 142-144 |
| En el nivel descriptivo se modela el caso normal ("happy path"); las variantes solo si son parte del flujo normal | p. 147 |
| En el nivel descriptivo usar XOR-gateways para bifurcar y evitar uniones tecnicas (XOR-join) innecesarias | p. 147 |
| Un subproceso se marca con el signo (+) y su detalle se modela en un diagrama propio | p. 84 |
