---
tipo: especificacion-herramienta
area: herramientas
estado_documento: VIGENTE
clase_conocimiento: DECISION
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-19
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
aliases:
  - Gestor local de modelos
---

# Gestor local de modelos

Este directorio implementa la [iniciativa de modelamiento hibrido](../../00-gobernanza/iniciativas/iniciativa-modelamiento-hibrido.md) con dos cadenas locales, sin servicios externos al renderizar:

- **PlantUML**, para vistas conceptuales que no son BPMN y modelos logicos ya iniciados en `.puml`.
- **Cadena BPMN** (`DEC-025`), para los diagramas de proceso: tabla en Markdown, BPMN 2.0 generado y validado, y vistas SVG y PNG producidas con bpmn-js.

Ninguna herramienta modifica la semantica del modelo por su cuenta ni otorga aprobacion humana.

## Dependencias

- Python 3.11 o posterior, con `lxml` (fijado en `requirements-herramientas.txt`).
- PlantUML: Windows x64, o Java 11 o posterior en otras plataformas.
- Cadena BPMN: Microsoft Edge o Google Chrome instalado. Otra ruta se indica en la variable `BPMN_NAVEGADOR`.
- Acceso a internet solo la primera vez, para descargar los artefactos fijados en `plantuml.lock.json` y `bpmn-js.lock.json`. Se comprueban por SHA-256 y se guardan en `99-temporal/herramientas/` (no se versionan).

## Cadena BPMN

```text
<codigo>-diagrama-proceso-tabla.md --tabla_a_bpmn.py--> <codigo>-diagrama-proceso.bpmn
                                                           |-- validacion D1-D3 y trazado D4
                                                           |-- renderizar_bpmn.py --> .svg (Obsidian) y .png
                                                           `-- copia para Bizagi (opcional, edicion manual)
```

| Archivo | Funcion |
|---|---|
| `tabla_a_bpmn.py` | Lee la tabla o lista, calcula el trazado, genera el `.bpmn`, lo valida, produce la copia para Bizagi y una vista HTML local |
| `_validar_bpmn.py` | D1 esquema oficial de la OMG, D2 referencias, D3 bloqueos y elementos inalcanzables (juego de tokens) |
| `_revisar_trazado.py` | D4: flujos que atraviesan elementos o etiquetas, flujos superpuestos, mensajes que cruzan pools ajenos, etiquetas montadas |
| `_bpmn_a_bizagi.py` | Copia en el dialecto que importa Bizagi Modeler; agrega el proceso vacio que Bizagi exige en los pools cerrados |
| `renderizar_bpmn.py` | SVG y PNG con bpmn-js en Edge o Chrome sin ventana; colores de estilo Bizagi solo en los derivados |
| `bpmn-js.lock.json` | Version, URL y SHA-256 de bpmn-js |
| `xsd_bpmn20/` | Esquemas oficiales BPMN 2.0 de la OMG |

### Uso

Desde la raiz del repositorio:

```powershell
# 1. Generar y validar el BPMN desde la tabla
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\tabla_a_bpmn.py `
  02-procesos\...\<codigo>-diagrama-proceso-tabla.md 99-temporal\modelos\<codigo>

# 2. Generar las vistas versionadas
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_bpmn.py `
  02-procesos\...\<codigo>-diagrama-proceso.bpmn `
  --output 02-procesos\...\<codigo>-diagrama-proceso.svg `
  --png 02-procesos\...\<codigo>-diagrama-proceso.png

# 3. Comprobar que el SVG versionado esta al dia, sin sobrescribirlo
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_bpmn.py `
  02-procesos\...\<codigo>-diagrama-proceso.bpmn `
  --output 02-procesos\...\<codigo>-diagrama-proceso.svg --check
```

`tabla_a_bpmn.py` escribe en la carpeta indicada `<nombre>.bpmn`, `validacion.txt`, `bizagi/<nombre>_bizagi.bpmn` y `<nombre>_visor.html`. El `.bpmn` que se versiona en la carpeta del proceso se copia desde ahi con el nombre `<codigo>-diagrama-proceso.bpmn`, una vez que la validacion no presenta hallazgos o estos quedan explicados en el sustento. Sin carpeta de salida, los resultados van a `salida/`, que Git ignora.

### Entrada

La fuente se redacta con la [plantilla de diagrama en tabla](../../00-gobernanza/plantillas/modelamiento/diagrama-proceso-tabla.md): tablas `## Pools`, `## Elementos` y `## Mensajes`. Las columnas adicionales, como `Clase` y `Fuente`, no se dibujan y sostienen la trazabilidad. Tambien se admite el formato de lista (`## Pool: X`, `### Carril`, `- ID (tipo) Nombre -> siguientes`).

Tipos admitidos: inicio, inicio-mensaje, inicio-temporizador, tarea, tarea-usuario, tarea-manual, tarea-servicio, subproceso, compuerta, compuerta-paralela, compuerta-inclusiva, temporizador, mensaje-recepcion, mensaje-envio, fin, fin-mensaje y fin-terminal.

### Trazado

Columnas por orden del flujo; una fila por rama de cada compuerta dentro del carril; flujos en angulo recto que esquivan cajas y etiquetas; puertos de mensaje repartidos; pools externos cerrados en bandas, los que envian arriba y los que reciben abajo, junto al elemento con el que se comunican; etiquetas dimensionadas segun su texto. El control D4 informa cualquier superposicion restante.

### Vistas SVG y PNG

`renderizar_bpmn.py` carga el BPMN en bpmn-js (`bpmn-navigated-viewer` 17.11.1) dentro de Edge o Chrome sin ventana, con un perfil temporal propio, y obtiene el SVG mediante la exportacion oficial de bpmn-js. El PNG es una captura de ese SVG (escala 2 por defecto). Los colores de estilo Bizagi y las etiquetas en negro se aplican a una copia en memoria: el `.bpmn` fuente no cambia. El SVG lleva la marca `GENERADO - NO EDITAR` y numera las flechas en orden fijo, de modo que la misma entrada produce los mismos bytes en el mismo equipo. La ubicacion del texto depende de las fuentes instaladas: `--check` debe ejecutarse en el entorno de referencia del proyecto.

La licencia de bpmn-js (MIT con clausula de marca de agua) exige no retirar ni alterar la marca de agua de bpmn.io en aplicaciones o sitios. El proyecto no modifica la biblioteca; la vista HTML la conserva.

### Bizagi

La copia `bizagi/<nombre>_bizagi.bpmn` se importa en Bizagi Modeler (Archivo > Importar > BPMN). Importacion probada con Bizagi Modeler 4.2 el 2026-10-19. Bizagi recorta etiquetas largas: la herramienta avisa cuando un nombre de evento o compuerta supera 40 caracteres o un mensaje supera 50. El camino de vuelta desde Bizagi (`.bpm` a BPMN) esta pendiente de adaptar.

### Limites

- No genera todavia subprocesos de evento, eventos de borde, eventos de senal o condicionales ni anotaciones; se documentan en el sustento hasta que se incorporen.
- Un nombre de carril no puede contener ";".
- En la etapa formal, el `.bpmn` pasa a ser la fuente maestra y la tabla queda como antecedente (estandar de artefactos, seccion 5).

### Procedencia de los esquemas

Copias identicas, verificadas el 2026-10-19, de los esquemas publicados por la OMG en `https://www.omg.org/spec/BPMN/20100501/`:

| Archivo | SHA-256 |
|---|---|
| `BPMN20.xsd` | `A07C159CB0594573DD7C97B1370DD116112378F377E43C89A8BF512AC5030705` |
| `BPMNDI.xsd` | `F0DFF1CD559D1514D8EBFC8C646F58402BCACED27EC22E2AA6456C2DCC80B038` |
| `DC.xsd` | `A2F90E5AD9BB48C6915E4E034B4E27AC838264A1D4F27BFC70DBDFC69351312D` |
| `DI.xsd` | `8220B179C175572DF74E08A51BFFABE957867962035CEE7B5FEE0B6ACB4C4498` |
| `Semantic.xsd` | `C4318842F7D2BBC262D7954C9452C501DB16F0868EAC0B8732EC5D7FB384D9A7` |

El validador y la herramienta provienen del proyecto de la directiva SGE; el trazado, el control D4 y el conversor para Bizagi se rehicieron en este proyecto (`DEC-025`).

## PlantUML

En Windows x64 se usa la [distribucion nativa oficial de PlantUML 1.2026.8](https://github.com/plantuml/plantuml/releases/tag/v1.2026.8), sin depender del Java global. En otras plataformas se usa el JAR con Java 11 o posterior. Los binarios se almacenan en `99-temporal/herramientas/plantuml/`.

```powershell
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_plantuml.py `
  02-procesos\S4-gestion-de-las-inversiones\S4-diagrama-proceso-logico.puml `
  --output 02-procesos\S4-gestion-de-las-inversiones\S4-diagrama-proceso-logico.svg

# Comprobar sin sobrescribir
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_plantuml.py `
  02-procesos\S4-gestion-de-las-inversiones\S4-diagrama-proceso-logico.puml `
  --output 02-procesos\S4-gestion-de-las-inversiones\S4-diagrama-proceso-logico.svg --check
```

La descarga falla si el contenido remoto no coincide con el hash fijado. La salida se escribe de forma atomica y `--check` devuelve un codigo distinto de cero cuando falta o difiere el SVG.

## Relaciones

- [Estandar de artefactos de modelamiento](../../00-gobernanza/estandar-artefactos-modelamiento.md)
- [Plantilla de diagrama en tabla](../../00-gobernanza/plantillas/modelamiento/diagrama-proceso-tabla.md)
- [Plantilla de modelo logico con carriles](../../00-gobernanza/plantillas/modelamiento/modelo-logico-carriles.puml)
- [Registro de decisiones](../../00-gobernanza/registro-decisiones.md)
- [S4 Gestion de las inversiones](../../02-procesos/S4-gestion-de-las-inversiones/S4-ficha-producto-proceso.md)
