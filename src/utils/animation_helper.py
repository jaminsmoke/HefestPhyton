"""
Hefest - Animation Helper
Clase utilitaria para gestionar animaciones y efectos visuales modernos

Este módulo proporciona funciones para crear animaciones fluidas y efectos
visuales avanzados usando QPropertyAnimation y otros efectos de Qt.
"""

from PyQt6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    QRect,
    QPoint,
    QSequentialAnimationGroup,
)
from PyQt6.QtWidgets import (
    QGraphicsOpacityEffect,
    QGraphicsDropShadowEffect,
    QGraphicsBlurEffect,
)
from PyQt6.QtGui import QColor
import logging

logger = logging.getLogger(__name__)


class AnimationHelper:
    """Helper class para gestionar animaciones y efectos visuales"""

    @staticmethod
    def fade_in(widget, duration=300, start_opacity=0.0, end_opacity=1.0):
        """Animación de fade in"""
        try:
            # Reutilizar efecto si ya existe y es del tipo correcto
            effect = widget.graphicsEffect()
            if not isinstance(effect, QGraphicsOpacityEffect):
                effect = QGraphicsOpacityEffect(
                    widget
                )  # Establecer el widget como padre
                widget.setGraphicsEffect(effect)

            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(start_opacity)
            animation.setEndValue(end_opacity)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start(
                QPropertyAnimation.DeletionPolicy.DeleteWhenStopped
            )  # Política de eliminación

            # Mantener referencia para evitar garbage collection si es necesario,
            # aunque DeleteWhenStopped debería manejarlo.
            # widget._fade_animation = animation
            return animation
        except Exception as e:
            logger.error(f"Error en fade_in para {widget}: {e}")
            return None

    @staticmethod
    def fade_out(widget, duration=300, callback=None):
        """Animación de fade out"""
        try:
            effect = widget.graphicsEffect()
            if not isinstance(effect, QGraphicsOpacityEffect):
                effect = QGraphicsOpacityEffect(
                    widget
                )  # Establecer el widget como padre
                widget.setGraphicsEffect(effect)

            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(duration)
            animation.setStartValue(
                widget.windowOpacity() if effect.opacity() == 1.0 else effect.opacity()
            )  # Usar opacidad actual
            animation.setEndValue(0.0)
            animation.setEasingCurve(QEasingCurve.Type.InCubic)

            if callback:
                animation.finished.connect(callback)

            animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
            # widget._fade_animation = animation
            return animation
        except Exception as e:
            logger.error(f"Error en fade_out para {widget}: {e}")
            return None

    @staticmethod
    def slide_in(widget, direction="left", duration=400, distance=200):
        """Animación de deslizamiento hacia adentro"""
        try:
            current_pos = widget.pos()

            if direction == "left":
                start_pos = QPoint(current_pos.x() - distance, current_pos.y())
            elif direction == "right":
                start_pos = QPoint(current_pos.x() + distance, current_pos.y())
            elif direction == "top":
                start_pos = QPoint(current_pos.x(), current_pos.y() - distance)
            else:  # bottom
                start_pos = QPoint(current_pos.x(), current_pos.y() + distance)

            widget.move(start_pos)

            animation = QPropertyAnimation(widget, b"pos")
            animation.setDuration(duration)
            animation.setStartValue(start_pos)
            animation.setEndValue(current_pos)
            animation.setEasingCurve(QEasingCurve.Type.OutBack)
            animation.start()

            widget._slide_animation = animation
            return animation
        except Exception as e:
            logger.error(f"Error en slide_in: {e}")
            return None

    @staticmethod
    def slide_out(widget, direction="left", duration=400, distance=200, callback=None):
        """Animación de deslizamiento hacia afuera"""
        try:
            current_pos = widget.pos()

            if direction == "left":
                end_pos = QPoint(current_pos.x() - distance, current_pos.y())
            elif direction == "right":
                end_pos = QPoint(current_pos.x() + distance, current_pos.y())
            elif direction == "top":
                end_pos = QPoint(current_pos.x(), current_pos.y() - distance)
            else:  # bottom
                end_pos = QPoint(current_pos.x(), current_pos.y() + distance)

            animation = QPropertyAnimation(widget, b"pos")
            animation.setDuration(duration)
            animation.setStartValue(current_pos)
            animation.setEndValue(end_pos)
            animation.setEasingCurve(QEasingCurve.Type.InBack)

            if callback:
                animation.finished.connect(callback)

            animation.start()
            widget._slide_animation = animation
            return animation
        except Exception as e:
            logger.error(f"Error en slide_out: {e}")
            return None

    @staticmethod
    def scale_animation(widget, start_scale=1.0, end_scale=1.05, duration=200):
        """Animación de escala para efectos hover"""
        try:
            current_geometry = widget.geometry()
            center_x = current_geometry.center().x()
            center_y = current_geometry.center().y()

            width = int(current_geometry.width() * end_scale)
            height = int(current_geometry.height() * end_scale)

            new_x = center_x - width // 2
            new_y = center_y - height // 2

            end_geometry = QRect(new_x, new_y, width, height)

            animation = QPropertyAnimation(widget, b"geometry")
            animation.setDuration(duration)
            animation.setStartValue(current_geometry)
            animation.setEndValue(end_geometry)
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start()

            widget._scale_animation = animation
            return animation
        except Exception as e:
            logger.error(f"Error en scale_animation: {e}")
            return None

    @staticmethod
    def bounce_animation(widget, intensity=10, duration=600):
        """Animación de rebote"""
        try:
            original_pos = widget.pos()

            # Crear grupo de animaciones secuenciales
            group = QSequentialAnimationGroup()

            # Primera fase: subir
            up_animation = QPropertyAnimation(widget, b"pos")
            up_animation.setDuration(duration // 3)
            up_animation.setStartValue(original_pos)
            up_animation.setEndValue(
                QPoint(original_pos.x(), original_pos.y() - intensity)
            )
            up_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

            # Segunda fase: bajar con rebote
            down_animation = QPropertyAnimation(widget, b"pos")
            down_animation.setDuration(duration // 3)
            down_animation.setStartValue(
                QPoint(original_pos.x(), original_pos.y() - intensity)
            )
            down_animation.setEndValue(
                QPoint(original_pos.x(), original_pos.y() + intensity // 2)
            )
            down_animation.setEasingCurve(QEasingCurve.Type.OutBounce)

            # Tercera fase: volver a posición original
            settle_animation = QPropertyAnimation(widget, b"pos")
            settle_animation.setDuration(duration // 3)
            settle_animation.setStartValue(
                QPoint(original_pos.x(), original_pos.y() + intensity // 2)
            )
            settle_animation.setEndValue(original_pos)
            settle_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

            group.addAnimation(up_animation)
            group.addAnimation(down_animation)
            group.addAnimation(settle_animation)
            group.start()

            widget._bounce_animation = group
            return group
        except Exception as e:
            logger.error(f"Error en bounce_animation: {e}")
            return None


class EffectsHelper:
    """Helper class para aplicar efectos gráficos"""

    @staticmethod
    def apply_opacity_effect(widget, opacity=0.5, duration=None):
        """Aplica un efecto de opacidad, opcionalmente animado"""
        try:
            effect = widget.graphicsEffect()
            if not isinstance(effect, QGraphicsOpacityEffect):
                effect = QGraphicsOpacityEffect(widget)
                widget.setGraphicsEffect(effect)

            if duration:
                animation = QPropertyAnimation(effect, b"opacity")
                animation.setDuration(duration)
                animation.setStartValue(effect.opacity())
                animation.setEndValue(opacity)
                animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
                animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
                # widget._opacity_animation = animation
            else:
                effect.setOpacity(opacity)
            return effect
        except Exception as e:
            logger.error(f"Error aplicando efecto de opacidad a {widget}: {e}")
            return None

    @staticmethod
    def apply_drop_shadow(
        widget, blur_radius=15, x_offset=5, y_offset=5, color=QColor(0, 0, 0, 80)
    ):
        """Aplica un efecto de sombra"""
        try:
            # Intentar reutilizar el efecto si ya existe y es del tipo correcto
            existing_effect = widget.graphicsEffect()
            if isinstance(existing_effect, QGraphicsDropShadowEffect):
                shadow_effect = existing_effect
            else:
                shadow_effect = QGraphicsDropShadowEffect(
                    widget
                )  # Establecer el widget como padre
                # Si había otro tipo de efecto, no podemos simplemente reemplazarlo
                # sin considerar si se deben componer. Por ahora, lo reemplazamos.
                widget.setGraphicsEffect(shadow_effect)

            shadow_effect.setBlurRadius(blur_radius)
            shadow_effect.setXOffset(x_offset)
            shadow_effect.setYOffset(y_offset)
            shadow_effect.setColor(color)
            return shadow_effect
        except Exception as e:
            logger.error(f"Error aplicando sombra a {widget}: {e}")
            return None

    @staticmethod
    def apply_blur_effect(widget, blur_radius=5, duration=None):
        """Aplica un efecto de desenfoque, opcionalmente animado"""
        try:
            effect = widget.graphicsEffect()
            if not isinstance(effect, QGraphicsBlurEffect):
                effect = QGraphicsBlurEffect(widget)  # Establecer el widget como padre
                widget.setGraphicsEffect(effect)

            if duration:
                animation = QPropertyAnimation(effect, b"blurRadius")
                animation.setDuration(duration)
                animation.setStartValue(effect.blurRadius())
                animation.setEndValue(blur_radius)
                animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
                animation.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)
                # widget._blur_animation = animation
            else:
                effect.setBlurRadius(blur_radius)
            return effect
        except Exception as e:
            logger.error(f"Error aplicando efecto de desenfoque a {widget}: {e}")
            return None

    @staticmethod
    def apply_acrylic_effect(widget, opacity=0.85, blur_radius=15):
        """Aplica efecto acrílico (glassmorphism)"""
        try:
            # Crear efecto combinado de opacidad y blur
            opacity_effect = QGraphicsOpacityEffect()
            opacity_effect.setOpacity(opacity)

            # Aplicar estilo con fondo semitransparente
            widget.setStyleSheet(
                f"""
                background-color: rgba(255, 255, 255, {int(opacity * 255)});
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                backdrop-filter: blur({blur_radius}px);
            """
            )

            widget.setGraphicsEffect(opacity_effect)
            return opacity_effect
        except Exception as e:
            logger.error(f"Error en apply_acrylic_effect: {e}")
            return None


class TransitionHelper:
    """Helper class para transiciones entre vistas"""

    @staticmethod
    def cross_fade_transition(old_widget, new_widget, duration=500):
        """Transición cruzada entre dos widgets"""
        try:
            # Fade out el widget anterior
            fade_out_anim = AnimationHelper.fade_out(old_widget, duration // 2)

            # Fade in el widget nuevo después de un pequeño delay
            def start_fade_in():
                AnimationHelper.fade_in(new_widget, duration // 2)
                new_widget.show()

            if fade_out_anim:
                fade_out_anim.finished.connect(start_fade_in)
            else:
                start_fade_in()

        except Exception as e:
            logger.error(f"Error en cross_fade_transition: {e}")

    @staticmethod
    def slide_transition(old_widget, new_widget, direction="left", duration=400):
        """Transición deslizante entre dos widgets"""
        try:
            # Deslizar hacia afuera el widget anterior
            slide_out_anim = AnimationHelper.slide_out(
                old_widget, direction, duration, callback=lambda: old_widget.hide()
            )

            # Deslizar hacia adentro el widget nuevo
            opposite_direction = {
                "left": "right",
                "right": "left",
                "top": "bottom",
                "bottom": "top",
            }.get(direction, "right")

            new_widget.show()
            AnimationHelper.slide_in(new_widget, opposite_direction, duration)

        except Exception as e:
            logger.error(f"Error en slide_transition: {e}")
