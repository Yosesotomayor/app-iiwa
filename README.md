# App IIWA - Sistema de Procesamiento de Padrones

## Desarrollado por INFORA CONSULTORIAS

**App IIWA** es un sistema profesional desarrollado por **INFORA CONSULTORIAS** para el procesamiento automatizado de padrones de agua. La aplicación integra las funcionalidades de **CAMPO** (análisis de rezagos) y **CAJA** (análisis de pagos) en una sola herramienta.

### Funcionalidades Principales
- **Módulo CAMPO**: Procesamiento de rezagos de agua por código postal
- **Módulo CAJA**: Análisis de pagos y evidencias con geolocalización
- **Interfaz unificada**: Una aplicación para ambos procesos
- **Generación automática**: Reportes en formato Excel listos para uso

---

## INSTALACIÓN Y USO

### Opción 1: Ejecutables (Recomendado para usuarios finales)

**Esta es la opción más fácil si no tienes conocimientos técnicos.**

#### Para Windows:
1. Ir a la página de descargas: https://github.com/Yosesotomayor/app-iiwa/releases
2. Descargar el archivo `App-IIWA-v1.2.0-Windows-x64.zip`
3. Extraer el archivo ZIP en una carpeta
4. Hacer doble clic en `App-IIWA.exe`
5. La aplicación se abre automáticamente

#### Para macOS (Intel):
1. Ir a la página de descargas: https://github.com/Yosesotomayor/app-iiwa/releases
2. Descargar el archivo `App-IIWA-v1.2.0-macOS-Intel.zip`
3. Extraer el archivo ZIP
4. Hacer doble clic en `App-IIWA.app`
5. Si aparece una advertencia de seguridad, ir a Preferencias del Sistema > Seguridad y permitir la aplicación

#### Para macOS (Silicon/M1/M2):
1. Ir a la página de descargas: https://github.com/Yosesotomayor/app-iiwa/releases
2. Descargar el archivo `App-IIWA-v1.2.0-macOS-Silicon.zip`
3. Extraer el archivo ZIP
4. Hacer doble clic en `App-IIWA.app`
5. Si aparece una advertencia de seguridad, ir a Preferencias del Sistema > Seguridad y permitir la aplicación

### Opción 2: Instalación para desarrolladores

**Solo para usuarios con conocimientos técnicos de Python:**

```bash
pip install git+https://github.com/Yosesotomayor/app-iiwa.git@v1.2.0
app-iiwa
```

---

## CÓMO USAR LA APLICACIÓN

### 1. Preparar los archivos

#### Para proceso CAMPO:
Crear una carpeta con los siguientes archivos:
- `SISTEMA.xlsx` - Archivo principal con datos de cuentas
- `LISTA C.P..xlsx` - Lista de códigos postales

#### Para proceso CAJA:
Crear una carpeta con los siguientes archivos:
- `SISTEMA.xlsx` - Archivo principal con datos de pagos
- `REGISTROS.csv` - Datos de geolocalización
- `FOLIOS.csv` - Información de folios de notificación

### 2. Ejecutar la aplicación

1. **Abrir App IIWA** (según las instrucciones de instalación arriba)

2. **Seleccionar tipo de proceso**:
   - Marcar "CAMPO" para análisis de rezagos
   - Marcar "CAJA" para análisis de pagos

3. **Configurar rutas**:
   - **Carpeta de datos**: Seleccionar la carpeta donde están los archivos de entrada
   - **Carpeta de salida**: Seleccionar donde se guardarán los reportes
   - **Archivo SISTEMA**: Seleccionar el archivo SISTEMA.xlsx específico

4. **Opcional**: Escribir una etiqueta personalizada para las hojas del reporte

5. **Iniciar proceso**: Hacer clic en "Iniciar Proceso"

6. **Monitorear progreso**: La aplicación mostrará el progreso en tiempo real

7. **Revisar resultados**: Al finalizar, los reportes estarán en la carpeta de salida seleccionada

### 3. Archivos de salida

#### Proceso CAMPO genera:
- `ReporteRezagoAgua.xlsx` - Reporte principal con múltiples hojas
- `reporte_macro.xlsx` - Datos organizados por código postal
- `CodigosPostales.xlsx` - Análisis detallado por CP
- `resumen_cps.xlsx` - Resumen visual en formato grid

#### Proceso CAJA genera:
- `REPORTE_COMPLETO.xlsx` - Consolidado de todos los análisis
- `evidencias_x_fecha.xlsx` - Evidencias organizadas por fecha de pago
- `pagos_diarios.xlsx` - Análisis de pagos por día
- `pagos_x_cp.xlsx` - Pagos agrupados por código postal
- `E. folio Geolocalización.xlsx` - Datos con coordenadas geográficas

---

## REQUISITOS DEL SISTEMA

### Para Ejecutables (Sin instalación técnica):
- **Windows**: Windows 10 o superior (64 bits)
- **macOS**: macOS 10.15 o superior
- **RAM**: Mínimo 4GB
- **Espacio**: 100MB para la aplicación + espacio para datos
- **Sin requisitos adicionales**: No necesita Python ni programas extra

### Para Instalación Técnica:
- Python 3.9 o superior
- Sistema operativo: Windows, macOS, o Linux
- RAM: Mínimo 4GB (recomendado 8GB para archivos grandes)
- Espacio en disco: 500MB + espacio para datos

---

## SOPORTE TÉCNICO

### Desarrollado por INFORA CONSULTORIAS

Para soporte técnico y consultas:
- **Repositorio**: https://github.com/Yosesotomayor/app-iiwa
- **Descargas**: https://github.com/Yosesotomayor/app-iiwa/releases
- **Reportar problemas**: https://github.com/Yosesotomayor/app-iiwa/issues

### Solución de Problemas Comunes

#### La aplicación no inicia en macOS:
- Ir a Preferencias del Sistema > Seguridad y Privacidad
- Hacer clic en "Permitir de todos modos" junto al mensaje de App-IIWA

#### Error de archivo no encontrado:
- Verificar que los archivos requeridos estén en la carpeta correcta
- Comprobar que los nombres de archivo coincidan exactamente (incluyendo mayúsculas)

#### La aplicación se cierra inesperadamente:
- Verificar que los archivos Excel no estén dañados
- Asegurar que hay suficiente espacio en disco
- Comprobar que no hay otros programas usando los archivos Excel

---

## INFORMACIÓN TÉCNICA

### Versión: 1.2.5
### Fecha de release: Octubre 2024
### Compatibilidad: Windows 10+, macOS 10.15+

### Changelog v1.2.5:
- Ejecutables nativos para Windows y macOS
- Interfaz optimizada y más estable
- Detección automática de arquitectura (Intel/Silicon)
- Mejoras en el procesamiento de archivos grandes
- Corrección de errores menores

### Tecnologías utilizadas:
- Interfaz gráfica: Tkinter
- Procesamiento de datos: pandas, numpy
- Generación de Excel: openpyxl, xlsxwriter
- Empaquetado: PyInstaller

---

**© 2025 INFORA CONSULTORIAS. Todos los derechos reservados.**
