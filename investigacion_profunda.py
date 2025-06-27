#!/usr/bin/env python3
"""
Investigación profunda del problema de las tarjetas
"""

import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from ui.modules.tpv_module.components.mesas_area import MesasArea
from services.tpv_service import Mesa

def investigar_problema():
    app = QApplication(sys.argv)
    
    print("🔍 INVESTIGACIÓN PROFUNDA DEL PROBLEMA")
    print("=" * 50)
    
    # Crear mesas de prueba
    mesas = [
        Mesa(1, "1", "Terraza", "libre", 4),
        Mesa(2, "2", "Interior", "ocupada", 6),
        Mesa(3, "3", "Terraza", "reservada", 4),
    ]
    
    # Crear MesasArea
    mesas_area = MesasArea()
    
    print("📊 ESTADO INICIAL (después de __init__):")
    analizar_tarjetas(mesas_area)
    
    print("\n📊 DESPUÉS DE set_mesas:")
    mesas_area.set_mesas(mesas)
    analizar_tarjetas(mesas_area)
    
    print("\n📊 DESPUÉS DE update_ultra_premium_stats:")
    mesas_area.update_ultra_premium_stats()
    analizar_tarjetas(mesas_area)
    
    print("\n📊 DESPUÉS DE update_stats_from_mesas:")
    mesas_area.update_stats_from_mesas()
    analizar_tarjetas(mesas_area)
    
    # Crear ventana para ver visualmente
    window = QMainWindow()
    window.setWindowTitle("🔍 Investigación Visual")
    window.setCentralWidget(mesas_area)
    window.resize(1400, 800)
    window.show()
    
    print("\n✅ VENTANA CREADA - Compara con lo que ves en pantalla")
    
    return app.exec()

def analizar_tarjetas(mesas_area):
    """Analiza el estado actual de las tarjetas"""
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
            layout = widget.layout()
            if layout and layout.count() >= 2:
                # Verificar el segundo elemento (nombre)
                name_item = layout.itemAt(1)
                if name_item and name_item.widget() and isinstance(name_item.widget(), QLabel):
                    actual_text = name_item.widget().text()
                    status = "✅" if actual_text == expected_label else "❌"
                    print(f"  {widget_name}: {status} '{actual_text}' (esperado: '{expected_label}')")
                else:
                    print(f"  {widget_name}: ❌ No se encontró QLabel en posición 1")
            else:
                print(f"  {widget_name}: ❌ Layout inválido")
        else:
            print(f"  {widget_name}: ❌ Widget no existe")

if __name__ == "__main__":
    exit_code = investigar_problema()
    sys.exit(exit_code)