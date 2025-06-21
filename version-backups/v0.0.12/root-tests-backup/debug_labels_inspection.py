"""
Test específico para verificar que los QLabels se crean correctamente
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

from src.ui.modules.dashboard_admin_v3.advanced_metric_card import AdvancedMetricCard


class DebugLabelsWindow(QMainWindow):
    """Ventana para inspeccionar los QLabels dentro de las tarjetas"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Debug - Inspección de QLabels")
        self.setGeometry(200, 200, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Crear tarjeta de test
        self.test_card = AdvancedMetricCard(
            icon="💰", 
            title="Ventas Test", 
            value="€1,234.56", 
            subtitle="Debug test", 
            trend="+5.2%", 
            color="#10b981"        )
        
        main_layout.addWidget(self.test_card)
        
        # FORZAR VISIBILIDAD ABSOLUTA
        self.test_card.setVisible(True)
        self.test_card.show()
        
        # Información de debug
        self.debug_info()
        
    def debug_info(self):
        """Muestra información de debug sobre los widgets"""
        print("\n🔍 DEBUG INFO - Inspección de widgets:")
        print(f"Tarjeta creada: {self.test_card}")
        print(f"Tarjeta visible: {self.test_card.isVisible()}")
        print(f"Tamaño tarjeta: {self.test_card.size()}")
        
        # Buscar todos los QLabel dentro de la tarjeta
        labels = self.test_card.findChildren(QLabel)
        print(f"\n📋 QLabels encontrados: {len(labels)}")
        
        for i, label in enumerate(labels):
            print(f"  Label {i+1}:")
            print(f"    Texto: '{label.text()}'")
            print(f"    Visible: {label.isVisible()}")
            print(f"    Tamaño: {label.size()}")
            print(f"    Posición: {label.pos()}")
            print(f"    StyleSheet: {label.styleSheet()[:100]}...")
            print()
        
        # Verificar si value_label existe
        if hasattr(self.test_card, 'value_label') and self.test_card.value_label:
            print(f"✅ value_label existe: {self.test_card.value_label.text()}")
        else:
            print("❌ value_label NO existe")
            
        # Verificar si trend_label existe
        if hasattr(self.test_card, 'trend_label') and self.test_card.trend_label:
            print(f"✅ trend_label existe: {self.test_card.trend_label.text()}")
        else:
            print("❌ trend_label NO existe")


def main():
    app = QApplication(sys.argv)
    
    # Crear ventana de debug
    window = DebugLabelsWindow()
    window.show()
    
    print("🔍 Inspecciona la consola para ver los detalles de los widgets")
    print("📋 Cierra la ventana cuando termines")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
