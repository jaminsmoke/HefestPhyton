"""
MesaDialog con Pestañas - Versión mejorada usando TabbedDialog
Diálogo moderno y organizado para gestión completa de mesas
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
    QFrame, QGridLayout, QMessageBox, QLineEdit, QSpinBox, QTextEdit,
    QListWidget, QListWidgetItem
)
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from services.tpv_service import Mesa
from .reserva_dialog import ReservaDialog
from ..mesa_event_bus import mesa_event_bus
from ....components.TabbedDialog import TabbedDialog
from src.ui.modules.tpv_module.event_bus import reserva_event_bus

logger = logging.getLogger(__name__)


class MesaDialog(TabbedDialog):
    """Diálogo de mesa con pestañas horizontales modernas"""

    mesa_updated = pyqtSignal(Mesa)
    iniciar_tpv_requested = pyqtSignal(int)
    crear_reserva_requested = pyqtSignal(int)
    cambiar_estado_requested = pyqtSignal(int, str)
    reserva_cancelada = pyqtSignal()
    reserva_creada = pyqtSignal()

    def __init__(self, mesa: Mesa, parent=None, reserva_service=None):
        self.mesa = mesa
        self.reserva_service = reserva_service
        # Inicializar diálogo base
        super().__init__(f"Mesa {mesa.numero}", parent)
        # Mejor visualización: tamaño mínimo recomendado
        self.setMinimumSize(600, 520)
        self.setMaximumWidth(800)
        # Configurar header específico
        self.set_header_title(
            f"Mesa {mesa.numero} - {mesa.zona}",
            f"Capacidad: {mesa.capacidad} personas • Estado: {mesa.estado.title()}"
        )
        # Crear pestañas
        self.setup_tabs()
        # Conectar señales
        self.connect_signals()

    def setup_tabs(self):
        """Configura las pestañas del diálogo"""
        # Pestaña 1: Información
        info_page = self.create_info_page()
        self.add_tab(info_page, "Información", "📋")

        # Pestaña 2: Acciones
        actions_page = self.create_actions_page()
        self.add_tab(actions_page, "Acciones", "⚡")

        # Pestaña 3: Configuración
        config_page = self.create_config_page()
        self.add_tab(config_page, "Configuración", "⚙️")

        # Pestaña 4: Historial
        history_page = self.create_history_page()
        self.add_tab(history_page, "Historial", "📊")

    def create_info_page(self) -> QWidget:
        """Crea la página de información"""
        # Usar solo la importación global de QVBoxLayout y QScrollArea
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        # Panel de estado actual
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        info_layout = QGridLayout(info_frame)
        info_layout.setSpacing(15)
        # Estado
        estado_color = {
            'libre': '#28a745', 'ocupada': '#dc3545',
            'reservada': '#ffc107', 'mantenimiento': '#6c757d'
        }.get(self.mesa.estado, '#6c757d')
        info_layout.addWidget(QLabel("Estado:"), 0, 0)
        self.estado_value = QLabel(self.mesa.estado.title())
        self.estado_value.setStyleSheet(f"color: {estado_color}; font-weight: bold;")
        self.estado_value.setMinimumWidth(80)
        self.estado_value.setWordWrap(True)
        info_layout.addWidget(self.estado_value, 0, 1)
        # Personas
        info_layout.addWidget(QLabel("Ocupación:"), 1, 0)
        self.personas_value = QLabel(f"{self.mesa.personas_display}/{self.mesa.capacidad}")
        self.personas_value.setMinimumWidth(80)
        self.personas_value.setWordWrap(True)
        info_layout.addWidget(self.personas_value, 1, 1)
        # Nombre/Alias
        info_layout.addWidget(QLabel("Nombre:"), 2, 0)
        self.alias_value = QLabel(self.mesa.nombre_display)
        self.alias_value.setMinimumWidth(120)
        self.alias_value.setWordWrap(True)
        self.alias_value.setStyleSheet("font-weight: 500; font-size: 14px;")
        info_layout.addWidget(self.alias_value, 2, 1)
        layout.addWidget(info_frame)
        # Lista de reservas activas
        if self.reserva_service:
            reservas_frame = QFrame()
            reservas_frame.setStyleSheet("""
                QFrame {
                    background: #fff3cd;
                    border: 1px solid #ffeaa7;
                    border-radius: 8px;
                    padding: 15px;
                }
            """)
            reservas_layout = QVBoxLayout(reservas_frame)
            reservas_label = QLabel("Reservas Activas:")
            reservas_label.setWordWrap(True)
            reservas_layout.addWidget(reservas_label)
            self.reservas_list = QListWidget()
            self.reservas_list.setMaximumHeight(120)
            self.cargar_reservas_en_lista()
            reservas_layout.addWidget(self.reservas_list)
            layout.addWidget(reservas_frame)
        layout.addStretch()
        # Envolver en scroll si el contenido crece
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(page)
        return scroll

    def create_actions_page(self) -> QWidget:
        """Crea la página de acciones (botones en columna para mejor visualización)"""
        # QVBoxLayout y QScrollArea ya están importados globalmente
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(24)
        # Título
        title = QLabel("Acciones Disponibles")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setWordWrap(True)
        layout.addWidget(title)
        # Botones en columna (vertical)
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(18)
        self.tpv_btn = self.create_action_button("🍽️ Iniciar TPV", "#28a745", "Abrir punto de venta")
        self.reserva_btn = self.create_action_button("📅 Nueva Reserva", "#ffc107", "Crear reserva")
        self.estado_btn = self.create_action_button("🔄 Cambiar Estado", "#17a2b8", "Modificar estado")
        self.liberar_btn = self.create_action_button("🔓 Liberar Mesa", "#dc3545", "Liberar mesa")
        for btn in [self.tpv_btn, self.reserva_btn, self.estado_btn, self.liberar_btn]:
            btn.setMinimumWidth(180)
            btn.setMaximumWidth(320)
            btn.setMinimumHeight(38)
            buttons_layout.addWidget(btn)
        layout.addLayout(buttons_layout)
        layout.addStretch()
        # Envolver en scroll si el contenido crece (pero normalmente no será necesario)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(page)
        return scroll

    def create_config_page(self) -> QWidget:
        """Crea la página de configuración"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Formulario de configuración
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 20px;
            }
        """)

        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)

        # Alias
        form_layout.addWidget(QLabel("Alias de la mesa:"))
        self.alias_input = QLineEdit(self.mesa.nombre_display)
        self.alias_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.alias_input)

        # Capacidad
        form_layout.addWidget(QLabel("Capacidad:"))
        self.capacidad_input = QSpinBox()
        self.capacidad_input.setValue(self.mesa.capacidad)
        self.capacidad_input.setRange(1, 20)
        self.capacidad_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.capacidad_input)

        # Notas
        form_layout.addWidget(QLabel("Notas:"))
        self.notas_input = QTextEdit(self.mesa.notas)
        self.notas_input.setMaximumHeight(100)
        self.notas_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(self.notas_input)

        layout.addWidget(form_frame)
        layout.addStretch()
        return page

    def create_history_page(self) -> QWidget:
        """Crea la página de historial"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Historial simulado
        history_items = [
            "🕐 14:30 - Mesa liberada",
            "🍽️ 12:00 - Pedido completado (€45.50)",
            "👥 11:30 - Mesa ocupada (3 personas)",
            "📅 Ayer - Reserva cancelada"
        ]

        for item in history_items:
            item_frame = QFrame()
            item_frame.setStyleSheet("""
                QFrame {
                    background: white;
                    border-left: 4px solid #667eea;
                    border-radius: 4px;
                    padding: 12px;
                    margin: 4px 0;
                }
            """)
            item_layout = QHBoxLayout(item_frame)
            item_layout.addWidget(QLabel(item))
            layout.addWidget(item_frame)

        layout.addStretch()
        return page

    def create_action_button(self, text: str, color: str, tooltip: str) -> QPushButton:
        """Crea un botón de acción estilizado"""
        btn = QPushButton(text)
        btn.setMinimumHeight(60)
        btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        btn.setToolTip(tooltip)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px;
            }}
            QPushButton:hover {{
                background: {color}dd;
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background: {color}bb;
            }}
        """)
        return btn

    def get_input_style(self) -> str:
        """Estilo para campos de entrada"""
        return """
            QLineEdit, QSpinBox, QTextEdit {
                border: 2px solid #e9ecef;
                border-radius: 8px;
                padding: 10px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus, QSpinBox:focus, QTextEdit:focus {
                border-color: #667eea;
                outline: none;
            }
        """

    def cargar_reservas_en_lista(self):
        """Carga las reservas en la lista y asegura consistencia de datos"""
        if not hasattr(self, 'reservas_list') or not self.reserva_service:
            return
        self.reservas_list.clear()
        reservas_por_mesa = self.reserva_service.obtener_reservas_activas_por_mesa()
        reservas = reservas_por_mesa.get(self.mesa.id, [])
        for r in reservas:
            texto = f"{r.fecha_reserva.strftime('%d/%m/%Y')} {r.hora_reserva} - {r.cliente_nombre} ({r.numero_personas}p)"
            item = QListWidgetItem(texto)
            item.setData(32, r)
            self.reservas_list.addItem(item)
        # Forzar refresco visual
        self.reservas_list.repaint()

    def connect_signals(self):
        """Conecta las señales"""
        self.tpv_btn.clicked.connect(lambda: self.iniciar_tpv_requested.emit(self.mesa.id))
        self.reserva_btn.clicked.connect(self.on_reserva_clicked)
        self.estado_btn.clicked.connect(lambda: self.cambiar_estado_requested.emit(self.mesa.id, "libre"))
        self.liberar_btn.clicked.connect(self.on_liberar_clicked)

        if hasattr(self, 'reservas_list'):
            self.reservas_list.itemClicked.connect(self.on_reserva_seleccionada)

    def on_reserva_clicked(self):
        """Maneja clic en botón de reserva"""
        reserva_dialog = ReservaDialog(self, self.mesa, reserva_service=self.reserva_service)
        reserva_dialog.reserva_creada.connect(self.procesar_reserva)
        reserva_dialog.exec()
        self.cargar_reservas_en_lista()

    def on_liberar_clicked(self):
        """Maneja liberación de mesa"""
        self.mesa.estado = 'libre'
        self.mesa.personas_temporal = 0
        self.mesa.alias = ''
        self.mesa_updated.emit(self.mesa)
        mesa_event_bus.mesa_actualizada.emit(self.mesa)
        self.update_ui()

    def on_reserva_seleccionada(self, item):
        """Maneja selección de reserva"""
        reserva = item.data(32)
        dialog = ReservaDialog(self, self.mesa, reserva_service=self.reserva_service, reserva=reserva, modo_edicion=True)
        dialog.reserva_cancelada.connect(lambda r: self.cargar_reservas_en_lista())
        dialog.reserva_editada.connect(lambda r: self.cargar_reservas_en_lista())
        dialog.exec()
        self.cargar_reservas_en_lista()

    def procesar_reserva(self, reserva):
        """Procesa nueva reserva, la guarda y emite eventos globales"""
        if self.mesa and self.reserva_service and reserva:
            from datetime import datetime
            # Asegurar que la reserva se crea con estado 'activa' y todos los campos requeridos
            fecha_hora = datetime.combine(reserva.fecha_reserva, datetime.strptime(reserva.hora_reserva, '%H:%M').time())
            reserva_db = self.reserva_service.crear_reserva(
                mesa_id=reserva.mesa_id,
                cliente=reserva.cliente_nombre,
                fecha_hora=fecha_hora,
                duracion_min=getattr(reserva, 'duracion_min', 120),
                telefono=getattr(reserva, 'cliente_telefono', None),
                personas=getattr(reserva, 'numero_personas', None),
                notas=getattr(reserva, 'notas', None)
            )
            # Forzar estado 'activa' en la base de datos si el modelo lo requiere
            if hasattr(reserva_db, 'estado'):
                reserva_db.estado = 'activa'
            self.mesa.estado = 'reservada'
            mesa_event_bus.mesa_actualizada.emit(self.mesa)
            self.reserva_creada.emit()
            reserva_event_bus.reserva_creada.emit(reserva_db)
            self.update_ui()

    def collect_data(self) -> dict:
        """Recolecta datos del formulario"""
        return {
            'alias': self.alias_input.text(),
            'capacidad': self.capacidad_input.value(),
            'notas': self.notas_input.toPlainText()
        }

    def validate_data(self, data: dict) -> bool:
        """Valida los datos"""
        if not data['alias'].strip():
            QMessageBox.warning(self, "Validación", "El alias no puede estar vacío")
            return False
        return True

    def handle_accept(self):
        """Maneja aceptación del diálogo"""
        data = self.collect_data()
        if self.validate_data(data):
            # Aplicar cambios temporales (alias, capacidad, notas)
            self.mesa.alias = data['alias']
            self.mesa.capacidad = data['capacidad']
            self.mesa.notas = data['notas']

            # Persistencia y sincronización global: solo emitir evento global, sin dependencias directas
            mesa_event_bus.mesa_actualizada.emit(self.mesa)

            # Emitir señal local para listeners directos (si existen)
            self.mesa_updated.emit(self.mesa)

            self.accept()

    def update_ui(self):
        """Actualiza la interfaz"""
        estado_color = {
            'libre': '#28a745', 'ocupada': '#dc3545',
            'reservada': '#ffc107', 'mantenimiento': '#6c757d'
        }.get(self.mesa.estado, '#6c757d')

        self.estado_value.setText(self.mesa.estado.title())
        self.estado_value.setStyleSheet(f"color: {estado_color}; font-weight: bold;")
        self.personas_value.setText(f"{self.mesa.personas_display}/{self.mesa.capacidad}")
        self.alias_value.setText(self.mesa.nombre_display)

        # Actualizar subtítulo del header
        self.set_header_title(
            f"Mesa {self.mesa.numero} - {self.mesa.zona}",
            f"Capacidad: {self.mesa.capacidad} personas • Estado: {self.mesa.estado.title()}"
        )
