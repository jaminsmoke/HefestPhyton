"""
TPV Avanzado - Panel de pedidos modernizado con gestión avanzada
"""

from typing import Any, Dict, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QPushButton, QFrame, QHeaderView, QScrollArea, QComboBox,
    QSpinBox, QTextEdit, QGroupBox, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from .styles_modern import (
    get_modern_button_style,
    get_modern_table_style,
    get_modern_input_style,
    get_status_badge_style,
    COLORS,
    SPACING,
    BORDER_RADIUS
)


class ModernOrderItem(QWidget):
    """Item moderno de pedido con controles avanzados"""
    
    quantity_changed = pyqtSignal(int, int)  # item_id, new_quantity
    item_removed = pyqtSignal(int)  # item_id
    notes_changed = pyqtSignal(int, str)  # item_id, notes
    
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.item_data = item_data
        self.item_id = item_data.get('id', 0)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del item"""
        # Frame principal
        self.setStyleSheet(f"""
            ModernOrderItem {{
                background: {COLORS['white']};
                border: 1px solid {COLORS['gray_200']};
                border-radius: {BORDER_RADIUS['md']};
                margin: {SPACING['xs']};
                padding: {SPACING['md']};
            }}
            ModernOrderItem:hover {{
                border-color: {COLORS['primary_light']};
                background: {COLORS['gray_50']};
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(8)
        
        # Fila principal: Producto + Precio + Controles
        main_row = QHBoxLayout()
        
        # Información del producto
        product_info = QVBoxLayout()
        
        # Nombre del producto
        self.product_name = QLabel(self.item_data.get('nombre', 'Producto'))
        self.product_name.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        self.product_name.setStyleSheet(f"color: {COLORS['gray_800']};")
        product_info.addWidget(self.product_name)
        
        # Precio unitario
        precio = self.item_data.get('precio', 0.0)
        self.unit_price = QLabel(f"€{precio:.2f} /ud")
        self.unit_price.setFont(QFont("Segoe UI", 10))
        self.unit_price.setStyleSheet(f"color: {COLORS['gray_600']};")
        product_info.addWidget(self.unit_price)
        
        main_row.addLayout(product_info, 2)
        
        # Controles de cantidad
        quantity_group = QHBoxLayout()
        
        # Botón menos
        self.minus_btn = QPushButton("−")
        self.minus_btn.setFixedSize(28, 28)
        self.minus_btn.setStyleSheet(get_modern_button_style("secondary", "sm"))
        self.minus_btn.clicked.connect(self.decrease_quantity)
        quantity_group.addWidget(self.minus_btn)
        
        # Spinner de cantidad
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setRange(1, 99)
        self.quantity_spin.setValue(self.item_data.get('cantidad', 1))
        self.quantity_spin.setStyleSheet(get_modern_input_style())
        self.quantity_spin.setFixedWidth(60)
        self.quantity_spin.valueChanged.connect(self.on_quantity_changed)
        quantity_group.addWidget(self.quantity_spin)
        
        # Botón más
        self.plus_btn = QPushButton("+")
        self.plus_btn.setFixedSize(28, 28)
        self.plus_btn.setStyleSheet(get_modern_button_style("primary", "sm"))
        self.plus_btn.clicked.connect(self.increase_quantity)
        quantity_group.addWidget(self.plus_btn)
        
        main_row.addLayout(quantity_group)
        
        # Total del item
        self.total_label = QLabel()
        self.total_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.total_label.setStyleSheet(f"color: {COLORS['primary']};")
        self.total_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.update_total()
        main_row.addWidget(self.total_label)
        
        # Botón eliminar
        self.remove_btn = QPushButton("🗑️")
        self.remove_btn.setFixedSize(32, 32)
        self.remove_btn.setStyleSheet(get_modern_button_style("danger", "sm"))
        self.remove_btn.clicked.connect(self.remove_item)
        main_row.addWidget(self.remove_btn)
        
        layout.addLayout(main_row)
        
        # Área de notas (expandible)
        self.notes_area = QTextEdit()
        self.notes_area.setPlaceholderText("Notas especiales (ej: sin cebolla, extra queso...)")
        self.notes_area.setMaximumHeight(60)
        self.notes_area.setStyleSheet(get_modern_input_style())
        self.notes_area.textChanged.connect(self.on_notes_changed)
        layout.addWidget(self.notes_area)
        
        # Inicialmente ocultar notas
        self.notes_area.hide()
        
        # Botón para mostrar/ocultar notas
        self.notes_btn = QPushButton("📝 Añadir notas")
        self.notes_btn.setStyleSheet(get_modern_button_style("secondary", "sm"))
        self.notes_btn.clicked.connect(self.toggle_notes)
        layout.addWidget(self.notes_btn)
    
    def update_total(self):
        """Actualiza el total del item"""
        cantidad = self.quantity_spin.value()
        precio = self.item_data.get('precio', 0.0)
        total = cantidad * precio
        self.total_label.setText(f"€{total:.2f}")
    
    def increase_quantity(self):
        """Incrementa la cantidad"""
        current = self.quantity_spin.value()
        self.quantity_spin.setValue(current + 1)
    
    def decrease_quantity(self):
        """Decrementa la cantidad"""
        current = self.quantity_spin.value()
        if current > 1:
            self.quantity_spin.setValue(current - 1)
    
    def on_quantity_changed(self, value):
        """Maneja cambios en la cantidad"""
        self.update_total()
        self.quantity_changed.emit(self.item_id, value)
    
    def remove_item(self):
        """Elimina el item del pedido"""
        self.item_removed.emit(self.item_id)
    
    def toggle_notes(self):
        """Muestra/oculta el área de notas"""
        if self.notes_area.isVisible():
            self.notes_area.hide()
            self.notes_btn.setText("📝 Añadir notas")
        else:
            self.notes_area.show()
            self.notes_btn.setText("📝 Ocultar notas")
            self.notes_area.setFocus()
    
    def on_notes_changed(self):
        """Maneja cambios en las notas"""
        notes = self.notes_area.toPlainText()
        self.notes_changed.emit(self.item_id, notes)
    
    def get_item_data(self):
        """Obtiene los datos actuales del item"""
        return {
            **self.item_data,
            'cantidad': self.quantity_spin.value(),
            'notas': self.notes_area.toPlainText(),
            'total': self.quantity_spin.value() * self.item_data.get('precio', 0.0)
        }


class ModernPaymentPanel(QWidget):
    """Panel moderno de pago con múltiples métodos"""
    
    payment_processed = pyqtSignal(dict)  # Datos del pago
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del panel de pago"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        
        # Métodos de pago
        payment_group = QGroupBox("💳 Método de Pago")
        payment_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {COLORS['gray_200']};
                border-radius: {BORDER_RADIUS['md']};
                margin-top: 10px;
                padding-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }}
        """)
        
        payment_layout = QGridLayout(payment_group)
        
        # Botones de método de pago
        self.payment_methods = {
            "efectivo": "💵 Efectivo",
            "tarjeta": "💳 Tarjeta",
            "movil": "📱 Móvil",
            "vale": "🎫 Vale"
        }
        
        self.payment_buttons = {}
        row, col = 0, 0
        
        for method_id, method_name in self.payment_methods.items():
            btn = QPushButton(method_name)
            btn.setCheckable(True)
            btn.setStyleSheet(get_modern_button_style("secondary", "md"))
            btn.clicked.connect(lambda checked, m=method_id: self.select_payment_method(m))
            payment_layout.addWidget(btn, row, col)
            self.payment_buttons[method_id] = btn
            
            col += 1
            if col >= 2:
                col = 0
                row += 1
        
        layout.addWidget(payment_group)
        
        # Propina
        tip_group = QGroupBox("💰 Propina")
        tip_group.setStyleSheet(payment_group.styleSheet())
        tip_layout = QHBoxLayout(tip_group)
        
        # Porcentajes predefinidos
        tip_percentages = [0, 5, 10, 15, 20]
        self.tip_buttons = {}
        
        for percentage in tip_percentages:
            btn = QPushButton(f"{percentage}%")
            btn.setCheckable(True)
            btn.setStyleSheet(get_modern_button_style("secondary", "sm"))
            btn.clicked.connect(lambda checked, p=percentage: self.set_tip_percentage(p))
            tip_layout.addWidget(btn)
            self.tip_buttons[percentage] = btn
        
        # Propina personalizada
        tip_layout.addWidget(QLabel("Custom:"))
        self.custom_tip = QSpinBox()
        self.custom_tip.setRange(0, 999)
        self.custom_tip.setSuffix(" €")
        self.custom_tip.setStyleSheet(get_modern_input_style())
        self.custom_tip.valueChanged.connect(self.on_custom_tip_changed)
        tip_layout.addWidget(self.custom_tip)
        
        layout.addWidget(tip_group)
        
        # Botón de pagar
        self.pay_button = QPushButton("💰 PROCESAR PAGO")
        self.pay_button.setStyleSheet(get_modern_button_style("success", "lg"))
        self.pay_button.setMinimumHeight(50)
        self.pay_button.clicked.connect(self.process_payment)
        layout.addWidget(self.pay_button)
        
        # Estado inicial
        self.selected_payment_method = None
        self.selected_tip = 0
        self.update_pay_button()
    
    def select_payment_method(self, method_id):
        """Selecciona un método de pago"""
        # Deseleccionar otros botones
        for mid, btn in self.payment_buttons.items():
            btn.setChecked(mid == method_id)
            if mid == method_id:
                btn.setStyleSheet(get_modern_button_style("primary", "md"))
            else:
                btn.setStyleSheet(get_modern_button_style("secondary", "md"))
        
        self.selected_payment_method = method_id
        self.update_pay_button()
    
    def set_tip_percentage(self, percentage):
        """Establece el porcentaje de propina"""
        # Deseleccionar otros botones
        for p, btn in self.tip_buttons.items():
            btn.setChecked(p == percentage)
            if p == percentage:
                btn.setStyleSheet(get_modern_button_style("primary", "sm"))
            else:
                btn.setStyleSheet(get_modern_button_style("secondary", "sm"))
        
        self.selected_tip = percentage
        self.custom_tip.setValue(0)  # Reset custom tip
        self.update_pay_button()
    
    def on_custom_tip_changed(self, value):
        """Maneja cambios en la propina personalizada"""
        if value > 0:
            # Deseleccionar botones de porcentaje
            for btn in self.tip_buttons.values():
                btn.setChecked(False)
                btn.setStyleSheet(get_modern_button_style("secondary", "sm"))
            self.selected_tip = value
        else:
            self.selected_tip = 0
        
        self.update_pay_button()
    
    def update_pay_button(self):
        """Actualiza el estado del botón de pago"""
        enabled = self.selected_payment_method is not None
        self.pay_button.setEnabled(enabled)
        
        if enabled:
            method_name = self.payment_methods[self.selected_payment_method]
            if self.selected_tip > 0:
                if isinstance(self.selected_tip, int) and self.selected_tip < 30:
                    # Es porcentaje
                    self.pay_button.setText(f"💰 PAGAR ({method_name} + {self.selected_tip}%)")
                else:
                    # Es cantidad fija
                    self.pay_button.setText(f"💰 PAGAR ({method_name} + €{self.selected_tip})")
            else:
                self.pay_button.setText(f"💰 PAGAR ({method_name})")
    
    def process_payment(self):
        """Procesa el pago"""
        if not self.selected_payment_method:
            return
        
        payment_data = {
            'method': self.selected_payment_method,
            'tip': self.selected_tip,
            'tip_type': 'percentage' if self.selected_tip < 30 else 'amount'
        }
        
        self.payment_processed.emit(payment_data)
    
    def reset_payment(self):
        """Resetea el panel de pago"""
        self.selected_payment_method = None
        self.selected_tip = 0
        
        # Deseleccionar todos los botones
        for btn in self.payment_buttons.values():
            btn.setChecked(False)
            btn.setStyleSheet(get_modern_button_style("secondary", "md"))
        
        for btn in self.tip_buttons.values():
            btn.setChecked(False)
            btn.setStyleSheet(get_modern_button_style("secondary", "sm"))
        
        self.custom_tip.setValue(0)
        self.update_pay_button()


class ModernOrderPanel(QWidget):
    """Panel moderno de gestión de pedidos"""
    
    order_updated = pyqtSignal(dict)  # Datos del pedido actualizado
    payment_requested = pyqtSignal(dict)  # Solicitud de pago
    
    def __init__(self, parent_tpv, parent=None):
        super().__init__(parent)
        self.parent_tpv = parent_tpv
        self.order_items = []  # Lista de items del pedido
        self.item_widgets = {}  # Widgets de items
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del panel"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(16)
        
        # Header del pedido
        header = self.create_order_header()
        layout.addWidget(header)
        
        # Lista de items del pedido
        self.items_scroll = self.create_items_scroll()
        layout.addWidget(self.items_scroll, 1)
        
        # Resumen del pedido
        self.summary_widget = self.create_order_summary()
        layout.addWidget(self.summary_widget)
        
        # Panel de pago
        self.payment_panel = ModernPaymentPanel()
        self.payment_panel.payment_processed.connect(self.on_payment_processed)
        layout.addWidget(self.payment_panel)
        
        # Aplicar estilos
        self.apply_panel_styles()
    
    def create_order_header(self):
        """Crea el header del panel de pedidos"""
        header = QFrame()
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Título
        title = QLabel("🧾 Pedido Actual")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {COLORS['gray_800']};")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Botón limpiar pedido
        self.clear_order_btn = QPushButton("🗑️ Limpiar")
        self.clear_order_btn.setStyleSheet(get_modern_button_style("warning", "sm"))
        self.clear_order_btn.clicked.connect(self.clear_order)
        layout.addWidget(self.clear_order_btn)
        
        return header
    
    def create_items_scroll(self):
        """Crea el área scrollable de items"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: 1px solid {COLORS['gray_200']};
                border-radius: {BORDER_RADIUS['md']};
                background: {COLORS['gray_50']};
            }}
        """)
        
        # Widget contenedor
        self.items_container = QWidget()
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setContentsMargins(8, 8, 8, 8)
        self.items_layout.setSpacing(4)
        
        # Mensaje cuando no hay items
        self.empty_message = QLabel("No hay productos en el pedido")
        self.empty_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_message.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['gray_500']};
                font-style: italic;
                padding: {SPACING['xl']};
            }}
        """)
        self.items_layout.addWidget(self.empty_message)
        
        self.items_layout.addStretch()
        scroll.setWidget(self.items_container)
        
        return scroll
    
    def create_order_summary(self):
        """Crea el resumen del pedido"""
        summary = QFrame()
        summary.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['gray_50']}, 
                    stop:1 {COLORS['white']});
                border: 2px solid {COLORS['gray_200']};
                border-radius: {BORDER_RADIUS['lg']};
                padding: {SPACING['lg']};
            }}
        """)
        
        layout = QVBoxLayout(summary)
        layout.setSpacing(8)
        
        # Subtotal
        self.subtotal_label = QLabel("Subtotal: €0.00")
        self.subtotal_label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.subtotal_label)
        
        # IVA
        self.tax_label = QLabel("IVA (21%): €0.00")
        self.tax_label.setFont(QFont("Segoe UI", 12))
        layout.addWidget(self.tax_label)
        
        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet(f"background: {COLORS['gray_300']};")
        layout.addWidget(separator)
        
        # Total
        self.total_label = QLabel("TOTAL: €0.00")
        self.total_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.total_label.setStyleSheet(f"color: {COLORS['primary']};")
        layout.addWidget(self.total_label)
        
        return summary
    
    def apply_panel_styles(self):
        """Aplica estilos al panel"""
        self.setStyleSheet(f"""
            ModernOrderPanel {{
                background: {COLORS['white']};
                border-radius: {BORDER_RADIUS['lg']};
            }}
        """)
    
    def add_product(self, product_data):
        """Añade un producto al pedido"""
        # Verificar si el producto ya existe
        existing_item = None
        for item in self.order_items:
            if item.get('id') == product_data.get('id'):
                existing_item = item
                break
        
        if existing_item:
            # Incrementar cantidad
            existing_item['cantidad'] = existing_item.get('cantidad', 1) + 1
            self.update_item_widget(existing_item)
        else:
            # Añadir nuevo item
            new_item = {
                **product_data,
                'cantidad': 1,
                'notas': '',
                'item_id': len(self.order_items)  # ID único para el widget
            }
            self.order_items.append(new_item)
            self.create_item_widget(new_item)
        
        self.update_order_summary()
        self.update_empty_state()
    
    def create_item_widget(self, item_data):
        """Crea un widget para un item del pedido"""
        item_widget = ModernOrderItem(item_data)
        item_widget.quantity_changed.connect(self.on_item_quantity_changed)
        item_widget.item_removed.connect(self.on_item_removed)
        item_widget.notes_changed.connect(self.on_item_notes_changed)
        
        # Insertar antes del stretch
        self.items_layout.insertWidget(self.items_layout.count() - 1, item_widget)
        
        # Guardar referencia
        item_id = item_data.get('item_id', 0)
        self.item_widgets[item_id] = item_widget
    
    def update_item_widget(self, item_data):
        """Actualiza un widget de item existente"""
        item_id = item_data.get('item_id', 0)
        if item_id in self.item_widgets:
            widget = self.item_widgets[item_id]
            widget.quantity_spin.setValue(item_data.get('cantidad', 1))
            widget.update_total()
    
    def on_item_quantity_changed(self, item_id, new_quantity):
        """Maneja cambios en la cantidad de un item"""
        for item in self.order_items:
            if item.get('item_id') == item_id:
                item['cantidad'] = new_quantity
                break
        
        self.update_order_summary()
    
    def on_item_removed(self, item_id):
        """Maneja la eliminación de un item"""
        # Remover del layout
        if item_id in self.item_widgets:
            widget = self.item_widgets[item_id]
            self.items_layout.removeWidget(widget)
            widget.deleteLater()
            del self.item_widgets[item_id]
        
        # Remover de la lista
        self.order_items = [item for item in self.order_items if item.get('item_id') != item_id]
        
        self.update_order_summary()
        self.update_empty_state()
    
    def on_item_notes_changed(self, item_id, notes):
        """Maneja cambios en las notas de un item"""
        for item in self.order_items:
            if item.get('item_id') == item_id:
                item['notas'] = notes
                break
    
    def update_order_summary(self):
        """Actualiza el resumen del pedido"""
        subtotal = sum(
            item.get('precio', 0) * item.get('cantidad', 1) 
            for item in self.order_items
        )
        
        tax = subtotal * 0.21  # IVA 21%
        total = subtotal + tax
        
        self.subtotal_label.setText(f"Subtotal: €{subtotal:.2f}")
        self.tax_label.setText(f"IVA (21%): €{tax:.2f}")
        self.total_label.setText(f"TOTAL: €{total:.2f}")
        
        # Actualizar estado del panel de pago
        self.payment_panel.setEnabled(len(self.order_items) > 0)
    
    def update_empty_state(self):
        """Actualiza el estado vacío del pedido"""
        has_items = len(self.order_items) > 0
        self.empty_message.setVisible(not has_items)
        self.clear_order_btn.setEnabled(has_items)
    
    def clear_order(self):
        """Limpia el pedido actual"""
        # Remover todos los widgets
        for widget in self.item_widgets.values():
            self.items_layout.removeWidget(widget)
            widget.deleteLater()
        
        # Limpiar datos
        self.order_items.clear()
        self.item_widgets.clear()
        
        # Actualizar UI
        self.update_order_summary()
        self.update_empty_state()
        
        # Reset panel de pago
        self.payment_panel.reset_payment()
    
    def on_payment_processed(self, payment_data):
        """Maneja el procesamiento del pago"""
        if not self.order_items:
            return
        
        # Calcular totales
        subtotal = sum(
            item.get('precio', 0) * item.get('cantidad', 1) 
            for item in self.order_items
        )
        
        tax = subtotal * 0.21
        
        # Calcular propina
        tip_amount = 0
        if payment_data.get('tip', 0) > 0:
            if payment_data.get('tip_type') == 'percentage':
                tip_amount = subtotal * (payment_data['tip'] / 100)
            else:
                tip_amount = payment_data['tip']
        
        total = subtotal + tax + tip_amount
        
        # Datos completos del pedido
        order_data = {
            'items': [widget.get_item_data() for widget in self.item_widgets.values()],
            'subtotal': subtotal,
            'tax': tax,
            'tip': tip_amount,
            'total': total,
            'payment_method': payment_data['method'],
            'mesa_id': getattr(self.parent_tpv.mesa, 'numero', 0) if self.parent_tpv.mesa else 0
        }
        
        # Emitir señal
        self.payment_requested.emit(order_data)
    
    def get_order_data(self):
        """Obtiene los datos completos del pedido"""
        return {
            'items': [widget.get_item_data() for widget in self.item_widgets.values()],
            'total_items': len(self.order_items),
            'subtotal': sum(item.get('precio', 0) * item.get('cantidad', 1) for item in self.order_items)
        }


def create_modern_pedido_panel(parent_tpv) -> ModernOrderPanel:
    """
    Función factory para crear el panel de pedidos moderno
    
    Args:
        parent_tpv: Instancia del TPV principal
        
    Returns:
        ModernOrderPanel: Panel de pedidos configurado
    """
    return ModernOrderPanel(parent_tpv)
