# App IIWA - Procesador Unificado de Padrones

[![CI/CD Pipeline](https://github.com/yosesotomayor/app-iiwa/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/yosesotomayor/app-iiwa/actions)
[![PyPI version](https://badge.fury.io/py/app-iiwa.svg)](https://badge.fury.io/py/app-iiwa)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Una aplicación unificada que combina las funcionalidades de **CAMPO** y **CAJA** en una sola interfaz gráfica intuitiva, desarrollada con gestión moderna de dependencias usando **UV**.

## Características

### Proceso CAMPO

- Procesamiento de datos de rezagos de agua
- Generación de reportes por código postal
- Análisis detallados por tipo de conexión y consumo
- Consolidación de agua, drenaje, recargos, mejoras e IVA
- Creación de reportes para macros
- Exportación a múltiples formatos Excel

### Proceso CAJA

- Análisis de pagos y evidencias
- Cálculo de rezagos IIWA (2024-6 y anteriores)
- Generación de evidencias por fecha de pago
- Reportes diarios y por código postal
- Integración con geolocalización (REGISTROS y FOLIOS)
- Consolidación de múltiples archivos en un reporte final

### Interfaz Unificada

- **Logs en Tiempo Real:** Muestra el progreso detallado con timestamps
- **Selección Flexible de Rutas:** Carpetas de entrada y salida personalizables
- **Validaciones Automáticas:** Verificación de archivos requeridos
- **Ejecución Multi-threaded:** UI responsiva que no se bloquea
- **Compatibilidad Multi-plataforma:** Windows, macOS, Linux

## 🚀 Instalación y Ejecución

### ✅ Método Recomendado: UV (Más Rápido)

1. **Instalar UV:**
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Reiniciar terminal después de la instalación
   ```

2. **Clonar y ejecutar:**
   ```bash
   git clone https://github.com/yosesotomayor/app-iiwa.git
   cd app-iiwa
   
   # Método más fácil: Script automático
   ./start.sh
   
   # O manualmente:
   uv run python -m app_iiwa
   python run.py
   ```

### 🔧 Método Alternativo: Python del Sistema

Si UV no funciona o prefieres usar Python tradicional:

```bash
git clone https://github.com/yosesotomayor/app-iiwa.git
cd app-iiwa

# Instalar dependencias
pip install pandas numpy openpyxl xlsxwriter

# Ejecutar
PYTHONPATH=src python -m app_iiwa

# O usar el script automático
python run.py
```

### 📦 Desde Release (Sin código)

1. Ve a [Releases](https://github.com/yosesotomayor/app-iiwa/releases)
2. Descarga `app-iiwa-v1.0.0.zip`
3. Extrae y ejecuta `run.py`

> **💡 Nota:** El script `run.py` detecta automáticamente la mejor forma de ejecutar la aplicación en tu sistema.
3. Extrae y ejecuta `run.py`

## Estructura del Proyecto

```
App_iiwa/
├── src/app_iiwa/           # Código fuente principal
│   ├── __init__.py         # Punto de entrada del paquete
│   └── app.py             # Aplicación principal
├── tests/                  # Pruebas automatizadas
├── scripts/               # Scripts de build y utilidades
│   └── build.py           # Script de construcción
├── .github/workflows/     # Workflows de CI/CD
│   └── ci.yml            # Pipeline automatizado
├── data/                  # Carpeta de datos de entrada
├── output/               # Carpeta de resultados
├── pyproject.toml        # Configuración del proyecto (UV/pip)
├── README.md            # Esta documentación
├── LICENSE              # Licencia MIT
├── CHANGELOG.md         # Registro de cambios
├── .gitignore          # Archivos ignorados por Git
└── run.py              # Script de ejecución simple
```

## Archivos Requeridos

### Para Proceso CAMPO:

- `data/SISTEMA.xlsx` - Archivo principal de datos
- `data/LISTA C.P..xlsx` - Lista de códigos postales

### Para Proceso CAJA:

- `data/SISTEMA.xlsx` - Archivo principal de datos
- `data/REGISTROS.csv` - Datos de registro (opcional)
- `data/FOLIOS.csv` - Información de folios (opcional)

## Uso de la Aplicación

1. **Seleccionar Proceso:**

   - Elige entre CAMPO o CAJA
2. **Configurar Rutas:**

   - Carpeta de datos: archivos de entrada
   - Carpeta de salida: resultados generados
   - Archivo SISTEMA.xlsx (para CAMPO)
3. **Ejecutar:**

   - Presiona "Iniciar Proceso"
   - Observa logs en tiempo real con timestamps
   - Los resultados se guardan automáticamente
4. **Explorar Resultados:**

   - Usa "Abrir Salida" para ver archivos generados
   - "Limpiar Log" para reset del registro

## Reportes Generados

### CAMPO:

- `ReporteRezagoAgua.xlsx` - Reporte principal consolidado
- `reporte_macro.xlsx` - Archivo para procesamiento por macros
- `CodigosPostales.xlsx` - Análisis detallado por CP
- `resumen_cps.xlsx` - Resumen en formato grid

### CAJA:

- `reporte_completo.xlsx` - Reporte consolidado final
- `evidencias_x_fecha.xlsx` - Evidencias por fecha de pago
- `pagos_diarios.xlsx` - Análisis de pagos diarios
- `pagos_x_cp.xlsx` - Pagos por código postal
- `E. folio Geolocalización.xlsx` - Datos con geolocalización
- `sin_folio.xlsx` - Registros sin folio de notificación

## 🔧 Desarrollo

### Configuración del Entorno de Desarrollo

```bash
# Clonar repositorio
git clone https://github.com/yosesotomayor/app-iiwa.git
cd app-iiwa

# Instalar con dependencias de desarrollo
uv sync --group dev

# Ejecutar pruebas
uv run pytest

# Verificaciones de calidad
uv run black src/ tests/     # Formateo
uv run isort src/ tests/     # Organizar imports
uv run flake8 src/ tests/    # Linting
uv run mypy src/            # Type checking
```

### Build y Release

```bash
# Build completo con verificaciones
python scripts/build.py

# Solo build del paquete
uv build

# Ejecutar pruebas
uv run pytest --cov=app_iiwa
```

## Crear un Release

### 1. Preparar Release

```bash
# 1. Actualizar versión en src/app_iiwa/__init__.py
# 2. Actualizar CHANGELOG.md
# 3. Commit cambios
git add .
git commit -m "Prepare release v1.0.0"
git push
```

### 2. Crear Tag y Release

```bash
# Crear tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 3. GitHub Release (Automático)

El workflow de GitHub Actions automáticamente:

- ✅ Ejecuta pruebas en múltiples plataformas
- ✅ Verifica calidad del código
- ✅ Construye el paquete
- ✅ Crea bundle de release
- ✅ Publica en PyPI (opcional)
- ✅ Adjunta artefactos al release

## 🐛 Solución de Problemas

### 💻 Problemas de Tkinter en macOS

Si ves errores como `Can't find a usable init.tcl` o `unknown option "-font"`:

```bash
# Solución 1: Usar el script automático
TK_SILENCE_DEPRECATION=1 python run.py

# Solución 2: Instalar python-tk con Homebrew
brew install python-tk

# Solución 3: Usar Python del sistema directamente
/usr/bin/python3 -m pip install pandas numpy openpyxl xlsxwriter
PYTHONPATH=src /usr/bin/python3 -m app_iiwa
```

### ⚙️ Error: "uv not found"
```bash
# Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh
# IMPORTANTE: Reiniciar terminal después de instalar
```

### 📄 Error: "No existe SISTEMA.xlsx"
- Verifica que el archivo esté en la carpeta de datos especificada
- El nombre debe ser exactamente "SISTEMA.xlsx" (case-sensitive)
- Asegúrate de que no sea un archivo de Excel oculto o temporal

### 📊 Error: "Columna faltante"
- **CAMPO** requiere: `agua`, `drenaje`, `mejoras`, `iva`, `Principal`, `Derivada`
- **CAJA** requiere: `fechapago`, `FolioImpreso`, `pagdCosto`, `conDescripcion`
- Abre el archivo Excel y verifica los nombres exactos de las columnas

### 📜 Logs aparecen en la GUI
- Los logs ahora aparecen directamente en la interfaz gráfica con timestamps
- Si no se actualizan, presiona "Limpiar Log" y vuelve a intentar
- En casos extremos, reinicia la aplicación

### 🚀 La aplicación no inicia
```bash
# Verifica Python
python3 --version  # Debe ser 3.9 o superior

# Verifica dependencias
python3 -c "import pandas, numpy, openpyxl, xlsxwriter, tkinter; print('Todo OK')"

# Usa el script de diagnóstico
python run.py  # Este detecta y sugiere soluciones
```

## CI/CD Pipeline

El proyecto incluye workflows automatizados de GitHub Actions:

**Testing:** Pruebas en Python 3.8-3.12 en Ubuntu, Windows, macOS

**Code Quality:** Black, isort, flake8, mypy

**Security:** Trivy vulnerability scanning

**Build:** Construcción automática de paquetes

**Release:** Deploy automático a PyPI en releases

**Coverage:** Reportes de cobertura con Codecov

## Requisitos del Sistema

- **Python:** 3.8 o superior
- **SO:** Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- **RAM:** Mínimo 4GB (recomendado 8GB para archivos grandes)
- **Espacio:** ~100MB para instalación + espacio para datos

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.📞 Soporte

- **Issues:** [GitHub Issues](https://github.com/yosesotomayor/app-iiwa/issues)
- **Discusiones:** [GitHub Discussions](https://github.com/yosesotomayor/app-iiwa/discussions)
- **Email:** iiwa@sistema.mx

## 🙏 Reconocimientos

Esta aplicación unifica y mejora las funcionalidades de los proyectos CAMPO y CAJA originales, proporcionando una experiencia de usuario moderna y robusta con logs en tiempo real.

---

**Versión:** 1.0.0  
**Autor:** Sistema IIWA  
**Fecha:** Octubre 2024  
**Gestión:** UV Package Manager  
**Estado:** ✅ Funcional y probado en macOS
