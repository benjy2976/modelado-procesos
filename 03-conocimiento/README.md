---
tipo: mapa-de-contenido
area: conocimiento
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# Conocimiento

[Inicio](../00-inicio.md)

Esta area contiene conocimiento reutilizable por varios procesos: reglas normativas curadas, sus eventos de revision y catalogos comunes de actores, sistemas, documentos, riesgos y reglas de negocio. Su operacion se rige por el [protocolo de conocimiento confiable](../00-gobernanza/protocolo-conocimiento-confiable.md). Las plantillas se encuentran en [Plantillas](../00-gobernanza/plantillas/README.md).

## Reglas normativas

- `reglas/*.yaml`: una regla atomica por archivo; fuente maestra editable.
- [Eventos de revision](revisiones/README.md): `revisiones/*.yaml`, eventos inmutables de propuesta, observacion, validacion, retiro o revalidacion.
- `catalogo-reglas.csv`: indice generado desde los YAML para busqueda, control y consumo por la aplicacion web.

El catalogo CSV no se edita manualmente una vez que exista el generador. Si existe diferencia, prevalecen los YAML y sus eventos de revision.

### Identificadores

Formato recomendado: `REG-<DOMINIO>-<TEMA>-NNN`, por ejemplo `REG-CON-EJEC-001`. El identificador no cambia cuando se corrige la redaccion. Una regla materialmente distinta recibe otro identificador y relaciona la regla que reemplaza.

### Restriccion

Los borradores producidos por IA deben conservar `estado_validacion: BORRADOR-IA`. Solo el flujo humano de revision puede establecer `VALIDADO`.

## Catalogos comunes

Carpetas reservadas; se completan cuando exista evidencia:

- `actores-y-roles/`
- `sistemas/`
- `documentos-y-formatos/`
- `riesgos-y-controles/`
- `reglas-de-negocio/`

Los indicadores no se catalogan aqui: cada proceso mantiene sus fichas de indicador en su carpeta de [Procesos](../02-procesos/README.md).

## Relaciones

- [Glosario del proyecto](../glosario.md)
- [Manual operativo del conocimiento](../00-gobernanza/manual-operativo-del-conocimiento.md)
- [Validador de conocimiento](../05-herramientas/validador-conocimiento/README.md)
