"""
Diálogo de Mesa - Gestión completa y mejorada de una mesa individual
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
    QFrame, QGridLayout, QMessageBox, QLineEdit, QSpinBox, QTextEdit,
    QScrollArea, QSizePolicy, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from services.tpv_service import Mesa
from .reserva_dialog import ReservaDialog
from ..mesa_event_bus import mesa_event_bus

logger = logging.getLogger(__name__)


class MesaDialog(QDialog):
    """Diálogo mejorado para la gestión completa de una mesa"""

    mesa_updated = pyqtSignal(Mesa)  # Señal para actualizar el grid
    iniciar_tpv_requested = pyqtSignal(int)  # mesa_id
    crear_reserva_requested = pyqtSignal(int)  # mesa_id
    cambiar_estado_requested = pyqtSignal(int, str)  # mesa_id, nuevo_estado
    reserva_cancelada = pyqtSignal()
    reserva_creada = pyqtSignal()  # Señal global para agenda

    def __init__(self, mesa: Mesa, parent=None, reserva_service=None):
        super().__init__(parent)
        self.mesa = mesa
        self.reserva_service = reserva_service  # Puede ser None
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Configura la interfaz principal del diálogo"""
        self.setWindowTitle(f"Gestión Mesa {self.mesa.numero} - {self.mesa.zona}")
        self.setFixedSize(520, 700)  # Más alto para mejor separación
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 24)  # más margen inferior
        main_layout.setSpacing(15)

        # Header con información de la mesa
        self.setup_header(main_layout)

        # Añadir lista de reservas activas/futuras justo después del header
        from PyQt6.QtWidgets import QListWidget, QListWidgetItem
        self.reservas_list = QListWidget()
        self.reservas_list.setMinimumHeight(80)
        self.reservas_list.setFont(QFont("Segoe UI", 10))
        self.reservas_list.setStyleSheet("background: #fffbe6; border-radius: 8px; margin-bottom: 8px;")
        self.cargar_reservas_en_lista()
        main_layout.addWidget(self.reservas_list)

        # Panel de información actual
        self.setup_info_panel(main_layout)

        # Panel de acciones principales
        self.setup_actions_panel(main_layout)

        # Panel de configuración
        self.setup_config_panel(main_layout)

        # Añadir stretch para empujar el footer abajo
        main_layout.addStretch()

        # Botones de cierre
        self.setup_footer(main_layout)

        self.apply_styles()

    def cargar_reservas_en_lista(self):
        self.reservas_list.clear()
        if self.reserva_service:
            reservas_por_mesa = self.reserva_service.obtener_reservas_activas_por_mesa()
            reservas = reservas_por_mesa.get(self.mesa.id, [])
            for r in reservas:
                texto = f"{r.fecha_reserva.strftime('%d/%m/%Y')} {r.hora_reserva} - {r.cliente_nombre} ({r.numero_personas}p)"
                item = QListWidgetItem(texto)
                item.setData(32, r)  # Qt.UserRole = 32
                self.reservas_list.addItem(item)

    def setup_header(self, parent_layout: QVBoxLayout):
        """Header con información de la mesa"""
        header_frame = QFrame()
        header_frame.setFixedHeight(90)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 16px;
                padding: 0px 0px 0px 0px;
                margin-bottom: 8px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        mesa_title = QLabel(f"Mesa {self.mesa.numero}")
        mesa_title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        mesa_title.setStyleSheet("color: white; margin: 0; padding-top: 10px;")
        mesa_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(mesa_title)

        mesa_details = QLabel(f"Zona: {self.mesa.zona} | Capacidad: {self.mesa.capacidad} personas")
        mesa_details.setStyleSheet("color: #e0e0e0; font-size: 14px; margin-bottom: 0px;")
        mesa_details.setFont(QFont("Segoe UI", 12, QFont.Weight.Normal))
        mesa_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(mesa_details)

        parent_layout.addWidget(header_frame)

    def setup_info_panel(self, parent_layout: QVBoxLayout):
        """Panel de información actual de la mesa"""
        info_frame = QFrame()
        info_frame.setMinimumHeight(130)
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #fff;
                border: 1px solid #d1dbe6;
                border-radius: 12px;
                padding: 0px;
                margin: 8px 0 8px 0;
            }
        """)
        info_layout = QGridLayout(info_frame)
        info_layout.setHorizontalSpacing(16)
        info_layout.setVerticalSpacing(12)
        info_layout.setContentsMargins(18, 16, 18, 16)
        # Estado actual
        estado_color = {
            'libre': '#28a745',
            'ocupada': '#dc3545',
            'reservada': '#ffc107',
            'mantenimiento': '#6c757d'
        }.get(self.mesa.estado, '#6c757d')
        estado_label = QLabel("Estado Actual:")
        estado_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        estado_label.setStyleSheet("color: #22223b;")
        estado_label.setMinimumHeight(32)
        info_layout.addWidget(estado_label, 0, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.estado_value = QLabel(self.mesa.estado.title())
        self.estado_value.setFont(QFont("Segoe UI", 13, QFont.Weight.Normal))
        self.estado_value.setStyleSheet(f"color: {estado_color};")
        self.estado_value.setMinimumHeight(32)
        info_layout.addWidget(self.estado_value, 0, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # Personas actuales
        personas_label = QLabel("Personas:")
        personas_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        personas_label.setStyleSheet("color: #22223b;")
        personas_label.setMinimumHeight(32)
        info_layout.addWidget(personas_label, 1, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        personas_text = f"{self.mesa.personas_display}/{self.mesa.capacidad}"
        self.personas_value = QLabel(personas_text)
        self.personas_value.setFont(QFont("Segoe UI", 13, QFont.Weight.Normal))
        self.personas_value.setStyleSheet("color: #22223b;")
        self.personas_value.setMinimumHeight(32)
        info_layout.addWidget(self.personas_value, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # Alias actual
        alias_label = QLabel("Nombre:")
        alias_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        alias_label.setStyleSheet("color: #22223b;")
        alias_label.setMinimumHeight(32)
        info_layout.addWidget(alias_label, 2, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.alias_value = QLabel(self.mesa.nombre_display)
        self.alias_value.setFont(QFont("Segoe UI", 13, QFont.Weight.Normal))
        self.alias_value.setStyleSheet("color: #22223b;")
        self.alias_value.setMinimumHeight(32)
        info_layout.addWidget(self.alias_value, 2, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        parent_layout.addWidget(info_frame)

    def setup_actions_panel(self, parent_layout: QVBoxLayout):
        """Panel de acciones principales (espacio extra para el título)"""
        actions_frame = QFrame()
        actions_frame.setMinimumHeight(150)  # Más alto
        actions_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 1px solid #dee2e6;
                border-radius: 12px;
                padding: 0px 0px 10px 0px;
                margin: 8px 0 8px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
        """)
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(10, 6, 10, 10)  # menos margen superior
        actions_layout.setSpacing(6)

        # Título grande y con más altura
        title = QLabel("Acciones Disponibles")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMinimumHeight(48)
        title.setStyleSheet("color: #22223b; background: transparent; padding: 0; margin: 0;")
        actions_layout.addWidget(title)

        actions_layout.addSpacing(14)  # separación amplia entre título y botones

        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(14)
        buttons_row.setContentsMargins(0, 0, 0, 0)

        # Botones principales con efectos modernos
        self.tpv_btn = QPushButton("🍽️ Iniciar TPV")
        self.tpv_btn.setMinimumHeight(36)
        self.tpv_btn.setMaximumWidth(120)
        self.tpv_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.tpv_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #34ce57, stop:1 #28a745);
                color: white; border: none; border-radius: 10px;
                box-shadow: 0 3px 6px rgba(40,167,69,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #1e7e34);
                transform: translateY(-1px);
            }
        """)
        buttons_row.addWidget(self.tpv_btn)

        self.reserva_btn = QPushButton("📅 Reserva")
        self.reserva_btn.setMinimumHeight(36)
        self.reserva_btn.setMaximumWidth(120)
        self.reserva_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.reserva_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffd93d, stop:1 #ffc107);
                color: #212529; border: none; border-radius: 10px;
                box-shadow: 0 3px 6px rgba(255,193,7,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffc107, stop:1 #e0a800);
                transform: translateY(-1px);
            }
        """)
        buttons_row.addWidget(self.reserva_btn)

        self.estado_btn = QPushButton("🔄 Estado")
        self.estado_btn.setMinimumHeight(36)
        self.estado_btn.setMaximumWidth(120)
        self.estado_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.estado_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #20c997, stop:1 #17a2b8);
                color: white; border: none; border-radius: 10px;
                box-shadow: 0 3px 6px rgba(23,162,184,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #138496);
                transform: translateY(-1px);
            }
        """)
        buttons_row.addWidget(self.estado_btn)

        self.liberar_btn = QPushButton("🔓 Liberar")
        self.liberar_btn.setMinimumHeight(36)
        self.liberar_btn.setMaximumWidth(120)
        self.liberar_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.liberar_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e74c3c, stop:1 #dc3545);
                color: white; border: none; border-radius: 10px;
                box-shadow: 0 3px 6px rgba(220,53,69,0.3);
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                transform: translateY(-1px);
            }
        """)
        buttons_row.addWidget(self.liberar_btn)

        actions_layout.addLayout(buttons_row)
        actions_layout.addSpacing(2)
        parent_layout.addWidget(actions_frame)

    def setup_config_panel(self, parent_layout: QVBoxLayout):
        """Panel de configuración rápida (scroll limitado dentro del borde)"""
        from PyQt6.QtWidgets import QScrollArea, QWidget, QSizePolicy, QVBoxLayout, QLabel, QHBoxLayout

        bordered_frame = QFrame()
        bordered_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 1px solid #dee2e6;
                border-radius: 12px;
                padding: 0px;
                margin: 8px 0 8px 0;
                box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            }
        """)
        bordered_layout = QVBoxLayout(bordered_frame)
        bordered_layout.setContentsMargins(8, 8, 8, 8)
        bordered_layout.setSpacing(0)
        # Título fuera del scroll
        title = QLabel("Configuración Rápida")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #22223b; background: transparent; padding-top: 5px; padding-bottom: 8px; letter-spacing: 0.5px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMinimumHeight(56)
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        bordered_layout.addWidget(title)
        bordered_layout.addSpacing(6)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        scroll_content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(8)
        # Alias (horizontal)
        alias_row = QHBoxLayout()
        alias_row.setContentsMargins(0, 0, 0, 0)
        alias_row.setSpacing(8)
        alias_title = QLabel("Alias de mesa")
        alias_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        alias_title.setStyleSheet("color: #495057; min-width: 120px; text-align: right;")
        alias_row.addWidget(alias_title)
        self.alias_input = QLineEdit(self.mesa.nombre_display)
        self.alias_input.setPlaceholderText("Alias de la mesa")
        self.alias_input.setFont(QFont("Segoe UI", 12))
        self.alias_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #80bdff;
                outline: none;
            }
        """)
        alias_row.addWidget(self.alias_input, 1)
        scroll_layout.addLayout(alias_row)
        # Capacidad (horizontal)
        capacidad_row = QHBoxLayout()
        capacidad_row.setContentsMargins(0, 0, 0, 0)
        capacidad_row.setSpacing(8)
        capacidad_title = QLabel("Capacidad")
        capacidad_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        capacidad_title.setStyleSheet("color: #495057; min-width: 120px; text-align: right;")
        capacidad_row.addWidget(capacidad_title)
        self.capacidad_input = QSpinBox()
        self.capacidad_input.setValue(self.mesa.capacidad)
        self.capacidad_input.setRange(1, 100)
        self.capacidad_input.setFont(QFont("Segoe UI", 12))
        self.capacidad_input.setStyleSheet("""
            QSpinBox {
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
                background: white;
            }
            QSpinBox:focus {
                border-color: #80bdff;
                outline: none;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 18px;
                height: 14px;
                background: #e9ecef;
                border: 1px solid #ced4da;
                border-radius: 4px;
                margin: 1px;
            }
            QSpinBox::up-arrow, QSpinBox::down-arrow {
                width: 10px;
                height: 10px;
            }
        """)
        capacidad_row.addWidget(self.capacidad_input, 1)
        scroll_layout.addLayout(capacidad_row)
        # Notas adicionales (alineado a la izquierda, campo grande a la derecha)
        notas_row = QHBoxLayout()
        notas_row.setContentsMargins(0, 0, 0, 0)
        notas_row.setSpacing(8)
        notas_title = QLabel("Notas adicionales")
        notas_title.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        notas_title.setStyleSheet("color: #495057; min-width: 120px; text-align: right; margin-top: 8px;")
        notas_row.addWidget(notas_title, 0, )
        self.notas_input = QTextEdit(self.mesa.notas)
        self.notas_input.setPlaceholderText("Notas adicionales")
        self.notas_input.setFont(QFont("Segoe UI", 12))
        self.notas_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
                min-height: 64px;
                background: white;
            }
            QTextEdit:focus {
                border-color: #80bdff;
                outline: none;
            }
        """)
        notas_row.addWidget(self.notas_input, 1)
        scroll_layout.addLayout(notas_row)
        scroll_area.setWidget(scroll_content)
        bordered_layout.addWidget(scroll_area)
        parent_layout.addWidget(bordered_frame)

    def setup_footer(self, parent_layout: QVBoxLayout):
        """Botones de cierre"""
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 0, 0, 0)
        footer_layout.setSpacing(10)

        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setMinimumHeight(36)
        self.cancel_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background: #f8f9fa;
                color: #212529;
                border: 1px solid #ced4da;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #e9ecef;
            }
        """)
        footer_layout.addWidget(self.cancel_btn)

        self.save_btn = QPushButton("Guardar")
        self.save_btn.setMinimumHeight(36)
        self.save_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.save_btn.setStyleSheet("""
            QPushButton {
                background: #007bff;
                color: white;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #0056b3;
            }
        """)
        footer_layout.addWidget(self.save_btn)

        parent_layout.addLayout(footer_layout)

    def connect_signals(self):
        """Conecta las señales de los botones a sus respectivos slots"""
        self.tpv_btn.clicked.connect(self.on_tpv_btn_clicked)
        self.reserva_btn.clicked.connect(self.on_reserva_btn_clicked)
        self.estado_btn.clicked.connect(self.on_estado_btn_clicked)
        self.liberar_btn.clicked.connect(self.on_liberar_btn_clicked)
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.on_save_btn_clicked)
        self.reservas_list.itemClicked.connect(self.on_reserva_seleccionada)

    def on_tpv_btn_clicked(self):
        """Inicia el TPV para la mesa actual"""
        self.iniciar_tpv_requested.emit(self.mesa.id)

    def on_reserva_btn_clicked(self):
        """Abre el diálogo de reserva para la mesa actual"""
        reserva_dialog = ReservaDialog(self, self.mesa, reserva_service=self.reserva_service)
        reserva_dialog.reserva_creada.connect(self.procesar_reserva)
        reserva_dialog.exec()
        self.cargar_reservas_en_lista()  # Refrescar lista de reservas

    def on_reserva_seleccionada(self, item):
        reserva = item.data(32)
        dialog = ReservaDialog(self, self.mesa, reserva_service=self.reserva_service, reserva=reserva, modo_edicion=True)
        dialog.reserva_editada.connect(self._on_reserva_editada)
        dialog.reserva_cancelada.connect(self._on_reserva_cancelada)
        dialog.exec()

    def _on_reserva_editada(self, reserva):
        self.cargar_reservas_en_lista()
        self.reserva_creada.emit()  # Notifica a la agenda/widgets
        self.update_ui()

    def _on_reserva_cancelada(self, reserva):
        self.cargar_reservas_en_lista()
        self.reserva_cancelada.emit()  # Notifica a la agenda/widgets
        try:
            from src.ui.modules.tpv_module.event_bus import reserva_event_bus
            reserva_event_bus.reserva_cancelada.emit(reserva)
        except ImportError:
            pass
        self.update_ui()

    def procesar_reserva(self, datos_reserva):
        """Procesa los datos de la nueva reserva y la guarda en ReservaService"""
        # Permitir tanto dict como objeto Reserva
        if hasattr(datos_reserva, '__dict__') and not isinstance(datos_reserva, dict):
            # Es un objeto Reserva
            r = datos_reserva
            mesa_id = getattr(r, 'mesa_id', None)
            cliente = getattr(r, 'cliente_nombre', getattr(r, 'cliente', ''))
            telefono = getattr(r, 'cliente_telefono', getattr(r, 'telefono', ''))
            fecha = getattr(r, 'fecha_reserva', None)
            hora = getattr(r, 'hora_reserva', None)
            if isinstance(hora, str):
                from datetime import datetime
                try:
                    hora_obj = datetime.strptime(hora, '%H:%M').time()
                except Exception:
                    hora_obj = None
            else:
                hora_obj = hora
            fecha_hora = None
            if fecha and hora_obj:
                from datetime import datetime
                fecha_hora = datetime.combine(fecha, hora_obj)
            elif fecha:
                fecha_hora = fecha
            duracion_min = 120  # Valor por defecto si no se provee
            personas = getattr(r, 'numero_personas', getattr(r, 'personas', 1))
            notas = getattr(r, 'notas', '')
            estado = getattr(r, 'estado', 'confirmada')
        else:
            # Es un dict
            mesa_id = datos_reserva.get('mesa_id')
            cliente = datos_reserva.get('cliente')
            telefono = datos_reserva.get('telefono')
            fecha = datos_reserva.get('fecha')
            hora = datos_reserva.get('hora')
            from datetime import datetime
            fecha_hora = datetime.combine(fecha, hora) if fecha and hora else fecha
            duracion_min = int(datos_reserva.get('duracion_horas', 1) * 60)
            personas = datos_reserva.get('personas', 1)
            notas = datos_reserva.get('notas')
            estado = datos_reserva.get('estado', 'confirmada')
        # Validación de solapamiento frontend
        if self.reserva_service and mesa_id and fecha_hora:
            try:
                from datetime import timedelta
                reservas_activas = self.reserva_service.obtener_reservas_activas_por_mesa().get(mesa_id, [])
                nueva_inicio = fecha_hora
                if nueva_inicio is None:
                    QMessageBox.critical(self, "Error de reserva", "Faltan datos de fecha y hora para la reserva.")
                    return
                nueva_fin = nueva_inicio + timedelta(minutes=duracion_min)
                solapada = False
                for r in reservas_activas:
                    existente_inicio = getattr(r, 'fecha_hora', None)
                    existente_fin = None
                    if hasattr(r, 'duracion_min'):
                        if existente_inicio is not None:
                            existente_fin = existente_inicio + timedelta(minutes=getattr(r, 'duracion_min', 120))
                        else:
                            continue  # Saltar reservas mal formateadas
                    elif hasattr(r, 'hora_reserva') and hasattr(r, 'fecha_reserva'):
                        try:
                            hora_obj = r.hora_reserva
                            if isinstance(hora_obj, str):
                                hora_obj = datetime.strptime(hora_obj, '%H:%M').time()
                            if r.fecha_reserva and hora_obj:
                                existente_inicio = datetime.combine(r.fecha_reserva, hora_obj)
                                existente_fin = existente_inicio + timedelta(minutes=120)
                            else:
                                continue  # Saltar reservas mal formateadas
                        except Exception:
                            existente_fin = None
                    if existente_inicio and existente_fin:
                        if (nueva_inicio < existente_fin) and (nueva_fin > existente_inicio):
                            solapada = True
                            break
                if solapada:
                    QMessageBox.warning(self, "Solapamiento de reserva", "Ya existe una reserva para esa mesa en el rango horario seleccionado.")
                    return
                self.reserva_service.crear_reserva(
                    mesa_id=mesa_id,
                    cliente=cliente,
                    fecha_hora=fecha_hora,
                    duracion_min=duracion_min,
                    telefono=telefono,
                    personas=personas,
                    notas=notas
                )
                self.reserva_creada.emit()  # Notifica a la agenda
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar la reserva: {e}")
        # ...actualiza estado local...
        if self.mesa:
            self.mesa.estado = 'reservada'
            mesa_event_bus.mesa_actualizada.emit(self.mesa)
            self.update_ui()

    def on_estado_btn_clicked(self):
        """Cambia el estado de la mesa"""
        nuevo_estado = self.estado_value.text().lower()
        self.cambiar_estado_requested.emit(self.mesa.id, nuevo_estado)

    def on_liberar_btn_clicked(self):
        """Libera la mesa actual"""
        self.mesa.estado = 'libre'
        self.mesa.personas_temporal = 0  # Reinicia el número de personas temporal
        self.mesa.alias = ''  # Limpia el alias temporal
        mesa_event_bus.mesa_actualizada.emit(self.mesa)
        self.reserva_cancelada.emit()  # Reactividad: notificar cancelación
        self.update_ui()

    def on_save_btn_clicked(self):
        """Guarda los cambios realizados en la configuración rápida"""
        self.mesa.alias = self.alias_input.text()
        nueva_capacidad = self.capacidad_input.value()
        self.mesa.notas = self.notas_input.toPlainText()
        # Si el número de personas es distinto de la capacidad, es temporal
        if self.mesa.capacidad != nueva_capacidad:
            self.mesa.personas_temporal = nueva_capacidad
        else:
            self.mesa.personas_temporal = None
        self.mesa.capacidad = nueva_capacidad
        # Emitir ambas señales para asegurar actualización
        self.mesa_updated.emit(self.mesa)
        mesa_event_bus.mesa_actualizada.emit(self.mesa)
        self.accept()

    def update_ui(self):
        """Actualiza la interfaz con los datos actuales de la mesa"""
        # Actualiza texto y color del estado
        self.estado_value.setText(self.mesa.estado.title())
        estado_color = {
            'libre': '#28a745',
            'ocupada': '#dc3545',
            'reservada': '#ffc107',
            'mantenimiento': '#6c757d'
        }.get(self.mesa.estado, '#6c757d')
        self.estado_value.setStyleSheet(f"color: {estado_color};")
        self.personas_value.setText(f"{self.mesa.personas_display}/{self.mesa.capacidad}")
        self.alias_value.setText(self.mesa.nombre_display)

    def apply_styles(self):
        """Aplica estilos generales al diálogo"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
        """)
