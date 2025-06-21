"""
Script de debug para comparar la visualización de las tarjetas 
entre tests y aplicación principal
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

# Importar las clases del dashboard
from src.ui.modules.dashboard_admin_v3.advanced_metric_card import AdvancedMetricCard
from src.ui.modules.dashboard_admin_v3.admin_metrics_widgets import AdminMetricsSection


class DebugWindow(QMainWindow):
    """Ventana de debug para comparar tarjetas"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Debug - Visualización de Tarjetas")
        self.setGeometry(200, 200, 1200, 800)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        
        # Título
        title = QLabel("🔍 Debug - Comparación de Visualización")
        title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #0f172a;
                padding: 10px;
                background: #f8fafc;
                border-radius: 8px;
                text-align: center;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)
        
        # Layout horizontal para comparar
        comparison_layout = QHBoxLayout()
        
        # Lado izquierdo: Tarjeta individual
        left_section = QWidget()
        left_layout = QVBoxLayout(left_section)
        
        left_title = QLabel("📋 Tarjeta Individual (como en tests)")
        left_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        left_layout.addWidget(left_title)
        
        # Crear tarjeta individual
        single_card = AdvancedMetricCard(
            icon="💰", 
            title="Ventas Diarias", 
            value="€2,450.75", 
            subtitle="vs ayer", 
            trend="+12.5%", 
            color="#10b981"
        )
        single_card.setFixedSize(300, 180)
        left_layout.addWidget(single_card)
        left_layout.addStretch()
        
        # Lado derecho: Sección completa
        right_section = QWidget()
        right_layout = QVBoxLayout(right_section)
        
        right_title = QLabel("📊 Sección Completa (como en app principal)")
        right_title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        right_layout.addWidget(right_title)
        
        # Crear sección de métricas completa
        metrics_section = AdminMetricsSection()
        metrics_section.setMinimumHeight(400)
        right_layout.addWidget(metrics_section)
        
        # Añadir secciones al layout de comparación
        comparison_layout.addWidget(left_section, 1)
        comparison_layout.addWidget(right_section, 2)
        
        main_layout.addLayout(comparison_layout)
        
        # Información de debug
        debug_info = QLabel("🔧 Comparando: Tarjeta individual vs Sección completa")
        debug_info.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #6b7280;
                background: #f1f5f9;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        main_layout.addWidget(debug_info)
        
        print("✅ Ventana de debug creada")
        print("👀 Observa las diferencias entre la tarjeta individual y la sección completa")


def main():
    app = QApplication(sys.argv)
    
    # Crear ventana de debug
    window = DebugWindow()
    window.show()
    
    print("\n🔍 INSTRUCCIONES DE DEBUG:")
    print("1. Observa la tarjeta individual (izquierda)")
    print("2. Observa la sección completa (derecha)")  
    print("3. Compara qué elementos se ven en cada caso")
    print("4. Cierra la ventana cuando termines")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
