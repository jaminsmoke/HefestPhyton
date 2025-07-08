"""
Decoradores de utilidad para el sistema Hefest.
Funciones auxiliares para control de acceso y otras funcionalidades.
"""

from functools import wraps
from services.auth_service import AuthService
from core.models import Role
from PyQt6.QtWidgets import QMessageBox

def require_role(role):
    """
    Decorador que verifica si el usuario actual tiene el rol requerido
    para ejecutar una función.
    
    Args:
        role (Role): El rol mínimo requerido para ejecutar la función
    
    Returns:
        function: Función decorada que verifica permisos antes de ejecutarse
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not AuthService().has_permission(role):
                QMessageBox.warning(
                    args[0] if args else None,
                    "Acceso denegado",
                    f"Requiere permiso de {role.value} para esta acción"
                )
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
