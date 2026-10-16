---
tipo: mapa-de-contenido
area: s4-3-ejecucion-inversion
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# S4.3 Ejecucion de la inversion

[Inicio](../../../00-inicio.md) · [Modelamiento](../../README.md)

Area de trabajo vigente para alcance, levantamiento, modelos AS-IS, analisis, propuesta TO-BE, aplicacion BIM y validacion.

La descomposicion no se incorporara hasta recibir y contrastar la propuesta del equipo. Los archivos conservaran nombres estables y las lineas base aprobadas se publicaran como releases.

Los modelos se mantienen separados en `02-modelos/as-is` y `02-modelos/to-be`; el diagnostico y las oportunidades permanecen en `03-analisis`. Durante el levantamiento se usara PlantUML como modelo logico y, al formalizar, BPMN 2.0 XML pasara a ser el unico maestro del diagrama conforme al [estandar de artefactos](../../../00-gobernanza/estandar-artefactos-modelamiento.md).

## Componentes

- `00-alcance`: delimitacion del proceso y exclusiones.
- `01-levantamiento`: evidencia y narrativa AS-IS.
- `02-modelos/as-is`: modelo logico PlantUML y fuente BPMN del funcionamiento formalizado.
- `03-analisis`: problemas, riesgos, brechas y oportunidades.
- `02-modelos/to-be`: modelos logicos y propuestas BPMN de proceso futuro.
- [Aplicacion BIM](04-bim/README.md): requisitos e intercambios de informacion.
- `05-validacion`: observaciones y evidencia de revision humana.

## Dependencias

- [Inventario de procesos](../../../02-arquitectura-procesos/inventario-procesos.md)
- [Referencias](../../../01-referencias/README.md)
- [Manual operativo del conocimiento](../../../00-gobernanza/manual-operativo-del-conocimiento.md)
- [Iniciativa de modelamiento hibrido](../../../00-gobernanza/iniciativas/iniciativa-modelamiento-hibrido.md)
- [Recursos reutilizables](../../../04-recursos-reutilizables/README.md)
