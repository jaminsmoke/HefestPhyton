from typing import Optional, Dict, List, Any
import logging
from datetime import datetime
from PyQt6.QtWidgets import (
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
            import re

"""
Módulo de Gestión de Proveedores para Hefest
============================================

Interfaz dedicada para la gestión completa de proveedores
"""


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
    QTextEdit,
)

_ = logging.getLogger(__name__)


class SupplierManagerWidget(QWidget):
    """
    Widget especializado para la gestión de proveedores
    """

    # Señales
    _ = pyqtSignal()
    proveedor_seleccionado = pyqtSignal(dict)

    def __init__(self, inventario_service, parent=None):
        """Inicializar el widget gestor de proveedores"""
        super().__init__(parent)

        self.inventario_service = inventario_service
        self.proveedores_cache = []

        self.init_ui()
        self.load_suppliers()

        logger.info("SupplierManagerWidget inicializado correctamente")

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

        # Panel de búsqueda y acciones
        search_panel = self.create_search_panel()
        layout.addWidget(search_panel)

        # Tabla de proveedores
        self.suppliers_table = self.create_suppliers_table()
        layout.addWidget(self.suppliers_table)

        # Panel de estadísticas
        stats_panel = self.create_stats_panel()
        layout.addWidget(stats_panel)

        self.apply_styles()

    def create_header(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear el header del módulo"""
        header = QFrame()
        header.setObjectName("HeaderFrame")
        _ = QHBoxLayout(header)

        # Título
        title = QLabel("🏢 Gestión de Proveedores")
        title.setObjectName("ModuleTitle")
        layout.addWidget(title)

        layout.addStretch()

        # Información rápida
        info_label = QLabel("Administra la información de tus proveedores")
        info_label.setObjectName("ModuleSubtitle")
        layout.addWidget(info_label)

        return header

    def create_search_panel(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear panel de búsqueda y acciones"""
        panel = QFrame()
        panel.setObjectName("SearchPanel")
        _ = QHBoxLayout(panel)

        # Búsqueda
        _ = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar proveedores...")
        self.search_input.textChanged.connect(self.filter_suppliers)

        layout.addWidget(search_label)
        layout.addWidget(self.search_input)
        layout.addStretch()

        # Botones de acción
        self.add_btn = QPushButton("➕ Nuevo Proveedor")
        self.add_btn.clicked.connect(self.add_supplier)

        self.edit_btn = QPushButton("✏️ Editar")
        self.edit_btn.clicked.connect(self.edit_selected_supplier)
        self.edit_btn.setEnabled(False)

        self.delete_btn = QPushButton("🗑️ Eliminar")
        self.delete_btn.clicked.connect(self.delete_selected_supplier)
        self.delete_btn.setEnabled(False)

        layout.addWidget(self.add_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)

        return panel

    def create_suppliers_table(self) -> QTableWidget:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear la tabla de proveedores"""
        table = QTableWidget()
        table.setObjectName("SuppliersTable")  # Configurar columnas
        _ = [
            "ID",
            "Nombre",
            "Contacto",
            "Teléfono",
            "Email",
            "Dirección",
            "Categoría",
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
            header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Contacto
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Teléfono
            header.resizeSection(3, 120)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)  # Email
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Stretch)  # Dirección
            header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)  # Categoría
            header.resizeSection(6, 100)
            header.setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)  # Estado
            header.resizeSection(7, 80)

        # Conectar señales
        table.itemSelectionChanged.connect(self.on_supplier_selected)
        table.itemDoubleClicked.connect(self.edit_selected_supplier)

        return table

    def create_stats_panel(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crear panel de estadísticas"""
        panel = QFrame()
        panel.setObjectName("StatsPanel")
        _ = QHBoxLayout(panel)

        # Estadísticas básicas
        self.total_suppliers_label = QLabel("Total: 0")
        self.active_suppliers_label = QLabel("Activos: 0")
        self.inactive_suppliers_label = QLabel("Inactivos: 0")

        layout.addWidget(QLabel("📊"))
        layout.addWidget(self.total_suppliers_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.active_suppliers_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.inactive_suppliers_label)
        layout.addStretch()

        return panel

    def load_suppliers(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cargar proveedores desde el servicio"""
        try:
            self.proveedores_cache = self.inventario_service.get_proveedores()
            self.update_suppliers_table()
            self.update_statistics()

        except Exception as e:
            logger.error("Error cargando proveedores: %s", e)
            QMessageBox.warning(
                self, "Error", f"No se pudieron cargar los proveedores: {str(e)}"
            )

    def update_suppliers_table(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar la tabla de proveedores"""
        try:
            self.suppliers_table.setRowCount(len(self.proveedores_cache))

            for row, proveedor in enumerate(self.proveedores_cache):
                # ID
                self.suppliers_table.setItem(
                    row, 0, QTableWidgetItem(str(proveedor.get("id", "")))
                )

                # Nombre
                self.suppliers_table.setItem(
                    row, 1, QTableWidgetItem(proveedor.get("nombre", ""))
                )

                # Contacto
                self.suppliers_table.setItem(
                    row, 2, QTableWidgetItem(proveedor.get("contacto", ""))
                )

                # Teléfono
                self.suppliers_table.setItem(
                    row, 3, QTableWidgetItem(proveedor.get("telefono", ""))
                )

                # Email
                self.suppliers_table.setItem(
                    row, 4, QTableWidgetItem(proveedor.get("email", ""))
                )  # Dirección
                self.suppliers_table.setItem(
                    row, 5, QTableWidgetItem(proveedor.get("direccion", ""))
                )

                # Categoría
                categoria = proveedor.get("categoria", "General")
                _ = QTableWidgetItem(categoria or "General")
                # Colorear según la categoría
                if categoria == "Bebidas":
                    categoria_item.setBackground(QColor("#e3f2fd"))
                elif categoria == "Comida":
                    categoria_item.setBackground(QColor("#f3e5f5"))
                elif categoria == "Limpieza":
                    categoria_item.setBackground(QColor("#e8f5e8"))
                elif categoria == "Servicios":
                    categoria_item.setBackground(QColor("#fff3e0"))
                else:  # General y otros
                    categoria_item.setBackground(QColor("#f5f5f5"))
                self.suppliers_table.setItem(row, 6, categoria_item)

                # Estado
                activo = proveedor.get("activo", True)
                estado_text = "Activo" if activo else "Inactivo"
                _ = QTableWidgetItem(estado_text)
                if activo:
                    item.setBackground(QColor("#d4edda"))
                else:
                    item.setBackground(QColor("#f8d7da"))
                self.suppliers_table.setItem(row, 7, item)

        except Exception as e:
            logger.error("Error actualizando tabla de proveedores: %s", e)

    def update_statistics(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar estadísticas"""
        try:
            _ = len(self.proveedores_cache)
            active = sum(1 for p in self.proveedores_cache if p.get("activo", True))
            _ = total - active

            self.total_suppliers_label.setText(f"Total: {total}")
            self.active_suppliers_label.setText(f"Activos: {active}")
            self.inactive_suppliers_label.setText(f"Inactivos: {inactive}")

        except Exception as e:
            logger.error("Error actualizando estadísticas: %s", e)

    def filter_suppliers(self, text: str):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Filtrar proveedores por texto"""
        try:
            for row in range(self.suppliers_table.rowCount()):
                _ = False

                # Buscar en nombre, contacto, teléfono y email
                for col in [1, 2, 3, 4]:  # Nombre, Contacto, Teléfono, Email
                    item = self.suppliers_table.item(row, col)
                    if item and text.lower() in item.text().lower():
                        _ = True
                        break

                self.suppliers_table.setRowHidden(row, not show_row)

        except Exception as e:
            logger.error("Error filtrando proveedores: %s", e)

    def on_supplier_selected(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Manejar selección de proveedor"""
        selected_rows = set(item.row() for item in self.suppliers_table.selectedItems())
        has_selection = bool(selected_rows)

        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

        if has_selection:
            row = next(iter(selected_rows))
            if row < len(self.proveedores_cache):
                proveedor = self.proveedores_cache[row]
                self.proveedor_seleccionado.emit(proveedor)

    def add_supplier(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Agregar nuevo proveedor"""
        dialog = SupplierDialog(self.inventario_service, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_suppliers()
            self.proveedor_actualizado.emit()

    def edit_selected_supplier(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Editar proveedor seleccionado"""
        try:
            _ = set(
                item.row() for item in self.suppliers_table.selectedItems()
            )
            if not selected_rows:
                return

            row = next(iter(selected_rows))
            if row < len(self.proveedores_cache):
                proveedor = self.proveedores_cache[row]
                dialog = SupplierDialog(self.inventario_service, self, proveedor)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.load_suppliers()
                    self.proveedor_actualizado.emit()

        except Exception as e:
            logger.error("Error editando proveedor: %s", e)
            QMessageBox.warning(
                self, "Error", f"No se pudo editar el proveedor: {str(e)}"
            )

    def delete_selected_supplier(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Eliminar proveedor seleccionado"""
        try:
            _ = set(
                item.row() for item in self.suppliers_table.selectedItems()
            )
            if not selected_rows:
                return

            row = next(iter(selected_rows))
            if row < len(self.proveedores_cache):
                _ = self.proveedores_cache[row]

                # Confirmar eliminación
                _ = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Estás seguro de que deseas eliminar el proveedor '{proveedor.get('nombre', '')}'?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )

                if reply == QMessageBox.StandardButton.Yes:
                    if self.inventario_service.eliminar_proveedor(proveedor.get("id")):
                        self.load_suppliers()
                        self.proveedor_actualizado.emit()
                        QMessageBox.information(
                            self, "Éxito", "Proveedor eliminado correctamente"
                        )
                    else:
                        QMessageBox.warning(
                            self, "Error", "No se pudo eliminar el proveedor"
                        )

        except Exception as e:
            logger.error("Error eliminando proveedor: %s", e)
            QMessageBox.warning(
                self, "Error", f"No se pudo eliminar el proveedor: {str(e)}"
            )

    def apply_styles(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Aplicar estilos al widget"""
        self.setStyleSheet(
            """
            #HeaderFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #11998e, stop:1 #38ef7d);
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 10px;
            }
            
            #ModuleTitle {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            
            #ModuleSubtitle {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
            }
            
            #SearchPanel {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
            }
              #SuppliersTable {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                gridline-color: #f1f5f9;
                selection-background-color: #10b981;
                selection-color: white;
                outline: none;
            }
            
            #SuppliersTable::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
                border: none;
            }
            
            #SuppliersTable::item:selected {
                background: #10b981;
                color: white;
                border: none;
                outline: none;
            }
            
            #SuppliersTable::item:hover {
                background: #e6f7ff;
            }
            
            #SuppliersTable QHeaderView::section {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                padding: 8px;
                font-weight: bold;
                color: #374151;
            }
            
            #SuppliersTable QHeaderView::section:horizontal {
                border-left: none;
                border-right: none;
                border-top: none;
            }
            
            #StatsPanel {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                padding: 10px;
                font-weight: bold;
                color: #4a5568;
            }
            
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background: #059669;
            }
            
            QPushButton:disabled {
                background: #9ca3af;
                color: #6b7280;
            }
            
            QLineEdit {
                border: 2px solid #e2e8f0;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
            }
            
            QLineEdit:focus {
                border-color: #10b981;
            }
        """
        )


class SupplierDialog(QDialog):
    """Diálogo mejorado para crear/editar proveedores con validaciones avanzadas"""

    def __init__(self, inventario_service, parent=None, proveedor=None):
        """TODO: Add docstring"""
        super().__init__(parent)

        self.inventario_service = inventario_service
        self.proveedor = proveedor
        self.is_edit_mode = proveedor is not None

        self.init_ui()
        self.setup_validations()

        if self.is_edit_mode:
            self.load_supplier_data()

    def init_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicializar interfaz del diálogo mejorada"""
        self.setWindowTitle(
            "✏️ Editar Proveedor" if self.is_edit_mode else "➕ Nuevo Proveedor"
        )
        self.setModal(True)
        self.resize(600, 500)

        # Aplicar estilos
        self.setStyleSheet(
            """
            QDialog {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QLineEdit, QTextEdit {
                border: 2px solid #e9ecef;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #007bff;
            }
            QLabel {
                font-weight: 500;
                color: #495057;
            }
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
            QPushButton#saveBtn {
                background-color: #28a745;
                color: white;
                border: none;
            }
            QPushButton#saveBtn:hover {
                background-color: #218838;
            }
            QPushButton#cancelBtn {
                background-color: #6c757d;
                color: white;
                border: none;
            }
            QPushButton#cancelBtn:hover {
                background-color: #5a6268;
            }
            .error {
                border: 2px solid #dc3545 !important;
            }
            .valid {
                border: 2px solid #28a745 !important;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header con icono
        _ = QHBoxLayout()
        header_icon = QLabel("🏢")
        header_icon.setFont(QFont("Arial", 24))
        header_text = QLabel("Gestión de Proveedor")
        header_text.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(header_icon)
        header_layout.addWidget(header_text)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Formulario principal
        form_group = QGroupBox("📋 Información del Proveedor")
        form_layout = QGridLayout(form_group)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)

        _ = 0

        # Nombre (obligatorio)
        name_label = QLabel("* Nombre:")
        name_label.setStyleSheet("color: #212529; font-weight: 600;")
        form_layout.addWidget(name_label, row, 0)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Nombre de la empresa o proveedor (requerido)"
        )
        self.name_input.setMaxLength(150)
        form_layout.addWidget(self.name_input, row, 1)

        # Label de error para nombre
        row += 1
        self.name_error_label = QLabel("")
        self.name_error_label.setStyleSheet("color: #dc3545; font-size: 12px;")
        form_layout.addWidget(self.name_error_label, row, 1)

        # Contacto
        row += 1
        contact_label = QLabel("Contacto:")
        contact_label.setStyleSheet("color: #212529; font-weight: 600;")
        form_layout.addWidget(contact_label, row, 0)

        self.contact_input = QLineEdit()
        self.contact_input.setPlaceholderText("Persona de contacto")
        self.contact_input.setMaxLength(100)
        form_layout.addWidget(self.contact_input, row, 1)

        # Teléfono
        row += 1
        phone_label = QLabel("Teléfono:")
        phone_label.setStyleSheet("color: #212529; font-weight: 600;")
        form_layout.addWidget(phone_label, row, 0)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Número de teléfono (ej: +1234567890)")
        self.phone_input.setMaxLength(20)
        form_layout.addWidget(self.phone_input, row, 1)

        # Label de error para teléfono
        row += 1
        self.phone_error_label = QLabel("")
        self.phone_error_label.setStyleSheet("color: #dc3545; font-size: 12px;")
        form_layout.addWidget(self.phone_error_label, row, 1)

        # Email
        row += 1
        email_label = QLabel("Email:")
        email_label.setStyleSheet("color: #212529; font-weight: 600;")
        form_layout.addWidget(email_label, row, 0)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText(
            "Correo electrónico (ej: contacto@empresa.com)"
        )
        self.email_input.setMaxLength(150)
        form_layout.addWidget(self.email_input, row, 1)

        # Label de error para email
        row += 1
        self.email_error_label = QLabel("")
        self.email_error_label.setStyleSheet("color: #dc3545; font-size: 12px;")
        form_layout.addWidget(self.email_error_label, row, 1)

        # Dirección
        row += 1
        address_label = QLabel("Dirección:")
        address_label.setStyleSheet("color: #212529; font-weight: 600;")
        form_layout.addWidget(address_label, row, 0, Qt.AlignmentFlag.AlignTop)

        self.address_input = QTextEdit()
        self.address_input.setPlaceholderText("Dirección completa del proveedor")
        self.address_input.setMaximumHeight(100)
        form_layout.addWidget(
            self.address_input, row, 1
        )  # Contador de caracteres para dirección
        row += 1
        self.address_char_counter = QLabel("0/300 caracteres")
        self.address_char_counter.setStyleSheet("color: #6c757d; font-size: 11px;")
        form_layout.addWidget(
            self.address_char_counter, row, 1, Qt.AlignmentFlag.AlignRight
        )

        # Categoría
        row += 1
        category_label = QLabel("Categoría:")
        category_label.setStyleSheet("color: #212529; font-weight: 600;")
        form_layout.addWidget(category_label, row, 0)

        self.category_combo = QComboBox()
        self.category_combo.setEditable(True)
        self.category_combo.setPlaceholderText("Seleccione o escriba una categoría")
        self.category_combo.setMaximumWidth(300)
        form_layout.addWidget(self.category_combo, row, 1)

        layout.addWidget(form_group)

        # Información adicional en modo edición
        if self.is_edit_mode:
            info_group = QGroupBox("ℹ️ Información del Sistema")
            _ = QGridLayout(info_group)

            # ID
            info_layout.addWidget(QLabel("ID:"), 0, 0)
            self.id_label = QLabel("N/A")
            self.id_label.setStyleSheet("font-weight: 600; color: #495057;")
            info_layout.addWidget(self.id_label, 0, 1)

            # Fecha de creación
            info_layout.addWidget(QLabel("Creado:"), 1, 0)
            self.created_label = QLabel("N/A")
            info_layout.addWidget(self.created_label, 1, 1)

            layout.addWidget(info_group)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("💾 Guardar" if self.is_edit_mode else "✅ Crear")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.clicked.connect(self.save_supplier)
        self.save_btn.setDefault(True)

        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)

        layout.addLayout(buttons_layout)

    def setup_validations(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configurar validaciones en tiempo real"""
        # Validación del nombre
        self.name_input.textChanged.connect(self.validate_name)

        # Validación del teléfono
        self.phone_input.textChanged.connect(self.validate_phone)

        # Validación del email
        self.email_input.textChanged.connect(
            self.validate_email
        )  # Contador de caracteres para dirección
        self.address_input.textChanged.connect(self.update_address_counter)

        # Cargar categorías después de configurar validaciones
        self.load_categories()

    def load_categories(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cargar categorías de proveedores en el combo box"""
        try:
            if hasattr(self.inventario_service, "get_categorias_proveedores"):
                _ = self.inventario_service.get_categorias_proveedores()
            else:
                # Fallback si el método no existe
                _ = [
                    "General",
                    "Bebidas",
                    "Comida",
                    "Limpieza",
                    "Papelería",
                    "Servicios",
                ]

            self.category_combo.clear()
            for categoria in categorias:
                self.category_combo.addItem(categoria)

            # Establecer valor por defecto
            if not self.is_edit_mode:
                self.category_combo.setCurrentText("General")

        except Exception as e:
            logger.error("Error cargando categorías: %s", e)
            # Categorías por defecto en caso de error
            _ = [
                "General",
                "Bebidas",
                "Comida",
                "Limpieza",
                "Papelería",
                "Servicios",
            ]
            self.category_combo.clear()
            for categoria in default_categories:
                self.category_combo.addItem(categoria)

    def load_supplier_data(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cargar datos del proveedor en edición"""
        if self.proveedor:
            self.name_input.setText(self.proveedor.get("nombre", ""))
            self.contact_input.setText(self.proveedor.get("contacto", ""))
            self.phone_input.setText(self.proveedor.get("telefono", ""))
            self.email_input.setText(self.proveedor.get("email", ""))
            self.address_input.setPlainText(self.proveedor.get("direccion", ""))

            # Cargar categoría
            categoria = self.proveedor.get("categoria", "General")
            if categoria:
                self.category_combo.setCurrentText(categoria)
            else:
                self.category_combo.setCurrentText("General")

            # Información del sistema
            if hasattr(self, "id_label"):
                self.id_label.setText(str(self.proveedor.get("id", "N/A")))
            if hasattr(self, "created_label"):
                created = self.proveedor.get("fecha_creacion", "N/A")
                if created != "N/A":
                    try:

                        if isinstance(created, str):
                            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                            _ = dt.strftime("%d/%m/%Y %H:%M")
                    except Exception as e:
                        logging.error("Error: %s", e)
                        pass
                self.created_label.setText(str(created))

            # Ejecutar validaciones iniciales
            self.validate_name()
            self.validate_phone()
            self.validate_email()
            self.update_address_counter()

    def save_supplier(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Guardar el proveedor con validaciones completas"""  # Validar formulario completo
        if not self.validate_form():
            return

        try:
            _ = self.name_input.text().strip()
            contacto = self.contact_input.text().strip()
            _ = self.phone_input.text().strip()
            email = self.email_input.text().strip()
            _ = self.address_input.toPlainText().strip()
            categoria = self.category_combo.currentText().strip() or "General"

            if self.is_edit_mode and self.proveedor:
                # Actualizar proveedor existente
                _ = self.inventario_service.actualizar_proveedor(
                    self.proveedor.get("id"),
                    nombre,
                    contacto,
                    telefono,
                    email,
                    direccion,
                    categoria,
                )
                _ = (
                    "Proveedor actualizado exitosamente"
                    if success
                    else "Error al actualizar el proveedor"
                )
            else:
                # Crear nuevo proveedor
                _ = self.inventario_service.crear_proveedor(
                    nombre, contacto, telefono, email, direccion, categoria
                )
                _ = (
                    "Proveedor creado exitosamente"
                    if success
                    else "Error al crear el proveedor"
                )

            if success:
                QMessageBox.information(self, "✅ Éxito", message)
                self.accept()
            else:
                QMessageBox.warning(self, "⚠️ Error", message)

        except Exception as e:
            logger.error("Error al guardar proveedor: %s", e)
            QMessageBox.critical(
                self,
                "❌ Error Crítico",
                f"Error inesperado al guardar el proveedor:\n{str(e)}",
            )

    def validate_form(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Validar todo el formulario antes de guardar"""
        _ = True
        error_messages = []

        # Validar nombre (obligatorio)
        if not self.validate_name():
            _ = False
            error_messages.append(
                "• El nombre es obligatorio y debe tener al menos 2 caracteres"
            )

        # Validar teléfono (opcional pero debe ser válido si se proporciona)
        phone = self.phone_input.text().strip()
        if phone and not self.validate_phone():
            _ = False
            error_messages.append("• El formato del teléfono no es válido")

        # Validar email (opcional pero debe ser válido si se proporciona)
        email = self.email_input.text().strip()
        if email and not self.validate_email():
            _ = False
            error_messages.append("• El formato del email no es válido")
        # Validar dirección (opcional pero con límite)
        direccion = self.address_input.toPlainText().strip()
        if len(direccion) > 300:
            _ = False
            error_messages.append("• La dirección no puede exceder 300 caracteres")

        # Mostrar errores si los hay
        if not is_valid:
            _ = "Por favor, corrija los siguientes errores:\n\n" + "\n".join(
                error_messages
            )
            QMessageBox.warning(self, "⚠️ Errores de Validación", error_text)

        return is_valid

    def validate_name(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Validar el campo nombre en tiempo real"""
        name = self.name_input.text().strip()

        if not name:
            self.name_error_label.setText("❌ El nombre es obligatorio")
            self.name_input.setStyleSheet("border: 2px solid #dc3545;")
            return False
        elif len(name) < 2:
            self.name_error_label.setText(
                "⚠️ El nombre debe tener al menos 2 caracteres"
            )
            self.name_input.setStyleSheet("border: 2px solid #ffc107;")
            return False
        else:
            self.name_error_label.setText("")
            self.name_input.setStyleSheet("")
            return True

    def validate_phone(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Validar el campo teléfono en tiempo real"""
        phone = self.phone_input.text().strip()

        if phone and len(phone) > 0:
            # Validar formato básico de teléfono (solo números, espacios, guiones, paréntesis y +)

            phone_pattern = r"^[\+]?[\d\s\-\(\)]+$"

            if not re.match(phone_pattern, phone):
                self.phone_error_label.setText("⚠️ Formato de teléfono inválido")
                self.phone_input.setStyleSheet("border: 2px solid #ffc107;")
                return False
            elif len(phone) < 7:
                self.phone_error_label.setText("⚠️ Número de teléfono muy corto")
                self.phone_input.setStyleSheet("border: 2px solid #ffc107;")
                return False
            else:
                self.phone_error_label.setText("✅ Teléfono válido")
                self.phone_error_label.setStyleSheet("color: #28a745; font-size: 12px;")
                self.phone_input.setStyleSheet("border: 2px solid #28a745;")
                return True
        else:
            self.phone_error_label.setText("")
            self.phone_input.setStyleSheet("")
            return True

    def validate_email(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Validar el campo email en tiempo real"""
        email = self.email_input.text().strip()

        if email and len(email) > 0:
            # Validar formato básico de email

            email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

            if not re.match(email_pattern, email):
                self.email_error_label.setText("⚠️ Formato de email inválido")
                self.email_input.setStyleSheet("border: 2px solid #ffc107;")
                return False
            else:
                self.email_error_label.setText("✅ Email válido")
                self.email_error_label.setStyleSheet("color: #28a745; font-size: 12px;")
                self.email_input.setStyleSheet("border: 2px solid #28a745;")
                return True
        else:
            self.email_error_label.setText("")
            self.email_input.setStyleSheet("")
            return True

    def update_address_counter(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualizar contador de caracteres para dirección"""
        text = self.address_input.toPlainText()
        char_count = len(text)

        if char_count > 300:
            # Truncar texto si excede el límite
            self.address_input.setPlainText(text[:300])
            char_count = 300

        self.address_char_counter.setText(f"{char_count}/300 caracteres")

        if char_count > 270:
            self.address_char_counter.setStyleSheet(
                "color: #dc3545; font-size: 11px; font-weight: bold;"
            )
        elif char_count > 240:
            self.address_char_counter.setStyleSheet(
                "color: #ffc107; font-size: 11px; font-weight: bold;"
            )
        else:
            self.address_char_counter.setStyleSheet("color: #6c757d; font-size: 11px;")

    def _update_save_button_state(self):
        """Actualizar estado del botón guardar basado en validaciones"""
        # Solo el nombre es obligatorio - Verificar directamente sin llamar validate_name() para evitar recursión
        name = self.name_input.text().strip()
        name_valid = bool(name) and len(name) >= 2
        self.save_btn.setEnabled(name_valid)
