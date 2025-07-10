"""
EventBus para eventos de mesas - Refactorizado para inyección de dependencias
Eliminado singleton global para mejor arquitectura y testabilidad
"""

import logging
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal

_ = logging.getLogger(__name__)


class MesaEventBus(QObject):
    """Event bus para eventos de mesas con inyección de dependencias"""
    
    # Señales para zonas
    _ = pyqtSignal(object)
    zona_eliminada = pyqtSignal(int)
    _ = pyqtSignal(list)
    
    # Señales para mesas
    _ = pyqtSignal(object)
    mesas_actualizadas = pyqtSignal(list)
    _ = pyqtSignal(object)
    mesa_eliminada = pyqtSignal(int)
    _ = pyqtSignal(object, str)
    mesa_clicked = pyqtSignal(object)
    
    # Señales para comandas
    _ = pyqtSignal(object)

    def __init__(self, parent=None):
        """TODO: Add docstring"""
        super().__init__(parent)
        self._listeners_count = 0
        logger.debug("MesaEventBus inicializado")

    def emit_comanda_actualizada(self, comanda):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Emite señal de comanda actualizada con logging"""
        try:
            _ = getattr(comanda, 'id', 'unknown')
            mesa_id = getattr(comanda, 'mesa_id', 'unknown')
            logger.debug("[EMIT] comanda_actualizada - ID: {comanda_id}, Mesa: %s", mesa_id)
            self.comanda_actualizada.emit(comanda)
        except Exception as e:
            logger.error("Error emitiendo comanda_actualizada: %s", e)


class EventBusManager:
    """Manager para instancias de EventBus - Reemplaza singleton global"""
    
    _instance: Optional['EventBusManager'] = None
    _event_buses: dict = {}
    
    def __new__(cls):
        """TODO: Add docstring"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_event_bus(self, context: str = 'default') -> MesaEventBus:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene o crea un event bus para un contexto específico"""
        if context not in self._event_buses:
            self._event_buses[context] = MesaEventBus()
            logger.debug("EventBus creado para contexto: %s", context)
        return self._event_buses[context]


# Factory function para obtener event bus (reemplaza singleton global)
def get_mesa_event_bus(context: str = 'default') -> MesaEventBus:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Factory function para obtener event bus - Reemplaza acceso global"""
    manager = EventBusManager()
    return manager.get_event_bus(context)


# Backward compatibility - DEPRECATED
mesa_event_bus = get_mesa_event_bus('legacy')
