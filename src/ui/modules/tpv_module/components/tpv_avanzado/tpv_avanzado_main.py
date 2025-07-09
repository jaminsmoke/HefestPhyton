"""
TPV Avanzado - Componente principal modularizado
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QLabel
from PyQt6.QtCore import Qt, pyqtSignal

from services.tpv_service import TPVService, Mesa

from .tpv_avanzado_header import create_header
from .tpv_avanzado_productos import create_productos_panel
from .tpv_avanzado_pedido import create_pedido_panel

logger = logging.getLogger(__name__)


class TPVAvanzado(QWidget):
    pedido_completado = pyqtSignal(int, float)  # mesa_id, total

    def __init__(
        self,
        mesa: Optional[Mesa] = None,
        tpv_service: Optional[TPVService] = None,
        db_manager=None,
        parent=None,
    ):
        super().__init__(parent)
        # Inicialización obligatoria para evitar advertencias y asegurar robustez
        self.selected_user = None
        self.mesa = mesa
        if db_manager is None:
            raise ValueError(
                "db_manager es obligatorio y debe ser inyectado explícitamente en TPVAvanzado"
            )
        logger.info(
            f"[TPVAvanzado] db_manager recibido en constructor: {type(db_manager)} - {db_manager}"
        )
        if tpv_service:
            self.tpv_service = tpv_service
            logger.info(f"[TPVAvanzado] Usando tpv_service externo: {self.tpv_service}")
        else:
            self.tpv_service = TPVService(db_manager=db_manager)
            logger.info(
                f"[TPVAvanzado] TPVService creado con db_manager: {self.tpv_service.db_manager}"
            )
        self.current_order = None
        self.header_mesa_label: Optional[QLabel] = (
            None  # Añadido para evitar error de Pyright
        )
        self.estado_pedido_label = None  # Referencia al QLabel de estado del pedido (se asigna en create_pedido_panel)
        # --- NUEVO: Recuperar comanda activa al abrir el TPV ---
        if self.mesa and self.tpv_service:
            comanda = None
            if hasattr(self.tpv_service, "get_comanda_activa"):
                comanda = self.tpv_service.get_comanda_activa(self.mesa.numero)
            if comanda:
                logger.info(f"[TPVAvanzado] Comanda activa recuperada para mesa {self.mesa.numero}: {comanda}")
                self.current_order = comanda
            else:
                # Forzar creación y persistencia de comanda si no existe
                # Obtener usuario autenticado si existe
                usuario_id = -1
                if self.selected_user is not None and hasattr(self.selected_user, "id"):
                    usuario_id = self.selected_user.id
                else:
                    # Intentar obtener usuario autenticado desde AuthService
                    try:
                        from services.auth_service import get_auth_service
                        auth_service = get_auth_service()
                        if hasattr(auth_service, "current_user") and auth_service.current_user and hasattr(auth_service.current_user, "id"):
                            usuario_id = auth_service.current_user.id
                    except Exception:
                        pass
                # Asegurar que usuario_id sea siempre int
                if usuario_id is None:
                    usuario_id = -1
                logger.info(f"[TPVAvanzado] No existe comanda activa para mesa {self.mesa.numero}, creando nueva con usuario_id={usuario_id}...")
                nueva_comanda = self.tpv_service.crear_comanda(self.mesa.numero, usuario_id=usuario_id)
                logger.info(f"[TPVAvanzado] Comanda creada y persistida para mesa {self.mesa.numero}: {nueva_comanda}")
                self.current_order = nueva_comanda
        self.setup_ui()
        # --- Sincronización en tiempo real: escuchar cambios de comanda ---
        try:
            from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

            mesa_event_bus.comanda_actualizada.connect(self._on_comanda_actualizada)
        except Exception:
            pass

    def set_pedido_actual(self, order):
        """Asigna el pedido actual y refresca la UI de estado"""
        self.current_order = order
        self.refrescar_estado_pedido_ui()

    def refrescar_estado_pedido_ui(self):
        """Refresca el label y el combo de estado del pedido según el estado actual"""
        # Actualiza label
        self.actualizar_estado_pedido_label()
        # Actualiza combo
        combo = getattr(self, "estado_pedido_combo", None)
        if combo is not None:
            combo.blockSignals(True)
            combo.clear()
            estado_actual = None
            if self.current_order is not None:
                estado_actual = getattr(self.current_order, "estado", None)
            TRANSICIONES_VALIDAS = {
                "abierta": ["en_proceso", "cancelada"],
                "en_proceso": ["pagada", "cancelada"],
                "pagada": ["cerrada"],
            }
            opciones = []
            if estado_actual in TRANSICIONES_VALIDAS:
                opciones = TRANSICIONES_VALIDAS[estado_actual]
            combo.addItem("Seleccionar...")
            for op in opciones:
                combo.addItem(op.capitalize(), op)
            combo.setEnabled(bool(opciones))
            combo.setCurrentIndex(0)
            combo.blockSignals(False)

    def actualizar_estado_pedido_label(self):
        """Actualiza el label de estado del pedido en la UI"""
        label = getattr(self, "estado_pedido_label", None)
        if label is not None and hasattr(label, "setText"):
            if self.current_order is not None:
                estado = getattr(self.current_order, "estado", "Desconocido")
                label.setText(estado.capitalize())
            else:
                label.setText("Sin pedido")

    """TPV Avanzado modularizado para gestión completa de ventas"""

    pedido_completado = pyqtSignal(int, float)  # mesa_id, total

    # Eliminar duplicado: solo debe quedar el __init__ que acepta db_manager

    def _on_comanda_actualizada(self, comanda):
        """Callback: refresca el pedido si la comanda corresponde a la mesa actual"""
        if not self.mesa or not comanda:
            return
        if hasattr(comanda, "mesa_id") and comanda.mesa_id == self.mesa.id:
            self.set_pedido_actual(comanda)

    def setup_ui(self):
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
        if self.header_mesa_label is not None:
            self.header_mesa_label.setText(f"Mesa {mesa.numero} - {mesa.zona}")

    def nuevo_pedido(self):
        """Inicia un nuevo pedido con registro de usuario (camarero/cajero)"""
        if self.mesa and self.tpv_service:
            usuario_id = getattr(self, "selected_user", None)
            if usuario_id and hasattr(usuario_id, "id"):
                usuario_id = usuario_id.id
            else:
                usuario_id = -1  # Manejar caso sin usuario seleccionado
            self.current_order = self.tpv_service.crear_comanda(
                self.mesa.numero, usuario_id=usuario_id
            )
            logger.info(
                f"Nuevo pedido iniciado para mesa {self.mesa.numero} por usuario {usuario_id}"
            )
            self.refrescar_estado_pedido_ui()

    def procesar_pago(self):
        """Procesa el pago del pedido actual y registra el usuario que realiza el cobro"""
        if self.current_order and self.mesa:
            usuario_id = getattr(self, "selected_user", None)
            if usuario_id and hasattr(usuario_id, "id"):
                usuario_id = usuario_id.id
            else:
                usuario_id = -1  # Manejar caso sin usuario seleccionado
            comanda_id = (
                self.current_order.id if self.current_order.id is not None else -1
            )
            if not isinstance(comanda_id, int):
                try:
                    comanda_id = int(comanda_id)
                except Exception:
                    comanda_id = -1
            self.tpv_service.pagar_comanda(comanda_id, usuario_id=usuario_id)
            total = self.current_order.total
            self.pedido_completado.emit(self.mesa.id, total)
            logger.info(
                f"Pedido completado - Mesa {self.mesa.numero}: €{total:.2f} (usuario {usuario_id})"
            )
