"""
Servicio centralizado para gestión de reservas con persistencia en SQLite.
"""
import sqlite3
from datetime import datetime
from typing import List, Optional
from .reserva_model import Reserva

class ReservaService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mesa_id INTEGER NOT NULL,
                    cliente TEXT NOT NULL,
                    fecha_hora TEXT NOT NULL,
                    duracion_min INTEGER NOT NULL,
                    estado TEXT NOT NULL,
                    notas TEXT
                )
            ''')
            conn.commit()

    def crear_reserva(self, mesa_id: int, cliente: str, fecha_hora: datetime, duracion_min: int, notas: Optional[str] = None) -> Reserva:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO reservas (mesa_id, cliente, fecha_hora, duracion_min, estado, notas)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (mesa_id, cliente, fecha_hora.isoformat(), duracion_min, "activa", notas))
            reserva_id = c.lastrowid if c.lastrowid is not None else -1
            conn.commit()
        return Reserva(int(reserva_id), mesa_id, cliente, fecha_hora, duracion_min, "activa", notas)

    def cancelar_reserva(self, reserva_id: int):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('UPDATE reservas SET estado = ? WHERE id = ?', ("cancelada", reserva_id))
            conn.commit()

    def obtener_reservas_activas(self) -> List[Reserva]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas FROM reservas WHERE estado = ?', ("activa",))
            rows = c.fetchall()
        return [Reserva(id=row[0], mesa_id=row[1], cliente=row[2], fecha_hora=datetime.fromisoformat(row[3]), duracion_min=row[4], estado=row[5], notas=row[6]) for row in rows]

    def obtener_reservas_por_fecha(self, fecha: datetime) -> List[Reserva]:
        fecha_str = fecha.date().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas FROM reservas WHERE date(fecha_hora) = ? AND estado = ?', (fecha_str, "activa"))
            rows = c.fetchall()
        return [Reserva(id=row[0], mesa_id=row[1], cliente=row[2], fecha_hora=datetime.fromisoformat(row[3]), duracion_min=row[4], estado=row[5], notas=row[6]) for row in rows]

    def get_reserva(self, reserva_id: int) -> Optional[Reserva]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas FROM reservas WHERE id = ?', (reserva_id,))
            row = c.fetchone()
        if row:
            return Reserva(id=row[0], mesa_id=row[1], cliente=row[2], fecha_hora=datetime.fromisoformat(row[3]), duracion_min=row[4], estado=row[5], notas=row[6])
        return None

    def obtener_reservas_activas_por_mesa(self) -> dict:
        """Devuelve un diccionario {mesa_id: [Reserva, ...]} de reservas activas por mesa."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute('SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas FROM reservas WHERE estado = ?', ("activa",))
            rows = c.fetchall()
        reservas_por_mesa = {}
        for row in rows:
            reserva = Reserva(id=row[0], mesa_id=row[1], cliente=row[2], fecha_hora=datetime.fromisoformat(row[3]), duracion_min=row[4], estado=row[5], notas=row[6])
            reservas_por_mesa.setdefault(reserva.mesa_id, []).append(reserva)
        return reservas_por_mesa
