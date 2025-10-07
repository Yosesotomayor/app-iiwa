#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de ejecución para App IIWA con UV
"""

import subprocess
import sys
from pathlib import Path

def main():
    """Ejecuta la aplicación usando UV"""
    project_root = Path(__file__).parent
    
    print("🚀 Iniciando App IIWA con UV...")
    
    # Verificar que UV está instalado
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("❌ UV no está instalado")
        print("📦 Instala UV: https://github.com/astral-sh/uv")
        print("   macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh")
        print("   Windows: powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
        sys.exit(1)
    
    # Ejecutar la aplicación
    try:
        subprocess.run(["uv", "run", "python", "-m", "app_iiwa"], 
                      cwd=project_root, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando la aplicación: {e}")
        print("💡 Intenta: uv sync")
        sys.exit(1)

if __name__ == "__main__":
    main()