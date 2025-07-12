"""
Hefest - Sistema Integral de Hostelería y Hospedería
Punto de entrada principal de la aplicación

Este módulo inicializa los componentes principales y lanza la interfaz gráfica.
"""

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from typing import Any, Optional, Type

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QDialog,
    QInputDialog,
    QLineEdit,
    QMessageBox,
)

# Configurar el path para acceder a los módulos de la aplicación
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Asegurar que tanto src/ como el directorio raíz estén en el path
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Imports relativos para facilitar la portabilidad
from data.db_manager import DatabaseManager
from services.audit_service import AuditService
from services.auth_service import get_auth_service
from ui.components.user_selector import UserSelector
from ui.windows.authentication_dialog import LoginDialog
from ui.windows.hefest_main_window import MainWindow

LOG_DIR = os.path.join(parent_dir, "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "hefest_app.log")

# Formato detallado para consola y archivo
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# Handler de archivo rotativo (5MB, 3 backups)
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Handler de consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))


# Configuración global
logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
logger = logging.getLogger(__name__)

# Asegurar propagación y nivel DEBUG para todos los loggers
logging.captureWarnings(True)


def global_exception_hook(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: Optional[Any],
) -> None:
    """Maneja excepciones no capturadas globalmente."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical(
        "Excepción no capturada: %s",
        exc_value,
        exc_info=(exc_type, exc_value, exc_traceback),
    )

    try:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText("Error Crítico")
        msg.setInformativeText(
            "Se ha producido un error inesperado. "
            "La aplicación se cerrará. Revisa los logs para más detalles."
        )
        msg.setDetailedText(str(exc_value))
        msg.exec()
    except Exception as e:
        logger.error("Error al mostrar el diálogo crítico: %s", e)

    sys.exit(1)


sys.excepthook = global_exception_hook


class Hefest:
    """Clase principal que gestiona el ciclo de vida de la aplicación"""

    def __init__(self) -> None:
        """Inicializa la aplicación y sus componentes principales."""
        logger.info("Iniciando Hefest v1.0")

        self.app: QApplication = QApplication(sys.argv)
        # Filtro de logs de Qt para ignorar avisos irrelevantes (alternativa a QLoggingCategory)
        try:
            from PyQt6.QtCore import QMessageLogContext, QtMsgType, qInstallMessageHandler

            def qt_message_handler(_msg_type, _context, message):
                # Ignora avisos irrelevantes de estilos no soportados
                if message and (
                    "box-shadow" in message
                    or "transform" in message
                    or "Unknown property overflow" in message
                    or "Unknown property text-overflow" in message
                ):
                    return
                print(message)

            qInstallMessageHandler(qt_message_handler)
        except ImportError:
            pass  # Si no está PyQt6, no se instala el filtro

        self.app.setApplicationName("Hefest")
        self.app.setApplicationVersion("1.0.0")

        # Configurar el estilo
        self._setup_style()

        # Inicializar componentes
        self.db: DatabaseManager = DatabaseManager()
        self.auth_service = get_auth_service()

        AuditService.log("Sistema iniciado", details={"version": "1.0.0"})

        self.main_window: Optional[MainWindow] = None

    def _setup_style(self) -> None:
        """Configura el estilo visual moderno de la aplicación."""
        font = QFont("Segoe UI", 10)
        self.app.setFont(font)

        # Configurar estilo base
        self.app.setStyle("Fusion")

        # Aplicar estilos base modernos
        base_styles = """
            QMainWindow {
                background-color: #fafafa;
                color: #1f2937;
            }
            QWidget {
                font-family: 'Segoe UI';
            }
        """
        self.app.setStyleSheet(base_styles)
        logger.info("Estilos base aplicados correctamente")

    def show_login(self) -> bool:
        """Muestra el diálogo de login y el selector de usuario."""
        if not self._show_basic_login():
            logger.info("Login básico cancelado, cerrando aplicación.")
            return False
        return self._show_user_selector()

    def _show_basic_login(self) -> bool:
        """Muestra el login básico para acceso al programa."""
        login_dialog = LoginDialog()
        if login_dialog.exec() == QDialog.DialogCode.Accepted:
            logger.info("Login básico exitoso.")
            return True
        logger.info("Login básico cancelado.")
        return False

    def _show_user_selector(self) -> bool:
        """Muestra el selector de usuario para autenticación por roles."""
        user_selector = UserSelector(self.auth_service)
        user_selector.user_selected.connect(self.authenticate_user)
        if user_selector.exec() == QDialog.DialogCode.Accepted:
            return True
        logger.info("Selección de usuario cancelada, cerrando aplicación.")
        return False

    def authenticate_user(self, user: Any) -> None:
        """Autentica al usuario seleccionado solicitando su PIN."""
        # Solicitar PIN
        pin, ok = QInputDialog.getText(
            None,
            "Autenticación",
            f"Ingrese PIN para {user.name}",
            QLineEdit.EchoMode.Password,
        )

        if ok and pin:
            if self.auth_service.login(user.id, pin):
                AuditService.log("Inicio de sesión", user)
                logger.info("Inicio de sesión exitoso para %s", user.name)
                self.show_main_window()
            else:
                QMessageBox.warning(None, "Error", "PIN incorrecto")
                self.show_login()
        else:
            self.show_login()

    def init_main_window(self) -> MainWindow:
        """Inicializa la ventana principal."""
        if not self.main_window:
            self.main_window = MainWindow(auth_service=self.auth_service)
            self.main_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        return self.main_window

    def show_main_window(self) -> None:
        """Muestra la ventana principal de la aplicación."""
        main_window = self.init_main_window()
        main_window.showMaximized()
        main_window.raise_()
        main_window.activateWindow()

    def run(self) -> int:
        """Ejecuta el ciclo de vida de la aplicación."""
        if self.show_login():
            return self.app.exec()
        return 1


def main() -> int:
    """Punto de entrada principal de la aplicación."""
    try:
        hefest_app = Hefest()
        return hefest_app.run()
    except Exception as e:
        logger.critical("Error fatal en la aplicación: %s", e, exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
