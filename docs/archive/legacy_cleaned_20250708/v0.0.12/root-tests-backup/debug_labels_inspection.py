# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from src.ui.modules.dashboard_admin_v3.advanced_metric_card import AdvancedMetricCard

"""
Test específico para verificar que los QLabels se crean correctamente
"""

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))




class DebugLabelsWindow(QMainWindow):
    """Ventana para inspeccionar los QLabels dentro de las tarjetas"""
    
    def __init__(self):
        """TODO: Add docstring"""
        super().__init__()
        self.setWindowTitle("Debug - Inspección de QLabels")
        self.setGeometry(200, 200, 800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        _ = QVBoxLayout(central_widget)
        
        # Crear tarjeta de test
        self.test_card = AdvancedMetricCard(
            _ = "💰", 
            title="Ventas Test", 
            _ = "€1,234.56", 
            subtitle="Debug test", 
            _ = "+5.2%", 
            color="#10b981"        )
        
        main_layout.addWidget(self.test_card)
        
        # FORZAR VISIBILIDAD ABSOLUTA
        self.test_card.setVisible(True)
        self.test_card.show()
        
        # Información de debug
        self.debug_info()
        
    def debug_info(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Muestra información de debug sobre los widgets"""
        print("\n🔍 DEBUG INFO - Inspección de widgets:")
        print("Tarjeta creada: %s" % self.test_card)
        print("Tarjeta visible: %s" % self.test_card.isVisible())
        print("Tamaño tarjeta: %s" % self.test_card.size())
        
        # Buscar todos los QLabel dentro de la tarjeta
        labels = self.test_card.findChildren(QLabel)
        print("\n📋 QLabels encontrados: %s" % len(labels))
        
        for i, label in enumerate(labels):
            print("  Label %s:" % i % 1)
            print("    Texto: '%s'" % label.text())
            print("    Visible: %s" % label.isVisible())
            print("    Tamaño: %s" % label.size())
            print("    Posición: %s" % label.pos())
            print("    StyleSheet: %s..." % label.styleSheet()[:100])
            print()
        
        # Verificar si value_label existe
        if hasattr(self.test_card, 'value_label') and self.test_card.value_label:
            print("✅ value_label existe: %s" % self.test_card.value_label.text())
        else:
            print("❌ value_label NO existe")
            
        # Verificar si trend_label existe
        if hasattr(self.test_card, 'trend_label') and self.test_card.trend_label:
            print("✅ trend_label existe: %s" % self.test_card.trend_label.text())
        else:
            print("❌ trend_label NO existe")


def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    _ = QApplication(sys.argv)
    
    # Crear ventana de debug
    window = DebugLabelsWindow()
    window.show()
    
    print("🔍 Inspecciona la consola para ver los detalles de los widgets")
    print("📋 Cierra la ventana cuando termines")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
