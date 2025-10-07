#!/usr/bin/env python3
"""
Tests básicos para App IIWA
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_import_app_iiwa():
    """Test que verifica que el módulo se puede importar correctamente"""
    try:
        import app_iiwa

        assert app_iiwa.__version__ == "2.0.0"
        assert hasattr(app_iiwa, "main")
        assert callable(app_iiwa.main)
    except ImportError as e:
        import pytest

        pytest.fail(f"No se pudo importar app_iiwa: {e}")


def test_app_iiwa_class_import():
    """Test que verifica que la clase principal se puede importar"""
    try:
        from app_iiwa.app import AppIIWA

        assert AppIIWA is not None
        # Verificar que tiene los métodos principales
        assert hasattr(AppIIWA, "run")
        assert hasattr(AppIIWA, "__init__")
    except ImportError as e:
        import pytest

        pytest.fail(f"No se pudo importar AppIIWA: {e}")


def test_version_info():
    """Test que verifica la información de versión"""
    try:
        import app_iiwa

        assert hasattr(app_iiwa, "__version__")
        assert hasattr(app_iiwa, "__author__")
        assert hasattr(app_iiwa, "__description__")
        assert app_iiwa.__author__ == "Sistema IIWA"
    except ImportError:
        import pytest

        pytest.skip("No se pudo importar app_iiwa para verificar versión")


if __name__ == "__main__":
    import pytest

    pytest.main([__file__])
