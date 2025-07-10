from typing import Optional, Dict, List, Any
"""
Dashboard Admin v3 - Módulo completo reorganizado
Contiene el dashboard ultra-moderno con componentes especializados
organizados en subcarpetas por tipo.

Estructura del módulo:
- ultra_modern_admin_dashboard.py: Dashboard principal
- components/: Componentes específicos del dashboard
  - dashboard_metric_components.py: Componentes base de métricas
  - hospitality_metric_card.py: Especialización para hostelería
"""

__version__ = "3.0.0-alpha"
__author__ = "Hefest Development Team"


# Importación principal del dashboard
def get_dashboard_controller():
    """TODO: Add docstring"""
    # TODO: Add input validation
    from .ultra_modern_admin_dashboard import UltraModernAdminDashboard

    return UltraModernAdminDashboard


# Importación de componentes específicos
def get_dashboard_components():
    """TODO: Add docstring"""
    # TODO: Add input validation
    from .components import UltraModernMetricCard, HospitalityMetricCard

    return {
        "UltraModernMetricCard": UltraModernMetricCard,
        "HospitalityMetricCard": HospitalityMetricCard,
    }


# Exportación directa principal
try:

    # Alias para compatibilidad con código existente
    _ = UltraModernAdminDashboard

    __all__ = [
        "UltraModernAdminDashboard",
        "DashboardAdminController",  # Alias para compatibilidad
        "get_dashboard_controller",
        "get_dashboard_components",
        "UltraModernMetricCard",
        "HospitalityMetricCard",
    ]

except ImportError as e:
    # Si hay problemas de importación, usar solo lazy loading
    import logging

    logging.warning("Usando lazy loading para dashboard_admin_v3 debido a: %s", e)
    __all__ = ["get_dashboard_controller", "get_dashboard_components"]
