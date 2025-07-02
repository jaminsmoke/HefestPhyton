"""
Prototipo Pestañas Flotantes: Pestañas Tipo Libreta Flotantes
Pestañas que flotan FUERA del diálogo principal, como en una libreta real
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QTextEdit, QPushButton, QFrame, QStackedWidget
)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPoint
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QLinearGradient, QPolygon


class LibretaTabFlotante(QWidget):
    """Pestaña flotante que simula un separador de libreta física"""

    clicked = pyqtSignal()

    def __init__(self, text: str, color: str, parent=None):
        super().__init__(parent)
        self.tab_text = text
        self.tab_color = QColor(color)
        self.is_active = False
        # Solape visual: la base de la pestaña entra 8px en el header
        self.setFixedSize(96, 42)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)

    def set_active(self, active: bool):
        """Establece si la pestaña está activa"""
        self.is_active = active
        self.update()

    def mousePressEvent(self, event):
        """Maneja el clic en la pestaña"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()

    def paintEvent(self, event):
        """Dibuja la pestaña flotante con integración visual al header (solape y gradiente base)"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width()
        height = self.height()
        # Gradiente base de la pestaña (8px) del color de la pestaña
        base_gradient = QLinearGradient(0, 0, width, 8)
        if self.is_active:
            base_gradient.setColorAt(0, self.tab_color.lighter(120))
            base_gradient.setColorAt(1, self.tab_color)
            gradient = QLinearGradient(0, 8, width, height)
            gradient.setColorAt(0, self.tab_color.lighter(130))
            gradient.setColorAt(0.5, self.tab_color.lighter(110))
            gradient.setColorAt(1, self.tab_color)
            shadow_offset = 3
            shadow_color = QColor(0, 0, 0, 90)
        else:
            base_gradient.setColorAt(0, self.tab_color.darker(110))
            base_gradient.setColorAt(1, self.tab_color.darker(130))
            gradient = QLinearGradient(0, 8, width, height)
            gradient.setColorAt(0, self.tab_color.darker(110))
            gradient.setColorAt(0.5, self.tab_color.darker(120))
            gradient.setColorAt(1, self.tab_color.darker(130))
            shadow_offset = 2
            shadow_color = QColor(0, 0, 0, 60)
        # Sombra difusa solo en la parte inferior y derecha para integración más natural
        shadow_path = QPolygon([
            QPoint(10, height-10),
            QPoint(width-8, height-6),
            QPoint(width-4, 18),
            QPoint(width-1, 8),
            QPoint(width-1, height-1),
            QPoint(8, height-1)
        ])
        shadow_brush = QBrush(QColor(0, 0, 0, 38 if self.is_active else 28))
        painter.setBrush(shadow_brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(shadow_path)
        # Base: color de la pestaña (8px)
        painter.setBrush(QBrush(base_gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, width-shadow_offset, 12, 11, 11)
        # Pestaña principal
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(self.tab_color.darker(150), 2))
        painter.drawRoundedRect(0, 8, width-shadow_offset, height-shadow_offset-8, 11, 13)
        # Efecto de "doblado"
        if self.is_active:
            corner_size = 10
            painter.setBrush(QBrush(self.tab_color.darker(120)))
            points = QPolygon([
                QPoint(width-corner_size-shadow_offset, 8),
                QPoint(width-shadow_offset, 8),
                QPoint(width-shadow_offset, corner_size+8),
                QPoint(width-corner_size-shadow_offset, corner_size+8)
            ])
            painter.drawPolygon(points)
        # Texto
        painter.setPen(QPen(QColor(255, 255, 255) if self.is_active else QColor(220, 220, 220)))
        font = QFont("Segoe UI", 8, QFont.Weight.Bold)
        painter.setFont(font)
        text_rect = QRect(3, 8, width-shadow_offset-6, height-shadow_offset-8)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.tab_text)


class LibretaDialogFlotante(QDialog):
    """Diálogo principal con pestañas flotantes externas"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🍽️ Gestión de Mesa - Pestañas Flotantes")
        # Ajuste: más alto y menos ancho para aspecto atractivo
        self.setFixedSize(420, 600)
        # Fondo estándar sin redondeo
        self.setStyleSheet("QDialog { background: #f8f9fa; }")
        self.tabs_flotantes = []
        self.current_index = 0
        self.setup_ui()
        # Asegura que las pestañas se posicionen correctamente al mostrar el diálogo
        self._pending_show_tabs = True
        self.setup_floating_tabs()

    def setup_ui(self):
        """Configura la interfaz principal (sin sidebar)"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.setup_header(layout)

        # Contenido principal (ocupa toda la ventana)
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background: white;
                border: none;
            }
        """)
        self.setup_pages()
        layout.addWidget(self.stacked_widget, 1)

        # Footer
        self.setup_footer(layout)

    def setup_floating_tabs(self):
        """Configura las pestañas flotantes"""
        tab_configs = [
            ("📋 Info", "#3498db"),
            ("📅 Reserva", "#e74c3c"),
            ("⚙️ Config", "#f39c12"),
            ("📊 Historial", "#9b59b6")
        ]
        tab_spacing = 38  # Más juntas, pero con leve separación visual
        for i, (text, color) in enumerate(tab_configs):
            tab = LibretaTabFlotante(text, color, self)
            tab.clicked.connect(lambda idx=i: self.set_current_tab(idx))
            tab.setParent(None)  # No hereda geometría del diálogo
            tab.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
            tab.show()
            self.tabs_flotantes.append(tab)
        # Activar primera pestaña
        if self.tabs_flotantes:
            self.tabs_flotantes[0].set_active(True)
        self.update_floating_tabs_position(force=True)

    def moveEvent(self, event):
        """Actualiza posición de pestañas cuando se mueve el diálogo"""
        super().moveEvent(event)
        self.update_floating_tabs_position()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_floating_tabs_position()

    def showEvent(self, event):
        super().showEvent(event)
        if getattr(self, '_pending_show_tabs', False):
            self.update_floating_tabs_position(force=True)
            self._pending_show_tabs = False

    def update_floating_tabs_position(self, force=False):
        """Actualiza la posición de las pestañas flotantes para que cuelguen por fuera arriba-izquierda"""
        if not self.tabs_flotantes:
            return
        # Calcula la posición global de la esquina superior izquierda del diálogo
        dialog_pos = self.mapToGlobal(self.rect().topLeft())
        # Ajuste: las pestañas cuelgan por fuera, alineadas arriba izquierda
        tab_offset_x = -90
        tab_offset_y = 52  # Solapa 8px dentro del header
        tab_spacing = 38  # Más juntas
        for i, tab in enumerate(self.tabs_flotantes):
            tab_x = dialog_pos.x() + tab_offset_x
            tab_y = dialog_pos.y() + tab_offset_y + (i * tab_spacing)
            tab.move(tab_x, tab_y)

    def set_current_tab(self, index: int):
        """Cambia a la pestaña especificada"""
        if 0 <= index < len(self.tabs_flotantes):
            # Desactivar pestaña anterior
            if self.current_index < len(self.tabs_flotantes):
                self.tabs_flotantes[self.current_index].set_active(False)

            # Activar nueva pestaña
            self.current_index = index
            self.tabs_flotantes[index].set_active(True)
            self.stacked_widget.setCurrentIndex(index)

    def closeEvent(self, event):
        """Cierra las pestañas flotantes al cerrar el diálogo"""
        for tab in self.tabs_flotantes:
            tab.close()
        super().closeEvent(event)

    def setup_header(self, layout):
        """Header del diálogo"""
        header = QFrame()
        header.setFixedHeight(60)
        # Gradiente igual al de la base de las pestañas, sin redondeo
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
            }
        """)
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(30, 0, 30, 0)
        title = QLabel("Mesa 5 - Terraza")
        title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        status = QLabel("🟢 Disponible")
        status.setFont(QFont("Segoe UI", 14))
        status.setStyleSheet("color: rgba(255,255,255,0.9);")
        header_layout.addWidget(status)
        layout.addWidget(header)

    def setup_pages(self):
        """Configura las páginas de contenido"""
        # Página 1: Info
        info_page = QWidget()
        info_layout = QVBoxLayout(info_page)
        info_layout.setContentsMargins(40, 40, 40, 40)
        info_layout.setSpacing(25)

        title = QLabel("Información de la Mesa")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 15px;")
        info_layout.addWidget(title)

        # Campos más espaciosos
        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Número:"))
        numero_input = QLineEdit("5")
        numero_input.setStyleSheet(self.get_input_style())
        row1.addWidget(numero_input)
        row1.addWidget(QLabel("Zona:"))
        zona_input = QLineEdit("Terraza")
        zona_input.setStyleSheet(self.get_input_style())
        row1.addWidget(zona_input)
        info_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Capacidad:"))
        capacidad_input = QLineEdit("4 personas")
        capacidad_input.setStyleSheet(self.get_input_style())
        row2.addWidget(capacidad_input)
        row2.addStretch()
        info_layout.addLayout(row2)

        info_layout.addWidget(QLabel("Notas:"))
        notas_input = QTextEdit()
        notas_input.setPlaceholderText("Observaciones sobre la mesa...")
        notas_input.setStyleSheet(self.get_input_style())
        notas_input.setMaximumHeight(120)
        info_layout.addWidget(notas_input)

        info_layout.addStretch()
        self.stacked_widget.addWidget(info_page)

        # Página 2: Reserva
        reserva_page = QWidget()
        reserva_layout = QVBoxLayout(reserva_page)
        reserva_layout.setContentsMargins(40, 40, 40, 40)
        reserva_layout.setSpacing(25)

        title = QLabel("Gestión de Reservas")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #e74c3c; margin-bottom: 15px;")
        reserva_layout.addWidget(title)

        reserva_layout.addWidget(QLabel("Cliente:"))
        cliente_input = QLineEdit()
        cliente_input.setPlaceholderText("Nombre del cliente")
        cliente_input.setStyleSheet(self.get_input_style())
        reserva_layout.addWidget(cliente_input)

        datetime_row = QHBoxLayout()
        datetime_row.addWidget(QLabel("Fecha:"))
        fecha_input = QLineEdit("2024-01-15")
        fecha_input.setStyleSheet(self.get_input_style())
        datetime_row.addWidget(fecha_input)
        datetime_row.addWidget(QLabel("Hora:"))
        hora_input = QLineEdit("20:00")
        hora_input.setStyleSheet(self.get_input_style())
        datetime_row.addWidget(hora_input)
        reserva_layout.addLayout(datetime_row)

        reserva_layout.addStretch()
        self.stacked_widget.addWidget(reserva_page)

        # Página 3: Config
        config_page = QWidget()
        config_layout = QVBoxLayout(config_page)
        config_layout.setContentsMargins(40, 40, 40, 40)
        config_layout.setSpacing(25)

        title = QLabel("Configuración Avanzada")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #f39c12; margin-bottom: 15px;")
        config_layout.addWidget(title)

        config_layout.addWidget(QLabel("Configuraciones especiales de la mesa..."))
        config_layout.addStretch()
        self.stacked_widget.addWidget(config_page)

        # Página 4: Historial
        history_page = QWidget()
        history_layout = QVBoxLayout(history_page)
        history_layout.setContentsMargins(40, 40, 40, 40)
        history_layout.setSpacing(25)

        title = QLabel("Historial de Actividad")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #9b59b6; margin-bottom: 15px;")
        history_layout.addWidget(title)

        history_items = [
            "🕐 14:30 - Mesa liberada",
            "🍽️ 12:00 - Pedido completado (€45.50)",
            "👥 11:30 - Mesa ocupada (3 personas)",
            "📅 Ayer - Reserva cancelada"
        ]

        for item in history_items:
            item_label = QLabel(item)
            item_label.setStyleSheet("""
                QLabel {
                    padding: 12px;
                    background: #f8f9fa;
                    border-left: 4px solid #9b59b6;
                    margin: 3px 0;
                    border-radius: 4px;
                }
            """)
            history_layout.addWidget(item_label)

        history_layout.addStretch()
        self.stacked_widget.addWidget(history_page)

    def setup_footer(self, layout):
        """Footer del diálogo"""
        footer = QFrame()
        footer.setFixedHeight(60)
        footer.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
        """)

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(30, 0, 30, 0)

        footer_layout.addStretch()

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet(self.get_button_style("#6c757d"))
        cancel_btn.clicked.connect(self.reject)
        footer_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Guardar")
        save_btn.setStyleSheet(self.get_button_style("#28a745"))
        save_btn.clicked.connect(self.accept)
        footer_layout.addWidget(save_btn)

        layout.addWidget(footer)

    def get_input_style(self):
        """Estilo para campos de entrada"""
        return """
            QLineEdit, QTextEdit {
                border: 2px solid #e9ecef;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #80bdff;
                outline: none;
            }
        """

    def get_button_style(self, color):
        """Estilo para botones"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                min-width: 100px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: {color}dd;
            }}
            QPushButton:pressed {{
                background: {color}bb;
            }}
        """


def main():
    """Función principal"""
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QDialog {
            background: #f8f9fa;
        }
        QLabel {
            color: #495057;
        }
    """)

    dialog = LibretaDialogFlotante()
    dialog.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
