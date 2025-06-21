"""
Tarjeta de métrica COMPATIBLE con PyQt6 CSS - SIN propiedades CSS modernas
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AdvancedMetricCardCompatible(QWidget):
    """Tarjeta de métrica COMPATIBLE con filtro CSS de PyQt6"""
    
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
        
        self.setup_compatible_ui()
        
        # FORZAR VISIBILIDAD
        self.setVisible(True)
        self.show()
        
        print(f"✅ AdvancedMetricCardCompatible creada: {self.title}")
          
    def setup_compatible_ui(self):
        """UI COMPATIBLE con PyQt6 - Solo propiedades CSS soportadas"""
        
        # TAMAÑO FIJO para evitar problemas de layout
        self.setFixedSize(260, 160)
        
        # Estilo COMPATIBLE - Solo propiedades soportadas por PyQt6
        self.setStyleSheet(f"""
            AdvancedMetricCardCompatible {{
                background-color: #ffffff;
                border: 2px solid {self.color};
                padding: 10px;
            }}
            AdvancedMetricCardCompatible:hover {{
                background-color: #f8fafc;
                border: 3px solid {self.color};
            }}
        """)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 12, 15, 12)
        main_layout.setSpacing(8)
        
        # Fila superior: Icon + Trend badge
        top_row = QHBoxLayout()
        top_row.setSpacing(8)
        
        # Icon GRANDE
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                background: transparent;
                border: none;
                color: #374151;
            }
        """)
        icon_label.setVisible(True)
        icon_label.show()
        top_row.addWidget(icon_label)
        
        # Spacer
        top_row.addStretch()
        
        # Trend badge
        if self.trend:
            trend_color = self._get_trend_color(self.trend)
            self.trend_label = QLabel(self.trend)
            self.trend_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {trend_color};
                    color: white;
                    font-size: 9px;
                    font-weight: bold;
                    padding: 2px 5px;
                    border: 1px solid {trend_color};
                }}
            """)
            self.trend_label.setVisible(True)
            self.trend_label.show()
            top_row.addWidget(self.trend_label)
        
        main_layout.addLayout(top_row)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #374151;
                background: transparent;
                border: none;
            }
        """)
        title_label.setVisible(True)
        title_label.show()
        main_layout.addWidget(title_label)
        
        # Value PRINCIPAL
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 22px;
                font-weight: bold;
                color: {self.color};
                background: transparent;
                border: none;
            }}
        """)
        self.value_label.setVisible(True)
        self.value_label.show()
        main_layout.addWidget(self.value_label)
        
        # Subtitle
        if self.subtitle:
            subtitle_label = QLabel(self.subtitle)
            subtitle_label.setStyleSheet("""
                QLabel {
                    font-size: 10px;
                    color: #6b7280;
                    background: transparent;
                    border: none;
                }
            """)
            subtitle_label.setVisible(True)
            subtitle_label.show()
            main_layout.addWidget(subtitle_label)
        
        # Spacer
        main_layout.addStretch()
        
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
        """Actualizar valores dinámicamente"""
        if self.value_label:
            self.value_label.setText(new_value)
            self.value = new_value
            
        if new_trend and self.trend_label:
            trend_color = self._get_trend_color(new_trend)
            self.trend_label.setText(new_trend)
            self.trend_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {trend_color};
                    color: white;
                    font-size: 9px;
                    font-weight: bold;
                    padding: 2px 5px;
                    border: 1px solid {trend_color};
                }}
            """)
            self.trend = new_trend
