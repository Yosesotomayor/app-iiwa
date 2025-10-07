#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de ejecución para App IIWA con UV
Maneja automáticamente problemas de tkinter en macOS
"""

import subprocess
import sys
import os
from pathlib import Path

def check_tkinter():
    """Verifica si tkinter funciona correctamente"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw() 
        root.destroy()
        return True, None
    except Exception as e:
        return False, str(e)

def get_system_python():
    """Encuentra el Python del sistema que tiene tkinter funcionando"""
    possible_pythons = [
        "/usr/bin/python3",
        "/System/Library/Frameworks/Python.framework/Versions/3.9/bin/python3",
        "/System/Library/Frameworks/Python.framework/Versions/3.8/bin/python3",
        "/usr/local/bin/python3",
        "python3",
        "python"
    ]

    for python_cmd in possible_pythons:
        try:
            # Verificar que existe y puede importar tkinter
            result = subprocess.run([
                python_cmd, "-c", 
                "import tkinter; tk=tkinter.Tk(); tk.withdraw(); tk.destroy(); print('OK')"
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0 and "OK" in result.stdout:
                return python_cmd
        except (FileNotFoundError, subprocess.TimeoutExpired, subprocess.CalledProcessError):
            continue
    
    return None

def install_python_tk():
    """Intenta instalar python-tk usando Homebrew"""
    print("🔧 Intentando instalar python-tk con Homebrew...")
    try:
        subprocess.run(["brew", "install", "python-tk"], check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def run_with_uv():
    """Ejecuta con UV"""
    project_root = Path(__file__).parent
    try:
        subprocess.run(["uv", "run", "python", "-m", "app_iiwa"], 
                        cwd=project_root, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error con UV: {e}")
        return False

def run_with_system_python(python_cmd):
    """Ejecuta con Python del sistema"""
    project_root = Path(__file__).parent
    
    print(f"🔧 Usando Python del sistema: {python_cmd}")
    
    # Instalar dependencias con pip
    print("📦 Instalando dependencias...")
    try:
        subprocess.run([
            python_cmd, "-m", "pip", "install", "pandas", "numpy", 
            "openpyxl", "xlsxwriter", "Pillow"
        ], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("⚠️  Error instalando dependencias, continuando...")
    
    # Ejecutar la aplicación
    env = os.environ.copy()
    env['PYTHONPATH'] = str(project_root / "src")
    
    try:
        subprocess.run([python_cmd, "-m", "app_iiwa"], 
                      cwd=project_root, env=env, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando con Python del sistema: {e}")
        return False

def main():
    """Función principal con detección automática de problemas"""
    print("🚀 Iniciando App IIWA...")
    
    project_root = Path(__file__).parent
    
    # 1. Verificar UV
    uv_available = False
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        uv_available = True
        print("✅ UV disponible")
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("⚠️  UV no disponible")
    
    # 2. Si UV está disponible, intentar primero
    if uv_available:
        print("🔄 Intentando con UV...")
        if run_with_uv():
            print("✅ Ejecutado exitosamente con UV")
            return
        else:
            print("⚠️  UV falló, intentando alternativas...")

    # 3. Buscar Python del sistema que funcione
    system_python = get_system_python()
    if system_python:
        print(f"✅ Python del sistema encontrado: {system_python}")
        if run_with_system_python(system_python):
            print("✅ Ejecutado exitosamente con Python del sistema")
            return

    # 4. Si nada funciona, mostrar ayuda
    print("\n❌ No se pudo ejecutar la aplicación")
    print("\n🛠️  SOLUCIONES POSIBLES:")
    print("1. Instalar Homebrew y python-tk:")
    print("   /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"")
    print("   brew install python-tk")
    print()
    print("2. O usar Python del sistema:")
    print("   /usr/bin/python3 -m pip install pandas numpy openpyxl xlsxwriter")
    print(f"   PYTHONPATH={project_root}/src /usr/bin/python3 -m app_iiwa")
    print()
    print("3. O instalar UV correctamente:")
    print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
    print("   uv python install 3.11  # Instalar Python con tkinter")
    print()
    
    sys.exit(1)

if __name__ == "__main__":
    main()