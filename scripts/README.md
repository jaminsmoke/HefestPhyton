# 🛠️ Scripts y Herramientas - Sistema Hefest

Scripts de instalación, empaquetado, automatización y utilidades para el desarrollo y distribución del proyecto Hefest.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [📦 Scripts Disponibles](#-scripts-disponibles) | 18-42 | Lista de scripts y su propósito |
| [🚀 Instalación y Empaquetado](#-instalación-y-empaquetado) | 44-75 | Proceso de build y distribución |
| [🔧 Herramientas de Desarrollo](#-herramientas-de-desarrollo) | 77-95 | Scripts para desarrollo y QA |
| [📁 Políticas de Scripts](#-políticas-de-scripts) | 97-fin | **Políticas de creación y mantenimiento** |

---

## 📦 Scripts Disponibles

### �️ Scripts de Build y Distribución

| Script | Propósito | Uso |
|--------|-----------|-----|
| `build_exe.py` | Generar ejecutable con PyInstaller | `python scripts/build_exe.py` |
| `installer.py` | Crear instalador de sistema | `python scripts/installer.py` |
| `release.py` | Automatizar proceso de release | `python scripts/release.py` |
| `auto_release.py` | Release automático con GitHub | `python scripts/auto_release.py` |

### 🔧 Scripts de Desarrollo

| Script | Propósito | Uso |
|--------|-----------|-----|
| `quality_analysis.py` | Análisis de calidad de código | `python scripts/quality_analysis.py` |
| `create_version_backup_professional.ps1` | Backup versionado | `.\scripts\create_version_backup_professional.ps1` |

### 📊 Scripts de Migración

| Script | Propósito | Ubicación |
|--------|-----------|-----------|
| Migración de archivos | Scripts de migración específicos | `scripts/migration/` |

### 🔍 Scripts de Análisis

| Script | Propósito | Ubicación |
|--------|-----------|-----------|
| Análisis de estructura | Scripts de análisis y depuración | `scripts/analysis/` |

### 🧪 Scripts de Testing Manual

| Script | Propósito | Ubicación |
|--------|-----------|-----------|
| Testing manual | Scripts para testing y validación manual | `scripts/testing/` |

### 🎭 Scripts de Demos

| Script | Propósito | Ubicación |
|--------|-----------|-----------|
| `demo_v3_arquitectura.py` | Demostración de arquitectura V3 | `scripts/demos/` |

---

## 🚀 Instalación y Empaquetado

### 📦 Instalación como Paquete Python

#### ✅ Instalación Básica
```bash
# Desde código fuente
pip install -e .

# Con dependencias de desarrollo  
pip install -e .[dev]

# Con herramientas de build
pip install -e .[build]

# Instalación completa
pip install -e .[all]
```

#### ✅ Verificar Instalación
```bash
# Ejecutar aplicación
python main.py

# Ejecutar tests
python -m pytest tests/ -v

# Verificar importaciones
python -c "from src.main import main; print('✅ Instalación correcta')"
```

### � Generar Ejecutable (.exe)

#### ✅ Opción 1: PyInstaller (Recomendado)
```bash
# Ejecutable básico
python scripts/build_exe.py

# Ejecutable único (un solo archivo)
python scripts/build_exe.py --onefile

# Sin ventana de consola
python scripts/build_exe.py --windowed

# Build completo limpio
python scripts/build_exe.py --clean --onefile --windowed
```

#### ✅ Requisitos del Sistema
- **Python**: 3.10 o superior
- **PyQt6**: >= 6.5.0
- **Memoria**: 2GB RAM mínimo
- **Espacio**: 500MB disponible
- **PyInstaller**: >= 5.10.0 (para .exe)

---

## 🔧 Herramientas de Desarrollo

### 📊 Análisis de Calidad
```bash
# Ejecutar análisis completo de código
python scripts/quality_analysis.py

# Genera reportes de:
# - Complejidad ciclomática
# - Cobertura de tests  
# - Análisis estático de código
# - Métricas de mantenibilidad
```

### 💾 Sistema de Backup
```powershell
# Crear backup versionado (PowerShell)
.\scripts\create_version_backup_professional.ps1

# Genera backup comprimido con:
# - Timestamp automático
# - Exclusión de archivos temporales
# - Verificación de integridad
```

### 🚀 Release Automático
```bash
# Proceso de release manual
python scripts/release.py

# Release automático con GitHub Actions
python scripts/auto_release.py

# Incluye:
# - Actualización de versión
# - Generación de changelog
# - Build de ejecutable
# - Upload a GitHub Releases
```

---

## 📁 Políticas de Scripts

> **🎯 IMPORTANTE**: Todos los scripts deben seguir estándares de calidad, documentación y mantenibilidad establecidos.

### 📝 Nomenclatura de Scripts

#### ✅ Formato Estándar
```
[proposito]_[funcionalidad].py
```

**Ejemplos válidos**:
- `build_exe.py` (build + ejecutable)
- `quality_analysis.py` (análisis + calidad)
- `auto_release.py` (automatización + release)
- `installer.py` (instalación)

#### ✅ Para Scripts PowerShell
```
[proposito]_[funcionalidad]_[tipo].ps1
```

**Ejemplos válidos**:
- `create_version_backup_professional.ps1`
- `deploy_production_automated.ps1`

### 🔧 Estructura de Script Requerida

#### ✅ Template para Scripts Python
```python
#!/usr/bin/env python3
"""
[NOMBRE DEL SCRIPT] - [PROPÓSITO]

Descripción detallada del script y su funcionalidad.

Uso:
    python scripts/[nombre_script].py [argumentos]

Ejemplos:
    python scripts/build_exe.py --onefile
    python scripts/quality_analysis.py --full

Requisitos:
    - Python 3.10+
    - [Lista de dependencias]

Autor: [Nombre]
Fecha: [Fecha de creación]
Versión: [Versión del script]
"""

import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

# Configuración del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

def main():
    """Función principal del script"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    print(f"🚀 Iniciando {__file__.split('/')[-1]}: {datetime.now()}")
    
    try:
        execute_script_logic(args)
        print("✅ Script completado exitosamente")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def create_argument_parser():
    """Crear parser de argumentos"""
    parser = argparse.ArgumentParser(description=__doc__)
    # Agregar argumentos específicos
    return parser

def execute_script_logic(args):
    """Lógica principal del script"""
    pass

if __name__ == "__main__":
    main()
```

### � Políticas de Contenido

#### ✅ INCLUIR SIEMPRE
- **Docstring detallado** con propósito y uso
- **Manejo de errores** robusto
- **Logging** de progreso y errores
- **Argumentos de línea de comandos** cuando sea apropiado
- **Validación de requisitos** del sistema
- **Documentación de dependencias**
- **Ejemplos de uso** concretos

#### ✅ CARACTERÍSTICAS REQUERIDAS
- **Idempotencia**: El script debe ser seguro de ejecutar múltiples veces
- **Reversibilidad**: Operaciones críticas deben tener rollback
- **Validación**: Verificar precondiciones antes de ejecutar
- **Reporting**: Mostrar progreso y resultados claramente
- **Error handling**: Fallos controlados con mensajes útiles

#### ❌ EVITAR
- Scripts sin documentación
- Hardcodeo de rutas absolutas
- Operaciones destructivas sin confirmación
- Scripts que no validan dependencias
- Código duplicado entre scripts

### � Proceso de Creación

#### Al Crear un Nuevo Script:
1. **Determinar propósito** específico y único
2. **Seguir nomenclatura** estándar
3. **Usar template** correspondiente (Python/PowerShell)
4. **Documentar uso** con ejemplos
5. **Probar** en diferentes entornos
6. **Actualizar este README** con el nuevo script

#### Control de Calidad:
- [ ] Script tiene docstring completo
- [ ] Maneja errores apropiadamente
- [ ] Valida precondiciones
- [ ] Muestra progreso claramente
- [ ] Es idempotente
- [ ] Documentado en este README

### 🗂️ Organización de Scripts

#### 📂 Estructura por Categoría
```
scripts/
├── README.md                   # 🎯 ESTE ARCHIVO
├── build_exe.py               # 🏗️ BUILD - Generar ejecutable
├── installer.py               # 📦 INSTALACIÓN - Crear instalador
├── release.py                 # 🚀 RELEASE - Automatizar releases
├── auto_release.py            # 🤖 AUTO RELEASE - GitHub Actions
├── quality_analysis.py        # 📊 CALIDAD - Análisis de código
├── create_version_backup_professional.ps1  # 💾 BACKUP
├── analysis/                  # 🔍 ANÁLISIS
│   ├── README.md             # 📖 Documentación de análisis
│   ├── root_cleanup_analysis.py
│   └── utils_cleanup_analysis.py
├── testing/                   # 🧪 TESTING MANUAL
│   └── README.md             # 📖 Documentación de testing
├── demos/                     # 🎭 DEMOSTRACIONES
│   ├── README.md             # 📖 Documentación de demos
│   └── demo_v3_arquitectura.py
└── migration/                 # 🔄 MIGRACIÓN
    ├── README.md
    └── [scripts de migración]
```

#### 📋 Criterios de Ubicación
- **Scripts de build**: Directamente en `scripts/`
- **Scripts de migración**: En `scripts/migration/`
- **Scripts de análisis**: En `scripts/analysis/`
- **Scripts de testing manual**: En `scripts/testing/`
- **Scripts de demos**: En `scripts/demos/`
- **Scripts de deployment**: En `scripts/deployment/` (si existen)
- **Scripts de utilidades**: En `scripts/utils/` (si existen)

### 📊 Mantenimiento y Evolución

#### Revisión Periódica:
- **Mensual**: Verificar que scripts funcionan correctamente
- **Por release**: Actualizar scripts de build si es necesario
- **Trimestral**: Revisar y optimizar scripts complejos

#### Integración con CI/CD:
- Scripts deben ser ejecutables en pipelines automáticos
- Documentar dependencias del sistema operativo
- Mantener compatibilidad con diferentes versiones de Python

#### Versionado de Scripts:
- Scripts críticos deben tener número de versión
- Cambios significativos requieren actualización de documentación
- Mantener compatibilidad hacia atrás cuando sea posible

---

**� Para crear un nuevo script**: Sigue el [template correspondiente](#-estructura-de-script-requerida) y las [políticas de contenido](#-políticas-de-contenido) según el tipo de script que desarrolles.
