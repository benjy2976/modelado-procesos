---
tipo: plantilla
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: NO-APLICA
tags:
  - tema/automatizacion
---

# Plantilla de contexto funcional

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

Crear un `context.md` junto a cada módulo funcional real. Antes de escribirlo, leer servicios, rutas, modelos y pruebas de la capacidad. No crear archivos vacíos ni dejar marcadores por completar. Registrar una contradicción como pendiente concreto cuando las fuentes no permitan resolverla.

El contexto es la fuente de propósito, actores, reglas de negocio, estados y flujo del módulo. El transporte HTTP se documenta en [API](api.md), comandos en [CLI](cli.md), persistencia en [modelo de datos](modelo-datos.md) y composición en [arquitectura](arquitectura.md). Indexar el nuevo contexto en [Guía de IA](guia_IA.md).

## Estructura que debe adaptarse

1. **Propósito:** usuario, problema y resultado observable en una o dos frases.
2. **Alcance y límites:** capacidades incluidas, exclusiones y dependencias funcionales.
3. **Vocabulario:** solo términos propios cuyo significado pueda confundirse.
4. **Actores:** acciones permitidas, identidad comprobada o ausencia de autorización.
5. **Reglas:** condición y resultado; enlazar evidencia, sin repetir campos de schema.
6. **Flujo:** entrada, transiciones decisivas, salida y efectos.
7. **Errores y recuperación:** fallos de dominio y respuesta del usuario o sistema.
8. **Escenarios verificables:** casos principal, de permiso y de excepción con sus pruebas.
9. **Decisiones recientes:** fecha, razón, impacto y fuente cuando expliquen una regla aún vigente.

Usar títulos `## Propósito`, `## Actores`, `## Reglas` y `## Flujo` para las cuatro secciones obligatorias. Añadir otras secciones solo cuando el módulo las requiera. El [contexto actual de la mesa](../mesa_modelamiento/context.md) es un ejemplo adaptado a evidencia real.
