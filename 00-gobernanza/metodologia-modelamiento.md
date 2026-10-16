---
id: GOV-METODOLOGIA-MODELAMIENTO
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: DECISION
proceso:
  - S4.3
fecha_creacion: 2026-10-14
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
---

# Metodologia de modelamiento

Secuencia de trabajo para documentar cada proceso con la estructura de `DEC-017`: carpetas jerarquizadas por codigo, documentos conforme a la NT 002-2025-PCM-SGP y estado registrado en metadatos. Las rutas y nombres de archivo se definen en el [estandar de artefactos](estandar-artefactos-modelamiento.md).

## Documentacion del proceso

1. Delimitar inicio, fin, entradas, productos, receptores y exclusiones en la portada y el sustento del proceso.
2. Identificar fuentes normativas, institucionales y evidencias reales, y registrarlas en el sustento.
3. Preparar extracciones trazables y reglas normativas propuestas.
4. Obtener validacion especializada de las reglas que condicionan el alcance.
5. Construir el paquete de contexto autorizado para la tarea.
6. Levantar el proceso mediante entrevistas y recorrido de casos; registrar cada dato en el sustento como observado, normativo, referencia, inferencia o propuesta.
7. Elaborar la ficha de producto y proceso con los campos del Anexo 2.
8. Construir el diagrama del proceso: modelo logico PlantUML durante el levantamiento y BPMN 2.0 formal al consolidarse.
9. Determinar los procesos del nivel siguiente y repetir los pasos 6 a 8 en la carpeta de cada uno hasta el ultimo nivel.
10. Definir las fichas de indicador (Anexo 4) y, en el ultimo nivel, riesgos, registros y procedimiento cuando cumpla los criterios del numeral 6.1.3 d.
11. Ejecutar revision independiente de trazabilidad y consistencia.

## Circuito de revision

12. Llevar cada documento por los niveles `ELABORACION`, `REVISION-EQUIPO`, `OPINION-TECNICA` y `APROBACION`, registrando cada conformidad en el historial del sustento. Una observacion devuelve el documento a `ELABORACION`.
13. Al aprobarse, marcar `APROBADO`, publicar la linea base mediante tag y exportar los PDF derivados.

## Etapa posterior

14. Analizar tiempos, problemas, riesgos, controles, cumplimiento e intercambios de informacion, y disenar el TO-BE en `02-procesos/to-be/`. Esta etapa esta pendiente y requiere decision expresa para iniciarse.

## Capas complementarias

- Proceso: eventos, actividades, decisiones y participantes.
- Informacion: documentos, modelos, registros, sistemas, proposito de uso y estado de revision/aprobacion.
- Cumplimiento: normas, articulos, reglas y evidencias.
- Desempeno: tiempo, costo, calidad, riesgo e indicadores.

## Puerta normativa

Una regla pendiente puede orientar la investigacion, pero no sustentar por si sola una linea base publicada. Para usos normativos debe encontrarse en estado `VALIDADO`; si cambia su fuente o alcance, pasa a `REVALIDACION-REQUERIDA` y se revisa su impacto en los modelos relacionados.

## Relaciones

- [Estandar de artefactos](estandar-artefactos-modelamiento.md)
- [Procesos](../02-procesos/00-PROCESOS.md)
- [Plantillas de procesos](plantillas/00-plantillas.md)
- [Manual operativo del conocimiento](manual-operativo-del-conocimiento.md)
