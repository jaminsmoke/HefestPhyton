"""
reservas_agenda_view.py
Widget visual para la agenda/listado de reservas activas.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QHBoxLayout,
    QDialog,
    QFormLayout,
    QLineEdit,
    QDateTimeEdit,
    QSpinBox,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal, QTimer, QSize
from typing import Any, Optional
from .reserva_service import ReservaService


class CrearReservaDialog(QDialog):
    def __init__(
        self, parent: Optional[QWidget] = None, tpv_service: Optional[Any] = None
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Crear nueva reserva")
        layout = QFormLayout(self)
        from PyQt6.QtWidgets import QComboBox

        self.mesa_id_input = QComboBox()
        # Obtener ids string reales de las mesas
        mesas_ids = []
        if tpv_service and hasattr(tpv_service, "get_mesas"):
            try:
                mesas = tpv_service.get_mesas()
                mesas_ids = [str(m.id) for m in mesas]
            except Exception as e:
                print(f"[CrearReservaDialog] Error obteniendo mesas: {e}")
        self.mesa_id_input.addItems(mesas_ids)
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

    def get_data(self) -> dict[str, Any]:
        return {
            "mesa_id": self.mesa_id_input.currentText().strip(),
            "cliente": self.cliente_input.text(),
            "telefono": self.telefono_input.text(),
            "fecha_hora": self.fecha_hora_input.dateTime().toPyDateTime(),
            "duracion_min": self.duracion_input.value(),
            "notas": self.notas_input.text(),
        }


class ReservasAgendaView(QWidget):
    reserva_creada = pyqtSignal()
    reserva_cancelada = pyqtSignal()

    def __init__(
        self,
        reserva_service: ReservaService,
        tpv_service: Any = None,
        parent: Optional[QWidget] = None,
    ) -> None:
        super().__init__(parent)
        self.reserva_service = reserva_service
        self.tpv_service = tpv_service  # type: ignore[reportUnknownMemberType]
        self.setWindowTitle("Agenda de Reservas")

        # Suscribirse a eventos globales de reservas
        try:
            from src.ui.modules.tpv_module.event_bus import reserva_event_bus

            def log_and_load_reservas(event_name):
                def inner(reserva):
                    print(
                        f"[ReservasAgendaView] Señal recibida: {event_name} para reserva: {getattr(reserva, 'id', None)} mesa_id={getattr(reserva, 'mesa_id', None)}"
                    )
                    self.load_reservas()

                return inner

            reserva_event_bus.reserva_cancelada.connect(
                log_and_load_reservas("reserva_cancelada")
            )
            reserva_event_bus.reserva_creada.connect(
                log_and_load_reservas("reserva_creada")
            )
        except ImportError:
            print("[ReservasAgendaView] No se pudo importar reserva_event_bus")
        layout = QVBoxLayout(self)
        self.label = QLabel("Reservas activas:")
        layout.addWidget(self.label)
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        self.refresh_button = QPushButton("Actualizar")
        self.refresh_button.clicked.connect(self.load_reservas)
        layout.addWidget(self.refresh_button)
        self.list_widget.itemDoubleClicked.connect(self.confirmar_cancelacion_reserva)

        # --- INICIO EXCEPCIÓN FUNCIONAL: Mantener lógica de creación de reservas desde agenda, pero deshabilitada en UI ---
        # TODO [v0.0.13][EXCEPCIÓN FUNCIONAL]: Por política, la creación de reservas desde la agenda está deshabilitada en la UI,
        # pero la lógica y el botón se mantienen ocultos para facilitar futura reactivación si se requiere.
        # Plan de cumplimiento: Documentar en README y reactivar solo si la política cambia.
        self.btn_crear_reserva = QPushButton("Crear reserva")
        self.btn_crear_reserva.clicked.connect(self.crear_reserva_desde_agenda)
        self.btn_crear_reserva.setVisible(False)  # Mantener oculto por política
        layout.addWidget(self.btn_crear_reserva)
        # --- FIN EXCEPCIÓN FUNCIONAL ---

        self.load_reservas()

    def crear_reserva_desde_agenda(self):
        # TODO [v0.0.13][EXCEPCIÓN FUNCIONAL]: Método mantenido por compatibilidad, no accesible desde la UI por política actual.
        dialog = CrearReservaDialog(self, tpv_service=self.tpv_service)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            try:
                reserva = self.reserva_service.crear_reserva(
                    mesa_id=data["mesa_id"],
                    cliente=data["cliente"],
                    fecha_hora=data["fecha_hora"],
                    duracion_min=data["duracion_min"],
                    telefono=data["telefono"],
                    personas=None,  # O adaptar si se añade campo en dialog
                    notas=data["notas"],
                )
                print(f"[ReservasAgendaView] Reserva creada desde agenda: {reserva}")
                self.load_reservas()
                QTimer.singleShot(0, self.reserva_creada.emit)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo crear la reserva: {e}")

    def load_reservas(self) -> None:
        from .reserva_list_item_widget import ReservaListItemWidget

        self.list_widget.clear()
        reservas = self.reserva_service.obtener_reservas_activas()
        for reserva in reservas:
            item = QListWidgetItem()
            item.setSizeHint(QSize(420, 70))
            widget = ReservaListItemWidget(reserva)
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, widget)
            item.setData(Qt.ItemDataRole.UserRole, getattr(reserva, "id", None))  # type: ignore

    def confirmar_cancelacion_reserva(self, item: QListWidgetItem) -> None:
        reserva_id = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(
            self,
            "Cancelar reserva",
            "¿Seguro que deseas cancelar esta reserva?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                # Pasar tpv_service para emitir evento mesa_actualizada
                exito = self.reserva_service.cancelar_reserva(reserva_id, tpv_service=self.tpv_service)
                if exito:
                    QMessageBox.information(
                        self, "Reserva cancelada", "La reserva ha sido cancelada."
                    )
                    self.load_reservas()
                    QTimer.singleShot(
                        0, self.reserva_cancelada.emit
                    )  # Emite la señal tras actualizar la UI
                else:
                    QMessageBox.warning(
                        self, "Error", "No se pudo cancelar la reserva."
                    )
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"No se pudo cancelar la reserva: {e}"
                )

    def format_reserva(self, reserva: Any) -> str:
        alias_str = (
            f" ({getattr(reserva, 'alias', '')})"
            if getattr(reserva, "alias", None)
            else ""
        )
        telefono_str = (
            f" | Tel: {reserva.cliente_telefono}"
            if getattr(reserva, "cliente_telefono", None)
            else ""
        )
        personas_str = (
            f" | Personas: {reserva.numero_personas}"
            if getattr(reserva, "numero_personas", None)
            else ""
        )
        # Unificar fecha y hora
        fecha_hora_str = ""
        if getattr(reserva, "fecha_reserva", None) and getattr(
            reserva, "hora_reserva", None
        ):
            if reserva.fecha_reserva is not None:
                fecha_hora_str = f"{reserva.fecha_reserva.strftime('%d/%m/%Y')} {reserva.hora_reserva}"
            else:
                fecha_hora_str = f"{reserva.hora_reserva}"
        elif getattr(reserva, "fecha_reserva", None):
            if reserva.fecha_reserva is not None:
                fecha_hora_str = reserva.fecha_reserva.strftime("%d/%m/%Y")
        # No hay duracion_min en el modelo unificado, así que lo omitimos o lo calculamos si es necesario
        return f"Mesa {reserva.mesa_id}{alias_str} | {reserva.cliente_nombre} | {fecha_hora_str}{personas_str}{telefono_str} | {reserva.estado}"
