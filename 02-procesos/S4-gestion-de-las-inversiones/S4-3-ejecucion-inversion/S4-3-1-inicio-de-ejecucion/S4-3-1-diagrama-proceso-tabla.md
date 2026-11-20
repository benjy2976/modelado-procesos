---
id: AP-S4-3-1-DIAGRAMA-PROCESO-TABLA
tipo: nota-conocimiento
area: procesos
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
codigo_proceso: S4.3.1
nivel_proceso: 2
perfil_trazado: zigzag-controlado
proceso:
  - S4.3.1
fecha_creacion: 2026-11-18
fecha_actualizacion: 2026-11-18
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/procesos
  - proceso/s4/s4-3/s4-3-1
---

# S4.3.1 Inicio de ejecucion

Sube a: [S4.3.1 Inicio de ejecucion](00-S4-3-1-inicio-de-ejecucion.md)

Primera reconstruccion logica del supuesto de **obra bajo el sistema de entrega de solo construccion, gestionada por la sede del Gobierno Regional Huanuco a traves de la SGGOS**. La tabla no representa un flujo institucional validado. Contraste y limites en el [sustento](S4-3-1-sustento.md).

Notas que no se dibujan:

- La instancia es una por contrato de obra. El inicio aqui se refiere al **plazo de ejecucion contractual**, no solo a la firma del contrato ni a la entrega fisica del terreno.
- La entidad debe iniciar las gestiones para cumplir las condiciones del articulo 176.1 dentro de veintidos dias desde la suscripcion del contrato; el numeral 176.3 no fija en ese lapso la culminacion de todas ellas.
- El inspector o equipo de inspectores es una alternativa transitoria solo bajo las condiciones del articulo 186.4; la existencia de personal o capacidad tecnica, por si sola, no habilita esa ruta.
- La actualizacion del expediente o documentacion tecnica, el adelanto directo y el contrato tripartito de la JPRD se verifican **cuando corresponden**. La entrega total o parcial del terreno corresponde a solo construccion.
- La contratacion de equipo complementario del Bizagi recibido queda como interfaz con el proceso de contratacion y como asunto operativo por confirmar. No se le atribuye condicion legal de inicio.
- La ruta principal identifica al **Gobierno Regional Huanuco** como entidad contratante, a GRA y OACGD en el tramo documental y a GRI/SGGOS en la gestion de obra. La SGGOS es unidad tecnica del GORE, no una entidad contratante separada. Otras oficinas o unidades ejecutoras que contraten o ejecuten obras requieren su variante y el instrumento que acredite su competencia.
- El ROF respalda funciones generales y dependencia jerarquica, pero no prescribe el itinerario exacto del contrato ni el acto de designacion del coordinador. La secuencia de las cajas 13-17 es **propuesta operativa** a partir de la precision del usuario; instrumento de designacion, canal y firmante pendientes. Los numeros 1-12 se mantienen como referencias estables del primer modelo.
- Las condiciones pendientes mantienen abierto el tramite: la contratacion de supervision, la designacion habilitada de inspeccion o la acreditacion de los otros requisitos permiten reanudar la verificacion. Los eventos de espera son una propuesta logica, no atribuyen al coordinador la competencia de contratar, designar, pagar o entregar terreno. No equivalen al diferimiento contractual del art. 176.7, que requiere acuerdo entre las partes. La ruta ante incumplimiento y las consecuencias del art. 176.4 requieren desarrollo posterior.
- El medio de comunicacion al contratista y el acta de inicio requieren evidencia institucional o contractual. Las verificaciones del coordinador son asignaciones funcionales propuestas; no sustituyen las actuaciones de las unidades competentes para cada condicion.

## Pools

| Pool | Carriles |
|---|---|
| Gobierno Regional Huanuco | GRA — Tramite del contrato; OACGD — Registro documentario; GRI — Gerencia Regional de Infraestructura; SGGOS — Subgerente de Gestion de Obras y Supervision; SGGOS — Coordinador de obra |

## Elementos

| ID | Numero | Pool | Carril | Tipo | Nombre | Siguiente | Documentos | Plazo | Anotacion | Clase | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E1 | 1 | Gobierno Regional Huanuco | GRA — Tramite del contrato | inicio | Contrato de obra suscrito | T0A | entra: Contrato de obra |  |  | PROP | ROF, art. 25 d; Bizagi recibido; contrato concreto pendiente |
| T0A | 13 | Gobierno Regional Huanuco | GRA — Tramite del contrato | tarea-usuario | Remitir contrato para registro | T0B | sale: Contrato suscrito |  |  | PROP | ROF, arts. 20 y 25; secuencia operativa por confirmar |
| T0B | 14 | Gobierno Regional Huanuco | OACGD — Registro documentario | tarea-usuario | Registrar y notificar contrato a GRI | T0C | sale: Notificacion y registro del contrato |  |  | PROP | ROF, art. 20; usuario, 2026-11-18; canal por confirmar |
| T0C | 15 | Gobierno Regional Huanuco | GRI — Gerencia Regional de Infraestructura | tarea-usuario | Derivar contrato a SGGOS | T0D |  |  |  | PROP | ROF, arts. 92-94 y 97; ruta interna inferida |
| T0D | 16 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea | Designar coordinador de obra | T0E | sale: Designacion, instrumento por confirmar |  |  | EQ | Precision operativa del usuario, 2026-11-18; competencia y forma pendientes |
| T0E | 17 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea-usuario | Notificar designacion y remitir contrato | T1 | sale: Contrato y designacion comunicados |  |  | EQ | Precision operativa del usuario, 2026-11-18; medio por confirmar |
| T1 | 2 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Recibir contrato y revisar condiciones de inicio | T2 |  |  | Ambito: obra bajo solo construccion | PROP | Bizagi recibido; precision del usuario, 2026-11-18; Reglamento, art. 176.1 |
| T2 | 3 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Verificar supervision contratada o inspeccion habilitada | G1 |  |  |  | PROP | Ley, art. 62.5; Reglamento, arts. 176.1 b y 186.1-186.4 |
| G1 | 4 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Hay supervision? | T3 [Si]; G3 [No] (por defecto) |  |  |  | PROP | Reglamento, arts. 176.1 b y 186.4 |
| G3 | 18 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Procede inspeccion temporal? | T8 [Si]; C1 [No] (por defecto) |  |  |  | PROP | Ley, art. 62.5; Reglamento, art. 186.4; precision del usuario, 2026-11-18 |
| T8 | 19 | Gobierno Regional Huanuco | SGGOS — Subgerente de Gestion de Obras y Supervision | tarea | Gestionar designacion de inspector | GE1 |  |  |  | PROP | Bizagi recibido; precision del usuario, 2026-11-18; Ley, art. 62.5 |
| GE1 | 20 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-eventos | ¿Que se acredita primero? | C1B; C2 |  |  |  | PROP | Precision del usuario, 2026-11-18; Ley, art. 62.5 |
| C1B | 29 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | condicional | Supervisor contratado | T2 |  |  |  | PROP | Reglamento, art. 176.1 b; precision del usuario, 2026-11-18 |
| C1 | 21 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | condicional | Supervisor contratado | T2 |  |  |  | PROP | Reglamento, arts. 176.1 b y 176.7; precision del usuario, 2026-11-18 |
| C2 | 22 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | condicional | Inspector designado | T2 |  |  |  | PROP | Ley, art. 62.5; Reglamento, art. 186.4; precision del usuario, 2026-11-18 |
| T3 | 5 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Comunicar al contratista quien supervisa la obra | T4 |  |  |  | PROP | Reglamento, art. 176.1 b; adscripcion operativa pendiente |
| T4 | 6 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Verificar documentos tecnicos | T5 |  |  |  | PROP | Reglamento, art. 176.1 a |
| T5 | 7 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Verificar adelanto y JPRD | T6 |  |  | Segun aplicabilidad del art. 176.1 c-d | PROP | Reglamento, art. 176.1 c-d; art. 179 |
| T6 | 8 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Verificar entrega del terreno | G2 |  |  | Total o parcial, segun corresponda | PROP | Reglamento, art. 176.1 e |
| G2 | 9 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | ¿Condiciones cumplidas? | T7 [Si]; T9 [No] (por defecto) |  |  |  | PROP | Reglamento, art. 176.1 |
| T9 | 23 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Coordinar requisitos pendientes | GE2 |  |  |  | PROP | Reglamento, arts. 176.1, 176.4 y 176.7; precision del usuario, 2026-11-18 |
| GE2 | 24 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta-eventos | ¿Que requisito se acredita? | C3; C4; C5; C6 |  |  |  | PROP | Reglamento, art. 176.1; precision del usuario, 2026-11-18 |
| C3 | 25 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | condicional | Documentos tecnicos entregados | G4 | entra: Documentacion tecnica actualizada, si aplica |  | Cuando hubo cambios durante la seleccion | PROP | Reglamento, art. 176.1 a |
| C4 | 26 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | condicional | Adelanto directo entregado | G4 | entra: Acreditacion del adelanto, si aplica |  | Segun solicitud del contratista y excepciones normativas | PROP | Reglamento, art. 176.1 c |
| C5 | 27 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | condicional | Contrato JPRD suscrito | G4 | entra: Contrato tripartito, si aplica |  | Solo si corresponde JPRD | PROP | Reglamento, art. 176.1 d |
| C6 | 28 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | condicional | Terreno entregado | G4 | entra: Acreditacion de entrega del terreno |  | Total o parcial segun corresponda | PROP | Reglamento, art. 176.1 e |
| G4 | 30 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | compuerta | Requisito acreditado | T4 |  |  |  | PROP | Propuesta de disposicion BPMN; Reglamento, art. 176.1 |
| T7 | 10 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | tarea | Comunicar cumplimiento de condiciones de inicio | F1 | sale: Comunicacion de inicio |  | El medio y la firma son pendientes de confirmar | PROP | Bizagi recibido, actividad final; Reglamento, art. 176.1 |
| F1 | 11 | Gobierno Regional Huanuco | SGGOS — Coordinador de obra | fin-mensaje | Inicio del plazo comunicado |  |  |  |  | PROP | Reglamento, art. 176.1; formulacion de salida por confirmar |

## Mensajes

| Desde | Hacia | Nombre |
|---|---|---|
