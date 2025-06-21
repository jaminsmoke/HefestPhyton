# ⚙️ Configuraciones del Sistema - Hefest

Archivos de configuración por entorno para el sistema Hefest, incluyendo configuraciones de base de datos, UI, logging y servicios.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [📁 Archivos de Configuración](#-archivos-de-configuración) | 18-35 | Configuraciones por entorno |
| [🔧 Uso de Configuraciones](#-uso-de-configuraciones) | 37-55 | Carga y aplicación de config |
| [📁 Políticas de Organización](#-políticas-de-organización) | 57-fin | Estándares para configuración |

---

## 📁 Archivos de Configuración

### 🎯 Configuraciones por Entorno

| Archivo | Entorno | Propósito | Estado |
|---------|---------|-----------|--------|
| `default.json` | Base | Configuración por defecto | ✅ Activo |
| `development.json` | Desarrollo | Configuración para desarrollo | ✅ Activo |
| `production.json` | Producción | Configuración para producción | ✅ Activo |

### 📊 Estructura de Configuración

#### ✅ Categorías Principales
- **Database**: Configuración de base de datos
- **UI**: Configuraciones de interfaz de usuario
- **Logging**: Niveles y configuración de logs
- **Services**: Configuración de servicios del sistema
- **Performance**: Configuraciones de rendimiento

---

## 🔧 Uso de Configuraciones

### 📦 Carga Automática

```python
# El sistema carga configuraciones automáticamente
from src.utils.config import load_config, get_setting

# Cargar configuración por entorno
config = load_config('config/default.json')

# Obtener configuración específica
db_host = get_setting('database.host', default='localhost')
ui_theme = get_setting('ui.theme', default='modern')
```

### 🎯 Jerarquía de Configuración

1. **`default.json`** - Configuración base y valores por defecto
2. **`development.json`** - Sobrescribe defaults para desarrollo
3. **`production.json`** - Sobrescribe defaults para producción

### 🔧 Variables de Entorno

```bash
# Establecer entorno (opcional)
export HEFEST_ENV=development    # Linux/Mac
set HEFEST_ENV=development       # Windows

# El sistema usa default.json si no se especifica entorno
```

---

## 📁 Políticas de Organización

### 📝 Nomenclatura de Configuraciones

**Formato**: `[ENTORNO].json`

**Entornos permitidos**:
- `default.json` - Configuración base (obligatorio)
- `development.json` - Desarrollo local
- `production.json` - Producción/despliegue
- `testing.json` - Tests automáticos (opcional)

### 🎯 Estructura JSON Estándar

#### ✅ Formato Recomendado
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "name": "hefest_db",
    "type": "sqlite"
  },
  "ui": {
    "theme": "modern",
    "language": "es",
    "window_size": {
      "width": 1200,
      "height": 800
    }
  },
  "logging": {
    "level": "INFO",
    "file": "logs/hefest.log",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  },
  "services": {
    "auth": {
      "timeout": 30,
      "max_attempts": 3
    },
    "inventory": {
      "auto_refresh": true,
      "refresh_interval": 300
    }
  }
}
```

### 🔒 Seguridad y Mejores Prácticas

#### ✅ Información Sensible
- **NO incluir** contraseñas o tokens en archivos de configuración
- **Usar variables de entorno** para datos sensibles
- **Documentar** qué variables de entorno son necesarias

#### ✅ Validación de Configuración
- **Validar estructura** JSON al cargar
- **Proveer defaults** para todas las configuraciones
- **Documentar** valores requeridos vs opcionales

### 🔄 Flujo de Trabajo

1. **Modificar `default.json`** para cambios base
2. **Sobrescribir en archivos específicos** solo lo necesario  
3. **Probar configuración** en entorno de desarrollo
4. **Validar en producción** antes de desplegar
5. **Documentar cambios** significativos

### 📊 Ejemplo de Jerarquía

```json
// default.json
{
  "database": {"host": "localhost"},
  "ui": {"theme": "modern"}
}

// development.json  
{
  "database": {"host": "dev.database.local"},
  "logging": {"level": "DEBUG"}
}

// Resultado final en desarrollo:
{
  "database": {"host": "dev.database.local"},  // Sobrescrito
  "ui": {"theme": "modern"},                   // Heredado
  "logging": {"level": "DEBUG"}                // Añadido
}
```

---

**📖 Documentación relacionada**: [`src/utils/README.md`](../src/utils/README.md) • [`README.md`](../README.md)
