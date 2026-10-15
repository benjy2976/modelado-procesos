# Plan de descargas y evaluacion

El lote base fue descargado y evaluado el 2026-10-14. Los binarios publicos funcionan como cache local regenerable y no se versionan en Git; el indice de URL y SHA-256 si se versiona.

Para reconstruir la biblioteca despues de clonar:

```powershell
python 05-herramientas/catalogador-documental/descargar_recursos.py --modo restaurar
```

## Orden propuesto

### Lote 1 - Metodo y BIM

- Norma Tecnica y Guia practica de Gestion por Procesos.
- Guia Nacional BIM y Guia Tecnica BIM.
- Lineamientos de adopcion, guia openBIM y practicas colaborativas.
- Nota tecnica de recursos tecnologicos y tipologias obligatorias.
- Plantillas EIR, BEP, CCA, matriz de responsabilidades, MIDP y TIDP.

### Lote 2 - Invierte.pe

- Decreto Legislativo 1252 y reglamento actualizado.
- Directiva General 001-2019-EF/63.01 consolidada.
- Anexos y formatos de ejecucion y cierre.

### Lote 3 - Contrataciones

- Ley 32069 consolidada.
- Reglamento consolidado y modificatorias.
- Directivas, bases estandar y orientaciones aplicables a ejecucion contractual.

### Lote 4 - Control y administracion directa

- Directiva 017-2023-CG/GMPL, directriz y anexos.
- INFOBRAS y Cuaderno de Obra Digital.
- Control simultaneo y control concurrente.

### Lote 5 - Presupuesto y normativa tecnica

- Normas anuales que afecten ejecucion.
- Reglamento Nacional de Edificaciones.
- Normativa sectorial de la tipologia elegida para el piloto.

### Lote 6 - Institucional

Se solicita o localiza dentro del GRH. No todo estara publicado en internet.

## Flujo por archivo

1. Abrir la pagina oficial y verificar emisor, fecha y modificatorias.
2. Descargar sin cambiar el archivo original.
3. Calcular SHA-256 y registrar URL, fecha de consulta, tamano y formato.
4. Medir paginas, texto extraible y orden de lectura.
5. Renderizar una muestra de paginas para control visual.
6. Asignar estado OCR y puntajes de la rubrica.
7. Crear OCR derivado solo si es necesario.
8. Volver a medir y conservar la evaluacion antes/despues.
9. Crear resumen y relaciones con procesos solamente despues de verificar calidad.

## Recursos que pueden requerir busqueda o acceso interno

- Resolucion o acto que aprueba el mapa de procesos version 3.0.
- ROF y documentos de organizacion vigentes con sus modificaciones.
- Directivas internas de ejecucion de obras, supervision, valorizaciones, adicionales, ampliaciones, recepcion y liquidacion.
- Formatos y listas de verificacion realmente utilizados.
- Convenios y reglas para modalidades especiales.
- Expedientes anonimizados representativos.
- Manuales o instructivos de sistemas internos.
- Plan o diagnostico institucional de adopcion BIM, si existe.
- EIR, BEP o pilotos BIM previos del GRH.
- Acceso legal a normas ISO o NTP que no sean de libre descarga.

## Criterio de parada

No descargar colecciones completas solo por disponibilidad. Si una familia normativa depende de la tipologia o modalidad, primero se define el piloto y luego se incorpora el subconjunto aplicable.
