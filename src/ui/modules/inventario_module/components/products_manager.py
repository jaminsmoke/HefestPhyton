"""
Módulo de Gestión de Productos para Hefest - v0.0.12
====================================================

Widget principal y controlador central para la gestión completa de productos
de inventario en establecimientos de hostelería.

FUNCIONALIDADES PRINCIPALES:
----------------------------
- CRUD completo de productos (Crear, Leer, Actualizar, Eliminar)
- Gestión de stock y alertas de inventario
- Filtros avanzados y búsqueda inteligente
- Importación/Exportación de datos (CSV, Excel)
- Cálculos automáticos de precios y márgenes
- Gestión de categorías y proveedores
- Histórico de movimientos de stock

COMPONENTES INTEGRADOS:
----------------------
- Tabla de productos con ordenación y filtros
- Panel de filtros avanzados (InventoryFiltersWidget)
- Buscador inteligente (ProductSearchWidget)
- Resumen ejecutivo (InventorySummaryWidget)
- Diálogos modales para CRUD (product_dialogs_pro)

ARQUITECTURA:
------------
- MVC Pattern: Este widget actúa como Controlador y Vista
- Modelo: inventario_service_real.py (capa de datos)
- Comunicación por señales PyQt6 para desacoplamiento
- Validaciones en tiempo real y manejo robusto de errores

CARACTERÍSTICAS TÉCNICAS:
------------------------
- Actualización automática de datos cada 30 segundos
- Cache inteligente para optimizar rendimiento
- Validaciones de integridad de datos
- Logs detallados para debugging y auditoría
- Responsive design adaptable a diferentes tamaños

AUTOR: Hefest Development Team
VERSIÓN: v0.0.12
FECHA: Diciembre 2024
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QLineEdit,
    QComboBox,
    QGroupBox,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QDialog,
    QFileDialog,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

# Importar diálogos profesionales
from ..dialogs.product_dialogs_pro import (
    NewProductDialog,
    EditProductDialog,
    StockAdjustmentDialog,
    DeleteConfirmationDialog,
)

_ = logging.getLogger(__name__)


class ProductsManagerWidget(QWidget):
    """
    Widget especializado para la gestión de productos
    """

    # Señales
    _ = pyqtSignal(dict)
    producto_actualizado = pyqtSignal()

    def __init__(self, inventario_service, parent=None):
        """Inicializar el widget gestor de productos"""
        super().__init__(parent)

        self.inventario_service = inventario_service
        self.productos_cache = []
        self.categorias_cache = []

        self.init_ui()
        self.load_products()
        self.load_categories()

        # Timer para actualización automática
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(60000)  # Actualizar cada minuto

        logger.info("ProductsManagerWidget inicializado correctamente")

    def init_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicializar la interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header
        header = self.create_header()
        layout.addWidget(header)

        # Panel de búsqueda y filtros
        search_panel = self.create_search_panel()
        layout.addWidget(search_panel)

        # Tabla de productos
        self.products_table = self.create_products_table()
        layout.addWidget(self.products_table)

        # Panel de estadísticas y alertas
        bottom_panel = self.create_bottom_panel()
        layout.addWidget(bottom_panel)

        self.apply_styles()

    def create_header(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear el header del módulo"""
        header = QFrame()
        header.setObjectName("HeaderFrame")
        _ = QHBoxLayout(header)

        # Título
        title = QLabel("📦 Gestión de Productos")
        title.setObjectName("ModuleTitle")
        layout.addWidget(title)

        layout.addStretch()

        # Botones de acción rápida
        self.add_product_btn = QPushButton("➕ Nuevo Producto")
        self.add_product_btn.clicked.connect(self.add_product)

        self.export_btn = QPushButton("📊 Exportar")
        self.export_btn.clicked.connect(self.export_to_csv)

        layout.addWidget(self.add_product_btn)
        layout.addWidget(self.export_btn)

        return header

    def create_search_panel(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear panel de búsqueda y filtros"""
        panel = QFrame()
        panel.setObjectName("SearchPanel")
        _ = QHBoxLayout(panel)

        # Búsqueda por texto
        _ = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar productos...")
        self.search_input.textChanged.connect(self.on_search_changed)

        # Filtro por categoría
        _ = QLabel("Categoría:")
        self.category_combo = QComboBox()
        self.category_combo.addItem("Todas las categorías", "")
        self.category_combo.currentTextChanged.connect(self.on_category_changed)

        layout.addWidget(search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)
        layout.addStretch()

        # Botones de acción
        self.edit_btn = QPushButton("✏️ Editar")
        self.edit_btn.clicked.connect(self.edit_selected_product)
        self.edit_btn.setEnabled(False)

        self.stock_btn = QPushButton("📦 Ajustar Stock")
        self.stock_btn.clicked.connect(self.adjust_stock)
        self.stock_btn.setEnabled(False)

        self.delete_btn = QPushButton("🗑️ Eliminar")
        self.delete_btn.clicked.connect(self.delete_selected_product)
        self.delete_btn.setEnabled(False)

        layout.addWidget(self.edit_btn)
        layout.addWidget(self.stock_btn)
        layout.addWidget(self.delete_btn)

        return panel

    def create_products_table(self) -> QTableWidget:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear la tabla de productos"""
        table = QTableWidget()
        table.setObjectName("ProductsTable")

        # Configurar columnas
        _ = [
            "ID",
            "Nombre",
            "Categoría",
            "Precio",
            "Stock",
            "Stock Mín.",
            "Estado",
        ]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        # Configurar tabla
        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)

        # Ajustar columnas
        header = table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
            header.resizeSection(0, 60)
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Nombre
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # Categoría
            header.resizeSection(2, 120)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Precio
            header.resizeSection(3, 100)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Stock
            header.resizeSection(4, 80)
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Stock Mín.
            header.resizeSection(5, 90)
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Estado
            header.resizeSection(6, 100)

        # Conectar señales
        table.itemSelectionChanged.connect(self.on_product_selected)
        table.itemDoubleClicked.connect(self.edit_selected_product)

        return table

    def create_bottom_panel(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear panel inferior con estadísticas y alertas"""
        panel = QFrame()
        _ = QHBoxLayout(panel)

        # Panel de estadísticas
        stats_panel = self.create_stats_panel()
        layout.addWidget(stats_panel)

        # Panel de alertas
        alerts_panel = self.create_alerts_panel()
        layout.addWidget(alerts_panel)

        return panel

    def create_stats_panel(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear panel de estadísticas"""
        panel = QFrame()
        panel.setObjectName("StatsPanel")
        _ = QVBoxLayout(panel)

        # Título
        title = QLabel("📊 Estadísticas")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)

        # Estadísticas
        self.total_products_label = QLabel("Total productos: 0")
        self.total_value_label = QLabel("Valor total: $0.00")
        self.low_stock_label = QLabel("Stock bajo: 0")
        self.out_of_stock_label = QLabel("Sin stock: 0")

        layout.addWidget(self.total_products_label)
        layout.addWidget(self.total_value_label)
        layout.addWidget(self.low_stock_label)
        layout.addWidget(self.out_of_stock_label)

        return panel

    def create_alerts_panel(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear panel de alertas"""
        panel = QFrame()
        panel.setObjectName("AlertsPanel")
        _ = QVBoxLayout(panel)

        # Título
        title = QLabel("⚠️ Alertas")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)

        # Lista de alertas (simplificada)
        self.alerts_label = QLabel("No hay alertas")
        layout.addWidget(self.alerts_label)

        return panel

    def load_products(self, search_text: str = "", category: str = ""):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cargar productos desde el servicio"""
        try:
            self.productos_cache = self.inventario_service.get_productos(
                search_text, category
            )
            self.update_products_table()
            self.update_statistics()
            self.update_alerts()

        except Exception as e:
            logger.error("Error cargando productos: %s", e)
            QMessageBox.warning(
                self, "Error", f"No se pudieron cargar los productos: {str(e)}"
            )

    def load_categories(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cargar categorías desde el servicio"""
        try:
            _ = self.inventario_service.get_categorias()

            # Limpiar combo
            self.category_combo.clear()
            self.category_combo.addItem("Todas las categorías", "")

            # Agregar categorías
            for categoria in categorias:
                self.category_combo.addItem(categoria, categoria)

            self.categorias_cache = categorias

        except Exception as e:
            logger.error("Error cargando categorías: %s", e)

    def update_products_table(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar la tabla de productos"""
        try:
            self.products_table.setRowCount(len(self.productos_cache))

            for row, producto in enumerate(self.productos_cache):
                # ID
                self.products_table.setItem(row, 0, QTableWidgetItem(str(producto.id)))

                # Nombre
                self.products_table.setItem(row, 1, QTableWidgetItem(producto.nombre))

                # Categoría
                self.products_table.setItem(
                    row, 2, QTableWidgetItem(producto.categoria)
                )

                # Precio
                precio_item = QTableWidgetItem(f"${producto.precio:.2f}")
                precio_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
                self.products_table.setItem(row, 3, precio_item)

                # Stock actual
                stock_item = QTableWidgetItem(str(producto.stock))
                stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                # Colorear según nivel de stock
                if producto.stock == 0:
                    stock_item.setBackground(QColor("#fee2e2"))  # Rojo claro
                elif producto.necesita_reposicion():
                    stock_item.setBackground(QColor("#fef3c7"))  # Amarillo claro
                else:
                    stock_item.setBackground(QColor("#dcfce7"))  # Verde claro

                self.products_table.setItem(row, 4, stock_item)

                # Stock mínimo
                min_stock_item = QTableWidgetItem(str(producto.stock_minimo))
                min_stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.products_table.setItem(row, 5, min_stock_item)

                # Estado
                if producto.stock == 0:
                    _ = "Sin Stock"
                    color = QColor("#fca5a5")
                elif producto.necesita_reposicion():
                    _ = "Stock Bajo"
                    color = QColor("#fbbf24")
                else:
                    _ = "Disponible"
                    color = QColor("#86efac")

                estado_item = QTableWidgetItem(estado)
                estado_item.setBackground(color)
                estado_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.products_table.setItem(row, 6, estado_item)

        except Exception as e:
            logger.error("Error actualizando tabla de productos: %s", e)

    def update_statistics(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar estadísticas"""
        try:
            _ = len(self.productos_cache)
            total_value = sum(p.precio * p.stock for p in self.productos_cache)
            _ = sum(
                1
                for p in self.productos_cache
                if p.necesita_reposicion() and p.stock > 0
            )
            out_of_stock = sum(1 for p in self.productos_cache if p.stock == 0)

            self.total_products_label.setText(f"Total productos: {total_products}")
            self.total_value_label.setText(f"Valor total: ${total_value:.2f}")
            self.low_stock_label.setText(f"Stock bajo: {low_stock}")
            self.out_of_stock_label.setText(f"Sin stock: {out_of_stock}")

        except Exception as e:
            logger.error("Error actualizando estadísticas: %s", e)

    def update_alerts(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar alertas"""
        try:
            _ = []

            # Productos sin stock
            sin_stock = [p for p in self.productos_cache if p.stock == 0]
            if sin_stock:
                alertas.append(f"⚠️ {len(sin_stock)} producto(s) sin stock")

            # Productos con stock bajo
            _ = [
                p
                for p in self.productos_cache
                if p.necesita_reposicion() and p.stock > 0
            ]
            if stock_bajo:
                alertas.append(f"⚠️ {len(stock_bajo)} producto(s) con stock bajo")

            if alertas:
                self.alerts_label.setText("\n".join(alertas))
            else:
                self.alerts_label.setText("✅ No hay alertas")

        except Exception as e:
            logger.error("Error actualizando alertas: %s", e)

    def on_search_changed(self, text: str):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Manejar cambio en búsqueda"""
        category = self.category_combo.currentData() or ""
        self.load_products(text, category)

    def on_category_changed(self, category: str):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Manejar cambio en filtro de categoría"""
        _ = self.search_input.text()
        category_data = self.category_combo.currentData() or ""
        self.load_products(search_text, category_data)

    def on_product_selected(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Manejar selección de producto"""
        selected_rows = set(item.row() for item in self.products_table.selectedItems())
        has_selection = bool(selected_rows)

        self.edit_btn.setEnabled(has_selection)
        self.stock_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

        if has_selection:
            row = next(iter(selected_rows))
            if row < len(self.productos_cache):
                producto = self.productos_cache[row]
                self.producto_seleccionado.emit(
                    {
                        "id": producto.id,
                        "nombre": producto.nombre,
                        "categoria": producto.categoria,
                        "precio": producto.precio,
                        "stock": producto.stock,
                        "stock_minimo": producto.stock_minimo,
                    }
                )

    def add_product(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Agregar nuevo producto usando diálogo profesional"""
        try:
            # Crear diálogo con categorías disponibles y servicio de inventario
            _ = NewProductDialog(
                parent=self,
                _ = self.categorias_cache,
                inventario_service=self.inventario_service,
            )

            if dialog.exec() == QDialog.DialogCode.Accepted:
                # El diálogo ya maneja la creación del producto internamente
                logger.info("Producto creado exitosamente desde diálogo")
                self.load_products()  # Recargar la tabla
                self.producto_actualizado.emit()

        except Exception as e:
            logger.error("Error creando producto: %s", e)
            QMessageBox.warning(
                self, "Error", f"No se pudo crear el producto: {str(e)}"
            )

    def edit_selected_product(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Editar producto seleccionado usando diálogo profesional"""
        try:
            _ = set(
                item.row() for item in self.products_table.selectedItems()
            )
            if not selected_rows:
                return

            row = next(iter(selected_rows))
            if row < len(self.productos_cache):
                _ = self.productos_cache[row]
                # Usar el diálogo profesional de edición
                _ = EditProductDialog(
                    parent=self,
                    _ = producto,
                    categories=self.categorias_cache,
                    _ = self.inventario_service,
                )

                if dialog.exec() == QDialog.DialogCode.Accepted:
                    # El diálogo ya maneja la actualización del producto internamente
                    logger.info(
                        f"Producto '{producto.nombre}' actualizado exitosamente desde diálogo"
                    )
                    self.load_products()  # Recargar la tabla
                    self.producto_actualizado.emit()

        except Exception as e:
            logger.error("Error editando producto: %s", e)
            QMessageBox.warning(
                self, "Error", f"No se pudo editar el producto: {str(e)}"
            )

    def adjust_stock(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Ajustar stock del producto seleccionado"""
        try:
            _ = set(
                item.row() for item in self.products_table.selectedItems()
            )
            if not selected_rows:
                return

            row = next(iter(selected_rows))
            if row < len(self.productos_cache):
                _ = self.productos_cache[row]
                # Usar diálogo simple
                from PyQt6.QtWidgets import QInputDialog

                nuevo_stock, ok = QInputDialog.getInt(
                    self,
                    "Ajustar Stock",
                    f"Stock actual de {producto.nombre}: {producto.stock}\nNuevo stock:",
                    producto.stock,
                    0,
                    9999,
                )
                if ok:
                    if self.inventario_service.actualizar_stock(
                        producto.id, nuevo_stock
                    ):
                        self.load_products()
                        self.producto_actualizado.emit()
                        QMessageBox.information(
                            self, "Éxito", "Stock actualizado correctamente"
                        )
                    else:
                        QMessageBox.warning(
                            self, "Error", "No se pudo actualizar el stock"
                        )

        except Exception as e:
            logger.error("Error ajustando stock: %s", e)
            QMessageBox.warning(self, "Error", f"No se pudo ajustar el stock: {str(e)}")

    def delete_selected_product(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Eliminar producto seleccionado"""
        try:
            _ = set(
                item.row() for item in self.products_table.selectedItems()
            )
            if not selected_rows:
                return

            row = next(iter(selected_rows))
            if row < len(self.productos_cache):
                _ = self.productos_cache[row]

                reply = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Eliminar el producto '{producto.nombre}'?\nEsta acción no se puede deshacer.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )

                if reply == QMessageBox.StandardButton.Yes:
                    if self.inventario_service.eliminar_producto(producto.id):
                        self.load_products()
                        self.producto_actualizado.emit()
                        QMessageBox.information(
                            self, "Éxito", "Producto eliminado correctamente"
                        )
                    else:
                        QMessageBox.warning(
                            self, "Error", "No se pudo eliminar el producto"
                        )

        except Exception as e:
            logger.error("Error eliminando producto: %s", e)
            QMessageBox.warning(
                self, "Error", f"No se pudo eliminar el producto: {str(e)}"
            )

    def export_to_csv(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Exportar productos a CSV"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Exportar Productos",
                f"productos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "CSV Files (*.csv)",
            )

            if file_path:
                import csv

                with open(file_path, "w", newline="", encoding="utf-8") as file:
                    _ = csv.writer(file)

                    # Header
                    writer.writerow(
                        ["ID", "Nombre", "Categoría", "Precio", "Stock", "Stock Mínimo"]
                    )

                    # Datos
                    for producto in self.productos_cache:
                        writer.writerow(
                            [
                                producto.id,
                                producto.nombre,
                                producto.categoria,
                                producto.precio,
                                producto.stock,
                                producto.stock_minimo,
                            ]
                        )

                QMessageBox.information(
                    self, "Éxito", f"Productos exportados a:\n{file_path}"
                )

        except Exception as e:
            logger.error("Error exportando productos: %s", e)
            QMessageBox.warning(self, "Error", f"Error exportando productos: {str(e)}")

    def refresh_data(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar datos automáticamente"""
        try:
            _ = self.search_input.text()
            category = self.category_combo.currentData() or ""
            self.load_products(search_text, category)

        except Exception as e:
            logger.error("Error en actualización automática: %s", e)

    def cleanup(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Limpiar recursos"""
        try:
            if hasattr(self, "refresh_timer"):
                self.refresh_timer.stop()

        except Exception as e:
            logger.error("Error en cleanup: %s", e)

    def apply_styles(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Aplicar estilos al widget"""
        self.setStyleSheet(
            """
            #HeaderFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1e3c72, stop:1 #2a5298);
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }

            #ModuleTitle {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }

            #SearchPanel {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
            }
              #ProductsTable {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                gridline-color: #f1f5f9;
                selection-background-color: #3b82f6;
                selection-color: white;
                outline: none;
            }

            #ProductsTable::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
                border: none;
            }

            #ProductsTable::item:selected {
                background: #3b82f6;
                color: white;
                border: none;
                outline: none;
            }

            #ProductsTable::item:hover {
                background: #e6f3ff;
            }

            #ProductsTable QHeaderView::section {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                padding: 8px;
                font-weight: bold;
                color: #374151;
            }

            #ProductsTable QHeaderView::section:horizontal {
                border-left: none;
                border-right: none;
                border-top: none;
            }

            #StatsPanel, #AlertsPanel {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 15px;
                margin: 5px;
                min-width: 200px;
            }

            #PanelTitle {
                font-weight: bold;
                font-size: 16px;
                color: #2d3748;
                margin-bottom: 10px;
            }

            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 100px;
            }

            QPushButton:hover {
                background: #2563eb;
            }

            QPushButton:disabled {
                background: #9ca3af;
                color: #6b7280;
            }

            QLineEdit, QComboBox {
                border: 2px solid #e2e8f0;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
            }

            QLineEdit:focus, QComboBox:focus {
                border-color: #3b82f6;
            }
        """
        )
