#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
App IIWA - Aplicación Unificada para Procesamiento de Padrones
Combina las funcionalidades de CAJA y CAMPO en una sola interfaz
"""

__version__ = "1.2.0"
__author__ = "Sistema IIWA"
__email__ = "iiwa@sistema.mx"
__license__ = "MIT"
__description__ = (
    "Aplicación Unificada para Procesamiento de Padrones - Combina CAMPO y CAJA"
)

from .app import AppIIWA


def main():
    """Punto de entrada principal de la aplicación"""
    app = AppIIWA()
    app.run()


if __name__ == "__main__":
    main()
