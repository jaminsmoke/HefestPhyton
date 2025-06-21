# 🛠️ Utilidades del Sistema - Hefest

Herramientas auxiliares, helpers y utilidades de soporte para el funcionamiento del sistema Hefest.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🔧 Utilidades Disponibles](#-utilidades-disponibles) | 18-50 | Módulos y herramientas implementadas |
| [🚀 Uso de Utilidades](#-uso-de-utilidades) | 52-70 | Importación y uso de cada módulo |
| [📁 Políticas de Organización](#-políticas-de-organización) | 72-fin | Estándares para utilidades |

---

## 🔧 Utilidades Disponibles

### ⚙️ Configuración y Gestión

| Módulo | Propósito | Estado |
|--------|-----------|--------|
| `application_config_manager.py` | Gestión de configuración principal del sistema | ✅ Activo |
| `real_data_manager.py` | Gestión centralizada de datos reales | ✅ Activo |
| `decorators.py` | Decoradores de utilidad y control de acceso | ✅ Activo |
| `modern_styles.py` | Estilos CSS modernos para la UI | ✅ Activo |
| `monitoring.py` | Monitoreo y métricas del sistema | ✅ Activo |
| `animation_helper.py` | Ayudas para animaciones UI | ✅ Activo |
| `qt_css_compat.py` | Compatibilidad CSS para Qt | ✅ Activo |
| `archive/` | Archivos archivados y obsoletos | 📁 Archivo |

### 🎨 UI y Componentes Visuales

| Módulo | Propósito | Estado |
|--------|-----------|--------|
| `modern_styles.py` | Estilos modernos para componentes UI | ✅ Activo |
| `qt_css_compat.py` | Compatibilidad de CSS con Qt | ✅ Activo |
| `animation_helper.py` | Helpers para animaciones UI | ✅ Activo |

### 🔍 Desarrollo y Debugging

| Módulo | Propósito | Estado |
|--------|-----------|--------|
| `monitoring.py` | Monitoreo y logging del sistema | ✅ Activo |
| `decorators.py` | Decoradores útiles para desarrollo | ✅ Activo |

### 🎯 Funcionalidades por Módulo

#### ⚙️ Configuración
- **`application_config_manager.py`**: Gestión principal de configuración del sistema
- **`real_data_manager.py`**: Manager de datos reales del sistema

#### 🎨 UI y Visuales
- **`modern_styles.py`**: Estilos CSS modernos para PyQt6
- **`qt_css_compat.py`**: Wrapper para compatibilidad CSS/Qt
- **`animation_helper.py`**: Funciones para animaciones fluidas

#### 🔍 Desarrollo
- **`monitoring.py`**: Sistema de logs y métricas de rendimiento
- **`decorators.py`**: Decoradores para timing, logging, validación

---

## 🚀 Uso de Utilidades

### 📦 Importación Estándar

```python
# Configuración
from src.utils.application_config_manager import ConfigManager
from src.utils.real_data_manager import RealDataManager

# UI y Estilos
from src.utils.modern_styles import ModernStyles
from src.utils.qt_css_compat import apply_css_to_widget
from src.utils.animation_helper import create_fade_animation

# Desarrollo
from src.utils.monitoring import logger, performance_monitor
from src.utils.decorators import timer, validate_args
```

### 🔧 Ejemplos de Uso

#### Configuración
```python
# Cargar configuración
config = load_config('config/default.json')
db_url = get_setting('database.host', default='localhost')
```

#### Estilos y UI
```python
# Aplicar estilos modernos
styles = ModernStyles()
widget.setStyleSheet(styles.get_button_style())
```

#### Monitoring
```python
# Logging y métricas
logger.info("Iniciando operación")
with performance_monitor("operacion_critica"):
    # código a medir
    pass
```

---

## 📁 Políticas de Organización

### 📝 Nomenclatura de Utilidades

**Formato**: `[CATEGORIA]_[PROPOSITO].py`

**Categorías permitidas**:
- `config_` - Gestión de configuración
- `modern_` - Componentes UI modernos  
- `qt_` - Compatibilidad con Qt
- `animation_` - Animaciones y efectos
- `data_` - Gestión de datos
- Sin prefijo - Utilidades generales (`decorators.py`, `monitoring.py`)

### 🎯 Criterios de Creación

#### ✅ Cuándo Crear una Utilidad
- **Funcionalidad reutilizable** en múltiples módulos
- **Helper functions** que simplifican tareas comunes
- **Wrappers** para librerías externas
- **Abstracciones** de funcionalidad compleja

#### ✅ Características de una Buena Utilidad
- **Autocontenida**: Pocas dependencias externas
- **Documentada**: Docstrings claras y ejemplos
- **Testeada**: Tests unitarios cuando sea posible
- **Específica**: Un propósito claro y bien definido

### 📊 Estructura Recomendada

```python
"""
[NOMBRE_UTILIDAD]: Descripción breve del propósito.

Ejemplo de uso:
    from src.utils.mi_utilidad import MiClase
    
    utilidad = MiClase()
    resultado = utilidad.hacer_algo()
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class MiUtilidad:
    """Clase principal de la utilidad."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Inicializar utilidad con configuración opcional."""
        self.config = config or {}
    
    def hacer_algo(self) -> Any:
        """Método principal de la utilidad."""
        pass

# Funciones auxiliares si es necesario
def helper_function() -> bool:
    """Función helper para casos específicos."""
    return True
```

### 🔄 Flujo de Trabajo

1. **Identificar necesidad** de utilidad reutilizable
2. **Crear módulo** siguiendo nomenclatura estándar
3. **Implementar funcionalidad** con documentación
4. **Crear tests** si es lógica compleja
5. **Actualizar imports** en `__init__.py` si es necesario
6. **Documentar en este README** la nueva utilidad

---

**📖 Documentación relacionada**: [`src/README.md`](../README.md) • [`src/services/README.md`](../services/README.md)
