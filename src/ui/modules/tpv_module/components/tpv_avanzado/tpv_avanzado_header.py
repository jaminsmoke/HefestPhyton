"""
TPV Avanzado - Header modularizado
"""

from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def create_header(parent, parent_layout):
    """Crea el header del TPV avanzado"""
    header = QFrame()
    header.setStyleSheet("""
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #667eea, stop:1 #764ba2);
            border-radius: 12px;
            padding: 15px;
            margin: 5px;
        }
    """)
    header.setFixedHeight(80)
    
    layout = QHBoxLayout(header)
    layout.setContentsMargins(20, 10, 20, 10)
    
    # Información de la mesa
    info_layout = QVBoxLayout()
    
    title = QLabel("🍽️ TPV Avanzado")
    title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
    title.setStyleSheet("color: white;")
    info_layout.addWidget(title)
    
    # Label para la mesa (se actualiza dinámicamente)
    parent.header_mesa_label = QLabel("Seleccione una mesa")
    if parent.mesa:
        parent.header_mesa_label.setText(f"Mesa {parent.mesa.numero} - {parent.mesa.zona}")
    parent.header_mesa_label.setFont(QFont("Segoe UI", 12))
    parent.header_mesa_label.setStyleSheet("color: rgba(255, 255, 255, 0.9);")
    info_layout.addWidget(parent.header_mesa_label)
    
    layout.addLayout(info_layout)
    layout.addStretch()
    
    # Botones de acción rápida
    actions_layout = QHBoxLayout()
    
    nuevo_btn = QPushButton("📝 Nuevo")
    nuevo_btn.setStyleSheet("""
        QPushButton {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: bold;
        }
        QPushButton:hover {
            background: rgba(255, 255, 255, 0.3);
        }
    """)
    nuevo_btn.clicked.connect(parent.nuevo_pedido)
    actions_layout.addWidget(nuevo_btn)
    
    layout.addLayout(actions_layout)
    parent_layout.addWidget(header)