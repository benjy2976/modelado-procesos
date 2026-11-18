---
id: CON-GUIA-OPINION-092
tipo: nota-conocimiento
area: conocimiento
estado_documento: BORRADOR
clase_conocimiento: NORMATIVO
proceso:
  - S4.3.2.2
  - S4.3.2.3
fecha_creacion: 2026-11-18
fecha_actualizacion: 2026-11-18
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/conocimiento
  - tema/contrataciones
---

# Opinion D000092-2026-OECE-DTN

Sube a: [Guias de lectura](00-fuentes.md)

Criterio interpretativo oficial incorporado como conocimiento propuesto por IA. No acredita aprobacion de un caso ni validacion normativa institucional.

## Identificacion y control

| Campo | Registro |
|---|---|
| Catalogo | `CON-010` |
| Fuente oficial | [Ficha OECE](https://www.gob.pe/institucion/oece/informes-publicaciones/8596051-opinion-n-d000092-2026-oece-dtn); [descarga oficial](https://cdn.www.gob.pe/uploads/document/file/10621119/8596051-opinion-d092-2026-oece-dtn.pdf?v=1789430079) |
| Documento local | [PDF](../../01-referencias/04-contrataciones-publicas/opiniones-oece/opinion-d000092-2026-oece-dtn.pdf) |
| Fecha | 2026-08-27, segun ficha oficial |
| Consulta | 2026-11-18 |
| SHA-256 | `BA387F8733A82F17A84C11BD4DE9957BB22F7DEF91746BB90E8CBD706B71521C` |
| Legibilidad | 11 paginas; todas con texto nativo; no requiere OCR |
| Vigencia | Interpretacion de Ley 32069 y DS 009-2025-EF modificado por DS 001-2026-EF. No se presume aplicabilidad a Ley 30225 ni administracion directa. Control de criterios posteriores y validacion especializada pendientes. |
| Verificacion | Descarga oficial y hash local; lectura textual y revision visual focalizada de paginas relevantes. No se verifico criptograficamente la firma ni se atribuye validacion humana. |

El PDF se conserva como recurso publico regenerable, excluido de Git conforme a la politica del repositorio. URL, hash y ruta quedan en los catalogos y registro de descargas; la guia y las reglas se versionan. La extraccion de consulta vive en `01-referencias/09-derivados-texto/cache/CON-010/opinion-d000092-2026-oece-dtn.txt` y no sustituye el original.

## Lectura para el modelo

| Materia | Parafrasis del criterio | Ubicacion PDF |
|---|---|---|
| Inicio y computo | El procedimiento inicia con la anotacion de necesidad; los 15 dias se cuentan desde el dia siguiente, independientemente del plazo para ratificar | 2.1, p. 2; 3.1, pp. 8-9 |
| Presentacion | La presentacion efectiva exige ratificacion de supervision; su demora no suspende ni afecta el transcurso del plazo | 2.2-2.3, p. 3; 3.2-3.3, p. 9 |
| Plazo adicional | El adicional de 15 dias es minimo, puede ser mayor con sustento objetivo; la solicitud posterior al vencimiento no impide por si sola su otorgamiento | 2.5-2.7, pp. 4-5; 3.6-3.7, pp. 9-10 |
| Elaborador contratista | Presenta ante entidad y supervisor; supervision tiene 10 dias y la opinion del proyectista u organo tecnico se emite en el mismo plazo | 2.9 A, p. 6; 3.9, p. 10 |
| Elaborador supervisor | Presenta a entidad; 12 dias habiles para resolucion desde el dia siguiente de recibir expediente; opinion previa del proyectista u organo tecnico | 2.9 B, p. 6; 3.10, p. 10 |
| Elaborador entidad | Presenta a supervision para opinion; luego entidad notifica resolucion dentro del plazo de 12 dias habiles. Si procede por antiguedad, interviene proyectista | 2.9 C, p. 6; 3.11, p. 10 |
| Opinion tecnica previa | Primero proyectista si no paso mas de un anio de conformidad; en defecto, organo competente. Precisa supuesto inoficioso cuando elabora entidad y no corresponde proyectista | 2.8, p. 5; 3.8, p. 10 |
| Incidencia neta | Restar deductivos vinculados tambien para el tramo superior al 30 % y hasta 50 %; no descontar reducciones independientes u otras modificaciones | 2.10, pp. 7-8; 3.12-3.13, p. 11 |
| Notificacion | Distingue la funcionalidad SEACE/Pladicop y el regimen transitorio de notificacion al domicilio o correo contractual | 2.11, p. 8; 3.14-3.15, p. 11 |

## Aplicacion y limites

**Propuesta:** recibir la respuesta de S4.3.2.2 como antecedente, anotar la necesidad especifica y conservar la fecha de esa anotacion para el computo. La opinion no convierte la consulta en aprobacion del adicional ni obliga a repetir una anotacion ya valida. La independencia de ambos procedimientos se sustenta en la [Opinion D000083](guia-opinion-d000083-2026-oece-dtn.md).

La nota al pie 4 de p. 2 exige comunicar la ratificacion al contratista o al organo elaborador, segun corresponda. Por ello, la tabla diferencia el inicio de elaboracion de la condicion para presentar. No se suman 5 dias de ratificacion mas 15 nuevos de elaboracion.

El criterio de 2.9 C habla del plazo correspondiente para supervision; no enuncia alli un plazo numerico autonomo para el caso de elaboracion por entidad. La tabla lo distingue de los 10 dias expresos para contratista, conservando la precision numerica como pendiente de validacion. La Opinion resuelve la secuencia que antes se habia marcado enteramente como insuficiente.

La nota sobre funcionalidades de SEACE describe la situacion a la fecha de la opinion; no acredita su estado operativo al 18-11-2026. El canal de notificacion se verifica por contrato y fecha. No se introducen penalidades automaticas: dependen de bases y supuesto, conforme 2.4 y 3.4-3.5.

## Reglas propuestas y relaciones

- [REG-CON-ADIC-003: inicio del computo](../reglas/reg-con-adic-003.yaml).
- [REG-CON-ADIC-004: ratificacion para presentar](../reglas/reg-con-adic-004.yaml).
- [REG-CON-ADIC-005: demora sin suspension](../reglas/reg-con-adic-005.yaml).
- [Sustento S4.3.2.3](../../02-procesos/S4-gestion-de-las-inversiones/S4-3-ejecucion-inversion/S4-3-2-ejecucion/S4-3-2-3-gestion-modificaciones-alcance/S4-3-2-3-sustento.md).

Pendiente: validacion especializada, bases y caso concreto. El enlace de LP aportado por el usuario sirvio para localizar el documento; el sustento se toma del PDF oficial.
