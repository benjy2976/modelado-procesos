---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: PROPUESTA
fecha_creacion: 2026-10-15
fecha_actualizacion: 2026-10-15
confidencialidad: INTERNO
tags:
  - tema/automatizacion
---

# Entorno propuesto para trabajo documental y desarrollo

Esta guia propone un conjunto local de herramientas para acelerar catalogacion, extraccion, trazabilidad y desarrollo. Distingue la instalacion observada de los usos futuros: disponer de una biblioteca no equivale a tener implementados el extractor, el validador normativo o una aplicacion web.

[Herramientas](00-HERRAMIENTAS.md) · Se rige por [Reproducibilidad](../00-gobernanza/reproducibilidad.md) y el [estandar de Obsidian](../00-gobernanza/estandar-obligatorio-obsidian.md).

## Instalacion observada

El 2026-10-15 se encontro Git con Git LFS 3.6.0. El lanzador de Windows reconoce CPython 3.14.3 de 64 bits, 3.10.11 de 32 bits y 3.9.13 de 32 bits; ademas existe Miniforge con Python 3.14.7 de 64 bits. El comando `python` apunta a 3.10.11 y `python3` a 3.14.3. Se creo `.venv` con CPython 3.14.7 de 64 bits, sin cambiar el Python predeterminado ni el `PATH` permanente del equipo.

El perfil ampliado admite CPython estable 3.11 o posterior. Python 3.10 no se adopta como minimo porque alcanzo fin de soporte el 2026-10-01, segun el [estado oficial de versiones de Python](https://devguide.python.org/versions/). La matriz objetivo actual comprende 3.11, 3.12, 3.13 y 3.14; en este equipo se ejecuto la prueba funcional con 3.14.7. Una version posterior puede intentar preparar el entorno, pero no se declara compatible hasta que resuelva el archivo fijado, instale todas las distribuciones y supere el verificador.

Las versiones de todas las dependencias, incluidas las transitivas, estan en [requirements-herramientas.txt](../requirements-herramientas.txt), con hashes de distribuciones. El inventario regenerable de cada equipo se escribe en `99-temporal/entorno-instalado.json` y no se versiona. La comprobacion se describe mas abajo; no certifica vigencia normativa ni seguridad integral de los paquetes.

## Herramientas del perfil ampliado

Los enlaces de esta tabla son referencias oficiales del proyecto o sus mantenedores en PyPI, consultadas el 2026-10-15. La columna de utilidad es una propuesta de aplicacion en este repositorio.

| Herramienta | Version fijada | Utilidad propuesta |
|---|---|---|
| [uv](https://docs.astral.sh/uv/) | 0.13.1 | Resolver dependencias y regenerar el archivo fijado con hashes. |
| [pypdf](https://pypi.org/project/pypdf/) | 6.10.0 | Medir texto por pagina y apoyar el evaluador documental existente. |
| [pdfplumber](https://pypi.org/project/pdfplumber/) | 0.11.10 | Extraer texto y tablas con posicion para contrastarlos con la pagina original. |
| [PyYAML](https://pypi.org/project/PyYAML/) | 6.0.3 | Leer reglas, metadatos y paquetes de contexto usando `safe_load`. |
| [jsonschema](https://pypi.org/project/jsonschema/) | 4.26.0 | Comprobar estructura de reglas y eventos; no validar su contenido juridico. |
| [lxml](https://pypi.org/project/lxml/) | 6.1.3 | Procesar XML BPMN y comprobarlo contra los esquemas oficiales de la OMG en la cadena BPMN (`DEC-025`). La prueba del verificador comprueba lectura XML. |
| [openpyxl](https://pypi.org/project/openpyxl/) | 3.1.5 | Leer y generar matrices XLSX. No calcula formulas como Excel. |
| [python-docx](https://pypi.org/project/python-docx/) | 1.2.0 | Producir borradores Word a partir de conocimiento trazable. |
| [ReportLab](https://pypi.org/project/reportlab/) | 5.0.1 | Generar reportes PDF derivados de datos y fuentes editables. |
| [Pillow](https://pypi.org/project/Pillow/) | 12.3.0 | Inspeccionar y preparar imagenes derivadas para revision documental. |
| [RapidFuzz](https://pypi.org/project/RapidFuzz/) | 3.14.6 | Sugerir coincidencias entre titulos, actores y terminos; requiere revision humana. |
| [pytest](https://docs.pytest.org/en/stable/) | 9.1.1 | Probar futuros extractores y validadores con casos controlados. |
| [Ruff](https://docs.astral.sh/ruff/) | 0.17.1 | Detectar errores comunes en scripts y mantener formato consistente. |

La cadena BPMN (`DEC-025`) necesita ademas Microsoft Edge o Google Chrome, que viene instalado en Windows 10 y 11, para generar las vistas SVG y PNG sin ventana; `verificar_entorno.py` informa una advertencia si no lo encuentra. bpmn-js no se instala con pip: se descarga una vez desde la URL fijada en `05-herramientas/gestor-modelos/bpmn-js.lock.json`, se comprueba por SHA-256 y se guarda en `99-temporal/herramientas/bpmn-js/`. Detalle en el [gestor local de modelos](gestor-modelos/00-gestor-modelos.md).

PDFMiner y PDFium llegan como dependencias de pdfplumber; no hace falta instalar Poppler para la comprobacion incluida. No se han instalado plugins de comunidad de Obsidian ni servicios de nube. Las operaciones de comprobacion usan datos sinteticos y memoria local, sin enviar documentos a servicios externos. Instalar o actualizar paquetes si requiere conexion al indice de paquetes.

## Guia al clonar en Windows

### Requisitos del equipo

Instalar Git desde [Git para Windows](https://git-scm.com/download/win), comprobar Git LFS y disponer de una version estable de CPython 3.11 o posterior. Obsidian se usa para autoria segun el estandar del proyecto. Si las aplicaciones ya existen, no es necesario reinstalarlas.

```powershell
git --version
git lfs version
py -0p
python3 --version
```

En el equipo observado, `python3` selecciona Python 3.14 de 64 bits y es apto para preparar el proyecto. Si no existe ningun interprete compatible, el administrador de Python permite instalar una version estable soportada; por ejemplo:

```powershell
py install 3.14
```

Si el comando no existe, instalar una version estable 3.11 o posterior desde [Python para Windows](https://www.python.org/downloads/windows/). Se recomienda la version estable mas reciente que figure en la matriz probada. Cerrar y abrir la terminal despues de instalar. En una red institucional, usar los instaladores e indices autorizados. No colocar credenciales en archivos versionados.

### Preparacion automatica

Reemplazar la URL de ejemplo por la del repositorio:

```powershell
git clone <URL-DEL-REPOSITORIO> modelado-procesos
cd modelado-procesos
git lfs install --local
git lfs pull
python3 05-herramientas/preparar_entorno.py
```

El preparador crea `.venv` si falta, exige CPython estable 3.11 o posterior, instala con `pip --require-hashes` y ejecuta la comprobacion funcional. Puede volver a ejecutarse; no borra el entorno existente ni elimina paquetes adicionales. Un entorno nuevo es la referencia para reproducir exactamente el conjunto. No requiere activar `.venv` ni cambiar la politica de ejecucion de PowerShell. Si `python3` no identifica un interprete compatible, se puede sustituir por `py -3.11`, `py -3.12`, `py -3.13`, `py -3.14` o por la ruta exacta de otro CPython compatible.

### Alternativa manual

```powershell
python3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --require-hashes -r requirements-herramientas.txt
.\.venv\Scripts\python.exe 05-herramientas/verificar_entorno.py
```

El perfil minimo anterior sigue disponible con `requirements.txt` para quien solo necesite el evaluador PDF. Instalar ambos perfiles en entornos separados si se desea comparar su reproducibilidad.

### Restaurar y auditar documentos

La instalacion de herramientas y la restauracion de documentos son pasos independientes:

```powershell
.\.venv\Scripts\python.exe 05-herramientas/catalogador-documental/descargar_recursos.py --modo restaurar
.\.venv\Scripts\python.exe 05-herramientas/auditar_reproducibilidad.py
```

El restaurador escribe solo recursos ausentes y verifica hashes; no sustituye originales existentes. Los recursos no disponibles o modificados requieren revision segun el protocolo. El auditor revisa la biblioteca, exclusiones y LFS; el verificador de entorno revisa herramientas. Se deben usar ambos para finalidades distintas.

### Uso diario

Seleccionar `.venv/Scripts/python.exe` como interprete del editor y ejecutar los scripts con esa ruta. Ejemplos:

```powershell
.\.venv\Scripts\python.exe 05-herramientas/verificar_entorno.py
.\.venv\Scripts\python.exe -m ruff check 05-herramientas/preparar_entorno.py 05-herramientas/verificar_entorno.py
.\.venv\Scripts\python.exe -m pytest --version
```

`pytest --version` solo comprueba la disponibilidad del ejecutor; no existe aun una suite general del proyecto. No aplicar correcciones masivas de Ruff al codigo existente sin revisar su alcance.

## Otros sistemas operativos

El preparador contempla `.venv/bin/python` en Linux/macOS. Con CPython estable 3.11 o posterior, Git y LFS disponibles:

```bash
python3 05-herramientas/preparar_entorno.py
.venv/bin/python 05-herramientas/verificar_entorno.py
```

El archivo fijado se resuelve universalmente desde Python 3.11 mediante el [mecanismo de resolucion universal de uv](https://docs.astral.sh/uv/concepts/resolution/). La prueba funcional local se ejecuto en Windows x64 con Python 3.14.7; la instalacion en Linux/macOS y las demas versiones de la matriz quedan pendientes de prueba funcional. La resolucion universal comprueba metadatos y marcadores, pero no sustituye la ejecucion en cada sistema.

## Mantenimiento de versiones

[requirements-herramientas.in](../requirements-herramientas.in) declara el conjunto directo; `.txt` es el resultado fijado que consume la instalacion. Mantener `pypdf` alineado con `requirements.txt`.

```powershell
# Regenerar para Python 3.11 y posteriores, preservando versiones compatibles ya fijadas.
.\.venv\Scripts\python.exe -m uv pip compile requirements-herramientas.in --universal --python-version 3.11 --generate-hashes --no-header --output-file requirements-herramientas.txt
# Para una actualizacion intencional, agregar --upgrade al comando anterior.
python3 05-herramientas/preparar_entorno.py
```

Revisar el diff, comprobar versiones y funciones, actualizar esta tabla y repetir la instalacion en entornos limpios para cada version de la matriz antes de ampliar la compatibilidad declarada. Los hashes verifican la distribucion descargada; no reemplazan la evaluacion del paquete. Las dependencias no se actualizan automaticamente al trabajar.

No existe una garantia tecnica honesta para todas las versiones futuras de Python. La politica es mantener el limite inferior sin fijar un limite superior artificial: una version nueva comienza como candidata, debe resolver e instalar las dependencias fijadas y superar `verificar_entorno.py`; despues se incorpora expresamente a la matriz probada. Un fallo obliga a actualizar o sustituir la dependencia afectada, nunca a omitir la comprobacion.

## Propuesta de ampliacion por necesidad

Estas herramientas quedan propuestas, sin instalar en esta intervencion. La seleccion evita decidir el framework web antes del hito previsto.

| Herramienta | Cuando incorporarla | Condicion de uso |
|---|---|---|
| [Tesseract OCR](https://tesseract-ocr.github.io/) y [OCRmyPDF](https://ocrmypdf.readthedocs.io/) | Primer lote confirmado sin texto aprovechable | Preparar dependencias y lenguaje espanol; procesar solo copias derivadas y revisar fidelidad. |
| [Pandoc](https://pandoc.org/) | Exportaciones repetidas de Markdown a Word/HTML | Definir plantilla y comprobar visualmente el resultado. |
| [bpmn.io](https://bpmn.io/) y Node.js LTS | Editor o renderizador BPMN integrado | Mantener `.bpmn` como fuente maestra y SVG/PDF como derivados; fijar dependencias cuando exista aplicacion. |
| [IfcOpenShell](https://ifcopenshell.org/) | Primer caso real de consulta IFC | Comprobar compatibilidad, tamano y necesidades de informacion antes de agregarlo. |

## Solucion de problemas

- **`python`, `python3` o `py` no encontrado:** abrir una terminal nueva y comprobar la instalacion. Usar la ruta del ejecutable compatible directamente si no existe el lanzador.
- **Git no disponible en esta sesion:** abrir una terminal nueva. Si existe en la ruta habitual, puede habilitarse solo para la sesion con `$env:PATH = 'C:\Program Files\Git\cmd;' + $env:PATH`. No reinstalar sin comprobarlo.
- **`.venv` usa otra version:** el preparador se detiene. Conservar o renombrar manualmente el entorno anterior antes de crear otro; el script no lo elimina.
- **Fallo de hash o descarga:** detenerse y revisar indice, proxy, conectividad o archivo fijado. No desactivar hashes ni verificaciones TLS.
- **Conexion restringida:** solicitar acceso al indice autorizado o preparar un repositorio de ruedas compatible con este archivo y plataforma.
- **Comprobacion funcional fallida:** consultar la salida y `99-temporal/entorno-instalado.json`; no declarar el entorno listo hasta resolverla.

## Pendientes y relaciones

La propuesta de herramientas no aprueba cambios metodologicos ni sustituye validacion humana. La instalacion observada es un hecho tecnico local. Esta guia implementa la preparacion del [area de herramientas](00-HERRAMIENTAS.md) y apoya los requisitos del [extractor](extractor-documental/00-extractor-documental.md) y del [validador](validador-conocimiento/00-validador-conocimiento.md).

Decision tecnica local de esta preparacion: conservar el perfil minimo y agregar un perfil ampliado con CPython estable 3.11 o posterior en `.venv`, sin dependencias globales. La compatibilidad se gobierna mediante un minimo, una matriz probada y una puerta de incorporacion para versiones futuras; su adopcion como estandar del equipo sigue siendo propuesta.

La auditoria documental ejecutada el 2026-10-15 encontro presentes y revisados los 219 recursos publicos indexados en esta copia local. La cache documental sigue siendo regenerable y no forma parte de Git. Esta intervencion no descargo ni modifico originales.

- Pendiente: probar clonacion desde otro equipo y transferencia LFS.
- Pendiente: probar instalacion fuera de Windows x64.
- Pendiente: desarrollar el extractor trazable y el validador de esquemas usando este entorno.
