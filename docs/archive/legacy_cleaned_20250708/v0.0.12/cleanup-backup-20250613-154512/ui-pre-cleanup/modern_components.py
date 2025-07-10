# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
"""
Hefest - Modern UI Components
Widgets personalizados con efectos visuales modernos

Este módulo contiene componentes UI personalizados que implementan
efectos visuales avanzados como glassmorphism, hover effects, etc.
"""

from PyQt6.QtWidgets import (QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QWidget, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtGui import QColor, QFont, QPalette, QPainter, QBrush, QLinearGradient, QPen
from utils.animation_helper import AnimationHelper, EffectsHelper
import logging

_ = logging.getLogger(__name__)

class ModernCard(QFrame):
    """Tarjeta moderna con efectos visuales y animaciones"""
    
    # Señales para notificar cambios en las propiedades
    _ = pyqtSignal(float)
    scaleChanged = pyqtSignal(float)
    
    def __init__(self, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        
        # Configuración visual base
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            ModernCard {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
            }
        """)
        
        # Estado y propiedades de animación
        self._shadow_strength = 4
        self._hover = False
        
        # Aplicar sombra base usando QGraphicsDropShadowEffect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(self._shadow_strength)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.setGraphicsEffect(shadow)
        self._shadow_effect = shadow
    
    def enterEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        self._hover = True
        self._shadow_effect.setBlurRadius(12)
        self._shadow_effect.setColor(QColor(0, 0, 0, 80))
        
    def leaveEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        self._hover = False
        self._shadow_effect.setBlurRadius(4)
        self._shadow_effect.setColor(QColor(0, 0, 0, 50))
    
    def mousePressEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        if event.button() == Qt.MouseButton.LeftButton:
            self._shadow_effect.setBlurRadius(2)
            self._shadow_effect.setColor(QColor(0, 0, 0, 30))
            
    def mouseReleaseEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        if event.button() == Qt.MouseButton.LeftButton:
            if self._hover:
                self._shadow_effect.setBlurRadius(12)
                self._shadow_effect.setColor(QColor(0, 0, 0, 80))
            else:
                self._shadow_effect.setBlurRadius(4)
                self._shadow_effect.setColor(QColor(0, 0, 0, 50))
            
    def paintEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibujar fondo
        painter.setBrush(QColor("white"))
        painter.setPen(QPen(QColor("#e5e7eb"), 1))
        painter.drawRoundedRect(self.rect(), 8, 8)
        painter.end()

class ModernButton(QPushButton):
    """Botón moderno con efectos de hover y animaciones"""
    
    def __init__(self, text="", icon=None, style="primary", parent=None):
        """TODO: Add docstring"""
        super().__init__(text, parent)
        self.style_type = style
        self.setup_style()
        self.is_hovered = False
        
        if icon:
            self.setIcon(icon)
    
    def setup_style(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura el estilo del botón"""
        _ = """
            QPushButton {
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
                min-width: 120px;
            }
        """
        
        if self.style_type == "primary":
            _ = base_style + """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #3b82f6, stop:1 #2563eb);
                    color: white;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #2563eb, stop:1 #1d4ed8);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #1d4ed8, stop:1 #1e40af);
                }
            """
        elif self.style_type == "secondary":
            _ = base_style + """
                QPushButton {
                    background-color: #f3f4f6;
                    color: #374151;
                    border: 1px solid #d1d5db;
                }
                QPushButton:hover {
                    background-color: #e5e7eb;
                    border-color: #9ca3af;
                }
                QPushButton:pressed {
                    background-color: #d1d5db;
                }
            """
        else:  # outline
            _ = base_style + """
                QPushButton {
                    background-color: transparent;
                    color: #3b82f6;
                    border: 2px solid #3b82f6;
                }
                QPushButton:hover {
                    background-color: #3b82f6;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #2563eb;
                    border-color: #2563eb;
                }
            """
        
        self.setStyleSheet(style)
        
        # Aplicar sombra
        EffectsHelper.apply_drop_shadow(
            self, blur_radius=8, y_offset=2, color=QColor(0, 0, 0, 15)
        )
    
    def enterEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Efecto hover"""
        super().enterEvent(event)
        if not self.is_hovered:
            self.is_hovered = True
            # Sombra más pronunciada
            EffectsHelper.apply_drop_shadow(
                self, blur_radius=12, y_offset=4, color=QColor(0, 0, 0, 25)
            )
            # Animación de elevación sutil
            AnimationHelper.scale_animation(self, 1.0, 1.02, 100)
    
    def leaveEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Fin del hover"""
        super().leaveEvent(event)
        if self.is_hovered:
            self.is_hovered = False
            # Volver a sombra normal
            EffectsHelper.apply_drop_shadow(
                self, blur_radius=8, y_offset=2, color=QColor(0, 0, 0, 15)
            )
            # Volver a escala normal
            AnimationHelper.scale_animation(self, 1.02, 1.0, 100)

class GlassPanel(QFrame):
    """Panel simple sin efectos para depuración"""
    
    def __init__(self, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        # No aplicar estilos ni efectos visuales
        # self.setup_style()
        # self.setup_effects()
        self.setStyleSheet("")

class AnimatedSidebar(QFrame):
    """Sidebar con animaciones de entrada y salida"""
    
    def __init__(self, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.is_expanded = True
        self.collapsed_width = 60
        self.expanded_width = 250
        self.setup_ui()
        self.setup_style()
    
    def setup_ui(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura la interfaz del sidebar"""
        self.setFixedWidth(self.expanded_width)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 20, 10, 20)
        self.main_layout.setSpacing(10)
    
    def setup_style(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Configura el estilo del sidebar"""
        self.setStyleSheet("""
            AnimatedSidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f8fafc, stop:1 #f1f5f9);
                border-right: 1px solid #e2e8f0;
            }
        """)
        
        # Aplicar sombra
        EffectsHelper.apply_drop_shadow(
            self, blur_radius=15, x_offset=3, y_offset=0,
            _ = QColor(0, 0, 0, 10)
        )
    
    def toggle_sidebar(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alterna entre expandido y colapsado"""
        _ = self.collapsed_width if self.is_expanded else self.expanded_width
        
        # Animación de ancho
        from PyQt6.QtCore import QPropertyAnimation
        self.width_animation = QPropertyAnimation(self, b"minimumWidth")
        self.width_animation.setDuration(300)
        self.width_animation.setStartValue(self.width())
        self.width_animation.setEndValue(target_width)
        self.width_animation.start()
        
        # También animar el máximo
        self.max_width_animation = QPropertyAnimation(self, b"maximumWidth")
        self.max_width_animation.setDuration(300)
        self.max_width_animation.setStartValue(self.width())
        self.max_width_animation.setEndValue(target_width)
        self.max_width_animation.start()
        
        self.is_expanded = not self.is_expanded

class LoadingSpinner(QWidget):
    """Spinner de carga animado"""
    
    def __init__(self, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.setFixedSize(40, 40)
    
    def start_animation(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicia la animación de rotación"""
        self.timer.start(50)  # 50ms = ~20 FPS
        self.show()
    
    def stop_animation(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Detiene la animación"""
        self.timer.stop()
        self.hide()
    
    def rotate(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Rota el spinner"""
        self.angle = (self.angle + 10) % 360
        self.update()

    def paintEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Dibuja el spinner"""
        if not self.isVisible():
            return
            
        _ = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Centro del widget
            _ = self.width() // 2
            center_y = self.height() // 2
            _ = min(center_x, center_y) - 5
            
            # Configurar el brush con gradiente
            gradient = QLinearGradient(0, 0, self.width(), self.height())
            gradient.setColorAt(0, QColor(59, 130, 246, 255))  # Azul completo
            gradient.setColorAt(0.7, QColor(59, 130, 246, 100))  # Azul semi-transparente
            gradient.setColorAt(1, QColor(59, 130, 246, 0))      # Transparente
            
            painter.setBrush(QBrush(gradient))
            painter.setPen(Qt.PenStyle.NoPen)
            
            # Rotar el painter
            painter.translate(center_x, center_y)
            painter.rotate(self.angle)
            
            # Dibujar arcos
            for i in range(8):
                painter.rotate(45)
                painter.drawEllipse(-2, -radius, 4, radius // 3)
        except Exception as e:
            # Si hay error en el painting, simplemente ignorar
            logger.error("Error en paintEvent de LoadingSpinner: %s", e)
            pass
        finally:
            painter.end()

class StatusIndicator(QWidget):
    """Indicador de estado animado"""
    
    def __init__(self, status="success", parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.status = status
        self.setFixedSize(12, 12)
        self.pulse_timer = QTimer()
        self.pulse_timer.timeout.connect(self.pulse)
        self.opacity = 1.0
        self.pulse_direction = -1
    
    def set_status(self, status):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cambia el estado del indicador"""
        self.status = status
        self.update()
        
        if status == "loading":
            self.start_pulse()
        else:
            self.stop_pulse()
    
    def start_pulse(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicia la animación de pulso"""
        self.pulse_timer.start(50)
    
    def stop_pulse(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Detiene la animación de pulso"""
        self.pulse_timer.stop()
        self.opacity = 1.0
        self.update()
    
    def pulse(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Efecto de pulso"""
        self.opacity += self.pulse_direction * 0.05
        if self.opacity <= 0.3:
            self.pulse_direction = 1
        elif self.opacity >= 1.0:
            self.pulse_direction = -1
        self.update()

    def paintEvent(self, event):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Dibuja el indicador"""
        if not self.isVisible():
            return
            
        _ = QPainter(self)
        try:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Colores según el estado
            _ = {
                "success": QColor(34, 197, 94),    # Verde
                "error": QColor(239, 68, 68),      # Rojo
                "warning": QColor(245, 158, 11),   # Amarillo
                "loading": QColor(59, 130, 246)    # Azul
            }
            
            color = colors.get(self.status, colors["success"])
            color.setAlphaF(self.opacity)
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(1, 1, 10, 10)
        except Exception as e:
            # Si hay error en el painting, simplemente ignorar
            logger.error("Error en paintEvent de StatusIndicator: %s", e)
            pass
        finally:
            painter.end()
