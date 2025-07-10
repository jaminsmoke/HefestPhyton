from typing import Optional, Dict, List, Any
"""
Módulo TPV (Terminal Punto de Venta) - Hefest
============================================

Este módulo contiene todos los componentes relacionados con el Terminal Punto de Venta,
incluyendo gestión de mesas, comandas, pagos y facturación.

Estructura:
- components/: Componentes principales del TPV
- dialogs/: Diálogos modales del TPV
- widgets/: Widgets reutilizables del TPV
"""

# Importación directa de la clase principal
from .tpv_module import TPVModule

# Importación diferida para evitar problemas de dependencias circulares
__all__ = ["TPVModule"]


def get_tpv_module():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Obtiene la clase TPVModule de forma diferida"""

    return TPVModule
