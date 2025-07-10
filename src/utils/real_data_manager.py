"""
DataManager para SOLO datos reales - Versión con tendencias económicas-administrativas
Configuración inicial: todos los valores en cero (estado real del sistema)
"""

from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from typing import Dict, Any, Optional, Tuple
import logging
from datetime import datetime

_ = logging.getLogger(__name__)


class RealDataManager(QObject):
    """Manager centralizado para gestión SOLO de datos reales del dashboard"""

    # Señales para comunicación
    _ = pyqtSignal(dict)
    metric_updated = pyqtSignal(str, dict)
    _ = pyqtSignal(str)

    def __init__(self, db_manager=None, parent=None):
        """TODO: Add docstring"""
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
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Inicia el monitoreo de datos reales"""
        if self.is_running:
            return

        self.update_timer.start(interval_ms)
        self.is_running = True
        self.fetch_all_real_data()

        logger.info("RealDataManager iniciado - Intervalo: %sms", interval_ms)

    def stop_monitoring(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Detiene el monitoreo"""
        if self.is_running:
            self.update_timer.stop()
            self.is_running = False
            logger.info("RealDataManager detenido")

    def fetch_all_real_data(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene datos reales de la BD"""
        try:
            data = self._get_real_metrics_formatted()

            self._data_cache.update(data)
            self._last_update = datetime.now()

            self.data_updated.emit(data)

            for metric_name, metric_data in data.items():
                self.metric_updated.emit(metric_name, metric_data)

            # logger.debug("Datos reales actualizados: %s métricas", len(data))

        except Exception as e:
            error_msg = f"Error obteniendo datos reales: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)

    def _get_real_metrics_formatted(self) -> Dict[str, Dict[str, Any]]:
        """Obtener métricas reales formateadas para el dashboard"""

        # Obtener métricas reales de la BD
        _ = self._get_raw_hospitality_metrics()

        # Configuración de formato
        _ = {
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
        _ = {}
        for metric_name, metric_config in config.items():
            _ = raw_metrics.get(metric_name, 0)

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
            _ = ((current_value - previous_value) / previous_value) * 100

            # Formatear con lógica económica
            if abs(trend_numeric) < 0.1:
                _ = "±0.0%"
            elif trend_numeric > 0:
                _ = f"+{trend_numeric:.1f}%"
            else:
                trend_text = f"{trend_numeric:.1f}%"

            return trend_text, trend_numeric

        except Exception as e:
            # logger.debug("Error calculando tendencia para {metric_name}: %s", e)
            return "+0.0%", 0.0

    def _get_historical_metric_value(self, metric_name: str) -> Optional[float]:
        """Obtener valor histórico de una métrica (24h antes)"""
        if not self.db_manager:
            return None

        try:
            # Mapeo de métricas a consultas históricas con lógica económica-administrativa
            _ = {
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
            # logger.debug("Error obteniendo datos históricos de {metric_name}: %s", e)
            return None

    def _get_raw_hospitality_metrics(self) -> Dict[str, Any]:
        """Obtener métricas sin formato desde la BD - Optimizado con single batch query"""
        if not self.db_manager:
            logger.info("Sin BD - Devolviendo configuración inicial (ceros)")
            return self._get_initial_config_metrics()

        try:
            # Single optimized batch query para todas las métricas
            _ = self.db_manager.query("""
                WITH daily_data AS (
                    SELECT 
                        COALESCE(SUM(total), 0) as ventas_diarias,
                        COUNT(CASE WHEN estado IN ('pendiente', 'en_preparacion') THEN 1 END) as comandas_activas,
                        COALESCE(AVG(CASE WHEN total > 0 THEN total END), 0) as ticket_promedio,
                        COUNT(*) as total_comandas_hoy,
                        COALESCE(AVG(CASE WHEN valoracion IS NOT NULL THEN CAST(valoracion AS FLOAT) END), 0) as satisfaccion_cliente,
                        COALESCE(AVG(CASE WHEN estado = 'completada' THEN 
                            COALESCE(tiempo_servicio, (strftime('%s', fecha_completado) - strftime('%s', fecha_hora)) / 60)
                        END), 0) as tiempo_servicio,
                        COALESCE(((SUM(CASE WHEN total > 0 THEN total - costo_ingredientes ELSE 0 END) / 
                                  NULLIF(SUM(CASE WHEN total > 0 THEN total ELSE 0 END), 0)) * 100), 0) as margen_bruto
                    FROM comandas 
                    WHERE DATE(fecha_hora) = DATE('now')
                ),
                mesa_data AS (
                    SELECT 
                        COUNT(*) as total_mesas,
                        COUNT(CASE WHEN estado='ocupada' THEN 1 END) as mesas_ocupadas
                    FROM mesas
                ),
                other_data AS (
                    SELECT 
                        (SELECT COUNT(*) FROM reservas WHERE estado='confirmada' AND DATE(fecha_entrada) >= DATE('now')) as reservas_futuras,
                        (SELECT COUNT(*) FROM habitaciones) as total_habitaciones,
                        (SELECT COUNT(*) FROM habitaciones WHERE estado='libre') as habitaciones_libres,
                        (SELECT COUNT(*) FROM productos WHERE stock > 0) as productos_stock,
                        (SELECT COALESCE((CAST(SUM(stock) AS FLOAT) / NULLIF(SUM(stock_minimo), 0)) * 100, 0) 
                         FROM productos WHERE categoria = 'Bebidas' OR nombre LIKE '%bebida%' OR nombre LIKE '%refresco%') as inventario_bebidas
                )
                SELECT 
                    d.ventas_diarias, d.comandas_activas, d.ticket_promedio, d.total_comandas_hoy,
                    d.satisfaccion_cliente, d.tiempo_servicio, d.margen_bruto,
                    m.total_mesas, m.mesas_ocupadas,
                    o.reservas_futuras, o.total_habitaciones, o.habitaciones_libres, 
                    o.productos_stock, o.inventario_bebidas
                FROM daily_data d, mesa_data m, other_data o
            """)
            
            if not result or len(result) == 0:
                return self._get_initial_config_metrics()
                
            _ = result[0]
            
            # Procesar resultados del batch query
            _ = int(row[7])
            occupied_tables = int(row[8])
            _ = int(row[10])
            
            metrics = {
                "ventas_diarias": float(row[0]),
                "comandas_activas": int(row[1]),
                "ticket_promedio": round(float(row[2]), 2),
                "satisfaccion_cliente": round(float(row[4]), 1),
                "tiempo_servicio": round(float(row[5]), 1),
                "margen_bruto": round(float(row[6]), 1),
                "mesas_ocupadas": occupied_tables,
                "ocupacion_mesas": round((occupied_tables / max(total_tables, 1)) * 100, 1),
                "_total_tables_text": f"/{total_tables}",
                "reservas_futuras": int(row[9]),
                "habitaciones_libres": int(row[11]),
                "_total_rooms_text": f"/{total_rooms}",
                "productos_stock": int(row[12]),
                "inventario_bebidas": round(float(row[13]), 1),
                "rotacion_mesas": round(float(row[3]) / max(total_tables, 1), 1)
            }

            # Log del estado optimizado
            _ = (
                "✅ CON DATOS"
                if any(v > 0 for k, v in metrics.items() if not k.startswith("_"))
                else "📋 CONFIGURACIÓN INICIAL"
            )
            
            return metrics

        except Exception as e:
            logger.error("Error obteniendo métricas reales (batch optimizado): %s", e)
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
            # logger.debug("Query falló (normal en config inicial): %s", e)
            return default_value

    def get_last_update(self) -> Optional[datetime]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Timestamp de última actualización"""
        return self._last_update

    def force_refresh(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Forzar actualización inmediata"""
        logger.info("Actualización forzada de datos reales")
        self.fetch_all_real_data()
