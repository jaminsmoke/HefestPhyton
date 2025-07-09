"""
Controlador MesaController - Lógica de negocio para gestión de mesas
Versión: v0.0.14
"""

import logging
from typing import List, Optional, Callable
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal

from services.tpv_service import TPVService, Mesa

logger = logging.getLogger(__name__)


class MesaController(QObject):
    def crear_mesa_con_numero(self, numero: int, capacidad: int, zona: str) -> bool:
        """Crea una nueva mesa con número específico delegando en TPVService"""
        try:
            if not self.tpv_service:
                self.error_occurred.emit("No hay servicio TPV disponible")
                return False
            nueva_mesa = None
            if hasattr(self.tpv_service, "crear_mesa_con_numero"):
                nueva_mesa = self.tpv_service.crear_mesa_con_numero(
                    numero, capacidad, zona
                )
            else:
                # Fallback: usar crear_mesa normal (sin número específico)
                nueva_mesa = self.tpv_service.crear_mesa(capacidad, zona)
            if nueva_mesa:
                self.mesas.append(nueva_mesa)
                self.load_mesas()  # Recargar desde servicio tras crear
                logger.info(
                    f"Mesa {nueva_mesa.numero} creada correctamente en zona {zona}"
                )
                return True
            else:
                self.error_occurred.emit("Error creando la mesa")
                return False
        except Exception as e:
            error_msg = f"Error creando mesa con número: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False

    """Controlador para la lógica de negocio de las mesas"""

    # Señales
    error_occurred = pyqtSignal(str)  # Error ocurrido
    # Importar el EventBus global de mesas
    from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus

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
            # ...
            # El servicio debe emitir la señal global, no el controlador

            # logger.debug(f"Cargadas {len(self.mesas)} mesas")

        except Exception as e:
            error_msg = f"Error cargando mesas: {e}"
            logger.error(error_msg)
            # ...
            self.error_occurred.emit(error_msg)

    def crear_mesa(self, capacidad: int, zona: str) -> bool:
        """Crea una nueva mesa con numeración automática contextualizada por zona"""
        try:
            if not self.tpv_service:
                self.error_occurred.emit("No hay servicio TPV disponible")
                return False

            # Crear mesa con numeración automática
            nueva_mesa = self.tpv_service.crear_mesa(capacidad=capacidad, zona=zona)

            if nueva_mesa:
                self.mesas.append(nueva_mesa)
                self.load_mesas()  # Recargar desde servicio tras crear
                logger.info(
                    f"Mesa {nueva_mesa.numero} creada correctamente en zona {zona}"
                )
                return True
            else:
                self.error_occurred.emit("Error creando la mesa")
                return False

        except Exception as e:
            error_msg = f"Error creando mesa: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False

    def editar_mesa(
        self, numero: str, nuevo_numero: str, capacidad: int, zona: str
    ) -> bool:
        """Edita una mesa existente usando el identificador string 'numero'"""
        try:
            if not self.tpv_service:
                self.error_occurred.emit("No hay servicio TPV disponible")
                return False

            # Encontrar la mesa por numero
            mesa_actual = None
            for mesa in self.mesas:
                if mesa.numero == numero:
                    mesa_actual = mesa
                    break

            if not mesa_actual:
                self.error_occurred.emit("Mesa no encontrada")
                return False

            # Validar que no exista otra mesa con el mismo nuevo_numero
            if any(
                mesa.numero == nuevo_numero and mesa.numero != numero
                for mesa in self.mesas
            ):
                self.error_occurred.emit(
                    f"Ya existe otra mesa con el número {nuevo_numero}"
                )
                return False

            # Actualizar datos
            mesa_actual.numero = str(nuevo_numero)
            mesa_actual.capacidad = capacidad
            mesa_actual.zona = zona

            MesaController.mesa_event_bus.mesa_actualizada.emit(mesa_actual)
            self.load_mesas()  # Recargar desde servicio tras editar

            # logger.debug(f"Mesa {nuevo_numero} actualizada correctamente")
            return True

        except Exception as e:
            error_msg = f"Error editando mesa: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False

    def eliminar_mesa(self, numero: str) -> bool:
        """Elimina una mesa usando el identificador string 'numero'"""
        try:
            if not self.tpv_service:
                self.error_occurred.emit("No hay servicio TPV disponible")
                return False

            # Encontrar la mesa
            mesa_actual = None
            for mesa in self.mesas:
                if mesa.numero == numero:
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
            if self.tpv_service.eliminar_mesa_por_numero(numero):
                # Actualizar cache local
                self.mesas = [mesa for mesa in self.mesas if mesa.numero != numero]

                MesaController.mesa_event_bus.mesa_eliminada.emit(numero)
                self.load_mesas()  # Recargar desde servicio tras eliminar

                # logger.debug(f"Mesa {mesa_actual.numero} eliminada correctamente")
                return True
            else:
                self.error_occurred.emit("Error eliminando mesa del sistema")
                return False

        except Exception as e:
            error_msg = f"Error eliminando mesa: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False

    def cambiar_estado_mesa(self, numero: str, nuevo_estado: str) -> bool:
        """Cambia el estado de una mesa usando el identificador string 'numero'"""
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
                if mesa.numero == numero:
                    mesa_actual = mesa
                    break

            if not mesa_actual:
                self.error_occurred.emit("Mesa no encontrada")
                return False

            # Cambiar estado localmente
            mesa_actual.estado = nuevo_estado

            MesaController.mesa_event_bus.mesa_actualizada.emit(mesa_actual)
            self.load_mesas()  # Recargar desde servicio tras cambiar estado

            logger.info(
                f"Estado de mesa {mesa_actual.numero} cambiado a {nuevo_estado}"
            )
            return True

        except Exception as e:
            error_msg = f"Error cambiando estado de mesa: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
            return False

    def ocupar_mesa(self, numero: str) -> bool:
        """Ocupa una mesa (cambia estado a ocupada)"""
        return self.cambiar_estado_mesa(numero, "ocupada")

    def liberar_mesa(self, numero: str) -> bool:
        """Libera una mesa (cambia estado a libre)"""
        return self.cambiar_estado_mesa(numero, "libre")

    def reservar_mesa(self, numero: str) -> bool:
        """Reserva una mesa (cambia estado a reservada)"""
        return self.cambiar_estado_mesa(numero, "reservada")

    def poner_en_mantenimiento(self, numero: str) -> bool:
        """Pone una mesa en mantenimiento"""
        return self.cambiar_estado_mesa(numero, "mantenimiento")

    def get_mesa_by_numero(self, numero: str) -> Optional[Mesa]:
        """Obtiene una mesa por su número (string)"""
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
            # El servicio debe emitir la señal global, no el controlador

            # logger.debug(f"Cargadas {len(mesas)} mesas desde el servicio")

        except Exception as e:
            error_msg = f"Error cargando mesas: {e}"
            logger.error(error_msg)
            self.error_occurred.emit(error_msg)
