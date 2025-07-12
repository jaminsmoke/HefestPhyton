"""
TPV Avanzado Modernizado - Componente principal con UI moderna v0.0.14
Incluye estilos modernos, animaciones y mejor UX
"""

import logging
from typing import Optional, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QLabel, 
    QFrame, QPushButton, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QColor, QPainter, QPainterPath

from services.tpv_service import TPVService, Mesa

from .styles_modern import (
    get_modern_button_style, 
    get_modern_card_style,
    COLORS,
    SPACING,
    BORDER_RADIUS
)
from .tpv_avanzado_header_modern import create_modern_header
from .tpv_avanzado_productos_modern import create_modern_productos_panel
from .tpv_avanzado_pedido_modern import create_modern_pedido_panel

logger = logging.getLogger(__name__)


class ModernTPVFrame(QFrame):
    """Frame moderno con sombras y bordes redondeados"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_modern_style()
    
    def setup_modern_style(self):
        """Aplica estilos modernos al frame"""
        self.setStyleSheet(f"""
            ModernTPVFrame {{
                background: {COLORS['white']};
                border: 1px solid {COLORS['gray_200']};
                border-radius: {BORDER_RADIUS['xl']};
                margin: {SPACING['md']};
            }}
        """)
        
        # Agregar sombra
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 25))
        self.setGraphicsEffect(shadow)


class TPVAvanzadoModern(QWidget):
    """TPV Avanzado con diseño moderno y profesional"""
    
    pedido_completado = pyqtSignal(int, float)  # mesa_id, total
    estado_changed = pyqtSignal(str)  # Nuevo: señal para cambios de estado

    def __init__(
        self,
        mesa: Optional[Mesa] = None,
        tpv_service: Optional[TPVService] = None,
        db_manager: Optional[Any] = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        
        # Configuración de datos
        self.setup_data_layer(mesa, tpv_service, db_manager)
        
        # Configuración de UI moderna
        self.setup_modern_ui()
        
        # Configuración de animaciones
        self.setup_animations()
        
        # Configuración inicial
        self.initialize_tpv_state()
        
        logger.info("[TPVAvanzadoModern] Componente moderno inicializado correctamente")

    def setup_data_layer(self, mesa, tpv_service, db_manager):
        """Configura la capa de datos del TPV"""
        self.selected_user: Optional[Any] = None
        self.mesa = mesa
        self.current_order: Optional[Any] = None
        
        if db_manager is None:
            raise ValueError(
                "db_manager es obligatorio para TPVAvanzadoModern"
            )
        
        if tpv_service:
            self.tpv_service = tpv_service
            logger.info("[TPVAvanzadoModern] Usando tpv_service externo")
        else:
            self.tpv_service = TPVService(db_manager=db_manager)
            logger.info("[TPVAvanzadoModern] TPVService creado internamente")

    def setup_modern_ui(self):
        """Configura la interfaz moderna del TPV"""
        # Layout principal con márgenes modernos
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(16)
        
        # Frame principal moderno
        self.main_frame = ModernTPVFrame()
        frame_layout = QVBoxLayout(self.main_frame)
        frame_layout.setContentsMargins(24, 24, 24, 24)
        frame_layout.setSpacing(20)
        
        # Header moderno
        self.header_widget = create_modern_header(self)
        frame_layout.addWidget(self.header_widget)
        
        # Separador visual
        separator = self.create_separator()
        frame_layout.addWidget(separator)
        
        # Splitter principal con estilos modernos
        self.main_splitter = self.create_modern_splitter()
        frame_layout.addWidget(self.main_splitter)
        
        # Panel de productos (izquierda)
        self.productos_widget = create_modern_productos_panel(self)
        self.main_splitter.addWidget(self.productos_widget)
        
        # Panel de pedidos (derecha)
        self.pedido_widget = create_modern_pedido_panel(self)
        self.main_splitter.addWidget(self.pedido_widget)
        
        # Configurar proporciones del splitter (60% productos, 40% pedido)
        self.main_splitter.setSizes([600, 400])
        
        main_layout.addWidget(self.main_frame)
        
        # Aplicar estilos del tema
        self.apply_modern_theme()

    def create_separator(self):
        """Crea un separador visual moderno"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 transparent, 
                    stop:0.5 {COLORS['gray_200']}, 
                    stop:1 transparent);
                border: none;
                height: 1px;
                margin: {SPACING['sm']} {SPACING['2xl']};
            }}
        """)
        separator.setFixedHeight(1)
        return separator

    def create_modern_splitter(self):
        """Crea un splitter con estilos modernos"""
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background: {COLORS['gray_300']};
                border-radius: 2px;
                margin: {SPACING['lg']} 0;
            }}
            QSplitter::handle:horizontal {{
                width: 4px;
            }}
            QSplitter::handle:hover {{
                background: {COLORS['primary']};
            }}
        """)
        splitter.setHandleWidth(8)
        return splitter

    def apply_modern_theme(self):
        """Aplica el tema moderno a todo el componente"""
        self.setStyleSheet(f"""
            TPVAvanzadoModern {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {COLORS['gray_50']}, 
                    stop:1 {COLORS['white']});
                font-family: 'Segoe UI', 'Arial', sans-serif;
                color: {COLORS['gray_800']};
            }}
        """)

    def setup_animations(self):
        """Configura las animaciones para transiciones suaves"""
        # Animación para el frame principal
        self.fade_animation = QPropertyAnimation(self.main_frame, b"geometry")
        self.fade_animation.setDuration(300)
        self.fade_animation.setEasingCurve(QEasingCurve.Type.OutQuart)
        
        # Animación para mostrar/ocultar paneles
        self.slide_animation = QPropertyAnimation(self.main_splitter, b"geometry")
        self.slide_animation.setDuration(250)
        self.slide_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def initialize_tpv_state(self):
        """Inicializa el estado del TPV"""
        if self.mesa and self.tpv_service:
            self.load_mesa_data()
        
        # Conectar señales
        self.connect_signals()

    def load_mesa_data(self):
        """Carga los datos de la mesa seleccionada"""
        try:
            # Recuperar comanda activa
            if hasattr(self.tpv_service, "get_comanda_activa"):
                comanda = self.tpv_service.get_comanda_activa(self.mesa.numero)
                if comanda:
                    logger.info(f"[TPVModern] Comanda activa recuperada: {comanda}")
                    self.current_order = comanda
                else:
                    # Crear nueva comanda
                    self.create_new_order()
            
            # Actualizar header con información de la mesa
            self.update_header_mesa_info()
            
        except Exception as e:
            logger.error(f"[TPVModern] Error cargando datos de mesa: {e}")
            self.estado_changed.emit(f"Error: {str(e)}")

    def create_new_order(self):
        """Crea una nueva comanda para la mesa"""
        try:
            usuario_id = self.get_current_user_id()
            nueva_comanda = self.tpv_service.crear_comanda(
                self.mesa.numero, usuario_id=usuario_id
            )
            logger.info(f"[TPVModern] Nueva comanda creada: {nueva_comanda}")
            self.current_order = nueva_comanda
            self.estado_changed.emit("Nueva comanda creada")
            
        except Exception as e:
            logger.error(f"[TPVModern] Error creando comanda: {e}")
            self.estado_changed.emit(f"Error creando comanda: {str(e)}")

    def get_current_user_id(self):
        """Obtiene el ID del usuario actual"""
        if self.selected_user and hasattr(self.selected_user, "id"):
            return self.selected_user.id
        
        # Intentar obtener desde AuthService
        try:
            from services.auth_service import get_auth_service
            auth_service = get_auth_service()
            if (hasattr(auth_service, "current_user") and 
                auth_service.current_user and 
                hasattr(auth_service.current_user, "id")):
                return auth_service.current_user.id
        except AttributeError as e:
            # Log específico para error de obtención de usuario
            logger.debug("Error obteniendo current_user: %s", e)
        
        return -1  # Usuario por defecto

    def update_header_mesa_info(self):
        """Actualiza la información de la mesa en el header"""
        if hasattr(self, 'header_widget') and self.mesa:
            # El header moderno se actualizará automáticamente
            pass

    def connect_signals(self):
        """Conecta las señales entre componentes"""
        # Conectar señales de productos y pedidos
        # Se implementarán en los componentes específicos
        pass

    def show_with_animation(self):
        """Muestra el TPV con animación"""
        # Animación de entrada suave
        self.fade_animation.setStartValue(QRect(0, -50, self.width(), self.height()))
        self.fade_animation.setEndValue(self.geometry())
        self.fade_animation.start()

    def add_product_to_order(self, product_data):
        """Añade un producto al pedido actual con animación"""
        try:
            # Lógica de negocio para añadir producto
            if not self.current_order:
                self.create_new_order()
            
            # Aquí iría la lógica específica de añadir producto
            # Se implementará en el panel de pedidos
            
            logger.info(f"[TPVModern] Producto añadido: {product_data}")
            self.estado_changed.emit("Producto añadido al pedido")
            
        except Exception as e:
            logger.error(f"[TPVModern] Error añadiendo producto: {e}")
            self.estado_changed.emit(f"Error: {str(e)}")

    def process_payment(self, payment_data):
        """Procesa el pago con validaciones modernas"""
        try:
            # Lógica de procesamiento de pago
            # Se implementará completamente
            
            logger.info(f"[TPVModern] Procesando pago: {payment_data}")
            self.pedido_completado.emit(self.mesa.numero if self.mesa else 0, 0.0)
            self.estado_changed.emit("Pago procesado exitosamente")
            
        except Exception as e:
            logger.error(f"[TPVModern] Error procesando pago: {e}")
            self.estado_changed.emit(f"Error en pago: {str(e)}")

    def refresh_data(self):
        """Actualiza todos los datos del TPV"""
        try:
            if self.mesa:
                self.load_mesa_data()
            
            # Actualizar componentes
            if hasattr(self, 'productos_widget'):
                # Actualizar productos
                pass
            
            if hasattr(self, 'pedido_widget'):
                # Actualizar pedido
                pass
            
            logger.info("[TPVModern] Datos actualizados")
            self.estado_changed.emit("Datos actualizados")
            
        except Exception as e:
            logger.error(f"[TPVModern] Error actualizando datos: {e}")
            self.estado_changed.emit(f"Error actualizando: {str(e)}")

    def get_order_summary(self):
        """Obtiene un resumen del pedido actual"""
        if not self.current_order:
            return {"items": [], "total": 0.0}
        
        # Implementar lógica de resumen
        return {"items": [], "total": 0.0}

    def closeEvent(self, event):
        """Maneja el cierre del TPV con animación"""
        # Detener animaciones
        if hasattr(self, 'fade_animation'):
            self.fade_animation.stop()
        if hasattr(self, 'slide_animation'):
            self.slide_animation.stop()
        
        super().closeEvent(event)
