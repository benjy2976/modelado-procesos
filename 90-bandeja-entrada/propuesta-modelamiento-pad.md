---
id: BAN-PROP-MODELAMIENTO-PAD
tipo: propuesta
area: bandeja-entrada
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
proceso: []
fecha_creacion: 2026-10-20
fecha_actualizacion: 2026-10-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/referencias
  - tema/procesos
---

# Propuesta de modelamiento del PAD

Sube a: [Bandeja de entrada](00-BANDEJA-ENTRADA.md)

Este paquete deja preparada la estructura de fichas, diagramas BPMN y sustento para el PAD descrito en el PDF recibido. **S1.4 es el proceso padre aprobado; codigo de Nivel 2, descomposicion y AS-IS pendientes.** La directiva recibida es una propuesta, no un levantamiento de ejecucion. Los campos no sustentados se dejan como `EVIDENCIA-INSUFICIENTE`.

## Alcance propuesto

El [mapa aprobado, rama S1](../02-procesos/mapa-de-procesos-institucional/mapa-procesos-nivel-1-s1.md) ubica los productos disciplinarios en **S1.4 Administracion de las personas** (paginas PDF 25 y 110-111). El numeral 5.4.1 del borrador de directiva, pagina 9, denomina un subproceso «Gestion del Regimen Disciplinario y Procedimiento Administrativo Sancionador», sin codigo aprobado de Nivel 2. Se propone modelar **una instancia por caso** desde la recepcion o inicio de oficio hasta el no ha lugar o la decision final notificada, con recursos y custodia como interacciones que requieren delimitarse. La amonestacion verbal queda fuera del flujo PAD candidato hasta resolver PAD-05 de la [revision documental](revision-proyecto-directiva-pad.md).

La separacion preliminar sigue las fases que el propio borrador denomina en el numeral 6.8, paginas 22-27. Esta tabla no crea codigos ni aprueba una descomposicion:

| Unidad de modelamiento candidata | Evidencia de nombre y limite | Codigo NT | Nivel | Producto candidato |
|---|---|---|---|---|
| Administracion de las personas, proceso padre aprobado | Mapa Nivel 1 y ficha S1, paginas PDF 25 y 110-111 | **S1.4** | **1** | Informes y resoluciones de procedimientos disciplinarios, entre otros productos del proceso padre |
| Gestion del Regimen Disciplinario y Procedimiento Administrativo Sancionador, hijo candidato | Borrador de directiva, numeral 5.4.1, pagina PDF 9 | EVIDENCIA-INSUFICIENTE | Nivel 2 propuesto, no aprobado | Resultado del caso disciplinario documentado, por contrastar con la interfaz de S1.4 |
| Investigacion preliminar y precalificacion | Numerales 6.5 y 6.8.1, paginas 19-20 y 22-23 | EVIDENCIA-INSUFICIENTE | EVIDENCIA-INSUFICIENTE | Proveido de no ha lugar o informe de precalificacion |
| Fase instructiva | Numerales 6.8.2-6.8.14, paginas 23-25 | EVIDENCIA-INSUFICIENTE | EVIDENCIA-INSUFICIENTE | Informe de instruccion |
| Fase sancionadora | Numerales 6.8.15-6.8.23, paginas 25-27 | EVIDENCIA-INSUFICIENTE | EVIDENCIA-INSUFICIENTE | Decision final de sancion o archivo, notificada |

## Fichas de producto y proceso: datos listos y vacios

Se prepararon [cinco fichas candidatas con los campos del Anexo 2](../02-procesos/S1-gestion-del-recurso-humano/S1-4-administracion-de-las-personas/modelos-pad/00-modelos-pad.md), una por unidad diagramada, para revisar su contenido mientras se decide la jerarquia. No afirman que existan cinco procesos institucionales. La ficha institucional S1 es una fuente aprobada que no se edita. El cuadro siguiente resume los insumos de esas fichas:

| Campo del Anexo 2 | Proceso PAD candidato | Precalificacion | Instruccion | Sancion o archivo |
|---|---|---|---|---|
| Nombre del proceso | Denominacion del numeral 5.4.1, pendiente de confirmar | Denominacion del numeral 6.5, pendiente | Denominacion del numeral 6.8, pendiente | Denominacion del numeral 6.8, pendiente |
| Tipo de proceso | El padre S1 es de Apoyo segun ficha aprobada, pagina PDF 110; clasificacion del hijo pendiente | Igual | Igual | Igual |
| Dueno del proceso | La ficha S1 atribuye S1 a la Sub Gerencia de Gestion de Recursos Humanos, pagina PDF 110; el dueno NT del hijo PAD debe confirmarse | EVIDENCIA-INSUFICIENTE | EVIDENCIA-INSUFICIENTE | EVIDENCIA-INSUFICIENTE |
| Objetivo del proceso | Propuesta a contrastar: conducir los casos disciplinarios con resultado documentado; inspirada en objetivo y finalidad de pagina 5 | Obtener un resultado de precalificacion sustentado (paginas 19-20) | Sustanciar el caso y remitir informe al organo sancionador (paginas 23-25) | Emitir y comunicar la decision final (paginas 25-27) |
| Objetivo estrategico | EVIDENCIA-INSUFICIENTE: falta instrumento de planeamiento aplicable | Igual | Igual | Igual |
| Riesgos y registros | Solo se consignaran en fichas de ultimo nivel; nivel aun pendiente | Igual | Igual | Igual |
| Elaborado, revisado, aprobado | Cargos institucionales de la plantilla, sin atribuir conformidad ni firmas | Igual | Igual | Igual |

### Proveedor, entrada, producto y receptor candidatos

| Unidad candidata | Proveedor observado o por confirmar | Entrada mencionada | Producto mencionado | Receptor mencionado o por confirmar | Fuente PDF |
|---|---|---|---|---|---|
| Precalificacion | Denunciante, area informante, control o iniciativa de oficio | Denuncia, reporte o informe de control | Proveido de no ha lugar **o** informe de precalificacion | Denunciante/archivo y organo instructor, respectivamente; detalle por confirmar | 6.1.8, 6.5, 6.8.1; paginas 16-20, 22-23; anexos 3-6 |
| Instruccion | Secretaria Tecnica y organo instructor | Informe de precalificacion y expediente | Acto de inicio notificado e informe de instruccion | Servidor o ex servidor y organo sancionador | 6.8.2-6.8.14; paginas 23-25; anexos 1, 7 y 8 |
| Sancion o archivo | Organo instructor | Informe de instruccion y actuaciones del caso | Acto de sancion o de archivo y constancia de notificacion | Servidor o ex servidor; areas de registro/custodia segun resultado, por confirmar | 6.8.15-6.8.23 y 6.18-6.19; paginas 25-27 y 31-32; anexos 9-10 |

No se incorpora un producto unico artificial para todos los casos: el resultado es alternativo y depende de la decision documentada. Las relaciones con registro de sanciones, legajo, recurso y archivo central se detallaran tras confirmar las competencias y la frontera de cada proceso.

## Diagramas BPMN propuestos

Ya se prepararon [cinco modelos BPMN de trabajo](../02-procesos/S1-gestion-del-recurso-humano/S1-4-administracion-de-las-personas/modelos-pad/00-modelos-pad.md), agrupados bajo S1.4 con tablas fuente y derivados generados mediante `05-herramientas/gestor-modelos/construir_modelos.py`. Identifican los archivos como `pad-trabajo-*` mientras sigue pendiente el codigo NT del hijo PAD. Se usaron solo elementos de la [paleta BPMN 2.0 del proyecto](../00-gobernanza/estandar-artefactos-modelamiento.md), seccion 7.3. Las secuencias son propuestas basadas en el borrador; no representan un AS-IS observado ni una linea base aprobada.

| Diagrama de trabajo | Inicio y cierre a confirmar | Elementos BPMN de la paleta empleados o a evaluar | Evidencia PDF | Punto que impide cerrarlo |
|---|---|---|---|---|
| Vista del proceso PAD por fases | Recepcion de caso o investigacion de oficio; no ha lugar o decision final comunicada | Inicio, subprocesos de llamada, compuerta exclusiva para resultado de precalificacion, fines y flujos de mensaje con participantes externos | 5.4.1, 6.5, 6.8; paginas 9, 19-27 | Codigo, limites, papel del recurso y traspaso de custodia |
| Investigacion preliminar y precalificacion | Denuncia/reporte/conocimiento de oficio; proveido o informe | Inicio de mensaje o indefinido segun disparador, tareas, compuerta exclusiva y dos fines | 6.1.8, 6.2, 6.4, 6.5 y 6.8.1; paginas 16-23 | Denuncia anonima, nueva evaluacion, prescripcion y aprobacion de las variantes |
| Fase instructiva | Informe de precalificacion recibido; informe de instruccion remitido | Tareas, mensajes, compuertas exclusivas para competencia y descargos, eventos de espera solo si el hecho de espera se confirma | 6.5.3-6.5.4 y 6.8.2-6.8.14; paginas 20 y 23-25 | Competencia por caso, forma del acto de inicio y plazos validados |
| Fase sancionadora | Informe de instruccion recibido; decision final comunicada | Tareas, compuerta exclusiva para informe oral y resultado, mensajes y fines de sancion/archivo | 6.8.15-6.8.23; paginas 25-27 | Variantes de audiencia, nulidad, registro y notificacion |
| Recursos y segunda instancia, si queda dentro del alcance | Recurso recibido tras decision; resolucion y comunicacion | Pool externo cerrado del Tribunal cuando corresponda, flujos de mensaje, tareas y fines | 6.16-6.18; paginas 31-32; grafico 3, pagina 54 | Jerarquia institucional y competencia; no asumir que todo caso recurre |

Los carriles candidatos son los **roles** Secretaria Tecnica, organo instructor y organo sancionador; la SGGRH participa segun funciones documentadas. Denunciante, servidor o ex servidor y Tribunal del Servicio Civil, cuando proceda, son participantes externos al control del proceso y se relacionarian mediante mensajes. El borrador usa distintas autoridades para un mismo rol segun caso; no se fijara un carril institucional unico hasta resolver esas variantes. Los plazos y canales del borrador no se codificaran como temporizadores ni reglas automatizadas sin validacion normativa.

## Fichas de indicador candidatas

El PDF no contiene ficha de indicador, serie base, metas ni responsable NT. Se prepararon [fichas candidatas del Anexo 4](../02-procesos/S1-gestion-del-recurso-humano/S1-4-administracion-de-las-personas/modelos-pad/pad-trabajo-fichas-indicador.md) para definir con el equipo, **sin valores ni metas inventados**:

| Nombre candidato | Tipo propuesto | Metodo de calculo propuesto | Fuente de datos necesaria | Campos pendientes |
|---|---|---|---|---|
| Casos recibidos con respuesta registrada al denunciante | Proceso | Casos con constancia de respuesta / casos recibidos que requieren respuesta, en el periodo | Registro de denuncias y cargos de respuesta | Poblacion exacta, responsable, frecuencia, linea base y meta |
| Casos con resultado de precalificacion documentado | Producto | Casos con proveido o informe de precalificacion / casos evaluados, en el periodo | Registro de casos y documentos de precalificacion | Denominador, calidad del producto, responsable, frecuencia, linea base y meta |
| Decisiones finales notificadas con constancia | Producto | Decisiones finales con constancia de notificacion / decisiones finales emitidas, en el periodo | Registro de decisiones y cargos de notificacion | Fuente institucional, responsable, frecuencia, linea base y meta |

El sentido esperado y unidad de medida se decidiran con el dueno del proceso; una proporcion propuesta no prueba cumplimiento juridico. La ficha formal conservara todos los campos del Anexo 4, incluidos justificacion, definicion de variables, serie y logros esperados, cuando exista evidencia suficiente.

## Procedimientos y otros artefactos

La [plantilla del Anexo 7](../00-gobernanza/plantillas/nt-002/procedimiento.md) solo se aplica al **ultimo nivel** y si se cumple un criterio del numeral 6.1.3 d de la [NT oficial](https://www.gob.pe/institucion/pcm/normas-legales/6501954-002-2025-pcm-sgp), consultada el 2026-10-20. La [evaluacion de aplicabilidad](../02-procesos/S1-gestion-del-recurso-humano/S1-4-administracion-de-las-personas/modelos-pad/pad-trabajo-aplicabilidad-procedimientos.md) deja registrado por que no se emite aun un procedimiento NT: ultimo nivel y criterio siguen sin documentarse. Los candidatos a evaluar son precalificacion, instruccion y decision/notificacion; sus tareas deben salir de evidencia verificada, y el diagrama del procedimiento sera BPMN segun Anexo 8.

Cada proceso confirmado requerira nota indice, ficha de producto y proceso, ficha de indicador cuando se defina, tabla y derivados BPMN, sustento con fuente y discrepancias, y procedimiento solo si corresponde. Los anexos 1-11 del PDF son **formatos o estructuras documentales recibidas**, no equivalen a las fichas de los Anexos 2, 4 y 7 de la NT. El sustento enlazara los formatos pertinentes sin copiar datos de expedientes ni atribuirles vigencia.

## Secuencia para trasladar a `02-procesos`

1. Conservar el anclaje aprobado S1 > S1.4. Confirmar codigo NT, nombre, dueno y frontera del **hijo PAD** y registrar la decision de descomposicion; no asignar `S1.4.n` por cuenta del proyecto.
2. Obtener AS-IS observado y contrastar la directiva vigente, el borrador y sus anexos; registrar diferencias sin mezclarlos.
3. Resolver los puntos PAD-01 a PAD-10 de la [revision documental](revision-proyecto-directiva-pad.md) y las variantes por tipo de caso.
4. Abrir la carpeta por codigo y su nota indice; redactar las fichas desde las plantillas y enlazarlas desde el indice.
5. Redactar cada tabla BPMN con `Clase` y `Fuente` por elemento, generar derivados y ejecutar los controles D1 a D5. Registrar hallazgos en el sustento.
6. Someter fichas, modelos y eventual procedimiento al circuito humano sin atribuir niveles de revision ni aprobacion desde esta propuesta.

## Relaciones

- Se sustenta en: [Revision del proyecto de directiva PAD](revision-proyecto-directiva-pad.md).
- Se sustenta en: [S1 en el mapa institucional Nivel 1](../02-procesos/mapa-de-procesos-institucional/mapa-procesos-nivel-1-s1.md).
- Se rige por: [Estandar de artefactos](../00-gobernanza/estandar-artefactos-modelamiento.md).
- Se rige por: [Protocolo de conocimiento confiable](../00-gobernanza/protocolo-conocimiento-confiable.md).
