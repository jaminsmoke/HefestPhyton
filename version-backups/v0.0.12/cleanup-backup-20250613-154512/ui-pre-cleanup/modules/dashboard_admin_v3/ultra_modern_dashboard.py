"""
DASHBOARD ADMIN V2 - Arquitectura Visual Rediseñada
Sistema completo sin filtros destructivos
Diseño ultra-moderno con tarjetas sofisticadas
"""

import logging
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QGridLayout, QSizePolicy, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QFont

from ui.visual_system_v2 import ModernStyleSystemV2, VisualEffectsV2, ResponsiveLayoutV2
from .ultra_modern_metric_card import UltraModernMetricCard

logger = logging.getLogger(__name__)

class UltraModernMetricsSection(QWidget):
    """Sección de métricas ultra-moderna sin filtros destructivos"""
    
    metrics_updated = pyqtSignal()
    card_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.metric_cards = {}
        self.animation_timer = QTimer()
        
        self.setup_ultra_modern_ui()
        self.setup_data_simulation()
        
        # Asegurar visibilidad total
        self.setVisible(True)
        self.show()
        
        logger.info("✨ UltraModernMetricsSection creada")
    
    def setup_ultra_modern_ui(self):
        """Configura interfaz ultra-moderna"""
        
        # Layout principal con espaciado sofisticado
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 20)
        main_layout.setSpacing(20)
        
        # === CABECERA SOFISTICADA ===
        header_container = self.create_modern_header()
        main_layout.addWidget(header_container)
        
        # === GRID DE MÉTRICAS RESPONSIVE ===
        metrics_container = self.create_metrics_grid()
        main_layout.addWidget(metrics_container, stretch=1)
        
        # Aplicar efectos visuales al contenedor
        self.apply_container_effects()
    
    def create_modern_header(self):
        """Crea cabecera moderna con tipografía sofisticada"""
        
        header = QFrame()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 10)
        header_layout.setSpacing(15)
        
        # Título principal con estilo moderno
        title = QLabel("📊 Métricas Clave")
        title_style = ModernStyleSystemV2.get_label_style(
            variant='title',
            color='text_primary',
            weight='bold'
        )
        title.setStyleSheet(title_style)
        VisualEffectsV2.apply_modern_font(title, variant='title')
        header_layout.addWidget(title)
        
        # Espaciador
        header_layout.addStretch()
        
        # Indicador de estado
        status_label = QLabel("🟢 Datos en vivo")
        status_style = ModernStyleSystemV2.get_label_style(
            variant='caption',
            color='success',
            weight='medium'
        )
        status_label.setStyleSheet(status_style)
        header_layout.addWidget(status_label)
        
        return header
    
    def create_metrics_grid(self):
        """Crea grid responsive de métricas ultra-modernas"""
        
        # Contenedor principal
        container = QFrame()
        container.setObjectName("metrics-container")
        
        # Grid layout responsive
        grid = ResponsiveLayoutV2.setup_metric_grid(container, columns=3, spacing=20)
        
        # Datos de métricas con más variedad y colores
        metrics_data = [
            # Fila 1 - Métricas principales
            {
                'icon': '💰',
                'title': 'Ingresos Diarios',
                'value': '€2,847.50',
                'subtitle': 'Ventas de hoy',
                'trend': '+12.3%',
                'accent': 'success',
                'size': 'medium'
            },
            {
                'icon': '🏨',
                'title': 'Ocupación',
                'value': '18/24',
                'subtitle': 'Mesas ocupadas',
                'trend': '+6 mesas',
                'accent': 'primary',
                'size': 'medium'
            },
            {
                'icon': '⚡',
                'title': 'Tiempo Servicio',
                'value': '11.2 min',
                'subtitle': 'Promedio actual',
                'trend': '-2.3 min',
                'accent': 'accent_teal',
                'size': 'medium'
            },
            
            # Fila 2 - Métricas secundarias
            {
                'icon': '⭐',
                'title': 'Satisfacción',
                'value': '4.8/5',
                'subtitle': 'Rating promedio',
                'trend': '+0.3 pts',
                'accent': 'warning',
                'size': 'medium'
            },
            {
                'icon': '📋',
                'title': 'Órdenes Activas',
                'value': '27',
                'subtitle': 'En preparación',
                'trend': '+8 nuevas',
                'accent': 'accent_purple',
                'size': 'medium'
            },
            {
                'icon': '🎯',
                'title': 'Ticket Promedio',
                'value': '€42.15',
                'subtitle': 'Por cliente',
                'trend': '+€4.80',
                'accent': 'accent_orange',
                'size': 'medium'
            }
        ]
        
        # Crear tarjetas ultra-modernas
        for i, metric_data in enumerate(metrics_data):
            
            # Crear tarjeta ultra-moderna
            card = UltraModernMetricCard(
                icon=metric_data['icon'],
                title=metric_data['title'],
                value=metric_data['value'],
                subtitle=metric_data['subtitle'],
                trend=metric_data['trend'],
                accent_color=metric_data['accent'],
                size=metric_data['size']
            )
            
            # Conectar señales para interactividad
            card.card_clicked.connect(lambda t=metric_data['title']: self.on_card_clicked(t))
            card.card_hovered.connect(lambda hovered, c=card: self.on_card_hovered(c, hovered))
            
            # Posición en grid
            row = i // 3
            col = i % 3
            grid.addWidget(card, row, col)
            
            # Guardar referencia
            card_key = metric_data['title'].lower().replace(' ', '_')
            self.metric_cards[card_key] = card
            
            logger.debug(f"✨ Tarjeta ultra-moderna creada: {metric_data['title']}")
        
        return container
    
    def setup_data_simulation(self):
        """Configura simulación de datos en tiempo real"""
        
        self.animation_timer.timeout.connect(self.simulate_live_updates)
        self.animation_timer.start(8000)  # Actualización cada 8 segundos
    
    def simulate_live_updates(self):
        """Simula actualizaciones de datos en vivo"""
        import random
        
        # Datos realistas para simulación
        updates = {
            'ingresos_diarios': {
                'values': ['€2,650.25', '€2,847.50', '€2,934.75', '€3,125.00'],
                'trends': ['+8.5%', '+12.3%', '+15.7%', '+18.2%']
            },
            'ocupación': {
                'values': ['16/24', '18/24', '20/24', '22/24'],
                'trends': ['+4 mesas', '+6 mesas', '+8 mesas', '+10 mesas']
            },
            'tiempo_servicio': {
                'values': ['12.8 min', '11.2 min', '10.5 min', '9.8 min'],
                'trends': ['-1.2 min', '-2.3 min', '-3.1 min', '-4.0 min']
            },
            'satisfacción': {
                'values': ['4.6/5', '4.8/5', '4.9/5', '5.0/5'],
                'trends': ['+0.1 pts', '+0.3 pts', '+0.4 pts', '+0.5 pts']
            },
            'órdenes_activas': {
                'values': ['23', '27', '31', '35'],
                'trends': ['+5 nuevas', '+8 nuevas', '+12 nuevas', '+16 nuevas']
            },
            'ticket_promedio': {
                'values': ['€38.90', '€42.15', '€45.30', '€48.75'],
                'trends': ['+€2.25', '+€4.80', '+€7.15', '+€9.50']
            }
        }
        
        # Actualizar una tarjeta aleatoria
        card_keys = list(self.metric_cards.keys())
        if card_keys:
            selected_key = random.choice(card_keys)
            card = self.metric_cards[selected_key]
            
            if selected_key in updates:
                data = updates[selected_key]
                new_value = random.choice(data['values'])
                new_trend = random.choice(data['trends'])
                
                # Actualizar con animación
                card.update_metrics(new_value, new_trend)
                
                logger.info(f"🔄 Métrica actualizada: {selected_key} = {new_value}")
        
        self.metrics_updated.emit()
    
    def on_card_clicked(self, title):
        """Maneja click en tarjeta"""
        logger.info(f"🖱️ Tarjeta clickeada: {title}")
        self.card_selected.emit(title)
    
    def on_card_hovered(self, card, is_hovered):
        """Maneja hover en tarjeta con efectos adicionales"""
        if is_hovered:
            # Efecto sutil en tarjetas vecinas
            self.apply_neighbor_dimming(card, True)
        else:
            # Restaurar tarjetas vecinas
            self.apply_neighbor_dimming(card, False)
    
    def apply_neighbor_dimming(self, active_card, dim_others):
        """Aplica efecto de dimming a tarjetas no activas"""
        
        for card in self.metric_cards.values():
            if card != active_card:
                if dim_others:
                    # Efecto sutil de dimming
                    card.setStyleSheet(card.styleSheet() + """
                        QWidget { 
                            background: rgba(248, 250, 252, 0.8);
                        }
                    """)
                else:
                    # Restaurar estilo original
                    # Re-aplicar estilo base
                    card_style = ModernStyleSystemV2.get_metric_card_style(
                        accent_color=card.accent_color,
                        size=card.card_size
                    )
                    card.setStyleSheet(card_style)
    
    def apply_container_effects(self):
        """Aplica efectos visuales al contenedor"""
        
        # Estilo del contenedor principal
        self.setStyleSheet("""
            UltraModernMetricsSection {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #fafbfc, stop:1 #f1f5f9);
                border: none;
                border-radius: 16px;
            }
        """)
        
        # Aplicar sombra sutil al contenedor
        VisualEffectsV2.apply_elevation_shadow(self, level='low')
    
    def get_metrics_summary(self):
        """Obtiene resumen de todas las métricas"""
        
        summary = {}
        for key, card in self.metric_cards.items():
            summary[key] = {
                'title': card.title,
                'value': card.value,
                'trend': card.trend,
                'accent_color': card.accent_color
            }
        
        return summary
    
    def set_theme_colors(self, color_scheme='default'):
        """Cambia esquema de colores de todas las tarjetas"""
        
        color_schemes = {
            'default': ['primary', 'success', 'accent_teal', 'warning', 'accent_purple', 'accent_orange'],
            'professional': ['primary', 'primary_dark', 'text_primary', 'text_secondary', 'primary', 'primary_dark'],
            'vibrant': ['accent_purple', 'accent_teal', 'accent_orange', 'accent_pink', 'success', 'warning'],
            'monochrome': ['text_primary', 'text_secondary', 'text_tertiary', 'text_primary', 'text_secondary', 'text_tertiary']
        }
        
        colors = color_schemes.get(color_scheme, color_schemes['default'])
        
        for i, card in enumerate(self.metric_cards.values()):
            if i < len(colors):
                card.set_accent_color(colors[i])
        
        logger.info(f"🎨 Esquema de colores cambiado a: {color_scheme}")
