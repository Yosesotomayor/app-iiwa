# 🚀 Guía de Release - App IIWA

Esta guía te ayudará a crear releases de manera consistente y automatizada.

## 📋 Pre-requisitos

- [x] UV instalado (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [x] Git configurado con permisos al repositorio
- [x] Acceso al repositorio en GitHub
- [x] Tokens configurados (opcional para PyPI)

## 🔄 Flujo de Release

### 1. Preparar el Release

```bash
# 1. Cambiar a rama main
git checkout main
git pull origin main

# 2. Crear rama de release
git checkout -b release/v1.0.0

# 3. Actualizar versión en src/app_iiwa/__init__.py
# Cambiar: __version__ = "1.0.0"

# 4. Actualizar CHANGELOG.md
# Agregar nuevas características, fixes, etc.

# 5. Ejecutar build y tests
python scripts/build.py

# 6. Commit cambios
git add .
git commit -m "Prepare release v1.0.0"
```

### 2. Merge y Tag

```bash
# 1. Merge a main
git checkout main
git merge release/v1.0.0
git push origin main

# 2. Crear tag
git tag -a v1.0.0 -m "Release v1.0.0 - Aplicación Unificada CAMPO/CAJA"
git push origin v1.0.0

# 3. Limpiar rama de release
git branch -d release/v1.0.0
```

### 3. GitHub Release (Automático)

Una vez que el tag es pusheado, GitHub Actions automáticamente:

1. **🧪 Testing:** Ejecuta pruebas en todas las plataformas
2. **🔍 Quality:** Verifica código con black, isort, flake8
3. **🔐 Security:** Scanner de vulnerabilidades  
4. **📦 Build:** Construye paquetes wheel y sdist
5. **📋 Bundle:** Crea ZIP con todo necesario para release
6. **🏷️ Release:** Crea release en GitHub con artefactos
7. **📤 PyPI:** Publica en PyPI (si está configurado)

### 4. Verificar Release

```bash
# 1. Verificar que el release existe en GitHub
# Ir a: https://github.com/usuario/app-iiwa/releases

# 2. Verificar artefactos
# - app-iiwa-v1.0.0.zip (bundle completo)
# - Wheel y source distribution

# 3. Test de instalación
uv add app-iiwa==1.0.0
app-iiwa --version
```

## 📁 Contenido del Release

Cada release incluye:

### Artefactos Automáticos:
- **Source Code (zip):** Código fuente en ZIP
- **Source Code (tar.gz):** Código fuente en tar.gz
- **Release Bundle:** `app-iiwa-v1.0.0.zip`

### Bundle Contents:
```
app-iiwa-v1.0.0/
├── src/app_iiwa/          # Código fuente
├── dist/                  # Paquetes wheel/sdist
├── README.md             # Documentación
├── LICENSE               # Licencia MIT
├── CHANGELOG.md          # Cambios de la versión
├── pyproject.toml        # Configuración del proyecto
└── run.py               # Script de ejecución simple
```

## 🏷️ Versionado Semántico

Seguimos [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (ej: 1.2.3)
- **MAJOR:** Cambios incompatibles de API
- **MINOR:** Nueva funcionalidad compatible
- **PATCH:** Bug fixes compatibles

### Ejemplos:
- `v1.0.0` - Release inicial
- `v1.1.0` - Nueva característica (nuevo proceso)
- `v1.0.1` - Bug fix (error en GUI)
- `v2.0.0` - Cambio incompatible (nueva arquitectura)

## 🔧 Configuración de Secretos

Para publicación automática en PyPI, configurar en GitHub:

```
Settings → Secrets and variables → Actions → New repository secret
```

**Secrets necesarios:**
- `PYPI_API_TOKEN` - Token de PyPI para publicación

**Obtener token PyPI:**
1. Ir a https://pypi.org/manage/account/token/
2. Crear nuevo token con scope: "Entire account"
3. Copiar token en GitHub Secrets

## 🐛 Resolución de Problemas

### Error: "Tag already exists"
```bash
# Eliminar tag local y remoto
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# Crear nuevo tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Error: "Build failed"
```bash
# Verificar tests localmente
python scripts/build.py

# Verificar que pasa todas las pruebas
uv run pytest

# Verificar calidad de código
uv run black --check src/
uv run flake8 src/
```

### Error: "PyPI upload failed"
- Verificar que el token PYPI_API_TOKEN está configurado
- Verificar que la versión no existe ya en PyPI
- Verificar que el paquete pasa twine check

## 📊 Workflow de CI/CD

El archivo `.github/workflows/ci.yml` define:

### Jobs ejecutados:
1. **test:** Python 3.8-3.12 en Ubuntu/Windows/macOS
2. **lint:** Code quality checks
3. **security:** Vulnerability scanning
4. **build:** Package building
5. **create-release-bundle:** Bundle creation
6. **publish:** PyPI publication

### Triggers:
- **Push** a `main` o `develop`
- **Pull Request** a `main`
- **Release** published

## 📈 Métricas de Release

Después de cada release, revisar:

- ✅ Downloads en GitHub Releases
- ✅ Instalaciones desde PyPI
- ✅ Issues reportados
- ✅ Feedback de usuarios

## 🔄 Rollback de Release

Si es necesario hacer rollback:

```bash
# 1. Eliminar release en GitHub UI
# 2. Eliminar tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0

# 3. Crear hotfix release
git checkout -b hotfix/v1.0.1
# Fix issues...
git commit -m "Fix critical issue"

# 4. Nueva release
git tag -a v1.0.1 -m "Hotfix v1.0.1"
git push origin v1.0.1
```

---

**¡Con esta guía tendrás releases consistentes y profesionales!** 🎉