"""
Clase base para todos los módulos de la aplicación Hefest.
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PyQt6.QtCore import pyqtSignal

logger = logging.getLogger(__name__)

# Import CSS compatibility filter
try:
    from utils.qt_css_compat import purge_modern_css_from_widget_tree
except ImportError:
    logger.warning("CSS compatibility filter not available")
    purge_modern_css_from_widget_tree = None


class BaseModule(QWidget):
    """Clase base para todos los módulos de la aplicación"""

    # Señales comunes para todos los módulos
    status_changed = pyqtSignal(str)  # Para actualizar la barra de estado
    error_occurred = pyqtSignal(str)  # Para notificar errores

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_base_ui()

        # Asegurar visibilidad del módulo base
        self.setVisible(True)
        self.show()

        # Apply CSS compatibility filter to all modules
        if purge_modern_css_from_widget_tree:
            try:
                purge_modern_css_from_widget_tree(self)
                logger.debug(
                    f"CSS compatibility filter applied to {self.__class__.__name__}"
                )
            except Exception as e:
                logger.warning(
                    f"Failed to apply CSS compatibility filter to {self.__class__.__name__}: {e}"
                )

    def setup_base_ui(self):
        """Configura la interfaz base común para todos los módulos"""
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Header del módulo
        self.header = self.create_module_header()
        if self.header:
            self.main_layout.addWidget(self.header)

        # Contenedor principal
        self.content = QFrame()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.addWidget(self.content)

    def create_module_header(self):
        """
        Crea el header del módulo.
        Debe ser implementado por las clases hijas.
        """
        return None

    def on_module_activated(self):
        """Se llama cuando el módulo se activa"""
        logger.info(f"Módulo {self.__class__.__name__} activado")

    def on_module_deactivated(self):
        """Se llama cuando el módulo se desactiva"""
        logger.info(f"Módulo {self.__class__.__name__} desactivado")

    def refresh(self):
        """Actualiza los datos del módulo"""
