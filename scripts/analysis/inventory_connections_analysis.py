#!/usr/bin/env python3
"""
Análisis de Conexiones - Módulo de Inventario Hefest
=================================================

Verifica las conexiones entre el módulo de inventario y la base de datos,
validando servicios, componentes y funcionalidades.
"""

import sys
import os

# Configurar paths correctamente
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, project_root)
sys.path.insert(0, src_path)

def test_inventory_connections():
    """Verificar conexiones del módulo de inventario"""
    
    print("🔗 ANÁLISIS CONEXIONES MÓDULO DE INVENTARIO")
    print("=" * 50)
    
    issues = []
    connections_ok = True
    
    # 1. IMPORTAR COMPONENTES PRINCIPALES
    print("\n📦 IMPORTANDO COMPONENTES...")
    
    try:
        print("   Importando DatabaseManager...")
        from data.db_manager import DatabaseManager
        print("   ✅ DatabaseManager importado")
    except Exception as e:
        print(f"   ❌ Error importando DatabaseManager: {e}")
        issues.append("DatabaseManager no disponible")
        connections_ok = False
    
    try:
        print("   Importando InventarioService...")
        from services.inventario_service_real import InventarioService
        print("   ✅ InventarioService importado")
    except Exception as e:
        print(f"   ❌ Error importando InventarioService: {e}")
        issues.append("InventarioService no disponible")
        connections_ok = False
    
    try:
        print("   Importando InventarioModule...")
        from ui.modules.inventario_module import InventarioModule
        print("   ✅ InventarioModule importado")
    except Exception as e:
        print(f"   ❌ Error importando InventarioModule: {e}")
        issues.append("InventarioModule no disponible")
        connections_ok = False
    
    try:
        print("   Importando Managers especializados...")
        from ui.modules.inventario_module.components import (
            ProductsManagerWidget, 
            CategoryManagerWidget, 
            SupplierManagerWidget
        )
        print("   ✅ Managers especializados importados")
    except Exception as e:
        print(f"   ❌ Error importando Managers: {e}")
        issues.append("Managers especializados no disponibles")
        connections_ok = False
    
    if not connections_ok:
        print(f"\n❌ FALLO EN IMPORTACIONES")
        return False, issues
    
    # 2. VERIFICAR CONEXIÓN BASE DE DATOS
    print("\n🗃️  VERIFICANDO CONEXIÓN BASE DE DATOS...")
    
    try:
        db_manager = DatabaseManager()
        print("   ✅ DatabaseManager inicializado")
        
        # Verificar que se puede conectar
        with db_manager._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            print(f"   ✅ Conexión exitosa - {table_count} tablas detectadas")
            
    except Exception as e:
        print(f"   ❌ Error en conexión BD: {e}")
        issues.append("Conexión a base de datos falla")
        connections_ok = False
    
    # 3. VERIFICAR SERVICIO DE INVENTARIO
    print("\n🛠️  VERIFICANDO SERVICIO DE INVENTARIO...")
    
    try:
        inventario_service = InventarioService(db_manager)
        print("   ✅ InventarioService inicializado")
        
        # Verificar métodos principales
        methods_to_check = [
            'obtener_productos',
            'obtener_categorias', 
            'obtener_proveedores',
            'agregar_producto',
            'actualizar_stock'
        ]
        
        for method in methods_to_check:
            if hasattr(inventario_service, method):
                print(f"   ✅ Método {method} disponible")
            else:
                print(f"   ❌ Método {method} faltante")
                issues.append(f"Método {method} no implementado")
                connections_ok = False
                
    except Exception as e:
        print(f"   ❌ Error inicializando InventarioService: {e}")
        issues.append("InventarioService no funciona")
        connections_ok = False
    
    # 4. VERIFICAR ESTRUCTURA DE TABLAS INVENTARIO
    print("\n📋 VERIFICANDO TABLAS DE INVENTARIO...")
    
    required_tables = [
        ('productos', ['id', 'nombre', 'precio', 'stock', 'categoria']),
        ('categorias', ['id', 'nombre']),
        ('proveedores', ['id', 'nombre', 'contacto']),
        ('movimientos_stock', ['id', 'producto_id', 'tipo', 'cantidad', 'fecha'])
    ]
    
    try:
        with db_manager._get_connection() as conn:
            cursor = conn.cursor()
            
            for table_name, expected_columns in required_tables:
                # Verificar si tabla existe
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
                table_exists = cursor.fetchone()
                
                if table_exists:
                    print(f"   ✅ Tabla {table_name} existe")
                    
                    # Verificar columnas
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns = [col[1] for col in cursor.fetchall()]
                    
                    missing_columns = set(expected_columns) - set(columns)
                    if missing_columns:
                        print(f"   ⚠️  Tabla {table_name} - columnas faltantes: {missing_columns}")
                        issues.append(f"Tabla {table_name} incompleta")
                    else:
                        print(f"   ✅ Tabla {table_name} - estructura completa")
                else:
                    print(f"   ❌ Tabla {table_name} no existe")
                    issues.append(f"Tabla {table_name} faltante")
                    connections_ok = False
                    
    except Exception as e:
        print(f"   ❌ Error verificando tablas: {e}")
        issues.append("Error accediendo a estructura de tablas")
        connections_ok = False
    
    # 5. VERIFICAR WIDGETS DEL MÓDULO
    print("\n🖼️  VERIFICANDO WIDGETS DE INVENTARIO...")
    
    widget_classes = [
        ('ProductsManagerWidget', 'Gestión de productos'),
        ('CategoryManagerWidget', 'Gestión de categorías'),
        ('SupplierManagerWidget', 'Gestión de proveedores')
    ]
    
    for widget_name, description in widget_classes:
        try:
            widget_class = globals()[widget_name]
            # Verificar que es una clase de Qt
            print(f"   ✅ {widget_name} - {description}")
        except Exception as e:
            print(f"   ❌ {widget_name} no disponible: {e}")
            issues.append(f"Widget {widget_name} faltante")
            connections_ok = False
    
    # RESULTADO FINAL
    print("\n" + "=" * 50)
    if connections_ok:
        print("🔗 ✅ TODAS LAS CONEXIONES CORRECTAS")
        print("     Módulo de inventario listo para funcionar")
    else:
        print("🔗 ❌ PROBLEMAS EN CONEXIONES DETECTADOS")
        print("\n🔍 ISSUES ENCONTRADOS:")
        for issue in issues:
            print(f"     • {issue}")
    
    print("=" * 50)
    
    return connections_ok, issues

def analyze_inventory_functionality():
    """Analizar funcionalidades disponibles"""
    
    print("\n🎯 FUNCIONALIDADES DEL MÓDULO DE INVENTARIO")
    print("-" * 50)
    
    functionalities = {
        "✅ Implementadas": [
            "Conexión a base de datos",
            "Interfaz con pestañas especializadas",
            "Widgets para productos, categorías, proveedores",
            "Estructura de tablas preparada"
        ],
        "🔄 Por implementar": [
            "CRUD completo de productos",
            "Gestión de stock y alertas",
            "Movimientos de inventario",
            "Reportes de inventario",
            "Integración con TPV",
            "Gestión de pedidos a proveedores",
            "Análisis de rotación de productos",
            "Exportación de datos"
        ]
    }
    
    for category, items in functionalities.items():
        print(f"\n{category}:")
        for item in items:
            print(f"   • {item}")

if __name__ == "__main__":
    connections_ok, issues = test_inventory_connections()
    
    if connections_ok:
        analyze_inventory_functionality()
    
    print(f"\n📋 Estado conexiones: {'✅ OK' if connections_ok else '❌ ISSUES'}")
