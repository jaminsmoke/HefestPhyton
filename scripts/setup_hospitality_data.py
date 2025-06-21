"""
Script para introducir datos básicos coherentes en la base de datos
para que el dashboard muestre información real
"""

import sys
import os

# Añadir la ruta del proyecto al path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from data.db_manager import DatabaseManager
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def setup_basic_hospitality_data():
    """Configurar datos básicos para un establecimiento hostelero"""
    db = DatabaseManager()
    
    logger.info("🏨 Configurando datos básicos de hostelería...")
    
    try:
        # 1. CREAR MESAS (restaurante con 20 mesas)
        logger.info("📋 Creando mesas...")
        mesas_data = []
        for i in range(1, 21):  # 20 mesas
            zona = "Terraza" if i <= 8 else "Interior" if i <= 16 else "VIP"
            estado = "libre"  # Todas las mesas empiezan libres
            capacidad = 4 if i <= 15 else 6  # Mesas VIP más grandes
            
            mesas_data.append((f"Mesa {i:02d}", zona, estado, capacidad))
        
        # Insertar mesas
        for mesa in mesas_data:
            db.execute("""
                INSERT OR IGNORE INTO mesas (numero, zona, estado, capacidad) 
                VALUES (?, ?, ?, ?)
            """, mesa)
        
        logger.info(f"✅ {len(mesas_data)} mesas creadas")
        
        # 2. CREAR HABITACIONES (pequeño hotel con 12 habitaciones)
        logger.info("🛏️ Creando habitaciones...")
        habitaciones_data = []
        for i in range(101, 113):  # Habitaciones 101-112
            tipo = "Individual" if i <= 104 else "Doble" if i <= 110 else "Suite"
            estado = "libre"  # Todas empiezan libres
            precio = 60 if tipo == "Individual" else 85 if tipo == "Doble" else 120
            
            habitaciones_data.append((str(i), tipo, estado, precio))
        
        # Insertar habitaciones
        for habitacion in habitaciones_data:
            db.execute("""
                INSERT OR IGNORE INTO habitaciones (numero, tipo, estado, precio_base) 
                VALUES (?, ?, ?, ?)
            """, habitacion)
        
        logger.info(f"✅ {len(habitaciones_data)} habitaciones creadas")
        
        # 3. OCUPAR ALGUNAS MESAS PARA SIMULAR ACTIVIDAD REAL
        logger.info("🍽️ Simulando ocupación actual...")
        mesas_a_ocupar = [1, 3, 7, 12, 15]  # 5 mesas ocupadas
        for mesa_num in mesas_a_ocupar:
            db.execute("""
                UPDATE mesas SET estado = 'ocupada' 
                WHERE numero = ?
            """, (f"Mesa {mesa_num:02d}",))
        
        logger.info(f"✅ {len(mesas_a_ocupar)} mesas marcadas como ocupadas")
        
        # 4. CREAR ALGUNAS COMANDAS DEL DÍA
        logger.info("📝 Creando comandas del día...")
        hoy = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        comandas_data = [
            (1, 1, hoy, "completada", 45.80),
            (3, 1, hoy, "completada", 32.50), 
            (7, 1, hoy, "en_preparacion", 67.20),
            (12, 1, hoy, "pendiente", 28.90),
            (15, 1, hoy, "pendiente", 55.40)
        ]
        
        for comanda in comandas_data:
            db.execute("""
                INSERT OR IGNORE INTO comandas (mesa_id, empleado_id, fecha_hora, estado, total) 
                VALUES (?, ?, ?, ?, ?)
            """, comanda)
        
        logger.info(f"✅ {len(comandas_data)} comandas creadas")
        
        # 5. CREAR ALGUNAS RESERVAS FUTURAS
        logger.info("📅 Creando reservas...")
        mañana = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        pasado_mañana = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        
        # Primero crear algunos clientes
        clientes_data = [
            ("Juan", "Pérez", "12345678A", "600123456", "juan@email.com"),
            ("María", "García", "87654321B", "600654321", "maria@email.com"),
            ("Carlos", "López", "11223344C", "600112233", "carlos@email.com")
        ]
        
        for cliente in clientes_data:
            db.execute("""
                INSERT OR IGNORE INTO clientes (nombre, apellidos, dni, telefono, email) 
                VALUES (?, ?, ?, ?, ?)
            """, cliente)
        
        # Crear reservas
        reservas_data = [
            (1, 1, mañana, mañana, "confirmada"),
            (2, 2, mañana, pasado_mañana, "confirmada"),
            (3, 3, pasado_mañana, pasado_mañana, "confirmada")
        ]
        
        for reserva in reservas_data:
            db.execute("""
                INSERT OR IGNORE INTO reservas (cliente_id, habitacion_id, fecha_entrada, fecha_salida, estado) 
                VALUES (?, ?, ?, ?, ?)
            """, reserva)
        
        logger.info(f"✅ {len(reservas_data)} reservas creadas")
        
        # 6. VERIFICAR RESULTADOS
        logger.info("\n📊 RESUMEN DE DATOS CREADOS:")
        
        total_mesas = db.query("SELECT COUNT(*) FROM mesas")[0][0]
        mesas_ocupadas = db.query("SELECT COUNT(*) FROM mesas WHERE estado='ocupada'")[0][0]
        logger.info(f"  • Mesas: {total_mesas} total, {mesas_ocupadas} ocupadas")
        
        total_habitaciones = db.query("SELECT COUNT(*) FROM habitaciones")[0][0]
        logger.info(f"  • Habitaciones: {total_habitaciones} total")
        
        total_comandas = db.query("SELECT COUNT(*) FROM comandas")[0][0]
        comandas_hoy = db.query("SELECT COUNT(*) FROM comandas WHERE DATE(fecha_hora) = DATE('now')")[0][0]
        ventas_hoy = db.query("SELECT COALESCE(SUM(total), 0) FROM comandas WHERE DATE(fecha_hora) = DATE('now')")[0][0]
        logger.info(f"  • Comandas: {total_comandas} total, {comandas_hoy} hoy")
        logger.info(f"  • Ventas del día: {ventas_hoy:.2f}€")
        
        total_reservas = db.query("SELECT COUNT(*) FROM reservas")[0][0]
        reservas_futuras = db.query("SELECT COUNT(*) FROM reservas WHERE DATE(fecha_entrada) >= DATE('now')")[0][0]
        logger.info(f"  • Reservas: {total_reservas} total, {reservas_futuras} futuras")
        
        logger.info("\n🎉 ¡Datos básicos configurados correctamente!")
        
    except Exception as e:
        logger.error(f"❌ Error configurando datos: {e}")
        raise


if __name__ == "__main__":
    setup_basic_hospitality_data()
