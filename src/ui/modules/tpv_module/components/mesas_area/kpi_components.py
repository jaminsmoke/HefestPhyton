from typing import Optional, Dict, List, Any
"""
kpi_components.py
Componentes reutilizables para widgets KPI avanzados (tooltips, badges, animaciones, sparkline, accesibilidad, layout)
"""

from PyQt6.QtWidgets import QFrame, QLabel, QWidget
from PyQt6.QtCore import Qt


class TooltipAvanzado(QLabel):
    def __init__(self, text, parent=None):
        """TODO: Add docstring"""
        super().__init__(text, parent)
        self.setObjectName("TooltipAvanzado")
        self.setStyleSheet(
            """
            QLabel#TooltipAvanzado {
                background: rgba(60, 60, 120, 0.92);
                color: #fff;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 13px;
                box-shadow: 0 2px 12px 0 rgba(60,60,120,0.18);
            }
        """
        )
        self.setWordWrap(True)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)


class BadgeKPI(QLabel):
    def __init__(self, text, color="#a21caf", parent=None):
        """TODO: Add docstring"""
        super().__init__(text, parent)
        self.setObjectName("BadgeKPI")
        self.setStyleSheet(
            f"""
            QLabel#BadgeKPI {{
                background: {color};
                color: #fff;
                border-radius: 7px;
                padding: 2px 8px;
                font-size: 11px;
                font-weight: bold;
            }}
        """
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)


# Animación básica de hover y actualización de valor
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve


class AnimacionKPI:
    @staticmethod
    def animar_hover(widget, color_hover="#ede9fe"):
        """TODO: Add docstring"""
        # TODO: Add input validation
        # Cambia el fondo temporalmente al hacer hover
        anim = QPropertyAnimation(widget, b"styleSheet")
        anim.setDuration(180)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        # No cambia realmente el color, placeholder para integración real
        return anim


# SparklineKPI: Placeholder visual (implementación real requiere librería de gráficos)
class SparklineKPI(QLabel):
    def __init__(self, data=None, color="#a21caf", parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self.setObjectName("SparklineKPI")
        self.setText("[sparkline]")  # Placeholder visual
        self.setStyleSheet(f"color: {color}; font-size: 10px; margin: 2px 0;")
        # TODO: Integrar librería de gráficos para sparkline real


# AccesibilidadKPI: utilidades para accesibilidad
class AccesibilidadKPI:
    @staticmethod
    def set_accessible_label(widget, label):
        """TODO: Add docstring"""
        # TODO: Add input validation
        widget.setAccessibleName(label)
        widget.setToolTip(label)


# LayoutKPI: opciones de layout flexibles (placeholder)
class LayoutKPI:
    @staticmethod
    def apply_layout_options(widget, opts):
        """TODO: Add docstring"""
        # TODO: Add input validation
        # opts: dict con opciones de layout (márgenes, alineación, etc.)
        if not opts:
            return
        if "margins" in opts:
            widget.setContentsMargins(*opts["margins"])
        if "alignment" in opts:
            widget.setAlignment(opts["alignment"])
