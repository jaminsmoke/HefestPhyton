"""
Tarjeta de métrica avanzada - RESPONSIVE y visualmente diferenciada
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class AdvancedMetricCard(QWidget):
    """Tarjeta de métrica RESPONSIVE con diseño moderno y diferenciado"""
    
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
        
        self.setup_modern_ui()
        
        # FORZAR VISIBILIDAD de todos los componentes
        self.setVisible(True)
        self.show()
        
        print(f"✅ AdvancedMetricCard MODERNA creada: {self.title}")
          
    def setup_modern_ui(self):
        """UI MODERNA con mejor visualización y diferenciación"""
        
        # TAMAÑO RESPONSIVE - se ajusta al contenedor
        self.setMinimumSize(240, 140)
          # Estilo MODERNO con mejor diferenciación visual (sin box-shadow)
        self.setStyleSheet(f"""
            AdvancedMetricCard {{
                background-color: #ffffff;
                border: 2px solid {self.color};
                border-radius: 12px;
                margin: 3px;
            }}
            AdvancedMetricCard:hover {{
                background-color: #f8fafc;
                border: 3px solid {self.color};
            }}
        """)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)
        
        # Fila superior: Icon + Trend badge
        top_row = QHBoxLayout()
        top_row.setSpacing(8)
          # Icon GRANDE y llamativo
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                background: transparent;
                border: none;
                margin: 0;
                padding: 0;
            }
        """)
        icon_label.setVisible(True)
        icon_label.show()
        top_row.addWidget(icon_label)
        
        # Spacer para empujar el trend badge a la derecha
        top_row.addStretch()
          # Trend badge (si existe)
        if self.trend:
            trend_color = self._get_trend_color(self.trend)
            self.trend_label = QLabel(self.trend)
            self.trend_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {trend_color};
                    color: white;
                    font-size: 10px;
                    font-weight: bold;
                    padding: 3px 6px;
                    border-radius: 8px;
                    max-width: 60px;
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
                font-size: 14px;
                font-weight: 600;
                color: #374151;
                background: transparent;
                border: none;
                margin: 0;
            }
        """)
        title_label.setVisible(True)
        title_label.show()
        main_layout.addWidget(title_label)
        
        # Value PRINCIPAL (más destacado)
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 24px;
                font-weight: 700;
                color: {self.color};
                background: transparent;
                border: none;
                margin: 2px 0;            }}
        """)
        self.value_label.setVisible(True)
        self.value_label.show()
        main_layout.addWidget(self.value_label)
          # Subtitle
        if self.subtitle:
            subtitle_label = QLabel(self.subtitle)
            subtitle_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #6b7280;
                    background: transparent;
                    border: none;
                    margin: 0;
                }
            """)
            subtitle_label.setVisible(True)
            subtitle_label.show()
            main_layout.addWidget(subtitle_label)
        
        # Spacer para mantener proporción
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
                    font-size: 10px;
                    font-weight: bold;
                    padding: 3px 6px;
                    border-radius: 8px;
                    max-width: 60px;
                }}
            """)
            self.trend = new_trend
