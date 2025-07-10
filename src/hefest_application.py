#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hefest - Sistema Integral de Hostelería y Hospedería
Punto de entrada principal de la aplicación
"""

import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from PyQt6.QtWidgets import QApplication, QDialog, QInputDialog, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt, QLoggingCategory
from PyQt6.QtGui import QFont

from data.db_manager import DatabaseManager
from ui.windows.hefest_main_window import MainWindow
from core.hefest_data_models import User
from services.auth_service import get_auth_service
from services.audit_service import AuditService
from ui.windows.authentication_dialog import LoginDialog
from ui.components.user_selector import UserSelector

# Configuración de logging
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "hefest_app.log")

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

logging.basicConfig(level=logging.DEBUG, handlers=[file_handler, console_handler])
logger = logging.getLogger(__name__)

def global_exception_hook(exc_type, exc_value, exc_traceback):
    """Maneja excepciones no capturadas"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Excepción no capturada", exc_info=(exc_type, exc_value, exc_traceback))
    try:
        QMessageBox.critical(None, "Error crítico", 
                           f"Error inesperado. Revisa el log.\n\n{exc_value}")
    except Exception as e:
        logging.error("Error mostrando mensaje: %s", e)
    sys.exit(1)

sys.excepthook = global_exception_hook

class Hefest:
    """Clase principal de la aplicación"""

    def __init__(self):
        """Inicializa la aplicación"""
        logger.info("Iniciando Hefest v1.0")

        self.app = QApplication(sys.argv)
        
        try:
            QLoggingCategory.setFilterRules("*.debug=false;qt.qpa.*=false")
        except Exception as e:
            logging.error("Error configurando Qt logging: %s", e)
        
        self.app.setApplicationName("Hefest")
        self.app.setApplicationVersion("1.0.0")
        
        self._setup_style()
        
        self.db = DatabaseManager()
        self.auth_service = get_auth_service()
        AuditService.log("Sistema iniciado", details={"version": "1.0.0"})
        
        self.main_window = None

    def _setup_style(self):
        """Configura el estilo visual"""
        font = QFont("Segoe UI", 10)
        self.app.setFont(font)
        self.app.setStyle("Fusion")
        
        try:
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
            logger.info("Estilos base aplicados")
        except Exception as e:
            logger.error("Error aplicando estilos: %s", e)

    def show_login(self):
        """Muestra login básico y selector de usuario"""
        if not self.show_basic_login():
            logger.info("Login básico cancelado")
            return False
        return self.show_user_selector()

    def show_basic_login(self) -> bool:
        """Muestra login básico"""
        login_dialog = LoginDialog()
        result = login_dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            logger.info("Login básico exitoso")
            return True
        else:
            logger.info("Login básico cancelado")
            return False

    def show_user_selector(self) -> bool:
        """Muestra selector de usuario"""
        user_selector = UserSelector(self.auth_service)
        user_selector.user_selected.connect(self.authenticate_user)
        
        result = user_selector.exec()
        if result == QDialog.DialogCode.Accepted:
            return True
        else:
            logger.info("Selección de usuario cancelada")
            return False

    def authenticate_user(self, user: User) -> bool:
        """Autentica usuario con PIN"""
        pin, ok = QInputDialog.getText(
            None,
            "Autenticación",
            f"Ingrese PIN para {user.name}:",
            QLineEdit.EchoMode.Password,
        )

        if ok and pin:
            if user.id is not None and self.auth_service.login(user.id, pin):
                AuditService.log("Inicio de sesión", user)
                logger.info("Inicio de sesión exitoso para %s", user.name)
                self.show_main_window()
                return True
            else:
                QMessageBox.warning(None, "Error", "PIN incorrecto")
                return self.show_login()

        return self.show_login()

    def init_main_window(self):
        """Inicializa ventana principal"""
        if not self.main_window:
            self.main_window = MainWindow(auth_service=self.auth_service)
            self.main_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
            self.app.setActiveWindow(self.main_window)
        return self.main_window

    def show_main_window(self):
        """Muestra ventana principal"""
        main_window = self.init_main_window()
        main_window.showMaximized()
        main_window.raise_()

    def run(self):
        """Ejecuta la aplicación"""
        if self.show_login():
            return self.app.exec()
        else:
            return 1

def main():
    """Función principal"""
    try:
        hefest_app = Hefest()
        return hefest_app.run()
    except Exception as e:
        logger.error("Error crítico: %s", e)
        return 1

if __name__ == "__main__":
    sys.exit(main())