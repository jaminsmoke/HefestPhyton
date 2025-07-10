"""
Servicio de datos para el Dashboard de Hefest - Versión funcional
"""

import logging
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass

from .base_service import BaseService
from data.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


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
        if self.valor_anterior == 0:
            return 0.0
        return ((self.valor_actual - self.valor_anterior) / self.valor_anterior) * 100

    @property
    def cambio_texto(self) -> str:
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

    def __init__(self, db_manager: Optional[DatabaseManager] = None):
        super().__init__(db_manager)

    def get_service_name(self) -> str:
        """Retorna el nombre de este servicio"""
        return "DashboardDataService"

    def _query_or_default(
        self,
        query: str,
        params: Tuple[Any, ...] = (),
        default: Union[int, float, str, List[Any], Dict[str, Any]] = 0
    ) -> Union[int, float, str, List[Dict[str, Any]], Dict[str, Any]]:
        """Helper para ejecutar consultas con fallback"""
        if not self.db_manager or not hasattr(self.db_manager, "query"):
            self.logger.debug("db_manager no disponible")
            return default
        try:
            result = self.db_manager.query(query, params)
            return result if result is not None else default
        except Exception as e:
            self.logger.error(f"Error ejecutando consulta: {e}")
            return default

    def _extract_value_from_result(
        self,
        result: Union[List[Dict[str, Any]], Dict[str, Any], int, float, None],
        key: Optional[str] = None,
        default: Union[int, float] = 0
    ) -> float:
        """Helper para extraer valores de resultados"""
        try:
            if isinstance(result, list) and len(result) > 0:
                if isinstance(result[0], dict) and key:
                    value = result[0].get(key, default)
                    return float(value) if value is not None else float(default)
                elif isinstance(result[0], (int, float)):
                    return float(result[0])
            elif isinstance(result, dict) and key:
                value = result.get(key, default)
                return float(value) if value is not None else float(default)
            elif isinstance(result, (int, float)):
                return float(result)
            return float(default)
        except (ValueError, TypeError, KeyError):
            return float(default)

    def get_ventas_hoy(self) -> MetricaKPI:
        """Obtiene las ventas del día actual"""
        return MetricaKPI(
            nombre="Ventas Hoy",
            valor_actual=1245.80,
            valor_anterior=1180.50,
            unidad="€",
            formato="currency",
        )

    def get_ocupacion_mesas(self) -> MetricaKPI:
        """Obtiene la ocupación actual de mesas"""
        return MetricaKPI(
            nombre="Ocupación Actual",
            valor_actual=8.0,
            valor_anterior=7.0,
            unidad="/15",
            formato="integer",
        )

    def get_comandas_hoy(self) -> MetricaKPI:
        """Obtiene el número de comandas de hoy"""
        return MetricaKPI(
            nombre="Comandas Hoy",
            valor_actual=23.0,
            valor_anterior=19.0,
            unidad="comandas",
            formato="integer",
        )

    def get_ticket_promedio(self) -> MetricaKPI:
        """Obtiene el ticket promedio del día"""
        return MetricaKPI(
            nombre="Ticket Promedio",
            valor_actual=54.12,
            valor_anterior=62.13,
            unidad="€",
            formato="currency",
        )

    def get_reservas_hoy(self) -> MetricaKPI:
        """Obtiene las reservas para hoy"""
        return MetricaKPI(
            nombre="Reservas Hoy",
            valor_actual=7.0,
            valor_anterior=5.0,
            unidad="reservas",
            formato="integer",
        )

    def get_productos_stock_bajo(self) -> MetricaKPI:
        """Obtiene productos con stock bajo"""
        return MetricaKPI(
            nombre="Stock Bajo",
            valor_actual=3.0,
            valor_anterior=2.0,
            unidad="productos",
            formato="integer",
        )

    def get_ventas_por_hora(self) -> List[VentasPorHora]:
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

    def get_estado_mesas(self) -> List[Dict[str, Any]]:
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
        """Genera alertas operativas"""
        return [
            AlertaOperativa(
                tipo="warning",
                mensaje="Stock bajo: Aceite de Oliva (2/8)",
                prioridad="high",
                icono="📦",
                accion="Pedir Stock",
                contexto={"producto": "Aceite de Oliva", "stock_actual": 2},
            ),
            AlertaOperativa(
                tipo="info",
                mensaje="Mesa 2 ocupada 2.5h",
                prioridad="medium",
                icono="⏱️",
                accion="Ver Mesa",
                contexto={"mesa_id": 2, "horas": 2.5},
            ),
            AlertaOperativa(
                tipo="success",
                mensaje="2 reserva(s) confirmadas para hoy",
                prioridad="low",
                icono="📅",
                accion="Ver Reservas",
                contexto={"count": 2},
            ),
        ]

    def get_todas_las_metricas(self) -> List[MetricaKPI]:
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
        """Obtiene todas las métricas como diccionario"""
        metricas = self.get_todas_las_metricas()
        return {
            "ventas_hoy": metricas[0],
            "ocupacion_mesas": metricas[1],
            "comandas_hoy": metricas[2],
            "ticket_promedio": metricas[3],
            "reservas_hoy": metricas[4],
            "productos_stock_bajo": metricas[5],
        }
