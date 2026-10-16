---
tipo: especificacion-herramienta
area: herramientas
estado_documento: VIGENTE
clase_conocimiento: DECISION
fecha_creacion: 2026-10-16
fecha_actualizacion: 2026-10-16
responsable: equipo-proyecto
confidencialidad: INTERNO
tags:
  - tema/automatizacion
  - tema/procesos
aliases:
  - Gestor local de modelos
---

# Gestor local de modelos

Este directorio inicia la Fase 1 de la [iniciativa de modelamiento hibrido](../../00-gobernanza/iniciativas/iniciativa-modelamiento-hibrido.md). Por ahora fija PlantUML y permite producir o comprobar un SVG desde una fuente `.puml` sin utilizar servicios externos. No modifica la semantica del modelo ni otorga aprobacion humana.

## Dependencias

- Python 3.11 o posterior.
- Windows x64, o Java 11 o posterior en otras plataformas.
- Acceso a internet solo la primera vez, para descargar el artefacto oficial fijado en `plantuml.lock.json`.

En Windows x64 se usa la [distribucion nativa oficial de PlantUML 1.2026.8](https://github.com/plantuml/plantuml/releases/tag/v1.2026.8), sin depender del Java global. En otras plataformas se usa el JAR con Java 11 o posterior. Los binarios no se versionan: se almacenan en `99-temporal/herramientas/plantuml/`, se comprueban mediante SHA-256 y pueden reconstruirse desde el archivo de bloqueo.

## Uso

Desde la raiz del repositorio:

```powershell
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_plantuml.py `
  02-procesos\s4-gestion-de-las-inversiones\s4-diagrama-proceso-logico.puml `
  --output 02-procesos\s4-gestion-de-las-inversiones\s4-diagrama-proceso-logico.svg
```

Para comprobar que el derivado versionado esta actualizado sin sobrescribirlo:

```powershell
.\.venv\Scripts\python.exe 05-herramientas\gestor-modelos\renderizar_plantuml.py `
  02-procesos\s4-gestion-de-las-inversiones\s4-diagrama-proceso-logico.puml `
  --output 02-procesos\s4-gestion-de-las-inversiones\s4-diagrama-proceso-logico.svg `
  --check
```

La descarga falla si el contenido remoto no coincide con el hash fijado. La salida se escribe de forma atomica y el comando `--check` devuelve un codigo distinto de cero cuando falta o difiere el SVG.

## Relaciones

- [Estandar de artefactos de modelamiento](../../00-gobernanza/estandar-artefactos-modelamiento.md)
- [Plantilla de modelo logico con carriles](../../00-gobernanza/plantillas/modelamiento/modelo-logico-carriles.puml)
- [S4 Gestion de las inversiones](../../02-procesos/s4-gestion-de-las-inversiones/s4-ficha-producto-proceso.md)
