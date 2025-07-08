"""
EventBus global para eventos de mesas (creación, actualización, borrado, alias, clic, etc.).
Permite que cualquier componente escuche y emita eventos de mesas de forma centralizada.
"""

from PyQt6.QtCore import QObject, pyqtSignal


class MesaEventBus(QObject):
    # Señales para zonas (v0.0.12)
    zona_creada = pyqtSignal(object)  # Nueva zona creada (objeto o dict)
    zona_eliminada = pyqtSignal(int)  # Zona eliminada (ID)
    zonas_actualizadas = pyqtSignal(list)  # Lista de zonas actualizada
    mesa_actualizada = pyqtSignal(object)  # Mesa individual actualizada
    mesas_actualizadas = pyqtSignal(list)  # Lista de mesas actualizada
    comanda_actualizada = pyqtSignal(
        object
    )  # Comanda actualizada (alta, cambio de estado, cierre, etc.)
    mesa_creada = pyqtSignal(object)  # Nueva mesa creada
    mesa_eliminada = pyqtSignal(int)  # Mesa eliminada (ID)
    alias_cambiado = pyqtSignal(object, str)  # Mesa y nuevo alias
    mesa_clicked = pyqtSignal(object)  # Mesa clicada (global)


# Instancia global
mesa_event_bus = MesaEventBus()
