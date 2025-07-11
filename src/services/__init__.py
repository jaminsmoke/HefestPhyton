"""
Módulo de Servicios de Negocio - Proyecto Hefest
===============================================

Este módulo contiene todos los servicios de negocio de la aplicación Hefest,
incluyendo servicios para hospedería, TPV e inventario.

Servicios disponibles:
- HospederiaService: Gestión de hospedería y reservas
- TPVService: Gestión del punto de venta
- InventarioService: Gestión del inventario y productos

Autor: Proyecto Hefest
Versión: 0.0.12
"""

# Archivo para hacer que el directorio sea un paquete Python
# Servicios de negocio para la aplicación Hefest

from .hospederia_service import HospederiaService
from .tpv_service import TPVService
from .inventario_service_real import InventarioService

__all__ = ["HospederiaService", "TPVService", "InventarioService"]
