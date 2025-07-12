#!/usr/bin/env python3
"""
Script de depuración para verificar el problema de carga de categorías
"""

import sys
import sqlite3
from pathlib import Path

# Configurar la ruta del proyecto
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

def debug_categorias():
    """Depurar el problema de categorías"""
    
    print("=" * 60)
    print("🔍 DEPURACIÓN DE CATEGORÍAS")
    print("=" * 60)
    
    # 1. Conexión directa a la base de datos
    db_path = project_root / "data" / "hefest.db"
    print(f"📂 Base de datos: {db_path}")
    print(f"📊 Existe: {db_path.exists()}")
    
    if not db_path.exists():
        print("❌ Error: Base de datos no encontrada")
        return
    
    # 2. Verificar tabla categorias directamente
    print("\n🗄️ CONSULTA DIRECTA A LA BASE DE DATOS:")
    try:
        with sqlite3.connect(str(db_path)) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Verificar estructura de la tabla
            cursor.execute("PRAGMA table_info(categorias)")
            columns = cursor.fetchall()
            print(f"📋 Columnas en tabla categorias:")
            for col in columns:
                print(f"   - {col['name']} ({col['type']})")
            
            # Obtener todas las categorías
            cursor.execute("SELECT * FROM categorias")
            rows = cursor.fetchall()
            print(f"\n📊 Total de registros en categorias: {len(rows)}")
            
            for row in rows:
                print(f"   ID: {row['id']}, Nombre: {row['nombre']}, Activa: {row['activa']}")
                
            # Obtener solo las activas
            cursor.execute("SELECT * FROM categorias WHERE activa = 1")
            active_rows = cursor.fetchall()
            print(f"\n✅ Categorías activas: {len(active_rows)}")
            
    except Exception as e:
        print(f"❌ Error en consulta directa: {e}")
        return
    
    # 3. Solo prueba directa con SQLite por ahora
    print("\n✅ DEPURACIÓN COMPLETADA")
    print("=" * 60)

if __name__ == "__main__":
    debug_categorias()
