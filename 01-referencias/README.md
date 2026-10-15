# Referencias

Esta area conserva documentos externos e institucionales. Los originales son inmutables.

Los binarios de fuentes publicas de las areas `02` a `08` funcionan como una cache local regenerable: no se incorporan a Git. Git conserva el indice con URL y SHA-256, la configuracion de fuentes y el descargador. Despues de clonar el repositorio se restauran con:

```powershell
python 05-herramientas/catalogador-documental/descargar_recursos.py --modo restaurar
```

Los documentos institucionales no reproducibles se evaluan individualmente. Los documentos aprobados sin restricciones pueden conservarse mediante Git LFS; expedientes y evidencia sensible deben permanecer en almacenamiento institucional controlado y en Git solo se registra su referencia.

Cada recurso debe registrarse en `00-catalogo/catalogo-documental.csv`. Si requiere OCR, la salida se almacena como derivado y nunca reemplaza al original.

La carpeta se organiza por materia:

- `01-institucionales-grh`
- `02-gestion-por-procesos`
- `03-invierte-pe`
- `04-contrataciones-publicas`
- `05-control-gubernamental`
- `06-presupuesto-y-administracion`
- `07-normativa-tecnica-sectorial`
- `08-bim`
- `09-derivados-texto`: cache Markdown regenerable para busqueda y apoyo de IA; no reemplaza los originales.
