"""
Módulo de gestión de usuarios para el sistema Hefest.
Permite ver y gestionar usuarios del sistema.
"""

import logging
from PyQt6.QtWidgets import (
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
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.modules.module_base_interface import BaseModule
from core.hefest_data_models import User, Role
from services.auth_service import get_auth_service
from services.audit_service import AuditService
from utils.decorators import require_role

logger = logging.getLogger(__name__)


class UserManagementModule(BaseModule):
    """Módulo de gestión de usuarios"""

    def __init__(self, parent=None):
        logger.info("Inicializando UserManagementModule...")
        super().__init__(parent)
        self.auth_service = get_auth_service()
        logger.info("AuthService inicializado correctamente.")
        self.setup_ui()
        logger.info("Interfaz de usuario configurada.")
        self.load_users()
        logger.info("Usuarios cargados en la tabla.")

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Usar el layout ya existente de BaseModule
        main_layout = self.content_layout
        main_layout.setSpacing(20)

        # Título
        title = QLabel("Gestión de Usuarios")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        main_layout.addWidget(title)

        # Barra de herramientas
        toolbar_layout = QHBoxLayout()

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
        header = self.users_table.horizontalHeader()
        # Corrigiendo errores restantes en user_management_module
        # Aseguramos que header no sea None antes de usar setSectionResizeMode
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        main_layout.addWidget(self.users_table)

        # Botones de acción
        actions_layout = QHBoxLayout()

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

            logger.info(f"Cargados {len(users)} usuarios en la tabla")

        except Exception as e:
            logger.error(f"Error al cargar usuarios: {e}")
            QMessageBox.warning(
                self, "Error", "Error al cargar los usuarios"
            )

    def add_user(self):
        """Muestra el diálogo para agregar un nuevo usuario"""
        from ui.dialogs.user_management_dialog import UserDialog
        dialog = UserDialog(self)
        if dialog.exec() == dialog.DialogCode.Accepted:
            new_user = dialog.get_user_data()
            try:
                # Validar campos requeridos
                required_fields = {"name", "role", "email", "phone", "username", "password"}
                if not required_fields.issubset(new_user):
                    raise ValueError("Faltan campos requeridos para agregar usuario")
                new_user_obj = User(
                    id=-1,
                    username=new_user["username"],
                    name=new_user["name"],
                    role=new_user["role"],
                    password=new_user["password"],
                    email=new_user.get("email", ""),
                    phone=new_user.get("phone", ""),
                    is_active=True
                )
                if new_user_obj.id is not None:
                    self.auth_service._users_cache[new_user_obj.id] = new_user_obj  # Añadir a cache
                self.load_users()
                QMessageBox.information(self, "Éxito", "Usuario agregado correctamente")
            except Exception as e:
                logger.error(f"Error al agregar usuario: {e}")
                QMessageBox.warning(self, "Error", "No se pudo agregar el usuario")

    def edit_user(self):
        """Edita el usuario seleccionado"""
        current_row = self.users_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un usuario para editar")
            return
        item = self.users_table.item(current_row, 0)
        if item is not None and item.text():
            user_id = int(item.text())
            user = self.auth_service.get_user_by_id(user_id)
            from ui.dialogs.user_management_dialog import UserDialog
            dialog = UserDialog(self, user)
            if dialog.exec() == dialog.DialogCode.Accepted:
                updated_user_data = dialog.get_user_data()
                updated_user = User(**updated_user_data)
                try:
                    if updated_user.id is not None:
                        self.auth_service._users_cache[updated_user.id] = updated_user
                    self.load_users()
                    QMessageBox.information(self, "Éxito", "Usuario actualizado correctamente")
                except Exception as e:
                    logger.error(f"Error al actualizar usuario: {e}")
                    QMessageBox.warning(self, "Error", "No se pudo actualizar el usuario")
        else:
            QMessageBox.warning(self, "Error", "No se pudo obtener el ID del usuario seleccionado")

    def delete_user(self):
        """Elimina el usuario seleccionado"""
        current_row = self.users_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Advertencia", "Por favor, selecciona un usuario para eliminar")
            return
        item = self.users_table.item(current_row, 0)
        if item is not None and item.text():
            user_id = int(item.text())
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
                    QMessageBox.information(self, "Éxito", "Usuario eliminado correctamente")
                except Exception as e:
                    logger.error(f"Error al eliminar usuario: {e}")
                    QMessageBox.warning(self, "Error", "No se pudo eliminar el usuario")
        else:
            QMessageBox.warning(self, "Error", "No se pudo obtener el ID del usuario seleccionado")

    def refresh(self):
        """Actualiza los datos del módulo"""
        logger.info("Actualizando módulo de gestión de usuarios...")
        self.load_users()
        self.status_changed.emit("Usuarios actualizados")
