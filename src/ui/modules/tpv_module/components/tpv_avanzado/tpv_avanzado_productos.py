"""
TPV Avanzado - Panel de productos modularizado
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                            QTabWidget, QGridLayout, QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def create_productos_panel(parent, splitter):
    """Crea el panel de productos y categorías"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)
    
    # Barra de búsqueda
    search_frame = QFrame()
    search_frame.setStyleSheet("""
        QFrame {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 5px;
        }
    """)
    search_layout = QHBoxLayout(search_frame)
    
    search_input = QLineEdit()
    search_input.setPlaceholderText("🔍 Buscar productos...")
    search_input.setStyleSheet("""
        QLineEdit {
            border: none;
            padding: 8px;
            font-size: 14px;
            background: transparent;
        }
    """)
    search_layout.addWidget(search_input)
    layout.addWidget(search_frame)
    
    # Pestañas de categorías
    tabs = QTabWidget()
    tabs.setStyleSheet("""
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
    """)
    
    # Crear pestañas de categorías
    categorias = ["Bebidas", "Entrantes", "Principales", "Postres"]
    for categoria in categorias:
        tab = create_categoria_tab(parent, categoria)
        tabs.addTab(tab, categoria)
    
    layout.addWidget(tabs)
    splitter.addWidget(widget)


def create_categoria_tab(parent, categoria):
    """Crea una pestaña para una categoría específica"""
    tab = QWidget()
    layout = QVBoxLayout(tab)
    layout.setContentsMargins(15, 15, 15, 15)
    
    # Grid de productos
    grid_layout = QGridLayout()
    grid_layout.setSpacing(10)
    
    # Obtener productos de la categoría
    if parent.tpv_service:
        productos = parent.tpv_service.get_productos_por_categoria(categoria)
    else:
        productos = []
    
    # Si no hay productos, mostrar algunos de ejemplo
    if not productos:
        productos_ejemplo = {
            "Bebidas": [("Coca Cola", 2.50), ("Agua", 1.50), ("Cerveza", 2.80), ("Café", 1.30)],
            "Entrantes": [("Patatas Bravas", 5.50), ("Croquetas", 7.00), ("Nachos", 6.50)],
            "Principales": [("Paella", 12.00), ("Entrecot", 18.50), ("Pasta", 9.50)],
            "Postres": [("Tarta", 4.50), ("Helado", 3.80), ("Flan", 3.20)]
        }
        productos_data = productos_ejemplo.get(categoria, [])
    else:
        productos_data = [(p.nombre, p.precio) for p in productos]
    
    # Crear botones de productos
    row, col = 0, 0
    for nombre, precio in productos_data:
        btn = create_producto_button(parent, nombre, precio)
        grid_layout.addWidget(btn, row, col)
        
        col += 1
        if col >= 3:  # 3 columnas
            col = 0
            row += 1
    
    layout.addLayout(grid_layout)
    layout.addStretch()
    
    return tab


def create_producto_button(parent, nombre, precio):
    """Crea un botón para un producto"""
    btn = QPushButton()
    btn.setFixedSize(120, 80)
    
    # Layout interno del botón
    btn_layout = QVBoxLayout()
    
    nombre_label = QLabel(nombre)
    nombre_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
    nombre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    nombre_label.setWordWrap(True)
    
    precio_label = QLabel(f"€{precio:.2f}")
    precio_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
    precio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    precio_label.setStyleSheet("color: #059669;")
    
    btn.setStyleSheet("""
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff, stop:1 #f8f9fa);
            border: 2px solid #e5e7eb;
            border-radius: 10px;
            text-align: center;
        }
        QPushButton:hover {
            border-color: #3b82f6;
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #eff6ff, stop:1 #dbeafe);
        }
        QPushButton:pressed {
            background: #bfdbfe;
        }
    """)
    
    # Conectar click del botón
    btn.clicked.connect(lambda: agregar_producto(parent, nombre, precio))
    
    # Texto del botón
    btn.setText(f"{nombre}\n€{precio:.2f}")
    
    return btn


def agregar_producto(parent, nombre, precio):
    """Agrega un producto al pedido actual"""
    if hasattr(parent, 'agregar_producto_pedido'):
        parent.agregar_producto_pedido(nombre, precio)