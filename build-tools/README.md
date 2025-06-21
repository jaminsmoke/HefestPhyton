# 🔨 Build Tools - Sistema Hefest

Herramientas de construcción, testing multi-entorno y automatización de build para el proyecto Hefest.

---

## � Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🛠️ Herramientas Disponibles](#%EF%B8%8F-herramientas-disponibles) | 18-30 | Lista de herramientas de build |
| [🚀 Uso y Comandos](#-uso-y-comandos) | 32-50 | Instrucciones de ejecución |
| [⚙️ Configuración](#%EF%B8%8F-configuración) | 52-fin | Variables y dependencias |

---

## 🛠️ Herramientas Disponibles

### 📦 Herramientas de Build

| Herramienta | Archivo | Propósito |
|-------------|---------|-----------|
| **Tox** | `tox.ini` | Testing multi-entorno y automatización |

### 🎯 Entornos Configurados

#### ✅ Testing Multi-Python
- **py310**: Testing en Python 3.10
- **py311**: Testing en Python 3.11  
- **py312**: Testing en Python 3.12

#### ✅ Herramientas de Calidad
- **lint**: Linting con flake8 y mypy
- **format**: Formateo con black e isort
- **docs**: Generación de documentación

#### ✅ Build y Distribución
- **build**: Construcción de paquetes wheel y sdist

---

## 🚀 Uso y Comandos

### 🔧 Testing Multi-Entorno

```bash
# Instalar tox
pip install tox

# Ejecutar todos los entornos
tox

# Solo Python específico
tox -e py310
tox -e py311

# Solo linting y formateo
tox -e lint
tox -e format

# Build de paquetes
tox -e build
```

### 📊 Gestión de Entornos

```bash
# Ver entornos configurados
tox -l

# Recrear entorno limpio
tox -r -e py310

# Ejecutar con verbose
tox -v

# Parallel execution
tox -p auto
```

### � Testing Específico

```bash
# Solo tests unitarios
tox -e py310 -- tests/unit/

# Tests con cobertura
tox -e py310 -- --cov=src --cov-report=html

# Tests específicos
tox -e py310 -- tests/unit/test_auth_service.py
```

---

## ⚙️ Configuración

### 🔧 Variables de Entorno

| Variable | Valor | Propósito |
|----------|-------|-----------|
| `PYTHONPATH` | `{toxinidir}/src` | Path automático para imports |
| `TOX_PARALLEL_NO_SPINNER` | `1` | Desactiva spinner en CI/CD |

### 📦 Dependencias por Entorno

#### 🧪 Testing
```ini
pytest >= 7.0
pytest-cov >= 4.0
pytest-qt >= 4.0
pytest-mock >= 3.0
```

#### 🔍 Linting
```ini
black >= 23.0
flake8 >= 6.0
mypy >= 1.0
isort >= 5.0
```

#### 🏗️ Build
```ini
build >= 0.10
wheel >= 0.40
setuptools >= 65.0
```

### 🎯 Configuración Tox

El archivo `tox.ini` configura:
- **Aislamiento**: Cada entorno en virtualenv separado
- **Paralelización**: Ejecución simultánea de tests
- **Coverage**: Reportes de cobertura automáticos
- **CI/CD Ready**: Optimizado para pipelines automáticos

---

**📖 Para usar las build tools**: Ejecuta `tox -l` para ver entornos disponibles y `tox -e [entorno]` para ejecutar tareas específicas.
