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

class HefestDataAnalyzer:    def __init__(self):
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
        
        # Análisis por tabla
        tables_analysis = {}
        
        # 1. Usuarios
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN nombre LIKE '%admin%' OR nombre LIKE '%test%' OR nombre LIKE '%demo%' THEN 1 END) as factory FROM usuarios")
        users_data = cursor.fetchone()
        
        # 2. Productos
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN precio = 0 OR precio IS NULL THEN 1 END) as zero_price FROM productos")
        products_data = cursor.fetchone()
        
        # 3. Habitaciones
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN precio_base = 0 OR precio_base IS NULL THEN 1 END) as zero_price FROM habitaciones")
        rooms_data = cursor.fetchone()
        
        # 4. Reservas
        cursor.execute("SELECT COUNT(*) as total FROM reservas")
        reservations_data = cursor.fetchone()
        
        # 5. Categorias
        cursor.execute("SELECT COUNT(*) as total FROM categorias")
        categories_data = cursor.fetchone()
        
        # 6. Proveedores
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
        
        print(f"\n🏨 HABITACIONES: {rooms_data['total']} total")
        if rooms_data['total'] > 0:
            print(f"   • Precio cero/nulo: {rooms_data['zero_price']} ({(rooms_data['zero_price']/rooms_data['total']*100):.1f}%)")
            print(f"   • Tipo: {'🏭 FACTORY DATA' if rooms_data['zero_price'] >= rooms_data['total']/2 else '💰 DATOS REALES'}")
        else:
            print("   • Estado: ⚠️ VACÍO - NECESITA DATOS")
        
        print(f"\n📅 RESERVAS: {reservations_data['total']} total")
        print(f"   • Estado: {'⚠️ VACÍO' if reservations_data['total'] == 0 else '✅ CON DATOS'}")
        
        print(f"\n🏷️ CATEGORÍAS: {categories_data['total']} total")
        print(f"   • Estado: {'⚠️ VACÍO' if categories_data['total'] == 0 else '✅ CON DATOS'}")
        
        print(f"\n🚚 PROVEEDORES: {suppliers_data['total']} total")
        print(f"   • Estado: {'⚠️ VACÍO' if suppliers_data['total'] == 0 else '✅ CON DATOS'}")
        
        return {
            'usuarios': users_data,
            'productos': products_data,
            'habitaciones': rooms_data,
            'reservas': reservations_data,
            'categorias': categories_data,
            'proveedores': suppliers_data
        }
    
    def analyze_inventory_connections(self):
        """Analizar conexiones del módulo inventario"""
        print("\n🔗 ANÁLISIS DE CONEXIONES - MÓDULO INVENTARIO")
        print("=" * 60)
        
        cursor = self.conn.cursor()
        
        # Verificar integridad referencial
        print("📋 INTEGRIDAD REFERENCIAL:")
        print("-" * 30)
        
        # 1. Productos -> Categorías
        cursor.execute("""
            SELECT COUNT(*) as total_productos,
                   COUNT(CASE WHEN categoria IS NOT NULL AND categoria != '' THEN 1 END) as con_categoria,
                   COUNT(CASE WHEN p.categoria = c.nombre THEN 1 END) as categoria_valida
            FROM productos p
            LEFT JOIN categorias c ON p.categoria = c.nombre
        """)
        product_cat = cursor.fetchone()
        
        print(f"📦 Productos ↔ Categorías:")
        if product_cat['total_productos'] > 0:
            print(f"   • Total productos: {product_cat['total_productos']}")
            print(f"   • Con categoría: {product_cat['con_categoria']}")
            print(f"   • Categoría válida: {product_cat['categoria_valida']}")
            print(f"   • Integridad: {(product_cat['categoria_valida']/product_cat['total_productos']*100):.1f}%")
        else:
            print("   • ⚠️ No hay productos para verificar")
        
        # 2. Movimientos stock -> Productos
        cursor.execute("""
            SELECT COUNT(*) as total_movimientos,
                   COUNT(CASE WHEN p.id IS NOT NULL THEN 1 END) as producto_valido
            FROM movimientos_stock ms
            LEFT JOIN productos p ON ms.producto_id = p.id
        """)
        stock_prod = cursor.fetchone()
        
        print(f"\n📊 Movimientos Stock ↔ Productos:")
        if stock_prod['total_movimientos'] > 0:
            print(f"   • Total movimientos: {stock_prod['total_movimientos']}")
            print(f"   • Producto válido: {stock_prod['producto_valido']}")
            print(f"   • Integridad: {(stock_prod['producto_valido']/stock_prod['total_movimientos']*100):.1f}%")
        else:
            print("   • ⚠️ No hay movimientos de stock")
        
        # 3. Verificar estructura de tablas inventario
        print(f"\n🗂️ ESTRUCTURA TABLAS INVENTARIO:")
        print("-" * 35)
        
        inventory_tables = ['productos', 'categorias', 'proveedores', 'movimientos_stock']
        
        for table in inventory_tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            print(f"\n📋 Tabla '{table}':")
            for col in columns:
                nullable = "NULL" if col['notnull'] == 0 else "NOT NULL"
                default = f" DEFAULT {col['dflt_value']}" if col['dflt_value'] else ""
                print(f"   • {col['name']} ({col['type']}) {nullable}{default}")
    
    def suggest_factory_data(self):
        """Sugerir datos de fábrica para testing"""
        print("\n🏭 SUGERENCIAS DE DATOS DE FÁBRICA")
        print("=" * 50)
        
        suggestions = {
            'categorias': [
                "('Bebidas', 'Refrescos, zumos, agua')",
                "('Alimentación', 'Comida y snacks')",
                "('Limpieza', 'Productos de limpieza')",
                "('Amenities', 'Artículos de cortesía')",
                "('Textil', 'Ropa de cama y toallas')"
            ],
            'proveedores': [
                "('PROVEEDOR DEMO 1', 'demo1@test.com', '000-000-001', 'Calle Demo 1')",
                "('PROVEEDOR DEMO 2', 'demo2@test.com', '000-000-002', 'Calle Demo 2')",
                "('PROVEEDOR DEMO 3', 'demo3@test.com', '000-000-003', 'Calle Demo 3')"
            ],
            'productos': [
                "('Agua Mineral 500ml', 0.50, 0, 'Bebidas')",
                "('Toalla Baño', 15.00, 0, 'Textil')",
                "('Champú Demo', 3.00, 0, 'Amenities')",
                "('Detergente', 8.00, 0, 'Limpieza')",
                "('Sandwich Demo', 4.50, 0, 'Alimentación')"
            ]
        }
        
        for table, data_list in suggestions.items():
            print(f"\n📋 {table.upper()}:")
            print("-" * 20)
            for item in data_list:
                print(f"   • {item}")
    
    def check_inventory_module_compatibility(self):
        """Verificar compatibilidad con el módulo de inventario"""
        print("\n🔧 COMPATIBILIDAD MÓDULO INVENTARIO")
        print("=" * 50)
        
        cursor = self.conn.cursor()
        
        # Verificar campos esperados por el módulo
        expected_fields = {
            'productos': ['id', 'nombre', 'precio', 'stock', 'categoria'],
            'categorias': ['id', 'nombre'],
            'proveedores': ['id', 'nombre', 'email', 'telefono'],
            'movimientos_stock': ['id', 'producto_id', 'tipo', 'cantidad', 'fecha']
        }
        
        compatibility_score = 0
        total_checks = 0
        
        for table, fields in expected_fields.items():
            cursor.execute(f"PRAGMA table_info({table})")
            existing_columns = [col['name'] for col in cursor.fetchall()]
            
            print(f"\n📋 Tabla '{table}':")
            
            for field in fields:
                total_checks += 1
                if field in existing_columns:
                    print(f"   ✅ {field}")
                    compatibility_score += 1
                else:
                    print(f"   ❌ {field} - FALTANTE")
        
        compatibility_percent = (compatibility_score / total_checks * 100)
        
        print(f"\n📊 PUNTUACIÓN COMPATIBILIDAD:")
        print(f"   • Campos encontrados: {compatibility_score}/{total_checks}")
        print(f"   • Porcentaje: {compatibility_percent:.1f}%")
        
        if compatibility_percent >= 90:
            print("   • Estado: ✅ EXCELENTE COMPATIBILIDAD")
        elif compatibility_percent >= 70:
            print("   • Estado: ⚠️ BUENA COMPATIBILIDAD - Revisar campos faltantes")
        else:
            print("   • Estado: ❌ PROBLEMAS DE COMPATIBILIDAD - Requiere ajustes")
        
        return compatibility_percent

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
        
        # 2. Análisis de conexiones inventario
        analyzer.analyze_inventory_connections()
        
        # 3. Verificar compatibilidad módulo
        compatibility = analyzer.check_inventory_module_compatibility()
        
        # 4. Sugerir datos de fábrica
        analyzer.suggest_factory_data()
        
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
        
        print(f"🔧 Compatibilidad módulo: {compatibility:.1f}%")
        
        if compatibility >= 90:
            print("🎉 LISTO para implementar funcionalidades completas")
        else:
            print("⚠️  Revisar estructura antes de implementar")
        
    except Exception as e:
        print(f"❌ Error durante análisis: {e}")
    finally:
        if analyzer.conn:
            analyzer.conn.close()

if __name__ == "__main__":
    main()
