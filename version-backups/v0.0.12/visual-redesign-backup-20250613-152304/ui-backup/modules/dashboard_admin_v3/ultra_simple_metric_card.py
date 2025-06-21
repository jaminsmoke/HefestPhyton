"""
Tarjeta de métrica ULTRA SIMPLIFICADA que funciona como las básicas
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSizePolicy, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class UltraSimpleMetricCard(QWidget):
    """Tarjeta ultra simple que replica la estructura de las tarjetas básicas que funcionan"""
    
    def __init__(self, icon="💰", title="Ventas", value="€2,450", subtitle="Hoy vs Ayer", 
                 trend="+12%", color="#10b981", parent=None):
        super().__init__(parent)
        
        self.icon = icon
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.trend = trend
        self.color = color
        
        # Referencias para updates
        self.value_label = None
        self.trend_label = None
        
        self.setup_ultra_simple_ui()
        
        print(f"🟢 UltraSimpleMetricCard creada: {self.title}")
        
    def setup_ultra_simple_ui(self):
        """UI ultra simple exactamente como las tarjetas básicas que funcionan"""
        
        # Tamaño fijo como las básicas
        self.setFixedSize(280, 190)
        
        # Estilo ultra simple como las básicas
        self.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 2px solid {self.color};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        
        # Layout simple
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Icon simple
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("font-size: 24px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(icon_label)
        
        # Title simple
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0f172a;")
        layout.addWidget(title_label)
        
        # Value simple
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {self.color};")
        layout.addWidget(self.value_label)
        
        # Subtitle simple
        subtitle_label = QLabel(self.subtitle)
        subtitle_label.setStyleSheet("font-size: 12px; color: #64748b;")
        layout.addWidget(subtitle_label)
        
        # Trend simple
        if self.trend:
            self.trend_label = QLabel(self.trend)
            trend_color = self._get_trend_color(self.trend)
            self.trend_label.setStyleSheet(f"""
                font-size: 12px; 
                font-weight: bold; 
                color: {trend_color};
                background-color: {trend_color}20;
                padding: 4px 8px;
                border-radius: 8px;
            """)
            layout.addWidget(self.trend_label)
        
        # Spacer
        layout.addStretch()
        
    def _get_trend_color(self, trend):
        """Determina el color según la tendencia"""
        if not trend:
            return "#64748b"
        if "+" in trend:
            return "#10b981"
        elif "-" in trend:
            return "#ef4444"
        return "#64748b"
    
    def update_value(self, new_value: str, new_trend: str = ""):
        """Actualizar valores"""
        if self.value_label:
            self.value_label.setText(new_value)
            self.value = new_value
            
        if new_trend and self.trend_label:
            trend_color = self._get_trend_color(new_trend)
            self.trend_label.setText(new_trend)
            self.trend_label.setStyleSheet(f"""
                font-size: 12px; 
                font-weight: bold; 
                color: {trend_color};
                background-color: {trend_color}20;
                padding: 4px 8px;
                border-radius: 8px;
            """)
