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
from .advanced_metric_card_modern import AdvancedMetricCardModern

logger = logging.getLogger(__name__)


class AdminMetricsSection(QWidget):
    """Sección de métricas RESPONSIVE con grid adaptativo 3x2"""
    
    metrics_updated = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.metric_cards = {}
        self.setup_ui()
        
        # Asegurar visibilidad
        self.setVisible(True)
        self.show()
        
        # Timer para simular actualizaciones
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.simulate_data_update)
        self.update_timer.start(5000)
        
    def setup_ui(self):
        """Configuración RESPONSIVE de la interfaz - Grid adaptativo 3x2"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 5, 15, 10)  # Márgenes reducidos
        main_layout.setSpacing(5)  # Spacing reducido
        
        # Título más compacto
        title = QLabel("📈 Métricas Clave")
        title.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: 700;
                color: #0f172a;
                margin-bottom: 5px;
                background: transparent;
            }
        """)
        main_layout.addWidget(title)
        
        # Contenedor de tarjetas RESPONSIVE
        cards_container = QFrame()
        cards_container.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)
        
        # Layout del contenedor
        container_layout = QVBoxLayout(cards_container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Crear grid RESPONSIVE
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setSpacing(10)  # Spacing entre tarjetas
        grid_layout.setContentsMargins(0, 0, 0, 0)

        # Métricas principales con datos más relevantes y iconos mejorados
        metrics_data = [
            # Fila 1
            ("💰", "Ventas Diarias", "€2,450.75", "vs ayer", "+12.5%", "#10b981"),
            ("🏨", "Ocupación Mesa", "15/20", "mesas ocupadas", "+3 mesas", "#3b82f6"),
            ("⏱️", "Tiempo Servicio", "12 min", "promedio", "-3 min", "#8b5cf6"),
            
            # Fila 2  
            ("⭐", "Satisfacción", "4.8/5", "rating clientes", "+0.2 pts", "#f59e0b"),
            ("📋", "Órdenes Activas", "23", "en preparación", "+7 nuevas", "#ef4444"),
            ("🎫", "Ticket Medio", "€38.75", "por cliente", "+€3.25", "#06b6d4"),
        ]
          # Crear tarjetas ROBUSTAS con mejor diferenciación
        for i, (icon, title, value, subtitle, trend, color) in enumerate(metrics_data):
            card = AdvancedMetricCardModern(icon, title, value, subtitle, trend, color)
              # TAMAÑO FIJO: la versión robusta maneja su propio tamaño
            # card.setMinimumSize(240, 140)  # Ya no necesario
            # card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)  # Ya no necesario
            card.setVisible(True)
            card.show()
            
            self.metric_cards[title.lower().replace(' ', '_')] = card
            
            row = i // 3  # 3 columnas
            col = i % 3   
            grid_layout.addWidget(card, row, col)        # Configurar grid para TARJETAS MODERNAS (280-320 x 160-200)
        for col in range(3):
            grid_layout.setColumnStretch(col, 1)  # Expansión equilibrada
            grid_layout.setColumnMinimumWidth(col, 280)  # Ancho mínimo para tarjetas modernas
            
        for row in range(2):
            grid_layout.setRowStretch(row, 1)  # Expansión equilibrada  
            grid_layout.setRowMinimumHeight(row, 160)  # Alto mínimo para tarjetas modernas
            grid_layout.setRowMinimumHeight(row, 160)  # Alto fijo de tarjetas
            
        # Añadir grid al contenedor
        container_layout.addWidget(grid_widget, stretch=1)
        
        # Añadir contenedor al layout principal  
        main_layout.addWidget(cards_container, stretch=1)
        
        print("✅ AdminMetricsSection RESPONSIVE con métricas mejoradas")
        
    def simulate_data_update(self):
        """Simula actualización de datos realistas"""
        updates = {
            'ventas_diarias': (f"€{random.randint(2200, 2800):.2f}", f"+{random.randint(8, 15):.1f}%"),
            'ocupación_mesa': (f"{random.randint(12, 18)}/20", f"+{random.randint(1, 4)} mesas"),
            'tiempo_servicio': (f"{random.randint(10, 15)} min", f"-{random.randint(1, 5)} min"),
            'satisfacción': (f"{random.uniform(4.5, 4.9):.1f}/5", f"+{random.uniform(0.1, 0.3):.1f} pts"),
            'órdenes_activas': (f"{random.randint(18, 28)}", f"+{random.randint(3, 8)} nuevas"),
            'ticket_medio': (f"€{random.uniform(35, 42):.2f}", f"+€{random.uniform(1, 4):.2f}"),
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
