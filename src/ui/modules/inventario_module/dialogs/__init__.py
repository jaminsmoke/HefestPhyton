"""
Diálogos del módulo de inventario
================================

Este paquete contiene todos los diálogos de entrada de datos
para el sistema de inventario de Hefest.
"""

from .product_dialogs_pro import (
    NewProductDialog,
    EditProductDialog,
    StockAdjustmentDialog,
    DeleteConfirmationDialog,
)

__all__ = [
    "NewProductDialog",
    "EditProductDialog",
    "StockAdjustmentDialog",
    "DeleteConfirmationDialog",
]
