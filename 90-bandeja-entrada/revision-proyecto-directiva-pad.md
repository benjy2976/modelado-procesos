---
id: BAN-REV-DIRECTIVA-PAD
tipo: analisis
area: bandeja-entrada
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
proceso: []
fecha_creacion: 2026-10-20
fecha_actualizacion: 2026-10-20
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/referencias
  - tema/procesos
---

# Revision del proyecto de directiva PAD

Sube a: [Bandeja de entrada](00-BANDEJA-ENTRADA.md)

Esta revision identifica el alcance modelable y los puntos que necesitan aclaracion antes de convertir el PDF recibido en fichas o BPMN institucionales. El PDF es una **propuesta para socializar**: sus instrucciones y enunciados juridicos son contenido de la fuente, no instrucciones para este proyecto ni reglas validadas.

## Identificacion y limite de la fuente

| Campo | Resultado de la revision |
|---|---|
| Documento recibido | Proyecto de directiva general para el procedimiento administrativo disciplinario en el Gobierno Regional Huanuco |
| Ubicacion | Archivo entregado por el usuario fuera del repositorio; pendiente de catalogacion institucional |
| SHA-256 | `038AE5C432C25876C61A234E08F55DC95ED124493D806F4CCA0EDB269CD76869` |
| Extension y legibilidad | 54 paginas PDF con texto extraible; los graficos 2 y 3 de las paginas PDF 53 y 54 fueron revisados visualmente |
| Fecha de consulta | 2026-10-20 |
| Estado observado | Portada rotulada «PROPUESTA» y cuadros de firma sin completar, pagina PDF 1; control de cambios con campos pendientes, pagina PDF 3 |
| Vigencia de sus reglas | EVIDENCIA-INSUFICIENTE. No se aporto acto aprobatorio ni comprobacion de vigencia y aplicabilidad de cada fuente juridica citada |
| Uso autorizado en este analisis | Evidencia de lo que el borrador propone; no sustento normativo de una linea base |

El [mapa institucional Nivel 1 aprobado, rama S1](../02-procesos/mapa-de-procesos-institucional/mapa-procesos-nivel-1-s1.md) identifica **S1.4 Administracion de las personas** y la ficha S1 situa alli «Informes y resoluciones de procedimientos disciplinarios» (paginas PDF 25 y 110-111 del mapa). El numeral 5.4.1 de este proyecto de directiva, pagina PDF 9, menciona «Gestion del Regimen Disciplinario y Procedimiento Administrativo Sancionador» sin codigo de Nivel 2. S1.4 es el anclaje aprobado; el nombre y codigo de un eventual hijo PAD siguen pendientes.

## Evidencia observada para modelar

| Bloque descrito por el borrador | Evidencia en el PDF | Actuaciones y salidas mencionadas |
|---|---|---|
| Recepcion e investigacion preliminar | Numerales 6.1.8, 6.2, 6.4, 6.5 y 6.8.1; paginas 16-20 y 22-23 | Recepcion de denuncia, reporte o informe de control; investigacion y precalificacion; proveido de no ha lugar o informe de precalificacion remitido al organo instructor. Anexos 2-6, paginas 40-45. |
| Instruccion | Numerales 6.8.2-6.8.14; paginas 23-25 | Evaluacion por organo instructor, acto de inicio, notificacion, descargos, informe de instruccion al organo sancionador. Anexos 1, 7 y 8, paginas 39 y 46-47. |
| Decision sancionadora o archivo | Numerales 6.8.15-6.8.23; paginas 25-27 | Comunicacion del informe, eventual informe oral y decision final. Anexos 9 y 10, paginas 48-49. |
| Actuaciones posteriores y transversales | Numerales 6.10-6.19 y IX; paginas 28-37 | Control de prescripcion, medidas cautelares, notificaciones, recursos, registros y custodia. El grafico 3, pagina 54, incluye segunda instancia. |

Estas filas describen **lo escrito en el borrador**, no una observacion de la practica actual del Gobierno Regional ni una exigencia normativa corroborada. El [paquete de modelamiento propuesto](propuesta-modelamiento-pad.md) transforma esta evidencia en campos y diagramas candidatos.

## Discrepancias y puntos de control

| ID | Evidencia observada | Consecuencia para el modelamiento |
|---|---|---|
| PAD-01 | La portada usa `Nº 01-E2-DI-GRA-SGGRH-V1.0`; la pagina 2, `DI-SGGRH-001`; la cabecera, version `2.0` (paginas 1-3). | Confirmar identificador, version y documento que reemplazaria antes de registrar una fuente vigente. |
| PAD-02 | Firmas y sellos de la portada vacios; informe de sustento de la hoja de cambios con puntos suspensivos (paginas 1 y 3). | No atribuir formulacion, revision, aprobacion ni vigencia. |
| PAD-03 | El numeral `4.5` se usa dos veces para reglas de aplicacion y exclusiones (paginas 7-8). | Aclarar citas precisas antes de derivar reglas o controles. |
| PAD-04 | Las definiciones de denunciante y ex servidor mencionan al MEF; tambien aparecen MEF en competencia de comision y una directiva del MEF sobre hostigamiento sexual (paginas 9, 23 y 37). | Confirmar si son residuos de otra entidad. No trasladarlos a carriles, alcance ni fichas del GRH. |
| PAD-05 | El numeral 6.6.1 excluye la amonestacion verbal del PAD; los numerales 6.8.3 y 6.8.16 la incluyen en listas de organos de las fases del PAD (paginas 20, 23 y 25). | Resolver el limite del proceso antes de diagramar esa variante. |
| PAD-06 | El texto admite denuncia anonima y a la vez enumera identificacion y firma como contenido minimo (pagina 18). | Precisar la excepcion y sus condiciones antes de una compuerta de admision. |
| PAD-07 | El original del expediente se custodia en Secretaria Tecnica durante el PAD y luego en Recursos Humanos; el punto de entrega no esta descompuesto en tareas (paginas 31-32). | EVIDENCIA-INSUFICIENTE para un flujo de transferencia detallado. |
| PAD-08 | El apartado de edictos habla de Fiscalia, delito, Fiscal, Distrito Fiscal y Ministerio Publico (pagina 36). | Someter esa seccion a depuracion juridica; no incorporarla al procedimiento de notificacion del PAD. |
| PAD-09 | El grafico 3 muestra plazos y segunda instancia, pero no representa las ramas de «no ha lugar», organo incompetente, prescripcion, cautelares o nulidad (pagina 54 frente a paginas 19-31). | Usar el grafico como vista recibida, no como BPMN completo ni como fuente exclusiva de decisiones. |
| PAD-10 | Las paginas 33-38 proponen diversos canales de notificacion, incluida mensajeria y publicaciones; no se aporta verificacion de habilitacion, seguridad ni aplicabilidad para cada canal. | EVIDENCIA-INSUFICIENTE para seleccionar canales validos o automatizar notificaciones. |

## Separacion de clases de conocimiento

- **Evidencia observada:** las denominaciones, actuaciones, documentos y graficos que aparecen en las paginas citadas.
- **Exigencia normativa:** ninguna regla del PDF se adopta como tal en esta revision. La [NT 002-2025-PCM-SGP](https://www.gob.pe/institucion/pcm/normas-legales/6501954-002-2025-pcm-sgp) es la fuente oficial del formato de artefactos; consulta 2026-10-20. Su aplicacion concreta se rige por el [estandar de artefactos](../00-gobernanza/estandar-artefactos-modelamiento.md).
- **Inferencia:** el PAD se ubica bajo S1.4 por el producto disciplinario de la ficha aprobada S1 y el numeral 5.4.1 del borrador. Falta la descomposicion institucional de S1.4.
- **Propuesta:** la arquitectura de fichas y diagramas del documento relacionado, pendiente de contraste con el equipo y con fuentes oficiales vigentes.

## Pendientes

1. Obtener el codigo NT, nivel, nombre y dueno institucional de un eventual proceso PAD **hijo de S1.4**. El analisis de la fuente permanece en esta bandeja; el [paquete de modelos y formatos de trabajo](../02-procesos/S1-gestion-del-recurso-humano/S1-4-administracion-de-las-personas/modelos-pad/00-modelos-pad.md) se agrupa bajo S1.4 sin atribuirle un codigo al hijo.
2. Solicitar la directiva vigente y el acto que eventualmente apruebe o sustituya este borrador; contrastar versiones y observaciones de socializacion.
3. Revisar con personal competente las discrepancias PAD-01 a PAD-10, especialmente las de competencia, notificacion, prescripcion y segunda instancia.
4. Corroborar cada regla juridica en fuente oficial, con fecha, vigencia y ubicacion precisa, mediante el [protocolo de conocimiento confiable](../00-gobernanza/protocolo-conocimiento-confiable.md) antes de usarla como sustento normativo.
5. Obtener evidencia de la ejecucion actual para construir un AS-IS; el PDF, por ser propuesta, no demuestra como opera hoy el PAD.

## Relaciones

- Produce: [Propuesta de modelamiento PAD](propuesta-modelamiento-pad.md).
- Se rige por: [Estandar de artefactos](../00-gobernanza/estandar-artefactos-modelamiento.md).
- Se rige por: [Protocolo de conocimiento confiable](../00-gobernanza/protocolo-conocimiento-confiable.md).
