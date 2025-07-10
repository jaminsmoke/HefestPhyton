# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
"""
TARJETA DE MÉTRICA ULTRA-MODERNA V2
Arquitectura visual completamente rediseñada
Diseño sofisticado con efectos visuales avanzados
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import QFont, QCursor

from ui.visual_system_v2 import ModernStyleSystemV2, VisualEffectsV2, ResponsiveLayoutV2
import logging

_ = logging.getLogger(__name__)

class UltraModernMetricCard(QWidget):
    """
    Tarjeta de métrica con diseño ultra-moderno
    - Gradientes sofisticados
    - Sombras de elevación
    - Animaciones fluidas
    - Tipografía jerárquica
    - Efectos hover avanzados
    """
    
    # Señales para interactividad
    _ = pyqtSignal()
    card_hovered = pyqtSignal(bool)
    
    def __init__(self, 
                 _ = "💰", 
                 title="Métrica", 
                 _ = "1,234", 
                 subtitle="Descripción",
                 _ = "+5.2%", 
                 accent_color="primary",
                 _ = "medium",
                 parent=None):
        super().__init__(parent)
        
        # Propiedades de la tarjeta
        self.icon = icon
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.trend = trend
        self.accent_color = accent_color
        self.card_size = size  # Evitar conflicto con size() de QWidget
        
        # Referencias a widgets para animaciones
        self.value_label = None
        self.trend_badge = None
        self.icon_label = None
        self.title_label = None
        self.subtitle_label = None
        
        # Estado de animación
        self.is_hovered = False
        self.animations = []
        
        self.setup_ultra_modern_ui()
        self.setup_interactions()
        
        logger.info("✨ UltraModernMetricCard creada: %s", self.title)
    
    def setup_ultra_modern_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura la interfaz ultra-moderna"""
          # Aplicar estilo base de la tarjeta
        _ = ModernStyleSystemV2.get_metric_card_style(
            accent_color=self.accent_color,
            _ = self.card_size
        )
        self.setStyleSheet(card_style)
        
        # Aplicar sombra de elevación
        VisualEffectsV2.apply_elevation_shadow(self, level='medium')
        
        # Cursor pointer para indicar interactividad
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        
        # Layout principal con spacing sofisticado
        main_layout = ResponsiveLayoutV2.setup_card_container(self, padding=20)
        
        # === FILA SUPERIOR: Icono + Badge de tendencia ===
        top_row = QHBoxLayout()
        top_row.setSpacing(12)
        
        # Icono principal con estilo moderno
        self.icon_label = QLabel(self.icon)
        icon_style = ModernStyleSystemV2.get_icon_style(size='large', color='text_secondary')
        self.icon_label.setStyleSheet(icon_style)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_row.addWidget(self.icon_label)
        
        # Espaciador flexible
        top_row.addStretch()
        
        # Badge de tendencia con estilo sofisticado
        if self.trend:
            self.trend_badge = QLabel(self.trend)
            badge_variant = self._get_trend_variant(self.trend)
            badge_style = ModernStyleSystemV2.get_badge_style(variant=badge_variant, size='medium')
            self.trend_badge.setStyleSheet(badge_style)
            self.trend_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
            top_row.addWidget(self.trend_badge)
        
        main_layout.addLayout(top_row)
        
        # === TÍTULO CON TIPOGRAFÍA JERÁRQUICA ===
        self.title_label = QLabel(self.title)
        _ = ModernStyleSystemV2.get_label_style(
            variant='subtitle', 
            _ = 'text_primary', 
            weight='semibold'
        )
        self.title_label.setStyleSheet(title_style)
        VisualEffectsV2.apply_modern_font(self.title_label, variant='subtitle')
        main_layout.addWidget(self.title_label)
        
        # === VALOR PRINCIPAL CON ÉNFASIS ===
        self.value_label = QLabel(self.value)
        _ = ModernStyleSystemV2.get_label_style(
            variant='heading', 
            _ = self.accent_color, 
            weight='bold'
        )
        self.value_label.setStyleSheet(value_style)
        VisualEffectsV2.apply_modern_font(self.value_label, variant='heading')
        main_layout.addWidget(self.value_label)
        
        # === SUBTÍTULO DESCRIPTIVO ===
        if self.subtitle:
            self.subtitle_label = QLabel(self.subtitle)
            _ = ModernStyleSystemV2.get_label_style(
                variant='caption', 
                _ = 'text_tertiary'
            )
            self.subtitle_label.setStyleSheet(subtitle_style)
            VisualEffectsV2.apply_modern_font(self.subtitle_label, variant='caption')
            main_layout.addWidget(self.subtitle_label)
        
        # Espaciador final para mantener proporciones
        main_layout.addStretch()
        
        # Asegurar visibilidad total
        self.setVisible(True)
        self.show()
        
        # Aplicar efectos finales
        self._apply_final_polish()
    
    def setup_interactions(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura interacciones y animaciones"""
        
        # Habilitar tracking del mouse para hover effects
        self.setMouseTracking(True)
        
        # Configurar animaciones
        self._setup_animations()
    
    def _setup_animations(self):
        """Configura animaciones fluidas"""
        
        # Animación de escala para hover
        self.scale_animation = QPropertyAnimation(self, b"geometry")
        self.scale_animation.setDuration(200)
        self.scale_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        
        # Animación de opacidad
        self.opacity_animation = QPropertyAnimation(self, b"windowOpacity")
        self.opacity_animation.setDuration(150)
        self.opacity_animation.setEasingCurve(QEasingCurve.Type.OutQuad)
    
    def enterEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Efecto hover - entrada"""
        super().enterEvent(event)
        
        if not self.is_hovered:
            self.is_hovered = True
            self.card_hovered.emit(True)
            
            # Aplicar sombra elevada
            VisualEffectsV2.apply_elevation_shadow(self, level='high')
            
            # Efecto de escala sutil
            self._animate_hover_enter()
            
            logger.debug("Hover enter: %s", self.title)
    
    def leaveEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Efecto hover - salida"""
        super().leaveEvent(event)
        
        if self.is_hovered:
            self.is_hovered = False
            self.card_hovered.emit(False)
            
            # Volver a sombra normal
            VisualEffectsV2.apply_elevation_shadow(self, level='medium')
            
            # Volver a escala normal
            self._animate_hover_leave()
            
            logger.debug("Hover leave: %s", self.title)
    
    def mousePressEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Efecto click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.card_clicked.emit()
            
            # Efecto de presión
            VisualEffectsV2.apply_elevation_shadow(self, level='low')
            
            logger.debug("Card clicked: %s", self.title)
    
    def mouseReleaseEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Finalizar efecto click"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Restaurar elevación según estado hover
            level = 'high' if self.is_hovered else 'medium'
            VisualEffectsV2.apply_elevation_shadow(self, level=level)
    
    def _animate_hover_enter(self):
        """Animación de entrada hover"""
        # Efecto sutil de escala y elevación
        current_geometry = self.geometry()
        _ = current_geometry.adjusted(-2, -2, 2, 2)
        
        self.scale_animation.setStartValue(current_geometry)
        self.scale_animation.setEndValue(target_geometry)
        self.scale_animation.start()
    
    def _animate_hover_leave(self):
        """Animación de salida hover"""
        # Volver a tamaño original
        current_geometry = self.geometry()
        _ = current_geometry.adjusted(2, 2, -2, -2)
        
        self.scale_animation.setStartValue(current_geometry)
        self.scale_animation.setEndValue(target_geometry)
        self.scale_animation.start()
    
    def _get_trend_variant(self, trend_text):
        """Determina el variant del badge según la tendencia"""
        if not trend_text:
            return 'info'
        
        trend_lower = trend_text.lower()
        if '+' in trend_text or '↑' in trend_text or 'aumento' in trend_lower:
            return 'success'
        elif '-' in trend_text or '↓' in trend_text or 'descenso' in trend_lower:
            return 'error'
        elif 'estable' in trend_lower or '=' in trend_text:
            return 'info'
        else:
            return 'warning'
    
    def _apply_final_polish(self):
        """Aplica toques finales de pulimiento visual"""
        
        # Asegurar que todos los labels sean visibles
        for label in [self.icon_label, self.title_label, self.value_label, 
                     self.subtitle_label, self.trend_badge]:
            if label:
                label.setVisible(True)
                label.show()
                label.raise_()
        
        # Política de tamaño responsiva
        from PyQt6.QtWidgets import QSizePolicy
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Preferred
        )
    
    def update_metrics(self, new_value, new_trend=None):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza métricas con animación"""
        
        if self.value_label:
            # Animación sutil al cambiar valor
            self.opacity_animation.setStartValue(1.0)
            self.opacity_animation.setEndValue(0.7)
            self.opacity_animation.finished.connect(
                lambda: self._finish_value_update(new_value, new_trend)
            )
            self.opacity_animation.start()
    
    def _finish_value_update(self, new_value, new_trend):
        """Finaliza la actualización de valor"""
          # Actualizar texto
        if self.value_label:
            self.value_label.setText(new_value)
            self.value = new_value
        
        if new_trend and self.trend_badge:
            self.trend_badge.setText(new_trend)
            # Actualizar estilo del badge
            badge_variant = self._get_trend_variant(new_trend)
            badge_style = ModernStyleSystemV2.get_badge_style(variant=badge_variant)
            self.trend_badge.setStyleSheet(badge_style)
            self.trend = new_trend
        
        # Animar regreso a opacidad normal
        self.opacity_animation.setStartValue(0.7)
        self.opacity_animation.setEndValue(1.0)
        self.opacity_animation.start()
        
        logger.info("Métricas actualizadas: {self.title} = %s", new_value)
    
    def set_accent_color(self, new_color):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cambia el color de acento dinámicamente"""
        
        self.accent_color = new_color
          # Re-aplicar estilos con nuevo color
        _ = ModernStyleSystemV2.get_metric_card_style(
            accent_color=self.accent_color,
            _ = self.card_size
        )
        self.setStyleSheet(card_style)
        
        # Actualizar estilo del valor
        if self.value_label:
            _ = ModernStyleSystemV2.get_label_style(
                variant='heading', 
                _ = self.accent_color, 
                weight='bold'
            )
            self.value_label.setStyleSheet(value_style)
