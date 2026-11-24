---
id: AP-S4-3-2-7-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.2.7
nivel_proceso: 3
perfil_trazado: zigzag-controlado
tipo_proceso: APOYO
proceso_padre: S4.3.2
estado_institucional: PROPUESTA
nivel_revision: ELABORACION
proceso:
  - S4.3.2.7
fecha_creacion: 2026-11-18
fecha_actualizacion: 2026-11-24
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-2/s4-3-2-7
---

# S4.3.2.7 Gestion de reducciones de prestaciones

Sube a: [S4.3.2.7 Gestion de reducciones de prestaciones](00-S4-3-2-7-gestion-reducciones-prestaciones.md)

Modelo conceptual propuesto mediante DEC-047. Condiciones, fuentes y limites en el sustento.

## Pools

| Pool | Carriles |
| --- | --- |
| Gobierno Regional Huanuco | Area usuaria competente (por confirmar); Unidad competente (por confirmar); Autoridad de gestion administrativa |
| Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad |

## Elementos

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Adjunto | Interrumpe | Documentos | Plazo | Disparador | Anotacion | Clase | Fuente |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| E1 | 1 | Gobierno Regional Huanuco | Area usuaria competente (por confirmar) | inicio-mensaje | Necesidad de reduccion recibida | T1 |  |  |  |  |  |  | PROP | DEC-047 |
| T1 | 2 | Gobierno Regional Huanuco | Area usuaria competente (por confirmar) | tarea | Sustentar reduccion y verificar supuesto aplicable | G1 |  |  |  |  |  | Art. 109: finalidad, prestaciones no ejecutadas, divisibles y cuantificables; limite y oportunidad | PROP | Reglamento art. 109.1; adscripcion pendiente |
| G1 | 3 | Gobierno Regional Huanuco | Area usuaria competente (por confirmar) | compuerta | ¿Se acreditan las condiciones de la reduccion? | G3 [Si]; F0 [No o no acreditado] |  |  |  |  |  | Condiciones a)-c) y limite del 25 % (art. 109.1) | NORM | Reglamento art. 109.1 |
| G3 | 16 | Gobierno Regional Huanuco | Area usuaria competente (por confirmar) | compuerta | ¿Corresponde opinion de supervision? | T2 [Si]; T3 [No] |  |  |  |  |  | Art. 109.1 d: obras y consultoria de obras, de corresponder | NORM | Reglamento art. 109.1 d |
| T2 | 4 | Gobierno Regional Huanuco | Area usuaria competente (por confirmar) | mensaje-envio | Solicitar opinion del supervisor | M1 |  |  |  |  |  |  | PROP | Reglamento art. 109.1 d; ruta de obra con supervisor |
| M1 | 5 | Gobierno Regional Huanuco | Area usuaria competente (por confirmar) | mensaje-recepcion | Opinion de supervision recibida | T3 |  |  |  |  |  |  | PROP | DEC-047 |
| T3 | 6 | Gobierno Regional Huanuco | Unidad competente (por confirmar) | tarea | Integrar sustento y controles aplicables | T4 |  |  |  |  |  | Circuito interno y controles por acreditar; sin plazo adicional inventado | PROP | DEC-047 |
| T4 | 7 | Gobierno Regional Huanuco | Autoridad de gestion administrativa | tarea-usuario | Resolver reduccion y efecto en plazo | G2 |  |  |  |  |  | La misma resolucion determina si se reduce el plazo (art. 109.2) | NORM | Reglamento art. 109.1-109.2; Ley art. 63.1 |
| G2 | 8 | Gobierno Regional Huanuco | Autoridad de gestion administrativa | compuerta | ¿Reduccion dispuesta? | T5 [Si]; F2 [No] |  |  |  |  |  |  | PROP | DEC-047 |
| T5 | 9 | Gobierno Regional Huanuco | Unidad competente (por confirmar) | tarea | Publicar resolucion en Pladicop y actualizar registros | F1 |  |  |  |  |  | Sin adenda (art. 109.3). Interfaz: el contratista puede pedir disminuir garantias (art. 117.3); adecuacion en 10 dias habiles (art. 117.4) | NORM | Reglamento arts. 109.3 y 117.3-117.4 |
| F1 | 10 | Gobierno Regional Huanuco | Unidad competente (por confirmar) | fin-mensaje | Reduccion publicada |  |  |  |  |  |  |  | PROP | DEC-047 |
| F2 | 11 | Gobierno Regional Huanuco | Autoridad de gestion administrativa | fin-mensaje | Decision no favorable comunicada |  |  |  |  |  |  |  | PROP | DEC-047 |
| F0 | 12 | Gobierno Regional Huanuco | Area usuaria competente (por confirmar) | fin | Caso pendiente de sustento o ruta especifica |  |  |  |  |  |  | No es denegacion de fondo; otros regimenes y variante sin supervisor pendientes | PROP | DEC-047 |
| SE | 13 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | inicio-mensaje | Solicitud de opinion recibida | ST |  |  |  |  |  |  | PROP | DEC-047 |
| ST | 14 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | tarea | Emitir opinion sobre reduccion | SF |  |  |  |  |  | Inspector: por inferencia del art. 186.1, pendiente de confirmacion | NORM | Reglamento arts. 109.1 d y 186.1 |
| SF | 15 | Supervisor o inspector de obra | Supervisor o inspector de obra, segun modalidad | fin-mensaje | Opinion remitida |  |  |  |  |  |  |  | PROP | DEC-047 |

## Mensajes

| Desde | Hacia | Nombre |
| --- | --- | --- |
| T2 | SE | Solicitud de opinion |
| SF | M1 | Opinion de supervision |
