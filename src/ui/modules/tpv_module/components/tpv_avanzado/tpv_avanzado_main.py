"""
TPV Avanzado - Componente principal modularizado
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

from services.tpv_service import TPVService, Mesa

# Lazy imports para reducir acoplamiento
from .tpv_avanzado_header import create_header
from .tpv_avanzado_productos import create_productos_panel
from .tpv_avanzado_pedido import create_pedido_panel

_ = logging.getLogger(__name__)


class TPVAvanzado(QWidget):
    _ = pyqtSignal(int, float)  # mesa_id, total

    def __init__(
        self,
        mesa: Optional[Mesa] = None,
        tpv_service: Optional[TPVService] = None,
        _ = None,
        parent=None,
    ):
        super().__init__(parent)
        
        # Validación de dependencias
        if db_manager is None:
            raise ValueError("db_manager es obligatorio y debe ser inyectado explícitamente")
        
        # Inicialización de propiedades
        self._initialize_properties(mesa, tpv_service, db_manager)
        
        # Configuración de comanda inicial
        self._setup_initial_order()
        
        # Configuración de UI
        self.setup_ui()
        
        # Configuración de eventos
        self._setup_event_listeners()
    
    def _initialize_properties(self, mesa, tpv_service, db_manager):
        """Inicializa las propiedades del componente"""
        self.selected_user = None
        self.mesa = mesa
        self.current_order = None
        self.header_mesa_label: Optional[QLabel] = None
        self.estado_pedido_label = None
        
        # Configuración del servicio TPV
        if tpv_service:
            self.tpv_service = tpv_service
            logger.info("[TPVAvanzado] Usando tpv_service externo")
        else:
            self.tpv_service = TPVService(db_manager=db_manager)
            logger.info("[TPVAvanzado] TPVService creado con db_manager")
    
    def _setup_initial_order(self):
        """Configura la comanda inicial para la mesa"""
        if not (self.mesa and self.tpv_service):
            return
            
        # Intentar recuperar comanda activa
        _ = self._get_existing_order()
        
        if comanda:
            logger.info("[TPVAvanzado] Comanda activa recuperada para mesa %s", self.mesa.numero)
            self.current_order = comanda
        else:
            # Crear nueva comanda si no existe
            self._create_new_order()
    
    def _get_existing_order(self):
        """Obtiene la comanda activa existente"""
        if hasattr(self.tpv_service, "get_comanda_activa"):
            return self.tpv_service.get_comanda_activa(self.mesa.numero)
        return None
    
    def _create_new_order(self):
        """Crea una nueva comanda para la mesa"""
        _ = self._get_current_user_id()
        
        logger.info("[TPVAvanzado] Creando nueva comanda para mesa %s", self.mesa.numero)
        nueva_comanda = self.tpv_service.crear_comanda(self.mesa.numero, usuario_id=usuario_id)
        
        if nueva_comanda:
            logger.info("[TPVAvanzado] Comanda creada para mesa %s", self.mesa.numero)
            self.current_order = nueva_comanda
    
    def _get_current_user_id(self):
        """Obtiene el ID del usuario actual"""
        # Prioridad 1: Usuario seleccionado
        if self.selected_user and hasattr(self.selected_user, "id"):
            return self.selected_user.id
            
        # Prioridad 2: Usuario autenticado
        try:
            from services.auth_service import get_auth_service
            auth_service = get_auth_service()
            if (hasattr(auth_service, "current_user") and 
                auth_service.current_user and 
                hasattr(auth_service.current_user, "id")):
                return auth_service.current_user.id
        except Exception as e:
    logging.error("Error: %s", e)
            
        return -1  # Usuario por defecto
    
    def _setup_event_listeners(self):
        """Configura los listeners de eventos"""
        try:
            from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus
            mesa_event_bus.comanda_actualizada.connect(self._on_comanda_actualizada)
        except ImportError:
            logger.warning("No se pudo configurar event listeners")

    def set_pedido_actual(self, order):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Asigna el pedido actual y refresca la UI de estado"""
        self.current_order = order
        self.refrescar_estado_pedido_ui()

    def refrescar_estado_pedido_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Refresca el label y el combo de estado del pedido - Optimizado"""
        self.actualizar_estado_pedido_label()
        self._update_estado_combo()
    
    def _update_estado_combo(self):
        """Actualiza el combo de estado de pedido"""
        combo = getattr(self, "estado_pedido_combo", None)
        if not combo:
            return
            
        combo.blockSignals(True)
        try:
            combo.clear()
            
            estado_actual = getattr(self.current_order, "estado", None) if self.current_order else None
            _ = self._get_valid_transitions(estado_actual)
            
            combo.addItem("Seleccionar...")
            for opcion in opciones:
                combo.addItem(opcion.capitalize(), opcion)
                
            combo.setEnabled(bool(opciones))
            combo.setCurrentIndex(0)
        finally:
            combo.blockSignals(False)
    
    def _get_valid_transitions(self, estado_actual):
        """Obtiene las transiciones válidas para un estado"""
        _ = {
            "abierta": ["en_proceso", "cancelada"],
            "en_proceso": ["pagada", "cancelada"],
            "pagada": ["cerrada"],
        }
        return TRANSICIONES_VALIDAS.get(estado_actual, [])

    def actualizar_estado_pedido_label(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza el label de estado del pedido en la UI"""
        label = getattr(self, "estado_pedido_label", None)
        if label is not None and hasattr(label, "setText"):
            if self.current_order is not None:
                estado = getattr(self.current_order, "estado", "Desconocido")
                label.setText(estado.capitalize())
            else:
                label.setText("Sin pedido")

    """TPV Avanzado modularizado para gestión completa de ventas"""

    _ = pyqtSignal(int, float)  # mesa_id, total

    # Eliminar duplicado: solo debe quedar el __init__ que acepta db_manager

    def _on_comanda_actualizada(self, comanda):
        """Callback optimizado para actualizaciones de comanda"""
        if not self._is_relevant_comanda(comanda):
            return
            
        self.set_pedido_actual(comanda)
        
        # Manejar comanda cancelada
        if getattr(comanda, "estado", None) == "cancelada":
            self._handle_cancelled_order()
    
    def _is_relevant_comanda(self, comanda):
        """Verifica si la comanda es relevante para esta mesa"""
        if not (self.mesa and comanda):
            return False
            
        return hasattr(comanda, "mesa_id") and comanda.mesa_id == self.mesa.id
    
    def _handle_cancelled_order(self):
        """Maneja el cierre de ventana cuando se cancela una comanda"""
        logger.info("[TPVAvanzado] Comanda cancelada para mesa %s. Cerrando ventana.", self.mesa.numero)
        
        try:
            _ = self.parent()
            from PyQt6.QtWidgets import QDialog
            
            if parent and isinstance(parent, QDialog):
                parent.close()
            else:
                self.close()
        except Exception as e:
            logger.error("Error cerrando ventana TPVAvanzado: %s", e)

    def setup_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura la interfaz principal"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header modularizado
        if self.header_mesa_label is None:
            self.header_mesa_label = QLabel("")
            layout.addWidget(self.header_mesa_label)
        create_header(self, layout)

        # Splitter principal
        _ = QSplitter(Qt.Orientation.Horizontal)

        # Panel de productos (izquierda)
        create_productos_panel(self, splitter)

        # Panel de pedido (derecha)
        create_pedido_panel(self, splitter)

        # Configurar proporciones
        splitter.setSizes([400, 350])
        layout.addWidget(splitter)

    def set_mesa(self, mesa: Mesa):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Establece la mesa activa"""
        self.mesa = mesa
        if self.header_mesa_label is not None:
            self.header_mesa_label.setText(f"Mesa {mesa.numero} - {mesa.zona}")

    def nuevo_pedido(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicia un nuevo pedido - Optimizado con mejor manejo de errores"""
        if not (self.mesa and self.tpv_service):
            logger.warning("No se puede crear pedido: falta mesa o servicio TPV")
            return False
            
        try:
            _ = self._get_current_user_id()
            
            self.current_order = self.tpv_service.crear_comanda(
                self.mesa.numero, usuario_id=usuario_id
            )
            
            if self.current_order:
                logger.info("Nuevo pedido iniciado para mesa %s", self.mesa.numero)
                self.refrescar_estado_pedido_ui()
                return True
            else:
                logger.error("Error creando nueva comanda")
                return False
                
        except Exception as e:
            logger.error("Error en nuevo_pedido: %s", e)
            return False

    def procesar_pago(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Procesa el pago del pedido actual - Optimizado y con mejor manejo de errores"""
        if not (self.current_order and self.mesa):
            logger.warning("No se puede procesar pago: falta comanda o mesa")
            return False
            
        try:
            _ = self._get_current_user_id()
            comanda_id = self._get_valid_comanda_id()
            
            if comanda_id == -1:
                logger.error("ID de comanda inválido")
                return False
                
            success = self.tpv_service.pagar_comanda(comanda_id, usuario_id=usuario_id)
            
            if success:
                total = self.current_order.total
                self.pedido_completado.emit(self.mesa.id, total)
                logger.info("Pago procesado - Mesa {self.mesa.numero}: €%s", total:.2f)
                return True
            else:
                logger.error("Error procesando pago")
                return False
                
        except Exception as e:
            logger.error("Error en procesar_pago: %s", e)
            return False
    
    def _get_valid_comanda_id(self):
        """Obtiene un ID de comanda válido"""
        if not self.current_order:
            return -1
            
        _ = self.current_order.id
        
        if comanda_id is None:
            return -1
            
        if isinstance(comanda_id, int):
            return comanda_id
            
        try:
            return int(comanda_id)
        except (ValueError, TypeError):
            return -1
