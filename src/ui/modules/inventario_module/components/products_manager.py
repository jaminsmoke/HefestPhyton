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
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

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
    QMessageBox,
    QDialog,
    QFileDialog,
    QTextEdit,
    QFormLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor

# Importar utilidades comunes
from .inventory_common_utils import (
    InventoryManagerBase,
    InventoryDialogBase,
    InventoryValidationUtils,
    CommonInventoryStyles,
)

logger = logging.getLogger(__name__)


class ProductsManagerWidget(InventoryManagerBase):
    """Widget especializado para la gestión de productos"""

    # Señales
    producto_seleccionado = pyqtSignal(dict)
    producto_actualizado = pyqtSignal()

    def __init__(
        self, inventario_service: Any, parent: Optional[QWidget] = None
    ) -> None:
        """Inicializar el widget gestor de productos"""
        # PRIMERO: Almacenar el servicio de inventario
        self.inventario_service = inventario_service
        self.productos_cache: List[Dict[str, Any]] = []
        self.categorias_cache: List[Dict[str, Any]] = []

        # SEGUNDO: Flag para evitar carga inicial prematura
        self._skip_initial_load = True

        # TERCERO: Pasar db_manager desde el inventario_service si está disponible
        db_manager = (
            getattr(inventario_service, "db_manager", None) or inventario_service
        )
        super().__init__(db_manager=db_manager, parent=parent)

        # CUARTO: Configuraciones adicionales
        self.title_label.setText("📦 Gestión de Productos")

        # Configurar tabla específica para productos
        self._setup_products_table()
        self._setup_connections()

        self.init_ui()
        self.load_categories()

        # Timer para actualización automática
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)  # type: ignore
        self.refresh_timer.start(60000)  # Actualizar cada minuto

        # AHORA cargar datos después de que todo esté inicializado
        self._skip_initial_load = False
        self.load_products()

        logger.info("ProductsManagerWidget inicializado correctamente")

    def init_ui(self) -> None:
        """Inicializar elementos adicionales después de la tabla"""
        # Panel de búsqueda y filtros (insertar después del header base)
        search_panel = self.create_search_panel()
        self.main_layout.insertWidget(1, search_panel)

        # Panel de estadísticas y alertas moderno (al final)
        bottom_panel = self.create_bottom_panel()
        self.main_layout.addWidget(bottom_panel)

        self.apply_styles()

    def create_search_panel(self) -> QFrame:
        """Crear panel de búsqueda y filtros"""
        panel = QFrame()
        panel.setObjectName("SearchPanel")
        layout = QHBoxLayout(panel)

        # Búsqueda por texto
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar productos...")
        self.search_input.textChanged.connect(self.on_search_changed)  # type: ignore

        # Filtro por categoría
        category_label = QLabel("Categoría:")
        self.category_combo = QComboBox()
        self.category_combo.addItem("Todas las categorías", "")
        self.category_combo.currentTextChanged.connect(self.on_category_changed)  # type: ignore

        layout.addWidget(search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(category_label)
        layout.addWidget(self.category_combo)
        layout.addStretch()

        # Botón adicional específico de productos
        self.stock_btn = QPushButton("📦 Ajustar Stock")
        self.stock_btn.clicked.connect(self.adjust_stock)
        self.stock_btn.setEnabled(False)

        layout.addWidget(self.stock_btn)

        return panel

    def create_bottom_panel(self) -> QFrame:
        """Crear panel inferior con estadísticas y alertas"""
        panel = QFrame()
        layout = QHBoxLayout(panel)

        # Panel de estadísticas
        stats_panel = self.create_stats_panel()
        layout.addWidget(stats_panel)

        # Panel de alertas
        alerts_panel = self.create_alerts_panel()
        layout.addWidget(alerts_panel)

        return panel

    def create_stats_panel(self) -> QFrame:
        """Crear panel de estadísticas"""
        panel = QFrame()
        panel.setObjectName("StatsPanel")
        layout = QVBoxLayout(panel)

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
        """Crear panel de alertas"""
        panel = QFrame()
        panel.setObjectName("AlertsPanel")
        layout = QVBoxLayout(panel)

        # Título
        title = QLabel("⚠️ Alertas")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)

        # Lista de alertas (simplificada)
        self.alerts_label = QLabel("No hay alertas")
        layout.addWidget(self.alerts_label)

        return panel

    def load_products(self, search_text: str = "", category: str = "") -> None:
        """Cargar productos desde el servicio"""
        try:
            logger.info(
                f"[UI] Llamando a get_productos con search_text='{search_text}', category='{category}'"
            )
            self.productos_cache = self.inventario_service.get_productos(  # type: ignore
                search_text, category
            )
            logger.info(f"[UI] Productos recibidos: {self.productos_cache}")
            self.update_products_table()
            self.update_statistics()
            self.update_alerts()
        except Exception as e:
            logger.error(f"Error cargando productos: {e}")
            QMessageBox.warning(
                self, "Error", f"No se pudieron cargar los productos: {str(e)}"
            )

    def load_categories(self) -> None:
        """Cargar categorías disponibles como diccionarios (id, nombre)"""
        try:
            categorias = self.inventario_service.get_categorias_completas()  # type: ignore
            self.category_combo.clear()
            self.category_combo.addItem("Todas las categorías", "")
            for categoria in categorias:
                nombre = categoria.get("nombre", "Sin nombre")
                categoria_id = categoria.get("id", "")
                self.category_combo.addItem(nombre, categoria_id)
            self.categorias_cache = categorias
        except Exception as e:
            logger.error(f"Error cargando categorías: {e}")

    def update_products_table(self) -> None:
        """Actualizar la tabla de productos"""
        try:
            logger.info(
                f"[UI] Actualizando tabla con {len(self.productos_cache)} productos"
            )
            self.items_cache = self.productos_cache
            self.table.setSortingEnabled(False)
            self.table.setRowCount(len(self.productos_cache))

            # Crear cache de categorías por id y por nombre
            categorias_por_id = {
                str(cat.get("id")): cat.get("nombre", "")
                for cat in self.categorias_cache
            }
            categorias_por_nombre = {
                cat.get("nombre", ""): cat.get("nombre", "")
                for cat in self.categorias_cache
            }

            for row, producto in enumerate(self.productos_cache):
                logger.info(f"[UI] Insertando producto en fila {row}: {producto}")

                # ID
                self.table.setItem(row, 0, QTableWidgetItem(str(producto.id)))

                # Nombre
                self.table.setItem(row, 1, QTableWidgetItem(producto.nombre))

                # Categoría - Soporte para productos legacy (solo nombre) y nuevos (id)
                categoria_id = getattr(producto, "categoria_id", None)
                categoria_nombre = None
                if categoria_id:
                    categoria_nombre = categorias_por_id.get(str(categoria_id))
                if not categoria_nombre:
                    # Intentar por nombre legacy
                    categoria_nombre = categorias_por_nombre.get(
                        getattr(producto, "categoria", ""), "Sin categoría"
                    )
                logger.info(
                    f"[UI] Fila {row}: categoria_id={categoria_id}, categoria_nombre={categoria_nombre}"
                )
                self.table.setItem(row, 2, QTableWidgetItem(categoria_nombre))

                # Precio
                precio_item = QTableWidgetItem(f"${producto.precio:.2f}")
                precio_item.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
                self.table.setItem(row, 3, precio_item)

                # Stock actual
                stock_item = QTableWidgetItem(str(producto.stock_actual))
                stock_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if producto.stock_actual == 0:
                    stock_item.setBackground(QColor("#dc3545"))
                    stock_item.setForeground(QColor("white"))
                elif (
                    hasattr(producto, "stock_minimo")
                    and producto.stock_actual <= producto.stock_minimo
                ):
                    stock_item.setBackground(QColor("#ffc107"))
                self.table.setItem(row, 4, stock_item)

                # Stock mínimo
                stock_min_item = QTableWidgetItem(
                    str(getattr(producto, "stock_minimo", 0))
                )
                stock_min_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, 5, stock_min_item)

                # Estado
                if producto.stock_actual == 0:
                    estado = "Sin stock"
                    color = QColor("#dc3545")
                elif (
                    hasattr(producto, "stock_minimo")
                    and producto.stock_actual <= producto.stock_minimo
                ):
                    estado = "Stock bajo"
                    color = QColor("#ffc107")
                else:
                    estado = "Disponible"
                    color = QColor("#28a745")

                estado_item = QTableWidgetItem(estado)
                estado_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                estado_item.setForeground(color)
                self.table.setItem(row, 6, estado_item)

            self.table.viewport().update()
            self.table.setSortingEnabled(True)

            if self.table.rowCount() == 0:
                logger.warning(
                    "[UI] La tabla de productos quedó vacía tras el llenado."
                )

        except Exception as e:
            logger.error(f"Error actualizando tabla de productos: {e}")

    def update_statistics(self):
        """Actualizar estadísticas"""
        try:
            total_products = len(self.productos_cache)
            total_value = sum(p.precio * p.stock for p in self.productos_cache)
            low_stock = sum(
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
            logger.error(f"Error actualizando estadísticas: {e}")

    def _setup_products_table(self):
        """Configura la tabla específica para productos"""
        headers = [
            "ID",
            "Nombre",
            "Categoría",
            "Precio",
            "Stock",
            "Stock Mín.",
            "Estado",
        ]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setObjectName("ProductsTable")

        # Configurar columnas
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Nombre
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)  # Categoría
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Precio
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Stock
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Stock Mín.
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Estado

            # Anchos específicos
            self.table.setColumnWidth(0, 60)
            self.table.setColumnWidth(2, 120)
            self.table.setColumnWidth(3, 80)
            self.table.setColumnWidth(4, 80)
            self.table.setColumnWidth(5, 80)
            self.table.setColumnWidth(6, 100)

        # Configurar comportamiento de la tabla
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)

        # Conectar señales específicas
        self.table.itemSelectionChanged.connect(self.on_product_selected)
        self.table.itemDoubleClicked.connect(self.edit_selected_product)

    def _setup_connections(self):
        """Configurar conexiones específicas de productos"""
        super()._setup_connections()
        # Sobrescribir las conexiones de la clase base con las específicas de productos
        self.add_btn.clicked.disconnect()  # Desconectar la conexión base
        self.edit_btn.clicked.disconnect()
        self.delete_btn.clicked.disconnect()
        self.refresh_btn.clicked.disconnect()

        # Conectar con los métodos específicos de productos
        self.add_btn.clicked.connect(self.add_product)
        self.edit_btn.clicked.connect(self.edit_selected_product)
        self.delete_btn.clicked.connect(self.delete_selected_product)
        self.refresh_btn.clicked.connect(self.load_products)

    def _load_data(self):
        """Cargar datos específicos de productos"""
        # Control de carga inicial prematura
        if hasattr(self, "_skip_initial_load") and self._skip_initial_load:
            logger.debug("Saltando carga inicial de productos")
            return

        # Solo cargar si la UI está completamente inicializada
        if hasattr(self, "table") and hasattr(self, "inventario_service"):
            self.load_products()
        else:
            logger.debug("UI no inicializada aún, posponiendo carga de productos")

    def update_alerts(self):
        """Actualizar alertas"""
        try:
            alertas = []

            # Productos sin stock
            sin_stock = [p for p in self.productos_cache if p.stock == 0]
            if sin_stock:
                alertas.append(f"⚠️ {len(sin_stock)} producto(s) sin stock")

            # Productos con stock bajo
            stock_bajo = [
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
            logger.error(f"Error actualizando alertas: {e}")

    def on_search_changed(self, text: str):
        """Manejar cambio en búsqueda"""
        category = self.category_combo.currentData() or ""
        self.load_products(text, category)

    def on_category_changed(self, category: str):
        """Manejar cambio en filtro de categoría"""
        search_text = self.search_input.text()
        category_data = self.category_combo.currentData() or ""
        self.load_products(search_text, category_data)

    def on_product_selected(self):
        """Manejar selección de producto"""
        selected_rows = set(item.row() for item in self.table.selectedItems())
        has_selection = bool(selected_rows)

        # Habilitar/deshabilitar botones según selección
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        if hasattr(self, "stock_btn"):
            self.stock_btn.setEnabled(has_selection)

        if has_selection:
            row = next(iter(selected_rows))
            if row < len(self.productos_cache):
                producto = self.productos_cache[row]
                self.producto_seleccionado.emit(
                    {
                        "id": producto.id,
                        "nombre": producto.nombre,
                        "categoria": getattr(producto, "categoria", ""),
                        "precio": producto.precio,
                        "stock": producto.stock_actual,
                        "stock_minimo": getattr(producto, "stock_minimo", 0),
                    }
                )

    def add_product(self):
        """Agregar nuevo producto usando diálogo profesional"""
        try:
            # Crear diálogo con categorías disponibles y servicio de inventario
            dialog = ProductDialog(
                parent=self,
                inventario_service=self.inventario_service,
                producto=None,  # Nuevo producto
            )

            if dialog.exec() == QDialog.DialogCode.Accepted:
                # El diálogo ya maneja la creación del producto internamente
                logger.info("Producto creado exitosamente desde diálogo")
                self.load_products()  # Recargar la tabla
                self.producto_actualizado.emit()

        except Exception as e:
            logger.error(f"Error creando producto: {e}")
            QMessageBox.warning(
                self, "Error", f"No se pudo crear el producto: {str(e)}"
            )

    def edit_selected_product(self):
        """Editar producto seleccionado"""
        try:
            current_row = self.table.currentRow()
            if current_row >= 0 and current_row < len(self.productos_cache):
                producto = self.productos_cache[current_row]
                dialog = ProductDialog(self.inventario_service, self, producto)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.load_products()
                    self.producto_actualizado.emit()
            else:
                QMessageBox.information(
                    self, "Información", "Seleccione un producto para editar"
                )
        except Exception as e:
            logger.error(f"Error editando producto: {e}")
            QMessageBox.warning(self, "Error", f"Error al editar producto: {str(e)}")

    def adjust_stock(self):
        """Ajustar stock del producto seleccionado"""
        try:
            selected_rows = set(item.row() for item in self.table.selectedItems())
            if not selected_rows:
                return

            row = next(iter(selected_rows))
            if row < len(self.productos_cache):
                producto = self.productos_cache[row]
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
            logger.error(f"Error ajustando stock: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo ajustar el stock: {str(e)}")

    def delete_selected_product(self):
        """Eliminar producto seleccionado"""
        try:
            current_row = self.table.currentRow()
            if current_row >= 0 and current_row < len(self.productos_cache):
                producto = self.productos_cache[current_row]

                reply = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Eliminar el producto '{producto.get('nombre', 'N/A')}'?\nEsta acción no se puede deshacer.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )

                if reply == QMessageBox.StandardButton.Yes:
                    success = self.inventario_service.eliminar_producto(
                        producto.get("id")
                    )
                    if success:
                        self.load_products()
                        self.producto_actualizado.emit()
                        QMessageBox.information(
                            self, "Éxito", "Producto eliminado correctamente"
                        )
                    else:
                        QMessageBox.warning(
                            self, "Error", "No se pudo eliminar el producto"
                        )
            else:
                QMessageBox.information(
                    self, "Información", "Seleccione un producto para eliminar"
                )
        except Exception as e:
            logger.error(f"Error eliminando producto: {e}")
            QMessageBox.warning(self, "Error", f"Error al eliminar producto: {str(e)}")

    def export_to_csv(self):
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
                    writer = csv.writer(file)

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
            logger.error(f"Error exportando productos: {e}")
            QMessageBox.warning(self, "Error", f"Error exportando productos: {str(e)}")

    def refresh_data(self):
        """Actualizar datos automáticamente"""
        try:
            search_text = self.search_input.text()
            category = self.category_combo.currentData() or ""
            self.load_products(search_text, category)

        except Exception as e:
            logger.error(f"Error en actualización automática: {e}")

    def cleanup(self):
        """Limpiar recursos"""
        try:
            if hasattr(self, "refresh_timer"):
                self.refresh_timer.stop()

        except Exception as e:
            logger.error(f"Error en cleanup: {e}")

    def apply_styles(self):
        """Aplicar estilos al widget"""
        self.setStyleSheet(
            """
            QWidget {
                background-color: #ffffff;
            }

            #SearchPanel {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
            }
            QTableWidget {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                gridline-color: #f1f5f9;
                selection-background-color: #3b82f6;
                selection-color: white;
                outline: none;
                alternate-background-color: #f8fafc;
            }

            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
                border: none;
            }

            QTableWidget::item:selected {
                background: #3b82f6;
                color: white;
                border: none;
                outline: none;
            }

            QTableWidget::item:hover {
                background: #e6f3ff;
            }

            QTableWidget QHeaderView::section {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                padding: 8px;
                font-weight: bold;
                color: #374151;
            }

            QTableWidget QHeaderView::section:horizontal {
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

        # Aplicar estilo específico al título heredado
        if hasattr(self, "title_label"):
            self.title_label.setStyleSheet(
                """
                font-size: 24px;
                font-weight: bold;
                color: #1e3c72;
                padding: 10px 0;
            """
            )


class ProductDialog(InventoryDialogBase):
    """Diálogo para agregar/editar productos"""

    def __init__(self, inventario_service, parent=None, producto=None):
        self.inventario_service = inventario_service
        self.producto_data = producto
        self.is_edit = producto is not None

        title = "Editar Producto" if self.is_edit else "Nuevo Producto"
        super().__init__(parent, title, (600, 500))

        if self.is_edit:
            self._load_product_data()

    def _setup_ui(self):
        """Configuración específica de UI para productos"""
        super()._setup_ui()

        # Información básica
        basic_form = QFormLayout()

        # Campo nombre
        self.name_edit = QLineEdit()
        basic_form.addRow("Nombre*:", self.name_edit)

        # Campo categoría
        self.category_combo = QComboBox()
        self._load_categories()
        basic_form.addRow("Categoría*:", self.category_combo)

        # Campo precio
        self.price_edit = QLineEdit()
        basic_form.addRow("Precio*:", self.price_edit)

        # Campo stock actual
        self.stock_edit = QLineEdit()
        basic_form.addRow("Stock Actual:", self.stock_edit)

        # Campo stock mínimo
        self.min_stock_edit = QLineEdit()
        basic_form.addRow("Stock Mínimo:", self.min_stock_edit)

        self.add_form_section("Información Básica", basic_form)

        # Descripción
        desc_form = QFormLayout()
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        desc_form.addRow("Descripción:", self.description_edit)

        self.add_form_section("Descripción", desc_form)

    def _load_categories(self):
        """Cargar categorías disponibles"""
        try:
            categorias = self.inventario_service.get_categorias_completas()
            self.category_combo.clear()
            self.category_combo.addItem("Seleccionar categoría", "")
            for categoria in categorias:
                nombre = categoria.get("nombre", "Sin nombre")
                categoria_id = categoria.get("id", "")
                self.category_combo.addItem(nombre, categoria_id)
        except Exception as e:
            logger.error(f"Error cargando categorías: {e}")

    def _load_product_data(self):
        """Cargar datos de producto para edición"""
        if self.producto_data:
            self.name_edit.setText(str(self.producto_data.get("nombre", "")))
            self.price_edit.setText(str(self.producto_data.get("precio", "")))
            self.stock_edit.setText(str(self.producto_data.get("stock_actual", "")))
            self.min_stock_edit.setText(str(self.producto_data.get("stock_minimo", "")))
            self.description_edit.setPlainText(
                str(self.producto_data.get("descripcion", ""))
            )

            # Seleccionar categoría
            categoria = self.producto_data.get("categoria", "")
            index = self.category_combo.findText(categoria)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)

    def accept(self):
        """Validar y guardar producto"""
        if not self._validate_form():
            return

        try:
            producto_data = {
                "nombre": self.name_edit.text().strip(),
                "categoria_id": self.category_combo.currentData(),
                "precio": float(self.price_edit.text().strip()),
                "stock_actual": int(self.stock_edit.text().strip() or "0"),
                "stock_minimo": int(self.min_stock_edit.text().strip() or "0"),
                "descripcion": self.description_edit.toPlainText().strip(),
            }

            if self.is_edit:
                producto_data["id"] = self.producto_data["id"]
                success = self.inventario_service.actualizar_producto(producto_data)
                message = "Producto actualizado correctamente"
            else:
                success = self.inventario_service.crear_producto(producto_data)
                message = "Producto creado correctamente"

            if success:
                self.show_success(message)
                super().accept()
            else:
                self.show_error("Error al guardar el producto")

        except ValueError as e:
            self.show_error("Error en los datos numéricos")
        except Exception as e:
            logger.error(f"Error guardando producto: {e}")
            self.show_error(f"Error inesperado: {str(e)}")

    def _validate_form(self) -> bool:
        """Validar formulario de producto"""
        # Validar nombre
        if not InventoryValidationUtils.validate_required_field(
            self.name_edit.text(), "Nombre"
        ):
            self.show_error("El nombre es obligatorio")
            self.name_edit.setFocus()
            return False

        # Validar categoría
        if self.category_combo.currentData() == "":
            self.show_error("Debe seleccionar una categoría")
            self.category_combo.setFocus()
            return False

        # Validar precio
        try:
            precio = float(self.price_edit.text().strip())
            if precio <= 0:
                self.show_error("El precio debe ser mayor a 0")
                self.price_edit.setFocus()
                return False
        except ValueError:
            self.show_error("El precio debe ser un número válido")
            self.price_edit.setFocus()
            return False

        return True
