"""
Modelos centrales para el sistema Hefest - v0.0.12
==================================================

Define las estructuras de datos principales del sistema.
Solo incluye modelos que se están utilizando activamente.

MODELOS ACTIVOS:
- User: Modelo de usuario del sistema
- Role: Enum de roles de usuario

AUTOR: Hefest Development Team
VERSIÓN: v0.0.12
FECHA: Diciembre 2024
"""

from enum import Enum
from typing import Optional
from datetime import datetime
from dataclasses import dataclass


class Role(Enum):
    """Roles de usuario en el sistema"""

    EMPLOYEE = "employee"
    MANAGER = "manager"
    ADMIN = "admin"


@dataclass
class User:
    """Modelo de usuario del sistema"""

    id: Optional[int]
    username: str
    password: str
    name: str
    role: Role
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool = True
    last_access: Optional[datetime] = None
    created_at: Optional[datetime] = None

    @property
    def pin(self) -> str:
        """Alias para password para compatibilidad con AuthService"""
        return self.password

    @pin.setter
    def pin(self, value: str):
        """Setter para pin que actualiza password"""
        self.password = value

    def __str__(self):
        return f"User(username='{self.username}', name='{self.name}', role={self.role})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False
        return self.id == other.id
