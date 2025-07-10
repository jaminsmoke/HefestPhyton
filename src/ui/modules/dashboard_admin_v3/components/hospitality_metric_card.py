"""
Tarjeta de métricas especializada para hostelería con datos reales
COMPLETAMENTE AUTO-GESTIONADA - Se conecta directamente al RealDataManager
"""

from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtCore import pyqtSignal, QTimer

from .dashboard_metric_components import UltraModernMetricCard
import logging

logger = logging.getLogger(__name__)


class HospitalityMetricCard(UltraModernMetricCard):
    """Tarjeta especializada para métricas hosteleras con datos reales - AUTO-GESTIONADA"""

    # Señal para cuando se actualiza la métrica
    metric_updated = pyqtSignal(str, dict)

    def __init__(
        self,
        metric_type,
        data_manager=None,
        title="",
        value="0",
        unit="",
        trend="+0.0%",
        target=None,
        metric_color=None,
        icon="",
        parent=None,
    ):

        # Configuración específica por tipo de métrica hostelera
        self.hospitality_config = {
            "ocupacion": {
                "title": "Ocupación de Habitaciones",
                "unit": "%",
                "icon": "🛏️",
                "target": 90,
                "color": "#3B82F6",  # blue-500
                "description": "Porcentaje de habitaciones ocupadas",
            },
            "ventas_diarias": {
                "title": "Ventas Diarias",
                "unit": "€",
                "icon": "💰",
                "target": 2500,
                "color": "#8B5CF6",  # purple-500
                "description": "Ingresos totales del día",
            },
            "coste_medio": {
                "title": "Coste Medio por Noche",
                "unit": "€/noche",
                "icon": "📊",
                "target": 85,
                "color": "#F59E0B",  # amber-500
                "description": "Precio promedio por habitación",
            },
            "satisfaccion": {
                "title": "Satisfacción del Cliente",
                "unit": "★",
                "icon": "⭐",
                "target": 4.8,
                "color": "#10B981",  # emerald-500
                "description": "Puntuación media de satisfacción",
            },
            "reservas_activas": {
                "title": "Reservas Activas",
                "unit": "",
                "icon": "📅",
                "target": 35,
                "color": "#14B8A6",  # teal-500
                "description": "Reservas confirmadas actualmente",
            },
            "tiempo_espera": {
                "title": "Tiempo de Espera",
                "unit": "min",
                "icon": "⏱️",
                "target": 5,
                "color": "#F59E0B",  # amber-500
                "description": "Tiempo promedio de espera en recepción",
            },
            "mesas_ocupadas": {
                "title": "Mesas Ocupadas",
                "unit": "/24",
                "icon": "🪑",
                "target": 22,
                "color": "#6366F1",  # indigo-500
                "description": "Mesas ocupadas en el restaurante",
            },
            "comandas_activas": {
                "title": "Comandas Activas",
                "unit": "",
                "icon": "📋",
                "target": 12,
                "color": "#EC4899",  # pink-500
                "description": "Órdenes pendientes en cocina",
            },
            # Nuevas métricas hosteleras
            "ticket_promedio": {
                "title": "Ticket Promedio",
                "unit": "€",
                "icon": "🧾",
                "target": 28,
                "color": "#8B5CF6",  # purple-500
                "description": "Gasto promedio por cliente",
            },
            "rotacion_mesas": {
                "title": "Rotación de Mesas",
                "unit": "veces",
                "icon": "🔄",
                "target": 3.5,
                "color": "#6366F1",  # indigo-500
                "description": "Veces que se ocupa cada mesa",
            },
            "inventario_bebidas": {
                "title": "Stock de Bebidas",
                "unit": "%",
                "icon": "🍺",
                "target": 95,
                "color": "#F59E0B",  # amber-500
                "description": "Nivel de inventario de bebidas",
            },
            "margen_bruto": {
                "title": "Margen Bruto",
                "unit": "%",
                "icon": "📈",
                "target": 70,
                "color": "#10B981",  # emerald-500
                "description": "Margen de beneficio bruto",
            },
        }

        self.metric_type = metric_type
        self.config = self.hospitality_config.get(
            metric_type,
            {
                "title": title,
                "unit": unit,
                "icon": icon,
                "target": target,
                "color": metric_color or "#3B82F6",
                "description": f"Métrica de {title}",
            },
        )

        # Inicializar la tarjeta base con los datos de configuración
        super().__init__(
            title=self.config["title"],
            value=value,
            unit=self.config["unit"],
            trend=trend,
            target=str(self.config.get("target", 0)),
            metric_type="info",  # Tipo base
            icon=self.config["icon"],
            parent=parent,
        )

        # AUTO-GESTIÓN: Configuración del data manager
        self.data_manager = data_manager
        self.auto_refresh_enabled = True

        # Timer para auto-actualización (independiente del dashboard)
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.auto_refresh_data)

        # Si tenemos data_manager, conectarnos a sus señales
        if self.data_manager:
            self.data_manager.metric_updated.connect(self.on_metric_data_updated)
            self.data_manager.data_updated.connect(self.on_all_data_updated)
            # logger.debug(f"Tarjeta {metric_type} conectada al RealDataManager")

        self.setup_hospitality_features()

        # Iniciar auto-actualización si hay data manager
        if self.data_manager and self.auto_refresh_enabled:
            self.start_auto_refresh()

        # logger.debug(
        #     f"HospitalityMetricCard creada para {metric_type} - Auto-gestionada: {bool(self.data_manager)}"
        # )

    def start_auto_refresh(self, interval_ms=3000):
        """Iniciar actualización automática de datos"""
        if self.data_manager and not self.refresh_timer.isActive():
            self.refresh_timer.start(interval_ms)
            self.auto_refresh_data()  # Primera actualización inmediata
            # logger.debug(
            #     f"Auto-refresh iniciado para {self.metric_type} cada {interval_ms}ms"
            # )

    def stop_auto_refresh(self):
        """Detener actualización automática"""
        if self.refresh_timer.isActive():
            self.refresh_timer.stop()
            # logger.debug(f"Auto-refresh detenido para {self.metric_type}")

    def auto_refresh_data(self):
        """Actualización automática de datos desde el RealDataManager"""
        if not self.data_manager or not self.auto_refresh_enabled:
            return

        try:
            # Obtener datos actualizados para esta métrica específica
            self.data_manager.fetch_all_real_data()
            cache = getattr(self.data_manager, "_data_cache", {})

            # Buscar datos para esta métrica
            metric_data = cache.get(self.metric_type, {})

            if metric_data:
                self.update_from_real_data(metric_data)
                # logger.debug(
                #     f"Datos auto-actualizados para {self.metric_type}: {metric_data}"
                # )

        except Exception as e:
            logger.error(f"Error en auto-refresh de {self.metric_type}: {e}")

    def on_metric_data_updated(self, metric_name, metric_data):
        """Callback cuando el RealDataManager actualiza datos de métricas"""
        if metric_name == self.metric_type:
            self.update_from_real_data(metric_data)

    def on_all_data_updated(self, all_data):
        """Callback cuando el RealDataManager actualiza todos los datos"""
        metric_data = all_data.get(self.metric_type, {})
        if metric_data:
            self.update_from_real_data(metric_data)

    def update_from_real_data(self, metric_data):
        """Actualizar la tarjeta usando datos reales del RealDataManager"""
        try:
            value = metric_data.get("value", self.value)
            trend = metric_data.get("trend", self.trend)
            target = metric_data.get("target", self.target)

            # Actualizar usando el método especializado de hostelería
            self.update_metric_data(value, trend, metric_data)

            # logger.debug(
            #     f"Métrica {self.metric_type} actualizada desde datos reales: {value}"
            # )

        except Exception as e:
            logger.error(
                f"Error actualizando {self.metric_type} desde datos reales: {e}"
            )

        self.setup_hospitality_features()

    def setup_hospitality_features(self):
        """Configurar características específicas de hostelería"""

        # Agregar barra de progreso si hay objetivo
        if "target" in self.config and self.config["target"]:
            self.add_progress_bar()

        # Aplicar color específico de la métrica
        self.apply_hospitality_styling()

        # Agregar tooltip con descripción
        self.setToolTip(self.config.get("description", ""))

    def add_progress_bar(self):
        """Agregar barra de progreso para métricas con objetivo"""
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(6)

        # Estilo de la barra de progreso
        progress_style = f"""
            QProgressBar {{
                background: #E5E7EB;
                border-radius: 3px;
                border: none;
            }}
            QProgressBar::chunk {{
                background: {self.config['color']};
                border-radius: 3px;
            }}
        """
        self.progress_bar.setStyleSheet(progress_style)

        # Agregar la barra al layout principal
        self.main_layout.addWidget(self.progress_bar)

    def apply_hospitality_styling(self):
        """Aplicar estilo específico de hostelería"""
        # Borde lateral con color de la métrica
        hospitality_style = f"""
            HospitalityMetricCard {{
                border-left: 4px solid {self.config['color']};
                border-radius: 12px;
                background: white;
                margin: 2px;
            }}
            HospitalityMetricCard:hover {{
                border-left: 6px solid {self.config['color']};
                background: #F9FAFB;
            }}        """
        self.setStyleSheet(hospitality_style)

    def update_metric_data(self, value, trend=None, additional_data=None):
        """Actualizar datos de la métrica con información específica de hostelería"""
        try:
            # Usar el método de la clase base que ya maneja la lógica básica
            super().update_metric_data(value=value, trend=trend)

            # Aplicar lógica específica de hostelería
            if trend is not None and isinstance(trend, (int, float)):
                self.trend = f"{'+' if trend >= 0 else ''}{trend:.1f}%"
                if hasattr(self, "trend_label"):
                    self.trend_label.setText(self.trend)

            # Actualizar barra de progreso específica de hostelería si existe
            if hasattr(self, "progress_bar") and "target" in self.config:
                target = self.config["target"]
                if target > 0:
                    try:
                        # Convertir valor a float para cálculo
                        numeric_value = float(
                            str(value).replace(",", "").replace("€", "").strip()
                        )
                        progress_value = min(100, int((numeric_value / target) * 100))
                        self.progress_bar.setValue(progress_value)
                    except (ValueError, TypeError):
                        self.progress_bar.setValue(0)

            # Emitir señal específica de hostelería
            self.metric_updated.emit(
                self.metric_type,
                {
                    "value": value,
                    "trend": self.trend,
                    "target": self.config.get("target"),
                    "config": self.config,
                    "additional_data": additional_data or {},
                },
            )

            # logger.debug(f"Métrica hostelera {self.metric_type} actualizada: {value}")

        except Exception as e:
            logger.error(
                f"Error actualizando métrica hostelera {self.metric_type}: {e}"
            )

    def get_metric_info(self):
        """Obtener información completa de la métrica"""
        return {
            "type": self.metric_type,
            "title": self.config["title"],
            "value": self.value,
            "unit": self.config["unit"],
            "trend": self.trend,
            "target": self.config.get("target"),
            "color": self.config["color"],
            "icon": self.config["icon"],
            "description": self.config.get("description"),
            "progress": (
                self.progress_bar.value()
                if hasattr(self, "progress_bar") and self.progress_bar
                else None
            ),
        }

    def set_target(self, new_target):
        """Actualizar objetivo de la métrica"""
        self.config["target"] = new_target
        if hasattr(self, "progress_bar"):
            # Recalcular progreso con nuevo objetivo
            self.update_metric_data(self.value)

        logger.info(f"Objetivo actualizado para {self.metric_type}: {new_target}")

    def is_target_achieved(self):
        """Verificar si se ha alcanzado el objetivo"""
        if "target" not in self.config:
            return None

        try:
            numeric_value = float(
                str(self.value).replace(",", "").replace("€", "").strip()
            )
            target = self.config["target"]

            # Para métricas donde menor es mejor (tiempo_espera)
            if self.metric_type in ["tiempo_espera"]:
                return numeric_value <= target
            else:
                return numeric_value >= target

        except (ValueError, TypeError):
            return False

    def get_performance_status(self):
        """Obtener estado de rendimiento de la métrica"""
        if not self.is_target_achieved():
            return "below_target"

        try:
            numeric_value = float(
                str(self.value).replace(",", "").replace("€", "").strip()
            )
            target = self.config["target"]

            if numeric_value >= target * 1.1:  # 10% por encima del objetivo
                return "excellent"
            elif numeric_value >= target:
                return "good"
            else:
                return "needs_improvement"

        except (ValueError, TypeError):
            return "unknown"

    def cleanup(self):
        """Limpiar recursos y desconectar señales"""
        try:
            self.stop_auto_refresh()

            if self.data_manager:
                # Desconectar señales del data manager
                self.data_manager.metric_updated.disconnect(self.on_metric_data_updated)
                self.data_manager.data_updated.disconnect(self.on_all_data_updated)
                # logger.debug(
                #     f"Tarjeta {self.metric_type} desconectada del RealDataManager"
                # )

        except Exception as e:
            logger.warning(f"Error en cleanup de {self.metric_type}: {e}")

    def __del__(self):
        """Destructor para asegurar limpieza de recursos"""
        try:
            self.cleanup()
        except:
            pass  # Evitar errores en destructor
