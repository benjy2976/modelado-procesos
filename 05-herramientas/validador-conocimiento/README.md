# Requisitos del validador de conocimiento

## Objetivo

Construir una aplicacion web interna para que el equipo transforme propuestas humanas o de IA en conocimiento normativo confiable, con revision especializada, trazabilidad y control de cambios. La aplicacion es un requisito del proyecto; no es una mejora opcional.

Hasta disponer del MVP, el mismo flujo se ejecuta mediante YAML, eventos de revision y solicitudes de cambio en Git. La ausencia temporal de la interfaz no elimina ninguna puerta de control.

## Fuente de datos

- Fuente maestra: `04-recursos-reutilizables/conocimiento/reglas/*.yaml`.
- Auditoria: `04-recursos-reutilizables/conocimiento/revisiones/*.yaml`.
- Vista regenerable: `04-recursos-reutilizables/conocimiento/catalogo-reglas.csv`.
- Evidencia: originales identificados en el catalogo documental, nunca copiados dentro de la aplicacion.

La aplicacion debe serializar las escrituras para evitar conflictos y producir cambios legibles por Git. No debe introducir una segunda fuente maestra oculta en una base de datos.

## Roles minimos

| Rol | Facultades |
|---|---|
| Proponente | Crear y corregir borradores; enviar a revision |
| Especialista | Revisar fuente, vigencia, aplicabilidad e interpretacion; observar o validar |
| Responsable metodologico | Administrar dominios, asignaciones y criterios; no sustituye al especialista |
| Consulta | Buscar y usar solo reglas autorizadas para su finalidad |
| Agente IA | Proponer y comparar; nunca validar, retirar ni alterar eventos humanos |

## Flujo

1. Crear o importar borrador y registrar si su origen es humano o IA.
2. Mostrar en paralelo original, extraccion y regla propuesta.
3. Comprobar campos, cita, hash y calidad de extraccion.
4. Asignar especialista por materia.
5. Registrar observaciones y nueva revision sin perder la anterior.
6. Validar solo con identidad humana autenticada.
7. Generar evento inmutable y actualizar el YAML de la regla.
8. Regenerar el catalogo y ejecutar controles de consistencia.
9. Marcar revalidacion cuando cambie una dependencia.

## Pantallas del MVP

1. Tablero por estado, dominio, proceso, modalidad y especialista.
2. Catalogo con busqueda y filtros.
3. Ficha de regla con historial y relaciones.
4. Revisor lado a lado: pagina del original, Markdown extraido y campos estructurados.
5. Bandeja de asignaciones y observaciones.
6. Vista de impacto: procesos, actividades BPMN y paquetes que usan la regla.
7. Reporte de reglas bloqueadas, vencidas o pendientes de revalidacion.

## Requisitos funcionales obligatorios

- Autenticacion e identificacion institucional.
- Autorizacion por rol y especialidad.
- La IA no puede ejecutar la transicion a `VALIDADO`.
- El validador no puede aprobar sin abrir la evidencia y confirmar la ubicacion normativa.
- Registro de fecha, usuario, rol, resultado, comentario, hash y commit.
- Historial inmutable de eventos y comparacion entre revisiones.
- Deteccion de fuentes modificadas y revalidacion en cascada.
- Busqueda por texto, articulo, proceso, modalidad, actor y estado.
- Exportacion de reglas validadas y paquetes de contexto.
- Validaciones de esquema antes de escribir archivos.
- Enlaces relativos y portables dentro del repositorio.

## Requisitos no funcionales

- Ejecucion local o en infraestructura institucional autorizada.
- Sin envio de originales o datos sensibles a servicios externos por defecto.
- Respaldo mediante Git y recuperacion reproducible.
- Operacion auditable y registros con fecha y zona horaria.
- Accesibilidad basica, navegacion por teclado y textos comprensibles.
- Rendimiento suficiente para catalogos de miles de reglas sin exigir una plataforma compleja.

## Criterios de aceptacion del MVP

- Un proponente crea una regla desde la plantilla y la envia a revision.
- Un especialista visualiza la pagina fuente y registra observacion o validacion.
- Ningun usuario o agente sin permiso puede validar.
- Cada accion genera un evento y un cambio Git legible.
- Un cambio de hash lleva las reglas dependientes a `REVALIDACION-REQUERIDA`.
- El catalogo CSV se reconstruye sin edicion manual.
- Se puede generar un paquete de contexto que contenga solo reglas validadas.

## Evolucion prevista

1. Generador y validador de esquemas en linea de comandos.
2. Web de consulta de solo lectura.
3. Flujo autenticado de propuesta, observacion y validacion.
4. Trazabilidad con BPMN y generacion de paquetes de contexto.
5. Busqueda semantica, solo si el catalogo curado justifica su complejidad.

La seleccion de framework, autenticacion y despliegue se decidira al iniciar la implementacion, sin alterar este contrato funcional.
