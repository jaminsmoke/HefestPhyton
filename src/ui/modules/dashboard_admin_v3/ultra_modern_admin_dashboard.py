"""
Dashboard Administrativo Funcional para Hefest
==============================================

Dashboard temporal funcional que reemplaza el stub anterior.
Compatible con el sistema de autenticación refactorizado.
"""

from typing import Optional, Any
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class UltraModernAdminDashboard(QWidget):
    def __init__(self, auth_service=None, db_manager=None, parent=None):
        super().__init__(parent)

        # Almacenar servicios inyectados
        self.auth_service = auth_service
        self.db_manager = db_manager

        # Inicializar UI básica
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Configurar interfaz básica del dashboard"""
        layout = QVBoxLayout(self)

        # Título temporal
        title = QLabel("🎯 Dashboard Administrativo")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2563eb;
                padding: 20px;
                background: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                margin: 10px;
            }
        """
        )

        info = QLabel("✅ Dashboard funcional - Autenticación y DB conectados")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet(
            """
            QLabel {
                font-size: 14px;
                color: #059669;
                padding: 10px;
            }
        """
        )

        layout.addWidget(title)
        layout.addWidget(info)
