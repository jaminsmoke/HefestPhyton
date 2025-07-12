"""
Utilidades comunes para el módulo de inventario
Elimina duplicación de código en supplier_manager, category_manager, y product_dialogs
"""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QTextEdit,
    QCheckBox,
    QGroupBox,
    QFrame,
    QScrollArea,
    QMessageBox,
    QDialog,
    QDialogButtonBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

logger = logging.getLogger(__name__)


class InventoryDialogBase(QDialog):
    """Clase base para diálogos de inventario con funcionalidad común"""

    # Señales comunes
    item_saved = pyqtSignal(dict)
    item_updated = pyqtSignal(dict)
    item_deleted = pyqtSignal(int)

    def __init__(self, parent=None, title="Dialog", size=(400, 300)):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(*size)
        self.setModal(True)

        # Configuración común
        self._setup_ui()
        self._setup_connections()
        self._apply_styles()

    def _setup_ui(self):
        """Configuración base de UI - debe ser implementada por subclases"""
        self.main_layout = QVBoxLayout(self)

        # Contenedor principal con scroll
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.content_layout = QVBoxLayout(self.scroll_widget)

        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        # Botones estándar
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.button_box)

    def _setup_connections(self):
        """Configuración de conexiones base"""
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def _apply_styles(self):
        """Aplica estilos comunes"""
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 6px;
                margin-top: 6px;
                padding-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """
        )

    def add_form_section(self, title: str, layout: QFormLayout) -> QGroupBox:
        """Agrega una sección con formulario"""
        group = QGroupBox(title)
        group.setLayout(layout)
        self.content_layout.addWidget(group)
        return group

    def add_widget_section(self, title: str, widget: QWidget) -> QGroupBox:
        """Agrega una sección con widget personalizado"""
        group = QGroupBox(title)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        group.setLayout(layout)
        self.content_layout.addWidget(group)
        return group

    def create_form_field(
        self, label: str, widget: QWidget, required: bool = False
    ) -> Tuple[QLabel, QWidget]:
        """Crea un campo de formulario estandarizado"""
        label_widget = QLabel(label + ("*" if required else ""))
        if required:
            label_widget.setStyleSheet("color: #dc3545; font-weight: bold;")
        return label_widget, widget

    def show_error(self, message: str, title: str = "Error"):
        """Muestra mensaje de error estándar"""
        QMessageBox.critical(self, title, message)

    def show_success(self, message: str, title: str = "Éxito"):
        """Muestra mensaje de éxito estándar"""
        QMessageBox.information(self, title, message)

    def show_warning(self, message: str, title: str = "Advertencia"):
        """Muestra mensaje de advertencia estándar"""
        QMessageBox.warning(self, title, message)

    def confirm_action(self, message: str, title: str = "Confirmar") -> bool:
        """Solicita confirmación del usuario"""
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        return reply == QMessageBox.StandardButton.Yes


class InventoryManagerBase(QWidget):
    """Clase base para gestores de inventario (suppliers, categories, products)"""

    # Señales comunes
    item_selected = pyqtSignal(dict)
    items_changed = pyqtSignal()

    def __init__(self, db_manager, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager

        # Estado común
        self.current_item = None
        self.items_cache = []

        self._setup_ui()
        self._setup_connections()
        self._load_data()

    def _setup_ui(self):
        """Configuración base de UI"""
        self.main_layout = QVBoxLayout(self)

        # Header con botones de acción
        self.header_layout = QHBoxLayout()

        # Título
        self.title_label = QLabel("Manager")
        self.title_label.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            color: #333;
            margin: 10px 0;
        """
        )

        # Botones de acción
        self.add_btn = QPushButton("Agregar")
        self.edit_btn = QPushButton("Editar")
        self.delete_btn = QPushButton("Eliminar")
        self.refresh_btn = QPushButton("Actualizar")

        # Estado inicial de botones
        self.edit_btn.setEnabled(False)
        self.delete_btn.setEnabled(False)

        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.add_btn)
        self.header_layout.addWidget(self.edit_btn)
        self.header_layout.addWidget(self.delete_btn)
        self.header_layout.addWidget(self.refresh_btn)

        # Tabla de datos
        self.table = QTableWidget()
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)

        # Layout principal
        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addWidget(self.table)

        self._apply_styles()

    def _setup_connections(self):
        """Configuración de conexiones base"""
        self.add_btn.clicked.connect(self.add_item)
        self.edit_btn.clicked.connect(self.edit_item)
        self.delete_btn.clicked.connect(self.delete_item)
        self.refresh_btn.clicked.connect(self.refresh_data)

        self.table.selectionModel().currentRowChanged.connect(
            self._on_selection_changed
        )
        self.table.itemDoubleClicked.connect(self.edit_item)

    def _apply_styles(self):
        """Aplica estilos comunes"""
        self.setStyleSheet(
            """
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
            QTableWidget {
                gridline-color: #dee2e6;
                background-color: white;
                alternate-background-color: #f8f9fa;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """
        )

    def _on_selection_changed(self, current, previous):
        """Maneja cambios de selección"""
        has_selection = current.isValid()
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

        if has_selection:
            row = current.row()
            if 0 <= row < len(self.items_cache):
                self.current_item = self.items_cache[row]
                self.item_selected.emit(self.current_item)
        else:
            self.current_item = None

    def setup_table_columns(
        self, headers: List[str], widths: Optional[List[int]] = None
    ):
        """Configura las columnas de la tabla"""
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        if widths:
            for i, width in enumerate(widths):
                if i < len(headers):
                    self.table.setColumnWidth(i, width)

    def populate_table(self, items: List[Dict[str, Any]], field_mapping: List[str]):
        """Puebla la tabla con datos"""
        self.items_cache = items
        self.table.setRowCount(len(items))

        for row, item in enumerate(items):
            for col, field in enumerate(field_mapping):
                value = item.get(field, "")
                if value is None:
                    value = ""

                table_item = QTableWidgetItem(str(value))
                table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, col, table_item)

    def get_selected_item(self) -> Optional[Dict[str, Any]]:
        """Obtiene el elemento seleccionado"""
        return self.current_item

    def refresh_data(self):
        """Actualiza los datos - debe ser implementado por subclases"""
        self._load_data()

    def _load_data(self):
        """Carga datos - debe ser implementado por subclases"""
        pass

    def add_item(self):
        """Agrega nuevo elemento - debe ser implementado por subclases"""
        pass

    def edit_item(self):
        """Edita elemento - debe ser implementado por subclases"""
        pass

    def delete_item(self):
        """Elimina elemento - debe ser implementado por subclases"""
        pass


class InventoryValidationUtils:
    """Utilidades de validación para módulos de inventario"""

    @staticmethod
    def validate_required_field(value: str, field_name: str) -> Tuple[bool, str]:
        """Valida campo requerido"""
        if not value or not value.strip():
            return False, f"{field_name} es requerido"
        return True, ""

    @staticmethod
    def validate_numeric_field(
        value: str, field_name: str, min_val: float = 0, max_val: Optional[float] = None
    ) -> Tuple[bool, str]:
        """Valida campo numérico"""
        try:
            num_val = float(value)
            if num_val < min_val:
                return False, f"{field_name} debe ser mayor o igual a {min_val}"
            if max_val is not None and num_val > max_val:
                return False, f"{field_name} debe ser menor o igual a {max_val}"
            return True, ""
        except ValueError:
            return False, f"{field_name} debe ser un número válido"

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Valida formato de email"""
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, email):
            return True, ""
        return False, "Formato de email inválido"

    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """Valida formato de teléfono"""
        import re

        # Permite varios formatos de teléfono
        pattern = r"^[\+]?[1-9][\d\s\-\(\)]{7,15}$"
        if re.match(pattern, phone.replace(" ", "")):
            return True, ""
        return False, "Formato de teléfono inválido"

    @staticmethod
    def validate_text_length(
        value: str, field_name: str, min_length: int = 1, max_length: int = 255
    ) -> bool:
        """Valida longitud de texto"""
        if not isinstance(value, str):
            return False
        if len(value.strip()) < min_length:
            return False
        if len(value.strip()) > max_length:
            return False
        return True

    @staticmethod
    def validate_unique_field(
        value: str,
        existing_values: List[str],
        field_name: str,
        ignore_value: str = None,
    ) -> Tuple[bool, str]:
        """Valida que un campo sea único"""
        if ignore_value and value == ignore_value:
            return True, ""
        if value in existing_values:
            return False, f"{field_name} ya existe"
        return True, ""


class CommonInventoryStyles:
    """Estilos comunes para módulos de inventario"""

    @staticmethod
    def get_dialog_style():
        """Estilo para diálogos"""
        return """
            QDialog {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 12px;
                color: #333;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px;
                font-size: 12px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
                border-color: #007bff;
                outline: none;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """

    @staticmethod
    def get_manager_style():
        """Estilo para gestores"""
        return """
            QWidget {
                background-color: #ffffff;
            }
            QTableWidget {
                gridline-color: #dee2e6;
                background-color: white;
                alternate-background-color: #f8f9fa;
                border: 1px solid #dee2e6;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
            QHeaderView::section {
                background-color: #e9ecef;
                padding: 8px;
                border: none;
                font-weight: bold;
                color: #333;
            }
        """
