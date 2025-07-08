"""
Widgets de gráficos para el Dashboard Admin v3
Diseño elegante de visualización de datos basado en Dashboard V2
"""

import logging
import random
from typing import List, Dict, Any, Optional
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QFrame, QSizePolicy, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QPen, QBrush, QColor, QLinearGradient
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class SimpleMetricChart(QWidget):
    """Widget elegante para mostrar gráficos de métricas estilo V2"""
    
    def __init__(self, title: str = "Métrica", color: str = "#3b82f6", parent=None):
        super().__init__(parent)
        self.title = title
        self.color = color
        self.data_points = []
        self.max_points = 15
        self.min_value = 0
        self.max_value = 100
        
        # Configuración del widget - Más grande para ocupar más espacio
        self.setMinimumSize(350, 220)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        # Generar datos iniciales
        self.generate_sample_data()
        
        # Estilo elegante sin propiedades no compatibles
        self.setStyleSheet(f"""
            SimpleMetricChart {{
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
            }}
            SimpleMetricChart:hover {{
                border-color: {self.color};
                border-width: 2px;
            }}
        """)
        
    def generate_sample_data(self):
        """Genera datos de muestra realistas"""
        base_value = random.randint(50, 80)
        for i in range(self.max_points):
            # Crear variación natural en los datos
            variation = random.randint(-10, 10)
            value = max(0, min(100, base_value + variation))
            self.data_points.append(value)
            base_value = value
            
        self.max_value = max(self.data_points) * 1.2
        self.min_value = min(self.data_points) * 0.8
        
    def add_data_point(self, value: float):
        """Añade un punto de datos al gráfico"""
        self.data_points.append(value)
        
        # Mantener solo los últimos N puntos
        if len(self.data_points) > self.max_points:
            self.data_points.pop(0)
            
        # Actualizar rango de valores
        if self.data_points:
            self.min_value = min(self.data_points) * 0.9
            self.max_value = max(self.data_points) * 1.1
            
        self.update()  # Redibujar
        
    def clear_data(self):
        """Limpia todos los datos del gráfico"""
        self.data_points.clear()
        self.update()
        
    def paintEvent(self, event):
        """Dibuja el gráfico con estilo elegante"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Área de dibujo
        rect = self.rect()
        margin = 20
        chart_rect = rect.adjusted(margin, margin * 2, -margin, -margin)
        
        # Fondo
        painter.fillRect(rect, QColor(255, 255, 255))
        
        # Título
        painter.setPen(QPen(QColor("#1e293b")))
        painter.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        title_rect = rect.adjusted(0, 5, 0, -rect.height() + 25)
        painter.drawText(title_rect, Qt.AlignmentFlag.AlignCenter, self.title)
        
        if not self.data_points:
            # Mensaje cuando no hay datos
            painter.setPen(QPen(QColor("#64748b")))
            painter.setFont(QFont("Segoe UI", 9))
            painter.drawText(chart_rect, Qt.AlignmentFlag.AlignCenter, "Sin datos")
            return
            
        # Dibujar línea de datos
        if len(self.data_points) > 1:
            # Preparar puntos
            points = []
            width = chart_rect.width()
            height = chart_rect.height()
            
            for i, value in enumerate(self.data_points):
                x = chart_rect.left() + (i / (len(self.data_points) - 1)) * width
                
                # Normalizar valor al rango del gráfico
                if self.max_value > self.min_value:
                    normalized = (value - self.min_value) / (self.max_value - self.min_value)
                else:
                    normalized = 0.5
                    
                y = chart_rect.bottom() - normalized * height
                points.append((x, y))
                
            # Dibujar línea
            painter.setPen(QPen(QColor(self.color), 3))
            for i in range(len(points) - 1):
                painter.drawLine(int(points[i][0]), int(points[i][1]), 
                               int(points[i+1][0]), int(points[i+1][1]))
                
            # Dibujar puntos
            painter.setBrush(QBrush(QColor(self.color)))
            painter.setPen(QPen(QColor("#ffffff"), 2))
            for x, y in points:
                painter.drawEllipse(int(x-4), int(y-4), 8, 8)
                
        # Dibujar grid ligero
        painter.setPen(QPen(QColor("#f1f5f9"), 1))
        
        # Líneas horizontales del grid
        for i in range(1, 4):
            y = chart_rect.top() + (i / 4) * chart_rect.height()
            painter.drawLine(chart_rect.left(), int(y), chart_rect.right(), int(y))


class DashboardChartsSection(QWidget):
    """Sección que contiene gráficos elegantes estilo V2"""
    
    charts_updated = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chart_widgets = {}
        self.setup_ui()
        
        # Timer para actualización automática
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_charts)
        self.update_timer.start(6000)  # Actualizar cada 6 segundos
        
    def setup_ui(self):
        """Configura la interfaz elegante de gráficos"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)
        
        # Título de la sección
        title_label = QLabel("Tendencias y Análisis")
        title_label.setStyleSheet("""
            color: #0f172a;
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 16px;
        """)
        layout.addWidget(title_label)
          # Grid de gráficos en 2x2 - Más espacioso
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)  # Más espacio entre gráficos
        charts_grid.setContentsMargins(0, 0, 0, 0)
        
        # Gráficos específicos del negocio
        chart_configs = [
            ("Ventas por Hora", "#10b981", "€"),
            ("Flujo de Clientes", "#3b82f6", "personas"),
            ("Tiempo de Servicio", "#f59e0b", "min"),
            ("Satisfacción", "#8b5cf6", "/5"),
        ]
        
        # Crear gráficos en grid 2x2
        for i, (title, color, unit) in enumerate(chart_configs):
            chart = SimpleMetricChart(title, color)
            self.chart_widgets[title.lower().replace(' ', '_')] = chart
            
            row = i // 2
            col = i % 2
            charts_grid.addWidget(chart, row, col)
        
        # Configurar stretch para distribución elegante - Filas también tienen stretch
        for col in range(2):
            charts_grid.setColumnStretch(col, 1)
        for row in range(2):
            charts_grid.setRowStretch(row, 1)            
        layout.addLayout(charts_grid)
        # No addStretch() para que los gráficos ocupen todo el espacio disponible
        
    def update_charts(self):
        """Actualiza todos los gráficos con datos simulados"""
        updates = {
            'ventas_por_hora': random.uniform(200, 400),
            'flujo_de_clientes': random.randint(15, 35),
            'tiempo_de_servicio': random.uniform(35, 55),
            'satisfacción': random.uniform(4.2, 4.9),        }
        
        for chart_key, chart in self.chart_widgets.items():
            if chart_key in updates:
                chart.add_data_point(updates[chart_key])
                
        # Emitir señal con los datos actualizados
        self.charts_updated.emit(updates)
        
    def update_metric(self, metric_name: str, value: float):
        """Actualiza un gráfico específico"""
        key = metric_name.lower().replace(' ', '_')
        if key in self.chart_widgets:
            self.chart_widgets[key].add_data_point(value)
            
    def get_chart_widgets(self):
        """Retorna el diccionario de widgets de gráficos"""
        return self.chart_widgets
