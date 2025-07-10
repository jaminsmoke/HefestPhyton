
ALLOWED_TABLES = {
    'usuarios', 'productos', 'mesas', 'clientes', 'habitaciones',
    'reservas', 'comandas', 'comanda_detalles', 'categorias',
    'proveedores', 'movimientos_stock', 'zonas'
}

def validate_table_name(table):
    if table not in ALLOWED_TABLES:
        raise ValueError(f"Table '{table}' not allowed")
    return table

from typing import Optional, Dict, List, Any
"""
Script para resetear la base de datos a configuración inicial
Elimina todos los datos de demostración y deja el sistema limpio
"""

import sys
import os

# Añadir la ruta del proyecto al path de forma segura
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

from data.db_manager import DatabaseManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reset_to_initial_state():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Resetear base de datos a estado inicial (configuración limpia)"""
    _ = DatabaseManager()
    
    logger.info("🔄 Reseteando base de datos a configuración inicial...")
    
    try:
        # 1. LIMPIAR TODAS LAS TABLAS DE DATOS (mantener estructura)
        logger.info("🗑️ Eliminando todos los datos...")
        
        # Eliminar en orden correcto (respetando foreign keys)
        _ = [
            'comanda_detalles',  # Primero los detalles
            'comandas',          # Luego las comandas
            'reservas',          # Reservas
            'mesas',            # Mesas
            'habitaciones',     # Habitaciones
            'productos',        # Productos (excepto usuarios que necesitamos para login)
            'clientes'          # Clientes
        ]
        
        for table in tables_to_clean:
            try:
                _ = db.query("SELECT COUNT(*) FROM " + table)[0][0]
                db.execute("DELETE FROM " + validate_table_name(table))
                logger.info("  ✅ {table}: %s registros eliminados", deleted_count)
            except Exception as e:
                logger.warning("  ⚠️ Error limpiando {table}: %s", e)
        
        # 2. RESETEAR SECUENCIAS (AUTO INCREMENT)
        logger.info("🔢 Reseteando secuencias...")
        
        _ = [
            'mesas', 'habitaciones', 'productos', 'clientes', 
            'reservas', 'comandas', 'comanda_detalles'
        ]
        
        for table in sequences_to_reset:
            try:
                # SQLite usa AUTOINCREMENT, reseteamos la secuencia
                db.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
                logger.info("  ✅ Secuencia de %s reseteada", table)
            except Exception as e:
                logger.warning("  ⚠️ Error reseteando secuencia de {table}: %s", e)
        
        # 3. VERIFICAR ESTADO FINAL
        logger.info("\n📊 VERIFICACIÓN DEL ESTADO INICIAL:")
        
        _ = [
            ('mesas', 'Mesas'),
            ('habitaciones', 'Habitaciones'), 
            ('productos', 'Productos'),
            ('clientes', 'Clientes'),
            ('reservas', 'Reservas'),
            ('comandas', 'Comandas'),
            ('comanda_detalles', 'Detalles de comandas')
        ]
        
        _ = True
        for table, display_name in verification_tables:
            try:
                count = db.query("SELECT COUNT(*) FROM " + table)[0][0]
                status = "✅ VACÍA" if count == 0 else f"❌ TIENE {count} REGISTROS"
                logger.info("  • {display_name}: %s", status)
                if count > 0:
                    _ = False
            except Exception as e:
                logger.error("  • {display_name}: ❌ ERROR - %s", e)
                _ = False
        
        # 4. VERIFICAR USUARIOS (DEBEN MANTENERSE)
        try:
            users_count = db.query("SELECT COUNT(*) FROM usuarios")[0][0]
            logger.info("  • Usuarios del sistema: ✅ %s (MANTENIDOS)", users_count)
        except Exception as e:
            logger.error("  • Usuarios del sistema: ❌ ERROR - %s", e)
        
        # 5. RESULTADO FINAL
        if all_empty:
            logger.info("\n🎉 ¡RESETEO COMPLETADO EXITOSAMENTE!")
            logger.info("📋 Estado: Configuración inicial (sin datos)")
            logger.info("🔐 Usuarios: Mantenidos para login")
            logger.info("💡 El dashboard mostrará valores en cero (estado real)")
        else:
            logger.warning("\n⚠️ El reseteo no fue completamente exitoso")
            logger.warning("Algunas tablas aún contienen datos")
            
    except Exception as e:
        logger.error("❌ Error durante el reseteo: %s", e)
        raise


def show_initial_state_info():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Mostrar información sobre el estado inicial"""
    logger.info("\n" ,  "="*60)
    logger.info("🏨 HEFEST - CONFIGURACIÓN INICIAL")
    logger.info("="*60)
    logger.info("📊 Dashboard: Mostrará métricas en cero")
    logger.info("🏪 Establecimiento: Sin mesas, habitaciones, productos")
    logger.info("📋 Comandas: Sin registros de ventas")
    logger.info("👥 Clientes: Sin registros")
    logger.info("📅 Reservas: Sin reservas")
    logger.info("")
    logger.info("🔐 USUARIOS DISPONIBLES PARA LOGIN:")
    logger.info("  • admin / admin123 (Administrador)")
    logger.info("  • manager123 / manager123 (Manager)")
    logger.info("  • employee123 / employee123 (Empleado)")
    logger.info("")
    logger.info("📝 PRÓXIMOS PASOS:")
    logger.info("  1. Configurar mesas del establecimiento")
    logger.info("  2. Añadir productos al inventario")
    logger.info("  3. Configurar habitaciones (si aplica)")
    logger.info("  4. Registrar clientes")
    logger.info("  5. Comenzar a tomar comandas")
    logger.info("="*60)


if __name__ == "__main__":
    reset_to_initial_state()
    show_initial_state_info()
