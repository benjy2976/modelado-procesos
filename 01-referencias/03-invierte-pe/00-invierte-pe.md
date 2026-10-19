---
tipo: mapa-de-contenido
area: invierte-pe
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
aliases:
  - Invierte.pe
tags:
  - tema/invierte-pe
---

# Invierte.pe

Sube a: [Referencias](../00-REFERENCIAS.md)

Normas, directivas, anexos, formatos y documentos de orientacion vigentes del Sistema Nacional de Programacion Multianual y Gestion de Inversiones.

## Contenido por carpeta

- `marco-legal/`: Decreto Legislativo 1252 y reglamentos, incluido el vigente DS 140-2026-EF.
- `directiva-general/`: Directiva 001-2019-EF/63.01 actualizada.
- `cierre-inversiones/`: RD 0002-2025-EF/63.01, Formato 09 y nota tecnica; RD 0018-2025-EF/63.01.
- `formatos-ejecucion/`: [Formato N 08-A, actualizacion del 18/02/2026](https://www.mef.gob.pe/es/anexos-y-formatos) (`INV-005A`, XLSX) e instructivo de 2019 (`INV-005`, PDF). El formato es una cache local restaurable desde el indice de descargas; el instructivo se conserva como referencia historica.
- `obras-por-impuestos/`: TUO de la Ley 29230, su reglamento y modificatoria (`INV-006`, `INV-006A`, `INV-006B`).

## Descargar el Formato 08-A

En la [pagina oficial de anexos y formatos del MEF](https://www.mef.gob.pe/es/anexos-y-formatos), seleccionar **Formato N 08-A**. El enlace directo comprobado el 2026-10-19 es [formato8a_directiva001_2019EF6301_2026_1.xlsx](https://mef.gob.pe/contenidos/inv_publica/anexos/formato8a_directiva001_2019EF6301_2026_1.xlsx). Guardar el archivo como `01-referencias/03-invierte-pe/formatos-ejecucion/formato-08-a.xlsx` solo si aun no existe; no sustituir una copia sin comparar el hash.

El SHA-256 de la copia incorporada es `FB2A4B00F9F9666401E433DE5C41C296F065520D8F6F739B8F09D76E81A3F5E3`. Tras clonar el repositorio, este comando recupera el archivo si falta y comprueba ese hash. Revisa todos los recursos ausentes del indice.

```powershell
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/descargar_recursos.py --modo restaurar
```
