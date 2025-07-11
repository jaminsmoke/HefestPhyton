"""
Servicio de gestión de habitaciones y reservas.
"""

import logging
from typing import List, Dict, Optional, Any, TYPE_CHECKING
from dataclasses import dataclass
from datetime import date

from .base_service import BaseService

if TYPE_CHECKING:
    from data.db_manager import DatabaseManager

logger = logging.getLogger(__name__)


@dataclass
class Habitacion:
    """Clase de datos para una habitación"""

    id: int
    numero: str
    tipo: str
    estado: str  # libre, ocupada, limpieza, mantenimiento, reservada
    precio_base: float
    planta: str


@dataclass
class Reserva:
    """Clase de datos para una reserva"""

    id: Optional[int]
    habitacion_id: int
    cliente_nombre: str
    cliente_dni: str
    cliente_telefono: str
    cliente_email: str
    fecha_entrada: date
    fecha_salida: date
    precio_total: float
    estado: str  # pendiente, confirmada, cancelada, completada


class HospederiaService(BaseService):
    """Servicio para la gestión de hospedería"""

    def __init__(self, db_manager: Optional["DatabaseManager"] = None):
        super().__init__(db_manager)
        self._habitaciones_cache = []
        self._load_habitaciones()

    def get_service_name(self) -> str:
        """Retorna el nombre de este servicio"""
        return "HospederiaService"

    def _load_habitaciones(self):
        """Carga las habitaciones desde la base de datos o crea datos de prueba"""
        if self.db_manager:
            # TODO: Cargar desde base de datos
            pass
        else:
            # Datos de prueba
            self._habitaciones_cache = [
                Habitacion(1, "101", "Individual", "libre", 60.0, "Primera"),
                Habitacion(2, "102", "Doble", "ocupada", 85.0, "Primera"),
                Habitacion(3, "103", "Suite", "reservada", 120.0, "Primera"),
                Habitacion(4, "104", "Doble", "limpieza", 85.0, "Primera"),
                Habitacion(5, "201", "Individual", "libre", 60.0, "Segunda"),
                Habitacion(6, "202", "Doble", "ocupada", 85.0, "Segunda"),
                Habitacion(7, "203", "Suite", "libre", 120.0, "Segunda"),
                Habitacion(8, "301", "Triple", "mantenimiento", 110.0, "Tercera"),
            ]

    def get_habitaciones(self) -> List[Habitacion]:
        """Obtiene todas las habitaciones"""
        return self._habitaciones_cache.copy()

    def get_habitacion_by_id(self, habitacion_id: int) -> Optional[Habitacion]:
        """Obtiene una habitación por su ID"""
        for hab in self._habitaciones_cache:
            if hab.id == habitacion_id:
                return hab
        return None

    def get_habitaciones_by_estado(self, estado: str) -> List[Habitacion]:
        """Obtiene habitaciones filtradas por estado"""
        return [hab for hab in self._habitaciones_cache if hab.estado == estado]

    def actualizar_estado_habitacion(
        self, habitacion_id: int, nuevo_estado: str
    ) -> bool:
        """Actualiza el estado de una habitación"""
        estados_validos = ["libre", "ocupada", "limpieza", "mantenimiento", "reservada"]

        if nuevo_estado not in estados_validos:
            logger.error(f"Estado inválido: {nuevo_estado}")
            return False

        for hab in self._habitaciones_cache:
            if hab.id == habitacion_id:
                hab.estado = nuevo_estado
                logger.info(f"Habitación {hab.numero} cambió a estado: {nuevo_estado}")
                return True

        logger.error(f"Habitación con ID {habitacion_id} no encontrada")
        return False

    def get_estadisticas_ocupacion(self) -> Dict[str, int]:
        """Obtiene estadísticas de ocupación"""
        stats = {
            "total": len(self._habitaciones_cache),
            "libres": 0,
            "ocupadas": 0,
            "reservadas": 0,
            "limpieza": 0,
            "mantenimiento": 0,
        }

        for hab in self._habitaciones_cache:
            if hab.estado in stats:
                stats[hab.estado] += 1

        return stats

    def get_rooms(self) -> List[Dict[str, Any]]:
        """Obtiene habitaciones en formato para el módulo UI"""
        rooms: List[Dict[str, Any]] = []
        for hab in self._habitaciones_cache:
            # Mapear estados a formato UI
            status_map: Dict[str, str] = {
                "libre": "available",
                "ocupada": "occupied",
                "limpieza": "cleaning",
                "mantenimiento": "maintenance",
                "reservada": "reserved",
            }

            rooms.append(
                {
                    "id": hab.id,
                    "number": hab.numero,
                    "type": hab.tipo,
                    "status": status_map.get(hab.estado, "unknown"),
                    "price": hab.precio_base,
                    "floor": hab.planta,
                }
            )
        return rooms

    def get_reservations(self) -> List[Dict[str, Any]]:
        """Obtiene reservas en formato para el módulo UI"""
        # Datos de prueba para reservas
        reservations: List[Dict[str, Any]] = [
            {
                "id": 1,
                "client_name": "Juan Pérez",
                "room_number": "102",
                "check_in_date": "2025-06-10",
                "check_out_date": "2025-06-12",
                "status": "Confirmada",
            },
            {
                "id": 2,
                "client_name": "María García",
                "room_number": "103",
                "check_in_date": "2025-06-11",
                "check_out_date": "2025-06-13",
                "status": "Pendiente",
            },
            {
                "id": 3,
                "client_name": "Carlos López",
                "room_number": "202",
                "check_in_date": "2025-06-09",
                "check_out_date": "2025-06-11",
                "status": "Check-in realizado",
            },
        ]
        return reservations

    def create_reservation(self, reservation_data: Dict[str, Any]) -> bool:
        """Crea una nueva reserva"""
        try:
            # Validar datos requeridos
            required_fields = [
                "client_name",
                "room_number",
                "check_in_date",
                "check_out_date",
            ]
            for field in required_fields:
                if field not in reservation_data:
                    logger.error(f"Campo requerido faltante: {field}")
                    return False

            # Buscar habitación por número
            room_id = None
            for hab in self._habitaciones_cache:
                if hab.numero == reservation_data["room_number"]:
                    room_id = hab.id
                    break

            if not room_id:
                logger.error(
                    f"Habitación {reservation_data['room_number']} no encontrada"
                )
                return False
            # Verificar disponibilidad
            habitacion = self.get_habitacion_by_id(room_id)
            if not habitacion or habitacion.estado not in ["libre"]:
                logger.error(
                    f"Habitación {reservation_data['room_number']} no disponible"
                )
                return False

            # Actualizar estado de habitación
            self.actualizar_estado_habitacion(room_id, "reservada")

            logger.info(
                f"Reserva creada para {reservation_data['client_name']} en habitación {reservation_data['room_number']}"
            )
            return True

        except Exception as e:
            logger.error(f"Error al crear reserva: {e}")
            return False

    def perform_checkin(self, checkin_data: Dict[str, Any]) -> bool:
        """Realiza check-in de una reserva"""
        try:
            room_number = checkin_data.get("room_number")
            if not room_number:
                return False

            # Buscar habitación
            for hab in self._habitaciones_cache:
                if hab.numero == room_number:
                    if hab.estado == "reservada":
                        self.actualizar_estado_habitacion(hab.id, "ocupada")
                        logger.info(f"Check-in realizado en habitación {room_number}")
                        return True
                    break

            return False

        except Exception as e:
            logger.error(f"Error en check-in: {e}")
            return False

    def perform_checkout(self, checkout_data: Dict[str, Any]) -> bool:
        """Realiza check-out de una habitación"""
        try:
            room_number = checkout_data.get("room_number")
            cleaning_required = checkout_data.get("cleaning_required", True)

            if not room_number:
                return False

            # Buscar habitación
            for hab in self._habitaciones_cache:
                if hab.numero == room_number:
                    if hab.estado == "ocupada":
                        new_status = "limpieza" if cleaning_required else "libre"
                        self.actualizar_estado_habitacion(hab.id, new_status)
                        logger.info(f"Check-out realizado en habitación {room_number}")
                        return True
                    break

            return False

        except Exception as e:
            logger.error(f"Error en check-out: {e}")
            return False
