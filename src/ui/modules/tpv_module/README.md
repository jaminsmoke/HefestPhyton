# Módulo TPV (Terminal Punto de Venta) - Hefest

## 📁 **Estructura Organizada**

Esta carpeta contiene la implementación completa del módulo TPV organizada siguiendo el patrón arquitectural del proyecto Hefest v0.0.13.

### 🏗️ **Arquitectura del Módulo**

```
src/ui/modules/tpv_module/
├── tpv_module.py           # ✅ Módulo principal (TPVTab)
├── __init__.py             # Configuración del paquete
├── components/             # Componentes principales TPV
│   └── __init__.py         
├── dialogs/               # Diálogos modales
│   └── __init__.py
└── widgets/               # Widgets reutilizables
    └── __init__.py
```

### 📦 **Componentes Principales**

#### 🎯 **tpv_module.py** - Módulo Principal
- **Clase principal**: `TPVTab` (heredada de `BaseModule`)
- **Funcionalidad**: Terminal Punto de Venta completo
- **Componentes**: Gestión de mesas, comandas, pagos y facturación
- **Líneas de código**: 809 líneas (implementación robusta)

#### 🏗️ **Subcarpetas Organizadas**

##### 📂 **components/**
*Preparada para futuros componentes principales:*
- `order_manager.py` - Gestión de pedidos
- `payment_processor.py` - Procesamiento de pagos
- `ticket_generator.py` - Generación de tickets
- `product_selector.py` - Selector de productos

##### 📂 **dialogs/**
*Preparada para diálogos modales:*
- `payment_dialog.py` - Diálogo de pago
- `ticket_dialog.py` - Vista previa de tickets
- `order_summary_dialog.py` - Resumen de pedidos

##### 📂 **widgets/**
*Preparada para widgets reutilizables:*
- `product_grid.py` - Grid de productos
- `order_summary.py` - Resumen del pedido
- `payment_methods.py` - Métodos de pago
- `numeric_keypad.py` - Teclado numérico

### 🔧 **Estado Actual (v0.0.13)**

#### ✅ **Implementado**
- [x] **Estructura de carpetas** organizada y completa
- [x] **TPVTab principal** movido a nueva ubicación
- [x] **Archivos __init__.py** configurados
- [x] **Importaciones** actualizadas en módulos principales

#### 🚀 **Próximos Pasos**
- [  ] **Refactorización del código** en componentes separados
- [  ] **Modernización de la interfaz** siguiendo estándares v0.0.12
- [  ] **Integración con inventario** profesional
- [  ] **Testing completo** de funcionalidades

### 🎯 **Funcionalidades Incluidas**

#### 🏢 **Gestión de Mesas**
- Sistema de mesas con estados (libre, ocupada, reservada)
- Capacidad y zonificación (comedor, terraza, barra)
- Diálogo de gestión individual por mesa

#### 🛒 **Gestión de Comandas**
- Creación y modificación de pedidos
- Líneas de comanda con productos individuales
- Cálculo automático de totales

#### 💰 **Procesamiento de Pagos**
- Múltiples métodos de pago (efectivo, tarjeta, transferencia, vales)
- Sistema de descuentos (porcentaje y cantidad fija)
- Cálculo de IVA y totales

#### 🧾 **Facturación**
- Generación de facturas completas
- Estados de factura (pendiente, pagada, cancelada)
- Referencia a comandas y métodos de pago

### 🔌 **Integración con el Sistema**

#### 📊 **Servicios Backend**
- **TPVService**: Servicio principal en `src/services/tpv_service.py`
- **Modelos de datos**: Mesa, Comanda, LineaComanda, Factura, etc.
- **Base de datos**: Integración con SQLite existente

#### 🎨 **UI Framework**
- **PyQt6**: Framework de interfaz principal
- **BaseModule**: Herencia del patrón base del sistema
- **Consistencia visual**: Preparado para estándares v0.0.12

### 📋 **Importación del Módulo**

```python
# Importación desde otros módulos
from ui.modules.tpv_module.tpv_module import TPVTab

# Uso en la aplicación principal
tpv_instance = TPVTab(parent=main_window)
```

### ⚠️ **Notas de Desarrollo**

#### 🔧 **Estado del Código**
- **Código funcional**: Base sólida de 809 líneas
- **Arquitectura robusta**: Separación clara de responsabilidades
- **Integración existente**: Conectado con servicios backend
- **Preparado para mejoras**: Estructura organizada para optimización

#### 🎯 **Plan de Optimización v0.0.13**
1. **Refactorización**: Separar componentes en archivos individuales
2. **Modernización**: Aplicar estándares de diseño v0.0.12
3. **Integración**: Conectar con inventario profesional
4. **Performance**: Optimización de operaciones críticas

---

## 📚 **Documentación Relacionada**

- `docs/development/planning/[v0.0.13]_INICIO_DESARROLLO_MODULO_TPV_BASICO.md`
- `docs/development/analysis/[v0.0.13]_ANALISIS_ESTADO_ACTUAL_MODULO_TPV.md`
- `docs/development/completed/[v0.0.13]_PREPARACION_TPV_DEVELOPMENT_COMPLETADA.md`

**Versión**: v0.0.13  
**Estado**: ✅ ESTRUCTURA ORGANIZADA - LISTO PARA DESARROLLO  
**Fecha**: 20/06/2025
