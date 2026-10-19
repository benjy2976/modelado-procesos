---
id: AP-S4-3-1-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.1
nivel_proceso: 2
proceso:
  - S4.3.1
fecha_creacion: 2026-10-19
fecha_actualizacion: 2026-10-19
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-1
---

# S4.3.1 Gestión de la ejecución

<!-- Fuente editable del diagrama en la etapa logica (DEC-025, DEC-026). Genera S4-3-1-diagrama-proceso.bpmn, .svg, .png y .html con 05-herramientas/gestor-modelos/construir_modelos.py. -->

Sube a: [S4.3.1 Gestion de la ejecucion](00-S4-3-1-gestion-de-la-ejecucion.md)

Vista de nivel 2: el flujo principal prepara la ejecucion (planificar, contratar, designar y verificar las condiciones de inicio), entrega las condiciones de inicio a S4.3.2 y espera a que todas las ejecuciones hayan sido recibidas o constatadas para entregar la informacion de liquidacion (`DEC-023`, `DEC-024`). Lo que ocurre de forma periodica o a demanda mientras la ejecucion sigue activa son subprocesos de evento sin interrupcion, contraidos, que se detallaran en su propio diagrama de nivel 3. Clase de cada elemento: `OBS` ficha aprobada de S4, `NORM` normativa citada en el sustento, `EQ` equipo, `PROP` propuesta. Fuentes y vacios en el [sustento de S4.3.1](S4-3-1-sustento.md).

Notas que no se dibujan:

- Contrataciones que se requieren segun la modalidad: en contrata, la obra y la supervision; en administracion directa, segun el plan de abastecimiento, las adquisiciones de los primeros treinta dias (`REG-CGR-AD-003`, `REG-CGR-AD-004`); en todas, el componente de gestion (`EQ`; Instructivo del Formato 08-A, p. 19-20).
- Alcance (`EQ`): todas las inversiones; modalidades contrata, administracion directa y Obras por Impuestos. En diseno y construccion no se contrata la obra, porque el contrato proviene de S4.2; en Obras por Impuestos el flujo es `EVIDENCIA-INSUFICIENTE` hasta leer `INV-006`.
- Un solo carril con el responsable de S4.3 en la ficha S4 (`OBS`). Los carriles del modelo del equipo (GRI, SGOS y coordinador de proyecto) quedan por confirmar; carriles por unidad de organizacion: `EVIDENCIA-INSUFICIENTE`.
- Si la inversion tiene varios contratos o frentes, la verificacion y la comunicacion de las condiciones de inicio se repiten por cada uno (`PROP`); su representacion se resolvera en el nivel 3.
- La ruta del expediente para pagos (desde S4.3.1 y no desde S4.3.2, como muestra el diagrama de S4.3) es una `PROPUESTA` por confirmar.
- Sin ubicar todavia: el programa de mantenimiento (`REG-INV-EJEC-009`) y el registro de la culminacion en el Formato 09, seccion B (`REG-INV-EJEC-007`, pregunta P8 del sustento de S4.3).

## Pools

| Pool | Carriles |
|---|---|
| S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Disparador | Anotacion | Grupo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| E-1 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | inicio-mensaje | Expediente técnico aprobado recibido | T-1 |  | Una instancia por inversión |  |  |  | OBS | Ficha S4, p. impresas 120-121; DEC-023 |
| T-1 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | tarea | Planificar la ejecución de la inversión | T-2 | entra: Expediente técnico; sale: Planificación | Recursos, contrataciones, cronograma, riesgos y controles |  |  |  | NORM | REG-INV-EJEC-002; respuesta P5 del equipo |
| T-2 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | tarea | Requerir las contrataciones y la designación de personal | E-2 | sale: Términos de referencia o especificaciones técnicas |  |  |  |  | NORM | Instructivo del Formato 08-A, p. 20; REG-CGR-AD-003; REG-CGR-AD-004; REG-CON-OBRA-001 |
| E-2 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | mensaje-recepcion | Contratos y adquisiciones recibidos | G-1 |  |  |  |  |  | OBS | Ficha S4, p. impresas 120-121 |
| G-1 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta | ¿Cuenta con supervisor contratado? | G-2 [Sí]; T-3 [No] |  |  |  |  |  | EQ | Modelo 1 del equipo; Reglamento de la Ley 32069, art. 186.1 |
| T-3 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | tarea | Designar al inspector o al equipo de inspectores | G-2 |  |  |  | Si la obra requiere supervisor, solo mientras se contrata y hasta el límite de la valorización acumulada |  | NORM | Reglamento de la Ley 32069, art. 186.1 y 186.4 |
| G-2 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta |  | T-4 |  |  |  |  |  | PROP |  |
| T-4 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | tarea | Asignar el rol de Monitor y conformar el equipo de gestión | T-5 |  |  |  |  |  | NORM | REG-CON-CDI-002; Instructivo del Formato 08-A, p. 19-20; práctica del equipo |
| T-5 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | tarea | Verificar las condiciones de inicio | G-3 |  |  |  | Contrata: art. 176.1 del Reglamento. Administración directa: num. 7.3.1 de la Directiva 017-2023-CG |  | NORM | REG-CON-OBRA-002; Directiva 017-2023-CG, num. 7.3.1; modelo 1 del equipo |
| G-3 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta | ¿Condiciones de inicio cumplidas? | G-6 [Sí]; T-6 [No] |  |  |  |  |  | PROP |  |
| T-6 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | tarea | Gestionar las condiciones pendientes | G-6 |  |  |  |  |  | PROP | REG-CON-OBRA-002 |
| G-6 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta |  | H-1 |  |  |  |  |  | PROP |  |
| H-1 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | mensaje-envio | Condiciones de inicio comunicadas | E-3 |  |  |  |  |  | PROP | DEC-024; modelo 1 del equipo |
| E-3 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | condicional | Todas las ejecuciones recibidas o constatadas | T-7 |  |  |  | Se cumple con los mensajes de S4.3.3: recepción o constatación concluida |  | PROP | DEC-023 |
| T-7 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | tarea | Consolidar la información técnica y financiera para la liquidación | G-4 | sale: Información técnico y financiero para liquidación |  |  |  |  | OBS | Ficha S4, p. impresas 120-121; respuesta P4 del equipo |
| G-4 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta | ¿Contrato resuelto con saldo por ejecutar? | G-5 [Sí]; F-1 [No] |  |  |  |  |  | EQ | Respuesta P6 del equipo |
| G-5 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta-paralela |  | T-8; F-1 |  |  |  |  |  | EQ | Respuesta P6 del equipo |
| T-8 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | tarea | Elaborar el informe de estado situacional por saldo de obra | F-2 | sale: Informe de estado situacional |  |  |  |  | OBS | Ficha S4, p. impresas 120-121 |
| F-1 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | fin-mensaje | Información para liquidación enviada |  |  |  |  |  |  | OBS | Ficha S4, p. impresas 120-121 |
| F-2 | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | fin-mensaje | Estado situacional por saldo enviado |  |  |  |  |  |  | OBS | Ficha S4, p. impresas 120-121 |
| SM | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso-evento-temporizador | Seguimiento mensual de la ejecución |  |  | Primeros diez días hábiles del mes siguiente | Cada mes | Formato N.° 12-B. Envía a MEF / INFOBRAS: reporte de inversiones ejecutadas | Seguimiento | NORM | REG-INV-EJEC-005; REG-INV-EJEC-006; ficha S4 |
| PG | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso-evento-mensaje | Trámite del expediente para pagos |  |  |  | Valorización aprobada recibida de S4.3.2 | Envía a S2.1 Gestión Contable: expediente para pagos. Ruta por confirmar | Seguimiento | PROP | Ficha S4; S4.3.2, subproceso S4.3.2.1 |
| MO | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso-evento-mensaje | Actualización por modificaciones de la ejecución |  |  |  | Modificación comunicada por S4.3.2 | Adicional, reducción, mayor metrado, plazo, suspensión o paralización. Actualiza la planificación y el seguimiento | Seguimiento | PROP | REG-INV-EJEC-002; REG-INV-EJEC-004; S4.3.2 |
| PV | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso-evento-condicional | Provisión de bienes, servicios y personal |  |  |  | Necesidad prevista o requerida por S4.3.2 | Envía a S3.1 el requerimiento y recibe de S3.2 lo contratado o adquirido | Provisión | EQ | DEC-023; REG-CGR-AD-003; Directiva 017-2023-CG, num. 7.3.3; práctica del equipo |
| OP | S4.3.1 Gestión de la ejecución | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso-evento-condicional | Registro de obra pública paralizada |  |  |  | Obra en el supuesto de obra pública paralizada | Inventario en el Banco de Inversiones e informe de estado situacional | Provisión | NORM | REG-CON-PARAL-001; Ley 31589, TUO, art. 3.1 y 4.1 |

## Mensajes

| Desde | Hacia | Nombre | Clase |
|---|---|---|---|
| S4.2 Elaboración del expediente técnico | E-1 | Expediente técnico, documento equivalente aprobado y/o EETT | OBS |
| Gobiernos Nacional, Regional y Local | T-1 | Convenios | OBS |
| T-2 | S3.1 Programación de bienes y servicios | Designación de personal y/o requerimiento de contratación de consultoría de obra/bienes y servicios | OBS |
| S3.2 Contratación de bienes y servicios | E-2 | Servicio contratado / bien adquirido / consultoría y obra contratada | OBS |
| H-1 | S4.3.2 Ejecución | Condiciones de inicio cumplidas | PROP |
| F-1 | S4.4 Liquidación, transferencia y cierre de inversión | Información técnico y financiero para liquidación ET | OBS |
| F-2 | S4.2 Elaboración del expediente técnico | Informe de estado situacional por saldo de obra | OBS |
