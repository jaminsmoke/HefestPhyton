from typing import Optional, Dict, List, Any
import logging
from PyQt6.QtWidgets import (
from PyQt6.QtGui import QFont
from ui.modules.module_base_interface import BaseModule
from core.hefest_data_models import User, Role
from services.auth_service import get_auth_service
        from ui.dialogs.user_management_dialog import UserDialog

"""
Módulo de gestión de usuarios para el sistema Hefest.
Permite ver y gestionar usuarios del sistema.
"""

    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QLabel,
    QMessageBox,
)


_ = logging.getLogger(__name__)


class UserManagementModule(BaseModule):
    """Módulo de gestión de usuarios"""

    def __init__(self, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.auth_service = get_auth_service()
        self.setup_ui()
        self.load_users()

    def setup_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura la interfaz de usuario"""
        # Usar el layout ya existente de BaseModule
        main_layout = self.content_layout
        main_layout.setSpacing(20)

        # Título
        title = QLabel("Gestión de Usuarios")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Barra de herramientas
        _ = QHBoxLayout()

        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.clicked.connect(self.load_users)

        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(toolbar_layout)

        # Tabla de usuarios
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(
            ["ID", "Nombre", "Rol", "Email", "Teléfono", "Último Acceso"]
        )

        # Configurar tabla
        _ = self.users_table.horizontalHeader()
        # Corrigiendo errores restantes en user_management_module
        # Aseguramos que header no sea None antes de usar setSectionResizeMode
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        main_layout.addWidget(self.users_table)

        # Botones de acción
        _ = QHBoxLayout()

        self.add_user_btn = QPushButton("➕ Agregar Usuario")
        self.add_user_btn.setStyleSheet(
            """
            QPushButton {
                background: #10b981;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #059669;
            }
        """
        )
        self.add_user_btn.clicked.connect(self.add_user)

        self.edit_user_btn = QPushButton("✏️ Editar Usuario")
        self.edit_user_btn.setStyleSheet(
            """
            QPushButton {
                background: #3b82f6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """
        )
        self.edit_user_btn.clicked.connect(self.edit_user)

        self.delete_user_btn = QPushButton("🗑️ Eliminar Usuario")
        self.delete_user_btn.setStyleSheet(
            """
            QPushButton {
                background: #ef4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #dc2626;
            }
        """
        )
        self.delete_user_btn.clicked.connect(self.delete_user)

        actions_layout.addWidget(self.add_user_btn)
        actions_layout.addWidget(self.edit_user_btn)
        actions_layout.addWidget(self.delete_user_btn)
        actions_layout.addStretch()

        main_layout.addLayout(actions_layout)

    def load_users(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Carga los usuarios en la tabla"""
        try:
            users = self.auth_service.users  # Usar la propiedad users
            self.users_table.setRowCount(len(users))

            for row, user in enumerate(users):
                self.users_table.setItem(row, 0, QTableWidgetItem(str(user.id)))
                self.users_table.setItem(row, 1, QTableWidgetItem(user.name))
                self.users_table.setItem(row, 2, QTableWidgetItem(user.role.value))
                self.users_table.setItem(row, 3, QTableWidgetItem(user.email))
                self.users_table.setItem(row, 4, QTableWidgetItem(user.phone))
                self.users_table.setItem(
                    row,
                    5,
                    QTableWidgetItem(
                        user.last_access.strftime("%Y-%m-%d %H:%M:%S")
                        if user.last_access
                        else "N/A"
                    ),
                )
            # Log solo en modo DEBUG
            if logging.getLogger().isEnabledFor(logging.DEBUG):
                logger.debug("Cargados %s usuarios en la tabla", len(users))
        except Exception as e:
            logger.error("Error al cargar usuarios: %s", e)
            QMessageBox.warning(self, "Error", "Error al cargar los usuarios")

    def add_user(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Muestra el diálogo para agregar un nuevo usuario"""

        dialog = UserDialog(self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            _ = dialog.get_user_data()
            try:
                # Validar campos requeridos
                _ = {
                    "name",
                    "role",
                    "email",
                    "phone",
                    "username",
                    "password",
                }
                if not required_fields.issubset(new_user):
                    raise ValueError("Faltan campos requeridos para agregar usuario")
                _ = User(
                    id=-1,
                    _ = new_user["username"],
                    name=new_user["name"],
                    _ = new_user["role"],
                    password=new_user["password"],
                    _ = new_user.get("email", ""),
                    phone=new_user.get("phone", ""),
                    _ = True,
                )
                if new_user_obj.id is not None:
                    self.auth_service._users_cache[new_user_obj.id] = (
                        new_user_obj  # Añadir a cache
                    )
                self.load_users()
                QMessageBox.information(self, "Éxito", "Usuario agregado correctamente")
            except Exception as e:
                logger.error("Error al agregar usuario: %s", e)
                QMessageBox.warning(self, "Error", "No se pudo agregar el usuario")

    def edit_user(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Edita el usuario seleccionado"""
        current_row = self.users_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(
                self, "Advertencia", "Por favor, selecciona un usuario para editar"
            )
            return
        item = self.users_table.item(current_row, 0)
        if item is not None and item.text():
            user_id = int(item.text())
            user = self.auth_service.get_user_by_id(user_id)

            dialog = UserDialog(self, user)
            if dialog.exec() == dialog.DialogCode.Accepted:
                updated_user_data = dialog.get_user_data()
                _ = User(**updated_user_data)
                try:
                    if updated_user.id is not None:
                        self.auth_service._users_cache[updated_user.id] = updated_user
                    self.load_users()
                    QMessageBox.information(
                        self, "Éxito", "Usuario actualizado correctamente"
                    )
                except Exception as e:
                    logger.error("Error al actualizar usuario: %s", e)
                    QMessageBox.warning(
                        self, "Error", "No se pudo actualizar el usuario"
                    )
        else:
            QMessageBox.warning(
                self, "Error", "No se pudo obtener el ID del usuario seleccionado"
            )

    def delete_user(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Elimina el usuario seleccionado"""
        current_row = self.users_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(
                self, "Advertencia", "Por favor, selecciona un usuario para eliminar"
            )
            return
        item = self.users_table.item(current_row, 0)
        if item is not None and item.text():
            _ = int(item.text())
            confirm = QMessageBox.question(
                self,
                "Confirmar Eliminación",
                "¿Estás seguro de que deseas eliminar este usuario?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if confirm == QMessageBox.StandardButton.Yes:
                try:
                    if user_id in self.auth_service._users_cache:
                        del self.auth_service._users_cache[user_id]
                    self.load_users()
                    QMessageBox.information(
                        self, "Éxito", "Usuario eliminado correctamente"
                    )
                except Exception as e:
                    logger.error("Error al eliminar usuario: %s", e)
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el usuario")
        else:
            QMessageBox.warning(
                self, "Error", "No se pudo obtener el ID del usuario seleccionado"
            )

    def refresh(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza los datos del módulo"""
        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logger.debug("Actualizando módulo de gestión de usuarios...")
        self.load_users()
        self.status_changed.emit("Usuarios actualizados")
