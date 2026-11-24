---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: NO-APLICA
tags:
  - tema/automatizacion
---

# Traslado del proyecto entre equipos

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

El [script de traslado](../scripts/trasladar_proyecto.py) crea un ZIP para aplicar **encima de un clon del mismo commit**. Incluye archivos que no están en Git, los ignorados por Git y los cambios locales de archivos versionados. Por tanto conserva los PDF descargados, `01-referencias/09-derivados-texto/cache/` con la extracción y OCR de las fases 1 y 2, `99-temporal/` y las sesiones `.mesa-sesiones/`. El manifiesto registra el commit base, rutas, tamaños y SHA-256; `verificar` vuelve a calcular los hashes antes de restaurar.

Se excluyen `.git`, `.venv`, `node_modules`, cachés de compilación y prueba, `.mesa-local`, archivos `.env` y claves reconocibles por nombre o extensión. El paquete **no contiene ni reconstruye `OCR_MCP_KEY`**, y la configuración del MCP OCR debe hacerse con la credencial y permisos del nuevo equipo. Los resultados ya obtenidos se pueden leer sin repetir el OCR. Revise el contenido del ZIP antes de transferirlo si existen otros archivos locales con datos sensibles que no siguen esos nombres.

En el equipo de origen, después de publicar el commit que se va a clonar, ejecute desde la raíz del repositorio:

```powershell
python 05-herramientas/gestor-modelos/scripts/trasladar_proyecto.py exportar D:\traslado\ejecucion-local.zip
python 05-herramientas/gestor-modelos/scripts/trasladar_proyecto.py verificar D:\traslado\ejecucion-local.zip
Get-FileHash D:\traslado\ejecucion-local.zip -Algorithm SHA256
```

Copie el ZIP fuera del repositorio y compare su SHA-256 en el otro equipo. Clone el repositorio con Git LFS si corresponde, colóquelo en el commit indicado por `verificar` y, sobre un clon limpio, ejecute:

```powershell
python 05-herramientas/gestor-modelos/scripts/trasladar_proyecto.py restaurar D:\traslado\ejecucion-local.zip
git status --short
```

La restauración comprueba el commit, la limpieza del clon, cada entrada del ZIP y la ausencia de archivos locales con el mismo nombre. No toca `.git` ni borra directorios; reproduce únicamente las eliminaciones locales de archivos versionados registradas en el manifiesto. Si la verificación falla, no restaura nada. Instale después las dependencias de Python y Nuxt en el nuevo equipo; esas carpetas no forman parte del paquete.

Este mecanismo conserva el trabajo del repositorio, no el historial de conversación del agente ni los servicios y permisos de Windows. El [plan de corrida](plan-corrida-documental-y-auditoria.md) y el [informe de preparación PDF](informe-preparacion-biblioteca-pdf.md) registran las decisiones y resultados necesarios para continuar el análisis sin reconstruir el contexto desde cero.
