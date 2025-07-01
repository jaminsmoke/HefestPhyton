"""
Sistema Centralizado de Alertas para Hefest
==========================================

Este servicio centraliza todas las alertas del sistema y permite
la comunicación entre módulos y el dashboard.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)


class TipoDepartamento(Enum):
    """Departamentos que pueden generar alertas"""

    INVENTARIO = "inventario"
    TPV = "tpv"
    HOSPEDERIA = "hospederia"
    SISTEMA = "sistema"
    USUARIOS = "usuarios"


class EstadoAlerta(Enum):
    """Estados de las alertas"""

    NUEVA = "nueva"
    VISTA = "vista"
    EN_PROCESO = "en_proceso"
    RESUELTA = "resuelta"
    IGNORADA = "ignorada"


@dataclass
class AlertaCentralizada:
    """Alerta centralizada del sistema"""

    id: Optional[str]
    departamento: TipoDepartamento
    tipo: str
    prioridad: str  # "baja", "media", "alta", "critica"
    titulo: str
    mensaje: str
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None
    estado: EstadoAlerta = EstadoAlerta.NUEVA
    datos_contexto: Optional[Dict[str, Any]] = None
    acciones_disponibles: Optional[List[str]] = None

    @property
    def es_activa(self) -> bool:
        """Indica si la alerta está activa"""
        return self.estado in [
            EstadoAlerta.NUEVA,
            EstadoAlerta.VISTA,
            EstadoAlerta.EN_PROCESO,
        ]

    @property
    def color_prioridad(self) -> str:
        """Retorna el color asociado a la prioridad"""
        colors = {
            "baja": "#10b981",
            "media": "#f59e0b",
            "alta": "#ef4444",
            "critica": "#dc2626",
        }
        return colors.get(self.prioridad, "#6b7280")

    @property
    def icono_departamento(self) -> str:
        """Retorna el icono asociado al departamento"""
        iconos = {
            TipoDepartamento.INVENTARIO: "📦",
            TipoDepartamento.TPV: "💰",
            TipoDepartamento.HOSPEDERIA: "🏨",
            TipoDepartamento.SISTEMA: "⚙️",
            TipoDepartamento.USUARIOS: "👤",
        }
        return iconos.get(self.departamento, "📋")


class AlertasService:
    """Servicio centralizado de alertas"""

    def __init__(self):
        self.alertas_cache = []
        self.contadores_departamento = {}
        self.logger = logging.getLogger(__name__)

    def registrar_alertas_inventario(
        self, alertas_inventario
    ) -> List[AlertaCentralizada]:
        """Convierte alertas de inventario a alertas centralizadas"""
        alertas_centralizadas = []

        try:
            for alerta in alertas_inventario:
                alerta_central = AlertaCentralizada(
                    id=f"inv_{alerta.producto_id}_{alerta.tipo.value}",
                    departamento=TipoDepartamento.INVENTARIO,
                    tipo=alerta.tipo.value,
                    prioridad=alerta.prioridad.value,
                    titulo=alerta.titulo,
                    mensaje=alerta.mensaje,
                    fecha_creacion=alerta.fecha_creacion,
                    datos_contexto={
                        "producto_id": alerta.producto_id,
                        "producto_nombre": alerta.producto_nombre,
                        **alerta.datos_adicionales,
                    },
                    acciones_disponibles=(
                        ["Ajustar Stock", "Ver Producto", "Generar Pedido"]
                        if alerta.tipo.value
                        in ["stock_agotado", "stock_bajo", "stock_critico"]
                        else []
                    ),
                )
                alertas_centralizadas.append(alerta_central)

            self.logger.info(
                f"Registradas {len(alertas_centralizadas)} alertas de inventario"
            )
            return alertas_centralizadas

        except Exception as e:
            self.logger.error(f"Error registrando alertas de inventario: {e}")
            return []

    def get_alertas_dashboard(self) -> Dict[str, Any]:
        """Obtiene resumen de alertas para el dashboard"""
        try:
            # Obtener alertas de inventario
            from services.inventario_service_real import InventarioService

            try:
                from data.db_manager import DatabaseManager

                db_manager = DatabaseManager()
                inventario_service = InventarioService(db_manager)
                # Cambiado: obtener productos con stock bajo como alertas activas
                alertas_inventario = inventario_service.get_productos_stock_bajo()
                alertas_centralizadas = self.registrar_alertas_inventario(alertas_inventario)
            except Exception as e:
                self.logger.error(f"Error obteniendo alertas de inventario: {e}")
                alertas_centralizadas = []

            # Generar resumen
            total_alertas = len(alertas_centralizadas)
            alertas_por_prioridad = {}
            alertas_por_departamento = {}

            for alerta in alertas_centralizadas:
                # Contar por prioridad
                if alerta.prioridad not in alertas_por_prioridad:
                    alertas_por_prioridad[alerta.prioridad] = 0
                alertas_por_prioridad[alerta.prioridad] += 1

                # Contar por departamento
                dept_key = alerta.departamento.value
                if dept_key not in alertas_por_departamento:
                    alertas_por_departamento[dept_key] = {
                        "total": 0,
                        "criticas": 0,
                        "altas": 0,
                        "medias": 0,
                        "bajas": 0,
                    }
                alertas_por_departamento[dept_key]["total"] += 1
                alertas_por_departamento[dept_key][alerta.prioridad + "s"] += 1

            # Alertas más urgentes (máximo 5)
            alertas_urgentes = sorted(
                alertas_centralizadas,
                key=lambda x: (
                    {"critica": 4, "alta": 3, "media": 2, "baja": 1}.get(
                        x.prioridad, 0
                    ),
                    x.fecha_creacion,
                ),
                reverse=True,
            )[:5]

            resumen = {
                "total_alertas": total_alertas,
                "alertas_por_prioridad": alertas_por_prioridad,
                "alertas_por_departamento": alertas_por_departamento,
                "alertas_urgentes": [
                    {
                        "id": alerta.id,
                        "departamento": alerta.departamento.value,
                        "icono": alerta.icono_departamento,
                        "titulo": alerta.titulo,
                        "mensaje": (
                            alerta.mensaje[:100] + "..."
                            if len(alerta.mensaje) > 100
                            else alerta.mensaje
                        ),
                        "prioridad": alerta.prioridad,
                        "color": alerta.color_prioridad,
                        "fecha": alerta.fecha_creacion.strftime("%H:%M"),
                        "acciones": alerta.acciones_disponibles or [],
                    }
                    for alerta in alertas_urgentes
                ],
                "timestamp": datetime.now().isoformat(),
                "estado_general": self._evaluar_estado_general(alertas_centralizadas),
            }

            return resumen

        except Exception as e:
            self.logger.error(f"Error obteniendo alertas para dashboard: {e}")
            return {
                "total_alertas": 0,
                "alertas_por_prioridad": {},
                "alertas_por_departamento": {},
                "alertas_urgentes": [],
                "timestamp": datetime.now().isoformat(),
                "estado_general": "desconocido",
            }

    def _evaluar_estado_general(self, alertas: List[AlertaCentralizada]) -> str:
        """Evalúa el estado general del sistema basado en las alertas"""
        if not alertas:
            return "optimo"

        criticas = len([a for a in alertas if a.prioridad == "critica"])
        altas = len([a for a in alertas if a.prioridad == "alta"])

        if criticas >= 3:
            return "critico"
        elif criticas >= 1 or altas >= 5:
            return "alerta"
        elif altas >= 1:
            return "atencion"
        else:
            return "normal"

    def procesar_accion_alerta(self, alerta_id: str, accion: str) -> Dict[str, Any]:
        """Procesa una acción sobre una alerta específica"""
        try:
            # Identificar el tipo de alerta por su ID
            if alerta_id.startswith("inv_"):
                return self._procesar_accion_inventario(alerta_id, accion)
            else:
                return {"success": False, "message": "Tipo de alerta no reconocido"}

        except Exception as e:
            self.logger.error(
                f"Error procesando acción {accion} para alerta {alerta_id}: {e}"
            )
            return {"success": False, "message": f"Error: {str(e)}"}

    def _procesar_accion_inventario(
        self, alerta_id: str, accion: str
    ) -> Dict[str, Any]:
        """Procesa acciones específicas de inventario"""
        # Extraer información del ID de la alerta
        partes = alerta_id.split("_")
        if len(partes) >= 2:
            producto_id = partes[1]
        else:
            return {"success": False, "message": "ID de alerta inválido"}

        if accion == "Ver Producto":
            return {
                "success": True,
                "action": "navigate_to_inventory",
                "data": {"producto_id": producto_id},
            }
        elif accion == "Ajustar Stock":
            return {
                "success": True,
                "action": "open_stock_adjustment",
                "data": {"producto_id": producto_id},
            }
        elif accion == "Generar Pedido":
            return {
                "success": True,
                "action": "generate_order",
                "data": {"producto_id": producto_id},
            }
        else:
            return {"success": False, "message": f"Acción '{accion}' no reconocida"}


# Instancia global del servicio
alertas_service = AlertasService()
