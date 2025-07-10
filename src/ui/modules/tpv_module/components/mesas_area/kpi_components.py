"""
kpi_components.py
Componentes reutilizables para widgets KPI avanzados
(tooltips, badges, animaciones, sparkline, accesibilidad, layout)
"""

from typing import Any, Dict, Optional

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt
from PyQt6.QtWidgets import QLabel, QWidget


class TooltipAvanzado(QLabel):

    def __init__(self, text: str, parent: Optional[QWidget] = None):
        super().__init__(text, parent)  # type: ignore[misc]
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
        self.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )  # type: ignore[misc]


class BadgeKPI(QLabel):

    def __init__(
        self, text: str, color: str = "#a21caf", parent: Optional[QWidget] = None
    ):
        super().__init__(text, parent)  # type: ignore[misc]
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
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)  # type: ignore[misc]


# Animación básica de hover y actualización de valor


class AnimacionKPI:
    @staticmethod
    def animar_hover(
        widget: QWidget, color_hover: str = "#ede9fe"
    ) -> QPropertyAnimation:
        # Cambia el fondo temporalmente al hacer hover
        anim = QPropertyAnimation(widget, b"styleSheet")  # type: ignore[misc]
        anim.setDuration(180)
        anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        # No cambia realmente el color, placeholder para integración real
        return anim


# SparklineKPI: Placeholder visual (requiere librería de gráficos)
class SparklineKPI(QLabel):

    def __init__(
        self,
        data: Optional[Any] = None,
        color: str = "#a21caf",
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)  # type: ignore[misc]
        self.setObjectName("SparklineKPI")
        self.setText("[sparkline]")  # Placeholder visual
        self.setStyleSheet(f"color: {color}; font-size: 10px; margin: 2px 0;")
        # Pendiente: Integrar librería de gráficos para sparkline real


# AccesibilidadKPI: utilidades para accesibilidad
class AccesibilidadKPI:
    @staticmethod
    def set_accessible_label(widget: QWidget, label: str) -> None:
        widget.setAccessibleName(label)  # type: ignore[misc]
        widget.setToolTip(label)  # type: ignore[misc]


# LayoutKPI: opciones de layout flexibles (placeholder)
class LayoutKPI:
    @staticmethod
    def apply_layout_options(widget: QWidget, opts: Dict[str, Any]) -> None:
        # opts: dict con opciones de layout (márgenes, alineación, etc.)
        if not opts:
            return
        if "margins" in opts:
            widget.setContentsMargins(*opts["margins"])  # type: ignore[misc]
        if "alignment" in opts:
            # Solo QLabel tiene setAlignment, verificar tipo
            if hasattr(widget, "setAlignment"):
                widget.setAlignment(opts["alignment"])  # type: ignore[misc]
