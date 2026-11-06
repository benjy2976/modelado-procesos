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
fecha_actualizacion: 2026-11-05
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2
---

# S4.3.2 Ejecucion

<!-- Fuente editable del diagrama en la etapa logica (DEC-025, DEC-026). -->

Sube a: [S4.3.2 Ejecucion](00-S4-3-2-ejecucion.md)

Vista de nivel 2 actualizada por `DEC-041`: una instancia de Ejecucion permanece activa hasta la obra culminada, la resolucion o la nulidad. Mientras esta activa atiende seis procesos de nivel 3 activados por eventos, repetibles, concurrentes y no interruptivos.

Notas que no se dibujan:

- La actividad "Ejecutar la obra conforme al expediente tecnico" representa el alcance de larga duracion y no recibe codigo de proceso ni marcador de bucle.
- Los seis subprocesos de evento no llevan flujo de secuencia y pueden coexistir mientras la ejecucion principal siga activa.
- Los grupos son ayudas de lectura: Control periodico, Atencion de incidencias, Modificaciones de alcance y Modificaciones de plazo.
- Adicional, reduccion o deductivo y mayores cantidades permanecen dentro de S4.3.2.3 como variantes internas sin nivel 4.
- Cuaderno de Incidencias es la denominacion institucional uniforme adoptada para los modelos; las fuentes de administracion directa pueden usar cuaderno de obra.
- El carril del padre es una abstraccion de la ejecucion completa. La pertenencia de residente, contratista o representante legal, supervisor contratado, inspector y unidades del GORE se desarrolla en los procesos hijos conforme a `DEC-042`.
- La resolucion y la nulidad interrumpen la actividad principal mediante eventos de borde; la obra culminada es su salida normal.

## Pools

| Pool | Carriles |
|---|---|
| S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Grupo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E-1 | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | inicio-mensaje | Acta de inicio de obra recibida | T-1 |  |  |  | Una instancia de larga duracion; unidad exacta pendiente |  |  |  | EQ | Propuesta del equipo, 2026-11-02; DEC-030 |
| T-1 | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | tarea | Ejecutar la obra conforme al expediente tecnico | F-1 |  |  |  | Permanece activa hasta la culminacion, resolucion o nulidad; registra ocurrencias en el Cuaderno de Incidencias |  |  |  | EQ | DEC-030; Reglamento, art. 188; Directiva 017-2023-CG, num. 7.3.2 |
| F-1 | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | fin-mensaje | Obra culminada |  |  |  |  |  |  |  |  | NORM | REG-CON-OBRA-003; REG-CGR-AD-002 |
| B-1 | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | borde-condicional | Contrato resuelto | F-2 | T-1 | Si |  | Interrumpe la ejecucion |  |  |  | NORM | REG-CON-OBRA-004; Reglamento, arts. 122 y 123 |
| B-2 | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | borde-condicional | Contrato declarado nulo | F-3 | T-1 | Si |  | Interrumpe la ejecucion |  |  |  | NORM | Ley 32069, art. 71; Reglamento, art. 111 |
| F-2 | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | fin-mensaje | Ejecucion terminada por resolucion |  |  |  |  |  |  |  |  | NORM | REG-CON-OBRA-004; Reglamento, arts. 122 y 123 |
| F-3 | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | fin-mensaje | Ejecucion terminada por nulidad |  |  |  |  |  |  |  |  | NORM | Ley 32069, art. 71; Reglamento, art. 111 |
| CP | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | subproceso-evento-temporizador | S4.3.2.1 Control periodico de la ejecucion |  |  |  |  | Una instancia por periodo de control | Cierre de cada mes | Nucleo inicial: valorizacion | Control periodico | EQ | DEC-032; Reglamento, art. 210.1; Directiva 017-2023-CG, num. 7.3.4 |
| CO | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | subproceso-evento-mensaje | S4.3.2.2 Atencion de consultas de obra |  |  |  |  | Una instancia por consulta | Consulta registrada en el Cuaderno de Incidencias | Puede originar una instancia de S4.3.2.3 a S4.3.2.6 | Atencion de incidencias | EQ | DEC-032 y DEC-041; Reglamento, art. 190 |
| MA | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | subproceso-evento-condicional | S4.3.2.3 Gestion de modificaciones de alcance |  |  |  |  | Una instancia por solicitud o causal | Causal de modificacion de alcance | Adicional, reduccion o deductivo y mayores cantidades | Modificaciones de alcance | EQ | DEC-041; Ley 32069, arts. 63-64; Reglamento, arts. 109 y 194-197 |
| AP | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | subproceso-evento-condicional | S4.3.2.4 Gestion de ampliaciones de plazo |  |  |  |  | Una instancia por solicitud o causal | Causal de ampliacion de plazo | Requiere evaluar la afectacion aplicable | Modificaciones de plazo | EQ | DEC-041; Reglamento, arts. 198, 200 y 201; Directiva 017-2023-CG, num. 7.3.7 |
| SP | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | subproceso-evento-condicional | S4.3.2.5 Formalizacion de suspensiones de plazo |  |  |  |  | Una instancia por suspension o reanudacion | Causa de suspension o cese de la causa | Suspension contractual; AD con evidencia insuficiente | Modificaciones de plazo | EQ | DEC-041; Reglamento, arts. 107 y 202 |
| PR | S4.3.2 Ejecucion | Ejecucion, control y gestion institucional de la obra | subproceso-evento-condicional | S4.3.2.6 Gestion de paralizacion y reinicio |  |  |  |  | Una instancia por paralizacion o reinicio | Causal de paralizacion o condiciones de reinicio | Tratamiento diferenciado por regimen | Modificaciones de plazo | EQ | DEC-041; REG-CGR-AD-005; REG-CON-PARAL-001 |

## Mensajes

| Desde | Hacia | Nombre | Clase |
|---|---|---|---|
| S4.3.1 Inicio de ejecucion | E-1 | Acta de inicio de obra | EQ |
| F-1 | S4.3.3 Recepcion | Obra culminada para recepcion | PROP |
| F-2 | S4.3.3 Recepcion | Contrato resuelto para constatacion e inventario | PROP |
| F-3 | S4.3.3 Recepcion | Contrato nulo: tratamiento por definir | PROP |
