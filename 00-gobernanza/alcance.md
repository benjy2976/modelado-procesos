---
id: GOV-ALCANCE
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: DECISION
proceso:
  - S4.3
fecha_creacion: 2026-10-14
fecha_actualizacion: 2026-11-25
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/gobernanza
---

# Alcance

## Incluye

- Biblioteca normativa e institucional relacionada con gestion y ejecucion de inversiones.
- Modelamiento progresivo de los niveles inferiores de S4.3, desde el nivel 2 en adelante (`DEC-022`). El mapa Nivel 0 y la ficha S4 aprobados no se modifican por ahora; las mejoras al nivel 1 se registran como observaciones en el sustento de S4.
- Trazabilidad entre norma, regla, actividad, rol, sistema, evidencia, riesgo y control.
- Catalogo versionado de reglas y validacion especializada mediante una aplicacion web interna.
- Paquetes de contexto controlados para el trabajo con personas y modelos de IA.
- Incorporacion de requisitos, intercambios y estados de informacion BIM.
- Modelos AS-IS y TO-BE claramente separados.
- Modelamiento logico PlantUML, formalizacion BPMN y desarrollo progresivo del gestor local aprobado en INI-001.

## No definido aun

- Descomposicion definitiva de S4.3.
- Modalidad de ejecucion que se usara como primer piloto.
- Plataforma CDE institucional.

La descomposicion y el piloto operativo se definiran despues de recibir la propuesta del equipo y revisar la documentacion aplicable. La construccion del gestor de modelos se desarrolla por fases conforme a la [iniciativa INI-001](iniciativas/iniciativa-modelamiento-hibrido.md).

## Ampliaciones de alcance diferidas

Por decisión del usuario del 2026-11-25 (`DEC-061`), la etapa actual se cierra con los procesos ya definidos en el árbol de S4.3. Una ampliación de alcance es un diagrama nuevo, no considerado hasta ahora, que pasaría a ser proceso hijo de uno existente. Esas propuestas no se modelan en esta etapa: se anotan aquí para retomarlas en una etapa distinta. Los ajustes dentro de los diagramas existentes siguen en alcance.

| Propuesta | Padre probable | Origen | Situación en los modelos actuales |
|---|---|---|---|
| Resolución del contrato de obra (Reglamento de la Ley 32069, arts. 122-123), incluida la suspensión del contrato vinculado al resolverse el principal (202.4) | S4.3.2 Ejecución | Fase 5 de la auditoría; [informe consolidado](../05-herramientas/gestor-modelos/docs/informe-auditoria-fase-5-S4-3.md) | Solo el evento de borde «Contrato resuelto» (B-1) de S4.3.2 y su salida a S4.3.3. Los fines por superar el 50 % de S4.3.2.3 y S4.3.2.8 remiten a ese evento (`DEC-060`). Código y nombre por definir |
| Tratamiento de la nulidad del contrato atribuible al contratista | S4.3.2 Ejecución, posiblemente junto con la resolución | Fase 5; `DEC-059` | `EVIDENCIA-INSUFICIENTE`: sin tratamiento normativo identificado. F-3 de S4.3.2 solo cubre la nulidad no atribuible (111.3) |
| Variante de S4.3.2.6 para obras bajo la Ley 31589, solo si se decide representarla en un diagrama propio | S4.3.2 Ejecución | Fase 5 | La decisión del alcance por régimen de S4.3.2.6 sigue en alcance; solo un diagrama separado sería ampliación |
| Modelo de S4.3.3 Recepción | S4.3 Ejecución de la inversión | Decisión del usuario del 2026-11-25 (`DEC-062`) | Figura en el árbol con su [nota índice](../02-procesos/S4-gestion-de-las-inversiones/S4-3-ejecucion-inversion/S4-3-3-recepcion/00-S4-3-3-recepcion.md), sin diagrama. No es un diagrama nuevo, pero se difiere por decisión expresa. S4.3 y S4.3.2 mantienen sus salidas hacia S4.3.3 como interfaz pendiente |
