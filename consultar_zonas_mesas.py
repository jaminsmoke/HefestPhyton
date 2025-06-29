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
    """Consulta y muestra las zonas de mesas disponibles"""
    try:
        # Inicializar el gestor de base de datos
        db_manager = DatabaseManager()
        
        print("=" * 60)
        print("CONSULTA DE ZONAS DE MESAS DISPONIBLES")
        print("=" * 60)
        
        # Consultar todas las mesas
        mesas = db_manager.query("SELECT id, numero, zona, estado, capacidad FROM mesas ORDER BY zona, numero")
        
        if not mesas:
            print("[ERROR] No se encontraron mesas en la base de datos")
            return
        
        print(f"[INFO] Total de mesas encontradas: {len(mesas)}")
        print()
        
        # Agrupar por zonas
        zonas_counter = Counter()
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
            print(f"   {zona}: {cantidad} mesas")
        
        print()
        print("[DETALLE] INFORMACION POR ZONA:")
        print("=" * 60)
        
        # Mostrar detalle de cada zona
        for zona in sorted(zonas_detalle.keys()):
            print(f"\n[ZONA] {zona.upper()}")
            print("-" * 50)
            
            mesas_zona = zonas_detalle[zona]
            estados_zona = Counter(mesa['estado'] for mesa in mesas_zona)
            
            print(f"   Total mesas: {len(mesas_zona)}")
            print(f"   Estados: {dict(estados_zona)}")
            print()
            
            # Mostrar cada mesa de la zona
            for mesa in sorted(mesas_zona, key=lambda x: x['numero']):
                estado_simbolo = {
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
        zonas_problematicas = []
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
                print(f"   - {zona}: Pocas mesas ({len(zonas_detalle[zona])}) y todas libres")
        
        if zonas_vacias:
            print("[VACIAS] Zonas vacias (sin mesas):")
            for zona in zonas_vacias:
                print(f"   - {zona}")
        
        # Mostrar zonas más utilizadas
        zonas_ocupadas = {}
        for zona, mesas_zona in zonas_detalle.items():
            ocupadas = sum(1 for mesa in mesas_zona if mesa['estado'] in ['ocupada', 'reservada'])
            if ocupadas > 0:
                zonas_ocupadas[zona] = ocupadas
        
        if zonas_ocupadas:
            print("\n[ACTIVIDAD] Zonas con mayor actividad:")
            for zona, ocupadas in sorted(zonas_ocupadas.items(), key=lambda x: x[1], reverse=True):
                total_zona = len(zonas_detalle[zona])
                porcentaje = (ocupadas / total_zona) * 100
                print(f"   - {zona}: {ocupadas}/{total_zona} mesas ocupadas/reservadas ({porcentaje:.1f}%)")
        
        print()
        print("=" * 60)
        print("[EXITO] Consulta completada exitosamente")
        
    except Exception as e:
        print(f"[ERROR] Error al consultar las zonas de mesas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    consultar_zonas_mesas()