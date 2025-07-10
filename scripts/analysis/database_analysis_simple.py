from typing import Optional, Dict, List, Any
import logging
#!/usr/bin/env python3
"""
Análisis Completo de Base de Datos Hefest
========================================

Verifica si los datos son reales o de fábrica (factory data)
y analiza la integridad de las conexiones del módulo inventario.
"""

import sqlite3
import os
from datetime import datetime

class HefestDataAnalyzer:
    def __init__(self):
        """TODO: Add docstring"""
        self.db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'hefest.db')
        self.db_path = os.path.abspath(self.db_path)
        self.conn = None
        
    def connect(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Conectar a la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
    logging.error("❌ Error conectando: %s", e)
            return False
    
    def analyze_data_type(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Analizar si los datos son reales o de fábrica"""
        print("🔍 ANÁLISIS DE TIPO DE DATOS")
        print("=" * 50)
        
        _ = self.conn.cursor()
        
        # 1. Usuarios
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN nombre LIKE '%admin%' OR nombre LIKE '%test%' OR nombre LIKE '%demo%' THEN 1 END) as factory FROM usuarios")
        _ = cursor.fetchone()
        
        # 2. Productos
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN precio = 0 OR precio IS NULL THEN 1 END) as zero_price FROM productos")
        _ = cursor.fetchone()
        
        # 3. Categorias
        cursor.execute("SELECT COUNT(*) as total FROM categorias")
        _ = cursor.fetchone()
        
        # 4. Proveedores
        cursor.execute("SELECT COUNT(*) as total FROM proveedores")
        _ = cursor.fetchone()
        
        # Mostrar análisis
        print("👥 USUARIOS: %s total" % users_data['total'])
        print("   • Factory/Demo: {users_data['factory']} (%s%)" % (users_data['factory']/max(users_data['total'],1)*100):.1f)
        print("   • Tipo: %s" % '🏭 FACTORY DATA' if users_data['factory'] >= users_data['total']/2 else '👤 DATOS REALES')
        
        print("\n📦 PRODUCTOS: %s total" % products_data['total'])
        if products_data['total'] > 0:
            print("   • Precio cero/nulo: {products_data['zero_price']} (%s%)" % (products_data['zero_price']/products_data['total']*100):.1f)
            print("   • Tipo: %s" % '🏭 FACTORY DATA' if products_data['zero_price'] >= products_data['total']/2 else '💰 DATOS REALES')
        else:
            print("   • Estado: ⚠️ VACÍO - NECESITA DATOS")
        
        print("\n🏷️ CATEGORÍAS: %s total" % categories_data['total'])
        print("   • Estado: %s" % '⚠️ VACÍO' if categories_data['total'] == 0 else '✅ CON DATOS')
        
        print("\n🚚 PROVEEDORES: %s total" % suppliers_data['total'])
        print("   • Estado: %s" % '⚠️ VACÍO' if suppliers_data['total'] == 0 else '✅ CON DATOS')
        
        return {
            'usuarios': users_data,
            'productos': products_data,
            'categorias': categories_data,
            'proveedores': suppliers_data
        }
    
    def check_inventory_structure(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verificar estructura de tablas de inventario"""
        print("\n🗂️ ESTRUCTURA TABLAS INVENTARIO")
        print("=" * 50)
        
        _ = self.conn.cursor()
        
        inventory_tables = ['productos', 'categorias', 'proveedores', 'movimientos_stock']
        
        for table in inventory_tables:
            try:
                cursor.execute(f"PRAGMA table_info({table})")
                _ = cursor.fetchall()
                
                print("\n📋 Tabla '%s':" % table)
                if columns:
                    for col in columns:
                        nullable = "NULL" if col['notnull'] == 0 else "NOT NULL"
                        default = f" DEFAULT {col['dflt_value']}" if col['dflt_value'] else ""
                        print("   • {col['name']} ({col['type']}) {nullable}%s" % default)
                else:
                    print("   ❌ Tabla no encontrada")
            except Exception as e:
    logging.error("   ❌ Error: %s", e)

def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    print("🔍 ANÁLISIS COMPLETO - BASE DE DATOS HEFEST")
    print("=" * 60)
    print("📅 Fecha: %s" % datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    _ = HefestDataAnalyzer()
    
    if not analyzer.connect():
        return
    
    try:
        # 1. Análisis de tipo de datos
        _ = analyzer.analyze_data_type()
        
        # 2. Verificar estructura
        analyzer.check_inventory_structure()
        
        # Resumen final
        print("\n🎯 RESUMEN EJECUTIVO")
        print("=" * 30)
        
        _ = []
        if data_analysis['productos']['total'] == 0:
            empty_tables.append('productos')
        if data_analysis['categorias']['total'] == 0:
            empty_tables.append('categorias')
        if data_analysis['proveedores']['total'] == 0:
            empty_tables.append('proveedores')
        
        if empty_tables:
            print("⚠️  Tablas vacías: %s" % ', '.join(empty_tables))
            print("📋 Recomendación: Poblar con datos de fábrica")
        else:
            print("✅ Todas las tablas tienen datos")
        
    except Exception as e:
    logging.error("❌ Error durante análisis: %s", e)
    finally:
        if analyzer.conn:
            analyzer.conn.close()

if __name__ == "__main__":
    main()
