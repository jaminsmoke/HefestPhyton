"""
Tarjeta de métrica avanzada - Versión FUNCIONAL basada en estructura simple
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor

class AdvancedMetricCard(QWidget):
    """Tarjeta de métrica moderna FUNCIONAL - Basada en estructura simple que funciona"""
    
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
        
        self.setup_functional_ui()
        
        print(f"✅ AdvancedMetricCard FUNCIONAL creada: {self.title}")
        
    def setup_functional_ui(self):
        """UI funcional basada en la estructura simple que funciona"""
        
        # Tamaño fijo como las que funcionan
        self.setFixedSize(280, 190)
        
        # Estilo simple pero elegante que funciona
        self.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 2px solid {self.color};
                border-radius: 12px;
                padding: 15px;
            }}
            QWidget:hover {{
                background-color: #f8fafc;
                border: 2px solid {self.color};
            }}
        """)
        
        # Layout simple y funcional
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header con icon y trend
        header_layout = QHBoxLayout()
        
        # Icon
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("font-size: 24px;")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header_layout.addWidget(icon_label)
        
        header_layout.addStretch()
        
        # Trend badge
        if self.trend:
            trend_color = self._get_trend_color(self.trend)
            self.trend_label = QLabel(self.trend)
            self.trend_label.setStyleSheet(f"""
                font-size: 12px; 
                font-weight: bold; 
                color: {trend_color};
                background-color: {trend_color}20;
                padding: 4px 8px;
                border-radius: 8px;
            """)
            header_layout.addWidget(self.trend_label)
        
        layout.addLayout(header_layout)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0f172a;")
        layout.addWidget(title_label)
        
        # Value (principal)
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {self.color};")
        layout.addWidget(self.value_label)
        
        # Subtitle
        subtitle_label = QLabel(self.subtitle)
        subtitle_label.setStyleSheet("font-size: 12px; color: #64748b;")
        layout.addWidget(subtitle_label)
        
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
