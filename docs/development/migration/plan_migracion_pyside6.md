# Plan de Migración de PyQt6 a PySide6

## 1. Resumen Ejecutivo

Este documento detalla el plan para migrar la aplicación Hefest de PyQt6 a PySide6, con el objetivo de resolver problemas de linting, mejorar la compatibilidad y beneficiarse de una licencia más flexible.

**Tiempo estimado**: 2-3 semanas  
**Impacto en producción**: Bajo (con enfoque incremental)  
**Recursos necesarios**: 1-2 desarrolladores

## 2. Justificación

### Problemas Actuales con PyQt6
- Errores y advertencias frecuentes en herramientas de linting
- Problemas de compatibilidad con algunas herramientas de desarrollo
- Restricciones de licencia (GPL)

### Beneficios Esperados de PySide6
- Licencia LGPL más flexible
- Mejor integración con herramientas de desarrollo
- Mantenimiento oficial por Qt Company
- Menos problemas de linting y advertencias

## 3. Análisis de Impacto

### Componentes Afectados
- Todos los módulos UI (`src/ui/`)
- Filtros de mensajes Qt (`main.py`)
- Scripts de prueba que utilizan PyQt

### Compatibilidad
PySide6 y PyQt6 son ~95% compatibles. Principales diferencias:
- Sintaxis de señales/slots
- Algunos nombres de métodos
- Manejo de QVariant

## 4. Fases de Migración

### Fase 1: Preparación y Análisis (3-5 días)

#### 1.1 Inventario de Componentes
```python
# Script para identificar todos los archivos que usan PyQt6
import os

def find_pyqt_files(root_dir):
    pyqt_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'PyQt6' in content:
                        pyqt_files.append(path)
    return pyqt_files

# Uso: find_pyqt_files('src')
```

#### 1.2 Entorno de Prueba
- Crear rama `feature/pyside6-migration`
- Configurar entorno virtual para pruebas

#### 1.3 Instalación de Dependencias
```bash
pip uninstall PyQt6 PyQt6-Qt6 PyQt6-sip
pip install PySide6
```

### Fase 2: Migración de Código Base (5-7 días)

#### 2.1 Script de Migración Automática

```python
import os
import re

def migrate_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar imports
    content = re.sub(r'from PyQt6', 'from PySide6', content)
    content = re.sub(r'import PyQt6', 'import PySide6', content)
    
    # Ajustar sintaxis de señales
    content = re.sub(r'\.connect\((.*?)\)  # type: ignore', r'.connect(\1)', content)
    
    # Ajustar QMessageLogContext
    content = re.sub(r'QtMsgType, QMessageLogContext', 
                    r'QtMsgType, QtMessageLogContext', content)
    
    # Guardar cambios
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Migrado: {file_path}")

def migrate_directory(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                migrate_file(os.path.join(root, file))

# Uso: migrate_directory('src')
```

#### 2.2 Orden de Migración
1. Utilidades y componentes base (`src/utils/`)
2. Componentes UI simples (`src/ui/components/`)
3. Ventanas y diálogos (`src/ui/windows/`)
4. Módulos principales (`src/ui/modules/`)
5. Launcher principal (`main.py`)

#### 2.3 Ajustes Manuales Necesarios

| Componente PyQt6 | Ajuste para PySide6 |
|------------------|---------------------|
| `QDialog.DialogCode.Accepted` | `QDialog.Accepted` |
| `QMessageBox.Icon.Critical` | `QMessageBox.Critical` |
| `Qt.AlignmentFlag.AlignRight` | `Qt.AlignRight` |
| `QtCore.Signal` | `QtCore.Signal` (sin cambios) |
| `QtCore.Slot` | `QtCore.Slot` (sin cambios) |

### Fase 3: Pruebas y Correcciones (7-10 días)

#### 3.1 Pruebas Unitarias
- Ejecutar pruebas existentes
- Crear pruebas específicas para componentes UI

#### 3.2 Pruebas de Integración
- Verificar interacción entre componentes
- Probar flujos de trabajo completos

#### 3.3 Pruebas de Rendimiento
- Comparar tiempos de carga
- Verificar uso de memoria

#### 3.4 Corrección de Problemas
- Resolver incompatibilidades encontradas
- Ajustar tipos y anotaciones

### Fase 4: Finalización y Documentación (3-5 días)

#### 4.1 Actualización de Documentación
- Actualizar README.md
- Actualizar comentarios en código

#### 4.2 Actualización de Dependencias
- Actualizar `requirements.txt`
- Actualizar scripts de instalación

#### 4.3 Revisión Final
- Revisión de código
- Pruebas finales

#### 4.4 Despliegue
- Fusionar rama a `main`
- Crear nueva versión

## 5. Riesgos y Mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Incompatibilidades no detectadas | Media | Alto | Pruebas exhaustivas, enfoque incremental |
| Problemas de rendimiento | Baja | Medio | Benchmarks comparativos |
| Regresiones en UI | Media | Alto | Pruebas visuales, capturas de pantalla |
| Tiempo de migración mayor al estimado | Media | Medio | Priorizar componentes críticos |

## 6. Script de Verificación Post-Migración

```python
def verify_migration():
    """Verifica que no queden referencias a PyQt6 en el código."""
    import os
    
    pyqt_references = []
    
    for root, _, files in os.walk('src'):
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'PyQt6' in content:
                        pyqt_references.append(path)
    
    if pyqt_references:
        print("⚠️ Se encontraron referencias a PyQt6 en:")
        for path in pyqt_references:
            print(f"  - {path}")
    else:
        print("✅ No se encontraron referencias a PyQt6")
```

## 7. Rollback Plan

En caso de problemas críticos:

1. Revertir a la rama anterior
2. Reinstalar PyQt6
3. Restaurar configuraciones específicas de PyQt6

## 8. Conclusión

La migración a PySide6 ofrece beneficios significativos en términos de licenciamiento, mantenibilidad y compatibilidad con herramientas de desarrollo. Con un enfoque incremental y pruebas exhaustivas, los riesgos pueden ser minimizados.

---

**Autor**: Equipo de Desarrollo Hefest  
**Fecha**: Enero 2025  
**Versión**: 1.0