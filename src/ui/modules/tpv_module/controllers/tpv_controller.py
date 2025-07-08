"""
Controlador principal del módulo TPV - Maneja la lógica de negocio
"""

import logging
from typing import Dict, List, Optional, Any
from PyQt6.QtCore import QObject, pyqtSignal
from services.tpv_service import TPVService, Mesa, Comanda, Producto

logger = logging.getLogger(__name__)


class TPVController(QObject):
    """Controlador principal que maneja la lógica de negocio del TPV"""

    # Señales para comunicación con la UI
    mesa_updated = pyqtSignal(Mesa)
    comanda_updated = pyqtSignal(Comanda)
    producto_added = pyqtSignal(int, int, int)  # comanda_id, producto_id, cantidad
    error_occurred = pyqtSignal(str)
    status_changed = pyqtSignal(str)

    def __init__(self, db_manager=None):
        super().__init__()
        # Siempre inicializar TPVService con db_manager real
        # TODO v0.0.14: Forzar que todas las instancias de TPVController reciban db_manager real. Si detectas un uso sin db_manager, refactorizar y registrar en README.
        self.tpv_service = TPVService(db_manager=db_manager)
        self._active_orders: Dict[int, Comanda] = {}

    def get_all_mesas(self) -> List[Mesa]:
        """Obtiene todas las mesas disponibles"""
        try:
            return self.tpv_service.get_todas_mesas()
        except Exception as e:
            logger.error(f"Error al obtener mesas: {e}")
            self.error_occurred.emit(f"Error al cargar mesas: {str(e)}")
            return []

    def get_mesa_by_id(self, mesa_id: int) -> Optional[Mesa]:
        """Obtiene una mesa específica por ID"""
        try:
            return self.tpv_service.get_mesa_por_id(mesa_id)
        except Exception as e:
            logger.error(f"Error al obtener mesa {mesa_id}: {e}")
            self.error_occurred.emit(f"Error al cargar mesa: {str(e)}")
            return None

    def open_mesa(self, mesa_id: int) -> Optional[Comanda]:
        """Abre una mesa y retorna la comanda activa o crea una nueva"""
        try:
            mesa = self.get_mesa_by_id(mesa_id)
            if not mesa:
                return None

            # Buscar comanda activa
            comanda = self.tpv_service.get_comanda_activa(mesa_id)
            if not comanda:
                # Crear nueva comanda
                comanda = self.tpv_service.crear_comanda(mesa_id)
                self.status_changed.emit(f"Nueva comanda creada para Mesa {mesa.numero}")
            else:
                self.status_changed.emit(f"Comanda existente cargada para Mesa {mesa.numero}")

            # Almacenar en caché
            if comanda:
                self._active_orders[mesa_id] = comanda
                self.comanda_updated.emit(comanda)

            return comanda

        except Exception as e:
            logger.error(f"Error al abrir mesa {mesa_id}: {e}")
            self.error_occurred.emit(f"Error al abrir mesa: {str(e)}")
            return None

    def add_product_to_order(self, mesa_id: int, producto_id: int, cantidad: int = 1) -> bool:
        """Añade un producto a la comanda de una mesa"""
        try:
            comanda = self._active_orders.get(mesa_id)
            if not comanda:
                comanda = self.open_mesa(mesa_id)
                if not comanda:
                    return False

            # Verificar que la comanda tiene ID válido
            if not hasattr(comanda, 'id') or comanda.id is None:
                self.error_occurred.emit("Comanda inválida")
                return False

            # Obtener información del producto
            producto = self.tpv_service.get_producto_por_id(producto_id)
            if not producto:
                self.error_occurred.emit("Producto no encontrado")
                return False

            # Añadir producto a la comanda
            self.tpv_service.agregar_producto_a_comanda(
                comanda.id, producto.id, producto.nombre, producto.precio, cantidad
            )

            # Actualizar comanda en caché
            updated_comanda = self.tpv_service.get_comanda_por_id(comanda.id)
            if updated_comanda:
                self._active_orders[mesa_id] = updated_comanda
                self.comanda_updated.emit(updated_comanda)
                self.producto_added.emit(comanda.id, producto_id, cantidad)
                self.status_changed.emit(f"Producto '{producto.nombre}' añadido a la comanda")

            return True

        except Exception as e:
            logger.error(f"Error al añadir producto {producto_id} a mesa {mesa_id}: {e}")
            self.error_occurred.emit(f"Error al añadir producto: {str(e)}")
            return False

    def remove_product_from_order(self, mesa_id: int, producto_id: int) -> bool:
        """Elimina un producto de la comanda"""
        try:
            comanda = self._active_orders.get(mesa_id)
            if not comanda or not hasattr(comanda, 'id') or comanda.id is None:
                return False

            self.tpv_service.eliminar_producto_de_comanda(comanda.id, producto_id)

            # Actualizar comanda en caché
            updated_comanda = self.tpv_service.get_comanda_por_id(comanda.id)
            if updated_comanda:
                self._active_orders[mesa_id] = updated_comanda
                self.comanda_updated.emit(updated_comanda)
                self.status_changed.emit("Producto eliminado de la comanda")

            return True

        except Exception as e:
            logger.error(f"Error al eliminar producto {producto_id} de mesa {mesa_id}: {e}")
            self.error_occurred.emit(f"Error al eliminar producto: {str(e)}")
            return False

    def update_product_quantity(self, mesa_id: int, producto_id: int, nueva_cantidad: int) -> bool:
        """Actualiza la cantidad de un producto en la comanda"""
        try:
            comanda = self._active_orders.get(mesa_id)
            if not comanda or not hasattr(comanda, 'id') or comanda.id is None:
                return False

            self.tpv_service.cambiar_cantidad_producto(comanda.id, producto_id, nueva_cantidad)

            # Actualizar comanda en caché
            updated_comanda = self.tpv_service.get_comanda_por_id(comanda.id)
            if updated_comanda:
                self._active_orders[mesa_id] = updated_comanda
                self.comanda_updated.emit(updated_comanda)
                self.status_changed.emit(f"Cantidad actualizada a {nueva_cantidad}")

            return True

        except Exception as e:
            logger.error(f"Error al actualizar cantidad en mesa {mesa_id}: {e}")
            self.error_occurred.emit(f"Error al actualizar cantidad: {str(e)}")
            return False

    def save_order(self, mesa_id: int) -> bool:
        """Guarda la comanda actual"""
        try:
            comanda = self._active_orders.get(mesa_id)
            if not comanda or not hasattr(comanda, 'id') or comanda.id is None:
                return False

            self.tpv_service.guardar_comanda(comanda.id)
            self.status_changed.emit("Comanda guardada correctamente")
            return True

        except Exception as e:
            logger.error(f"Error al guardar comanda de mesa {mesa_id}: {e}")
            self.error_occurred.emit(f"Error al guardar comanda: {str(e)}")
            return False

    def process_payment(self, mesa_id: int, payment_data: Dict[str, Any]) -> bool:
        """Procesa el pago de una comanda"""
        try:
            comanda = self._active_orders.get(mesa_id)
            if not comanda or not hasattr(comanda, 'id') or comanda.id is None:
                return False

            # Procesar pago (aquí se puede implementar diferentes métodos)
            self.tpv_service.pagar_comanda(comanda.id)

            # Liberar mesa
            self.tpv_service.liberar_mesa(mesa_id)

            # Limpiar caché
            if mesa_id in self._active_orders:
                del self._active_orders[mesa_id]

            # Actualizar estado de mesa
            mesa = self.get_mesa_by_id(mesa_id)
            if mesa:
                self.mesa_updated.emit(mesa)

            self.status_changed.emit("Pago procesado correctamente")
            return True

        except Exception as e:
            logger.error(f"Error al procesar pago de mesa {mesa_id}: {e}")
            self.error_occurred.emit(f"Error al procesar pago: {str(e)}")
            return False

    def get_active_comandas(self) -> List[Comanda]:
        """Obtiene todas las comandas activas"""
        try:
            return self.tpv_service.get_comandas_activas()
        except Exception as e:
            logger.error(f"Error al obtener comandas activas: {e}")
            self.error_occurred.emit(f"Error al cargar comandas: {str(e)}")
            return []

    def get_all_productos(self) -> List[Producto]:
        """Obtiene todos los productos disponibles"""
        try:
            return self.tpv_service.get_todos_productos()
        except Exception as e:
            logger.error(f"Error al obtener productos: {e}")
            self.error_occurred.emit(f"Error al cargar productos: {str(e)}")
            return []

    def get_productos_by_categoria(self, categoria: str) -> List[Producto]:
        """Obtiene productos filtrados por categoría"""
        try:
            if categoria == "Todas":
                return self.get_all_productos()
            return self.tpv_service.get_productos_por_categoria(categoria)
        except Exception as e:
            logger.error(f"Error al obtener productos por categoría {categoria}: {e}")
            self.error_occurred.emit(f"Error al filtrar productos: {str(e)}")
            return []

    def get_categorias(self) -> List[str]:
        """Obtiene todas las categorías de productos"""
        try:
            return self.tpv_service.get_categorias_productos()
        except Exception as e:
            logger.error(f"Error al obtener categorías: {e}")
            self.error_occurred.emit(f"Error al cargar categorías: {str(e)}")
            return []

    def get_order_total(self, mesa_id: int) -> float:
        """Calcula el total de una comanda"""
        comanda = self._active_orders.get(mesa_id)
        if not comanda or not comanda.lineas:
            return 0.0
        return sum(linea.total for linea in comanda.lineas)

    def clear_cache(self):
        """Limpia la caché de comandas activas"""
        self._active_orders.clear()
        self.status_changed.emit("Caché limpiada")
