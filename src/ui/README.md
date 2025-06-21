# UI Hefest (Sintetizado)

- Componentes y módulos de interfaz en subcarpetas.
- Nomenclatura: clara y descriptiva.
- Cada módulo debe tener README propio si es complejo.
- Para detalles, ver README completo si es necesario.

---

# 🎨 UI Components - Interfaz de Usuario

Componentes de interfaz de usuario del sistema Hefest, organizados por tipo y funcionalidad con arquitectura moderna.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🏗️ Estructura de Carpetas](#-estructura-de-carpetas) | 18-45 | Organización por tipos de componentes |
| [🎯 Criterios de Ubicación](#-criterios-de-ubicación) | 47-85 | Dónde crear cada tipo de componente |
| [🎨 Estándares de Diseño](#-estándares-de-diseño) | 87-105 | Guidelines de UI/UX y responsividad |
| [🔗 Comunicación entre Componentes](#-comunicación-entre-componentes) | 107-125 | Señales PyQt y arquitectura |
| [📊 Estado Actual](#-estado-actual) | 127-145 | Componentes implementados v0.0.12 |
| [📁 Políticas de Componentes UI](#-políticas-de-componentes-ui) | 147-fin | **Políticas de nomenclatura y creación** |

---

## 🏗️ Estructura de Carpetas

### � Organización por Tipo de Componente

```
src/ui/
├── components/          # 🧩 Componentes reutilizables
│   ├── ModernButton.py     # Botones con efectos visuales
│   ├── DataTable.py        # Tablas de datos
│   └── AnimatedCard.py     # Cards con animaciones
├── modules/             # 📋 Módulos principales completos
│   ├── dashboard_admin_v3/ # Dashboard moderno V3
│   ├── tpv_module/         # Terminal punto de venta
│   ├── inventario_module/  # Gestión de inventario
│   ├── hospederia_module/  # Sistema de hospedería
│   └── user_management_module/ # Gestión de usuarios
├── dialogs/             # 💬 Ventanas de diálogo modales
│   ├── UserDialog.py       # Crear/editar usuarios
│   ├── ProductDialog.py    # Gestión de productos
│   └── ConfirmDialog.py    # Confirmaciones
└── windows/             # 🪟 Ventanas principales
    ├── MainWindow.py       # Ventana principal
    ├── LoginWindow.py      # Autenticación
    └── SplashScreen.py     # Pantalla de carga
```

### 🎯 Arquitectura Moderna V3

**Dashboard V3**: Sistema completo con métricas en tiempo real  
**Componentes Modernos**: Animaciones, efectos visuales, responsividad  
**Integración Real**: Conectado con datos reales de base de datos

---

## 🎯 Criterios de Ubicación

### 🧩 **components/** - Componentes Reutilizables

**Cuándo usar**:
- ✅ Se reutiliza en múltiples módulos
- ✅ Es un widget independiente  
- ✅ Tiene funcionalidad genérica
- ✅ Puede configurarse con parámetros

```python
# Ejemplo: ModernButton.py
class ModernButton(QPushButton):
    """Botón moderno reutilizable con efectos visuales"""
    def __init__(self, text="", style="primary", parent=None):
        # Componente configurable y reutilizable
```

### 📋 **modules/** - Módulos Principales

**Cuándo usar**:
- ✅ Es una funcionalidad completa
- ✅ Maneja un área específica del negocio
- ✅ Integra múltiples componentes
- ✅ Tiene su propia lógica de estado

```python
# Ejemplo: InventoryModule.py
class InventoryModule(QWidget):
    """Módulo completo de gestión de inventario"""
    def __init__(self):
        # Integra búsqueda, tabla, botones, etc.
```

### 💬 **dialogs/** - Ventanas de Diálogo

**Cuándo usar**:
- ✅ Es una ventana modal
- ✅ Solicita información específica
- ✅ Confirma acciones del usuario
- ✅ Es temporal y se cierra

### 🪟 **windows/** - Ventanas Principales

**Cuándo usar**:
- ✅ Es una ventana principal
- ✅ Maneja el flujo general
- ✅ Contiene múltiples módulos
- ✅ Es punto de entrada

---

## 🎨 Estándares de Diseño

### 🎨 Estilo Visual

- **Colores**: Variables CSS definidas en `assets/styles/`
- **Consistencia**: Theme unificado en toda la aplicación
- **Modo Oscuro**: Implementado donde sea relevante
- **Iconos**: Set consistente con biblioteca establecida

### ⚡ Animaciones y Efectos

- **Transiciones**: `QPropertyAnimation` para suavidad
- **Duración**: 200-300ms para efectos rápidos
- **Curvas**: `QEasingCurve.OutCubic` como estándar
- **Performance**: Optimizadas para 60fps

### 📱 Responsividad

- **Layouts**: Flexibles (`QVBoxLayout`, `QHBoxLayout`)
- **Resize Events**: Implementados cuando sea necesario
- **Resolución Mínima**: 1024x768
- **Escalabilidad**: Preparado para múltiples tamaños

---

## 🔗 Comunicación entre Componentes

### 📡 Señales PyQt (Recomendado)

```python
# Definir señales en componentes
class MyComponent(QWidget):
    data_changed = pyqtSignal(dict)
    action_requested = pyqtSignal(str, object)
    
    def some_method(self):
        # Emitir señales
        self.data_changed.emit(new_data)
        self.action_requested.emit("save", data)
```

### 🚫 Evitar Referencias Directas

- ❌ `parent.module.update_data()` - Acoplamiento fuerte
- ✅ `self.data_updated.emit(data)` - Comunicación por señales

### 🏗️ Arquitectura de Comunicación

- **Módulos → Ventana Principal**: Vía señales
- **Componentes → Módulos**: Vía señales  
- **Servicios → UI**: Vía callbacks o señales

---

## 📊 Estado Actual

### ✅ Componentes Implementados v0.0.12

| Componente | Estado | Descripción |
|------------|--------|-------------|
| **Dashboard V3** | ✅ Completado | Arquitectura moderna con métricas reales |
| **Componentes Modernos** | ✅ Completado | Botones, cards, indicadores animados |
| **Módulos Principales** | ✅ Completado | TPV, Inventario, Hospedería operativos |
| **Sistema Autenticación** | ✅ Completado | Login y gestión de usuarios |
| **Testing UI** | ✅ Completado | 17/17 tests de UI pasando |

### 🎯 Próximos Componentes

- `NotificationCenter.py` - Centro de notificaciones
- `AdvancedSearchBox.py` - Búsqueda con filtros
- `ExportDialog.py` - Diálogo de exportación
- `ChartWidget.py` - Widget de gráficos personalizados

---

## 📁 Políticas de Componentes UI

### 📝 Nomenclatura Estándar

#### ✅ Patrón de Nombres
```
[TipoComponente][NombreEspecifico].py
```

#### ✅ Ejemplos Correctos
- `ModernButton.py` - Componente reutilizable
- `DashboardMetricCard.py` - Componente específico
- `LoginDialog.py` - Diálogo específico
- `MainWindow.py` - Ventana principal
- `InventoryModule.py` - Módulo completo

#### ❌ Ejemplos Incorrectos
- `button.py` - Sin descripción específica
- `modern_dialog.py` - Formato snake_case
- `ui_component.py` - Muy genérico

### 📍 Criterios de Ubicación

| Tipo | Ubicación | Características |
|------|-----------|----------------|
| **Reutilizable** | `components/` | Configurable, genérico, usado en múltiples lugares |
| **Funcionalidad Completa** | `modules/` | Área de negocio específica, integra componentes |
| **Modal** | `dialogs/` | Ventana temporal, solicita información |
| **Principal** | `windows/` | Punto de entrada, orquesta flujos |

### 🏗️ Estructura de Código Estándar

```python
"""
[NombreComponente] - [Descripción breve]

Propósito: [Para qué se usa]
Ubicación: src/ui/[carpeta]/[archivo].py
Dependencias: [PyQt6, otros componentes]
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

class [NombreComponente](QWidget):
    """[Descripción detallada del componente]"""
    
    # Señales del componente
    signal_name = pyqtSignal(object)
    
    def __init__(self, parent=None):
        """Inicializar componente"""
        super().__init__(parent)
        self.setupUI()
        self.connectSignals()
    
    def setupUI(self):
        """Configurar interfaz visual"""
        pass
    
    def connectSignals(self):
        """Conectar señales y slots"""
        pass
```

### 🧪 Testing de Componentes

#### Ubicación de Tests
- **Tests UI**: `tests/ui/test_[componente].py`
- **Tests Integración**: `tests/integration/test_[modulo]_integration.py`

#### Estructura de Test
```python
# tests/ui/test_[componente].py
class Test[Componente]:
    def test_initialization(self):
        """Test creación básica"""
        
    def test_user_interaction(self):
        """Test interacciones del usuario"""
        
    def test_signal_emission(self):
        """Test emisión de señales"""
```

### ✅ Criterios de Calidad

#### ✅ HACER
- Usar nomenclatura consistente PascalCase
- Documentar propósito y dependencias
- Implementar señales para comunicación
- Seguir estándares de diseño visual
- Crear tests para componentes críticos
- Reutilizar componentes existentes antes de crear nuevos

#### ❌ NO HACER
- Nomenclatura en snake_case
- Referencias directas entre módulos
- Hardcodear estilos en código Python
- Crear componentes sin documentación
- Ignorar estándares de animación
- Duplicar funcionalidad existente

### 📋 Checklist para Nuevo Componente

- [ ] Nombre sigue patrón `[Tipo][Nombre].py`
- [ ] Ubicación correcta según funcionalidad
- [ ] Docstring completo con propósito
- [ ] Estructura estándar implementada
- [ ] Señales definidas para comunicación
- [ ] Estilos usando variables CSS
- [ ] Tests básicos creados
- [ ] Documentación actualizada

### 🔄 Mantenimiento

- **Revisar reutilización** antes de crear componentes nuevos
- **Actualizar tests** cuando cambie funcionalidad
- **Mantener consistencia** visual y de código
- **Documentar cambios** significativos en changelog

---

**💡 Recordatorio**: Antes de crear un componente, verifica si ya existe algo similar en `components/` que puedas reutilizar o extender.
- ✅ Maneja el flujo general
- ✅ Contiene múltiples módulos
- ✅ Es punto de entrada

```python
# Ejemplo: MainWindow.py
class MainWindow(QMainWindow):
    """Ventana principal del sistema"""
    def __init__(self):
        # Orquesta módulos y navegación
```

## 📝 ESTRUCTURA ESTÁNDAR DE COMPONENTE

### Template Básico:
```python
"""
[NombreComponente] - [Descripción breve]

Propósito: [Para qué se usa]
Ubicación: src/ui/[carpeta]/[archivo].py
Dependencias: [PyQt6, otros componentes]
"""

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal

class [NombreComponente](QWidget):
    """[Descripción detallada del componente]"""
    
    # Señales del componente
    signal_name = pyqtSignal(object)
    
    def __init__(self, parent=None):
        """Inicializar componente"""
        super().__init__(parent)
        self.setupUI()
        self.connectSignals()
    
    def setupUI(self):
        """Configurar interfaz visual"""
        pass
    
    def connectSignals(self):
        """Conectar señales y slots"""
        pass
```

## 🎨 ESTÁNDARES DE DISEÑO

### **Colores y Estilo**
- Usar variables CSS definidas en `assets/styles/`
- Mantener consistencia con el theme general
- Implementar modo claro/oscuro cuando sea relevante

### **Animaciones**
- Usar `QPropertyAnimation` para transiciones suaves
- Duración estándar: 200-300ms para efectos rápidos
- Curvas de animación: `QEasingCurve.OutCubic`

### **Responsividad**
- Usar layouts flexibles (`QVBoxLayout`, `QHBoxLayout`)
- Implementar `resizeEvent` cuando sea necesario
- Mínimo de resolución: 1024x768

## 🔗 COMUNICACIÓN ENTRE COMPONENTES

### **Usar Señales PyQt**
```python
# Definir señales
data_changed = pyqtSignal(dict)
action_requested = pyqtSignal(str, object)

# Emitir señales
self.data_changed.emit(new_data)
self.action_requested.emit("save", data)
```

### **Evitar Referencias Directas**
- ❌ `parent.module.update_data()`
- ✅ `self.data_updated.emit(data)`

## 🧪 TESTING DE COMPONENTES UI

### **Estructura de Test**
```python
# tests/ui/test_[componente].py
class Test[Componente]:
    def test_initialization(self):
        """Test creación básica"""
        
    def test_user_interaction(self):
        """Test interacciones del usuario"""
        
    def test_signal_emission(self):
        """Test emisión de señales"""
```

## 📊 Estado Actual (Junio 2025)

### ✅ Componentes Implementados:
- **Dashboard V3**: Arquitectura moderna completa ✅
- **Componentes Modernos**: Botones, cards, indicadores ✅  
- **Módulos Principales**: TPV, Inventario, Hospedería ✅
- **Sistema de Autenticación**: Login y gestión usuarios ✅

### 🎯 Próximos Componentes:
- `NotificationCenter.py` - Centro de notificaciones
- `AdvancedSearchBox.py` - Búsqueda con filtros
- `ExportDialog.py` - Diálogo de exportación
- `ChartWidget.py` - Widget de gráficos personalizados

---

**💡 Recordatorio**: Antes de crear un componente, verifica si ya existe algo similar en `components/` que puedas reutilizar o extender.

*Políticas actualizadas: 13 de Junio 2025 - v0.0.12*
