"""
Módulo de gestión de hospedería que hereda de BaseModule.
"""

import logging
from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QGridLayout,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QComboBox,
    QLineEdit,
    QDateEdit,
    QSpinBox,
    QMessageBox,
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QTextEdit,
    QGroupBox,
    QCheckBox,
    QHeaderView,
)
from PyQt6.QtCore import Qt, QDate, QTimer
from PyQt6.QtGui import QFont

from .module_base_interface import BaseModule
from services.hospederia_service import HospederiaService

logger = logging.getLogger(__name__)


class HospederiaModule(BaseModule):
    """Módulo completo de gestión de hospedería"""

    def __init__(self):
        super().__init__()
        self.hospederia_service = HospederiaService()
        self.rooms_data = []
        self.reservations_data = []

        # Timer para actualización automática
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.refresh_data)
        self.update_timer.start(30000)  # Actualizar cada 30 segundos

        self.setup_ui()
        self.refresh_data()

    def create_module_header(self):
        """Crea el header del módulo de hospedería"""
        header = QFrame()
        header.setObjectName("module-header")
        header.setFixedHeight(60)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        title = QLabel("🏨 Gestión de Hospedería")
        title.setObjectName("module-title")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #1f2937;")
        layout.addWidget(title)

        layout.addStretch()

        # Indicadores de estado
        stats_layout = QHBoxLayout()

        self.available_label = QLabel("Disponibles: 0")
        self.available_label.setStyleSheet(
            "color: #10b981; font-weight: bold; margin-right: 15px;"
        )
        stats_layout.addWidget(self.available_label)

        self.occupied_label = QLabel("Ocupadas: 0")
        self.occupied_label.setStyleSheet(
            "color: #ef4444; font-weight: bold; margin-right: 15px;"
        )
        stats_layout.addWidget(self.occupied_label)

        self.cleaning_label = QLabel("Limpieza: 0")
        self.cleaning_label.setStyleSheet(
            "color: #f59e0b; font-weight: bold; margin-right: 15px;"
        )
        stats_layout.addWidget(self.cleaning_label)

        layout.addLayout(stats_layout)

        # Botones de acción
        new_booking_btn = QPushButton("📅 Nueva Reserva")
        new_booking_btn.setObjectName("action-button")
        new_booking_btn.setStyleSheet(
            """
            QPushButton {
                padding: 8px 16px;
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #2563eb;
            }
        """
        )
        new_booking_btn.clicked.connect(self.show_new_reservation_dialog)
        layout.addWidget(new_booking_btn)

        check_in_btn = QPushButton("🏠 Check-in")
        check_in_btn.setStyleSheet(
            """
            QPushButton {
                padding: 8px 16px;
                background: #10b981;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                margin-left: 10px;
            }
            QPushButton:hover {
                background: #059669;
            }        """
        )
        check_in_btn.clicked.connect(self.show_check_in_dialog)
        layout.addWidget(check_in_btn)

        return header

    def setup_ui(self):
        """Configura la interfaz del módulo de hospedería"""
        # Crear el header del módulo
        header = self.create_module_header()
        self.content_layout.addWidget(header)

        # Inicializar tabla de reservas
        self.reservations_table = QTableWidget()
        self.reservations_table.setColumnCount(5)
        self.reservations_table.setHorizontalHeaderLabels(
            ["ID", "Huésped", "Fecha Check-In", "Fecha Check-Out", "Estado"]
        )
        header = self.reservations_table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Agregar tabla al layout principal
        self.content_layout.addWidget(self.reservations_table)

        # Botón de actualizar
        refresh_btn = QPushButton("Actualizar Reservas")
        refresh_btn.clicked.connect(self.load_reservations)
        self.content_layout.addWidget(refresh_btn)

        # Asegurarse de que el método `load_reservations` esté definido
        self.load_reservations = (
            self.load_reservations or self._placeholder_load_reservations
        )

    def _placeholder_load_reservations(self):
        """Placeholder para evitar errores si `load_reservations` no está implementado"""
        QMessageBox.information(
            self,
            "Información",
            "La funcionalidad de cargar reservas aún no está implementada.",
        )

    def create_rooms_tab(self):
        """Crea la pestaña de gestión de habitaciones"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Panel de habitaciones
        rooms_title = QLabel("Estado de Habitaciones")
        rooms_title.setStyleSheet(
            "font-size: 18px; font-weight: bold; margin-bottom: 10px;"
        )
        layout.addWidget(rooms_title)

        # Grid de habitaciones
        rooms_grid = QGridLayout()
        rooms_grid.setSpacing(10)
        self.populate_rooms_grid(rooms_grid)

        rooms_widget = QWidget()
        rooms_widget.setLayout(rooms_grid)
        layout.addWidget(rooms_widget)

        layout.addStretch()
        return widget

    def create_reservations_tab(self):
        """Crea la pestaña de gestión de reservas"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tabla de reservas
        self.reservations_table = QTableWidget()  # Inicialización del atributo
        self.reservations_table.setColumnCount(6)
        self.reservations_table.setHorizontalHeaderLabels(
            ["ID", "Cliente", "Habitación", "Check-in", "Check-out", "Estado"]
        )
        header = self.reservations_table.horizontalHeader()
        if header:
            header.setStretchLastSection(True)

        layout.addWidget(self.reservations_table)

        # Botones de acción
        buttons_layout = QHBoxLayout()

        new_reservation_btn = QPushButton("Nueva Reserva")
        new_reservation_btn.clicked.connect(self.show_new_reservation_dialog)
        buttons_layout.addWidget(new_reservation_btn)

        edit_reservation_btn = QPushButton("Editar Reserva")
        buttons_layout.addWidget(edit_reservation_btn)

        cancel_reservation_btn = QPushButton("Cancelar Reserva")
        buttons_layout.addWidget(cancel_reservation_btn)

        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)

        return widget

    def create_checkin_tab(self):
        """Crea la pestaña de check-in/check-out"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Sección de check-in
        checkin_group = QGroupBox("Check-in")
        checkin_layout = QFormLayout(checkin_group)

        self.checkin_reservation_combo = QComboBox()
        checkin_layout.addRow("Reserva:", self.checkin_reservation_combo)

        checkin_btn = QPushButton("Realizar Check-in")
        checkin_btn.clicked.connect(self.show_check_in_dialog)
        checkin_layout.addRow(checkin_btn)

        layout.addWidget(checkin_group)

        # Sección de check-out
        checkout_group = QGroupBox("Check-out")
        checkout_layout = QFormLayout(checkout_group)

        self.checkout_room_combo = QComboBox()
        checkout_layout.addRow("Habitación:", self.checkout_room_combo)

        checkout_btn = QPushButton("Realizar Check-out")
        checkout_btn.clicked.connect(self.show_check_out_dialog)
        checkout_layout.addRow(checkout_btn)

        layout.addWidget(checkout_group)

        layout.addStretch()
        return widget

    def populate_rooms_grid(self, grid_layout):
        """Popula el grid con las habitaciones"""
        rooms = [
            ("101", "Disponible", "#10b981"),
            ("102", "Ocupada", "#ef4444"),
            ("103", "Limpieza", "#f59e0b"),
            ("104", "Disponible", "#10b981"),
            ("201", "Ocupada", "#ef4444"),
            ("202", "Disponible", "#10b981"),
            ("203", "Mantenimiento", "#6b7280"),
            ("204", "Disponible", "#10b981"),
        ]

        row, col = 0, 0
        for room_number, status, color in rooms:
            room_btn = QPushButton(f"Hab. {room_number}\n{status}")
            room_btn.setFixedSize(100, 80)
            room_btn.setStyleSheet(
                f"""
                QPushButton {{
                    background: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 12px;
                }}
                QPushButton:hover {{
                    opacity: 0.8;
                }}
            """
            )
            room_btn.clicked.connect(
                lambda checked, room=room_number: self.show_room_details(room)
            )

            grid_layout.addWidget(room_btn, row, col)
            col += 1
            if col > 3:  # 4 columnas
                col = 0
                row += 1

    def show_room_details(self, room_number):
        """Muestra los detalles de una habitación"""
        QMessageBox.information(
            self,
            "Detalles de Habitación",
            f"Información de la habitación {room_number}",
        )

    def show_new_reservation_dialog(self):
        """Muestra el diálogo para crear una nueva reserva"""
        dialog = NewReservationDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()

    def show_check_in_dialog(self):
        """Muestra el diálogo de check-in"""
        dialog = CheckInDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()

    def show_check_out_dialog(self):
        """Muestra el diálogo de check-out"""
        dialog = CheckOutDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()

    def refresh_data(self):
        """Actualiza los datos del módulo"""
        try:
            # Actualizar datos de habitaciones
            self.rooms_data = self.hospederia_service.get_rooms()

            # Actualizar datos de reservas
            self.reservations_data = self.hospederia_service.get_reservations()

            # Actualizar estadísticas
            self.update_room_statistics()

            # Actualizar tablas
            self.update_reservations_table()

            logger.info("Datos de hospedería actualizados correctamente")

        except Exception as e:
            logger.error(f"Error al actualizar datos de hospedería: {e}")
            QMessageBox.warning(
                self, "Error", "Error al actualizar los datos de hospedería"
            )

    def update_room_statistics(self):
        """Actualiza las estadísticas de habitaciones"""
        if hasattr(self, "available_label"):
            available_count = len(
                [r for r in self.rooms_data if r.get("status") == "available"]
            )
            occupied_count = len(
                [r for r in self.rooms_data if r.get("status") == "occupied"]
            )
            cleaning_count = len(
                [r for r in self.rooms_data if r.get("status") == "cleaning"]
            )

            self.available_label.setText(f"Disponibles: {available_count}")
            self.occupied_label.setText(f"Ocupadas: {occupied_count}")
            self.cleaning_label.setText(f"Limpieza: {cleaning_count}")

    def update_reservations_table(self):
        """Actualiza la tabla de reservas"""
        if hasattr(self, "reservations_table"):
            self.reservations_table.setRowCount(len(self.reservations_data))

            for row, reservation in enumerate(self.reservations_data):
                self.reservations_table.setItem(
                    row, 0, QTableWidgetItem(str(reservation.get("id", "")))
                )
                self.reservations_table.setItem(
                    row, 1, QTableWidgetItem(reservation.get("client_name", ""))
                )
                self.reservations_table.setItem(
                    row, 2, QTableWidgetItem(reservation.get("room_number", ""))
                )
                self.reservations_table.setItem(
                    row, 3, QTableWidgetItem(reservation.get("check_in_date", ""))
                )
                self.reservations_table.setItem(
                    row, 4, QTableWidgetItem(reservation.get("check_out_date", ""))
                )
                self.reservations_table.setItem(
                    row, 5, QTableWidgetItem(reservation.get("status", ""))
                )

    def refresh(self):
        """Actualiza los datos del módulo"""
        logger.info("Actualizando módulo de hospedería...")
        self.refresh_data()
        self.status_changed.emit("Hospedería actualizada")


class NewReservationDialog(QDialog):
    """Diálogo para crear nuevas reservas"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva Reserva")
        self.setFixedSize(400, 350)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        # Campos del formulario
        self.client_name_edit = QLineEdit()
        layout.addRow("Nombre del Cliente:", self.client_name_edit)

        self.client_phone_edit = QLineEdit()
        layout.addRow("Teléfono:", self.client_phone_edit)

        self.room_combo = QComboBox()
        self.room_combo.addItems(
            ["101", "102", "103", "104", "201", "202", "203", "204"]
        )
        layout.addRow("Habitación:", self.room_combo)

        self.check_in_date = QDateEdit(QDate.currentDate())
        layout.addRow("Fecha Check-in:", self.check_in_date)

        self.check_out_date = QDateEdit(QDate.currentDate().addDays(1))
        layout.addRow("Fecha Check-out:", self.check_out_date)

        self.guests_spin = QSpinBox()
        self.guests_spin.setMinimum(1)
        self.guests_spin.setMaximum(4)
        layout.addRow("Número de Huéspedes:", self.guests_spin)

        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        layout.addRow("Notas:", self.notes_edit)

        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)


class CheckInDialog(QDialog):
    """Diálogo para realizar check-in"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Check-in")
        self.setFixedSize(350, 250)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.reservation_combo = QComboBox()
        # Aquí cargarías las reservas pendientes
        layout.addRow("Reserva:", self.reservation_combo)

        self.actual_checkin_date = QDateEdit(QDate.currentDate())
        layout.addRow("Fecha Real Check-in:", self.actual_checkin_date)

        self.payment_method_combo = QComboBox()
        self.payment_method_combo.addItems(["Efectivo", "Tarjeta", "Transferencia"])
        layout.addRow("Método de Pago:", self.payment_method_combo)

        self.deposit_required = QCheckBox("Requiere Depósito")
        layout.addRow(self.deposit_required)

        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)


class CheckOutDialog(QDialog):
    """Diálogo para realizar check-out"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Check-out")
        self.setFixedSize(350, 300)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout(self)

        self.room_combo = QComboBox()
        # Aquí cargarías las habitaciones ocupadas
        layout.addRow("Habitación:", self.room_combo)

        self.actual_checkout_date = QDateEdit(QDate.currentDate())
        layout.addRow("Fecha Real Check-out:", self.actual_checkout_date)

        self.additional_charges_edit = QLineEdit("0.00")
        layout.addRow("Cargos Adicionales:", self.additional_charges_edit)

        self.cleaning_required = QCheckBox("Requiere Limpieza")
        self.cleaning_required.setChecked(True)
        layout.addRow(self.cleaning_required)

        self.damage_check = QCheckBox("Reportar Daños")
        layout.addRow(self.damage_check)

        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        layout.addRow("Notas:", self.notes_edit)

        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
