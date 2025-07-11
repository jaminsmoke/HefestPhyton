#!/usr/bin/env python3
"""
Script para estandarizar las zonas de mesas: 5 zonas con 10 mesas cada una
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))

from data.db_manager import DatabaseManager

def estandarizar_zonas_mesas():
    """Estandariza las zonas de mesas a 5 zonas con 10 mesas cada una"""
    try:
        db_manager = DatabaseManager()
        
        print("=" * 60)
        print("ESTANDARIZACION DE ZONAS DE MESAS")
        print("=" * 60)
        
        # Definir la estructura estándar
        zonas_estandar = {
            'Terraza': {'prefijo': 'T', 'capacidades': [2, 2, 2, 4, 4, 4, 6, 6, 6, 8]},
            'Interior': {'prefijo': 'I', 'capacidades': [2, 2, 4, 4, 4, 4, 6, 6, 8, 8]},
            'Barra': {'prefijo': 'B', 'capacidades': [2, 2, 2, 2, 2, 2, 4, 4, 4, 4]},
            'VIP': {'prefijo': 'V', 'capacidades': [4, 4, 6, 6, 6, 8, 8, 10, 10, 12]},
            'Comedor': {'prefijo': 'C', 'capacidades': [4, 4, 4, 6, 6, 6, 8, 8, 10, 12]}
        }
        
        # Limpiar todas las mesas existentes
        print("[1/3] Eliminando mesas existentes...")
        db_manager.execute("DELETE FROM mesas")
        print("    - Todas las mesas eliminadas")
        
        # Crear las mesas estandarizadas
        print("[2/3] Creando mesas estandarizadas...")
        mesa_id = 1
        
        for zona, config in zonas_estandar.items():
            prefijo = config['prefijo']
            capacidades = config['capacidades']
            
            print(f"    - Creando zona {zona}...")
            
            for i in range(10):  # 10 mesas por zona
                numero_mesa = f"{prefijo}{i+1:02d}"  # T01, T02, etc.
                capacidad = capacidades[i]
                
                db_manager.execute("""
                    INSERT INTO mesas (numero, zona, estado, capacidad)
                    VALUES (?, ?, ?, ?)
                """, (numero_mesa, zona, "libre", capacidad))
                
                mesa_id += 1
            
            print(f"      [OK] {zona}: 10 mesas creadas ({prefijo}01-{prefijo}10)")
        
        # Verificar resultado
        print("[3/3] Verificando resultado...")
        mesas_totales = db_manager.query("SELECT COUNT(*) as total FROM mesas")[0]['total']
        
        print(f"    - Total de mesas creadas: {mesas_totales}")
        
        # Mostrar resumen por zona
        for zona in zonas_estandar.keys():
            count = db_manager.query("SELECT COUNT(*) as count FROM mesas WHERE zona = ?", (zona,))[0]['count']
            print(f"    - {zona}: {count} mesas")
        
        print()
        print("=" * 60)
        print("[EXITO] Estandarizacion completada exitosamente")
        print("- 5 zonas creadas: Terraza, Interior, Barra, VIP, Comedor")
        print("- 10 mesas por zona (50 mesas totales)")
        print("- Numeracion coherente: T01-T10, I01-I10, B01-B10, V01-V10, C01-C10")
        print("- Capacidades variadas segun el tipo de zona")
        
    except Exception as e:
        print(f"[ERROR] Error al estandarizar las zonas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    estandarizar_zonas_mesas()