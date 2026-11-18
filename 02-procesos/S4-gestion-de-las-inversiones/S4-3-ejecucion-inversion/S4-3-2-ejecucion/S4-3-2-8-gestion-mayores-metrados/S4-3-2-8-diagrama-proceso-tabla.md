---
id: AP-S4-3-2-8-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.8
nivel_proceso: 3
perfil_trazado: zigzag-controlado
tipo_proceso: APOYO
proceso_padre: S4.3.2
estado_institucional: PROPUESTA
nivel_revision: ELABORACION
proceso:
  - S4.3.2.8
fecha_creacion: 2026-11-18
fecha_actualizacion: 2026-11-18
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-8
---

# S4.3.2.8 Gestion de mayores metrados

Sube a: [S4.3.2.8 Gestion de mayores metrados](00-S4-3-2-8-gestion-mayores-metrados.md)

Modelo conceptual propuesto mediante DEC-047. Condiciones, fuentes y limites en el sustento.

## Pools

| Pool | Carriles |
| --- | --- |
| Contratista | Residente de obra |
| Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad |
| Gobierno Regional Huanuco |  |
| S4.3.2.1 Control periodico de la ejecucion |  |

## Elementos

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Clase | Fuente |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R1 | 1 | Contratista | Residente de obra | inicio-condicional | Necesidad de mayores metrados identificada | R2 |  |  |  |  |  |  | PROP | DEC-047 |
| R2 | 2 | Contratista | Residente de obra | tarea-usuario | Solicitar mayores metrados en cuaderno | R3 |  |  |  |  |  |  | NORM | Reglamento art. 197.1 |
| R3 | 3 | Contratista | Residente de obra | mensaje-envio | Remitir solicitud a supervision | R4 |  |  |  |  |  |  | PROP | DEC-047 |
| R4 | 4 | Contratista | Residente de obra | mensaje-recepcion | Pronunciamiento de supervision recibido | RG |  |  |  |  |  |  | PROP | DEC-047 |
| RG | 5 | Contratista | Residente de obra | compuerta | ¿Ejecucion autorizada? | R5 [Si]; RF0 [No] |  |  |  |  |  |  | PROP | DEC-047 |
| R5 | 6 | Contratista | Residente de obra | tarea | Ejecutar y sustentar mayores metrados del periodo | RF |  |  |  |  |  |  | NORM | Reglamento art. 197.1-197.2 |
| RF | 7 | Contratista | Residente de obra | fin-mensaje | Sustento remitido a valorizacion |  |  |  |  |  |  | Pago sujeto a autorizacion de autoridad de gestion administrativa; interfaz S4.3.2.1 | PROP | DEC-047 |
| RF0 | 8 | Contratista | Residente de obra | fin | Ejecucion no habilitada por esta ruta |  |  |  |  |  |  |  | PROP | DEC-047 |
| S1 | 9 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Solicitud en cuaderno recibida | S2 |  |  |  |  |  |  | PROP | DEC-047 |
| S2 | 10 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Verificar figura, modalidad y acumulados | SG |  |  |  |  |  |  | NORM | Reglamento art. 197.1 y 197.4 |
| SG | 11 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | compuerta | ¿Corresponde autorizar mayores metrados? | S3 [Si]; S4 [No o no acreditado] |  |  |  |  |  |  | PROP | DEC-047 |
| S3 | 12 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea-usuario | Autorizar ejecucion en cuaderno y comunicar a entidad | SF1 |  |  |  |  |  |  | NORM | Reglamento art. 197.1 |
| SF1 | 13 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Autorizacion de ejecucion remitida |  |  |  |  |  |  |  | PROP | DEC-047 |
| S4 | 14 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Documentar impedimento o necesidad de reclasificar | SF0 |  |  |  |  |  | Si excede limite, tratamiento art. 197.4; no habilitar ejecucion | PROP | DEC-047 |
| SF0 | 15 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Pronunciamiento sin autorizacion remitido |  |  |  |  |  |  |  | PROP | DEC-047 |

## Mensajes

| Desde | Hacia | Nombre |
| --- | --- | --- |
| R3 | S1 | Solicitud de mayores metrados |
| SF1 | R4 | Autorizacion |
| SF0 | R4 | Pronunciamiento sin autorizacion |
| S3 | Gobierno Regional Huanuco | Comunicacion de autorizacion |
| RF | S4.3.2.1 Control periodico de la ejecucion | Sustento para valorizacion y autorizacion de pago |
