---
id: GOV-PLAN-TRABAJO
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
  - tema/gobernanza
---

# Plan de trabajo inicial

## Fase 1 - Preparacion

- Crear estructura y reglas del repositorio.
- Catalogar los archivos existentes.
- Preparar cola y criterios de descarga.

## Fase 2 - Biblioteca

- Descargar por lotes desde fuentes oficiales.
- Verificar identidad, vigencia, hash, formato y accesibilidad.
- Evaluar OCR, estructura y utilidad.
- Crear texto derivado y resumen solo cuando aporte valor.

## Fase 3 - Conocimiento confiable y apoyo de IA

- Implementar extraccion Markdown con hash y marcadores de pagina.
- Crear reglas atomicas y catalogo generado.
- Validar el flujo manual con especialistas del equipo.
- Implementar el validador de esquemas y la web de consulta.
- Implementar el flujo autenticado de revision y validacion.
- Generar paquetes de contexto reproducibles para personas y modelos.

## Fase 4 - Preparacion del piloto

- Estado al 2026-10-16: piloto PlantUML implementado tecnicamente y estructura centrada en procesos implementada (`DEC-017`); pendiente la conformidad humana de la traduccion S4 y los insumos para la ficha de S4.3.
- Recibir los levantamientos del equipo y el documento interno para elaborar fichas.
- Elaborar la ficha de producto y proceso de S4.3 y su descomposicion en procesos Nivel 2.
- Contrastar propuesta, normativa y evidencia institucional.
- Seleccionar modalidad o caso piloto.
- Revisar la vista PlantUML de interacciones S4 ya generada; el mapa institucional Nivel 0 conserva su representacion conceptual Markdown/Mermaid.

## Fase 5 - Modelamiento

- Construir y revisar el modelo logico PlantUML.
- Levantar y validar AS-IS.
- Formalizar el modelo validado en BPMN 2.0 XML y generar sus derivados.
- Analizar brechas y requisitos BIM.
- Formular y validar TO-BE.
- Publicar una linea base solo con trazabilidad normativa y humana completa.

## Fase 6 - Automatizacion del modelamiento

- Implementar manifiestos, construccion incremental, hashes y validadores.
- Generar SVG y resumenes Markdown sin edicion manual.
- Implementar intercambio compacto de operaciones con IA.
- Construir la aplicacion web local sobre el mismo nucleo que la CLI.
- Integrar controles previos a revision, commit y release.

La construccion se rige por la [iniciativa de modelamiento hibrido](iniciativas/iniciativa-modelamiento-hibrido.md).
