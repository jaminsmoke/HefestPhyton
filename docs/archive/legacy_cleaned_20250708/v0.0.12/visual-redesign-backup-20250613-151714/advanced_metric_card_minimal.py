# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
"""
Tarjeta de métrica ULTRA SIMPLE - SIN CSS problemático, solo configuración nativa PyQt6
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette

class AdvancedMetricCardMinimal(QWidget):
    """Tarjeta de métrica MÍNIMA - Solo configuración nativa PyQt6, sin CSS complejo"""
    
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
        
        self.setup_minimal_ui()
        
        # FORZAR VISIBILIDAD
        self.setVisible(True)
        self.show()
        
        print("✅ AdvancedMetricCardMinimal creada: %s" % self.title)
          
    def setup_minimal_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """UI MÍNIMA - Solo configuración nativa PyQt6, evitando CSS complejo"""
        
        # TAMAÑO FIJO
        self.setFixedSize(260, 160)
        
        # ESTILO MÍNIMO - Solo background y border básico
        self.setStyleSheet(f"""
            AdvancedMetricCardMinimal {{
                background-color: white;
                border: 2px solid {self.color};
            }}
        """)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 12, 15, 12)
        main_layout.setSpacing(8)
        
        # Fila superior: Icon + Trend badge
        top_row = QHBoxLayout()
        top_row.setSpacing(8)
        
        # Icon GRANDE con configuración nativa
        _ = QLabel(self.icon)
        icon_font = QFont()
        icon_font.setPointSize(24)
        icon_label.setFont(icon_font)
        icon_label.setVisible(True)
        icon_label.show()
        top_row.addWidget(icon_label)
        
        # Spacer
        top_row.addStretch()
        
        # Trend badge - MUY SIMPLE
        if self.trend:
            _ = self._get_trend_color(self.trend)
            self.trend_label = QLabel(self.trend)
            self.trend_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {trend_color};
                    color: white;
                    padding: 2px 4px;
                }}
            """)
            trend_font = QFont()
            trend_font.setPointSize(8)
            trend_font.setBold(True)
            self.trend_label.setFont(trend_font)
            self.trend_label.setVisible(True)
            self.trend_label.show()
            top_row.addWidget(self.trend_label)
        
        main_layout.addLayout(top_row)
        
        # Title con configuración nativa
        _ = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setVisible(True)
        title_label.show()
        main_layout.addWidget(title_label)
        
        # Value PRINCIPAL con configuración nativa
        self.value_label = QLabel(self.value)
        value_font = QFont()
        value_font.setPointSize(20)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        # Aplicar color usando QPalette en lugar de CSS
        self.value_label.setStyleSheet(f"QLabel {{ color: {self.color}; }}")
        self.value_label.setVisible(True)
        self.value_label.show()
        main_layout.addWidget(self.value_label)
        
        # Subtitle con configuración nativa
        if self.subtitle:
            _ = QLabel(self.subtitle)
            subtitle_font = QFont()
            subtitle_font.setPointSize(9)
            subtitle_label.setFont(subtitle_font)
            subtitle_label.setStyleSheet("QLabel { color: #666666; }")
            subtitle_label.setVisible(True)
            subtitle_label.show()
            main_layout.addWidget(subtitle_label)
        
        # Spacer
        main_layout.addStretch()
        
        print("🔧 Configuración mínima aplicada para: %s" % self.title)
        
    def _get_trend_color(self, trend):
        """Determina el color según la tendencia"""
        if not trend:
            return "#6b7280"
        if "+" in trend or "↑" in trend:
            return "#10b981"  # Verde para positivo
        elif "-" in trend or "↓" in trend:
            return "#ef4444"  # Rojo para negativo
        return "#6b7280"  # Gris neutro
    
    def update_value(self, new_value: str, new_trend: str = ""):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar valores dinámicamente"""
        if self.value_label:
            self.value_label.setText(new_value)
            self.value = new_value
            
        if new_trend and self.trend_label:
            _ = self._get_trend_color(new_trend)
            self.trend_label.setText(new_trend)
            self.trend_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {trend_color};
                    color: white;
                    padding: 2px 4px;
                }}
            """)
            self.trend = new_trend
