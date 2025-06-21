"""
Widgets especializados para el módulo de inventario
=================================================

Este paquete contiene widgets reutilizables y especializados
para la gestión de inventario en hostelería.
"""

from .inventory_filters import InventoryFiltersWidget
from .inventory_summary import InventorySummaryWidget
from .product_search import ProductSearchWidget

__all__ = ["InventoryFiltersWidget", "InventorySummaryWidget", "ProductSearchWidget"]
