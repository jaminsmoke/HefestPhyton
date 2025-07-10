# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
from PyQt6.QtGui import QFont, QIcon, QColor
from .base_module import BaseModule
from services.inventario_service import InventarioService, Producto, Proveedor

"""
Módulo de Inventario para la aplicación Hefest.
"""

                            QTableWidgetItem, QHeaderView, QLineEdit, QComboBox, QLabel,
                            QDialog, QFormLayout, QDoubleSpinBox, QSpinBox, QMessageBox,
                            QTabWidget, QFrame, QGridLayout, QProgressBar)


_ = logging.getLogger(__name__)

class ProductoDialog(QDialog):
    """Diálogo para crear o editar un producto"""
    def __init__(self, producto=None, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.producto = producto  # None si es nuevo, dict si es edición
        self.init_ui()
        
    def init_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicializa la interfaz de usuario del diálogo"""
        if self.producto:
            self.setWindowTitle(f"Editar Producto: {self.producto['nombre']}")
        else:
            self.setWindowTitle("Nuevo Producto")
            
        self.setMinimumWidth(400)
        
        _ = QVBoxLayout()
        
        # Formulario
        _ = QFormLayout()
        
        # Nombre
        self.nombre_input = QLineEdit()
        if self.producto:
            self.nombre_input.setText(self.producto["nombre"])
        form_layout.addRow("Nombre:", self.nombre_input)
        
        # Categoría
        self.categoria_combo = QComboBox()
        categorias = ["Bebidas", "Entrantes", "Platos Principales", "Postres", "Menú del día", "Limpieza", "Otros"]
        self.categoria_combo.addItems(categorias)
        if self.producto and "categoria" in self.producto:
            index = self.categoria_combo.findText(self.producto["categoria"])
            if index >= 0:
                self.categoria_combo.setCurrentIndex(index)
        form_layout.addRow("Categoría:", self.categoria_combo)
        
        # Precio
        self.precio_spin = QDoubleSpinBox()
        self.precio_spin.setRange(0, 999.99)
        self.precio_spin.setDecimals(2)
        self.precio_spin.setSuffix(" €")
        if self.producto and "precio" in self.producto:
            self.precio_spin.setValue(self.producto["precio"])
        form_layout.addRow("Precio:", self.precio_spin)
        
        # Stock actual
        self.stock_spin = QSpinBox()
        self.stock_spin.setRange(0, 9999)
        if self.producto and "stock" in self.producto:
            self.stock_spin.setValue(self.producto["stock"])
        form_layout.addRow("Stock actual:", self.stock_spin)
        
        # Stock mínimo
        self.stock_min_spin = QSpinBox()
        self.stock_min_spin.setRange(0, 9999)
        if self.producto and "stock_min" in self.producto:
            self.stock_min_spin.setValue(self.producto["stock_min"])
        form_layout.addRow("Stock mínimo:", self.stock_min_spin)
        
        # Proveedor
        self.proveedor_combo = QComboBox()
        proveedores = ["Distribuciones García", "Cafés del mundo", "Alimentos Básicos SL", "Otro"]
        self.proveedor_combo.addItems(proveedores)
        if self.producto and "proveedor" in self.producto:
            index = self.proveedor_combo.findText(self.producto["proveedor"])
            if index >= 0:
                self.proveedor_combo.setCurrentIndex(index)
        form_layout.addRow("Proveedor:", self.proveedor_combo)
        
        layout.addLayout(form_layout)
        
        # Botones
        _ = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.save_btn = QPushButton("Guardar")
        self.save_btn.clicked.connect(self.accept)
        self.save_btn.setDefault(True)
        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def get_producto_data(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna los datos del formulario como un diccionario"""
        _ = {
            "nombre": self.nombre_input.text(),
            "categoria": self.categoria_combo.currentText(),
            "precio": self.precio_spin.value(),
            "stock": self.stock_spin.value(),
            "stock_min": self.stock_min_spin.value(),
            "proveedor": self.proveedor_combo.currentText()
        }
        
        if self.producto and "id" in self.producto:
            producto["id"] = self.producto["id"]
            
        return producto


class InventarioTab(BaseModule):
    """Tab principal para el módulo de inventario"""
    def __init__(self, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.setup_ui()
        self._cargar_datos_prueba()
    
    def create_module_header(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea el header personalizado del módulo de inventario"""
        header = QFrame()
        header.setObjectName("module-header")
        header.setFixedHeight(60)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        
        title = QLabel("Gestión de Inventario")
        title.setObjectName("module-title")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1f2937;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Botón de nuevo producto
        nuevo_btn = QPushButton("Nuevo Producto")
        nuevo_btn.setObjectName("action-button")
        nuevo_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background: #10b981;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                margin-right: 8px;
            }
            QPushButton:hover {
                background: #059669;
            }
        """)
        nuevo_btn.clicked.connect(self._nuevo_producto)
        layout.addWidget(nuevo_btn)
        
        refresh_btn = QPushButton("Actualizar")
        refresh_btn.setObjectName("action-button")
        refresh_btn.setStyleSheet("""
            QPushButton {
                padding: 8px 16px;
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """)
        refresh_btn.clicked.connect(self.refresh)
        layout.addWidget(refresh_btn)
        
        return header
        
    def setup_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicializa la interfaz de usuario del inventario"""
        # Tabs para diferentes vistas
        self.tabs = QTabWidget()
        
        # Panel de productos
        self.vista_productos = QWidget()
        self._init_vista_productos()
        self.tabs.addTab(self.vista_productos, "Productos")
        
        # Panel de alertas de stock
        self.vista_alertas = QWidget()
        self._init_vista_alertas()
        self.tabs.addTab(self.vista_alertas, "Alertas de Stock")
        
        # Panel de proveedores
        self.vista_proveedores = QWidget()
        self._init_vista_proveedores()
        self.tabs.addTab(self.vista_proveedores, "Proveedores")
        
        # Panel de estadísticas
        self.vista_estadisticas = QWidget()
        self._init_vista_estadisticas()
        self.tabs.addTab(self.vista_estadisticas, "Estadísticas")
        
        # Agregar el contenido al layout del BaseModule
        self.content_layout.addWidget(self.tabs)
        
    def _init_vista_productos(self):
        """Inicializa la vista de productos"""
        _ = QVBoxLayout()
        
        # Barra de búsqueda y filtros
        _ = QHBoxLayout()
        
        self.busqueda_input = QLineEdit()
        self.busqueda_input.setPlaceholderText("Buscar producto...")
        busqueda_layout.addWidget(self.busqueda_input)
        
        busqueda_layout.addWidget(QLabel("Categoría:"))
        self.categoria_combo = QComboBox()
        self.categoria_combo.addItem("Todas")
        busqueda_layout.addWidget(self.categoria_combo)
        
        self.buscar_btn = QPushButton("Buscar")
        self.buscar_btn.setStyleSheet("background-color: #2196F3; color: white;")
        busqueda_layout.addWidget(self.buscar_btn)
        
        layout.addLayout(busqueda_layout)
          # Tabla de productos
        self.productos_table = QTableWidget(0, 7)
        self.productos_table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Categoría", "Precio", "Stock", "Mín", "Acciones"]
        )
        header = self.productos_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.productos_table.setColumnWidth(0, 50)  # ID más estrecho
        layout.addWidget(self.productos_table)
        
        # Botones de acción
        _ = QHBoxLayout()
        
        self.nuevo_btn = QPushButton("Nuevo Producto")
        self.nuevo_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        self.nuevo_btn.clicked.connect(self._nuevo_producto)
        acciones_layout.addWidget(self.nuevo_btn)
        
        self.importar_btn = QPushButton("Importar")
        acciones_layout.addWidget(self.importar_btn)
        
        self.exportar_btn = QPushButton("Exportar")
        acciones_layout.addWidget(self.exportar_btn)
        
        layout.addLayout(acciones_layout)
        
        self.vista_productos.setLayout(layout)
        
        # Conectar señales
        self.buscar_btn.clicked.connect(self._buscar_productos)
        
    def _init_vista_alertas(self):
        """Inicializa la vista de alertas de stock"""
        _ = QVBoxLayout()
        
        # Información
        info_label = QLabel("Productos con nivel de stock bajo el mínimo establecido:")
        info_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(info_label)
          # Tabla de alertas
        self.alertas_table = QTableWidget(0, 5)
        self.alertas_table.setHorizontalHeaderLabels(
            ["Nombre", "Stock Actual", "Stock Mínimo", "Proveedor", "Acciones"]
        )
        header = self.alertas_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.alertas_table)
        
        # Botón de pedido automatizado
        pedido_layout = QHBoxLayout()
        pedido_layout.addStretch()
        self.pedido_auto_btn = QPushButton("Generar Pedido Automático")
        self.pedido_auto_btn.setStyleSheet("background-color: #FF9800; color: white;")
        self.pedido_auto_btn.clicked.connect(self._generar_pedido_automatico)
        pedido_layout.addWidget(self.pedido_auto_btn)
        layout.addLayout(pedido_layout)
        
        self.vista_alertas.setLayout(layout)
    
    def _init_vista_proveedores(self):
        """Inicializa la vista de proveedores"""
        _ = QVBoxLayout()
          # Tabla de proveedores
        self.proveedores_table = QTableWidget(0, 5)
        self.proveedores_table.setHorizontalHeaderLabels(
            ["Nombre", "Contacto", "Teléfono", "Email", "Acciones"]
        )
        header = self.proveedores_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.proveedores_table)
        
        # Botones de acción
        _ = QHBoxLayout()
        
        self.nuevo_prov_btn = QPushButton("Nuevo Proveedor")
        self.nuevo_prov_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        acciones_layout.addWidget(self.nuevo_prov_btn)
        
        self.pedido_btn = QPushButton("Realizar Pedido")
        self.pedido_btn.setStyleSheet("background-color: #FF9800; color: white;")
        acciones_layout.addWidget(self.pedido_btn)
        
        layout.addLayout(acciones_layout)
        
        self.vista_proveedores.setLayout(layout)
    
    def _init_vista_estadisticas(self):
        """Inicializa la vista de estadísticas de inventario"""
        _ = QVBoxLayout()
        
        # Gráficos con valores ficticios (sólo para demo)
        # Nivel de stock por categoría
        layout.addWidget(QLabel("Nivel de stock por categoría:"))
        
        _ = ["Bebidas", "Entrantes", "Platos Principales", "Postres", "Limpieza"]
        niveles = [75, 45, 60, 90, 30]  # Porcentajes ficticios
        
        for i, (cat, nivel) in enumerate(zip(categorias, niveles)):
            layout.addWidget(QLabel(f"{cat}:"))
            
            barra = QProgressBar()
            barra.setValue(nivel)
            
            # Color según nivel
            if nivel < 30:
                barra.setStyleSheet("QProgressBar::chunk { background-color: #F44336; }")
            elif nivel < 70:
                barra.setStyleSheet("QProgressBar::chunk { background-color: #FFC107; }")
            else:
                barra.setStyleSheet("QProgressBar::chunk { background-color: #4CAF50; }")
                
            layout.addWidget(barra)
            
        # Más estadísticas
        stats_layout = QGridLayout()
        stats_layout.addWidget(QLabel("Total productos:"), 0, 0)
        stats_layout.addWidget(QLabel("45"), 0, 1)
        stats_layout.addWidget(QLabel("Valor de inventario:"), 1, 0)
        stats_layout.addWidget(QLabel("3,542.75 €"), 1, 1)
        stats_layout.addWidget(QLabel("Productos en alerta:"), 2, 0)
        stats_layout.addWidget(QLabel("8"), 2, 1)
        
        layout.addLayout(stats_layout)
        layout.addStretch()
        
        self.vista_estadisticas.setLayout(layout)
    
    def _cargar_datos_prueba(self):
        """Carga datos de prueba usando el servicio de inventario"""
        # Inicializar el servicio de inventario
        self.inventario_service = InventarioService()
        
        # Cargar categorías
        _ = self.inventario_service.get_categorias()
        self.categoria_combo.clear()
        self.categoria_combo.addItem("Todas")
        self.categoria_combo.addItems(categorias)
        
        # Cargar productos
        self._cargar_productos()
        
        # Cargar alertas
        self._cargar_alertas()
        
        # Cargar proveedores
        self._cargar_proveedores()
        
        # Actualizar estadísticas
        self._actualizar_estadisticas()
        
    def _cargar_productos(self):
        """Carga los productos del servicio en la tabla"""
        # Limpiar tabla
        self.productos_table.setRowCount(0)
        
        # Obtener productos del servicio
        _ = self.inventario_service.get_productos()
        
        # Llenar tabla
        for i, producto in enumerate(productos):
            self.productos_table.insertRow(i)
            
            # Convertir objeto Producto a datos para la tabla
            self.productos_table.setItem(i, 0, QTableWidgetItem(str(producto.id)))
            self.productos_table.setItem(i, 1, QTableWidgetItem(producto.nombre))
            self.productos_table.setItem(i, 2, QTableWidgetItem(producto.categoria))
            self.productos_table.setItem(i, 3, QTableWidgetItem(f"{producto.precio:.2f} €"))
            
            # Stock con color según nivel
            _ = QTableWidgetItem(str(producto.stock_actual))
            if producto.stock_actual <= producto.stock_minimo:
                stock_item.setBackground(QColor(255, 200, 200))  # Rojo claro
            self.productos_table.setItem(i, 4, stock_item)
            
            self.productos_table.setItem(i, 5, QTableWidgetItem(str(producto.stock_minimo)))
            
            # Botones de acción
            _ = QWidget()
            acciones_layout = QHBoxLayout()
            acciones_layout.setContentsMargins(2, 2, 2, 2)
            acciones_layout.setSpacing(2)
            
            editar_btn = QPushButton("Editar")
            editar_btn.setStyleSheet("background-color: #2196F3; color: white;")
            editar_btn.clicked.connect(lambda checked, p=producto: self._editar_producto(p))
            
            eliminar_btn = QPushButton("Eliminar")
            eliminar_btn.setStyleSheet("background-color: #F44336; color: white;")
            eliminar_btn.clicked.connect(lambda checked, p=producto: self._eliminar_producto(p))
            
            acciones_layout.addWidget(editar_btn)
            acciones_layout.addWidget(eliminar_btn)
            acciones_widget.setLayout(acciones_layout)
            
            self.productos_table.setCellWidget(i, 6, acciones_widget)
    
    def _cargar_alertas(self):
        """Carga las alertas de stock bajo mínimo"""
        # Limpiar tabla
        self.alertas_table.setRowCount(0)
        
        # Obtener productos bajo mínimo
        _ = self.inventario_service.get_productos_bajo_minimo()
        
        # Llenar tabla
        for i, alerta in enumerate(alertas):
            self.alertas_table.insertRow(i)
            
            self.alertas_table.setItem(i, 0, QTableWidgetItem(alerta.nombre))
            
            stock_item = QTableWidgetItem(str(alerta.stock_actual))
            stock_item.setBackground(QColor(255, 200, 200))  # Rojo claro
            self.alertas_table.setItem(i, 1, stock_item)
            
            self.alertas_table.setItem(i, 2, QTableWidgetItem(str(alerta.stock_minimo)))
            self.alertas_table.setItem(i, 3, QTableWidgetItem(alerta.proveedor_nombre or "Sin proveedor"))
            
            # Botón de pedir
            pedir_btn = QPushButton("Realizar Pedido")
            pedir_btn.setStyleSheet("background-color: #FF9800; color: white;")
            pedir_btn.clicked.connect(lambda checked, p=alerta: self._realizar_pedido(p))
            self.alertas_table.setCellWidget(i, 4, pedir_btn)
    
    def _cargar_proveedores(self):
        """Carga los proveedores en la tabla"""
        # Limpiar tabla
        self.proveedores_table.setRowCount(0)
        
        # Obtener proveedores del servicio
        _ = self.inventario_service.get_proveedores()
        
        # Llenar tabla
        for i, proveedor in enumerate(proveedores):
            self.proveedores_table.insertRow(i)
            
            self.proveedores_table.setItem(i, 0, QTableWidgetItem(proveedor.nombre))
            self.proveedores_table.setItem(i, 1, QTableWidgetItem(proveedor.contacto))
            self.proveedores_table.setItem(i, 2, QTableWidgetItem(proveedor.telefono))
            self.proveedores_table.setItem(i, 3, QTableWidgetItem(proveedor.email))
            
            # Botones de acción
            _ = QWidget()
            acciones_layout = QHBoxLayout()
            acciones_layout.setContentsMargins(2, 2, 2, 2)
            
            editar_btn = QPushButton("Editar")
            editar_btn.setStyleSheet("background-color: #2196F3; color: white;")
            
            eliminar_btn = QPushButton("Eliminar")
            eliminar_btn.setStyleSheet("background-color: #F44336; color: white;")
            
            acciones_layout.addWidget(editar_btn)
            acciones_layout.addWidget(eliminar_btn)
            acciones_widget.setLayout(acciones_layout)
            
            self.proveedores_table.setCellWidget(i, 4, acciones_widget)
    
    def _actualizar_estadisticas(self):
        """Actualiza los datos estadísticos"""
        # En una implementación real, aquí se actualizarían los gráficos
        # y estadísticas con datos reales desde el servicio
        pass
    
    def _buscar_productos(self):
        """Busca productos según los criterios de búsqueda"""
        _ = self.busqueda_input.text()
        categoria = self.categoria_combo.currentText()
        
        if categoria == "Todas":
            _ = ""
            
        if hasattr(self, 'inventario_service'):
            # Obtener productos filtrados
            _ = self.inventario_service.get_productos(texto, categoria)
            
            # Limpiar y volver a cargar la tabla
            self.productos_table.setRowCount(0)
            
            # Llenar tabla con resultados
            for i, producto in enumerate(productos):
                self.productos_table.insertRow(i)
                
                # Convertir objeto Producto a datos para la tabla
                self.productos_table.setItem(i, 0, QTableWidgetItem(str(producto.id)))
                self.productos_table.setItem(i, 1, QTableWidgetItem(producto.nombre))
                self.productos_table.setItem(i, 2, QTableWidgetItem(producto.categoria))
                self.productos_table.setItem(i, 3, QTableWidgetItem(f"{producto.precio:.2f} €"))
                
                # Stock con color según nivel
                _ = QTableWidgetItem(str(producto.stock_actual))
                if producto.stock_actual <= producto.stock_minimo:
                    stock_item.setBackground(QColor(255, 200, 200))  # Rojo claro
                self.productos_table.setItem(i, 4, stock_item)
                
                self.productos_table.setItem(i, 5, QTableWidgetItem(str(producto.stock_minimo)))
                
                # Botones de acción
                _ = QWidget()
                acciones_layout = QHBoxLayout()
                acciones_layout.setContentsMargins(2, 2, 2, 2)
                
                editar_btn = QPushButton("Editar")
                editar_btn.setStyleSheet("background-color: #2196F3; color: white;")
                editar_btn.clicked.connect(lambda checked, p=producto: self._editar_producto(p))
                
                eliminar_btn = QPushButton("Eliminar")
                eliminar_btn.setStyleSheet("background-color: #F44336; color: white;")
                eliminar_btn.clicked.connect(lambda checked, p=producto: self._eliminar_producto(p))
                
                acciones_layout.addWidget(editar_btn)
                acciones_layout.addWidget(eliminar_btn)
                acciones_widget.setLayout(acciones_layout)
                
                self.productos_table.setCellWidget(i, 6, acciones_widget)
    
    def _nuevo_producto(self):
        """Abre el diálogo para crear un nuevo producto"""
        dialog = ProductoDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            _ = dialog.get_producto_data()
            
            if hasattr(self, 'inventario_service'):
                try:
                    # Convertir dict a objeto Producto
                    _ = Producto(
                        id=None,
                        _ = producto_data["nombre"],
                        categoria=producto_data["categoria"],
                        _ = producto_data["precio"],
                        stock_actual=producto_data["stock"],
                        _ = producto_data["stock_min"],
                        proveedor_nombre=producto_data["proveedor"]
                    )
                    
                    # Usar el servicio para crear el producto
                    self.inventario_service.crear_producto(nuevo_producto)
                    
                    # Recargar datos
                    self._cargar_productos()
                    self._cargar_alertas()
                    
                    self.status_changed.emit(f"Producto '{producto_data['nombre']}' agregado correctamente")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo crear el producto: {str(e)}")
                    logger.error("Error al crear producto: %s", e)
    
    def _editar_producto(self, producto):
        """Abre el diálogo para editar un producto"""
        # Convertir objeto Producto a dict para el diálogo
        _ = {
            "id": producto.id,
            "nombre": producto.nombre,
            "categoria": producto.categoria,
            "precio": producto.precio,
            "stock": producto.stock_actual,
            "stock_min": producto.stock_minimo,
            "proveedor": producto.proveedor_nombre or ""
        }
        
        dialog = ProductoDialog(producto_dict, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            _ = dialog.get_producto_data()
            
            if hasattr(self, 'inventario_service'):
                try:
                    # Convertir dict a objeto Producto
                    _ = Producto(
                        id=producto.id,
                        _ = producto_actualizado["nombre"],
                        categoria=producto_actualizado["categoria"],
                        _ = producto_actualizado["precio"],
                        stock_actual=producto_actualizado["stock"],
                        _ = producto_actualizado["stock_min"],
                        proveedor_nombre=producto_actualizado["proveedor"]
                    )
                    
                    # Usar el servicio para actualizar el producto
                    self.inventario_service.actualizar_producto(producto_obj)
                    
                    # Recargar datos
                    self._cargar_productos()
                    self._cargar_alertas()
                    
                    self.status_changed.emit(f"Producto '{producto_actualizado['nombre']}' actualizado correctamente")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo actualizar el producto: {str(e)}")
                    logger.error("Error al actualizar producto: %s", e)
    
    def _eliminar_producto(self, producto):
        """Elimina un producto del inventario"""
        _ = QMessageBox.question(
            self, 
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar el producto '{producto.nombre}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirmacion == QMessageBox.StandardButton.Yes:
            if hasattr(self, 'inventario_service'):
                try:
                    # Usar el servicio para eliminar el producto
                    self.inventario_service.eliminar_producto(producto.id)
                    
                    # Recargar datos
                    self._cargar_productos()
                    self._cargar_alertas()
                    
                    self.status_changed.emit(f"Producto '{producto.nombre}' eliminado correctamente")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"No se pudo eliminar el producto: {str(e)}")
                    logger.error("Error al eliminar producto: %s", e)
    
    def _realizar_pedido(self, producto):
        """Realiza un pedido para un producto"""
        QMessageBox.information(
            self,
            "Pedido realizado",
            f"Se ha realizado un pedido de {producto.nombre} al proveedor {producto.proveedor_nombre or 'desconocido'}."
        )
        self.status_changed.emit(f"Pedido de {producto.nombre} realizado")
    
    def _generar_pedido_automatico(self):
        """Genera un pedido automático para todos los productos bajo mínimo"""
        if hasattr(self, 'inventario_service'):
            try:                # Generar pedido automático usando el servicio
                _ = self.inventario_service.generar_pedido_automatico()
                
                if pedidos:
                    # Verificar si pedidos es una lista o un objeto individual
                    _ = len(pedidos) if isinstance(pedidos, (list, tuple)) else 1
                    QMessageBox.information(
                        self,
                        "Pedidos generados",
                        f"Se han generado {num_pedidos} pedidos automáticos para productos bajo mínimo."
                    )
                    self.status_changed.emit(f"{num_pedidos} pedidos automáticos generados")
                else:
                    QMessageBox.information(
                        self,
                        "Sin pedidos",
                        "No hay productos que requieran pedido automático o todos los productos bajo mínimo carecen de proveedor asignado."
                    )
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudieron generar pedidos automáticos: {str(e)}")
                logger.error("Error al generar pedidos automáticos: %s", e)
    
    def refresh(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza los datos del módulo de inventario"""
        super().refresh()
        
        if not hasattr(self, 'inventario_service'):
            self._cargar_datos_prueba()
            return
            
        # Recargar todos los datos
        self._cargar_productos()
        self._cargar_alertas()
        self._cargar_proveedores()
        self._actualizar_estadisticas()
        
        logger.info("Datos del inventario actualizados")
        self.status_changed.emit("Inventario actualizado correctamente")
    
    def on_module_activated(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Se llama cuando el módulo de inventario se activa"""
        super().on_module_activated()
        self.status_changed.emit("Inventario - Gestión de productos y stock")
    
    def on_module_deactivated(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Se llama cuando el módulo de inventario se desactiva"""
        super().on_module_deactivated()
        # Guardar cambios si es necesario
