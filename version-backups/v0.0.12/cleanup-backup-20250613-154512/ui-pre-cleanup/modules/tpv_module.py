"""
Módulo TPV (Terminal Punto de Venta) para la aplicación Hefest.
"""

import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
                            QTableWidgetItem, QHeaderView, QLabel, QSplitter, QFrame,
                            QDialog, QFormLayout, QComboBox, QSpinBox, QDoubleSpinBox,
                            QMessageBox, QGridLayout, QTabWidget, QLineEdit, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon, QFont

from .base_module import BaseModule
from services.tpv_service import TPVService, Mesa, Comanda, LineaComanda, Producto

logger = logging.getLogger(__name__)

class MesaDialog(QDialog):
    """Diálogo para gestionar una mesa"""
    
    def __init__(self, mesa: Mesa, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.tpv_service = TPVService()
        self.comanda = None
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Configura la interfaz de usuario del diálogo"""
        self.setWindowTitle(f"Mesa {self.mesa.numero} - {self.mesa.zona}")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Información de la mesa
        info_layout = QHBoxLayout()
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.Shape.StyledPanel)
        info_frame_layout = QFormLayout(info_frame)
        
        self.estado_label = QLabel(self.mesa.estado.capitalize())
        self.capacidad_label = QLabel(str(self.mesa.capacidad))
        
        info_frame_layout.addRow("Estado:", self.estado_label)
        info_frame_layout.addRow("Capacidad:", self.capacidad_label)
        
        info_layout.addWidget(info_frame)
        info_layout.addStretch()
        layout.addLayout(info_layout)
        
        # Separador principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(splitter, stretch=1)
        
        # Productos disponibles
        productos_widget = QWidget()
        productos_layout = QVBoxLayout(productos_widget)
        productos_layout.setContentsMargins(0, 0, 0, 0)
        
        productos_label = QLabel("Productos")
        productos_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        productos_layout.addWidget(productos_label)
        
        # Categorias de productos
        self.categoria_combo = QComboBox()
        self.categoria_combo.currentTextChanged.connect(self.filtrar_productos)
        productos_layout.addWidget(self.categoria_combo)
        
        # Tabla de productos
        self.productos_table = QTableWidget()
        self.productos_table.setColumnCount(3)
        self.productos_table.setHorizontalHeaderLabels(["Nombre", "Precio", "Stock"])
        header = self.productos_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.productos_table.doubleClicked.connect(self.agregar_producto)
        productos_layout.addWidget(self.productos_table)
        
        # Botones de acción para productos
        productos_buttons_layout = QHBoxLayout()
        self.agregar_btn = QPushButton("Añadir a comanda")
        self.agregar_btn.clicked.connect(self.agregar_producto)
        productos_buttons_layout.addWidget(self.agregar_btn)
        productos_layout.addLayout(productos_buttons_layout)
        
        splitter.addWidget(productos_widget)
        
        # Comanda actual
        comanda_widget = QWidget()
        comanda_layout = QVBoxLayout(comanda_widget)
        comanda_layout.setContentsMargins(0, 0, 0, 0)
        
        comanda_label = QLabel("Comanda actual")
        comanda_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        comanda_layout.addWidget(comanda_label)
        
        # Tabla de la comanda
        self.comanda_table = QTableWidget()
        self.comanda_table.setColumnCount(4)
        self.comanda_table.setHorizontalHeaderLabels(["Producto", "Precio", "Cantidad", "Total"])
        header = self.comanda_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        comanda_layout.addWidget(self.comanda_table)
        
        # Resumen y acciones de comanda
        resumen_layout = QHBoxLayout()
        self.total_label = QLabel("Total: 0.00 €")
        self.total_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        resumen_layout.addWidget(self.total_label)
        resumen_layout.addStretch()
        
        self.eliminar_btn = QPushButton("Eliminar línea")
        self.eliminar_btn.clicked.connect(self.eliminar_linea)
        resumen_layout.addWidget(self.eliminar_btn)
        
        self.cantidad_btn = QPushButton("Cambiar cantidad")
        self.cantidad_btn.clicked.connect(self.cambiar_cantidad)
        resumen_layout.addWidget(self.cantidad_btn)
        
        comanda_layout.addLayout(resumen_layout)
        
        # Botones finales
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.cerrar_btn = QPushButton("Cerrar")
        self.cerrar_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(self.cerrar_btn)
        
        self.guardar_btn = QPushButton("Guardar comanda")
        self.guardar_btn.setDefault(True)
        self.guardar_btn.clicked.connect(self.guardar_comanda)
        buttons_layout.addWidget(self.guardar_btn)
        
        self.pagar_btn = QPushButton("Pagar")
        self.pagar_btn.clicked.connect(self.pagar_comanda)
        buttons_layout.addWidget(self.pagar_btn)
        
        splitter.addWidget(comanda_widget)
        
        layout.addLayout(buttons_layout)
        
        # Configurar tamaño del splitter
        splitter.setSizes([int(self.width() * 0.4), int(self.width() * 0.6)])
        
    def load_data(self):
        """Carga los datos iniciales"""
        # Cargar categorías de productos
        categorias = self.tpv_service.get_categorias_productos()
        self.categoria_combo.addItem("Todas")
        self.categoria_combo.addItems(categorias)
        
        # Cargar todos los productos
        self.cargar_productos("Todas")
        
        # Cargar comanda actual si existe
        self.comanda = self.tpv_service.get_comanda_activa(self.mesa.id)
        if self.comanda:
            self.cargar_comanda()
        else:
            # Crear nueva comanda
            self.comanda = self.tpv_service.crear_comanda(self.mesa.id)
            
    def filtrar_productos(self, categoria):
        """Filtra los productos por categoría"""
        self.cargar_productos(categoria)
        
    def cargar_productos(self, categoria):
        """Carga los productos en la tabla"""
        if categoria == "Todas":
            productos = self.tpv_service.get_todos_productos()
        else:
            productos = self.tpv_service.get_productos_por_categoria(categoria)
            
        self.productos_table.setRowCount(0)
        for producto in productos:
            row = self.productos_table.rowCount()
            self.productos_table.insertRow(row)
            
            self.productos_table.setItem(row, 0, QTableWidgetItem(producto.nombre))
            self.productos_table.setItem(row, 1, QTableWidgetItem(f"{producto.precio:.2f} €"))
            
            stock_item = QTableWidgetItem(str(producto.stock_actual) if producto.stock_actual is not None else "N/A")
            self.productos_table.setItem(row, 2, stock_item)
            
            # Guardar el ID del producto como dato de usuario
            item = self.productos_table.item(row, 0)
            if item:
                item.setData(Qt.ItemDataRole.UserRole, producto.id)
            
    def cargar_comanda(self):
        """Carga la comanda actual en la tabla"""
        self.comanda_table.setRowCount(0)
        if not self.comanda or not self.comanda.lineas:
            self.actualizar_total()
            return
            
        for linea in self.comanda.lineas:
            row = self.comanda_table.rowCount()
            self.comanda_table.insertRow(row)
            
            self.comanda_table.setItem(row, 0, QTableWidgetItem(linea.producto_nombre))
            self.comanda_table.setItem(row, 1, QTableWidgetItem(f"{linea.precio_unidad:.2f} €"))
            self.comanda_table.setItem(row, 2, QTableWidgetItem(str(linea.cantidad)))
            self.comanda_table.setItem(row, 3, QTableWidgetItem(f"{linea.total:.2f} €"))
            
            # Guardar ID del producto como dato de usuario
            item = self.comanda_table.item(row, 0)
            if item:
                item.setData(Qt.ItemDataRole.UserRole, linea.producto_id)
              
        self.actualizar_total()
        
    def actualizar_total(self):
        """Actualiza el total de la comanda"""
        total = sum(linea.total for linea in self.comanda.lineas) if self.comanda and self.comanda.lineas else 0
        self.total_label.setText(f"Total: {total:.2f} €")
        
    def agregar_producto(self):
        """Añade un producto a la comanda"""
        current_row = self.productos_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selección requerida", "Por favor, seleccione un producto primero.")
            return
            
        item = self.productos_table.item(current_row, 0)
        if not item:
            QMessageBox.warning(self, "Error", "No se pudo obtener la información del producto.")
            return
            
        producto_id = item.data(Qt.ItemDataRole.UserRole)
        producto_nombre = item.text()
        
        if not self.comanda or not hasattr(self.comanda, 'id') or self.comanda.id is None:
            QMessageBox.critical(self, "Error", "No hay una comanda activa.")
            return
        
        # Obtener detalles del producto
        producto = self.tpv_service.get_producto_por_id(producto_id)
        if not producto:
            QMessageBox.critical(self, "Error", "No se pudo encontrar el producto seleccionado.")
            return
        
        # Diálogo para cantidad
        cantidad_dialog = QDialog(self)
        cantidad_dialog.setWindowTitle("Cantidad")
        dialog_layout = QFormLayout(cantidad_dialog)
        
        cantidad_spin = QSpinBox()
        cantidad_spin.setMinimum(1)
        cantidad_spin.setMaximum(99)
        cantidad_spin.setValue(1)
        
        dialog_layout.addRow(f"Cantidad de {producto_nombre}:", cantidad_spin)
        
        buttons_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(cantidad_dialog.reject)
        add_btn = QPushButton("Añadir")
        add_btn.clicked.connect(cantidad_dialog.accept)
        add_btn.setDefault(True)
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(add_btn)
        dialog_layout.addRow("", buttons_layout)
        
        if cantidad_dialog.exec():
            cantidad = cantidad_spin.value()
            self.tpv_service.agregar_producto_a_comanda(
                self.comanda.id, 
                producto.id,
                producto.nombre,
                producto.precio,
                cantidad
            )
            
            # Recargar la comanda
            if hasattr(self.comanda, 'id') and self.comanda.id is not None:
                self.comanda = self.tpv_service.get_comanda_por_id(self.comanda.id)
                self.cargar_comanda()
            
    def eliminar_linea(self):
        """Elimina una línea de la comanda"""
        current_row = self.comanda_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selección requerida", "Por favor, seleccione una línea primero.")
            return
            
        item = self.comanda_table.item(current_row, 0)
        if not item:
            QMessageBox.warning(self, "Error", "No se pudo obtener la información del producto.")
            return
            
        if not self.comanda or not hasattr(self.comanda, 'id') or self.comanda.id is None:
            QMessageBox.critical(self, "Error", "No hay una comanda activa.")
            return
            
        producto_id = item.data(Qt.ItemDataRole.UserRole)
        
        if QMessageBox.question(self, "Confirmar eliminación", 
                                "¿Está seguro de eliminar este ítem de la comanda?",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.tpv_service.eliminar_producto_de_comanda(self.comanda.id, producto_id)
            
            # Recargar la comanda
            if hasattr(self.comanda, 'id') and self.comanda.id is not None:
                self.comanda = self.tpv_service.get_comanda_por_id(self.comanda.id)
                self.cargar_comanda()
            
    def cambiar_cantidad(self):
        """Cambia la cantidad de un producto en la comanda"""
        current_row = self.comanda_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selección requerida", "Por favor, seleccione una línea primero.")
            return
            
        item_producto = self.comanda_table.item(current_row, 0)
        item_cantidad = self.comanda_table.item(current_row, 2)
        
        if not item_producto or not item_cantidad:
            QMessageBox.warning(self, "Error", "No se pudo obtener la información del producto.")
            return
            
        if not self.comanda or not hasattr(self.comanda, 'id') or self.comanda.id is None:
            QMessageBox.critical(self, "Error", "No hay una comanda activa.")
            return
            
        producto_id = item_producto.data(Qt.ItemDataRole.UserRole)
        producto_nombre = item_producto.text()
        cantidad_actual = int(item_cantidad.text())
        
        # Diálogo para cantidad
        cantidad_dialog = QDialog(self)
        cantidad_dialog.setWindowTitle("Cambiar cantidad")
        dialog_layout = QFormLayout(cantidad_dialog)
        
        cantidad_spin = QSpinBox()
        cantidad_spin.setMinimum(1)
        cantidad_spin.setMaximum(99)
        cantidad_spin.setValue(cantidad_actual)
        
        dialog_layout.addRow(f"Nueva cantidad de {producto_nombre}:", cantidad_spin)
        
        buttons_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(cantidad_dialog.reject)
        change_btn = QPushButton("Cambiar")
        change_btn.clicked.connect(cantidad_dialog.accept)
        change_btn.setDefault(True)
        
        buttons_layout.addWidget(cancel_btn)
        buttons_layout.addWidget(change_btn)
        dialog_layout.addRow("", buttons_layout)
        
        if cantidad_dialog.exec():
            nueva_cantidad = cantidad_spin.value()
            self.tpv_service.cambiar_cantidad_producto(self.comanda.id, producto_id, nueva_cantidad)
            
            # Recargar la comanda
            if hasattr(self.comanda, 'id') and self.comanda.id is not None:
                self.comanda = self.tpv_service.get_comanda_por_id(self.comanda.id)
                self.cargar_comanda()
            
    def guardar_comanda(self):
        """Guarda la comanda actual"""
        if not self.comanda or not self.comanda.lineas:
            QMessageBox.warning(self, "Comanda vacía", "La comanda está vacía. No hay nada que guardar.")
            return
            
        if not hasattr(self.comanda, 'id') or self.comanda.id is None:
            QMessageBox.critical(self, "Error", "No hay una comanda activa válida.")
            return
            
        try:
            self.tpv_service.guardar_comanda(self.comanda.id)
            QMessageBox.information(self, "Comanda guardada", "La comanda ha sido guardada correctamente.")
            self.accept()
        except Exception as e:
            logger.error(f"Error al guardar comanda: {e}")
            QMessageBox.critical(self, "Error", f"No se pudo guardar la comanda: {str(e)}")
            
    def pagar_comanda(self):
        """Gestiona el pago de la comanda"""
        if not self.comanda or not self.comanda.lineas:
            QMessageBox.warning(self, "Comanda vacía", "La comanda está vacía. No hay nada que pagar.")
            return
            
        if not hasattr(self.comanda, 'id') or self.comanda.id is None:
            QMessageBox.critical(self, "Error", "No hay una comanda activa válida.")
            return
            
        # En una implementación real, aquí abriríamos un diálogo de pago
        # Por ahora, simplemente marcamos como pagada
        if QMessageBox.question(self, "Confirmar pago", 
                               f"¿Confirmar el pago de {self.total_label.text()}?",
                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            try:
                self.tpv_service.pagar_comanda(self.comanda.id)
                QMessageBox.information(self, "Pago exitoso", "La comanda ha sido pagada correctamente.")
                # Liberar la mesa
                self.tpv_service.liberar_mesa(self.mesa.id)
                self.accept()
            except Exception as e:
                logger.error(f"Error al pagar comanda: {e}")
                QMessageBox.critical(self, "Error", f"No se pudo procesar el pago: {str(e)}")


class TPVTab(BaseModule):
    """Módulo de TPV (Terminal Punto de Venta)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tpv_service = TPVService()
        self.setup_ui()
        
    def create_module_header(self):
        """Crea el header del módulo TPV"""
        header = QFrame()
        header.setObjectName("module-header")
        header.setStyleSheet("QFrame#module-header { background-color: #3182CE; color: white; }")
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Terminal Punto de Venta (TPV)")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Botones de acción
        refresh_btn = QPushButton()
        refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_btn.setToolTip("Actualizar")
        refresh_btn.clicked.connect(self.refresh)
        header_layout.addWidget(refresh_btn)
        
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar")
        self.search_input.textChanged.connect(self.filter_mesas)
        search_layout.addWidget(self.search_input)
        
        self.filtro_combo = QComboBox()
        self.filtro_combo.addItems(["Todas", "Libres", "Ocupadas"])
        self.filtro_combo.currentTextChanged.connect(self.filter_mesas)
        search_layout.addWidget(self.filtro_combo)
        
        header_layout.addLayout(search_layout)
        
        return header
        
    def setup_ui(self):
        """Configura la interfaz específica del módulo TPV"""
        # Pestañas principales
        self.tabs = QTabWidget()
        self.content_layout.addWidget(self.tabs)
        
        # Pestaña de mesas
        self.tab_mesas = QWidget()
        self.tabs.addTab(self.tab_mesas, "Mesas")
        
        tab_mesas_layout = QVBoxLayout(self.tab_mesas)
        
        # Grid de mesas
        self.mesas_grid = QGridLayout()
        self.mesas_grid.setSpacing(10)
        
        # Scroll area para el grid de mesas
        scroll_area = QWidget()
        scroll_area.setLayout(self.mesas_grid)
        tab_mesas_layout.addWidget(scroll_area)
        
        # Pestaña de comandas
        self.tab_comandas = QWidget()
        self.tabs.addTab(self.tab_comandas, "Comandas")
        
        tab_comandas_layout = QVBoxLayout(self.tab_comandas)
        
        # Tabla de comandas
        self.comandas_table = QTableWidget()
        self.comandas_table.setColumnCount(5)
        self.comandas_table.setHorizontalHeaderLabels(["Mesa", "Apertura", "Estado", "Items", "Total"])
        header = self.comandas_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.comandas_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.comandas_table.doubleClicked.connect(self.ver_comanda)
        tab_comandas_layout.addWidget(self.comandas_table)
        
        # Botones de acción para comandas
        comandas_buttons = QHBoxLayout()
        self.ver_btn = QPushButton("Ver comanda")
        self.ver_btn.clicked.connect(self.ver_comanda)
        comandas_buttons.addWidget(self.ver_btn)
        
        self.imprimir_btn = QPushButton("Imprimir comanda")
        self.imprimir_btn.clicked.connect(self.imprimir_comanda)
        comandas_buttons.addWidget(self.imprimir_btn)
        
        comandas_buttons.addStretch()
        tab_comandas_layout.addLayout(comandas_buttons)
        
    def on_module_activated(self):
        """Se llama cuando el módulo se activa"""
        super().on_module_activated()
        self.refresh()
        
    def on_module_deactivated(self):
        """Se llama cuando el módulo se desactiva"""
        super().on_module_deactivated()
        # Liberar recursos si es necesario
        
    def refresh(self):
        """Actualiza los datos del módulo"""
        self.cargar_mesas()
        self.cargar_comandas()
        
    def cargar_mesas(self):
        """Carga el grid de mesas desde el servicio"""        # Limpiar grid
        while self.mesas_grid.count():
            item = self.mesas_grid.takeAt(0)
            if item:
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                
        # Obtener mesas
        try:
            mesas = self.tpv_service.get_todas_mesas()
            
            # Filtrar si es necesario
            filtro_texto = self.search_input.text().lower()
            filtro_estado = self.filtro_combo.currentText()
            
            mesas_filtradas = []
            for mesa in mesas:
                # Filtrar por texto
                if filtro_texto and filtro_texto not in mesa.numero.lower() and filtro_texto not in mesa.zona.lower():
                    continue
                    
                # Filtrar por estado
                if filtro_estado == "Libres" and mesa.estado != "libre":
                    continue
                if filtro_estado == "Ocupadas" and mesa.estado != "ocupada":
                    continue
                    
                mesas_filtradas.append(mesa)
            
            # Mostrar mesas filtradas
            row, col = 0, 0
            for mesa in mesas_filtradas:
                mesa_widget = QPushButton(f"Mesa {mesa.numero}\n{mesa.zona}")
                mesa_widget.setMinimumSize(120, 80)
                
                # Estilo según estado
                if mesa.estado == "libre":
                    mesa_widget.setStyleSheet("background-color: #48BB78; color: white;")
                elif mesa.estado == "ocupada":
                    mesa_widget.setStyleSheet("background-color: #F56565; color: white;")
                else:
                    mesa_widget.setStyleSheet("background-color: #ECC94B; color: white;")
                
                # Guardar ID de mesa como propiedad
                mesa_widget.setProperty("mesa_id", mesa.id)
                
                # Conectar señal de clic
                mesa_widget.clicked.connect(lambda _, m=mesa: self.abrir_mesa(m))
                
                self.mesas_grid.addWidget(mesa_widget, row, col)
                
                col += 1
                if col >= 5:  # 5 columnas
                    col = 0
                    row += 1
                    
            # Mensaje si no hay mesas
            if not mesas_filtradas:
                no_mesas_label = QLabel("No se encontraron mesas con los filtros seleccionados")
                no_mesas_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                no_mesas_label.setStyleSheet("font-size: 14px; color: #718096;")
                self.mesas_grid.addWidget(no_mesas_label, 0, 0, 1, 5)
                
        except Exception as e:
            logger.error(f"Error al cargar mesas: {e}")
            error_label = QLabel(f"Error al cargar mesas: {str(e)}")
            error_label.setStyleSheet("color: red;")
            self.mesas_grid.addWidget(error_label, 0, 0)
            
    def filter_mesas(self):
        """Filtra las mesas según los criterios seleccionados"""
        self.cargar_mesas()
        
    def abrir_mesa(self, mesa):
        """Abre el diálogo de gestión de una mesa"""
        dialog = MesaDialog(mesa, self)
        if dialog.exec():
            # Refrescar datos si se hizo algún cambio
            self.refresh()
            
    def cargar_comandas(self):
        """Carga las comandas en la tabla"""
        self.comandas_table.setRowCount(0)
        
        try:
            comandas = self.tpv_service.get_comandas_activas()
            
            for comanda in comandas:
                row = self.comandas_table.rowCount()
                self.comandas_table.insertRow(row)
                
                # Obtener info de la mesa
                mesa = self.tpv_service.get_mesa_por_id(comanda.mesa_id)
                mesa_nombre = f"Mesa {mesa.numero}" if mesa else f"Mesa {comanda.mesa_id}"
                
                # Calcular total
                total = sum(linea.total for linea in comanda.lineas) if comanda.lineas else 0
                
                self.comandas_table.setItem(row, 0, QTableWidgetItem(mesa_nombre))
                self.comandas_table.setItem(row, 1, QTableWidgetItem(comanda.fecha_apertura.strftime("%H:%M:%S")))
                self.comandas_table.setItem(row, 2, QTableWidgetItem(comanda.estado.capitalize()))
                self.comandas_table.setItem(row, 3, QTableWidgetItem(str(len(comanda.lineas))))
                self.comandas_table.setItem(row, 4, QTableWidgetItem(f"{total:.2f} €"))
                
                # Guardar ID de comanda como dato de usuario
                item = self.comandas_table.item(row, 0)
                if item:
                    item.setData(Qt.ItemDataRole.UserRole, comanda.id)
                
        except Exception as e:
            logger.error(f"Error al cargar comandas: {e}")
            self.status_changed.emit(f"Error al cargar comandas: {str(e)}")
            
    def ver_comanda(self):
        """Muestra los detalles de una comanda seleccionada"""
        current_row = self.comandas_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selección requerida", "Por favor, seleccione una comanda primero.")
            return
            
        item = self.comandas_table.item(current_row, 0)
        if not item:
            QMessageBox.warning(self, "Error", "No se pudo obtener la información de la comanda.")
            return
            
        comanda_id = item.data(Qt.ItemDataRole.UserRole)
        comanda = self.tpv_service.get_comanda_por_id(comanda_id)
        
        if not comanda:
            QMessageBox.critical(self, "Error", "No se pudo encontrar la comanda seleccionada.")
            return
            
        mesa = self.tpv_service.get_mesa_por_id(comanda.mesa_id)
        if mesa:
            self.abrir_mesa(mesa)
            
    def imprimir_comanda(self):
        """Imprime la comanda seleccionada"""
        current_row = self.comandas_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Selección requerida", "Por favor, seleccione una comanda primero.")
            return
            
        item = self.comandas_table.item(current_row, 0)
        if not item:
            QMessageBox.warning(self, "Error", "No se pudo obtener la información de la comanda.")
            return
            
        comanda_id = item.data(Qt.ItemDataRole.UserRole)
        
        # En una implementación real, aquí integraríamos con un sistema de impresión
        QMessageBox.information(self, "Impresión simulada", 
                              f"Imprimiendo comanda #{comanda_id}.\n\n"
                              "En una implementación real, esta funcionalidad enviaría "
                              "la comanda a la impresora de pedidos o TPV física.")