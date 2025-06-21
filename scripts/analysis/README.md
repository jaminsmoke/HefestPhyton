# 🔍 Scripts de Análisis - Sistema Hefest

Scripts especializados para análisis de código, estructura de proyecto y depuración del sistema Hefest.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🔧 Scripts Disponibles](#-scripts-disponibles) | 18-40 | Herramientas de análisis implementadas |
| [🚀 Uso y Ejecución](#-uso-y-ejecución) | 42-60 | Comandos y procedimientos de uso |
| [📁 Políticas de Organización](#-políticas-de-organización) | 62-fin | Estándares para scripts de análisis |

---

## 🔧 Scripts Disponibles

### 📊 Análisis de Estructura

| Script | Propósito | Estado |
|--------|-----------|--------|
| `root_cleanup_analysis.py` | Análisis de archivos en raíz del proyecto | ✅ Activo |
| `utils_cleanup_analysis.py` | Análisis de utilidades y dependencias | ✅ Activo |

### 🎯 Funcionalidades Principales

#### ✅ `root_cleanup_analysis.py`
- **Función**: Analiza archivos mal ubicados en la raíz del proyecto
- **Salida**: Listado de archivos con sugerencias de reubicación
- **Uso**: Identificación de archivos fuera de lugar

#### ✅ `utils_cleanup_analysis.py`
- **Función**: Analiza estructura de utilidades y dependencias
- **Salida**: Reporte de archivos redundantes o mal organizados
- **Uso**: Limpieza de archivos de soporte

---

## 🚀 Uso y Ejecución

### 📝 Comandos Básicos

```bash
# Ejecutar análisis de raíz
python scripts/analysis/root_cleanup_analysis.py

# Ejecutar análisis de utilidades
python scripts/analysis/utils_cleanup_analysis.py

# Ejecutar todos los análisis
python scripts/analysis/root_cleanup_analysis.py && python scripts/analysis/utils_cleanup_analysis.py
```

### 🔧 Configuración

- **Directorio de trabajo**: Ejecutar desde raíz del proyecto
- **Dependencias**: Requiere Python 3.10+
- **Salida**: Reportes en consola y archivos de log

---

## 📁 Políticas de Organización

### 📝 Nomenclatura de Scripts de Análisis

**Formato**: `[TIPO]_[OBJETIVO]_analysis.py`

**Tipos permitidos**:
- `root_` - Análisis de archivos en raíz
- `utils_` - Análisis de utilidades
- `code_` - Análisis de código fuente
- `structure_` - Análisis de estructura
- `performance_` - Análisis de rendimiento

### 🎯 Criterios de Creación

#### ✅ Cuándo Crear un Script de Análisis
- **Análisis repetitivo** necesario para mantenimiento
- **Validación de estructura** después de cambios grandes
- **Depuración de problemas** específicos del proyecto
- **Auditoría de código** o archivos

#### ✅ Estructura de Script Estándar
```python
#!/usr/bin/env python3
"""
Descripción del análisis que realiza el script.
"""

def main():
    """Función principal del análisis."""
    # Lógica del análisis
    pass

if __name__ == "__main__":
    main()
```

### 📊 Ejemplos de Nomenclatura

#### ✅ Correcto
```
root_cleanup_analysis.py        # Análisis de limpieza de raíz
utils_dependency_analysis.py    # Análisis de dependencias de utils
code_quality_analysis.py        # Análisis de calidad de código
structure_validation_analysis.py # Validación de estructura
```

#### ❌ Incorrecto
```
analysis.py                     # Muy genérico
cleanup.py                      # Falta tipo y objetivo
root_analysis_script.py         # Redundante 'script'
analisis_utils.py              # Inconsistente (español/inglés)
```

### 🔄 Flujo de Trabajo

1. **Identificar necesidad** de análisis
2. **Crear script** siguiendo nomenclatura estándar
3. **Documentar propósito** en docstring
4. **Probar ejecución** desde raíz del proyecto
5. **Actualizar este README** con nuevo script

---

**📖 Documentación relacionada**: [`scripts/README.md`](../README.md) • [`docs/analysis/README.md`](../../docs/analysis/README.md)
