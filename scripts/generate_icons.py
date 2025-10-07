#!/usr/bin/env python3
"""
Script para generar iconos para PyInstaller desde principal.jpeg
"""

import os
import sys
from pathlib import Path
from PIL import Image

def create_icons():
    """Crea iconos .ico y .icns desde principal.jpeg"""
    
    project_root = Path(__file__).parent.parent
    icon_source = project_root / "principal.jpeg"
    
    if not icon_source.exists():
        print(f"❌ No se encontró principal.jpeg en {icon_source}")
        return False
    
    print(f"📁 Usando icono fuente: {icon_source}")
    
    try:
        # Cargar imagen original
        img = Image.open(icon_source)
        print(f"📐 Imagen original: {img.size}")
        
        # Crear versión square (usar el mínimo de width/height)
        min_size = min(img.size)
        
        # Recortar al centro para hacer cuadrado
        left = (img.width - min_size) // 2
        top = (img.height - min_size) // 2
        right = left + min_size
        bottom = top + min_size
        
        img_square = img.crop((left, top, right, bottom))
        print(f"✂️ Imagen recortada: {img_square.size}")
        
        # Generar icono .ico para Windows (múltiples tamaños)
        ico_path = project_root / "icon.ico"
        sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
        
        ico_images = []
        for size in sizes:
            resized = img_square.resize(size, Image.Resampling.LANCZOS)
            ico_images.append(resized)
        
        ico_images[0].save(
            ico_path, 
            format='ICO', 
            sizes=[img.size for img in ico_images],
            append_images=ico_images[1:]
        )
        print(f"✅ Creado icon.ico: {ico_path}")
        
        # Para macOS, crear un .png de alta calidad (PyInstaller lo convertirá)
        png_path = project_root / "icon.png"
        img_1024 = img_square.resize((1024, 1024), Image.Resampling.LANCZOS)
        img_1024.save(png_path, format='PNG', optimize=True)
        print(f"✅ Creado icon.png: {png_path}")
        
        print("🎉 Iconos generados exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error generando iconos: {e}")
        return False

if __name__ == "__main__":
    success = create_icons()
    sys.exit(0 if success else 1)