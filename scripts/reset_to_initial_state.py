"""
Script para resetear la base de datos a configuración inicial
Elimina todos los datos de demostración y deja el sistema limpio
"""

import sys
import os

# Añadir la ruta del proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.db_manager import DatabaseManager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def reset_to_initial_state():
    """Resetear base de datos a estado inicial (configuración limpia)"""
    db = DatabaseManager()
    
    logger.info("🔄 Reseteando base de datos a configuración inicial...")
    
    try:
        # 1. LIMPIAR TODAS LAS TABLAS DE DATOS (mantener estructura)
        logger.info("🗑️ Eliminando todos los datos...")
        
        # Eliminar en orden correcto (respetando foreign keys)
        tables_to_clean = [
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
                deleted_count = db.query(f"SELECT COUNT(*) FROM {table}")[0][0]
                db.execute(f"DELETE FROM {table}")
                logger.info(f"  ✅ {table}: {deleted_count} registros eliminados")
            except Exception as e:
                logger.warning(f"  ⚠️ Error limpiando {table}: {e}")
        
        # 2. RESETEAR SECUENCIAS (AUTO INCREMENT)
        logger.info("🔢 Reseteando secuencias...")
        
        sequences_to_reset = [
            'mesas', 'habitaciones', 'productos', 'clientes', 
            'reservas', 'comandas', 'comanda_detalles'
        ]
        
        for table in sequences_to_reset:
            try:
                # SQLite usa AUTOINCREMENT, reseteamos la secuencia
                db.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
                logger.info(f"  ✅ Secuencia de {table} reseteada")
            except Exception as e:
                logger.warning(f"  ⚠️ Error reseteando secuencia de {table}: {e}")
        
        # 3. VERIFICAR ESTADO FINAL
        logger.info("\n📊 VERIFICACIÓN DEL ESTADO INICIAL:")
        
        verification_tables = [
            ('mesas', 'Mesas'),
            ('habitaciones', 'Habitaciones'), 
            ('productos', 'Productos'),
            ('clientes', 'Clientes'),
            ('reservas', 'Reservas'),
            ('comandas', 'Comandas'),
            ('comanda_detalles', 'Detalles de comandas')
        ]
        
        all_empty = True
        for table, display_name in verification_tables:
            try:
                count = db.query(f"SELECT COUNT(*) FROM {table}")[0][0]
                status = "✅ VACÍA" if count == 0 else f"❌ TIENE {count} REGISTROS"
                logger.info(f"  • {display_name}: {status}")
                if count > 0:
                    all_empty = False
            except Exception as e:
                logger.error(f"  • {display_name}: ❌ ERROR - {e}")
                all_empty = False
        
        # 4. VERIFICAR USUARIOS (DEBEN MANTENERSE)
        try:
            users_count = db.query("SELECT COUNT(*) FROM usuarios")[0][0]
            logger.info(f"  • Usuarios del sistema: ✅ {users_count} (MANTENIDOS)")
        except Exception as e:
            logger.error(f"  • Usuarios del sistema: ❌ ERROR - {e}")
        
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
        logger.error(f"❌ Error durante el reseteo: {e}")
        raise


def show_initial_state_info():
    """Mostrar información sobre el estado inicial"""
    logger.info("\n" + "="*60)
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
