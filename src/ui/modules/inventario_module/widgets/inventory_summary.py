"""
Widget de resumen de inventario - Hefest v0.0.12
===============================================

Widget que muestra un resumen ejecutivo del estado del inventario con
métricas clave, alertas visuales y estadísticas importantes para hostelería.

MÉTRICAS MOSTRADAS:
------------------
- Total de productos registrados
- Valor total del inventario (€)
- Productos con stock bajo
- Productos sin stock (agotados)
- Valor promedio por producto
- Distribución por categorías

ALERTAS VISUALES:
----------------
- Stock crítico (productos < stock mínimo)
- Productos sin movimiento
- Productos próximos a caducar
- Alertas de reposición

CARACTERÍSTICAS:
---------------
- Actualización automática de datos
- Colores intuitivos (verde=ok, amarillo=precaución, rojo=crítico)
- Clickeable para navegación rápida
- Responsive design adaptable

INTEGRACIÓN:
-----------
- Obtiene datos de inventario_service_real.py
- Se actualiza cuando cambia el inventario
- Permite navegación directa a productos problemáticos

AUTOR: Hefest Development Team
VERSIÓN: v0.0.12
"""

import logging
from typing import Dict, Any, List
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QProgressBar,
    QGridLayout,
    QPushButton,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QMouseEvent

from src.utils.modern_styles import ModernStyles

logger = logging.getLogger(__name__)


class ClickableFrame(QFrame):
    """Frame que emite señal al hacer clic"""

    clicked = pyqtSignal(dict)

    def __init__(self, alert_data: dict, parent=None):
        super().__init__(parent)
        self.alert_data = alert_data

    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.alert_data)
        super().mousePressEvent(ev)


class ClickableLabel(QLabel):
    """Label que emite señal al hacer clic"""

    clicked = pyqtSignal(str)

    def __init__(self, text: str, category: str, parent=None):
        super().__init__(text, parent)
        self.category = category

    def mousePressEvent(self, ev: QMouseEvent):
        if ev.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.category)
        super().mousePressEvent(ev)


class InventorySummaryWidget(QWidget):
    """
    Widget de resumen de inventario con métricas clave.

    Características:
    - Métricas principales (total productos, valor, alertas)
    - Gráfico de distribución por categorías
    - Indicadores de estado visual
    - Alertas prioritarias
    """

    # Señales
    alert_clicked = pyqtSignal(dict)  # Clic en alerta
    category_clicked = pyqtSignal(str)  # Clic en categoría
    refresh_requested = pyqtSignal()  # Solicitud de actualización

    def __init__(self, parent=None):
        super().__init__(parent)
        self.modern_styles = ModernStyles()
        self.summary_data = {}
        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self):
        """Configura la interfaz del resumen"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(16, 16, 16, 16)

        # Header con título y botón de actualización
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)

        # Métricas principales
        metrics_layout = self._create_metrics_section()
        main_layout.addLayout(metrics_layout)

        # Alertas críticas
        alerts_widget = self._create_alerts_section()
        main_layout.addWidget(alerts_widget)

        # Distribución por categorías
        categories_widget = self._create_categories_section()
        main_layout.addWidget(categories_widget)

        main_layout.addStretch()

    def _create_header(self) -> QHBoxLayout:
        """Crea el header del widget"""
        layout = QHBoxLayout()

        # Título
        title_label = QLabel("📊 Resumen de Inventario")
        title_label.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
        """
        )
        layout.addWidget(title_label)

        layout.addStretch()

        # Botón de actualización
        self.refresh_btn = QPushButton("🔄 Actualizar")
        self.refresh_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #17a2b8;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #138496;
            }
        """
        )
        self.refresh_btn.clicked.connect(self.refresh_requested.emit)
        layout.addWidget(self.refresh_btn)

        return layout

    def _create_metrics_section(self) -> QGridLayout:
        """Crea la sección de métricas principales"""
        layout = QGridLayout()
        layout.setSpacing(12)

        # Métrica: Total de productos
        self.total_products_widget = self._create_metric_card(
            title="Total Productos", value="0", icon="📦", color="#007bff"
        )
        layout.addWidget(self.total_products_widget, 0, 0)

        # Métrica: Valor total del inventario
        self.total_value_widget = self._create_metric_card(
            title="Valor Total", value="0.00 €", icon="💰", color="#28a745"
        )
        layout.addWidget(self.total_value_widget, 0, 1)

        # Métrica: Productos con stock bajo
        self.low_stock_widget = self._create_metric_card(
            title="Stock Bajo", value="0", icon="⚠️", color="#ffc107"
        )
        layout.addWidget(self.low_stock_widget, 0, 2)

        # Métrica: Productos agotados
        self.out_of_stock_widget = self._create_metric_card(
            title="Agotados", value="0", icon="🚫", color="#dc3545"
        )
        layout.addWidget(self.out_of_stock_widget, 0, 3)

        return layout

    def _create_metric_card(
        self, title: str, value: str, icon: str, color: str
    ) -> QFrame:
        """Crea una tarjeta de métrica"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.Box)
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 16px;
                border-left: 4px solid {color};
            }}
            QFrame:hover {{
                /* box-shadow: 0 2px 4px rgba(0,0,0,0.1); */
            }}
        """
        )

        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        # Header con icono y título
        header_layout = QHBoxLayout()

        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        header_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            """
            font-size: 12px;
            font-weight: bold;
            color: #6c757d;
        """
        )
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        layout.addLayout(header_layout)

        # Valor principal
        value_label = QLabel(value)
        value_label.setObjectName("value_label")
        value_label.setStyleSheet(
            f"""
            font-size: 28px;
            font-weight: bold;
            color: {color};
        """
        )
        layout.addWidget(value_label)

        return card

    def _create_alerts_section(self) -> QFrame:
        """Crea la sección de alertas críticas"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: #fff3cd;
                border: 1px solid #ffeeba;
                border-radius: 8px;
                padding: 12px;
            }
        """
        )

        layout = QVBoxLayout(frame)
        layout.setSpacing(8)

        # Título de la sección
        title_label = QLabel("🚨 Alertas Críticas")
        title_label.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            color: #856404;
        """
        )
        layout.addWidget(title_label)

        # Contenedor de alertas
        self.alerts_container = QWidget()
        self.alerts_layout = QVBoxLayout(self.alerts_container)
        self.alerts_layout.setSpacing(4)
        layout.addWidget(self.alerts_container)

        # Mensaje inicial
        self.no_alerts_label = QLabel("No hay alertas críticas")
        self.no_alerts_label.setStyleSheet("color: #6c757d; font-style: italic;")
        layout.addWidget(self.no_alerts_label)

        return frame

    def _create_categories_section(self) -> QFrame:
        """Crea la sección de distribución por categorías"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 12px;
            }
        """
        )

        layout = QVBoxLayout(frame)
        layout.setSpacing(8)

        # Título de la sección
        title_label = QLabel("📈 Distribución por Categorías")
        title_label.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            color: #495057;
        """
        )
        layout.addWidget(title_label)

        # Contenedor de categorías
        self.categories_container = QWidget()
        self.categories_layout = QVBoxLayout(self.categories_container)
        self.categories_layout.setSpacing(6)
        layout.addWidget(self.categories_container)

        return frame

    def _apply_styles(self):
        """Aplica estilos al widget"""
        colors = self.modern_styles.COLORS
        self.setStyleSheet(
            f"""
            InventorySummaryWidget {{
                background-color: {colors['background']};
            }}
        """
        )

    def update_summary(self, data: Dict[str, Any]):
        """
        Actualiza el resumen con nuevos datos.

        Args:
            data: Datos del resumen de inventario
        """
        self.summary_data = data

        # Actualizar métricas principales
        self._update_metrics(data)

        # Actualizar alertas
        self._update_alerts(data.get("alerts", []))

        # Actualizar categorías        self._update_categories(data.get('categories', {}))

    def _update_metrics(self, data: Dict[str, Any]):
        """Actualiza las métricas principales"""
        # Total productos
        total_products = data.get("total_products", 0)
        total_value_label = self.total_products_widget.findChild(QLabel, "value_label")
        if total_value_label:
            total_value_label.setText(str(total_products))

        # Valor total
        total_value = data.get("total_value", 0.0)
        value_label = self.total_value_widget.findChild(QLabel, "value_label")
        if value_label:
            value_label.setText(f"{total_value:.2f} €")

        # Stock bajo
        low_stock = data.get("low_stock_products", 0)
        low_stock_label = self.low_stock_widget.findChild(QLabel, "value_label")
        if low_stock_label:
            low_stock_label.setText(str(low_stock))

        # Agotados
        out_of_stock = data.get("out_of_stock_products", 0)
        out_stock_label = self.out_of_stock_widget.findChild(QLabel, "value_label")
        if out_stock_label:
            out_stock_label.setText(str(out_of_stock))

    def _update_alerts(self, alerts: List[Dict[str, Any]]):
        """Actualiza las alertas críticas"""
        # Limpiar alertas existentes
        self._clear_alerts()

        if not alerts:
            self.no_alerts_label.show()
            return

        self.no_alerts_label.hide()

        # Mostrar solo las 5 alertas más críticas
        critical_alerts = alerts[:5]

        for alert in critical_alerts:
            alert_widget = self._create_alert_item(alert)
            self.alerts_layout.addWidget(alert_widget)

    def _update_categories(self, categories: Dict[str, int]):
        """Actualiza la distribución por categorías"""
        # Limpiar categorías existentes
        self._clear_categories()

        if not categories:
            return
        # Crear barras de progreso para cada categoría
        max_value = max(categories.values()) if categories else 1

        for category, count in categories.items():
            category_widget = self._create_category_item(category, count, max_value)
            self.categories_layout.addWidget(category_widget)

    def _create_alert_item(self, alert: Dict[str, Any]) -> QWidget:
        """Crea un widget para una alerta individual"""
        widget = ClickableFrame(alert)
        widget.setFrameStyle(QFrame.Shape.Box)
        widget.setStyleSheet(
            """
            QFrame {
                background-color: #f8d7da;
                border: 1px solid #f5c6cb;
                border-radius: 4px;
                padding: 6px;
            }
        """
        )
        widget.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)

        # Información de la alerta
        info_label = QLabel(alert.get("message", "Alerta sin mensaje"))
        info_label.setStyleSheet("font-size: 11px; color: #721c24;")
        layout.addWidget(info_label)

        layout.addStretch()

        # Severity indicator
        severity = alert.get("severity", "low")
        severity_label = QLabel(severity.upper())
        severity_label.setStyleSheet(
            f"""
            font-size: 10px;
            font-weight: bold;
            color: {'#dc3545' if severity == 'high' else '#ffc107' if severity == 'medium' else '#28a745'};
        """
        )
        layout.addWidget(severity_label)

        # Conectar señal
        widget.clicked.connect(self.alert_clicked.emit)

        return widget

    def _create_category_item(
        self, category: str, count: int, max_value: int
    ) -> QWidget:
        """Crea un widget para una categoría"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 2, 0, 2)
        # Nombre de la categoría
        category_label = ClickableLabel(category, category)
        category_label.setFixedWidth(120)
        category_label.setStyleSheet("font-size: 11px; font-weight: bold;")
        category_label.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(category_label)

        # Barra de progreso
        progress_bar = QProgressBar()
        progress_bar.setMaximum(max_value)
        progress_bar.setValue(count)
        progress_bar.setTextVisible(True)
        progress_bar.setFormat(f"{count} productos")
        progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 3px;
                text-align: center;
                font-size: 10px;
                height: 16px;
            }
            QProgressBar::chunk {
                background-color: #007bff;
                border-radius: 2px;
            }
        """
        )
        layout.addWidget(progress_bar)

        # Conectar señal
        category_label.clicked.connect(self.category_clicked.emit)

        return widget

    def _clear_alerts(self):
        """Limpia todas las alertas"""
        while self.alerts_layout.count():
            child = self.alerts_layout.takeAt(0)
            if child and child.widget():
                widget = child.widget()
                if widget:
                    widget.deleteLater()

    def _clear_categories(self):
        """Limpia todas las categorías"""
        while self.categories_layout.count():
            child = self.categories_layout.takeAt(0)
            if child and child.widget():
                widget = child.widget()
                if widget:
                    widget.deleteLater()

    def get_summary_data(self) -> Dict[str, Any]:
        """Obtiene los datos del resumen actual"""
        return self.summary_data.copy()
