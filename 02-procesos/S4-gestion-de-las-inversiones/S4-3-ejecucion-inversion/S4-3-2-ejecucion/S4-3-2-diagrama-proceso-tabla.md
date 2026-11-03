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
fecha_actualizacion: 2026-11-03
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2
---

# S4.3.2 Ejecución

<!-- Fuente editable del diagrama en la etapa logica (DEC-025, DEC-026). Genera S4-3-2-diagrama-proceso.bpmn, .svg, .png y .html con 05-herramientas/gestor-modelos/construir_modelos.py. -->

Sube a: [S4.3.2 Ejecucion](00-S4-3-2-ejecucion.md)

Vista de nivel 2 actualizada por el equipo (`DEC-030`, `DEC-031`): una instancia de Ejecucion permanece activa hasta la obra culminada, la resolucion o la nulidad. Mientras esta activa atiende, de forma repetible y concurrente, tres bloques de eventos: Control periodico, Consultas de obra y Gestionar modificaciones de alcance o plazo. Clase de cada elemento: `NORM` normativa citada en el sustento, `EQ` equipo, `PROP` propuesta. El catalogo detallado de eventos se conserva en el [sustento de S4.3.2](S4-3-2-sustento.md) y en el respaldo temporal.

Notas que no se dibujan:

- Alcance (`EQ`): contrata y administracion directa se mantienen provisionalmente en un solo diagrama; sus diferencias se detallaran dentro de cada bloque.
- Roles normativos en un solo carril; carriles por unidad de organizacion: `EVIDENCIA-INSUFICIENTE`.
- La actividad "Ejecutar la obra conforme al expediente tecnico" representa el alcance de larga duracion. No lleva marcador de bucle porque no reinicia secuencialmente el subproceso completo.
- Los tres subprocesos de evento son no interruptivos: pueden iniciarse varias veces y coexistir mientras la ejecucion principal siga activa. No llevan flujo de secuencia; pertenecen al alcance de S4.3.2 y cada uno conserva su propio disparador.
- Control periodico agrupa la valorizacion y otros controles recurrentes; Consultas de obra agrupa las consultas; Gestionar modificaciones de alcance o plazo agrupa adicionales, reducciones, mayores metrados, suspensiones, ampliaciones y paralizaciones. El agrupamiento es `EQ`; el detalle permanece en el sustento.
- Los tres son bloques operativos del BPMN, no procesos formales de nivel 3. Solo se desagregaran si el analisis confirma objetivo, entrada, producto, responsable e instancia propios.
- La resolucion y la nulidad son eventos de borde condicionales que interrumpen "Ejecutar la obra"; la obra culminada es su salida normal. La conformidad tecnica se reserva para analizarla dentro de S4.3.3 Recepcion.
- Toda modificacion se registra en el Banco de Inversiones antes de ejecutarse (`REG-INV-EJEC-004`).

## Pools

| Pool | Carriles |
|---|---|
| S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Grupo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E-1 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | inicio-mensaje | Acta de inicio de obra recibida | T-1 |  |  |  | Una instancia de larga duración; unidad exacta pendiente de confirmar |  |  |  | EQ | Propuesta del equipo, 2026-11-02; DEC-030 |
| T-1 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | tarea | Ejecutar la obra conforme al expediente técnico | F-1 |  |  |  | Permanece activa hasta la culminación, resolución o nulidad; registra ocurrencias en el cuaderno de obra |  |  |  | EQ | Propuesta del equipo, 2026-11-02; Reglamento de la Ley 32069, art. 188; Directiva 017-2023-CG, num. 7.3.2 |
| F-1 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | fin-mensaje | Obra culminada |  |  |  |  |  |  |  |  | NORM | REG-CON-OBRA-003; REG-CGR-AD-002 |
| B-1 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | borde-condicional | Contrato resuelto | F-2 | T-1 | Sí |  | Interrumpe la ejecución |  |  |  | NORM | REG-CON-OBRA-004; Reglamento, arts. 122 y 123 |
| B-2 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | borde-condicional | Contrato declarado nulo | F-3 | T-1 | Sí |  | Interrumpe la ejecución |  |  |  | NORM | Ley 32069, art. 71; Reglamento, art. 111 |
| F-2 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | fin-mensaje | Ejecución terminada por resolución |  |  |  |  |  |  |  |  | NORM | REG-CON-OBRA-004; Reglamento, arts. 122 y 123 |
| F-3 | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | fin-mensaje | Ejecución terminada por nulidad |  |  |  |  |  |  |  |  | NORM | Ley 32069, art. 71; Reglamento, art. 111 |
| CP | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-temporizador | Control periódico |  |  |  |  | Bloque operativo agrupado por el equipo | Cierre de cada mes | Incluye valorización y controles periódicos; el detalle se desarrollará posteriormente | Eventos activos | EQ | Propuesta del equipo, 2026-11-02; Reglamento, art. 210.1; Directiva 017-2023-CG, num. 7.3.4 |
| CO | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-mensaje | Consultas de obra |  |  |  |  | Bloque operativo agrupado por el equipo | Consulta anotada en el cuaderno de obra | Puede originar una modificación de alcance o plazo | Eventos activos | EQ | Propuesta del equipo, 2026-11-02; Reglamento, art. 190; Directiva 017-2023-CG, num. 7.3.7 b |
| MP | S4.3.2 Ejecución | Contratista o residente, supervisor o inspector y entidad | subproceso-evento-condicional | Gestionar modificaciones de alcance o plazo |  |  |  |  | Bloque operativo agrupado por el equipo | Causal de modificación de alcance o plazo | Incluye adicional con deductivo vinculado, reducción, mayores metrados, suspensión, ampliación y paralización | Eventos activos | EQ | Propuesta del equipo, 2026-11-02; catalogo de eventos del sustento |

## Mensajes

| Desde | Hacia | Nombre | Clase |
|---|---|---|---|
| S4.3.1 Inicio de ejecución | E-1 | Acta de inicio de obra | EQ |
| F-1 | S4.3.3 Recepción | Obra culminada para recepción | PROP |
| F-2 | S4.3.3 Recepción | Contrato resuelto para constatación e inventario | PROP |
| F-3 | S4.3.3 Recepción | Contrato nulo: tratamiento por definir | PROP |
