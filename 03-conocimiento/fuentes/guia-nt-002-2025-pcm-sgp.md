---
id: CON-GUIA-NT-002-2025-PCM-SGP
tipo: nota-conocimiento
area: conocimiento
estado_documento: BORRADOR
clase_conocimiento: NORMATIVO
proceso: []
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
aliases:
  - Guia de la Norma Tecnica de gestion por procesos
tags:
  - tema/conocimiento
  - tema/procesos
---

# Guia de lectura: Norma Tecnica 002-2025-PCM-SGP, gestion por procesos

Sube a: [Guias de lectura de fuentes](00-fuentes.md)

Norma que regula como las entidades identifican, documentan, aprueban, evaluan y mejoran sus procesos. Es la base de la estructura de `02-procesos` (`DEC-017`).

## Identificacion

| Campo | Valor |
|---|---|
| Catalogo | `PROC-001` |
| Original | [norma-tecnica-n-002-2025-pcm-sgp-f-f.pdf](../../01-referencias/02-gestion-por-procesos/originales/nt-002-2025-pcm-sgp/norma-tecnica-n-002-2025-pcm-sgp-f-f.pdf) (32 paginas, con texto) |
| SHA-256 | `16225C398C24D45B601EFEEF20C9E456EF81F0217BBB0A35E8A41BF2F4B60254` |
| Aprobacion | Resolucion de Secretaria de Gestion Publica 002-2025-PCM-SGP, 21-02-2025 |
| Fecha de consulta | 2026-10-16 |
| Vigencia | Por confirmar segun el catalogo |

## Mapa de lectura

| Tema | Ubicacion | Pagina PDF |
|---|---|---:|
| Fases del ciclo de gestion por procesos | Numeral 5.4 y capitulo 6 | 7-20 |
| Identificar productos y determinar procesos (niveles) | Numerales 6.1.1 y 6.1.2 | 8-11 |
| Documentos de procesos y criterios del procedimiento | Numeral 6.1.3 | 11-14 |
| Circuito de aprobacion | Numeral 6.1.4, Tablas 1 y 2 | 14 |
| Glosario (actividad, proceso, nivel, procedimiento, tarea) | Glosario | 21-23 |
| Formatos | Anexos 1 a 8 | 25-32 |

## Puntos clave para el modelamiento

| Tema | Lo que establece (parafrasis) | Ubicacion | Regla |
|---|---|---|---|
| Niveles | El nivel 0 (macroproceso) se desagrega en nivel 1, 2 hasta n; los duenos determinan los niveles 1 en adelante | Glosario p. 22; num. 6.1.2 paso 3, p. 11 | - |
| Codigo | Letra M, E o S mas numeracion por nivel (M1, M1.2, M1.2.4) | Anexo 1, p. 25 | - |
| Documentos | Ficha de producto y proceso con diagrama, ficha de indicador, mapa de procesos y procedimiento | Num. 6.1.3, p. 11 | - |
| Procedimiento | Solo en procesos de ultimo nivel, maximo uno por proceso y solo si cumple algun criterio | Num. 6.1.3 d, p. 13 | `REG-GPP-DOC-001` |
| Diagrama | Representa secuencia, roles, entradas, productos y receptores; se recomienda BPMN | Num. 6.1.3 a y nota 8, p. 12 | - |
| Modelo del diagrama | Un proceso con carriles por rol en orden jerarquico, inicio con elemento de entrada, actividades en infinitivo, divergencias y convergencias, subprocesos cuyas entradas y salidas interactuan con el proceso, registros y producto antes del fin | Anexo 3, p. 27 | - |
| Aprobacion | Elabora y aprueba el dueno del proceso, con opinion tecnica de la unidad de gestion por procesos | Num. 6.1.4, Tabla 1, p. 14 | - |
| Actividad y tarea | La actividad agrupa tareas; la tarea es el nivel mas desagregado y se describe en el procedimiento | Glosario, p. 21-23 | - |

## Alertas

- La NT no fija un numero de niveles: la descomposicion termina donde el dueno determina el ultimo nivel.
- Un subproceso BPMN de un diagrama de nivel 1 corresponde a un proceso de nivel 2 con su propia ficha.
