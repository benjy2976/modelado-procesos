---
id: CON-GUIA-ROF-GRH-2023
tipo: nota-conocimiento
area: conocimiento
estado_documento: BORRADOR
clase_conocimiento: NORMATIVO
proceso:
  - S4.3.2.2
  - S4.3.2.3
fecha_creacion: 2026-11-03
fecha_actualizacion: 2026-11-04
responsable: equipo-proyecto
confidencialidad: INTERNO
aliases:
  - Guia del ROF del Gobierno Regional Huanuco 2023
tags:
  - tema/conocimiento
  - tema/referencias
---

# Guia de lectura: ROF del Gobierno Regional Huanuco 2023

Sube a: [Guias de lectura de fuentes](00-fuentes.md)

Guia para localizar las disposiciones institucionales que distribuyen competencias entre la Gerencia Regional de Infraestructura (GRI), la Sub Gerencia de Estudios (SGE) y la Sub Gerencia de Gestion de Obras y Supervision (SGGOS). Es una propuesta de lectura preparada por IA y requiere validacion humana conforme al protocolo de conocimiento confiable.

## Identificacion

| Campo | Ordenanza aprobatoria | Reglamento de Organizacion y Funciones |
|---|---|---|
| Catalogo | `LOC-006` | `LOC-007` |
| Original | [Ordenanza Regional N.° 013-2023-GRH-CR](../../01-referencias/01-institucionales-grh/originales/ordenanza-regional-013-2023-grh-cr.pdf) | [ROF del Gobierno Regional Huanuco](../../01-referencias/01-institucionales-grh/originales/reglamento-organizacion-funciones-grh-2023.pdf) |
| Vista OCR | [Markdown](../../01-referencias/01-institucionales-grh/derivados-ocr/ordenanza-regional-013-2023-grh-cr.md) · [JSONL](../../01-referencias/01-institucionales-grh/derivados-ocr/ordenanza-regional-013-2023-grh-cr.jsonl) | [Markdown](../../01-referencias/01-institucionales-grh/derivados-ocr/reglamento-organizacion-funciones-grh-2023.md) · [JSONL](../../01-referencias/01-institucionales-grh/derivados-ocr/reglamento-organizacion-funciones-grh-2023.jsonl) |
| SHA-256 | `674E49FF9814BC1244BC17026363B0A5B2A8CF67620AA5D472564FC1A9B3A08D` | `71778D14CC60B83B798B607CD63B26B897BFB81CD87D8BE856848A7BCC47D8DA` |
| Fecha del documento | 2023-10-17 | 2023-10-17 |
| Fecha de consulta | 2026-11-03 | 2026-11-03 |

## Disposiciones relevantes

| Tema | Lectura propuesta | Ubicacion precisa | Clase |
|---|---|---|---|
| Aprobacion | La Ordenanza Regional aprueba el ROF que forma parte integrante de ella | Ordenanza, art. primero, PDF p. 5 | `EXIGENCIA-NORMATIVA` |
| Derogacion | Se deroga el ROF anterior aprobado mediante Ordenanza Regional N.° 040-2020-GRH-CR y sus modificaciones listadas | Ordenanza, art. tercero, PDF pp. 5-6 | `EXIGENCIA-NORMATIVA` |
| Vigencia | La ordenanza entra en vigencia al dia siguiente de su publicacion en el diario oficial | Ordenanza, art. quinto, PDF p. 6 | `EXIGENCIA-NORMATIVA`; fecha efectiva de publicacion pendiente de registrar |
| OACGD | La Oficina de Atencion al Ciudadano y Gestion Documental recibe, registra, clasifica, deriva, distribuye y tramita los documentos que ingresan por mesa de partes | ROF, art. 20, PDF p. 15, numeracion impresa p. 14 | `EXIGENCIA-NORMATIVA` |
| SGE | Es una unidad organica de linea dependiente de la GRI y responsable de los expedientes tecnicos | ROF, art. 95, PDF p. 47, numeracion impresa p. 46 | `EXIGENCIA-NORMATIVA` |
| Absolucion de consultas | La SGE tiene la funcion de absolver consultas sobre ocurrencias en la ejecucion de obras de inversiones publicas e IOARR | ROF, art. 96, lit. i, PDF p. 47, numeracion impresa p. 46 | `EXIGENCIA-NORMATIVA` |
| SGGOS | Es responsable del control y seguimiento de la ejecucion de las obras de inversion publica | ROF, art. 97, PDF p. 47, numeracion impresa p. 46 | `EXIGENCIA-NORMATIVA` |
| Pronunciamientos de SGGOS | Puede emitir pronunciamientos u opiniones dentro de su competencia | ROF, art. 98, lit. o, PDF p. 48, numeracion impresa p. 47 | `EXIGENCIA-NORMATIVA` |
| GRAJ | La Gerencia Regional de Asesoria Juridica asesora a los organos de la entidad, emite opiniones legales y revisa o visa actos dentro de su competencia | ROF, arts. 44-45, PDF p. 24, numeracion impresa p. 22 | `EXIGENCIA-NORMATIVA` |
| Presupuesto | La Subgerencia de Presupuesto Publico es responsable del proceso presupuestario y efectua seguimiento de la disponibilidad presupuestaria | ROF, art. 51, PDF pp. 26-27, numeracion impresa pp. 24-25 | `EXIGENCIA-NORMATIVA` |
| GRI | La Gerencia Regional de Infraestructura dirige y monitorea la ejecucion de los proyectos de inversion y expide resoluciones en materias de su competencia | ROF, arts. 92-93, PDF p. 46, numeracion impresa pp. 44-45 | `EXIGENCIA-NORMATIVA` |

## Aplicacion propuesta a S4.3.2.2

- La frase de la normativa nacional segun la cual la entidad absuelve una consulta no debe permanecer como una actividad institucional generica en el modelo del GORE Huanuco.
- La absolucion tecnica sobre ocurrencias de obra se asigna a la SGE porque el articulo 96, literal i, lo dispone expresamente.
- La SGGOS mantiene el control y seguimiento de la ejecucion. Su participacion en la recepcion, seguimiento y canalizacion de la consulta hacia la SGE combina la competencia del ROF con la evidencia operativa aportada por el equipo y registrada en `DEC-033`; no se presenta como una secuencia impuesta literalmente por el ROF.
- La intervencion del proyectista produce una opinion tecnica de apoyo; no desplaza la competencia institucional de la SGE para absolver la consulta cuando corresponda a la entidad.
- El ROF no basta por si solo para identificar quien firma o notifica el documento final. Para S4.3.2.2, `DEC-033` registra como evidencia operativa del equipo que los especialistas de la SGE elaboran el informe tecnico y el Subgerente de Estudios firma siempre la respuesta. Esta precision permite modelar la responsabilidad, pero no se convierte en exigencia normativa ni en regla validada.

## Consecuencia para el diagrama

El pool del Gobierno Regional Huanuco se desagrega en carriles para la Oficina de Atencion al Ciudadano y Gestion Documental, SGGOS, especialistas de la SGE y Subgerente de Estudios. Esta distribucion combina las competencias del ROF con la evidencia operativa registrada en `DEC-033`: Mesa de Partes registra y deriva, la SGGOS sigue y canaliza, los especialistas de la SGE elaboran el informe tecnico y el Subgerente de Estudios firma la respuesta.

El contratista, la supervision contratada y el proyectista se representan como participantes separados porque conservan control propio sobre sus actividades y se comunican con la entidad mediante mensajes. El inspector, cuando sustituye a una supervision contratada, pertenece a la entidad y requiere una variante del modelo; no debe representarse como pool externo.

## Aplicacion propuesta a S4.3.2.3

- OACGD recibe, registra, deriva y notifica; no evalua el fondo tecnico de una modificacion.
- SGGOS es la unidad candidata para articular y seguir el expediente por su competencia de control y seguimiento de obras. La secuencia concreta y el rol del monitor o coordinador son una inferencia basada tambien en el Bizagi observado y requieren validacion operativa.
- SGE interviene cuando la figura exige opinion del organo responsable de los expedientes tecnicos. Los articulos 95-96 permiten identificar a SGE como ese organo en el GORE, pero no hacen obligatoria su participacion en toda modificacion.
- Presupuesto y GRAJ intervienen solo cuando la figura y el contenido del expediente requieren disponibilidad presupuestal u opinion o revision legal. El ROF distribuye competencias; no establece por si solo una secuencia universal.
- GRI puede integrar y elevar el expediente en la propuesta, pero debe confirmarse quien remite formalmente a la Contraloria y quien suscribe cada acto.
- El ROF no sustituye la resolucion o acto de delegacion vigente. Por ello, el diagrama mantiene el carril generico "Autoridad competente segun figura y umbral" y registra la firma como `EVIDENCIA-INSUFICIENTE`.

## Alertas

- Esta guia no tiene estado `VALIDADO` y no atribuye conformidad a ninguna unidad o persona.
- La vigencia material del ROF depende de la publicacion prevista por la ordenanza y de modificatorias posteriores; ambas verificaciones deben mantenerse en la trazabilidad normativa.
- Las vistas OCR son auxiliares. Ante diferencias de lectura, prevalece el PDF original.
