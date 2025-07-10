# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
import logging
from PyQt6.QtWidgets import (
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from services.inventario_service_real import Producto

"""
Diálogo Corregido para Productos - Hefest v0.0.12
=================================================

Versión simplificada y robusta del diálogo de productos
que evita conflictos de layout y renderiza correctamente.
"""

    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QLabel, QTextEdit, QGroupBox,
    QCheckBox, QDateEdit, QMessageBox
)


_ = logging.getLogger(__name__)


class NewProductDialogFixed(QDialog):
    """Diálogo corregido para crear nuevos productos"""

    def __init__(self, parent=None, categories=None, inventario_service=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.inventario_service = inventario_service
        self.categories = categories or []
        
        self.setWindowTitle("Nuevo Producto")
        self.setModal(True)
        self.setMinimumSize(600, 650)
        self.resize(600, 650)
        
        self.setup_ui()
        self.setup_validation()
        self.load_initial_data()
        
    def setup_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configurar interfaz de usuario simplificada pero completa"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("📦 Nuevo Producto")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #2563eb;
                padding: 10px;
                border-bottom: 2px solid #e5e7eb;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)
        
        # Información Básica
        basic_group = self.create_basic_group()
        layout.addWidget(basic_group)
        
        # Información Comercial
        commercial_group = self.create_commercial_group()
        layout.addWidget(commercial_group)
        
        # Información de Inventario
        inventory_group = self.create_inventory_group()
        layout.addWidget(inventory_group)
        
        # Información Adicional
        additional_group = self.create_additional_group()
        layout.addWidget(additional_group)
        
        # Botones
        buttons_layout = self.create_buttons()
        layout.addLayout(buttons_layout)
        
    def create_basic_group(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear grupo de información básica"""
        group = QGroupBox("📋 Información Básica")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Nombre
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre del producto (requerido)")
        layout.addRow("* Nombre:", self.nombre_input)
        
        # Categoría
        self.categoria_combo = QComboBox()
        self.categoria_combo.setEditable(True)
        self.categoria_combo.setPlaceholderText("Seleccionar categoría")
        layout.addRow("* Categoría:", self.categoria_combo)
        
        # Código
        self.codigo_input = QLineEdit()
        self.codigo_input.setPlaceholderText("Código interno (opcional)")
        layout.addRow("Código/SKU:", self.codigo_input)
        
        # Descripción
        self.descripcion_input = QTextEdit()
        self.descripcion_input.setMaximumHeight(60)
        self.descripcion_input.setPlaceholderText("Descripción del producto...")
        layout.addRow("Descripción:", self.descripcion_input)
        
        return group
        
    def create_commercial_group(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear grupo de información comercial"""
        group = QGroupBox("💰 Información Comercial")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Precio de compra
        self.precio_compra_input = QDoubleSpinBox()
        self.precio_compra_input.setRange(0.0, 999999.99)
        self.precio_compra_input.setDecimals(2)
        self.precio_compra_input.setSuffix(" €")
        layout.addRow("Precio de compra:", self.precio_compra_input)
        
        # Precio de venta
        self.precio_venta_input = QDoubleSpinBox()
        self.precio_venta_input.setRange(0.01, 999999.99)
        self.precio_venta_input.setDecimals(2)
        self.precio_venta_input.setSuffix(" €")
        layout.addRow("* Precio de venta:", self.precio_venta_input)
        
        # IVA
        self.iva_input = QDoubleSpinBox()
        self.iva_input.setRange(0.0, 50.0)
        self.iva_input.setDecimals(1)
        self.iva_input.setValue(21.0)
        self.iva_input.setSuffix(" %")
        layout.addRow("IVA:", self.iva_input)
        
        # Margen (calculado automáticamente)
        self.margen_label = QLabel("0.0 %")
        self.margen_label.setStyleSheet("color: #059669; font-weight: bold;")
        layout.addRow("Margen:", self.margen_label)
        
        return group
        
    def create_inventory_group(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear grupo de información de inventario"""
        group = QGroupBox("📦 Gestión de Inventario")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Stock inicial
        self.stock_inicial_input = QSpinBox()
        self.stock_inicial_input.setRange(0, 999999)
        self.stock_inicial_input.setValue(0)
        layout.addRow("Stock inicial:", self.stock_inicial_input)
        
        # Stock mínimo
        self.stock_minimo_input = QSpinBox()
        self.stock_minimo_input.setRange(0, 9999)
        self.stock_minimo_input.setValue(5)
        layout.addRow("Stock mínimo:", self.stock_minimo_input)
        
        # Stock máximo
        self.stock_maximo_input = QSpinBox()
        self.stock_maximo_input.setRange(0, 999999)
        self.stock_maximo_input.setValue(100)
        layout.addRow("Stock máximo:", self.stock_maximo_input)
        
        # Ubicación
        self.ubicacion_input = QLineEdit()
        self.ubicacion_input.setPlaceholderText("Almacén, estantería, etc.")
        layout.addRow("Ubicación:", self.ubicacion_input)
        
        return group
        
    def create_additional_group(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear grupo de información adicional"""
        group = QGroupBox("📝 Información Adicional")
        group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        layout = QFormLayout(group)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Es perecedero
        self.perecedero_checkbox = QCheckBox("Es producto perecedero")
        layout.addRow("", self.perecedero_checkbox)
        
        # Fecha de caducidad
        self.caducidad_input = QDateEdit()
        self.caducidad_input.setDate(QDate.currentDate().addDays(30))
        self.caducidad_input.setCalendarPopup(True)
        self.caducidad_input.setEnabled(False)
        layout.addRow("Fecha caducidad:", self.caducidad_input)
        
        # Notas
        self.notas_input = QTextEdit()
        self.notas_input.setMaximumHeight(60)
        self.notas_input.setPlaceholderText("Notas adicionales, alergenos, etc.")
        layout.addRow("Notas:", self.notas_input)
        
        return group
        
    def create_buttons(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear botones de acción"""
        layout = QHBoxLayout()
        layout.setSpacing(10)
        
        # Estado de validación
        self.validation_label = QLabel("")
        self.validation_label.setStyleSheet("color: #dc2626; font-weight: bold;")
        layout.addWidget(self.validation_label)
        
        layout.addStretch()
        
        # Botón cancelar
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.cancel_btn)
        
        # Botón guardar
        self.save_btn = QPushButton("Guardar Producto")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_product)
        layout.addWidget(self.save_btn)
        
        return layout
        
    def setup_validation(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configurar validaciones en tiempo real"""
        # Conectar eventos para validación
        self.nombre_input.textChanged.connect(self.validate_form)
        self.categoria_combo.currentTextChanged.connect(self.validate_form)
        self.precio_venta_input.valueChanged.connect(self.validate_form)
        self.precio_venta_input.valueChanged.connect(self.calculate_margin)
        self.precio_compra_input.valueChanged.connect(self.calculate_margin)
        
        # Habilitar/deshabilitar fecha de caducidad
        self.perecedero_checkbox.toggled.connect(self.caducidad_input.setEnabled)
        
    def load_initial_data(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cargar datos iniciales"""
        try:
            if self.inventario_service:
                # Cargar categorías
                categorias = self.inventario_service.get_categorias()
                self.categoria_combo.addItems(categorias)
            elif self.categories:
                self.categoria_combo.addItems(self.categories)
                
        except Exception as e:
            logger.error("Error cargando datos: %s", e)
            
    def validate_form(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Validar formulario en tiempo real"""
        _ = []
        
        # Validar nombre
        if not self.nombre_input.text().strip():
            errors.append("El nombre es requerido")
            
        # Validar categoría
        if not self.categoria_combo.currentText().strip():
            errors.append("La categoría es requerida")
            
        # Validar precio
        if self.precio_venta_input.value() <= 0:
            errors.append("El precio debe ser mayor a 0")
            
        # Mostrar errores
        if errors:
            self.validation_label.setText(f"⚠️ {errors[0]}")
            self.save_btn.setEnabled(False)
        else:
            self.validation_label.setText("✅ Formulario válido")
            self.save_btn.setEnabled(True)
            
    def calculate_margin(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Calcular margen automáticamente"""
        try:
            _ = self.precio_compra_input.value()
            venta = self.precio_venta_input.value()
            
            if compra > 0 and venta > 0:
                margen = ((venta - compra) / venta) * 100
                self.margen_label.setText(f"{margen:.1f} %")
                
                # Colorear según el margen
                if margen < 10:
                    _ = "#dc2626"  # Rojo
                elif margen < 30:
                    _ = "#d97706"  # Amarillo
                else:
                    _ = "#059669"  # Verde
                    
                self.margen_label.setStyleSheet(f"color: {color}; font-weight: bold;")
            else:
                self.margen_label.setText("N/A")
                
        except Exception as e:
            logger.error("Error calculando margen: %s", e)
            
    def save_product(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Guardar el producto"""
        try:
            if not self.inventario_service:
                QMessageBox.warning(self, "Error", "No hay conexión con el servicio de inventario")
                return
                
            # Recopilar datos
            _ = self.nombre_input.text().strip()
            categoria = self.categoria_combo.currentText().strip()
            _ = self.precio_venta_input.value()
            stock_inicial = self.stock_inicial_input.value()
            _ = self.stock_minimo_input.value()
            
            # Crear producto
            _ = self.inventario_service.crear_producto(
                nombre=nombre,
                _ = categoria,
                precio=precio,
                _ = stock_inicial,
                stock_minimo=stock_minimo
            )
            
            if resultado:
                QMessageBox.information(self, "Éxito", f"Producto '{nombre}' creado correctamente")
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "No se pudo crear el producto")
                
        except Exception as e:
            logger.error("Error guardando producto: %s", e)
            QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")
            
    def get_product_data(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtener datos del producto para uso externo"""
        return {
            "nombre": self.nombre_input.text().strip(),
            "categoria": self.categoria_combo.currentText().strip(),
            "precio": self.precio_venta_input.value(),
            "stock_inicial": self.stock_inicial_input.value(),
            "stock_minimo": self.stock_minimo_input.value(),
            "codigo": self.codigo_input.text().strip(),
            "descripcion": self.descripcion_input.toPlainText().strip(),
            "notas": self.notas_input.toPlainText().strip()
        }
