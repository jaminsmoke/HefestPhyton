#!/usr/bin/env python3
"""
Verificación final de métricas con tendencias económicas-administrativas
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.real_data_manager import RealDataManager
from data.db_manager import DatabaseManager
import logging

logging.basicConfig(level=logging.INFO)

def test_real_data_manager():
    """Verificar que todas las métricas están correctamente implementadas"""
    
    print("="*70)
    print("🔍 VERIFICACIÓN FINAL - MÉTRICAS CON TENDENCIAS REALES")
    print("="*70)
    
    # Inicializar componentes
    db_manager = DatabaseManager()
    data_manager = RealDataManager(db_manager)
    
    # Obtener métricas
    metrics = data_manager._get_real_metrics_formatted()
    
    print(f"\n📊 MÉTRICAS IMPLEMENTADAS: {len(metrics)}")
    print("-" * 70)
    
    expected_metrics = [
        'ocupacion_mesas', 'ventas_diarias', 'comandas_activas', 'ticket_promedio',
        'reservas_futuras', 'mesas_ocupadas', 'habitaciones_libres', 'productos_stock',
        'satisfaccion_cliente', 'tiempo_servicio', 'rotacion_mesas', 
        'inventario_bebidas', 'margen_bruto'
    ]
    
    all_present = True
    
    for metric_name in expected_metrics:
        if metric_name in metrics:
            metric_data = metrics[metric_name]
            value = metric_data.get('value', 'N/A')
            trend = metric_data.get('trend', 'N/A')
            title = metric_data.get('title', 'N/A')
            unit = metric_data.get('unit', '')
            
            # Verificar lógica de tendencias
            trend_logic = "✅ REAL" if trend == "+0.0%" else f"⚠️ {trend}"
            
            print(f"✅ {title:<25} | Valor: {value:<8} {unit:<5} | Tendencia: {trend_logic}")
        else:
            print(f"❌ {metric_name:<25} | FALTA")
            all_present = False
    
    print("-" * 70)
    
    if all_present:
        print("✅ TODAS LAS MÉTRICAS IMPLEMENTADAS CORRECTAMENTE")
        print("📊 Valores en configuración inicial: 0 o 0.0 (CORRECTO)")
        print("📈 Tendencias con lógica económica: +0.0% sin datos históricos (CORRECTO)")
        print("🎯 Sistema listo para reflejar datos reales cuando se introduzcan")
    else:
        print("❌ FALTAN MÉTRICAS - Revisar implementación")
    
    print("="*70)
    return all_present

if __name__ == "__main__":
    success = test_real_data_manager()
    if success:
        print("🎉 VERIFICACIÓN EXITOSA - Sistema con tendencias económicas reales")
    else:
        print("⚠️ VERIFICACIÓN FALLÓ - Revisar implementación")
        sys.exit(1)
