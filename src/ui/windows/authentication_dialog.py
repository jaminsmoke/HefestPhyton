"""
Módulo de inicio de sesión para la aplicación Hefest.
Incluye efectos visuales modernos y animaciones.
"""

import logging
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
)
from PyQt6.QtCore import Qt

from services.auth_service import get_auth_service

logger = logging.getLogger(__name__)


class LoginDialog(QDialog):
    """Diálogo de inicio de sesión con diseño corporativo integrado"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Hefest - Inicio de Sesión")
        self.setFixedSize(440, 520)  # Aumentamos altura para mejor espaciado
        self.setWindowFlags(
            Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint
        )  # Sin bordes de ventana
        # Estilo base del diálogo con degradado profesional
        self.setStyleSheet(
            """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2C3E50, stop:1 #3498DB);
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                background: rgba(255, 255, 255, 0.1);
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid rgba(255, 255, 255, 0.4);
                background: rgba(255, 255, 255, 0.15);
            }
            QLineEdit::placeholder {
                color: rgba(255, 255, 255, 0.5);
            }
            QCheckBox {
                color: rgba(255, 255, 255, 0.8);
                font-size: 13px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                background: rgba(255, 255, 255, 0.1);
            }
            QCheckBox::indicator:checked {
                background: #3498DB;
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton {
                background: rgba(52, 152, 219, 0.9);
                border: none;
                border-radius: 6px;
                color: white;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(41, 128, 185, 1.0);
            }
            QPushButton:pressed {
                background: rgba(41, 128, 185, 0.8);
            }        """
        )
        self.setup_ui()

    def setup_ui(self):
        # Layout principal con márgenes amplios
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 30, 50, 30)  # Reducimos márgenes superiores
        layout.setSpacing(15)  # Reducimos espaciado

        # Sección superior con logo y título
        header_layout = QVBoxLayout()
        header_layout.setSpacing(6)  # Reducimos espaciado interno

        # Logo
        logo_label = QLabel("🏨")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet(
            """
            font-size: 42px;
            margin-bottom: 5px;
            color: white;
            min-height: 50px;
            max-height: 50px;
        """
        )

        # Título
        title = QLabel("HEFEST")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            font-size: 26px;
            font-weight: bold;
            color: white;
            letter-spacing: 2px;
            margin-bottom: 5px;
            min-height: 35px;
        """
        )  # Subtítulo
        subtitle = QLabel("Sistema Integral de Hostelería")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet(
            """
            font-size: 13px;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 10px;
        """
        )

        # Información de credenciales de prueba (más compacta)
        credentials_info = QLabel("Credenciales: admin/1234 • hefest/admin • demo/demo")
        credentials_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credentials_info.setStyleSheet(
            """
            font-size: 10px;
            color: rgba(255, 255, 255, 0.5);
            background: rgba(0, 0, 0, 0.15);
            border-radius: 4px;
            padding: 6px;
            margin: 3px;
        """
        )

        header_layout.addWidget(logo_label)
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        header_layout.addWidget(credentials_info)
        layout.addLayout(header_layout)

        # Espaciador más pequeño
        layout.addSpacing(20)

        # Campo de usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setFixedHeight(45)
        layout.addWidget(self.username_input)

        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(45)
        layout.addWidget(self.password_input)

        # Mensaje de error
        self.error_label = QLabel()
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.setStyleSheet(
            """
            color: #ff7675;
            font-size: 13px;
            min-height: 20px;
        """
        )
        layout.addWidget(self.error_label)

        # Checkbox recordar
        self.remember_checkbox = QCheckBox("Recordar mis credenciales")
        layout.addWidget(self.remember_checkbox)

        # Botón de inicio de sesión
        self.login_btn = QPushButton("Iniciar Sesión")
        self.login_btn.setFixedHeight(45)
        self.login_btn.clicked.connect(self.try_login)
        layout.addWidget(self.login_btn)  # Espaciador final
        layout.addStretch(1)

        # Enter para login
        self.password_input.returnPressed.connect(self.login_btn.click)

    def try_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # Limpiar mensaje de error anterior
        self.error_label.setText("")

        if not username or not password:
            self.error_label.setText("Por favor, ingrese usuario y contraseña")
            return

        try:
            auth_service = get_auth_service()
            logger.info(f"Intentando login con usuario: '{username}'")

            # Usar el método de login básico
            if auth_service.authenticate_basic_login(username, password):
                logger.info(f"Login básico exitoso para: {username}")
                self.accept()
            else:
                logger.warning(f"Login básico fallido para: {username}")
                self.error_label.setText(
                    "Usuario o contraseña incorrectos.\nVerifique las credenciales de prueba."
                )

        except Exception as e:
            logger.error(f"Error durante el login: {e}")
            self.error_label.setText(f"Error de conexión: {str(e)}")

    # Eliminado keyPressEvent para evitar doble trigger de login
