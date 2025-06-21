# 🎨 Assets y Recursos - Sistema Hefest

Recursos visuales, gráficos y multimedia del proyecto Hefest incluyendo iconos, imágenes, estilos y fuentes.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🗂️ Estructura de Assets](#%EF%B8%8F-estructura-de-assets) | 18-35 | Organización de recursos por tipo |
| [🚀 Uso e Integración](#-uso-e-integración) | 37-50 | Cómo se incluyen los assets en el proyecto |
| [📸 Estado de Recursos](#-estado-de-recursos) | 52-fin | Recursos disponibles y pendientes |

---

## �️ Estructura de Assets

### � Organización por Tipo de Recurso

```
assets/
├── README.md                   # 🎯 ESTE ARCHIVO
├── images/                     # 🖼️ Imágenes y capturas
│   ├── hefest_logo.png        # Logo principal del proyecto
│   ├── dashboard_preview.png  # Captura del dashboard principal
│   ├── login_screen.png       # Captura de pantalla de login
│   └── modules_overview.png   # Vista general de módulos
├── icons/                      # 🎨 Iconos de aplicación
│   ├── hefest.ico             # Icono principal para Windows
│   ├── app_icon.png           # Icono multi-tamaño
│   └── [módulo_icons]/        # Iconos por módulo
├── styles/                     # 🎨 Hojas de estilo
│   ├── modern_theme.qss       # Tema principal Qt
│   ├── animations.css         # Animaciones CSS
│   └── [temas_adicionales]/   # Otros temas
└── fonts/                      # 📝 Tipografías
    ├── corporate_fonts/       # Fuentes corporativas
    └── ui_fonts/             # Fuentes de interfaz
```

### � Propósito de los Assets

- 🎨 **Identidad visual**: Logo y elementos gráficos corporativos
- 🖼️ **Documentación**: Capturas y diagramas explicativos  
- 🎯 **Interfaz de usuario**: Iconos y elementos visuales de la UI
- 🎨 **Tematización**: Estilos y personalizaciones visuales
- 📝 **Tipografías**: Fuentes para consistencia visual

---

## 🚀 Uso e Integración

### 📦 Integración en Build

Los assets se incluyen automáticamente mediante:

```python
# MANIFEST.in - Para distribución pip
include assets/**/*
recursive-include assets *

# pyproject.toml - Configuración setuptools
[tool.setuptools.package-data]
"*" = ["assets/**/*"]

# scripts/build_exe.py - Para ejecutables PyInstaller  
datas = [('assets', 'assets')]
```

### � Referencias en Código

```python
# Acceso a assets desde el código
from pathlib import Path

ASSETS_DIR = Path(__file__).parent.parent / "assets"
LOGO_PATH = ASSETS_DIR / "images" / "hefest_logo.png"
ICON_PATH = ASSETS_DIR / "icons" / "hefest.ico"
```

---

## 📸 Estado de Recursos

### ✅ Recursos Disponibles

| Tipo | Archivo | Estado | Descripción |
|------|---------|--------|-------------|
| 📁 Estructuras | `README.md` | ✅ Disponible | Documentación de assets |
| 🎨 Estilos | `styles/modern_theme.qss` | ✅ Disponible | Tema principal Qt |
| 🎨 Estilos | `styles/animations.css` | ✅ Disponible | Animaciones CSS |

### 📸 Recursos Pendientes

| Tipo | Archivo | Prioridad | Uso |
|------|---------|-----------|-----|
| 🖼️ Logo | `images/hefest_logo.png` | Alta | README principal |
| 📱 Captura | `images/dashboard_preview.png` | Alta | Documentación |
| 📱 Captura | `images/login_screen.png` | Media | Documentación |
| 📱 Captura | `images/modules_overview.png` | Media | Documentación |
| 🎯 Icono | `icons/hefest.ico` | Alta | Ejecutables Windows |
| 🎯 Icono | `icons/app_icon.png` | Media | Aplicación multiplataforma |

### 📝 Fuentes y Tipografías

| Categoría | Estado | Descripción |
|-----------|--------|-------------|
| 📝 Corporativas | ⏳ Pendiente | Fuentes de marca corporativa |
| 📝 UI | ⏳ Pendiente | Fuentes de interfaz de usuario |

### 🎨 Temas y Estilos

| Tema | Estado | Descripción |
|------|--------|-------------|
| 🌟 Moderno | ✅ Disponible | Tema principal actual |
| 🌙 Oscuro | ⏳ Pendiente | Tema oscuro alternativo |
| 🏢 Corporativo | ⏳ Pendiente | Tema empresarial |

---

**📖 Para añadir nuevos assets**: Coloca los archivos en la subcarpeta correspondiente según su tipo y actualiza la documentación relevante.
