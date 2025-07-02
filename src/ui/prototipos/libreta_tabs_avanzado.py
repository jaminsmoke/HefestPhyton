"""
Prototipo Avanzado: Pestañas Tipo Libreta
Implementación mejorada del patrón visual de separadores de libreta física
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QWidget, 
    QLabel, QLineEdit, QTextEdit, QPushButton, QFrame, QStackedWidget,
    QSpacerItem, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QLinearGradient, QPolygon
from PyQt6.QtCore import QPoint


class LibretaTab(QPushButton):
    """Pestaña personalizada que simula un separador de libreta física"""
    
    def __init__(self, text: str, color: str, parent=None):
        super().__init__(parent)
        self.tab_text = text
        self.tab_color = QColor(color)
        self.is_active = False
        self.setFixedSize(120, 40)
        self.setCheckable(True)
        
    def set_active(self, active: bool):
        """Establece si la pestaña está activa"""
        self.is_active = active
        self.setChecked(active)
        self.update()
        
    def paintEvent(self, event):
        """Dibuja la pestaña con efecto de libreta física"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dimensiones
        width = self.width()
        height = self.height()
        
        # Crear gradiente para efecto 3D
        if self.is_active:
            gradient = QLinearGradient(0, 0, width, 0)
            gradient.setColorAt(0, self.tab_color.lighter(120))
            gradient.setColorAt(0.5, self.tab_color)
            gradient.setColorAt(1, self.tab_color.darker(110))
            
            # Sombra más pronunciada para pestaña activa
            shadow_color = QColor(0, 0, 0, 60)
        else:
            gradient = QLinearGradient(0, 0, width, 0)
            gradient.setColorAt(0, self.tab_color.darker(120))
            gradient.setColorAt(0.5, self.tab_color.darker(110))
            gradient.setColorAt(1, self.tab_color.darker(130))
            
            shadow_color = QColor(0, 0, 0, 30)
        
        # Dibujar sombra
        painter.setBrush(QBrush(shadow_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(2, 2, width-2, height-2, 8, 8)
        
        # Dibujar pestaña principal
        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(self.tab_color.darker(140), 1))
        painter.drawRoundedRect(0, 0, width-2, height-2, 8, 8)
        
        # Efecto de "doblado" en la esquina superior derecha
        if self.is_active:
            corner_size = 8
            painter.setBrush(QBrush(self.tab_color.darker(130)))
            points = QPolygon([
                QPoint(width-corner_size-2, 0),
                QPoint(width-2, 0),
                QPoint(width-2, corner_size),
                QPoint(width-corner_size-2, corner_size)
            ])
            painter.drawPolygon(points)
        
        # Dibujar texto
        painter.setPen(QPen(QColor(255, 255, 255) if self.is_active else QColor(200, 200, 200)))
        font = QFont("Segoe UI", 9, QFont.Weight.Bold)
        painter.setFont(font)
        
        text_rect = QRect(5, 0, width-10, height)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.tab_text)


class LibretaTabWidget(QWidget):
    """Widget contenedor que maneja las pestañas tipo libreta"""
    
    tab_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tabs = []
        self.pages = []
        self.current_index = 0
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz del widget de pestañas"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Panel izquierdo para pestañas
        self.tabs_panel = QWidget()
        self.tabs_panel.setFixedWidth(130)
        self.tabs_panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border-right: 2px solid #dee2e6;
            }
        """)
        
        self.tabs_layout = QVBoxLayout(self.tabs_panel)
        self.tabs_layout.setContentsMargins(5, 10, 5, 10)
        self.tabs_layout.setSpacing(3)
        self.tabs_layout.addStretch()
        
        # Panel derecho para contenido
        self.content_panel = QFrame()
        self.content_panel.setStyleSheet("""
            QFrame {
                background: white;
                border: none;
            }
        """)
        
        self.stacked_widget = QStackedWidget(self.content_panel)
        content_layout = QVBoxLayout(self.content_panel)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.addWidget(self.stacked_widget)
        
        layout.addWidget(self.tabs_panel)
        layout.addWidget(self.content_panel, 1)
        
    def add_tab(self, widget: QWidget, text: str, color: str = "#3498db"):
        """Añade una nueva pestaña"""
        # Crear pestaña
        tab = LibretaTab(text, color)
        tab.clicked.connect(lambda: self.set_current_index(len(self.tabs)))
        
        # Añadir a la lista y layout
        self.tabs.append(tab)
        self.pages.append(widget)
        self.tabs_layout.insertWidget(len(self.tabs)-1, tab)
        self.stacked_widget.addWidget(widget)
        
        # Si es la primera pestaña, activarla
        if len(self.tabs) == 1:
            self.set_current_index(0)
            
    def set_current_index(self, index: int):
        """Cambia a la pestaña especificada"""
        if 0 <= index < len(self.tabs):
            # Desactivar pestaña anterior
            if self.current_index < len(self.tabs):
                self.tabs[self.current_index].set_active(False)
            
            # Activar nueva pestaña
            self.current_index = index
            self.tabs[index].set_active(True)
            self.stacked_widget.setCurrentIndex(index)
            self.tab_changed.emit(index)


class LibretaDialogDemo(QDialog):
    """Diálogo de demostración usando el patrón de pestañas libreta"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🍽️ Gestión de Mesa - Patrón Libreta")
        self.setFixedSize(700, 500)
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header
        self.setup_header(layout)
        
        # Contenido principal con pestañas
        self.tab_widget = LibretaTabWidget()
        self.setup_tabs()
        layout.addWidget(self.tab_widget, 1)
        
        # Footer
        self.setup_footer(layout)
        
    def setup_header(self, layout):
        """Configura el header del diálogo"""
        header = QFrame()
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #667eea, stop:1 #764ba2);
                border: none;
            }
        """)
        
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 0, 20, 0)
        
        title = QLabel("Mesa 5 - Terraza")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: white;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        status = QLabel("🟢 Disponible")
        status.setFont(QFont("Segoe UI", 12))
        status.setStyleSheet("color: rgba(255,255,255,0.9);")
        header_layout.addWidget(status)
        
        layout.addWidget(header)
        
    def setup_tabs(self):
        """Configura las pestañas del diálogo"""
        # Pestaña 1: Información General
        info_page = self.create_info_page()
        self.tab_widget.add_tab(info_page, "📋 Info", "#3498db")
        
        # Pestaña 2: Reservas
        reserva_page = self.create_reserva_page()
        self.tab_widget.add_tab(reserva_page, "📅 Reserva", "#e74c3c")
        
        # Pestaña 3: Configuración
        config_page = self.create_config_page()
        self.tab_widget.add_tab(config_page, "⚙️ Config", "#f39c12")
        
        # Pestaña 4: Historial
        history_page = self.create_history_page()
        self.tab_widget.add_tab(history_page, "📊 Historial", "#9b59b6")
        
    def create_info_page(self):
        """Crea la página de información general"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título de sección
        title = QLabel("Información de la Mesa")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Campos de información
        info_layout = QVBoxLayout()
        info_layout.setSpacing(15)
        
        # Número y zona
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
        
        # Capacidad
        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Capacidad:"))
        capacidad_input = QLineEdit("4 personas")
        capacidad_input.setStyleSheet(self.get_input_style())
        row2.addWidget(capacidad_input)
        row2.addStretch()
        info_layout.addLayout(row2)
        
        # Notas
        layout.addLayout(info_layout)
        layout.addWidget(QLabel("Notas:"))
        notas_input = QTextEdit()
        notas_input.setPlaceholderText("Observaciones sobre la mesa...")
        notas_input.setStyleSheet(self.get_input_style())
        notas_input.setMaximumHeight(100)
        layout.addWidget(notas_input)
        
        layout.addStretch()
        return page
        
    def create_reserva_page(self):
        """Crea la página de reservas"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("Gestión de Reservas")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #e74c3c; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Formulario de reserva
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Cliente
        form_layout.addWidget(QLabel("Cliente:"))
        cliente_input = QLineEdit()
        cliente_input.setPlaceholderText("Nombre del cliente")
        cliente_input.setStyleSheet(self.get_input_style())
        form_layout.addWidget(cliente_input)
        
        # Fecha y hora
        datetime_row = QHBoxLayout()
        datetime_row.addWidget(QLabel("Fecha:"))
        fecha_input = QLineEdit("2024-01-15")
        fecha_input.setStyleSheet(self.get_input_style())
        datetime_row.addWidget(fecha_input)
        datetime_row.addWidget(QLabel("Hora:"))
        hora_input = QLineEdit("20:00")
        hora_input.setStyleSheet(self.get_input_style())
        datetime_row.addWidget(hora_input)
        form_layout.addLayout(datetime_row)
        
        layout.addLayout(form_layout)
        layout.addStretch()
        return page
        
    def create_config_page(self):
        """Crea la página de configuración"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("Configuración Avanzada")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #f39c12; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Opciones de configuración
        config_layout = QVBoxLayout()
        config_layout.setSpacing(15)
        
        config_layout.addWidget(QLabel("Configuraciones especiales de la mesa..."))
        
        layout.addLayout(config_layout)
        layout.addStretch()
        return page
        
    def create_history_page(self):
        """Crea la página de historial"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        title = QLabel("Historial de Actividad")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #9b59b6; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Lista de historial
        history_layout = QVBoxLayout()
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
                    padding: 8px;
                    background: #f8f9fa;
                    border-left: 3px solid #9b59b6;
                    margin: 2px 0;
                }
            """)
            history_layout.addWidget(item_label)
        
        layout.addLayout(history_layout)
        layout.addStretch()
        return page
        
    def setup_footer(self, layout):
        """Configura el footer del diálogo"""
        footer = QFrame()
        footer.setFixedHeight(60)
        footer.setStyleSheet("""
            QFrame {
                background: #f8f9fa;
                border-top: 1px solid #dee2e6;
            }
        """)
        
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(20, 0, 20, 0)
        
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
        """Retorna el estilo para campos de entrada"""
        return """
            QLineEdit, QTextEdit {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
                background: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border-color: #80bdff;
                outline: none;
            }
        """
        
    def get_button_style(self, color):
        """Retorna el estilo para botones"""
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


def main():
    """Función principal para ejecutar el prototipo"""
    app = QApplication(sys.argv)
    
    # Configurar estilo global
    app.setStyleSheet("""
        QDialog {
            background: #f8f9fa;
        }
        QLabel {
            color: #495057;
        }
    """)
    
    dialog = LibretaDialogDemo()
    dialog.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()