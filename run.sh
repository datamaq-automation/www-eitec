#!/usr/bin/env bash
set -e

# Detectar directorio del script
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Activar venv si existe
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Asegurar que 'src' esté en PYTHONPATH para resolver imports
export PYTHONPATH="${PROJECT_DIR}/src:${PYTHONPATH:-}"

# Ejecutar Uvicorn apuntando al módulo correcto
exec uvicorn infrastructure.fastapi.app:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload