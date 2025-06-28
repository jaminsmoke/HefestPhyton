#!/usr/bin/env python3
"""
Diagnóstico profundo de las tarjetas para identificar el problema exacto
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from PyQt6.QtWidgets import QApplication, QLabel
from ui.modules.tpv_module.components.mesas_area import MesasArea
from services.tpv_service import Mesa

def debug_tarjetas():
    app = QApplication(sys.argv)
    
    # Crear mesas de prueba
    mesas = [
        Mesa(1, "1", "Terraza", "libre", 4),
        Mesa(2, "2", "Interior", "ocupada", 6),
        Mesa(3, "3", "Terraza", "reservada", 4),
    ]
    
    # Crear MesasArea
    mesas_area = MesasArea()
    mesas_area.set_mesas(mesas)
    
    print("🔍 DIAGNÓSTICO PROFUNDO DE TARJETAS")
    print("=" * 50)
    
    if hasattr(mesas_area, 'stats_widgets'):
        for i, stat_info in enumerate(mesas_area.stats_widgets):
            print(f"\n📊 TARJETA {i+1}: {stat_info.get('type', 'N/A')}")
            print("-" * 30)
            
            widget = stat_info.get('widget')
            if widget and widget.layout():
                layout = widget.layout()
                print(f"Layout items: {layout.count()}")
                
                for j in range(layout.count()):
                    item = layout.itemAt(j)
                    if item and item.widget():
                        w = item.widget()
                        if isinstance(w, QLabel):
                            text = w.text()
                            print(f"  [{j}] QLabel: '{text}'")
                            
                            # Verificar si contiene el nombre esperado
                            expected_label = stat_info.get('label', '')
                            if expected_label.lower() in text.lower():
                                print(f"      ✅ Contiene el nombre esperado: '{expected_label}'")
                            else:
                                print(f"      ❌ NO contiene el nombre esperado: '{expected_label}'")
    
    # Ahora probar actualización manual paso a paso
    print("\n🔄 PROBANDO ACTUALIZACIÓN MANUAL")
    print("=" * 50)
    
    # Simular actualización de la primera tarjeta (zonas)
    if hasattr(mesas_area, 'zonas_widget'):
        print("\n🎯 ACTUALIZANDO TARJETA ZONAS:")
        widget = mesas_area.zonas_widget
        layout = widget.layout()
        
        print("ANTES de actualizar:")
        for j in range(layout.count()):
            item = layout.itemAt(j)
            if item and item.widget() and isinstance(item.widget(), QLabel):
                print(f"  [{j}] '{item.widget().text()}'")
        
        # Intentar actualizar usando el método actual
        mesas_area._update_stat_widget(widget, "3")
        
        print("DESPUÉS de actualizar:")
        for j in range(layout.count()):
            item = layout.itemAt(j)
            if item and item.widget() and isinstance(item.widget(), QLabel):
                print(f"  [{j}] '{item.widget().text()}'")
    
    return 0

if __name__ == "__main__":
    debug_tarjetas()