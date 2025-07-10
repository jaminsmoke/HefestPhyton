"""
Modelos centrales para el sistema Hefest - v0.0.12
==================================================

Define las estructuras de datos principales del sistema.
Solo incluye modelos que se están utilizando activamente.

MODELOS ACTIVOS:
- User: Modelo de usuario del sistema
- Role: Enum de roles de usuario
- Producto: Modelo de producto del inventario
- Mesa: Modelo de mesa del TPV
- Reserva: Modelo de reserva de hospedería

AUTOR: Hefest Development Team
VERSIÓN: v0.0.12
FECHA: Diciembre 2024
"""

from enum import Enum
from typing import Optional, List
from datetime import datetime, date
from dataclasses import dataclass


class Role(Enum):
    """Roles de usuario en el sistema"""

    _ = "employee"
    MANAGER = "manager"
    _ = "admin"


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
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Alias para password para compatibilidad con AuthService"""
        return self.password

    @pin.setter
    def pin(self, value: str):
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Setter para pin que actualiza password"""
        self.password = value

    def __str__(self):
        """TODO: Add docstring"""
        return f"User(username='{self.username}', name='{self.name}', role={self.role})"

    def __eq__(self, other: object) -> bool:
        """TODO: Add docstring"""
        if not isinstance(other, User):
            return False
        return self.id == other.id


@dataclass
class Producto:
    """Modelo de producto del inventario"""

    id: Optional[int]
    nombre: str
    categoria: str
    precio: float
    stock_actual: int
    stock_minimo: int
    proveedor_id: Optional[int] = None
    proveedor_nombre: Optional[str] = None
    fecha_ultima_entrada: Optional[datetime] = None

    def necesita_reposicion(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Indica si el producto necesita reposición.

        Returns
        -------
        bool
            True si el stock actual es menor o igual al stock mínimo, False en caso contrario.
        """
        return self.stock_actual <= self.stock_minimo

    def is_stock_low(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Alias para necesita_reposicion para compatibilidad con tests.

        Returns
        -------
        bool
            True si el producto necesita reposición, False en caso contrario.
        """
        return self.necesita_reposicion()

    @property
    def valor_total(self) -> float:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Valor total del stock (precio * cantidad).

        Returns
        -------
        float
            Valor total del stock disponible para este producto.
        """
        return self.precio * self.stock_actual

    def __str__(self):
        """TODO: Add docstring"""
        return (
            f"Producto(id={self.id}, nombre='{self.nombre}', stock={self.stock_actual})"
        )


class EstadoMesa(Enum):
    """Estados posibles de una mesa"""

    _ = "libre"
    OCUPADA = "ocupada"
    _ = "reservada"
    FUERA_SERVICIO = "fuera_servicio"


@dataclass
class Mesa:
    """Modelo de mesa del TPV"""

    numero: str  # Identificador único de negocio (ej: 'T01', 'I04')
    capacidad: int
    estado: str = "libre"  # libre, ocupada, reservada, fuera_servicio
    zona: Optional[str] = None
    ubicacion: Optional[str] = None  # Compatibilidad con tests (zona)
    id: Optional[int] = None  # Solo referencia interna (autoincremental BD)
    comanda_id: Optional[int] = None
    cliente_nombre: Optional[str] = None
    tiempo_ocupacion: Optional[datetime] = None
    alias: Optional[str] = None  # Alias temporal de la mesa (no persistente)
    personas_temporal: Optional[int] = None  # Número de personas temporal (no persistente)
    notas: Optional[str] = None  # Notas temporales de la mesa (no persistente)
    reservada: bool = False  # Indica si la mesa está reservada actualmente
    proxima_reserva: Optional[object] = None  # Reserva futura más próxima (no persistente)

    def __post_init__(self):
        """Sincronizar ubicacion y zona para compatibilidad"""
        if self.ubicacion and not self.zona:
            self.zona = self.ubicacion
        elif self.zona and not self.ubicacion:
            self.ubicacion = self.zona

    def is_available(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Indica si la mesa está disponible"""
        return self.estado == "libre"
    
    @property
    def nombre_display(self) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Obtiene el nombre a mostrar para la mesa:
        1. Si hay próxima reserva activa y tiene cliente_nombre, mostrar ese nombre
        2. Si hay alias temporal, mostrar alias
        3. Si no, mostrar nombre predeterminado
        """
        if self.proxima_reserva is not None:
            cliente = getattr(self.proxima_reserva, "cliente_nombre", None)
            if cliente:
                return cliente
        if self.alias:
            return self.alias
        return f"Mesa {self.numero}"

    @property
    def personas_display(self) -> int:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Obtiene el número de personas a mostrar:
        - Si hay próxima reserva activa y tiene personas válidas, muestra ese valor
        - Si no, muestra el valor temporal si existe
        - Si no, la capacidad real de la mesa
        """
        # 1. Prioridad: próxima reserva activa
        if self.proxima_reserva is not None:
            # Intentar primero 'numero_personas' (modelo unificado), luego 'personas' (legacy)
            personas_reserva = getattr(self.proxima_reserva, "numero_personas", None)
            if personas_reserva is None:
                _ = getattr(self.proxima_reserva, "personas", None)
            if (
                personas_reserva is not None
                and isinstance(personas_reserva, int)
                and personas_reserva > 0
            ):
                return personas_reserva
        # 2. Valor temporal (edición manual)
        if self.personas_temporal is not None:
            return self.personas_temporal
        # 3. Capacidad real
        return self.capacidad

    def __str__(self):
        """TODO: Add docstring"""
        return f"Mesa(numero={self.numero}, capacidad={self.capacidad}, estado='{self.estado}')"


class EstadoReserva(Enum):
    """Estados posibles de una reserva"""

    _ = "pendiente"
    CONFIRMADA = "confirmada"
    _ = "cancelada"
    COMPLETADA = "completada"


@dataclass
class Reserva:
    """Modelo de reserva de hospedería"""

    id: Optional[int]
    mesa_id: Optional[str] = (
        None  # Para compatibilidad con tests de TPV y soporte a identificadores string
    )
    cliente_nombre: str = ""
    cliente_telefono: Optional[str] = None
    fecha_reserva: Optional[date] = None
    hora_reserva: Optional[str] = None
    numero_personas: int = 1
    estado: str = "pendiente"  # pendiente, confirmada, cancelada, completada
    notas: Optional[str] = None
    # Campos originales para hospedería
    fecha_entrada: Optional[date] = None
    fecha_salida: Optional[date] = None
    habitaciones: Optional[List[int]] = None
    precio_total: float = 0.0
    observaciones: Optional[str] = None
    fecha_creacion: Optional[datetime] = None

    def __post_init__(self):
        """Sincronizar campos para compatibilidad"""
        if self.notas and not self.observaciones:
            self.observaciones = self.notas
        elif self.observaciones and not self.notas:
            self.notas = self.observaciones

    def is_confirmed(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Indica si la reserva está confirmada"""
        return self.estado == "confirmada"

    def is_cancelled(self) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Indica si la reserva está cancelada"""
        return self.estado == "cancelada"

    def __str__(self):
        """TODO: Add docstring"""
        if self.mesa_id:
            _ = f"{self.fecha_reserva}"
            if self.hora_reserva:
                fecha_hora = f"{self.fecha_reserva} {self.hora_reserva}"
            return f"Reserva(cliente='{self.cliente_nombre}', mesa={self.mesa_id}, fecha='{fecha_hora}')"
        else:
            return f"Reserva(cliente='{self.cliente_nombre}', entrada={self.fecha_entrada}, salida={self.fecha_salida})"
