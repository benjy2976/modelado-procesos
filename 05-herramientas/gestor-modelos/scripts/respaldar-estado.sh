#!/usr/bin/env bash
# Respalda el estado operativo que vive fuera de Git (plan B, docs/plan-versiones-validacion.md):
# sesiones de edición (instantáneas y copias), registro de versiones y cola de trabajos de agentes.
# Uso: scripts/respaldar-estado.sh [destino]   (por defecto ~/respaldos/modelado-procesos)
# Conserva los 30 respaldos más recientes. No modifica el repositorio.
set -euo pipefail

raiz="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
destino="${1:-$HOME/respaldos/modelado-procesos}"
sello="$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$destino"

carpetas=()
for c in .mesa-sesiones .mesa-versiones .mesa-trabajos; do
  [ -d "$raiz/$c" ] && carpetas+=("$c")
done
if [ "${#carpetas[@]}" -eq 0 ]; then
  echo "Nada que respaldar en $raiz"
  exit 0
fi

archivo="$destino/estado-$sello.tar.gz"
tar -C "$raiz" -czf "$archivo" "${carpetas[@]}"
tar -tzf "$archivo" > /dev/null
echo "Respaldo verificado: $archivo ($(du -h "$archivo" | cut -f1); ${carpetas[*]})"

# Retención: los 30 más recientes.
# Los nombres llevan sello UTC ordenable, así que el orden alfabético inverso es el cronológico inverso.
mapfile -t viejos < <(find "$destino" -maxdepth 1 -name 'estado-*.tar.gz' -printf '%f\n' | sort -r | tail -n +31)
for v in "${viejos[@]}"; do rm -f -- "$destino/$v"; done
