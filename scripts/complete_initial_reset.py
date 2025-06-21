#!/usr/bin/env python3
"""
Script para reseteo COMPLETO a estado de configuración inicial
- Elimina TODOS los datos de operación (mesas, productos, reservas, comandas, etc.)
- Mantiene SOLO usuarios para login
- Deja el sistema en estado de configuración inicial completa
"""

import sqlite3
import logging
from pathlib import Path
import sys
import os

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - RESET - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ruta de la base de datos
DB_PATH = Path(__file__).parent.parent / "data" / "hefest.db"

def reset_to_initial_configuration():
    """Resetear completamente a configuración inicial"""
    
    if not DB_PATH.exists():
        logger.error(f"Base de datos no encontrada: {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        logger.info("🔄 INICIANDO RESETEO COMPLETO A CONFIGURACIÓN INICIAL")
        
        # Tablas a limpiar COMPLETAMENTE (datos operacionales)
        tables_to_clear = [
            'mesas',
            'productos', 
            'clientes',
            'habitaciones',
            'reservas',
            'comandas',
            'comanda_detalles',
            'reservas_restaurant',
            'empleados'
        ]
        
        # Limpiar datos operacionales
        for table in tables_to_clear:
            try:
                cursor.execute(f"DELETE FROM {table}")
                count = cursor.rowcount
                logger.info(f"  ✅ {table}: {count} registros eliminados")
            except sqlite3.OperationalError as e:
                logger.warning(f"  ⚠️ {table}: {e}")
        
        # Resetear secuencias automáticas
        cursor.execute("DELETE FROM sqlite_sequence WHERE name NOT IN ('usuarios')")
        logger.info("  ✅ Secuencias reseteadas (excepto usuarios)")
        
        # Verificar usuarios (se mantienen)
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        user_count = cursor.fetchone()[0]
        logger.info(f"  👥 Usuarios mantenidos: {user_count}")
        
        # Commit de todos los cambios
        conn.commit()
        
        # Verificación final
        logger.info("\n📊 ESTADO FINAL DESPUÉS DEL RESETEO:")
        for table in tables_to_clear:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                status = "✅ VACÍA" if count == 0 else f"⚠️ {count} registros"
                logger.info(f"  {table}: {status}")
            except sqlite3.OperationalError:
                logger.info(f"  {table}: ⚠️ No existe")
        
        conn.close()
        
        logger.info("\n🎉 RESETEO COMPLETO EXITOSO")
        logger.info("📋 Estado: CONFIGURACIÓN INICIAL COMPLETA")
        logger.info("🔐 Login: usuarios mantenidos")
        logger.info("📊 Dashboard: mostrará valores 0 o vacíos")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error durante el reseteo: {e}")
        return False

def verify_initial_state():
    """Verificar que estamos en estado inicial correcto"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        logger.info("\n🔍 VERIFICACIÓN DEL ESTADO INICIAL:")
        
        # Verificar tablas vacías
        operational_tables = ['mesas', 'productos', 'clientes', 'habitaciones', 
                             'reservas', 'comandas', 'comanda_detalles', 'empleados']
        
        all_empty = True
        for table in operational_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                if count > 0:
                    logger.warning(f"  ⚠️ {table}: {count} registros (debería estar vacía)")
                    all_empty = False
                else:
                    logger.info(f"  ✅ {table}: vacía")
            except sqlite3.OperationalError:
                logger.info(f"  ➖ {table}: no existe")
        
        # Verificar usuarios
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        user_count = cursor.fetchone()[0]
        if user_count > 0:
            logger.info(f"  ✅ usuarios: {user_count} registros (correcto)")
        else:
            logger.error("  ❌ usuarios: sin registros (ERROR - necesarios para login)")
            all_empty = False
        
        conn.close()
        
        if all_empty:
            logger.info("\n✅ ESTADO INICIAL VERIFICADO CORRECTAMENTE")
            logger.info("🚀 Sistema listo para configuración inicial")
        else:
            logger.warning("\n⚠️ El sistema no está en estado inicial limpio")
        
        return all_empty
        
    except Exception as e:
        logger.error(f"❌ Error en verificación: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("🔄 HEFEST - RESETEO COMPLETO A CONFIGURACIÓN INICIAL")
    print("="*60)
    
    # Ejecutar reseteo
    if reset_to_initial_configuration():
        print("\n" + "="*60)
        print("✅ RESETEO COMPLETADO")
        
        # Verificar estado
        if verify_initial_state():
            print("🎯 Sistema en CONFIGURACIÓN INICIAL perfecta")
            print("📊 Dashboard mostrará valores reales (0 o vacíos)")
            print("🔐 Login funcionará normalmente")
        else:
            print("⚠️ Verificar manualmente el estado del sistema")
    else:
        print("❌ RESETEO FALLÓ - Revisar logs")
        sys.exit(1)
    
    print("="*60)
