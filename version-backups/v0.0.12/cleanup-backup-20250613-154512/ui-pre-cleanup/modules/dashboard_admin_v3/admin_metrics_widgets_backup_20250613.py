"""
Widgets de métricas RESPONSIVE para Dashboard Admin v3
Solo con AdvancedMetricCard - versión responsive que se ajusta al contenedor
"""

import logging
import random
from typing import Optional
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont

from .dashboard_config import METRICS_CONFIG, CONTAINER_CONFIG
from .advanced_metric_card import AdvancedMetricCard

logger = logging.getLogger(__name__)


class AdminMetricsSection(QWidget):
    """Sección de métricas RESPONSIVE con grid adaptativo 3x2"""
    
    metrics_updated = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.metric_cards = {}
        self.setup_ui()
          # Asegurar visibilidad        self.setVisible(True)
        self.show()
        
        # Timer para simular actualizaciones
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.simulate_data_update)
        self.update_timer.start(5000)
        
    def setup_ui(self):
        """Configuración RESPONSIVE de la interfaz - Grid adaptativo 3x2"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(10)  # Reducir spacing principal
        
        # Título
        title = QLabel("📈 Métricas Clave")
        title.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 8px;
                background: transparent;
            }
        """)
        main_layout.addWidget(title)
        
        # Contenedor de tarjetas RESPONSIVE (sin altura fija)
        cards_container = QFrame()
        cards_container.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        # ELIMINAMOS setFixedHeight para que se ajuste automáticamente
        
        # Layout del contenedor
        container_layout = QVBoxLayout(cards_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Crear grid RESPONSIVE
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(15)  # Spacing entre tarjetas
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Métricas principales (6 tarjetas en 3x2)
        metrics_data = [
            # Fila 1
            ("💰", "Ventas", "€2,450", "Hoy vs Ayer", "+12%", "#10b981"),
            ("🏨", "Ocupación", "75%", "15/20 Mesas", "+3", "#3b82f6"),
            ("⏱️", "Tiempo", "45 min", "Promedio", "-5 min", "#8b5cf6"),
            
            # Fila 2  
            ("⭐", "Satisfacción", "4.8/5", "Clientes", "+0.2", "#f59e0b"),
            ("📋", "Órdenes", "23", "Activas", "+7", "#ef4444"),
            ("🎫", "Ticket", "€38.50", "Promedio", "+€3.20", "#06b6d4"),
        ]
          # Crear tarjetas RESPONSIVE
        for i, (icon, title, value, subtitle, trend, color) in enumerate(metrics_data):
            card = AdvancedMetricCard(icon, title, value, subtitle, trend, color)
            
            # TAMAÑO RESPONSIVE: se ajusta al contenedor disponible
            # Mínimo 250x160, pero crece con el contenedor
            card.setMinimumSize(250, 160)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            card.setVisible(True)
            card.show()
            
            self.metric_cards[title.lower().replace(' ', '_')] = card
            
            row = i // 3  # 3 columnas
            col = i % 3   
            grid_layout.addWidget(card, row, col)
            
        # Configurar grid RESPONSIVE
        for col in range(3):
            grid_layout.setColumnStretch(col, 1)  # Todas las columnas se expanden igual
            grid_layout.setColumnMinimumWidth(col, 250)  # Ancho mínimo
            
        for row in range(2):
            grid_layout.setRowStretch(row, 1)  # Todas las filas se expanden igual
            grid_layout.setRowMinimumHeight(row, 160)  # Alto mínimo
              # Añadir grid al contenedor
        container_layout.addWidget(grid_widget, stretch=1)  # stretch=1 para ocupar todo el espacio
        
        # Añadir contenedor al layout principal  
        main_layout.addWidget(cards_container, stretch=1)  # stretch=1 para expandir
        
        print("✅ AdminMetricsSection RESPONSIVE con 6 tarjetas visibles")
        
    def simulate_data_update(self):
        """Simula actualización de datos realistas"""
        updates = {
            'ventas': (f"€{random.randint(2200, 2800)}", f"+{random.randint(8, 15)}%"),
            'ocupación': (f"{random.randint(65, 85)}%", f"+{random.randint(1, 5)}"),
            'tiempo': (f"{random.randint(40, 50)} min", f"-{random.randint(2, 8)} min"),
            'satisfacción': (f"{random.uniform(4.5, 4.9):.1f}/5", f"+{random.uniform(0.1, 0.3):.1f}"),
            'órdenes': (f"{random.randint(18, 28)}", f"+{random.randint(3, 8)}"),
            'ticket': (f"€{random.uniform(35, 42):.2f}", f"+€{random.uniform(1, 4):.2f}"),
        }
        
        for card_key, (new_value, new_trend) in updates.items():
            if card_key in self.metric_cards:
                self.metric_cards[card_key].update_value(new_value, new_trend)
        
        self.metrics_updated.emit()
        logger.debug("Métricas actualizadas automáticamente")
        
    def get_metrics_data(self):
        """Retorna datos actuales de métricas"""
        data = {}
        for key, card in self.metric_cards.items():
            if hasattr(card, 'value_label') and card.value_label:
                data[key] = card.value_label.text()
        return data
