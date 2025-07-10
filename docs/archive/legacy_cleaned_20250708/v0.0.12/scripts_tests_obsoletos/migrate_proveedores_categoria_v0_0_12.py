# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
import sqlite3
import os
import logging

#!/usr/bin/env python3
"""
Script de migración para agregar categorías a proveedores
Versión: v0.0.12
Fecha: 19 de junio de 2025

CAMBIOS:
- Agregar columna categoria TEXT a tabla proveedores
- Establecer categoría por defecto "General" para proveedores existentes
- Mantener compatibilidad con datos existentes
"""


# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_db_path() -> str:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Obtener la ruta de la base de datos"""
    current_dir = os.path.dirname(__file__)
    _ = os.path.join(current_dir, 'hefest.db')
    
    if not os.path.exists(db_path):
        logger.error("No se encontró la base de datos en: %s", db_path)
        raise FileNotFoundError(f"Base de datos no encontrada: {db_path}")
    
    return db_path

def backup_database() -> bool:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Crear respaldo de la base de datos"""
    try:
        db_path = get_db_path()
        _ = db_path.replace('.db', '_backup_categoria_proveedores_v0.0.12.db')
        
        with open(db_path, 'rb') as original:
            with open(backup_path, 'wb') as backup:
                backup.write(original.read())
        
        logger.info("Respaldo creado exitosamente: %s", backup_path)
        return True
        
    except Exception as e:
        logger.error("Error creando respaldo: %s", e)
        return False

def check_table_structure() -> dict:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Verificar la estructura actual de la tabla proveedores"""
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        _ = conn.cursor()
        
        # Verificar si la tabla proveedores existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='proveedores'")
        _ = cursor.fetchone() is not None
        
        # Verificar columnas existentes
        _ = []
        if table_exists:
            cursor.execute("PRAGMA table_info(proveedores)")
            _ = [column[1] for column in cursor.fetchall()]
        
        # Verificar si ya existe la columna categoria
        _ = 'categoria' in columns
        
        # Contar proveedores existentes
        _ = 0
        if table_exists:
            cursor.execute("SELECT COUNT(*) FROM proveedores")
            _ = cursor.fetchone()[0]
        
        conn.close()
        
        _ = {
            'table_exists': table_exists,
            'columns': columns,
            'categoria_exists': categoria_exists,
            'proveedor_count': proveedor_count
        }
        
        logger.info("Estructura actual: %s", result)
        return result
        
    except Exception as e:
        logger.error("Error verificando estructura: %s", e)
        return {}

def migrate_proveedores_table() -> bool:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Migrar la tabla proveedores para incluir categorías"""
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        _ = conn.cursor()
        
        # Verificar estructura actual
        _ = check_table_structure()
        
        if not structure.get('table_exists'):
            logger.error("La tabla proveedores no existe")
            return False
        
        if structure.get('categoria_exists'):
            logger.info("La columna categoria ya existe en la tabla proveedores")
            return True
        
        # Agregar columna categoria
        logger.info("Agregando columna categoria a tabla proveedores...")
        cursor.execute("ALTER TABLE proveedores ADD COLUMN categoria TEXT DEFAULT 'General'")
        
        # Actualizar proveedores existentes con categoría por defecto
        proveedor_count = structure.get('proveedor_count', 0)
        if proveedor_count > 0:
            logger.info("Actualizando %s proveedores existentes con categoría 'General'...", proveedor_count)
            cursor.execute("UPDATE proveedores SET categoria = 'General' WHERE categoria IS NULL")
            updated_rows = cursor.rowcount
            logger.info("Actualizados %s proveedores con categoría por defecto", updated_rows)
        
        # Verificar la migración
        cursor.execute("PRAGMA table_info(proveedores)")
        _ = [column[1] for column in cursor.fetchall()]
        
        if 'categoria' in columns_after:
            logger.info("✅ Migración completada exitosamente")
            
            # Mostrar estructura final
            cursor.execute("SELECT COUNT(*) FROM proveedores WHERE categoria IS NOT NULL")
            categorized_count = cursor.fetchone()[0]
            logger.info("Proveedores con categoría asignada: %s", categorized_count)
            
            conn.commit()
            conn.close()
            return True
        else:
            logger.error("❌ Error en la migración: columna categoria no encontrada después de la migración")
            conn.rollback()
            conn.close()
            return False
            
    except Exception as e:
        logger.error("Error en migración: %s", e)
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def verify_migration() -> bool:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Verificar que la migración se completó correctamente"""
    try:
        _ = check_table_structure()
        
        if not structure.get('categoria_exists'):
            logger.error("❌ Verificación fallida: columna categoria no encontrada")
            return False
        
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        _ = conn.cursor()
        
        # Verificar que todos los proveedores tienen categoría
        cursor.execute("SELECT COUNT(*) FROM proveedores WHERE categoria IS NULL OR categoria = ''")
        _ = cursor.fetchone()[0]
        
        if null_count > 0:
            logger.warning("⚠️ %s proveedores sin categoría asignada", null_count)
        
        # Mostrar resumen de categorías
        cursor.execute("SELECT categoria, COUNT(*) FROM proveedores GROUP BY categoria")
        _ = cursor.fetchall()
        
        logger.info("📊 Resumen de categorías de proveedores:")
        for categoria, count in categories:
            logger.info("  - {categoria}: %s proveedores", count)
        
        conn.close()
        
        logger.info("✅ Verificación completada exitosamente")
        return True
        
    except Exception as e:
        logger.error("Error en verificación: %s", e)
        return False

def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Función principal de migración"""
    logger.info("🚀 Iniciando migración de categorías para proveedores...")
    
    try:
        # 1. Crear respaldo
        logger.info("1. Creando respaldo de la base de datos...")
        if not backup_database():
            logger.error("❌ Error creando respaldo. Abortando migración.")
            return False
        
        # 2. Verificar estructura actual
        logger.info("2. Verificando estructura actual...")
        structure = check_table_structure()
        if not structure:
            logger.error("❌ Error verificando estructura. Abortando migración.")
            return False
        
        # 3. Realizar migración
        logger.info("3. Ejecutando migración...")
        if not migrate_proveedores_table():
            logger.error("❌ Error en migración. Abortando.")
            return False
        
        # 4. Verificar migración
        logger.info("4. Verificando migración...")
        if not verify_migration():
            logger.error("❌ Error en verificación. Revisar manualmente.")
            return False
        
        logger.info("🎉 Migración completada exitosamente!")
        logger.info("✅ La tabla proveedores ahora incluye soporte para categorías")
        
        return True
        
    except Exception as e:
        logger.error("❌ Error fatal en migración: %s", e)
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ MIGRACIÓN EXITOSA")
        print("Los proveedores ahora soportan categorías (Bebidas, Comida, Postres, etc.)")
    else:
        print("\n❌ MIGRACIÓN FALLIDA")
        print("Revisar los logs para más detalles")
