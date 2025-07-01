"""
reservas_agenda_view.py
Widget visual para la agenda/listado de reservas activas.
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QDateTimeEdit, QSpinBox, QMessageBox
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal, QTimer
from .reserva_service import ReservaService
from core.hefest_data_models import Reserva
from src.ui.modules.tpv_module.dialogs.reserva_dialog import ReservaDialog
from datetime import datetime, timedelta
from services.tpv_service import Mesa

class CrearReservaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear nueva reserva")
        layout = QFormLayout(self)
        self.mesa_id_input = QLineEdit()
        self.cliente_input = QLineEdit()
        self.telefono_input = QLineEdit()
        self.fecha_hora_input = QDateTimeEdit(QDateTime.currentDateTime())
        self.fecha_hora_input.setCalendarPopup(True)
        self.duracion_input = QSpinBox()
        self.duracion_input.setRange(15, 600)
        self.duracion_input.setValue(60)
        self.notas_input = QLineEdit()
        layout.addRow("Mesa ID:", self.mesa_id_input)
        layout.addRow("Cliente:", self.cliente_input)
        layout.addRow("Teléfono:", self.telefono_input)
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
            'telefono': self.telefono_input.text(),
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

        # Suscribirse a eventos globales de reservas
        try:
            from src.ui.modules.tpv_module.event_bus import reserva_event_bus
            reserva_event_bus.reserva_cancelada.connect(lambda reserva: self.load_reservas())
            reserva_event_bus.reserva_creada.connect(lambda reserva: self.load_reservas())
        except ImportError:
            pass  # Si no existe el event_bus, ignorar
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
                duracion_min = int(data['duracion_horas'] * 60)
                # Validación de solapamiento frontend
                reservas_activas = self.reserva_service.obtener_reservas_activas_por_mesa().get(mesa_id, [])
                nueva_inicio = fecha_hora
                nueva_fin = nueva_inicio + timedelta(minutes=duracion_min)
                solapada = False
                for r in reservas_activas:
                    existente_inicio = r.fecha_hora
                    existente_fin = existente_inicio + timedelta(minutes=r.duracion_min)
                    if (nueva_inicio < existente_fin) and (nueva_fin > existente_inicio):
                        solapada = True
                        break
                if solapada:
                    QMessageBox.warning(self, "Solapamiento de reserva", "Ya existe una reserva para esa mesa en el rango horario seleccionado.")
                    return
                self.reserva_service.crear_reserva(
                    mesa_id=mesa_id,
                    cliente=data['cliente'],
                    fecha_hora=fecha_hora,
                    duracion_min=duracion_min,
                    telefono=data.get('telefono'),
                    personas=data.get('personas'),
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
                exito = self.reserva_service.cancelar_reserva(reserva_id)
                if exito:
                    QMessageBox.information(self, "Reserva cancelada", "La reserva ha sido cancelada.")
                    self.load_reservas()
                    QTimer.singleShot(0, self.reserva_cancelada.emit)  # Emite la señal tras actualizar la UI
                else:
                    QMessageBox.warning(self, "Error", "No se pudo cancelar la reserva.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cancelar la reserva: {e}")

    def format_reserva(self, reserva: Reserva) -> str:
        alias_str = f" ({getattr(reserva, 'alias', '')})" if getattr(reserva, 'alias', None) else ""
        telefono_str = f" | Tel: {reserva.cliente_telefono}" if getattr(reserva, 'cliente_telefono', None) else ""
        personas_str = f" | Personas: {reserva.numero_personas}" if getattr(reserva, 'numero_personas', None) else ""
        # Unificar fecha y hora
        fecha_hora_str = ""
        if getattr(reserva, 'fecha_reserva', None) and getattr(reserva, 'hora_reserva', None):
            if reserva.fecha_reserva is not None:
                fecha_hora_str = f"{reserva.fecha_reserva.strftime('%d/%m/%Y')} {reserva.hora_reserva}"
            else:
                fecha_hora_str = f"{reserva.hora_reserva}"
        elif getattr(reserva, 'fecha_reserva', None):
            if reserva.fecha_reserva is not None:
                fecha_hora_str = reserva.fecha_reserva.strftime('%d/%m/%Y')
        # No hay duracion_min en el modelo unificado, así que lo omitimos o lo calculamos si es necesario
        return f"Mesa {reserva.mesa_id}{alias_str} | {reserva.cliente_nombre} | {fecha_hora_str}{personas_str}{telefono_str} | {reserva.estado}"
