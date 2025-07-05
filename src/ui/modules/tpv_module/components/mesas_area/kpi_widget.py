"""
kpi_widget.py
Widget KPI avanzado reutilizable para TPV y dashboard.
Depende de los componentes de kpi_components.py
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from .kpi_components import TooltipAvanzado, BadgeKPI

class KPIWidget(QFrame):
    def __init__(self, icon, label, value, color, bg_color, tooltip=None, badge=None, trend=None, sparkline=None,
                 on_click=None, accessible_label=None, animation=None, layout_opts=None, parent=None):
        super().__init__(parent)
        self.setObjectName("KPIWidget")
        self.setStyleSheet(f"""
            QFrame#KPIWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {bg_color}, stop:0.5 #f3e8ff, stop:1 #e0e7ff);
                border: 2.5px solid {color};
                border-radius: 18px;
                margin: 4px;
                padding: 8px 6px 10px 6px;
                box-shadow: 0 4px 24px 0 rgba(120, 60, 180, 0.10), 0 1.5px 8px 0 rgba(120, 60, 180, 0.08);
                backdrop-filter: blur(8px);
                background-color: rgba(255,255,255,0.55);
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 10, 8, 8)
        layout.setSpacing(3)
        # Icono
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        icon_label.setStyleSheet("font-size: 38px; margin-bottom: 2px;")
        layout.addWidget(icon_label)
        # Valor y badge
        row = QHBoxLayout()
        value_label = QLabel(str(value))
        value_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #222;")
        row.addWidget(value_label)
        if badge:
            badge_widget = BadgeKPI(badge.get('text', ''), badge.get('color', color))
            row.addWidget(badge_widget)
        row.addStretch(1)
        layout.addLayout(row)
        # Etiqueta
        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-size: 13px; color: #6b21a8; margin-top: 2px;")
        label_widget.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(label_widget)
        # Tooltip avanzado
        if tooltip:
            tooltip_widget = TooltipAvanzado(tooltip) if isinstance(tooltip, str) else tooltip
            label_widget.setToolTip(tooltip_widget.text() if isinstance(tooltip_widget, QLabel) else str(tooltip_widget))
        # TODO: trend, sparkline, accesibilidad, animaciones, callbacks, layout_opts
        # ...
