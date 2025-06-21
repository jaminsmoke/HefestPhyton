"""
Widget FiltersPanel - Panel de filtros para gestión de mesas
Versión: v0.0.13
"""

import logging
from typing import Callable, Optional
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal

logger = logging.getLogger(__name__)


class FiltersPanel(QFrame):
    """Panel de filtros moderno y organizado para el TPV"""
    
    # Señales
    zone_changed = pyqtSignal(str)  # Zona seleccionada
    status_changed = pyqtSignal(str)  # Estado seleccionado
    view_changed = pyqtSignal(str)  # Modo de vista
    refresh_requested = pyqtSignal()  # Solicitud de actualización
    
    # Señal consolidada para cambios de filtros
    filters_changed = pyqtSignal(dict)  # Todos los filtros como dict
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_zone = "Todas"
        self.selected_status = "Todos"
        self.view_mode = "grid"
        
        self.zone_buttons = {}
        self.status_buttons = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del panel de filtros"""
        self.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 1px solid #e0e6ed;
                border-radius: 16px;
                padding: 20px;
                margin: 4px;
            }
        """)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        
        # Título del panel
        self.create_title(main_layout)
        
        # Contenido de filtros
        self.create_filters_content(main_layout)
    
    def create_title(self, layout: QVBoxLayout):
        """Crea el título del panel"""
        title_layout = QHBoxLayout()
        
        title_icon = QLabel("🎛️")
        title_icon.setStyleSheet("font-size: 18px;")
        
        title_label = QLabel("Filtros y Control")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                margin-left: 8px;
            }
        """)
        
        title_layout.addWidget(title_icon)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
    
    def create_filters_content(self, layout: QVBoxLayout):
        """Crea el contenido principal de filtros"""
        filters_content = QHBoxLayout()
        filters_content.setSpacing(24)
        
        # Filtros por zona
        self.create_zone_filters(filters_content)
        
        # Separador
        filters_content.addWidget(self.create_separator())
        
        # Filtros por estado
        self.create_status_filters(filters_content)
        
        # Separador
        filters_content.addWidget(self.create_separator())
        
        # Controles de vista
        self.create_view_controls(filters_content)
        
        filters_content.addStretch()
        
        # Botón actualizar
        self.create_refresh_button(filters_content)
        
        layout.addLayout(filters_content)
    
    def create_separator(self) -> QFrame:
        """Crea un separador vertical"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet("color: #dee2e6; margin: 0px 8px;")
        return separator
    
    def create_zone_filters(self, layout: QHBoxLayout):
        """Crea filtros por zona con botones toggle"""
        zone_container = QWidget()
        zone_layout = QVBoxLayout(zone_container)
        zone_layout.setSpacing(8)
        
        # Título
        zone_title = QLabel("🏢 Zonas")
        zone_title.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #495057;
                margin-bottom: 4px;
            }
        """)
        zone_layout.addWidget(zone_title)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(6)
        
        zones = ["Todas", "Comedor", "Terraza", "Barra", "Privado"]
        
        for zone in zones:
            btn = self.create_filter_button(zone, "#007bff")
            btn.clicked.connect(lambda checked, z=zone: self.on_zone_selected(z))
            self.zone_buttons[zone] = btn
            buttons_layout.addWidget(btn)
        
        # Seleccionar "Todas" por defecto
        self.zone_buttons["Todas"].setChecked(True)
        
        zone_layout.addLayout(buttons_layout)
        layout.addWidget(zone_container)
    
    def create_status_filters(self, layout: QHBoxLayout):
        """Crea filtros por estado con botones toggle"""
        status_container = QWidget()
        status_layout = QVBoxLayout(status_container)
        status_layout.setSpacing(8)
        
        # Título
        status_title = QLabel("📊 Estados")
        status_title.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #495057;
                margin-bottom: 4px;
            }
        """)
        status_layout.addWidget(status_title)
        
        # Botones
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(6)
        
        status_info = [
            ("Todos", "#6c757d"),
            ("Libre", "#28a745"),
            ("Ocupada", "#dc3545"),
            ("Reservada", "#ffc107")
        ]
        
        for status, color in status_info:
            btn = self.create_filter_button(status, color)
            btn.clicked.connect(lambda checked, s=status: self.on_status_selected(s))
            self.status_buttons[status] = btn
            buttons_layout.addWidget(btn)
        
        # Seleccionar "Todos" por defecto
        self.status_buttons["Todos"].setChecked(True)
        
        status_layout.addLayout(buttons_layout)
        layout.addWidget(status_container)
    
    def create_view_controls(self, layout: QHBoxLayout):
        """Crea controles de vista"""
        view_container = QWidget()
        view_layout = QVBoxLayout(view_container)
        view_layout.setSpacing(8)
        
        # Título
        view_title = QLabel("👁️ Vista")
        view_title.setStyleSheet("""
            QLabel {
                font-size: 12px;
                font-weight: bold;
                color: #495057;
                margin-bottom: 4px;
            }
        """)
        view_layout.addWidget(view_title)
        
        # Botones de vista
        view_buttons_layout = QHBoxLayout()
        view_buttons_layout.setSpacing(4)
        
        self.grid_view_btn = QPushButton("⊞")
        self.grid_view_btn.setFixedSize(28, 28)
        self.grid_view_btn.setCheckable(True)
        self.grid_view_btn.setChecked(True)
        self.grid_view_btn.setToolTip("Vista en cuadrícula")
        
        self.list_view_btn = QPushButton("☰")
        self.list_view_btn.setFixedSize(28, 28)
        self.list_view_btn.setCheckable(True)
        self.list_view_btn.setToolTip("Vista en lista")
        
        view_style = """
            QPushButton {
                background-color: #e9ecef;
                border: 2px solid #dee2e6;
                border-radius: 4px;
                color: #6c757d;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #6f42c1;
                border-color: #6f42c1;
                color: white;
            }
        """
        
        self.grid_view_btn.setStyleSheet(view_style)
        self.list_view_btn.setStyleSheet(view_style)
        
        self.grid_view_btn.clicked.connect(lambda: self.on_view_changed("grid"))
        self.list_view_btn.clicked.connect(lambda: self.on_view_changed("list"))
        
        view_buttons_layout.addWidget(self.grid_view_btn)
        view_buttons_layout.addWidget(self.list_view_btn)
        
        view_layout.addLayout(view_buttons_layout)
        layout.addWidget(view_container)
    
    def create_filter_button(self, text: str, color: str) -> QPushButton:
        """Crea un botón de filtro estándar"""
        btn = QPushButton(text)
        btn.setFixedSize(70, 28)
        btn.setCheckable(True)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(108, 117, 125, 0.1);
                border: 2px solid {color};
                border-radius: 14px;
                color: {color};
                font-weight: 500;
                font-size: 10px;
            }}
            QPushButton:checked {{
                background-color: {color};
                color: white;
            }}
            QPushButton:hover {{
                background-color: rgba(108, 117, 125, 0.1);
            }}
        """)
        return btn
    
    def create_refresh_button(self, layout: QHBoxLayout):
        """Crea el botón de actualización"""
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setFixedSize(120, 36)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                border: none;
                border-radius: 18px;
                color: white;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_requested.emit)
        layout.addWidget(refresh_btn)
    
    def on_zone_selected(self, zone: str):
        """Maneja la selección de zona"""
        try:
            # Desmarcar otros botones de zona
            for btn_zone, btn in self.zone_buttons.items():
                btn.setChecked(btn_zone == zone)
            
            self.selected_zone = zone
            self.zone_changed.emit(zone)
            logger.debug(f"Zona seleccionada: {zone}")
            
            # Emitir señal consolidada de filtros
            self._emit_filters_changed()
            
        except Exception as e:
            logger.error(f"Error seleccionando zona: {e}")
    
    def on_status_selected(self, status: str):
        """Maneja la selección de estado"""
        try:
            # Desmarcar otros botones de estado
            for btn_status, btn in self.status_buttons.items():
                btn.setChecked(btn_status == status)
            
            self.selected_status = status
            self.status_changed.emit(status)
            logger.debug(f"Estado seleccionado: {status}")
            
            # Emitir señal consolidada de filtros
            self._emit_filters_changed()
            
        except Exception as e:
            logger.error(f"Error seleccionando estado: {e}")
    
    def on_view_changed(self, mode: str):
        """Maneja el cambio de modo de vista"""
        try:
            self.view_mode = mode
            
            # Actualizar botones
            self.grid_view_btn.setChecked(mode == "grid")
            self.list_view_btn.setChecked(mode == "list")
            
            self.view_changed.emit(mode)
            logger.debug(f"Modo de vista: {mode}")
            
        except Exception as e:
            logger.error(f"Error cambiando vista: {e}")
    
    def _emit_filters_changed(self):
        """Emite la señal consolidada con todos los filtros"""
        filters = self.get_current_filters()
        self.filters_changed.emit(filters)
        logger.debug(f"Filtros cambiados: {filters}")

    def get_current_filters(self) -> dict:
        """Obtiene los filtros actuales"""
        return {
            'zone': self.selected_zone,
            'status': self.selected_status,
            'view_mode': self.view_mode
        }
