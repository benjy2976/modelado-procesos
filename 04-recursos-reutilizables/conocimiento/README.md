---
tipo: mapa-de-contenido
area: conocimiento
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# Conocimiento estructurado

[Inicio](../../00-inicio.md) · [Recursos reutilizables](../README.md)

Esta area contiene conocimiento reutilizable y validado. Su operacion se rige por `00-gobernanza/protocolo-conocimiento-confiable.md`.

## Fuentes maestras

- `reglas/*.yaml`: una regla atomica por archivo; fuente maestra editable.
- `revisiones/*.yaml`: eventos inmutables de propuesta, observacion, validacion, retiro o revalidacion.
- `catalogo-reglas.csv`: indice generado desde los YAML para busqueda, control y consumo por la aplicacion web.

El catalogo CSV no se edita manualmente una vez que exista el generador. Si existe diferencia, prevalecen los YAML y sus eventos de revision.

## Identificadores

Formato recomendado: `REG-<DOMINIO>-<TEMA>-NNN`, por ejemplo `REG-CON-EJEC-001`. El identificador no cambia cuando se corrige la redaccion. Una regla materialmente distinta recibe otro identificador y relaciona la regla que reemplaza.

## Restriccion

Los borradores producidos por IA deben conservar `estado_validacion: BORRADOR-IA`. Solo el flujo humano de revision puede establecer `VALIDADO`.

## Relaciones

- [Manual operativo del conocimiento](../../00-gobernanza/manual-operativo-del-conocimiento.md)
- [Protocolo de conocimiento confiable](../../00-gobernanza/protocolo-conocimiento-confiable.md)
- [Eventos de revision](revisiones/README.md)
- [Validador de conocimiento](../../05-herramientas/validador-conocimiento/README.md)
