"""
TPV Avanzado - Panel de productos modularizado
"""

from typing import Any, Optional, Dict, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QTabWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def create_productos_panel(parent: Any, splitter: Any) -> None:
    """Crea el panel de productos y categorías"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)

    # Barra de búsqueda
    search_frame = QFrame()
    search_frame.setStyleSheet(
        """
        QFrame {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 5px;
        }
    """
    )
    search_layout = QHBoxLayout(search_frame)

    search_input = QLineEdit()
    search_input.setPlaceholderText("🔍 Buscar productos...")
    search_input.setStyleSheet(
        """
        QLineEdit {
            border: none;
            padding: 8px;
            font-size: 14px;
            background: transparent;
        }
    """
    )
    search_layout.addWidget(search_input)
    layout.addWidget(search_frame)

    # Pestañas de categorías
    tabs = QTabWidget()
    tabs.setStyleSheet(
        """
        QTabWidget::pane {
            border: 1px solid #e5e7eb;
            background: white;
            border-radius: 8px;
        }
        QTabBar::tab {
            padding: 10px 15px;
            margin-right: 2px;
            background: #f9fafb;
            border: 1px solid #e5e7eb;
            border-bottom: none;
            border-radius: 6px 6px 0 0;
        }
        QTabBar::tab:selected {
            background: white;
            border-bottom: 1px solid white;
        }
    """
    )

    # Crear pestañas de categorías
    categorias = ["Bebidas", "Entrantes", "Principales", "Postres"]
    for categoria in categorias:
        tab = create_categoria_tab(parent, categoria)
        tabs.addTab(tab, categoria)

    layout.addWidget(tabs)
    splitter.addWidget(widget)  # type: ignore


def create_categoria_tab(parent: Any, categoria: str) -> QWidget:
    """Crea una pestaña para una categoría específica"""
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.setContentsMargins(15, 15, 15, 15)

    # Grid de productos
    grid_layout = QGridLayout()
    grid_layout.setSpacing(10)

    # Obtener productos de la categoría (con stock)
    productos_data: List[Dict[str, Any]] = []
    if parent.tpv_service:  # type: ignore
        productos = parent.tpv_service.get_productos_por_categoria(categoria)  # type: ignore
        for p in productos:  # type: ignore
            productos_data.append(  # type: ignore
                {
                    "nombre": p.nombre,  # type: ignore
                    "precio": p.precio,  # type: ignore
                    "stock": getattr(p, "stock", None),  # type: ignore
                }
            )
    # Eliminar productos de ejemplo: si no hay productos reales, no mostrar nada

    # Crear botones de productos con stock
    row, col = 0, 0
    for prod in productos_data:  # type: ignore
        btn = create_producto_button(
            parent, prod["nombre"], prod["precio"], prod.get("stock")  # type: ignore
        )
        grid_layout.addWidget(btn, row, col)
        col += 1
        if col >= 3:
            col = 0
            row += 1

    layout.addLayout(grid_layout)
    layout.addStretch()

    return tab


def create_producto_button(
    parent: Any, nombre: str, precio: float, stock: Optional[Any] = None
) -> QPushButton:
    """Crea un botón para un producto, mostrando stock y bloqueando si no hay stock"""
    btn = QPushButton()
    btn.setFixedSize(120, 80)

    # Layout interno del botón
    btn_layout: QVBoxLayout = QVBoxLayout()

    nombre_label = QLabel(nombre)
    nombre_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
    nombre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    nombre_label.setWordWrap(True)

    precio_label = QLabel(f"€{precio:.2f}")
    precio_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
    precio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    precio_label.setStyleSheet("color: #059669;")

    # Mostrar stock
    stock_text: str = ""
    if stock is not None:
        if stock <= 0:
            stock_text = "Sin stock"
        else:
            stock_text = f"Stock: {stock}"
    stock_label = QLabel(stock_text)
    stock_label.setFont(QFont("Segoe UI", 9))
    stock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    if stock is not None and stock <= 0:
        stock_label.setStyleSheet("color: #dc2626;")
    else:
        stock_label.setStyleSheet("color: #64748b;")

    # Layout visual
    btn_layout.addWidget(nombre_label)
    btn_layout.addWidget(precio_label)
    btn_layout.addWidget(stock_label)
    btn.setLayout(btn_layout)

    # Deshabilitar si no hay stock
    if stock is not None and stock <= 0:
        btn.setEnabled(False)
        btn.setToolTip("Sin stock disponible")
    else:
        btn.clicked.connect(lambda: agregar_producto(parent, nombre, precio))  # type: ignore

    return btn


def agregar_producto(parent: Any, nombre: str, precio: float) -> None:
    """Agrega un producto al pedido actual"""
    if hasattr(parent, "agregar_producto_pedido"):  # type: ignore
        parent.agregar_producto_pedido(nombre, precio)  # type: ignore
