"""
Widget de Mesa - Componente visual para representar una mesa individual
"""

import logging
from PyQt6.QtWidgets import (
    QPushButton, QVBoxLayout, QLabel, QWidget, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QFont, QPalette, QColor
from services.tpv_service import Mesa

logger = logging.getLogger(__name__)


class MesaWidget(QPushButton):
    """Widget personalizado para mostrar el estado de una mesa"""

    mesa_clicked = pyqtSignal(Mesa)
    mesa_status_changed = pyqtSignal(Mesa, str)  # mesa, nuevo_estado

    def __init__(self, mesa: Mesa, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self._is_animating = False
        self.setup_ui()
        self.update_appearance()

        # Conectar señal de clic
        self.clicked.connect(self._on_clicked)

    def setup_ui(self):
        """Configura la interfaz del widget de mesa"""
        self.setMinimumSize(120, 100)
        self.setMaximumSize(140, 120)

        # Configurar fuente
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.setFont(font)

        # Texto del botón
        self.update_text()

        # Propiedades para animaciones
        self.setProperty("mesa_id", self.mesa.id)

    def update_text(self):
        """Actualiza el texto mostrado en el widget"""
        text = f"Mesa {self.mesa.numero}\n{self.mesa.zona}"

        # Añadir información adicional según el estado
        if self.mesa.estado == "ocupada":
            # Aquí podríamos mostrar tiempo de ocupación
            text += "\n🕐 Ocupada"
        elif self.mesa.estado == "reservada":
            text += "\n📅 Reservada"
        elif self.mesa.estado == "limpieza":
            text += "\n🧽 Limpieza"
        else:
            text += "\n✅ Libre"

        self.setText(text)

    def update_appearance(self):
        """Actualiza la apariencia visual según el estado de la mesa"""
        if self.mesa.estado == "libre":
            self._set_style_libre()
        elif self.mesa.estado == "ocupada":
            self._set_style_ocupada()
        elif self.mesa.estado == "reservada":
            self._set_style_reservada()
        elif self.mesa.estado == "limpieza":
            self._set_style_limpieza()
        else:
            self._set_style_default()

    def _set_style_libre(self):
        """Estilo para mesa libre"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #48BB78;
                color: white;
                border: 2px solid #38A169;
                border-radius: 8px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #38A169;
                border-color: #2F855A;
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background-color: #2F855A;
            }
        """)

    def _set_style_ocupada(self):
        """Estilo para mesa ocupada"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #F56565;
                color: white;
                border: 2px solid #E53E3E;
                border-radius: 8px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #E53E3E;
                border-color: #C53030;
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background-color: #C53030;
            }
        """)

    def _set_style_reservada(self):
        """Estilo para mesa reservada"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #ED8936;
                color: white;
                border: 2px solid #DD6B20;
                border-radius: 8px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #DD6B20;
                border-color: #C05621;
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background-color: #C05621;
            }
        """)

    def _set_style_limpieza(self):
        """Estilo para mesa en limpieza"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #9F7AEA;
                color: white;
                border: 2px solid #805AD5;
                border-radius: 8px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #805AD5;
                border-color: #6B46C1;
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background-color: #6B46C1;
            }
        """)

    def _set_style_default(self):
        """Estilo por defecto"""
        self.setStyleSheet("""
            QPushButton {
                background-color: #A0AEC0;
                color: white;
                border: 2px solid #718096;
                border-radius: 8px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #718096;
                border-color: #4A5568;
                transform: scale(1.02);
            }
            QPushButton:pressed {
                background-color: #4A5568;
            }
        """)

    def update_mesa(self, nueva_mesa: Mesa):
        """Actualiza los datos de la mesa y refresca la UI"""
        old_estado = self.mesa.estado
        self.mesa = nueva_mesa

        # Actualizar texto y apariencia
        self.update_text()
        self.update_appearance()

        # Emitir señal si cambió el estado
        if old_estado != nueva_mesa.estado:
            self.mesa_status_changed.emit(nueva_mesa, nueva_mesa.estado)
            self._animate_state_change()

    def _animate_state_change(self):
        """Anima el cambio de estado de la mesa"""
        if self._is_animating:
            return

        self._is_animating = True

        # Animación de pulso
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(200)
        self.animation.setEasingCurve(QEasingCurve.Type.OutBounce)

        # Obtener geometría actual
        current_geo = self.geometry()

        # Crear geometría expandida
        expanded_geo = QRect(
            current_geo.x() - 5,
            current_geo.y() - 5,
            current_geo.width() + 10,
            current_geo.height() + 10
        )

        # Configurar animación
        self.animation.setStartValue(current_geo)
        self.animation.setKeyValueAt(0.5, expanded_geo)
        self.animation.setEndValue(current_geo)

        # Conectar fin de animación
        self.animation.finished.connect(self._on_animation_finished)

        # Iniciar animación
        self.animation.start()

    def _on_animation_finished(self):
        """Se ejecuta cuando termina la animación"""
        self._is_animating = False
        if hasattr(self, 'animation'):
            self.animation.deleteLater()

    def _on_clicked(self):
        """Maneja el clic en la mesa"""
        if not self._is_animating:
            self.mesa_clicked.emit(self.mesa)

    def set_highlight(self, highlight: bool):
        """Resalta o desresalta la mesa"""
        if highlight:
            self.setStyleSheet(self.styleSheet() + """
                QPushButton {
                    border: 3px solid #3182CE;
                }
            """)
        else:
            self.update_appearance()

    def is_available(self) -> bool:
        """Retorna True si la mesa está disponible para ser ocupada"""
        return self.mesa.estado in ["libre"]

    def is_busy(self) -> bool:
        """Retorna True si la mesa está ocupada o reservada"""
        return self.mesa.estado in ["ocupada", "reservada"]

    def get_mesa_info(self) -> dict:
        """Retorna información completa de la mesa"""
        return {
            "id": self.mesa.id,
            "numero": self.mesa.numero,
            "zona": self.mesa.zona,
            "estado": self.mesa.estado,
            "capacidad": getattr(self.mesa, 'capacidad', 4),
            "available": self.is_available(),
            "busy": self.is_busy()
        }
