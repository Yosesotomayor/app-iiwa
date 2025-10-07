#!/usr/bin/env python3
"""
Script para crear ejecutables de App IIWA usando PyInstaller
Genera ejecutables para Windows y macOS
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
import tempfile
import zipfile

def get_version():
    """Obtiene la versión actual del paquete"""
    try:
        # Leer desde __init__.py
        init_file = Path(__file__).parent.parent / "src" / "app_iiwa" / "__init__.py"
        with open(init_file, 'r') as f:
            for line in f:
                if line.startswith('__version__'):
                    return line.split('"')[1]
    except Exception:
        pass
    return "1.2.0"

def clean_build_dirs():
    """Limpia directorios de build anteriores"""
    dirs_to_clean = ['build', 'dist_exe']
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"[CLEAN] Limpiado directorio: {dir_name}")

def create_spec_file():
    """Crea el archivo .spec para PyInstaller"""
    
    # Obtener rutas absolutas
    project_root = Path(__file__).parent.parent.absolute()
    src_path = project_root / "src"
    icon_path = project_root / "principal.jpeg"
    
    spec_content = f'''# -*- coding: utf-8 -*-
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Configuración de rutas
project_root = Path(r"{project_root}")
src_path = project_root / "src"

block_cipher = None

a = Analysis(
    [str(src_path / "app_iiwa" / "__main__.py")],
    pathex=[str(src_path)],
    binaries=[],
    datas=[
        # Incluir archivos de datos si los hay
    ],
    hiddenimports=[
        'app_iiwa',
        'app_iiwa.app',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'pandas',
        'numpy',
        'openpyxl',
        'xlsxwriter',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'datetime',
        'pathlib',
        'threading',
        'queue',
        'platform',
        'subprocess',
        'tempfile',
        'warnings',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'jupyter',
        'notebook',
        'IPython',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='App-IIWA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon=str(project_root / "principal.jpeg") if (project_root / "principal.jpeg").exists() else None,
)

# Para macOS, crear también un bundle .app
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='App-IIWA.app',
        icon=None,
        bundle_identifier='mx.sistema.iiwa.app',
        info_plist={{
            'CFBundleDisplayName': 'App IIWA',
            'CFBundleGetInfoString': 'Aplicacion Unificada para Procesamiento de Padrones',
            'CFBundleIdentifier': 'mx.sistema.iiwa.app',
            'CFBundleVersion': '{get_version()}',
            'CFBundleShortVersionString': '{get_version()}',
            'LSMinimumSystemVersion': '10.15.0',
        }},
    )
'''
    
    spec_file = Path("app_iiwa.spec")
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"[OK] Archivo .spec creado: {spec_file}")
    return spec_file

def build_executable():
    """Construye el ejecutable usando PyInstaller"""
    
    print(f"[BUILD] Construyendo ejecutable para {platform.system()}...")
    
    # Crear archivo spec
    spec_file = create_spec_file()
    
    try:
        # Comando PyInstaller
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--distpath', 'dist_exe',
            str(spec_file)
        ]
        
        print(f"[EXEC] Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("[OK] Ejecutable construido exitosamente!")
        print("[INFO] Archivos generados:")
        
        dist_path = Path("dist_exe")
        if dist_path.exists():
            for item in dist_path.iterdir():
                print(f"  - {item}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error construyendo ejecutable:")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False
    
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        return False

def create_release_bundle():
    """Crea un bundle para el release"""
    
    version = get_version()
    system = platform.system().lower()
    
    if system == 'darwin':
        # Detectar arquitectura de macOS
        arch = platform.machine().lower()
        if arch == 'arm64':
            platform_name = "macOS-Silicon"
        else:
            platform_name = "macOS-Intel"
        
        # En macOS, comprimir la app
        app_path = Path("dist_exe/App-IIWA.app")
        if app_path.exists():
            bundle_name = f"App-IIWA-v{version}-{platform_name}.zip"
            
            with zipfile.ZipFile(bundle_name, 'w', zipfile.ZIP_DEFLATED) as zf:
                for root, dirs, files in os.walk(app_path):
                    for file in files:
                        file_path = Path(root) / file
                        arc_name = file_path.relative_to(app_path.parent)
                        zf.write(file_path, arc_name)
            
            print(f"INFO: Bundle creado: {bundle_name}")
            return bundle_name
    
    elif system == 'windows':
        # En Windows, comprimir el exe y dependencias
        exe_path = Path("dist_exe/App-IIWA.exe")
        if exe_path.exists():
            bundle_name = f"App-IIWA-v{version}-Windows-x64.zip"
            
            with zipfile.ZipFile(bundle_name, 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.write(exe_path, exe_path.name)
                
            print(f"INFO: Bundle creado: {bundle_name}")
            return bundle_name
    
    return None

def main():
    """Función principal"""
    print("INICIO: Construcción de ejecutables App IIWA")
    print(f"SISTEMA: {platform.system()} {platform.machine()}")
    print(f"VERSION: {get_version()}")
    
    # Cambiar al directorio del proyecto
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    print(f"DIRECTORIO: {project_root}")
    
    # Limpiar directorios anteriores
    clean_build_dirs()
    
    # Verificar que PyInstaller está disponible
    print("VERIFICACION: PyInstaller...")
    try:
        import PyInstaller
        print(f"OK: PyInstaller {PyInstaller.__version__} disponible")
    except ImportError:
        print("ERROR: PyInstaller no está disponible. Instálalo con: uv sync --extra build")
        return 1
    
    # Construir ejecutable
    success = build_executable()
    if not success:
        return 1
    
    # Crear bundle para release
    bundle = create_release_bundle()
    if bundle:
        print(f"LISTO: Bundle para release: {bundle}")
    
    print("COMPLETADO: Construcción finalizada exitosamente")
    return 0

if __name__ == "__main__":
    sys.exit(main())