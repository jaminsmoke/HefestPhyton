"""
Componente TPVDashboard - Dashboard de métricas del TPV
Versión: v0.0.13
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from services.tpv_service import TPVService

# Unificación widgets KPI: solo se usan KPIWidget y kpi_components
from .mesas_area.kpi_widget import KPIWidget

logger = logging.getLogger(__name__)

def clear_layout(widget):
    """Elimina el layout existente de un widget, si lo tiene, para evitar warnings de layouts duplicados."""
    old_layout = widget.layout() if hasattr(widget, 'layout') else None
    if old_layout is not None:
        while old_layout.count():
            item = old_layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.setParent(None)
        old_layout.deleteLater()

class TPVDashboard(QWidget):
    """Dashboard con métricas del TPV mejorado y dinámico"""

    def __init__(self, tpv_service: Optional[TPVService] = None, parent=None):
        super().__init__(parent)
        self.tpv_service = tpv_service
        self.metric_cards = {}
        self.setup_ui()

        # Timer para actualizar métricas
        self.metrics_timer = QTimer()
        self.metrics_timer.timeout.connect(self.update_metrics)
        self.metrics_timer.start(30000)  # Actualizar cada 30 segundos

        # Actualizar métricas iniciales
        self.update_metrics()

    def setup_ui(self):
        clear_layout(self)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        # Configuración de métricas y tooltips/badges
        metrics_config = [
            {
                "key": "mesas_activas",
                "icon": "🍽️",
                "label": "Mesas Ocupadas",
                "value": "0/0",
                "color": "#2196f3",
                "bg_color": "#e0f2fe",
                "tooltip": "Cantidad de mesas ocupadas respecto al total.",
                "badge": {"text": "M", "color": "#2196f3"}
            },
            {
                "key": "ventas_dia",
                "icon": "💰",
                "label": "Ventas Hoy",
                "value": "€0.00",
                "color": "#4caf50",
                "bg_color": "#e8f5e9",
                "tooltip": "Total de ventas del día en curso.",
                "badge": {"text": "$", "color": "#4caf50"}
            },
            {
                "key": "comandas_activas",
                "icon": "📝",
                "label": "Comandas Activas",
                "value": "0",
                "color": "#ff9800",
                "bg_color": "#fff3e0",
                "tooltip": "Número de comandas abiertas actualmente.",
                "badge": {"text": "C", "color": "#ff9800"}
            },
            {
                "key": "tiempo_promedio",
                "icon": "⏱️",
                "label": "Tiempo Prom.",
                "value": "0min",
                "color": "#9c27b0",
                "bg_color": "#f3e8ff",
                "tooltip": "Tiempo promedio de ocupación de mesa.",
                "badge": {"text": "T", "color": "#9c27b0"}
            }
        ]

        for metric in metrics_config:
            metric_widget = KPIWidget(
                icon=str(metric["icon"]),
                label=str(metric["label"]),
                value=str(metric["value"]),
                color=str(metric["color"]),
                bg_color=str(metric["bg_color"]),
                tooltip=str(metric["tooltip"]),
                badge=metric["badge"]
            )
            self.metric_cards[metric["key"]] = metric_widget
            layout.addWidget(metric_widget)

        layout.addStretch()

    # Eliminada función create_metric_card: solo se usa KPIWidget

    def update_metrics(self):
        """Actualiza las métricas en tiempo real con datos del servicio"""
        try:
            # Valores por defecto (estado inicial/sin datos)
            mesas_ocupadas = 0
            total_mesas = 0
            total_comandas = 0
            ventas_dia = 0.0
            tiempo_promedio = "0min"

            # Si hay servicio TPV, obtener datos reales
            if self.tpv_service:
                try:
                    # Obtener datos actuales
                    mesas = self.tpv_service.get_mesas()
                    comandas_activas = self.tpv_service.get_comandas_activas()

                    # Calcular métricas de mesas
                    if mesas:
                        mesas_ocupadas = len([m for m in mesas if m.estado == "ocupada"])
                        total_mesas = len(mesas)

                    # Calcular comandas activas
                    if comandas_activas:
                        total_comandas = len(comandas_activas)

                        # Calcular ventas del día con manejo de errores
                        for comanda in comandas_activas:
                            try:
                                # Usar la propiedad total de la comanda
                                comanda_total = comanda.total if hasattr(comanda, 'total') else 0.0
                                ventas_dia += comanda_total if comanda_total else 0.0
                            except (AttributeError, TypeError) as e:
                                logger.warning(f"Error calculando total de comanda {comanda.id}: {e}")
                                continue

                        # Calcular tiempo promedio (placeholder - sería más complejo en implementación real)
                        tiempo_promedio = "12min" if total_comandas > 0 else "0min"
                except Exception as e:
                    logger.warning(f"Error obteniendo datos del servicio TPV: {e}")
                    # Mantener valores por defecto

            # Actualizar tarjetas con datos calculados (reales o por defecto)
            self.update_metric_card("mesas_activas", f"{mesas_ocupadas}/{total_mesas}")
            self.update_metric_card("ventas_dia", f"€{ventas_dia:.2f}")
            self.update_metric_card("comandas_activas", str(total_comandas))
            self.update_metric_card("tiempo_promedio", tiempo_promedio)

        except Exception as e:
            logger.error(f"Error actualizando métricas del dashboard: {e}")
            # Mostrar valores por defecto en caso de error crítico
            self.update_metric_card("mesas_activas", "0/0")
            self.update_metric_card("ventas_dia", "€0.00")
            self.update_metric_card("comandas_activas", "0")
            self.update_metric_card("tiempo_promedio", "0min")

    def update_metric_card(self, metric_key: str, new_value: str):
        """Actualiza el valor de una tarjeta KPIWidget"""
        if metric_key in self.metric_cards:
            card = self.metric_cards[metric_key]
            # Aquí se asume que el primer QLabel con font-size:28px es el valor
            for child in card.findChildren(QLabel):
                try:
                    if "font-size: 28px" in child.styleSheet():
                        child.setText(str(new_value))
                        break
                except Exception:
                    continue

    def set_service(self, tpv_service: TPVService):
        """Establece el servicio TPV"""
        self.tpv_service = tpv_service
        self.update_metrics()
