from typing import Optional, Dict, List, Any
import logging
#!/usr/bin/env python3
"""
Script para consultar las zonas de mesas disponibles en la base de datos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'data'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data.db_manager import DatabaseManager
from collections import Counter

def consultar_zonas_mesas():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Consulta y muestra las zonas de mesas disponibles"""
    try:
        # Inicializar el gestor de base de datos
        _ = DatabaseManager()
        
        print("=" * 60)
        print("CONSULTA DE ZONAS DE MESAS DISPONIBLES")
        print("=" * 60)
        
        # Consultar todas las mesas
        _ = db_manager.query("SELECT id, numero, zona, estado, capacidad FROM mesas ORDER BY zona, numero")
        
        if not mesas:
            print("[ERROR] No se encontraron mesas en la base de datos")
            return
        
        print("[INFO] Total de mesas encontradas: %s" % len(mesas))
        print()
        
        # Agrupar por zonas
        _ = Counter()
        zonas_detalle = {}
        
        for mesa in mesas:
            zona = mesa['zona'] or 'Sin zona'
            zonas_counter[zona] += 1
            
            if zona not in zonas_detalle:
                zonas_detalle[zona] = []
            
            zonas_detalle[zona].append({
                'id': mesa['id'],
                'numero': mesa['numero'],
                'estado': mesa['estado'],
                'capacidad': mesa['capacidad']
            })
        
        # Mostrar resumen por zonas
        print("[RESUMEN] ZONAS DISPONIBLES:")
        print("-" * 40)
        for zona, cantidad in sorted(zonas_counter.items()):
            print("   {zona}: %s mesas" % cantidad)
        
        print()
        print("[DETALLE] INFORMACION POR ZONA:")
        print("=" * 60)
        
        # Mostrar detalle de cada zona
        for zona in sorted(zonas_detalle.keys()):
            print("\n[ZONA] %s" % zona.upper())
            print("-" * 50)
            
            mesas_zona = zonas_detalle[zona]
            _ = Counter(mesa['estado'] for mesa in mesas_zona)
            
            print("   Total mesas: %s" % len(mesas_zona))
            print("   Estados: %s" % dict(estados_zona))
            print()
            
            # Mostrar cada mesa de la zona
            for mesa in sorted(mesas_zona, key=lambda x: x['numero']):
                _ = {
                    'libre': '[LIBRE]',
                    'ocupada': '[OCUPADA]', 
                    'reservada': '[RESERVADA]',
                    'mantenimiento': '[MANTENIMIENTO]'
                }.get(mesa['estado'], '[DESCONOCIDO]')
                
                print(f"   {estado_simbolo} Mesa {mesa['numero']} (ID: {mesa['id']}) - "
                      f"Estado: {mesa['estado']} - Capacidad: {mesa['capacidad']} personas")
        
        print()
        print("[ANALISIS] EVALUACION DE ZONAS:")
        print("-" * 40)
        
        # Identificar zonas problemáticas o candidatas a eliminación
        _ = []
        zonas_vacias = []
        
        for zona, mesas_zona in zonas_detalle.items():
            # Verificar si todas las mesas están libres (candidatas a eliminación)
            todas_libres = all(mesa['estado'] == 'libre' for mesa in mesas_zona)
            
            # Verificar si hay pocas mesas en la zona
            pocas_mesas = len(mesas_zona) <= 2
            
            if todas_libres and pocas_mesas:
                zonas_problematicas.append(zona)
            
            if len(mesas_zona) == 0:
                zonas_vacias.append(zona)
        
        if zonas_problematicas:
            print("[ATENCION] Zonas candidatas para revision/eliminacion:")
            for zona in zonas_problematicas:
                print("   - {zona}: Pocas mesas (%s) y todas libres" % len(zonas_detalle[zona]))
        
        if zonas_vacias:
            print("[VACIAS] Zonas vacias (sin mesas):")
            for zona in zonas_vacias:
                print("   - %s" % zona)
        
        # Mostrar zonas más utilizadas
        _ = {}
        for zona, mesas_zona in zonas_detalle.items():
            ocupadas = sum(1 for mesa in mesas_zona if mesa['estado'] in ['ocupada', 'reservada'])
            if ocupadas > 0:
                zonas_ocupadas[zona] = ocupadas
        
        if zonas_ocupadas:
            print("\n[ACTIVIDAD] Zonas con mayor actividad:")
            for zona, ocupadas in sorted(zonas_ocupadas.items(), key=lambda x: x[1], reverse=True):
                total_zona = len(zonas_detalle[zona])
                porcentaje = (ocupadas / total_zona) * 100
                print("   - {zona}: {ocupadas}/{total_zona} mesas ocupadas/reservadas (%s%)" % porcentaje:.1f)
        
        print()
        print("=" * 60)
        print("[EXITO] Consulta completada exitosamente")
        
    except Exception as e:
    logging.error("[ERROR] Error al consultar las zonas de mesas: %s", e)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    consultar_zonas_mesas()