"""
Clase base para todos los módulos de la aplicación Hefest.
"""

import logging
from abc import ABCMeta, abstractmethod
from typing import Optional, Dict, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame
from PyQt6.QtCore import pyqtSignal

_ = logging.getLogger(__name__)

# Import CSS compatibility filter
try:
    from utils.qt_css_compat import purge_modern_css_from_widget_tree
except ImportError:
    logger.warning("CSS compatibility filter not available")
    _ = None


# Metaclase personalizada para resolver conflicto entre QWidget y ABC
class QWidgetABCMeta(type(QWidget), ABCMeta):
    def __new__(mcs, name, bases, namespace, **kwargs):
        """TODO: Add docstring"""
        return super().__new__(mcs, name, bases, namespace)


class BaseModule(QWidget, metaclass=QWidgetABCMeta):
    """Clase base abstracta para todos los módulos de la aplicación"""
    
    # Señales comunes para todos los módulos
    _ = pyqtSignal(str)  # Para actualizar la barra de estado
    error_occurred = pyqtSignal(str)  # Para notificar errores
    _ = pyqtSignal(dict)  # Para notificar cambios de datos

    def __init__(self, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        
        # Dependency injection container
        self._dependencies: Dict[str, Any] = {}
        
        # Module state
        self._is_initialized = False
        self._is_active = False
        
        self.setup_base_ui()
        self._apply_css_compatibility()
        
        # Mark as initialized
        self._is_initialized = True

    def _apply_css_compatibility(self):
        """Apply CSS compatibility filter"""
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
    
    def inject_dependency(self, name: str, dependency: Any):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inject a dependency into the module"""
        self._dependencies[name] = dependency
        
    def get_dependency(self, name: str) -> Optional[Any]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Get an injected dependency"""
        return self._dependencies.get(name)
    
    @property
    def is_initialized(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        return self._is_initialized
        
    @property
    def is_active(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        return self._is_active

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

    def create_module_header(self) -> Optional[QWidget]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Crea el header del módulo.
        Puede ser implementado por las clases hijas.
        """
        return None

    def on_module_activated(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Se llama cuando el módulo se activa"""
        self._is_active = True
        logger.info("Módulo %s activado", self.__class__.__name__)
        self.status_changed.emit(f"{self.__class__.__name__} activado")

    def on_module_deactivated(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Se llama cuando el módulo se desactiva"""
        self._is_active = False
        logger.info("Módulo %s desactivado", self.__class__.__name__)
        self.status_changed.emit(f"{self.__class__.__name__} desactivado")

    @abstractmethod
    def refresh(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza los datos del módulo - debe ser implementado por subclases"""
        pass
        
    def validate_dependencies(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valida que todas las dependencias requeridas estén disponibles"""
        required_deps = self.get_required_dependencies()
        for dep_name in required_deps:
            if dep_name not in self._dependencies:
                logger.error("Dependencia requerida '{dep_name}' no encontrada en %s", self.__class__.__name__)
                return False
        return True
        
    def get_required_dependencies(self) -> list:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna lista de dependencias requeridas - puede ser sobrescrito por subclases"""
        return []
