# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-10-07

### Added
- 🎉 Aplicación unificada que combina CAMPO y CAJA
- 📊 Proceso CAMPO para análisis de rezagos de agua
  - Generación de reportes por código postal
  - Consolidación de agua, drenaje, recargos, mejoras e IVA
  - Exportación de resúmenes en formato grid
  - Creación de reportes para macros
  - Libro detallado por códigos postales
- 💰 Proceso CAJA para análisis de pagos y evidencias
  - Cálculo de rezagos IIWA (2024-6 y anteriores)
  - Evidencias por fecha de pago
  - Reportes diarios y por código postal
  - Integración con geolocalización (REGISTROS y FOLIOS)
  - Consolidación final en Excel multi-hoja
- 🖥️ Interfaz gráfica unificada con Tkinter
  - Selección de proceso (CAMPO/CAJA)
  - Selectores de rutas de entrada y salida
  - Logs en tiempo real con timestamps
  - Barra de progreso indeterminada
  - Botones de acción (limpiar logs, abrir salida)
- 🔧 Características técnicas
  - Ejecución multi-threaded (UI no se bloquea)
  - Validación de archivos requeridos
  - Manejo robusto de errores
  - Compatibilidad multi-plataforma (Windows, macOS, Linux)
  - Detección automática de rutas del sistema
- 📦 Sistema de gestión con UV
  - Configuración con pyproject.toml
  - Scripts de entrada configurados
  - Dependencias optimizadas
- 🚀 Sistema de releases para GitHub
  - Workflows automatizados de CI/CD
  - Scripts de build y distribución
  - Documentación completa

### Technical Details
- **Python**: 3.8+ required
- **Dependencies**: pandas, numpy, openpyxl, xlsxwriter
- **GUI Framework**: Tkinter (included with Python)
- **Package Manager**: UV (recommended)
- **Build System**: Hatchling
- **Testing**: pytest with coverage
- **Code Quality**: black, isort, flake8, mypy

### Files Generated
#### CAMPO Process:
- `ReporteRezagoAgua.xlsx` - Main consolidated report
- `reporte_macro.xlsx` - Macro processing file
- `CodigosPostales.xlsx` - Detailed analysis by postal code
- `resumen_cps.xlsx` - Grid format summary

#### CAJA Process:
- `reporte_completo.xlsx` - Final consolidated report
- `evidencias_x_fecha.xlsx` - Evidence by payment date
- `pagos_diarios.xlsx` - Daily payment analysis
- `pagos_x_cp.xlsx` - Payments by postal code
- `E. folio Geolocalización.xlsx` - Data with geolocation
- `sin_folio.xlsx` - Records without notification folio

## [Unreleased]

### Planned
- [ ] Configuración avanzada de exportación
- [ ] Soporte para más formatos de entrada
- [ ] Plantillas personalizables de reportes
- [ ] Integración con bases de datos
- [ ] API REST para procesamiento automatizado
- [ ] Dashboard web opcional
- [ ] Notificaciones por email
- [ ] Programación de tareas automatizadas