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
        self.db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'hefest.db')
        self.db_path = os.path.abspath(self.db_path)
        self.conn = None
        
    def connect(self):
        """Conectar a la base de datos"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return True
        except Exception as e:
            print(f"❌ Error conectando: {e}")
            return False
    
    def analyze_data_type(self):
        """Analizar si los datos son reales o de fábrica"""
        print("🔍 ANÁLISIS DE TIPO DE DATOS")
        print("=" * 50)
        
        cursor = self.conn.cursor()
        
        # 1. Usuarios
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN nombre LIKE '%admin%' OR nombre LIKE '%test%' OR nombre LIKE '%demo%' THEN 1 END) as factory FROM usuarios")
        users_data = cursor.fetchone()
        
        # 2. Productos
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN precio = 0 OR precio IS NULL THEN 1 END) as zero_price FROM productos")
        products_data = cursor.fetchone()
        
        # 3. Categorias
        cursor.execute("SELECT COUNT(*) as total FROM categorias")
        categories_data = cursor.fetchone()
        
        # 4. Proveedores
        cursor.execute("SELECT COUNT(*) as total FROM proveedores")
        suppliers_data = cursor.fetchone()
        
        # Mostrar análisis
        print(f"👥 USUARIOS: {users_data['total']} total")
        print(f"   • Factory/Demo: {users_data['factory']} ({(users_data['factory']/max(users_data['total'],1)*100):.1f}%)")
        print(f"   • Tipo: {'🏭 FACTORY DATA' if users_data['factory'] >= users_data['total']/2 else '👤 DATOS REALES'}")
        
        print(f"\n📦 PRODUCTOS: {products_data['total']} total")
        if products_data['total'] > 0:
            print(f"   • Precio cero/nulo: {products_data['zero_price']} ({(products_data['zero_price']/products_data['total']*100):.1f}%)")
            print(f"   • Tipo: {'🏭 FACTORY DATA' if products_data['zero_price'] >= products_data['total']/2 else '💰 DATOS REALES'}")
        else:
            print("   • Estado: ⚠️ VACÍO - NECESITA DATOS")
        
        print(f"\n🏷️ CATEGORÍAS: {categories_data['total']} total")
        print(f"   • Estado: {'⚠️ VACÍO' if categories_data['total'] == 0 else '✅ CON DATOS'}")
        
        print(f"\n🚚 PROVEEDORES: {suppliers_data['total']} total")
        print(f"   • Estado: {'⚠️ VACÍO' if suppliers_data['total'] == 0 else '✅ CON DATOS'}")
        
        return {
            'usuarios': users_data,
            'productos': products_data,
            'categorias': categories_data,
            'proveedores': suppliers_data
        }
    
    def check_inventory_structure(self):
        """Verificar estructura de tablas de inventario"""
        print("\n🗂️ ESTRUCTURA TABLAS INVENTARIO")
        print("=" * 50)
        
        cursor = self.conn.cursor()
        
        inventory_tables = ['productos', 'categorias', 'proveedores', 'movimientos_stock']
        
        for table in inventory_tables:
            try:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                
                print(f"\n📋 Tabla '{table}':")
                if columns:
                    for col in columns:
                        nullable = "NULL" if col['notnull'] == 0 else "NOT NULL"
                        default = f" DEFAULT {col['dflt_value']}" if col['dflt_value'] else ""
                        print(f"   • {col['name']} ({col['type']}) {nullable}{default}")
                else:
                    print("   ❌ Tabla no encontrada")
            except Exception as e:
                print(f"   ❌ Error: {e}")

def main():
    print("🔍 ANÁLISIS COMPLETO - BASE DE DATOS HEFEST")
    print("=" * 60)
    print(f"📅 Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    analyzer = HefestDataAnalyzer()
    
    if not analyzer.connect():
        return
    
    try:
        # 1. Análisis de tipo de datos
        data_analysis = analyzer.analyze_data_type()
        
        # 2. Verificar estructura
        analyzer.check_inventory_structure()
        
        # Resumen final
        print("\n🎯 RESUMEN EJECUTIVO")
        print("=" * 30)
        
        empty_tables = []
        if data_analysis['productos']['total'] == 0:
            empty_tables.append('productos')
        if data_analysis['categorias']['total'] == 0:
            empty_tables.append('categorias')
        if data_analysis['proveedores']['total'] == 0:
            empty_tables.append('proveedores')
        
        if empty_tables:
            print(f"⚠️  Tablas vacías: {', '.join(empty_tables)}")
            print("📋 Recomendación: Poblar con datos de fábrica")
        else:
            print("✅ Todas las tablas tienen datos")
        
    except Exception as e:
        print(f"❌ Error durante análisis: {e}")
    finally:
        if analyzer.conn:
            analyzer.conn.close()

if __name__ == "__main__":
    main()
