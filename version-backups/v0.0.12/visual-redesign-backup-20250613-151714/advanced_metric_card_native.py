"""
Tarjeta de métrica SIN CSS - Solo configuración nativa PyQt6
Evita completamente setStyleSheet para elementos principales
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

class AdvancedMetricCardNative(QWidget):
    """Tarjeta de métrica usando SOLO configuración nativa PyQt6 - SIN setStyleSheet"""
    
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
        
        self.setup_native_ui()
        
        # FORZAR VISIBILIDAD
        self.setVisible(True)
        self.show()
        
        print(f"🔥 AdvancedMetricCardNative creada (SIN CSS): {self.title}")
          
    def setup_native_ui(self):
        """UI usando SOLO configuración nativa PyQt6 - EVITANDO setStyleSheet"""
        
        # TAMAÑO FIJO
        self.setFixedSize(260, 160)
        
        # Configurar fondo usando palette en lugar de CSS
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffffff"))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # Frame con border usando QFrame en lugar de CSS
        frame = QFrame(self)
        frame.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        frame.setLineWidth(2)
        frame.resize(self.size())
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 12, 15, 12)
        main_layout.setSpacing(8)
        
        # Fila superior: Icon + Trend badge
        top_row = QHBoxLayout()
        top_row.setSpacing(8)
        
        # Icon GRANDE usando solo configuración nativa
        icon_label = QLabel(self.icon)
        icon_font = QFont()
        icon_font.setPointSize(28)
        icon_label.setFont(icon_font)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # SIN setStyleSheet - solo configuración nativa
        icon_label.setVisible(True)
        icon_label.show()
        top_row.addWidget(icon_label)
        
        # Spacer
        top_row.addStretch()
        
        # Trend badge - SOLO CON CONFIGURACIÓN NATIVA
        if self.trend:
            self.trend_label = QLabel(self.trend)
            trend_font = QFont()
            trend_font.setPointSize(8)
            trend_font.setBold(True)
            self.trend_label.setFont(trend_font)
            
            # Configurar color de fondo usando palette
            trend_palette = self.trend_label.palette()
            trend_color = self._get_trend_qcolor(self.trend)
            trend_palette.setColor(QPalette.ColorRole.Window, trend_color)
            trend_palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
            self.trend_label.setPalette(trend_palette)
            self.trend_label.setAutoFillBackground(True)
            self.trend_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
            self.trend_label.setVisible(True)
            self.trend_label.show()
            top_row.addWidget(self.trend_label)
        
        main_layout.addLayout(top_row)
        
        # Title usando solo configuración nativa
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        # Color usando palette
        title_palette = title_label.palette()
        title_palette.setColor(QPalette.ColorRole.WindowText, QColor("#374151"))
        title_label.setPalette(title_palette)
        title_label.setVisible(True)
        title_label.show()
        main_layout.addWidget(title_label)
        
        # Value PRINCIPAL usando solo configuración nativa
        self.value_label = QLabel(self.value)
        value_font = QFont()
        value_font.setPointSize(22)
        value_font.setBold(True)
        self.value_label.setFont(value_font)
        # Color usando palette
        value_palette = self.value_label.palette()
        value_palette.setColor(QPalette.ColorRole.WindowText, QColor(self.color))
        self.value_label.setPalette(value_palette)
        self.value_label.setVisible(True)
        self.value_label.show()
        main_layout.addWidget(self.value_label)
        
        # Subtitle usando solo configuración nativa
        if self.subtitle:
            subtitle_label = QLabel(self.subtitle)
            subtitle_font = QFont()
            subtitle_font.setPointSize(9)
            subtitle_label.setFont(subtitle_font)
            # Color usando palette
            subtitle_palette = subtitle_label.palette()
            subtitle_palette.setColor(QPalette.ColorRole.WindowText, QColor("#6b7280"))
            subtitle_label.setPalette(subtitle_palette)
            subtitle_label.setVisible(True)
            subtitle_label.show()
            main_layout.addWidget(subtitle_label)
        
        # Spacer
        main_layout.addStretch()
        
        print(f"🔥 Configuración NATIVA aplicada para: {self.title} (SIN CSS)")
        
    def _get_trend_qcolor(self, trend):
        """Determina el QColor según la tendencia"""
        if not trend:
            return QColor("#6b7280")
        if "+" in trend or "↑" in trend:
            return QColor("#10b981")  # Verde para positivo
        elif "-" in trend or "↓" in trend:
            return QColor("#ef4444")  # Rojo para negativo
        return QColor("#6b7280")  # Gris neutro
    
    def update_value(self, new_value: str, new_trend: str = ""):
        """Actualizar valores dinámicamente"""
        if self.value_label:
            self.value_label.setText(new_value)
            self.value = new_value
            
        if new_trend and self.trend_label:
            self.trend_label.setText(new_trend)
            # Actualizar color usando palette
            trend_palette = self.trend_label.palette()
            trend_color = self._get_trend_qcolor(new_trend)
            trend_palette.setColor(QPalette.ColorRole.Window, trend_color)
            self.trend_label.setPalette(trend_palette)
            self.trend = new_trend
