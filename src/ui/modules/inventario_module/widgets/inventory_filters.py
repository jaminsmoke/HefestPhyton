"""
Widget de filtros para el inventario - Hefest v0.0.12
=====================================================

Widget especializado para filtrar productos en el inventario con múltiples
criterios de búsqueda avanzada, diseñado específicamente para hostelería.

FUNCIONALIDADES:
---------------
- Filtro por categoría (Bebidas, Alimentos, Limpieza, etc.)
- Filtro por proveedor
- Filtro por rango de stock (mínimo/máximo)
- Filtro por rango de precios
- Búsqueda por texto libre en nombre/descripción
- Filtros combinables con lógica AND
- Limpieza rápida de todos los filtros

SEÑALES EMITIDAS:
----------------
- filters_changed: Cuando cambian los criterios de filtro
- clear_filters: Cuando se limpian todos los filtros

INTEGRACIÓN:
-----------
- Se conecta con products_manager.py para filtrar la tabla
- Utiliza inventario_service_real.py para obtener datos de filtros

AUTOR: Hefest Development Team
VERSIÓN: v0.0.12
"""

import logging
from typing import List, Dict, Any
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QComboBox,
    QLineEdit,
    QPushButton,
    QCheckBox,
    QSlider,
    QLabel,
)
from PyQt6.QtCore import Qt, pyqtSignal

from src.utils.modern_styles import ModernStyles

logger = logging.getLogger(__name__)


class InventoryFiltersWidget(QWidget):
    """
    Widget para filtros avanzados de inventario.

    Características:
    - Filtro por categoría
    - Filtro por proveedor
    - Filtro por rango de stock
    - Filtro por rango de precio
    - Estado de producto
    - Búsqueda de texto
    """

    # Señales
    filters_changed = pyqtSignal(dict)  # Emite los filtros aplicados
    filters_cleared = pyqtSignal()  # Limpia todos los filtros

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modern_styles = ModernStyles()
        self.current_filters = {}
        self._setup_ui()
        self._apply_styles()
        self._connect_signals()

    def _setup_ui(self):
        """Configura la interfaz de filtros"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Título
        title_label = QLabel("🔍 Filtros de Inventario")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Grupo de filtros básicos
        basic_group = self._create_basic_filters_group()
        main_layout.addWidget(basic_group)

        # Grupo de filtros avanzados
        advanced_group = self._create_advanced_filters_group()
        main_layout.addWidget(advanced_group)

        # Botones de acción
        buttons_layout = self._create_action_buttons()
        main_layout.addLayout(buttons_layout)

        main_layout.addStretch()

    def _create_basic_filters_group(self) -> QGroupBox:
        """Crea el grupo de filtros básicos"""
        group = QGroupBox("Filtros Básicos")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)

        # Búsqueda por texto
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar producto...")
        layout.addWidget(QLabel("Búsqueda:"))
        layout.addWidget(self.search_input)

        # Filtro por categoría
        self.category_combo = QComboBox()
        self.category_combo.addItem("Todas las categorías", "")
        layout.addWidget(QLabel("Categoría:"))
        layout.addWidget(self.category_combo)

        # Filtro por proveedor
        self.supplier_combo = QComboBox()
        self.supplier_combo.addItem("Todos los proveedores", "")
        layout.addWidget(QLabel("Proveedor:"))
        layout.addWidget(self.supplier_combo)

        return group

    def _create_advanced_filters_group(self) -> QGroupBox:
        """Crea el grupo de filtros avanzados"""
        group = QGroupBox("Filtros Avanzados")
        layout = QVBoxLayout(group)
        layout.setSpacing(8)

        # Filtro por estado
        state_layout = QHBoxLayout()
        state_layout.addWidget(QLabel("Estado:"))

        self.state_all = QCheckBox("Todos")
        self.state_all.setChecked(True)
        self.state_good = QCheckBox("Bueno")
        self.state_low = QCheckBox("Bajo")
        self.state_critical = QCheckBox("Crítico")
        self.state_out = QCheckBox("Agotado")

        state_layout.addWidget(self.state_all)
        state_layout.addWidget(self.state_good)
        state_layout.addWidget(self.state_low)
        state_layout.addWidget(self.state_critical)
        state_layout.addWidget(self.state_out)
        state_layout.addStretch()

        layout.addLayout(state_layout)

        # Rango de stock
        stock_layout = QVBoxLayout()
        stock_layout.addWidget(QLabel("Rango de Stock:"))

        stock_controls = QHBoxLayout()
        self.stock_min_slider = QSlider(Qt.Orientation.Horizontal)
        self.stock_min_slider.setRange(0, 1000)
        self.stock_min_slider.setValue(0)
        self.stock_min_label = QLabel("0")

        self.stock_max_slider = QSlider(Qt.Orientation.Horizontal)
        self.stock_max_slider.setRange(0, 1000)
        self.stock_max_slider.setValue(1000)
        self.stock_max_label = QLabel("1000")

        stock_controls.addWidget(QLabel("Mín:"))
        stock_controls.addWidget(self.stock_min_slider)
        stock_controls.addWidget(self.stock_min_label)
        stock_controls.addWidget(QLabel("Máx:"))
        stock_controls.addWidget(self.stock_max_slider)
        stock_controls.addWidget(self.stock_max_label)

        stock_layout.addLayout(stock_controls)
        layout.addLayout(stock_layout)

        return group

    def _create_action_buttons(self) -> QHBoxLayout:
        """Crea los botones de acción"""
        layout = QHBoxLayout()

        # Botón aplicar filtros
        self.apply_btn = QPushButton("Aplicar Filtros")
        self.apply_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """
        )

        # Botón limpiar filtros
        self.clear_btn = QPushButton("Limpiar")
        self.clear_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #545b62;
            }
        """
        )

        layout.addStretch()
        layout.addWidget(self.apply_btn)
        layout.addWidget(self.clear_btn)

        return layout

    def _connect_signals(self):
        """Conecta las señales de los widgets"""
        # Conectar cambios de filtros básicos
        self.search_input.textChanged.connect(self._on_filter_changed)
        self.category_combo.currentTextChanged.connect(self._on_filter_changed)
        self.supplier_combo.currentTextChanged.connect(self._on_filter_changed)

        # Conectar checkboxes de estado
        self.state_all.toggled.connect(self._on_state_all_changed)
        self.state_good.toggled.connect(self._on_filter_changed)
        self.state_low.toggled.connect(self._on_filter_changed)
        self.state_critical.toggled.connect(self._on_filter_changed)
        self.state_out.toggled.connect(self._on_filter_changed)

        # Conectar sliders
        self.stock_min_slider.valueChanged.connect(self._on_stock_min_changed)
        self.stock_max_slider.valueChanged.connect(self._on_stock_max_changed)

        # Conectar botones
        self.apply_btn.clicked.connect(self._apply_filters)
        self.clear_btn.clicked.connect(self._clear_filters)

    def _apply_styles(self):
        """Aplica estilos modernos"""
        colors = self.modern_styles.COLORS
        self.setStyleSheet(
            f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {colors['border']};
                border-radius: 8px;
                margin-top: 6px;
                padding-top: 12px;
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
            
            QLineEdit {{
                padding: 6px;
                border: 1px solid {colors['border']};
                border-radius: 4px;
                background-color: {colors['surface']};
            }}
            
            QComboBox {{
                padding: 6px;
                border: 1px solid {colors['border']};
                border-radius: 4px;
                background-color: {colors['surface']};
            }}
            
            QCheckBox {{
                spacing: 5px;
            }}
            
            QSlider::groove:horizontal {{
                border: 1px solid {colors['border']};
                height: 6px;
                background: {colors['surface_variant']};
                border-radius: 3px;
            }}
            
            QSlider::handle:horizontal {{
                background: {colors['primary']};
                border: 1px solid {colors['primary']};
                width: 14px;
                border-radius: 7px;
                margin: -4px 0;
            }}
        """
        )

    def _on_filter_changed(self):
        """Maneja cambios en los filtros"""
        # Auto-aplicar filtros en tiempo real (opcional)

    def _on_state_all_changed(self, checked: bool):
        """Maneja el cambio del checkbox 'Todos'"""
        if checked:
            self.state_good.setChecked(False)
            self.state_low.setChecked(False)
            self.state_critical.setChecked(False)
            self.state_out.setChecked(False)
        self._on_filter_changed()

    def _on_stock_min_changed(self, value: int):
        """Maneja cambios en el slider mínimo de stock"""
        self.stock_min_label.setText(str(value))
        if value > self.stock_max_slider.value():
            self.stock_max_slider.setValue(value)
        self._on_filter_changed()

    def _on_stock_max_changed(self, value: int):
        """Maneja cambios en el slider máximo de stock"""
        self.stock_max_label.setText(str(value))
        if value < self.stock_min_slider.value():
            self.stock_min_slider.setValue(value)
        self._on_filter_changed()

    def _apply_filters(self):
        """Aplica los filtros actuales"""
        filters = {
            "search_text": self.search_input.text().strip(),
            "category": self.category_combo.currentData() or "",
            "supplier": self.supplier_combo.currentData() or "",
            "states": self._get_selected_states(),
            "stock_min": self.stock_min_slider.value(),
            "stock_max": self.stock_max_slider.value(),
        }

        self.current_filters = filters
        self.filters_changed.emit(filters)

    def _clear_filters(self):
        """Limpia todos los filtros"""
        self.search_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.supplier_combo.setCurrentIndex(0)
        self.state_all.setChecked(True)
        self.stock_min_slider.setValue(0)
        self.stock_max_slider.setValue(1000)

        self.current_filters = {}
        self.filters_cleared.emit()

    def _get_selected_states(self) -> List[str]:
        """Obtiene los estados seleccionados"""
        if self.state_all.isChecked():
            return ["all"]

        states = []
        if self.state_good.isChecked():
            states.append("good")
        if self.state_low.isChecked():
            states.append("low")
        if self.state_critical.isChecked():
            states.append("critical")
        if self.state_out.isChecked():
            states.append("out")

        return states

    def load_categories(self, categories: List[str]):
        """Carga las categorías disponibles"""
        self.category_combo.clear()
        self.category_combo.addItem("Todas las categorías", "")
        for category in categories:
            self.category_combo.addItem(category, category)

    def load_suppliers(self, suppliers: List[str]):
        """Carga los proveedores disponibles"""
        self.supplier_combo.clear()
        self.supplier_combo.addItem("Todos los proveedores", "")
        for supplier in suppliers:
            self.supplier_combo.addItem(supplier, supplier)

    def get_current_filters(self) -> Dict[str, Any]:
        """Obtiene los filtros actuales"""
        return self.current_filters.copy()
