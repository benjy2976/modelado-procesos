---
id: AP-S4-3-2-5-SUSTENTO
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: REFERENCIA
codigo_proceso: S4.3.2.5
nivel_proceso: 3
proceso:
  - S4.3.2.5
fecha_creacion: 2026-11-05
fecha_actualizacion: 2026-11-05
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-5
---

# S4.3.2.5 Formalizacion de suspensiones de plazo - Sustento

Sube a: [S4.3.2.5 Formalizacion de suspensiones de plazo](00-S4-3-2-5-formalizacion-suspensiones-plazo.md)

## Delimitacion y trazabilidad

Este proceso recibe del anterior S4.3.2.3 la suspension contractual y su reanudacion. `DEC-041` la separa porque depende de una causa que impide continuar, exige coordinacion y acuerdo de las partes y produce actos distintos de una ampliacion o paralizacion.

`DEC-042` corrige la colaboracion: residente y contratista o representante legal son carriles del mismo participante Ejecutor de obra. El residente registra y sustenta la causa; el contratista o su representante expresa la respuesta contractual al acuerdo de suspension cuando corresponde. Control de obra representa alternativamente al supervisor contratado o al inspector de la entidad, sin presumir que pertenezcan a la misma organizacion ni que concurran.

Cuaderno de Incidencias es la denominacion institucional uniforme. La fuente de administracion directa puede usar "cuaderno de obra", pero no existe evidencia suficiente para presumir una figura equivalente de suspension contractual en esa modalidad.

## Fuentes utilizadas

| Fuente | Ubicacion precisa | Estado | Uso |
|---|---|---|---|
| Reglamento de la Ley 32069 | Arts. 107 y 202, PDF pp. 59 y 114-115; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta | Acuerdo de suspension y reanudacion en contrata |
| ROF GRH 2023 | Arts. 20 y 97-98; consulta 2026-11-04 | `EXIGENCIA-NORMATIVA` propuesta e `INFERENCIA` | Registro y seguimiento interno |
| Modelo anterior S4.3.2.3 | Variante agrupada `MOD-PLA-SUS` y ruta de reinicio | Antecedente en Git; propuesta no aprobada | Trazabilidad del contenido redistribuido |
| `DEC-041` | Registro de decisiones | `DECISION` | Codigo, nombre, limites y responsabilidades |

## Elementos registrados

| Elemento | Contenido | Clase | Fuente |
|---|---|---|---|
| Disparadores | Causa que impide continuar; cese de la causa | Normativo citado | Reglamento, arts. 202.1-202.2 |
| Instancias | Una por suspension y otra por reanudacion | Decision del equipo | DEC-041 |
| Productos | Suspension formalizada; reanudacion formalizada | Propuesta | Analisis del flujo |
| Decision | Titular de la competencia o autoridad delegada | Decision del equipo | DEC-041; delegacion concreta pendiente |

## Vacios de evidencia

| Vacio | Marca | Fuente o accion necesaria |
|---|---|---|
| Suspension equivalente en administracion directa | `EVIDENCIA-INSUFICIENTE` | Fuente aplicable y validacion especializada |
| Dueno, delegacion y unidad que prepara el acto | `EVIDENCIA-INSUFICIENTE` | ROF, delegaciones y procedimiento vigente |
| Documento exacto de acuerdo, suspension y reanudacion | `EVIDENCIA-INSUFICIENTE` | Muestras no sensibles y serie documental |
| Criterio y responsable de verificar el cese de la causa | `EVIDENCIA-INSUFICIENTE` | Procedimiento y asignacion funcional |
| Indicador, meta y fuente de datos | `EVIDENCIA-INSUFICIENTE` | Definicion del dueno |

## Informacion BIM

`EVIDENCIA-INSUFICIENTE`.

## Control de trazado

La generacion focalizada del 2026-11-05 deja D1, D2, D3 y D5 sin hallazgos. D4 registra seis advertencias exclusivamente geometricas al consolidar al residente y al contratista o representante en el mismo Ejecutor de obra: los mensajes directos de propuesta y respuesta entre el GORE y el ejecutor atraviesan el pool intermedio Control de obra. La relacion triangular entre ejecutor, control y entidad impide que los tres intercambios sean adyacentes en una disposicion lineal de pools. Se adopta el derivado de trabajo con `--forzar`; queda pendiente revision visual humana y ajuste BPMN-DI antes de una linea base. No se modifica el generador.

## Historial de revision

| Documento | Nivel | Fecha | Resultado | Rol o unidad | Evidencia |
|---|---|---|---|---|---|
| Juego inicial S4.3.2.5 | `ELABORACION` | 2026-11-05 | Propuesta creada; pendiente revision | Equipo del proyecto con asistencia de IA | `DEC-041`; fuentes citadas |
| Precision de participantes | `ELABORACION` | 2026-11-05 | Residente y contratista o representante integrados en Ejecutor de obra con responsabilidades separadas | Equipo del proyecto con asistencia de IA | `DEC-042` |

## Relaciones

- [S4.3.2.6 Gestion de paralizacion y reinicio](../S4-3-2-6-gestion-paralizacion-reinicio/00-S4-3-2-6-gestion-paralizacion-reinicio.md)
- [Sustento de S4.3.2](../S4-3-2-sustento.md)
