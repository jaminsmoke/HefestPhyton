# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
"""Módulos de la aplicación Hefest"""

from .base_module import BaseModule
# from .hospederia_module import HospederiaTab  # Comentado temporalmente
from .tpv_module import TPVTab
# from .advanced_tpv_module import AdvancedTPVModule  # Comentado temporalmente
from .inventario_module import InventarioTab
# from .user_management_module import UserManagementModule  # Comentado temporalmente
from .configuracion_module import ConfiguracionModule
# from .reportes_module import ReportesModule

__all__ = ['BaseModule', 'TPVTab', 'InventarioTab', 'ConfiguracionModule']  # Módulos funcionales
