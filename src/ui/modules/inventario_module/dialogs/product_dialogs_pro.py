"""
Diálogos profesionales para el módulo de inventario - Hefest v0.0.12
=====================================================================

Este módulo contiene todos los diálogos de entrada de datos para el sistema
de inventario de Hefest, específicamente diseñados para hostelería.

CLASES PRINCIPALES:
------------------
- ProductDialog: Clase base para diálogos de productos
- NewProductDialog: Crear nuevos productos
- EditProductDialog: Editar productos existentes
- StockAdjustmentDialog: Ajustar inventario/stock
- DeleteConfirmationDialog: Confirmar eliminación de productos

CARACTERÍSTICAS:
---------------
- Validación de datos en tiempo real
- Integración con inventario_service_real.py
- Interfaz moderna con PyQt6
- Categorías específicas para hostelería
- Gestión de precios con IVA incluido
- Cálculos automáticos de márgenes

DEPENDENCIAS:
------------
- services.inventario_service_real: Servicio de datos
- PyQt6: Framework de interfaz gráfica
- utils.modern_styles: Estilos modernos personalizados

AUTOR: Hefest Development Team
FECHA: Diciembre 2024
VERSIÓN: v0.0.12
"""

import logging
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGridLayout,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QDoubleSpinBox,
    QPushButton,
    QLabel,
    QTextEdit,
    QFrame,
    QMessageBox,
    QDialogButtonBox,
    QGroupBox,
    QCheckBox,
    QDateEdit,
    QWidget,
    QScrollArea,
)
from PyQt6.QtCore import Qt, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QIcon

from services.inventario_service_real import Producto

logger = logging.getLogger(__name__)


class ProductDialog(QDialog):
    """Diálogo base profesional para productos con diseño moderno"""

    def __init__(self, parent=None, title="Producto", inventario_service=None):
        super().__init__(parent)
        self.setObjectName("ProductDialog")
        self.inventario_service = inventario_service
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(800, 900)  # Tamaño más grande para mejor visualización

        self.setup_ui()
        self.apply_styles()
        self.load_initial_data()

    def setup_ui(self):
        """Configurar la interfaz de usuario profesional"""
        self.setFixedSize(750, 850)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = self.create_header()
        layout.addWidget(header)

        # Contenido principal con scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Widget contenedor del contenido
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)
        content_layout.setContentsMargins(25, 25, 25, 25)

        # Información básica
        basic_group = self.create_basic_info_group()
        content_layout.addWidget(basic_group)

        # Información comercial
        commercial_group = self.create_commercial_info_group()
        content_layout.addWidget(commercial_group)

        # Información de inventario
        inventory_group = self.create_inventory_info_group()
        content_layout.addWidget(inventory_group)

        # Información adicional
        additional_group = self.create_additional_info_group()
        content_layout.addWidget(additional_group)

        # Stretch al final
        content_layout.addStretch()

        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)

        # Footer con botones
        footer = self.create_footer()
        layout.addWidget(footer)

    def create_header(self) -> QFrame:
        """Crear header profesional"""
        header = QFrame()
        header.setObjectName("DialogHeader")
        header.setFixedHeight(80)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(30, 0, 30, 0)

        # Icono y título
        icon_label = QLabel("📦")
        icon_label.setFont(QFont("Segoe UI Emoji", 24))

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)

        title = QLabel(self.windowTitle())
        title.setObjectName("DialogTitle")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))

        subtitle = QLabel("Complete la información del producto")
        subtitle.setObjectName("DialogSubtitle")
        subtitle.setFont(QFont("Segoe UI", 11))

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        layout.addWidget(icon_label)
        layout.addLayout(title_layout)
        layout.addStretch()

        return header

    def create_basic_info_group(self) -> QFrame:
        """Crear grupo de información básica usando QFrame simple"""
        frame = QFrame()
        frame.setObjectName("BasicInfoFrame")
        frame.setStyleSheet(
            """
            #BasicInfoFrame {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 20px;
                margin: 10px 0px;
            }
        """
        )

        layout = QVBoxLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título del grupo
        title_label = QLabel("📋 Información Básica")
        title_label.setObjectName("GroupTitle")
        title_label.setStyleSheet(
            """
            #GroupTitle {
                font-size: 16px;
                font-weight: bold;
                color: #1e293b;
                padding: 10px 0px;
            }
        """
        )
        layout.addWidget(title_label)

        # Grid para los campos
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        grid_layout.setColumnStretch(1, 1)

        # Nombre del producto
        nombre_label = QLabel("* Nombre del producto:")
        nombre_label.setStyleSheet("font-weight: 500; color: #374151;")
        nombre_label.setMinimumWidth(150)
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ej: Coca Cola 330ml, Pizza Margherita...")
        self.nombre_input.textChanged.connect(self.validate_form)
        grid_layout.addWidget(nombre_label, 0, 0)
        grid_layout.addWidget(self.nombre_input, 0, 1)

        # Categoría
        categoria_label = QLabel("* Categoría:")
        categoria_label.setStyleSheet("font-weight: 500; color: #374151;")
        categoria_label.setMinimumWidth(150)
        self.categoria_combo = QComboBox()
        self.categoria_combo.setEditable(True)
        self.categoria_combo.setPlaceholderText("Seleccionar o crear nueva categoría")
        self.categoria_combo.currentTextChanged.connect(self.validate_form)
        grid_layout.addWidget(categoria_label, 1, 0)
        grid_layout.addWidget(self.categoria_combo, 1, 1)

        # Código/SKU
        codigo_label = QLabel("Código/SKU:")
        codigo_label.setStyleSheet("font-weight: 500; color: #374151;")
        codigo_label.setMinimumWidth(150)
        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("Código interno del producto (opcional)")
        grid_layout.addWidget(codigo_label, 2, 0)
        grid_layout.addWidget(self.codigo_input, 2, 1)

        # Descripción
        descripcion_label = QLabel("Descripción:")
        descripcion_label.setStyleSheet("font-weight: 500; color: #374151;")
        descripcion_label.setMinimumWidth(150)
        descripcion_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.descripcion_input = QTextEdit()
        self.descripcion_input.setMaximumHeight(80)
        self.descripcion_input.setPlaceholderText(
            "Descripción detallada del producto..."
        )
        grid_layout.addWidget(descripcion_label, 3, 0)
        grid_layout.addWidget(self.descripcion_input, 3, 1)

        layout.addLayout(grid_layout)
        return frame

    def create_commercial_info_group(self) -> QFrame:
        """Crear sección de información comercial"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                margin: 10px 0px;
                padding: 10px;
            }
        """
        )

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título de la sección
        title_label = QLabel("💰 Información Comercial")
        title_label.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            color: #1e293b;
            background: white;
            padding: 5px 10px;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            margin-bottom: 10px;
        """
        )
        layout.addWidget(title_label)

        # Grid layout para los campos
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(3, 1)

        # Precio de compra
        precio_compra_label = QLabel("Precio de compra:")
        precio_compra_label.setStyleSheet("font-weight: 500; color: #374151;")
        precio_compra_label.setMinimumWidth(120)
        self.precio_compra_input = QDoubleSpinBox()
        self.precio_compra_input.setRange(0.00, 999999.99)
        self.precio_compra_input.setDecimals(2)
        self.precio_compra_input.setSuffix(" €")
        self.precio_compra_input.valueChanged.connect(self.calculate_margin)
        grid_layout.addWidget(precio_compra_label, 0, 0)
        grid_layout.addWidget(self.precio_compra_input, 0, 1)

        # Precio de venta
        precio_venta_label = QLabel("* Precio de venta:")
        precio_venta_label.setStyleSheet("font-weight: 500; color: #374151;")
        precio_venta_label.setMinimumWidth(120)
        self.precio_input = QDoubleSpinBox()
        self.precio_input.setRange(0.01, 999999.99)
        self.precio_input.setDecimals(2)
        self.precio_input.setSuffix(" €")
        self.precio_input.valueChanged.connect(self.calculate_margin)
        self.precio_input.valueChanged.connect(self.validate_form)
        grid_layout.addWidget(precio_venta_label, 0, 2)
        grid_layout.addWidget(self.precio_input, 0, 3)

        # Margen de beneficio
        margen_label = QLabel("Margen de beneficio:")
        margen_label.setStyleSheet("font-weight: 500; color: #374151;")
        margen_label.setMinimumWidth(120)
        self.margen_label = QLabel("0.00%")
        self.margen_label.setObjectName("MarginLabel")
        self.margen_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        grid_layout.addWidget(margen_label, 1, 0)
        grid_layout.addWidget(self.margen_label, 1, 1)

        # IVA
        iva_label = QLabel("IVA (%):")
        iva_label.setStyleSheet("font-weight: 500; color: #374151;")
        iva_label.setMinimumWidth(120)
        self.iva_input = QDoubleSpinBox()
        self.iva_input.setRange(0.00, 100.00)
        self.iva_input.setDecimals(2)
        self.iva_input.setValue(21.00)  # IVA estándar España
        self.iva_input.setSuffix("%")
        grid_layout.addWidget(iva_label, 1, 2)
        grid_layout.addWidget(self.iva_input, 1, 3)

        # Proveedor
        proveedor_label = QLabel("Proveedor:")
        proveedor_label.setStyleSheet("font-weight: 500; color: #374151;")
        proveedor_label.setMinimumWidth(120)
        self.proveedor_combo = QComboBox()
        self.proveedor_combo.setEditable(True)
        self.proveedor_combo.setPlaceholderText("Seleccionar proveedor")
        grid_layout.addWidget(proveedor_label, 2, 0)
        grid_layout.addWidget(self.proveedor_combo, 2, 1, 1, 3)

        layout.addLayout(grid_layout)
        return frame

    def create_inventory_info_group(self) -> QFrame:
        """Crear sección de gestión de inventario"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                margin: 10px 0px;
                padding: 10px;
            }
        """
        )

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título de la sección
        title_label = QLabel("📊 Gestión de Inventario")
        title_label.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            color: #1e293b;
            background: white;
            padding: 5px 10px;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            margin-bottom: 10px;
        """
        )
        layout.addWidget(title_label)

        # Grid layout para los campos
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(3, 1)

        # Stock actual
        stock_actual_label = QLabel("Stock actual:")
        stock_actual_label.setStyleSheet("font-weight: 500; color: #374151;")
        stock_actual_label.setMinimumWidth(120)
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 999999)
        self.stock_input.setSuffix(" unidades")
        grid_layout.addWidget(stock_actual_label, 0, 0)
        grid_layout.addWidget(self.stock_input, 0, 1)

        # Stock mínimo
        stock_min_label = QLabel("Stock mínimo:")
        stock_min_label.setStyleSheet("font-weight: 500; color: #374151;")
        stock_min_label.setMinimumWidth(120)
        self.stock_min_input = QSpinBox()
        self.stock_min_input.setRange(0, 999999)
        self.stock_min_input.setValue(5)
        self.stock_min_input.setSuffix(" unidades")
        grid_layout.addWidget(stock_min_label, 0, 2)
        grid_layout.addWidget(self.stock_min_input, 0, 3)

        # Stock máximo
        stock_max_label = QLabel("Stock máximo:")
        stock_max_label.setStyleSheet("font-weight: 500; color: #374151;")
        stock_max_label.setMinimumWidth(120)
        self.stock_max_input = QSpinBox()
        self.stock_max_input.setRange(0, 999999)
        self.stock_max_input.setValue(100)
        self.stock_max_input.setSuffix(" unidades")
        grid_layout.addWidget(stock_max_label, 1, 0)
        grid_layout.addWidget(self.stock_max_input, 1, 1)

        # Ubicación
        ubicacion_label = QLabel("Ubicación:")
        ubicacion_label.setStyleSheet("font-weight: 500; color: #374151;")
        ubicacion_label.setMinimumWidth(120)
        self.ubicacion_input = QLineEdit()
        self.ubicacion_input.setPlaceholderText("Ej: Estante A-1, Nevera 2...")
        grid_layout.addWidget(ubicacion_label, 1, 2)
        grid_layout.addWidget(self.ubicacion_input, 1, 3)

        # Unidad de medida
        unidad_label = QLabel("Unidad de medida:")
        unidad_label.setStyleSheet("font-weight: 500; color: #374151;")
        unidad_label.setMinimumWidth(120)
        self.unidad_combo = QComboBox()
        self.unidad_combo.addItems(
            [
                "Unidades",
                "Kg",
                "Gramos",
                "Litros",
                "Ml",
                "Cajas",
                "Paquetes",
                "Botellas",
                "Latas",
            ]
        )
        grid_layout.addWidget(unidad_label, 2, 0)
        grid_layout.addWidget(self.unidad_combo, 2, 1)

        # Estado
        estado_label = QLabel("Estado:")
        estado_label.setStyleSheet("font-weight: 500; color: #374151;")
        estado_label.setMinimumWidth(120)
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Activo", "Inactivo", "Descontinuado", "Agotado"])
        grid_layout.addWidget(estado_label, 2, 2)
        grid_layout.addWidget(self.estado_combo, 2, 3)

        layout.addLayout(grid_layout)
        return frame

    def create_additional_info_group(self) -> QFrame:
        """Crear sección de información adicional"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(
            """
            QFrame {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                margin: 10px 0px;
                padding: 10px;
            }
        """
        )

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Título de la sección
        title_label = QLabel("📝 Información Adicional")
        title_label.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            color: #1e293b;
            background: white;
            padding: 5px 10px;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            margin-bottom: 10px;
        """
        )
        layout.addWidget(title_label)

        # Grid layout para los campos
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        grid_layout.setColumnStretch(1, 1)
        grid_layout.setColumnStretch(3, 1)

        # Fecha de caducidad
        from PyQt6.QtWidgets import QDateEdit
        from PyQt6.QtCore import QDate

        fecha_label = QLabel("Fecha de caducidad:")
        fecha_label.setStyleSheet("font-weight: 500; color: #374151;")
        fecha_label.setMinimumWidth(120)
        self.caducidad_input = QDateEdit()
        self.caducidad_input.setDate(QDate.currentDate().addDays(30))
        self.caducidad_input.setCalendarPopup(True)
        grid_layout.addWidget(fecha_label, 0, 0)
        grid_layout.addWidget(self.caducidad_input, 0, 1)

        # Es perecedero
        perecedero_label = QLabel("Producto perecedero:")
        perecedero_label.setStyleSheet("font-weight: 500; color: #374151;")
        perecedero_label.setMinimumWidth(120)
        self.perecedero_checkbox = QCheckBox()
        self.perecedero_checkbox.stateChanged.connect(self.on_perecedero_changed)
        grid_layout.addWidget(perecedero_label, 0, 2)
        grid_layout.addWidget(self.perecedero_checkbox, 0, 3)

        # Notas
        notas_label = QLabel("Notas:")
        notas_label.setStyleSheet("font-weight: 500; color: #374151;")
        notas_label.setMinimumWidth(120)
        notas_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.notas_input = QTextEdit()
        self.notas_input.setMaximumHeight(80)
        self.notas_input.setPlaceholderText(
            "Notas adicionales, alergenos, instrucciones especiales..."
        )
        grid_layout.addWidget(notas_label, 1, 0)
        grid_layout.addWidget(self.notas_input, 1, 1, 1, 3)

        layout.addLayout(grid_layout)
        return frame

    def create_footer(self) -> QFrame:
        """Crear footer con botones de acción"""
        footer = QFrame()
        footer.setObjectName("DialogFooter")
        footer.setFixedHeight(70)

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(30, 0, 30, 0)

        # Información de validación
        self.validation_label = QLabel("")
        self.validation_label.setObjectName("ValidationLabel")
        layout.addWidget(self.validation_label)

        layout.addStretch()

        # Botones
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setObjectName("SecondaryButton")
        self.cancel_btn.clicked.connect(self.reject)

        self.accept_btn = QPushButton("Guardar Producto")
        self.accept_btn.setObjectName("PrimaryButton")
        self.accept_btn.clicked.connect(self.accept_product)
        self.accept_btn.setEnabled(False)

        layout.addWidget(self.cancel_btn)
        layout.addWidget(self.accept_btn)

        return footer

    def apply_styles(self):
        """Aplicar estilos al diálogo"""
        self.setStyleSheet(
            """
            QDialog {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }
            
            #DialogHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #4f46e5, stop:1 #7c3aed);
                border-radius: 8px 8px 0 0;
                padding: 15px 20px;
            }
            
            #DialogTitle {
                color: white;
                font-weight: bold;
            }
            
            #DialogSubtitle {
                color: rgba(255, 255, 255, 0.9);
            }
            
            QGroupBox {
                font-weight: bold;
                color: #374151;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                margin: 15px 0px;
                padding-top: 25px;
                min-height: 120px;
                font-size: 14px;
                background: white;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 5px 15px;
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 4px;
                top: -12px;
                font-weight: bold;
                color: #1e293b;
            }
            
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
                padding: 10px 14px;
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                font-size: 14px;
                background: white;
                min-height: 20px;
            }
            
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, 
            QDoubleSpinBox:focus, QTextEdit:focus {
                border-color: #4f46e5;
                outline: none;
                background: #fefefe;
            }
            
            QLabel {
                color: #374151;
                font-size: 14px;
                font-weight: 500;
                padding: 2px 0px;
            }
            
            QDateEdit {
                padding: 10px 14px;
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                font-size: 14px;
                background: white;
                min-height: 20px;
            }
            
            QDateEdit:focus {
                border-color: #4f46e5;
                outline: none;
                background: #fefefe;
            }
            
            QCheckBox {
                font-size: 14px;
                color: #374151;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #e2e8f0;
                border-radius: 4px;
                background: white;
            }
            
            QCheckBox::indicator:checked {
                background: #4f46e5;
                border-color: #4f46e5;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOSIgdmlld0JveD0iMCAwIDEyIDkiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xMSAxTDQgOEwxIDUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
            
            #PrimaryButton {
                background: #4f46e5;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
                min-width: 100px;
            }
            
            #PrimaryButton:hover {
                background: #4338ca;
            }
            
            #PrimaryButton:pressed {
                background: #3730a3;
            }
            
            #SecondaryButton {
                background: white;
                color: #374151;
                border: 2px solid #e2e8f0;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
                min-width: 100px;
            }
            
            #SecondaryButton:hover {
                background: #f8fafc;
                border-color: #cbd5e1;
            }
            
            #SecondaryButton:pressed {
                background: #f1f5f9;
            }
            
            #DialogFooter {
                background: #f8fafc;
                border-top: 1px solid #e2e8f0;
                border-radius: 0 0 8px 8px;
            }
            
            #ValidationLabel {
                font-size: 12px;
                padding: 4px 8px;
                border-radius: 4px;
            }
            
            #MarginLabel {
                font-size: 12px;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
                background: #f1f5f9;
            }
        """
        )

    def set_categories(self, categories: list):
        """Establecer las categorías disponibles"""
        self.categoria_combo.clear()
        self.categoria_combo.addItems(categories)

    def accept_product(self):
        """Validar y aceptar el producto"""
        if not self.validate_form():
            return
        self.accept()

    def load_initial_data(self):
        """Cargar datos iniciales (categorías, proveedores)"""
        try:
            if self.inventario_service:
                # Cargar categorías
                categorias = self.inventario_service.get_categorias()
                categoria_names = [
                    cat.get("nombre", cat) if isinstance(cat, dict) else str(cat)
                    for cat in categorias
                ]
                self.categoria_combo.addItems(categoria_names)

                # Cargar proveedores
                proveedores = self.inventario_service.get_proveedores()
                proveedor_names = [
                    (
                        prov.get("nombre", str(prov))
                        if isinstance(prov, dict)
                        else str(prov)
                    )
                    for prov in proveedores
                ]
                self.proveedor_combo.addItems(proveedor_names)

        except Exception as e:
            logger.error(f"Error cargando datos iniciales: {e}")

    def calculate_margin(self):
        """Calcular margen de beneficio automáticamente"""
        try:
            precio_compra = self.precio_compra_input.value()
            precio_venta = self.precio_input.value()

            if precio_compra > 0 and precio_venta > 0:
                margen = ((precio_venta - precio_compra) / precio_compra) * 100
                self.margen_label.setText(f"{margen:.2f}%")

                # Cambiar color según el margen
                if margen < 10:
                    color = "#ef4444"  # Rojo
                elif margen < 30:
                    color = "#f59e0b"  # Amarillo
                else:
                    color = "#10b981"  # Verde                self.margen_label.setStyleSheet(f"color: {color}; font-weight: bold;")
            else:
                self.margen_label.setText("0.00%")
                self.margen_label.setStyleSheet("color: #6b7280;")

        except Exception as e:
            logger.error(f"Error calculando margen: {e}")

    def on_perecedero_changed(self, state):
        """Manejar cambio en checkbox de producto perecedero"""
        is_perecedero = state == Qt.CheckState.Checked.value
        self.caducidad_input.setEnabled(is_perecedero)

        if not is_perecedero:
            # Si no es perecedero, poner fecha muy lejana
            self.caducidad_input.setDate(QDate.currentDate().addYears(10))

    def validate_form(self):
        """Validar formulario en tiempo real"""
        is_valid = True
        errors = []

        # Validar nombre
        nombre = self.nombre_input.text().strip()
        if not nombre:
            errors.append("El nombre es obligatorio")
            is_valid = False

        # Validar categoría
        categoria = self.categoria_combo.currentText().strip()
        if not categoria:
            errors.append("La categoría es obligatoria")
            is_valid = False

        # Validar precio
        precio = self.precio_input.value()
        if precio <= 0:
            errors.append("El precio debe ser mayor a 0")
            is_valid = False

        # Actualizar UI
        self.accept_btn.setEnabled(is_valid)

        if errors:
            self.validation_label.setText("⚠️ " + "; ".join(errors))
            self.validation_label.setStyleSheet("color: #ef4444; font-size: 12px;")
        else:
            self.validation_label.setText("✅ Formulario válido")
            self.validation_label.setStyleSheet("color: #10b981; font-size: 12px;")

        return is_valid

    def get_product_data(self) -> Dict[str, Any]:
        """Obtener los datos completos del producto"""
        return {
            "nombre": self.nombre_input.text().strip(),
            "categoria": self.categoria_combo.currentText().strip(),
            "codigo": self.codigo_input.text().strip(),
            "descripcion": self.descripcion_input.toPlainText().strip(),
            "precio_compra": self.precio_compra_input.value(),
            "precio": self.precio_input.value(),
            "iva": self.iva_input.value(),
            "proveedor": self.proveedor_combo.currentText().strip(),
            "stock_actual": self.stock_input.value(),
            "stock_minimo": self.stock_min_input.value(),
            "stock_maximo": self.stock_max_input.value(),
            "ubicacion": self.ubicacion_input.text().strip(),
            "unidad_medida": self.unidad_combo.currentText(),
            "estado": self.estado_combo.currentText(),
            "fecha_caducidad": self.caducidad_input.date().toString("yyyy-MM-dd"),
            "es_perecedero": self.perecedero_checkbox.isChecked(),
            "notas": self.notas_input.toPlainText().strip(),
        }


class NewProductDialog(ProductDialog):
    """Diálogo para crear un nuevo producto"""

    def __init__(self, parent=None, categories=None, inventario_service=None):
        super().__init__(parent, "Nuevo Producto", inventario_service)

        if categories:
            self.set_categories(categories)  # Enfocar el primer campo
        self.nombre_input.setFocus()

    def accept_product(self):
        """Validar y guardar el nuevo producto"""
        if not self.validate_form():
            return

        try:
            # Obtener datos del formulario
            product_data = self.get_product_data()

            # Guardar producto usando el servicio de inventario
            if self.inventario_service:
                # Crear producto usando los parámetros correctos del servicio
                nuevo_producto = self.inventario_service.crear_producto(
                    nombre=product_data["nombre"],
                    categoria=product_data["categoria"],
                    precio=product_data["precio"],
                    stock_inicial=product_data["stock_actual"],
                    stock_minimo=product_data["stock_minimo"],
                )

                if nuevo_producto:
                    logger.info(
                        f"Producto '{product_data['nombre']}' creado exitosamente con ID: {nuevo_producto.id}"
                    )

                    # Mostrar mensaje de éxito
                    from PyQt6.QtWidgets import QMessageBox

                    QMessageBox.information(
                        self,
                        "✅ Producto Creado",
                        f"El producto '{product_data['nombre']}' ha sido creado exitosamente.\n\n"
                        f"ID: {nuevo_producto.id}\n"
                        f"Categoría: {nuevo_producto.categoria}\n"
                        f"Precio: €{nuevo_producto.precio:.2f}\n"
                        f"Stock inicial: {nuevo_producto.stock_actual} unidades",
                    )

                    # Cerrar diálogo
                    self.accept()
                else:
                    logger.error("Error al crear producto en la base de datos")
                    from PyQt6.QtWidgets import QMessageBox

                    QMessageBox.warning(
                        self,
                        "❌ Error al Guardar",
                        "No se pudo guardar el producto en la base de datos.\n\n"
                        "Posibles causas:\n"
                        "• Problema de conexión con la base de datos\n"
                        "• Datos inválidos\n"
                        "• Producto duplicado\n\n"
                        "Verifique los datos e intente nuevamente.",
                    )
            else:
                logger.error("No hay servicio de inventario disponible")
                from PyQt6.QtWidgets import QMessageBox

                QMessageBox.warning(
                    self,
                    "❌ Error de Configuración",
                    "No hay servicio de inventario disponible.\n\n"
                    "El sistema no puede guardar productos en este momento.\n"
                    "Contacte al administrador del sistema.",
                )

        except Exception as e:
            logger.error(f"Error al guardar producto: {e}")
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.critical(
                self,
                "❌ Error Inesperado",
                f"Ocurrió un error inesperado al guardar el producto:\n\n"
                f"{str(e)}\n\n"
                f"Por favor, intente nuevamente o contacte al soporte técnico.",
            )


class EditProductDialog(ProductDialog):
    """Diálogo para editar un producto existente"""

    def __init__(
        self,
        parent=None,
        producto: Optional[Producto] = None,
        categories=None,
        inventario_service=None,
    ):
        super().__init__(parent, "Editar Producto", inventario_service)

        if categories:
            self.set_categories(categories)

        if producto:
            self.load_product_data(producto)

        self.nombre_input.setFocus()
        self.nombre_input.selectAll()

    def load_product_data(self, producto: Producto):
        """Cargar datos del producto en el formulario"""
        # Guardar referencia al producto original para el método accept_product
        self._original_producto = producto

        self.nombre_input.setText(producto.nombre)

        # Buscar la categoría en el combo o agregarla si no existe
        index = self.categoria_combo.findText(producto.categoria)
        if index >= 0:
            self.categoria_combo.setCurrentIndex(index)
        else:
            self.categoria_combo.addItem(producto.categoria)
            self.categoria_combo.setCurrentText(producto.categoria)

        self.precio_input.setValue(producto.precio)
        self.stock_input.setValue(producto.stock_actual)
        self.stock_min_input.setValue(producto.stock_minimo)

    def accept_product(self):
        """Validar y guardar cambios en el producto existente"""
        if not self.validate_form():
            return

        try:
            # Obtener datos del formulario
            product_data = self.get_product_data()
            # Actualizar producto usando el servicio de inventario
            if self.inventario_service and hasattr(
                self, "_original_producto"
            ):  # Usar el método actualizar_producto del servicio
                success = self.inventario_service.actualizar_producto(
                    producto_id=self._original_producto.id,
                    nombre=product_data["nombre"],
                    categoria=product_data["categoria"],
                    precio=product_data["precio"],
                    stock=product_data["stock_actual"],
                    stock_minimo=product_data["stock_minimo"],
                )

                if success:
                    logger.info(
                        f"Producto '{product_data['nombre']}' actualizado exitosamente"
                    )

                    # Mostrar mensaje de éxito
                    from PyQt6.QtWidgets import QMessageBox

                    QMessageBox.information(
                        self,
                        "✅ Producto Actualizado",
                        f"El producto '{product_data['nombre']}' ha sido actualizado correctamente.",
                    )

                    # Cerrar diálogo con código de aceptación
                    self.accept()
                else:
                    from PyQt6.QtWidgets import QMessageBox

                    QMessageBox.warning(
                        self,
                        "❌ Error",
                        "No se pudo actualizar el producto. Por favor, inténtelo de nuevo.",
                    )
            else:
                from PyQt6.QtWidgets import QMessageBox

                QMessageBox.warning(
                    self, "❌ Error", "Servicio de inventario no disponible."
                )

        except Exception as e:
            logger.error(f"Error actualizando producto: {e}")
            from PyQt6.QtWidgets import QMessageBox

            QMessageBox.critical(
                self,
                "❌ Error Crítico",
                f"Error inesperado al actualizar el producto:\n{str(e)}",
            )


class StockAdjustmentDialog(QDialog):
    """Diálogo para ajustar el stock de un producto"""

    def __init__(self, parent=None, producto: Optional[Producto] = None):
        super().__init__(parent)
        self.producto = producto
        self.setWindowTitle("Ajustar Stock")
        self.setModal(True)
        self.setFixedSize(450, 400)

        self.setup_ui()
        self.apply_styles()

        if producto:
            self.load_product_info(producto)

    def setup_ui(self):
        """Configurar interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QFrame()
        header.setObjectName("DialogHeader")
        header.setFixedHeight(60)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Ajustar Stock")
        title.setObjectName("DialogTitle")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))

        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addWidget(header)

        # Información del producto
        info_group = QGroupBox("Información del Producto")
        info_layout = QFormLayout(info_group)

        self.producto_label = QLabel("N/A")
        self.producto_label.setStyleSheet("font-weight: bold; color: #1f2937;")
        info_layout.addRow("Producto:", self.producto_label)

        self.stock_actual_label = QLabel("0")
        self.stock_actual_label.setStyleSheet("font-weight: bold; color: #059669;")
        info_layout.addRow("Stock Actual:", self.stock_actual_label)

        self.stock_minimo_label = QLabel("0")
        self.stock_minimo_label.setStyleSheet("color: #6b7280;")
        info_layout.addRow("Stock Mínimo:", self.stock_minimo_label)

        layout.addWidget(info_group)

        # Ajuste de stock
        adjust_group = QGroupBox("Ajuste de Stock")
        adjust_layout = QFormLayout(adjust_group)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems(["Entrada", "Salida", "Ajuste Manual"])
        self.tipo_combo.currentTextChanged.connect(self.on_tipo_changed)
        adjust_layout.addRow("Tipo de Movimiento:", self.tipo_combo)

        self.cantidad_input = QSpinBox()
        self.cantidad_input.setRange(1, 999999)
        self.cantidad_input.valueChanged.connect(self.update_preview)
        adjust_layout.addRow("Cantidad:", self.cantidad_input)

        self.nuevo_stock_label = QLabel("0")
        self.nuevo_stock_label.setStyleSheet(
            "font-weight: bold; font-size: 14px; color: #4f46e5;"
        )
        adjust_layout.addRow("Nuevo Stock:", self.nuevo_stock_label)

        self.observaciones_input = QTextEdit()
        self.observaciones_input.setMaximumHeight(60)
        self.observaciones_input.setPlaceholderText("Motivo del ajuste...")
        adjust_layout.addRow("Observaciones:", self.observaciones_input)

        layout.addWidget(adjust_group)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setObjectName("SecondaryButton")
        cancel_btn.clicked.connect(self.reject)

        self.accept_btn = QPushButton("Aplicar Ajuste")
        self.accept_btn.setObjectName("PrimaryButton")
        self.accept_btn.clicked.connect(self.accept_adjustment)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.accept_btn)

        layout.addLayout(button_layout)

    def apply_styles(self):
        """Aplicar estilos al diálogo"""
        self.setStyleSheet(
            """
            QDialog {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
            
            #DialogHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #f59e0b, stop:1 #f97316);
                border-radius: 8px 8px 0 0;
                padding: 15px 20px;
            }
            
            #DialogTitle {
                color: white;
                font-weight: bold;
            }
            
            QGroupBox {
                font-weight: bold;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background: white;
            }
            
            #PrimaryButton {
                background: #f59e0b;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }
            
            #PrimaryButton:hover {
                background: #d97706;
            }
            
            #SecondaryButton {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            
            #SecondaryButton:hover {
                background: #e5e7eb;
            }
        """
        )

    def load_product_info(self, producto: Producto):
        """Cargar información del producto"""
        self.producto_label.setText(producto.nombre)
        self.stock_actual_label.setText(str(producto.stock_actual))
        self.stock_minimo_label.setText(str(producto.stock_minimo))
        self.update_preview()

    def on_tipo_changed(self, tipo: str):
        """Manejar cambio de tipo de movimiento"""
        if tipo == "Entrada":
            self.cantidad_input.setPrefix("+ ")
            self.accept_btn.setText("Agregar Stock")
        elif tipo == "Salida":
            self.cantidad_input.setPrefix("- ")
            self.accept_btn.setText("Reducir Stock")
        else:  # Ajuste Manual
            self.cantidad_input.setPrefix("")
            self.accept_btn.setText("Ajustar Stock")

        self.update_preview()

    def update_preview(self):
        """Actualizar vista previa del nuevo stock"""
        if not self.producto:
            return

        tipo = self.tipo_combo.currentText()
        cantidad = self.cantidad_input.value()
        stock_actual = self.producto.stock_actual

        if tipo == "Entrada":
            nuevo_stock = stock_actual + cantidad
        elif tipo == "Salida":
            nuevo_stock = max(0, stock_actual - cantidad)
        else:  # Ajuste Manual
            nuevo_stock = cantidad

        self.nuevo_stock_label.setText(str(nuevo_stock))

        # Cambiar color según el estado
        if nuevo_stock == 0:
            color = "#ef4444"  # Rojo
        elif nuevo_stock <= self.producto.stock_minimo:
            color = "#f59e0b"  # Amarillo
        else:
            color = "#059669"  # Verde

        self.nuevo_stock_label.setStyleSheet(
            f"font-weight: bold; font-size: 14px; color: {color};"
        )

    def accept_adjustment(self):
        """Validar y aceptar el ajuste"""
        if not self.validate_adjustment():
            return
        self.accept()

    def validate_adjustment(self) -> bool:
        """Validar el ajuste de stock"""
        if not self.producto:
            return False

        tipo = self.tipo_combo.currentText()
        cantidad = self.cantidad_input.value()

        if cantidad <= 0:
            QMessageBox.warning(self, "Error", "La cantidad debe ser mayor a cero.")
            self.cantidad_input.setFocus()
            return False

        if tipo == "Salida" and cantidad > self.producto.stock_actual:
            reply = QMessageBox.question(
                self,
                "Stock insuficiente",
                f"La cantidad a retirar ({cantidad}) es mayor al stock actual ({self.producto.stock_actual}).\n"
                "¿Deseas continuar? El stock resultante será 0.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.No:
                return False
        return True

    def get_adjustment_data(self) -> Dict[str, Any]:
        """Obtener los datos del ajuste"""
        if not self.producto:
            return {}

        tipo = self.tipo_combo.currentText()
        cantidad = self.cantidad_input.value()
        stock_actual = self.producto.stock_actual

        if tipo == "Entrada":
            nuevo_stock = stock_actual + cantidad
        elif tipo == "Salida":
            nuevo_stock = max(0, stock_actual - cantidad)
        else:  # Ajuste Manual
            nuevo_stock = cantidad

        return {
            "tipo": tipo.lower().replace(" ", "_"),
            "cantidad": cantidad,
            "nuevo_stock": nuevo_stock,
            "nueva_cantidad": nuevo_stock,  # Alias para compatibilidad
            "observaciones": self.observaciones_input.toPlainText().strip(),
        }


class DeleteConfirmationDialog(QDialog):
    """Diálogo de confirmación para eliminar producto"""

    def __init__(self, parent=None, producto: Optional[Producto] = None):
        super().__init__(parent)
        self.producto = producto
        self.setWindowTitle("Confirmar Eliminación")
        self.setModal(True)
        self.setFixedSize(400, 300)

        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        """Configurar interfaz de usuario"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header = QFrame()
        header.setObjectName("DangerHeader")
        header.setFixedHeight(60)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("⚠️ Confirmar Eliminación")
        title.setObjectName("DialogTitle")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))

        header_layout.addWidget(title)
        header_layout.addStretch()

        layout.addWidget(header)

        # Mensaje de advertencia
        warning_label = QLabel()
        if self.producto:
            warning_label.setText(
                f"¿Estás seguro de que deseas eliminar el producto '{self.producto.nombre}'?\n\n"
                f"Información del producto:\n"
                f"• Categoría: {self.producto.categoria}\n"
                f"• Stock actual: {self.producto.stock_actual}\n"
                f"• Precio: €{self.producto.precio:.2f}\n\n"
                f"Esta acción no se puede deshacer."
            )
        else:
            warning_label.setText(
                "¿Estás seguro de que deseas eliminar este producto?\n\nEsta acción no se puede deshacer."
            )

        warning_label.setStyleSheet(
            """
            QLabel {
                color: #374151;
                font-size: 14px;
                line-height: 1.5;
                padding: 20px;
                background: #fef2f2;
                border: 1px solid #fecaca;
                border-radius: 8px;
            }
        """
        )
        warning_label.setWordWrap(True)

        layout.addWidget(warning_label)

        # Checkbox de confirmación
        self.confirm_checkbox = QCheckBox(
            "Entiendo que esta acción no se puede deshacer"
        )
        self.confirm_checkbox.stateChanged.connect(self.on_confirm_changed)
        layout.addWidget(self.confirm_checkbox)

        # Botones
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setObjectName("SecondaryButton")
        cancel_btn.clicked.connect(self.reject)

        self.delete_btn = QPushButton("Eliminar Producto")
        self.delete_btn.setObjectName("DangerButton")
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.accept)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(self.delete_btn)

        layout.addLayout(button_layout)

    def apply_styles(self):
        """Aplicar estilos al diálogo"""
        self.setStyleSheet(
            """
            QDialog {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
            
            #DangerHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #ef4444, stop:1 #dc2626);
                border-radius: 8px 8px 0 0;
                padding: 15px 20px;
            }
            
            #DialogTitle {
                color: white;
                font-weight: bold;
            }
            
            QCheckBox {
                font-size: 14px;
                color: #374151;
                spacing: 8px;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #d1d5db;
                border-radius: 4px;
                background: white;
            }
            
            QCheckBox::indicator:checked {
                background: #ef4444;
                border-color: #ef4444;
            }
            
            QCheckBox::indicator:checked:hover {
                background: #dc2626;
            }
            
            #DangerButton {
                background: #ef4444;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                min-width: 140px;
            }
            
            #DangerButton:hover:enabled {
                background: #dc2626;
            }
            
            #DangerButton:disabled {
                background: #d1d5db;
                color: #9ca3af;
            }
            
            #SecondaryButton {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            
            #SecondaryButton:hover {
                background: #e5e7eb;
            }
        """
        )

    def on_confirm_changed(self, state):
        """Manejar cambio en el checkbox de confirmación"""
        self.delete_btn.setEnabled(state == Qt.CheckState.Checked.value)
