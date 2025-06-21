# 🧪 Tests - Sistema Hefest

Suite completa de tests del sistema Hefest, organizada profesionalmente con datos reales y cobertura completa.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🏗️ Estructura de Tests](#-estructura-de-tests) | 18-35 | Organización por tipos y archivos |
| [🚀 Uso de la Suite](#-uso-de-la-suite) | 37-65 | Comandos y ejecución de tests |
| [📊 Estado Actual](#-estado-actual) | 67-85 | Estado y estadísticas de tests |
| [🔧 Comandos de Desarrollo](#-comandos-de-desarrollo) | 87-110 | Herramientas avanzadas y troubleshooting |
| [💡 Filosofía de Testing](#-filosofía-de-testing) | 112-130 | Principios y mejores prácticas |
| [📁 Políticas de Testing](#-políticas-de-testing) | 132-fin | **Políticas de creación y organización de tests** |

---

## 🏗️ Estructura de Tests

### 📂 Organización por Tipos

```
tests/
├── __init__.py                 # Inicialización del paquete
├── test_suite.py              # Suite principal de tests
├── unit/                      # Tests unitarios independientes
│   ├── test_auth_service.py   # Autenticación y autorización
│   ├── test_inventario_service.py # Inventario (DATOS REALES)
│   ├── test_models.py         # Modelos de datos
│   └── test_database_manager.py # Gestor de base de datos
├── integration/               # Tests de flujos completos
│   └── test_user_inventory_integration.py # Integración usuario-inventario
└── ui/                       # Tests de interfaz de usuario
    └── test_ui_components.py  # Componentes UI
```

### ✅ Migración a Datos Reales Completada

**Antes**: Datos simulados/hardcodeados  
**Después**: Mocks realistas basados en BD real

```python
# Datos reales mockeados
mock_db.query.return_value = [
    {"id": 1, "nombre": "Coca Cola", "precio": 2.50, "stock": 15}
]
```

---

## 🚀 Uso de la Suite

### Comandos Principales

```bash
# Ejecutar TODOS los tests
python -m tests.test_suite

# Solo tests unitarios
python -m tests.test_suite unit

# Solo tests de integración  
python -m tests.test_suite integration

# Tests con pytest (alternativo)
pytest tests/ -v
```

### Comandos Especializados

```bash
# Tests específicos por nombre
pytest tests/unit/test_inventario_service.py::TestInventarioServiceReal::test_get_productos -v

# Tests que contengan palabra clave
pytest tests/ -k "inventario" -v

# Tests con cobertura de código
pytest tests/ --cov=src --cov-report=html
```

---

## 📊 Estado Actual

### ✅ Tests Pasando (45/45 - 100%)

| Categoría | Tests | Estado | Descripción |
|-----------|-------|--------|-------------|
| **Unit Tests** | 25/25 | ✅ Completado | Servicios con datos reales |
| **Integration** | 3/3 | ✅ Completado | Flujos usuario-sistema |
| **UI Tests** | 17/17 | ✅ Completado | Componentes de interfaz |

### 📈 Métricas de Calidad
- **Coverage**: 95%+ en módulos críticos
- **Datos**: 100% migración a datos reales completada
- **Velocidad**: Tests unitarios < 1s, integración < 5s
- **Estabilidad**: 0 tests flaky detectados

---

## 🔧 Comandos de Desarrollo

### Análisis y Depuración

```bash
# Generar reporte de cobertura HTML
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Ver cobertura en navegador
start htmlcov/index.html  # Windows
open htmlcov/index.html   # Mac
```

### Limpieza y Mantenimiento

```bash
# Limpiar cache de tests (PowerShell)
Get-ChildItem -Path tests -Recurse -Name "__pycache__" | ForEach-Object { Remove-Item -Path $_ -Recurse -Force }

# Usar task de VS Code
Ctrl+Shift+P > "Tasks: Run Task" > "Limpiar Cache"
```

### Troubleshooting

```bash
# Error "Module not found" - Configurar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:./src"

# Tests lentos - Solo unitarios
python -m tests.test_suite unit

# Cache issues - Limpiar todo
find . -type d -name "__pycache__" -exec rm -r {} +
```

---

## 💡 Filosofía de Testing

### 🎯 Principios

#### Tests Unitarios
- **Aislados**: Cada test es independiente
- **Rápidos**: Ejecución inmediata usando mocks
- **Datos Reales**: Servicios usan estructura de BD real
- **Coverage**: Cobertura completa de funcionalidades críticas

#### Tests de Integración  
- **Workflow Real**: Prueban flujos completos usuario-sistema
- **Base de Datos**: Usan BD de test real
- **Escenarios**: Cubren casos de uso reales del negocio

#### Tests de UI
- **Componentes**: Prueban widgets y diálogos individuales
- **Interacción**: Simulan clicks, input de usuario
- **Responsividad**: Verifican adaptación a diferentes tamaños

### 🏗️ Estructura de Test Estándar

```python
def test_metodo_especifico(self):
    """Test descripción clara de qué se prueba"""
    # Arrange - Preparar datos/mocks
    mock_data = {...}
    
    # Act - Ejecutar función bajo test
    resultado = service.metodo(params)
    
    # Assert - Verificar resultado
    self.assertEqual(resultado, expected)
```

---

## 📁 Políticas de Testing

### 📝 Nomenclatura de Tests

#### ✅ Archivos
- **Formato**: `test_[modulo].py`
- **Ubicación**: Según tipo en `unit/`, `integration/`, `ui/`
- **Ejemplos**: `test_auth_service.py`, `test_user_inventory_integration.py`

#### ✅ Clases y Métodos
- **Clases**: `Test[ClaseObjeto]` (ej: `TestInventarioService`)
- **Métodos**: `test_[funcionalidad_especifica]` (ej: `test_get_productos_success`)
- **Docstrings**: Descripción clara de qué se prueba

### 📍 Ubicación de Tests

| Tipo de Test | Ubicación | Cuándo usar |
|--------------|-----------|-------------|
| **Unitario** | `tests/unit/` | Testing de servicios, modelos, funciones aisladas |
| **Integración** | `tests/integration/` | Testing de flujos completos usuario-sistema |
| **UI** | `tests/ui/` | Testing de componentes, widgets, diálogos |

### 🔧 Estándares de Código

#### ✅ Mocking Guidelines
- **Mock BD**: Siempre usar mocks para base de datos en tests unitarios
- **Datos Realistas**: Los mocks deben reflejar estructura real de datos
- **Type Guards**: Usar verificaciones de tipo cuando sea necesario

#### ✅ Estructura Obligatoria
```python
# Imports estándar
import unittest
from unittest.mock import Mock, patch
from PyQt6.QtWidgets import QApplication

# Imports del proyecto
from src.services.auth_service import AuthService
from src.core.models import Usuario

class TestAuthService(unittest.TestCase):
    def setUp(self):
        """Configuración antes de cada test"""
        pass
        
    def tearDown(self):
        """Limpieza después de cada test"""
        pass
        
    def test_caso_especifico(self):
        """Docstring explicando qué se prueba"""
        # Arrange, Act, Assert
        pass
```

### 📊 Criterios de Calidad

#### ✅ HACER
- Usar datos realistas en mocks
- Nombrar tests descriptivamente
- Incluir docstrings explicativas
- Seguir patrón Arrange-Act-Assert
- Mockear dependencias externas
- Limpiar recursos en tearDown

#### ❌ NO HACER
- Tests que dependan de otros tests
- Datos hardcodeados irrealistas
- Tests sin docstrings
- Mockear la función bajo test
- Tests que modifiquen BD real
- Tests flaky o inconsistentes

### 🔄 Mantenimiento de Tests

- **Ejecutar** suite completa antes de commits
- **Actualizar** tests cuando cambie funcionalidad
- **Revisar cobertura** periódicamente
- **Limpiar** tests obsoletos o duplicados
- **Documentar** cambios significativos

### 🚀 Integración CI/CD

Tests preparados para pipelines automatizados:

```yaml
# Ejemplo .github/workflows/tests.yml
- name: Run Tests
  run: |
    python -m pytest tests/ -v --cov=src
    python -m tests.test_suite
```

---

**📖 Para crear un nuevo test**: Sigue la [nomenclatura](#-nomenclatura-de-tests) y [ubicación](#-ubicación-de-tests) según el tipo de test que necesites.
