---
id: GOV-PROT-GESTION-INICIATIVAS
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
proceso: []
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/gobernanza
  - tema/iniciativas
---

# Protocolo de gestion de iniciativas

Este protocolo establece como se propone, decide, construye, verifica y cierra una iniciativa del proyecto. Ninguna iniciativa de automatizacion o cambio metodologico debe entrar en ejecucion sin una ficha enlazada, alcance definido, decisiones registradas y criterios de aceptacion verificables.

## 1. Alcance

Se aplica a iniciativas que introduzcan o cambien:

- herramientas, aplicaciones o automatizaciones;
- esquemas, plantillas o vocabularios compartidos;
- metodos de levantamiento, modelamiento o validacion;
- integraciones con IA, Obsidian, BIM, Git o servicios externos;
- fuentes maestras, derivados o reglas de versionado;
- procesos de publicacion, revision o aprobacion.

Una tarea local y reversible puede documentarse en su artefacto de trabajo. Cuando la tarea cambie una convencion, afecte varias areas o requiera desarrollo progresivo, debe promoverse a iniciativa.

## 2. Registro y ubicacion

Las iniciativas transversales se registran en `00-gobernanza/iniciativas/` y se enlazan desde su [mapa de contenido](iniciativas/README.md). Una iniciativa especifica de un area puede mantener sus entregables en esa area, pero su ficha y estado deben aparecer en el registro central.

Cada iniciativa usa un identificador estable `INI-NNN` y la [plantilla de iniciativa](../04-recursos-reutilizables/plantillas/obsidian/iniciativa.md).

## 3. Estados de una iniciativa

`estado_iniciativa` es independiente de `estado_documento`.

| Estado | Significado | Condicion de entrada |
|---|---|---|
| PROPUESTA | Alternativa en evaluacion | Problema y objetivo documentados |
| APROBADA | Enfoque y alcance autorizados | Decision registrada y criterios de aceptacion definidos |
| EN-EJECUCION | Construccion o adopcion activa | Responsable operativo, fase y siguiente entrega identificados |
| EN-PAUSA | Trabajo detenido por decision expresa | Motivo, impacto y condicion de reanudacion registrados |
| COMPLETADA | Resultado aceptado y operacion transferida | Criterios de aceptacion satisfechos y documentacion actualizada |
| CANCELADA | Iniciativa cerrada sin completar | Decision, motivo y tratamiento de artefactos registrados |

Una IA puede preparar o actualizar la ficha, pero no debe atribuir por si sola aprobacion, aceptacion ni cierre. Estos cambios requieren una decision o evidencia humana identificable.

## 4. Contenido minimo

La ficha de una iniciativa debe definir:

1. problema u oportunidad;
2. resultado esperado y usuarios;
3. alcance y exclusiones;
4. principios y decisiones aplicables;
5. arquitectura y artefactos afectados;
6. fuentes maestras y derivados;
7. mecanismo de modificacion y automatizacion;
8. fases, entregables y dependencias;
9. requisitos funcionales y no funcionales;
10. criterios de aceptacion y pruebas;
11. riesgos, seguridad, privacidad y mitigaciones;
12. reproducibilidad, versionado y publicacion;
13. estrategia de adopcion, transicion y retiro;
14. decisiones relacionadas, pendientes y siguiente paso.

No se deben declarar fechas, responsables o recursos que el equipo no haya confirmado. Si faltan, se usa `pendiente`.

## 5. Puertas de control

### 5.1 Puerta de decision

Antes de aprobar:

- el problema y la necesidad deben estar demostrados;
- las alternativas relevantes deben estar comparadas;
- el alcance y las exclusiones deben ser comprensibles;
- las decisiones que cambien convenciones deben estar en el registro.

### 5.2 Puerta de construccion

Antes de implementar:

- deben definirse fuentes maestras y derivados;
- debe existir una estrategia de prueba y recuperacion;
- las dependencias deben poder instalarse de forma reproducible;
- la seguridad y el tratamiento de datos deben estar delimitados;
- el primer incremento debe tener criterios de aceptacion.

### 5.3 Puerta de adopcion

Antes de usar el resultado como parte del metodo:

- las pruebas funcionales y de integridad deben aprobarse;
- la documentacion de uso y mantenimiento debe estar disponible;
- los artefactos generados deben ser reproducibles;
- deben registrarse limitaciones y trabajo pendiente;
- el equipo debe aceptar el resultado del incremento.

### 5.4 Puerta de publicacion

Antes de una linea base o release se aplican tambien el [protocolo de versionado y releases](protocolo-versionado-y-releases.md) y las validaciones especificas del producto.

## 6. Cambios y decisiones

- Un ajuste dentro del alcance aprobado se registra en la ficha y en Git.
- Un cambio de fuente maestra, arquitectura, seguridad, alcance o criterio de aceptacion requiere una nueva decision.
- Una iniciativa no reescribe el historial: conserva identificador y ruta; Git mantiene las versiones.
- Las decisiones reemplazadas permanecen en el registro e indican expresamente su sucesora.

## 7. Seguimiento

La ficha mantiene un unico `siguiente paso` verificable. Las tareas operativas pueden registrarse en la ficha, actas o herramienta de seguimiento, siempre enlazando el entregable afectado.

El estado general del proyecto resume solo los hitos relevantes y enlaza la iniciativa; no duplica su especificacion.

## 8. Relaciones

- [Registro de iniciativas](iniciativas/README.md)
- [Registro de decisiones](registro-decisiones.md)
- [Plan de trabajo](plan-de-trabajo.md)
- [Protocolo de versionado y releases](protocolo-versionado-y-releases.md)
- [Estandar obligatorio de Obsidian](estandar-obligatorio-obsidian.md)
