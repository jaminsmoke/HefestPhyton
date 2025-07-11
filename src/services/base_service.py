"""
Base Service - Clase base común para todos los servicios de Hefest

Propósito: Eliminar duplicación de código y estandarizar patrones comunes
Ubicación: src/services/base_service.py
"""

import logging
from typing import Optional, Dict, Any, TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from data.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class BaseService(ABC):
    """
    Clase base abstracta para todos los servicios de Hefest.

    Proporciona funcionalidades comunes:
    - Gestión de db_manager
    - Logging estandarizado
    - Manejo de errores base
    - Patrones de inicialización
    """

    def __init__(self, db_manager: Optional["DatabaseManager"] = None) -> None:
        """
        Inicialización base para todos los servicios.

        Args:
            db_manager: Instancia del gestor de base de datos
        """
        self.db_manager = db_manager
        self.logger = logging.getLogger(self.__class__.__name__)

        # Log de inicialización
        if self.db_manager:
            self.logger.debug(
                f"{self.__class__.__name__} inicializado con base de datos"
            )
        # Eliminado warning obsoleto: todos los servicios relevantes usan ya la base de datos de Hefest

    @property
    def has_database(self) -> bool:
        """Retorna True si el servicio tiene conexión a base de datos"""
        return self.db_manager is not None

    def require_database(self, operation_name: str = "operación") -> bool:
        """
        Valida que existe conexión a base de datos para una operación.

        Args:
            operation_name: Nombre de la operación para logging

        Returns:
            bool: True si hay conexión, False caso contrario
        """
        if not self.has_database:
            self.logger.error(
                f"No se puede realizar {operation_name} sin conexión a base de datos"
            )
            return False
        return True

    def handle_db_error(
        self, error: Exception, operation: str, default_return: Any = None
    ) -> Any:
        """
        Manejo estandarizado de errores de base de datos.

        Args:
            error: Excepción capturada
            operation: Descripción de la operación que falló
            default_return: Valor por defecto a retornar

        Returns:
            El valor por defecto especificado
        """
        self.logger.error(f"Error en {operation}: {error}")
        return default_return

    def log_operation(
        self, operation: str, details: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log estandarizado de operaciones del servicio.

        Args:
            operation: Descripción de la operación
            details: Detalles adicionales para el log
        """
        if details:
            self.logger.info(f"{operation}: {details}")
        else:
            self.logger.info(operation)

    @abstractmethod
    def get_service_name(self) -> str:
        """Retorna el nombre del servicio para logging y debugging"""

    def get_service_status(self) -> Dict[str, Any]:
        """
        Retorna el estado actual del servicio.

        Returns:
            Dict con información de estado del servicio
        """
        return {
            "service_name": self.get_service_name(),
            "has_database": self.has_database,
            "initialized": True,
            "class": self.__class__.__name__,
        }
