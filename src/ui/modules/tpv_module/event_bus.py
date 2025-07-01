"""
EventBus global para eventos de reservas (creación, edición, cancelación).
Permite que cualquier componente escuche y emita eventos de reservas de forma centralizada.
"""
from PyQt6.QtCore import QObject, pyqtSignal

class ReservaEventBus(QObject):
    reserva_creada = pyqtSignal(object)   # Reserva creada o editada
    reserva_cancelada = pyqtSignal(object)  # Reserva cancelada

# Instancia global
reserva_event_bus = ReservaEventBus()
