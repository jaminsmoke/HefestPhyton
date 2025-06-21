"""
Componente TPVDashboard - Dashboard de métricas del TPV
Versión: v0.0.13
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from services.tpv_service import TPVService

logger = logging.getLogger(__name__)


class TPVDashboard(QWidget):
    """Dashboard con métricas del TPV mejorado y dinámico"""
    
    def __init__(self, tpv_service: Optional[TPVService] = None, parent=None):
        super().__init__(parent)
        self.tpv_service = tpv_service
        self.metric_cards = {}
        self.setup_ui()
        
        # Timer para actualizar métricas
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self.update_metrics)
        self.metrics_timer.start(30000)  # Actualizar cada 30 segundos
        
        # Actualizar métricas iniciales
        self.update_metrics()
        
    def setup_ui(self):
        """Configura la interfaz del dashboard"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Métricas dinámicas del día
        metrics_config = [
            ("mesas_activas", "🍽️", "Mesas Ocupadas", "0/0", "#2196f3"),
            ("ventas_dia", "💰", "Ventas Hoy", "€0.00", "#4caf50"), 
            ("comandas_activas", "📝", "Comandas Activas", "0", "#ff9800"),
            ("tiempo_promedio", "⏱️", "Tiempo Prom.", "0min", "#9c27b0")
        ]
        
        for metric_key, icon, title, default_value, color in metrics_config:
            metric_widget = self.create_metric_card(metric_key, icon, title, default_value, color)
            self.metric_cards[metric_key] = metric_widget
            layout.addWidget(metric_widget)
            
        layout.addStretch()
        
    def create_metric_card(self, key: str, icon: str, title: str, value: str, color: str) -> QWidget:
        """Crea una tarjeta de métrica mejorada"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 12px;
                padding: 12px;
                margin: 2px;
            }}
            QFrame:hover {{
                background-color: #f8f9fa;
                border-width: 3px;
            }}
            QLabel {{
                border: none;
                background-color: transparent;
            }}
        """)
        card.setFixedSize(160, 100)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Header con icono y título
        header_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 20px; color: {color};")
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 11px; font-weight: bold; color: {color};")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Valor principal
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        value_label.setFont(font)
        value_label.setStyleSheet(f"color: {color};")
        layout.addWidget(value_label)
        
        # Guardar referencia al label del valor para actualizaciones
        setattr(card, 'value_label', value_label)
        setattr(card, 'metric_key', key)
        
        return card
        
    def update_metrics(self):
        """Actualiza las métricas en tiempo real con datos del servicio"""
        if not self.tpv_service:
            logger.debug("No hay servicio TPV disponible para actualizar métricas")
            return
            
        try:
            # Obtener datos actuales
            mesas = self.tpv_service.get_mesas()
            comandas_activas = self.tpv_service.get_comandas_activas()
            
            # Calcular métricas
            mesas_ocupadas = len([m for m in mesas if m.estado == "ocupada"])
            total_mesas = len(mesas)
            total_comandas = len(comandas_activas)
            
            # Calcular ventas del día (suma de totales de comandas)
            ventas_dia = sum(comanda.total for comanda in comandas_activas)
            
            # Calcular tiempo promedio (placeholder - sería más complejo en implementación real)
            tiempo_promedio = "12min" if comandas_activas else "0min"
            
            # Actualizar tarjetas
            self.update_metric_card("mesas_activas", f"{mesas_ocupadas}/{total_mesas}")
            self.update_metric_card("ventas_dia", f"€{ventas_dia:.2f}")
            self.update_metric_card("comandas_activas", str(total_comandas))
            self.update_metric_card("tiempo_promedio", tiempo_promedio)
            
            logger.debug("Métricas del dashboard TPV actualizadas")
            
        except Exception as e:
            logger.error(f"Error actualizando métricas del dashboard: {e}")
            
    def update_metric_card(self, metric_key: str, new_value: str):
        """Actualiza el valor de una tarjeta específica"""
        if metric_key in self.metric_cards:
            card = self.metric_cards[metric_key]
            value_label = getattr(card, 'value_label', None)
            if value_label:
                value_label.setText(new_value)
                
    def set_service(self, tpv_service: TPVService):
        """Establece el servicio TPV"""
        self.tpv_service = tpv_service
        self.update_metrics()
