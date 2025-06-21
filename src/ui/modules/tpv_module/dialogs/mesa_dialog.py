"""
Diálogo de Mesa - Gestión completa de una mesa individual
"""

import logging
from typing import Optional, List
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QSplitter, QWidget,
    QLabel, QTableWidget, QTableWidgetItem, QPushButton,
    QComboBox, QSpinBox, QHeaderView, QFormLayout, QMessageBox,
    QFrame, QGroupBox, QScrollArea, QGridLayout, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon

from ..controllers.tpv_controller import TPVController
from services.tpv_service import Mesa, Comanda, Producto

logger = logging.getLogger(__name__)


class MesaDialog(QDialog):
    """Diálogo avanzado para la gestión completa de una mesa"""
    
    mesa_updated = pyqtSignal(Mesa)
    comanda_saved = pyqtSignal(int)  # comanda_id
    payment_processed = pyqtSignal(int, float)  # mesa_id, total
    
    def __init__(self, mesa: Mesa, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.controller = TPVController()
        self.current_comanda: Optional[Comanda] = None
        self.productos_cache: List[Producto] = []
        
        # Timer para auto-guardar
        self.auto_save_timer = QTimer()
        self.auto_save_timer.timeout.connect(self._auto_save)
        self.auto_save_timer.start(30000)  # Auto-guardar cada 30 segundos
        
        self.setup_ui()
        self.connect_signals()
        self.load_initial_data()
        
    def setup_ui(self):
        """Configura la interfaz principal del diálogo"""
        self.setWindowTitle(f"Mesa {self.mesa.numero} - {self.mesa.zona}")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header con información de la mesa
        self.setup_header(main_layout)
        
        # Splitter principal (productos | comanda)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setChildrenCollapsible(False)
        
        # Panel de productos (izquierda)
        self.setup_productos_panel(splitter)
        
        # Panel de comanda (derecha)
        self.setup_comanda_panel(splitter)
        
        # Configurar proporción del splitter
        splitter.setSizes([400, 600])
        main_layout.addWidget(splitter)
        
        # Footer con botones principales
        self.setup_footer(main_layout)
        
        # Aplicar estilos
        self.apply_styles()
    
    def setup_header(self, parent_layout: QVBoxLayout):
        """Configura el header con información de la mesa"""
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
                color: white;
                padding: 10px;
            }
        """)
        
        header_layout = QHBoxLayout(header_frame)
        
        # Información de la mesa
        mesa_info = QVBoxLayout()
        
        mesa_title = QLabel(f"🍽️ Mesa {self.mesa.numero}")
        mesa_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        mesa_title.setStyleSheet("color: white; margin: 0;")
        mesa_info.addWidget(mesa_title)
        
        mesa_details = QLabel(f"Zona: {self.mesa.zona} | Estado: {self.mesa.estado.title()}")
        mesa_details.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 12px;")
        mesa_info.addWidget(mesa_details)
        
        header_layout.addLayout(mesa_info)
        header_layout.addStretch()
        
        # Estado de tiempo
        self.time_label = QLabel("Tiempo: 00:00:00")
        self.time_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        header_layout.addWidget(self.time_label)
        
        parent_layout.addWidget(header_frame)
    
    def setup_productos_panel(self, splitter: QSplitter):
        """Configura el panel de productos"""
        productos_widget = QWidget()
        productos_layout = QVBoxLayout(productos_widget)
        productos_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header del panel de productos
        productos_header = QFrame()
        productos_header.setStyleSheet("""
            QFrame {
                background-color: #F8F9FA;
                border: 1px solid #DEE2E6;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        productos_header_layout = QHBoxLayout(productos_header)
        
        productos_title = QLabel("🛍️ Catálogo de Productos")
        productos_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        productos_title.setStyleSheet("color: #495057;")
        productos_header_layout.addWidget(productos_title)
        
        productos_header_layout.addStretch()
        
        # Filtro por categoría
        categoria_label = QLabel("Categoría:")
        categoria_label.setStyleSheet("color: #6C757D; font-weight: bold;")
        productos_header_layout.addWidget(categoria_label)
        
        self.categoria_combo = QComboBox()
        self.categoria_combo.setMinimumWidth(120)
        self.categoria_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #CED4DA;
                border-radius: 4px;
                padding: 4px 8px;
                background-color: white;
            }
            QComboBox:focus { border-color: #80BDFF; }
        """)
        productos_header_layout.addWidget(self.categoria_combo)
        
        productos_layout.addWidget(productos_header)
        
        # Tabla de productos
        self.productos_table = QTableWidget()
        self.productos_table.setColumnCount(3)
        self.productos_table.setHorizontalHeaderLabels(["Producto", "Precio", "Stock"])
        
        # Configurar tabla
        header = self.productos_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        self.productos_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.productos_table.setAlternatingRowColors(True)
        self.productos_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #DEE2E6;
                border-radius: 4px;
                gridline-color: #DEE2E6;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #E3F2FD;
                color: #1976D2;
            }
        """)
        productos_layout.addWidget(self.productos_table)
        
        # Controles de productos
        productos_controls = QHBoxLayout()
        
        self.cantidad_spin = QSpinBox()
        self.cantidad_spin.setMinimum(1)
        self.cantidad_spin.setMaximum(99)
        self.cantidad_spin.setValue(1)
        self.cantidad_spin.setPrefix("Cant: ")
        self.cantidad_spin.setStyleSheet("""
            QSpinBox {
                border: 1px solid #CED4DA;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }
        """)
        productos_controls.addWidget(self.cantidad_spin)
        
        productos_controls.addStretch()
        
        self.add_producto_btn = QPushButton("➕ Añadir")
        self.add_producto_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #218838; }
            QPushButton:pressed { background-color: #1E7E34; }
            QPushButton:disabled { 
                background-color: #6C757D; 
                color: #ADB5BD; 
            }
        """)
        productos_controls.addWidget(self.add_producto_btn)
        
        productos_layout.addLayout(productos_controls)
        
        splitter.addWidget(productos_widget)
    
    def setup_comanda_panel(self, splitter: QSplitter):
        """Configura el panel de la comanda"""
        comanda_widget = QWidget()
        comanda_layout = QVBoxLayout(comanda_widget)
        comanda_layout.setContentsMargins(0, 0, 0, 0)
        
        # Header del panel de comanda
        comanda_header = QFrame()
        comanda_header.setStyleSheet("""
            QFrame {
                background-color: #FFF3CD;
                border: 1px solid #FFEAA7;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        comanda_header_layout = QHBoxLayout(comanda_header)
        
        comanda_title = QLabel("📋 Comanda Actual")
        comanda_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        comanda_title.setStyleSheet("color: #856404;")
        comanda_header_layout.addWidget(comanda_title)
        
        comanda_header_layout.addStretch()
        
        self.comanda_status = QLabel("Estado: Nueva")
        self.comanda_status.setStyleSheet("color: #856404; font-weight: bold;")
        comanda_header_layout.addWidget(self.comanda_status)
        
        comanda_layout.addWidget(comanda_header)
        
        # Tabla de comanda
        self.comanda_table = QTableWidget()
        self.comanda_table.setColumnCount(4)
        self.comanda_table.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad", "Total"])
        
        # Configurar tabla de comanda
        comanda_header = self.comanda_table.horizontalHeader()
        if comanda_header:
            comanda_header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
            comanda_header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
            comanda_header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
            comanda_header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        self.comanda_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.comanda_table.setAlternatingRowColors(True)
        self.comanda_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #DEE2E6;
                border-radius: 4px;
                gridline-color: #DEE2E6;
                background-color: white;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #FFF3CD;
                color: #856404;
            }
        """)
        comanda_layout.addWidget(self.comanda_table)
        
        # Controles de comanda
        comanda_controls_layout = QVBoxLayout()
        
        # Línea de acciones de línea
        linea_actions = QHBoxLayout()
        
        self.remove_linea_btn = QPushButton("🗑️ Eliminar")
        self.remove_linea_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC3545;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #C82333; }
            QPushButton:disabled { 
                background-color: #6C757D; 
                color: #ADB5BD; 
            }
        """)
        linea_actions.addWidget(self.remove_linea_btn)
        
        self.edit_cantidad_btn = QPushButton("✏️ Cantidad")
        self.edit_cantidad_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFC107;
                color: #212529;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #E0A800; }
            QPushButton:disabled { 
                background-color: #6C757D; 
                color: #ADB5BD; 
            }
        """)
        linea_actions.addWidget(self.edit_cantidad_btn)
        
        linea_actions.addStretch()
        comanda_controls_layout.addLayout(linea_actions)
        
        # Total
        total_frame = QFrame()
        total_frame.setStyleSheet("""
            QFrame {
                background-color: #E8F5E8;
                border: 2px solid #28A745;
                border-radius: 6px;
                padding: 12px;
                margin: 5px 0;
            }
        """)
        total_layout = QHBoxLayout(total_frame)
        
        total_layout.addStretch()
        self.total_label = QLabel("Total: 0.00 €")
        self.total_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.total_label.setStyleSheet("color: #155724;")
        total_layout.addWidget(self.total_label)
        
        comanda_controls_layout.addWidget(total_frame)
        comanda_layout.addLayout(comanda_controls_layout)
        
        splitter.addWidget(comanda_widget)
    
    def setup_footer(self, parent_layout: QVBoxLayout):
        """Configura el footer con botones principales"""
        footer_layout = QHBoxLayout()
        
        # Botón de cerrar
        self.close_btn = QPushButton("❌ Cerrar")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C757D;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #5A6268; }
        """)
        footer_layout.addWidget(self.close_btn)
        
        footer_layout.addStretch()
        
        # Botón de guardar
        self.save_btn = QPushButton("💾 Guardar")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #17A2B8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #138496; }
        """)
        footer_layout.addWidget(self.save_btn)
        
        # Botón de pagar
        self.pay_btn = QPushButton("💳 Pagar")
        self.pay_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #218838; }
            QPushButton:disabled { 
                background-color: #6C757D; 
                color: #ADB5BD; 
            }
        """)
        footer_layout.addWidget(self.pay_btn)
        
        parent_layout.addLayout(footer_layout)
    
    def apply_styles(self):
        """Aplica estilos generales al diálogo"""
        self.setStyleSheet("""
            QDialog {
                background-color: #FFFFFF;
            }
        """)
    
    def connect_signals(self):
        """Conecta las señales de los widgets"""
        # Controles de productos
        self.categoria_combo.currentTextChanged.connect(self.load_productos)
        self.add_producto_btn.clicked.connect(self.add_selected_producto)
        self.productos_table.itemDoubleClicked.connect(self.add_selected_producto)
        
        # Controles de comanda
        self.remove_linea_btn.clicked.connect(self.remove_selected_linea)
        self.edit_cantidad_btn.clicked.connect(self.edit_selected_cantidad)
        
        # Botones principales
        self.close_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.save_comanda)
        self.pay_btn.clicked.connect(self.process_payment)
        
        # Señales del controlador
        self.controller.comanda_updated.connect(self.on_comanda_updated)
        self.controller.error_occurred.connect(self.show_error)
        self.controller.status_changed.connect(self.update_status)
    
    def load_initial_data(self):
        """Carga los datos iniciales"""
        # Cargar categorías
        categorias = self.controller.get_categorias()
        self.categoria_combo.addItem("Todas")
        self.categoria_combo.addItems(categorias)
        
        # Cargar productos iniciales
        self.load_productos("Todas")
        
        # Abrir mesa en el controlador
        self.current_comanda = self.controller.open_mesa(self.mesa.id)
        if self.current_comanda:
            self.update_comanda_display()
        
        # Actualizar estado de botones
        self.update_button_states()
    
    def load_productos(self, categoria: str):
        """Carga los productos de una categoría"""
        self.productos_cache = self.controller.get_productos_by_categoria(categoria)
        self.update_productos_table()
    
    def update_productos_table(self):
        """Actualiza la tabla de productos"""
        self.productos_table.setRowCount(len(self.productos_cache))
        
        for row, producto in enumerate(self.productos_cache):
            # Nombre del producto
            nombre_item = QTableWidgetItem(producto.nombre)
            nombre_item.setData(Qt.ItemDataRole.UserRole, producto.id)
            self.productos_table.setItem(row, 0, nombre_item)
            
            # Precio
            precio_item = QTableWidgetItem(f"{producto.precio:.2f} €")
            precio_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.productos_table.setItem(row, 1, precio_item)
            
            # Stock
            stock_text = str(producto.stock_actual) if producto.stock_actual is not None else "N/A"
            stock_item = QTableWidgetItem(stock_text)
            stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.productos_table.setItem(row, 2, stock_item)
    
    def add_selected_producto(self):
        """Añade el producto seleccionado a la comanda"""
        current_row = self.productos_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selección requerida", "Por favor, seleccione un producto.")
            return
        
        producto_item = self.productos_table.item(current_row, 0)
        if not producto_item:
            return
        
        producto_id = producto_item.data(Qt.ItemDataRole.UserRole)
        cantidad = self.cantidad_spin.value()
        
        if self.controller.add_product_to_order(self.mesa.id, producto_id, cantidad):
            self.cantidad_spin.setValue(1)  # Reset cantidad
    
    def on_comanda_updated(self, comanda: Comanda):
        """Actualiza la visualización cuando se actualiza la comanda"""
        self.current_comanda = comanda
        self.update_comanda_display()
        self.update_button_states()
    
    def update_comanda_display(self):
        """Actualiza la visualización de la comanda"""
        if not self.current_comanda:
            self.comanda_table.setRowCount(0)
            self.total_label.setText("Total: 0.00 €")
            return
        
        # Actualizar tabla
        self.comanda_table.setRowCount(len(self.current_comanda.lineas))
        
        for row, linea in enumerate(self.current_comanda.lineas):
            # Producto
            producto_item = QTableWidgetItem(linea.producto_nombre)
            producto_item.setData(Qt.ItemDataRole.UserRole, linea.producto_id)
            self.comanda_table.setItem(row, 0, producto_item)
            
            # Precio unitario
            precio_item = QTableWidgetItem(f"{linea.precio_unidad:.2f} €")
            precio_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.comanda_table.setItem(row, 1, precio_item)
            
            # Cantidad
            cantidad_item = QTableWidgetItem(str(linea.cantidad))
            cantidad_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.comanda_table.setItem(row, 2, cantidad_item)
              # Total línea
            total_item = QTableWidgetItem(f"{linea.total:.2f} €")
            total_item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.comanda_table.setItem(row, 3, total_item)
        
        # Actualizar total
        total = self.controller.get_order_total(self.mesa.id)
        self.total_label.setText(f"Total: {total:.2f} €")
        
        # Actualizar estado
        if self.current_comanda:
            estado_text = f"Estado: {self.current_comanda.estado.title()}"
            if hasattr(self.current_comanda, 'fecha_apertura'):
                estado_text += f" | Apertura: {self.current_comanda.fecha_apertura.strftime('%H:%M')}"
            self.comanda_status.setText(estado_text)
    
    def update_button_states(self):
        """Actualiza el estado de los botones según el contexto"""
        has_comanda = self.current_comanda is not None
        has_items = False
        
        if has_comanda and self.current_comanda is not None:
            if hasattr(self.current_comanda, 'lineas') and self.current_comanda.lineas:
                has_items = len(self.current_comanda.lineas) > 0
                
        has_selection = self.comanda_table.currentRow() >= 0
        
        self.add_producto_btn.setEnabled(has_comanda)
        self.remove_linea_btn.setEnabled(has_items and has_selection)
        self.edit_cantidad_btn.setEnabled(has_items and has_selection)
        self.save_btn.setEnabled(has_items)
        self.pay_btn.setEnabled(has_items)
    
    def remove_selected_linea(self):
        """Elimina la línea seleccionada de la comanda"""
        current_row = self.comanda_table.currentRow()
        if current_row < 0:
            return
        
        producto_item = self.comanda_table.item(current_row, 0)
        if not producto_item:
            return
        
        producto_id = producto_item.data(Qt.ItemDataRole.UserRole)
        
        if QMessageBox.question(
            self, "Confirmar eliminación",
            "¿Está seguro de eliminar este producto de la comanda?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self.controller.remove_product_from_order(self.mesa.id, producto_id)
    
    def edit_selected_cantidad(self):
        """Edita la cantidad del producto seleccionado"""
        current_row = self.comanda_table.currentRow()
        if current_row < 0:
            return
        
        producto_item = self.comanda_table.item(current_row, 0)
        cantidad_item = self.comanda_table.item(current_row, 2)
        
        if not producto_item or not cantidad_item:
            return
        
        producto_id = producto_item.data(Qt.ItemDataRole.UserRole)
        cantidad_actual = int(cantidad_item.text())
        
        # Diálogo simple para nueva cantidad
        nueva_cantidad, ok = QSpinBox().value(), True  # Simplificado por ahora
        if ok and nueva_cantidad > 0:
            self.controller.update_product_quantity(self.mesa.id, producto_id, nueva_cantidad)
    
    def save_comanda(self):
        """Guarda la comanda actual"""
        if self.controller.save_order(self.mesa.id):
            self.comanda_saved.emit(self.current_comanda.id if self.current_comanda else 0)
            QMessageBox.information(self, "Éxito", "Comanda guardada correctamente.")
    
    def process_payment(self):
        """Procesa el pago de la comanda"""
        if not self.current_comanda or not self.current_comanda.lineas:
            return
        
        total = self.controller.get_order_total(self.mesa.id)
        
        if QMessageBox.question(
            self, "Confirmar pago",
            f"¿Procesar pago de {total:.2f} €?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            
            if self.controller.process_payment(self.mesa.id, {"total": total}):
                self.payment_processed.emit(self.mesa.id, total)
                QMessageBox.information(self, "Pago exitoso", "El pago ha sido procesado correctamente.")
                self.accept()
    
    def show_error(self, message: str):
        """Muestra un mensaje de error"""
        QMessageBox.critical(self, "Error", message)
    
    def update_status(self, status: str):
        """Actualiza el estado mostrado"""
        # Aquí se podría mostrar el estado en una barra de estado
        pass
    
    def _auto_save(self):
        """Auto-guarda la comanda si hay cambios"""
        if self.current_comanda and self.current_comanda.lineas:
            self.controller.save_order(self.mesa.id)
    
    def closeEvent(self, event):
        """Maneja el cierre del diálogo"""
        self.auto_save_timer.stop()
        super().closeEvent(event)
