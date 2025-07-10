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

class HefestDataAnalyzer:    def __init__(self):
        # Usar path seguro para evitar path traversal
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(script_dir))
        self.db_path = os.path.join(project_root, 'data', 'hefest.db')
        
        # Validar que el path esté dentro del proyecto
        if not os.path.commonpath([project_root, self.db_path]) == project_root:
            raise ValueError("Invalid database path - security violation")
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
        
        # Análisis por tabla
        _ = {}
        
        # 1. Usuarios
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN nombre LIKE '%admin%' OR nombre LIKE '%test%' OR nombre LIKE '%demo%' THEN 1 END) as factory FROM usuarios")
        _ = cursor.fetchone()
        
        # 2. Productos
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN precio = 0 OR precio IS NULL THEN 1 END) as zero_price FROM productos")
        _ = cursor.fetchone()
        
        # 3. Habitaciones
        cursor.execute("SELECT COUNT(*) as total, COUNT(CASE WHEN precio_base = 0 OR precio_base IS NULL THEN 1 END) as zero_price FROM habitaciones")
        _ = cursor.fetchone()
        
        # 4. Reservas
        cursor.execute("SELECT COUNT(*) as total FROM reservas")
        _ = cursor.fetchone()
        
        # 5. Categorias
        cursor.execute("SELECT COUNT(*) as total FROM categorias")
        _ = cursor.fetchone()
        
        # 6. Proveedores
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
        
        print("\n🏨 HABITACIONES: %s total" % rooms_data['total'])
        if rooms_data['total'] > 0:
            print("   • Precio cero/nulo: {rooms_data['zero_price']} (%s%)" % (rooms_data['zero_price']/rooms_data['total']*100):.1f)
            print("   • Tipo: %s" % '🏭 FACTORY DATA' if rooms_data['zero_price'] >= rooms_data['total']/2 else '💰 DATOS REALES')
        else:
            print("   • Estado: ⚠️ VACÍO - NECESITA DATOS")
        
        print("\n📅 RESERVAS: %s total" % reservations_data['total'])
        print("   • Estado: %s" % '⚠️ VACÍO' if reservations_data['total'] == 0 else '✅ CON DATOS')
        
        print("\n🏷️ CATEGORÍAS: %s total" % categories_data['total'])
        print("   • Estado: %s" % '⚠️ VACÍO' if categories_data['total'] == 0 else '✅ CON DATOS')
        
        print("\n🚚 PROVEEDORES: %s total" % suppliers_data['total'])
        print("   • Estado: %s" % '⚠️ VACÍO' if suppliers_data['total'] == 0 else '✅ CON DATOS')
        
        return {
            'usuarios': users_data,
            'productos': products_data,
            'habitaciones': rooms_data,
            'reservas': reservations_data,
            'categorias': categories_data,
            'proveedores': suppliers_data
        }
    
    def analyze_inventory_connections(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Analizar conexiones del módulo inventario"""
        print("\n🔗 ANÁLISIS DE CONEXIONES - MÓDULO INVENTARIO")
        print("=" * 60)
        
        _ = self.conn.cursor()
        
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
        _ = cursor.fetchone()
        
        print(f"📦 Productos ↔ Categorías:")
        if product_cat['total_productos'] > 0:
            print("   • Total productos: %s" % product_cat['total_productos'])
            print("   • Con categoría: %s" % product_cat['con_categoria'])
            print("   • Categoría válida: %s" % product_cat['categoria_valida'])
            print("   • Integridad: %s%" % (product_cat['categoria_valida']/product_cat['total_productos']*100):.1f)
        else:
            print("   • ⚠️ No hay productos para verificar")
        
        # 2. Movimientos stock -> Productos
        cursor.execute("""
            SELECT COUNT(*) as total_movimientos,
                   COUNT(CASE WHEN p.id IS NOT NULL THEN 1 END) as producto_valido
            FROM movimientos_stock ms
            LEFT JOIN productos p ON ms.producto_id = p.id
        """)
        _ = cursor.fetchone()
        
        print(f"\n📊 Movimientos Stock ↔ Productos:")
        if stock_prod['total_movimientos'] > 0:
            print("   • Total movimientos: %s" % stock_prod['total_movimientos'])
            print("   • Producto válido: %s" % stock_prod['producto_valido'])
            print("   • Integridad: %s%" % (stock_prod['producto_valido']/stock_prod['total_movimientos']*100):.1f)
        else:
            print("   • ⚠️ No hay movimientos de stock")
        
        # 3. Verificar estructura de tablas inventario
        print(f"\n🗂️ ESTRUCTURA TABLAS INVENTARIO:")
        print("-" * 35)
        
        _ = ['productos', 'categorias', 'proveedores', 'movimientos_stock']
        
        for table in inventory_tables:
            cursor.execute(f"PRAGMA table_info({table})")
            _ = cursor.fetchall()
            print("\n📋 Tabla '%s':" % table)
            for col in columns:
                nullable = "NULL" if col['notnull'] == 0 else "NOT NULL"
                default = f" DEFAULT {col['dflt_value']}" if col['dflt_value'] else ""
                print("   • {col['name']} ({col['type']}) {nullable}%s" % default)
    
    def suggest_factory_data(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Sugerir datos de fábrica para testing"""
        print("\n🏭 SUGERENCIAS DE DATOS DE FÁBRICA")
        print("=" * 50)
        
        _ = {
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
            print("\n📋 %s:" % table.upper())
            print("-" * 20)
            for item in data_list:
                print("   • %s" % item)
    
    def check_inventory_module_compatibility(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verificar compatibilidad con el módulo de inventario"""
        print("\n🔧 COMPATIBILIDAD MÓDULO INVENTARIO")
        print("=" * 50)
        
        _ = self.conn.cursor()
        
        # Verificar campos esperados por el módulo
        _ = {
            'productos': ['id', 'nombre', 'precio', 'stock', 'categoria'],
            'categorias': ['id', 'nombre'],
            'proveedores': ['id', 'nombre', 'email', 'telefono'],
            'movimientos_stock': ['id', 'producto_id', 'tipo', 'cantidad', 'fecha']
        }
        
        _ = 0
        total_checks = 0
        
        for table, fields in expected_fields.items():
            cursor.execute(f"PRAGMA table_info({table})")
            _ = [col['name'] for col in cursor.fetchall()]
            
            print("\n📋 Tabla '%s':" % table)
            
            for field in fields:
                total_checks += 1
                if field in existing_columns:
                    print("   ✅ %s" % field)
                    compatibility_score += 1
                else:
                    print("   ❌ %s - FALTANTE" % field)
        
        _ = (compatibility_score / total_checks * 100)
        
        print(f"\n📊 PUNTUACIÓN COMPATIBILIDAD:")
        print("   • Campos encontrados: {compatibility_score}/%s" % total_checks)
        print("   • Porcentaje: %s%" % compatibility_percent:.1f)
        
        if compatibility_percent >= 90:
            print("   • Estado: ✅ EXCELENTE COMPATIBILIDAD")
        elif compatibility_percent >= 70:
            print("   • Estado: ⚠️ BUENA COMPATIBILIDAD - Revisar campos faltantes")
        else:
            print("   • Estado: ❌ PROBLEMAS DE COMPATIBILIDAD - Requiere ajustes")
        
        return compatibility_percent

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
        
        # 2. Análisis de conexiones inventario
        analyzer.analyze_inventory_connections()
        
        # 3. Verificar compatibilidad módulo
        _ = analyzer.check_inventory_module_compatibility()
        
        # 4. Sugerir datos de fábrica
        analyzer.suggest_factory_data()
        
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
        
        print("🔧 Compatibilidad módulo: %s%" % compatibility:.1f)
        
        if compatibility >= 90:
            print("🎉 LISTO para implementar funcionalidades completas")
        else:
            print("⚠️  Revisar estructura antes de implementar")
        
    except Exception as e:
    logging.error("❌ Error durante análisis: %s", e)
    finally:
        if analyzer.conn:
            analyzer.conn.close()

if __name__ == "__main__":
    main()
