# PLAN DE LIMPIEZA Y ORGANIZACIÓN - HEFEST

## ARCHIVOS IDENTIFICADOS PARA LIMPIEZA

### 🗑️ RAÍZ - Archivos Obsoletos/Temporales:
- `debug_auth.py` - Script de debugging temporal ❌
- `debug_dashboard_direct.py` - Script de debugging temporal ❌
- `debug_permissions.py` - Script de debugging temporal ❌
- `test_auth_flow.py` - Test temporal fuera de carpeta tests/ ❌
- `test_dashboard_complete.py` - Test temporal fuera de carpeta tests/ ❌
- `test_login_fix.py` - Test temporal fuera de carpeta tests/ ❌
- `DASHBOARD_ACCESS_RESOLUTION.md` - Documentación temporal ❌
- `SOLUCION_PERMISOS_DASHBOARD.md` - Documentación temporal ❌

### 🗑️ SRC/UTILS - Archivos No Utilizados:
- `dashboard_data_manager.py` - Datos simulados, NO usado ❌
- `hospitality_data_manager.py` - Datos simulados, NO usado ❌  
- `real_data_manager_clean.py` - Backup obsoleto, NO usado ❌

### 📁 ARCHIVOS A MOVER/ORGANIZAR:

#### Tests temporales → tests/unit/
- Mover tests de la raíz a su ubicación correcta

#### Documentación temporal → docs/archive/
- Crear carpeta archive para documentos temporales/resueltos

#### Scripts de diagnóstico → scripts/analysis/
- Organizar scripts de análisis y diagnóstico

## ACCIONES A EJECUTAR:

### 1. LIMPIEZA DE RAÍZ
- ✅ Eliminar archivos de debug temporales
- ✅ Eliminar tests fuera de lugar
- ✅ Archivar documentación temporal

### 2. LIMPIEZA DE SRC/UTILS  
- ✅ Eliminar data managers no utilizados
- ✅ Limpiar archivos de backup obsoletos

### 3. ORGANIZACIÓN DE ESTRUCTURA
- ✅ Crear carpetas de archivo cuando sea necesario
- ✅ Mover archivos a ubicaciones correctas
- ✅ Actualizar README's

### 4. VERIFICACIÓN POST-LIMPIEZA
- ✅ Verificar que el sistema sigue funcionando
- ✅ Actualizar documentación
- ✅ Commit de limpieza

---

**INICIO DE EJECUCIÓN...**
