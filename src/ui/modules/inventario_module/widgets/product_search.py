"""
Widget de búsqueda de productos - Hefest v0.0.12
===============================================

Widget especializado para búsqueda avanzada de productos con funcionalidades
de autocompletado, filtros rápidos y búsqueda inteligente para hostelería.

FUNCIONALIDADES:
---------------
- Búsqueda en tiempo real (while typing)
- Autocompletado inteligente con sugerencias
- Búsqueda por código de producto/EAN
- Búsqueda por nombre y descripción
- Filtros rápidos por categoría más usadas
- Historial de búsquedas recientes
- Búsqueda fonética para nombres similares

CAMPOS DE BÚSQUEDA:
------------------
- Nombre del producto
- Código/EAN/SKU
- Descripción/notas
- Proveedor
- Categoría

CARACTERÍSTICAS TÉCNICAS:
------------------------
- Debounce de 300ms para optimizar rendimiento
- Límite de resultados para evitar sobrecargas
- Cache de resultados para búsquedas repetidas
- Destacado de términos de búsqueda en resultados

SEÑALES EMITIDAS:
----------------
- search_changed: Cuando cambia el término de búsqueda
- product_selected: Cuando se selecciona un producto específico

AUTOR: Hefest Development Team
VERSIÓN: v0.0.12
"""

import logging
from typing import List, Dict, Any, Optional, Callable
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QCompleter,
    QPushButton,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal, QStringListModel, QTimer
from PyQt6.QtGui import QFont, QColor

from src.utils.modern_styles import ModernStyles

logger = logging.getLogger(__name__)


class ProductSearchWidget(QWidget):
    """
    Widget de búsqueda avanzada de productos.

    Características:
    - Búsqueda en tiempo real
    - Autocompletado
    - Historial de búsquedas
    - Filtros rápidos por categoría
    - Resultados interactivos
    """

    # Señales
    search_changed = pyqtSignal(str)  # Cambio en búsqueda
    product_selected = pyqtSignal(dict)  # Producto seleccionado
    filter_applied = pyqtSignal(str, str)  # Filtro aplicado (tipo, valor)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modern_styles = ModernStyles()
        self.search_history: List[str] = []
        self.product_suggestions: List[Dict[str, Any]] = []
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self._perform_search)

        self._setup_ui()
        self._apply_styles()
        self._connect_signals()

    def _setup_ui(self):
        """Configura la interfaz de búsqueda"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Título
        title_label = QLabel("🔍 Búsqueda de Productos")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        main_layout.addWidget(title_label)

        # Campo de búsqueda principal
        search_layout = self._create_search_section()
        main_layout.addLayout(search_layout)

        # Filtros rápidos
        filters_layout = self._create_quick_filters()
        main_layout.addLayout(filters_layout)

        # Resultados de búsqueda
        results_widget = self._create_results_section()
        main_layout.addWidget(results_widget)

        # Historial
        history_widget = self._create_history_section()
        main_layout.addWidget(history_widget)

        main_layout.addStretch()

    def _create_search_section(self) -> QVBoxLayout:
        """Crea la sección de búsqueda principal"""
        layout = QVBoxLayout()
        layout.setSpacing(8)

        # Campo de búsqueda
        search_input_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Buscar productos por nombre, código o categoría..."
        )
        self.search_input.setMinimumHeight(35)
        search_input_layout.addWidget(self.search_input)

        # Botón de búsqueda
        self.search_btn = QPushButton("🔍")
        self.search_btn.setFixedSize(35, 35)
        self.search_btn.setToolTip("Buscar")
        search_input_layout.addWidget(self.search_btn)

        # Botón limpiar
        self.clear_btn = QPushButton("✖")
        self.clear_btn.setFixedSize(35, 35)
        self.clear_btn.setToolTip("Limpiar búsqueda")
        search_input_layout.addWidget(self.clear_btn)

        layout.addLayout(search_input_layout)

        # Configurar autocompletado
        self.completer = QCompleter()
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.search_input.setCompleter(self.completer)

        return layout

    def _create_quick_filters(self) -> QHBoxLayout:
        """Crea los filtros rápidos"""
        layout = QHBoxLayout()

        # Etiqueta
        filters_label = QLabel("Filtros rápidos:")
        filters_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(filters_label)

        # Botones de filtro
        self.filter_buttons = {}

        filter_options = [
            ("stock_bajo", "📉 Stock Bajo", "#ffc107"),
            ("agotado", "🚫 Agotados", "#dc3545"),
            ("mas_vendidos", "⭐ Más Vendidos", "#28a745"),
            ("nuevos", "🆕 Nuevos", "#17a2b8"),
        ]

        for filter_key, filter_text, color in filter_options:
            btn = QPushButton(filter_text)
            btn.setCheckable(True)
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background-color: white;
                    border: 2px solid {color};
                    color: {color};
                    padding: 4px 8px;
                    border-radius: 15px;
                    font-size: 11px;
                    font-weight: bold;
                }}
                QPushButton:checked {{
                    background-color: {color};
                    color: white;
                }}
                QPushButton:hover {{
                    background-color: {color};
                    color: white;
                }}
            """
            )

            self.filter_buttons[filter_key] = btn
            layout.addWidget(btn)

        layout.addStretch()
        return layout

    def _create_results_section(self) -> QFrame:
        """Crea la sección de resultados"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(
            """
            QFrame {
                border: 1px solid #e9ecef;
                border-radius: 8px;
                background-color: white;
            }
        """
        )

        layout = QVBoxLayout(frame)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        # Título de resultados
        self.results_title = QLabel("Resultados de búsqueda")
        self.results_title.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(self.results_title)

        # Lista de resultados
        self.results_list = QListWidget()
        self.results_list.setMaximumHeight(200)
        self.results_list.setStyleSheet(
            """
            QListWidget {
                border: none;
                outline: none;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f8f9fa;
            }
            QListWidget::item:hover {
                background-color: #f8f9fa;
            }
            QListWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
        """
        )
        layout.addWidget(self.results_list)

        # Mensaje cuando no hay resultados
        self.no_results_label = QLabel("No se encontraron productos")
        self.no_results_label.setStyleSheet(
            "color: #6c757d; font-style: italic; text-align: center;"
        )
        self.no_results_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_results_label.hide()
        layout.addWidget(self.no_results_label)

        return frame

    def _create_history_section(self) -> QFrame:
        """Crea la sección de historial"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(
            """
            QFrame {
                border: 1px solid #e9ecef;
                border-radius: 8px;
                background-color: #f8f9fa;
            }
        """
        )

        layout = QVBoxLayout(frame)
        layout.setSpacing(6)
        layout.setContentsMargins(12, 8, 12, 8)

        # Header del historial
        history_header = QHBoxLayout()

        history_title = QLabel("📝 Búsquedas recientes")
        history_title.setStyleSheet(
            "font-weight: bold; font-size: 11px; color: #6c757d;"
        )
        history_header.addWidget(history_title)

        # Botón limpiar historial
        self.clear_history_btn = QPushButton("Limpiar")
        self.clear_history_btn.setStyleSheet(
            """
            QPushButton {
                background: none;
                border: none;
                color: #007bff;
                font-size: 10px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #0056b3;
            }
        """
        )
        history_header.addWidget(self.clear_history_btn)

        layout.addLayout(history_header)

        # Lista de historial
        self.history_list = QListWidget()
        self.history_list.setMaximumHeight(80)
        self.history_list.setStyleSheet(
            """
            QListWidget {
                border: none;
                background-color: transparent;
                outline: none;
            }
            QListWidget::item {
                padding: 2px 4px;
                color: #6c757d;
                font-size: 10px;
            }
            QListWidget::item:hover {
                background-color: #e9ecef;
                color: #495057;
            }
        """
        )
        layout.addWidget(self.history_list)

        return frame

    def _connect_signals(self):
        """Conecta las señales de los widgets"""
        # Campo de búsqueda
        self.search_input.textChanged.connect(self._on_search_text_changed)
        self.search_input.returnPressed.connect(self._perform_search)

        # Botones
        self.search_btn.clicked.connect(self._perform_search)
        self.clear_btn.clicked.connect(self._clear_search)
        self.clear_history_btn.clicked.connect(self._clear_history)

        # Lista de resultados
        self.results_list.itemClicked.connect(self._on_result_selected)
        self.results_list.itemDoubleClicked.connect(self._on_result_double_clicked)

        # Lista de historial
        self.history_list.itemClicked.connect(self._on_history_selected)

        # Filtros rápidos
        for filter_key, btn in self.filter_buttons.items():
            btn.clicked.connect(
                lambda checked, key=filter_key: self._on_filter_clicked(key, checked)
            )

        # Completer
        self.completer.activated.connect(self._on_completer_activated)

    def _apply_styles(self):
        """Aplica estilos modernos"""
        colors = self.modern_styles.COLORS

        self.setStyleSheet(
            f"""
            QLineEdit {{
                border: 2px solid {colors['border']};
                border-radius: 6px;
                padding: 8px;
                font-size: 13px;
                background-color: {colors['surface']};
            }}

            QLineEdit:focus {{
                border-color: {colors['primary']};
            }}

            QPushButton {{
                background-color: {colors['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: {colors['primary_hover']};
            }}
        """
        )

    def _on_search_text_changed(self, text: str):
        """Maneja cambios en el texto de búsqueda"""
        # Iniciar búsqueda con delay para evitar demasiadas consultas
        self.search_timer.stop()
        if text.strip():
            self.search_timer.start(300)  # 300ms delay
        else:
            self._clear_results()

    def _perform_search(self):
        """Realiza la búsqueda"""
        search_text = self.search_input.text().strip()

        if not search_text:
            return

        # Añadir al historial
        self._add_to_history(search_text)

        # Emitir señal de búsqueda
        self.search_changed.emit(search_text)

    def _clear_search(self):
        """Limpia la búsqueda"""
        self.search_input.clear()
        self._clear_results()

        # Desactivar filtros
        for btn in self.filter_buttons.values():
            btn.setChecked(False)

    def _clear_results(self):
        """Limpia los resultados de búsqueda"""
        self.results_list.clear()
        self.no_results_label.hide()
        self.results_title.setText("Resultados de búsqueda")

    def _on_result_selected(self, item: QListWidgetItem):
        """Maneja selección de resultado"""
        data = item.data(Qt.ItemDataRole.UserRole)
        if data:
            self.product_selected.emit(data)

    def _on_result_double_clicked(self, item: QListWidgetItem):
        """Maneja doble clic en resultado"""
        self._on_result_selected(item)

    def _on_history_selected(self, item: QListWidgetItem):
        """Maneja selección del historial"""
        self.search_input.setText(item.text())
        self._perform_search()

    def _on_filter_clicked(self, filter_key: str, checked: bool):
        """Maneja clic en filtro rápido"""
        if checked:
            # Desactivar otros filtros (solo uno activo a la vez)
            for key, btn in self.filter_buttons.items():
                if key != filter_key:
                    btn.setChecked(False)

            self.filter_applied.emit("quick_filter", filter_key)
        else:
            self.filter_applied.emit("quick_filter", "")

    def _on_completer_activated(self, text: str):
        """Maneja activación del autocompletado"""
        self.search_input.setText(text)
        self._perform_search()

    def _add_to_history(self, search_text: str):
        """Añade una búsqueda al historial"""
        if search_text in self.search_history:
            self.search_history.remove(search_text)

        self.search_history.insert(0, search_text)

        # Mantener solo los últimos 10
        self.search_history = self.search_history[:10]

        self._update_history_display()

    def _update_history_display(self):
        """Actualiza la visualización del historial"""
        self.history_list.clear()
        for search in self.search_history:
            item = QListWidgetItem(search)
            self.history_list.addItem(item)

    def _clear_history(self):
        """Limpia el historial de búsquedas"""
        self.search_history.clear()
        self.history_list.clear()

    def update_search_results(self, products: List[Dict[str, Any]]):
        """
        Actualiza los resultados de búsqueda.

        Args:
            products: Lista de productos encontrados
        """
        self.results_list.clear()

        if not products:
            self.no_results_label.show()
            self.results_title.setText("No se encontraron productos")
            return

        self.no_results_label.hide()
        self.results_title.setText(f"Encontrados {len(products)} producto(s)")

        for product in products:
            item = self._create_result_item(product)
            self.results_list.addItem(item)

    def _create_result_item(self, product: Dict[str, Any]) -> QListWidgetItem:
        """Crea un item de resultado"""
        nombre = product.get("nombre", "Sin nombre")
        codigo = product.get("codigo", "")
        categoria = product.get("categoria", "")
        stock = product.get("stock", 0)
        # Formato del texto
        text = f"{nombre}"
        if codigo:
            text += f" ({codigo})"
        if categoria:
            text += f" - {categoria}"
        text += f" | Stock: {stock}"

        item = QListWidgetItem(text)
        item.setData(Qt.ItemDataRole.UserRole, product)  # Guardar datos del producto

        # Colorear según stock
        if stock <= 0:
            item.setBackground(QColor(255, 235, 235))
        elif stock <= product.get("stock_minimo", 0):
            item.setBackground(QColor(255, 248, 220))

        return item

    def update_suggestions(self, suggestions: List[str]):
        """
        Actualiza las sugerencias de autocompletado.

        Args:
            suggestions: Lista de sugerencias
        """
        model = QStringListModel(suggestions)
        self.completer.setModel(model)

    def set_search_text(self, text: str):
        """Establece el texto de búsqueda"""
        self.search_input.setText(text)

    def get_search_text(self) -> str:
        """Obtiene el texto de búsqueda actual"""
        return self.search_input.text().strip()

    def get_active_filters(self) -> List[str]:
        """Obtiene los filtros activos"""
        active_filters = []
        for filter_key, btn in self.filter_buttons.items():
            if btn.isChecked():
                active_filters.append(filter_key)
        return active_filters
