# Archivo de Utilidades Archivadas

Este directorio contiene archivos de utilidades que han sido archivados por diversos motivos.

## Archivos Archivados

### advanced_config.py (múltiples versiones)
- **Fecha de archivo**: 2025-06-14
- **Razón**: Problemas graves de indentación y duplicidad funcional
- **Alternativa actual**: `application_config_manager.py`
- **Estado**: No funcional - errores de sintaxis
- **Descripción**: Intento de implementar configuración avanzada con encriptación y validación de esquemas

#### Versiones archivadas:
- `advanced_config.py` - Versión más reciente con errores de indentación
- `advanced_config.py.backup` - Backup creado durante refactorización  
- `advanced_config.py.problematic` - Versión marcada como problemática

#### Funcionalidad reemplazada por:
- **Configuración básica**: `application_config_manager.py`
- **Configuración avanzada**: Por implementar en futuras versiones

## Notas para Desarrolladores

Si necesitas características avanzadas de configuración (encriptación, validación de esquemas, hot-reload), considera:

1. **Refactorizar** `advanced_config.py` desde cero con indentación correcta
2. **Integrar** las características avanzadas en `application_config_manager.py`
3. **Crear** un nuevo módulo de configuración avanzada

## Uso Actual del Sistema

El sistema utiliza actualmente:
- `application_config_manager.py` - Configuración principal
- `ConfigManager` - Clase de configuración estándar

No hay referencias activas a `advanced_config.py` en el código base.
