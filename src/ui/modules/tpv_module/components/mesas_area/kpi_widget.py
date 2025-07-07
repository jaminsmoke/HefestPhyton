"""
EXCEPCIÓN DE TIPADO PyQt6: Este archivo puede contener advertencias de Pyright/Pylance sobre miembros dinámicos, argumentos o retornos de métodos de PyQt6.
Se recomienda usar `Any`, `cast(Any, ...)` y/o `# type: ignore[reportUnknownMemberType,reportUnknownArgumentType,reportUnknownVariableType]` donde sea necesario para evitar falsos positivos.
Cumple con la política de Hefest v0.0.12.
"""
"""
kpi_widget.py
Widget KPI avanzado reutilizable para TPV y dashboard.
Depende de los componentes de kpi_components.py
"""


from typing import Optional, Callable, Dict, Any, Union
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt
from .kpi_components import TooltipAvanzado, BadgeKPI

class KPIWidget(QFrame):
    def __init__(
        self,
        icon: str,
        label: str,
        value: Union[str, int, float],
        color: str,
        bg_color: str,
        tooltip: Optional[Union[str, TooltipAvanzado]] = None,
        badge: Optional[Dict[str, Any]] = None,
        trend: Optional[Any] = None,
        sparkline: Optional[Any] = None,
        on_click: Optional[Callable[..., None]] = None,
        accessible_label: Optional[str] = None,
        animation: Optional[Any] = None,
        layout_opts: Optional[Dict[str, Any]] = None,
        parent: Optional[QWidget] = None
    ) -> None:
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
        from typing import Any
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 10, 8, 8)
        layout.setSpacing(3)
        # Icono
        icon_label: Any = QLabel(icon)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        icon_label.setStyleSheet("font-size: 38px; margin-bottom: 2px;")
        layout.addWidget(icon_label)  # type: ignore[reportUnknownArgumentType]
        # Valor y badge
        row: Any = QHBoxLayout()
        value_label: Any = QLabel(str(value))
        value_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #222;")
        row.addWidget(value_label)  # type: ignore[reportUnknownArgumentType]
        if badge:
            badge_widget: Any = BadgeKPI(badge.get('text', ''), badge.get('color', color))
            row.addWidget(badge_widget)  # type: ignore[reportUnknownArgumentType]
        row.addStretch(1)
        layout.addLayout(row)  # type: ignore[reportUnknownArgumentType]
        # Etiqueta
        class AliasLabel(QLabel):
            def __init__(self, text):
                super().__init__(text)
                self.setStyleSheet("font-size: 12px; color: #6b21a8; margin-top: 2px; padding: 0 4px; max-width: 170px; min-width: 60px; min-height: 18px; max-height: 28px; qproperty-alignment: 'AlignHCenter'; background: transparent; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;")
                self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
                self.setWordWrap(False)
            def resizeEvent(self, event):
                fm = self.fontMetrics()
                if self.height() < 22 or fm.horizontalAdvance(self.text()) > 160:
                    self.setStyleSheet("font-size: 10px; color: #6b21a8; margin-top: 1px; padding: 0 2px; max-width: 170px; min-width: 60px; min-height: 14px; max-height: 22px; qproperty-alignment: 'AlignHCenter'; background: transparent; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;")
                else:
                    self.setStyleSheet("font-size: 12px; color: #6b21a8; margin-top: 2px; padding: 0 4px; max-width: 170px; min-width: 60px; min-height: 18px; max-height: 28px; qproperty-alignment: 'AlignHCenter'; background: transparent; text-overflow: ellipsis; white-space: nowrap; overflow: hidden;")
                super().resizeEvent(event)
        label_widget: Any = AliasLabel(label)
        layout.addWidget(label_widget)  # type: ignore[reportUnknownArgumentType]
        # Tooltip avanzado: aplicar a toda la tarjeta y opcionalmente al label
        if tooltip:
            tooltip_widget: Any = TooltipAvanzado(tooltip) if isinstance(tooltip, str) else tooltip
            tooltip_text = tooltip_widget.text() if tooltip_widget else ""
            self.setToolTip(tooltip_text)
            label_widget.setToolTip(tooltip_text)
        # TODO: trend, sparkline, accesibilidad, animaciones, callbacks, layout_opts
        # ...
