"""
TPV Avanzado - Panel de pedido modularizado
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QLabel, QPushButton, QFrame, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def create_pedido_panel(parent, splitter):
    """Crea el panel de pedido actual y pago"""
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(10, 10, 10, 10)
    layout.setSpacing(10)
    
    # Header del pedido
    header_frame = QFrame()
    header_frame.setStyleSheet("""
        QFrame {
            background: #f8f9fa;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 10px;
        }
    """)
    header_layout = QHBoxLayout(header_frame)
    
    pedido_title = QLabel("📋 Pedido Actual")
    pedido_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    pedido_title.setStyleSheet("color: #374151;")
    header_layout.addWidget(pedido_title)
    
    header_layout.addStretch()
    
    clear_btn = QPushButton("🗑️ Limpiar")
    clear_btn.setStyleSheet("""
        QPushButton {
            background: #ef4444;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #dc2626;
        }
    """)
    clear_btn.clicked.connect(lambda: limpiar_pedido(parent))
    header_layout.addWidget(clear_btn)
    
    layout.addWidget(header_frame)
    
    # Tabla de productos del pedido
    parent.pedido_table = QTableWidget()
    parent.pedido_table.setColumnCount(4)
    parent.pedido_table.setHorizontalHeaderLabels(["Producto", "Precio", "Cant.", "Total"])
    
    # Configurar tabla
    header = parent.pedido_table.horizontalHeader()
    if header:
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
    
    parent.pedido_table.setStyleSheet("""
        QTableWidget {
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            background: white;
            gridline-color: #f3f4f6;
        }
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #f3f4f6;
        }
        QTableWidget::item:selected {
            background: #eff6ff;
            color: #1d4ed8;
        }
        QHeaderView::section {
            background: #f9fafb;
            padding: 10px;
            border: none;
            border-bottom: 2px solid #e5e7eb;
            font-weight: bold;
            color: #374151;
        }
    """)
    
    layout.addWidget(parent.pedido_table)
    
    # Panel de totales
    totales_frame = create_totales_panel(parent)
    layout.addWidget(totales_frame)
    
    # Botones de acción
    actions_frame = create_actions_panel(parent)
    layout.addWidget(actions_frame)
    
    # Inicializar método para agregar productos
    parent.agregar_producto_pedido = lambda nombre, precio: agregar_producto_a_pedido(parent, nombre, precio)
    
    splitter.addWidget(widget)


def create_totales_panel(parent):
    """Crea el panel de totales"""
    frame = QFrame()
    frame.setStyleSheet("""
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #f0f9ff, stop:1 #e0f2fe);
            border: 2px solid #0ea5e9;
            border-radius: 10px;
            padding: 15px;
        }
    """)
    
    layout = QVBoxLayout(frame)
    
    # Labels de totales
    parent.subtotal_label = QLabel("Subtotal: €0.00")
    parent.subtotal_label.setFont(QFont("Segoe UI", 12))
    parent.subtotal_label.setStyleSheet("color: #374151;")
    layout.addWidget(parent.subtotal_label)
    
    parent.iva_label = QLabel("IVA (21%): €0.00")
    parent.iva_label.setFont(QFont("Segoe UI", 12))
    parent.iva_label.setStyleSheet("color: #374151;")
    layout.addWidget(parent.iva_label)
    
    parent.total_label = QLabel("TOTAL: €0.00")
    parent.total_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
    parent.total_label.setStyleSheet("color: #059669; margin-top: 5px;")
    layout.addWidget(parent.total_label)
    
    return frame


def create_actions_panel(parent):
    """Crea el panel de botones de acción"""
    frame = QFrame()
    layout = QVBoxLayout(frame)
    layout.setSpacing(10)
    
    # Botón de procesar pago
    pago_btn = QPushButton("💳 Procesar Pago")
    pago_btn.setFixedHeight(50)
    pago_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
    pago_btn.setStyleSheet("""
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #34d399, stop:1 #10b981);
            color: white;
            border: none;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(16, 185, 129, 0.3);
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #10b981, stop:1 #059669);
            transform: translateY(-1px);
        }
        QPushButton:pressed {
            background: #047857;
        }
    """)
    pago_btn.clicked.connect(lambda: procesar_pago(parent))
    layout.addWidget(pago_btn)
    
    # Fila de botones secundarios
    secondary_layout = QHBoxLayout()
    
    descuento_btn = QPushButton("🏷️ Descuento")
    descuento_btn.setStyleSheet("""
        QPushButton {
            background: #f59e0b;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #d97706;
        }
    """)
    secondary_layout.addWidget(descuento_btn)
    
    nota_btn = QPushButton("📝 Nota")
    nota_btn.setStyleSheet("""
        QPushButton {
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 12px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #4f46e5;
        }
    """)
    secondary_layout.addWidget(nota_btn)
    
    layout.addLayout(secondary_layout)
    
    return frame


def agregar_producto_a_pedido(parent, nombre, precio):
    """Agrega un producto al pedido actual"""
    table = parent.pedido_table
    
    # Buscar si el producto ya existe
    for row in range(table.rowCount()):
        if table.item(row, 0) and table.item(row, 0).text() == nombre:
            # Incrementar cantidad
            cantidad_item = table.item(row, 2)
            cantidad_actual = int(cantidad_item.text())
            nueva_cantidad = cantidad_actual + 1
            cantidad_item.setText(str(nueva_cantidad))
            
            # Actualizar total de la línea
            total_linea = precio * nueva_cantidad
            table.setItem(row, 3, QTableWidgetItem(f"€{total_linea:.2f}"))
            
            actualizar_totales(parent)
            return
    
    # Si no existe, agregar nueva fila
    row = table.rowCount()
    table.insertRow(row)
    
    table.setItem(row, 0, QTableWidgetItem(nombre))
    table.setItem(row, 1, QTableWidgetItem(f"€{precio:.2f}"))
    table.setItem(row, 2, QTableWidgetItem("1"))
    table.setItem(row, 3, QTableWidgetItem(f"€{precio:.2f}"))
    
    actualizar_totales(parent)


def actualizar_totales(parent):
    """Actualiza los totales del pedido"""
    table = parent.pedido_table
    subtotal = 0.0
    
    for row in range(table.rowCount()):
        total_item = table.item(row, 3)
        if total_item:
            total_text = total_item.text().replace('€', '')
            subtotal += float(total_text)
    
    iva = subtotal * 0.21
    total = subtotal + iva
    
    parent.subtotal_label.setText(f"Subtotal: €{subtotal:.2f}")
    parent.iva_label.setText(f"IVA (21%): €{iva:.2f}")
    parent.total_label.setText(f"TOTAL: €{total:.2f}")


def limpiar_pedido(parent):
    """Limpia el pedido actual"""
    parent.pedido_table.setRowCount(0)
    actualizar_totales(parent)


def procesar_pago(parent):
    """Procesa el pago del pedido"""
    table = parent.pedido_table
    if table.rowCount() == 0:
        return
    
    total_text = parent.total_label.text().replace('TOTAL: €', '')
    total = float(total_text)
    
    if hasattr(parent, 'procesar_pago'):
        parent.procesar_pago()
    
    # Limpiar pedido después del pago
    limpiar_pedido(parent)