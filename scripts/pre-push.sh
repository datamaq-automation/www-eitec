#!/bin/bash

# Inicio del cronómetro
start_time=$(date +%s)
echo "🚀 Ejecutando tests antes de hacer push... (Iniciado a las $(date +"%H:%M:%S"))"
export PYTHONPATH=$PYTHONPATH:.

# Preferir pytest del entorno virtual si existe
if [ -f "venv/bin/pytest" ]; then
    PYTEST="venv/bin/pytest"
elif [ -f "./venv/bin/pytest" ]; then
    PYTEST="./venv/bin/pytest"
else
    PYTEST="pytest"
fi

# Ejecutamos pytest con cobertura, umbral del 85% y generamos un reporte en consola al final
$PYTEST --cov=src --cov-report=term-missing --cov-fail-under=85 tests/
status=$?

end_time=$(date +%s)
duration=$((end_time - start_time))

if [ $status -eq 0 ]; then
    echo "✅ Todos los tests pasaron en ${duration}s. Continuando con el push."
    exit 0
else
    echo "❌ Los tests fallaron tras ${duration}s. Abortando push."
    exit 1
fi
