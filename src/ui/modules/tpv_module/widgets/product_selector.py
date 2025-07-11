"""
Product Selector Widget - Selector profesional de productos para TPV
Versión: v0.0.14
"""

import logging
from typing import List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QScrollArea,
    QFrame,
    QSizePolicy,
    QSpacerItem,
    QApplication,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from services.tpv_service import Producto

logger = logging.getLogger(__name__)


class ProductCard(QFrame):
    """Tarjeta individual de producto con diseño moderno"""

    product_selected = pyqtSignal(Producto, int)

    def __init__(self, producto: Producto, parent=None):
        super().__init__(parent)
        self.producto = producto
        self.quantity = 1
        self.setup_ui()
        self.setup_styles()

    def setup_ui(self):
        """Configura la interfaz de la tarjeta de producto"""
        self.setFixedSize(180, 220)
        self.setFrameStyle(QFrame.Shape.Box)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Imagen del producto (placeholder)
        self.image_label = QLabel()
        self.image_label.setFixedSize(120, 80)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet(
            """
            QLabel {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                border-radius: 6px;
                color: #666;
                font-size: 11px;
            }
        """
        )
        self.image_label.setText("📦\nImagen")
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Nombre del producto
        self.name_label = QLabel(self.producto.nombre)
        self.name_label.setWordWrap(True)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.name_label.setFont(font)
        layout.addWidget(self.name_label)

        # Precio
        self.price_label = QLabel(f"€{self.producto.precio:.2f}")
        self.price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(12)
        font.setBold(True)
        self.price_label.setFont(font)
        self.price_label.setStyleSheet("color: #2e7d32;")
        layout.addWidget(self.price_label)

        # Stock disponible
        if hasattr(self.producto, "stock") and self.producto.stock is not None:
            stock_text = f"Stock: {self.producto.stock}"
            stock_color = "#d32f2f" if self.producto.stock < 5 else "#1976d2"
        else:
            stock_text = "Disponible"
            stock_color = "#1976d2"

        self.stock_label = QLabel(stock_text)
        self.stock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stock_label.setStyleSheet(f"color: {stock_color}; font-size: 9px;")
        layout.addWidget(self.stock_label)

        # Botón de añadir
        self.add_button = QPushButton("Añadir")
        self.add_button.setFixedHeight(32)
        self.add_button.clicked.connect(self.on_add_clicked)
        layout.addWidget(self.add_button)

    def setup_styles(self):
        """Configura los estilos de la tarjeta"""
        self.setStyleSheet(
            """
            ProductCard {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
            }
            ProductCard:hover {
                border-color: #2196f3;
                background-color: #f8f9fa;
            }
            QPushButton {
                background-color: #2196f3;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #1976d2;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """
        )

    def on_add_clicked(self):
        """Maneja el clic en el botón añadir"""
        self.product_selected.emit(self.producto, self.quantity)

        # Animación de feedback
        self.add_button.setText("✓ Añadido")
        QApplication.processEvents()

        # Restaurar texto después de un momento
        from PyQt6.QtCore import QTimer

        QTimer.singleShot(1000, lambda: self.add_button.setText("Añadir"))


class ProductSelectorWidget(QWidget):
    """Widget selector de productos profesional y moderno"""

    product_selected = pyqtSignal(Producto, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.productos: List[Producto] = []
        self.filtered_productos: List[Producto] = []
        self.product_cards: List[ProductCard] = []
        self.current_category = "Todos"
        self.search_text = ""

        self.setup_ui()
        self.load_sample_data()
        self.update_product_grid()

    def setup_ui(self):
        """Configura la interfaz principal"""
        import logging

        old_layout = self.layout()
        if old_layout is not None:
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            try:
                old_layout.deleteLater()
            except RuntimeError as e:
                logging.warning(f"No se pudo eliminar el layout anterior: {e}")
        layout = QVBoxLayout()
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        self.setLayout(layout)

        # Header con título
        header_layout = QHBoxLayout()

        title_label = QLabel("Selector de Productos")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        title_label.setStyleSheet("color: #1976d2; margin-bottom: 8px;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Filtros y búsqueda
        filters_layout = QHBoxLayout()

        # Búsqueda
        search_label = QLabel("Buscar:")
        search_label.setStyleSheet("font-weight: bold; color: #333;")
        filters_layout.addWidget(search_label)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar productos...")
        self.search_input.setFixedHeight(36)
        self.search_input.textChanged.connect(self.on_search_changed)
        self.search_input.setStyleSheet(
            """
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2196f3;
            }
        """
        )
        filters_layout.addWidget(self.search_input)

        filters_layout.addSpacing(20)

        # Filtro por categoría
        category_label = QLabel("Categoría:")
        category_label.setStyleSheet("font-weight: bold; color: #333;")
        filters_layout.addWidget(category_label)

        self.category_combo = QComboBox()
        self.category_combo.setFixedHeight(36)
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        self.category_combo.setStyleSheet(
            """
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                min-width: 150px;
            }
            QComboBox:focus {
                border-color: #2196f3;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border: 6px solid transparent;
                border-top: 6px solid #666;
                margin-right: 8px;
            }
        """
        )
        filters_layout.addWidget(self.category_combo)

        filters_layout.addStretch()
        layout.addLayout(filters_layout)

        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(separator)

        # Área de productos con scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: #fafafa;
                border-radius: 8px;
            }
        """
        )

        # Widget contenedor de productos
        self.products_widget = QWidget()
        self.products_layout = QGridLayout(self.products_widget)
        self.products_layout.setSpacing(16)
        self.products_layout.setContentsMargins(16, 16, 16, 16)

        self.scroll_area.setWidget(self.products_widget)
        layout.addWidget(self.scroll_area, 1)

        # Información de estado
        self.status_label = QLabel("Cargando productos...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet(
            "color: #666; font-style: italic; padding: 20px;"
        )
        layout.addWidget(self.status_label)

    def load_sample_data(self):
        """Carga datos de ejemplo para demostración"""
        sample_productos = [
            Producto(1, "Café Americano", 2.50, "Bebidas", 25),
            Producto(2, "Café con Leche", 3.00, "Bebidas", 30),
            Producto(3, "Cappuccino", 3.50, "Bebidas", 22),
            Producto(4, "Té Verde", 2.00, "Bebidas", 15),
            Producto(5, "Agua Mineral", 1.50, "Bebidas", 50),
            Producto(6, "Refresco Cola", 2.20, "Bebidas", 35),
            Producto(7, "Sandwich Mixto", 4.50, "Comida", 18),
            Producto(8, "Tostada con Jamón", 3.80, "Comida", 12),
            Producto(9, "Croissant", 2.80, "Comida", 8),
            Producto(10, "Ensalada César", 8.50, "Comida", 6),
            Producto(11, "Pasta Carbonara", 12.00, "Comida", 4),
            Producto(12, "Pizza Margarita", 10.50, "Comida", 3),
            Producto(13, "Tarta de Chocolate", 4.20, "Postres", 7),
            Producto(14, "Helado Vainilla", 3.50, "Postres", 10),
            Producto(15, "Flan Casero", 3.80, "Postres", 5),
            Producto(16, "Cerveza", 2.80, "Alcohol", 40),
            Producto(17, "Vino Tinto Copa", 4.50, "Alcohol", 25),
            Producto(18, "Gin Tonic", 8.00, "Alcohol", 15),
        ]

        self.productos = sample_productos

        # Actualizar combo de categorías
        categorias = ["Todos"] + list(set(p.categoria for p in self.productos))
        self.category_combo.clear()
        self.category_combo.addItems(categorias)

    def update_product_grid(self):
        """Actualiza la grilla de productos"""
        # Limpiar tarjetas existentes
        for card in self.product_cards:
            card.setParent(None)
            card.deleteLater()
        self.product_cards.clear()

        # Filtrar productos
        self.filtered_productos = self.filter_products()

        if not self.filtered_productos:
            self.status_label.setText(
                "No se encontraron productos con los filtros aplicados"
            )
            self.status_label.show()
            return

        self.status_label.hide()

        # Crear nuevas tarjetas
        columns = 4  # Número de columnas en la grilla
        for i, producto in enumerate(self.filtered_productos):
            card = ProductCard(producto)
            card.product_selected.connect(self.product_selected.emit)

            row = i // columns
            col = i % columns
            self.products_layout.addWidget(card, row, col)
            self.product_cards.append(card)

        # Añadir espaciador para mantener las tarjetas alineadas arriba
        spacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        final_row = (len(self.filtered_productos) - 1) // columns + 1
        self.products_layout.addItem(spacer, final_row, 0, 1, columns)

    def filter_products(self) -> List[Producto]:
        """Filtra productos según criterios actuales"""
        filtered = self.productos

        # Filtrar por categoría
        if self.current_category != "Todos":
            filtered = [p for p in filtered if p.categoria == self.current_category]

        # Filtrar por búsqueda
        if self.search_text:
            search_lower = self.search_text.lower()
            filtered = [p for p in filtered if search_lower in p.nombre.lower()]

        return filtered

    def on_search_changed(self, text: str):
        """Maneja cambios en el texto de búsqueda"""
        self.search_text = text.strip()
        self.update_product_grid()

    def on_category_changed(self, category: str):
        """Maneja cambios en la categoría seleccionada"""
        self.current_category = category
        self.update_product_grid()

    def set_productos(self, productos: List[Producto]):
        """Establece la lista de productos"""
        self.productos = productos

        # Actualizar combo de categorías
        categorias = ["Todos"] + list(set(p.categoria for p in productos))
        self.category_combo.clear()
        self.category_combo.addItems(categorias)

        self.update_product_grid()


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    # Crear y mostrar el widget
    widget = ProductSelectorWidget()
    widget.show()
    widget.resize(800, 600)

    sys.exit(app.exec())
