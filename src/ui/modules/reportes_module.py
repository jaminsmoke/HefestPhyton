"""
Módulo de reportes y estadísticas del sistema Hefest.
Proporciona informes detallados sobre ventas, ocupación, inventario y otros KPIs del negocio.
"""

import logging
from datetime import datetime
from typing import Optional, List, Tuple

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QLabel,
    QPushButton,
    QDateEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFrame,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal, QTimer
from PyQt6.QtGui import QColor

# Comentado: PyQt6.QtChart no está disponible en todas las instalaciones
# from PyQt6.QtChart import QChart, QChartView, QBarSeries, QBarSet, QLineSeries, QPieSeries, QPieSlice
# from PyQt6.QtChart import QCategoryAxis, QValueAxis

from ui.modules.module_base_interface import BaseModule

logger = logging.getLogger(__name__)


class ReportesModule(BaseModule):
    """Módulo de reportes y estadísticas del sistema"""

    # Señales
    reporte_generado = pyqtSignal(str, dict)  # (tipo_reporte, datos)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)  # type: ignore
        self.setup_ui()
        self.cargar_datos_iniciales()

        # Inicializar atributos de fecha
        self.fecha_desde: QDateEdit = QDateEdit()
        self.fecha_hasta: QDateEdit = QDateEdit()

        # Timer para actualización automática
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.actualizar_datos)  # type: ignore
        self.timer.start(60000)  # Actualizar cada minuto

    def create_module_header(self) -> QFrame:  # type: ignore[override]
        """Crea el header del módulo de reportes"""
        header = QFrame()
        header.setObjectName("module-header")
        header.setFixedHeight(70)
        header.setStyleSheet(
            """
            QFrame#module-header {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8b5cf6, stop:1 #06b6d4);
                border-radius: 8px;
                margin: 10px;
            }
        """
        )

        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 0, 20, 0)

        # Icono y título
        title_container = QHBoxLayout()

        icon_label = QLabel("📊")
        icon_label.setStyleSheet("font-size: 32px;")
        title_container.addWidget(icon_label)

        title_text = QVBoxLayout()
        title = QLabel("Reportes y Estadísticas")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        subtitle = QLabel("Análisis detallado del rendimiento del negocio")
        subtitle.setStyleSheet("font-size: 14px; color: rgba(255,255,255,0.8);")

        title_text.addWidget(title)
        title_text.addWidget(subtitle)
        title_container.addLayout(title_text)

        layout.addLayout(title_container)
        layout.addStretch()

        # Botones de acción
        exportar_btn = QPushButton("📄 Exportar Reporte")
        exportar_btn.setStyleSheet(
            """
            QPushButton {
                background: rgba(255,255,255,0.2);
                color: white;
                border: 1px solid rgba(255,255,255,0.3);
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.3);
            }
        """
        )
        exportar_btn.clicked.connect(self.exportar_reporte)  # type: ignore

        actualizar_btn = QPushButton("🔄 Actualizar")
        actualizar_btn.setStyleSheet(
            """
            QPushButton {
                background: rgba(255,255,255,0.1);
                color: white;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.2);
            }
        """
        )
        actualizar_btn.clicked.connect(self.actualizar_datos)  # type: ignore

        layout.addWidget(exportar_btn)
        layout.addWidget(actualizar_btn)

        return header

    def create_filtros_panel(self) -> QFrame:
        """Crea el panel de filtros para los reportes"""
        panel = QFrame()
        panel.setStyleSheet("background: #f3f4f6; border-radius: 8px; padding: 10px;")
        layout = QHBoxLayout(panel)

        # Filtros de fecha
        date_label = QLabel("Fecha:")
        date_label.setStyleSheet("font-weight: bold;")
        self.start_date: QDateEdit = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.end_date: QDateEdit = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())

        layout.addWidget(date_label)
        layout.addWidget(self.start_date)
        layout.addWidget(QLabel("a"))
        layout.addWidget(self.end_date)

        # Botón de aplicar filtros
        apply_btn = QPushButton("Aplicar Filtros")
        apply_btn.setStyleSheet(
            "background: #3b82f6; color: white; padding: 6px 12px; border-radius: 6px;"
        )
        apply_btn.clicked.connect(self.aplicar_filtros)  # type: ignore
        layout.addWidget(apply_btn)

        layout.addStretch()
        return panel

    def create_dashboard_tab(self) -> None:
        """Crea la pestaña del dashboard de reportes"""
        dashboard_tab = QWidget()
        layout = QVBoxLayout(dashboard_tab)

        # KPI Cards
        kpi_layout = QHBoxLayout()
        kpi_layout.addWidget(
            self.create_kpi_card("Ventas Totales", "€0.00", "+5%", "#10b981")
        )
        kpi_layout.addWidget(self.create_kpi_card("Reservas", "0", "-2%", "#ef4444"))
        kpi_layout.addWidget(self.create_kpi_card("Ocupación", "0%", "+1%", "#3b82f6"))
        layout.addLayout(kpi_layout)

        # Gráficos
        charts_layout = QHBoxLayout()
        charts_layout.addWidget(self.create_ventas_chart())
        charts_layout.addWidget(self.create_ocupacion_chart())
        layout.addLayout(charts_layout)

        self.tabs.addTab(dashboard_tab, "Dashboard")

    def create_ventas_tab(self) -> None:
        """Crea la pestaña de reportes de ventas"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Métricas de ventas
        metricas_layout = QHBoxLayout()

        metricas_data: List[Tuple[str, str, str]] = [
            ("Total Ventas", "15,670€", "Este mes"),
            ("Promedio Diario", "522€", "Últimos 30 días"),
            ("Mejor Día", "1,256€", "15 de Mayo"),
            ("Crecimiento", "+18%", "vs mes anterior"),
        ]

        for titulo, valor, periodo in metricas_data:
            card = self.create_metric_card(titulo, valor, periodo)
            metricas_layout.addWidget(card)

        layout.addLayout(metricas_layout)

        # Gráfico de tendencia de ventas
        tendencia_chart = self.create_tendencia_ventas_chart()
        layout.addWidget(tendencia_chart)

        # Tabla detallada de ventas
        ventas_table = self.create_ventas_detalle_table()
        layout.addWidget(ventas_table)

        self.tabs.addTab(tab, "💰 Ventas")

    def create_hospederia_tab(self) -> None:
        """Crea la pestaña de reportes de hospedería"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Métricas de hospedería
        hospederia_layout = QHBoxLayout()

        hospederia_data: List[Tuple[str, str, str]] = [
            ("Tasa de Ocupación", "78%", "Este mes"),
            ("Habitaciones Disponibles", "12/55", "Hoy"),
            ("Promedio Estancia", "2.3 días", "Este mes"),
            ("Ingresos por Habitación", "125€", "Promedio"),
        ]

        for titulo, valor, periodo in hospederia_data:
            card = self.create_metric_card(titulo, valor, periodo)
            hospederia_layout.addWidget(card)

        layout.addLayout(hospederia_layout)

        # Gráfico de ocupación por tipo de habitación
        ocupacion_tipo_chart = self.create_ocupacion_tipo_chart()
        layout.addWidget(ocupacion_tipo_chart)

        # Tabla de reservas
        reservas_table = self.create_reservas_table()
        layout.addWidget(reservas_table)

        self.tabs.addTab(tab, "🏨 Hospedería")

    def create_inventario_tab(self) -> None:
        """Crea la pestaña de reportes de inventario"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Métricas de inventario
        inventario_layout = QHBoxLayout()

        inventario_data: List[Tuple[str, str, str]] = [
            ("Valor Total Stock", "8,450€", "Actualizado"),
            ("Productos Críticos", "12", "Stock bajo"),
            ("Rotación Promedio", "15 días", "Este mes"),
            ("Productos Agotados", "3", "Requerido pedido"),
        ]

        for titulo, valor, periodo in inventario_data:
            card = self.create_metric_card(titulo, valor, periodo)
            inventario_layout.addWidget(card)

        layout.addLayout(inventario_layout)

        # Gráfico de productos más vendidos
        productos_chart = self.create_productos_vendidos_chart()
        layout.addWidget(productos_chart)

        # Tabla de stock crítico
        stock_table = self.create_stock_critico_table()
        layout.addWidget(stock_table)

        self.tabs.addTab(tab, "📦 Inventario")

    def create_financiero_tab(self) -> None:
        """Crea la pestaña de reportes financieros"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Métricas financieras
        financiero_layout = QHBoxLayout()

        financiero_data: List[Tuple[str, str, str]] = [
            ("Ingresos Totales", "18,920€", "Este mes"),
            ("Gastos Operativos", "12,450€", "Este mes"),
            ("Beneficio Neto", "6,470€", "Este mes"),
            ("Margen de Beneficio", "34.2%", "Este mes"),
        ]

        for titulo, valor, periodo in financiero_data:
            card = self.create_metric_card(titulo, valor, periodo)
            financiero_layout.addWidget(card)

        layout.addLayout(financiero_layout)

        # Gráfico de flujo de caja
        flujo_chart = self.create_flujo_caja_chart()
        layout.addWidget(flujo_chart)

        # Tabla de transacciones recientes
        transacciones_table = self.create_transacciones_table()
        layout.addWidget(transacciones_table)

        self.tabs.addTab(tab, "💵 Financiero")

    def create_kpi_card(self, titulo: str, valor: str, cambio: str, color: str) -> QFrame:
        """Crea una tarjeta de KPI"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel)
        card.setStyleSheet(
            f"""
            QFrame {{
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 20px;
                border-left: 4px solid {color};
            }}
        """
        )

        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        # Título
        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("color: #6b7280; font-size: 14px; font-weight: 500;")
        layout.addWidget(titulo_label)

        # Valor
        valor_label = QLabel(valor)
        valor_label.setStyleSheet("color: #1f2937; font-size: 28px; font-weight: bold;")
        layout.addWidget(valor_label)

        # Cambio
        cambio_label = QLabel(cambio)
        color_cambio: str = "#10b981" if cambio.startswith("+") else "#ef4444"
        cambio_label.setStyleSheet(
            f"color: {color_cambio}; font-size: 14px; font-weight: 600;"
        )
        layout.addWidget(cambio_label)

        return card

    def create_metric_card(self, titulo: str, valor: str, periodo: str) -> QFrame:
        """Crea una tarjeta de métrica"""
        card = QFrame()
        card.setFrameStyle(QFrame.Shape.StyledPanel)
        card.setStyleSheet(
            """
            QFrame {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
                padding: 15px;
            }
        """
        )

        layout = QVBoxLayout(card)
        layout.setSpacing(5)

        titulo_label = QLabel(titulo)
        titulo_label.setStyleSheet("color: #6b7280; font-size: 12px; font-weight: 500;")
        layout.addWidget(titulo_label)

        valor_label = QLabel(valor)
        valor_label.setStyleSheet("color: #1f2937; font-size: 20px; font-weight: bold;")
        layout.addWidget(valor_label)

        periodo_label = QLabel(periodo)
        periodo_label.setStyleSheet("color: #9ca3af; font-size: 11px;")
        layout.addWidget(periodo_label)

        return card

    def create_ventas_chart(self) -> QLabel:
        """Placeholder para el gráfico de ventas"""
        chart_placeholder = QLabel("Gráfico de Ventas (Placeholder)")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("font-size: 16px; color: #6b7280;")
        return chart_placeholder

    def create_ocupacion_chart(self) -> QLabel:
        """Placeholder para el gráfico de ocupación"""
        chart_placeholder = QLabel("Gráfico de Ocupación (Placeholder)")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("font-size: 16px; color: #6b7280;")
        return chart_placeholder

    def create_resumen_table(self) -> QLabel:
        """Placeholder para la tabla de resumen"""
        table_placeholder = QLabel("Tabla de Resumen (Placeholder)")
        table_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_placeholder.setStyleSheet("font-size: 16px; color: #6b7280;")
        return table_placeholder

    def create_tendencia_ventas_chart(self) -> QLabel:
        """Placeholder para el gráfico de tendencia de ventas"""
        chart_placeholder = QLabel("Gráfico de Tendencia de Ventas (Placeholder)")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("font-size: 16px; color: #6b7280;")
        return chart_placeholder

    def create_ventas_detalle_table(self) -> QTableWidget:
        """Crea la tabla detallada de ventas"""
        table = QTableWidget(10, 6)
        table.setHorizontalHeaderLabels(  # type: ignore
            ["Fecha", "Mesa/Habitación", "Total", "Método Pago", "Empleado", "Estado"]
        )

        # Datos ficticios
        import random

        datos_ejemplo: List[List[str]] = []
        for i in range(10):
            fecha = f"{random.randint(1, 30):02d}/05/2025"
            mesa = (
                f"Mesa {random.randint(1, 20)}"
                if random.choice([True, False])
                else f"Hab. {random.randint(101, 250)}"
            )
            total = f"{random.randint(25, 150)}€"
            metodo = random.choice(["Efectivo", "Tarjeta", "Transferencia"])
            empleado = random.choice(["Ana García", "Carlos López", "María Ruiz"])
            estado = random.choice(["Completado", "Pendiente", "Cancelado"])

            datos_ejemplo.append([fecha, mesa, total, metodo, empleado, estado])

        for i, fila in enumerate(datos_ejemplo):
            for j, valor in enumerate(fila):
                item = QTableWidgetItem(valor)
                if j == 5:  # Columna estado
                    if valor == "Completado":
                        item.setBackground(QColor("#dcfce7"))
                    elif valor == "Pendiente":
                        item.setBackground(QColor("#fef3c7"))
                    else:
                        item.setBackground(QColor("#fee2e2"))
                table.setItem(i, j, item)

        header = table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)

        return table

    def create_ocupacion_tipo_chart(self) -> QLabel:
        """Placeholder para el gráfico de ocupación por tipo"""
        chart_placeholder = QLabel("Gráfico de Ocupación por Tipo (Placeholder)")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("font-size: 16px; color: #6b7280;")
        return chart_placeholder

    def create_productos_vendidos_chart(self) -> QLabel:
        """Placeholder para el gráfico de productos vendidos"""
        chart_placeholder = QLabel("Gráfico de Productos Vendidos (Placeholder)")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("font-size: 16px; color: #6b7280;")
        return chart_placeholder

    def create_stock_critico_table(self) -> QLabel:
        """Placeholder para la tabla de stock crítico"""
        table_placeholder = QLabel("Tabla de Stock Crítico (Placeholder)")
        table_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        table_placeholder.setStyleSheet("font-size: 16px; color: #6b7280;")
        return table_placeholder

    def create_flujo_caja_chart(self) -> QLabel:
        """Placeholder para el gráfico de flujo de caja"""
        chart_placeholder = QLabel("Gráfico de Flujo de Caja (Placeholder)")
        chart_placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        chart_placeholder.setStyleSheet("font-size: 16px; color: #6b7280;")
        return chart_placeholder

    def create_transacciones_table(self) -> QTableWidget:
        """Crea la tabla de transacciones recientes"""
        table = QTableWidget(8, 5)
        table.setHorizontalHeaderLabels(  # type: ignore
            ["Fecha", "Concepto", "Tipo", "Importe", "Saldo"]
        )

        # Datos ficticios de transacciones
        datos_transacciones: List[List[str]] = [
            ["10/06/2025", "Venta TPV Mesa 5", "Ingreso", "+85€", "12,450€"],
            ["10/06/2025", "Compra Proveedor Alimentaria", "Gasto", "-320€", "12,365€"],
            ["09/06/2025", "Pago Habitación 205", "Ingreso", "+160€", "12,685€"],
            ["09/06/2025", "Mantenimiento Equipos", "Gasto", "-150€", "12,525€"],
            ["08/06/2025", "Venta TPV Mesa 12", "Ingreso", "+125€", "12,675€"],
            ["08/06/2025", "Salario Empleados", "Gasto", "-2,500€", "12,550€"],
            ["07/06/2025", "Reserva Suite Premium", "Ingreso", "+280€", "15,050€"],
            ["07/06/2025", "Suministros Limpieza", "Gasto", "-75€", "14,770€"],
        ]

        for i, fila in enumerate(datos_transacciones):
            for j, valor in enumerate(fila):
                item = QTableWidgetItem(valor)
                if j == 3:  # Columna importe
                    if valor.startswith("+"):
                        item.setForeground(QColor("#059669"))
                    else:
                        item.setForeground(QColor("#dc2626"))
                table.setItem(i, j, item)

        header = table.horizontalHeader()
        if header:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)

        return table

    def cambiar_periodo(self, periodo: str) -> None:
        """Cambia las fechas según el periodo seleccionado"""
        hoy = QDate.currentDate()

        if periodo == "Hoy":
            self.fecha_desde.setDate(hoy)
            self.fecha_hasta.setDate(hoy)
        elif periodo == "Ayer":
            ayer = hoy.addDays(-1)
            self.fecha_desde.setDate(ayer)
            self.fecha_hasta.setDate(ayer)
        elif periodo == "Última semana":
            self.fecha_desde.setDate(hoy.addDays(-7))
            self.fecha_hasta.setDate(hoy)
        elif periodo == "Último mes":
            self.fecha_desde.setDate(hoy.addDays(-30))
            self.fecha_hasta.setDate(hoy)
        elif periodo == "Últimos 3 meses":
            self.fecha_desde.setDate(hoy.addDays(-90))
            self.fecha_hasta.setDate(hoy)
        elif periodo == "Último año":
            self.fecha_desde.setDate(hoy.addDays(-365))
            self.fecha_hasta.setDate(hoy)

    def aplicar_filtros(self) -> None:
        """Aplica los filtros seleccionados"""
        start_date = self.start_date.date().toPyDate()
        end_date = self.end_date.date().toPyDate()
        logger.info(f"Aplicando filtros: {start_date} a {end_date}")
        QMessageBox.information(
            self,
            "Filtros Aplicados",
            f"Filtros aplicados de {start_date} a {end_date}.",
        )
        self.actualizar_datos()

    def actualizar_datos(self) -> None:
        """Actualiza todos los datos de los reportes"""
        logger.info("Actualizando datos de reportes...")
        # Aquí se implementaría la lógica para actualizar con datos reales

    def exportar_reporte(self) -> None:
        """Exporta el reporte actual"""
        tab_actual = self.tabs.currentIndex()
        nombres_tabs = ["Dashboard", "Ventas", "Hospedería", "Inventario", "Financiero"]

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            f"Exportar Reporte - {nombres_tabs[tab_actual]}",
            f"reporte_{nombres_tabs[tab_actual].lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "PDF Files (*.pdf);;Excel Files (*.xlsx);;CSV Files (*.csv)",
        )

        if file_path:
            try:
                # Simular exportación
                QMessageBox.information(
                    self,
                    "Exportación Completada",
                    f"Reporte exportado exitosamente a:\n{file_path}",
                )
                logger.info(f"Reporte exportado a: {file_path}")
            except Exception as e:
                logger.error(f"Error al exportar reporte: {e}")
                QMessageBox.critical(
                    self, "Error", f"Error al exportar el reporte:\n{str(e)}"
                )

    def cargar_datos_iniciales(self) -> None:
        """Carga los datos iniciales para los reportes"""
        logger.info("Cargando datos iniciales de reportes...")
        # Aquí se implementaría la carga inicial de datos

    def setup_ui(self) -> None:
        """Configura la interfaz del módulo"""
        # Header del módulo
        header = self.create_module_header()
        self.content_layout.addWidget(header)

        # Panel de filtros
        filtros_panel = self.create_filtros_panel()
        self.content_layout.addWidget(filtros_panel)

        # Crear tabs para diferentes tipos de reportes
        self.tabs: QTabWidget = QTabWidget()
        self.tabs.setStyleSheet(
            """
            QTabWidget::pane {
                border: 1px solid #e5e7eb;
                background: white;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #f9fafb;
                border: 1px solid #e5e7eb;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: 500;
            }
            QTabBar::tab:selected {
                background: white;
                border-bottom: 1px solid white;
                color: #8b5cf6;
            }
        """
        )  # Crear las diferentes pestañas de reportes
        self.create_dashboard_tab()
        self.content_layout.addWidget(self.tabs)

    def create_reservas_table(self) -> QTableWidget:
        """Crea la tabla de reservas"""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels(  # type: ignore
            ["ID", "Huésped", "Habitación", "Check-in", "Check-out", "Estado"]
        )

        # Datos de ejemplo
        reservas_data: List[List[str]] = [
            ["001", "Juan Pérez", "101", "2025-06-10", "2025-06-15", "Confirmada"],
            ["002", "María García", "205", "2025-06-11", "2025-06-13", "Check-in"],
            ["003", "Carlos López", "302", "2025-06-12", "2025-06-16", "Pendiente"],
        ]

        table.setRowCount(len(reservas_data))
        for i, reserva in enumerate(reservas_data):
            for j, dato in enumerate(reserva):
                table.setItem(i, j, QTableWidgetItem(str(dato)))

        header = table.horizontalHeader()
        if header is not None:
            header.setStretchLastSection(True)  # type: ignore
        return table
