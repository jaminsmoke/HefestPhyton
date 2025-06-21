"""
Componente MesasArea - Área de visualización y gestión de mesas
Versión: v0.0.13
"""

import logging
from typing import List, Optional, Callable
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QFrame, QScrollArea, QPushButton)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

from services.tpv_service import Mesa
from ..widgets.mesa_widget import MesaWidget

logger = logging.getLogger(__name__)


class MesasArea(QFrame):
    """Área de visualización y gestión de mesas"""
    
    # Señales
    mesa_clicked = pyqtSignal(Mesa)
    nueva_mesa_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesas: List[Mesa] = []
        self.filtered_mesas: List[Mesa] = []
        self.mesa_widgets: List[MesaWidget] = []
        
        self.current_zone_filter = "Todas"
        self.current_status_filter = "Todos"
        self.view_mode = "grid"
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del área de mesas"""
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e0e6ed;
                border-radius: 12px;
                margin: 4px;
            }
        """)
        
        container_layout = QVBoxLayout(self)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(16)
        
        # Header del área de mesas
        self.create_header(container_layout)
        
        # Separador
        self.create_separator(container_layout)
        
        # Área de scroll para las mesas
        self.create_scroll_area(container_layout)
    
    def create_header(self, layout: QVBoxLayout):
        """Crea el header del área de mesas"""
        header_layout = QHBoxLayout()
        
        title_icon = QLabel("🍽️")
        title_icon.setStyleSheet("font-size: 20px;")
        
        title_label = QLabel("Distribución de Mesas")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                margin-left: 8px;
            }
        """)
        
        header_layout.addWidget(title_icon)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Información de estado
        self.status_info = QLabel("Haga clic en una mesa para gestionar")
        self.status_info.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #7f8c8d;
                font-style: italic;
            }
        """)
        header_layout.addWidget(self.status_info)
        
        layout.addLayout(header_layout)
    
    def create_separator(self, layout: QVBoxLayout):
        """Crea un separador horizontal"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: #e0e6ed; margin: 4px 0px;")
        layout.addWidget(separator)
    
    def create_scroll_area(self, layout: QVBoxLayout):
        """Crea el área de scroll para las mesas"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: #fafbfc;
                border-radius: 8px;
            }
            QScrollBar:vertical {
                background-color: #f1f3f4;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #bdc3c7;
                border-radius: 6px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #95a5a6;
            }
        """)
        
        # Container para las mesas con padding
        mesas_container = QWidget()
        mesas_container.setStyleSheet("""
            QWidget {
                background-color: #fafbfc;
                border-radius: 8px;
            }
        """)
        
        self.mesas_layout = QGridLayout(mesas_container)
        self.mesas_layout.setSpacing(20)
        self.mesas_layout.setContentsMargins(20, 20, 20, 20)
        self.mesas_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        
        scroll_area.setWidget(mesas_container)
        layout.addWidget(scroll_area, 1)
    
    def set_mesas(self, mesas: List[Mesa]):
        """Establece la lista de mesas"""
        self.mesas = mesas
        self.apply_filters()
    
    def apply_filters(self, filters: Optional[dict] = None):
        """Aplica filtros específicos o usa los actuales"""
        if filters:
            self.current_zone_filter = filters.get('zone', 'Todas')
            self.current_status_filter = filters.get('status', 'Todos')
            self.view_mode = filters.get('view_mode', 'grid')
        
        try:
            self.filtered_mesas = self.mesas.copy()
            
            # Aplicar filtro de zona
            if self.current_zone_filter != "Todas":
                self.filtered_mesas = [
                    m for m in self.filtered_mesas 
                    if m.zona == self.current_zone_filter
                ]
            
            # Aplicar filtro de estado
            if self.current_status_filter != "Todos":
                estado_map = {
                    "Libre": "libre",
                    "Ocupada": "ocupada", 
                    "Reservada": "reservada"
                }
                estado_filtro = estado_map.get(self.current_status_filter)
                if estado_filtro:
                    self.filtered_mesas = [
                        m for m in self.filtered_mesas 
                        if m.estado == estado_filtro
                    ]
            
            # Actualizar vista
            QTimer.singleShot(50, self.populate_grid)
            
        except Exception as e:
            logger.error(f"Error aplicando filtros: {e}")
    
    def apply_search(self, search_text: str):
        """Aplica filtro de búsqueda por texto"""
        try:
            if not search_text:
                self.filtered_mesas = self.mesas.copy()
            else:
                # Buscar por número de mesa o zona
                search_lower = search_text.lower()
                self.filtered_mesas = [
                    m for m in self.mesas 
                    if (search_lower in str(m.numero).lower() or 
                        search_lower in m.zona.lower())
                ]
            
            # Aplicar otros filtros después de la búsqueda
            self.apply_filters()
            
        except Exception as e:
            logger.error(f"Error aplicando búsqueda: {e}")
    
    def refresh_mesas(self):
        """Refresca la vista de mesas"""
        self.apply_filters()
    
    def populate_grid(self):
        """Popula el grid de mesas con datos filtrados"""
        try:
            logger.debug("Poblando grid de mesas...")
            
            # Limpiar layout existente
            self.clear_layout()
            
            if not self.filtered_mesas:
                self.show_no_mesas_message()
                return
            
            # Crear widgets de mesa
            cols = 4  # 4 columnas por defecto
            
            for i, mesa in enumerate(self.filtered_mesas):
                row = i // cols
                col = i % cols
                
                # Crear widget de mesa
                mesa_widget = MesaWidget(mesa)
                mesa_widget.mesa_clicked.connect(self.mesa_clicked.emit)
                
                self.mesa_widgets.append(mesa_widget)
                self.mesas_layout.addWidget(mesa_widget, row, col)
            
            # Actualizar información de estado
            total_filtered = len(self.filtered_mesas)
            total_all = len(self.mesas)
            
            if total_filtered == total_all:
                status_text = f"Mostrando {total_all} mesa(s)"
            else:
                status_text = f"Mostrando {total_filtered} de {total_all} mesa(s)"
            
            self.status_info.setText(status_text)
            
            logger.debug(f"Grid poblado con {len(self.filtered_mesas)} mesas")
            
        except Exception as e:
            logger.error(f"Error poblando grid de mesas: {e}")
    
    def clear_layout(self):
        """Limpia todos los widgets del layout"""
        try:
            # Limpiar widgets de mesas
            self.mesa_widgets.clear()
            
            # Limpiar layout
            while self.mesas_layout.count():
                child = self.mesas_layout.takeAt(0)
                if child and child.widget():
                    widget = child.widget()
                    if widget:
                        widget.deleteLater()
                        
        except Exception as e:
            logger.error(f"Error limpiando layout: {e}")
    
    def show_no_mesas_message(self):
        """Muestra mensaje cuando no hay mesas que mostrar"""
        try:
            # Container para el mensaje
            message_container = QFrame()
            message_container.setStyleSheet("""
                QFrame {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f8f9fa, stop:1 #e9ecef);
                    border: 2px dashed #dee2e6;
                    border-radius: 16px;
                    padding: 30px;
                    margin: 20px;
                }
            """)
            
            container_layout = QVBoxLayout(message_container)
            container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            container_layout.setSpacing(16)
            
            # Determinar mensaje según filtros
            if self.current_zone_filter != "Todas" or self.current_status_filter != "Todos":
                # Mensaje de filtros activos
                icon_text = "🔍"
                title_text = "No se encontraron mesas"
                subtitle_text = f"No hay mesas que coincidan con los filtros aplicados"
                button_text = "🗑️ Limpiar Filtros"
                button_callback = self.clear_filters
            else:
                # Mensaje de no hay mesas
                icon_text = "🍽️"
                title_text = "No hay mesas disponibles"
                subtitle_text = "Configure las mesas de su restaurante para comenzar"
                button_text = "➕ Crear Primera Mesa"
                button_callback = self.nueva_mesa_requested.emit
            
            # Icono grande
            icon_label = QLabel(icon_text)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("""
                QLabel {
                    font-size: 48px;
                    color: #6c757d;
                    margin: 10px;
                }
            """)
            container_layout.addWidget(icon_label)
            
            # Título principal
            title_label = QLabel(title_text)
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 20px;
                    font-weight: bold;
                    color: #495057;
                    margin: 8px;
                }
            """)
            container_layout.addWidget(title_label)
            
            # Subtítulo
            subtitle_label = QLabel(subtitle_text)
            subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            subtitle_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #6c757d;
                    margin: 4px;
                }
            """)
            container_layout.addWidget(subtitle_label)
            
            # Botón de acción
            action_button = QPushButton(button_text)
            action_button.setFixedSize(200, 40)
            action_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #4CAF50, stop:1 #45a049);
                    border: none;
                    border-radius: 20px;
                    color: white;
                    font-weight: bold;
                    font-size: 14px;
                    margin: 10px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #45a049, stop:1 #3d8b40);
                }
                QPushButton:pressed {
                    background: #3d8b40;
                }
            """)
            action_button.clicked.connect(button_callback)
            
            # Centrar el botón
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(action_button)
            button_layout.addStretch()
            container_layout.addLayout(button_layout)
            
            # Agregar al layout principal ocupando todo el espacio
            self.mesas_layout.addWidget(message_container, 0, 0, 1, 4)
            
        except Exception as e:
            logger.error(f"Error mostrando mensaje de no mesas: {e}")
    
    def clear_filters(self):
        """Limpia todos los filtros activos"""
        self.current_zone_filter = "Todas"
        self.current_status_filter = "Todos"
        self.apply_filters()
    
    def set_zone_filter(self, zone: str):
        """Establece el filtro de zona"""
        self.current_zone_filter = zone
        self.apply_filters()
    
    def set_status_filter(self, status: str):
        """Establece el filtro de estado"""
        self.current_status_filter = status
        self.apply_filters()
    
    def set_view_mode(self, mode: str):
        """Establece el modo de vista"""
        self.view_mode = mode
        # TODO: Implementar vista de lista
        self.apply_filters()
    
    def refresh_data(self):
        """Refresca los datos de las mesas"""
        self.apply_filters()
    
    def update_mesa(self, mesa: Mesa):
        """Actualiza una mesa específica"""
        # Actualizar en la lista principal
        for i, m in enumerate(self.mesas):
            if m.id == mesa.id:
                self.mesas[i] = mesa
                break
        
        # Actualizar widgets visibles
        for widget in self.mesa_widgets:
            if widget.mesa.id == mesa.id:
                widget.update_mesa(mesa)
                break
        
        # Reaplicar filtros si es necesario
        self.apply_filters()
