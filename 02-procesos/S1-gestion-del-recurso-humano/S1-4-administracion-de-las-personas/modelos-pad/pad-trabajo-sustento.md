---
id: AP-S1-4-PAD-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
proceso: []
fecha_creacion: 2026-10-20
fecha_actualizacion: 2026-10-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s1/s1-4
---

# PAD - Sustento de fichas y formatos de trabajo

Sube a: [Modelos BPMN de trabajo para el PAD](00-modelos-pad.md)

Este sustento separa el contenido observado de la ficha institucional y del borrador de directiva, las inferencias de arquitectura y las propuestas usadas en el inventario, las cinco fichas y los indicadores. Ninguna regla juridica del borrador se registra como validada.

## Fuentes y autoridad

| Fuente | Ubicacion precisa y fecha de consulta | Estado y vigencia | Uso en este paquete |
|---|---|---|---|
| [Mapa de procesos Nivel 0 aprobado](../../../../01-referencias/01-institucionales-grh/originales/mapa-procesos-grh-nivel-0.pdf) | Pagina PDF 1; 2026-10-20 | Aprobado segun confirmacion del equipo; acto y fecha formal no visibles | Jerarquia S1 |
| [Mapa institucional aprobado](../../../../01-referencias/01-institucionales-grh/originales/mapa-procesos-grh-oficial.pdf), SHA-256 `92B61519CA6D15087BDB870E52D5586D4546789E0728C6947593DBF552C3C851` | Nivel 1 paginas PDF 21 y 25; ficha S1 paginas PDF 110-111; 2026-10-20 | Aprobado segun el usuario; vigencia formal posterior y acto no acreditados en esta copia | Codigo S1.4, denominacion, producto disciplinario, dueno y tipo de S1 |
| Proyecto de directiva PAD entregado por el usuario, SHA-256 `038AE5C432C25876C61A234E08F55DC95ED124493D806F4CCA0EDB269CD76869` | Numerales 5.4.1, 6.1.8, 6.4-6.5, 6.8, 6.16-6.19; paginas PDF 9, 16-27 y 31-32; anexos 5-10, paginas 44-49; 2026-10-20 | Portada «PROPUESTA», firmas vacias; sin vigencia acreditada | Denominaciones, roles, actividades y salidas **observados en el borrador**; no exigencia normativa |
| [NT 002-2025-PCM-SGP, fuente oficial](https://www.gob.pe/institucion/pcm/normas-legales/6501954-002-2025-pcm-sgp) y [copia local](../../../../01-referencias/02-gestion-por-procesos/originales/nt-002-2025-pcm-sgp/norma-tecnica-n-002-2025-pcm-sgp-f-f.pdf) | Numeral 6.1.3, Anexos 1, 2, 4, 7 y 8; consulta 2026-10-20 | Documento oficial consultado para estructura; aplicacion a un procedimiento concreto pendiente | Campos de inventario, fichas e indicadores; condicion para abrir procedimiento |

La lectura y discrepancias del PDF de directiva constan en la [revision documental](../../../../90-bandeja-entrada/revision-proyecto-directiva-pad.md). El original institucional no se modifica.

## Evidencia, inferencia y propuesta por ficha

| Unidad | Evidencia observada | Inferencia o propuesta de modelamiento | Vacio principal |
|---|---|---|---|
| [Caso PAD](pad-trabajo-caso-ficha-producto-proceso.md) | La ficha S1 ubica el producto disciplinario en S1.4 (p. 110); el borrador nombra el subproceso PAD (5.4.1, p. 9) y describe resultados alternativos (6.4-6.8, pp. 19-27) | Proponer un hijo PAD bajo S1.4 y una vista integral de una instancia; objetivo redactado para contrastar | Codigo, denominacion, dueno, limite final y producto NT aprobados |
| [Precalificacion](pad-trabajo-precalificacion-ficha-producto-proceso.md) | Secretaria Tecnica, proveido de no ha lugar o informe de precalificacion (6.1.8, 6.5 y 6.8.1, pp. 16-23) | Tratar la investigacion y precalificacion como unidad modelable, sin declarar un proceso independiente | Nivel, receptor del no ha lugar, variantes de denuncia y reglas vigentes |
| [Instruccion](pad-trabajo-instruccion-ficha-producto-proceso.md) | Organo Instructor, acto de inicio, descargos e informe de instruccion (6.5.3-6.5.4 y 6.8.2-6.8.14, pp. 20, 23-25) | Separar fase instructiva para revisar responsabilidades y salidas | Competencia por caso, cargos/unidades y nivel |
| [Decision](pad-trabajo-decision-ficha-producto-proceso.md) | Organo Sancionador, sancion o archivo y comunicacion (6.8.15-6.8.23, pp. 25-27; anexos 9-10, pp. 48-49) | Separar fase sancionadora para revisar sus rutas alternativas | Canales y validez de notificacion; nivel y dueno |
| [Recursos](pad-trabajo-recursos-ficha-producto-proceso.md) | Reconsideracion y apelacion descritas en 6.16-6.18, pp. 31-32 | Modelar solo resolucion de reconsideracion y derivacion de apelacion como interfaz candidata | Frontera con segunda instancia y proceso receptor; posible ausencia de proceso PAD propio |

Las tablas de los cinco BPMN conservan `Clase` y `Fuente` por elemento. La palabra `OBS` en ellas significa **texto observado en el borrador**, no evidencia de ejecucion actual.

## Productos y campos pendientes

| Campo de los formatos | Estado de evidencia | Accion para completarlo |
|---|---|---|
| Codigo, nivel y denominacion NT del hijo PAD y de sus posibles subprocesos | EVIDENCIA-INSUFICIENTE | Decision documentada de descomposicion de S1.4 |
| Tipo y dueno de cada proceso candidato | EVIDENCIA-INSUFICIENTE | Confirmar autoridad funcional y titularidad; la ficha S1 solo resuelve S1 |
| Objetivo estrategico | EVIDENCIA-INSUFICIENTE | Vincular con instrumento de planeamiento vigente |
| Riesgos y registros de ultimo nivel | EVIDENCIA-INSUFICIENTE | Confirmar ultimo nivel y levantar con responsables, separando registros de productos |
| Indicadores, formula operativa, responsable, frecuencia, linea base y metas | Tres propuestas sin adopcion ni datos | Revisar pertinencia y disponibilidad de datos; acordar definiciones y metas |
| Procedimientos y diagramas del Anexo 8 | EVIDENCIA-INSUFICIENTE | Confirmar ultimo nivel y criterio del numeral 6.1.3 d; ver [evaluacion de aplicabilidad](pad-trabajo-aplicabilidad-procedimientos.md) |
| Elaboracion, revision y aprobacion | PENDIENTE | Registrar solo conformidades humanas con evidencia |

## Discrepancias que impiden linea base

La [revision documental](../../../../90-bandeja-entrada/revision-proyecto-directiva-pad.md) detalla PAD-01 a PAD-10. Afectan especialmente la identificacion de la directiva, competencia, amonestacion verbal, denuncia anonima, custodia, notificaciones y segunda instancia. Ninguna ficha o indicador de este paquete resuelve esas discrepancias por su cuenta.

## Revision

| Fecha | Accion | Estado |
|---|---|---|
| 2026-10-20 | IA preparo inventario, cinco fichas del Anexo 2, fichas de indicador candidatas y evaluacion de procedimiento, a partir de las fuentes listadas | Propuesta en elaboracion; sin conformidad institucional |
