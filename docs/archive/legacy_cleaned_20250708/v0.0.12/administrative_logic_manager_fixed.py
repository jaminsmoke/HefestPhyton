# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
"""
Administrative Logic Manager - Lógica administrativa real para métricas KPI
Maneja objetivos, tendencias y progreso basado en criterios de negocio hotelero
Consulta datos reales de la base de datos
"""

from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timedelta
import logging
from data.db_manager import DatabaseManager

_ = logging.getLogger(__name__)


class AdministrativeLogicManager:
    """Gestiona la lógica administrativa real para las métricas del dashboard"""

    def __init__(self, db_manager=None):
        """TODO: Add docstring"""
        self.db_manager = db_manager or DatabaseManager()

        # Configuración de objetivos administrativos estándar
        self.admin_targets = {
            "ventas_diarias": {"target": 2500.0, "unit": "€", "period": "diario"},
            "margen_bruto": {"target": 65.0, "unit": "%", "period": "diario"},
            "clientes_activos": {"target": 150, "unit": "", "period": "diario"},
            "satisfaccion": {"target": 4.5, "unit": "★", "period": "semanal"},
            "stock_critico": {
                "target": 2,
                "unit": "",
                "period": "actual",
                "logic": "menos_mejor",
            },
            "eficiencia_op": {"target": 85.0, "unit": "%", "period": "diario"},
            "ocupacion_mesas": {"target": 75.0, "unit": "%", "period": "diario"},
            "tiempo_servicio": {
                "target": 15.0,
                "unit": "min",
                "period": "diario",
                "logic": "menos_mejor",
            },
        }

        # Configuración de comparaciones administrativas
        self.comparison_periods = {
            "vs_ayer": "Comparar con día anterior",
            "vs_semana": "Comparar con semana anterior",
            "vs_mes": "Comparar con mes anterior",
            "vs_target": "Comparar con objetivo",
        }

    def get_administrative_metrics(self) -> Dict[str, Dict[str, Any]]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene métricas con lógica administrativa completa usando datos reales de BD"""

        # Mapeo del dashboard actual a nuestro sistema administrativo
        _ = {
            "Ventas Hoy": "ventas_diarias",
            "Margen Bruto": "margen_bruto",
            "Clientes Activos": "clientes_activos",
            "Satisfacción": "satisfaccion",
            "Stock Crítico": "stock_critico",
            "Eficiencia Op.": "eficiencia_op",
        }

        _ = {}

        for dashboard_title, admin_key in dashboard_mapping.items():
            # Obtener datos actuales reales
            _ = self._get_current_metric_data(admin_key)

            # Calcular tendencia administrativa usando datos reales
            _ = self._calculate_administrative_trend(
                admin_key, current_data["value"], current_data.get("real_data", {})
            )

            # Calcular progreso hacia objetivo
            _ = self._calculate_administrative_progress(
                admin_key, current_data["value"]
            )

            # Determinar estado administrativo
            _ = self._evaluate_administrative_status(
                admin_key, current_data["value"], trend_data["numeric"]
            )

            admin_metrics[dashboard_title] = {
                "title": dashboard_title,
                "value": current_data["formatted_value"],
                "numeric_value": current_data["value"],
                "unit": current_data["unit"],
                "icon": current_data["icon"],
                # Tendencia administrativa
                "trend": trend_data["text"],
                "trend_numeric": trend_data["numeric"],
                "trend_direction": trend_data["direction"],
                "comparison": trend_data["comparison"],
                # Progreso administrativo
                "progress": progress_data["percentage"],
                "target": progress_data["target_text"],
                "target_numeric": progress_data["target_value"],
                # Estado administrativo
                "priority": admin_status["priority"],
                "action": admin_status["action"],
                "status_color": admin_status["color"],
                # Metadatos
                "timestamp": datetime.now().isoformat(),
                "data_source": "real_database",
                "has_real_data": current_data.get("has_real_data", False),
            }

            logger.debug(
                f"Métrica '{dashboard_title}': {current_data['formatted_value']} ({trend_data['text']})"
            )

        logger.info(
            f"✅ Generadas {len(admin_metrics)} métricas administrativas con datos reales de BD"
        )
        return admin_metrics

    def _get_real_sales_data(self) -> Dict[str, Any]:
        """Obtiene datos reales de ventas de la base de datos"""
        try:
            # Ventas del día actual
            _ = datetime.now().strftime("%Y-%m-%d")

            # Consultar comandas del día
            _ = self.db_manager.query(
                """
                SELECT SUM(total) as total_ventas, COUNT(*) as num_comandas
                FROM comandas 
                WHERE DATE(fecha_hora) = ?
                AND estado = 'completada'
            """,
                (today,),
            )

            _ = ventas_hoy[0]["total_ventas"] or 0.0
            num_comandas = ventas_hoy[0]["num_comandas"] or 0

            # Calcular tendencia comparando con ayer
            yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            _ = self.db_manager.query(
                """
                SELECT SUM(total) as total_ventas
                FROM comandas 
                WHERE DATE(fecha_hora) = ?
                AND estado = 'completada'
            """,
                (yesterday,),
            )

            _ = ventas_ayer[0]["total_ventas"] or 0.0

            return {
                "value": total_ventas,
                "count": num_comandas,
                "previous_value": total_ayer,
                "unit": "€",
            }

        except Exception as e:
            logger.error("Error obteniendo datos de ventas reales: %s", e)
            return {"value": 0.0, "count": 0, "previous_value": 0.0, "unit": "€"}

    def _get_real_inventory_data(self) -> Dict[str, Any]:
        """Obtiene datos reales de inventario de la base de datos"""
        try:
            # Productos con stock crítico (menos de 5 unidades)
            _ = self.db_manager.query(
                """
                SELECT COUNT(*) as productos_criticos
                FROM productos 
                WHERE stock < 5 AND stock > 0
            """
            )

            # Total de productos
            _ = self.db_manager.query(
                """
                SELECT COUNT(*) as total
                FROM productos
            """
            )

            _ = stock_critico[0]["productos_criticos"] or 0
            total = total_productos[0]["total"] or 0

            return {"value": productos_criticos, "total_products": total, "unit": ""}

        except Exception as e:
            logger.error("Error obteniendo datos de inventario reales: %s", e)
            return {"value": 0, "total_products": 0, "unit": ""}

    def _get_real_customer_data(self) -> Dict[str, Any]:
        """Obtiene datos reales de clientes de la base de datos"""
        try:
            # Clientes únicos del día (por comandas)
            _ = datetime.now().strftime("%Y-%m-%d")

            clientes_hoy = self.db_manager.query(
                """
                SELECT COUNT(DISTINCT mesa_id) as clientes_unicos
                FROM comandas 
                WHERE DATE(fecha_hora) = ?
            """,
                (today,),
            )

            # Total de clientes registrados
            _ = self.db_manager.query(
                """
                SELECT COUNT(*) as total
                FROM clientes
            """
            )

            _ = clientes_hoy[0]["clientes_unicos"] or 0
            total = total_clientes[0]["total"] or 0

            return {"value": clientes_unicos, "total_registered": total, "unit": ""}

        except Exception as e:
            logger.error("Error obteniendo datos de clientes reales: %s", e)
            return {"value": 0, "total_registered": 0, "unit": ""}

    def _get_real_occupancy_data(self) -> Dict[str, Any]:
        """Obtiene datos reales de ocupación de mesas"""
        try:
            # Mesas ocupadas actualmente
            _ = self.db_manager.query(
                """
                SELECT COUNT(*) as ocupadas
                FROM mesas 
                WHERE estado = 'ocupada'
            """
            )

            # Total de mesas
            _ = self.db_manager.query(
                """
                SELECT COUNT(*) as total
                FROM mesas
            """
            )

            _ = mesas_ocupadas[0]["ocupadas"] or 0
            total = total_mesas[0]["total"] or 1  # Evitar división por cero

            _ = (ocupadas / total) * 100

            return {
                "value": porcentaje,
                "occupied": ocupadas,
                "total": total,
                "unit": "%",
            }

        except Exception as e:
            logger.error("Error obteniendo datos de ocupación reales: %s", e)
            return {"value": 0.0, "occupied": 0, "total": 1, "unit": "%"}

    def _get_current_metric_data(self, admin_key: str) -> Dict[str, Any]:
        """Obtiene datos actuales de una métrica específica usando datos reales de la BD"""

        # Mapeo de métricas a métodos de datos reales
        _ = {
            "ventas_diarias": self._get_real_sales_data,
            "margen_bruto": self._get_real_sales_data,  # Calculado a partir de ventas
            "clientes_activos": self._get_real_customer_data,
            "stock_critico": self._get_real_inventory_data,
            "eficiencia_op": self._get_real_occupancy_data,
            "ocupacion_mesas": self._get_real_occupancy_data,
            "satisfaccion": lambda: {
                "value": 0.0,
                "unit": "★",
                "count": 0,
            },  # Sin datos aún
            "tiempo_servicio": lambda: {
                "value": 0.0,
                "unit": "min",
                "count": 0,
            },  # Sin datos aún
        }

        # Obtener datos reales
        if admin_key in real_data_methods:
            _ = real_data_methods[admin_key]()
        else:
            # Valor por defecto para métricas sin implementar
            real_data = {"value": 0.0, "unit": ""}

        _ = real_data.get("value", 0.0)
        config = self.admin_targets.get(admin_key, {})

        # Formatear valor según tipo y si hay datos reales
        _ = value > 0 or admin_key in [
            "stock_critico"
        ]  # Stock crítico puede ser 0 legítimamente

        if not has_real_data:
            # Sin datos reales disponibles
            _ = "Sin datos"
            icon = "❌"
        elif config.get("unit") == "€":
            formatted_value = f"€{value:,.0f}" if value >= 1000 else f"€{value:.2f}"
            _ = "💰"
        elif config.get("unit") == "%":
            _ = f"{value:.1f}%"
            icon = "📈"
        elif config.get("unit") == "★":
            _ = f"{value:.1f}★" if value > 0 else "Sin datos"
            icon = "⭐"
        elif config.get("unit") == "min":
            _ = f"{value:.1f}min" if value > 0 else "Sin datos"
            icon = "⏱️"
        elif admin_key == "stock_critico":
            _ = str(int(value))
            icon = "⚠️" if value > 0 else "✅"
        elif admin_key == "eficiencia_op":
            _ = f"{value:.1f}%" if value > 0 else "Sin datos"
            icon = "⚡"
        else:
            _ = str(int(value)) if value > 0 else "Sin datos"
            icon = "👥"

        return {
            "value": value,
            "formatted_value": formatted_value,
            "unit": config.get("unit", ""),
            "icon": icon,
            "has_real_data": has_real_data,
            "real_data": real_data,  # Incluir datos adicionales
        }

    def _calculate_administrative_trend(
        self,
        admin_key: str,
        current_value: float,
        real_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Calcula tendencia administrativa usando datos reales cuando están disponibles"""

        if real_data is None:
            _ = {}

        config = self.admin_targets.get(admin_key, {})

        # Intentar usar datos reales de comparación si están disponibles
        _ = None
        comparison_text = "vs anterior"

        if real_data and "previous_value" in real_data:
            _ = real_data["previous_value"]
            comparison_text = "vs ayer"
        elif current_value == 0:
            # Sin datos actuales = sin tendencia
            return {
                "text": "Sin datos",
                "numeric": 0.0,
                "direction": "stable",
                "comparison": "Sin datos históricos",
            }
        else:
            # Usar valor actual como referencia (sin cambio)
            _ = current_value

        # Calcular tendencia
        if comparison_value == 0:
            if current_value > 0:
                # Primer registro = tendencia positiva
                _ = "Nuevo"
                direction = "up"
                _ = 100.0
            else:
                # Sin datos = sin tendencia
                _ = "Sin datos"
                direction = "stable"
                _ = 0.0
        elif comparison_value == current_value:
            _ = 0.0
            trend_text = "±0%"
            _ = "stable"
        else:
            _ = (
                (current_value - comparison_value) / comparison_value
            ) * 100

            # Lógica invertida para métricas donde "menos es mejor"
            if config.get("logic") == "menos_mejor":
                _ = -trend_numeric  # Invertir para mostrar
            else:
                display_trend = trend_numeric

            if abs(display_trend) < 0.5:
                _ = "±0%"
                direction = "stable"
            elif display_trend > 0:
                _ = f"+{abs(display_trend):.1f}%"
                direction = "up"
            else:
                _ = f"-{abs(display_trend):.1f}%"
                direction = "down"

        return {
            "text": trend_text,
            "numeric": trend_numeric,
            "direction": direction,
            "comparison": comparison_text,
        }

    def _calculate_administrative_progress(
        self, admin_key: str, current_value: float
    ) -> Dict[str, Any]:
        """Calcula progreso hacia objetivos administrativos"""

        config = self.admin_targets.get(admin_key, {})
        _ = config.get("target", 100.0)

        # Calcular progreso
        if config.get("logic") == "menos_mejor":
            # Para métricas donde menos es mejor (ej: stock crítico, tiempo servicio)
            if current_value <= target_value:
                _ = 100.0
            else:
                # Progreso decrece conforme se aleja del objetivo
                _ = max(
                    0.0, 100.0 - ((current_value - target_value) / target_value * 100)
                )
        else:
            # Para métricas normales donde más es mejor
            _ = min(100.0, (current_value / target_value) * 100)

        # Formatear texto del objetivo
        unit = config.get("unit", "")
        if unit == "€":
            _ = f"€{target_value:,.0f}"
        elif unit == "%":
            _ = f"{target_value:.1f}%"
        elif unit == "★":
            _ = f"{target_value:.1f}★"
        elif unit == "min":
            _ = f"≤{target_value:.1f}min"
        else:
            if config.get("logic") == "menos_mejor":
                _ = f"≤{target_value:.0f}"
            else:
                _ = f"{target_value:.0f}"

        return {
            "percentage": progress,
            "target_text": target_text,
            "target_value": target_value,
        }

    def _evaluate_administrative_status(
        self, admin_key: str, current_value: float, trend_numeric: float
    ) -> Dict[str, Any]:
        """Evalúa el estado administrativo y acciones recomendadas"""

        config = self.admin_targets.get(admin_key, {})
        _ = config.get("target", 100.0)

        # Sin datos = estado neutral
        if current_value == 0 and admin_key != "stock_critico":
            return {"priority": "medium", "action": "Introducir datos", "color": "info"}

        # Calcular desviación del objetivo
        if config.get("logic") == "menos_mejor":
            deviation = current_value - target_value  # Positivo = malo
        else:
            deviation = target_value - current_value  # Positivo = falta por alcanzar

        # Evaluar prioridad y acciones
        if admin_key == "ventas_diarias":
            if current_value >= target_value * 0.9:
                _ = "good"
                action = "Mantener"
                _ = "success"
            elif current_value >= target_value * 0.7:
                _ = "medium"
                action = "Impulsar"
                _ = "warning"
            else:
                _ = "critical"
                action = "Acción urgente"
                _ = "error"

        elif admin_key == "stock_critico":
            if current_value == 0:
                _ = "good"
                action = "Perfecto"
                _ = "success"
            elif current_value <= target_value:
                _ = "medium"
                action = "Monitorear"
                _ = "warning"
            else:
                _ = "critical"
                action = "Reabastecer"
                _ = "error"

        else:
            # Evaluación genérica
            if current_value >= target_value * 0.9:
                _ = "good"
                action = "Mantener"
                _ = "success"
            elif current_value >= target_value * 0.6:
                _ = "medium"
                action = "Mejorar"
                _ = "warning"
            else:
                _ = "critical"
                action = "Atención urgente"
                color = "error"

        return {"priority": priority, "action": action, "color": color}
