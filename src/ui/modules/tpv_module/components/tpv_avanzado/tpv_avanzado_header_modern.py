"""
TPV Avanzado - Header moderno con información de mesa y controles
"""

from typing import Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

from .styles_modern import (
    get_modern_button_style, 
    get_status_badge_style,
    COLORS, 
    SPACING,
    BORDER_RADIUS
)


class ModernHeaderWidget(QWidget):
    """Header moderno para TPV con información de mesa y controles"""
    
    mesa_changed = pyqtSignal(int)  # Señal cuando cambia la mesa
    action_requested = pyqtSignal(str)  # Señal para acciones del header
    
    def __init__(self, parent_tpv, parent=None):
        super().__init__(parent)
        self.parent_tpv = parent_tpv
        self.setup_ui()
        self.update_mesa_info()
    
    def setup_ui(self):
        """Configura la interfaz del header moderno"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        
        # Sección izquierda: Información de mesa
        self.mesa_section = self.create_mesa_section()
        layout.addWidget(self.mesa_section)
        
        # Espaciador flexible
        layout.addStretch()
        
        # Sección central: Estado del pedido
        self.status_section = self.create_status_section()
        layout.addWidget(self.status_section)
        
        # Espaciador flexible
        layout.addStretch()
        
        # Sección derecha: Controles de acción
        self.actions_section = self.create_actions_section()
        layout.addWidget(self.actions_section)
        
        # Aplicar estilos
        self.apply_header_styles()
    
    def create_mesa_section(self):
        """Crea la sección de información de mesa"""
        section = QFrame()
        layout = QHBoxLayout(section)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)
        
        # Icono de mesa
        mesa_icon = QLabel("🍽️")
        mesa_icon.setFont(QFont("Segoe UI", 20))
        layout.addWidget(mesa_icon)
        
        # Información de mesa
        info_layout = QVBoxLayout()
        info_layout.setSpacing(2)
        
        # Número de mesa
        self.mesa_label = QLabel("Mesa 1")
        self.mesa_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.mesa_label.setStyleSheet(f"color: {COLORS['gray_800']};")
        info_layout.addWidget(self.mesa_label)
        
        # Estado de mesa
        self.mesa_status_label = QLabel("Disponible")
        self.mesa_status_label.setFont(QFont("Segoe UI", 11))
        self.mesa_status_label.setStyleSheet(f"color: {COLORS['gray_600']};")
        info_layout.addWidget(self.mesa_status_label)
        
        layout.addLayout(info_layout)
        
        # Estilo de la sección
        section.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {COLORS['primary']}, 
                    stop:1 {COLORS['primary_light']});
                border-radius: {BORDER_RADIUS['lg']};
                color: {COLORS['white']};
            }}
            QLabel {{
                color: {COLORS['white']};
                background: transparent;
            }}
        """)
        
        return section
    
    def create_status_section(self):
        """Crea la sección de estado del pedido"""
        section = QFrame()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.setSpacing(4)
        
        # Estado principal
        self.status_label = QLabel("Sin pedido")
        self.status_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Medium))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Información adicional
        self.status_info = QLabel("Listo para tomar pedido")
        self.status_info.setFont(QFont("Segoe UI", 10))
        self.status_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_info.setStyleSheet(f"color: {COLORS['gray_500']};")
        layout.addWidget(self.status_info)
        
        # Aplicar badge de estado
        self.update_status_badge("info")
        
        return section
    
    def create_actions_section(self):
        """Crea la sección de botones de acción"""
        section = QFrame()
        layout = QHBoxLayout(section)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Botón de nuevo pedido
        self.new_order_btn = QPushButton("🆕 Nuevo")
        self.new_order_btn.setStyleSheet(get_modern_button_style("primary", "sm"))
        self.new_order_btn.clicked.connect(
            lambda: self.action_requested.emit("new_order")
        )
        layout.addWidget(self.new_order_btn)
        
        # Botón de limpiar
        self.clear_btn = QPushButton("🗑️ Limpiar")
        self.clear_btn.setStyleSheet(get_modern_button_style("warning", "sm"))
        self.clear_btn.clicked.connect(
            lambda: self.action_requested.emit("clear_order")
        )
        layout.addWidget(self.clear_btn)
        
        # Botón de configuración
        self.settings_btn = QPushButton("⚙️")
        self.settings_btn.setStyleSheet(get_modern_button_style("secondary", "sm"))
        self.settings_btn.setFixedSize(36, 36)
        self.settings_btn.clicked.connect(
            lambda: self.action_requested.emit("settings")
        )
        layout.addWidget(self.settings_btn)
        
        return section
    
    def apply_header_styles(self):
        """Aplica estilos generales al header"""
        self.setStyleSheet(f"""
            ModernHeaderWidget {{
                background: {COLORS['white']};
                border-bottom: 2px solid {COLORS['gray_100']};
                padding: {SPACING['md']};
            }}
        """)
        
        # Establecer altura fija
        self.setFixedHeight(80)
    
    def update_mesa_info(self):
        """Actualiza la información de la mesa"""
        if hasattr(self.parent_tpv, 'mesa') and self.parent_tpv.mesa:
            mesa = self.parent_tpv.mesa
            self.mesa_label.setText(f"Mesa {mesa.numero}")
            
            # Actualizar estado según el estado de la mesa
            if hasattr(mesa, 'estado'):
                status_map = {
                    'libre': ('Disponible', 'success'),
                    'ocupada': ('Ocupada', 'warning'),
                    'reservada': ('Reservada', 'info'),
                    'mantenimiento': ('Mantenimiento', 'danger')
                }
                status_text, status_type = status_map.get(
                    mesa.estado, ('Desconocido', 'info')
                )
                self.mesa_status_label.setText(status_text)
            else:
                self.mesa_status_label.setText("Estado desconocido")
        else:
            self.mesa_label.setText("Sin mesa")
            self.mesa_status_label.setText("Seleccione una mesa")
    
    def update_status_badge(self, status_type="info"):
        """Actualiza el badge de estado del pedido"""
        if hasattr(self, 'status_label'):
            badge_style = get_status_badge_style(status_type)
            # Aplicar estilo al frame contenedor
            if hasattr(self, 'status_section'):
                self.status_section.setStyleSheet(f"""
                    QFrame {{
                        background: {COLORS['gray_50']};
                        border: 1px solid {COLORS['gray_200']};
                        border-radius: {BORDER_RADIUS['md']};
                    }}
                """)
    
    def update_order_status(self, status_text, info_text="", status_type="info"):
        """Actualiza el estado del pedido"""
        self.status_label.setText(status_text)
        self.status_info.setText(info_text)
        self.update_status_badge(status_type)
    
    def set_buttons_enabled(self, enabled=True):
        """Habilita o deshabilita los botones de acción"""
        self.new_order_btn.setEnabled(enabled)
        self.clear_btn.setEnabled(enabled)
        self.settings_btn.setEnabled(enabled)
    
    def highlight_action(self, action_name):
        """Resalta temporalmente un botón de acción"""
        button_map = {
            "new_order": self.new_order_btn,
            "clear_order": self.clear_btn,
            "settings": self.settings_btn
        }
        
        if action_name in button_map:
            button = button_map[action_name]
            # Efecto de resaltado temporal
            original_style = button.styleSheet()
            highlight_style = get_modern_button_style("success", "sm")
            button.setStyleSheet(highlight_style)
            
            # Restaurar estilo original después de 500ms
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(500, lambda: button.setStyleSheet(original_style))


def create_modern_header(parent_tpv) -> ModernHeaderWidget:
    """
    Función factory para crear el header moderno
    
    Args:
        parent_tpv: Instancia del TPV principal
        
    Returns:
        ModernHeaderWidget: Widget del header configurado
    """
    return ModernHeaderWidget(parent_tpv)
