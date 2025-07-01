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

class ReservaDialog(QDialog):
    reserva_creada = pyqtSignal(dict)

    def __init__(self, parent=None, mesa: Optional[Mesa] = None):
        super().__init__(parent)
        self.setWindowTitle("🍽️ Crear Reserva")
        self.setModal(True)
        self.setFixedSize(480, 620)
        self.mesa = mesa
        self.setup_ui()
        self.setup_styles()
        self.connect_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        self.setup_header(main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(16)

        self.setup_cliente_section(scroll_layout)
        self.setup_reserva_section(scroll_layout)
        self.setup_detalles_section(scroll_layout)

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

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

        self.telefono_input = self.create_input("Teléfono de contacto")
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
        footer_layout.setSpacing(12)

        self.cancelar_btn = QPushButton("❌ Cancelar")
        self.cancelar_btn.setMinimumHeight(44)
        self.cancelar_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        self.aceptar_btn = QPushButton("✅ Crear Reserva")
        self.aceptar_btn.setMinimumHeight(44)
        self.aceptar_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))

        footer_layout.addWidget(self.cancelar_btn)
        footer_layout.addWidget(self.aceptar_btn)
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
                padding: 12px 24px;
                font-weight: bold;
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
                    stop:0 #6c757d, stop:1 #495057);
                color: white;
            }
            QPushButton#cancelar_btn:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a6268, stop:1 #343a40);
            }
        """)

        self.aceptar_btn.setObjectName("aceptar_btn")
        self.cancelar_btn.setObjectName("cancelar_btn")

    def connect_signals(self):
        self.aceptar_btn.clicked.connect(self.validar_y_aceptar)
        self.cancelar_btn.clicked.connect(self.reject)
        self.personas_input.valueChanged.connect(self.verificar_capacidad)

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

    def validar_y_aceptar(self):
        if not self.cliente_input.text().strip():
            QMessageBox.warning(self, "Campo requerido", "El nombre del cliente es obligatorio.")
            self.cliente_input.setFocus()
            return

        if not self.telefono_input.text().strip():
            QMessageBox.warning(self, "Campo requerido", "El teléfono de contacto es obligatorio.")
            self.telefono_input.setFocus()
            return

        fecha_seleccionada = self.fecha_input.date().toPyDate()
        if fecha_seleccionada < datetime.now().date():
            QMessageBox.warning(self, "Fecha inválida", "No se pueden crear reservas en fechas pasadas.")
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
        self.reserva_creada.emit(datos_reserva)
        self.accept()

    def get_data(self):
        duracion_text = self.duracion_combo.currentText()
        duracion_horas = float(duracion_text.split()[0]) if duracion_text != "Más de 3 horas" else 3.5

        mesa_id = getattr(self.mesa, 'id', None) if self.mesa else None
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
