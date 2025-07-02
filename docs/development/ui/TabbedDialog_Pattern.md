# 📋 Patrón TabbedDialog - Diálogos con Pestañas Modernas

## 🎯 Objetivo

Establecer un patrón estándar y reutilizable para diálogos complejos con múltiples secciones, utilizando pestañas horizontales modernas y estructura consistente.

---

## 🏗️ Arquitectura

### **Componente Base: `TabbedDialog`**
- **Ubicación**: `src/ui/components/TabbedDialog.py`
- **Propósito**: Clase base reutilizable para diálogos con pestañas
- **Herencia**: Extiende `QDialog` de PyQt6

### **Estructura Estándar**
```
┌─────────────────────────────────────┐
│ 🏷️  HEADER (Título + Subtítulo)     │
├─────────────────────────────────────┤
│ [📋 Tab1] [⚙️ Tab2] [📊 Tab3]        │ ← Pestañas horizontales
├─────────────────────────────────────┤
│                                     │
│     CONTENIDO DE LA PESTAÑA         │
│                                     │
├─────────────────────────────────────┤
│        [Cancelar] [Guardar]         │ ← Footer estándar
└─────────────────────────────────────┘
```

---

## 🚀 Uso del Componente

### **1. Importar y Heredar**
```python
from src.ui.components.TabbedDialog import TabbedDialog

class MiDialog(TabbedDialog):
    def __init__(self, parent=None):
        super().__init__("Título del Diálogo", parent)
```

### **2. Configurar Header**
```python
self.set_header_title(
    "Título Principal",
    "Subtítulo descriptivo (opcional)"
)
```

### **3. Añadir Pestañas**
```python
# Crear página
page = QWidget()
layout = QVBoxLayout(page)
layout.addWidget(QLabel("Contenido"))

# Añadir pestaña
self.add_tab(page, "Información", "📋")  # widget, título, icono
```

---

## ✅ Beneficios del Patrón

- **Consistencia**: Todos los diálogos siguen el mismo patrón visual
- **Escalabilidad**: Fácil añadir/quitar secciones
- **Mantenibilidad**: Código reutilizable y centralizado
- **UX Familiar**: Pestañas conocidas por los usuarios
- **Responsive**: Se adapta al contenido automáticamente

---

## 🔧 Estado de Implementación

### **TabbedDialog Base** ✅
- Componente creado y funcional
- Probado exitosamente
- Listo para uso en producción

### **MesaDialogTabbed** ✅  
- Implementación de ejemplo completada
- 4 pestañas: Información, Acciones, Configuración, Historial
- Listo para integración

---

> **Nota**: Este patrón reemplaza los experimentos con pestañas flotantes, proporcionando una solución más estable y familiar para los usuarios.