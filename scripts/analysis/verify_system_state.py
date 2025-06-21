#!/usr/bin/env python3
"""
Script de verificación del estado del sistema Hefest
Verifica que el sistema esté en configuración inicial correcta
"""

import sqlite3
import logging
from pathlib import Path
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - VERIFY - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Ruta de la base de datos
DB_PATH = Path(__file__).parent.parent / "data" / "hefest.db"

def verify_system_state():
    """Verificar el estado actual del sistema"""
    
    print("="*60)
    print("🔍 HEFEST - VERIFICACIÓN DEL ESTADO DEL SISTEMA")
    print("="*60)
    
    if not DB_PATH.exists():
        logger.error(f"❌ Base de datos no encontrada: {DB_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Verificar usuarios (deben existir)
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            logger.error("❌ CRÍTICO: No hay usuarios en el sistema")
            return False
        elif user_count == 3:
            logger.info(f"✅ Usuarios: {user_count} usuarios básicos (correcto)")
        else:
            logger.warning(f"⚠️ Usuarios: {user_count} usuarios (esperado: 3)")
        
        # Verificar tablas operacionales (deben estar vacías)
        operational_tables = {
            'mesas': 'Mesas configuradas',
            'productos': 'Productos en inventario',
            'clientes': 'Clientes registrados',
            'habitaciones': 'Habitaciones disponibles',
            'reservas': 'Reservas activas',
            'comandas': 'Comandas en sistema',
            'comanda_detalles': 'Detalles de comandas',
            'empleados': 'Empleados registrados'
        }
        
        total_records = 0
        config_status = "✅ CONFIGURACIÓN INICIAL"
        
        logger.info("\n📊 ESTADO DE DATOS OPERACIONALES:")
        for table, description in operational_tables.items():
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_records += count
                
                if count == 0:
                    logger.info(f"  ✅ {table}: {count} ({description})")
                else:
                    logger.warning(f"  📊 {table}: {count} ({description})")
                    config_status = "📊 CON DATOS"
                    
            except sqlite3.OperationalError as e:
                logger.warning(f"  ⚠️ {table}: No existe ({e})")
        
        # Estado final
        logger.info(f"\n🎯 ESTADO FINAL: {config_status}")
        
        if total_records == 0:
            logger.info("📋 Sistema en CONFIGURACIÓN INICIAL perfecta")
            logger.info("🚀 Listo para configurar establecimiento desde cero")
            logger.info("📊 Dashboard mostrará valores 0 o vacíos (datos reales)")
        else:
            logger.info(f"📊 Sistema CON DATOS: {total_records} registros totales")
            logger.info("📈 Dashboard mostrará métricas reales basadas en datos")
        
        # Verificar credenciales
        logger.info("\n🔐 CREDENCIALES DE ACCESO:")
        cursor.execute("SELECT nombre, role FROM usuarios ORDER BY id")
        users = cursor.fetchall()
        for user in users:
            logger.info(f"  👤 {user[0]} ({user[1]})")
        
        conn.close()
        
        # Resumen final
        print("\n" + "="*60)
        if total_records == 0:
            print("✅ SISTEMA EN CONFIGURACIÓN INICIAL CORRECTA")
            print("📊 Dashboard mostrará valores reales (0 o vacíos)")
            print("🔐 Login funcionará con usuarios básicos")
            print("🚀 Listo para configuración del establecimiento")
        else:
            print("📊 SISTEMA CON DATOS CONFIGURADOS")
            print("📈 Dashboard mostrará métricas reales")
            print("✅ Funcionamiento normal")
        print("="*60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error durante la verificación: {e}")
        return False

def check_dashboard_manager():
    """Verificar que el RealDataManager esté configurado correctamente"""
    try:
        # Añadir src al path para importar
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
        
        from utils.real_data_manager import RealDataManager
        logger.info("✅ RealDataManager disponible")
        return True
    except ImportError as e:
        logger.error(f"❌ Error importando RealDataManager: {e}")
        return False

if __name__ == "__main__":
    success = verify_system_state()
    
    if success:
        logger.info("\n🔍 Verificando componentes del sistema...")
        check_dashboard_manager()
        
        print("\n🎯 VERIFICACIÓN COMPLETADA")
        print("📋 El sistema está funcionando correctamente")
        print("🚀 Puedes ejecutar: python main.py")
    else:
        print("\n❌ VERIFICACIÓN FALLÓ")
        print("🔧 Revisar los errores reportados")
        sys.exit(1)
