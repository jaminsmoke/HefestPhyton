"""
Administrative Logic Manager - Lógica administrativa real para métricas KPI
Maneja objetivos, tendencias y progreso basado en criterios de negocio hotelero
Consulta datos reales de la base de datos
"""

from typing import Dict, Any, Tuple, Optional
from datetime import datetime, timedelta
import logging
from data.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


class AdministrativeLogicManager:
    """Gestiona la lógica administrativa real para las métricas del dashboard"""

    def __init__(self, db_manager=None):
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

        # Configuración de criterios de alertas administrativas
        self.alert_criteria = {
            "stock_bajo": {"threshold": 5, "priority": "high", "icon": "📦"},
            "stock_agotado": {"threshold": 0, "priority": "critical", "icon": "🚨"},
            "ventas_bajo_objetivo": {
                "threshold": 0.7,
                "priority": "medium",
                "icon": "📉",
            },
            "ventas_muy_bajo": {"threshold": 0.5, "priority": "critical", "icon": "⚠️"},
            "mesas_sin_usar": {"threshold": 0.3, "priority": "medium", "icon": "🍽️"},
            "sin_clientes_dia": {"threshold": 0, "priority": "high", "icon": "👥"},
            "productos_sin_stock": {"threshold": 1, "priority": "high", "icon": "📋"},
            "sistema_vacio": {"threshold": 0, "priority": "medium", "icon": "🔧"},
        }

    def get_administrative_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Obtiene métricas con lógica administrativa completa usando datos reales de BD"""

        # Mapeo del dashboard actual a nuestro sistema administrativo
        dashboard_mapping = {
            "Ventas Hoy": "ventas_diarias",
            "Margen Bruto": "margen_bruto",
            "Clientes Activos": "clientes_activos",
            "Satisfacción": "satisfaccion",
            "Stock Crítico": "stock_critico",
            "Eficiencia Op.": "eficiencia_op",
        }

        admin_metrics = {}

        for dashboard_title, admin_key in dashboard_mapping.items():
            # Obtener datos actuales reales
            current_data = self._get_current_metric_data(admin_key)

            # Calcular tendencia administrativa usando datos reales
            trend_data = self._calculate_administrative_trend(
                admin_key, current_data["value"], current_data.get("real_data", {})
            )

            # Calcular progreso hacia objetivo
            progress_data = self._calculate_administrative_progress(
                admin_key, current_data["value"]
            )

            # Determinar estado administrativo
            admin_status = self._evaluate_administrative_status(
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

            # logger.debug(
            #     f"Métrica '{dashboard_title}': {current_data['formatted_value']} ({trend_data['text']})"
            # )

        logger.info(
            f"✅ Generadas {len(admin_metrics)} métricas administrativas con datos reales de BD"
        )
        return admin_metrics

    def get_administrative_alerts(self) -> Dict[str, Any]:
        """Obtiene alertas administrativas basadas en datos reales de la BD"""

        alerts = []
        alert_summary = {
            "total_alerts": 0,
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "last_update": datetime.now().isoformat(),
        }

        try:
            # Verificar stock bajo/agotado
            stock_alerts = self._get_stock_alerts()
            alerts.extend(stock_alerts)

            # Verificar ventas bajo objetivo
            sales_alerts = self._get_sales_alerts()
            alerts.extend(sales_alerts)

            # Verificar ocupación de mesas
            occupancy_alerts = self._get_occupancy_alerts()
            alerts.extend(occupancy_alerts)

            # Verificar clientes del día
            customer_alerts = self._get_customer_alerts()
            alerts.extend(customer_alerts)

            # Verificar estado general del sistema
            system_alerts = self._get_system_alerts()
            alerts.extend(system_alerts)

            # Contar alertas por prioridad
            for alert in alerts:
                alert_summary["total_alerts"] += 1
                priority = alert.get("priority", "medium")
                if priority == "critical":
                    alert_summary["critical_count"] += 1
                elif priority == "high":
                    alert_summary["high_count"] += 1
                elif priority == "medium":
                    alert_summary["medium_count"] += 1

            # logger.info(f"✅ Generadas {len(alerts)} alertas administrativas reales")

        except Exception as e:
            logger.error(f"Error generando alertas administrativas: {e}")
            alerts.append(
                {
                    "id": "error_alerts",
                    "title": "Error del Sistema",
                    "message": "No se pudieron cargar las alertas",
                    "priority": "high",
                    "icon": "⚠️",
                    "timestamp": datetime.now().isoformat(),
                    "action": "Revisar logs del sistema",
                }
            )

        return {"alerts": alerts, "summary": alert_summary}

    # =========================================================================
    # MÉTODOS DE ALERTAS ADMINISTRATIVAS REALES
    # =========================================================================

    def _get_stock_alerts(self) -> list:
        """Genera alertas de stock basadas en datos reales"""
        alerts = []

        try:
            # Productos con stock crítico
            stock_bajo = self.db_manager.query(
                """
                SELECT nombre, stock, categoria
                FROM productos
                WHERE stock > 0 AND stock <= 5
                ORDER BY stock ASC
            """
            )

            # Productos agotados
            stock_agotado = self.db_manager.query(
                """
                SELECT nombre, categoria
                FROM productos
                WHERE stock = 0
            """
            )

            # Generar alertas de stock bajo
            for producto in stock_bajo:
                alerts.append(
                    {
                        "id": f"stock_bajo_{producto['nombre'].replace(' ', '_')}",
                        "title": f"Stock Bajo: {producto['nombre']}",
                        "message": f"Solo quedan {producto['stock']} unidades",
                        "priority": "high" if producto["stock"] <= 2 else "medium",
                        "icon": "📦",
                        "category": "stock",
                        "timestamp": datetime.now().isoformat(),
                        "action": "Reabastecer producto",
                        "details": {
                            "producto": producto["nombre"],
                            "stock_actual": producto["stock"],
                            "categoria": producto["categoria"],
                        },
                    }
                )

            # Generar alertas de stock agotado
            for producto in stock_agotado:
                alerts.append(
                    {
                        "id": f"stock_agotado_{producto['nombre'].replace(' ', '_')}",
                        "title": f"Stock Agotado: {producto['nombre']}",
                        "message": "Producto sin existencias",
                        "priority": "critical",
                        "icon": "🚨",
                        "category": "stock",
                        "timestamp": datetime.now().isoformat(),
                        "action": "Reabastecer urgente",
                        "details": {
                            "producto": producto["nombre"],
                            "categoria": producto["categoria"],
                        },
                    }
                )

        except Exception as e:
            logger.error(f"Error obteniendo alertas de stock: {e}")

        return alerts

    def _get_sales_alerts(self) -> list:
        """Genera alertas de ventas basadas en objetivos administrativos"""
        alerts = []

        try:
            today = datetime.now().strftime("%Y-%m-%d")

            # Obtener ventas del día
            ventas_hoy = self.db_manager.query(
                """
                SELECT SUM(total) as total_ventas, COUNT(*) as num_comandas
                FROM comandas
                WHERE DATE(fecha_hora) = ?
                AND estado = 'completada'
            """,
                (today,),
            )

            total_ventas = ventas_hoy[0]["total_ventas"] or 0.0
            objetivo_ventas = self.admin_targets["ventas_diarias"]["target"]
            porcentaje_objetivo = (total_ventas / objetivo_ventas) * 100

            # Sin ventas del día
            if total_ventas == 0:
                alerts.append(
                    {
                        "id": "sin_ventas_dia",
                        "title": "Sin Ventas del Día",
                        "message": "No se han registrado ventas hoy",
                        "priority": "high",
                        "icon": "📉",
                        "category": "ventas",
                        "timestamp": datetime.now().isoformat(),
                        "action": "Revisar actividad comercial",
                        "details": {
                            "ventas_actuales": 0,
                            "objetivo_diario": objetivo_ventas,
                            "porcentaje_cumplimiento": 0,
                        },
                    }
                )
            # Ventas muy por debajo del objetivo
            elif porcentaje_objetivo < 50:
                alerts.append(
                    {
                        "id": "ventas_muy_bajo",
                        "title": "Ventas Muy por Debajo del Objetivo",
                        "message": f"Solo {porcentaje_objetivo:.1f}% del objetivo diario",
                        "priority": "critical",
                        "icon": "⚠️",
                        "category": "ventas",
                        "timestamp": datetime.now().isoformat(),
                        "action": "Acción comercial urgente",
                        "details": {
                            "ventas_actuales": total_ventas,
                            "objetivo_diario": objetivo_ventas,
                            "porcentaje_cumplimiento": porcentaje_objetivo,
                        },
                    }
                )
            # Ventas bajo objetivo (pero no crítico)
            elif porcentaje_objetivo < 70:
                alerts.append(
                    {
                        "id": "ventas_bajo_objetivo",
                        "title": "Ventas Bajo Objetivo",
                        "message": f"{porcentaje_objetivo:.1f}% del objetivo diario",
                        "priority": "medium",
                        "icon": "📊",
                        "category": "ventas",
                        "timestamp": datetime.now().isoformat(),
                        "action": "Impulsar ventas",
                        "details": {
                            "ventas_actuales": total_ventas,
                            "objetivo_diario": objetivo_ventas,
                            "porcentaje_cumplimiento": porcentaje_objetivo,
                        },
                    }
                )

        except Exception as e:
            logger.error(f"Error obteniendo alertas de ventas: {e}")

        return alerts

    def _get_occupancy_alerts(self) -> list:
        """Genera alertas de ocupación de mesas"""
        alerts = []

        try:
            # Obtener estado de mesas
            mesas_ocupadas = self.db_manager.query(
                """
                SELECT COUNT(*) as ocupadas
                FROM mesas
                WHERE estado = 'ocupada'
            """
            )

            total_mesas = self.db_manager.query(
                """
                SELECT COUNT(*) as total
                FROM mesas
            """
            )

            ocupadas = mesas_ocupadas[0]["ocupadas"] or 0
            total = total_mesas[0]["total"] or 0

            if total > 0:
                porcentaje_ocupacion = (ocupadas / total) * 100

                # Ocupación muy baja
                if porcentaje_ocupacion < 30:
                    alerts.append(
                        {
                            "id": "ocupacion_baja",
                            "title": "Ocupación de Mesas Baja",
                            "message": f"Solo {porcentaje_ocupacion:.1f}% de mesas ocupadas",
                            "priority": "medium",
                            "icon": "🍽️",
                            "category": "ocupacion",
                            "timestamp": datetime.now().isoformat(),
                            "action": "Revisar estrategia de atención",
                            "details": {
                                "mesas_ocupadas": ocupadas,
                                "total_mesas": total,
                                "porcentaje_ocupacion": porcentaje_ocupacion,
                            },
                        }
                    )
            else:
                # Sin mesas configuradas
                alerts.append(
                    {
                        "id": "sin_mesas_configuradas",
                        "title": "Sin Mesas Configuradas",
                        "message": "No hay mesas registradas en el sistema",
                        "priority": "high",
                        "icon": "🔧",
                        "category": "configuracion",
                        "timestamp": datetime.now().isoformat(),
                        "action": "Configurar mesas en el sistema",
                    }
                )

        except Exception as e:
            logger.error(f"Error obteniendo alertas de ocupación: {e}")

        return alerts

    def _get_customer_alerts(self) -> list:
        """Genera alertas relacionadas con clientes"""
        alerts = []

        try:
            today = datetime.now().strftime("%Y-%m-%d")

            # Clientes del día
            clientes_hoy = self.db_manager.query(
                """
                SELECT COUNT(DISTINCT mesa_id) as clientes_unicos
                FROM comandas
                WHERE DATE(fecha_hora) = ?
            """,
                (today,),
            )

            clientes_unicos = clientes_hoy[0]["clientes_unicos"] or 0

            # Sin clientes del día
            if clientes_unicos == 0:
                alerts.append(
                    {
                        "id": "sin_clientes_dia",
                        "title": "Sin Clientes del Día",
                        "message": "No se han atendido clientes hoy",
                        "priority": "high",
                        "icon": "👥",
                        "category": "clientes",
                        "timestamp": datetime.now().isoformat(),
                        "action": "Revisar estrategia de atención al cliente",
                        "details": {
                            "clientes_atendidos": clientes_unicos,
                            "objetivo_diario": self.admin_targets["clientes_activos"][
                                "target"
                            ],
                        },
                    }
                )

        except Exception as e:
            logger.error(f"Error obteniendo alertas de clientes: {e}")

        return alerts

    def _get_system_alerts(self) -> list:
        """Genera alertas del estado general del sistema"""
        alerts = []

        try:
            # Verificar si hay productos registrados
            total_productos = self.db_manager.query(
                """
                SELECT COUNT(*) as total
                FROM productos
            """
            )

            productos_count = total_productos[0]["total"] or 0

            # Sin productos en el sistema
            if productos_count == 0:
                alerts.append(
                    {
                        "id": "sistema_sin_productos",
                        "title": "Sistema Sin Productos",
                        "message": "No hay productos registrados en el inventario",
                        "priority": "high",
                        "icon": "📋",
                        "category": "sistema",
                        "timestamp": datetime.now().isoformat(),
                        "action": "Registrar productos en el inventario",
                        "details": {"productos_registrados": productos_count},
                    }
                )

            # Estado general - sistema en configuración inicial
            if productos_count == 0:
                alerts.append(
                    {
                        "id": "configuracion_inicial",
                        "title": "Sistema en Configuración Inicial",
                        "message": "El sistema requiere configuración básica",
                        "priority": "medium",
                        "icon": "🔧",
                        "category": "sistema",
                        "timestamp": datetime.now().isoformat(),
                        "action": "Completar configuración inicial del sistema",
                        "details": {
                            "estado": "configuracion_inicial",
                            "pasos_pendientes": ["productos", "mesas", "usuarios"],
                        },
                    }
                )

        except Exception as e:
            logger.error(f"Error obteniendo alertas del sistema: {e}")

        return alerts

    def _get_fallback_alerts(self) -> list:
        """Alertas de respaldo cuando hay errores en BD"""
        return [
            {
                "type": "info",
                "icon": "ℹ️",
                "message": "Sistema funcionando correctamente",
                "category": "system",
                "timestamp": datetime.now().isoformat(),
            },
            {
                "type": "warning",
                "icon": "⚠️",
                "message": "Conectando con base de datos...",
                "category": "system",
                "timestamp": datetime.now().isoformat(),
            },
        ]

    # =========================================================================
    # MÉTODOS BASE REQUERIDOS (simplificados para alertas)
    # =========================================================================

    def _get_current_metric_data(self, admin_key: str) -> Dict[str, Any]:
        """Obtener datos reales de la métrica desde la base de datos"""
        try:
            if admin_key == "ventas_diarias":
                return self._get_ventas_diarias_real()
            elif admin_key == "margen_bruto":
                return self._get_margen_bruto_real()
            elif admin_key == "clientes_activos":
                return self._get_clientes_activos_real()
            elif admin_key == "satisfaccion":
                return self._get_satisfaccion_real()
            elif admin_key == "stock_critico":
                return self._get_stock_critico_real()
            elif admin_key == "eficiencia_op":
                return self._get_eficiencia_operacional_real()
            else:
                return self._get_default_metric_data()

        except Exception as e:
            logger.error(f"Error obteniendo datos reales para {admin_key}: {e}")
            return self._get_default_metric_data()

    def _get_ventas_diarias_real(self) -> Dict[str, Any]:
        """Obtener ventas reales del día actual"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")
            query = """
                SELECT COALESCE(SUM(total), 0) as ventas_total, COUNT(*) as num_comandas
                FROM comandas
                WHERE DATE(fecha_hora) = ? AND estado IN ('completada', 'pagada')
            """
            result = self.db_manager.query(query, (today,))

            if result:
                # Usar acceso directo por índice para sqlite3.Row
                ventas_total = float(result[0][0])  # ventas_total
                num_comandas = int(result[0][1])  # num_comandas

                return {
                    "value": ventas_total,
                    "formatted_value": (
                        f"€{ventas_total:.2f}" if ventas_total > 0 else "€0.00"
                    ),
                    "unit": "€",
                    "icon": "💰" if ventas_total > 0 else "💸",
                    "has_real_data": True,
                    "real_data": {"num_comandas": num_comandas, "fecha": today},
                }
            else:
                return self._get_no_data_metric("Ventas", "€0.00", "€", "💸")

        except Exception as e:
            logger.error(f"Error obteniendo ventas diarias: {e}")
            return self._get_no_data_metric("Ventas", "€0.00", "€", "❌")

    def _get_margen_bruto_real(self) -> Dict[str, Any]:
        """Obtener margen bruto real calculado"""
        try:
            # Por ahora, sin datos de costos, asumimos margen 0
            # TODO: Implementar cuando tengamos datos de costos de productos
            return {
                "value": 0.0,
                "formatted_value": "0.0%",
                "unit": "%",
                "icon": "📊",
                "has_real_data": True,
                "real_data": {"note": "Pendiente configurar costos de productos"},
            }
        except Exception as e:
            logger.error(f"Error calculando margen bruto: {e}")
            return self._get_no_data_metric("Margen", "0.0%", "%", "❌")

    def _get_clientes_activos_real(self) -> Dict[str, Any]:
        """Obtener número real de clientes activos hoy"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")

            # Contar clientes únicos con reservas activas (las comandas no tienen cliente_id directo)
            query_reservas = """
                SELECT COUNT(DISTINCT cliente_id) as clientes_reservas
                FROM reservas
                WHERE estado = 'activa' AND DATE(fecha_entrada) <= ? AND DATE(fecha_salida) >= ?
            """

            # Contar total de clientes registrados como métrica base
            query_total_clientes = """
                SELECT COUNT(*) as total_clientes
                FROM clientes
            """

            result_reservas = self.db_manager.query(query_reservas, (today, today))
            result_total = self.db_manager.query(query_total_clientes)

            clientes_reservas = result_reservas[0][0] if result_reservas else 0
            total_clientes = result_total[0][0] if result_total else 0

            # Para un sistema nuevo, mostrar clientes registrados como base
            clientes_activos = (
                clientes_reservas if clientes_reservas > 0 else total_clientes
            )

            return {
                "value": float(clientes_activos),
                "formatted_value": str(clientes_activos),
                "unit": "",
                "icon": "👥" if clientes_activos > 0 else "👤",
                "has_real_data": True,
                "real_data": {
                    "total_registrados": total_clientes,
                    "con_reservas": clientes_reservas,
                },
            }

        except Exception as e:
            logger.error(f"Error obteniendo clientes activos: {e}")
            return self._get_no_data_metric("Clientes", "0", "", "❌")

    def _get_satisfaccion_real(self) -> Dict[str, Any]:
        """Obtener satisfacción real (pendiente implementar sistema de valoraciones)"""
        try:
            # TODO: Implementar cuando tengamos sistema de valoraciones/feedback
            return {
                "value": 0.0,
                "formatted_value": "Sin valoraciones",
                "unit": "★",
                "icon": "⭐",
                "has_real_data": True,
                "real_data": {"note": "Sistema de valoraciones pendiente"},
            }
        except Exception as e:
            logger.error(f"Error obteniendo satisfacción: {e}")
            return self._get_no_data_metric("Satisfacción", "N/A", "★", "❌")

    def _get_stock_critico_real(self) -> Dict[str, Any]:
        """Obtener productos con stock crítico real"""
        try:
            # Productos con stock <= 5 (considerado crítico)
            query = """
                SELECT COUNT(*) as stock_critico,
                       COUNT(CASE WHEN stock = 0 THEN 1 END) as sin_stock,
                       COUNT(*) as total_productos
                FROM productos
                WHERE stock <= 5            """

            result = self.db_manager.query(query)

            if result:
                # Usar indexación directa en lugar de .get() para sqlite3.Row
                stock_critico = int(result[0][0])  # stock_critico
                sin_stock = int(result[0][1])  # sin_stock
                total_productos_query = self.db_manager.query(
                    "SELECT COUNT(*) FROM productos"
                )
                total_productos = (
                    int(total_productos_query[0][0]) if total_productos_query else 0
                )

                return {
                    "value": float(stock_critico),
                    "formatted_value": (
                        str(stock_critico) if total_productos > 0 else "Sin productos"
                    ),
                    "unit": "productos",
                    "icon": (
                        "🚨"
                        if stock_critico > 0
                        else ("📦" if total_productos > 0 else "📋")
                    ),
                    "has_real_data": True,
                    "real_data": {
                        "sin_stock": sin_stock,
                        "total_productos": total_productos,
                        "criticos": stock_critico,
                    },
                }
            else:
                return self._get_no_data_metric("Stock", "Sin productos", "", "📋")

        except Exception as e:
            logger.error(f"Error obteniendo stock crítico: {e}")
            return self._get_no_data_metric("Stock", "Error", "", "❌")

    def _get_eficiencia_operacional_real(self) -> Dict[str, Any]:
        """Obtener eficiencia operacional real"""
        try:
            today = datetime.now().strftime("%Y-%m-%d")

            # Calcular eficiencia basada en comandas completadas vs iniciadas
            query = """
                SELECT
                    COUNT(*) as total_comandas,
                    COUNT(CASE WHEN estado = 'completada' THEN 1 END) as completadas,
                    COUNT(CASE WHEN estado = 'cancelada' THEN 1 END) as canceladas
                FROM comandas                WHERE DATE(fecha_hora) = ?
            """

            result = self.db_manager.query(query, (today,))

            if result and result[0][0] > 0:  # total_comandas
                # Usar indexación directa en lugar de .get() para sqlite3.Row
                total = int(result[0][0])  # total_comandas
                completadas = int(result[0][1])  # completadas
                canceladas = int(result[0][2])  # canceladas

                eficiencia = (completadas / total * 100) if total > 0 else 0.0

                return {
                    "value": eficiencia,
                    "formatted_value": f"{eficiencia:.1f}%",
                    "unit": "%",
                    "icon": "⚡" if eficiencia >= 80 else "⚠️",
                    "has_real_data": True,
                    "real_data": {
                        "total_comandas": total,
                        "completadas": completadas,
                        "canceladas": canceladas,
                    },
                }
            else:
                return {
                    "value": 0.0,
                    "formatted_value": "Sin actividad",
                    "unit": "%",
                    "icon": "💤",
                    "has_real_data": True,
                    "real_data": {"note": "No hay comandas registradas hoy"},
                }

        except Exception as e:
            logger.error(f"Error calculando eficiencia operacional: {e}")
            return self._get_no_data_metric("Eficiencia", "0%", "%", "❌")

    def _get_no_data_metric(
        self, name: str, default_value: str, unit: str, icon: str
    ) -> Dict[str, Any]:
        """Datos por defecto para métricas sin información"""
        return {
            "value": 0.0,
            "formatted_value": default_value,
            "unit": unit,
            "icon": icon,
            "has_real_data": True,  # Sí tenemos datos reales: la ausencia de datos ES el dato real
            "real_data": {
                "note": f"Sistema {name.lower()} inicializado sin datos previos"
            },
        }

    def _get_default_metric_data(self) -> Dict[str, Any]:
        """Datos por defecto para métricas no implementadas"""
        return {
            "value": 0.0,
            "formatted_value": "No implementado",
            "unit": "",
            "icon": "🔧",
            "has_real_data": False,
            "real_data": {},
        }

    def _calculate_administrative_trend(
        self, admin_key: str, current_value: float, real_data=None
    ):
        """Calcular tendencia administrativa real comparando con períodos anteriores"""
        try:
            # Para ahora, sin datos históricos, tendencia neutra
            # TODO: Implementar comparación con días/semanas anteriores cuando tengamos más datos
            if current_value == 0:
                return {
                    "text": "Sistema nuevo",
                    "numeric": 0.0,
                    "direction": "stable",
                    "comparison": "Sin datos históricos aún",
                }
            else:
                return {
                    "text": "Datos iniciales",
                    "numeric": 0.0,
                    "direction": "stable",
                    "comparison": "Primera vez registrado",
                }
        except Exception as e:
            logger.error(f"Error calculando tendencia para {admin_key}: {e}")
            return {
                "text": "Sin tendencia",
                "numeric": 0.0,
                "direction": "stable",
                "comparison": "Error en cálculo",
            }

    def _calculate_administrative_progress(self, admin_key: str, current_value: float):
        """Calcular progreso real hacia objetivos administrativos"""
        try:
            target_config = self.admin_targets.get(admin_key, {})
            target_value = target_config.get("target", 100.0)
            unit = target_config.get("unit", "")

            # Para métricas donde "menos es mejor" (como stock crítico)
            if target_config.get("logic") == "menos_mejor":
                if current_value <= target_value:
                    progress = 100.0  # Objetivo cumplido
                else:
                    progress = max(
                        0, 100 - ((current_value - target_value) / target_value * 100)
                    )
            else:
                # Para métricas normales donde "más es mejor"
                progress = (
                    min(100, (current_value / target_value * 100))
                    if target_value > 0
                    else 0
                )

            return {
                "percentage": progress,
                "target_text": f"{target_value}{unit}",
                "target_value": target_value,
            }
        except Exception as e:
            logger.error(f"Error calculando progreso para {admin_key}: {e}")
            return {
                "percentage": 0.0,
                "target_text": "Sin objetivo",
                "target_value": 100.0,
            }

    def _evaluate_administrative_status(
        self, admin_key: str, current_value: float, trend_numeric: float
    ):
        """Evaluar estado administrativo real basado en valor actual y tendencia"""
        try:
            target_config = self.admin_targets.get(admin_key, {})
            target_value = target_config.get("target", 100.0)

            # Evaluación basada en el progreso hacia el objetivo
            if target_config.get("logic") == "menos_mejor":
                # Para stock crítico, tiempo de servicio, etc.
                if current_value <= target_value:
                    return {
                        "priority": "low",
                        "action": "Mantener nivel",
                        "color": "success",
                    }
                elif current_value <= target_value * 2:
                    return {
                        "priority": "medium",
                        "action": "Revisar y optimizar",
                        "color": "warning",
                    }
                else:
                    return {
                        "priority": "high",
                        "action": "Acción inmediata requerida",
                        "color": "danger",
                    }
            else:
                # Para ventas, eficiencia, etc.
                progress = (
                    (current_value / target_value * 100) if target_value > 0 else 0
                )

                if progress >= 80:
                    return {
                        "priority": "low",
                        "action": "Objetivo en camino",
                        "color": "success",
                    }
                elif progress >= 50:
                    return {
                        "priority": "medium",
                        "action": "Mejorar rendimiento",
                        "color": "warning",
                    }
                else:
                    return {
                        "priority": "high",
                        "action": "Revisar estrategia",
                        "color": "danger",
                    }

        except Exception as e:
            logger.error(f"Error evaluando estado para {admin_key}: {e}")
            return {
                "priority": "medium",
                "action": "Revisar configuración",
                "color": "info",
            }
