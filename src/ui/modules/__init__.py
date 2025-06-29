"""Módulos de la aplicación Hefest"""

from .module_base_interface import BaseModule

# from .hospederia_module import HospederiaTab  # Comentado temporalmente
from .tpv_module.tpv_module import TPVModule


from .inventario_module import (
    InventarioModulePro as InventarioTab,
)  # Usar versión profesional

# from .user_management_module import UserManagementModule  # Comentado temporalmente
from .configuracion_module import ConfiguracionModule

# from .reportes_module import ReportesModule

__all__ = [
    "BaseModule",
    "TPVModule",
    "InventarioTab",
    "ConfiguracionModule",
]  # Módulos funcionales
