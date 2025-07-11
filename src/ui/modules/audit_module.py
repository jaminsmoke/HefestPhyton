"""
Módulo de auditoría para el sistema Hefest.
Muestra los registros de auditoría y permite filtrarlos.
"""

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QMessageBox,
)
from ui.modules.module_base_interface import BaseModule
from services.audit_service import AuditService
from PyQt6.QtCore import Qt
import logging

logger = logging.getLogger(__name__)


class AuditModule(BaseModule):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del módulo de auditoría"""
        # Crear el header del módulo
        header = self.create_module_header()
        self.content_layout.addWidget(header)

        # Inicializar tabla de auditoría
        self.audit_table = QTableWidget()
        self.audit_table.setColumnCount(4)
        self.audit_table.setHorizontalHeaderLabels(
            ["Fecha", "Usuario", "Acción", "Detalles"]
        )
        h_header = self.audit_table.horizontalHeader()
        if h_header:
            h_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Agregar tabla al layout principal
        self.content_layout.addWidget(self.audit_table)

        # Botón de actualizar
        refresh_btn = QPushButton("Actualizar Auditoría")
        refresh_btn.clicked.connect(self.load_audit_logs)
        self.content_layout.addWidget(refresh_btn)

    def load_audit_logs(self):
        """Carga los registros de auditoría en la tabla"""
        try:
            logs = AuditService.get_recent_logs()
            self.audit_table.setRowCount(len(logs))

            for row, log in enumerate(logs):
                self.audit_table.setItem(
                    row,
                    0,
                    QTableWidgetItem(log["timestamp"].strftime("%Y-%m-%d %H:%M:%S")),
                )
                self.audit_table.setItem(row, 1, QTableWidgetItem(log["user"]))
                self.audit_table.setItem(row, 2, QTableWidgetItem(log["action"]))
                self.audit_table.setItem(row, 3, QTableWidgetItem(str(log["details"])))

        except Exception as e:
            logger.error(f"Error al cargar registros de auditoría: {e}")
            QMessageBox.warning(
                self, "Error", "No se pudieron cargar los registros de auditoría"
            )
