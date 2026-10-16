---
id: GOV-PROP-NOTAS-INDICE-GRAFO
tipo: propuesta
area: gobernanza
estado_documento: VIGENTE
clase_conocimiento: DECISION
proceso: []
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/gobernanza
  - tema/obsidian
---

# Propuesta de nombres para notas indice y lectura del grafo

Propone reemplazar los `README.md` de la boveda por notas indice con nombre propio y ordenar los enlaces de navegacion. El objetivo es que el explorador y el grafo de Obsidian muestren la jerarquia de procesos y el conocimiento almacenado, y no una red de nodos llamados `README`. Aprobada por el equipo del proyecto el 2026-10-16 (`DEC-018`) e implementada el mismo dia; la columna "Actual" de la seccion 3.2 se conserva como registro de la correspondencia aplicada.

## 1. Diagnostico

Medicion sobre el repositorio al 2026-10-16 (commit `67ddd04`):

| Medida | Valor |
|---|---:|
| Notas Markdown | 77 |
| Notas llamadas `README.md` | 32 (42 %) |
| Enlaces internos entre notas | 319 |
| Enlaces que apuntan a una nota indice | 157 (49 %) |
| Enlaces que apuntan a `00-inicio.md` | 32 |

Efectos observados:

1. **Nombres repetidos.** El grafo rotula cada nodo con el nombre del archivo: hay 32 nodos `README` indistinguibles y el buscador rapido devuelve 32 coincidencias iguales.
2. **Estrella de navegacion.** Casi la mitad de los enlaces son de navegacion. La miga de pan `[Inicio]` de cada nota convierte a `00-inicio.md` en el nodo dominante, y el conocimiento real (fichas, sustentos, reglas, decisiones) queda en la periferia.
3. **Orden del explorador.** `README.md` se ordena alfabeticamente entre los demas archivos y no aparece como portada de la carpeta.

## 2. Alternativas evaluadas

| Alternativa | Ventajas | Desventajas | Evaluacion |
|---|---|---|---|
| A. Mantener `README.md` y agregar `aliases` | Sin migracion; GitHub muestra el README al abrir cada carpeta | El grafo y el explorador siguen mostrando `README`; el alias solo ayuda al buscador | Insuficiente |
| B. Nota con el mismo nombre de la carpeta (`s4-3-ejecucion-inversion/s4-3-ejecucion-inversion.md`) | Nombre unico y descriptivo; convencion conocida de "nota de carpeta" | Queda ordenada en medio de los archivos del proceso (`s4-3-diagrama...`, `s4-3-ejecucion...`, `s4-3-ficha...`) | Aceptable |
| C. Prefijo `00-` mas el nombre de la carpeta (`00-s4-3-ejecucion-inversion.md`) | Nombre unico y descriptivo; aparece primero entre los archivos; el prefijo identifica a simple vista que el nodo es un indice; coherente con `00-inicio.md` | GitHub deja de mostrar automaticamente el indice de cada carpeta; agrega tres caracteres al nombre | **Recomendada** |
| D. Plugin de comunidad "Folder Notes" (la carpeta abre su nota) o "Front Matter Title" (rotula con el titulo) | Mejor experiencia: la nota se oculta o el grafo muestra el titulo | Plugins de comunidad en modo restringido (estandar de Obsidian, seccion 16); dependencia externa | Evaluable mas adelante, complementaria a C |

Limitacion de Obsidian sin plugins: el explorador muestra siempre las subcarpetas antes que los archivos. Con la alternativa C, la nota indice queda primera entre los archivos de su carpeta, debajo de las subcarpetas.

## 3. Propuesta

### 3.1 Regla de nombres

1. La nota indice de cada carpeta se llama `00-<nombre>.md`.
2. `<nombre>` es el nombre de la carpeta sin su prefijo numerico: `02-procesos/` -> `00-procesos.md`; `s4-3-ejecucion-inversion/` -> `00-s4-3-ejecucion-inversion.md`.
3. Si el nombre resultante es generico o se repite en la boveda, se califica con su contexto: `originales/` -> `00-originales-institucionales-grh.md`; `revisiones/` -> `00-revisiones-conocimiento.md`.
4. Ningun otro archivo usa el prefijo `00-`, salvo `00-inicio.md` en la raiz. Asi el prefijo significa siempre "nota indice".
5. Se conserva `README.md` solo en la raiz, como portada del repositorio en GitHub y guia de instalacion. `00-inicio.md` sigue siendo la entrada de la boveda.
6. Cada nota indice declara `aliases` con su nombre legible, por ejemplo `S4.3 Ejecucion de la inversion`, para el buscador rapido y el autocompletado de enlaces.

### 3.2 Correspondencia

| Actual | Propuesto |
|---|---|
| `00-gobernanza/00-gobernanza.md` | `00-gobernanza/00-gobernanza.md` |
| `00-gobernanza/iniciativas/00-iniciativas.md` | `00-iniciativas.md` |
| `00-gobernanza/plantillas/00-plantillas.md` | `00-plantillas.md` |
| `01-referencias/00-referencias.md` | `00-referencias.md` |
| `01-referencias/01-institucionales-grh/originales/00-originales-institucionales-grh.md` | `00-originales-institucionales-grh.md` |
| `01-referencias/02-gestion-por-procesos/originales/00-originales-gestion-por-procesos.md` | `00-originales-gestion-por-procesos.md` |
| `01-referencias/03-invierte-pe/00-invierte-pe.md` | `00-invierte-pe.md` |
| `01-referencias/04-contrataciones-publicas/00-contrataciones-publicas.md` | `00-contrataciones-publicas.md` |
| `01-referencias/05-control-gubernamental/00-control-gubernamental.md` | `00-control-gubernamental.md` |
| `01-referencias/06-presupuesto-y-administracion/00-presupuesto-y-administracion.md` | `00-presupuesto-y-administracion.md` |
| `01-referencias/07-normativa-tecnica-sectorial/00-normativa-tecnica-sectorial.md` | `00-normativa-tecnica-sectorial.md` |
| `01-referencias/08-bim/00-bim.md` | `00-bim.md` |
| `01-referencias/09-derivados-texto/00-derivados-texto.md` | `00-derivados-texto.md` |
| `02-procesos/00-procesos.md` | `00-procesos.md` |
| `02-procesos/mapa-de-procesos-institucional/00-mapa-de-procesos-institucional.md` | `00-mapa-de-procesos-institucional.md` |
| `02-procesos/s4-gestion-de-las-inversiones/00-s4-gestion-de-las-inversiones.md` | `00-s4-gestion-de-las-inversiones.md` |
| `.../s4-3-ejecucion-inversion/README.md` | `00-s4-3-ejecucion-inversion.md` |
| `02-procesos/to-be/00-to-be.md` | `00-to-be.md` |
| `03-conocimiento/00-conocimiento.md` | `00-conocimiento.md` |
| `03-conocimiento/revisiones/00-revisiones-conocimiento.md` | `00-revisiones-conocimiento.md` |
| `04-coordinacion/00-coordinacion.md` | `00-coordinacion.md` |
| `04-coordinacion/bases/00-bases.md` | `00-bases.md` |
| `04-coordinacion/canvas/00-canvas.md` | `00-canvas.md` |
| `04-coordinacion/diario/00-diario.md` | `00-diario.md` |
| `04-coordinacion/reuniones/00-reuniones.md` | `00-reuniones.md` |
| `05-herramientas/00-herramientas.md` | `00-herramientas.md` |
| `05-herramientas/extractor-documental/00-extractor-documental.md` | `00-extractor-documental.md` |
| `05-herramientas/gestor-modelos/00-gestor-modelos.md` | `00-gestor-modelos.md` |
| `05-herramientas/validador-conocimiento/00-validador-conocimiento.md` | `00-validador-conocimiento.md` |
| `90-bandeja-entrada/00-bandeja-entrada.md` | `00-bandeja-entrada.md` |
| `99-temporal/00-temporal.md` | `00-temporal.md` |

Los `README.md` dentro de carpetas `originales` son notas descriptivas, no documentos originales; su cambio de nombre no altera ningun original protegido.

### 3.3 Regla de enlaces de navegacion

1. Cada nota enlaza hacia arriba solo a su indice inmediato, por ejemplo `Sube a: [S4.3 Ejecucion de la inversion](00-s4-3-ejecucion-inversion.md)`.
2. Solo las notas indice de las areas principales enlazan a `00-inicio.md`. La ruta completa se recorre subiendo de indice en indice.
3. Una nota indice lista a sus hijos con una linea de descripcion; no copia su contenido.
4. Los enlaces de la seccion `Relaciones` expresan relaciones reales (se rige por, se sustenta en, produce, implementa, valida) y no repiten la navegacion.

Resultado esperado: el grafo dibuja el arbol de areas y procesos, y sobre el se ven las relaciones de conocimiento. Los enlaces a `00-inicio.md` pasan de 32 a 10 (los indices de las ocho areas, el `README.md` raiz y la mencion del mapa raiz en el estandar de Obsidian).

### 3.4 Lectura del grafo con funciones nativas

El grafo de Obsidian permite filtros y grupos de color mediante busquedas, incluidas las de propiedades (`[propiedad:valor]`). Se proponen grupos comunes:

| Grupo | Consulta | Color sugerido |
|---|---|---|
| Notas indice | `[tipo:mapa-de-contenido]` | Gris |
| Documentos NT | `[documento_nt:ficha-producto-proceso] OR [documento_nt:ficha-indicador] OR [documento_nt:procedimiento]` | Azul |
| Sustentos | `file:sustento` | Turquesa |
| Conocimiento | `path:03-conocimiento` | Verde |
| Referencias | `path:01-referencias` | Marron |
| Gobernanza | `path:00-gobernanza` | Morado |

Y dos filtros de uso:

- **Vista de navegacion:** sin filtro; muestra el arbol completo.
- **Vista de conocimiento:** `-[tipo:mapa-de-contenido] -file:00-inicio -path:00-gobernanza/plantillas`; oculta indices y plantillas y deja solo el conocimiento y sus relaciones.

Las consultas se probaran en la version de Obsidian del equipo durante la implementacion. Para trabajar en un proceso se recomienda el grafo local de su nota indice con profundidad 2.

`.obsidian/graph.json` permanece excluido de Git: Obsidian reescribe en ese archivo el zoom y otros valores en cada uso, lo que generaria cambios constantes. La configuracion comun se documenta en el estandar de Obsidian y podra aplicarse con un script local opcional que escriba los grupos en el archivo de cada persona.

## 4. Impactos

- 31 archivos renombrados con `git mv` y 149 menciones a `README` en notas Markdown, actualizadas con el script de reescritura de rutas ya utilizado en `DEC-017`.
- `.gitignore` (`!99-temporal/00-temporal.md`) y el Canvas `flujo-del-conocimiento.canvas` (5 referencias).
- Documentos de reglas: `AGENTS.md` ("leer el README del area"), arquitectura de informacion, estandar de Obsidian (secciones 3.1, 7 y 8), estandar de artefactos (contrato de archivos) y `02-procesos` (tabla de documentos).
- Plantillas de portada de proceso y de mapa de contenido.
- El auditor de reproducibilidad solo exige el `README.md` raiz, que se conserva.
- GitHub deja de mostrar automaticamente el indice al abrir cada carpeta. Obsidian es el entorno obligatorio de produccion (`DEC-011`), por lo que el costo se considera aceptable.

## 5. Implementacion propuesta

1. Aprobacion de esta propuesta y registro de `DEC-018`.
2. Renombrar con `git mv` segun la tabla de la seccion 3.2.
3. Reescribir enlaces, el Canvas y `.gitignore` con el script de rutas.
4. Ajustar las migas de pan segun la seccion 3.3 y agregar `aliases` a las notas indice.
5. Actualizar `AGENTS.md`, estandares, arquitectura de informacion y plantillas.
6. Documentar los grupos y filtros del grafo en el estandar de Obsidian.
7. Verificar: cero enlaces rotos, cero notas huerfanas, ningun `README.md` fuera de la raiz y auditoria de reproducibilidad apta.

## 6. Decisiones requeridas

1. Adoptar la alternativa C (`00-<nombre>.md`) u otra.
2. Confirmar que el `README.md` raiz se conserva para GitHub.
3. Confirmar la regla de navegacion: enlace solo al indice inmediato y a `00-inicio.md` solo desde las areas.
4. Decidir si se prepara el script local que aplica los grupos de color del grafo.

## Relaciones

- Modifica: [arquitectura de informacion y enlaces](arquitectura-de-informacion.md).
- Se rige por: [estandar obligatorio de Obsidian](estandar-obligatorio-obsidian.md).
- Continua: [estructura centrada en procesos](propuesta-estructura-intuitiva.md) (`DEC-017`).
