"""
Módulo de Inventario para Hefest - Sistema de Gestión Hotelera
============================================================

Este módulo proporciona funcionalidades completas de inventario específicas
para el sector hotelero y de hostelería.

Características principales:
- Gestión de productos con categorías específicas de hostelería
- Control de stock en tiempo real con alertas inteligentes
- Gestión de proveedores y pedidos automáticos
- Análisis de consumo y estadísticas de rotación
- Integración con TPV y sistema de reservas
- Generación de informes de inventario y costos

Versión: v0.0.12
Autor: Hefest Development Team
"""

from .inventario_module import InventarioModule

# Usar la versión del módulo de inventario
InventarioTab = InventarioModule
InventarioModulePro = InventarioModule  # Mantener compatibilidad

__version__ = "0.0.12"
__all__ = ["InventarioModule", "InventarioTab", "InventarioModulePro"]

# Metadatos del módulo
MODULE_INFO = {
    "name": "Inventario",
    "description": "Sistema de gestión de inventario con pestañas especializadas",
    "version": __version__,
    "category": "Gestión",
    "icon": "📦",
    "requires": ["inventario_service_real", "module_base_interface"],
    "features": [
        "Gestión de productos con pestañas",
        "Gestión especializada de categorías",
        "Gestión completa de proveedores",
        "Interfaces intuitivas",
        "Control de stock avanzado",
        "Alertas automáticas",
        "Estadísticas en tiempo real",
    ],
}
