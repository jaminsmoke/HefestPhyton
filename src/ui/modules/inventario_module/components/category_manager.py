"""
Módulo de Gestión de Categorías para Hefest
==========================================

Interfaz dedicada para la gestión completa de categorías de productos
"""

import logging
from typing import Optional, List, Dict, Any

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
    QMessageBox,
    QDialog,
    QTextEdit,
    QDialogButtonBox,
    QFormLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

# Importar utilidades comunes
from .inventory_common_utils import (
    InventoryManagerBase,
    InventoryDialogBase,
    InventoryValidationUtils,
    CommonInventoryStyles,
)

logger = logging.getLogger(__name__)


class CategoryManagerWidget(InventoryManagerBase):
    """Widget especializado para la gestión de categorías"""

    # Señales
    categoria_actualizada = pyqtSignal()
    categoria_seleccionada = pyqtSignal(dict)

    def __init__(
        self, inventario_service: Any, parent: Optional[QWidget] = None
    ) -> None:
        """Inicializar el widget gestor de categorías"""
        # PRIMERO: Almacenar el servicio de inventario
        self.inventario_service = inventario_service
        self.categorias_cache: List[Dict[str, Any]] = []

        # Inicializar mapeos de IDs virtuales a reales
        self.id_mapping: Dict[int, int] = {}  # virtual_id -> real_id
        self.reverse_id_mapping: Dict[int, int] = {}  # real_id -> virtual_id

        # SEGUNDO: Pasar db_manager desde el inventario_service si está disponible
        db_manager = (
            getattr(inventario_service, "db_manager", None) or inventario_service
        )

        # IMPORTANTE: Indicar que no queremos carga automática al inicio
        self._skip_initial_load = True

        super().__init__(db_manager=db_manager, parent=parent)

        # TERCERO: Configuraciones adicionales
        self.title_label.setText("🏷️ Gestión de Categorías")

        # Configurar tabla específica para categorías
        self._configure_categories_table()

        # AHORA cargar datos después de que todo esté inicializado
        self._skip_initial_load = False
        self.load_categories()

        logger.info("CategoryManagerWidget inicializado correctamente")

    def _configure_categories_table(self):
        """Configurar la tabla específicamente para categorías"""
        # Configurar columnas
        headers = ["ID", "Nombre", "Descripción", "Productos", "Creada", "Modificada"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Configurar tabla
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)

        # Ajustar columnas
        header = self.table.horizontalHeader()
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

    def load_categories(self) -> None:
        """Cargar categorías desde el servicio"""
        try:
            logger.info("Cargando categorías desde el servicio...")
            self.categorias_cache = self.inventario_service.get_categorias_completas()  # type: ignore
            logger.info(f"Obtenidas {len(self.categorias_cache)} categorías")

            if self.categorias_cache:
                self.update_categories_table()
                # self.update_statistics()  # Comentado temporalmente
                logger.info("Categorías cargadas exitosamente")
            else:
                logger.warning("No se obtuvieron categorías del servicio")

        except Exception as e:
            logger.error(f"Error cargando categorías: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            QMessageBox.warning(
                self, "Error", f"No se pudieron cargar las categorías: {str(e)}"
            )

    def update_categories_table(self) -> None:
        """Actualizar la tabla de categorías con IDs reorganizados"""
        try:
            # Verificar que la tabla existe
            if not hasattr(self, "table") or self.table is None:
                logger.error("table no existe o es None")
                return

            # IMPORTANTE: Actualizar items_cache para que la clase base funcione
            self.items_cache = self.categorias_cache

            # Reorganizar categorías: activas primero con IDs consecutivos
            categorias_activas = [
                cat for cat in self.categorias_cache if cat.get("activa", True)
            ]
            categorias_inactivas = [
                cat for cat in self.categorias_cache if not cat.get("activa", True)
            ]

            # Crear mapeo de ID real a ID virtual para operaciones
            self.id_mapping = {}  # ID_virtual -> ID_real
            self.reverse_id_mapping = {}  # ID_real -> ID_virtual

            # Asignar IDs virtuales consecutivos
            virtual_id = 1
            for categoria in categorias_activas:
                real_id = categoria.get("id")
                self.id_mapping[virtual_id] = real_id
                self.reverse_id_mapping[real_id] = virtual_id
                categoria["virtual_id"] = virtual_id
                virtual_id += 1

            # Las inactivas mantienen sus IDs reales pero no se muestran
            # (por si en el futuro queremos mostrarlas)

            # Solo mostrar categorías activas
            categorias_a_mostrar = categorias_activas
            self.table.setRowCount(len(categorias_a_mostrar))

            for row, categoria in enumerate(categorias_a_mostrar):
                # ID Virtual (consecutivo)
                virtual_id = categoria["virtual_id"]
                self.table.setItem(row, 0, QTableWidgetItem(str(virtual_id)))

                # Nombre
                self.table.setItem(
                    row, 1, QTableWidgetItem(categoria.get("nombre", ""))
                )

                # Descripción
                descripcion = (
                    categoria.get("descripcion", "")
                    or f"Categoría: {categoria.get('nombre', '')}"
                )
                self.table.setItem(row, 2, QTableWidgetItem(descripcion))

                # Número de productos
                productos_count = self.get_products_count_for_category(
                    categoria.get("nombre", "")
                )
                self.table.setItem(row, 3, QTableWidgetItem(str(productos_count)))

                # Fecha creada
                fecha_creada = categoria.get("fecha_creacion", "N/A")
                if fecha_creada and fecha_creada != "N/A":
                    try:
                        # Formatear fecha si es necesario
                        if len(str(fecha_creada)) > 16:
                            fecha_creada = str(fecha_creada)[:16]
                    except:
                        fecha_creada = "N/A"
                self.table.setItem(row, 4, QTableWidgetItem(str(fecha_creada)))

                # Fecha modificada
                fecha_modificada = categoria.get("fecha_modificacion", "N/A") or "N/A"
                if fecha_modificada and fecha_modificada != "N/A":
                    try:
                        # Formatear fecha si es necesario
                        if len(str(fecha_modificada)) > 16:
                            fecha_modificada = str(fecha_modificada)[:16]
                    except:
                        fecha_modificada = "N/A"
                self.table.setItem(row, 5, QTableWidgetItem(str(fecha_modificada)))

        except Exception as e:
            logger.error(f"Error actualizando tabla de categorías: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")

    def get_products_count_for_category(self, categoria_nombre: str) -> int:
        """Obtener el número de productos para una categoría"""
        try:
            productos = self.inventario_service.get_productos(
                categoria=categoria_nombre
            )
            return len(productos)
        except:
            return 0

    def update_statistics(self) -> None:
        """Actualizar estadísticas"""
        try:
            total = len(self.categorias_cache)
            used = 0
            empty = 0

            # Las categorías ahora son objetos completos
            for categoria in self.categorias_cache:
                categoria_nombre = categoria.get("nombre", "")  # type: ignore
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

    def filter_categories(self, text: str) -> None:
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

    def add_new_category(self) -> None:
        """Agregar nueva categoría"""
        try:
            dialog = CategoryDialog(self.inventario_service, self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.load_categories()
                self.categoria_actualizada.emit()
                logger.info("Nueva categoría agregada exitosamente")
        except Exception as e:
            logger.error(f"Error al agregar categoría: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo agregar la categoría: {e}")

    def edit_selected_category(self) -> None:
        """Editar categoría seleccionada"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(
                self,
                "Selección requerida",
                "Por favor, selecciona una categoría para editar.",
            )
            return

        try:
            # Obtener ID virtual de la tabla
            virtual_id = int(self.table.item(current_row, 0).text())
            # Convertir a ID real usando el mapeo
            categoria_id = self.id_mapping.get(virtual_id)

            if not categoria_id:
                QMessageBox.warning(
                    self, "Error", "No se pudo obtener el ID de la categoría"
                )
                return

            categoria = next(
                (c for c in self.categorias_cache if c.get("id") == categoria_id), None
            )

            if categoria:
                dialog = CategoryDialog(self.inventario_service, self, categoria)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    self.load_categories()
                    self.categoria_actualizada.emit()
                    logger.info(f"Categoría {categoria_id} editada exitosamente")
        except Exception as e:
            logger.error(f"Error al editar categoría: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo editar la categoría: {e}")

    def delete_selected_category(self) -> None:
        """Eliminar categoría seleccionada"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.information(
                self,
                "Selección requerida",
                "Por favor, selecciona una categoría para eliminar.",
            )
            return

        try:
            # Obtener ID virtual de la tabla
            virtual_id = int(self.table.item(current_row, 0).text())
            # Convertir a ID real usando el mapeo
            categoria_id = self.id_mapping.get(virtual_id)

            if not categoria_id:
                QMessageBox.warning(
                    self, "Error", "No se pudo obtener el ID de la categoría"
                )
                return

            nombre = self.table.item(current_row, 1).text()

            logger.debug(
                f"Intentando eliminar categoría ID: {categoria_id}, Nombre: {nombre}"
            )

            reply = QMessageBox.question(
                self,
                "Confirmar eliminación",
                f"¿Estás seguro de que quieres eliminar la categoría '{nombre}'?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                logger.debug(
                    f"Usuario confirmó eliminación de categoría ID: {categoria_id}"
                )
                # Usar el método correcto para eliminar por ID
                if self.inventario_service.eliminar_categoria_por_id(categoria_id):
                    self.load_categories()
                    self.categoria_actualizada.emit()
                    logger.info(f"Categoría {categoria_id} eliminada exitosamente")
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "No se pudo eliminar la categoría. Puede tener productos asociados.",
                    )
        except Exception as e:
            logger.error(f"Error al eliminar categoría: {e}")
            QMessageBox.warning(self, "Error", f"No se pudo eliminar la categoría: {e}")

    def on_category_selected(self) -> None:
        """Manejar selección de categoría"""
        current_row = self.table.currentRow()
        if current_row >= 0:
            try:
                # Obtener ID virtual de la tabla
                virtual_id = int(self.table.item(current_row, 0).text())
                # Convertir a ID real usando el mapeo
                categoria_id = self.id_mapping.get(virtual_id)

                if categoria_id:
                    categoria = next(
                        (
                            c
                            for c in self.categorias_cache
                            if c.get("id") == categoria_id
                        ),
                        None,
                    )
                    if categoria:
                        self.categoria_seleccionada.emit(categoria)
            except Exception as e:
                logger.error(f"Error al seleccionar categoría: {e}")

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

    # Métodos de la clase base que necesitamos implementar
    def add_item(self):
        """Agregar nueva categoría"""
        self.add_new_category()

    def edit_item(self):
        """Editar categoría seleccionada"""
        self.edit_selected_category()

    def delete_item(self):
        """Eliminar categoría seleccionada"""
        self.delete_selected_category()

    def _on_selection_changed(self, current, previous):
        """Manejar cambio de selección - llamado por la clase base"""
        # Llamar al método base para actualizar estado de botones
        super()._on_selection_changed(current, previous)
        # Luego ejecutar lógica específica de categorías
        self.on_category_selected()

    def _setup_category_table(self):
        """Configura la tabla específica para categorías"""
        headers = ["ID", "Nombre", "Descripción", "Productos", "Creada", "Modificada"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        # Configurar columnas
        header = self.table.horizontalHeader()
        if header:
            header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # ID
            header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Nombre
            header.setSectionResizeMode(
                2, QHeaderView.ResizeMode.Stretch
            )  # Descripción
            header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Productos
            header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)  # Creada
            header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Modificada

            # Anchos específicos
            self.table.setColumnWidth(0, 60)
            self.table.setColumnWidth(3, 80)
            self.table.setColumnWidth(4, 100)
            self.table.setColumnWidth(5, 100)

        # Conectar señales específicas - NO sobrescribir las de la clase base
        # La clase base ya conecta currentRowChanged para manejar estado de botones
        self.table.itemDoubleClicked.connect(self.edit_selected_category)

    def _load_data(self):
        """Cargar datos específicos de categorías"""
        # Si estamos en inicialización y tenemos la bandera, saltar
        if hasattr(self, "_skip_initial_load") and self._skip_initial_load:
            logger.debug("Saltando carga inicial de categorías")
            return

        # Solo cargar si la UI está completamente inicializada
        if hasattr(self, "table") and hasattr(self, "inventario_service"):
            self.load_categories()
        else:
            logger.debug("UI no inicializada aún, posponiendo carga de categorías")


class CategoryDialog(InventoryDialogBase):
    """Diálogo para agregar/editar categorías"""

    def __init__(self, inventario_service, parent=None, categoria=None):
        self.inventario_service = inventario_service
        self.categoria_data = categoria
        self.is_edit = categoria is not None

        title = "Editar Categoría" if self.is_edit else "Nueva Categoría"
        super().__init__(parent, title, (400, 300))

        if self.is_edit:
            self._load_category_data()

    def _setup_ui(self):
        """Configuración específica de UI para categorías"""
        super()._setup_ui()

        # Formulario de categoría
        form_layout = QFormLayout()

        # Campo nombre
        self.name_edit = QLineEdit()
        form_layout.addRow("Nombre*:", self.name_edit)

        # Campo descripción
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        form_layout.addRow("Descripción:", self.description_edit)

        self.add_form_section("Información de Categoría", form_layout)

    def _load_category_data(self):
        """Cargar datos de categoría para edición"""
        if self.categoria_data:
            self.name_edit.setText(str(self.categoria_data.get("nombre", "")))
            self.description_edit.setPlainText(
                str(self.categoria_data.get("descripcion", ""))
            )

    def accept(self):
        """Validar y guardar categoría"""
        if not self._validate_form():
            return

        try:
            nombre = self.name_edit.text().strip()
            descripcion = self.description_edit.toPlainText().strip()

            if self.is_edit:
                categoria_id = self.categoria_data["id"]
                success = self.inventario_service.actualizar_categoria(
                    categoria_id, nombre, descripcion
                )
                message = "Categoría actualizada correctamente"
            else:
                success = self.inventario_service.crear_categoria(nombre, descripcion)
                message = "Categoría creada correctamente"

            if success:
                self.show_success(message)
                super().accept()
            else:
                self.show_error("Error al guardar la categoría")

        except Exception as e:
            logger.error(f"Error guardando categoría: {e}")
            self.show_error(f"Error inesperado: {str(e)}")

    def _validate_form(self) -> bool:
        """Validar formulario de categoría"""
        if not InventoryValidationUtils.validate_required_field(
            self.name_edit.text(), "Nombre"
        ):
            self.show_error("El nombre es obligatorio")
            self.name_edit.setFocus()
            return False

        if not InventoryValidationUtils.validate_text_length(
            self.name_edit.text(), "Nombre", 1, 100
        ):
            self.show_error("El nombre debe tener entre 1 y 100 caracteres")
            self.name_edit.setFocus()
            return False

        return True
