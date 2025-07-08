"""
dependency_bus.py
Singleton para compartir dependencias críticas (como db_manager) entre componentes UI.

TODO (07/07/2025):
Excepción funcional documentada en el roadmap: Este singleton se utiliza como workaround para garantizar que
todos los componentes críticos (especialmente TPVAvanzado y diálogos) tengan acceso consistente a db_manager.
Si se implementa un sistema de inyección de dependencias más formal, migrar y eliminar este bus.
Revisar todos los puntos de entrada de TPVAvanzado y asegurar que usan el bus o inyección explícita.
"""

_dependency_bus = {}


def set_dependency(key, value):
    _dependency_bus[key] = value


def get_dependency(key, default=None):
    return _dependency_bus.get(key, default)


def clear_dependencies():
    _dependency_bus.clear()
