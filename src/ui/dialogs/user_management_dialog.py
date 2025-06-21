"""
Diálogo para crear y editar usuarios del sistema.
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QPushButton,
    QLabel,
    QDialogButtonBox,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from core.hefest_data_models import Role


class UserDialog(QDialog):
    """Diálogo para crear/editar usuarios"""

    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Editar Usuario" if user else "Nuevo Usuario")
        self.setFixedSize(400, 300)
        self.setup_ui()

        if user:
            self.load_user_data()

    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout(self)

        # Título
        title = QLabel("Editar Usuario" if self.user else "Nuevo Usuario")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Formulario
        form_layout = QFormLayout()

        # Nombre
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Nombre completo del usuario")
        form_layout.addRow("Nombre:", self.name_edit)

        # Rol
        self.role_combo = QComboBox()
        self.role_combo.addItems([role.value for role in Role])
        form_layout.addRow("Rol:", self.role_combo)

        # PIN
        self.pin_edit = QLineEdit()
        self.pin_edit.setPlaceholderText("PIN de 4 dígitos")
        self.pin_edit.setMaxLength(10)
        form_layout.addRow("PIN:", self.pin_edit)

        # Email
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("correo@ejemplo.com")
        form_layout.addRow("Email:", self.email_edit)

        # Teléfono
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("+34-600-000-000")
        form_layout.addRow("Teléfono:", self.phone_edit)

        layout.addLayout(form_layout)

        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    def load_user_data(self):
        """Carga los datos del usuario para edición"""
        if self.user:
            self.name_edit.setText(self.user.name)

            # Buscar el índice del rol
            for i, role in enumerate(Role):
                if role == self.user.role:
                    self.role_combo.setCurrentIndex(i)
                    break

            self.pin_edit.setText(self.user.pin)
            self.email_edit.setText(self.user.email or "")
            self.phone_edit.setText(self.user.phone or "")

    def validate_and_accept(self):
        """Valida los datos antes de aceptar"""
        # Validar campos obligatorios
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Error", "El nombre es obligatorio")
            return

        if not self.pin_edit.text().strip():
            QMessageBox.warning(self, "Error", "El PIN es obligatorio")
            return

        # Validar longitud del PIN
        pin = self.pin_edit.text().strip()
        if len(pin) < 3:
            QMessageBox.warning(
                self, "Error", "El PIN debe tener al menos 3 caracteres"
            )
            return

        # Validar email si se proporciona
        email = self.email_edit.text().strip()
        if email and "@" not in email:
            QMessageBox.warning(self, "Error", "Email inválido")
            return

        self.accept()

    def get_user_data(self):
        """Obtiene los datos del formulario"""
        role_text = self.role_combo.currentText()
        role = next(role for role in Role if role.value == role_text)

        return {
            "nombre": self.name_edit.text().strip(),
            "role": role.name,  # Usar el nombre del enum para la BD
            "pin": self.pin_edit.text().strip(),
            "email": self.email_edit.text().strip() or None,
            "telefono": self.phone_edit.text().strip() or None,
        }
