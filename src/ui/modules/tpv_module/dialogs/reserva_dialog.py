from typing import Optional
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSpinBox, QTextEdit, QPushButton, QDateEdit, QTimeEdit, QMessageBox
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont

class ReservaDialog(QDialog):
    def __init__(self, parent=None, mesa: Optional[object] = None):
        super().__init__(parent)
        self.setWindowTitle("Crear Reserva")
        self.setModal(True)
        self.setFixedSize(400, 420)
        self.mesa = mesa
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 18, 24, 18)
        layout.setSpacing(14)

        title = QLabel("Nueva Reserva para Mesa" + (f" {self.mesa.numero}" if self.mesa else ""))
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Cliente
        cliente_label = QLabel("Cliente:")
        cliente_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.cliente_input = QLineEdit()
        self.cliente_input.setPlaceholderText("Nombre del cliente")
        layout.addWidget(cliente_label)
        layout.addWidget(self.cliente_input)

        # Fecha
        fecha_label = QLabel("Fecha:")
        fecha_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.fecha_input = QDateEdit()
        self.fecha_input.setCalendarPopup(True)
        self.fecha_input.setDate(QDate.currentDate())
        layout.addWidget(fecha_label)
        layout.addWidget(self.fecha_input)

        # Hora
        hora_label = QLabel("Hora:")
        hora_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.hora_input = QTimeEdit()
        self.hora_input.setTime(QTime.currentTime())
        layout.addWidget(hora_label)
        layout.addWidget(self.hora_input)

        # Personas
        personas_label = QLabel("Personas:")
        personas_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.personas_input = QSpinBox()
        self.personas_input.setMinimum(1)
        self.personas_input.setMaximum(20)
        if self.mesa:
            self.personas_input.setValue(self.mesa.capacidad)
        layout.addWidget(personas_label)
        layout.addWidget(self.personas_input)

        # Notas
        notas_label = QLabel("Notas:")
        notas_label.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.notas_input = QTextEdit()
        self.notas_input.setPlaceholderText("Observaciones especiales...")
        self.notas_input.setMinimumHeight(50)
        layout.addWidget(notas_label)
        layout.addWidget(self.notas_input)

        # Botones
        btn_row = QHBoxLayout()
        self.aceptar_btn = QPushButton("Reservar")
        self.aceptar_btn.clicked.connect(self.accept)
        self.cancelar_btn = QPushButton("Cancelar")
        self.cancelar_btn.clicked.connect(self.reject)
        btn_row.addWidget(self.aceptar_btn)
        btn_row.addWidget(self.cancelar_btn)
        layout.addLayout(btn_row)

    def get_data(self):
        return {
            "cliente": self.cliente_input.text().strip(),
            "fecha": self.fecha_input.date().toPyDate(),
            "hora": self.hora_input.time().toPyTime(),
            "personas": self.personas_input.value(),
            "notas": self.notas_input.toPlainText().strip(),
        }
