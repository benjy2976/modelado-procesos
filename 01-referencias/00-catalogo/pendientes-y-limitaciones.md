---
id: REF-PENDIENTES-LIMITACIONES
tipo: nota-conocimiento
area: referencias
estado_documento: VIGENTE
clase_conocimiento: OBSERVADO
proceso: []
fecha_creacion: 2026-10-15
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/referencias
---
# Pendientes y limitaciones del corpus documental

Fecha de corte: 2026-10-14.

El lote descargado constituye una biblioteca base para modelar la ejecucion de inversiones. No debe interpretarse como una compilacion juridica exhaustiva. Antes de formular una regla de proceso se debe confirmar vigencia, modificatorias y articulo aplicable en la fuente oficial.

## Recursos que requieren gestion interna o acceso licenciado

- Acto aprobatorio y version controlada del mapa y manual de procesos del Gobierno Regional de Huanuco.
- ROF, organigrama y documentos de organizacion vigentes del Gobierno Regional de Huanuco.
- Directivas internas vigentes de ejecucion, supervision, modificaciones, recepcion, liquidacion y transferencia.
- Inventario de sistemas, registros y formatos realmente usados por los equipos de ejecucion.
- Muestras anonimizadas de expedientes de obra por contrata y administracion directa.
- Serie NTP-ISO 19650 aplicable. Debe obtenerse mediante biblioteca, licencia institucional o INACAL; no se descargaran copias no autorizadas.

## Recursos que dependen del alcance del piloto

- Normas tecnicas sectoriales de la tipologia de inversion seleccionada.
- Manuales sectoriales, especificaciones tecnicas y disposiciones del concedente o financiador, cuando correspondan.
- Directivas y bases especiales para obras paralizadas, emergencias, reconstruccion, convenios u Obras por Impuestos, solo si la modalidad entra en alcance.
- Opiniones, pronunciamientos y precedentes del OECE o Contraloria asociados a controversias concretas; se incorporaran por necesidad, no de forma masiva.

## Recursos requeridos por el alcance de S4.3 (2026-10-16)

`DEC-020` incluye en S4.3 todas las inversiones y las modalidades de contrata, administracion directa y Obras por Impuestos. El 2026-10-16 se incorporaron con el descargador (`--modo descubrir`) y se evaluaron:

| ID | Recurso | Situacion |
|---|---|---|
| `INV-005` | Instructivo del Formato N 08-A (MEF, version 2019) | Con texto; leido para el componente de gestion del proyecto |
| `INV-006` | TUO de la Ley 29230 (DS 081-2022-EF) y su anexo | Con texto; pendiente de lectura |
| `INV-006A` | Reglamento de la Ley 29230 (DS 210-2022-EF) y su anexo | Con texto; pendiente de lectura |
| `INV-006B` | DS 011-2024-EF, modifica el reglamento de la Ley 29230 | Con texto; pendiente de lectura |
| `TEC-003` | Ley 29783 de Seguridad y Salud en el Trabajo | **Sin texto: requiere OCR en copia derivada** |
| `TEC-003A` | Reglamento de la Ley 29783 (DS 005-2012-TR) | Con texto; pendiente de lectura |
| `PRES-002` | Directiva 0004-2021-EF/54.01, almacenamiento y distribucion de bienes muebles | Con texto; pendiente de lectura |
| `PRES-002A` | RD 0006-2022-EF/54.01, modifica la Directiva 0004-2021-EF/54.01 | Con texto; pendiente de lectura |

Siguen faltando:

- Formato N 08-A vigente (la pagina de anexos del MEF indica actualizacion al 18-02-2026). El sitio del MEF bloquea la consulta automatizada de esa pagina; se requiere la URL directa del archivo para registrarlo en `fuentes-descarga.json`.
- Modificatorias de la Ley 29783 (Ley 30222) y de su reglamento (DS 006-2014-TR y DS 016-2016-TR).
- Modificatorias de la Ley 29230 posteriores al TUO (Leyes 31735, 32103, 32187 y 32460).
- Decreto Legislativo 1439 del Sistema Nacional de Abastecimiento y su reglamento, si se requiere su marco general.

## Alertas de mantenimiento

- El Reglamento de Invierte.pe vigente descargado es el DS 140-2026-EF, publicado el 18-07-2026. Los documentos anteriores se conservan como antecedentes y no deben tratarse como texto vigente sin revision.
- La Directiva General de Invierte.pe disponible se publica como actualizada a 2025; debe verificarse su adecuacion o modificacion posterior al DS 140-2026-EF antes de modelar obligaciones.
- Los textos consolidados de la Ley 32069 y su Reglamento indican su propia fecha de corte. Debe revisarse si existen modificaciones posteriores a esas fechas.
- El RNE es una coleccion extensa y mutable. Para cada piloto debe seleccionarse la norma tecnica aplicable y comprobarse la ultima modificatoria en MVCS.
- Los PDF marcados para OCR deben procesarse solo como copias derivadas; el original se conserva inmutable.

