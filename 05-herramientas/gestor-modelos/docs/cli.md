---
tipo: guia
area: herramientas
estado_documento: BORRADOR
clase_conocimiento: OBSERVADO
tags:
  - tema/automatizacion
---

# CLI de la aplicación

`modelador-procesos` es la entrada común del paquete Python. Las lecturas y observaciones comparten servicios con API y MCP; el comando `modelo` delega aún en el generador vigente.

Sube a: [Documentación de la aplicación](00-documentacion-aplicacion.md).

## Comandos

| Comando | Resultado |
|---|---|
| `arbol` | Árbol institucional en JSON |
| `proceso S4.3.2.3` | Datos y revisión de un proceso en JSON |
| `fuente <codigo> <referencia> <indice>` | Texto acotado de la fuente y página registrada, con hash y estado |
| `observaciones listar S4.3.2.3` | Registros y revisión vigente |
| `observaciones agregar <codigo> --texto ... --autor ... --revision ... [--elemento ...] [--tipo ...]` | Registro con ID y nueva revisión |
| `observaciones responder <codigo> <id> --texto ... --autor ... --revision ...` | Respuesta e historial con nueva revisión |
| `observaciones estado <codigo> <id> --valor ABIERTA\|RESUELTA --revision ... [--autor ...]` | Cambio de estado trazado |
| `modelo <codigo> [--check] [--exportar-imagenes]` | Salida y código de `modelar.py` |
| `api [--host 127.0.0.1] [--port 8000]` | Servidor HTTP local |
| `mcp [--transporte stdio]` | Servidor MCP local |
| `contrato [--check]` | Exporta `contracts/openapi.json` o comprueba que coincide con FastAPI |
| `sesiones iniciar <codigo>` | Captura árbol de trabajo y abre copia recuperable |
| `sesiones leer <codigo> <sesion>` | Manifiesto y preparación de la copia |
| `sesiones documento <codigo> <sesion> tabla\|sustento\|fuentes_visor` | Texto y hash de revisión |
| `sesiones editar <codigo> <sesion> <nombre> --archivo <ruta> --revision <hash>` | Sustituye solo el texto de la copia |
| `sesiones preparar <codigo> <sesion>` | Regenera copia, devuelve diff y D1–D5 |
| `sesiones integrar <codigo> <sesion> --revision <numero>` | Integra cambios preparados si el destino no cambió |
| `sesiones cerrar <codigo> <sesion>` | Libera editor; conserva instantánea y copia |

Se ejecuta desde la carpeta de la aplicación con `uv run modelador-procesos ...`. Un error de dominio se imprime en JSON en `stderr` y termina con código `1`; el comando `modelo` conserva el código de salida del generador. Los argumentos mal formados se rigen por `argparse`.

`contrato --check` devuelve `0` si el snapshot coincide con el schema generado y `1` si está desfasado. `contrato` sin `--check` sobrescribe únicamente el contrato generado, sin modificar procesos ni observaciones.
