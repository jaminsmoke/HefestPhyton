from typing import Optional, Dict, List, Any
import sys
import os
import sqlite3
from data.db_manager import DatabaseManager
import logging

"""
Script de migración de datos simulados a datos reales
Pobla la base de datos con datos iniciales básicos para testing
"""


# Agregar la ruta del proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def migrar_a_datos_reales():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """
    Migra el sistema de datos simulados a datos reales
    Crea datos básicos para que la aplicación funcione
    """
    
    logger.info("🚀 Iniciando migración a datos reales...")
    
    try:
        # Inicializar DatabaseManager
        _ = DatabaseManager()
        logger.info("✅ Conexión a base de datos establecida")
        
        # 1. Limpiar datos existentes (opcional - comentar si quieres mantener datos)
        limpiar_datos_existentes(db_manager)
        
        # 2. Agregar columnas faltantes si no existen
        agregar_columnas_faltantes(db_manager)
        
        # 3. Poblar con datos básicos
        poblar_productos_basicos(db_manager)
        poblar_habitaciones_basicas(db_manager)
        poblar_mesas_basicas(db_manager)
        poblar_empleados_basicos(db_manager)
        
        # 4. Verificar que todo esté bien
        verificar_migracion(db_manager)
        
        logger.info("🎉 Migración completada exitosamente")
        logger.info("📊 La aplicación ahora usa datos reales de la base de datos")
        
    except Exception as e:
        logger.error("❌ Error durante la migración: %s", e)
        return False
    
    return True

def limpiar_datos_existentes(db_manager):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Limpia datos existentes (opcional)"""
    logger.info("🧹 Limpiando datos existentes...")
    
    # Solo limpiamos si el usuario lo confirma
    confirm = input("¿Deseas limpiar todos los datos existentes? (s/N): ").lower()
    if confirm == 's':
        try:
            # Limpiar tablas principales (manteniendo estructura)
            db_manager.execute("DELETE FROM comandas")
            db_manager.execute("DELETE FROM comanda_detalles") 
            db_manager.execute("DELETE FROM reservas")
            db_manager.execute("DELETE FROM productos")
            db_manager.execute("DELETE FROM habitaciones")
            db_manager.execute("DELETE FROM mesas")
            # No limpiamos empleados/usuarios para mantener acceso
            logger.info("✅ Datos existentes limpiados")
        except Exception as e:
            logger.warning("Advertencia al limpiar datos: %s", e)
    else:
        logger.info("✅ Manteniendo datos existentes")

def agregar_columnas_faltantes(db_manager):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Agrega columnas que pueden faltar en la base de datos"""
    logger.info("🔧 Verificando y agregando columnas faltantes...")
    
    try:
        # Agregar columna stock_minimo a productos si no existe
        try:
            db_manager.execute("ALTER TABLE productos ADD COLUMN stock_minimo INTEGER DEFAULT 5")
            logger.info("✅ Columna stock_minimo agregada a productos")
        except sqlite3.OperationalError:
            logger.debug("Columna stock_minimo ya existe en productos")
        
        # Agregar columna proveedor_id a productos si no existe
        try:
            db_manager.execute("ALTER TABLE productos ADD COLUMN proveedor_id INTEGER")
            logger.info("✅ Columna proveedor_id agregada a productos")
        except sqlite3.OperationalError:
            logger.debug("Columna proveedor_id ya existe en productos")
            
        # Agregar columna capacidad a mesas si no existe
        try:
            db_manager.execute("ALTER TABLE mesas ADD COLUMN capacidad INTEGER DEFAULT 4")
            logger.info("✅ Columna capacidad agregada a mesas")
        except sqlite3.OperationalError:
            logger.debug("Columna capacidad ya existe en mesas")
            
    except Exception as e:
        logger.warning("Advertencia al agregar columnas: %s", e)

def poblar_productos_basicos(db_manager):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Pobla la tabla de productos con productos básicos"""
    logger.info("🛒 Poblando productos básicos...")
    
    _ = [
        # Bebidas
        ("Coca Cola 330ml", "Bebidas", 2.50, 20, 10),
        ("Agua Mineral 500ml", "Bebidas", 1.50, 30, 20),  
        ("Cerveza Estrella 330ml", "Bebidas", 2.80, 15, 12),
        ("Café Espresso", "Bebidas", 2.00, 0, 0),  # Sin stock inicial
        ("Zumo de Naranja", "Bebidas", 3.50, 10, 8),
        
        # Comidas
        ("Bocadillo Jamón", "Comidas", 4.50, 0, 0),  # Se hace al momento
        ("Ensalada César", "Comidas", 8.90, 0, 0),   # Se hace al momento
        ("Tortilla Española", "Comidas", 6.50, 0, 0), # Se hace al momento
        ("Patatas Bravas", "Comidas", 5.20, 0, 0),   # Se hace al momento
        
        # Snacks  
        ("Patatas Fritas", "Snacks", 1.80, 25, 15),
        ("Aceitunas", "Snacks", 3.20, 12, 8),
        ("Frutos Secos", "Snacks", 4.00, 8, 5),
        
        # Ingredientes/Provisiones
        ("Pan (barra)", "Ingredientes", 1.20, 0, 5),
        ("Huevos (docena)", "Ingredientes", 2.80, 0, 2),
        ("Aceite de Oliva", "Ingredientes", 8.50, 2, 1),
    ]
    
    try:
        for nombre, categoria, precio, stock, stock_minimo in productos_basicos:
            # Verificar si el producto ya existe
            existing = db_manager.query("SELECT id FROM productos WHERE nombre = ?", (nombre,))
            if not existing:
                db_manager.execute("""
                    INSERT INTO productos (nombre, categoria, precio, stock, stock_minimo)
                    VALUES (?, ?, ?, ?, ?)
                """, (nombre, categoria, precio, stock, stock_minimo))
                
        logger.info("✅ %s productos básicos poblados", len(productos_basicos))
        
    except Exception as e:
        logger.error("Error al poblar productos: %s", e)

def poblar_habitaciones_basicas(db_manager):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Pobla la tabla de habitaciones con habitaciones básicas"""
    logger.info("🏨 Poblando habitaciones básicas...")
    
    _ = [
        ("101", "Individual", "disponible", 45.00),
        ("102", "Individual", "disponible", 45.00),
        ("103", "Doble", "disponible", 65.00),
        ("104", "Doble", "ocupada", 65.00),
        ("105", "Doble", "disponible", 65.00),
        ("201", "Suite", "disponible", 95.00),
        ("202", "Suite", "mantenimiento", 95.00),
        ("203", "Individual", "disponible", 45.00),
        ("204", "Doble", "disponible", 65.00),
        ("205", "Suite", "ocupada", 95.00),
    ]
    
    try:
        for numero, tipo, estado, precio_base in habitaciones_basicas:
            # Verificar si la habitación ya existe
            existing = db_manager.query("SELECT id FROM habitaciones WHERE numero = ?", (numero,))
            if not existing:
                db_manager.execute("""
                    INSERT INTO habitaciones (numero, tipo, estado, precio_base)
                    VALUES (?, ?, ?, ?)
                """, (numero, tipo, estado, precio_base))
                
        logger.info("✅ %s habitaciones básicas pobladas", len(habitaciones_basicas))
        
    except Exception as e:
        logger.error("Error al poblar habitaciones: %s", e)

def poblar_mesas_basicas(db_manager):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Pobla la tabla de mesas con mesas básicas"""
    logger.info("🍽️ Poblando mesas básicas...")
    
    _ = [
        ("1", "Terraza", "libre", 4),
        ("2", "Terraza", "ocupada", 4), 
        ("3", "Terraza", "libre", 2),
        ("4", "Interior", "libre", 6),
        ("5", "Interior", "ocupada", 4),
        ("6", "Interior", "libre", 4),
        ("7", "Barra", "libre", 2),
        ("8", "Barra", "libre", 2),
        ("9", "Sala VIP", "libre", 8),
        ("10", "Sala VIP", "libre", 6),
    ]
    
    try:
        for numero, zona, estado, capacidad in mesas_basicas:
            # Verificar si la mesa ya existe
            existing = db_manager.query("SELECT id FROM mesas WHERE numero = ?", (numero,))
            if not existing:
                db_manager.execute("""
                    INSERT INTO mesas (numero, zona, estado, capacidad)
                    VALUES (?, ?, ?, ?)
                """, (numero, zona, estado, capacidad))
                
        logger.info("✅ %s mesas básicas pobladas", len(mesas_basicas))
        
    except Exception as e:
        logger.error("Error al poblar mesas: %s", e)

def poblar_empleados_basicos(db_manager):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Pobla la tabla de empleados con empleados básicos"""
    logger.info("👥 Poblando empleados básicos...")
    
    _ = [
        ("admin", "Administrador", "Sistema", "00000000A", "admin", "1234", 1),
        ("camarero1", "Juan", "Pérez", "12345678B", "camarero", "1234", 1),
        ("camarero2", "María", "García", "87654321C", "camarero", "1234", 1),
        ("recepcion", "Ana", "López", "11223344D", "recepcionista", "1234", 1),
    ]
    
    try:
        for username, nombre, apellidos, dni, rol, password, active in empleados_basicos:
            # Verificar si el empleado ya existe
            existing = db_manager.query("SELECT id FROM empleados WHERE username = ?", (username,))
            if not existing:
                db_manager.execute("""
                    INSERT INTO empleados (username, nombre, apellidos, dni, rol, password, active)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (username, nombre, apellidos, dni, rol, password, active))
                
        logger.info("✅ %s empleados básicos poblados", len(empleados_basicos))
        
    except Exception as e:
        logger.error("Error al poblar empleados: %s", e)

def verificar_migracion(db_manager):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Verifica que la migración se haya completado correctamente"""
    logger.info("🔍 Verificando migración...")
    
    try:
        # Contar registros en tablas principales
        _ = db_manager.query("SELECT COUNT(*) as count FROM productos")[0]['count']
        habitaciones = db_manager.query("SELECT COUNT(*) as count FROM habitaciones")[0]['count']
        _ = db_manager.query("SELECT COUNT(*) as count FROM mesas")[0]['count']
        empleados = db_manager.query("SELECT COUNT(*) as count FROM empleados")[0]['count']
        
        logger.info(f"📊 Resumen de datos:")
        logger.info("   - Productos: %s", productos)
        logger.info("   - Habitaciones: %s", habitaciones)
        logger.info("   - Mesas: %s", mesas)
        logger.info("   - Empleados: %s", empleados)
        
        # Verificar métricas administrativas
        _ = db_manager.get_admin_metrics()
        logger.info(f"📈 Métricas obtenidas:")
        logger.info("   - Ventas: %s", metrics.get('ventas', 'N/A'))
        logger.info("   - Ocupación: %s%", metrics.get('ocupacion', 'N/A'))
        logger.info("   - Órdenes activas: %s", metrics.get('ordenes_activas', 'N/A'))
        
        logger.info("✅ Verificación completada - Sistema listo para usar datos reales")
        
    except Exception as e:
        logger.error("Error durante la verificación: %s", e)

def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Función principal del script de migración"""
    print("="*60)
    print("🚀 MIGRACIÓN A DATOS REALES - SISTEMA HEFEST")
    print("="*60)
    print()
    print("Este script migrará el sistema de datos simulados a datos reales.")
    print("Se poblarán las tablas básicas con datos iniciales para testing.")
    print()
    
    confirm = input("¿Continuar con la migración? (s/N): ").lower()
    if confirm != 's':
        print("❌ Migración cancelada")
        return
    
    if migrar_a_datos_reales():
        print()
        print("="*60)
        print("🎉 MIGRACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        print("✅ El sistema ahora usa datos reales de la base de datos")
        print("✅ Todos los componentes están configurados para datos reales")
        print("✅ Las métricas se obtienen de transacciones reales")
        print()
        print("🚀 Puedes ejecutar la aplicación normalmente")
        print("📊 Las métricas mostrarán valores reales (muchos en 0 inicialmente)")
        print("📈 Los valores aumentarán conforme uses la aplicación")
    else:
        print()
        print("❌ MIGRACIÓN FALLIDA")
        print("Revisa los logs para más detalles")

if __name__ == "__main__":
    main()
