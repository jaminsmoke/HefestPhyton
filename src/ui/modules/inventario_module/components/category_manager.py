"""
Módulo de Gestión de Categorías para Hefest
==========================================

Interfaz dedicada para la gestión completa de categorías de productos
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
    QGroupBox,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QMessageBox,
    QDialog,
    QTextEdit,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

logger = logging.getLogger(__name__)


class CategoryManagerWidget(QWidget):
    """
    Widget especializado para la gestión de categorías
    """

    # Señales
    categoria_actualizada = pyqtSignal()
    categoria_seleccionada = pyqtSignal(dict)

    def __init__(self, inventario_service, parent=None):
        """Inicializar el widget gestor de categorías"""
        super().__init__(parent)

        self.inventario_service = inventario_service
        self.categorias_cache = []

        self.init_ui()
        self.load_categories()

        logger.info("CategoryManagerWidget inicializado correctamente")

    def init_ui(self):
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

        # Tabla de categorías
        self.categories_table = self.create_categories_table()
        layout.addWidget(self.categories_table)

        # Panel de estadísticas
        stats_panel = self.create_stats_panel()
        layout.addWidget(stats_panel)

        self.apply_styles()

    def create_header(self) -> QFrame:
        """Crear el header del módulo"""
        header = QFrame()
        header.setObjectName("HeaderFrame")
        layout = QHBoxLayout(header)

        # Título
        title = QLabel("🏷️ Gestión de Categorías")
        title.setObjectName("ModuleTitle")
        layout.addWidget(title)

        layout.addStretch()

        # Información rápida
        info_label = QLabel("Organiza y gestiona las categorías de productos")
        info_label.setObjectName("ModuleSubtitle")
        layout.addWidget(info_label)

        return header

    def create_search_panel(self) -> QFrame:
        """Crear panel de búsqueda y acciones"""
        panel = QFrame()
        panel.setObjectName("SearchPanel")
        layout = QHBoxLayout(panel)

        # Búsqueda
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar categorías...")
        self.search_input.textChanged.connect(self.filter_categories)

        layout.addWidget(search_label)
        layout.addWidget(self.search_input)
        layout.addStretch()

        # Botones de acción
        self.add_btn = QPushButton("➕ Nueva Categoría")
        self.add_btn.clicked.connect(self.add_category)

        self.edit_btn = QPushButton("✏️ Editar")
        self.edit_btn.clicked.connect(self.edit_selected_category)
        self.edit_btn.setEnabled(False)

        self.delete_btn = QPushButton("🗑️ Eliminar")
        self.delete_btn.clicked.connect(self.delete_selected_category)
        self.delete_btn.setEnabled(False)

        layout.addWidget(self.add_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)

        return panel

    def create_categories_table(self) -> QTableWidget:
        """Crear la tabla de categorías"""
        table = QTableWidget()
        table.setObjectName("CategoriesTable")

        # Configurar columnas
        headers = ["ID", "Nombre", "Descripción", "Productos", "Creada", "Modificada"]
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
            header.setSectionResizeMode(
                2, QHeaderView.ResizeMode.Stretch
            )  # Descripción
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Productos
            header.resizeSection(3, 80)
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Creada
            header.resizeSection(4, 120)
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Modificada
            header.resizeSection(5, 120)
        # Conectar señales
        table.itemSelectionChanged.connect(self.on_category_selected)
        table.itemDoubleClicked.connect(self.edit_selected_category)

        return table

    def create_stats_panel(self) -> QFrame:
        """Crear panel de estadísticas"""
        panel = QFrame()
        panel.setObjectName("StatsPanel")
        layout = QHBoxLayout(panel)

        # Estadísticas básicas
        self.total_categories_label = QLabel("Total: 0")
        self.used_categories_label = QLabel("En uso: 0")
        self.empty_categories_label = QLabel("Vacías: 0")

        layout.addWidget(QLabel("📊"))
        layout.addWidget(self.total_categories_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.used_categories_label)
        layout.addWidget(QLabel("|"))
        layout.addWidget(self.empty_categories_label)
        layout.addStretch()

        return panel

    def load_categories(self):
        """Cargar categorías desde el servicio"""
        try:
            self.categorias_cache = self.inventario_service.get_categorias_completas()
            self.update_categories_table()
            self.update_statistics()
        except Exception as e:
            logger.error(f"Error cargando categorías: {e}")
            QMessageBox.warning(
                self, "Error", f"No se pudieron cargar las categorías: {str(e)}"
            )

    def update_categories_table(self):
        """Actualizar la tabla de categorías"""
        try:
            # Las categorías ahora son objetos completos con todos los campos
            self.categories_table.setRowCount(len(self.categorias_cache))

            for row, categoria in enumerate(self.categorias_cache):
                # ID
                self.categories_table.setItem(
                    row, 0, QTableWidgetItem(str(categoria.get("id", "N/A")))
                )

                # Nombre
                self.categories_table.setItem(
                    row, 1, QTableWidgetItem(categoria.get("nombre", ""))
                )

                # Descripción
                descripcion = (
                    categoria.get("descripcion", "")
                    or f"Categoría: {categoria.get('nombre', '')}"
                )
                self.categories_table.setItem(row, 2, QTableWidgetItem(descripcion))

                # Número de productos
                productos_count = self.get_products_count_for_category(
                    categoria.get("nombre", "")
                )
                self.categories_table.setItem(
                    row, 3, QTableWidgetItem(str(productos_count))
                )

                # Fecha creada
                fecha_creada = categoria.get("fecha_creacion", "N/A")
                if fecha_creada and fecha_creada != "N/A":
                    try:
                        # Formatear fecha si es necesario
                        if len(str(fecha_creada)) > 16:
                            fecha_creada = str(fecha_creada)[:16]
                    except:
                        fecha_creada = "N/A"
                self.categories_table.setItem(
                    row, 4, QTableWidgetItem(str(fecha_creada))
                )

                # Fecha modificada
                fecha_modificada = categoria.get("fecha_modificacion", "N/A") or "N/A"
                if fecha_modificada and fecha_modificada != "N/A":
                    try:
                        # Formatear fecha si es necesario
                        if len(str(fecha_modificada)) > 16:
                            fecha_modificada = str(fecha_modificada)[:16]
                    except:
                        fecha_modificada = "N/A"
                self.categories_table.setItem(
                    row, 5, QTableWidgetItem(str(fecha_modificada))
                )

        except Exception as e:
            logger.error(f"Error actualizando tabla de categorías: {e}")

    def get_products_count_for_category(self, categoria_nombre: str) -> int:
        """Obtener el número de productos para una categoría"""
        try:
            productos = self.inventario_service.get_productos(
                categoria=categoria_nombre
            )
            return len(productos)
        except:
            return 0

    def update_statistics(self):
        """Actualizar estadísticas"""
        try:
            total = len(self.categorias_cache)
            used = 0
            empty = 0

            # Las categorías ahora son objetos completos
            for categoria in self.categorias_cache:
                categoria_nombre = categoria.get("nombre", "")
                count = self.get_products_count_for_category(categoria_nombre)
                if count > 0:
                    used += 1
                else:
                    empty += 1

            self.total_categories_label.setText(f"Total: {total}")
            self.used_categories_label.setText(f"En uso: {used}")
            self.empty_categories_label.setText(f"Vacías: {empty}")
        except Exception as e:
            logger.error(f"Error actualizando estadísticas: {e}")

    def filter_categories(self, text: str):
        """Filtrar categorías por texto"""
        try:
            for row in range(self.categories_table.rowCount()):
                nombre_item = self.categories_table.item(row, 1)
                desc_item = self.categories_table.item(row, 2)

                show_row = False
                if nombre_item and text.lower() in nombre_item.text().lower():
                    show_row = True
                elif desc_item and text.lower() in desc_item.text().lower():
                    show_row = True

                self.categories_table.setRowHidden(row, not show_row)

        except Exception as e:
            logger.error(f"Error filtrando categorías: {e}")

    def on_category_selected(self):
        """Manejar selección de categoría"""
        selected_rows = set(
            item.row() for item in self.categories_table.selectedItems()
        )
        has_selection = bool(selected_rows)

        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)

        if has_selection:
            row = next(iter(selected_rows))
            if row < len(self.categorias_cache):
                categoria = self.categorias_cache[
                    row
                ]  # Ya es un objeto completo                # Emitir la categoría completa
                self.categoria_seleccionada.emit(categoria)

    def add_category(self):
        """Agregar nueva categoría"""
        # Limpiar selección de la tabla para evitar conflictos
        self.categories_table.clearSelection()

        # Crear diálogo sin pasar categoría (modo creación)
        dialog = CategoryDialog(self.inventario_service, self, categoria=None)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_categories()
            self.categoria_actualizada.emit()
            # Limpiar selección después de crear
            self.categories_table.clearSelection()
            self.edit_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)

    def edit_selected_category(self):
        """Editar categoría seleccionada"""
        try:
            selected_rows = set(
                item.row() for item in self.categories_table.selectedItems()
            )
            if not selected_rows:
                return

            row = next(iter(selected_rows))
            if row < len(self.categorias_cache):
                categoria = self.categorias_cache[row]  # Ya es un objeto completo
                dialog = CategoryDialog(self.inventario_service, self, categoria)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.load_categories()
                    self.categoria_actualizada.emit()

        except Exception as e:
            logger.error(f"Error editando categoría: {e}")
            QMessageBox.warning(
                self, "Error", f"No se pudo editar la categoría: {str(e)}"
            )

    def delete_selected_category(self):
        """Eliminar categoría seleccionada"""
        try:
            selected_rows = set(
                item.row() for item in self.categories_table.selectedItems()
            )
            if not selected_rows:
                return

            row = next(iter(selected_rows))
            if row < len(self.categorias_cache):
                categoria = self.categorias_cache[row]  # Ya es un objeto completo
                categoria_nombre = categoria.get("nombre", "")
                categoria_id = categoria.get("id", None)

                if not categoria_nombre:
                    QMessageBox.warning(
                        self, "Error", "No se puede identificar la categoría"
                    )
                    return

                # Verificar si tiene productos
                productos_count = self.get_products_count_for_category(categoria_nombre)

                if productos_count > 0:
                    QMessageBox.warning(
                        self,
                        "No se puede eliminar",
                        f"La categoría '{categoria_nombre}' tiene {productos_count} producto(s) asociado(s). "
                        "No se puede eliminar una categoría con productos.",
                    )
                    return

                # Confirmar eliminación
                reply = QMessageBox.question(
                    self,
                    "Confirmar eliminación",
                    f"¿Estás seguro de que deseas eliminar la categoría '{categoria_nombre}'?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                )

                if reply == QMessageBox.StandardButton.Yes:
                    # Usar el ID de la categoría para eliminar (más seguro)
                    success = False
                    if categoria_id:
                        # Intentar eliminar por ID primero
                        success = self.inventario_service.eliminar_categoria_por_id(
                            categoria_id
                        )

                    if not success:
                        # Fallback: eliminar por nombre
                        success = self.inventario_service.eliminar_categoria(
                            categoria_nombre
                        )

                    if success:
                        self.load_categories()
                        self.categoria_actualizada.emit()
                        QMessageBox.information(
                            self, "Éxito", "Categoría eliminada correctamente"
                        )
                    else:
                        QMessageBox.warning(
                            self, "Error", "No se pudo eliminar la categoría"
                        )

        except Exception as e:
            logger.error(f"Error eliminando categoría: {e}")
            QMessageBox.warning(
                self, "Error", f"No se pudo eliminar la categoría: {str(e)}"
            )

    def apply_styles(self):
        """Aplicar estilos al widget"""
        self.setStyleSheet(
            """
            #HeaderFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
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
              #CategoriesTable {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 6px;
                gridline-color: #f1f5f9;
                selection-background-color: #3b82f6;
                selection-color: white;
                outline: none;
            }
            
            #CategoriesTable::item {
                padding: 8px;
                border-bottom: 1px solid #f1f5f9;
                border: none;
            }
            
            #CategoriesTable::item:selected {
                background: #3b82f6;
                color: white;
                border: none;
                outline: none;
            }
            
            #CategoriesTable::item:hover {
                background: #e6f3ff;
            }
            
            #CategoriesTable QHeaderView::section {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                padding: 8px;
                font-weight: bold;
                color: #374151;
            }
            
            #CategoriesTable QHeaderView::section:horizontal {
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
            
            QLineEdit {
                border: 2px solid #e2e8f0;
                border-radius: 4px;
                padding: 6px;
                font-size: 14px;
            }
            
            QLineEdit:focus {
                border-color: #3b82f6;
            }
        """
        )


class CategoryDialog(QDialog):
    """Diálogo mejorado para crear/editar categorías con validaciones avanzadas"""

    def __init__(self, inventario_service, parent=None, categoria=None):
        super().__init__(parent)

        self.inventario_service = inventario_service
        self.categoria = categoria
        self.is_edit_mode = categoria is not None

        # Log para debugging
        logger.info(
            f"CategoryDialog iniciado - Modo: {'Edición' if self.is_edit_mode else 'Creación'}"
        )
        if self.is_edit_mode and self.categoria:
            logger.info(
                f"Editando categoría ID: {self.categoria.get('id', 'N/A')} - Nombre: {self.categoria.get('nombre', 'N/A')}"
            )
        else:
            logger.info("Creando nueva categoría")

        self.init_ui()
        self.setup_validations()

        if self.is_edit_mode and self.categoria:
            self.load_category_data()

    def init_ui(self):
        """Inicializar interfaz del diálogo mejorada"""
        self.setWindowTitle(
            "✏️ Editar Categoría" if self.is_edit_mode else "➕ Nueva Categoría"
        )
        self.setModal(True)
        self.resize(500, 350)

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
            .error-label {
                color: #dc3545;
                font-size: 12px;
            }
        """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Header con icono
        header_layout = QHBoxLayout()
        header_icon = QLabel("📂")
        header_icon.setFont(QFont("Arial", 24))
        header_text = QLabel("Gestión de Categoría")
        header_text.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header_layout.addWidget(header_icon)
        header_layout.addWidget(header_text)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Formulario principal
        form_group = QGroupBox("📋 Información de la Categoría")
        form_layout = QGridLayout(form_group)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(10)

        # Nombre (obligatorio)
        name_label = QLabel("* Nombre:")
        name_label.setStyleSheet("color: #212529; font-weight: 600;")
        form_layout.addWidget(name_label, 0, 0)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText(
            "Ingrese el nombre de la categoría (requerido)"
        )
        self.name_input.setMaxLength(100)
        form_layout.addWidget(self.name_input, 0, 1)

        # Label de error para nombre
        self.name_error_label = QLabel("")
        self.name_error_label.setObjectName("errorLabel")
        self.name_error_label.setStyleSheet("color: #dc3545; font-size: 12px;")
        form_layout.addWidget(self.name_error_label, 1, 1)

        # Descripción
        desc_label = QLabel("Descripción:")
        desc_label.setStyleSheet("color: #212529; font-weight: 600;")
        form_layout.addWidget(desc_label, 2, 0, Qt.AlignmentFlag.AlignTop)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Descripción detallada de la categoría (opcional)"
        )
        self.description_input.setMaximumHeight(100)
        form_layout.addWidget(self.description_input, 2, 1)

        # Contador de caracteres
        self.char_counter = QLabel("0/500 caracteres")
        self.char_counter.setStyleSheet("color: #6c757d; font-size: 11px;")
        form_layout.addWidget(self.char_counter, 3, 1, Qt.AlignmentFlag.AlignRight)

        layout.addWidget(form_group)

        # Información adicional en modo edición
        if self.is_edit_mode:
            info_group = QGroupBox("ℹ️ Información del Sistema")
            info_layout = QGridLayout(info_group)

            # ID
            info_layout.addWidget(QLabel("ID:"), 0, 0)
            self.id_label = QLabel("N/A")
            self.id_label.setStyleSheet("font-weight: 600; color: #495057;")
            info_layout.addWidget(self.id_label, 0, 1)

            # Fecha de creación
            info_layout.addWidget(QLabel("Creada:"), 1, 0)
            self.created_label = QLabel("N/A")
            info_layout.addWidget(self.created_label, 1, 1)

            # Número de productos
            info_layout.addWidget(QLabel("Productos:"), 2, 0)
            self.products_count_label = QLabel("0")
            self.products_count_label.setStyleSheet("font-weight: 600; color: #28a745;")
            info_layout.addWidget(self.products_count_label, 2, 1)

            layout.addWidget(info_group)

        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.cancel_btn = QPushButton("❌ Cancelar")
        self.cancel_btn.setObjectName("cancelBtn")
        self.cancel_btn.clicked.connect(self.reject)

        self.save_btn = QPushButton("💾 Guardar" if self.is_edit_mode else "✅ Crear")
        self.save_btn.setObjectName("saveBtn")
        self.save_btn.clicked.connect(self.save_category)
        self.save_btn.setDefault(True)

        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)

        layout.addLayout(buttons_layout)

    def setup_validations(self):
        """Configurar validaciones en tiempo real"""
        # Validación del nombre
        self.name_input.textChanged.connect(self.validate_name)

        # Contador de caracteres para descripción
        self.description_input.textChanged.connect(self.update_char_counter)

    def validate_name(self):
        """Validar el campo nombre en tiempo real"""
        name = self.name_input.text().strip()

        if not name:
            self.name_error_label.setText("❌ El nombre es obligatorio")
            self.name_input.setStyleSheet("border: 2px solid #dc3545;")
            self.save_btn.setEnabled(False)
            return False
        elif len(name) < 2:
            self.name_error_label.setText(
                "⚠️ El nombre debe tener al menos 2 caracteres"
            )
            self.name_input.setStyleSheet("border: 2px solid #ffc107;")
            self.save_btn.setEnabled(False)
            return False
        else:
            self.name_error_label.setText("")
            self.name_input.setStyleSheet("")
            self.save_btn.setEnabled(True)
            return True

    def update_char_counter(self):
        """Actualizar contador de caracteres para descripción"""
        text = self.description_input.toPlainText()
        char_count = len(text)

        if char_count > 500:
            # Truncar texto si excede el límite
            self.description_input.setPlainText(text[:500])
            char_count = 500

        self.char_counter.setText(f"{char_count}/500 caracteres")

        if char_count > 450:
            self.char_counter.setStyleSheet(
                "color: #dc3545; font-size: 11px; font-weight: bold;"
            )
        elif char_count > 400:
            self.char_counter.setStyleSheet(
                "color: #ffc107; font-size: 11px; font-weight: bold;"
            )
        else:
            self.char_counter.setStyleSheet("color: #6c757d; font-size: 11px;")

    def load_category_data(self):
        """Cargar datos de la categoría en edición"""
        if self.categoria:
            self.name_input.setText(self.categoria.get("nombre", ""))
            self.description_input.setPlainText(self.categoria.get("descripcion", ""))

            # Información del sistema
            if hasattr(self, "id_label"):
                self.id_label.setText(str(self.categoria.get("id", "N/A")))
            if hasattr(self, "created_label"):
                created = self.categoria.get("fecha_creacion", "N/A")
                if created != "N/A":
                    try:
                        from datetime import datetime

                        if isinstance(created, str):
                            dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                            created = dt.strftime("%d/%m/%Y %H:%M")
                    except:
                        pass
                self.created_label.setText(str(created))
            # Actualizar contador de caracteres
            self.update_char_counter()  # Validar nombre cargado
            self.validate_name()

    def save_category(self):
        """Guardar la categoría con validaciones completas"""
        # Validar formulario completo
        if not self.validate_form():
            return

        try:
            nombre = self.name_input.text().strip()
            descripcion = self.description_input.toPlainText().strip()

            # Log detallado para debugging
            logger.info(
                f"Guardando categoría - Modo: {'Edición' if self.is_edit_mode else 'Creación'}"
            )
            logger.info(
                f"Datos: nombre='{nombre}', descripción='{descripcion[:50]}...'"
            )

            if self.is_edit_mode and self.categoria:
                # Actualizar categoría existente
                categoria_id = self.categoria.get("id")
                logger.info(f"Actualizando categoría existente ID: {categoria_id}")

                success = self.inventario_service.actualizar_categoria(
                    categoria_id, nombre, descripcion
                )
                message = (
                    "Categoría actualizada exitosamente"
                    if success
                    else "Error al actualizar la categoría"
                )
            else:
                # Crear nueva categoría
                logger.info("Creando nueva categoría")
                success = self.inventario_service.crear_categoria(nombre, descripcion)
                message = (
                    "Categoría creada exitosamente"
                    if success
                    else "Error al crear la categoría"
                )

            if success:
                QMessageBox.information(self, "✅ Éxito", message)
                self.accept()
            else:
                QMessageBox.warning(self, "⚠️ Error", message)

        except Exception as e:
            logger.error(f"Error al guardar categoría: {e}")
            QMessageBox.critical(
                self,
                "❌ Error Crítico",
                f"Error inesperado al guardar la categoría:\n{str(e)}",
            )

    def validate_form(self):
        """Validar todo el formulario antes de guardar"""
        is_valid = True
        error_messages = []

        # Validar nombre
        if not self.validate_name():
            is_valid = False
            error_messages.append(
                "• El nombre es obligatorio y debe tener al menos 2 caracteres"
            )

        # Validar descripción (opcional pero con límite)
        description = self.description_input.toPlainText().strip()
        if len(description) > 500:
            is_valid = False
            error_messages.append("• La descripción no puede exceder 500 caracteres")

        # Mostrar errores si los hay
        if not is_valid:
            error_text = "Por favor, corrija los siguientes errores:\n\n" + "\n".join(
                error_messages
            )
            QMessageBox.warning(self, "⚠️ Errores de Validación", error_text)

        return is_valid
