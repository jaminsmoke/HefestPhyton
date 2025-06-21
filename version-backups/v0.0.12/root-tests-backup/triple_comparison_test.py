#!/usr/bin/env python3
"""
Test de 3 versiones: Básica vs AdvancedMetricCard vs UltraSimple
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

# Importar las 3 versiones
from ui.modules.dashboard_admin_v3.advanced_metric_card import AdvancedMetricCard
from ui.modules.dashboard_admin_v3.ultra_simple_metric_card import UltraSimpleMetricCard

class Triple_Comparison_Test(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 TRIPLE COMPARACIÓN - Básica vs Advanced vs UltraSimple")
        self.setMinimumSize(1400, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Título
        title = QLabel("🔍 TRIPLE COMPARACIÓN DE TARJETAS")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px; color: #0f172a;")
        layout.addWidget(title)
        
        # Layout horizontal para las 3 versiones
        comparison_layout = QHBoxLayout()
        
        # VERSIÓN 1: Básica (que funciona)
        basic_container = QWidget()
        basic_layout = QVBoxLayout(basic_container)
        
        basic_title = QLabel("✅ BÁSICA (Funciona)")
        basic_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        basic_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #10b981; margin: 10px;")
        basic_layout.addWidget(basic_title)
        
        basic_card = self.create_basic_card()
        basic_layout.addWidget(basic_card)
        
        # VERSIÓN 2: AdvancedMetricCard (problemática)
        advanced_container = QWidget()
        advanced_layout = QVBoxLayout(advanced_container)
        
        advanced_title = QLabel("❌ ADVANCED (Problemática)")
        advanced_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        advanced_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #ef4444; margin: 10px;")
        advanced_layout.addWidget(advanced_title)
        
        advanced_card = AdvancedMetricCard("💰", "Advanced", "€2,450", "Test", "+12%", "#10b981")
        advanced_layout.addWidget(advanced_card)
        
        # VERSIÓN 3: UltraSimple (nueva)
        ultra_container = QWidget()
        ultra_layout = QVBoxLayout(ultra_container)
        
        ultra_title = QLabel("🧪 ULTRA SIMPLE (Prueba)")
        ultra_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ultra_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #3b82f6; margin: 10px;")
        ultra_layout.addWidget(ultra_title)
        
        ultra_card = UltraSimpleMetricCard("💰", "UltraSimple", "€2,450", "Test", "+12%", "#10b981")
        ultra_layout.addWidget(ultra_card)
        
        # Añadir las 3 versiones al layout
        comparison_layout.addWidget(basic_container)
        comparison_layout.addWidget(advanced_container)
        comparison_layout.addWidget(ultra_container)
        
        layout.addLayout(comparison_layout)
        
        # Info
        info = QLabel("Compara cuál se ve mejor: ✅ Básica | ❌ Advanced | 🧪 Ultra Simple")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("font-size: 12px; margin: 10px; color: #64748b;")
        layout.addWidget(info)
        
    def create_basic_card(self):
        """Crear tarjeta básica que funciona bien"""
        card = QWidget()
        card.setFixedSize(280, 190)
        card.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 2px solid #10b981;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Icon
        icon = QLabel("💰")
        icon.setStyleSheet("font-size: 24px;")
        layout.addWidget(icon)
        
        # Title
        title = QLabel("Básica")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #0f172a;")
        layout.addWidget(title)
        
        # Value
        value = QLabel("€2,450")
        value.setStyleSheet("font-size: 24px; font-weight: bold; color: #10b981;")
        layout.addWidget(value)
        
        # Subtitle
        subtitle = QLabel("Test")
        subtitle.setStyleSheet("font-size: 12px; color: #64748b;")
        layout.addWidget(subtitle)
        
        # Trend
        trend = QLabel("+12%")
        trend.setStyleSheet("""
            font-size: 12px; 
            font-weight: bold; 
            color: #10b981;
            background-color: #10b98120;
            padding: 4px 8px;
            border-radius: 8px;
        """)
        layout.addWidget(trend)
        
        layout.addStretch()
        
        return card

def main():
    app = QApplication(sys.argv)
    
    window = Triple_Comparison_Test()
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
