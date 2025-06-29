"""
TPV Avanzado - Componente principal modularizado
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter
from PyQt6.QtCore import Qt, pyqtSignal

from services.tpv_service import TPVService, Mesa

from .tpv_avanzado_header import create_header
from .tpv_avanzado_productos import create_productos_panel
from .tpv_avanzado_pedido import create_pedido_panel

logger = logging.getLogger(__name__)


class TPVAvanzado(QWidget):
    """TPV Avanzado modularizado para gestión completa de ventas"""
    
    pedido_completado = pyqtSignal(int, float)  # mesa_id, total
    
    def __init__(self, mesa: Optional[Mesa] = None, tpv_service: Optional[TPVService] = None, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.tpv_service = tpv_service or TPVService()
        self.current_order = None
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz principal"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header modularizado
        create_header(self, layout)
        
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel de productos (izquierda)
        create_productos_panel(self, splitter)
        
        # Panel de pedido (derecha)
        create_pedido_panel(self, splitter)
        
        # Configurar proporciones
        splitter.setSizes([400, 350])
        layout.addWidget(splitter)
        
    def set_mesa(self, mesa: Mesa):
        """Establece la mesa activa"""
        self.mesa = mesa
        if hasattr(self, 'header_mesa_label'):
            self.header_mesa_label.setText(f"Mesa {mesa.numero} - {mesa.zona}")
            
    def nuevo_pedido(self):
        """Inicia un nuevo pedido"""
        if self.mesa and self.tpv_service:
            self.current_order = self.tpv_service.crear_comanda(self.mesa.id)
            logger.info(f"Nuevo pedido iniciado para mesa {self.mesa.numero}")
            
    def procesar_pago(self):
        """Procesa el pago del pedido actual"""
        if self.current_order and self.mesa:
            total = self.current_order.total
            self.pedido_completado.emit(self.mesa.id, total)
            logger.info(f"Pedido completado - Mesa {self.mesa.numero}: €{total:.2f}")