"""
DataManager para SOLO datos reales - Versión con tendencias económicas-administrativas
Configuración inicial: todos los valores en cero (estado real del sistema)
"""

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from typing import Dict, Any, Optional, Tuple
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class RealDataManager(QObject):
    """Manager centralizado para gestión SOLO de datos reales del dashboard"""

    # Señales para comunicación
    data_updated = pyqtSignal(dict)
    metric_updated = pyqtSignal(str, dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, db_manager=None, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.is_running = False

        # Timer para actualizaciones
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.fetch_all_real_data)

        # Cache
        self._data_cache: Dict[str, Any] = {}
        self._last_update: Optional[datetime] = None

        logger.info("RealDataManager inicializado - Estado: Configuración inicial")

    def start_monitoring(self, interval_ms: int = 5000):
        """Inicia el monitoreo de datos reales"""
        if self.is_running:
            return

        self.update_timer.start(interval_ms)
        self.is_running = True
        self.fetch_all_real_data()

        logger.info(f"RealDataManager iniciado - Intervalo: {interval_ms}ms")

    def stop_monitoring(self):
        """Detiene el monitoreo"""
        if self.is_running:
            self.update_timer.stop()
            self.is_running = False
            logger.info("RealDataManager detenido")

    def fetch_all_real_data(self):
        """Obtiene datos reales de la BD"""
        try:
            data = self._get_real_metrics_formatted()

            self._data_cache.update(data)
            self._last_update = datetime.now()

            self.data_updated.emit(data)

            for metric_name, metric_data in data.items():
                self.metric_updated.emit(metric_name, metric_data)

            logger.debug(f"Datos reales actualizados: {len(data)} métricas")

        except Exception as e:
            error_msg = f"Error obteniendo datos reales: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)

    def _get_real_metrics_formatted(self) -> Dict[str, Dict[str, Any]]:
        """Obtener métricas reales formateadas para el dashboard"""

        # Obtener métricas reales de la BD
        raw_metrics = self._get_raw_hospitality_metrics()

        # Configuración de formato
        config = {
            "ocupacion_mesas": {"title": "Ocupación Mesas", "unit": "%", "icon": "🍽️"},
            "ventas_diarias": {"title": "Ventas Diarias", "unit": "€", "icon": "💰"},
            "comandas_activas": {"title": "Comandas Activas", "unit": "", "icon": "📋"},
            "ticket_promedio": {"title": "Ticket Promedio", "unit": "€", "icon": "🧾"},
            "reservas_futuras": {"title": "Reservas Futuras", "unit": "", "icon": "📅"},
            "mesas_ocupadas": {
                "title": "Mesas Ocupadas",
                "unit": raw_metrics.get("_total_tables_text", "/0"),
                "icon": "🪑",
            },
            "habitaciones_libres": {
                "title": "Habitaciones Libres",
                "unit": raw_metrics.get("_total_rooms_text", "/0"),
                "icon": "🛏️",
            },
            "productos_stock": {
                "title": "Productos en Stock",
                "unit": "",
                "icon": "📦",
            },
            "satisfaccion_cliente": {
                "title": "Satisfacción Cliente",
                "unit": "⭐",
                "icon": "⭐",
            },
            "tiempo_servicio": {"title": "Tiempo Servicio", "unit": "min", "icon": "⏱️"},
            "rotacion_mesas": {
                "title": "Rotación Mesas",
                "unit": "veces",
                "icon": "🔄",
            },
            "inventario_bebidas": {
                "title": "Inventario Bebidas",
                "unit": "%",
                "icon": "🥤",
            },
            "margen_bruto": {"title": "Margen Bruto", "unit": "%", "icon": "📊"},
        }

        # Formatear datos con tendencias reales
        formatted_data = {}
        for metric_name, metric_config in config.items():
            value = raw_metrics.get(metric_name, 0)

            # Calcular tendencia real basada en datos históricos
            trend_text, trend_numeric = self._calculate_real_trend(
                metric_name, float(value)
            )

            formatted_data[metric_name] = {
                "value": value,
                "trend": trend_text,
                "trend_numeric": trend_numeric,
                "title": metric_config["title"],
                "unit": metric_config["unit"],
                "format_type": (
                    "currency"
                    if "€" in metric_config["unit"]
                    else "percentage" if "%" in metric_config["unit"] else "number"
                ),
                "icon": metric_config["icon"],
                "timestamp": datetime.now().isoformat(),
                "source": "real_database" if self.db_manager else "initial_config",
            }

        return formatted_data

    def _calculate_real_trend(
        self, metric_name: str, current_value: float
    ) -> Tuple[str, float]:
        """Calcular tendencia real basada en datos históricos de la BD"""
        if not self.db_manager or current_value == 0:
            return "+0.0%", 0.0

        try:
            # Obtener valor del mismo período anterior (24 horas antes)
            previous_value = self._get_historical_metric_value(metric_name)

            if previous_value is None or previous_value == 0:
                return "+0.0%", 0.0

            # Calcular tendencia porcentual
            trend_numeric = ((current_value - previous_value) / previous_value) * 100

            # Formatear con lógica económica
            if abs(trend_numeric) < 0.1:
                trend_text = "±0.0%"
            elif trend_numeric > 0:
                trend_text = f"+{trend_numeric:.1f}%"
            else:
                trend_text = f"{trend_numeric:.1f}%"

            return trend_text, trend_numeric

        except Exception as e:
            logger.debug(f"Error calculando tendencia para {metric_name}: {e}")
            return "+0.0%", 0.0

    def _get_historical_metric_value(self, metric_name: str) -> Optional[float]:
        """Obtener valor histórico de una métrica (24h antes)"""
        if not self.db_manager:
            return None

        try:
            # Mapeo de métricas a consultas históricas con lógica económica-administrativa
            historical_queries = {
                "ventas_diarias": """
                    SELECT COALESCE(SUM(total), 0) 
                    FROM comandas 
                    WHERE DATE(fecha_hora) = DATE('now', '-1 day')
                """,
                "comandas_activas": """
                    SELECT COUNT(*) 
                    FROM comandas 
                    WHERE estado IN ('pendiente', 'en_preparacion')
                    AND datetime(fecha_hora) BETWEEN datetime('now', '-25 hours') 
                                                 AND datetime('now', '-23 hours')
                """,
                "ticket_promedio": """
                    SELECT COALESCE(AVG(total), 0) 
                    FROM comandas 
                    WHERE DATE(fecha_hora) = DATE('now', '-1 day') AND total > 0
                """,
                "reservas_futuras": """
                    SELECT COUNT(*) 
                    FROM reservas 
                    WHERE estado='confirmada' 
                    AND DATE(fecha_entrada) >= DATE('now', '-1 day')
                    AND created_at <= datetime('now', '-1 day')
                """,
                "ocupacion_mesas": """
                    SELECT COALESCE(
                        (CAST((SELECT COUNT(*) FROM mesas WHERE estado='ocupada') AS FLOAT) / 
                         NULLIF((SELECT COUNT(*) FROM mesas), 0)) * 100, 0
                    )
                """,
                "mesas_ocupadas": """
                    SELECT COUNT(*) FROM mesas WHERE estado='ocupada'
                """,
                "habitaciones_libres": """
                    SELECT COUNT(*) FROM habitaciones WHERE estado='libre'
                """,
                "productos_stock": """
                    SELECT COUNT(*) FROM productos WHERE stock > 0
                """,
                "satisfaccion_cliente": """
                    SELECT COALESCE(AVG(CAST(valoracion AS FLOAT)), 0) 
                    FROM comandas 
                    WHERE valoracion IS NOT NULL 
                    AND DATE(fecha_hora) = DATE('now', '-1 day')
                """,
                "tiempo_servicio": """
                    SELECT COALESCE(AVG(
                        CASE 
                            WHEN tiempo_servicio IS NOT NULL THEN tiempo_servicio
                            ELSE (strftime('%s', fecha_completado) - strftime('%s', fecha_hora)) / 60
                        END
                    ), 0)
                    FROM comandas 
                    WHERE estado = 'completada'
                    AND DATE(fecha_hora) = DATE('now', '-1 day')
                """,
                "rotacion_mesas": """
                    SELECT COALESCE(
                        (SELECT COUNT(*) FROM comandas WHERE DATE(fecha_hora) = DATE('now', '-1 day')) /
                        NULLIF((SELECT COUNT(*) FROM mesas), 0)
                    , 0)
                """,
                "inventario_bebidas": """
                    SELECT COALESCE(
                        (CAST(SUM(stock) AS FLOAT) / NULLIF(SUM(stock_minimo), 0)) * 100, 0
                    )
                    FROM productos 
                    WHERE categoria = 'Bebidas' OR nombre LIKE '%bebida%' OR nombre LIKE '%refresco%'
                """,
                "margen_bruto": """
                    SELECT COALESCE(
                        ((SUM(total) - SUM(costo_ingredientes)) / NULLIF(SUM(total), 0)) * 100, 0
                    )
                    FROM comandas 
                    WHERE DATE(fecha_hora) = DATE('now', '-1 day') AND total > 0
                """,
            }

            query = historical_queries.get(metric_name)
            if query:
                result = self._safe_query(query, 0.0)
                return float(result) if result is not None else None

            return None

        except Exception as e:
            logger.debug(f"Error obteniendo datos históricos de {metric_name}: {e}")
            return None

    def _get_raw_hospitality_metrics(self) -> Dict[str, Any]:
        """Obtener métricas sin formato desde la BD"""
        if not self.db_manager:
            logger.info("Sin BD - Devolviendo configuración inicial (ceros)")
            return self._get_initial_config_metrics()

        try:
            metrics = {}

            # MESAS
            total_tables = self._safe_query("SELECT COUNT(*) FROM mesas", 0)
            if total_tables > 0:
                occupied_tables = self._safe_query(
                    "SELECT COUNT(*) FROM mesas WHERE estado='ocupada'", 0
                )
                metrics["ocupacion_mesas"] = round(
                    (occupied_tables / total_tables) * 100, 1
                )
                metrics["mesas_ocupadas"] = occupied_tables
                metrics["_total_tables_text"] = f"/{total_tables}"
            else:
                metrics["ocupacion_mesas"] = 0.0
                metrics["mesas_ocupadas"] = 0
                metrics["_total_tables_text"] = "/0"

            # VENTAS
            daily_sales = self._safe_query(
                "SELECT COALESCE(SUM(total), 0) FROM comandas WHERE DATE(fecha_hora) = DATE('now')",
                0.0,
            )
            metrics["ventas_diarias"] = float(daily_sales)

            # COMANDAS
            active_orders = self._safe_query(
                "SELECT COUNT(*) FROM comandas WHERE estado IN ('pendiente', 'en_preparacion')",
                0,
            )
            metrics["comandas_activas"] = int(active_orders)

            # TICKET PROMEDIO
            avg_ticket = self._safe_query(
                "SELECT COALESCE(AVG(total), 0) FROM comandas WHERE DATE(fecha_hora) = DATE('now') AND total > 0",
                0.0,
            )
            metrics["ticket_promedio"] = round(float(avg_ticket), 2)

            # RESERVAS
            future_reservations = self._safe_query(
                "SELECT COUNT(*) FROM reservas WHERE estado='confirmada' AND DATE(fecha_entrada) >= DATE('now')",
                0,
            )
            metrics["reservas_futuras"] = int(future_reservations)

            # HABITACIONES
            total_rooms = self._safe_query("SELECT COUNT(*) FROM habitaciones", 0)
            if total_rooms > 0:
                free_rooms = self._safe_query(
                    "SELECT COUNT(*) FROM habitaciones WHERE estado='libre'", 0
                )
                metrics["habitaciones_libres"] = int(free_rooms)
                metrics["_total_rooms_text"] = f"/{total_rooms}"
            else:
                metrics["habitaciones_libres"] = 0
                metrics["_total_rooms_text"] = "/0"

            # PRODUCTOS
            products_in_stock = self._safe_query(
                "SELECT COUNT(*) FROM productos WHERE stock > 0", 0
            )
            metrics["productos_stock"] = int(products_in_stock)

            # SATISFACCIÓN CLIENTE
            satisfaction = self._safe_query(
                "SELECT COALESCE(AVG(CAST(valoracion AS FLOAT)), 0) FROM comandas WHERE valoracion IS NOT NULL AND DATE(fecha_hora) = DATE('now')",
                0.0,
            )
            metrics["satisfaccion_cliente"] = round(float(satisfaction), 1)

            # TIEMPO SERVICIO
            service_time = self._safe_query(
                """SELECT COALESCE(AVG(
                    CASE 
                        WHEN tiempo_servicio IS NOT NULL THEN tiempo_servicio
                        ELSE (strftime('%s', fecha_completado) - strftime('%s', fecha_hora)) / 60
                    END
                ), 0) FROM comandas WHERE estado = 'completada' AND DATE(fecha_hora) = DATE('now')""",
                0.0,
            )
            metrics["tiempo_servicio"] = round(float(service_time), 1)

            # ROTACIÓN MESAS
            if total_tables > 0:
                table_rotation = (
                    self._safe_query(
                        "SELECT COALESCE(COUNT(*), 0) FROM comandas WHERE DATE(fecha_hora) = DATE('now')",
                        0,
                    )
                    / total_tables
                )
            else:
                table_rotation = 0.0
            metrics["rotacion_mesas"] = round(float(table_rotation), 1)

            # INVENTARIO BEBIDAS
            beverages_inventory = self._safe_query(
                """SELECT COALESCE(
                    (CAST(SUM(stock) AS FLOAT) / NULLIF(SUM(stock_minimo), 0)) * 100, 0
                ) FROM productos WHERE categoria = 'Bebidas' OR nombre LIKE '%bebida%' OR nombre LIKE '%refresco%'""",
                0.0,
            )
            metrics["inventario_bebidas"] = round(float(beverages_inventory), 1)

            # MARGEN BRUTO
            gross_margin = self._safe_query(
                """SELECT COALESCE(
                    ((SUM(total) - SUM(costo_ingredientes)) / NULLIF(SUM(total), 0)) * 100, 0
                ) FROM comandas WHERE DATE(fecha_hora) = DATE('now') AND total > 0""",
                0.0,
            )
            metrics["margen_bruto"] = round(float(gross_margin), 1)

            # Log del estado
            config_status = (
                "✅ CON DATOS"
                if any(v > 0 for k, v in metrics.items() if not k.startswith("_"))
                else "📋 CONFIGURACIÓN INICIAL"
            )
            logger.info(f"Estado del establecimiento: {config_status}")

            return metrics

        except Exception as e:
            logger.error(f"Error obteniendo métricas reales: {e}")
            return self._get_initial_config_metrics()

    def _get_initial_config_metrics(self) -> Dict[str, Any]:
        """Métricas de configuración inicial (todo en cero)"""
        return {
            "ocupacion_mesas": 0.0,
            "ventas_diarias": 0.0,
            "comandas_activas": 0,
            "ticket_promedio": 0.0,
            "reservas_futuras": 0,
            "mesas_ocupadas": 0,
            "habitaciones_libres": 0,
            "productos_stock": 0,
            "satisfaccion_cliente": 0.0,
            "tiempo_servicio": 0.0,
            "rotacion_mesas": 0.0,
            "inventario_bebidas": 0.0,
            "margen_bruto": 0.0,
            "_total_tables_text": "/0",
            "_total_rooms_text": "/0",
        }

    def _safe_query(self, query: str, default_value: Any) -> Any:
        """Ejecutar consulta de BD de forma segura"""
        try:
            if not self.db_manager:
                return default_value
            result = self.db_manager.query(query)
            if result and len(result) > 0:
                return result[0][0]
            return default_value
        except Exception as e:
            logger.debug(f"Query falló (normal en config inicial): {e}")
            return default_value

    def get_last_update(self) -> Optional[datetime]:
        """Timestamp de última actualización"""
        return self._last_update

    def force_refresh(self):
        """Forzar actualización inmediata"""
        logger.info("Actualización forzada de datos reales")
        self.fetch_all_real_data()
