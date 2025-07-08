"""
Tarjeta de métrica MODERNA y SOFISTICADA
Usa el sistema de CSS inteligente compatible con PyQt6
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtGui import QFont, QColor

# Importar el gestor de estilos inteligente
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from utils.qt_smart_css_fixed import SmartStyleManager


class AdvancedMetricCardModern(QWidget):
    """Tarjeta de métrica MODERNA con diseño sofisticado y efectos visuales"""
    
    def __init__(self, icon="💰", title="Ventas", value="€2,450", subtitle="Hoy vs Ayer", 
                 trend="+12%", color="#3b82f6", parent=None):
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
        self.title_label = None
        self.icon_label = None
        self.subtitle_label = None
        
        # Estado de hover para animaciones
        self._hover_state = False
        
        self.setup_modern_ui()
        self.setup_effects()
        
        # FORZAR VISIBILIDAD
        self.setVisible(True)
        self.show()
        
        print(f"✅ AdvancedMetricCardModern creada: {self.title}")
          
    def setup_modern_ui(self):
        """UI MODERNA y SOFISTICADA con diseño profesional"""
        
        # TAMAÑO RESPONSIVE pero con mínimos razonables
        self.setMinimumSize(280, 160)
        self.setMaximumSize(320, 200)
        
        # Aplicar estilo moderno usando el sistema inteligente
        modern_style = SmartStyleManager.get_metric_card_style(self.color)
        self.setStyleSheet(modern_style)
        
        # Layout principal con espaciado profesional
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(12)
        
        # === FILA SUPERIOR: Icon + Trend Badge ===
        top_row = QHBoxLayout()
        top_row.setSpacing(12)
        
        # Icon con estilo moderno
        self.icon_label = QLabel(self.icon)
        self.icon_label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                background: transparent;
                border: none;
                color: #374151;
                font-weight: bold;
            }
        """)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setVisible(True)
        top_row.addWidget(self.icon_label)
        
        # Spacer flexible
        top_row.addStretch()
        
        # Trend badge moderno
        if self.trend:
            trend_color = self._get_trend_color(self.trend)
            badge_style = SmartStyleManager.get_badge_style(trend_color)
            
            self.trend_label = QLabel(self.trend)
            self.trend_label.setStyleSheet(badge_style)
            self.trend_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.trend_label.setVisible(True)
            top_row.addWidget(self.trend_label)
        
        main_layout.addLayout(top_row)
        
        # === TÍTULO PRINCIPAL ===
        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: 600;
                color: #1f2937;
                background: transparent;
                border: none;
                margin: 4px 0;
            }
        """)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.title_label.setVisible(True)
        main_layout.addWidget(self.title_label)
        
        # === VALOR PRINCIPAL (destacado) ===
        self.value_label = QLabel(self.value)
        self.value_label.setStyleSheet(f"""
            QLabel {{
                font-size: 26px;
                font-weight: 700;
                color: {self.color};
                background: transparent;
                border: none;
                margin: 2px 0;
            }}
        """)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.value_label.setVisible(True)
        main_layout.addWidget(self.value_label)
        
        # === SUBTÍTULO ===
        if self.subtitle:
            self.subtitle_label = QLabel(self.subtitle)
            self.subtitle_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    font-weight: 500;
                    color: #6b7280;
                    background: transparent;
                    border: none;
                    margin: 0;
                }
            """)
            self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.subtitle_label.setVisible(True)
            main_layout.addWidget(self.subtitle_label)
        
        # Spacer para mantener proporción
        main_layout.addStretch()
        
    def setup_effects(self):
        """Configura efectos visuales modernos usando QGraphicsDropShadowEffect"""
        # Sombra sutil para profundidad
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 25))  # Sombra sutil
        self.setGraphicsEffect(shadow)
        
        # Referencia para animaciones
        self._shadow_effect = shadow
        
    def enterEvent(self, event):
        """Efecto hover - aumentar sombra"""
        super().enterEvent(event)
        self._hover_state = True
        if self._shadow_effect:
            self._shadow_effect.setBlurRadius(15)
            self._shadow_effect.setColor(QColor(0, 0, 0, 40))
        
        # Cursor pointer para indicar interactividad
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        
    def leaveEvent(self, event):
        """Fin hover - volver a sombra normal"""
        super().leaveEvent(event)
        self._hover_state = False
        if self._shadow_effect:
            self._shadow_effect.setBlurRadius(8)
            self._shadow_effect.setColor(QColor(0, 0, 0, 25))
            
        # Volver a cursor normal
        self.setCursor(Qt.CursorShape.ArrowCursor)
        
    def _get_trend_color(self, trend):
        """Determina el color según la tendencia"""
        if not trend:
            return "#6b7280"
        if "+" in trend or "↑" in trend:
            return "#10b981"  # Verde para positivo
        elif "-" in trend or "↓" in trend:
            return "#ef4444"  # Rojo para negativo
        return "#f59e0b"  # Amarillo para neutro
    
    def update_value(self, new_value: str, new_trend: str = ""):
        """Actualizar valores dinámicamente con animación"""
        if self.value_label:
            # Efecto de actualización
            self.value_label.setText(new_value)
            self.value = new_value
            
        if new_trend and self.trend_label:
            trend_color = self._get_trend_color(new_trend)
            badge_style = SmartStyleManager.get_badge_style(trend_color)
            
            self.trend_label.setText(new_trend)
            self.trend_label.setStyleSheet(badge_style)
            self.trend = new_trend
            
    def set_highlight(self, highlighted=True):
        """Resalta la tarjeta (para animaciones o estados especiales)"""
        if highlighted:
            highlight_style = SmartStyleManager.get_metric_card_style("#f59e0b")  # Amarillo/dorado
            self.setStyleSheet(highlight_style)
            if self._shadow_effect:
                self._shadow_effect.setBlurRadius(20)
                self._shadow_effect.setColor(QColor(245, 158, 11, 60))  # Sombra dorada
        else:
            normal_style = SmartStyleManager.get_metric_card_style(self.color)
            self.setStyleSheet(normal_style)
            if self._shadow_effect:
                self._shadow_effect.setBlurRadius(8)
                self._shadow_effect.setColor(QColor(0, 0, 0, 25))
                
    def get_current_data(self):
        """Retorna los datos actuales de la tarjeta"""
        return {
            'icon': self.icon,
            'title': self.title,
            'value': self.value,
            'subtitle': self.subtitle,
            'trend': self.trend,
            'color': self.color
        }
