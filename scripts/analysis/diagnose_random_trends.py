#!/usr/bin/env python3
"""
Script de diagnóstico para el problema de tendencias aleatorias
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
script_dir = Path(__file__).parent
src_dir = script_dir.parent / "src"
sys.path.insert(0, str(src_dir))

from utils.real_data_manager import RealDataManager
from data.db_manager import DatabaseManager
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_trend_consistency():
    """Probar la consistencia de las tendencias"""
    
    print("="*60)
    print("🔍 DIAGNÓSTICO DE TENDENCIAS ALEATORIAS")
    print("="*60)
    
    # Inicializar componentes
    db_manager = DatabaseManager()
    data_manager = RealDataManager(db_manager)
    
    print("\n📊 Probando consistencia de tendencias (3 iteraciones)...")
    
    results = []
    
    for i in range(3):
        print(f"\n--- Iteración {i+1} ---")
        
        # Obtener métricas
        metrics = data_manager._get_real_metrics_formatted()
        
        iteration_result = {}
        for metric_name, metric_data in metrics.items():
            trend = metric_data.get('trend', 'N/A')
            value = metric_data.get('value', 0)
            
            iteration_result[metric_name] = {
                'value': value,
                'trend': trend
            }
            
            print(f"  {metric_name}: {value} (tendencia: {trend})")
        
        results.append(iteration_result)
        
        if i < 2:  # No esperar en la última iteración
            time.sleep(2)
    
    # Analizar consistencia
    print("\n" + "="*60)
    print("📋 ANÁLISIS DE CONSISTENCIA:")
    print("="*60)
    
    inconsistent_metrics = []
    
    for metric_name in results[0].keys():
        trends = [result[metric_name]['trend'] for result in results]
        values = [result[metric_name]['value'] for result in results]
        
        # Si los valores son iguales pero las tendencias cambian, hay problema
        if len(set(values)) == 1 and len(set(trends)) > 1:
            print(f"❌ {metric_name}: INCONSISTENTE")
            print(f"   Valores: {values} (todos iguales)")
            print(f"   Tendencias: {trends} (cambian aleatoriamente)")
            inconsistent_metrics.append(metric_name)
        else:
            print(f"✅ {metric_name}: CONSISTENTE")
    
    if inconsistent_metrics:
        print(f"\n🚨 PROBLEMA ENCONTRADO:")
        print(f"   {len(inconsistent_metrics)} métricas con tendencias aleatorias")
        print(f"   Métricas afectadas: {', '.join(inconsistent_metrics)}")
        
        # Diagnosticar la causa
        print(f"\n🔍 DIAGNÓSTICO DE LA CAUSA:")
        test_historical_queries(data_manager)
    else:
        print(f"\n✅ TODAS LAS TENDENCIAS SON CONSISTENTES")

def test_historical_queries(data_manager):
    """Probar las consultas históricas"""
    
    print("\n📋 Probando consultas históricas...")
    
    # Probar algunas métricas
    test_metrics = ['ventas_diarias', 'comandas_activas', 'ocupacion_mesas']
    
    for metric in test_metrics:
        print(f"\n--- {metric} ---")
        
        # Llamar varias veces la consulta histórica
        for i in range(3):
            historical_value = data_manager._get_historical_metric_value(metric)
            print(f"  Consulta {i+1}: {historical_value}")
            time.sleep(0.5)

if __name__ == "__main__":
    try:
        test_trend_consistency()
    except Exception as e:
        print(f"❌ Error en diagnóstico: {e}")
        import traceback
        traceback.print_exc()
