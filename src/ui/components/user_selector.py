"""
Componente de selección de usuario para el sistema Hefest.
Presenta una interfaz para seleccionar un usuario de la lista disponible.
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QGridLayout
from PyQt6.QtCore import Qt, pyqtSignal
from core.hefest_data_models import User


class UserSelector(QDialog):
    user_selected = pyqtSignal(object)  # Cambiado de User a object para compatibilidad con PyQt y tests

    def __init__(self, auth_service, parent=None):
        super().__init__(parent)
        self.auth_service = auth_service
        self.setWindowTitle("Seleccionar Usuario")
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.FramelessWindowHint)
        self.setStyleSheet(
            """
            QDialog {
                background: #ffffff;
                border-radius: 10px;
                border: 1px solid #e2e8f0;
            }
            QPushButton {
                padding: 15px;
                background: #f1f5f9;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background: #e2e8f0;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 15px;
            }
        """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Seleccione su usuario")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Crear una cuadrícula de botones de usuario
        grid = QGridLayout()
        grid.setSpacing(10)

        row, col = 0, 0
        max_cols = 3

        for user in self.auth_service.users:
            btn = QPushButton(f"{user.name}\n({user.role.value})")
            btn.setProperty("user_id", user.id)
            btn.clicked.connect(lambda _, u=user: self.select_user(u))
            grid.addWidget(btn, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        layout.addLayout(grid)
        self.setLayout(layout)

    def select_user(self, user: User):
        self.user_selected.emit(user)
        self.accept()
