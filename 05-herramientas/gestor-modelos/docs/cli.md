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

La preparación documental de las fases 1 y 2 usa `fuentes inventariar`, `fuentes diagnosticar-texto [--max-documentos N]`, `fuentes planificar-extraccion`, `fuentes priorizar --proceso S4.3.2`, `fuentes extraer --metodo nativo|ocr [--max-documentos N]`, `fuentes evaluar-extraccion` y `fuentes preparar-cotejo --id <ID> --pagina N [--archivo <ruta-registrada>]`. `--archivo` distingue un ID usado por varios PDF. `fuentes resolver-colisiones-cache` separa derivados históricos que compartían ID y hash pese a corresponder a rutas distintas; `fuentes aislar-paginas-ocr` reconstruye páginas OCR intermedias en una carpeta propia por PDF. Ninguno cambia los originales.

Estos comandos producen un manifiesto y Markdown paginado en `01-referencias/09-derivados-texto/cache/`, excluida de Git. El umbral inicial de 80 caracteres por página decide si se intenta OCR; no acredita fidelidad ni vigencia. OCR requiere `OCR_MCP_KEY` en el entorno local y procesa copias derivadas de PDF con URL pública HTTPS registrada y hash coincidente. Para un documento sin URL cuya procedencia se haya revisado, `fuentes extraer --metodo ocr --permitir-id-sin-url <ID>` habilita solo ese ID; el argumento puede repetirse. Los demás quedan pendientes. El PDF original no se altera.

| Comando | Resultado |
|---|---|
| `arbol` | Árbol institucional en JSON |
| `proceso S4.3.2.3` | Datos y revisión de un proceso en JSON |
| `fuente <codigo> <referencia> <indice>` | Texto acotado de la fuente y página registrada, con hash y estado |
| `fuentes` | Grupo de preparación documental; requiere una operación |
| `fuentes inventariar` | Reconciliación de PDF, catálogo, hashes y duplicados |
| `fuentes diagnosticar-texto [--max-documentos N]` | Medición de texto nativo por página |
| `fuentes planificar-extraccion` | Cola de extracción nativa y OCR selectivo |
| `fuentes priorizar --proceso <codigo>` | Prioridad provisional según citas en tablas y sustentos |
| `fuentes extraer --metodo nativo\|ocr [--max-documentos N]` | Markdown paginado o OCR sobre copias derivadas |
| `fuentes evaluar-extraccion` | Integridad, paginación y señales de cotejo |
| `fuentes preparar-cotejo --id <ID> --pagina N [--archivo <ruta-registrada>]` | Vista local de original y texto |
| `fuentes resolver-colisiones-cache` | Separa derivados históricos con procedencia diferente |
| `fuentes aislar-paginas-ocr` | Aísla páginas OCR intermedias de cada PDF |
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
