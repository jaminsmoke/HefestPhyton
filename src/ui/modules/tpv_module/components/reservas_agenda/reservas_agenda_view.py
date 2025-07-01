"""
reservas_agenda_view.py
Widget visual para la agenda/listado de reservas activas.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QDateTimeEdit, QSpinBox, QMessageBox
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal, QTimer
from .reserva_service import ReservaService
from .reserva_model import Reserva
from src.ui.modules.tpv_module.dialogs.reserva_dialog import ReservaDialog
from datetime import datetime
from services.tpv_service import Mesa

class CrearReservaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear nueva reserva")
        layout = QFormLayout(self)
        self.mesa_id_input = QLineEdit()
        self.cliente_input = QLineEdit()
        self.fecha_hora_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.fecha_hora_input.setCalendarPopup(True)
        self.duracion_input = QSpinBox()
        self.duracion_input.setRange(15, 600)
        self.duracion_input.setValue(60)
        self.notas_input = QLineEdit()
        layout.addRow("Mesa ID:", self.mesa_id_input)
        layout.addRow("Cliente:", self.cliente_input)
        layout.addRow("Fecha y hora:", self.fecha_hora_input)
        layout.addRow("Duración (min):", self.duracion_input)
        layout.addRow("Notas:", self.notas_input)
        btns = QHBoxLayout()
        self.btn_ok = QPushButton("Crear")
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)
        btns.addWidget(self.btn_ok)
        btns.addWidget(self.btn_cancel)
        layout.addRow(btns)

    def get_data(self):
        return {
            'mesa_id': self.mesa_id_input.text(),
            'cliente': self.cliente_input.text(),
            'fecha_hora': self.fecha_hora_input.dateTime().toPyDateTime(),
            'duracion_min': self.duracion_input.value(),
            'notas': self.notas_input.text()
        }

class ReservasAgendaView(QWidget):
    reserva_creada = pyqtSignal()
    reserva_cancelada = pyqtSignal()

    def __init__(self, reserva_service: ReservaService, tpv_service=None, parent=None):
        super().__init__(parent)
        self.reserva_service = reserva_service
        self.tpv_service = tpv_service  # Para buscar alias
        self.setWindowTitle("Agenda de Reservas")
        layout = QVBoxLayout(self)
        self.label = QLabel("Reservas activas:")
        layout.addWidget(self.label)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.load_reservas)
        layout.addWidget(self.refresh_button)
        self.list_widget.itemDoubleClicked.connect(self.confirmar_cancelacion_reserva)
        self.load_reservas()

    def abrir_dialogo_crear(self):
        dialog = ReservaDialog(self, None)  # No mesa concreta
        dialog.setWindowTitle("Crear nueva reserva (selecciona mesa)")
        # Campo para mesa_id
        mesa_id_input = QLineEdit()
        mesa_id_input.setPlaceholderText("ID de mesa a reservar")
        mesa_id_input.setMinimumHeight(36)
        # Insertar el campo en el layout del formulario
        form_layout = None
        for child in dialog.findChildren(QFormLayout):
            form_layout = child
            break
        if form_layout:
            form_layout.insertRow(0, "ID de Mesa:", mesa_id_input)
        dialog.aceptar_btn.clicked.disconnect()
        def aceptar():
            if not mesa_id_input.text().strip().isdigit():
                QMessageBox.warning(dialog, "Campo requerido", "Debes indicar un ID de mesa válido.")
                mesa_id_input.setFocus()
                return
            mesa_id = int(mesa_id_input.text())
            # Crear un objeto Mesa temporal solo con id y capacidad
            mesa_temp = Mesa(id=mesa_id, numero=str(mesa_id), zona="", estado="reservada", capacidad=dialog.personas_input.value())
            dialog.mesa = mesa_temp
            dialog.validar_y_aceptar()
        dialog.aceptar_btn.clicked.connect(aceptar)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                mesa_id = int(mesa_id_input.text())
                fecha_hora = datetime.combine(data['fecha'], data['hora'])
                self.reserva_service.crear_reserva(
                    mesa_id=mesa_id,
                    cliente=data['cliente'],
                    fecha_hora=fecha_hora,
                    duracion_min=int(data['duracion_horas'] * 60),
                    notas=data['notas'] or None
                )
                QMessageBox.information(self, "Reserva creada", "La reserva se ha creado correctamente.")
                self.load_reservas()
                self.reserva_creada.emit()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo crear la reserva: {e}")

    def load_reservas(self):
        self.list_widget.clear()
        reservas = self.reserva_service.obtener_reservas_activas()
        for reserva in reservas:
            item = QListWidgetItem(self.format_reserva(reserva))
            item.setData(Qt.ItemDataRole.UserRole, reserva.id)
            self.list_widget.addItem(item)

    def confirmar_cancelacion_reserva(self, item):
        reserva_id = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self,
            "Cancelar reserva",
            "¿Seguro que deseas cancelar esta reserva?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.reserva_service.cancelar_reserva(reserva_id)
                QMessageBox.information(self, "Reserva cancelada", "La reserva ha sido cancelada.")
                self.load_reservas()
                QTimer.singleShot(0, self.reserva_cancelada.emit)  # Emite la señal tras actualizar la UI
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cancelar la reserva: {e}")

    def format_reserva(self, reserva: Reserva) -> str:
        alias = None
        if self.tpv_service:
            try:
                mesas = self.tpv_service.get_mesas()
                mesa = next((m for m in mesas if m.id == reserva.mesa_id), None)
                if mesa and getattr(mesa, 'alias', None):
                    alias = mesa.alias
            except Exception:
                pass
        alias_str = f" ({alias})" if alias else ""
        return f"Mesa {reserva.mesa_id}{alias_str} | {reserva.cliente} | {reserva.fecha_hora.strftime('%d/%m/%Y %H:%M')} | {reserva.duracion_min} min | {reserva.estado}"
