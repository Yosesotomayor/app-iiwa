#!/usr/bin/env python3
# Script para crear un icono simple para App IIWA

import tkinter as tk
from pathlib import Path

def create_icon():
    """Crea un icono simple usando Tkinter Canvas"""
    
    # Crear ventana temporal
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana
    
    # Crear canvas
    size = 64
    canvas = tk.Canvas(root, width=size, height=size, bg='white')
    
    # Dibujar icono simple
    # Fondo circular azul
    margin = 4
    canvas.create_oval(margin, margin, size-margin, size-margin, 
                      fill='#2196F3', outline='#1976D2', width=2)
    
    # Texto "IIWA"
    canvas.create_text(size//2, size//2-2, text="IIWA", 
                      font=('Arial', 10, 'bold'), fill='white')
    
    # Pequeños elementos decorativos
    canvas.create_rectangle(size//2-8, size//2+8, size//2+8, size//2+10, 
                           fill='white', outline='')
    
    try:
        # Guardar como PostScript y luego convertir
        ps_file = Path(__file__).parent / 'assets' / 'icon.ps'
        canvas.postscript(file=str(ps_file))
        print(f"✅ Icono base creado en: {ps_file}")
        
        # Crear un icono de texto alternativo
        icon_text = """
🔄 IIWA
        """.strip()
        
        text_icon_file = Path(__file__).parent / 'assets' / 'icon.txt'
        text_icon_file.write_text(icon_text)
        print(f"✅ Icono de texto creado en: {text_icon_file}")
        
    except Exception as e:
        print(f"⚠️  No se pudo guardar el icono: {e}")
    
    root.destroy()

if __name__ == "__main__":
    create_icon()