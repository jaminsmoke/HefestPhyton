"""
Hefest - Sistema Integral de Hostelería y Hospedería
Punto de entrada principal de la aplicación

Este módulo inicializa los componentes principales y lanza la interfaz gráfica.
"""

import sys
import re
import logging
from typing import Optional, Type, Any
from PyQt6.QtWidgets import QApplication, QDialog, QInputDialog, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Configuración avanzada de logging global
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
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

# === Manejo global de excepciones no capturadas ===
def global_exception_hook(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: Optional[Any]
) -> None:
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)  # type: ignore
        return
    logger.critical("Excepción no capturada", exc_info=(exc_type, exc_value, exc_traceback))  # type: ignore
    # Opcional: mostrar mensaje de error al usuario
    try:
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Error crítico", f"Se ha producido un error inesperado. Revisa el log para más detalles.\n\n{exc_value}")
    except Exception:
        pass
    # Salida explícita para evitar procesos colgados
    sys.exit(1)
sys.excepthook = global_exception_hook

# Importar componentes necesarios
from data.db_manager import DatabaseManager
from ui.windows.hefest_main_window import MainWindow

from services.auth_service import get_auth_service
from services.audit_service import AuditService


class Hefest:
    """Clase principal que gestiona el ciclo de vida de la aplicación"""

    def __init__(self):
        """Inicializa la aplicación y sus componentes principales"""
        logger.info("Iniciando Hefest v1.0")

        # Inicializar la aplicación Qt
        self.app = QApplication(sys.argv)
        # Filtro para warnings de CSS backdrop-filter (stdout y stderr)
        import io
        import sys as _sys
        from typing import List

        class CSSWarningFilter(io.StringIO):
            def __init__(self, original: Any) -> None:
                super().__init__()
                self._original = original
                self._buffer: str = ""

            def write(self, txt: str) -> None:  # type: ignore
                self._buffer += txt  # type: ignore
                while "\n" in self._buffer:  # type: ignore
                    line, self._buffer = self._buffer.split("\n", 1)  # type: ignore
                    if not re.search(r"Unknown property backdrop-filter", line):  # type: ignore
                        if self._original is not None and hasattr(self._original, "write"):  # type: ignore
                            self._original.write(line + "\n")  # type: ignore

            def flush(self) -> None:
                if self._buffer:  # type: ignore
                    if not re.search(r"Unknown property backdrop-filter", self._buffer):  # type: ignore
                        if self._original is not None and hasattr(self._original, "write"):  # type: ignore
                            self._original.write(self._buffer)  # type: ignore
                    self._buffer = ""

            def writelines(self, lines: List[str]) -> None:  # type: ignore
                for line in lines:  # type: ignore
                    self.write(line)  # type: ignore
        _sys.stderr = CSSWarningFilter(_sys.__stderr__)
        _sys.stdout = CSSWarningFilter(_sys.__stdout__)
        # Intentar filtrar también mensajes de Qt (si es posible)
        try:
            from PyQt6.QtCore import QLoggingCategory
            QLoggingCategory.setFilterRules("*.debug=false;qt.qpa.*=false")
        except Exception:
            pass
        self.app.setApplicationName("Hefest")
        self.app.setApplicationVersion("1.0.0")
        # Configurar el estilo
        self._setup_style()

        # Inicializar componentes
        self.db = DatabaseManager()
        # Inicializar servicio de autenticación
        self.auth_service = get_auth_service()
        # Logging inicial
        AuditService.log("Sistema iniciado", details={"version": "1.0.0"})

        # Ventana principal (se creará después del login)
        self.main_window = None

    def _setup_style(self):
        """Configura el estilo visual moderno de la aplicación"""
        # Configurar fuente
        font = QFont("Segoe UI", 10)
        self.app.setFont(font)

        # Configurar estilo base
        self.app.setStyle("Fusion")

        # === SISTEMA VISUAL V3 ULTRA-MODERNO ===
        # NOTA: Filtro CSS destructivo DESHABILITADO para permitir estilos modernos
        # install_global_stylesheet_filter(self.app)  # DESHABILITADO - Era destructivo
        logger.info("🎨 Sistema Visual V3: Filtros CSS destructivos deshabilitados")

        # Aplicar estilos base modernos (sin conversión destructiva)
        try:
            # Usar estilos base simples sin filtros destructivos
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
            logger.info("✅ Estilos base V3 aplicados sin filtros destructivos")
        except Exception as e:
            logger.error(f"❌ Error al aplicar estilos base: {e}")

    def show_login(self):
        """Muestra primero login básico, luego selector de usuario"""
        # Paso 1: Login básico para acceso al programa
        if not self.show_basic_login():
            logger.info("Login básico cancelado, cerrando aplicación")
            return False

        # Paso 2: Selector de usuario/rol
        return self.show_user_selector()

    def show_basic_login(self) -> bool:
        """Muestra el login básico para acceso al programa"""
        from ui.windows.authentication_dialog import LoginDialog

        login_dialog = LoginDialog()
        result = login_dialog.exec()

        if result == QDialog.DialogCode.Accepted:
            logger.info("Login básico exitoso")
            return True
        else:
            logger.info("Login básico cancelado")
            return False

    def show_user_selector(self) -> bool:
        """Muestra el selector de usuario para autenticación por roles"""
        # Importar el selector de usuario
        from ui.components.user_selector import UserSelector

        # Mostrar el selector de usuario
        user_selector = UserSelector(self.auth_service)
        user_selector.user_selected.connect(self.authenticate_user)  # type: ignore

        # Ejecutar el selector
        result = user_selector.exec()
        if result == QDialog.DialogCode.Accepted:
            # La autenticación se maneja en el método authenticate_user
            return True
        else:
            logger.info("Selección de usuario cancelada, cerrando aplicación")
            return False

    from core.hefest_data_models import User

    def authenticate_user(self, user: "User") -> bool:
        """Autentica al usuario seleccionado solicitando su PIN"""
        # Solicitar PIN
        pin, ok = QInputDialog.getText(
            None,
            "Autenticación",
            f"Ingrese PIN para {user.name}:",
            QLineEdit.EchoMode.Password,
        )

        if ok and pin:
            if user.id is not None and self.auth_service.login(user.id, pin):
                # Registro en servicio de auditoría
                AuditService.log("Inicio de sesión", user)
                logger.info(f"Inicio de sesión exitoso para {user.name}")
                self.show_main_window()
                return True
            else:
                QMessageBox.warning(
                    None, "Error", "PIN incorrecto"
                )  # Volver a mostrar el selector de usuario
                return self.show_login()

        # Si canceló el diálogo de PIN
        return self.show_login()

    def init_main_window(self):
        """Inicializa la ventana principal"""
        if not self.main_window:
            # Pasar la instancia de AuthService a MainWindow
            self.main_window = MainWindow(auth_service=self.auth_service)
            # Configuración adicional para mantener la ventana activa
            self.main_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
            self.app.setActiveWindow(self.main_window)
        return self.main_window

    def show_main_window(self):
        """Muestra la ventana principal de la aplicación"""
        main_window = self.init_main_window()
        main_window.showMaximized()
        # Asegurarse de que la ventana está activa y al frente
        main_window.raise_()

    def run(self):
        """Ejecuta la aplicación"""
        if self.show_login():
            return self.app.exec()
        else:
            return 1  # Código de error si el login fue cancelado


def main():
    """Función principal de la aplicación"""
    try:
        # Crear la instancia principal de la aplicación
        hefest_app = Hefest()
        # Ejecutar la aplicación
        return hefest_app.run()
    except Exception as e:
        logger.error(f"Error crítico en la aplicación: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
