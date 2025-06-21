#!/usr/bin/env python3
"""
Script de migración para actualizar la estructura de la tabla productos
Versión: v0.0.12
Fecha: 18 de junio de 2025

CAMBIOS:
- Agregar columna proveedor_id INTEGER
- Agregar columna proveedor_nombre TEXT
- Migrar datos de la columna proveedor existente
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
    return os.path.join(os.path.dirname(__file__), 'hefest.db')

def backup_database() -> bool:
    """Crear respaldo de la base de datos"""
    try:
        db_path = get_db_path()
        backup_path = db_path.replace('.db', '_backup_v0.0.12.db')
        
        # Copiar la base de datos
        import shutil
        shutil.copy2(db_path, backup_path)
        
        logger.info(f"✅ Respaldo creado: {backup_path}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creando respaldo: {e}")
        return False

def check_table_structure() -> dict:
    """Verificar la estructura actual de la tabla productos"""
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener información de columnas
        cursor.execute("PRAGMA table_info(productos)")
        columns = cursor.fetchall()
        
        # Obtener SQL de creación
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='productos'")
        table_sql = cursor.fetchone()
        
        conn.close()
        
        column_names = [col[1] for col in columns]
        
        return {
            'columns': column_names,
            'sql': table_sql[0] if table_sql else None,
            'has_proveedor_id': 'proveedor_id' in column_names,
            'has_proveedor_nombre': 'proveedor_nombre' in column_names,
            'has_proveedor': 'proveedor' in column_names
        }
        
    except Exception as e:
        logger.error(f"❌ Error verificando estructura: {e}")
        return {}

def migrate_productos_table() -> bool:
    """Migrar la tabla productos a la nueva estructura"""
    try:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estructura actual
        structure = check_table_structure()
        logger.info(f"📋 Estructura actual - Columnas: {structure.get('columns', [])}")
        
        # Si ya tiene las columnas nuevas, no hacer nada
        if structure.get('has_proveedor_id') and structure.get('has_proveedor_nombre'):
            logger.info("✅ La tabla ya tiene la estructura correcta")
            conn.close()
            return True
        
        # Agregar columnas si no existen
        if not structure.get('has_proveedor_id'):
            logger.info("➕ Agregando columna proveedor_id...")
            cursor.execute("ALTER TABLE productos ADD COLUMN proveedor_id INTEGER")
        
        if not structure.get('has_proveedor_nombre'):
            logger.info("➕ Agregando columna proveedor_nombre...")
            cursor.execute("ALTER TABLE productos ADD COLUMN proveedor_nombre TEXT")
        
        # Migrar datos de la columna proveedor existente
        if structure.get('has_proveedor'):
            logger.info("🔄 Migrando datos de la columna proveedor...")
            
            # Obtener productos con proveedor
            cursor.execute("SELECT id, proveedor FROM productos WHERE proveedor IS NOT NULL AND proveedor != ''")
            productos_con_proveedor = cursor.fetchall()
            
            # Crear mapeo de proveedores
            proveedores_map = {}
            proveedor_id = 1
            
            for producto_id, proveedor_nombre in productos_con_proveedor:
                if proveedor_nombre not in proveedores_map:
                    proveedores_map[proveedor_nombre] = proveedor_id
                    proveedor_id += 1
                
                # Actualizar producto
                cursor.execute("""
                    UPDATE productos 
                    SET proveedor_id = ?, proveedor_nombre = ? 
                    WHERE id = ?
                """, (proveedores_map[proveedor_nombre], proveedor_nombre, producto_id))
            
            logger.info(f"✅ Migrados {len(productos_con_proveedor)} productos con {len(proveedores_map)} proveedores únicos")
        
        conn.commit()
        conn.close()
        
        logger.info("✅ Migración completada exitosamente")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en migración: {e}")
        return False

def verify_migration() -> bool:
    """Verificar que la migración fue exitosa"""
    try:
        structure = check_table_structure()
        
        required_columns = ['id', 'nombre', 'precio', 'stock', 'categoria', 'stock_actual', 'stock_minimo', 'proveedor_id', 'proveedor_nombre']
        actual_columns = structure.get('columns', [])
        
        missing_columns = [col for col in required_columns if col not in actual_columns]
        
        if missing_columns:
            logger.error(f"❌ Faltan columnas: {missing_columns}")
            return False
        
        logger.info("✅ Verificación exitosa - Todas las columnas requeridas están presentes")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error en verificación: {e}")
        return False

def main():
    """Función principal de migración"""
    logger.info("🚀 Iniciando migración de base de datos v0.0.12")
    
    # Paso 1: Crear respaldo
    logger.info("📁 Paso 1: Creando respaldo...")
    if not backup_database():
        logger.error("❌ No se pudo crear el respaldo. Abortando migración.")
        return False
    
    # Paso 2: Verificar estructura actual
    logger.info("🔍 Paso 2: Verificando estructura atual...")
    structure = check_table_structure()
    if not structure:
        logger.error("❌ No se pudo verificar la estructura. Abortando migración.")
        return False
    
    # Paso 3: Ejecutar migración
    logger.info("🔄 Paso 3: Ejecutando migración...")
    if not migrate_productos_table():
        logger.error("❌ Migración fallida. Restaurar desde respaldo si es necesario.")
        return False
    
    # Paso 4: Verificar migración
    logger.info("✅ Paso 4: Verificando migración...")
    if not verify_migration():
        logger.error("❌ Verificación fallida. Revisar estructura de la tabla.")
        return False
    
    logger.info("🎉 Migración completada exitosamente!")
    logger.info("💡 Tip: El respaldo está disponible en hefest_backup_v0.0.12.db")
    return True

if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
