#!/usr/bin/env python3
"""
HEFEST - REFACTORIZADOR TPV INTELIGENTE
=======================================
VERSIÓN: v0.0.14

Refactorización específica para el módulo TPV que tiene los mayores duplicados.
"""

import os
import re
import logging
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class TPVRefactorer:
    """Refactorizador específico para el módulo TPV"""
    
    def __init__(self):
        self.tpv_dir = Path("src/ui/modules/tpv_module")
        self.utils_dir = Path("src/utils")
        
    def create_tpv_utils(self):
        """Crea archivo de utilidades común para TPV"""
        
        # Crear directorio utils si no existe
        self.utils_dir.mkdir(exist_ok=True)
        
        # Utilidades TPV comunes
        tpv_utils_content = '''"""
HEFEST - UTILIDADES TPV COMUNES
===============================
Funciones comunes extraídas del módulo TPV para eliminar duplicación
"""

import logging
from typing import Any, Optional, Dict, List
from PyQt6.QtWidgets import QWidget, QLabel, QTableWidget, QMessageBox
from PyQt6.QtCore import QObject

logger = logging.getLogger(__name__)


def actualizar_labels_totales(parent: QWidget, subtotal: float, iva: float, total: float) -> None:
    """
    Actualiza los labels de totales de manera consistente
    
    Args:
        parent: Widget padre que contiene los labels
        subtotal: Valor del subtotal
        iva: Valor del IVA
        total: Valor total
    """
    try:
        # Buscar y actualizar label de subtotal
        subtotal_label = getattr(parent, 'subtotal_label', None)
        if subtotal_label and hasattr(subtotal_label, 'setText'):
            subtotal_label.setText(f"Subtotal: €{subtotal:.2f}")
        
        # Buscar y actualizar label de IVA
        iva_label = getattr(parent, 'iva_label', None)
        if iva_label and hasattr(iva_label, 'setText'):
            iva_label.setText(f"IVA (21%): €{iva:.2f}")
        
        # Buscar y actualizar label de total
        total_label = getattr(parent, 'total_label', None)
        if total_label and hasattr(total_label, 'setText'):
            total_label.setText(f"Total: €{total:.2f}")
            
    except Exception as e:
        logger.error(f"Error actualizando labels de totales: {e}")


def eliminar_producto_de_pedido(parent: Any, producto_nombre: str) -> None:
    """
    Elimina un producto individual del pedido y lo persiste en backend
    
    Args:
        parent: Widget padre que contiene la tabla de pedido
        producto_nombre: Nombre del producto a eliminar
    """
    try:
        table = getattr(parent, "pedido_table", None)
        if not table or not hasattr(table, 'rowCount'):
            logger.warning("No se encontró tabla de pedido válida")
            return
            
        # Buscar y eliminar el producto
        for row in range(table.rowCount()):
            item = table.item(row, 0)  # Columna de nombre del producto
            if item and item.text() == producto_nombre:
                table.removeRow(row)
                logger.info(f"Producto eliminado del pedido: {producto_nombre}")
                
                # Actualizar totales si existe el método
                if hasattr(parent, 'calcular_totales'):
                    parent.calcular_totales()
                break
                
    except Exception as e:
        logger.error(f"Error eliminando producto del pedido: {e}")


def mostrar_dialogo_confirmacion(parent: QWidget, titulo: str, mensaje: str) -> bool:
    """
    Muestra un diálogo de confirmación estándar
    
    Args:
        parent: Widget padre
        titulo: Título del diálogo
        mensaje: Mensaje a mostrar
        
    Returns:
        True si el usuario confirmó, False en caso contrario
    """
    try:
        reply = QMessageBox.question(
            parent,
            titulo,
            mensaje,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
        
    except Exception as e:
        logger.error(f"Error mostrando diálogo de confirmación: {e}")
        return False


def configurar_tabla_productos(tabla: QTableWidget, headers: List[str]) -> None:
    """
    Configura una tabla de productos con headers estándar
    
    Args:
        tabla: Widget de tabla a configurar
        headers: Lista de headers para las columnas
    """
    try:
        tabla.setColumnCount(len(headers))
        tabla.setHorizontalHeaderLabels(headers)
        
        # Configuración estándar de tabla
        tabla.setAlternatingRowColors(True)
        tabla.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        tabla.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #f1f3f4;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
    except Exception as e:
        logger.error(f"Error configurando tabla de productos: {e}")


def calcular_iva(subtotal: float, porcentaje: float = 21.0) -> float:
    """
    Calcula el IVA de un subtotal
    
    Args:
        subtotal: Subtotal sin IVA
        porcentaje: Porcentaje de IVA (por defecto 21%)
        
    Returns:
        Valor del IVA calculado
    """
    return subtotal * (porcentaje / 100.0)


def formatear_precio(precio: float) -> str:
    """
    Formatea un precio de manera consistente
    
    Args:
        precio: Precio a formatear
        
    Returns:
        Precio formateado como string
    """
    return f"€{precio:.2f}"


def validar_cantidad(cantidad_str: str) -> tuple[bool, float]:
    """
    Valida y convierte una cantidad de string a float
    
    Args:
        cantidad_str: Cantidad como string
        
    Returns:
        Tupla (es_valida, cantidad_numerica)
    """
    try:
        cantidad = float(cantidad_str.replace(',', '.'))
        if cantidad <= 0:
            return False, 0.0
        return True, cantidad
    except (ValueError, TypeError):
        return False, 0.0


def setup_logger_tpv() -> logging.Logger:
    """
    Configura logger específico para TPV
    
    Returns:
        Logger configurado
    """
    tpv_logger = logging.getLogger('hefest.tpv')
    if not tpv_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - TPV - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        tpv_logger.addHandler(handler)
        tpv_logger.setLevel(logging.INFO)
    
    return tpv_logger
'''
        
        # Crear archivo de utilidades TPV
        tpv_utils_file = self.utils_dir / "tpv_utils.py"
        with open(tpv_utils_file, 'w', encoding='utf-8') as f:
            f.write(tpv_utils_content)
        
        logger.info(f"✅ Archivo de utilidades TPV creado: {tpv_utils_file}")
        return tpv_utils_file

def main():
    """Función principal de refactorización TPV"""
    print("🔧 HEFEST - REFACTORIZADOR TPV")
    print("=" * 40)
    
    refactorer = TPVRefactorer()
    
    # Crear utilidades TPV
    utils_file = refactorer.create_tpv_utils()
    
    print(f"✅ Utilidades TPV creadas en: {utils_file}")
    print("\n📋 SIGUIENTE PASO:")
    print("   1. Revisar el archivo de utilidades generado")
    print("   2. Actualizar imports en archivos TPV duplicados")
    print("   3. Reemplazar código duplicado con llamadas a utilidades")
    print("   4. Ejecutar tests para validar cambios")

if __name__ == "__main__":
    main()
