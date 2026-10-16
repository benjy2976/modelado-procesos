---
tipo: mapa-de-contenido
area: referencias
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# Referencias

[Inicio](../00-inicio.md)

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

- [Institucionales GRH](01-institucionales-grh/originales/README.md)
- [Gestion por procesos](02-gestion-por-procesos/originales/README.md)
- [Invierte.pe](03-invierte-pe/README.md)
- [Contrataciones publicas](04-contrataciones-publicas/README.md)
- [Control gubernamental](05-control-gubernamental/README.md)
- [Presupuesto y administracion](06-presupuesto-y-administracion/README.md)
- [Normativa tecnica sectorial](07-normativa-tecnica-sectorial/README.md)
- [Biblioteca BIM](08-bim/README.md)
- [Derivados de texto](09-derivados-texto/README.md): cache regenerable; no reemplaza los originales.

## Relaciones

- Se rige por el [Manual operativo del conocimiento](../00-gobernanza/manual-operativo-del-conocimiento.md).
- Alimenta [Conocimiento estructurado](../03-conocimiento/README.md).
- Se automatiza mediante [Herramientas](../05-herramientas/README.md).
