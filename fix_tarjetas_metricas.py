#!/usr/bin/env python3
"""
Parche específico para corregir el problema de las tarjetas de métricas
"""

import sys
import os

# Agregar src al path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from ui.modules.tpv_module.components.mesas_area import MesasArea
from services.tpv_service import Mesa

def fix_update_stat_widget_method():
    """Aplica el parche al método _update_stat_widget"""
    
    def new_update_stat_widget(self, widget, new_value: str):
        """🔧 Versión corregida del método _update_stat_widget"""
        try:
            if not widget or not hasattr(widget, 'layout') or not widget.layout():
                return
            
            layout = widget.layout()
            
            # Buscar específicamente el QLabel del valor (el tercero en orden)
            labels_found = []
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget() and isinstance(item.widget(), QLabel):
                    labels_found.append(item.widget())
            
            # El tercer QLabel es el valor
            if len(labels_found) >= 3:
                value_label = labels_found[2]  # Índice 2 = tercer elemento
                value_label.setText(str(new_value))
                value_label.update()
                print(f"✅ Actualizado valor a: '{new_value}'")
            else:
                print(f"❌ No se encontraron suficientes QLabels: {len(labels_found)}")
                
        except Exception as e:
            print(f"❌ Error en _update_stat_widget: {e}")
    
    # Aplicar el parche
    MesasArea._update_stat_widget = new_update_stat_widget
    print("✅ Parche aplicado al método _update_stat_widget")

def test_fix():
    """Prueba la corrección"""
    app = QApplication(sys.argv)
    
    # Aplicar el parche
    fix_update_stat_widget_method()
    
    # Crear mesas de prueba
    mesas = [
        Mesa(1, "1", "Terraza", "libre", 4),
        Mesa(2, "2", "Interior", "ocupada", 6),
        Mesa(3, "3", "Terraza", "reservada", 4),
        Mesa(4, "4", "Interior", "libre", 2),
        Mesa(5, "5", "Privada", "ocupada", 8),
    ]
    
    # Crear MesasArea
    mesas_area = MesasArea()
    mesas_area.set_mesas(mesas)
    
    print("\n🔄 PROBANDO CORRECCIÓN:")
    print("-" * 30)
    
    # Forzar actualización
    mesas_area.update_ultra_premium_stats()
    
    # Verificar resultados
    print("\n📊 VALORES DESPUÉS DE LA CORRECCIÓN:")
    if hasattr(mesas_area, 'stats_widgets'):
        for stat_info in mesas_area.stats_widgets:
            widget = stat_info.get('widget')
            if widget and widget.layout():
                layout = widget.layout()
                labels = []
                for i in range(layout.count()):
                    item = layout.itemAt(i)
                    if item and item.widget() and isinstance(item.widget(), QLabel):
                        labels.append(item.widget())
                
                if len(labels) >= 3:
                    tipo = stat_info.get('type', 'N/A')
                    valor = labels[2].text()
                    print(f"  {tipo}: '{valor}'")
    
    # Mostrar ventana
    window = QMainWindow()
    window.setWindowTitle("🔧 Test Corrección Tarjetas")
    window.setCentralWidget(mesas_area)
    window.resize(1400, 800)
    window.show()
    
    print("\n✅ CORRECCIÓN APLICADA - Revisa la ventana")
    return app.exec()

if __name__ == "__main__":
    exit_code = test_fix()
    sys.exit(exit_code)