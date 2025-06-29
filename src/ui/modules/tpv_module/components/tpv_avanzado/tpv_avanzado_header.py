"""
TPV Avanzado - Header modularizado
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def create_header(parent, parent_layout):
    """Crea el header del TPV avanzado, centrado y con título perfectamente legible y elegante"""
    header = QFrame()
    header.setStyleSheet("""
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            border-top-left-radius: 22px;
            border-top-right-radius: 22px;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
            box-shadow: 0 4px 18px 0 rgba(102,126,234,0.10);
            margin: 0px 0px 12px 0px;
        }
    """)
    header.setFixedHeight(104)

    layout = QVBoxLayout(header)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    layout.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignHCenter)

    # Título destacado con fondo blanco translúcido y texto morado oscuro
    title = QLabel("🍽️ TPV Avanzado")
    title.setFont(QFont("Segoe UI", 25, QFont.Weight.ExtraBold))
    title.setStyleSheet("""
        background: rgba(255,255,255,0.92);
        color: #4B2991;
        border-radius: 20px;
        padding: 0px 38px 0px 38px;
        margin-top: 2px;
        margin-bottom: 2px;
        letter-spacing: 0.5px;
        box-shadow: 0 2px 12px 0 rgba(102,126,234,0.13);
    """)
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    layout.addWidget(title)

    # Información de la mesa, centrada y con mejor contraste
    parent.header_mesa_label = QLabel("Seleccione una mesa")
    if getattr(parent, 'mesa', None):
        parent.header_mesa_label.setText(f"Mesa {parent.mesa.numero} - {parent.mesa.zona}")
    parent.header_mesa_label.setFont(QFont("Segoe UI", 15, QFont.Weight.Medium))
    parent.header_mesa_label.setStyleSheet("color: rgba(255,255,255,0.96); margin-top: 2px; margin-bottom: 10px;")
    parent.header_mesa_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    layout.addWidget(parent.header_mesa_label)

    parent_layout.addWidget(header)
