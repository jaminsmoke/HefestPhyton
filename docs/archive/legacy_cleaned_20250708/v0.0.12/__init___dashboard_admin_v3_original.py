# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
"""
Dashboard Admin v3 - Módulo completo
Versión mejorada con métricas en tiempo real y servicio de datos integrado
"""

__version__ = "3.0.0-alpha"
__author__ = "Hefest Development Team"

# Importaciones lazy para evitar problemas circulares
def get_dashboard_controller():
    """TODO: Add docstring"""
    # TODO: Add input validation
    from .ultra_modern_admin_dashboard import UltraModernAdminDashboard
    return UltraModernAdminDashboard

def get_admin_data_service():
    """TODO: Add docstring"""
    # TODO: Add input validation
    from .admin_data_service import AdminDataService
    return AdminDataService

def get_admin_metrics_widgets():
    """TODO: Add docstring"""
    # TODO: Add input validation
    from .admin_charts_widgets import DashboardChartsSection
    return DashboardChartsSection

def get_dashboard_config():
    """TODO: Add docstring"""
    # TODO: Add input validation
    from .dashboard_config import (
        DEFAULT_CONFIG, 
        ADMIN_METRICS, 
        THEME_COLORS, 
        ALERT_THRESHOLDS,
        CHART_CONFIG,
        DASHBOARD_ROUTES,
        NOTIFICATION_CONFIG,
        EXPORT_CONFIG
    )
    return {
        'DEFAULT_CONFIG': DEFAULT_CONFIG,
        'ADMIN_METRICS': ADMIN_METRICS,
        'THEME_COLORS': THEME_COLORS,
        'ALERT_THRESHOLDS': ALERT_THRESHOLDS,
        'CHART_CONFIG': CHART_CONFIG,
        'DASHBOARD_ROUTES': DASHBOARD_ROUTES,
        'NOTIFICATION_CONFIG': NOTIFICATION_CONFIG,
        'EXPORT_CONFIG': EXPORT_CONFIG
    }

# Para compatibilidad hacia atrás, mantener algunas exportaciones directas
try:
    from .dashboard_config import DEFAULT_CONFIG, ADMIN_METRICS
    
    # Alias para compatibilidad con tests antiguos
    _ = UltraModernAdminDashboard
    
    __all__ = [
        "UltraModernAdminDashboard",
        "DashboardAdminController",  # Alias para compatibilidad
        "AdminDataService", 
        "DEFAULT_CONFIG",
        "ADMIN_METRICS",
        # Funciones lazy para evitar importaciones circulares en algunos casos
        "get_dashboard_controller",
        "get_admin_data_service", 
        "get_admin_metrics_widgets",
        "get_dashboard_config"
    ]
except ImportError as e:
    # Si hay problemas de importación, usar solo lazy loading
    import logging
    logging.warning("Usando lazy loading para dashboard_admin_v3 debido a: %s", e)
    _ = [
        "get_dashboard_controller",
        "get_admin_data_service", 
        "get_admin_metrics_widgets",
        "get_dashboard_config"
    ]
