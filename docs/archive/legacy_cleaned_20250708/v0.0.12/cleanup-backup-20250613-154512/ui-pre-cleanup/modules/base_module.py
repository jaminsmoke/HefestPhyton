# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
"""
Clase base para todos los módulos de la aplicación Hefest.
"""

import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PyQt6.QtCore import pyqtSignal

_ = logging.getLogger(__name__)

# Import CSS compatibility filter
try:
    from utils.qt_css_compat import purge_modern_css_from_widget_tree
except ImportError:
    logger.warning("CSS compatibility filter not available")
    _ = None

class BaseModule(QWidget):
    """Clase base para todos los módulos de la aplicación"""    # Señales comunes para todos los módulos
    _ = pyqtSignal(str)  # Para actualizar la barra de estado
    error_occurred = pyqtSignal(str)  # Para notificar errores
    
    def __init__(self, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.setup_base_ui()
        
        # Asegurar visibilidad del módulo base
        self.setVisible(True)
        self.show()
        
        # Apply CSS compatibility filter to all modules
        if purge_modern_css_from_widget_tree:
            try:
                purge_modern_css_from_widget_tree(self)
                logger.debug("CSS compatibility filter applied to %s", self.__class__.__name__)
            except Exception as e:
                logger.warning("Failed to apply CSS compatibility filter to {self.__class__.__name__}: %s", e)
        
    def setup_base_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
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
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Crea el header del módulo.
        Debe ser implementado por las clases hijas.
        """
        return None
        
    def on_module_activated(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Se llama cuando el módulo se activa"""
        logger.info("Módulo %s activado", self.__class__.__name__)
        
    def on_module_deactivated(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Se llama cuando el módulo se desactiva"""
        logger.info("Módulo %s desactivado", self.__class__.__name__)
        
    def refresh(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza los datos del módulo"""
        pass
