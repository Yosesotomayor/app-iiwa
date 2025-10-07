#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Punto de entrada para ejecutar App IIWA como módulo
Uso: python -m app_iiwa
"""

try:
    from . import main
except ImportError:
    # Fallback para PyInstaller
    from app_iiwa import main

if __name__ == "__main__":
    main()
