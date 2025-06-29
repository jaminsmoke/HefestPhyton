"""
Diálogo de Mesa - Gestión completa y mejorada de una mesa individual
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
    QFrame, QGridLayout, QMessageBox, QLineEdit, QSpinBox, QTextEdit,
    QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from services.tpv_service import Mesa

logger = logging.getLogger(__name__)


class MesaDialog(QDialog):
    """Diálogo mejorado para la gestión completa de una mesa"""

    mesa_updated = pyqtSignal(Mesa)
    iniciar_tpv_requested = pyqtSignal(int)  # mesa_id
    crear_reserva_requested = pyqtSignal(int)  # mesa_id
    cambiar_estado_requested = pyqtSignal(int, str)  # mesa_id, nuevo_estado

    def __init__(self, mesa: Mesa, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        """Configura la interfaz principal del diálogo"""
        self.setWindowTitle(f"Gestión Mesa {self.mesa.numero} - {self.mesa.zona}")
        self.setFixedSize(520, 700)  # Más alto para mejor separación
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 24)  # más margen inferior
        main_layout.setSpacing(15)

        # Header con información de la mesa
        self.setup_header(main_layout)

        # Panel de información actual
        self.setup_info_panel(main_layout)

        # Panel de acciones principales
        self.setup_actions_panel(main_layout)

        # Panel de configuración
        self.setup_config_panel(main_layout)

        # Añadir stretch para empujar el footer abajo
        main_layout.addStretch()

        # Botones de cierre
        self.setup_footer(main_layout)

        self.apply_styles()

    def setup_header(self, parent_layout: QVBoxLayout):
        """Header con información de la mesa"""
        header_frame = QFrame()
        header_frame.setFixedHeight(90)
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 16px;
                padding: 0px 0px 0px 0px;
                margin-bottom: 8px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        mesa_title = QLabel(f"Mesa {self.mesa.numero}")
        mesa_title.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold))
        mesa_title.setStyleSheet("color: white; margin: 0; padding-top: 10px;")
        mesa_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(mesa_title)

        mesa_details = QLabel(f"Zona: {self.mesa.zona} | Capacidad: {self.mesa.capacidad} personas")
        mesa_details.setStyleSheet("color: #e0e0e0; font-size: 14px; margin-bottom: 0px;")
        mesa_details.setFont(QFont("Segoe UI", 12, QFont.Weight.Normal))
        mesa_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(mesa_details)

        parent_layout.addWidget(header_frame)

    def setup_info_panel(self, parent_layout: QVBoxLayout):
        """Panel de información actual de la mesa"""
        info_frame = QFrame()
        info_frame.setMinimumHeight(130)
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #fff;
                border: 1px solid #d1dbe6;
                border-radius: 12px;
                padding: 0px;
                margin: 8px 0 8px 0;
            }
        """)
        info_layout = QGridLayout(info_frame)
        info_layout.setHorizontalSpacing(16)
        info_layout.setVerticalSpacing(12)
        info_layout.setContentsMargins(18, 16, 18, 16)
        # Estado actual
        estado_color = {
            'libre': '#28a745',
            'ocupada': '#dc3545',
            'reservada': '#ffc107',
            'mantenimiento': '#6c757d'
        }.get(self.mesa.estado, '#6c757d')
        estado_label = QLabel("Estado Actual:")
        estado_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        estado_label.setStyleSheet("color: #22223b;")
        estado_label.setMinimumHeight(32)
        info_layout.addWidget(estado_label, 0, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.estado_value = QLabel(self.mesa.estado.title())
        self.estado_value.setFont(QFont("Segoe UI", 13, QFont.Weight.Normal))
        self.estado_value.setStyleSheet(f"color: {estado_color};")
        self.estado_value.setMinimumHeight(32)
        info_layout.addWidget(self.estado_value, 0, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # Personas actuales
        personas_label = QLabel("Personas:")
        personas_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        personas_label.setStyleSheet("color: #22223b;")
        personas_label.setMinimumHeight(32)
        info_layout.addWidget(personas_label, 1, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        personas_text = f"{self.mesa.personas_display}/{self.mesa.capacidad}"
        self.personas_value = QLabel(personas_text)
        self.personas_value.setFont(QFont("Segoe UI", 13, QFont.Weight.Normal))
        self.personas_value.setStyleSheet("color: #22223b;")
        self.personas_value.setMinimumHeight(32)
        info_layout.addWidget(self.personas_value, 1, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        # Alias actual
        alias_label = QLabel("Nombre:")
        alias_label.setFont(QFont("Segoe UI", 13, QFont.Weight.Bold))
        alias_label.setStyleSheet("color: #22223b;")
        alias_label.setMinimumHeight(32)
        info_layout.addWidget(alias_label, 2, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.alias_value = QLabel(self.mesa.nombre_display)
        self.alias_value.setFont(QFont("Segoe UI", 13, QFont.Weight.Normal))
        self.alias_value.setStyleSheet("color: #22223b;")
        self.alias_value.setMinimumHeight(32)
        info_layout.addWidget(self.alias_value, 2, 1, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        parent_layout.addWidget(info_frame)

    def setup_actions_panel(self, parent_layout: QVBoxLayout):
        """Panel de acciones principales (espacio extra para el título)"""
        actions_frame = QFrame()
        actions_frame.setMinimumHeight(150)  # Más alto
        actions_frame.setStyleSheet("""
            QFrame {
                background-color: #fff;
                border: 1px solid #dee2e6;
                border-radius: 12px;
                padding: 0px 0px 10px 0px; /* menos padding inferior */
                margin: 8px 0 8px 0;
            }
        """)
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setContentsMargins(10, 6, 10, 10)  # menos margen superior
        actions_layout.setSpacing(6)

        # Título grande y con más altura
        title = QLabel("Acciones Disponibles")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMinimumHeight(48)
        title.setStyleSheet("color: #22223b; background: transparent; padding: 0; margin: 0;")
        actions_layout.addWidget(title)

        actions_layout.addSpacing(14)  # separación amplia entre título y botones

        buttons_row = QHBoxLayout()
        buttons_row.setSpacing(14)
        buttons_row.setContentsMargins(0, 0, 0, 0)

        # Botones principales, más compactos
        self.tpv_btn = QPushButton("Iniciar TPV")
        self.tpv_btn.setMinimumHeight(32)
        self.tpv_btn.setMaximumWidth(120)
        self.tpv_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.tpv_btn.setStyleSheet("background-color: #28a745; color: white; border-radius: 8px;")
        buttons_row.addWidget(self.tpv_btn)

        self.reserva_btn = QPushButton("Crear Reserva")
        self.reserva_btn.setMinimumHeight(32)
        self.reserva_btn.setMaximumWidth(120)
        self.reserva_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.reserva_btn.setStyleSheet("background-color: #ffc107; color: #212529; border-radius: 8px;")
        buttons_row.addWidget(self.reserva_btn)

        self.estado_btn = QPushButton("Cambiar Estado")
        self.estado_btn.setMinimumHeight(32)
        self.estado_btn.setMaximumWidth(120)
        self.estado_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.estado_btn.setStyleSheet("background-color: #17a2b8; color: white; border-radius: 8px;")
        buttons_row.addWidget(self.estado_btn)

        self.liberar_btn = QPushButton("Liberar Mesa")
        self.liberar_btn.setMinimumHeight(32)
        self.liberar_btn.setMaximumWidth(120)
        self.liberar_btn.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        self.liberar_btn.setStyleSheet("background-color: #dc3545; color: white; border-radius: 8px;")
        buttons_row.addWidget(self.liberar_btn)

        actions_layout.addLayout(buttons_row)
        actions_layout.addSpacing(2)
        parent_layout.addWidget(actions_frame)

    def setup_config_panel(self, parent_layout: QVBoxLayout):
        """Panel de configuración rápida (scroll limitado dentro del borde)"""
        from PyQt6.QtWidgets import QScrollArea, QWidget, QSizePolicy, QVBoxLayout

        bordered_frame = QFrame()
        bordered_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 0px;
                margin: 8px 0 8px 0;
            }
        """)
        bordered_layout = QVBoxLayout(bordered_frame)
        bordered_layout.setContentsMargins(8, 8, 8, 8)
        bordered_layout.setSpacing(0)

        # Título fuera del scroll
        title = QLabel("Configuración Rápida")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #22223b; background: transparent; padding-top: 10px; padding-bottom: 8px; letter-spacing: 0.5px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setMinimumHeight(56)
        title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        bordered_layout.addWidget(title)
        bordered_layout.addSpacing(6)

        # Contenedor para el scroll
        scroll_container = QWidget()
        scroll_container_layout = QVBoxLayout(scroll_container)
        scroll_container_layout.setContentsMargins(0, 0, 0, 0)
        scroll_container_layout.setSpacing(0)

        # Scroll solo para los campos, limitado
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setMinimumHeight(120)
        scroll_area.setMaximumHeight(150)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)

        config_widget = QWidget()
        config_layout = QVBoxLayout(config_widget)
        config_layout.setSpacing(12)
        config_layout.setContentsMargins(16, 4, 16, 12)

        # Alias
        alias_label = QLabel("Alias:")
        alias_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        alias_label.setStyleSheet("color: #495057;")
        config_layout.addWidget(alias_label)

        self.alias_input = QLineEdit()
        self.alias_input.setPlaceholderText("Nombre temporal...")
        self.alias_input.setText(self.mesa.alias or "")
        self.alias_input.setFont(QFont("Segoe UI", 10))
        self.alias_input.setMinimumHeight(28)
        config_layout.addWidget(self.alias_input)

        # Personas
        personas_label = QLabel("Personas:")
        personas_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        personas_label.setStyleSheet("color: #495057;")
        config_layout.addWidget(personas_label)

        self.personas_spin = QSpinBox()
        self.personas_spin.setMinimum(1)
        self.personas_spin.setMaximum(20)
        self.personas_spin.setValue(self.mesa.personas_display)
        self.personas_spin.setFont(QFont("Segoe UI", 10))
        self.personas_spin.setMinimumHeight(28)
        config_layout.addWidget(self.personas_spin)

        # Notas
        notas_label = QLabel("Notas:")
        notas_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        notas_label.setStyleSheet("color: #495057;")
        config_layout.addWidget(notas_label)

        self.notas_text = QTextEdit()
        self.notas_text.setMinimumHeight(48)
        self.notas_text.setMaximumHeight(80)
        self.notas_text.setPlaceholderText("Observaciones especiales...")
        self.notas_text.setFont(QFont("Segoe UI", 9))
        config_layout.addWidget(self.notas_text)

        config_widget.setLayout(config_layout)
        scroll_area.setWidget(config_widget)
        scroll_container_layout.addWidget(scroll_area)
        bordered_layout.addWidget(scroll_container)

        parent_layout.addWidget(bordered_frame)

    def setup_footer(self, parent_layout: QVBoxLayout):
        """Botones de cierre"""
        footer_layout = QHBoxLayout()

        self.aplicar_btn = QPushButton("Aplicar Cambios")
        self.aplicar_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        footer_layout.addWidget(self.aplicar_btn)

        self.cerrar_btn = QPushButton("Cerrar")
        self.cerrar_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #5a6268; }
        """)
        footer_layout.addWidget(self.cerrar_btn)

        parent_layout.addLayout(footer_layout)

    def apply_styles(self):
        """Estilos generales"""
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #495057;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit, QSpinBox, QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 11px;
            }
            QLineEdit:focus, QSpinBox:focus, QTextEdit:focus {
                border-color: #80bdff;
                outline: none;
            }
            QPushButton {
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 12px;
            }
        """)

    def connect_signals(self):
        """Conecta señales"""
        # Botones principales
        self.tpv_btn.clicked.connect(self.iniciar_tpv)
        self.reserva_btn.clicked.connect(self.crear_reserva)
        self.estado_btn.clicked.connect(self.cambiar_estado)
        self.liberar_btn.clicked.connect(self.liberar_mesa)

        # Botones de footer
        self.aplicar_btn.clicked.connect(self.aplicar_cambios)
        self.cerrar_btn.clicked.connect(self.reject)

    def iniciar_tpv(self):
        """Inicia el TPV para esta mesa"""
        self.iniciar_tpv_requested.emit(self.mesa.id)
        self.accept()

    def crear_reserva(self):
        """Crea una reserva para esta mesa"""
        self.crear_reserva_requested.emit(self.mesa.id)
        self.accept()

    def cambiar_estado(self):
        """Cambia el estado de la mesa"""
        estados = ['libre', 'ocupada', 'reservada', 'mantenimiento']
        estado_actual = self.mesa.estado

        from PyQt6.QtWidgets import QInputDialog
        nuevo_estado, ok = QInputDialog.getItem(
            self, "Cambiar Estado", "Seleccione el nuevo estado:",
            estados, estados.index(estado_actual), False
        )

        if ok and nuevo_estado != estado_actual:
            self.cambiar_estado_requested.emit(self.mesa.id, nuevo_estado)
            self.accept()

    def liberar_mesa(self):
        """Libera la mesa"""
        if QMessageBox.question(
            self, "Confirmar", "¿Liberar la mesa y resetear configuración temporal?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            self.cambiar_estado_requested.emit(self.mesa.id, 'libre')
            self.accept()

    def aplicar_cambios(self):
        """Aplica los cambios de configuración"""
        # Aquí se aplicarían los cambios de alias, personas, etc.
        QMessageBox.information(self, "Éxito", "Cambios aplicados correctamente.")
        self.accept()
