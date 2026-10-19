---
id: AP-S4-3-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3
nivel_proceso: 1
proceso:
  - S4.3
fecha_creacion: 2026-10-19
fecha_actualizacion: 2026-10-19
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3
---

# S4.3 Ejecución de la inversión

<!-- Fuente editable del diagrama en la etapa logica (DEC-025, DEC-026). Genera S4-3-diagrama-proceso.bpmn, .svg y .png con 05-herramientas/gestor-modelos/construir_modelos.py. Reemplaza al modelo logico PlantUML, que queda en el historial de Git. -->

Sube a: [S4.3 Ejecucion de la inversion](00-S4-3-ejecucion-inversion.md)

Diagrama de S4.3 conforme al Anexo 3 de la NT 002-2025-PCM-SGP: un proceso con su carril de rol, S4.3.1 en una rama paralela que permanece activa y la rama de ejecucion que espera las condiciones de inicio (`DEC-023`, `DEC-024`). Clase de cada elemento: `OBS` ficha aprobada de S4, `NORM` normativa citada en el sustento, `EQ` equipo, `PROP` propuesta. El sustento esta en [S4-3-sustento.md](S4-3-sustento.md).

Notas que no se dibujan:

- Alcance (`EQ`): todas las inversiones (proyectos, programas e IOARR); modalidades contrata, administracion directa y Obras por Impuestos.
- Diseno y construccion (`EQ`): S4.3.1 no contrata la obra; el contrato proviene de S4.2.
- Carriles por unidad de organizacion: `EVIDENCIA-INSUFICIENTE`; el carril consigna el responsable de la ficha S4.
- "Condiciones de inicio cumplidas" es un evento condicional: la rama de ejecucion espera a que S4.3.1 las cumpla (`DEC-024`).

## Pools

| Pool | Carriles |
|---|---|
| S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH |

## Elementos

| ID | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|
| E-1 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | inicio-mensaje | Expediente técnico aprobado recibido | G-1 | | Entrada desde S4.2 | OBS | Ficha S4, p. impresas 120-121 |
| G-1 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta-paralela | | S-1; E-2 | | | PROP | DEC-024 |
| S-1 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso | S4.3.1 Gestión de la ejecución | G-2 | | Una instancia por inversión, activa durante toda S4.3; planifica, contrata y provee, mantiene el equipo de gestión y hace el seguimiento | PROP | DEC-023 |
| E-2 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | condicional | Condiciones de inicio cumplidas | T-1 | | Las cumple S4.3.1 | PROP | DEC-024; REG-CON-OBRA-002 |
| T-1 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | tarea | Suscribir acta de inicio de obra o equivalente | S-2 | sale: Acta de inicio | | EQ | REG-CON-OBRA-002; Directiva 017-2023-CG, num. 7.3.1 |
| S-2 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso | S4.3.2 Ejecución | S-3 | | Una instancia por contrato o frente de ejecución; ejecución física y financiera | PROP | DEC-023 |
| S-3 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | subproceso | S4.3.3 Recepción | G-2 | | Una instancia por ejecución concluida o resuelta; recepción de obra, conformidad de bienes y servicios, o constatación física e inventario | PROP | DEC-023; REG-CON-OBRA-003; REG-CON-OBRA-004 |
| G-2 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta-paralela | | G-3 | | | PROP | DEC-024 |
| G-3 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta | ¿Contrato resuelto con saldo por ejecutar? | G-4 [Sí]; F-2 [No] | | | EQ | Insumo del equipo |
| G-4 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | compuerta-paralela | | F-1; F-2 | | | EQ | Insumo del equipo |
| F-1 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | fin-mensaje | Estado situacional por saldo enviado | | | | OBS | Ficha S4, p. impresas 120-121 |
| F-2 | S4.3 Ejecución de la inversión | Sub Gerencia de Gestión de Obras y Supervisión - unidades ejecutoras del GRH | fin-mensaje | Información para liquidación enviada | | | | OBS | Ficha S4, p. impresas 120-121 |

## Mensajes

| Desde | Hacia | Nombre | Clase |
|---|---|---|---|
| S4.2 Elaboración del expediente técnico | E-1 | Expediente técnico, documento equivalente aprobado y/o EETT | OBS |
| Gobiernos Nacional, Regional y Local | S-1 | Convenios | OBS |
| S-1 | S3.1 Programación de bienes y servicios | Designación de personal y/o requerimiento de contratación de consultoría de obra/bienes y servicios | OBS |
| S3.2 Contratación de bienes y servicios | S-1 | Servicio contratado / bien adquirido / consultoría y obra contratada | OBS |
| S-1 | MEF / INFOBRAS | Reporte de inversiones ejecutadas | OBS |
| S-2 | S2.1 Gestión Contable | Expediente para pagos | OBS |
| F-1 | S4.2 Elaboración del expediente técnico | Informe de estado situacional por saldo de obra | OBS |
| F-2 | S4.4 Liquidación, transferencia y cierre de inversión | Información técnico y financiero para liquidación ET | OBS |
