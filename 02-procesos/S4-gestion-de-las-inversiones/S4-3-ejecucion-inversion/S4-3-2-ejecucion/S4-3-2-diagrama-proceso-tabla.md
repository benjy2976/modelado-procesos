---
id: AP-S4-3-2-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2
nivel_proceso: 2
proceso:
  - S4.3.2
fecha_creacion: 2026-10-19
fecha_actualizacion: 2026-10-19
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2
---

# S4.3.2 Ejecución

<!-- Fuente editable del diagrama en la etapa logica (DEC-025, DEC-026). Genera S4-3-2-diagrama-proceso.bpmn, .svg y .png con 05-herramientas/gestor-modelos/construir_modelos.py. Reemplaza al modelo logico PlantUML, que queda en el historial de Git. -->

Sube a: [S4.3.2 Ejecucion](00-S4-3-2-ejecucion.md)

Vista de nivel 2: el flujo principal muestra la vida de la ejecucion y sus mensajes con S4.3.1 y S4.3.3; cada figura es un subproceso de evento sin interrupcion, contraido, con su disparador, que se detallara en su propio diagrama de nivel 3 (`DEC-024`). Los grupos son una ayuda de lectura, no procesos. Clase de cada elemento: `NORM` normativa citada en el sustento, `EQ` equipo, `PROP` propuesta. Catalogo de eventos y fuentes en el [sustento de S4.3.2](S4-3-2-sustento.md).

Notas que no se dibujan:

- Alcance (`EQ`): contrata y administracion directa en un solo diagrama, con diferencias anotadas en cada subproceso (`PROP`).
- Roles normativos en un solo carril; carriles por unidad de organizacion: `EVIDENCIA-INSUFICIENTE`.
- Toda modificacion se registra en el Banco de Inversiones antes de ejecutarse (`REG-INV-EJEC-004`).
- La resolucion y la nulidad son eventos de borde condicionales que interrumpen "Ejecutar la obra" (manual BPMN, sec. 2.8.3, p. 90); la obra culminada es la salida normal de la actividad. Reemplazan la compuerta "¿Como termina la ejecucion?" del modelo del equipo (`DEC-027`).
- Lo que cada subproceso de evento envia a S4.3.1 figura en su anotacion; los flujos de mensaje se dibujaran en su diagrama de nivel 3.
- Codigos S4.3.2.1 y S4.3.2.2 tomados del modelo del equipo; los demas son propuestos y estan por confirmar.
- Figuras candidatas no dibujadas: intensificacion del programa, actualizacion del programa, monitoreo y control, intervencion economica y reajustes.

## Pools

| Pool | Carriles |
|---|---|
| S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Grupo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E-1 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | inicio-mensaje | Condiciones de inicio cumplidas | T-1 |  |  |  | Una instancia por contrato o frente de ejecución |  |  |  | PROP | DEC-023; DEC-024 |
| T-1 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | tarea | Suscribir el acta de inicio de obra o equivalente | T-2 |  |  |  |  |  |  |  | EQ | REG-CON-OBRA-002 |
| T-2 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | tarea | Ejecutar la obra conforme al expediente técnico | F-1 |  |  |  | Conforme al programa de ejecución; registrar ocurrencias en el cuaderno de obra (contratista o residente) |  |  |  | NORM | Reglamento de la Ley 32069, art. 188; Directiva 017-2023-CG, num. 7.3.2 |
| F-1 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | fin-mensaje | Obra culminada |  |  |  |  |  |  |  |  | NORM | REG-CON-OBRA-003; REG-CGR-AD-002 |
| B-1 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | borde-condicional | Contrato resuelto | F-2 | T-2 | Sí |  | Interrumpe la ejecución |  |  |  | NORM | REG-CON-OBRA-004; Reglamento, arts. 122 y 123 |
| B-2 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | borde-condicional | Contrato declarado nulo | F-3 | T-2 | Sí |  | Interrumpe la ejecución |  |  |  | NORM | Ley 32069, art. 71; Reglamento, art. 111 |
| F-2 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | fin-mensaje | Ejecución terminada por resolución |  |  |  |  |  |  |  |  | NORM | REG-CON-OBRA-004; Reglamento, arts. 122 y 123 |
| F-3 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | fin-mensaje | Ejecución terminada por nulidad |  |  |  |  |  |  |  |  | NORM | Ley 32069, art. 71; Reglamento, art. 111 |
| V | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-temporizador | S4.3.2.1 Valorización |  |  |  |  | Código del equipo | Cierre de cada mes | Envía a S4.3.1: valorización aprobada para el expediente de pago | Control periódico | EQ | Reglamento, art. 210.1; Directiva 017-2023-CG, num. 7.3.4 |
| CO | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-mensaje | S4.3.2.5 Consulta de obra |  |  |  |  | Código propuesto | Consulta anotada en el cuaderno de obra | Puede originar S4.3.2.4 Ampliación de plazo | Atienden incidencias | PROP | Reglamento, art. 190; Directiva 017-2023-CG, num. 7.3.7 b |
| AD | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-condicional | S4.3.2.2 Adicional de obra con deductivo vinculado |  |  |  |  | Código del equipo | Prestación indispensable no prevista | Envía a S4.3.1: modificación aprobada | Modifican alcance y costo | EQ | REG-CON-ADIC-002; Reglamento, arts. 194 y 196; num. 7.3.6 |
| RD | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-condicional | S4.3.2.7 Reducción de prestaciones |  |  |  |  | Código propuesto | Prestación que deja de ser necesaria | Envía a S4.3.1: modificación aprobada | Modifican alcance y costo | PROP | REG-CON-ADIC-001 |
| MM | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-condicional | S4.3.2.8 Mayores metrados |  |  |  |  | Código propuesto | Mayor metrado en contrato a precios unitarios | "Menores metrados": EVIDENCIA-INSUFICIENTE. Envía a S4.3.1: mayor metrado autorizado | Modifican alcance y costo | PROP | Reglamento, art. 197; num. 7.3.6 |
| SU | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-condicional | S4.3.2.3 Suspensión de plazo |  |  |  |  | Código propuesto | Causa que impide continuar | Administración directa: EVIDENCIA-INSUFICIENTE. Envía a S4.3.1: suspensión y reinicio del plazo | Modifican el plazo | PROP | Reglamento, arts. 107 y 202 |
| AM | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-condicional | S4.3.2.4 Ampliación de plazo |  |  |  |  | Código propuesto | Causal que afecta la ruta crítica | Envía a S4.3.1: plazo modificado | Modifican el plazo | PROP | Reglamento, arts. 198, 200 y 201; num. 7.3.7 |
| PA | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-condicional | S4.3.2.6 Paralización de obra |  |  |  |  | Código propuesto | Supuesto de paralización | Puede derivar en la resolución del contrato. Envía a S4.3.1: paralización y reinicio | Modifican el plazo | PROP | REG-CGR-AD-005; REG-CON-PARAL-001; Ley 31589, art. 5.2 |

## Mensajes

| Desde | Hacia | Nombre | Clase |
|---|---|---|---|
| S4.3.1 Gestión de la ejecución | E-1 | Condiciones de inicio cumplidas | PROP |
| F-1 | S4.3.3 Recepción | Obra culminada para recepción | PROP |
| F-2 | S4.3.3 Recepción | Contrato resuelto para constatación e inventario | PROP |
| F-3 | S4.3.3 Recepción | Contrato nulo: tratamiento por definir | PROP |
