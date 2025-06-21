# 🔄 Scripts de Migración - Sistema Hefest

Scripts especializados para procesos de migración de datos, estructura de base de datos y transiciones del sistema Hefest.

---

## 📋 Índice de Contenidos

| Sección | Líneas | Descripción |
|---------|--------|-------------|
| [🛠️ Scripts Disponibles](#%EF%B8%8F-scripts-disponibles) | 18-35 | Lista de scripts de migración y su propósito |
| [📊 Proceso de Migración](#-proceso-de-migración) | 37-55 | Metodología y fases de migración |
| [🔧 Uso y Configuración](#-uso-y-configuración) | 57-75 | Instrucciones de ejecución y parámetros |
| [📁 Políticas de Scripts de Migración](#-políticas-de-scripts-de-migración) | 77-fin | **Políticas de creación y mantenimiento** |

---

## 🛠️ Scripts Disponibles

### 📦 Scripts de Migración de Datos

| Script | Propósito | Estado |
|--------|-----------|--------|
| `migrar_a_datos_reales.py` | Migración desde datos simulados a datos reales | ✅ Funcional |

### 🎯 Funcionalidades del Script Principal

#### ✅ `migrar_a_datos_reales.py`
- **Verificación de estructura**: Valida tablas requeridas
- **Creación de esquema**: Crea tablas faltantes con esquema correcto
- **Población inicial**: Pobla con datos básicos operativos
- **Configuración de defaults**: Establece valores por defecto apropiados
- **Validación de integridad**: Verifica datos después de migración

#### 📊 Datos que Puebla
```python
# Productos básicos operativos
productos = [
    {"nombre": "Coca Cola", "categoria": "Bebidas", "precio": 2.50, "stock": 20},
    {"nombre": "Agua Mineral", "categoria": "Bebidas", "precio": 1.50, "stock": 30},
    {"nombre": "Café", "categoria": "Bebidas", "precio": 4.50, "stock": 10},
    {"nombre": "Pan Tostado", "categoria": "Desayuno", "precio": 3.00, "stock": 15}
]

# Habitaciones de hotel operativas
habitaciones = [
    {"numero": 101, "tipo": "Individual", "precio_noche": 50.00, "estado": "disponible"},
    {"numero": 102, "tipo": "Doble", "precio_noche": 75.00, "estado": "disponible"},
    {"numero": 201, "tipo": "Suite", "precio_noche": 120.00, "estado": "disponible"}
]
```

---

## 📊 Proceso de Migración

### 🔄 Metodología de Migración Estándar

#### Fase 1: Verificación Pre-Migración
- **Backup**: Crear respaldo de datos existentes
- **Estructura**: Verificar tablas y esquemas requeridos
- **Dependencias**: Validar conexiones y permisos
- **Tests**: Ejecutar tests pre-migración

#### Fase 2: Ejecución de Migración
- **Crear estructura**: Generar tablas faltantes
- **Migrar datos**: Transferir/transformar información
- **Configurar defaults**: Establecer valores iniciales
- **Validar integridad**: Verificar consistencia

#### Fase 3: Verificación Post-Migración
- **Tests de integridad**: Validar datos migrados
- **Tests funcionales**: Verificar operatividad del sistema
- **Performance**: Evaluar rendimiento post-migración
- **Rollback plan**: Documentar proceso de reversión

---

## 🔧 Uso y Configuración

### 🚀 Ejecución Básica
```bash
# Migración completa estándar
python scripts/migration/migrar_a_datos_reales.py

# Modo verbose con detalles
python scripts/migration/migrar_a_datos_reales.py --verbose

# Modo dry-run (simular sin ejecutar)
python scripts/migration/migrar_a_datos_reales.py --dry-run

# Backup automático antes de migración
python scripts/migration/migrar_a_datos_reales.py --backup
```

### ⚙️ Opciones de Configuración
- `--verbose`: Mostrar detalles del proceso
- `--dry-run`: Simular migración sin ejecutar cambios
- `--backup`: Crear backup automático antes de migrar
- `--force`: Forzar migración aunque existan datos
- `--validate-only`: Solo validar estructura sin migrar

---

## 📁 Políticas de Scripts de Migración

> **🎯 IMPORTANTE**: Los scripts de migración son **críticos para el sistema**. Deben seguir estándares estrictos de calidad y seguridad.

### 📝 Nomenclatura de Scripts

#### ✅ Formato Estándar
```
migrar_[origen]_a_[destino].py
```

**Ejemplos válidos**:
- `migrar_simulados_a_reales.py`
- `migrar_v1_a_v2_esquema.py`
- `migrar_sqlite_a_postgresql.py`

#### ✅ Para Scripts Específicos
```
[operacion]_[componente]_migration.py
```

**Ejemplos válidos**:
- `update_schema_migration.py`
- `data_cleanup_migration.py`
- `index_optimization_migration.py`

### 🔧 Estructura de Script Requerida

#### ✅ Template Obligatorio
```python
#!/usr/bin/env python3
"""
Migración: [ORIGEN] → [DESTINO]

Descripción: [Qué hace esta migración]
Versión: [Versión aplicable]
Fecha: [Fecha de creación]
Autor: [Responsable]

IMPORTANTE: 
- Este script modifica datos del sistema
- Crear backup antes de ejecutar
- Validar en entorno de pruebas primero

Uso:
    python scripts/migration/[nombre_script].py [opciones]
"""

import sys
import os
import sqlite3
import argparse
from datetime import datetime
from pathlib import Path

# Configuración
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "hefest.db"
BACKUP_DIR = PROJECT_ROOT / "backups"

def main():
    """Función principal de migración"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    print(f"🔄 Iniciando migración: {datetime.now()}")
    
    try:
        # Validaciones pre-migración
        validate_preconditions()
        
        # Backup si se solicita
        if args.backup:
            create_backup()
        
        # Ejecutar migración
        if not args.dry_run:
            execute_migration()
        else:
            simulate_migration()
            
        # Validaciones post-migración
        validate_results()
        
        print("✅ Migración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error en migración: {e}")
        rollback_if_needed()
        sys.exit(1)

def validate_preconditions():
    """Validar condiciones antes de migrar"""
    pass

def create_backup():
    """Crear backup de seguridad"""
    pass

def execute_migration():
    """Ejecutar la migración real"""
    pass

def simulate_migration():
    """Simular migración sin cambios"""
    pass

def validate_results():
    """Validar resultados post-migración"""
    pass

def rollback_if_needed():
    """Proceso de rollback en caso de error"""
    pass

if __name__ == "__main__":
    main()
```

### 📍 Políticas de Seguridad

#### ✅ REQUISITOS OBLIGATORIOS
- **Backup automático**: Opción para crear backup antes de migrar
- **Dry-run mode**: Simulación sin cambios reales
- **Validación previa**: Verificar precondiciones antes de ejecutar
- **Validación posterior**: Verificar resultados después de migrar
- **Rollback plan**: Proceso documentado de reversión
- **Logging detallado**: Registro completo de todas las operaciones
- **Error handling**: Manejo robusto de errores y excepciones

#### ✅ VALIDACIONES REQUERIDAS
- **Estructura de BD**: Verificar tablas y esquemas
- **Permisos de acceso**: Validar permisos de lectura/escritura
- **Espacio disponible**: Verificar espacio en disco suficiente
- **Dependencias**: Validar librerías y conexiones necesarias
- **Estado del sistema**: Verificar que no haya procesos activos

#### ❌ PROHIBIDO
- Scripts sin backup automático
- Modificaciones destructivas sin confirmación
- Scripts sin dry-run mode
- Hardcodeo de rutas absolutas
- Scripts sin manejo de errores
- Operaciones sin logging

### 🔄 Proceso de Desarrollo

#### Al Crear un Script de Migración:
1. **Definir objetivo** específico de la migración
2. **Analizar impacto** en datos y sistema
3. **Usar template** obligatorio
4. **Implementar validaciones** pre y post
5. **Probar en entorno** de desarrollo
6. **Documentar rollback** plan
7. **Actualizar este README**

#### Control de Calidad:
- [ ] Script tiene dry-run mode
- [ ] Implementa backup automático
- [ ] Valida precondiciones
- [ ] Maneja errores apropiadamente
- [ ] Tiene proceso de rollback
- [ ] Está documentado completamente
- [ ] Probado en entorno de pruebas

### 📊 Trazabilidad y Auditoría

#### Documentación Requerida:
- **Objetivo**: Qué problema resuelve la migración
- **Impacto**: Qué datos/estructura se modifica
- **Proceso**: Pasos específicos de la migración
- **Rollback**: Cómo revertir si es necesario
- **Tests**: Cómo validar que funcionó correctamente

#### Integración con Documentación:
- Scripts documentados en `docs/development/migration/`
- Resultados documentados en `docs/changelog/`
- Análisis previos en `docs/analysis/`

---

**📖 Para crear un script de migración**: Sigue el [template obligatorio](#-template-obligatorio) y las [políticas de seguridad](#-políticas-de-seguridad) para garantizar operaciones seguras.

-- Verifica columnas requeridas
PRAGMA table_info(productos);
PRAGMA table_info(habitaciones);
PRAGMA table_info(comandas);
```

### Fase 2: Creación de Tablas Faltantes
```sql
-- Si no existe tabla productos
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    stock_minimo INTEGER NOT NULL DEFAULT 0,
    activo BOOLEAN NOT NULL DEFAULT 1,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Si no existe tabla habitaciones  
CREATE TABLE IF NOT EXISTS habitaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,
    tipo TEXT NOT NULL,
    precio_noche REAL NOT NULL,
    estado TEXT NOT NULL DEFAULT 'disponible',
    capacidad INTEGER NOT NULL DEFAULT 2,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Fase 3: Población con Datos Iniciales
- Inserta productos básicos si la tabla está vacía
- Crea habitaciones de ejemplo si no existen
- Establece configuración inicial del sistema
- Valida integridad referencial

### Fase 4: Validación
- Cuenta registros insertados
- Verifica restricciones de integridad
- Prueba consultas básicas de métricas
- Confirma que DataManager puede obtener datos reales

## Configuración de Valores por Defecto

### Campos Obligatorios → 0
```python
metrics = {
    'ventas': 0.0,              # Hasta que haya ventas reales
    'ocupacion': 0.0,           # Hasta que haya reservas
    'tiempo_servicio': 0.0,     # Hasta que haya órdenes
    'ticket_promedio': 0.0,     # Hasta que haya transacciones
    'ordenes_activas': 0        # Contador desde 0
}
```

### Campos Opcionales → None/Vacío
```python
optional_fields = {
    'fecha_ultima_venta': None,     # Hasta primera venta
    'proveedor_contacto': None,     # Hasta asignar proveedor
    'observaciones': '',            # Campo texto opcional
    'descuento_aplicado': None      # Hasta configurar descuentos
}
```

## Estados Post-Migración

### ✅ Sistema Listo para Datos Reales
- DataManager conectado a BD real
- Servicios obtienen datos de BD (no cache)
- Métricas reflejan estado real del negocio
- UI muestra valores reales (0 inicialmente)

### 🔄 Próximos Pasos Post-Migración
1. **Añadir productos reales** del negocio
2. **Configurar habitaciones reales** del hotel
3. **Registrar primeras ventas** para ver métricas
4. **Crear usuarios del sistema** con roles apropiados

## Rollback y Recuperación

### Backup Automático
El script crea backup automático antes de la migración:
```
data/backups/backup_pre_migration_YYYYMMDD_HHMMSS.db
```

### Restaurar Backup
```bash
# Restaurar desde backup
cp data/backups/backup_pre_migration_*.db data/hefest.db

# Verificar restauración
python -c "from data.db_manager import DatabaseManager; db = DatabaseManager(); print(db.query('SELECT COUNT(*) FROM productos'))"
```

## Monitoreo Post-Migración

### Verificar Estado del Sistema
```bash
# Ejecutar demo para verificar datos reales
python scripts/demo_v3_arquitectura.py

# Ejecutar tests para verificar integridad
python -m tests.test_suite unit

# Verificar métricas en dashboard
python main.py  # Abrir dashboard y verificar métricas
```

### Logs de Migración
Los logs se guardan en `logs/migration_YYYYMMDD.log` con:
- Timestamp de cada operación
- Registros insertados/actualizados
- Errores encontrados y soluciones
- Tiempo total de migración

## Troubleshooting

### Error: "Tabla no existe"
```bash
# Verificar estructura de BD
python -c "from data.db_manager import DatabaseManager; db = DatabaseManager(); print([r[0] for r in db.query('SELECT name FROM sqlite_master WHERE type=\'table\'')])"
```

### Error: "Datos duplicados"
```bash
# Limpiar datos duplicados
python -c "from data.db_manager import DatabaseManager; db = DatabaseManager(); db.execute('DELETE FROM productos WHERE id NOT IN (SELECT MIN(id) FROM productos GROUP BY nombre)')"
```

### Métricas no aparecen
```bash
# Verificar conexión DataManager
python -c "from src.utils.data_manager import DataManager; dm = DataManager(); print(dm.get_current_data())"
```

---

**Estado**: ✅ MIGRACIÓN COMPLETADA  
**Fecha**: 13 de Junio de 2025  
**Registros Insertados**: ~15 productos, ~10 habitaciones  
**Validación**: DataManager funcionando con datos reales  
