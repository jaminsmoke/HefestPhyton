from typing import Optional, Dict, List, Any
import logging
from PyQt6.QtWidgets import (
from PyQt6.QtCore import Qt, pyqtSignal
from ..module_base_interface import BaseModule
from services.inventario_service_real import InventarioService
from .components import (
            from data.db_manager import DatabaseManager

"""
Módulo de Inventario con Pestañas - Versión Refactorizada
========================================================

Widget principal que organiza el inventario en pestañas separadas:
- Productos
- Categorías
- Proveedores
"""


    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QFrame,
    QTabWidget,
    QMessageBox,
)

    ProductsManagerWidget,
    CategoryManagerWidget,
    SupplierManagerWidget,
)

_ = logging.getLogger(__name__)


class InventarioModule(BaseModule):
    """
    Módulo de inventario con pestañas separadas
    """

    # Señales
    _ = pyqtSignal()

    def __init__(self, parent=None):
        """Inicializar el módulo de inventario refactorizado"""
        super().__init__(parent)

        # Intentar obtener db_manager
        try:

            self.db_manager = DatabaseManager()
            logger.info("InventarioModule: DatabaseManager creado correctamente")
        except Exception as e:
            logger.error("InventarioModule: Error creando DatabaseManager: %s", e)
            self.db_manager = None

        self.inventario_service = InventarioService(self.db_manager)

        # Configurar UI
        self.init_ui()

        logger.info("InventarioModule inicializado correctamente")

    def init_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicializar la interfaz de usuario"""
        self.setObjectName("InventarioModule")

        # Usar el layout principal de BaseModule
        if hasattr(self, "main_layout"):
            _ = self.main_layout
        else:
            layout = QVBoxLayout(self)

        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header del módulo
        header = self.create_header()
        layout.addWidget(header)

        # Widget de pestañas
        self.tab_widget = self.create_tab_widget()
        layout.addWidget(self.tab_widget)

        self.apply_styles()

    def create_header(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear el header principal del módulo"""
        header = QFrame()
        header.setObjectName("MainHeaderFrame")
        _ = QHBoxLayout(header)

        # Título principal
        title = QLabel("📦 Sistema de Inventario Profesional")
        title.setObjectName("MainModuleTitle")
        layout.addWidget(title)

        layout.addStretch()

        # Botones de acción global
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.clicked.connect(self.refresh_all_data)

        self.export_btn = QPushButton("📊 Exportar")
        self.export_btn.clicked.connect(self.export_inventory)

        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.export_btn)

        return header

    def create_tab_widget(self) -> QTabWidget:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear el widget de pestañas"""
        tab_widget = QTabWidget()
        tab_widget.setObjectName("InventoryTabWidget")

        # Pestaña de Productos
        self.products_widget = ProductsManagerWidget(self.inventario_service, self)
        tab_widget.addTab(self.products_widget, "📦 Productos")

        # Pestaña de Categorías
        self.categories_widget = CategoryManagerWidget(self.inventario_service, self)
        tab_widget.addTab(self.categories_widget, "🏷️ Categorías")

        # Pestaña de Proveedores
        self.suppliers_widget = SupplierManagerWidget(self.inventario_service, self)
        tab_widget.addTab(self.suppliers_widget, "🏢 Proveedores")

        # Conectar señales
        self.products_widget.producto_actualizado.connect(self.on_inventory_updated)
        self.categories_widget.categoria_actualizada.connect(self.on_categories_updated)
        self.suppliers_widget.proveedor_actualizado.connect(self.on_suppliers_updated)

        return tab_widget

    def refresh_all_data(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar todos los datos"""
        try:
            # Actualizar cada pestaña
            self.products_widget.load_products()
            self.categories_widget.load_categories()
            self.suppliers_widget.load_suppliers()

            QMessageBox.information(
                self, "Actualizado", "Todos los datos han sido actualizados"
            )

        except Exception as e:
            logger.error("Error actualizando datos: %s", e)
            QMessageBox.warning(self, "Error", f"Error actualizando datos: {str(e)}")

    def export_inventory(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Exportar inventario completo"""
        try:
            # Usar la funcionalidad de exportación del widget de productos
            self.products_widget.export_to_csv()

        except Exception as e:
            logger.error("Error exportando inventario: %s", e)
            QMessageBox.warning(self, "Error", f"Error exportando inventario: {str(e)}")

    def on_inventory_updated(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Manejar actualización de inventario"""
        self.inventario_actualizado.emit()

        # Actualizar categorías para reflejar cambios en productos
        self.categories_widget.update_statistics()

    def on_categories_updated(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Manejar actualización de categorías"""
        # Actualizar productos para reflejar cambios en categorías
        self.products_widget.load_categories()  # Recargar categorías en el widget de productos

    def on_suppliers_updated(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Manejar actualización de proveedores"""
        # Los proveedores pueden afectar a los productos en el futuro
        pass

    def get_module_name(self) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtener el nombre del módulo"""
        return "Inventario Refactorizado"
    
    def refresh(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza los datos del módulo de inventario"""
        try:
            self.refresh_all_data()
        except Exception as e:
            logger.error("Error refrescando módulo de inventario: %s", e)

    def cleanup(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Limpiar recursos"""
        try:
            # Limpiar widgets hijos
            if hasattr(self, "products_widget"):
                self.products_widget.cleanup()
            if hasattr(self, "categories_widget"):
                # No necesita cleanup específico
                pass
            if hasattr(self, "suppliers_widget"):
                # No necesita cleanup específico
                pass

        except Exception as e:
            logger.error("Error en cleanup: %s", e)

    def apply_styles(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Aplicar estilos al módulo"""
        self.setStyleSheet(
            """
            #MainHeaderFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }
            
            #MainModuleTitle {
                color: white;
                font-size: 28px;
                font-weight: bold;
            }
            
            #InventoryTabWidget {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            
            #InventoryTabWidget::pane {
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                background: white;
            }
            
            #InventoryTabWidget::tab-bar {
                alignment: left;
            }
            
            #InventoryTabWidget QTabBar::tab {
                background: #f8fafc;
                color: #4a5568;
                border: 1px solid #e2e8f0;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }
            
            #InventoryTabWidget QTabBar::tab:selected {
                background: white;
                color: #2d3748;
                border-bottom: 1px solid white;
            }
            
            #InventoryTabWidget QTabBar::tab:hover:!selected {
                background: #edf2f7;
            }
            
            QPushButton {
                background: #4a5568;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background: #2d3748;
            }
        """
        )
