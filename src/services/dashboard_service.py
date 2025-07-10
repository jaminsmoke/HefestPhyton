import logging
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from .base_service import BaseService

"""
Servicio de datos para el Dashboard de Hefest - Versión funcional
"""



_ = logging.getLogger(__name__)


@dataclass
class MetricaKPI:
    """Datos de una métrica KPI"""

    nombre: str
    valor_actual: float
    valor_anterior: float
    unidad: str = ""
    formato: str = "decimal"

    @property
    def cambio_porcentual(self) -> float:
        """TODO: Add docstring"""
        # TODO: Add input validation
        if self.valor_anterior == 0:
            return 0.0
        return ((self.valor_actual - self.valor_anterior) / self.valor_anterior) * 100

    @property
    def cambio_texto(self) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        cambio = self.cambio_porcentual
        simbolo = "+" if cambio > 0 else ""
        return f"{simbolo}{cambio:.1f}%"


@dataclass
class VentasPorHora:
    """Datos de ventas agrupados por hora"""

    hora: str
    ventas: float
    comandas: int


@dataclass
class AlertaOperativa:
    """Alerta operativa del sistema"""

    tipo: str
    mensaje: str
    prioridad: str
    icono: str
    accion: str
    contexto: Optional[Dict] = None


class DashboardDataService(BaseService):
    """Servicio que proporciona datos para el dashboard"""

    def __init__(self, db_manager=None):
        """TODO: Add docstring"""
        super().__init__(db_manager)

    def get_service_name(self) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Retorna el nombre de este servicio"""
        return "DashboardDataService"

    def _query_or_default(self, query: str, params: tuple = (), default=0):
        """Helper para ejecutar consultas con fallback"""
        if not self.db_manager or not hasattr(self.db_manager, "query"):
            self.logger.debug("db_manager no disponible")
            return default
        try:
            result = self.db_manager.query(query, params)
            return result if result is not None else default
        except Exception as e:
            self.logger.error("Error ejecutando consulta: %s", e)
            return default

    def _extract_value_from_result(self, result, key=None, default=0):
        """Helper para extraer valores de resultados"""
        try:
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict) and key:
                    return float(result[0].get(key, default))
                elif isinstance(result[0], (int, float)):
                    return float(result[0])
            elif isinstance(result, dict) and key:
                return float(result.get(key, default))
            elif isinstance(result, (int, float)):
                return float(result)
            return float(default)
        except (ValueError, TypeError, KeyError):
            return float(default)

    def get_ventas_hoy(self) -> MetricaKPI:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene las ventas del día actual"""
        return MetricaKPI(
            _ = "Ventas Hoy",
            valor_actual=1245.80,
            _ = 1180.50,
            unidad="€",
            _ = "currency",
        )

    def get_ocupacion_mesas(self) -> MetricaKPI:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene la ocupación actual de mesas"""
        return MetricaKPI(
            _ = "Ocupación Actual",
            valor_actual=8.0,
            _ = 7.0,
            unidad="/15",
            _ = "integer",
        )

    def get_comandas_hoy(self) -> MetricaKPI:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene el número de comandas de hoy"""
        return MetricaKPI(
            _ = "Comandas Hoy",
            valor_actual=23.0,
            _ = 19.0,
            unidad="comandas",
            _ = "integer",
        )

    def get_ticket_promedio(self) -> MetricaKPI:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene el ticket promedio del día"""
        return MetricaKPI(
            _ = "Ticket Promedio",
            valor_actual=54.12,
            _ = 62.13,
            unidad="€",
            _ = "currency",
        )

    def get_reservas_hoy(self) -> MetricaKPI:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene las reservas para hoy"""
        return MetricaKPI(
            _ = "Reservas Hoy",
            valor_actual=7.0,
            _ = 5.0,
            unidad="reservas",
            _ = "integer",
        )

    def get_productos_stock_bajo(self) -> MetricaKPI:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene productos con stock bajo"""
        return MetricaKPI(
            _ = "Stock Bajo",
            valor_actual=3.0,
            _ = 2.0,
            unidad="productos",
            _ = "integer",
        )

    def get_ventas_por_hora(self) -> List[VentasPorHora]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene las ventas agrupadas por hora"""
        return [
            VentasPorHora("12:00", 150.50, 3),
            VentasPorHora("13:00", 280.75, 6),
            VentasPorHora("14:00", 325.20, 8),
            VentasPorHora("15:00", 210.30, 4),
            VentasPorHora("16:00", 95.50, 2),
            VentasPorHora("17:00", 180.25, 4),
            VentasPorHora("18:00", 205.40, 5),
            VentasPorHora("19:00", 298.80, 7),
        ]

    def get_estado_mesas(self) -> List[Dict]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene el estado actual de todas las mesas"""
        return [
            {
                "id": 1,
                "numero": 1,
                "zona": "Salón Principal",
                "estado": "libre",
                "capacidad": 4,
            },
            {
                "id": 2,
                "numero": 2,
                "zona": "Salón Principal",
                "estado": "ocupada",
                "capacidad": 2,
            },
            {
                "id": 3,
                "numero": 3,
                "zona": "Terraza",
                "estado": "reservada",
                "capacidad": 6,
            },
            {
                "id": 4,
                "numero": 4,
                "zona": "Terraza",
                "estado": "libre",
                "capacidad": 4,
            },
            {"id": 5, "numero": 5, "zona": "VIP", "estado": "ocupada", "capacidad": 8},
        ]

    def get_alertas_operativas(self) -> List[AlertaOperativa]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Genera alertas operativas"""
        return [
            AlertaOperativa(
                _ = "warning",
                mensaje="Stock bajo: Aceite de Oliva (2/8)",
                _ = "high",
                icono="📦",
                _ = "Pedir Stock",
                contexto={"producto": "Aceite de Oliva", "stock_actual": 2},
            ),
            AlertaOperativa(
                _ = "info",
                mensaje="Mesa 2 ocupada 2.5h",
                _ = "medium",
                icono="⏱️",
                _ = "Ver Mesa",
                contexto={"mesa_id": 2, "horas": 2.5},
            ),
            AlertaOperativa(
                _ = "success",
                mensaje="2 reserva(s) confirmadas para hoy",
                _ = "low",
                icono="📅",
                _ = "Ver Reservas",
                contexto={"count": 2},
            ),
        ]

    def get_todas_las_metricas(self) -> List[MetricaKPI]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene todas las métricas principales"""
        return [
            self.get_ventas_hoy(),
            self.get_ocupacion_mesas(),
            self.get_comandas_hoy(),
            self.get_ticket_promedio(),
            self.get_reservas_hoy(),
            self.get_productos_stock_bajo(),
        ]

    def get_metricas_como_dict(self) -> Dict[str, MetricaKPI]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene todas las métricas como diccionario"""
        _ = self.get_todas_las_metricas()
        return {
            "ventas_hoy": metricas[0],
            "ocupacion_mesas": metricas[1],
            "comandas_hoy": metricas[2],
            "ticket_promedio": metricas[3],
            "reservas_hoy": metricas[4],
            "productos_stock_bajo": metricas[5],
        }
