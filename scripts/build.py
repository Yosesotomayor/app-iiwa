#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de build para App IIWA usando UV
Automatiza el proceso de construcción y empaquetado
"""

import subprocess
import sys
import shutil
from pathlib import Path
import json
import zipfile
import os


def run_command(cmd, cwd=None, check=True):
    """Ejecuta un comando y devuelve el resultado"""
    print(f"🔄 Ejecutando: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)
    if result.stdout:
        print(f"📝 Output: {result.stdout}")
    if result.stderr:
        print(f"⚠️ Stderr: {result.stderr}")
    return result


def check_uv_installed():
    """Verifica que UV esté instalado"""
    try:
        result = run_command(["uv", "--version"], check=False)
        if result.returncode == 0:
            print(f"✅ UV instalado: {result.stdout.strip()}")
            return True
        else:
            print("❌ UV no está instalado")
            print("📦 Instala UV desde: https://github.com/astral-sh/uv")
            return False
    except FileNotFoundError:
        print("❌ UV no encontrado en PATH")
        print("📦 Instala UV desde: https://github.com/astral-sh/uv")
        return False


def setup_environment(project_root):
    """Configura el entorno virtual con UV"""
    print("🔧 Configurando entorno virtual...")
    
    # Crear venv si no existe
    venv_path = project_root / ".venv"
    if not venv_path.exists():
        run_command(["uv", "venv"], cwd=project_root)
    
    # Instalar dependencias
    run_command(["uv", "sync"], cwd=project_root)
    
    # Instalar dependencias de desarrollo
    run_command(["uv", "sync", "--group", "dev"], cwd=project_root)
    
    print("✅ Entorno configurado")


def run_tests(project_root):
    """Ejecuta las pruebas"""
    print("🧪 Ejecutando pruebas...")
    
    try:
        # Crear tests básicos si no existen
        tests_dir = project_root / "tests"
        if not (tests_dir / "test_basic.py").exists():
            create_basic_tests(tests_dir)
        
        run_command(["uv", "run", "pytest"], cwd=project_root)
        print("✅ Pruebas pasaron")
        return True
    except subprocess.CalledProcessError:
        print("❌ Las pruebas fallaron")
        return False


def create_basic_tests(tests_dir):
    """Crea pruebas básicas"""
    tests_dir.mkdir(exist_ok=True)
    
    init_file = tests_dir / "__init__.py"
    init_file.write_text("")
    
    test_content = '''#!/usr/bin/env python3
"""Tests básicos para App IIWA"""

import pytest
import sys
from pathlib import Path

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def test_imports():
    """Test de importaciones básicas"""
    try:
        import app_iiwa
        assert hasattr(app_iiwa, "__version__")
        assert hasattr(app_iiwa, "main")
    except ImportError as e:
        pytest.fail(f"Error importando app_iiwa: {e}")

def test_version():
    """Test de versión"""
    import app_iiwa
    assert app_iiwa.__version__ == "1.0.0"

def test_main_function_exists():
    """Test de que la función main existe"""
    import app_iiwa
    assert callable(app_iiwa.main)
'''
    
    test_file = tests_dir / "test_basic.py"
    test_file.write_text(test_content)


def run_quality_checks(project_root):
    """Ejecuta verificaciones de calidad de código"""
    print("🔍 Ejecutando verificaciones de calidad...")
    
    checks_passed = True
    
    # Black (formateo)
    try:
        run_command(["uv", "run", "black", "--check", "src/"], cwd=project_root)
        print("✅ Black: código bien formateado")
    except subprocess.CalledProcessError:
        print("⚠️ Black: ejecutando auto-formateo...")
        run_command(["uv", "run", "black", "src/"], cwd=project_root, check=False)
    
    # isort (imports)
    try:
        run_command(["uv", "run", "isort", "--check", "src/"], cwd=project_root)
        print("✅ isort: imports organizados")
    except subprocess.CalledProcessError:
        print("⚠️ isort: organizando imports...")
        run_command(["uv", "run", "isort", "src/"], cwd=project_root, check=False)
    
    # flake8 (linting)
    try:
        run_command(["uv", "run", "flake8", "src/"], cwd=project_root)
        print("✅ flake8: sin problemas de linting")
    except subprocess.CalledProcessError:
        print("⚠️ flake8: encontrados problemas de estilo")
        checks_passed = False
    
    return checks_passed


def build_package(project_root):
    """Construye el paquete"""
    print("📦 Construyendo paquete...")
    
    # Limpiar build anterior
    for dir_name in ["build", "dist", "*.egg-info"]:
        for path in project_root.glob(dir_name):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    
    # Construir con UV
    run_command(["uv", "build"], cwd=project_root)
    
    print("✅ Paquete construido")


def create_release_bundle(project_root):
    """Crea un bundle para release"""
    print("📦 Creando bundle de release...")
    
    version = get_version(project_root)
    release_dir = project_root / "releases" / f"v{version}"
    release_dir.mkdir(parents=True, exist_ok=True)
    
    # Copiar archivos importantes
    important_files = [
        "README.md",
        "LICENSE", 
        "CHANGELOG.md",
        "pyproject.toml"
    ]
    
    for file in important_files:
        src_file = project_root / file
        if src_file.exists():
            shutil.copy2(src_file, release_dir / file)
    
    # Copiar código fuente
    src_dir = release_dir / "src"
    if src_dir.exists():
        shutil.rmtree(src_dir)
    shutil.copytree(project_root / "src", src_dir)
    
    # Copiar dist
    dist_src = project_root / "dist"
    if dist_src.exists():
        dist_dst = release_dir / "dist"
        if dist_dst.exists():
            shutil.rmtree(dist_dst)
        shutil.copytree(dist_src, dist_dst)
    
    # Crear ZIP del release
    zip_path = release_dir.parent / f"app-iiwa-v{version}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(release_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(release_dir)
                zipf.write(file_path, arc_path)
    
    print(f"✅ Bundle creado: {zip_path}")
    return zip_path


def get_version(project_root):
    """Obtiene la versión del proyecto"""
    init_file = project_root / "src" / "app_iiwa" / "__init__.py"
    content = init_file.read_text()
    for line in content.splitlines():
        if line.startswith("__version__"):
            return line.split('"')[1]
    return "1.0.0"


def create_run_script(project_root):
    """Crea un script de ejecución simple"""
    script_content = '''#!/usr/bin/env python3
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
        sys.exit(1)
    
    # Ejecutar la aplicación
    try:
        subprocess.run(["uv", "run", "python", "-m", "app_iiwa"], 
                      cwd=project_root, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    script_path = project_root / "run.py"
    script_path.write_text(script_content)
    script_path.chmod(0o755)
    print(f"✅ Script de ejecución creado: {script_path}")


def main():
    """Función principal del script de build"""
    print("🏗️ App IIWA - Script de Build con UV")
    print("=" * 50)
    
    project_root = Path(__file__).parent.parent
    
    # Verificar UV
    if not check_uv_installed():
        sys.exit(1)
    
    # Configurar entorno
    setup_environment(project_root)
    
    # Ejecutar pruebas
    if not run_tests(project_root):
        response = input("❓ Las pruebas fallaron. ¿Continuar? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Verificaciones de calidad
    if not run_quality_checks(project_root):
        response = input("❓ Hay problemas de calidad. ¿Continuar? (y/N): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Construir paquete
    build_package(project_root)
    
    # Crear script de ejecución
    create_run_script(project_root)
    
    # Crear bundle de release
    release_bundle = create_release_bundle(project_root)
    
    print("\n🎉 Build completado exitosamente!")
    print(f"📦 Bundle de release: {release_bundle}")
    print("\n📋 Próximos pasos:")
    print("1. Revisar el contenido del release")
    print("2. Hacer commit de los cambios")
    print("3. Crear tag de versión")
    print("4. Subir a GitHub")
    print("5. Crear release en GitHub con el bundle")


if __name__ == "__main__":
    main()