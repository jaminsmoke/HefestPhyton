"""
Widget MesaWidget - Representación visual de una mesa
Versión: v0.0.13
"""

import logging
from typing import Optional, Callable
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QCursor

from services.tpv_service import Mesa

logger = logging.getLogger(__name__)


class MesaWidget(QFrame):
    """Widget para mostrar una mesa individual con diseño moderno"""
    
    # Señales
    mesa_clicked = pyqtSignal(Mesa)
    mesa_double_clicked = pyqtSignal(Mesa)
    
    def __init__(self, mesa: Mesa, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz del widget de mesa"""
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setFixedSize(140, 120)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Configurar estilo según estado
        self.update_appearance()
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Header con icono de estado
        self.create_header(layout)
        
        # Título principal
        self.create_title(layout)
        
        # Estado
        self.create_status(layout)
        
        # Información adicional
        self.create_info(layout)
        
        layout.addStretch()
    
    def create_header(self, layout: QVBoxLayout):
        """Crea el header con icono y número de mesa"""
        header_layout = QHBoxLayout()
        
        # Icono de estado
        self.estado_icon = QLabel(self.get_status_icon())
        self.estado_icon.setStyleSheet("font-size: 16px;")
        self.estado_icon.setFixedSize(20, 20)
        
        # Número de mesa
        self.mesa_number = QLabel(f"#{self.mesa.numero}")
        self.mesa_number.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.mesa_number.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                font-weight: bold;
                color: {self.get_text_color()};
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 8px;
                padding: 2px 6px;
            }}
        """)
        
        header_layout.addWidget(self.estado_icon)
        header_layout.addStretch()
        header_layout.addWidget(self.mesa_number)
        
        layout.addLayout(header_layout)
        layout.addSpacing(4)
    
    def create_title(self, layout: QVBoxLayout):
        """Crea el título principal de la mesa"""
        self.titulo_mesa = QLabel(f"Mesa {self.mesa.numero}")
        self.titulo_mesa.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titulo_mesa.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {self.get_text_color()};
                margin: 2px 0px;
            }}
        """)
        layout.addWidget(self.titulo_mesa)
    
    def create_status(self, layout: QVBoxLayout):
        """Crea la etiqueta de estado"""
        self.estado_label = QLabel(self.mesa.estado.replace('_', ' ').title())
        self.estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estado_label.setStyleSheet(f"""
            QLabel {{
                font-size: 11px;
                font-weight: 600;
                color: {self.get_text_color()};
                background-color: rgba(255, 255, 255, 0.8);
                border-radius: 10px;
                padding: 2px 8px;
                margin: 2px;
            }}
        """)
        layout.addWidget(self.estado_label)
    
    def create_info(self, layout: QVBoxLayout):
        """Crea la información adicional (capacidad y zona)"""
        info_layout = QHBoxLayout()
        info_layout.setSpacing(8)
        
        # Capacidad
        capacidad_container = self.create_info_item("👥", str(self.mesa.capacidad))
        info_layout.addWidget(capacidad_container)
        
        # Zona
        zona_text = self.mesa.zona[:4] + ".." if len(self.mesa.zona) > 4 else self.mesa.zona
        zona_container = self.create_info_item("🏢", zona_text)
        info_layout.addWidget(zona_container)
        
        layout.addLayout(info_layout)
    
    def create_info_item(self, icon: str, text: str) -> QWidget:
        """Crea un elemento de información con icono y texto"""
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(1)
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 12px;")
        
        # Texto
        text_label = QLabel(text)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text_label.setStyleSheet(f"""
            QLabel {{
                font-size: 10px;
                font-weight: bold;
                color: {self.get_text_color()};
            }}
        """)
        
        container_layout.addWidget(icon_label)
        container_layout.addWidget(text_label)
        
        return container
    
    def get_color_config(self) -> dict:
        """Obtiene la configuración de colores según el estado"""
        color_configs = {
            'libre': {
                'bg': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e8fce8, stop:1 #d4edd4)',
                'border': '#4CAF50',
                'text': '#2e7d32',
                'icon': '✅'
            },
            'ocupada': {
                'bg': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffeaea, stop:1 #f5c6c6)',
                'border': '#f44336',
                'text': '#c62828',
                'icon': '🔴'
            },
            'reservada': {
                'bg': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #fff9e6, stop:1 #f7e99e)',
                'border': '#ff9800',
                'text': '#f57c00',
                'icon': '📅'
            },
            'fuera_servicio': {
                'bg': 'qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #f5f5f5, stop:1 #e0e0e0)',
                'border': '#9e9e9e',
                'text': '#424242',
                'icon': '🚫'
            }
        }
        return color_configs.get(self.mesa.estado, color_configs['libre'])
    
    def get_status_icon(self) -> str:
        """Obtiene el icono del estado actual"""
        return self.get_color_config()['icon']
    
    def get_text_color(self) -> str:
        """Obtiene el color del texto según el estado"""
        return self.get_color_config()['text']
    
    def update_appearance(self):
        """Actualiza la apariencia visual según el estado"""
        config = self.get_color_config()
        
        self.setStyleSheet(f"""
            QFrame {{
                background: {config['bg']};
                border: 3px solid {config['border']};
                border-radius: 16px;
                padding: 8px;
                margin: 2px;
            }}
            QFrame:hover {{
                border-width: 4px;
                border-color: #2196f3;
            }}
            QLabel {{
                border: none;
                background: transparent;
            }}
        """)
    
    def update_mesa(self, mesa: Mesa):
        """Actualiza los datos de la mesa"""
        self.mesa = mesa
        
        # Actualizar textos
        if hasattr(self, 'titulo_mesa'):
            self.titulo_mesa.setText(f"Mesa {mesa.numero}")
        
        if hasattr(self, 'estado_label'):
            self.estado_label.setText(mesa.estado.replace('_', ' ').title())
        
        if hasattr(self, 'estado_icon'):
            self.estado_icon.setText(self.get_status_icon())
        
        if hasattr(self, 'mesa_number'):
            self.mesa_number.setText(f"#{mesa.numero}")
        
        # Actualizar apariencia
        self.update_appearance()
    
    def mousePressEvent(self, event):
        """Maneja el clic en la mesa"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mesa_clicked.emit(self.mesa)
        super().mousePressEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """Maneja el doble clic en la mesa"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mesa_double_clicked.emit(self.mesa)
        super().mouseDoubleClickEvent(event)
