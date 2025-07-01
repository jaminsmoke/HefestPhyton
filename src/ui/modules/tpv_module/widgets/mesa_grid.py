"""
Grid de Mesas - Widget que gestiona y muestra múltiples mesas
"""

import logging
from typing import List, Dict, Optional, Callable
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QScrollArea,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from ..components.mesa_widget import MesaWidget
from services.tpv_service import Mesa
from ..mesa_event_bus import mesa_event_bus

logger = logging.getLogger(__name__)


class MesaGridWidget(QWidget):
    """Widget que gestiona y muestra un grid de mesas"""

    mesa_selected = pyqtSignal(Mesa)
    mesa_double_clicked = pyqtSignal(Mesa)
    filter_changed = pyqtSignal(str, str)  # filtro_texto, filtro_estado
    refresh_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesas: List[Mesa] = []
        self.mesa_widgets: Dict[int, MesaWidget] = {}
        self._columns = 5  # Número de columnas por defecto
        self._selected_mesa: Optional[Mesa] = None

        # Timer para búsqueda con delay
        self._search_timer = QTimer()
        self._search_timer.setSingleShot(True)
        self._search_timer.timeout.connect(self._apply_filters)

        self.setup_ui()
        self._connect_event_bus()

    def _connect_event_bus(self):
        mesa_event_bus.mesa_clicked.connect(self._on_mesa_clicked)
        mesa_event_bus.mesa_actualizada.connect(self.update_mesa)
        mesa_event_bus.mesas_actualizadas.connect(self.refresh_mesas)
        mesa_event_bus.alias_cambiado.connect(self._on_alias_cambiado)

    def _on_alias_cambiado(self, mesa, nuevo_alias):
        if mesa.id in self.mesa_widgets:
            self.mesa_widgets[mesa.id].mesa.alias = nuevo_alias
            self.mesa_widgets[mesa.id].update_mesa(self.mesa_widgets[mesa.id].mesa)

    def setup_ui(self):
        """Configura la interfaz del grid de mesas"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header con controles
        self.setup_header(layout)

        # Área de scroll para el grid
        self.setup_scroll_area(layout)

        # Footer con información
        self.setup_footer(layout)

    def setup_header(self, parent_layout: QVBoxLayout):
        """Configura el header con controles de filtrado"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #F7FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                padding: 8px;
            }
        """)

        header_layout = QHBoxLayout(header_frame)

        # Título
        title = QLabel("🍽️ Gestión de Mesas")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2D3748; padding: 0 10px;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Filtros
        filter_layout = QHBoxLayout()

        # Búsqueda por texto
        search_label = QLabel("Buscar:")
        search_label.setStyleSheet("color: #4A5568; font-weight: bold;")
        filter_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Mesa, zona...")
        self.search_input.setMinimumWidth(150)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CBD5E0;
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3182CE;
                outline: none;
            }
        """)
        self.search_input.textChanged.connect(self._on_search_changed)
        filter_layout.addWidget(self.search_input)

        # Filtro por estado
        estado_label = QLabel("Estado:")
        estado_label.setStyleSheet("color: #4A5568; font-weight: bold; margin-left: 10px;")
        filter_layout.addWidget(estado_label)

        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Todas", "Libres", "Ocupadas", "Reservadas", "Limpieza"])
        self.estado_combo.setMinimumWidth(100)
        self.estado_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #CBD5E0;
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 12px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #3182CE;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #4A5568;
            }
        """)
        self.estado_combo.currentTextChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.estado_combo)

        # Botón de refresh
        self.refresh_btn = QPushButton("🔄")
        self.refresh_btn.setToolTip("Actualizar mesas")
        self.refresh_btn.setMaximumSize(32, 32)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3182CE;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2C5282;
            }
            QPushButton:pressed {
                background-color: #2A4A7C;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        filter_layout.addWidget(self.refresh_btn)

        header_layout.addLayout(filter_layout)
        parent_layout.addWidget(header_frame)

    def setup_scroll_area(self, parent_layout: QVBoxLayout):
        """Configura el área de scroll para el grid"""
        # Scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: 1px solid #E2E8F0;
                border-radius: 6px;
                background-color: white;
            }
        """)

        # Widget contenedor para el grid
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(15, 15, 15, 15)

        # Configurar scroll area
        scroll_area.setWidget(self.grid_container)
        parent_layout.addWidget(scroll_area)

    def setup_footer(self, parent_layout: QVBoxLayout):
        """Configura el footer con información de estado"""
        self.info_label = QLabel("Cargando mesas...")
        self.info_label.setStyleSheet("""
            QLabel {
                color: #718096;
                font-size: 12px;
                padding: 5px 10px;
                background-color: #F7FAFC;
                border: 1px solid #E2E8F0;
                border-radius: 4px;
            }
        """)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        parent_layout.addWidget(self.info_label)

    def set_mesas(self, mesas: List[Mesa]):
        """Establece la lista de mesas y actualiza el grid"""
        self.mesas = mesas
        self._create_mesa_widgets()
        self._apply_filters()
        self._update_info_label()

    def _create_mesa_widgets(self):
        """Crea los widgets de mesa"""
        # Limpiar widgets existentes
        for widget in self.mesa_widgets.values():
            widget.deleteLater()
        self.mesa_widgets.clear()

        # Crear nuevos widgets
        for mesa in self.mesas:
            mesa_widget = MesaWidget(mesa)
            self.mesa_widgets[mesa.id] = mesa_widget

    def _apply_filters(self):
        """Aplica los filtros actuales y reorganiza el grid"""
        # Limpiar grid
        self._clear_grid()

        # Obtener filtros
        search_text = self.search_input.text().lower().strip()
        estado_filter = self.estado_combo.currentText()

        # Filtrar mesas
        filtered_mesas = []
        for mesa in self.mesas:
            # Filtro por texto
            if search_text:
                mesa_text = f"{mesa.numero} {mesa.zona}".lower()
                if search_text not in mesa_text:
                    continue

            # Filtro por estado
            if estado_filter != "Todas":
                estado_map = {
                    "Libres": "libre",
                    "Ocupadas": "ocupada",
                    "Reservadas": "reservada",
                    "Limpieza": "limpieza"
                }
                if mesa.estado != estado_map.get(estado_filter, ""):
                    continue

            filtered_mesas.append(mesa)

        # Mostrar mesas filtradas
        self._populate_grid(filtered_mesas)

        # Emitir señal de cambio de filtro
        self.filter_changed.emit(search_text, estado_filter)

    def _clear_grid(self):
        """Limpia el grid de mesas"""
        for i in reversed(range(self.grid_layout.count())):
            item = self.grid_layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    self.grid_layout.removeWidget(widget)
                    # No eliminar el widget, solo ocultarlo
                    widget.setParent(None)

    def _populate_grid(self, mesas: List[Mesa]):
        """Puebla el grid con las mesas filtradas"""
        if not mesas:
            # Mostrar mensaje de "no hay mesas"
            no_mesas_label = QLabel("No se encontraron mesas con los filtros seleccionados")
            no_mesas_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_mesas_label.setStyleSheet("""
                QLabel {
                    color: #718096;
                    font-size: 14px;
                    font-style: italic;
                    padding: 40px;
                }
            """)
            self.grid_layout.addWidget(no_mesas_label, 0, 0, 1, self._columns)
            return

        # Añadir widgets al grid
        row, col = 0, 0
        for mesa in mesas:
            if mesa.id in self.mesa_widgets:
                widget = self.mesa_widgets[mesa.id]
                widget.setParent(self.grid_container)
                self.grid_layout.addWidget(widget, row, col)

                col += 1
                if col >= self._columns:
                    col = 0
                    row += 1

        # Añadir stretch al final
        self.grid_layout.setRowStretch(row + 1, 1)

    def _update_info_label(self):
        """Actualiza la etiqueta de información"""
        total = len(self.mesas)
        libres = sum(1 for m in self.mesas if m.estado == "libre")
        ocupadas = sum(1 for m in self.mesas if m.estado == "ocupada")
        reservadas = sum(1 for m in self.mesas if m.estado == "reservada")

        info_text = f"Total: {total} mesas | 🟢 Libres: {libres} | 🔴 Ocupadas: {ocupadas} | 🟠 Reservadas: {reservadas}"
        self.info_label.setText(info_text)

    def _on_search_changed(self):
        """Maneja el cambio en el texto de búsqueda con delay"""
        self._search_timer.stop()
        self._search_timer.start(300)  # 300ms de delay

    def _on_filter_changed(self):
        """Maneja el cambio en el filtro de estado"""
        self._apply_filters()

    def _on_mesa_clicked(self, mesa: Mesa):
        """Maneja el clic simple en una mesa (ahora por event bus)"""
        self._selected_mesa = mesa
        self._highlight_selected_mesa()
        self.mesa_selected.emit(mesa)

    def _on_mesa_single_click(self):
        """Maneja el clic simple (usado para detectar doble clic)"""
        # Este método se puede usar para implementar doble clic si es necesario
        pass

    def _on_mesa_status_changed(self, mesa: Mesa, nuevo_estado: str):
        """Maneja el cambio de estado de una mesa"""
        # Actualizar la mesa en la lista
        for i, m in enumerate(self.mesas):
            if m.id == mesa.id:
                self.mesas[i] = mesa
                break

        self._update_info_label()

    def _highlight_selected_mesa(self):
        """Resalta la mesa seleccionada"""
        for mesa_id, widget in self.mesa_widgets.items():
            widget.set_highlight(mesa_id == self._selected_mesa.id if self._selected_mesa else False)

    def update_mesa(self, mesa: Mesa):
        """Actualiza una mesa específica"""
        # Actualizar en la lista
        for i, m in enumerate(self.mesas):
            if m.id == mesa.id:
                self.mesas[i] = mesa
                break

        # Actualizar widget
        if mesa.id in self.mesa_widgets:
            self.mesa_widgets[mesa.id].update_mesa(mesa)

        self._update_info_label()

    def refresh_mesas(self, mesas: List[Mesa]):
        """Refresca completamente la lista de mesas"""
        self.set_mesas(mesas)

    def get_selected_mesa(self) -> Optional[Mesa]:
        """Retorna la mesa actualmente seleccionada"""
        return self._selected_mesa

    def set_columns(self, columns: int):
        """Establece el número de columnas del grid"""
        if columns > 0:
            self._columns = columns
            self._apply_filters()

    def clear_selection(self):
        """Limpia la selección actual"""
        self._selected_mesa = None
        self._highlight_selected_mesa()
