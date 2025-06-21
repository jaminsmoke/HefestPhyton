# 🧪 Scripts de Testing - Sistema Hefest

Scripts especializados para testing manual, validación de componentes y verificación de integridad del sistema Hefest.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🔧 Scripts Disponibles](#-scripts-disponibles) | 18-35 | Scripts de testing implementados |
| [🚀 Uso y Ejecución](#-uso-y-ejecución) | 37-55 | Comandos y procedimientos |
| [📁 Políticas de Organización](#-políticas-de-organización) | 57-fin | Estándares para scripts de testing |

---

## 🔧 Scripts Disponibles

### 📊 Scripts de Testing

| Script | Estado |
|--------|--------|
| *En desarrollo* | ⏳ Pendiente |

*Esta carpeta está preparada para recibir scripts de testing manual y validación de componentes.*

### 🎯 Tipos de Testing Esperados

- **Testing manual** de componentes UI
- **Validación de integridad** de servicios
- **Scripts de verificación** de configuración
- **Testing de integración** manual

---

## 🚀 Uso y Ejecución

### 📝 Comandos Básicos

```bash
# Ejecutar desde raíz del proyecto
python scripts/testing/[SCRIPT_NAME].py
```

### 🔧 Configuración

- **Directorio de trabajo**: Ejecutar desde raíz del proyecto
- **Dependencias**: Según cada script específico
- **Entorno**: Testing/desarrollo

---

## 📁 Políticas de Organización

### 📝 Nomenclatura de Scripts de Testing

**Formato**: `test_[COMPONENTE]_[TIPO].py`

**Ejemplos**:
```
test_dashboard_manual.py          # Testing manual de dashboard
test_components_validation.py     # Validación de componentes
test_services_integration.py      # Testing de integración de servicios
test_ui_visual_verification.py    # Verificación visual de UI
```

### 🎯 Criterios de Creación

#### ✅ Cuándo Crear un Script de Testing
- **Testing manual** que requiere intervención humana
- **Validación visual** de componentes UI
- **Verificación de integración** entre módulos
- **Testing de configuración** específica

#### ❌ Lo que NO va aquí
- **Tests unitarios automáticos** → `tests/unit/`
- **Tests de integración automáticos** → `tests/integration/`
- **Tests de UI automáticos** → `tests/ui/`

### 🔄 Flujo de Trabajo

1. **Identificar necesidad** de testing manual
2. **Crear script** siguiendo nomenclatura
3. **Documentar procedimiento** en docstring
4. **Actualizar este README** con el nuevo script

---

**📖 Documentación relacionada**: [`scripts/README.md`](../README.md) • [`tests/README.md`](../../tests/README.md)
