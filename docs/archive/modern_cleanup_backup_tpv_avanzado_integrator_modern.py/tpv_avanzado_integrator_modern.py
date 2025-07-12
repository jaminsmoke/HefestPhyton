"""
TPV Avanzado - Integrador principal para componentes modernos
"""

from typing import Optional, Dict, Any
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt, pyqtSignal

from .tpv_avanzado_main_modern import TPVAvanzadoModern
from .tpv_avanzado_header_modern import ModernHeaderWidget
from .tpv_avanzado_productos_modern import ModernProductPanel
from .tpv_avanzado_pedido_modern import ModernOrderPanel
from .styles_modern import COLORS, BORDER_RADIUS, SPACING

# Importaciones del sistema existente
from ui.services.tpv_service import TPVService
from data.models.mesa import Mesa


class TPVAvanzadoModernIntegrator(QWidget):
    """
    Integrador principal que conecta todos los componentes modernos del TPV
    """
    
    # Señales principales
    mesa_changed = pyqtSignal(object)  # Mesa
    order_completed = pyqtSignal(dict)  # Datos del pedido completado
    
    def __init__(self, tpv_service: TPVService, mesa: Optional[Mesa] = None, parent=None):
        super().__init__(parent)
        
        # Servicios y datos
        self.tpv_service = tpv_service
        self.mesa = mesa
        
        # Componentes principales
        self.header_widget = None
        self.products_panel = None
        self.order_panel = None
        self.main_controller = None
        
        # Estado del pedido
        self.current_order = {}
        
        self.setup_ui()
        self.connect_signals()
        self.initialize_data()
    
    def setup_ui(self):
        """Configura la interfaz principal"""
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)
        
        # Header moderno
        self.header_widget = ModernHeaderWidget(self.mesa)
        main_layout.addWidget(self.header_widget)
        
        # Splitter principal para productos y pedido
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background: {COLORS['gray_300']};
                width: 8px;
                border-radius: 4px;
                margin: 2px;
            }}
            QSplitter::handle:hover {{
                background: {COLORS['primary_light']};
            }}
        """)
        
        # Panel de productos (izquierda)
        self.products_panel = ModernProductPanel(self.tpv_service)
        main_splitter.addWidget(self.products_panel)
        
        # Panel de pedidos (derecha)
        self.order_panel = ModernOrderPanel(self)
        main_splitter.addWidget(self.order_panel)
        
        # Proporción inicial: 60% productos, 40% pedido
        main_splitter.setSizes([600, 400])
        
        main_layout.addWidget(main_splitter, 1)
        
        # Aplicar estilos al contenedor
        self.apply_container_styles()
    
    def connect_signals(self):
        """Conecta las señales entre componentes"""
        # Productos -> Pedido
        if self.products_panel:
            self.products_panel.product_selected.connect(self.on_product_selected)
        
        # Pedido -> Sistema
        if self.order_panel:
            self.order_panel.payment_requested.connect(self.on_payment_requested)
            self.order_panel.order_updated.connect(self.on_order_updated)
        
        # Header -> Sistema
        if self.header_widget:
            self.header_widget.mesa_action_requested.connect(self.on_mesa_action)
    
    def initialize_data(self):
        """Inicializa los datos de los componentes"""
        # Actualizar header con información de la mesa
        if self.header_widget and self.mesa:
            self.header_widget.update_mesa_info(self.mesa)
        
        # Cargar productos
        if self.products_panel:
            self.products_panel.load_products()
    
    def apply_container_styles(self):
        """Aplica estilos al contenedor principal"""
        self.setStyleSheet(f"""
            TPVAvanzadoModernIntegrator {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['gray_50']}, 
                    stop:1 {COLORS['white']});
                border-radius: {BORDER_RADIUS['lg']};
            }}
        """)
    
    def on_product_selected(self, product_data: Dict[str, Any]):
        """Maneja la selección de un producto"""
        if self.order_panel:
            self.order_panel.add_product(product_data)
            
        # Actualizar contador en el header
        self.update_order_counter()
    
    def on_order_updated(self, order_data: Dict[str, Any]):
        """Maneja actualizaciones del pedido"""
        self.current_order = order_data
        
        # Actualizar header
        self.update_order_counter()
        
        # Emitir señal para otros componentes
        self.order_updated.emit(order_data)
    
    def on_payment_requested(self, payment_data: Dict[str, Any]):
        """Maneja solicitudes de pago"""
        if not self.mesa:
            print("Error: No hay mesa seleccionada")
            return
        
        try:
            # Procesar el pago a través del servicio TPV
            result = self.tpv_service.procesar_pago(
                mesa_id=self.mesa.numero,
                items=payment_data['items'],
                metodo_pago=payment_data['payment_method'],
                propina=payment_data.get('tip', 0),
                total=payment_data['total']
            )
            
            if result.get('success', False):
                # Pago exitoso
                self.on_payment_completed(payment_data)
            else:
                # Error en el pago
                self.on_payment_error(result.get('error', 'Error desconocido'))
                
        except Exception as e:
            print(f"Error procesando pago: {e}")
            self.on_payment_error(str(e))
    
    def on_payment_completed(self, payment_data: Dict[str, Any]):
        """Maneja la finalización exitosa del pago"""
        # Limpiar el pedido
        if self.order_panel:
            self.order_panel.clear_order()
        
        # Actualizar estado de la mesa
        if self.mesa and self.header_widget:
            # La mesa queda libre después del pago
            self.mesa.estado = "libre"
            self.header_widget.update_mesa_info(self.mesa)
        
        # Emitir señal de pedido completado
        self.order_completed.emit(payment_data)
        
        # Mostrar confirmación
        self.show_payment_confirmation(payment_data)
    
    def on_payment_error(self, error_message: str):
        """Maneja errores en el pago"""
        # TODO: Mostrar dialog de error
        print(f"Error en el pago: {error_message}")
    
    def on_mesa_action(self, action: str, data: Any = None):
        """Maneja acciones relacionadas con la mesa"""
        if action == "change_status":
            self.change_mesa_status(data)
        elif action == "view_history":
            self.show_mesa_history()
        elif action == "print_order":
            self.print_current_order()
    
    def update_order_counter(self):
        """Actualiza el contador de items en el header"""
        if self.header_widget and self.order_panel:
            order_data = self.order_panel.get_order_data()
            item_count = order_data.get('total_items', 0)
            total = order_data.get('subtotal', 0.0)
            
            self.header_widget.update_order_summary(item_count, total)
    
    def change_mesa_status(self, new_status: str):
        """Cambia el estado de la mesa"""
        if not self.mesa:
            return
        
        try:
            # Actualizar a través del servicio
            self.tpv_service.cambiar_estado_mesa(self.mesa.numero, new_status)
            
            # Actualizar objeto local
            self.mesa.estado = new_status
            
            # Actualizar UI
            if self.header_widget:
                self.header_widget.update_mesa_info(self.mesa)
                
        except Exception as e:
            print(f"Error cambiando estado de mesa: {e}")
    
    def show_mesa_history(self):
        """Muestra el historial de la mesa"""
        if not self.mesa:
            return
        
        # TODO: Implementar dialog de historial
        print(f"Mostrando historial de mesa {self.mesa.numero}")
    
    def print_current_order(self):
        """Imprime el pedido actual"""
        if not self.order_panel:
            return
        
        order_data = self.order_panel.get_order_data()
        if order_data.get('total_items', 0) == 0:
            print("No hay items para imprimir")
            return
        
        # TODO: Implementar impresión
        print(f"Imprimiendo pedido: {order_data}")
    
    def show_payment_confirmation(self, payment_data: Dict[str, Any]):
        """Muestra confirmación de pago"""
        # TODO: Implementar dialog de confirmación elegante
        total = payment_data.get('total', 0.0)
        method = payment_data.get('payment_method', 'desconocido')
        print(f"✅ Pago completado: €{total:.2f} ({method})")
    
    def set_mesa(self, mesa: Mesa):
        """Establece la mesa actual"""
        self.mesa = mesa
        
        # Actualizar header
        if self.header_widget:
            self.header_widget.update_mesa_info(mesa)
        
        # Limpiar pedido anterior si existe
        if self.order_panel and self.order_panel.order_items:
            # TODO: Preguntar si desea guardar el pedido anterior
            self.order_panel.clear_order()
        
        # Emitir señal
        self.mesa_changed.emit(mesa)
    
    def get_current_mesa(self) -> Optional[Mesa]:
        """Obtiene la mesa actual"""
        return self.mesa
    
    def get_current_order(self) -> Dict[str, Any]:
        """Obtiene el pedido actual"""
        if self.order_panel:
            return self.order_panel.get_order_data()
        return {}
    
    def has_pending_order(self) -> bool:
        """Verifica si hay un pedido pendiente"""
        order_data = self.get_current_order()
        return order_data.get('total_items', 0) > 0
    
    def force_clear_order(self):
        """Fuerza el limpiado del pedido (para casos especiales)"""
        if self.order_panel:
            self.order_panel.clear_order()
    
    def refresh_products(self):
        """Refresca la lista de productos"""
        if self.products_panel:
            self.products_panel.load_products()
    
    def focus_product_search(self):
        """Enfoca el campo de búsqueda de productos"""
        if self.products_panel:
            self.products_panel.focus_search()


def create_modern_tpv_integrator(tpv_service: TPVService, mesa: Optional[Mesa] = None) -> TPVAvanzadoModernIntegrator:
    """
    Función factory para crear el integrador TPV moderno
    
    Args:
        tpv_service: Servicio TPV configurado
        mesa: Mesa opcional para inicializar
        
    Returns:
        TPVAvanzadoModernIntegrator: Integrador configurado y listo
    """
    return TPVAvanzadoModernIntegrator(tpv_service, mesa)


# Función de conveniencia para migración gradual
def create_legacy_compatible_tpv(tpv_service: TPVService, mesa: Optional[Mesa] = None) -> TPVAvanzadoModernIntegrator:
    """
    Crea una instancia compatible con el sistema legacy
    
    Args:
        tpv_service: Servicio TPV configurado  
        mesa: Mesa opcional
        
    Returns:
        TPVAvanzadoModernIntegrator: Instancia compatible
    """
    integrator = create_modern_tpv_integrator(tpv_service, mesa)
    
    # Configuraciones adicionales para compatibilidad
    # TODO: Añadir adaptadores para interfaces legacy si es necesario
    
    return integrator
