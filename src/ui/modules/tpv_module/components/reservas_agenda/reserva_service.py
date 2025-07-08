"""
Servicio centralizado para gestión de reservas con persistencia en SQLite.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional
from core.hefest_data_models import Reserva


class ReservaService:
    def editar_reserva(self, reserva_id: int, datos: dict) -> bool:
        """Actualiza los datos de una reserva existente. Solo permite editar si la reserva está activa o futura."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # Solo permitir edición si la reserva está activa o confirmada
            c.execute("SELECT estado FROM reservas WHERE id = ?", (reserva_id,))
            row = c.fetchone()
            if not row or row[0] not in ("activa", "confirmada"):
                return False
            # Actualizar campos editables
            campos = []
            valores = []
            for campo, valor in [
                ("cliente", datos.get("cliente")),
                ("fecha_hora", datos.get("fecha_hora")),
                ("duracion_min", datos.get("duracion_min")),
                ("telefono", datos.get("telefono")),
                ("personas", datos.get("personas")),
                ("notas", datos.get("notas")),
            ]:
                if valor is not None:
                    campos.append(f"{campo} = ?")
                    if campo == "fecha_hora" and hasattr(valor, "isoformat"):
                        valores.append(valor.isoformat())
                    else:
                        valores.append(valor)
            if not campos:
                return False
            valores.append(reserva_id)
            sql = f"UPDATE reservas SET {', '.join(campos)} WHERE id = ?"
            c.execute(sql, valores)
            conn.commit()
        return True

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self):
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS reservas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mesa_id TEXT NOT NULL,
                    cliente TEXT NOT NULL,
                    fecha_hora TEXT NOT NULL,
                    duracion_min INTEGER NOT NULL,
                    estado TEXT NOT NULL,
                    notas TEXT,
                    telefono TEXT,
                    personas INTEGER
                )
            """
            )
            conn.commit()

    def crear_reserva(
        self,
        mesa_id: str,
        cliente: str,
        fecha_hora: datetime,
        duracion_min: int,
        telefono: Optional[str] = None,
        personas: Optional[int] = None,
        notas: Optional[str] = None,
    ) -> Reserva:
        mesa_id_str = str(mesa_id) if mesa_id is not None else ""
        print(
            f"[ReservaService] Creando reserva: mesa_id={mesa_id_str}, cliente={cliente}, fecha_hora={fecha_hora}, duracion_min={duracion_min}, telefono={telefono}, personas={personas}, notas={notas}"
        )
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute(
                    """
                    INSERT INTO reservas (mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        mesa_id_str,
                        cliente,
                        fecha_hora.isoformat(),
                        duracion_min,
                        "activa",
                        notas,
                        telefono,
                        personas,
                    ),
                )
                reserva_id = c.lastrowid if c.lastrowid is not None else -1
                conn.commit()
            print(f"[ReservaService] Reserva creada con id={reserva_id}")
        except Exception as e:
            import traceback

            print(
                f"[ReservaService][ERROR] Error al crear reserva: {e}\n{traceback.format_exc()}"
            )
            raise
        return Reserva(
            id=int(reserva_id),
            mesa_id=mesa_id_str,
            cliente_nombre=cliente,
            cliente_telefono=telefono,
            fecha_reserva=fecha_hora.date(),
            hora_reserva=fecha_hora.strftime("%H:%M"),
            numero_personas=personas if personas is not None else 1,
            estado="activa",
            notas=notas,
        )

    def cancelar_reserva(self, reserva_id: int) -> bool:
        """Cancela la reserva cambiando su estado a 'cancelada'. Devuelve True si se modificó alguna fila."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "UPDATE reservas SET estado = ? WHERE id = ?", ("cancelada", reserva_id)
            )
            conn.commit()
            return c.rowcount > 0

    def obtener_reservas_activas(self) -> List[Reserva]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas FROM reservas WHERE estado = ?",
                ("activa",),
            )
            rows = c.fetchall()
        return [
            Reserva(
                id=row[0],
                mesa_id=str(row[1]) if row[1] is not None else None,
                cliente_nombre=row[2],
                cliente_telefono=row[7],
                fecha_reserva=datetime.fromisoformat(row[3]).date(),
                hora_reserva=datetime.fromisoformat(row[3]).strftime("%H:%M"),
                numero_personas=row[8] if row[8] is not None else 1,
                estado="confirmada",  # o row[5] si se quiere mantener el estado
                notas=row[6],
            )
            for row in rows
        ]

    def obtener_reservas_por_fecha(self, fecha: datetime) -> List[Reserva]:
        fecha_str = fecha.date().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas FROM reservas WHERE date(fecha_hora) = ? AND estado = ?",
                (fecha_str, "activa"),
            )
            rows = c.fetchall()
        return [
            Reserva(
                id=row[0],
                mesa_id=str(row[1]) if row[1] is not None else None,
                cliente_nombre=row[2],
                cliente_telefono=row[7],
                fecha_reserva=datetime.fromisoformat(row[3]).date(),
                hora_reserva=datetime.fromisoformat(row[3]).strftime("%H:%M"),
                numero_personas=row[8] if row[8] is not None else 1,
                estado="confirmada",  # o row[5]
                notas=row[6],
            )
            for row in rows
        ]

    def get_reserva(self, reserva_id: int) -> Optional[Reserva]:
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas FROM reservas WHERE id = ?",
                (reserva_id,),
            )
            row = c.fetchone()
        if row:
            return Reserva(
                id=row[0],
                mesa_id=str(row[1]) if row[1] is not None else None,
                cliente_nombre=row[2],
                cliente_telefono=row[7],
                fecha_reserva=datetime.fromisoformat(row[3]).date(),
                hora_reserva=datetime.fromisoformat(row[3]).strftime("%H:%M"),
                numero_personas=row[8] if row[8] is not None else 1,
                estado="confirmada",  # o row[5]
                notas=row[6],
            )
        return None

    def obtener_reservas_activas_por_mesa(self) -> dict:
        """Devuelve un diccionario {mesa_id: [Reserva, ...]} de reservas activas por mesa."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas FROM reservas WHERE estado = ?",
                ("activa",),
            )
            rows = c.fetchall()
        reservas_por_mesa = {}
        for row in rows:
            reserva = Reserva(
                id=row[0],
                mesa_id=str(row[1]) if row[1] is not None else None,
                cliente_nombre=row[2],
                cliente_telefono=row[7],
                fecha_reserva=datetime.fromisoformat(row[3]).date(),
                hora_reserva=datetime.fromisoformat(row[3]).strftime("%H:%M"),
                numero_personas=row[8] if row[8] is not None else 1,
                estado=row[5],  # Usar el estado real de la BD
                notas=row[6],
            )
            reservas_por_mesa.setdefault(reserva.mesa_id, []).append(reserva)
        return reservas_por_mesa
