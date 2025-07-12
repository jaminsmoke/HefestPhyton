"""
Módulo de Gestión de Proveedores para Hefest
============================================

Interfaz dedicada para la gestión completa de proveedores
"""

import logging
from typing import Optional, List, Dict, Any

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame,
    QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QComboBox, 
    QGroupBox, QGridLayout, QMessageBox, QDialog, QTextEdit, 
    QDialogButtonBox, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

# Importar utilidades comunes
from .inventory_common_utils import (
    InventoryManagerBase, InventoryDialogBase, InventoryValidationUtils,
    CommonInventoryStyles
)

logger = logging.getLogger(__name__)


class SupplierDialog(InventoryDialogBase):
    """Diálogo para agregar/editar proveedores"""
    
    def __init__(self, parent=None, supplier_data=None):
        self.supplier_data = supplier_data
        self.is_edit = supplier_data is not None
        
        title = "Editar Proveedor" if self.is_edit else "Nuevo Proveedor"
        super().__init__(parent, title, (500, 600))
        
        if self.is_edit:
            self._load_supplier_data()
    
    def _setup_ui(self):
        """Configuración específica de UI para proveedores"""
        super()._setup_ui()
        
        # Información básica
        basic_form = self._create_basic_info_form()
        self.add_form_section("Información Básica", basic_form)
        
        # Información de contacto
        contact_form = self._create_contact_info_form()
        self.add_form_section("Información de Contacto", contact_form)
        
        # Configuración adicional
        config_form = self._create_config_form()
        self.add_form_section("Configuración", config_form)
    
    def _create_basic_info_form(self):
        """Crea formulario de información básica"""
        form = QFormLayout()
        
        # Nombre (requerido)
        self.name_edit = QLineEdit()
        name_label, name_widget = self.create_form_field(
            "Nombre", self.name_edit, required=True
        )
        form.addRow(name_label, name_widget)
        
        # Contacto principal
        self.contact_edit = QLineEdit()
        contact_label, contact_widget = self.create_form_field(
            "Contacto Principal", self.contact_edit
        )
        form.addRow(contact_label, contact_widget)
        
        # Categoría
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "Alimentación", "Bebidas", "Limpieza", "Equipamiento",
            "Servicios", "Textil", "Tecnología", "Otros"
        ])
        category_label, category_widget = self.create_form_field(
            "Categoría", self.category_combo
        )
        form.addRow(category_label, category_widget)
        
        return form
    
    def _create_contact_info_form(self):
        """Crea formulario de información de contacto"""
        form = QFormLayout()
        
        # Teléfono
        self.phone_edit = QLineEdit()
        phone_label, phone_widget = self.create_form_field(
            "Teléfono", self.phone_edit
        )
        form.addRow(phone_label, phone_widget)
        
        # Email
        self.email_edit = QLineEdit()
        email_label, email_widget = self.create_form_field(
            "Email", self.email_edit
        )
        form.addRow(email_label, email_widget)
        
        # Dirección
        self.address_edit = QTextEdit()
        self.address_edit.setMaximumHeight(80)
        address_label, address_widget = self.create_form_field(
            "Dirección", self.address_edit
        )
        form.addRow(address_label, address_widget)
        
        return form
    
    def _create_config_form(self):
        """Crea formulario de configuración"""
        form = QFormLayout()
        
        # Estado
        self.status_combo = QComboBox()
        self.status_combo.addItems(["Activo", "Inactivo", "Suspendido"])
        status_label, status_widget = self.create_form_field(
            "Estado", self.status_combo
        )
        form.addRow(status_label, status_widget)
        
        # Notas
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        notes_label, notes_widget = self.create_form_field(
            "Notas", self.notes_edit
        )
        form.addRow(notes_label, notes_widget)
        
        return form
    
    def _load_supplier_data(self):
        """Carga datos del proveedor para edición"""
        if not self.supplier_data:
            return
            
        self.name_edit.setText(str(self.supplier_data.get('nombre', '')))
        self.contact_edit.setText(str(self.supplier_data.get('contacto', '')))
        self.phone_edit.setText(str(self.supplier_data.get('telefono', '')))
        self.email_edit.setText(str(self.supplier_data.get('email', '')))
        self.address_edit.setPlainText(str(self.supplier_data.get('direccion', '')))
        self.notes_edit.setPlainText(str(self.supplier_data.get('notas', '')))
        
        # Seleccionar categoría
        category = self.supplier_data.get('categoria', '')
        index = self.category_combo.findText(category)
        if index >= 0:
            self.category_combo.setCurrentIndex(index)
            
        # Seleccionar estado
        status = self.supplier_data.get('estado', 'Activo')
        index = self.status_combo.findText(status)
        if index >= 0:
            self.status_combo.setCurrentIndex(index)
    
    def get_supplier_data(self):
        """Obtiene los datos del formulario"""
        return {
            'nombre': self.name_edit.text().strip(),
            'contacto': self.contact_edit.text().strip(),
            'telefono': self.phone_edit.text().strip(),
            'email': self.email_edit.text().strip(),
            'direccion': self.address_edit.toPlainText().strip(),
            'categoria': self.category_combo.currentText(),
            'estado': self.status_combo.currentText(),
            'notas': self.notes_edit.toPlainText().strip()
        }
    
    def validate_data(self):
        """Valida los datos del formulario"""
        data = self.get_supplier_data()
        
        # Validar nombre requerido
        is_valid, msg = InventoryValidationUtils.validate_required_field(
            data['nombre'], 'Nombre del proveedor'
        )
        if not is_valid:
            self.show_error(msg)
            return False
            
        # Validar email si se proporciona
        if data['email']:
            is_valid, msg = InventoryValidationUtils.validate_email(data['email'])
            if not is_valid:
                self.show_error(msg)
                return False
                
        # Validar teléfono si se proporciona
        if data['telefono']:
            is_valid, msg = InventoryValidationUtils.validate_phone(data['telefono'])
            if not is_valid:
                self.show_error(msg)
                return False
                
        return True
    
    def accept(self):
        """Sobrescribe accept para validar antes de cerrar"""
        if self.validate_data():
            super().accept()


class SupplierManagerWidget(InventoryManagerBase):
    """Widget especializado para la gestión de proveedores"""

    # Señales adicionales específicas
    proveedor_actualizado = pyqtSignal()
    proveedor_seleccionado = pyqtSignal(dict)

    def __init__(self, inventario_service: Any, parent: Optional[QWidget] = None):
        """Inicializar el widget gestor de proveedores"""
        # PRIMERO: Configurar el servicio de inventario
        self.inventario_service = inventario_service
        
        # SEGUNDO: Flag para evitar carga inicial prematura
        self._skip_initial_load = True
        
        # Llamar al constructor base con db_manager
        super().__init__(db_manager=inventario_service, parent=parent)
        
        # TERCERO: Configuración específica
        self.title_label.setText("🏢 Gestión de Proveedores")
        self.setup_table_columns(
            ["ID", "Nombre", "Contacto", "Teléfono", "Email", "Dirección", "Categoría", "Estado"],
            [60, 150, 120, 100, 150, 200, 100, 80]
        )
        
        # Agregar campo de búsqueda específico
        self._add_search_field()
        
        # AHORA cargar datos después de que todo esté inicializado
        self._skip_initial_load = False
        self.load_suppliers()
        
        logger.info("SupplierManagerWidget inicializado correctamente")
    
    def _add_search_field(self):
        """Agrega campo de búsqueda al header"""
        # Insertar búsqueda antes de los botones
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar proveedores...")
        self.search_input.textChanged.connect(self.filter_suppliers)
        
        # Insertar en el layout del header
        self.header_layout.insertWidget(-4, search_label)  # Antes de los botones
        self.header_layout.insertWidget(-4, self.search_input)
    
    def _load_data(self):
        """Implementación específica para cargar proveedores"""
        # Control de carga inicial prematura
        if hasattr(self, '_skip_initial_load') and self._skip_initial_load:
            logger.debug("Saltando carga inicial de proveedores")
            return
            
        try:
            logger.info("Cargando proveedores desde el servicio...")
            self.suppliers_cache = self.inventario_service.get_proveedores()
            logger.info(f"Obtenidos {len(self.suppliers_cache)} proveedores")
            
            if self.suppliers_cache:
                self.update_suppliers_table()
                logger.info("Proveedores cargados exitosamente")
            else:
                logger.warning("No se obtuvieron proveedores del servicio")
                
        except Exception as e:
            logger.error(f"Error cargando proveedores: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            self.show_error(f"No se pudieron cargar los proveedores: {str(e)}")
    
    def load_suppliers(self) -> None:
        """Cargar proveedores desde el servicio"""
        self._load_data()
    
    def update_suppliers_table(self) -> None:
        """Actualizar la tabla de proveedores"""
        try:
            # Verificar que la tabla existe
            if not hasattr(self, 'table') or self.table is None:
                logger.error("table no existe o es None")
                return
                
            # IMPORTANTE: Actualizar items_cache para que la clase base funcione
            self.items_cache = self.suppliers_cache
            
            # Solo mostrar proveedores activos
            proveedores_activos = [
                prov for prov in self.suppliers_cache 
                if prov.get('activo', True) or prov.get('estado', '').lower() == 'activo'
            ]
            
            self.table.setRowCount(len(proveedores_activos))

            for row, proveedor in enumerate(proveedores_activos):
                # ID
                self.table.setItem(
                    row, 0, QTableWidgetItem(str(proveedor.get('id', '')))
                )

                # Nombre
                self.table.setItem(
                    row, 1, QTableWidgetItem(proveedor.get("nombre", ""))
                )

                # Contacto
                self.table.setItem(
                    row, 2, QTableWidgetItem(proveedor.get("contacto", ""))
                )
                
                # Teléfono
                self.table.setItem(
                    row, 3, QTableWidgetItem(proveedor.get("telefono", ""))
                )
                
                # Email
                self.table.setItem(
                    row, 4, QTableWidgetItem(proveedor.get("email", ""))
                )
                
                # Dirección
                self.table.setItem(
                    row, 5, QTableWidgetItem(proveedor.get("direccion", ""))
                )
                
                # Categoría
                self.table.setItem(
                    row, 6, QTableWidgetItem(proveedor.get("categoria", ""))
                )
                
                # Estado
                self.table.setItem(
                    row, 7, QTableWidgetItem(proveedor.get("estado", ""))
                )

            logger.info(f"Tabla de proveedores actualizada con {len(proveedores_activos)} elementos")
            
        except Exception as e:
            logger.error(f"Error actualizando tabla de proveedores: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
    
    def add_item(self):
        """Agregar nuevo proveedor"""
        dialog = SupplierDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_supplier_data()
                # Llamar con parámetros individuales que acepta el servicio
                self.inventario_service.crear_proveedor(
                    nombre=data['nombre'],
                    contacto=data['contacto'],
                    telefono=data['telefono'],
                    email=data['email'],
                    direccion=data['direccion'],
                    categoria=data['categoria']
                )
                self.load_suppliers()  # Usar método específico
                self.proveedor_actualizado.emit()
                self.show_success("Proveedor agregado exitosamente")
            except Exception as e:
                logger.error(f"Error agregando proveedor: {e}")
                self.show_error(f"Error al agregar proveedor: {str(e)}")
    
    def edit_item(self):
        """Editar proveedor seleccionado"""
        selected = self.get_selected_item()
        if not selected:
            self.show_warning("Por favor selecciona un proveedor para editar")
            return
            
        dialog = SupplierDialog(self, selected)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                data = dialog.get_supplier_data()
                # Llamar con parámetros individuales que acepta el servicio
                self.inventario_service.actualizar_proveedor(
                    proveedor_id=selected['id'],
                    nombre=data['nombre'],
                    contacto=data['contacto'],
                    telefono=data['telefono'],
                    email=data['email'],
                    direccion=data['direccion'],
                    categoria=data['categoria']
                )
                self.load_suppliers()  # Usar método específico
                self.proveedor_actualizado.emit()
                self.show_success("Proveedor actualizado exitosamente")
            except Exception as e:
                logger.error(f"Error actualizando proveedor: {e}")
                self.show_error(f"Error al actualizar proveedor: {str(e)}")
    
    def delete_item(self):
        """Eliminar proveedor seleccionado"""
        selected = self.get_selected_item()
        if not selected:
            self.show_warning(
                "Por favor selecciona un proveedor para eliminar"
            )
            return
            
        if self.confirm_action(
            f"¿Estás seguro de que deseas eliminar el proveedor "
            f"'{selected['nombre']}'?\nEsta acción no se puede deshacer."
        ):
            try:
                self.inventario_service.eliminar_proveedor(selected['id'])
                self.load_suppliers()  # Usar método específico
                self.proveedor_actualizado.emit()
                self.show_success("Proveedor eliminado exitosamente")
            except Exception as e:
                logger.error(f"Error eliminando proveedor: {e}")
                self.show_error(f"Error al eliminar proveedor: {str(e)}")
    
    def refresh_data(self):
        """Actualiza los datos de proveedores"""
        self.load_suppliers()
    
    def filter_suppliers(self):
        """Filtrar proveedores en la tabla"""
        search_text = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            match = False
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    match = True
                    break
            self.table.setRowHidden(row, not match)
    
    def show_error(self, message: str):
        """Mostrar mensaje de error"""
        QMessageBox.critical(self, "Error", message)
    
    def show_success(self, message: str):
        """Mostrar mensaje de éxito"""
        QMessageBox.information(self, "Éxito", message)
    
    def show_warning(self, message: str):
        """Mostrar mensaje de advertencia"""
        QMessageBox.warning(self, "Advertencia", message)
    
    def confirm_action(self, message: str) -> bool:
        """Solicitar confirmación"""
        reply = QMessageBox.question(
            self, "Confirmar", message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes

