# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

"""
AdvancedMetricCard - Versión ROBUSTA y SIMPLE
Solucionando problemas de visibilidad en PyQt6
"""



class AdvancedMetricCardRobust(QWidget):
    """Tarjeta de métrica ROBUSTA - versión simplificada que siempre funciona"""
    
    def __init__(self, icon="💰", title="Ventas", value="€2,450", subtitle="Hoy vs Ayer", 
                 trend="+12%", color="#10b981", parent=None):
        super().__init__(parent)
        
        # Datos
        self.icon = icon
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.trend = trend
        self.color = color        
        
        # Referencias
        self.value_label = None
        self.trend_label = None
        
        # Configurar UI INMEDIATAMENTE
        self.setup_robust_ui()
        
        # FORZAR visibilidad desde el inicio
        self.setVisible(True)
        self.setAttribute(Qt.WidgetAttribute.WA_AlwaysShowToolTips)
        
        print("✅ AdvancedMetricCardRobust creada: %s" % self.title)
          
    def setup_robust_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """UI ROBUSTA y SIMPLE - garantiza visibilidad"""
        
        # Tamaño fijo para evitar problemas de layout
        self.setFixedSize(280, 160)
        
        # Estilo SIMPLE y compatible
        self.setStyleSheet(f"""
            AdvancedMetricCardRobust {{
                background-color: #ffffff;
                border: 2px solid {self.color};
                border-radius: 12px;
            }}
        """)
        
        # Layout principal SIMPLE
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(8)
        
        # Fila superior: Icon + Trend
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)
        
        # Icon
        icon_label = QLabel(self.icon)
        icon_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                color: #374151;
            }
        """)
        icon_label.setVisible(True)
        top_layout.addWidget(icon_label)
        
        # Spacer
        top_layout.addStretch()
        
        # Trend badge
        if self.trend:
            _ = self._get_trend_color(self.trend)
            self.trend_label = QLabel(self.trend)
            self.trend_label.setStyleSheet(f"""
                QLabel {{
                    background-color: {trend_color};
                    color: white;
                    font-size: 10px;
                    font-weight: bold;
                    padding: 4px 8px;
                    border-radius: 6px;
                }}
            """)
            self.trend_label.setVisible(True)
            top_layout.addWidget(self.trend_label)
        
        main_layout.addLayout(top_layout)
        
        # Title
        title_label = QLabel(self.title)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #374151;
            }
        """)
        title_label.setVisible(True)
        main_layout.addWidget(title_label)
        
        # Value PRINCIPAL
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 22px;
                font-weight: bold;
                color: {self.color};
            }}
        """)
        self.value_label.setVisible(True)
        main_layout.addWidget(self.value_label)
        
        # Subtitle
        if self.subtitle:
            subtitle_label = QLabel(self.subtitle)
            subtitle_label.setStyleSheet("""
                QLabel {
                    font-size: 11px;
                    color: #6b7280;
                }
            """)
            subtitle_label.setVisible(True)
            main_layout.addWidget(subtitle_label)
        
        # Spacer final
        main_layout.addStretch()
        
    def _get_trend_color(self, trend):
        """Color de tendencia"""
        if "+" in trend or "↑" in trend:
            return "#10b981"  # Verde
        elif "-" in trend or "↓" in trend:
            return "#ef4444"  # Rojo
        return "#6b7280"  # Gris
    
    def update_value(self, new_value: str, new_trend: str = ""):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar valores"""
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
                    font-size: 10px;
                    font-weight: bold;
                    padding: 4px 8px;
                    border-radius: 6px;
                }}
            """)
            self.trend = new_trend
