#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Splash screen para App IIWA
Muestra pantalla de carga mientras la aplicación principal se inicializa
"""

import tkinter as tk
from tkinter import ttk
from pathlib import Path
import threading
import time

class SplashScreen:
    def __init__(self):
        self.splash = tk.Tk()
        self.splash.title("App IIWA")
        
        # Configurar ventana splash
        self.splash.geometry("400x300")
        self.splash.resizable(False, False)
        self.splash.configure(bg="#1a1a1a")
        
        # Centrar en pantalla
        self.splash.eval('tk::PlaceWindow . center')
        
        # Sin bordes
        self.splash.overrideredirect(True)
        
        # Crear contenido
        self.create_content()
        
    def create_content(self):
        """Crea el contenido del splash screen"""
        
        # Frame principal
        main_frame = tk.Frame(self.splash, bg="#1a1a1a")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Logo/Título
        title_frame = tk.Frame(main_frame, bg="#1a1a1a")
        title_frame.pack(expand=True, fill="x")
        
        # Título principal
        title_label = tk.Label(
            title_frame,
            text="App IIWA",
            font=("Arial", 24, "bold"),
            fg="#ffffff",
            bg="#1a1a1a"
        )
        title_label.pack(pady=(20, 5))
        
        # Subtítulo
        subtitle_label = tk.Label(
            title_frame,
            text="Sistema de Procesamiento de Padrones",
            font=("Arial", 12),
            fg="#cccccc",
            bg="#1a1a1a"
        )
        subtitle_label.pack(pady=(0, 5))
        
        # Empresa
        company_label = tk.Label(
            title_frame,
            text="INFORA CONSULTORIAS",
            font=("Arial", 10, "bold"),
            fg="#888888",
            bg="#1a1a1a"
        )
        company_label.pack(pady=(0, 20))
        
        # Barra de progreso
        progress_frame = tk.Frame(main_frame, bg="#1a1a1a")
        progress_frame.pack(fill="x", pady=(0, 20))
        
        self.progress = ttk.Progressbar(
            progress_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=10)
        
        # Texto de estado
        self.status_label = tk.Label(
            progress_frame,
            text="Iniciando aplicación...",
            font=("Arial", 10),
            fg="#cccccc",
            bg="#1a1a1a"
        )
        self.status_label.pack()
        
        # Versión
        version_label = tk.Label(
            main_frame,
            text="Versión 2.0.0",
            font=("Arial", 8),
            fg="#666666",
            bg="#1a1a1a"
        )
        version_label.pack(side="bottom")
        
    def show(self):
        """Muestra el splash screen"""
        self.splash.deiconify()
        self.progress.start()
        
    def update_status(self, text):
        """Actualiza el texto de estado"""
        self.status_label.configure(text=text)
        self.splash.update()
        
    def hide(self):
        """Oculta el splash screen"""
        self.progress.stop()
        self.splash.withdraw()
        
    def destroy(self):
        """Destruye el splash screen"""
        self.progress.stop()
        self.splash.destroy()
        
def show_splash_screen(duration=3):
    """
    Muestra splash screen por una duración específica
    
    Args:
        duration: Tiempo en segundos para mostrar el splash
    """
    splash = SplashScreen()
    
    def hide_after_delay():
        time.sleep(duration)
        splash.destroy()
    
    # Mostrar splash
    splash.show()
    
    # Programar cierre
    threading.Thread(target=hide_after_delay, daemon=True).start()
    
    # Mantener splash visible
    splash.splash.mainloop()
    
    return splash

if __name__ == "__main__":
    show_splash_screen(5)