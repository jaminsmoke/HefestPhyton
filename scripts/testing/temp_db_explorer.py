#!/usr/bin/env python3
"""
Script temporal para explorar la estructura de la base de datos Hefest
"""

import sqlite3
import os

def explore_database():
    """Explorar la estructura de la base de datos"""
    db_path = 'data/hefest.db'
    
    if not os.path.exists(db_path):
        print(f"❌ No se encontró la base de datos en: {db_path}")
        return
    
    print(f"🔍 Explorando base de datos: {db_path}")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Obtener todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\n📋 TABLAS EN LA BASE DE DATOS:")
        print("-" * 30)
        for table in tables:
            print(f"• {table[0]}")
        
        # Examinar estructura de cada tabla
        print("\n📊 ESTRUCTURA DETALLADA DE CADA TABLA:")
        print("=" * 60)
        
        for table in tables:
            table_name = table[0]
            print(f"\n🗂️  TABLA: {table_name}")
            print("-" * 40)
            
            # Obtener información de columnas
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            print("Columnas:")
            for col in columns:
                pk_info = " [PRIMARY KEY]" if col[5] else ""
                null_info = " [NOT NULL]" if col[3] else " [NULL]"
                default_info = f" DEFAULT({col[4]})" if col[4] else ""
                print(f"  - {col[1]}: {col[2]}{pk_info}{null_info}{default_info}")
            
            # Obtener conteo de registros
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"📈 Registros: {count}")
            
            # Mostrar algunos datos de ejemplo si hay registros
            if count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_data = cursor.fetchall()
                print("🔍 Datos de ejemplo:")
                for i, row in enumerate(sample_data, 1):
                    print(f"    {i}: {row}")
        
        # Examinar tablas específicas del inventario
        print("\n🎯 ANÁLISIS ESPECÍFICO - TABLAS DE INVENTARIO:")
        print("=" * 60)
        
        inventory_tables = ['categorias', 'productos', 'proveedores']
        for table_name in inventory_tables:
            if any(t[0] == table_name for t in tables):
                print(f"\n📦 {table_name.upper()}:")
                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()
                print(f"   Total registros: {len(data)}")
                if data:
                    print("   Primeros registros:")
                    for i, row in enumerate(data[:5], 1):
                        print(f"     {i}: {row}")
            else:
                print(f"⚠️  Tabla '{table_name}' no encontrada")
        
        conn.close()
        print(f"\n✅ Exploración completada exitosamente")
        
    except Exception as e:
        print(f"❌ Error explorando la base de datos: {e}")

if __name__ == "__main__":
    explore_database()
