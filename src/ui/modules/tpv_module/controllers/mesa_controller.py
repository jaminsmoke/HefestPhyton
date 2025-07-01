"""
Controlador MesaController - Lógica de negocio para gestión de mesas
Versión: v0.0.13
"""

import logging
from typing import List, Optional, Callable
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal

from services.tpv_service import TPVService, Mesa

logger = logging.getLogger(__name__)


class MesaController(QObject):
    """Controlador para la lógica de negocio de las mesas"""

    # Señales
    error_occurred = pyqtSignal(str)  # Error ocurrido
    # Importar el EventBus global de mesas
    from ..mesa_event_bus import mesa_event_bus

    def __init__(self, tpv_service: Optional[TPVService] = None, parent=None):
        super().__init__(parent)
        self.tpv_service = tpv_service
        self.mesas: List[Mesa] = []

    def set_service(self, tpv_service: TPVService):
        """Establece el servicio TPV"""
        self.tpv_service = tpv_service
        self.load_mesas()

    def load_mesas(self):
        """Carga las mesas desde el servicio"""
        try:
            if not self.tpv_service:
                logger.warning("No hay servicio TPV disponible")
                return

            self.mesas = self.tpv_service.get_mesas()
            MesaController.mesa_event_bus.mesas_actualizadas.emit(self.mesas)

            logger.info(f"Cargadas {len(self.mesas)} mesas")

        except Exception as e:
            error_msg = f"Error cargando mesas: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)

    def crear_mesa(self, capacidad: int, zona: str) -> bool:
        """Crea una nueva mesa con numeración automática contextualizada por zona"""
        try:
            if not self.tpv_service:
                self.error_occurred.emit("No hay servicio TPV disponible")
                return False

            # Crear mesa con numeración automática
            nueva_mesa = self.tpv_service.crear_mesa(
                capacidad=capacidad,
                zona=zona
            )

            if nueva_mesa:
                self.mesas.append(nueva_mesa)
                MesaController.mesa_event_bus.mesa_creada.emit(nueva_mesa)
                MesaController.mesa_event_bus.mesas_actualizadas.emit(self.mesas)

                logger.info(f"Mesa {nueva_mesa.numero} creada correctamente en zona {zona}")
                return True
            else:
                self.error_occurred.emit("Error creando la mesa")
                return False

        except Exception as e:
            error_msg = f"Error creando mesa: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False

    def editar_mesa(self, mesa_id: int, numero: int, capacidad: int, zona: str) -> bool:
        """Edita una mesa existente"""
        try:
            if not self.tpv_service:
                self.error_occurred.emit("No hay servicio TPV disponible")
                return False

            # Encontrar la mesa
            mesa_actual = None
            for mesa in self.mesas:
                if mesa.id == mesa_id:
                    mesa_actual = mesa
                    break

            if not mesa_actual:
                self.error_occurred.emit("Mesa no encontrada")
                return False

            # Validar que no exista otra mesa con el mismo número
            if any(mesa.numero == numero and mesa.id != mesa_id for mesa in self.mesas):
                self.error_occurred.emit(f"Ya existe otra mesa con el número {numero}")
                return False

            # Por ahora, solo actualizamos localmente hasta implementar en TPVService
            mesa_actual.numero = str(numero)
            mesa_actual.capacidad = capacidad
            mesa_actual.zona = zona

            MesaController.mesa_event_bus.mesa_actualizada.emit(mesa_actual)
            MesaController.mesa_event_bus.mesas_actualizadas.emit(self.mesas)

            logger.info(f"Mesa {numero} actualizada correctamente")
            return True

        except Exception as e:
            error_msg = f"Error editando mesa: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False
    def eliminar_mesa(self, mesa_id: int) -> bool:
        """Elimina una mesa"""
        try:
            if not self.tpv_service:
                self.error_occurred.emit("No hay servicio TPV disponible")
                return False

            # Encontrar la mesa
            mesa_actual = None
            for mesa in self.mesas:
                if mesa.id == mesa_id:
                    mesa_actual = mesa
                    break

            if not mesa_actual:
                self.error_occurred.emit("Mesa no encontrada")
                return False

            # Verificar que la mesa no esté ocupada
            if mesa_actual.estado == "ocupada":
                self.error_occurred.emit("No se puede eliminar una mesa ocupada")
                return False

            # Eliminar usando el servicio TPV (incluye base de datos)
            if self.tpv_service.eliminar_mesa(mesa_id):
                # Actualizar cache local
                self.mesas = [mesa for mesa in self.mesas if mesa.id != mesa_id]

                MesaController.mesa_event_bus.mesa_eliminada.emit(mesa_id)
                MesaController.mesa_event_bus.mesas_actualizadas.emit(self.mesas)

                logger.info(f"Mesa {mesa_actual.numero} eliminada correctamente")
                return True
            else:
                self.error_occurred.emit("Error eliminando mesa del sistema")
                return False

        except Exception as e:
            error_msg = f"Error eliminando mesa: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False

    def cambiar_estado_mesa(self, mesa_id: int, nuevo_estado: str) -> bool:
        """Cambia el estado de una mesa"""
        try:
            if not self.tpv_service:
                self.error_occurred.emit("No hay servicio TPV disponible")
                return False

            # Validar estado
            estados_validos = ["libre", "ocupada", "reservada", "mantenimiento"]
            if nuevo_estado not in estados_validos:
                self.error_occurred.emit(f"Estado inválido: {nuevo_estado}")
                return False

            # Encontrar la mesa
            mesa_actual = None
            for mesa in self.mesas:
                if mesa.id == mesa_id:
                    mesa_actual = mesa
                    break

            if not mesa_actual:
                self.error_occurred.emit("Mesa no encontrada")
                return False

            # Cambiar estado localmente
            mesa_actual.estado = nuevo_estado

            MesaController.mesa_event_bus.mesa_actualizada.emit(mesa_actual)
            MesaController.mesa_event_bus.mesas_actualizadas.emit(self.mesas)

            logger.info(f"Estado de mesa {mesa_actual.numero} cambiado a {nuevo_estado}")
            return True

        except Exception as e:
            error_msg = f"Error cambiando estado de mesa: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False

    def ocupar_mesa(self, mesa_id: int) -> bool:
        """Ocupa una mesa (cambia estado a ocupada)"""
        return self.cambiar_estado_mesa(mesa_id, "ocupada")

    def liberar_mesa(self, mesa_id: int) -> bool:
        """Libera una mesa (cambia estado a libre)"""
        return self.cambiar_estado_mesa(mesa_id, "libre")

    def reservar_mesa(self, mesa_id: int) -> bool:
        """Reserva una mesa (cambia estado a reservada)"""
        return self.cambiar_estado_mesa(mesa_id, "reservada")

    def poner_en_mantenimiento(self, mesa_id: int) -> bool:
        """Pone una mesa en mantenimiento"""
        return self.cambiar_estado_mesa(mesa_id, "mantenimiento")

    def get_mesa_by_id(self, mesa_id: int) -> Optional[Mesa]:
        """Obtiene una mesa por su ID"""
        for mesa in self.mesas:
            if mesa.id == mesa_id:
                return mesa
        return None

    def get_mesa_by_numero(self, numero: int) -> Optional[Mesa]:
        """Obtiene una mesa por su número"""
        for mesa in self.mesas:
            if mesa.numero == numero:
                return mesa
        return None

    def get_mesas_by_zona(self, zona: str) -> List[Mesa]:
        """Obtiene las mesas de una zona específica"""
        return [mesa for mesa in self.mesas if mesa.zona == zona]

    def get_mesas_by_estado(self, estado: str) -> List[Mesa]:
        """Obtiene las mesas con un estado específico"""
        return [mesa for mesa in self.mesas if mesa.estado == estado]

    def get_zonas_disponibles(self) -> List[str]:
        """Obtiene la lista de zonas disponibles"""
        zonas = set()
        for mesa in self.mesas:
            zonas.add(mesa.zona)
        return sorted(list(zonas))

    def refresh_mesas(self):
        """Refresca la lista de mesas"""
        self.load_mesas()

    def cargar_mesas(self):
        """Carga las mesas desde el servicio"""
        try:
            if not self.tpv_service:
                self.error_occurred.emit("No hay servicio TPV disponible")
                return

            mesas = self.tpv_service.get_mesas()
            self.mesas = mesas
            MesaController.mesa_event_bus.mesas_actualizadas.emit(mesas)

            logger.info(f"Cargadas {len(mesas)} mesas desde el servicio")

        except Exception as e:
            error_msg = f"Error cargando mesas: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
