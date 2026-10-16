---
tipo: guia
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: NO-APLICA
tags:
  - tema/gobernanza
  - tema/obsidian
---

# Arquitectura de informacion y enlaces

Sube a: [Gobernanza](00-GOBERNANZA.md)

## Objetivo

Mantener una boveda navegable para personas y agentes sin duplicar archivos ni depender de una herramienta propietaria. Las carpetas expresan pertenencia; los enlaces Markdown relativos expresan jerarquia y relaciones logicas.

## Jerarquia

```text
00-GESTION-POR-PROCESOS-GRH.md       nota de entrada
  -> <area>/00-<AREA>.md             nota indice del area
      -> documento o subarea         contenido
          -> evidencia, regla,       relaciones trazables
             proceso o herramienta
```

- `00-GESTION-POR-PROCESOS-GRH.md` es la entrada a la boveda. Su nombre es generico para acoger cualquier proceso del Gobierno Regional (`DEC-019`).
- Cada carpeta principal tiene una nota indice que funciona como mapa de contenido.
- Un subproceso o subarea con varios artefactos mantiene su propia nota indice.
- En `02-procesos` la jerarquia de carpetas reproduce la de procesos de la NT 002-2025-PCM-SGP: cada proceso es una carpeta nombrada con su codigo, anidada en la de su proceso padre, y su nota indice es la portada del proceso (`DEC-017`).
- Los procesos relacionados fuera de alcance existen como nodos de referencia: solo su nota indice, con `alcance_proyecto: REFERENCIA` (`DEC-019`).
- Los documentos no se mueven para representar estados; Git conserva el historial.

## Notas indice

Reglas adoptadas en `DEC-018` y ajustadas en `DEC-019`:

1. La nota indice de cada carpeta se llama `00-<nombre>.md`, donde `<nombre>` es el nombre de la carpeta sin su prefijo numerico.
2. Las mayusculas siguen la [convencion de nombres](convenciones-nombres.md): nota de entrada e indices de area completos en mayusculas (`00-PROCESOS.md`); procesos con el codigo NT en mayusculas (`00-S4-3-ejecucion-inversion.md`); demas indices en minusculas (`00-bases.md`).
3. Si el nombre resultante es generico o se repite en la boveda, se califica con su contexto: `00-originales-institucionales-grh.md`, `00-revisiones-conocimiento.md`.
4. Ningun otro archivo usa el prefijo `00-`. El prefijo identifica siempre una nota indice, tanto en el explorador como en el grafo.
5. `README.md` existe solo en la raiz, como portada del repositorio en GitHub y guia de instalacion.
6. Cada nota indice declara `aliases` con su nombre legible para el buscador rapido y el autocompletado de enlaces.

## Navegacion

1. Cada nota que necesite navegacion incluye al inicio una sola linea `Sube a: [Nombre](ruta)` hacia su nota indice inmediata.
2. Solo las notas indice de las areas principales suben a la nota de entrada; la ruta completa se recorre subiendo de indice en indice.
3. Una nota indice lista a sus hijos con una linea de descripcion y no copia su contenido.
4. Las secciones `Relaciones` expresan relaciones reales y no repiten la navegacion.
5. Las interacciones entre procesos se registran como enlaces en la seccion `Interacciones` de la nota indice del proceso en alcance, con el texto literal de su fuente. Las fichas aprobadas no se modifican para agregar enlaces.

## Tipos de relacion

| Relacion | Cuando se usa | Ejemplo |
|---|---|---|
| Padre-hijo | Pertenencia a un area o proceso | S4 -> S4.3 |
| Se rige por | Un artefacto debe cumplir un protocolo | Regla -> protocolo de conocimiento |
| Se sustenta en | Una afirmacion usa evidencia o norma | Actividad -> regla validada |
| Produce o transforma | Una etapa genera otro artefacto | Original -> extraccion |
| Implementa | Una herramienta automatiza una regla del metodo | Extractor -> protocolo documental |
| Valida | Una revision controla un producto | Evento de revision -> regla |
| Relacionado | Conexion util que no implica dependencia | Biblioteca BIM -> sustento de S4.3 |

No se crea un enlace solo para aumentar conexiones en el grafo. El texto que rodea al enlace debe explicar su significado.

## Convenciones

1. Usar enlaces Markdown relativos: `[Titulo](ruta/archivo.md)`.
2. Enlazar cada documento nuevo desde la nota indice de su area.
3. En documentos con varios niveles, incluir al inicio la linea `Sube a:` hacia su nota indice inmediata.
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

Los resultados se revisan por alcance: originales y binarios pueden no participar del grafo, pero todo Markdown de gobierno, conocimiento o procesos debe estar conectado a su mapa de contenido.

