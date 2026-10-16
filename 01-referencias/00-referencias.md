---
tipo: mapa-de-contenido
area: referencias
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
aliases:
  - Referencias
---

# Referencias

Sube a: [Inicio de la boveda](../00-inicio.md)

Esta area conserva documentos externos e institucionales. Los originales son inmutables.

Los binarios de fuentes publicas de las areas `02` a `08` funcionan como una cache local regenerable: no se incorporan a Git. Git conserva el indice con URL y SHA-256, la configuracion de fuentes y el descargador. Despues de clonar el repositorio se restauran con:

```powershell
python 05-herramientas/catalogador-documental/descargar_recursos.py --modo restaurar
```

Los documentos institucionales no reproducibles se evaluan individualmente. Los documentos aprobados sin restricciones pueden conservarse mediante Git LFS; expedientes y evidencia sensible deben permanecer en almacenamiento institucional controlado y en Git solo se registra su referencia.

Cada recurso debe registrarse en `00-catalogo/catalogo-documental.csv`. Si requiere OCR, la salida se almacena como derivado y nunca reemplaza al original.

## Catalogo y control

- [Plan de descargas](00-catalogo/plan-descargas.md)
- [Rubrica de calidad](00-catalogo/rubrica-calidad.md)
- [Resumen de calidad documental](00-catalogo/resumen-calidad-documental.md)
- [Revision visual de la muestra](00-catalogo/revision-visual-muestra.md)
- [Pendientes y limitaciones](00-catalogo/pendientes-y-limitaciones.md)

## Materias

- [Institucionales GRH](01-institucionales-grh/originales/00-originales-institucionales-grh.md)
- [Gestion por procesos](02-gestion-por-procesos/originales/00-originales-gestion-por-procesos.md)
- [Invierte.pe](03-invierte-pe/00-invierte-pe.md)
- [Contrataciones publicas](04-contrataciones-publicas/00-contrataciones-publicas.md)
- [Control gubernamental](05-control-gubernamental/00-control-gubernamental.md)
- [Presupuesto y administracion](06-presupuesto-y-administracion/00-presupuesto-y-administracion.md)
- [Normativa tecnica sectorial](07-normativa-tecnica-sectorial/00-normativa-tecnica-sectorial.md)
- [Biblioteca BIM](08-bim/00-bim.md)
- [Derivados de texto](09-derivados-texto/00-derivados-texto.md): cache regenerable; no reemplaza los originales.

## Relaciones

- Se rige por el [Manual operativo del conocimiento](../00-gobernanza/manual-operativo-del-conocimiento.md).
- Alimenta [Conocimiento estructurado](../03-conocimiento/00-conocimiento.md).
- Se automatiza mediante [Herramientas](../05-herramientas/00-herramientas.md).
