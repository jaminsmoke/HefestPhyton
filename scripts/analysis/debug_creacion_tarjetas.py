#!/usr/bin/env python3
"""
Debug específico del momento de creación de las tarjetas
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from PyQt6.QtWidgets import QApplication, QLabel
from ui.modules.tpv_module.components.mesas_area import MesasArea

def debug_creacion():
    app = QApplication(sys.argv)
    
    print("🔍 DEBUG CREACIÓN DE TARJETAS")
    print("=" * 40)
    
    # Crear MesasArea
    mesas_area = MesasArea()
    
    # Probar crear una tarjeta manualmente
    print("\n🎯 CREANDO TARJETA MANUAL:")
    test_widget = mesas_area.create_ultra_premium_stat("📍", "Zonas", "0", "#8b5cf6", "#f3e8ff", size=110, height=120)
    
    # Analizar la tarjeta creada
    layout = test_widget.layout()
    print(f"Layout items: {layout.count()}")
    
    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item and item.widget() and isinstance(item.widget(), QLabel):
            label = item.widget()
            print(f"  [{i}] QLabel: '{label.text()}'")
    
    print("\n🔍 ANALIZANDO TARJETAS EXISTENTES:")
    
    # Verificar las tarjetas ya creadas
    widgets_to_check = [
        ('zonas_widget', 'Zonas'),
        ('mesas_total_widget', 'Total'),
        ('mesas_libres_widget', 'Libres'),
        ('mesas_ocupadas_widget', 'Ocupadas'),
        ('mesas_reservadas_widget', 'Reservadas')
    ]
    
    for widget_name, expected_label in widgets_to_check:
        if hasattr(mesas_area, widget_name):
            widget = getattr(mesas_area, widget_name)
            print(f"\n📊 {widget_name}:")
            
            layout = widget.layout()
            if layout:
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and item.widget() and isinstance(item.widget(), QLabel):
                        label = item.widget()
                        text = label.text()
                        print(f"  [{i}] '{text}'")
                        
                        if i == 1:  # El segundo debería ser el nombre
                            if text == expected_label:
                                print(f"      ✅ Correcto: '{expected_label}'")
                            else:
                                print(f"      ❌ Incorrecto: esperaba '{expected_label}', obtuvo '{text}'")
    
    return 0

if __name__ == "__main__":
    debug_creacion()