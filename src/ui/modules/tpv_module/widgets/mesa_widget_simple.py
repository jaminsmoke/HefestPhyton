"""
Widget MesaWidget - Versión compacta y profesional
Diseño ultra-compacto con máxima legibilidad y organización profesional
Versión: v0.0.12
"""

from PyQt6.QtWidgets import QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from services.tpv_service import Mesa


class MesaWidget(QFrame):
    """Widget compacto y profesional para mostrar una mesa con diseño optimizado"""
    # Señales
    mesa_clicked = pyqtSignal(Mesa)
    mesa_double_clicked = pyqtSignal(Mesa)
    
    def __init__(self, mesa: Mesa, parent=None):
        super().__init__(parent)
        self.mesa = mesa
        self.setFixedSize(220, 160)  # Tamaño más compacto ajustado al contenido
        self.setObjectName("mesa_widget")
        self.setup_ui()
        self.apply_styles()
        
    def setup_ui(self):
        """Configura la interfaz ultra-compacta ajustada al contenido"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)  # Márgenes mínimos
        layout.setSpacing(2)  # Espaciado muy reducido
        
        # NOMBRE DE MESA - Compacto pero prominente
        self.numero_label = QLabel(f"Mesa {self.mesa.numero}")
        self.numero_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.numero_label.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self.numero_label.setObjectName("numero_label")
        layout.addWidget(self.numero_label)        # ESTADO - Badge ultra-compacto centrado sin contenedor extra
        self.estado_label = QLabel(self.get_estado_texto())
        self.estado_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.estado_label.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.estado_label.setObjectName("estado_label")
        self.estado_label.setFixedHeight(22)  # Altura fija para evitar cortes
        layout.addWidget(self.estado_label, 0, Qt.AlignmentFlag.AlignCenter)
        
        layout.addSpacing(4)  # Separador mínimo
        
        # CAPACIDAD - Información compacta
        self.capacidad_label = QLabel(f"👥 {self.mesa.capacidad} personas")
        self.capacidad_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.capacidad_label.setFont(QFont("Segoe UI", 11))
        self.capacidad_label.setObjectName("capacidad_label")
        layout.addWidget(self.capacidad_label)        # ZONA + IDENTIFICADOR - Información contextual en una línea
        zona_texto = self.mesa.zona if hasattr(self.mesa, 'zona') and self.mesa.zona else "Principal"
        
        # El número de mesa ya incluye el identificador correcto (T03, I04, etc.)
        identificador = self.mesa.numero
        
        self.zona_label = QLabel(f"🏢 {zona_texto} • {identificador}")
        self.zona_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zona_label.setFont(QFont("Segoe UI", 9))
        self.zona_label.setObjectName("zona_label")
        layout.addWidget(self.zona_label)
        
        # Sin stretch para mantener contenido compacto
        
    def get_estado_texto(self):
        """Obtiene el texto del estado de forma compacta"""
        estados = {
            'libre': '✓ LIBRE',
            'ocupada': '● OCUPADA',
            'reservada': '◐ RESERVADA',
            'pendiente': '◯ PENDIENTE'
        }
        return estados.get(self.mesa.estado, '? DESCONOCIDO')
        
    def get_colores(self):
        """Obtiene los colores según el estado"""
        colores = {
            'libre': {
                'fondo': '#f1f8e9',
                'borde': '#4caf50',
                'texto': '#2e7d32',
                'badge': '#4caf50'
            },
            'ocupada': {
                'fondo': '#ffebee',
                'borde': '#f44336',
                'texto': '#c62828',
                'badge': '#f44336'
            },
            'reservada': {
                'fondo': '#fff8e1',
                'borde': '#ff9800',
                'texto': '#ef6c00',
                'badge': '#ff9800'
            },
            'pendiente': {
                'fondo': '#f3e5f5',
                'borde': '#9c27b0',
                'texto': '#7b1fa2',
                'badge': '#9c27b0'
            }
        }
        return colores.get(self.mesa.estado, colores['libre'])
        
    def apply_styles(self):
        """Aplica estilos ultra-compactos ajustados al contenido"""
        colores = self.get_colores()
        
        # Estilo principal del widget - Compacto y ajustado
        self.setStyleSheet(f"""
            QFrame#mesa_widget {{
                background-color: {colores['fondo']};
                border: 4px solid {colores['borde']};
                border-radius: 8px;
                margin: 4px;
                padding: 2px;
            }}
            
            QFrame#mesa_widget:hover {{
                border: 5px solid #1976d2;
                background-color: #e3f2fd;
                margin: 3px;
            }}
        """)
        
        # Nombre de mesa - Prominente pero compacto
        self.numero_label.setStyleSheet(f"""
            QLabel#numero_label {{
                color: {colores['texto']};
                font-weight: bold;
                background-color: transparent;
                border: none;
                padding: 1px;
                margin: 0px;
                min-height: 24px;
            }}
        """)        # Estado - Badge ultra-compacto centrado perfectamente
        self.estado_label.setStyleSheet(f"""
            QLabel#estado_label {{
                color: white;
                background-color: {colores['badge']};
                padding: 4px 12px;
                border-radius: 6px;
                font-weight: bold;
                border: 1px solid {self._darken_color(colores['badge'])};
                margin: 2px 20px;
                min-height: 14px;
                max-width: 100px;
            }}
        """)
        
        # Capacidad - Información ajustada
        self.capacidad_label.setStyleSheet(f"""
            QLabel#capacidad_label {{
                color: {colores['texto']};
                font-weight: 500;
                background-color: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 4px;
                padding: 2px 6px;
                min-height: 18px;
                margin: 1px 0px;
            }}
        """)
          # Zona + Identificador - Información contextual compacta
        self.zona_label.setStyleSheet(f"""
            QLabel#zona_label {{
                color: #555555;
                font-weight: 500;
                background-color: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-radius: 4px;
                padding: 2px 8px;
                min-height: 16px;
                margin: 0px;
            }}
        """)
        
    def _darken_color(self, color_hex):
        """Oscurece un color hex para efectos"""
        color_map = {
            '#4caf50': '#388e3c',
            '#f44336': '#d32f2f',
            '#ff9800': '#f57c00',
            '#9c27b0': '#7b1fa2',
        }
        return color_map.get(color_hex, color_hex)
        
    def update_mesa(self, mesa: Mesa):
        """Actualiza los datos de la mesa"""
        self.mesa = mesa
        self.numero_label.setText(f"Mesa {mesa.numero}")
        self.capacidad_label.setText(f"👥 {mesa.capacidad} personas")
        self.estado_label.setText(self.get_estado_texto())
        
        zona_texto = mesa.zona if hasattr(mesa, 'zona') and mesa.zona else "Principal"
        
        # El número de mesa ya incluye el identificador correcto (T03, I04, etc.)
        identificador = mesa.numero
        
        self.zona_label.setText(f"🏢 {zona_texto} • {identificador}")
        
        self.apply_styles()
        
    def mousePressEvent(self, event):
        """Maneja click simple"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mesa_clicked.emit(self.mesa)
        super().mousePressEvent(event)
        
    def mouseDoubleClickEvent(self, event):
        """Maneja doble click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.mesa_double_clicked.emit(self.mesa)
        super().mouseDoubleClickEvent(event)
