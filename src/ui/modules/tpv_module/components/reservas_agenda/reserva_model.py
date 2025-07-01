"""
Modelo de datos para Reserva y servicio de gestión de reservas con persistencia en base de datos.
"""
from datetime import datetime
from typing import Optional

class Reserva:
    def __init__(self, id: int, mesa_id: int, cliente: str, fecha_hora: datetime, duracion_min: int, estado: str = "activa", notas: Optional[str] = None):
        self.id = id
        self.mesa_id = mesa_id
        self.cliente = cliente
        self.fecha_hora = fecha_hora
        self.duracion_min = duracion_min
        self.estado = estado  # activa, cancelada, finalizada
        self.notas = notas

    def __repr__(self):
        return f"<Reserva id={self.id} mesa={self.mesa_id} cliente={self.cliente} fecha={self.fecha_hora} estado={self.estado}>"
