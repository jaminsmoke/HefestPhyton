"""
Dashboard Metric Components - Sistema de Componentes Base para Dashboard

Propósito: Componentes base especializados para visualización de métricas en el Dashboard Admin V3
Ubicación: src/ui/components/dashboard_metric_components.py
Dependencias: PyQt6, logging

CONSOLIDADO: Solo datos reales, sin simulación de datos

Componentes principales:
- UltraModernMetricCard: Tarjeta base de métricas (solo datos reales)
- UltraModernDashboard: Contenedor principal del dashboard
- UltraModernTheme: Sistema de colores y estilos unificados
- UltraModernCard: Componente base para tarjetas reutilizables
- AnimatedProgressBar: Barra de progreso animada

Arquitectura limpia:
- Clase base limpia sin simulación de datos
- Solo muestra datos reales proporcionados externamente
- HospitalityMetricCard extiende esta funcionalidad con auto-gestión
"""

from PyQt6.QtWidgets import (
    QWidget,
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QGraphicsDropShadowEffect,
    QScrollArea,
    QApplication,
)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt6.QtGui import (
    QFont,
    QColor,
    QPainter,
    QLinearGradient,
    QBrush,
)
import logging
from datetime import datetime

# Importar utilidad de compatibilidad CSS
from utils.qt_css_compat import convert_to_qt_compatible_css

logger = logging.getLogger(__name__)


class AnimatedProgressBar(QFrame):
    """Barra de progreso animada con gradientes y efectos modernos"""

    valueChanged = pyqtSignal(float)

    def __init__(self, color="#3B82F6", height=6, parent=None):
        super().__init__(parent)
        self.color = QColor(color)
        self.setFixedHeight(height)
        self._value = 0.0
        self.theme = UltraModernTheme()

        # Configurar animación
        self.animation = QTimer()
        self.animation.timeout.connect(self._animate_step)
        self.animation_duration = 800
        self.animation_steps = 30
        self.animation_current_step = 0
        self.animation_start_value = 0.0
        self.animation_target_value = 0.0

        self.setStyleSheet("background: transparent;")

    def value(self):
        return self._value

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fondo
        bg_color = QColor(self.theme.COLORS["gray_200"])
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(
            0,
            0,
            self.width(),
            self.height(),
            self.theme.RADIUS["sm"],
            self.theme.RADIUS["sm"],
        )
        # Barra de progresso com gradiente
        progress_width = int(self.width() * self._value)
        if progress_width > 0:
            gradient = QLinearGradient(0, 0, progress_width, 0)
            gradient.setColorAt(0, self.color)
            gradient.setColorAt(1, QColor(self.color).lighter(120))

            painter.setBrush(QBrush(gradient))
            painter.drawRoundedRect(
                0,
                0,
                progress_width,
                self.height(),
                self.theme.RADIUS["sm"],
                self.theme.RADIUS["sm"],
            )

    def setValue(self, value, animated=True):
        """Establecer valor con opción de animación"""
        value = max(0.0, min(1.0, value))
        if animated and abs(value - self._value) > 0.01:
            self.animation_start_value = self._value
            self.animation_target_value = value
            self.animation_current_step = 0
            self.animation.start(int(self.animation_duration / self.animation_steps))
        else:
            self._value = value
            self.update()
            self.valueChanged.emit(self._value)

    def _animate_step(self):
        """Paso de animación"""
        if self.animation_current_step >= self.animation_steps:
            self.animation.stop()
            self._value = self.animation_target_value
        else:
            progress = self.animation_current_step / self.animation_steps
            # Easing out cubic
            progress = 1 - pow(1 - progress, 3)
            self._value = (
                self.animation_start_value
                + (self.animation_target_value - self.animation_start_value) * progress
            )
            self.animation_current_step += 1

        self.update()
        self.valueChanged.emit(self._value)


class UltraModernTheme:
    """Tema ultra-moderno con paleta sofisticada y valores de diseño"""

    # === PALETA DE COLORES ULTRA-MODERNA ===
    COLORS = {
        # Colores base
        "white": "#ffffff",
        "black": "#000000",  # Color principal del sistema
        "primary": "#3b82f6",  # Azul principal
        "success": "#22c55e",  # Verde para éxito
        "warning": "#f59e0b",  # Amarillo para advertencias
        "danger": "#ef4444",  # Rojo para errores
        "error": "#ef4444",  # Alias para danger
        "info": "#06b6d4",  # Cyan para información
        # Grises sofisticados
        "gray_50": "#fafafa",
        "gray_100": "#f5f5f5",
        "gray_200": "#e5e5e5",
        "gray_300": "#d4d4d4",
        "gray_400": "#a3a3a3",
        "gray_500": "#737373",
        "gray_600": "#525252",
        "gray_700": "#404040",
        "gray_800": "#262626",
        "gray_900": "#171717",
        # Azules modernos
        "blue_50": "#eff6ff",
        "blue_100": "#dbeafe",
        "blue_200": "#bfdbfe",
        "blue_300": "#93c5fd",
        "blue_400": "#60a5fa",
        "blue_500": "#3b82f6",
        "blue_600": "#2563eb",
        "blue_700": "#1d4ed8",
        "blue_800": "#1e40af",
        "blue_900": "#1e3a8a",
        # Púrpuras elegantes
        "purple_50": "#faf5ff",
        "purple_100": "#f3e8ff",
        "purple_200": "#e9d5ff",
        "purple_300": "#d8b4fe",
        "purple_400": "#c084fc",
        "purple_500": "#a855f7",
        "purple_600": "#9333ea",
        "purple_700": "#7c3aed",
        "purple_800": "#6b21a8",
        "purple_900": "#581c87",
        # Verdes modernos
        "green_50": "#f0fdf4",
        "green_100": "#dcfce7",
        "green_200": "#bbf7d0",
        "green_300": "#86efac",
        "green_400": "#4ade80",
        "green_500": "#22c55e",
        "green_600": "#16a34a",
        "green_700": "#15803d",
        "green_800": "#166534",
        "green_900": "#14532d",
        # Rojos elegantes
        "red_50": "#fef2f2",
        "red_100": "#fee2e2",
        "red_200": "#fecaca",
        "red_300": "#fca5a5",
        "red_400": "#f87171",
        "red_500": "#ef4444",
        "red_600": "#dc2626",
        "red_700": "#b91c1c",
        "red_800": "#991b1b",
        "red_900": "#7f1d1d",
        # Naranjas vibrantes
        "orange_50": "#fff7ed",
        "orange_100": "#ffedd5",
        "orange_200": "#fed7aa",
        "orange_300": "#fdba74",
        "orange_400": "#fb923c",
        "orange_500": "#f97316",
        "orange_600": "#ea580c",
        "orange_700": "#c2410c",
        "orange_800": "#9a3412",
        "orange_900": "#7c2d12",
    }

    # === ESPACIADO Y DIMENSIONES ===
    SPACING = {
        "xs": 4,
        "sm": 8,
        "md": 16,
        "lg": 24,
        "xl": 32,
        "xxl": 48,
        "xxxl": 64,
    }

    # === BORDES Y RADIOS ===
    RADIUS = {
        "none": 0,
        "sm": 4,
        "md": 8,
        "lg": 12,
        "xl": 16,
        "xxl": 24,
        "full": 9999,
    }

    # === TIPOGRAFÍA ===
    TYPOGRAPHY = {
        "font_family": "Segoe UI",
        "font_family_mono": "Consolas",
        # Tamaños
        "text_xs": 10,
        "text_sm": 12,
        "text_base": 14,
        "text_lg": 16,
        "text_xl": 18,
        "text_2xl": 20,
        "text_3xl": 24,
        "text_4xl": 28,
        "text_5xl": 32,
        "text_6xl": 36,
        "text_7xl": 48,
        "text_8xl": 64,
        "text_9xl": 80,
        # Pesos
        "font_thin": QFont.Weight.Thin,
        "font_light": QFont.Weight.Light,
        "font_normal": QFont.Weight.Normal,
        "font_medium": QFont.Weight.Medium,
        "font_semibold": QFont.Weight.DemiBold,
        "font_bold": QFont.Weight.Bold,
        "font_black": QFont.Weight.Black,
    }

    # === SOMBRAS ===
    SHADOWS = {
        "sm": {"blur": 6, "offset": (0, 1), "color": QColor(0, 0, 0, 25)},
        "md": {"blur": 10, "offset": (0, 4), "color": QColor(0, 0, 0, 30)},
        "lg": {"blur": 15, "offset": (0, 10), "color": QColor(0, 0, 0, 35)},
        "xl": {"blur": 25, "offset": (0, 20), "color": QColor(0, 0, 0, 40)},
        "xxl": {"blur": 50, "offset": (0, 25), "color": QColor(0, 0, 0, 45)},
    }


class UltraModernBaseWidget(QFrame):
    """Widget base ultra-moderno con funcionalidades avanzadas"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.theme = UltraModernTheme()
        self.setup_base_properties()
        self.setup_base_styling()

    def setup_base_properties(self):
        """Configurar propiedades base"""
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def setup_base_styling(self):
        """Configurar estilos base"""
        self.setStyleSheet(
            f"""
            UltraModernBaseWidget {{
                background-color: {self.theme.COLORS['white']};
                border: none;
            }}
        """
        )

    def add_shadow(self, level="md"):
        """Añadir sombra al widget"""
        if level in self.theme.SHADOWS:
            shadow_config = self.theme.SHADOWS[level]
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(shadow_config["blur"])
            shadow.setOffset(*shadow_config["offset"])
            shadow.setColor(shadow_config["color"])
            self.setGraphicsEffect(shadow)

    def create_font(self, size_key="text_base", weight_key="font_normal"):
        """Crear fuente con el tema"""
        font = QFont(self.theme.TYPOGRAPHY["font_family"])
        font.setPointSize(self.theme.TYPOGRAPHY[size_key])
        font.setWeight(self.theme.TYPOGRAPHY[weight_key])
        return font


class UltraModernCard(UltraModernBaseWidget):
    """Tarjeta ultra-moderna con efectos avanzados"""

    clicked = pyqtSignal()

    def __init__(self, padding=16, elevation="md", parent=None):
        super().__init__(parent)
        self.padding = padding
        self.elevation = elevation
        self.is_hovered = False
        self.is_pressed = False

        self.setup_card()
        self.setup_animations()

    def setup_card(self):
        """Configurar la tarjeta"""
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(
            self.padding, self.padding, self.padding, self.padding
        )
        self.main_layout.setSpacing(self.theme.SPACING["sm"])

        # Estilos de la tarjeta
        self.setStyleSheet(
            f"""
            UltraModernCard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.theme.COLORS['white']},
                    stop:1 {self.theme.COLORS['gray_50']});
                border: 1px solid {self.theme.COLORS['gray_200']};
                border-radius: {self.theme.RADIUS['xl']}px;
            }}
        """
        )

        # Añadir sombra
        self.add_shadow(self.elevation)

    def setup_animations(self):
        """Configurar animaciones"""
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def add_content(self, widget):
        """Añadir contenido a la tarjeta"""
        self.main_layout.addWidget(widget)


class UltraModernMetricCard(UltraModernCard):
    """Tarjeta de métrica ultra-moderna optimizada para gestión hostelera"""

    clicked = pyqtSignal(dict)  # Señal para clics en la tarjeta

    def __init__(
        self,
        title="Métrica",
        value="0",
        unit="",
        trend="+5.2%",
        metric_type="primary",
        icon="⭐",
        target="100",
        parent=None,
    ):
        super().__init__(padding=20, elevation="md", parent=parent)

        self.title = title
        self.value = value
        self.unit = unit
        self.trend = trend
        self.metric_type = metric_type
        self.icon = icon
        self.target = target
        self.current_numeric_value = self._parse_value(value)

        self.setup_metric_ui()
        self.setup_data_simulation()
        self.setup_interactions()

        # Tamaño mínimo optimizado para mejor visualización - removido setFixedSize
        self.setMinimumSize(280, 180)  # Altura aumentada para mejor visualización

        # Tooltip con información detallada
        self.update_tooltip()

    def _parse_value(self, value_str):
        """Parsear valor string a numérico para cálculos"""
        try:
            # Remover comas, puntos de miles y otros caracteres
            clean_value = str(value_str).replace(",", "").replace(".", "")
            # Buscar números en la cadena
            import re

            numbers = re.findall(r"\d+", clean_value)
            if numbers:
                return float(numbers[0])
            return 0.0
        except:
            return 0.0

    def setup_metric_ui(self):
        """Configurar UI específica de métricas hosteleras"""
        # Limpiar layout
        for i in reversed(range(self.main_layout.count())):
            item = self.main_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if widget:
                    widget.setParent(None)

        # Header: icono, título y tendencia
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        # Título con icono
        self.title_label = QLabel(f"{self.icon} {self.title}")
        title_font = self.create_font("text_sm", "font_medium")
        self.title_label.setFont(title_font)
        title_style = f"""
            QLabel {{
                color: {self.theme.COLORS['gray_700']};
                background: transparent;
                font-weight: 600;
                padding: 2px 0px;
            }}
        """
        self.title_label.setStyleSheet(convert_to_qt_compatible_css(title_style))
        # Indicador de tendencia mejorado
        self.trend_label = QLabel(self.trend)
        trend_font = self.create_font("text_xs", "font_semibold")
        self.trend_label.setFont(trend_font)
        self.trend_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Colores mejorados según tendencia
        if self.trend.startswith("+"):
            trend_color = self.theme.COLORS["green_600"]
            trend_bg = self.theme.COLORS["green_50"]
        elif self.trend.startswith("-"):
            trend_color = self.theme.COLORS["red_600"]
            trend_bg = self.theme.COLORS["red_50"]
        else:
            trend_color = self.theme.COLORS["blue_600"]
            trend_bg = self.theme.COLORS["blue_50"]

        trend_style = f"""
            QLabel {{
                color: {trend_color};
                background-color: {trend_bg};
                border: 1px solid {trend_color}40;
                border-radius: 12px;
                padding: 4px 8px;
                font-weight: 700;
                min-width: 50px;
            }}
        """
        self.trend_label.setStyleSheet(convert_to_qt_compatible_css(trend_style))

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.trend_label)

        # Valor principal
        value_layout = QHBoxLayout()
        value_layout.setContentsMargins(
            0, 8, 0, 6
        )  # Valor principal - OPTIMIZADO para máxima visibilidad
        self.value_label = QLabel(self.value)
        value_font = self.create_font(
            "text_4xl", "font_black"
        )  # Tamaño XL y peso máximo
        self.value_label.setFont(value_font)
        value_style = f"""
            QLabel {{
                color: {self.theme.COLORS['gray_900']};
                background: transparent;
                font-weight: 900;
                padding: 6px 0px;
                line-height: 1.1;
            }}
        """
        self.value_label.setStyleSheet(convert_to_qt_compatible_css(value_style))
        # Unidad con mejor estilo
        self.unit_label = QLabel(self.unit)
        unit_font = self.create_font("text_base", "font_medium")
        self.unit_label.setFont(unit_font)
        unit_style = f"""
            QLabel {{
                color: {self.theme.COLORS['gray_500']};
                background: transparent;
                font-weight: 500;
                padding: 0px 4px;
            }}
        """
        self.unit_label.setStyleSheet(convert_to_qt_compatible_css(unit_style))
        self.unit_label.setAlignment(
            Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignLeft
        )

        value_layout.addWidget(self.value_label)
        if self.unit:
            value_layout.addWidget(self.unit_label)
        value_layout.addStretch()  # Barra de progreso animada con mejor visibilidad
        progress_color = self.get_type_color()
        self.progress_indicator = AnimatedProgressBar(
            color=progress_color, height=10  # Aumentado para mejor visibilidad
        )

        # Calcular progreso vs objetivo
        target_numeric = self._parse_value(self.target)
        progress_value = (
            min(1.0, self.current_numeric_value / target_numeric)
            if target_numeric > 0
            else 0.5
        )
        self.progress_indicator.setValue(progress_value, animated=True)

        # Añadir elementos al layout
        self.main_layout.addLayout(header_layout)
        self.main_layout.addLayout(value_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.progress_indicator)

    def get_type_color(self):
        """Colores semánticos para métricas hosteleras"""
        type_colors = {
            "ocupacion": self.theme.COLORS["primary"],
            "ventas": self.theme.COLORS["success"],
            "costes": self.theme.COLORS["warning"],
            "satisfaccion": self.theme.COLORS["success"],
            "alertas": self.theme.COLORS["error"],
            "reservas": self.theme.COLORS["info"],
            "tiempo": self.theme.COLORS["warning"],
        }
        return type_colors.get(self.metric_type, self.theme.COLORS["primary"])

    def setup_data_simulation(self):
        """DESACTIVADO - Solo datos reales, sin simulación"""
        # Eliminada simulación de datos - Solo usar datos reales del RealDataManager
        # La clase base no debe simular datos, solo mostrar datos reales

    def update_metric_data(
        self, value=None, trend=None, target=None, progress_percentage=None
    ):
        """Actualizar los datos de la métrica con valores reales administrativos"""
        try:
            # Actualizar valor si se proporciona
            if value is not None:
                self.value = str(value)
                self.current_numeric_value = self._parse_value(value)
                self.value_label.setText(str(value))
                # logger.debug(f"📊 Valor actualizado: {value} para {self.title}")

            # Actualizar tendencia si se proporciona
            if trend is not None:
                self.trend = trend
                self.trend_label.setText(trend)

                # Actualizar colores de tendencia con CSS compatible
                if trend.startswith("+"):
                    trend_color = self.theme.COLORS["green_600"]
                    trend_bg = self.theme.COLORS["green_50"]
                elif trend.startswith("-"):
                    trend_color = self.theme.COLORS["red_600"]
                    trend_bg = self.theme.COLORS["red_50"]
                else:
                    trend_color = self.theme.COLORS["blue_600"]
                    trend_bg = self.theme.COLORS["blue_50"]

                trend_style = f"""
                    QLabel {{
                        color: {trend_color};
                        background-color: {trend_bg};
                        border: 1px solid {trend_color}40;
                        border-radius: 12px;
                        padding: 4px 8px;
                        font-weight: 700;
                        min-width: 50px;
                    }}
                """
                self.trend_label.setStyleSheet(
                    convert_to_qt_compatible_css(trend_style)
                )
                # logger.debug(f"📈 Tendencia actualizada: {trend} para {self.title}")

            # Actualizar objetivo si se proporciona
            if target is not None:
                self.target = str(target)

                # Solo recalcular progreso si no se proporciona porcentaje específico
                if progress_percentage is None:
                    target_numeric = self._parse_value(target)
                    progress_value = (
                        min(1.0, self.current_numeric_value / target_numeric)
                        if target_numeric > 0
                        else 0.5
                    )
                    if hasattr(self, "progress_indicator"):
                        self.progress_indicator.setValue(progress_value, animated=True)
                        # logger.debug(
                        #     f"📊 Progreso calculado: {progress_value*100:.1f}% para {self.title}"
                        # )

            # Actualizar progreso con porcentaje específico (datos administrativos reales)
            if progress_percentage is not None and hasattr(self, "progress_indicator"):
                # Convertir porcentaje a decimal si es necesario
                if progress_percentage > 1.0:
                    progress_value = progress_percentage / 100.0
                else:
                    progress_value = progress_percentage

                self.progress_indicator.setValue(progress_value, animated=True)
                # logger.debug(
                #     f"📊 Progreso administrativo real: {progress_percentage:.1f}% para {self.title}"
                # )

            # Actualizar tooltip con los nuevos datos
            self.update_tooltip()

        except Exception as e:
            logger.error(f"Error actualizando datos de métrica '{self.title}': {e}")

    def update_tooltip(self):
        """Actualizar tooltip con información detallada"""
        current_time = datetime.now().strftime("%H:%M:%S")
        target_numeric = self._parse_value(self.target)
        progress_percent = (
            (self.current_numeric_value / target_numeric * 100)
            if target_numeric > 0
            else 0
        )

        tooltip_text = f"""<b>{self.icon} {self.title}</b><br>
<b>Valor actual:</b> {self.value} {self.unit}<br>
<b>Objetivo:</b> {self.target} {self.unit}<br>
<b>Progreso:</b> {progress_percent:.1f}%<br>
<b>Tendencia:</b> {self.trend}<br>
<b>Última actualización:</b> {current_time}"""
        self.setToolTip(tooltip_text)

    def setup_interactions(self):
        """Configurar interacciones de la tarjeta"""
        # Configurar clics y efectos hover
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Configurar menú contextual básico
        self.context_menu = None  # Se puede expandir más tarde

    def mousePressEvent(self, event):
        """Manejar clics en la tarjeta"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Emitir señal con datos de la métrica
            metric_data = {
                "title": self.title,
                "value": self.value,
                "unit": self.unit,
                "trend": self.trend,
                "type": self.metric_type,
                "target": self.target,
            }
            self.clicked.emit(metric_data)
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Efecto al entrar con el ratón"""
        super().enterEvent(event)
        # Efecto de elevación al hacer hover
        self.raise_()
        self.add_shadow("xl")

    def leaveEvent(self, event):
        """Efecto al salir con el ratón"""
        super().leaveEvent(event)
        # Restaurar elevación original
        self.add_shadow(self.elevation)


class UltraModernDashboard(UltraModernBaseWidget):
    """Dashboard ultra-moderno con grid responsivo"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_dashboard()
        self.create_metric_cards()

    def setup_dashboard(self):
        """Configurar estructura del dashboard"""
        # Layout principal con scroll
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(self.theme.SPACING["lg"])

        # Título del dashboard
        title = QLabel("Dashboard Ultra-Moderno V3")
        title_font = self.create_font("text_6xl", "font_bold")
        title.setFont(title_font)
        title.setStyleSheet(
            f"""
            color: {self.theme.COLORS['gray_900']};
            background: transparent;
        """
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Subtítulo
        subtitle = QLabel("Métricas en tiempo real con diseño sofisticado")
        subtitle_font = self.create_font("text_lg", "font_normal")
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet(
            f"""
            color: {self.theme.COLORS['gray_600']};
            background: transparent;
        """
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Área de scroll para las métricas
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameStyle(QFrame.Shape.NoFrame)

        # Widget contenedor para las métricas
        self.metrics_container = QWidget()
        self.metrics_layout = QGridLayout(self.metrics_container)
        self.metrics_layout.setSpacing(self.theme.SPACING["lg"])
        self.metrics_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area.setWidget(self.metrics_container)

        # Añadir elementos
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(scroll_area, 1)  # Expandir

        # Styling del dashboard
        self.setStyleSheet(
            f"""
            UltraModernDashboard {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.theme.COLORS['gray_50']},
                    stop:1 {self.theme.COLORS['white']});            }}
            QScrollArea {{
                background: transparent;
                border: none;
            }}
        """
        )

    def create_metric_cards(self):
        """Crear tarjetas de métricas con datos estáticos de ejemplo (solo para testing del componente)"""
        # NOTA: Datos estáticos para demostración del componente base
        # En producción usar HospitalityMetricCard con datos reales
        metrics_data = [
            {
                "title": "Ventas Totales",
                "value": "15,234",
                "unit": "€",
                "trend": "+12.5%",
                "type": "success",
            },
            {
                "title": "Usuarios Activos",
                "value": "8,932",
                "unit": "",
                "trend": "+8.3%",
                "type": "primary",
            },
            {
                "title": "Conversiones",
                "value": "1,847",
                "unit": "",
                "trend": "-2.1%",
                "type": "warning",
            },
            {
                "title": "Ingresos",
                "value": "94,521",
                "unit": "€",
                "trend": "+15.7%",
                "type": "success",
            },
            {
                "title": "Pedidos",
                "value": "2,341",
                "unit": "",
                "trend": "+5.9%",
                "type": "info",
            },
            {
                "title": "Retorno",
                "value": "23.4",
                "unit": "%",
                "trend": "+3.2%",
                "type": "primary",
            },
        ]

        # Crear tarjetas en grid responsivo
        for i, data in enumerate(metrics_data):
            card = UltraModernMetricCard(
                title=data["title"],
                value=data["value"],
                unit=data["unit"],
                trend=data["trend"],
                metric_type=data["type"],
            )

            row = i // 3  # 3 columnas
            col = i % 3
            self.metrics_layout.addWidget(card, row, col)

            # Conectar evento click
            card.clicked.connect(
                lambda title=data["title"]: self.on_metric_clicked(title)
            )

    def on_metric_clicked(self, title):
        """Manejar click en métrica"""
        logger.info(f"Métrica clickeada: {title}")


# === FUNCIÓN DE PRUEBA ===
def create_ultra_modern_test_window():
    """Crear ventana de prueba del sistema ultra-moderno"""
    app = QApplication.instance() or QApplication([])

    # Ventana principal
    window = QWidget()
    window.setWindowTitle("Hefest - Sistema Ultra-Moderno V3")
    window.setGeometry(100, 100, 1200, 800)

    # Layout principal
    layout = QVBoxLayout(window)
    layout.setContentsMargins(0, 0, 0, 0)

    # Dashboard
    dashboard = UltraModernDashboard()
    layout.addWidget(dashboard)

    return window


if __name__ == "__main__":
    # Test directo
    app = QApplication([])
    window = create_ultra_modern_test_window()
    window.show()
    app.exec()
