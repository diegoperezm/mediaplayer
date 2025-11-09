#!/usr/bin/env bash
set -e  # Detiene el script si algo falla

echo "🔍 Ejecutando Ruff..."
ruff check . --fix

echo "🧠 Ejecutando Mypy..."
mypy .

echo "🛡️ Ejecutando Bandit..."
bandit -r src/

echo "✅ Análisis completado con éxito."

