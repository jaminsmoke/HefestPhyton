"""
Widget StatisticsPanel - Panel de estadísticas del TPV
Versión: v0.0.14
"""

import logging
from typing import Optional, List
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

from services.tpv_service import TPVService, Mesa

logger = logging.getLogger(__name__)


class StatisticsPanel(QFrame):
    """Panel de estadísticas moderno y claro"""

    def __init__(self, tpv_service: Optional[TPVService] = None, parent=None):
        super().__init__(parent)
        self.tpv_service = tpv_service
        self.setup_ui()

    def setup_ui(self):
        """Configura la interfaz del panel de estadísticas"""
        import logging

        self.setStyleSheet(
            """
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #357abd);
                border-radius: 16px;
                padding: 20px;
                margin: 4px;
                min-height: 100px;
            }
        """
        )

        # Refuerzo: limpiar layout anterior
        old_layout = self.layout()
        if old_layout is not None:
            while old_layout.count():
                item = old_layout.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    if widget:
                        widget.setParent(None)
            try:
                old_layout.deleteLater()
            except Exception:
                pass

        # Crear layout sin padre y asignar con setLayout
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(24)
        self.setLayout(stats_layout)
        self.stats_layout = stats_layout

        # Título descriptivo
        self.create_title_section(self.stats_layout)

        # Separador
        self.create_separator(self.stats_layout)

        # Estadísticas
        self.create_statistics_cards(self.stats_layout)

    def create_title_section(self, layout: QHBoxLayout):
        """Crea la sección del título"""
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel("📊 Estado del Restaurante")
        title_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: white;
                margin-bottom: 4px;
            }
        """
        )

        subtitle_label = QLabel("Información en tiempo real")
        subtitle_label.setStyleSheet(
            """
            QLabel {
                font-size: 11px;
                color: rgba(255, 255, 255, 0.8);
            }
        """
        )

        title_layout.addWidget(title_label)
        title_layout.addWidget(subtitle_label)
        title_layout.addStretch()

        layout.addWidget(title_container)

    def create_separator(self, layout: QHBoxLayout):
        """Crea un separador vertical"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setStyleSheet("color: rgba(255, 255, 255, 0.3); margin: 8px 0px;")
        layout.addWidget(separator)

    def create_statistics_cards(self, layout: QHBoxLayout):
        """Crea las tarjetas de estadísticas"""
        if not self.tpv_service:
            return

        mesas = self.tpv_service.get_mesas()
        stats_data = self.calculate_statistics(mesas)

        for title, value, subtitle, icon, color in stats_data:
            card = self.create_stat_card(title, value, subtitle, icon, color)
            layout.addWidget(card)

    def calculate_statistics(self, mesas: List[Mesa]) -> List[tuple]:
        """Calcula las estadísticas de las mesas"""
        total_mesas = len(mesas)
        mesas_ocupadas = len([m for m in mesas if m.estado == "ocupada"])
        mesas_reservadas = len([m for m in mesas if m.estado == "reservada"])
        mesas_libres = len([m for m in mesas if m.estado == "libre"])

        return [
            ("Total", str(total_mesas), "mesas", "🏢", "#ffffff"),
            ("Libres", str(mesas_libres), "disponibles", "✅", "#4CAF50"),
            ("Ocupadas", str(mesas_ocupadas), "en uso", "🔴", "#F44336"),
            ("Reservadas", str(mesas_reservadas), "próximas", "📅", "#FF9800"),
        ]

    def create_stat_card(
        self, title: str, value: str, subtitle: str, icon: str, color: str
    ) -> QFrame:
        """Crea una tarjeta de estadística limpia y profesional"""
        card = QFrame()
        card.setFixedSize(120, 70)
        card.setStyleSheet(
            """
            QFrame {
                background-color: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 6px;
            }
        """
        )

        layout = QVBoxLayout(card)
        layout.setSpacing(2)
        layout.setContentsMargins(8, 6, 8, 6)

        # Línea superior: icono y valor
        top_layout = QHBoxLayout()
        top_layout.setSpacing(4)

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 14px;")
        icon_label.setFixedSize(16, 16)

        value_label = QLabel(value)
        value_label.setStyleSheet(
            f"""
            QLabel {{
                font-size: 18px;
                font-weight: bold;
                color: {color};
            }}
        """
        )
        value_label.setAlignment(Qt.AlignmentFlag.AlignRight)

        top_layout.addWidget(icon_label)
        top_layout.addStretch()
        top_layout.addWidget(value_label)

        # Línea inferior: título
        title_label = QLabel(title)
        title_label.setStyleSheet(
            """
            QLabel {
                font-size: 12px;
                color: white;
                font-weight: 600;
            }
        """
        )

        # Subtítulo
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet(
            """
            QLabel {
                font-size: 9px;
                color: rgba(255, 255, 255, 0.7);
            }
        """
        )
        layout.addLayout(top_layout)
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)

        return card

    def update_statistics(self):
        """Actualiza las estadísticas"""
        if not self.tpv_service:
            return

        try:
            # Limpiar layout
            self.clear_layout()

            # Recrear el contenido
            self.setup_ui()

            # logger.debug("Estadísticas actualizadas")  # Eliminado debug

        except Exception as e:
            logger.error(f"Error actualizando estadísticas: {e}")

    def clear_layout(self):
        """Limpia el layout actual"""
        layout = self.layout()
        if layout:
            while layout.count():
                child = layout.takeAt(0)
                if child and child.widget():
                    widget = child.widget()
                    if widget:
                        widget.deleteLater()

    def set_service(self, tpv_service: TPVService):
        """Establece el servicio TPV"""
        self.tpv_service = tpv_service
        self.update_statistics()

    def refresh_statistics(self):
        """Refresca las estadísticas con datos actualizados"""
        try:
            if not self.tpv_service:
                logger.warning("No hay servicio TPV para refrescar estadísticas")
                return

            # Obtener datos actualizados
            mesas = self.tpv_service.get_mesas()

            # Recalcular estadísticas
            stats_data = self.calculate_statistics(mesas)
            # Limpiar y recrear las tarjetas
            # TODO: En lugar de limpiar todo, actualizar valores existentes
            # Por ahora, simplemente recreamos
            self.create_statistics_cards(self.stats_layout)

            # logger.debug("Estadísticas refrescadas")  # Eliminado debug

        except Exception as e:
            logger.error(f"Error refrescando estadísticas: {e}")
