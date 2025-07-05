"""
Componente Profesional de Alertas Administrativas
==============================================

Descripción:
    Componente visual desacoplado para mostrar alertas administrativas en tiempo real.
    Se integra con AdministrativeLogicManager para obtener alertas basadas en datos reales.

Autor: GitHub Copilot
Versión: v0.0.12
Fecha: 2024-12-15
"""

import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLabel,
    QScrollArea,
    QPushButton,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QMouseEvent

from utils.administrative_logic_manager import AdministrativeLogicManager
from utils.modern_styles import ModernStyles

logger = logging.getLogger(__name__)


class ClickableFrame(QFrame):
    """Frame personalizado que maneja eventos de clic correctamente."""

    clicked = pyqtSignal(dict)

    def __init__(self, alert_data: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.alert_data = alert_data
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event: QMouseEvent | None):
        """Maneja el evento de clic del mouse."""
        if event and event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.alert_data)
        super().mousePressEvent(event)


class AdministrativeAlertsComponent(QWidget):
    """
    Componente visual profesional para la gestión de alertas administrativas.

    Características:
    - Actualización automática de alertas cada 30 segundos
    - Priorización visual de alertas por tipo y urgencia
    - Integración con datos reales de la base de datos
    - Arquitectura limpia y desacoplada
    - Manejo profesional de errores
    """

    # Señales para comunicación con el dashboard principal
    alert_clicked = pyqtSignal(dict)  # Emite cuando se hace clic en una alerta
    refresh_requested = pyqtSignal()  # Emite cuando se solicita actualización

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Inicializa el componente de alertas administrativas.

        Args:
            parent: Widget padre (opcional)
        """
        super().__init__(parent)

        # Configuración inicial
        self.administrative_logic = AdministrativeLogicManager()
        self.current_alerts: List[Dict[str, Any]] = []
        self.modern_styles = ModernStyles()

        # Timer para actualización automática
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_alerts)
        self.refresh_timer.start(30000)  # Actualizar cada 30 segundos

        # Configurar UI
        self._setup_ui()
        self._apply_styles()

        # Cargar alertas iniciales
        self.refresh_alerts()

        logger.info("AdministrativeAlertsComponent inicializado correctamente")

    def _setup_ui(self):
        """Configura la interfaz de usuario del componente."""
        try:
            # Layout principal
            self.main_layout = QVBoxLayout(self)
            self.main_layout.setContentsMargins(16, 16, 16, 16)
            self.main_layout.setSpacing(12)

            # Header con título y botón de actualización
            self._setup_header()

            # Área de scroll para las alertas
            self._setup_alerts_area()

            # Footer con información de estado
            self._setup_footer()

        except Exception as e:
            logger.error(f"Error configurando UI de alertas: {e}")
            self._show_error_state("Error configurando interfaz")

    def _setup_header(self):
        """Configura el header del componente."""
        header_frame = QFrame()
        header_frame.setObjectName("alerts_header")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)

        # Título
        title_label = QLabel("Alertas Administrativas")
        title_label.setObjectName("alerts_title")
        title_font = QFont("Segoe UI", 14, QFont.Weight.Bold)
        title_label.setFont(title_font)

        # Botón de actualización
        refresh_btn = QPushButton("🔄 Actualizar")
        refresh_btn.setObjectName("alerts_refresh_btn")
        refresh_btn.clicked.connect(self.refresh_alerts)
        refresh_btn.setToolTip("Actualizar alertas manualmente")

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(refresh_btn)

        self.main_layout.addWidget(header_frame)

    def _setup_alerts_area(self):
        """Configura el área scrollable para mostrar las alertas."""
        # Crear scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll_area.setObjectName("alerts_scroll_area")

        # Widget contenedor para las alertas
        self.alerts_container = QWidget()
        self.alerts_layout = QVBoxLayout(self.alerts_container)
        self.alerts_layout.setContentsMargins(8, 8, 8, 8)
        self.alerts_layout.setSpacing(8)

        # Mensaje de estado inicial
        self.status_label = QLabel("Cargando alertas...")
        self.status_label.setObjectName("alerts_status_label")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alerts_layout.addWidget(self.status_label)

        self.scroll_area.setWidget(self.alerts_container)
        self.main_layout.addWidget(self.scroll_area)

    def _setup_footer(self):
        """Configura el footer con información de estado."""
        self.footer_frame = QFrame()
        self.footer_frame.setObjectName("alerts_footer")
        footer_layout = QHBoxLayout(self.footer_frame)
        footer_layout.setContentsMargins(8, 4, 8, 4)

        # Etiqueta de última actualización
        self.last_update_label = QLabel("Última actualización: --")
        self.last_update_label.setObjectName("alerts_last_update")
        footer_layout.addWidget(self.last_update_label)

        footer_layout.addStretch()

        # Contador de alertas
        self.alerts_count_label = QLabel("Alertas: 0")
        self.alerts_count_label.setObjectName("alerts_count")
        footer_layout.addWidget(self.alerts_count_label)

        self.main_layout.addWidget(self.footer_frame)

    def _apply_styles(self):
        """Aplica los estilos modernos al componente."""
        try:
            colors = self.modern_styles.COLORS
            styles = f"""
            /* Componente principal */
            AdministrativeAlertsComponent {{
                background-color: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 12px;
            }}

            /* Header */
            QFrame#alerts_header {{
                background-color: {colors['surface_variant']};
                border: none;
                border-radius: 8px;
                padding: 8px;
            }}

            QLabel#alerts_title {{
                color: {colors['text_primary']};
                font-weight: bold;
            }}

            QPushButton#alerts_refresh_btn {{
                background-color: {colors['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: 500;
            }}

            QPushButton#alerts_refresh_btn:hover {{
                background-color: {colors['primary_hover']};
            }}

            QPushButton#alerts_refresh_btn:pressed {{
                background-color: {colors['primary_pressed']};
            }}

            /* Scroll Area */
            QScrollArea#alerts_scroll_area {{
                border: none;
                background-color: transparent;
            }}

            QScrollArea#alerts_scroll_area QScrollBar:vertical {{
                background-color: {colors['surface_variant']};
                width: 8px;
                border-radius: 4px;
            }}

            QScrollArea#alerts_scroll_area QScrollBar::handle:vertical {{
                background-color: {colors['secondary']};
                border-radius: 4px;
                min-height: 20px;
            }}

            QScrollArea#alerts_scroll_area QScrollBar::handle:vertical:hover {{
                background-color: {colors['secondary_hover']};
            }}

            /* Status Label */
            QLabel#alerts_status_label {{
                color: {colors['text_secondary']};
                font-size: 14px;
                padding: 20px;
            }}

            /* Footer */
            QFrame#alerts_footer {{
                background-color: {colors['surface_variant']};
                border: none;
                border-radius: 6px;
            }}

            QLabel#alerts_last_update {{
                color: {colors['text_secondary']};
                font-size: 12px;
            }}

            QLabel#alerts_count {{
                color: {colors['text_primary']};
                font-size: 12px;
                font-weight: 500;
            }}

            /* Tarjetas de alerta */
            ClickableFrame {{
                background-color: {colors['surface']};
                border: 1px solid {colors['border']};
                border-radius: 8px;
                padding: 12px;
                margin: 4px;
            }}

            ClickableFrame:hover {{
                background-color: {colors['surface_hover']};
                border-color: {colors['border_focus']};
            }}

            ClickableFrame[alertType="critical"] {{
                border-left: 4px solid {colors['error']};
                background-color: {colors['surface_variant']};
            }}

            ClickableFrame[alertType="warning"] {{
                border-left: 4px solid {colors['warning']};
                background-color: {colors['surface_variant']};
            }}

            ClickableFrame[alertType="info"] {{
                border-left: 4px solid {colors['info']};
                background-color: {colors['surface_variant']};
            }}

            QLabel.alert_title {{
                color: {colors['text_primary']};
                font-size: 13px;
                font-weight: 600;
            }}

            QLabel.alert_message {{
                color: {colors['text_secondary']};
                font-size: 12px;
            }}

            QLabel.alert_timestamp {{
                color: {colors['text_muted']};
                font-size: 11px;
            }}
            """

            self.setStyleSheet(styles)

        except Exception as e:
            logger.error(f"Error aplicando estilos a alertas: {e}")

    def refresh_alerts(self):
        """Actualiza las alertas obteniendo datos reales de la base de datos."""
        try:
            # logger.debug("Iniciando actualización de alertas administrativas")

            # Obtener alertas reales del manager
            alerts_data = self.administrative_logic.get_administrative_alerts()
            alerts = (
                alerts_data.get("alerts", []) if isinstance(alerts_data, dict) else []
            )

            # logger.debug(f"Obtenidas {len(alerts)} alertas del sistema")

            # Actualizar el estado interno
            self.current_alerts = alerts

            # Limpiar el contenedor actual
            self._clear_alerts_container()

            # Renderizar las nuevas alertas
            if alerts:
                self._render_alerts(alerts)
                self.status_label.hide()
            else:
                self._show_no_alerts_state()

            # Actualizar información del footer
            self._update_footer_info()

            # Emitir señal de actualización completada
            self.refresh_requested.emit()

            # logger.debug("Actualización de alertas completada exitosamente")

        except Exception as e:
            logger.error(f"Error actualizando alertas: {e}")
            self._show_error_state(f"Error actualizando alertas: {str(e)}")

    def _clear_alerts_container(self):
        """Limpia todos los widgets del contenedor de alertas."""
        try:
            # Remover todos los widgets excepto el status_label
            for i in reversed(range(self.alerts_layout.count())):
                item = self.alerts_layout.itemAt(i)
                if item and item.widget() and item.widget() != self.status_label:
                    widget = item.widget()
                    self.alerts_layout.removeWidget(widget)
                    if widget:
                        widget.deleteLater()
        except Exception as e:
            logger.error(f"Error limpiando contenedor de alertas: {e}")

    def _render_alerts(self, alerts: List[Dict[str, Any]]):
        """
        Renderiza las alertas en el contenedor.

        Args:
            alerts: Lista de alertas a renderizar
        """
        try:
            # Ordenar alertas por prioridad (críticas primero)
            sorted_alerts = sorted(alerts, key=self._get_alert_priority, reverse=True)

            for alert in sorted_alerts:
                alert_widget = self._create_alert_widget(alert)
                if alert_widget:
                    self.alerts_layout.addWidget(alert_widget)

            # Agregar espaciador al final
            self.alerts_layout.addStretch()

        except Exception as e:
            logger.error(f"Error renderizando alertas: {e}")

    def _create_alert_widget(self, alert: Dict[str, Any]) -> Optional[QWidget]:
        """
        Crea un widget visual para una alerta específica.

        Args:
            alert: Diccionario con los datos de la alerta

        Returns:
            Widget de la alerta o None si hay error
        """
        try:
            # Frame principal de la alerta (usando el frame personalizado)
            alert_frame = ClickableFrame(alert, self)
            alert_frame.setObjectName("alert_card")

            # Configurar tipo de alerta para estilos
            alert_type = alert.get("type", "info")
            alert_frame.setProperty("alertType", alert_type)

            # Conectar señal de clic
            alert_frame.clicked.connect(self._on_alert_clicked)

            # Layout de la alerta
            alert_layout = QVBoxLayout(alert_frame)
            alert_layout.setContentsMargins(8, 8, 8, 8)
            alert_layout.setSpacing(4)

            # Header de la alerta (icono + título)
            header_layout = QHBoxLayout()

            # Icono según el tipo
            icon_label = QLabel(self._get_alert_icon(alert_type))
            icon_label.setFixedSize(16, 16)

            # Título
            title_label = QLabel(alert.get("title", "Alerta"))
            title_label.setObjectName("alert_title")
            title_label.setProperty("class", "alert_title")

            header_layout.addWidget(icon_label)
            header_layout.addWidget(title_label)
            header_layout.addStretch()

            # Mensaje
            message_label = QLabel(alert.get("message", ""))
            message_label.setObjectName("alert_message")
            message_label.setProperty("class", "alert_message")
            message_label.setWordWrap(True)

            # Timestamp
            timestamp_label = QLabel(f"Detectado: {alert.get('timestamp', 'Ahora')}")
            timestamp_label.setObjectName("alert_timestamp")
            timestamp_label.setProperty("class", "alert_timestamp")

            # Agregar widgets al layout
            alert_layout.addLayout(header_layout)
            alert_layout.addWidget(message_label)
            alert_layout.addWidget(timestamp_label)

            return alert_frame

        except Exception as e:
            logger.error(f"Error creando widget de alerta: {e}")
            return None

    def _get_alert_icon(self, alert_type: str) -> str:
        """
        Obtiene el icono unicode para el tipo de alerta.

        Args:
            alert_type: Tipo de alerta ('critical', 'warning', 'info')

        Returns:
            Icono unicode como string
        """
        icons = {"critical": "🚨", "warning": "⚠️", "info": "ℹ️"}
        return icons.get(alert_type, "ℹ️")

    def _get_alert_priority(self, alert: Dict[str, Any]) -> int:
        """
        Obtiene la prioridad numérica de una alerta para ordenamiento.

        Args:
            alert: Diccionario de la alerta

        Returns:
            Prioridad numérica (mayor = más prioritario)
        """
        priorities = {"critical": 3, "warning": 2, "info": 1}
        return priorities.get(alert.get("type", "info"), 1)

    def _show_no_alerts_state(self):
        """Muestra el estado cuando no hay alertas."""
        self.status_label.setText(
            "✅ No hay alertas activas\nTodos los sistemas funcionan correctamente"
        )
        self.status_label.show()

    def _show_error_state(self, error_msg: str):
        """
        Muestra el estado de error.

        Args:
            error_msg: Mensaje de error a mostrar
        """
        self.status_label.setText(f"❌ Error cargando alertas\n{error_msg}")
        self.status_label.show()

    def _update_footer_info(self):
        """Actualiza la información del footer."""
        try:
            # Actualizar timestamp
            now = datetime.now().strftime("%H:%M:%S")
            self.last_update_label.setText(f"Última actualización: {now}")

            # Actualizar contador
            count = len(self.current_alerts)
            critical_count = len(
                [a for a in self.current_alerts if a.get("type") == "critical"]
            )

            if critical_count > 0:
                self.alerts_count_label.setText(
                    f"Alertas: {count} ({critical_count} críticas)"
                )
                self.alerts_count_label.setStyleSheet(
                    f"color: {self.modern_styles.COLORS['error']};"
                )
            else:
                self.alerts_count_label.setText(f"Alertas: {count}")
                self.alerts_count_label.setStyleSheet(
                    f"color: {self.modern_styles.COLORS['text_primary']};"
                )

        except Exception as e:
            logger.error(f"Error actualizando footer: {e}")

    def _on_alert_clicked(self, alert: Dict[str, Any]):
        """
        Maneja el clic en una alerta específica.

        Args:
            alert: Datos de la alerta clickeada
        """
        try:
            # logger.debug(f"Alerta clickeada: {alert.get('title', 'Sin título')}")

            # Emitir señal con los datos de la alerta
            self.alert_clicked.emit(alert)

            # Mostrar información adicional si está disponible
            if alert.get("details"):
                self._show_alert_details(alert)

        except Exception as e:
            logger.error(f"Error manejando clic en alerta: {e}")

    def _show_alert_details(self, alert: Dict[str, Any]):
        """
        Muestra los detalles de una alerta en un diálogo.

        Args:
            alert: Datos de la alerta
        """
        try:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle(f"Detalles: {alert.get('title', 'Alerta')}")
            msg_box.setText(alert.get("message", ""))

            if alert.get("details"):
                msg_box.setDetailedText(alert["details"])

            # Configurar icono según el tipo
            if alert.get("type") == "critical":
                msg_box.setIcon(QMessageBox.Icon.Critical)
            elif alert.get("type") == "warning":
                msg_box.setIcon(QMessageBox.Icon.Warning)
            else:
                msg_box.setIcon(QMessageBox.Icon.Information)

            msg_box.exec()

        except Exception as e:
            logger.error(f"Error mostrando detalles de alerta: {e}")

    def get_current_alerts(self) -> List[Dict[str, Any]]:
        """
        Obtiene las alertas actuales del componente.

        Returns:
            Lista de alertas actuales
        """
        return self.current_alerts.copy()

    def get_alerts_count(self) -> Dict[str, int]:
        """
        Obtiene el conteo de alertas por tipo.

        Returns:
            Diccionario con conteos por tipo
        """
        counts = {"total": 0, "critical": 0, "warning": 0, "info": 0}

        for alert in self.current_alerts:
            counts["total"] += 1
            alert_type = alert.get("type", "info")
            if alert_type in counts:
                counts[alert_type] += 1

        return counts

    def set_auto_refresh(self, enabled: bool, interval_seconds: int = 30):
        """
        Configura la actualización automática de alertas.

        Args:
            enabled: Si la actualización automática está habilitada
            interval_seconds: Intervalo de actualización en segundos
        """
        try:
            if enabled:
                self.refresh_timer.start(interval_seconds * 1000)
                # logger.debug(
                #     f"Auto-refresh habilitado cada {interval_seconds} segundos"
                # )
            else:
                self.refresh_timer.stop()
                # logger.debug("Auto-refresh deshabilitado")
        except Exception as e:
            logger.error(f"Error configurando auto-refresh: {e}")

    def closeEvent(self, event):
        """Limpia recursos al cerrar el componente."""
        try:
            # Detener timer
            if hasattr(self, "refresh_timer"):
                self.refresh_timer.stop()

            # logger.debug("AdministrativeAlertsComponent cerrado correctamente")
            super().closeEvent(event)

        except Exception as e:
            logger.error(f"Error cerrando componente de alertas: {e}")
            super().closeEvent(event)


# Funciones auxiliares para uso externo
def create_alerts_component(
    parent: Optional[QWidget] = None,
) -> AdministrativeAlertsComponent:
    """
    Función de conveniencia para crear un componente de alertas.

    Args:
        parent: Widget padre opcional

    Returns:
        Instancia del componente de alertas
    """
    return AdministrativeAlertsComponent(parent)


def get_current_alerts_summary() -> Dict[str, Any]:
    """
    Obtiene un resumen de las alertas actuales del sistema.

    Returns:
        Diccionario con resumen de alertas
    """
    try:
        logic_manager = AdministrativeLogicManager()
        alerts_data = logic_manager.get_administrative_alerts()
        alerts = alerts_data.get("alerts", []) if isinstance(alerts_data, dict) else []

        summary = {
            "total": len(alerts),
            "critical": len([a for a in alerts if a.get("type") == "critical"]),
            "warning": len([a for a in alerts if a.get("type") == "warning"]),
            "info": len([a for a in alerts if a.get("type") == "info"]),
            "alerts": alerts,
        }

        return summary

    except Exception as e:
        logger.error(f"Error obteniendo resumen de alertas: {e}")
        return {
            "total": 0,
            "critical": 0,
            "warning": 0,
            "info": 0,
            "alerts": [],
            "error": str(e),
        }
