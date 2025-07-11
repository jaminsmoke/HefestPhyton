# 🧰 utils - Utilidades del Sistema

Breve descripción del propósito de la carpeta y su rol en la estructura del proyecto.

---

## 📋 Índice de Contenidos

| Sección                                             | Descripción                              |
| --------------------------------------------------- | ---------------------------------------- |
| [🗂️ Estructura](#estructura)                         | Organización interna y tipos de archivos |
| [📁 Políticas y Estándares](#políticas-y-estándares) | Qué se permite y qué no                  |
| [🚀 Uso e Integración](#uso-e-integración)           | Cómo se usa la carpeta (opcional)        |
| [📖 Información relevante](#información-relevante)   | Enlaces y notas (opcional)               |

---

## 🗂️ Estructura

```
utils/
├── application_config_manager.py   # Gestión de configuración
├── real_data_manager.py            # Datos reales
├── decorators.py                   # Decoradores
├── modern_styles.py                # Estilos CSS
├── monitoring.py                   # Monitoreo
├── animation_helper.py             # Animaciones UI
├── qt_css_compat.py                # Compatibilidad CSS/Qt
├── archive/                        # Utilidades archivadas
└── ...
```

- Explica brevemente la función de los principales archivos y subcarpetas.

---

## 📁 Políticas y Estándares

- Solo se permiten utilidades auxiliares, helpers y módulos de soporte.
- Nomenclatura clara y descriptiva.
- Prohibido incluir lógica de negocio, detalles de implementación o documentación de progreso.
- Referencia a la política general en el README raíz.

---


## 🚀 Uso e Integración

- Importa los módulos según la necesidad del sistema.
- Consulta los README de cada subcarpeta para detalles específicos.

### Ejemplo de integración de estilos visuales

```python
from src.utils.modern_styles import ModernStyles

# Aplicar estilo a un widget
my_widget.setStyleSheet(ModernStyles.get_base_widget_style())

# Aplicar estilo a un label de alias
alias_label.setStyleSheet(ModernStyles.get_alias_label_style())

# Usar estilos para botones modernos
my_button.setStyleSheet(ModernStyles.get_button_styles())
```

### Ejemplo de integración de animaciones

```python
from src.utils.animation_helper import AnimationHelper

# Animar aparición de un widget
AnimationHelper.fade_in(my_widget, duration=400)
```

---

## 📖 Información relevante (opcional)

- Para plantillas y políticas, consulta el README raíz del proyecto.
- Notas y advertencias visuales pueden incluirse aquí si es necesario.

---

> **Nota:** No incluir aquí detalles de progreso, migraciones, ni implementaciones específicas. Toda esa información debe estar en los documentos internos de `docs/`.

---

**Cumple con la política de estandarización y organización definida en el README raíz.**

---
