"""
Componente TPVDashboard - Dashboard de métricas del TPV
Versión: v0.0.13
"""

import logging
from typing import Optional
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from services.tpv_service import TPVService
from utils.qt_css_compat import convert_to_qt_compatible_css

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
          # Métricas dinámicas del día
        metrics_config = [
            ("mesas_activas", "🍽️", "Mesas Ocupadas", "0/0", "#2196f3"),
            ("ventas_dia", "💰", "Ventas Hoy", "€0.00", "#4caf50"),
            ("comandas_activas", "📝", "Comandas Activas", "0", "#ff9800"),
            ("tiempo_promedio", "⏱️", "Tiempo Prom.", "0min", "#9c27b0")
        ]

        for metric_key, icon, title, default_value, color in metrics_config:
            metric_widget = self.create_metric_card(metric_key, icon, title, default_value, color)
            self.metric_cards[metric_key] = metric_widget
            layout.addWidget(metric_widget)

        layout.addStretch()

    def create_metric_card(self, key: str, icon: str, title: str, value: str, color: str) -> QWidget:
        """Crea una tarjeta de métrica simple y compatible con PyQt6"""
        card = QFrame()
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setLineWidth(2)

        # Estilo muy simple para máxima compatibilidad
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 8px;
            }}
        """)
        card.setFixedSize(160, 100)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(4)

        # Header - en una sola línea para simplicidad
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)

        # Icono - sin CSS complejo
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 16px; color: {color};")
        header_layout.addWidget(icon_label)

        # Título - sin CSS complejo
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 9px; font-weight: bold; color: {color};")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        layout.addWidget(header_widget)

        # Espaciador
        layout.addStretch()

        # Valor principal - configuración simple
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Configurar fuente de forma programática (más confiable que CSS)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        value_label.setFont(font)
        value_label.setStyleSheet(f"color: {color};")

        layout.addWidget(value_label)
        layout.addStretch()

        # Guardar referencia para actualizaciones
        setattr(card, 'value_label', value_label)
        setattr(card, 'metric_key', key)

        return card

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
        """Actualiza el valor de una tarjeta específica"""
        if metric_key in self.metric_cards:
            card = self.metric_cards[metric_key]
            value_label = getattr(card, 'value_label', None)
            if value_label:
                value_label.setText(new_value)

    def set_service(self, tpv_service: TPVService):
        """Establece el servicio TPV"""
        self.tpv_service = tpv_service
        self.update_metrics()
