# App IIWA - Procesador Unificado de Padrones

[![CI/CD Pipeline](https://github.com/usuario/app-iiwa/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/usuario/app-iiwa/actions)
[![PyPI version](https://badge.fury.io/py/app-iiwa.svg)](https://badge.fury.io/py/app-iiwa)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
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

## Instalación

### Opción 1: Con UV (Recomendado)

1. **Instalar UV** (gestor de dependencias moderno):

   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

   # O con pip
   pip install uv
   ```
2. **Clonar y configurar el proyecto:**

   ```bash
   git clone https://github.com/usuario/app-iiwa.git
   cd app-iiwa
   uv sync
   ```
3. **Ejecutar la aplicación:**

   ```bash
   uv run app-iiwa
   # O alternativamente:
   python run.py
   ```

### Opción 2: Desde PyPI

```bash
# Instalar desde PyPI
uv add app-iiwa

# O con pip tradicional
pip install app-iiwa

# Ejecutar
app-iiwa
```

### Opción 3: Release Binario

1. Ve a [Releases](https://github.com/usuario/app-iiwa/releases)
2. Descarga `app-iiwa-v1.0.0.zip`
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
git clone https://github.com/usuario/app-iiwa.git
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

## Solución de Problemas

### Error: "uv not found"

```bash
# Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh
# Reiniciar terminal
```

### Error: "No existe SISTEMA.xlsx"

- Verifica que el archivo esté en la carpeta de datos especificada
- El nombre debe ser exactamente "SISTEMA.xlsx"

### Error: "Columna faltante"

- Revisa que SISTEMA.xlsx tenga las columnas requeridas:
  - CAMPO: agua, drenaje, mejoras, iva, etc.
  - CAJA: fechapago, FolioImpreso, pagdCosto, etc.

### Logs no se actualizan

- Los logs se actualizan cada 80ms automáticamente
- Si se cuelga, reinicia la aplicación

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

- **Issues:** [GitHub Issues](https://github.com/usuario/app-iiwa/issues)
- **Discusiones:** [GitHub Discussions](https://github.com/usuario/app-iiwa/discussions)
- **Email:** infora@gmail.com

---

**Versión:** 1.0.0
**Autor:** Sistema IIWA
**Fecha:** Octubre 2025
**Gestión:** UV Package Manager
