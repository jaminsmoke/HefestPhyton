#!/usr/bin/env python3
"""
Análisis Estado de Fábrica - Base de Datos Hefest
===============================================

Verifica si la base de datos está en estado de fábrica (limpia, sin uso)
o contiene datos reales de operaciones.
"""

import sqlite3
import os
from datetime import datetime

def analyze_factory_state():
    """Analizar si la base de datos está en estado de fábrica"""
    
    db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'hefest.db')
    db_path = os.path.abspath(db_path)
    
    print("🏭 ANÁLISIS ESTADO DE FÁBRICA - BASE DE DATOS HEFEST")
    print("=" * 60)
    print(f"📍 Ubicación: {db_path}")
    print(f"📅 Fecha análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        factory_state = True
        issues = []
        
        print("\n🔍 VERIFICANDO ESTADO DE FÁBRICA...")
        print("-" * 40)
        
        # 1. USUARIOS - Solo debe tener usuarios por defecto
        print("\n👥 USUARIOS:")
        cursor.execute("SELECT COUNT(*) as count FROM usuarios")
        user_count = cursor.fetchone()['count']
        
        cursor.execute("SELECT nombre, role FROM usuarios")
        users = cursor.fetchall()
        
        print(f"   Total usuarios: {user_count}")
        default_users = ['admin', 'manager', 'employee']
        current_users = [user['nombre'] for user in users]
        
        if set(current_users) == set(default_users) and user_count == 3:
            print("   ✅ Solo usuarios por defecto (ESTADO FÁBRICA)")
        else:
            print("   ❌ Usuarios adicionales detectados (DATOS REALES)")
            factory_state = False
            issues.append("Usuarios no estándar detectados")
        
        # 2. PRODUCTOS - Debe estar vacío o con productos demo sin stock
        print("\n📦 PRODUCTOS:")
        cursor.execute("SELECT COUNT(*) as count FROM productos")
        product_count = cursor.fetchone()['count']
        
        if product_count == 0:
            print("   ✅ Sin productos (ESTADO FÁBRICA)")
        else:
            cursor.execute("SELECT COUNT(*) as used FROM productos WHERE stock > 0")
            used_products = cursor.fetchone()['used']
            
            if used_products == 0:
                print(f"   ✅ {product_count} productos con stock=0 (ESTADO FÁBRICA)")
            else:
                print(f"   ❌ {used_products} productos con stock>0 (DATOS REALES)")
                factory_state = False
                issues.append(f"{used_products} productos con stock real")
        
        # 3. MOVIMIENTOS DE STOCK - Debe estar vacío
        print("\n📈 MOVIMIENTOS DE STOCK:")
        cursor.execute("SELECT COUNT(*) as count FROM movimientos_stock")
        movement_count = cursor.fetchone()['count']
        
        if movement_count == 0:
            print("   ✅ Sin movimientos (ESTADO FÁBRICA)")
        else:
            print(f"   ❌ {movement_count} movimientos registrados (DATOS REALES)")
            factory_state = False
            issues.append(f"{movement_count} movimientos de stock")
        
        # 4. CLIENTES - Debe estar vacío
        print("\n👨‍👩‍👧‍👦 CLIENTES:")
        cursor.execute("SELECT COUNT(*) as count FROM clientes")
        client_count = cursor.fetchone()['count']
        
        if client_count == 0:
            print("   ✅ Sin clientes (ESTADO FÁBRICA)")
        else:
            print(f"   ❌ {client_count} clientes registrados (DATOS REALES)")
            factory_state = False
            issues.append(f"{client_count} clientes registrados")
        
        # 5. RESERVAS - Debe estar vacío
        print("\n🏨 RESERVAS:")
        cursor.execute("SELECT COUNT(*) as count FROM reservas")
        reservation_count = cursor.fetchone()['count']
        
        if reservation_count == 0:
            print("   ✅ Sin reservas (ESTADO FÁBRICA)")
        else:
            print(f"   ❌ {reservation_count} reservas registradas (DATOS REALES)")
            factory_state = False
            issues.append(f"{reservation_count} reservas")
        
        # 6. COMANDAS - Debe estar vacío
        print("\n🧾 COMANDAS/ÓRDENES:")
        cursor.execute("SELECT COUNT(*) as count FROM comandas")
        order_count = cursor.fetchone()['count']
        
        if order_count == 0:
            print("   ✅ Sin comandas (ESTADO FÁBRICA)")
        else:
            print(f"   ❌ {order_count} comandas registradas (DATOS REALES)")
            factory_state = False
            issues.append(f"{order_count} comandas/órdenes")
        
        # 7. HABITACIONES - Puede tener habitaciones demo con estado neutro
        print("\n🏠 HABITACIONES:")
        cursor.execute("SELECT COUNT(*) as count FROM habitaciones")
        room_count = cursor.fetchone()['count']
        
        if room_count == 0:
            print("   ✅ Sin habitaciones configuradas (ESTADO FÁBRICA)")
        else:
            cursor.execute("SELECT COUNT(*) as occupied FROM habitaciones WHERE estado != 'disponible'")
            occupied_rooms = cursor.fetchone()['occupied']
            
            if occupied_rooms == 0:
                print(f"   ✅ {room_count} habitaciones disponibles (ESTADO FÁBRICA)")
            else:
                print(f"   ❌ {occupied_rooms} habitaciones ocupadas/reservadas (DATOS REALES)")
                factory_state = False
                issues.append(f"{occupied_rooms} habitaciones en uso")
        
        # 8. MESAS - Puede tener mesas demo con estado neutro
        print("\n🪑 MESAS:")
        cursor.execute("SELECT COUNT(*) as count FROM mesas")
        table_count = cursor.fetchone()['count']
        
        if table_count == 0:
            print("   ✅ Sin mesas configuradas (ESTADO FÁBRICA)")
        else:
            cursor.execute("SELECT COUNT(*) as occupied FROM mesas WHERE estado != 'libre'")
            occupied_tables = cursor.fetchone()['occupied']
            
            if occupied_tables == 0:
                print(f"   ✅ {table_count} mesas libres (ESTADO FÁBRICA)")
            else:
                print(f"   ❌ {occupied_tables} mesas ocupadas (DATOS REALES)")
                factory_state = False
                issues.append(f"{occupied_tables} mesas en uso")
        
        # RESULTADO FINAL
        print("\n" + "=" * 60)
        if factory_state:
            print("🏭 ✅ BASE DE DATOS EN ESTADO DE FÁBRICA")
            print("     Sistema limpio, listo para uso productivo")
        else:
            print("🏭 ❌ BASE DE DATOS CON DATOS REALES")
            print("     Sistema en uso, contiene datos operativos")
            print("\n🔍 ELEMENTOS NO FÁBRICA DETECTADOS:")
            for issue in issues:
                print(f"     • {issue}")
        
        print("=" * 60)
        
        return factory_state, issues
        
    except Exception as e:
        print(f"❌ Error en análisis: {e}")
        return False, [f"Error de conexión: {e}"]
        
    finally:
        if 'conn' in locals():
            conn.close()

def suggest_factory_reset():
    """Sugerir acciones para restaurar estado de fábrica"""
    print("\n🔄 ACCIONES PARA RESTAURAR ESTADO DE FÁBRICA:")
    print("-" * 50)
    print("1. 🗑️  Limpiar datos operativos:")
    print("   - Vaciar movimientos_stock")
    print("   - Vaciar clientes")
    print("   - Vaciar reservas")
    print("   - Vaciar comandas y comanda_detalles")
    print()
    print("2. 🔄 Resetear estados:")
    print("   - Habitaciones → estado='disponible'")
    print("   - Mesas → estado='libre'")
    print("   - Productos → stock=0")
    print()
    print("3. 👥 Mantener usuarios por defecto:")
    print("   - admin, manager, employee")
    print()
    print("4. 🏗️  Mantener estructura base:")
    print("   - Categorías básicas")
    print("   - Proveedores demo")
    print("   - Configuración de habitaciones/mesas")

if __name__ == "__main__":
    factory_state, issues = analyze_factory_state()
    
    if not factory_state:
        suggest_factory_reset()
    
    print(f"\n📋 Estado final: {'FÁBRICA' if factory_state else 'EN USO'}")
