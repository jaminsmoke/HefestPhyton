"""
DEBUG: Comparar AdvancedMetricCard vs tarjetas básicas
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

from src.ui.modules.dashboard_admin_v3.advanced_metric_card import AdvancedMetricCard

class BasicMetricCard(QWidget):
    """Tarjeta básica que funciona bien"""
    
    def __init__(self, icon="💰", title="Ventas", value="€2,450", color="#10b981"):
        super().__init__()
        self.setFixedSize(280, 190)
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0f172a;")
        layout.addWidget(title_label)
        
        # Value
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
        layout.addWidget(value_label)

class DebugWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DEBUG: Advanced vs Basic Cards")
        self.setFixedSize(600, 250)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Tarjeta básica (que funciona)
        basic_container = QVBoxLayout()
        basic_title = QLabel("BÁSICA (funciona)")
        basic_title.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        basic_container.addWidget(basic_title)
        
        basic_card = BasicMetricCard("💰", "Ventas", "€2,450", "#10b981")
        basic_container.addWidget(basic_card)
        
        basic_widget = QWidget()
        basic_widget.setLayout(basic_container)
        layout.addWidget(basic_widget)
        
        # Tarjeta avanzada (problema)
        advanced_container = QVBoxLayout()
        advanced_title = QLabel("AVANZADA (problema)")
        advanced_title.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        advanced_container.addWidget(advanced_title)
        
        advanced_card = AdvancedMetricCard("💰", "Ventas", "€2,450", "Hoy vs Ayer", "+12%", "#10b981")
        advanced_container.addWidget(advanced_card)
        
        advanced_widget = QWidget()
        advanced_widget.setLayout(advanced_container)
        layout.addWidget(advanced_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DebugWindow()
    window.show()
    
    print("=== DEBUG VISUAL ===")
    print("Básica: estructura simple")
    print("Avanzada: estructura compleja")
    print("===================")
    
    app.exec()
