"""
Configuración del Dashboard Admin v3
Configuraciones centralizadas y reutilizables
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from core.models import Role


@dataclass
class DashboardConfig:
    """Configuración principal del dashboard"""
    
    # Título del dashboard
    title: str = "Dashboard Administrativo v3"
    
    # Versión
    version: str = "3.0.0-alpha"
    
    # Permisos requeridos
    required_permissions: Optional[List[Role]] = None
    
    # Configuración de actualización
    auto_refresh_interval: int = 30000  # 30 segundos en ms
    
    # Configuración visual
    theme: str = "modern"
    enable_animations: bool = True
    
    def __post_init__(self):
        if self.required_permissions is None:
            self.required_permissions = [Role.ADMIN]


@dataclass 
class MetricConfig:
    """Configuración para métricas del dashboard"""
    
    name: str
    display_name: str
    unit: str = ""
    format_type: str = "number"  # number, currency, percentage
    refresh_interval: int = 5000  # 5 segundos
    show_trend: bool = True


# Configuración por defecto
DEFAULT_CONFIG = DashboardConfig()

# Métricas disponibles para administradores
ADMIN_METRICS = [
    MetricConfig(
        name="ventas_hoy",
        display_name="Ventas Hoy",
        unit="€",
        format_type="currency"
    ),
    MetricConfig(
        name="ocupacion_mesas",
        display_name="Ocupación Mesas",
        unit="/15",
        format_type="number"
    ),
    MetricConfig(
        name="tickets_pendientes",
        display_name="Tickets Pendientes",
        unit="",
        format_type="number"
    ),
    MetricConfig(
        name="ingresos_mes",
        display_name="Ingresos del Mes",
        unit="€",
        format_type="currency"
    ),
    MetricConfig("users_online", "Usuarios en Línea", "usuarios", "number"),
    MetricConfig("daily_revenue", "Ingresos Diarios", "€", "currency"),
    MetricConfig("system_load", "Carga del Sistema", "%", "percentage"),
    MetricConfig("database_size", "Tamaño BD", "MB", "number"),
    MetricConfig("active_sessions", "Sesiones Activas", "sesiones", "number"),
    MetricConfig("error_rate", "Tasa de Errores", "%", "percentage"),
    MetricConfig("response_time", "Tiempo Respuesta", "ms", "number"),
    MetricConfig("storage_used", "Almacenamiento", "%", "percentage"),
]

# Configuración visual avanzada optimizada para V3 Enhanced
THEME_COLORS = {
    "primary": "#3b82f6",
    "secondary": "#64748b",
    "success": "#10b981", 
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "info": "#06b6d4",
    "light": "#f8fafc",
    "dark": "#1e293b",
    "background": "#ffffff",
    "surface": "#ffffff",
    "border": "#e2e8f0",
    "text_primary": "#1e293b",
    "text_secondary": "#64748b"
}

# Configuración específica para métricas V3 Enhanced
METRICS_CONFIG = {
    "card_min_size": (240, 160),  # Tamaño mínimo de tarjetas
    "card_spacing": 8,           # Espaciado entre tarjetas (reducido)
    "grid_columns": 3,            # Columnas en el grid (3 para 3x2)
    "icon_size": 40,              # Tamaño de iconos circulares
    "value_font_size": 28,        # Tamaño de fuente para valores
    "title_font_size": 15,        # Tamaño de fuente para títulos
    "subtitle_font_size": 13,     # Tamaño de fuente para subtítulos
    "border_radius": 14,          # Radio de bordes
    "hover_shadow": "0 8px 20px -4px rgba(0, 0, 0, 0.1)"
}

# Configuración del contenedor principal
CONTAINER_CONFIG = {
    "metrics_container": {
        "padding": 24,
        "border_radius": 16,
        "spacing": 20,
        "size_policy": "expanding_fixed"  # Expanding width, Fixed height
    },
    "charts_container": {
        "padding": 20,
        "border_radius": 12,
        "min_height": 300,
        "size_policy": "expanding_expanding"
    },
    "alerts_container": {
        "padding": 20,
        "border_radius": 12,
        "min_width": 300,
        "size_policy": "fixed_expanding"
    }
}

# Configuraciones de alertas
ALERT_THRESHOLDS = {
    "system_load": {"warning": 70, "danger": 85},
    "error_rate": {"warning": 2.0, "danger": 5.0},
    "response_time": {"warning": 300, "danger": 500},
    "storage_used": {"warning": 80, "danger": 90}
}

# Configuración de gráficos
CHART_CONFIG = {
    "default_height": 200,
    "default_width": 400,
    "animation_duration": 500,
    "grid_enabled": True,
    "legend_position": "bottom"
}

# Rutas del dashboard
DASHBOARD_ROUTES = {
    "overview": "/admin/dashboard",
    "metrics": "/admin/dashboard/metrics", 
    "users": "/admin/dashboard/users",
    "system": "/admin/dashboard/system",
    "reports": "/admin/dashboard/reports"
}

# Configuración de notificaciones
NOTIFICATION_CONFIG = {
    "show_desktop_notifications": True,
    "auto_dismiss_after": 5000,  # 5 segundos
    "max_notifications": 3,
    "position": "top-right"
}

# Configuración de exportación
EXPORT_CONFIG = {
    "formats": ["PDF", "Excel", "CSV"],
    "default_format": "PDF",
    "include_charts": True,
    "date_format": "%Y-%m-%d %H:%M:%S"
}
