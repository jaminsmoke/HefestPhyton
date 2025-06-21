"""
Hefest - Sistema Integral de Hostelería y Hospedería
Punto de entrada principal de la aplicación

Este módulo inicializa los componentes principales y lanza la interfaz gráfica.
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication, QDialog, QInputDialog, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar componentes necesarios
from data.db_manager import DatabaseManager
from ui.windows.main_window import MainWindow
from utils.modern_styles import ModernStyles
# Importar la utilidad de compatibilidad CSS
from utils.qt_css_compat import convert_to_qt_compatible_css, install_global_stylesheet_filter

# Importar servicios de autenticación y auditoría
from services.auth_service import AuthService
from services.audit_service import AuditService
from core.models import Role
from utils.modern_styles import modern_styles
from utils.animation_helper import AnimationHelper

class Hefest:
    """Clase principal que gestiona el ciclo de vida de la aplicación"""
    
    def __init__(self):
        """Inicializa la aplicación y sus componentes principales"""
        logger.info("Iniciando Hefest v1.0")
        
        # Inicializar la aplicación Qt
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Hefest")
        self.app.setApplicationVersion("1.0.0")
          # Configurar el estilo
        self._setup_style()
        
        # Inicializar componentes
        self.db = DatabaseManager()
        # Inicializar servicio de autenticación
        self.auth_service = AuthService()
        
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
        self.app.setStyle('Fusion')
        
        # Instalar filtro global de compatibilidad CSS
        install_global_stylesheet_filter(self.app)
        
        # Aplicar el sistema de estilos modernos
        try:
            complete_stylesheet = modern_styles.get_complete_stylesheet()
            # Convertir estilos a formato compatible con Qt
            compatible_styles = convert_to_qt_compatible_css(complete_stylesheet)
            self.app.setStyleSheet(compatible_styles)
            logger.info("Estilos modernos aplicados correctamente")
        except Exception as e:
            logger.error(f"Error al aplicar estilos modernos: {e}")

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
        from ui.windows.login_dialog import LoginDialog
        
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
        user_selector.user_selected.connect(self.authenticate_user)
        
        # Ejecutar el selector
        result = user_selector.exec()
        if result == QDialog.DialogCode.Accepted:
            # La autenticación se maneja en el método authenticate_user
            return True
        else:
            logger.info("Selección de usuario cancelada, cerrando aplicación")
            return False
            
    def authenticate_user(self, user):
        """Autentica al usuario seleccionado solicitando su PIN"""
        # Solicitar PIN
        pin, ok = QInputDialog.getText(
            None, 
            "Autenticación", 
            f"Ingrese PIN para {user.name}:",
            QLineEdit.EchoMode.Password
        )
        
        if ok and pin:
            if self.auth_service.login(user.id, pin):
                # Registro en servicio de auditoría
                AuditService.log("Inicio de sesión", user)
                logger.info(f"Inicio de sesión exitoso para {user.name}")
                self.show_main_window()
                return True
            else:
                QMessageBox.warning(None, "Error", "PIN incorrecto")                # Volver a mostrar el selector de usuario
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
