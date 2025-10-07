#!/bin/bash

# Script de inicio rápido para App IIWA
# Detecta automáticamente la mejor forma de ejecutar la aplicación

echo "🚀 App IIWA - Inicio Rápido"
echo "============================"

# Verificar si estamos en macOS y silenciar warnings de Tk
if [[ "$OSTYPE" == "darwin"* ]]; then
    export TK_SILENCE_DEPRECATION=1
    echo "✅ macOS detectado - Configuración aplicada"
fi

# Intentar con UV primero
if command -v uv &> /dev/null; then
    echo "✅ UV encontrado - Usando UV"
    uv run python -m app_iiwa
elif command -v python3 &> /dev/null; then
    echo "✅ Python3 encontrado - Usando Python del sistema"
    python3 run.py
elif command -v python &> /dev/null; then
    echo "✅ Python encontrado - Usando Python"
    python run.py
else
    echo "❌ Error: No se encontró Python en el sistema"
    echo "💡 Instala Python 3.9+ desde https://python.org"
    exit 1
fi