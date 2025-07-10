from typing import Optional, Dict, List, Any
"""
Integración visual de la agenda de reservas en el TPV
Widget para pestaña de agenda de reservas, usando ReservaService y base de datos principal.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from data.db_manager import DatabaseManager
from src.ui.modules.tpv_module.components.reservas_agenda.reserva_service import (
    ReservaService,
)
from src.ui.modules.tpv_module.components.reservas_agenda.reservas_agenda_view import (
    ReservasAgendaView,
)


class ReservasAgendaTab(QWidget):
    def __init__(self, tpv_service=None, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        _ = QVBoxLayout(self)
        # Usar la base de datos principal
        db_path = (
            DatabaseManager().db_path
            if hasattr(DatabaseManager(), "db_path")
            else "data/hefest.db"
        )
        self.reserva_service = ReservaService(db_path)
        self.agenda_view = ReservasAgendaView(
            self.reserva_service, tpv_service=tpv_service
        )
        layout.addWidget(self.agenda_view)
        # QVBoxLayout ya está asignado en el constructor, no llamar a setLayout(layout)
