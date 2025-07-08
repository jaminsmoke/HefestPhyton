from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox,
    QTextEdit, QPushButton, QDateEdit, QTimeEdit, QMessageBox, QFrame,
    QComboBox, QScrollArea, QWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, QDate, QTime, pyqtSignal
from PyQt6.QtGui import QFont, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from datetime import datetime, timedelta
from services.tpv_service import Mesa
from core.hefest_data_models import Reserva
from src.ui.modules.tpv_module.event_bus import reserva_event_bus

class ReservaDialog(QDialog):
    reserva_editada = pyqtSignal(object)
    reserva_cancelada = pyqtSignal(object)
    reserva_creada = pyqtSignal(object)

    def __init__(self, parent=None, mesa: Optional[Mesa] = None, reserva_service=None, reserva: Optional[Reserva] = None, modo_edicion: bool = False):
        print(f"[ReservaDialog] __init__ llamado. mesa={getattr(mesa, 'id', None)}, modo_edicion={modo_edicion}")
        super().__init__(parent)
        self.setWindowTitle("🍽️ Editar Reserva" if modo_edicion else "🍽️ Crear Reserva")
        self.setModal(True)
        self.setFixedSize(520, 620)  # Aumenta el ancho para textos completos
        self.mesa = mesa
        self.reserva_service = reserva_service
        self.reserva = reserva
        self.modo_edicion = modo_edicion
        self.setup_ui()
        self.setup_styles()
        self.connect_signals()
        print(f"[ReservaDialog] connect_signals ejecutado. self.mesa={getattr(self.mesa, 'id', None)}")
        if self.modo_edicion and self.reserva:
            self.cargar_datos_reserva(self.reserva)
        print("[ReservaDialog] Inicialización completa")

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        self.setup_header(main_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(16)

        self.setup_cliente_section(scroll_layout)
        self.setup_reserva_section(scroll_layout)
        self.setup_detalles_section(scroll_layout)

        self.scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(self.scroll_area)

        self.setup_footer(main_layout)

    def setup_header(self, layout):
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                margin-bottom: 16px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 16, 20, 16)

        mesa_num = getattr(self.mesa, 'numero', None) if self.mesa else None
        title = QLabel(f"Nueva Reserva{f' - Mesa {mesa_num}' if mesa_num else ''}")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white; background: transparent;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)

        if self.mesa:
            capacidad = getattr(self.mesa, 'capacidad', 0)
            subtitle = QLabel(f"Capacidad: {capacidad} personas")
            subtitle.setFont(QFont("Segoe UI", 12))
            subtitle.setStyleSheet("color: rgba(255,255,255,0.9); background: transparent;")
            subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
            header_layout.addWidget(subtitle)

        layout.addWidget(header_frame)

    def setup_cliente_section(self, layout):
        section_frame = self.create_section_frame("👤 Información del Cliente")
        section_layout = QVBoxLayout(section_frame)
        section_layout.setContentsMargins(16, 54, 16, 16)
        section_layout.setSpacing(12)

        self.cliente_input = self.create_input("Nombre completo del cliente")
        section_layout.addWidget(self.cliente_input)

        self.telefono_input = self.create_input("Teléfono")
        phone_validator = QRegularExpressionValidator(QRegularExpression(r"^[+]?[0-9\s\-\(\)]{9,15}$"))
        self.telefono_input.setValidator(phone_validator)
        section_layout.addWidget(self.telefono_input)

        layout.addWidget(section_frame)

    def setup_reserva_section(self, layout):
        section_frame = self.create_section_frame("📅 Detalles de la Reserva")
        section_layout = QVBoxLayout(section_frame)
        section_layout.setContentsMargins(16, 54, 16, 16)
        section_layout.setSpacing(12)

        datetime_layout = QHBoxLayout()

        fecha_container = QVBoxLayout()
        fecha_label = QLabel("Fecha:")
        fecha_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(QDate.currentDate())
        self.fecha_input.setMinimumDate(QDate.currentDate())
        fecha_container.addWidget(fecha_label)
        fecha_container.addWidget(self.fecha_input)
        datetime_layout.addLayout(fecha_container)

        hora_container = QVBoxLayout()
        hora_label = QLabel("Hora:")
        hora_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.hora_input = QTimeEdit()
        current_time = QTime.currentTime()
        minutes = 30 if current_time.minute() < 30 else 0
        hour = current_time.hour() + (1 if current_time.minute() >= 30 else 0)
        self.hora_input.setTime(QTime(hour, minutes))
        hora_container.addWidget(hora_label)
        hora_container.addWidget(self.hora_input)
        datetime_layout.addLayout(hora_container)

        section_layout.addLayout(datetime_layout)

        details_layout = QHBoxLayout()

        personas_container = QVBoxLayout()
        personas_label = QLabel("Personas:")
        personas_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.personas_input = QSpinBox()
        self.personas_input.setMinimum(1)
        self.personas_input.setMaximum(20)
        if self.mesa:
            capacidad = getattr(self.mesa, 'capacidad', 1)
            self.personas_input.setValue(capacidad)
        personas_container.addWidget(personas_label)
        personas_container.addWidget(self.personas_input)
        details_layout.addLayout(personas_container)

        duracion_container = QVBoxLayout()
        duracion_label = QLabel("Duración:")
        duracion_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.duracion_combo = QComboBox()
        self.duracion_combo.addItems(["1 hora", "1.5 horas", "2 horas", "2.5 horas", "3 horas", "Más de 3 horas"])
        self.duracion_combo.setCurrentText("2 horas")
        duracion_container.addWidget(duracion_label)
        duracion_container.addWidget(self.duracion_combo)
        details_layout.addLayout(duracion_container)

        section_layout.addLayout(details_layout)

        estado_label = QLabel("Estado:")
        estado_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.estado_combo = QComboBox()
        self.estado_combo.addItems(["Confirmada", "Pendiente", "Tentativa"])
        section_layout.addWidget(estado_label)
        section_layout.addWidget(self.estado_combo)

        self.hora_input.timeChanged.connect(self.validar_hora_reserva)
        self.fecha_input.dateChanged.connect(self.validar_hora_reserva)
        self.duracion_combo.currentIndexChanged.connect(self.validar_hora_reserva)
        self.hora_feedback_label = QLabel("")
        self.hora_feedback_label.setFont(QFont("Segoe UI", 9))
        self.hora_feedback_label.setStyleSheet("color: #d32f2f;")
        self.hora_feedback_label.setWordWrap(True)
        self.hora_feedback_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        hora_container.addWidget(self.hora_feedback_label)

        self.sugerir_hora_btn = QPushButton("💡 Sugerir otra hora")
        self.sugerir_hora_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.sugerir_hora_btn.setStyleSheet("""
            QPushButton {
                background: #e9ecef;
                color: #333;
                border: 2px solid #ced4da;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: #ced4da;
            }
        """)
        self.sugerir_hora_btn.setVisible(False)
        hora_container.addWidget(self.sugerir_hora_btn)

        layout.addWidget(section_frame)

    def setup_detalles_section(self, layout):
        section_frame = self.create_section_frame("📝 Observaciones")
        section_layout = QVBoxLayout(section_frame)
        section_layout.setContentsMargins(16, 54, 16, 16)

        self.notas_input = QTextEdit()
        self.notas_input.setPlaceholderText("Alergias, preferencias, ocasión especial, etc...")
        self.notas_input.setMaximumHeight(80)
        section_layout.addWidget(self.notas_input)

        layout.addWidget(section_frame)

    def setup_footer(self, layout):
        footer_layout = QHBoxLayout()
        footer_layout.setContentsMargins(0, 16, 0, 0)
        footer_layout.setSpacing(24)  # Más separación visual entre botones

        self.cancelar_btn = QPushButton("❌\nCancelar")
        self.cancelar_btn.setMinimumHeight(44)
        self.cancelar_btn.setMinimumWidth(120)
        self.cancelar_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        self.cancelar_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        if self.modo_edicion:
            self.guardar_btn = QPushButton("✔️\nGuardar Cambios")
            self.guardar_btn.setMinimumHeight(44)
            self.guardar_btn.setMinimumWidth(120)
            self.guardar_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            self.guardar_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            self.eliminar_btn = QPushButton("🗑️\nCancelar Reserva")
            self.eliminar_btn.setMinimumHeight(44)
            self.eliminar_btn.setMinimumWidth(120)
            self.eliminar_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            self.eliminar_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            footer_layout.addWidget(self.eliminar_btn)
            footer_layout.addWidget(self.guardar_btn)
        else:
            self.aceptar_btn = QPushButton("✅\nCrear Reserva")
            self.aceptar_btn.setMinimumHeight(44)
            self.aceptar_btn.setMinimumWidth(120)
            self.aceptar_btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
            self.aceptar_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            footer_layout.addWidget(self.aceptar_btn)
        footer_layout.addWidget(self.cancelar_btn)
        layout.addLayout(footer_layout)

    def create_section_frame(self, title):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e0e0e0;
                border-radius: 12px;
                margin: 4px 0;
            }
        """)

        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("""
            QLabel {
                background: transparent;
                color: #333;
                padding: 12px 16px;
                border-bottom: 1px solid #f0f0f0;
            }
        """)
        title_label.setParent(frame)
        title_label.move(0, 0)
        title_label.resize(frame.width(), 48)

        return frame

    def create_input(self, placeholder):
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setMinimumHeight(36)
        return input_field

    def setup_styles(self):
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QLineEdit, QSpinBox, QDateEdit, QTimeEdit, QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus, QSpinBox:focus, QDateEdit:focus, QTimeEdit:focus, QComboBox:focus {
                border-color: #667eea;
                outline: none;
            }
            QTextEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
                background: white;
            }
            QTextEdit:focus {
                border-color: #667eea;
            }
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 8px 12px;
                font-weight: bold;
                min-width: 100px;
                max-width: 100%;
                white-space: normal;
                text-align: center;
                word-break: break-word;
                font-size: 11px;
            }
            QPushButton, QPushButton * {
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            QPushButton b {
                font-size: 11px;
            }
            QPushButton span {
                font-size: 11px;
            }
            QPushButton#guardar_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #20c997);
                color: white;
            }
            QPushButton#guardar_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #20c997, stop:1 #17a2b8);
            }
            QPushButton#eliminar_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff9800, stop:1 #ff7043);
                color: white;
            }
            QPushButton#eliminar_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff7043, stop:1 #ff9800);
            }
            QPushButton#aceptar_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #20c997);
                color: white;
            }
            QPushButton#aceptar_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #20c997, stop:1 #17a2b8);
            }
            QPushButton#cancelar_btn {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e53935, stop:1 #b71c1c);
                color: white;
            }
            QPushButton#cancelar_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #b71c1c, stop:1 #e53935);
            }
        """)
        # Solo asignar objectName si existen los botones
        if hasattr(self, "aceptar_btn"):
            self.aceptar_btn.setObjectName("aceptar_btn")
        if hasattr(self, "guardar_btn"):
            self.guardar_btn.setObjectName("guardar_btn")
        if hasattr(self, "eliminar_btn"):
            self.eliminar_btn.setObjectName("eliminar_btn")
        if hasattr(self, "cancelar_btn"):
            self.cancelar_btn.setObjectName("cancelar_btn")

    def connect_signals(self):
        if self.modo_edicion:
            self.guardar_btn.clicked.connect(self.editar_y_guardar)
            self.eliminar_btn.clicked.connect(self.confirmar_cancelacion_reserva)
        else:
            self.aceptar_btn.clicked.connect(self.validar_y_aceptar)
        self.cancelar_btn.clicked.connect(self.reject)
        self.personas_input.valueChanged.connect(self.verificar_capacidad)
        self.sugerir_hora_btn.clicked.connect(self.sugerir_proxima_hora_libre)

    def verificar_capacidad(self):
        if self.mesa:
            capacidad = getattr(self.mesa, 'capacidad', 0)
            if self.personas_input.value() > capacidad:
                self.personas_input.setStyleSheet("""
                    QSpinBox {
                        border: 2px solid #dc3545;
                        border-radius: 8px;
                        padding: 8px 12px;
                        background: #fff5f5;
                    }
                """)
            else:
                self.personas_input.setStyleSheet("")

    def validar_hora_reserva(self):
        self._proxima_hora_libre = None  # Inicializar siempre para evitar AttributeError
        if not self.mesa:
            self.hora_feedback_label.setText("")
            self.sugerir_hora_btn.setVisible(False)
            return
        from datetime import datetime, timedelta
        mesa_id = str(getattr(self.mesa, 'id', '')) if self.mesa else ''
        if not mesa_id:
            self.hora_feedback_label.setText("")
            self.sugerir_hora_btn.setVisible(False)
            return
        fecha = self.fecha_input.date().toPyDate()
        hora = self.hora_input.time().toPyTime()
        duracion_text = self.duracion_combo.currentText()
        # Adaptar a los textos de duración actuales
        if "Más de 3" in duracion_text:
            duracion_horas = 3.5
        else:
            duracion_horas = float(duracion_text.split()[0].replace(",", "."))
        duracion_min = int(duracion_horas * 60)
        nueva_inicio = datetime.combine(fecha, hora)
        nueva_fin = nueva_inicio + timedelta(minutes=duracion_min)
        # --- Nueva lógica: siempre sugerir próxima hora libre ---
        # Construir lista de (inicio, fin) ordenada y calcular self._proxima_hora_libre antes de validar si es pasado
        reservas_activas = []
        if self.reserva_service:
            reservas_por_mesa = self.reserva_service.obtener_reservas_activas_por_mesa()
            from datetime import timedelta as td
            fechas_a_considerar = [fecha]
            fechas_a_considerar.append(fecha + td(days=1))
            reservas_activas = [
                r for r in reservas_por_mesa.get(mesa_id, [])
                if getattr(r, 'fecha_reserva', None) in fechas_a_considerar or
                   (getattr(r, 'fecha_reserva', None) == fecha - td(days=1) and self._reserva_cruza_medianoche(r))
            ]
        reservas_intervalos = []
        for r in reservas_activas:
            try:
                hora_str = getattr(r, 'hora_reserva', None)
                if hora_str and isinstance(hora_str, str):
                    h, m = map(int, hora_str.split(":"))
                    existente_inicio = datetime.combine(r.fecha_reserva, datetime.min.time()).replace(hour=h, minute=m)
                else:
                    continue
                if hasattr(r, 'duracion_min') and r.duracion_min:
                    duracion_existente = r.duracion_min
                else:
                    duracion_existente = duracion_min
                existente_fin = existente_inicio + timedelta(minutes=duracion_existente)
                reservas_intervalos.append((existente_inicio, existente_fin))
            except Exception:
                continue
        reservas_intervalos.sort()
        # Buscar hueco entre reservas
        proxima_libre = nueva_inicio
        for inicio, fin in reservas_intervalos:
            if proxima_libre + timedelta(minutes=duracion_min) <= inicio:
                break
            elif proxima_libre >= inicio and proxima_libre < fin:
                proxima_libre = fin
        self._proxima_hora_libre = proxima_libre.time()

        # Validar si la hora es pasada
        if nueva_inicio < datetime.now():
            self.hora_feedback_label.setText("⚠️ La fecha y hora seleccionadas ya han pasado. Elige una hora futura o pulsa 'Sugerir otra hora'.")
            self.hora_feedback_label.setStyleSheet("color: #b71c1c; font-size: 13px; font-weight: bold;")
            # Si hay una sugerencia futura posible, mostrar el botón
            if self._proxima_hora_libre is not None:
                proxima = datetime.combine(fecha, self._proxima_hora_libre)
                if proxima > datetime.now():
                    self.sugerir_hora_btn.setVisible(True)
                    self.sugerir_hora_btn.setEnabled(True)
                else:
                    self.sugerir_hora_btn.setVisible(False)
                    self.sugerir_hora_btn.setEnabled(False)
            else:
                self.sugerir_hora_btn.setVisible(False)
                self.sugerir_hora_btn.setEnabled(False)
            return
        # ...continúa la lógica original después de este bloque...

        # Obtener reservas activas de la mesa para ese día
        reservas_activas = []
        if self.reserva_service:
            reservas_por_mesa = self.reserva_service.obtener_reservas_activas_por_mesa()
            # Buscar reservas activas de la mesa para el día actual y el siguiente (para detectar cruces de medianoche)
            fechas_a_considerar = [fecha]
            from datetime import timedelta as td
            fechas_a_considerar.append(fecha + td(days=1))
            reservas_activas = [
                r for r in reservas_por_mesa.get(mesa_id, [])
                if getattr(r, 'fecha_reserva', None) in fechas_a_considerar or
                   # También incluir reservas que empiezan el día anterior y terminan después de medianoche
                   (getattr(r, 'fecha_reserva', None) == fecha - td(days=1) and
                    self._reserva_cruza_medianoche(r))
            ]
        # --- Nueva lógica: siempre sugerir próxima hora libre ---
        solapada = False
        self._proxima_hora_libre = None
        # Construir lista de (inicio, fin) ordenada
        reservas_intervalos = []
        for r in reservas_activas:
            try:
                hora_str = getattr(r, 'hora_reserva', None)
                if hora_str and isinstance(hora_str, str):
                    h, m = map(int, hora_str.split(":"))
                    existente_inicio = datetime.combine(r.fecha_reserva, datetime.min.time()).replace(hour=h, minute=m)
                else:
                    continue
                if hasattr(r, 'duracion_min') and r.duracion_min:
                    duracion_existente = r.duracion_min
                else:
                    duracion_existente = duracion_min
                existente_fin = existente_inicio + timedelta(minutes=duracion_existente)
                reservas_intervalos.append((existente_inicio, existente_fin))
            except Exception:
                continue
        reservas_intervalos.sort()
        # Buscar hueco entre reservas
        proxima_libre = nueva_inicio
        for inicio, fin in reservas_intervalos:
            if proxima_libre + timedelta(minutes=duracion_min) <= inicio:
                # Hay hueco antes de esta reserva
                break
            elif proxima_libre >= inicio and proxima_libre < fin:
                # Está dentro de una reserva, saltar al final
                proxima_libre = fin
        self._proxima_hora_libre = proxima_libre.time()
        # Comprobar si la hora solicitada está disponible
        disponible = True
        for inicio, fin in reservas_intervalos:
            if (nueva_inicio < fin) and (nueva_fin > inicio):
                disponible = False
                break
        if not disponible:
            texto = f"Hora no disponible. Próxima hora libre: {self._proxima_hora_libre.strftime('%H:%M')}"
            self.sugerir_hora_btn.setVisible(True)
            self.sugerir_hora_btn.setEnabled(True)
            self.hora_feedback_label.setText(texto)
            self.hora_feedback_label.setStyleSheet("color: #d32f2f;")
        else:
            self.hora_feedback_label.setText("Hora disponible")
            self.hora_feedback_label.setStyleSheet("color: #388e3c;")
            self.sugerir_hora_btn.setVisible(False)
            self.sugerir_hora_btn.setEnabled(False)

    def sugerir_proxima_hora_libre(self):
        """Ajusta la hora de la reserva a la próxima hora libre sugerida y muestra feedback llamativo, sin mover el scroll ni expandir el contenido. Si la sugerencia es en el pasado, muestra advertencia y no ajusta la hora."""
        from datetime import datetime, date
        # Guardar posición actual del scroll vertical
        scroll_bar = getattr(self, "scroll_area", None)
        if scroll_bar is not None:
            scroll_bar = scroll_bar.verticalScrollBar()
        if scroll_bar is not None:
            scroll_pos = scroll_bar.value()
        else:
            scroll_pos = None
        if self._proxima_hora_libre is not None:
            # Validar que la sugerencia no sea en el pasado
            fecha = self.fecha_input.date().toPyDate()
            sugerida = datetime.combine(fecha, self._proxima_hora_libre)
            if sugerida < datetime.now():
                icono = "⚠️"
                texto = f"{icono} No hay una próxima hora libre válida en el futuro para esta mesa."
                self.hora_feedback_label.setText(texto)
                self.hora_feedback_label.setStyleSheet("color: #b71c1c; font-size: 13px; font-weight: bold;")
                # No ajustar la hora ni mostrar éxito
            else:
                try:
                    self.hora_input.setTime(QTime(self._proxima_hora_libre.hour, self._proxima_hora_libre.minute))
                    self.validar_hora_reserva()
                    # Mensaje con icono llamativo
                    icono = "⏰"
                    texto = f"{icono} Hora ajustada automáticamente a la próxima hora libre: <b>{self._proxima_hora_libre.strftime('%H:%M')}</b>"
                    self.hora_feedback_label.setText(texto)
                    # Efecto visual llamativo: fondo animado y borde
                    self.hora_feedback_label.setStyleSheet("""
                        color: #1976d2;
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e3f2fd, stop:1 #bbdefb);
                        border: 2px solid #1976d2;
                        border-radius: 8px;
                        padding: 6px 12px;
                        font-weight: bold;
                        font-size: 15px;
                        transition: background 0.5s, border 0.5s;
                    """)
                    # Parpadeo temporal
                    from PyQt6.QtCore import QTimer
                    def reset_feedback_style():
                        self.hora_feedback_label.setStyleSheet("color: #1976d2; font-size: 15px; font-weight: bold;")
                    QTimer.singleShot(1200, reset_feedback_style)
                except Exception as e:
                    print(f"[ReservaDialog] Error al sugerir próxima hora libre: {e}")
                    icono = "⚠️"
                    texto = f"{icono} Error al ajustar la próxima hora libre."
                    self.hora_feedback_label.setText(texto)
                    self.hora_feedback_label.setStyleSheet("color: #b71c1c; font-size: 13px; font-weight: bold;")
        else:
            print("[ReservaDialog] self._proxima_hora_libre es None al sugerir hora.")
            icono = "⚠️"
            texto = f"{icono} No se encontró una próxima hora libre para esta mesa."
            self.hora_feedback_label.setText(texto)
            self.hora_feedback_label.setStyleSheet("color: #b71c1c; font-size: 13px; font-weight: bold;")
        # Restaurar posición del scroll vertical
        if scroll_bar is not None and scroll_pos is not None:
            scroll_bar.setValue(scroll_pos)

    def validar_y_aceptar(self):
        print("[ReservaDialog] validar_y_aceptar llamado")
        if not self.cliente_input.text().strip():
            QMessageBox.warning(self, "Campo requerido", "El nombre del cliente es obligatorio.")
            self.cliente_input.setFocus()
            return

        if not self.telefono_input.text().strip():
            QMessageBox.warning(self, "Campo requerido", "El teléfono de contacto es obligatorio.")
            self.telefono_input.setFocus()
            return

        fecha_seleccionada = self.fecha_input.date().toPyDate()
        hora_seleccionada = self.hora_input.time().toPyTime()
        from datetime import datetime
        dt_reserva = datetime.combine(fecha_seleccionada, hora_seleccionada)
        if dt_reserva < datetime.now():
            QMessageBox.warning(self, "Fecha y hora inválidas", "No se pueden crear reservas en el pasado.")
            return

        if self.mesa:
            capacidad = getattr(self.mesa, 'capacidad', 0)
            if self.personas_input.value() > capacidad:
                respuesta = QMessageBox.question(
                    self, "Capacidad excedida",
                    f"La mesa tiene capacidad para {capacidad} personas, pero has seleccionado {self.personas_input.value()}.\n¿Deseas continuar?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if respuesta == QMessageBox.StandardButton.No:
                    return

        datos_reserva = self.get_data()
        print(f"[ReservaDialog] Datos recogidos para crear reserva: {datos_reserva}")
        # Crear objeto Reserva unificado
        reserva = Reserva(
            id=None,
            mesa_id=str(datos_reserva["mesa_id"]),
            cliente_nombre=datos_reserva["cliente"],
            cliente_telefono=datos_reserva["telefono"],
            fecha_reserva=datos_reserva["fecha"],
            hora_reserva=datos_reserva["hora"].strftime('%H:%M'),
            numero_personas=datos_reserva["personas"],
            estado="confirmada",  # o datos_reserva["estado"] si se requiere
            notas=datos_reserva["notas"]
        )
        print(f"[ReservaDialog] Emitiendo señal reserva_creada con reserva: {reserva}")
        self.reserva_creada.emit(reserva)
        self.accept()

    def get_data(self):
        duracion_text = self.duracion_combo.currentText()
        duracion_horas = float(duracion_text.split()[0]) if duracion_text != "Más de 3 horas" else 3.5

        mesa_id = str(getattr(self.mesa, 'id', '')) if self.mesa else ''
        mesa_numero = getattr(self.mesa, 'numero', None) if self.mesa else None

        return {
            "cliente": self.cliente_input.text().strip(),
            "telefono": self.telefono_input.text().strip(),
            "fecha": self.fecha_input.date().toPyDate(),
            "hora": self.hora_input.time().toPyTime(),
            "personas": self.personas_input.value(),
            "duracion_horas": duracion_horas,
            "estado": self.estado_combo.currentText().lower(),
            "notas": self.notas_input.toPlainText().strip(),
            "mesa_id": mesa_id,
            "mesa_numero": mesa_numero,
        }

    def _reserva_cruza_medianoche(self, reserva):
        """Devuelve True si la reserva termina después de medianoche (cruza de un día a otro)."""
        try:
            from datetime import datetime, timedelta
            fecha = getattr(reserva, 'fecha_reserva', None)
            hora_str = getattr(reserva, 'hora_reserva', None)
            if not fecha or not hora_str:
                return False
            h, m = map(int, hora_str.split(":"))
            inicio = datetime.combine(fecha, datetime.min.time()).replace(hour=h, minute=m)
            # Duración: si no existe, asumir 2h
            duracion = getattr(reserva, 'duracion_min', None)
            if duracion is None:
                duracion = 120
            fin = inicio + timedelta(minutes=duracion)
            return fin.date() > inicio.date()
        except Exception:
            return False

    def cargar_datos_reserva(self, reserva):
        """Carga los datos de una reserva existente en el formulario para edición."""
        from PyQt6.QtCore import QDate, QTime
        from datetime import datetime
        if reserva.fecha_reserva:
            self.fecha_input.setDate(QDate(reserva.fecha_reserva.year, reserva.fecha_reserva.month, reserva.fecha_reserva.day))
        if reserva.hora_reserva:
            try:
                hora_dt = datetime.strptime(reserva.hora_reserva, '%H:%M')
                self.hora_input.setTime(QTime(hora_dt.hour, hora_dt.minute))
            except Exception:
                pass
        self.cliente_input.setText(reserva.cliente_nombre or "")
        self.telefono_input.setText(reserva.cliente_telefono or "")
        self.personas_input.setValue(reserva.numero_personas or 1)
        self.notas_input.setText(reserva.notas or "")
        # Estado si aplica
        if hasattr(self, 'estado_combo') and reserva.estado:
            idx = self.estado_combo.findText(reserva.estado.capitalize())
            if idx >= 0:
                self.estado_combo.setCurrentIndex(idx)

    def editar_y_guardar(self):
        """Valida y guarda los cambios de la reserva editada."""
        datos = self.get_data()
        if self.reserva_service and self.reserva:
            exito = self.reserva_service.editar_reserva(self.reserva.id, datos)
            if exito:
                QMessageBox.information(self, "Reserva actualizada", "Los cambios se guardaron correctamente.")
                self.reserva_editada.emit(self.reserva)
                try:
                    from src.ui.modules.tpv_module.event_bus import reserva_event_bus
                    reserva_event_bus.reserva_creada.emit(self.reserva)
                except ImportError:
                    pass
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la reserva.")

    def confirmar_cancelacion_reserva(self):
        """Muestra un diálogo de confirmación antes de cancelar la reserva."""
        resp = QMessageBox.question(self, "Cancelar Reserva", "¿Seguro que deseas cancelar esta reserva?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if resp == QMessageBox.StandardButton.Yes:
            self.cancelar_reserva()

    def cancelar_reserva(self):
        """Cancela la reserva editada."""
        if self.reserva_service and self.reserva:
            exito = self.reserva_service.cancelar_reserva(self.reserva.id)
            if exito:
                QMessageBox.information(self, "Reserva cancelada", "La reserva fue cancelada correctamente.")
                self.reserva_cancelada.emit(self.reserva)
                reserva_event_bus.reserva_cancelada.emit(self.reserva)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "No se pudo cancelar la reserva.")
