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

import sqlite3
import os
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def get_db_path() -> str:
    """Obtener la ruta de la base de datos"""
    current_dir = os.path.dirname(__file__)
    db_path = os.path.join(current_dir, 'hefest.db')
    
    if not os.path.exists(db_path):
        logger.error(f"No se encontró la base de datos en: {db_path}")
        raise FileNotFoundError(f"Base de datos no encontrada: {db_path}")
    
    return db_path

def backup_database() -> bool:
    """Crear respaldo de la base de datos"""
    try:
        db_path = get_db_path()
        backup_path = db_path.replace('.db', '_backup_categoria_proveedores_v0.0.12.db')
        
        with open(db_path, 'rb') as original:
            with open(backup_path, 'wb') as backup:
                backup.write(original.read())
        
        logger.info(f"Respaldo creado exitosamente: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error creando respaldo: {e}")
        return False

def check_table_structure() -> dict:
    """Verificar la estructura actual de la tabla proveedores"""
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si la tabla proveedores existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='proveedores'")
        table_exists = cursor.fetchone() is not None
        
        # Verificar columnas existentes
        columns = []
        if table_exists:
            cursor.execute("PRAGMA table_info(proveedores)")
            columns = [column[1] for column in cursor.fetchall()]
        
        # Verificar si ya existe la columna categoria
        categoria_exists = 'categoria' in columns
        
        # Contar proveedores existentes
        proveedor_count = 0
        if table_exists:
            cursor.execute("SELECT COUNT(*) FROM proveedores")
            proveedor_count = cursor.fetchone()[0]
        
        conn.close()
        
        result = {
            'table_exists': table_exists,
            'columns': columns,
            'categoria_exists': categoria_exists,
            'proveedor_count': proveedor_count
        }
        
        logger.info(f"Estructura actual: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error verificando estructura: {e}")
        return {}

def migrate_proveedores_table() -> bool:
    """Migrar la tabla proveedores para incluir categorías"""
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estructura actual
        structure = check_table_structure()
        
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
            logger.info(f"Actualizando {proveedor_count} proveedores existentes con categoría 'General'...")
            cursor.execute("UPDATE proveedores SET categoria = 'General' WHERE categoria IS NULL")
            updated_rows = cursor.rowcount
            logger.info(f"Actualizados {updated_rows} proveedores con categoría por defecto")
        
        # Verificar la migración
        cursor.execute("PRAGMA table_info(proveedores)")
        columns_after = [column[1] for column in cursor.fetchall()]
        
        if 'categoria' in columns_after:
            logger.info("✅ Migración completada exitosamente")
            
            # Mostrar estructura final
            cursor.execute("SELECT COUNT(*) FROM proveedores WHERE categoria IS NOT NULL")
            categorized_count = cursor.fetchone()[0]
            logger.info(f"Proveedores con categoría asignada: {categorized_count}")
            
            conn.commit()
            conn.close()
            return True
        else:
            logger.error("❌ Error en la migración: columna categoria no encontrada después de la migración")
            conn.rollback()
            conn.close()
            return False
            
    except Exception as e:
        logger.error(f"Error en migración: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

def verify_migration() -> bool:
    """Verificar que la migración se completó correctamente"""
    try:
        structure = check_table_structure()
        
        if not structure.get('categoria_exists'):
            logger.error("❌ Verificación fallida: columna categoria no encontrada")
            return False
        
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar que todos los proveedores tienen categoría
        cursor.execute("SELECT COUNT(*) FROM proveedores WHERE categoria IS NULL OR categoria = ''")
        null_count = cursor.fetchone()[0]
        
        if null_count > 0:
            logger.warning(f"⚠️ {null_count} proveedores sin categoría asignada")
        
        # Mostrar resumen de categorías
        cursor.execute("SELECT categoria, COUNT(*) FROM proveedores GROUP BY categoria")
        categories = cursor.fetchall()
        
        logger.info("📊 Resumen de categorías de proveedores:")
        for categoria, count in categories:
            logger.info(f"  - {categoria}: {count} proveedores")
        
        conn.close()
        
        logger.info("✅ Verificación completada exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"Error en verificación: {e}")
        return False

def main():
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
        logger.error(f"❌ Error fatal en migración: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✅ MIGRACIÓN EXITOSA")
        print("Los proveedores ahora soportan categorías (Bebidas, Comida, Postres, etc.)")
    else:
        print("\n❌ MIGRACIÓN FALLIDA")
        print("Revisar los logs para más detalles")
