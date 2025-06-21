"""
Componentes especializados para el módulo de inventario
======================================================

Este módulo contiene widgets y componentes reutilizables
específicos para la gestión de inventario en hostelería.
"""

import logging
from typing import List, Dict, Any, Optional, Union
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QLabel,
    QFrame,
    QProgressBar,
    QComboBox,
    QLineEdit,
    QAbstractItemView,
    QMenu,
    QMessageBox,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont, QAction

from src.utils.modern_styles import ModernStyles

# Usar Any para tipado genérico y evitar conflictos
ProductoType = Any

logger = logging.getLogger(__name__)


class InventoryTableWidget(QTableWidget):
    """
    Tabla especializada para mostrar productos de inventario con funcionalidades avanzadas.

    Características:
    - Resaltado de productos con stock bajo
    - Menú contextual con acciones
    - Filtrado en tiempo real
    - Ordenamiento personalizado
    - Indicadores visuales de estado
    """

    # Señales personalizadas
    product_selected = pyqtSignal(object)  # ProductoType seleccionado
    product_edit_requested = pyqtSignal(object)  # Solicitud de edición
    product_delete_requested = pyqtSignal(object)  # Solicitud de eliminación
    stock_update_requested = pyqtSignal(object, int)  # Actualización de stock

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modern_styles = ModernStyles()
        self.products_data: List[Any] = []
        self._setup_table()
        self._setup_context_menu()
        self._apply_styles()

    def _setup_table(self):
        """Configura la tabla con las columnas necesarias"""
        # Configurar columnas
        columns = [
            "ID",
            "Código",
            "Nombre",
            "Categoría",
            "Stock",
            "Mín",
            "Precio",
            "Proveedor",
            "Estado",
            "Acciones",
        ]
        self.setColumnCount(len(columns))
        self.setHorizontalHeaderLabels(columns)

        # Configurar header
        header = self.horizontalHeader()
        if header:
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Nombre
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)  # Categoría

        # Anchos de columna
        self.setColumnWidth(0, 50)  # ID
        self.setColumnWidth(1, 80)  # Código
        self.setColumnWidth(4, 70)  # Stock
        self.setColumnWidth(5, 50)  # Mín
        self.setColumnWidth(6, 80)  # Precio
        self.setColumnWidth(8, 80)  # Estado
        self.setColumnWidth(9, 120)  # Acciones

        # Configuraciones de comportamiento
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)

        # Conectar señales
        self.itemSelectionChanged.connect(self._on_selection_changed)
        self.itemDoubleClicked.connect(self._on_item_double_clicked)

    def _setup_context_menu(self):
        """Configura el menú contextual"""
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)

    def _apply_styles(self):
        """Aplica estilos modernos a la tabla"""
        colors = self.modern_styles.COLORS
        styles = f"""
        QTableWidget {{
            gridline-color: {colors['border']};
            background-color: {colors['surface']};
            alternate-background-color: {colors['surface_variant']};
            selection-background-color: {colors['primary']};
            selection-color: white;
            border: 1px solid {colors['border']};
            border-radius: 8px;
        }}
        
        QHeaderView::section {{
            background-color: {colors['surface_variant']};
            color: {colors['text_primary']};
            padding: 8px;
            border: 1px solid {colors['border']};
            font-weight: bold;
        }}
        
        QHeaderView::section:hover {{
            background-color: {colors['surface_hover']};
        }}
        
        QTableWidget::item {{
            padding: 4px;
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: {colors['primary']};
            color: white;
        }}        """
        self.setStyleSheet(styles)

    def load_products(self, products: List[Any]):
        """
        Carga los productos en la tabla.

        Args:
            products: Lista de productos a mostrar
        """
        self.products_data = products
        self.setRowCount(len(products))

        for row, product in enumerate(products):
            self._populate_row(row, product)

    def _populate_row(self, row: int, product: ProductoType):
        """
        Llena una fila de la tabla con los datos del ProductoType.

        Args:
            row: Número de fila
            product: ProductoType a mostrar
        """
        # ID
        id_item = QTableWidgetItem(str(getattr(product, "id", "")))
        id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 0, id_item)

        # Código
        codigo_item = QTableWidgetItem(getattr(product, "codigo", ""))
        self.setItem(row, 1, codigo_item)

        # Nombre
        nombre_item = QTableWidgetItem(getattr(product, "nombre", ""))
        self.setItem(row, 2, nombre_item)

        # Categoría
        categoria_item = QTableWidgetItem(getattr(product, "categoria", ""))
        self.setItem(row, 3, categoria_item)

        # Stock (con indicador visual)
        stock_actual = getattr(product, "stock_actual", 0)
        stock_minimo = getattr(product, "stock_minimo", 0)
        stock_item = QTableWidgetItem(str(stock_actual))
        stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        # Colorear según nivel de stock
        if stock_actual <= 0:
            stock_item.setBackground(QColor(255, 235, 235))  # Rojo muy claro
            stock_item.setForeground(QColor(200, 0, 0))  # Rojo oscuro
        elif stock_actual <= stock_minimo:
            stock_item.setBackground(QColor(255, 248, 220))  # Amarillo claro
            stock_item.setForeground(QColor(180, 100, 0))  # Naranja oscuro

        self.setItem(row, 4, stock_item)

        # Stock mínimo
        min_item = QTableWidgetItem(str(stock_minimo))
        min_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setItem(row, 5, min_item)

        # Precio
        precio = getattr(product, "precio", 0.0)
        precio_item = QTableWidgetItem(f"{precio:.2f} €")
        precio_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        self.setItem(row, 6, precio_item)

        # Proveedor
        proveedor = getattr(product, "proveedor_nombre", None) or getattr(
            product, "proveedor", "Sin proveedor"
        )
        proveedor_item = QTableWidgetItem(str(proveedor))
        self.setItem(row, 7, proveedor_item)

        # Estado
        estado_widget = self._create_status_widget(product)
        self.setCellWidget(row, 8, estado_widget)

        # Acciones
        actions_widget = self._create_actions_widget(product)
        self.setCellWidget(row, 9, actions_widget)

    def _create_status_widget(self, product: ProductoType) -> QWidget:
        """
        Crea un widget de estado para mostrar el nivel de stock.

        Args:
            product: ProductoType para determinar el estado

        Returns:
            Widget con indicador de estado
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)

        stock_actual = getattr(product, "stock_actual", 0)
        stock_minimo = getattr(product, "stock_minimo", 0)

        # Determinar estado y color
        if stock_actual <= 0:
            status_text = "Agotado"
            color = "#dc3545"  # Rojo
        elif stock_actual <= stock_minimo:
            status_text = "Bajo"
            color = "#ffc107"  # Amarillo
        elif stock_actual <= stock_minimo * 2:
            status_text = "Medio"
            color = "#fd7e14"  # Naranja
        else:
            status_text = "Bueno"
            color = "#28a745"  # Verde

        # Crear etiqueta de estado
        status_label = QLabel(status_text)
        status_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: {color};
                color: white;
                padding: 2px 8px;
                border-radius: 10px;
                font-size: 11px;
                font-weight: bold;
            }}
        """
        )
        status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(status_label)
        return widget

    def _create_actions_widget(self, product: ProductoType) -> QWidget:
        """
        Crea un widget con botones de acción para cada ProductoType.

        Args:
            product: ProductoType para las acciones

        Returns:
            Widget con botones de acción
        """
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        # Botón editar
        edit_btn = QPushButton("✏️")
        edit_btn.setToolTip("Editar ProductoType")
        edit_btn.setFixedSize(24, 24)
        edit_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """
        )
        edit_btn.clicked.connect(lambda: self.product_edit_requested.emit(product))

        # Botón eliminar
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("Eliminar ProductoType")
        delete_btn.setFixedSize(24, 24)
        delete_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #c82333;
            }
        """
        )
        delete_btn.clicked.connect(lambda: self.product_delete_requested.emit(product))

        # Botón stock
        stock_btn = QPushButton("📦")
        stock_btn.setToolTip("Ajustar stock")
        stock_btn.setFixedSize(24, 24)
        stock_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """
        )
        stock_btn.clicked.connect(lambda: self._show_stock_dialog(product))

        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        layout.addWidget(stock_btn)

        return widget

    def _show_stock_dialog(self, product: ProductoType):
        """
        Muestra un diálogo para ajustar el stock del ProductoType.

        Args:
            product: ProductoType a ajustar
        """
        from PyQt6.QtWidgets import QInputDialog

        stock_actual = getattr(product, "stock_actual", 0)
        nombre = getattr(product, "nombre", "ProductoType")

        new_stock, ok = QInputDialog.getInt(
            self, "Ajustar Stock", f"Nuevo stock para {nombre}:", stock_actual, 0, 99999
        )

        if ok:
            self.stock_update_requested.emit(product, new_stock)

    def _on_selection_changed(self):
        """Maneja el cambio de selección en la tabla"""
        current_row = self.currentRow()
        if 0 <= current_row < len(self.products_data):
            product = self.products_data[current_row]
            self.product_selected.emit(product)

    def _on_item_double_clicked(self, item):
        """Maneja el doble clic en un item"""
        if item is None:
            return
        row = item.row()
        if 0 <= row < len(self.products_data):
            product = self.products_data[row]
            self.product_edit_requested.emit(product)

    def _show_context_menu(self, position):
        """
        Muestra el menú contextual.

        Args:
            position: Posición del clic
        """
        item = self.itemAt(position)
        if not item:
            return

        row = item.row()
        if not (0 <= row < len(self.products_data)):
            return

        product = self.products_data[row]

        # Crear menú contextual
        menu = QMenu(self)

        # Acciones
        edit_action = QAction("Editar ProductoType", self)
        edit_action.triggered.connect(lambda: self.product_edit_requested.emit(product))

        delete_action = QAction("Eliminar ProductoType", self)
        delete_action.triggered.connect(
            lambda: self.product_delete_requested.emit(product)
        )

        stock_action = QAction("Ajustar stock", self)
        stock_action.triggered.connect(lambda: self._show_stock_dialog(product))

        # Añadir acciones al menú
        menu.addAction(edit_action)
        menu.addAction(stock_action)
        menu.addSeparator()
        menu.addAction(delete_action)

        # Mostrar menú
        menu.exec(self.mapToGlobal(position))

    def _match_search_text(self, product, search_text: str) -> bool:
        if not search_text:
            return True
        nombre = getattr(product, "nombre", "")
        return search_text.lower() in nombre.lower()

    def _match_category(self, product, category: str) -> bool:
        if not category or category == "Todas":
            return True
        categoria = getattr(product, "categoria", "")
        return categoria == category

    def filter_products(self, search_text: str = "", category: str = ""):
        """
        Filtra los productos mostrados en la tabla.

        Args:
            search_text: Texto a buscar
            category: Categoría a filtrar
        """
        for row in range(self.rowCount()):
            show_row = True
            if row < len(self.products_data):
                product = self.products_data[row]
                show_row = self._match_search_text(
                    product, search_text
                ) and self._match_category(product, category)
            self.setRowHidden(row, not show_row)

    def get_selected_product(self) -> Optional[ProductoType]:
        """
        Obtiene el ProductoType actualmente seleccionado.

        Returns:
            ProductoType seleccionado o None
        """
        current_row = self.currentRow()
        if 0 <= current_row < len(self.products_data):
            return self.products_data[current_row]
        return None

    def refresh_product(self, updated_product: ProductoType):
        """
        Actualiza un ProductoType específico en la tabla.

        Args:
            updated_product: ProductoType actualizado
        """
        product_id = getattr(updated_product, "id", None)
        if product_id is None:
            return

        for row, product in enumerate(self.products_data):
            if getattr(product, "id", None) == product_id:
                self.products_data[row] = updated_product
                self._populate_row(row, updated_product)
                break


class StockAlertWidget(QWidget):
    """
    Widget para mostrar alertas de stock de forma visual y compacta.

    Características:
    - Indicadores de nivel de stock
    - Colores según criticidad
    - Botones de acción rápida
    - Actualización automática
    """

    # Señales
    order_requested = pyqtSignal(object)  # Solicitud de pedido

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modern_styles = ModernStyles()
        self.alert_products: List[ProductoType] = []
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Configura la interfaz del widget de alertas"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(8)
        main_layout.setContentsMargins(12, 12, 12, 12)

        # Header
        header_layout = QHBoxLayout()

        title_label = QLabel("🚨 Alertas de Stock")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #dc3545;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        # Contador de alertas
        self.count_label = QLabel("0 alertas")
        self.count_label.setStyleSheet("font-size: 12px; color: #6c757d;")
        header_layout.addWidget(self.count_label)

        main_layout.addLayout(header_layout)

        # Contenedor de alertas
        self.alerts_container = QWidget()
        self.alerts_layout = QVBoxLayout(self.alerts_container)
        self.alerts_layout.setSpacing(4)

        main_layout.addWidget(self.alerts_container)
        main_layout.addStretch()

    def _apply_styles(self):
        """Aplica estilos al widget"""
        colors = self.modern_styles.COLORS
        self.setStyleSheet(
            f"""
            StockAlertWidget {{
                background-color: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
            }}
        """
        )

    def load_alerts(self, products: List[ProductoType]):
        """
        Carga las alertas de stock.

        Args:
            products: Lista de productos con stock bajo
        """
        self.alert_products = products
        self._update_display()

    def _update_display(self):
        """Actualiza la visualización de alertas"""
        # Limpiar alertas existentes
        self._clear_alerts()
        # Actualizar contador
        count = len(self.alert_products)
        self.count_label.setText(f"{count} alerta{'s' if count != 1 else ''}")

        # Mostrar alertas
        for product in self.alert_products:
            alert_widget = self._create_alert_item(product)
            self.alerts_layout.addWidget(alert_widget)

    def _clear_alerts(self):
        """Limpia todas las alertas mostradas"""
        while self.alerts_layout.count():
            child = self.alerts_layout.takeAt(0)
            if child and child.widget():
                widget = child.widget()
                if widget:
                    widget.deleteLater()

    def _create_alert_item(self, product: ProductoType) -> QWidget:
        """
        Crea un widget para mostrar una alerta individual.

        Args:
            product: ProductoType con stock bajo

        Returns:
            Widget de la alerta
        """
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.Box)
        widget.setStyleSheet(
            """
            QFrame {
                background-color: #fff3cd;
                border: 1px solid #ffeeba;
                border-radius: 4px;
                padding: 4px;
            }
        """
        )

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)

        # Información del ProductoType
        info_layout = QVBoxLayout()

        nombre = getattr(product, "nombre", "ProductoType desconocido")
        name_label = QLabel(nombre)
        name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        info_layout.addWidget(name_label)

        stock_actual = getattr(product, "stock_actual", 0)
        stock_minimo = getattr(product, "stock_minimo", 0)
        stock_label = QLabel(f"Stock: {stock_actual} / {stock_minimo}")
        stock_label.setStyleSheet("font-size: 11px; color: #856404;")
        info_layout.addWidget(stock_label)

        layout.addLayout(info_layout)
        layout.addStretch()

        # Botón de pedido
        order_btn = QPushButton("Pedir")
        order_btn.setFixedSize(50, 24)
        order_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #ffc107;
                color: #212529;
                border: none;
                border-radius: 3px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """
        )
        order_btn.clicked.connect(lambda: self.order_requested.emit(product))
        layout.addWidget(order_btn)

        return widget


class InventoryStatsWidget(QWidget):
    """
    Widget para mostrar estadísticas del inventario de forma visual.

    Características:
    - Gráficos de barras simples
    - Métricas clave
    - Indicadores de tendencia
    - Actualización automática
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modern_styles = ModernStyles()
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Configura la interfaz de estadísticas"""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # Título
        title_label = QLabel("📊 Estadísticas de Inventario")
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title_label)

        # Métricas principales
        metrics_layout = QHBoxLayout()

        # Total productos
        total_widget = self._create_metric_widget("Total productos", "0", "#007bff")
        metrics_layout.addWidget(total_widget)

        # Valor inventario
        value_widget = self._create_metric_widget("Valor Total", "0.00 €", "#28a745")
        metrics_layout.addWidget(value_widget)

        # productos críticos
        critical_widget = self._create_metric_widget("Stock Crítico", "0", "#dc3545")
        metrics_layout.addWidget(critical_widget)

        layout.addLayout(metrics_layout)

        # Gráfico de categorías (simplificado)
        categories_label = QLabel("Stock por Categoría")
        categories_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(categories_label)

        # Contenedor de barras de progreso
        self.progress_container = QWidget()
        self.progress_layout = QVBoxLayout(self.progress_container)
        layout.addWidget(self.progress_container)

        layout.addStretch()

        # Guardar referencias para actualizar
        self.total_label = total_widget.findChild(QLabel, "value_label")
        self.value_label = value_widget.findChild(QLabel, "value_label")
        self.critical_label = critical_widget.findChild(QLabel, "value_label")

    def _create_metric_widget(self, title: str, value: str, color: str) -> QWidget:
        """
        Crea un widget de métrica.

        Args:
            title: Título de la métrica
            value: Valor de la métrica
            color: Color del widget

        Returns:
            Widget de métrica
        """
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.Box)
        widget.setStyleSheet(
            f"""
            QFrame {{
                background-color: {color};
                color: white;
                border-radius: 8px;
                padding: 8px;
            }}
        """
        )

        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value_label = QLabel(value)
        value_label.setObjectName("value_label")
        value_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 12px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(value_label)
        layout.addWidget(title_label)

        return widget

    def _apply_styles(self):
        """Aplica estilos al widget"""
        colors = self.modern_styles.COLORS
        self.setStyleSheet(
            f"""
            InventoryStatsWidget {{
                background-color: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 12px;
            }}
        """
        )

    def update_stats(self, stats: Dict[str, Any]):
        """
        Actualiza las estadísticas mostradas.

        Args:
            stats: Diccionario con las estadísticas
        """
        # Actualizar métricas principales
        if self.total_label:
            self.total_label.setText(str(stats.get("total_products", 0)))

        if self.value_label:
            self.value_label.setText(f"{stats.get('total_value', 0):.2f} €")

        if self.critical_label:
            self.critical_label.setText(str(stats.get("critical_products", 0)))
        # Actualizar gráfico de categorías
        self._update_category_chart(stats.get("categories", {}))

    def _update_category_chart(self, categories: Dict[str, int]):
        """
        Actualiza el gráfico de categorías.

        Args:
            categories: Diccionario con categorías y cantidades
        """
        # Limpiar barras existentes
        while self.progress_layout.count():
            child = self.progress_layout.takeAt(0)
            if child and child.widget():
                widget = child.widget()
                if widget:
                    widget.deleteLater()

        # Crear nuevas barras
        max_value = max(categories.values()) if categories else 1

        for category, count in categories.items():
            bar_widget = QWidget()
            bar_layout = QHBoxLayout(bar_widget)
            bar_layout.setContentsMargins(0, 2, 0, 2)

            # Etiqueta de categoría
            category_label = QLabel(category)
            category_label.setFixedWidth(120)
            category_label.setStyleSheet("font-size: 11px;")
            bar_layout.addWidget(category_label)

            # Barra de progreso
            progress_bar = QProgressBar()
            progress_bar.setMaximum(max_value)
            progress_bar.setValue(count)
            progress_bar.setTextVisible(True)
            progress_bar.setFormat(f"{count} productos")
            progress_bar.setStyleSheet(
                """
                QProgressBar {
                    border: 1px solid #ccc;
                    border-radius: 3px;
                    text-align: center;
                    font-size: 10px;
                }
                QProgressBar::chunk {
                    background-color: #007bff;
                    border-radius: 2px;
                }
            """
            )
            bar_layout.addWidget(progress_bar)

            self.progress_layout.addWidget(bar_widget)
