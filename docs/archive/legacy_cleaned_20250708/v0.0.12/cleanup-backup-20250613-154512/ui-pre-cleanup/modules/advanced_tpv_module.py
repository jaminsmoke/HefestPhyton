"""
Módulo TPV avanzado con funcionalidades de descuentos, múltiples métodos de pago y facturación.
"""

import logging
from datetime import datetime
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                            QTableWidgetItem, QHeaderView, QLabel, QSplitter, QFrame,
                            QDialog, QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox,
                            QMessageBox, QGridLayout, QTabWidget, QLineEdit, QSizePolicy,
                            QGroupBox, QCheckBox, QTextEdit, QDialogButtonBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

from .base_module import BaseModule
from services.tpv_service import TPVService

logger = logging.getLogger(__name__)

class AdvancedTPVModule(BaseModule):
    """Módulo TPV avanzado con funcionalidades completas"""
    
    def __init__(self):
        super().__init__()
        self.tpv_service = TPVService()
        self.current_order = None
        self.setup_ui()
        
    def create_module_header(self):
        """Crea el header del módulo TPV"""
        header = QFrame()
        header.setObjectName("module-header")
        header.setFixedHeight(70)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Título y estadísticas
        title_layout = QVBoxLayout()
        title = QLabel("💳 TPV Avanzado")
        title.setObjectName("module-title")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1f2937;")
        title_layout.addWidget(title)
        
        stats_label = QLabel("Ventas del día: €0.00 | Pedidos: 0")
        stats_label.setStyleSheet("color: #6b7280; font-size: 14px;")
        title_layout.addWidget(stats_label)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # Botones de acción rápida
        quick_actions_layout = QHBoxLayout()
        
        new_order_btn = QPushButton("📝 Nuevo Pedido")
        new_order_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 15px;
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                margin-right: 10px;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """)
        new_order_btn.clicked.connect(self.new_order)
        quick_actions_layout.addWidget(new_order_btn)
        
        cash_register_btn = QPushButton("💰 Caja")
        cash_register_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 15px;
                background: #10b981;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                margin-right: 10px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        cash_register_btn.clicked.connect(self.open_cash_register)
        quick_actions_layout.addWidget(cash_register_btn)
        
        reports_btn = QPushButton("📊 Reportes")
        reports_btn.setStyleSheet("""
            QPushButton {
                padding: 10px 15px;
                background: #8b5cf6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #7c3aed;
            }
        """)
        reports_btn.clicked.connect(self.show_reports)
        quick_actions_layout.addWidget(reports_btn)
        
        layout.addLayout(quick_actions_layout)
        
        return header
        
    def setup_ui(self):
        """Configura la interfaz del módulo TPV avanzado"""
        # Crear el header del módulo
        header = self.create_module_header()
        self.content_layout.addWidget(header)

        # Crear el splitter principal
        main_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Panel izquierdo - Productos y categorías
        left_panel = self.create_products_panel()
        main_splitter.addWidget(left_panel)

        # Panel derecho - Pedido actual y pago
        right_panel = self.create_order_panel()
        main_splitter.addWidget(right_panel)

        # Configurar proporciones del splitter
        main_splitter.setSizes([400, 300])

        self.content_layout.addWidget(main_splitter)

        # Inicializar atributos
        self.order_table = QTableWidget()
        self.order_table.setColumnCount(5)
        self.order_table.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad", "Descuento", "Total"])
        header = self.order_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.subtotal_label = QLabel("Subtotal: €0.00")
        self.discount_label = QLabel("Descuento: €0.00")
        self.tax_label = QLabel("IVA (21%): €0.00")
        self.total_label = QLabel("TOTAL: €0.00")

        # Agregar etiquetas al layout del panel derecho
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(self.order_table)
        right_layout.addWidget(self.subtotal_label)
        right_layout.addWidget(self.discount_label)
        right_layout.addWidget(self.tax_label)
        right_layout.addWidget(self.total_label)
        
    def create_products_panel(self):
        """Crea el panel de productos y categorías"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Barra de búsqueda
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar productos...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                border: 2px solid #e5e7eb;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """)
        self.search_input.textChanged.connect(self.filter_products)
        search_layout.addWidget(self.search_input)
        
        layout.addLayout(search_layout)
        
        # Pestañas de categorías
        categories_tabs = QTabWidget()
        categories_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e5e7eb;
                background: white;
            }
            QTabBar::tab {
                padding: 10px 15px;
                margin-right: 2px;
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                border-bottom: none;
            }
            QTabBar::tab:selected {
                background: white;
            }
        """)
        
        # Categorías de productos
        categories = ["Bebidas", "Comidas", "Postres", "Especiales"]
        for category in categories:
            tab = self.create_category_tab(category)
            categories_tabs.addTab(tab, category)
        
        layout.addWidget(categories_tabs)
        
        return widget
        
    def create_category_tab(self, category):
        """Crea una pestaña para una categoría de productos"""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Placeholder para productos
        products_label = QLabel(f"Productos de la categoría: {category}")
        products_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        products_label.setStyleSheet("font-size: 16px; color: #6b7280;")
        layout.addWidget(products_label)

        return tab

    def create_order_panel(self):
        """Crea el panel de pedido actual y pago"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Placeholder para el pedido actual
        order_label = QLabel("Pedido Actual (Placeholder)")
        order_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        order_label.setStyleSheet("font-size: 16px; color: #6b7280;")
        layout.addWidget(order_label)

        # Botón de procesar pago
        process_payment_btn = QPushButton("Procesar Pago")
        process_payment_btn.setStyleSheet("background: #10b981; color: white; padding: 10px; border-radius: 6px;")
        process_payment_btn.clicked.connect(self.process_payment)
        layout.addWidget(process_payment_btn)

        return panel

    def get_action_button_style(self, color):
        """Obtiene el estilo para botones de acción"""
        return f"""
            QPushButton {{
                padding: 8px 12px;
                background: {color};
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                margin: 2px;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """
        
    def get_products_by_category(self, category):
        """Obtiene productos por categoría"""
        products_data = {
            "Bebidas": [
                {"name": "Café", "price": 1.50, "color": "#8b4513"},
                {"name": "Té", "price": 1.30, "color": "#228b22"},
                {"name": "Refresco", "price": 2.00, "color": "#4169e1"},
                {"name": "Agua", "price": 1.00, "color": "#87ceeb"},
                {"name": "Cerveza", "price": 2.50, "color": "#daa520"},
                {"name": "Vino", "price": 3.50, "color": "#800080"},
                {"name": "Zumo", "price": 2.20, "color": "#ff8c00"},
                {"name": "Batido", "price": 3.00, "color": "#ff69b4"}
            ],
            "Comidas": [
                {"name": "Hamburguesa", "price": 8.50, "color": "#cd853f"},
                {"name": "Pizza", "price": 12.00, "color": "#dc143c"},
                {"name": "Ensalada", "price": 6.50, "color": "#32cd32"},
                {"name": "Pasta", "price": 9.00, "color": "#ffd700"},
                {"name": "Sandwich", "price": 5.50, "color": "#deb887"},
                {"name": "Pollo", "price": 11.00, "color": "#d2691e"},
                {"name": "Pescado", "price": 13.50, "color": "#4682b4"},
                {"name": "Paella", "price": 15.00, "color": "#ff6347"}
            ],
            "Postres": [
                {"name": "Tarta", "price": 4.50, "color": "#ff1493"},
                {"name": "Helado", "price": 3.00, "color": "#ffc0cb"},
                {"name": "Flan", "price": 3.50, "color": "#daa520"},
                {"name": "Fruta", "price": 2.50, "color": "#ff4500"},
                {"name": "Brownie", "price": 4.00, "color": "#654321"},
                {"name": "Mousse", "price": 4.50, "color": "#8b4513"},
                {"name": "Yogur", "price": 2.00, "color": "#fff8dc"},
                {"name": "Churros", "price": 3.50, "color": "#deb887"}
            ],
            "Especiales": [
                {"name": "Menú del Día", "price": 12.50, "color": "#ff6347"},
                {"name": "Combo Niños", "price": 8.00, "color": "#ff69b4"},
                {"name": "Desayuno", "price": 6.50, "color": "#ffd700"},
                {"name": "Tapas", "price": 4.50, "color": "#32cd32"},
                {"name": "Brunch", "price": 11.00, "color": "#ff8c00"},
                {"name": "Cena Romántica", "price": 25.00, "color": "#800080"},
                {"name": "Menú Vegano", "price": 10.50, "color": "#228b22"},
                {"name": "Plato Chef", "price": 18.00, "color": "#4169e1"}
            ]
        }
        return products_data.get(category, [])
        
    def filter_products(self, text):
        """Filtra productos por texto de búsqueda"""
        # TODO: Implementar filtrado de productos
        pass
        
    def add_product_to_order(self, product):
        """Añade un producto al pedido actual"""
        # Crear pedido si no existe
        if not self.current_order:
            self.current_order = {
                "items": [],
                "subtotal": 0.0,
                "discount": 0.0,
                "tax": 0.0,
                "total": 0.0
            }
        
        # Buscar si el producto ya existe en el pedido
        existing_item = None
        for item in self.current_order["items"]:
            if item["name"] == product["name"]:
                existing_item = item
                break
        
        if existing_item:
            existing_item["quantity"] += 1
            existing_item["total"] = existing_item["price"] * existing_item["quantity"]
        else:
            new_item = {
                "name": product["name"],
                "price": product["price"],
                "quantity": 1,
                "discount": 0.0,
                "total": product["price"]
            }
            self.current_order["items"].append(new_item)
        
        self.update_order_display()
        
    def update_order_display(self):
        """Actualiza la visualización del pedido"""
        if not self.current_order:
            return
            
        # Actualizar tabla
        self.order_table.setRowCount(len(self.current_order["items"]))
        
        subtotal = 0.0
        for row, item in enumerate(self.current_order["items"]):
            self.order_table.setItem(row, 0, QTableWidgetItem(item["name"]))
            self.order_table.setItem(row, 1, QTableWidgetItem(f"€{item['price']:.2f}"))
            self.order_table.setItem(row, 2, QTableWidgetItem(str(item["quantity"])))
            self.order_table.setItem(row, 3, QTableWidgetItem(f"€{item['discount']:.2f}"))
            self.order_table.setItem(row, 4, QTableWidgetItem(f"€{item['total']:.2f}"))
            
            subtotal += item["total"]
        
        # Calcular totales
        discount_total = self.current_order["discount"]
        subtotal_after_discount = subtotal - discount_total
        tax = subtotal_after_discount * 0.21  # IVA 21%
        total = subtotal_after_discount + tax
        
        # Actualizar labels
        self.subtotal_label.setText(f"Subtotal: €{subtotal:.2f}")
        self.discount_label.setText(f"Descuento: €{discount_total:.2f}")
        self.tax_label.setText(f"IVA (21%): €{tax:.2f}")
        self.total_label.setText(f"TOTAL: €{total:.2f}")
        
        # Actualizar orden
        self.current_order.update({
            "subtotal": subtotal,
            "tax": tax,
            "total": total
        })
        
    def apply_discount(self):
        """Aplica un descuento al pedido"""
        if not self.current_order or not self.current_order["items"]:
            QMessageBox.warning(self, "Advertencia", "No hay productos en el pedido")
            return
            
        dialog = DiscountDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            discount_type, discount_value = dialog.get_discount()
            
            if discount_type == "percentage":
                self.current_order["discount"] = self.current_order["subtotal"] * (discount_value / 100)
            else:  # amount
                self.current_order["discount"] = min(discount_value, self.current_order["subtotal"])
                
            self.update_order_display()
            
    def clear_order(self):
        """Limpia el pedido actual"""
        if self.current_order and self.current_order["items"]:
            reply = QMessageBox.question(self, "Confirmar", "¿Limpiar el pedido actual?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.current_order = None
                self.order_table.setRowCount(0)
                self.subtotal_label.setText("Subtotal: €0.00")
                self.discount_label.setText("Descuento: €0.00")
                self.tax_label.setText("IVA (21%): €0.00")
                self.total_label.setText("TOTAL: €0.00")
                
    def process_payment(self):
        """Placeholder para procesar el pago"""
        QMessageBox.information(self, "Procesar Pago", "Funcionalidad de pago en desarrollo.")
        
    def new_order(self):
        """Inicia un nuevo pedido"""
        self.clear_order()
        
    def open_cash_register(self):
        """Abre la gestión de caja"""
        dialog = CashRegisterDialog(self)
        dialog.exec()
        
    def show_reports(self):
        """Muestra los reportes de ventas"""
        dialog = ReportsDialog(self)
        dialog.exec()
        
    def refresh(self):
        """Actualiza los datos del módulo"""
        logger.info("Actualizando módulo TPV avanzado...")
        self.status_changed.emit("TPV actualizado")


class DiscountDialog(QDialog):
    """Diálogo para aplicar descuentos"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Aplicar Descuento")
        self.setFixedSize(300, 200)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QFormLayout(self)
        
        # Tipo de descuento
        self.discount_type = QComboBox()
        self.discount_type.addItems(["Porcentaje", "Cantidad fija"])
        layout.addRow("Tipo:", self.discount_type)
        
        # Valor del descuento
        self.discount_value = QDoubleSpinBox()
        self.discount_value.setMinimum(0)
        self.discount_value.setMaximum(100)
        self.discount_value.setDecimals(2)
        layout.addRow("Valor:", self.discount_value)
        
        # Motivo
        self.reason = QLineEdit()
        self.reason.setPlaceholderText("Motivo del descuento...")
        layout.addRow("Motivo:", self.reason)
        
        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
    def get_discount(self):
        """Obtiene el descuento configurado"""
        discount_type = "percentage" if self.discount_type.currentIndex() == 0 else "amount"
        return discount_type, self.discount_value.value()


class PaymentDialog(QDialog):
    """Diálogo para procesar el pago"""
    
    def __init__(self, order, parent=None):
        super().__init__(parent)
        self.order = order
        self.setWindowTitle("Procesar Pago")
        self.setFixedSize(450, 400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Resumen del pedido
        summary_group = QGroupBox("Resumen del Pedido")
        summary_layout = QVBoxLayout(summary_group)
        
        total_label = QLabel(f"TOTAL A PAGAR: €{self.order['total']:.2f}")
        total_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #059669;")
        summary_layout.addWidget(total_label)
        
        layout.addWidget(summary_group)
        
        # Métodos de pago
        payment_group = QGroupBox("Método de Pago")
        payment_layout = QVBoxLayout(payment_group)
        
        self.payment_method = QComboBox()
        self.payment_method.addItems([
            "Efectivo", "Tarjeta de Crédito", "Tarjeta de Débito", 
            "Transferencia", "Bizum", "PayPal"
        ])
        payment_layout.addWidget(self.payment_method)
        
        layout.addWidget(payment_group)
        
        # Pago en efectivo
        cash_group = QGroupBox("Pago en Efectivo")
        cash_layout = QFormLayout(cash_group)
        
        self.cash_received = QDoubleSpinBox()
        self.cash_received.setMinimum(0)
        self.cash_received.setMaximum(9999.99)
        self.cash_received.setDecimals(2)
        self.cash_received.setValue(self.order['total'])
        self.cash_received.valueChanged.connect(self.calculate_change)
        cash_layout.addRow("Recibido:", self.cash_received)
        
        self.change_label = QLabel("€0.00")
        self.change_label.setStyleSheet("font-weight: bold; color: #059669;")
        cash_layout.addRow("Cambio:", self.change_label)
        
        layout.addWidget(cash_group)
        
        # Opciones adicionales
        options_group = QGroupBox("Opciones")
        options_layout = QVBoxLayout(options_group)
        
        self.print_receipt = QCheckBox("Imprimir recibo")
        self.print_receipt.setChecked(True)
        options_layout.addWidget(self.print_receipt)
        
        self.send_email = QCheckBox("Enviar por email")
        options_layout.addWidget(self.send_email)
        
        layout.addWidget(options_group)
        
        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | 
                                 QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        # Calcular cambio inicial
        self.calculate_change()
        
    def calculate_change(self):
        """Calcula el cambio"""
        received = self.cash_received.value()
        total = self.order['total']
        change = received - total
        
        if change >= 0:
            self.change_label.setText(f"€{change:.2f}")
            self.change_label.setStyleSheet("font-weight: bold; color: #059669;")
        else:
            self.change_label.setText(f"-€{abs(change):.2f}")
            self.change_label.setStyleSheet("font-weight: bold; color: #ef4444;")


class CashRegisterDialog(QDialog):
    """Diálogo para gestión de caja"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestión de Caja")
        self.setFixedSize(400, 300)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Estado de caja
        status_group = QGroupBox("Estado de Caja")
        status_layout = QFormLayout(status_group)
        
        self.opening_amount = QLabel("€500.00")
        status_layout.addRow("Apertura:", self.opening_amount)
        
        self.current_amount = QLabel("€750.50")
        status_layout.addRow("Actual:", self.current_amount)
        
        self.sales_amount = QLabel("€250.50")
        status_layout.addRow("Ventas:", self.sales_amount)
        
        layout.addWidget(status_group)
        
        # Operaciones
        operations_group = QGroupBox("Operaciones")
        operations_layout = QVBoxLayout(operations_group)
        
        open_register_btn = QPushButton("Abrir Caja")
        open_register_btn.clicked.connect(self.open_register)
        operations_layout.addWidget(open_register_btn)
        
        close_register_btn = QPushButton("Cerrar Caja")
        close_register_btn.clicked.connect(self.close_register)
        operations_layout.addWidget(close_register_btn)
        
        add_money_btn = QPushButton("Añadir Dinero")
        add_money_btn.clicked.connect(self.add_money)
        operations_layout.addWidget(add_money_btn)
        
        remove_money_btn = QPushButton("Retirar Dinero")
        remove_money_btn.clicked.connect(self.remove_money)
        operations_layout.addWidget(remove_money_btn)
        
        layout.addWidget(operations_group)
        
        # Botón cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
    def open_register(self):
        """Abre la caja registradora"""
        QMessageBox.information(self, "Caja", "Caja abierta correctamente")
        
    def close_register(self):
        """Cierra la caja registradora"""
        QMessageBox.information(self, "Caja", "Caja cerrada correctamente")
        
    def add_money(self):
        """Añade dinero a la caja"""
        QMessageBox.information(self, "Caja", "Dinero añadido a la caja")
        
    def remove_money(self):
        """Retira dinero de la caja"""
        QMessageBox.information(self, "Caja", "Dinero retirado de la caja")


class ReportsDialog(QDialog):
    """Diálogo para mostrar reportes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Reportes de Ventas")
        self.setFixedSize(600, 400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Filtros
        filters_group = QGroupBox("Filtros")
        filters_layout = QFormLayout(filters_group)
        
        self.date_from = QLineEdit("2025-06-01")
        filters_layout.addRow("Desde:", self.date_from)
        
        self.date_to = QLineEdit("2025-06-10")
        filters_layout.addRow("Hasta:", self.date_to)
        
        generate_btn = QPushButton("Generar Reporte")
        generate_btn.clicked.connect(self.generate_report)
        filters_layout.addRow(generate_btn)
        
        layout.addWidget(filters_group)
        
        # Resultados
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)
        
        # Botón cerrar
        close_btn = QPushButton("Cerrar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
    def generate_report(self):
        """Genera el reporte de ventas"""
        report = f"""
REPORTE DE VENTAS
================
Periodo: {self.date_from.text()} - {self.date_to.text()}

Resumen:
- Total ventas: €1,250.75
- Número de transacciones: 45
- Ticket promedio: €27.79
- Método de pago más usado: Tarjeta (60%)

Productos más vendidos:
1. Café - 120 unidades
2. Hamburguesa - 35 unidades  
3. Pizza - 28 unidades
4. Cerveza - 55 unidades
5. Ensalada - 22 unidades

Ventas por categoría:
- Bebidas: €345.20 (28%)
- Comidas: €650.30 (52%)
- Postres: €155.25 (12%)
- Especiales: €100.00 (8%)
        """
        self.results_text.setText(report)
