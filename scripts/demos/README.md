# 🎭 Scripts de Demos - Sistema Hefest

Scripts para demostraciones, pruebas de concepto y validación de arquitecturas del sistema Hefest.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🎯 Demos Disponibles](#-demos-disponibles) | 18-35 | Scripts de demostración implementados |
| [🚀 Uso y Ejecución](#-uso-y-ejecución) | 37-55 | Comandos y procedimientos |
| [📁 Políticas de Organización](#-políticas-de-organización) | 57-fin | Estándares para scripts de demo |

---

## 🎯 Demos Disponibles

### 📊 Demostraciones de Arquitectura

| Script | Propósito | Estado |
|--------|-----------|--------|
| `demo_v3_arquitectura.py` | Demostración de arquitectura V3 visual | ✅ Activo |

### 🎭 Tipos de Demos

#### ✅ `demo_v3_arquitectura.py`
- **Función**: Demuestra la arquitectura visual V3
- **Uso**: Validación de diseño y componentes visuales
- **Audiencia**: Desarrolladores y stakeholders

---

## 🚀 Uso y Ejecución

### 📝 Comandos Básicos

```bash
# Ejecutar demo de arquitectura V3
python scripts/demos/demo_v3_arquitectura.py

# Ejecutar todos los demos (cuando haya más)
# python scripts/demos/demo_*.py
```

### 🔧 Configuración

- **Directorio de trabajo**: Ejecutar desde raíz del proyecto
- **Dependencias**: PyQt6, servicios del sistema
- **Propósito**: Demostración y validación

---

## 📁 Políticas de Organización

### 📝 Nomenclatura de Scripts de Demo

**Formato**: `demo_[COMPONENTE]_[TIPO].py`

**Ejemplos válidos**:
```
demo_v3_arquitectura.py           # Demo de arquitectura V3
demo_dashboard_features.py        # Demo de características del dashboard
demo_ui_components.py             # Demo de componentes UI
demo_integration_flow.py          # Demo de flujo de integración
```

### 🎯 Criterios de Creación

#### ✅ Cuándo Crear un Script de Demo
- **Pruebas de concepto** de nuevas funcionalidades
- **Demostraciones** para stakeholders o equipo
- **Validación de arquitectura** de componentes
- **Showcase** de capacidades del sistema

#### ✅ Características de un Buen Demo
- **Autocontenido**: Funciona independientemente
- **Documentado**: Explicación clara del propósito
- **Visual**: Muestra resultados tangibles
- **Educativo**: Enseña sobre el sistema

### 🔄 Flujo de Trabajo

1. **Identificar necesidad** de demostración
2. **Crear script** siguiendo nomenclatura estándar
3. **Implementar demo** autocontenido
4. **Documentar propósito** y uso
5. **Actualizar este README** con información del demo

### 📊 Mejores Prácticas

#### ✅ Estructura Recomendada
```python
#!/usr/bin/env python3
"""
Demo: [DESCRIPCIÓN DEL PROPÓSITO]
Audiencia: [DESARROLLADORES/STAKEHOLDERS/AMBOS]
"""

def main():
    """Función principal del demo."""
    print("Iniciando demo: [NOMBRE]")
    # Lógica del demo
    print("Demo completado exitosamente")

if __name__ == "__main__":
    main()
```

---

**📖 Documentación relacionada**: [`scripts/README.md`](../README.md) • [`src/ui/README.md`](../../src/ui/README.md)
