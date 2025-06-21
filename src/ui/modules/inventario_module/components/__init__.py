"""
Componentes del Módulo de Inventario
===================================

Widgets especializados para la gestión de inventario:
- ProductsManagerWidget: Gestión completa de productos
- CategoryManagerWidget: Gestión de categorías
- SupplierManagerWidget: Gestión de proveedores
"""

from .products_manager import ProductsManagerWidget
from .category_manager import CategoryManagerWidget
from .supplier_manager import SupplierManagerWidget

__all__ = ["ProductsManagerWidget", "CategoryManagerWidget", "SupplierManagerWidget"]
