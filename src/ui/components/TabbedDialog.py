from typing import Optional, Dict, List, Any
"""
TabbedDialog - Componente base para diálogos con pestañas horizontales
Proporciona estructura estándar y consistente para diálogos complejos
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QPushButton,
    QFrame,
    QTabWidget,
    QSizePolicy,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont


class TabbedDialog(QDialog):
    """Diálogo base con pestañas horizontales y estructura estándar"""

    # Señales estándar
    _ = pyqtSignal(dict)

    def __init__(self, title: str = "Diálogo", parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.dialog_title = title
        self.tab_pages = {}  # Almacena las páginas por nombre
        self.setup_base_ui()
        self.apply_base_styles()

    def setup_base_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura la estructura base del diálogo"""
        self.setModal(True)
        self.setMinimumSize(520, 600)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        self.header_frame = self.create_header()
        main_layout.addWidget(self.header_frame)

        # Pestañas
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(self.get_tab_styles())
        main_layout.addWidget(self.tab_widget, 1)

        # Footer
        self.footer_frame = self.create_footer()
        main_layout.addWidget(self.footer_frame)

    def create_header(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea el header estándar del diálogo"""
        header = QFrame()
        header.setFixedHeight(80)
        header.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
            }
        """
        )

        layout = QVBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(4)

        # Título principal
        self.title_label = QLabel(self.dialog_title)
        self.title_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: white; background: transparent;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        # Subtítulo (opcional)
        self.subtitle_label = QLabel("")
        self.subtitle_label.setFont(QFont("Segoe UI", 11))
        self.subtitle_label.setStyleSheet(
            "color: rgba(255,255,255,0.9); background: transparent;"
        )
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.subtitle_label)

        return header

    def create_footer(self) -> QFrame:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea el footer estándar con botones"""
        footer = QFrame()
        footer.setFixedHeight(60)
        footer.setStyleSheet(
            """
            QFrame {
                background: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
        """
        )

        layout = QHBoxLayout(footer)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(12)

        layout.addStretch()

        # Botón Cancelar
        self.cancel_btn = QPushButton("Cancelar")
        self.cancel_btn.setMinimumHeight(36)
        self.cancel_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.cancel_btn.setStyleSheet(self.get_button_style("#6c757d"))
        self.cancel_btn.clicked.connect(self.reject)
        layout.addWidget(self.cancel_btn)

        # Botón Aceptar/Guardar
        self.accept_btn = QPushButton("Guardar")
        self.accept_btn.setMinimumHeight(36)
        self.accept_btn.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.accept_btn.setStyleSheet(self.get_button_style("#28a745"))
        self.accept_btn.clicked.connect(self.handle_accept)
        layout.addWidget(self.accept_btn)

        return footer

    def add_tab(self, widget: QWidget, title: str, icon: str = ""):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Añade una pestaña al diálogo"""
        tab_title = f"{icon} {title}" if icon else title
        _ = self.tab_widget.addTab(widget, tab_title)
        self.tab_pages[title] = widget
        return index

    def set_header_title(self, title: str, subtitle: str = ""):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza el título y subtítulo del header"""
        self.title_label.setText(title)
        self.subtitle_label.setText(subtitle)
        self.subtitle_label.setVisible(bool(subtitle))

    def set_accept_button_text(self, text: str):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cambia el texto del botón de aceptar"""
        self.accept_btn.setText(text)

    def handle_accept(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Maneja la aceptación del diálogo - override en subclases"""
        data = self.collect_data()
        if self.validate_data(data):
            self.accepted_with_data.emit(data)
            self.accept()

    def collect_data(self) -> dict:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Recolecta datos de todas las pestañas - override en subclases"""
        return {}

    def validate_data(self, data: dict) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valida los datos antes de aceptar - override en subclases"""
        return True

    def get_tab_styles(self) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para las pestañas"""
        return """
            QTabWidget::pane {
                border: none;
                background: white;
            }
            QTabBar::tab {
                background: #f8f9fa;
                color: #495057;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: 600;
                font-size: 12px;
                min-width: 80px;
            }
            QTabBar::tab:selected {
                background: white;
                color: #495057;
                border-bottom: 3px solid #667eea;
            }
            QTabBar::tab:hover:!selected {
                background: #e9ecef;
                color: #495057;
            }
        """

    def get_button_style(self, color: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Estilos para botones"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: {color}dd;
            }}
            QPushButton:pressed {{
                background: {color}bb;
            }}
        """

    def apply_base_styles(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Aplica estilos base al diálogo"""
        self.setStyleSheet(
            """
            QDialog {
                background: #f8f9fa;
            }
            QLabel {
                color: #495057;
            }
        """
        )
