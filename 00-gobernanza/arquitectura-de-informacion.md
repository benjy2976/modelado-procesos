---
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
---

# Arquitectura de informacion y enlaces

[Inicio](../00-inicio.md) · [Gobernanza](README.md)

## Objetivo

Mantener una boveda navegable para personas y agentes sin duplicar archivos ni depender de una herramienta propietaria. Las carpetas expresan pertenencia; los enlaces Markdown relativos expresan jerarquia y relaciones logicas.

## Jerarquia

```text
00-inicio.md                         mapa raiz
  -> <area>/README.md                mapa del area
      -> documento o subarea         contenido
          -> evidencia, regla,       relaciones trazables
             proceso o herramienta
```

- `00-inicio.md` es la entrada a la boveda.
- Cada carpeta principal tiene un `README.md` que funciona como mapa de contenido.
- Un subproceso o subarea con varios artefactos mantiene su propio `README.md`.
- Los documentos no se mueven para representar estados; Git conserva el historial.

## Tipos de relacion

| Relacion | Cuando se usa | Ejemplo |
|---|---|---|
| Padre-hijo | Pertenencia a un area o proceso | Modelamiento -> S4.3 |
| Se rige por | Un artefacto debe cumplir un protocolo | Regla -> protocolo de conocimiento |
| Se sustenta en | Una afirmacion usa evidencia o norma | Actividad -> regla validada |
| Produce o transforma | Una etapa genera otro artefacto | Original -> extraccion |
| Implementa | Una herramienta automatiza una regla del metodo | Extractor -> protocolo documental |
| Valida | Una revision controla un producto | Evento de revision -> regla |
| Relacionado | Conexion util que no implica dependencia | BIM -> modelamiento S4.3 |

No se crea un enlace solo para aumentar conexiones en el grafo. El texto que rodea al enlace debe explicar su significado.

## Convenciones

1. Usar enlaces Markdown relativos: `[Titulo](ruta/archivo.md)`.
2. Enlazar cada documento nuevo desde el `README.md` de su area.
3. En documentos con varios niveles, incluir al inicio enlaces hacia `Inicio` y su mapa padre.
4. Usar nombres estables y descriptivos; no incorporar `final`, `final2` ni fechas para simular versiones.
5. Enlazar la fuente maestra, no una copia ni un PDF derivado, salvo cuando la relacion sea con la evidencia original.
6. No utilizar etiquetas como sustituto de una jerarquia o de una relacion explicita.
7. Verificar enlaces no resueltos y notas huerfanas antes de una release.

## Metadatos iniciales para mapas

Los mapas de contenido pueden declarar:

```yaml
---
tipo: mapa-de-contenido
area: nombre-estable
estado: vigente
---
```

Los esquemas de reglas, evidencia y paquetes de contexto conservan sus plantillas propias. No se agregan propiedades masivas a documentos existentes hasta definir y validar el vocabulario correspondiente.

## Uso en Obsidian y fuera de Obsidian

Obsidian interpreta estos enlaces, genera enlaces entrantes y construye el grafo. GitHub, editores Markdown y agentes tambien pueden resolverlos sin sintaxis exclusiva de Obsidian. La carpeta `.obsidian` conserva preferencias portables, pero la estructura de conocimiento permanece legible sin la aplicacion.

## Control previo a publicacion

```powershell
obsidian unresolved total
obsidian orphans
obsidian deadends
```

Los resultados se revisan por alcance: originales y binarios pueden no participar del grafo, pero todo Markdown de gobierno, conocimiento o modelamiento debe estar conectado a su mapa de contenido.

