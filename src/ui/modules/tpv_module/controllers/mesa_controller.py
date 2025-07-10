"""
Mesa Controller - Patrón Controller para eliminar acceso directo de UI a servicios
Implementa separación de capas y mejora la arquitectura del sistema
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

_ = logging.getLogger(__name__)


class MesaController:
    """Controller para operaciones de mesa - Elimina architecture violations"""
    
    def __init__(self, tpv_service=None, reserva_service=None):
        """Inicializa el controller con servicios inyectados"""
        if not tpv_service:
            raise ValueError("tpv_service es requerido")
            
        self.tpv_service = tpv_service
        self.reserva_service = reserva_service
        logger.debug("MesaController inicializado")
    
    def get_mesa_data(self, mesa_numero: str) -> Optional[Dict[str, Any]]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene datos actualizados de una mesa"""
        try:
            mesa = self.tpv_service.get_mesa_by_id(mesa_numero)
            if not mesa:
                return None
                
            return {
                'numero': mesa.numero,
                'estado': mesa.estado,
                'capacidad': mesa.capacidad,
                'zona': mesa.zona,
                'alias': getattr(mesa, 'alias', None),
                'notas': getattr(mesa, 'notas', None),
                'personas_temporal': getattr(mesa, 'personas_temporal', None),
                'nombre_display': mesa.nombre_display,
                'personas_display': mesa.personas_display
            }
        except Exception as e:
            logger.error("Error obteniendo datos de mesa {mesa_numero}: %s", e)
            return None
    
    def get_mesa_reservas(self, mesa_numero: str) -> List[Any]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene reservas activas de una mesa"""
        try:
            if not self.reserva_service:
                return []
                
            if hasattr(self.reserva_service, 'obtener_reservas_activas_por_mesa'):
                reservas_por_mesa = self.reserva_service.obtener_reservas_activas_por_mesa()
                return reservas_por_mesa.get(mesa_numero, [])
            else:
                # Fallback para servicios que no implementan el método
                return []
        except Exception as e:
            logger.error("Error obteniendo reservas de mesa {mesa_numero}: %s", e)
            return []
    
    def update_mesa(self, mesa_numero: str, data: Dict[str, Any]) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza datos de una mesa"""
        try:
            mesa = self.tpv_service.get_mesa_by_id(mesa_numero)
            if not mesa:
                logger.warning("Mesa %s no encontrada", mesa_numero)
                return False
            
            # Actualizar campos permitidos
            if 'alias' in data:
                success = self.tpv_service.cambiar_alias_mesa(mesa_numero, data['alias'])
                if not success:
                    return False
                    
            if 'capacidad' in data:
                mesa.capacidad = data['capacidad']
                
            if 'notas' in data:
                mesa.notas = data['notas']
            
            # Actualizar mesa en el servicio
            return self.tpv_service.update_mesa(mesa)
            
        except Exception as e:
            logger.error("Error actualizando mesa {mesa_numero}: %s", e)
            return False
    
    def liberar_mesa(self, mesa_numero: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Libera una mesa"""
        try:
            return self.tpv_service.liberar_mesa(mesa_numero)
        except Exception as e:
            logger.error("Error liberando mesa {mesa_numero}: %s", e)
            return False
    
    def create_reserva(self, mesa_numero: str, reserva_data: Dict[str, Any]) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea una nueva reserva para una mesa"""
        try:
            if not self.reserva_service:
                logger.warning("Servicio de reservas no disponible")
                return False
            
            # Validar datos requeridos
            required_fields = ['cliente_nombre', 'fecha_reserva', 'hora_reserva']
            for field in required_fields:
                if field not in reserva_data:
                    logger.error("Campo requerido faltante: %s", field)
                    return False
            
            # Construir fecha_hora
            _ = datetime.combine(
                reserva_data['fecha_reserva'],
                datetime.strptime(reserva_data['hora_reserva'], "%H:%M").time()
            )
            
            # Crear reserva a través del servicio
            if hasattr(self.reserva_service, 'crear_reserva'):
                _ = self.reserva_service.crear_reserva(
                    mesa_id=mesa_numero,
                    _ = reserva_data['cliente_nombre'],
                    fecha_hora=fecha_hora,
                    _ = reserva_data.get('duracion_min', 120),
                    telefono=reserva_data.get('cliente_telefono', ''),
                    _ = reserva_data.get('numero_personas', 1),
                    notas=reserva_data.get('notas', '')
                )
                return reserva is not None
            else:
                logger.warning("Método crear_reserva no disponible en el servicio")
                return False
                
        except Exception as e:
            logger.error("Error creando reserva para mesa {mesa_numero}: %s", e)
            return False
    
    def cancel_reserva(self, reserva_id: int) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cancela una reserva"""
        try:
            if not self.reserva_service:
                return False
                
            if hasattr(self.reserva_service, 'cancelar_reserva'):
                return self.reserva_service.cancelar_reserva(reserva_id)
            else:
                logger.warning("Método cancelar_reserva no disponible")
                return False
                
        except Exception as e:
            logger.error("Error cancelando reserva {reserva_id}: %s", e)
            return False
    
    def get_mesa_history(self, mesa_numero: str) -> List[Dict[str, Any]]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene historial de una mesa"""
        try:
            # Implementación básica - puede expandirse según necesidades
            return [
                {"timestamp": datetime.now(), "action": "Mesa consultada", "details": "Historial solicitado"}
            ]
        except Exception as e:
            logger.error("Error obteniendo historial de mesa {mesa_numero}: %s", e)
            return []
    
    def validate_mesa_operation(self, mesa_numero: str, operation: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valida si una operación es permitida en una mesa"""
        try:
            mesa = self.tpv_service.get_mesa_by_id(mesa_numero)
            if not mesa:
                return False
            
            # Reglas de validación según el estado
            if operation == "liberar" and mesa.estado == "ocupada":
                # Verificar si hay comanda activa
                comanda = self.tpv_service.get_comanda_activa(mesa_numero)
                if comanda and comanda.estado in ['abierta', 'en_proceso']:
                    return False  # No se puede liberar con comanda activa
            
            return True
            
        except Exception as e:
            logger.error("Error validando operación {operation} en mesa {mesa_numero}: %s", e)
            return False
    
    def cargar_mesas(self):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Carga las mesas desde el servicio TPV"""
        try:
            if self.tpv_service:
                mesas = self.tpv_service.get_mesas()
                logger.info("Cargadas %s mesas", len(mesas))
                return mesas
            return []
        except Exception as e:
            logger.error("Error cargando mesas: %s", e)
            return []
    
    def eliminar_mesa(self, mesa_numero: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Elimina una mesa por su número"""
        try:
            if self.tpv_service:
                return self.tpv_service.eliminar_mesa_por_numero(mesa_numero)
            return False
        except Exception as e:
            logger.error("Error eliminando mesa {mesa_numero}: %s", e)
            return False
    
    def crear_mesa(self, capacidad: int, zona: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea una nueva mesa"""
        try:
            if self.tpv_service:
                mesa = self.tpv_service.crear_mesa(capacidad, zona)
                return mesa is not None
            return False
        except Exception as e:
            logger.error("Error creando mesa: %s", e)
            return False
    
    def crear_mesa_con_numero(self, numero: int, capacidad: int, zona: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea una nueva mesa con número específico"""
        try:
            if self.tpv_service:
                mesa = self.tpv_service.crear_mesa_con_numero(numero, capacidad, zona)
                return mesa is not None
            return False
        except Exception as e:
            logger.error("Error creando mesa con número: %s", e)
            return False
    
    def cambiar_estado_mesa(self, mesa_numero: str, nuevo_estado: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cambia el estado de una mesa"""
        try:
            if self.tpv_service:
                return self.tpv_service.cambiar_estado_mesa(mesa_numero, nuevo_estado)
            return False
        except Exception as e:
            logger.error("Error cambiando estado de mesa: %s", e)
            return False


class MesaControllerFactory:
    """Factory para crear instancias de MesaController"""
    
    @staticmethod
    def create(tpv_service=None, reserva_service=None) -> MesaController:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Crea una instancia de MesaController con validaciones"""
        if not tpv_service:
            raise ValueError("tpv_service es requerido para crear MesaController")
            
        return MesaController(tpv_service=tpv_service, reserva_service=reserva_service)