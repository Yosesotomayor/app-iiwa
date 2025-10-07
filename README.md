# 🔄💧📊 App IIWA - Procesador Unificado de Padrones

<div align="center">
  <img src="principal.jpeg" alt="App IIWA Logo" width="128" height="128">
  
  **Aplicación Unificada para el Procesamiento Automatizado de Padrones de Agua**
  
  Combina las funcionalidades de **CAMPO** y **CAJA** en una sola interfaz gráfica moderna y elegante.
  
  [![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![UV](https://img.shields.io/badge/uv-ready-orange)](https://github.com/astral-sh/uv)
  [![macOS](https://img.shields.io/badge/macOS-supported-success)]()
  [![Windows](https://img.shields.io/badge/Windows-supported-success)]()
  [![Linux](https://img.shields.io/badge/Linux-supported-success)]()
</div>

## ✨ Características Principales

- **🎯 Interfaz Unificada**: Una sola aplicación con tema oscuro elegante
- **🖼️ Logo Profesional**: Icono personalizado optimizado para pantallas Retina
- **📊 Procesamiento CAMPO**: Análisis de rezagos de agua y reportes por código postal
- **💰 Procesamiento CAJA**: Análisis de pagos, evidencias y geolocalización
- **📱 GUI Moderna**: Interfaz gráfica intuitiva con logs en tiempo real y colores elegantes
- **🔄 Multiplataforma**: Compatible con Windows, macOS y Linux
- **⚡ Rápido**: Procesamiento optimizado con UV y gestión moderna de dependencias
- **📈 Reportes Detallados**: Exportación automática a Excel con múltiples hojas
- **🎨 Tema Oscuro**: Diseño moderno que complementa el logo corporativo

## 🚀 Instalación y Ejecución

### Método Recomendado (UV)
```bash
# Instalar UV si no lo tienes
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clonar el repositorio
git clone https://github.com/yosesotomayor/app-iiwa.git
cd app-iiwa

# Ejecutar directamente (UV manejará todo automáticamente)
python run.py
```

### Método Alternativo (pip)
```bash
git clone https://github.com/yosesotomayor/app-iiwa.git
cd app-iiwa
pip install -e .
python -m app_iiwa
```

### Script de Inicio Rápido
```bash
# Usar el script que detecta la mejor forma de ejecutar
./start.sh
```

## 📋 Guía de Uso Completa

### 🌊 Proceso CAMPO - Rezagos de Agua

**Archivos de entrada requeridos:**
- 📁 `data/SISTEMA.xlsx`: Datos principales del sistema de agua
- 📁 `data/LISTA C.P..xlsx`: Lista maestra de códigos postales

**Reportes generados:**
- 📊 `ReporteRezagoAgua.xlsx`: Reporte principal con análisis completo
- 🗂️ `CodigosPostales.xlsx`: Desglose detallado por código postal
- ⚙️ `reporte_macro.xlsx`: Datos optimizados para procesamiento con macros
- 📈 `resumen_cps.xlsx`: Resumen ejecutivo en formato grid

### 💰 Proceso CAJA - Análisis de Pagos

**Archivos de entrada requeridos:**
- 📁 `data/SISTEMA.xlsx`: Base de datos de pagos
- 📁 `data/REGISTROS.csv`: Registros de geolocalización (opcional)
- 📁 `data/FOLIOS.csv`: Datos de folios IIWA (opcional)

**Reportes generados:**
- 📋 `reporte_completo.xlsx`: Consolidado general con todas las hojas
- 📅 `evidencias_x_fecha.xlsx`: Evidencias organizadas por fecha de pago
- 📊 `pagos_diarios.xlsx`: Análisis diario de recaudación
- 🏘️ `pagos_x_cp.xlsx`: Análisis por código postal
- 🗺️ `E. folio Geolocalización.xlsx`: Datos con coordenadas GPS

## 🛠️ Desarrollo y Contribución

### Configurar Entorno de Desarrollo
```bash
# Clonar y configurar
git clone https://github.com/yosesotomayor/app-iiwa.git
cd app-iiwa

# Instalar dependencias de desarrollo
uv pip install -e ".[dev]"

# Ejecutar suite completa de pruebas
pytest --cov=app_iiwa --cov-report=html

# Formatear código
black src/ tests/
isort src/ tests/

# Verificación de calidad
flake8 src/ tests/
mypy src/
```

### Arquitectura del Proyecto
```
app-iiwa/
├── 🖼️ principal.jpeg          # Logo corporativo
├── 📁 src/app_iiwa/           # Código fuente principal
│   ├── __init__.py            # Metadata y versión
│   ├── __main__.py            # Punto de entrada como módulo
│   └── app.py                 # Aplicación principal con GUI
├── 🧪 tests/                  # Suite de pruebas
├── 📜 scripts/                # Herramientas de desarrollo
│   └── build.py               # Script de construcción
├── ⚙️ .github/workflows/      # Pipelines CI/CD
├── 🔧 pyproject.toml          # Configuración moderna del proyecto
├── 🚀 run.py                  # Launcher inteligente
├── 📋 start.sh                # Script de inicio para Unix
└── 📖 README.md               # Esta documentación
```

## 🔧 Solución de Problemas Frecuentes

### ❗ Error de tkinter en macOS
```bash
# Solución automática: el run.py detecta y usa Python del sistema
python run.py

# O instalar Python con soporte tkinter:
brew install python-tk
```

### 📦 Problemas con dependencias
```bash
# Limpiar caché completamente
uv cache clean
rm -rf .venv/

# Reinstalar desde cero
python run.py
```

### 🎨 Problemas de visualización
- La app detecta automáticamente las mejores fuentes disponibles
- El tema oscuro se adapta automáticamente al sistema
- Los iconos se optimizan para pantallas Retina en macOS

## 🏗️ Construcción y Release

### Construcción Local
```bash
# Usar el script automatizado
python scripts/build.py

# O manualmente
uv build
```

### Release Automático con GitHub Actions
1. Actualizar versión en `src/app_iiwa/__init__.py`
2. Actualizar `CHANGELOG.md` con cambios
3. Crear y push del tag:
   ```bash
   git add .
   git commit -m "Release v1.1.0: Improved UI and logo integration"
   git tag v1.1.0
   git push origin main --tags
   ```
4. GitHub Actions automáticamente:
   - ✅ Ejecuta todos los tests
   - 🏗️ Construye los paquetes
   - 📋 Crea el release con changelog
   - 📤 Sube los artefactos

## 🎨 Personalización

### Cambiar Logo
1. Reemplazar `principal.jpeg` con tu imagen (recomendado: 512x512px o mayor)
2. La app automáticamente la recorta y optimiza para diferentes tamaños

### Colores del Tema
Editar en `src/app_iiwa/app.py`:
- Fondo principal: `#1a1a1a`
- Área de logs: `#0d1117`
- Texto principal: `#e6edf3`
- Colores de estado personalizables

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas!

1. 🍴 Fork el proyecto
2. 🌿 Crea una rama (`git checkout -b feature/amazing-feature`)
3. ✅ Asegúrate de que los tests pasan (`pytest`)
4. 📝 Commit con mensaje descriptivo
5. 📤 Push y crea Pull Request

## 📊 Estadísticas del Proyecto

- **Lenguaje**: Python 3.9+
- **GUI**: Tkinter con tema personalizado
- **Gestión de Dependencias**: UV (moderno y rápido)
- **Procesamiento de Datos**: Pandas + NumPy
- **Exportación**: OpenPyXL + XlsxWriter
- **Imágenes**: Pillow para manejo de logo
- **Tests**: Pytest con cobertura
- **CI/CD**: GitHub Actions
- **Licencia**: MIT

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles completos.

## 🆘 Soporte y Comunidad

- 📖 **Documentación**: [GitHub Wiki](https://github.com/yosesotomayor/app-iiwa/wiki)
- 🐛 **Reportar Bugs**: [GitHub Issues](https://github.com/yosesotomayor/app-iiwa/issues)
- 💬 **Discusiones**: [GitHub Discussions](https://github.com/yosesotomayor/app-iiwa/discussions)
- 🚀 **Nuevas Features**: Crear issue con etiqueta `enhancement`

---

<div align="center">
  <strong>Hecho con ❤️ para el Sistema IIWA</strong>
  <br>
  <sub>Procesamiento inteligente de padrones de agua</sub>
</div>