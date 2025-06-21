"""
Dashboard Admin v3 - Módulo completo
Versión mejorada con métricas en tiempo real y servicio de datos integrado
"""

__version__ = "3.0.0-alpha"
__author__ = "Hefest Development Team"

# Importaciones lazy para evitar problemas circulares
def get_dashboard_controller():
    from .dashboard_admin_controller import DashboardAdminController
    return DashboardAdminController

def get_admin_data_service():
    from .admin_data_service import AdminDataService
    return AdminDataService

def get_admin_metrics_widgets():
    from .admin_metrics_widgets import AdminMetricsSection
    # Comentado hasta que existan estos widgets
    # from .admin_charts_widgets import DashboardChartsSection, MetricCard, SimpleLineChart
    return AdminMetricsSection

def get_dashboard_config():
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
    from .dashboard_admin_controller import DashboardAdminController
    __all__ = ["DashboardAdminController"]
except ImportError:
    # Si hay problemas de importación, usar lazy loading
    __all__ = [
        "get_dashboard_controller",
        "get_admin_data_service", 
        "get_admin_metrics_widgets",
        "get_dashboard_config"
    ]
