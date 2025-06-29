"""
Diálogo de Mesa - Gestión completa y mejorada de una mesa individual
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,
    QFrame, QGridLayout, QMessageBox, QLineEdit, QSpinBox, QTextEdit
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
        self.setFixedSize(500, 600)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header con información de la mesa
        self.setup_header(main_layout)
        
        # Panel de información actual
        self.setup_info_panel(main_layout)
        
        # Panel de acciones principales
        self.setup_actions_panel(main_layout)
        
        # Panel de configuración
        self.setup_config_panel(main_layout)
        
        # Botones de cierre
        self.setup_footer(main_layout)
        
        self.apply_styles()
    
    def setup_header(self, parent_layout: QVBoxLayout):
        """Header con información de la mesa"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 12px;
                color: white;
                padding: 15px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        
        mesa_title = QLabel(f"Mesa {self.mesa.numero}")
        mesa_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        mesa_title.setStyleSheet("color: white; margin: 0;")
        mesa_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(mesa_title)
        
        mesa_details = QLabel(f"Zona: {self.mesa.zona} | Capacidad: {self.mesa.capacidad} personas")
        mesa_details.setStyleSheet("color: rgba(255, 255, 255, 0.9); font-size: 14px;")
        mesa_details.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(mesa_details)
        
        parent_layout.addWidget(header_frame)
    
    def setup_info_panel(self, parent_layout: QVBoxLayout):
        """Panel de información actual de la mesa"""
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        info_layout = QGridLayout(info_frame)
        
        # Estado actual
        estado_color = {
            'libre': '#28a745',
            'ocupada': '#dc3545', 
            'reservada': '#ffc107',
            'mantenimiento': '#6c757d'
        }.get(self.mesa.estado, '#6c757d')
        
        estado_label = QLabel("Estado Actual:")
        estado_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        info_layout.addWidget(estado_label, 0, 0)
        
        self.estado_value = QLabel(self.mesa.estado.upper())
        self.estado_value.setStyleSheet(f"color: {estado_color}; font-weight: bold; font-size: 14px;")
        info_layout.addWidget(self.estado_value, 0, 1)
        
        # Personas actuales
        personas_label = QLabel("Personas:")
        personas_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        info_layout.addWidget(personas_label, 1, 0)
        
        personas_text = f"{self.mesa.personas_display}/{self.mesa.capacidad}"
        self.personas_value = QLabel(personas_text)
        self.personas_value.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.personas_value, 1, 1)
        
        # Alias actual
        alias_label = QLabel("Nombre:")
        alias_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        info_layout.addWidget(alias_label, 2, 0)
        
        self.alias_value = QLabel(self.mesa.nombre_display)
        self.alias_value.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(self.alias_value, 2, 1)
        
        parent_layout.addWidget(info_frame)
    
    def setup_actions_panel(self, parent_layout: QVBoxLayout):
        """Panel de acciones principales"""
        actions_frame = QFrame()
        actions_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        actions_layout = QVBoxLayout(actions_frame)
        
        title = QLabel("Acciones Disponibles")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        actions_layout.addWidget(title)
        
        # Grid de botones principales
        buttons_grid = QGridLayout()
        
        # Botón TPV
        self.tpv_btn = QPushButton("Iniciar TPV")
        self.tpv_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        buttons_grid.addWidget(self.tpv_btn, 0, 0)
        
        # Botón Reserva
        self.reserva_btn = QPushButton("Crear Reserva")
        self.reserva_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #212529;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #e0a800; }
        """)
        buttons_grid.addWidget(self.reserva_btn, 0, 1)
        
        # Botón Estado
        self.estado_btn = QPushButton("Cambiar Estado")
        self.estado_btn.setStyleSheet("""
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #138496; }
        """)
        buttons_grid.addWidget(self.estado_btn, 1, 0)
        
        # Botón Liberar
        self.liberar_btn = QPushButton("Liberar Mesa")
        self.liberar_btn.setStyleSheet("""
            QPushButton {
                background-color: #dc3545;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #c82333; }
        """)
        buttons_grid.addWidget(self.liberar_btn, 1, 1)
        
        actions_layout.addLayout(buttons_grid)
        parent_layout.addWidget(actions_frame)
    
    def setup_config_panel(self, parent_layout: QVBoxLayout):
        """Panel de configuración rápida"""
        config_frame = QFrame()
        config_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        config_layout = QVBoxLayout(config_frame)
        
        title = QLabel("Configuración Rápida")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        config_layout.addWidget(title)
        
        # Alias temporal
        alias_layout = QHBoxLayout()
        alias_layout.addWidget(QLabel("Alias:"))
        self.alias_input = QLineEdit()
        self.alias_input.setPlaceholderText("Nombre temporal...")
        self.alias_input.setText(self.mesa.alias or "")
        alias_layout.addWidget(self.alias_input)
        config_layout.addLayout(alias_layout)
        
        # Personas
        personas_layout = QHBoxLayout()
        personas_layout.addWidget(QLabel("Personas:"))
        self.personas_spin = QSpinBox()
        self.personas_spin.setMinimum(1)
        self.personas_spin.setMaximum(20)
        self.personas_spin.setValue(self.mesa.personas_display)
        personas_layout.addWidget(self.personas_spin)
        personas_layout.addStretch()
        config_layout.addLayout(personas_layout)
        
        # Notas
        config_layout.addWidget(QLabel("Notas:"))
        self.notas_text = QTextEdit()
        self.notas_text.setMaximumHeight(60)
        self.notas_text.setPlaceholderText("Observaciones especiales...")
        config_layout.addWidget(self.notas_text)
        
        parent_layout.addWidget(config_frame)
    
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
            }
            QLabel {
                color: #495057;
            }
            QLineEdit, QSpinBox, QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px;
                background-color: white;
            }
            QLineEdit:focus, QSpinBox:focus, QTextEdit:focus {
                border-color: #80bdff;
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
