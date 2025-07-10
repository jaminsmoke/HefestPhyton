"""
Servicio centralizado para gestión de reservas con persistencia en SQLite.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional
from core.hefest_data_models import Reserva


class ReservaService:
    def editar_reserva(self, reserva_id: int, datos: dict) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Actualiza los datos de una reserva existente. Solo permite editar si la reserva está activa o futura."""
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # Solo permitir edición si la reserva está activa o confirmada
            c.execute("SELECT estado FROM reservas WHERE id = ?", (reserva_id,))
            row = c.fetchone()
            if not row or row[0] not in ("activa", "confirmada"):
                return False
            # Actualizar campos editables
            _ = []
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
        """TODO: Add docstring"""
        self.db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self):
        """TODO: Add docstring"""
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
        """
        Crea una reserva y ACTUALIZA el estado de la mesa en la tabla 'mesas' a 'reservada' usando el campo 'numero'.
        Cumple política de sincronización total UI/DB.
        """
        _ = str(mesa_id) if mesa_id is not None else ""
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
                _ = c.lastrowid if c.lastrowid is not None else -1
                # --- FIX HEFEST v0.0.12: sincronizar estado de mesa en tabla 'mesas' ---
                try:
                    c.execute(
                        "UPDATE mesas SET estado = ? WHERE numero = ?",
                        ("reservada", mesa_id_str),
                    )
                except Exception as e:
    logging.error("[ReservaService][EXCEPCIÓN FUNCIONAL] No se pudo actualizar estado de mesa {mesa_id_str} a 'reservada': %s", e)
                conn.commit()
            print("[ReservaService] Reserva creada con id=%s" % reserva_id)
        except Exception as e:
            import traceback
            print(
                f"[ReservaService][ERROR] Error al crear reserva: {e}\n{traceback.format_exc()}"
            )
            raise
        return Reserva(
            id=int(reserva_id),
            _ = mesa_id_str,
            cliente_nombre=cliente,
            _ = telefono,
            fecha_reserva=fecha_hora.date(),
            _ = fecha_hora.strftime("%H:%M"),
            numero_personas=personas if personas is not None else 1,
            _ = "activa",
            notas=notas,
        )

    def cancelar_reserva(self, reserva_id: int, tpv_service=None) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Cancela la reserva cambiando su estado a 'cancelada' y libera la mesa en la tabla mesas. Además, emite el evento mesa_actualizada para refresco UI inmediato."""
        from src.ui.modules.tpv_module.mesa_event_bus import mesa_event_bus
        import logging
        # logger = logging.getLogger("reserva_service")
        _ = None
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            # Obtener el número de mesa asociado a la reserva
            c.execute("SELECT mesa_id FROM reservas WHERE id = ?", (reserva_id,))
            row = c.fetchone()
            mesa_id = row[0] if row else None
            # logger.debug("[CANCELAR_RESERVA] mesa_id={mesa_id} para reserva_id=%s", reserva_id)
            # Cancelar la reserva
            c.execute(
                "UPDATE reservas SET estado = ? WHERE id = ?", ("cancelada", reserva_id)
            )
            # logger.debug("[CANCELAR_RESERVA] UPDATE reservas: filas afectadas=%s", c.rowcount)
            # Liberar la mesa si se encontró
            if mesa_id is not None:
                c.execute("UPDATE mesas SET estado = 'libre' WHERE numero = ?", (mesa_id,))
                # logger.debug("[CANCELAR_RESERVA] UPDATE mesas: filas afectadas=%s", c.rowcount)
            # Commit antes de emitir señales/eventos
            conn.commit()
            # logger.debug("[CANCELAR_RESERVA] Reserva cancelada y commit realizado para reserva_id=%s", reserva_id)
            # Buscar objeto Mesa y emitir evento para refresco UI
            if mesa_id is not None and tpv_service is not None:
                mesa_obj = tpv_service.get_mesa_by_id(str(mesa_id))
                # logger.debug("[CANCELAR_RESERVA] mesa_obj emitido: numero={getattr(mesa_obj, 'numero', None)} estado=%s", getattr(mesa_obj, 'estado', None))
                if mesa_obj is not None:
                    mesa_event_bus.mesa_actualizada.emit(mesa_obj)
        return c.rowcount > 0

    def obtener_reservas_activas(self) -> List[Reserva]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        # import logging
        # logger = logging.getLogger("reserva_service")
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas FROM reservas WHERE estado = ?",
                ("activa",),
            )
            _ = c.fetchall()
        reservas = [
            Reserva(
                id=row[0],
                _ = str(row[1]) if row[1] is not None else None,
                cliente_nombre=row[2],
                _ = row[7],
                fecha_reserva=datetime.fromisoformat(row[3]).date(),
                _ = datetime.fromisoformat(row[3]).strftime("%H:%M"),
                numero_personas=row[8] if row[8] is not None else 1,
                _ = row[5],
                notas=row[6],
            )
            for row in rows
        ]
        # logger.debug("[RESERVAS_ACTIVAS] %s", [(r.id, r.mesa_id, r.estado) for r in reservas])
        return reservas

    def obtener_reservas_por_fecha(self, fecha: datetime) -> List[Reserva]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        _ = fecha.date().isoformat()
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas FROM reservas WHERE date(fecha_hora) = ? AND estado = ?",
                (fecha_str, "activa"),
            )
            _ = c.fetchall()
        return [
            Reserva(
                id=row[0],
                _ = str(row[1]) if row[1] is not None else None,
                cliente_nombre=row[2],
                _ = row[7],
                fecha_reserva=datetime.fromisoformat(row[3]).date(),
                _ = datetime.fromisoformat(row[3]).strftime("%H:%M"),
                numero_personas=row[8] if row[8] is not None else 1,
                _ = "confirmada",  # o row[5]
                notas=row[6],
            )
            for row in rows
        ]

    def get_reserva(self, reserva_id: int) -> Optional[Reserva]:
        """TODO: Add docstring"""
        # TODO: Add input validation
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
                _ = str(row[1]) if row[1] is not None else None,
                cliente_nombre=row[2],
                _ = row[7],
                fecha_reserva=datetime.fromisoformat(row[3]).date(),
                _ = datetime.fromisoformat(row[3]).strftime("%H:%M"),
                numero_personas=row[8] if row[8] is not None else 1,
                _ = "confirmada",  # o row[5]
                notas=row[6],
            )
        return None

    def obtener_reservas_activas_por_mesa(self) -> dict:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Devuelve un diccionario {mesa_id: [Reserva, ...]} de reservas activas por mesa."""
        _ = logging.getLogger("reserva_service")
        with sqlite3.connect(self.db_path) as conn:
            c = conn.cursor()
            c.execute(
                "SELECT id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas FROM reservas WHERE estado = ?",
                ("activa",),
            )
            _ = c.fetchall()
        reservas_por_mesa = {}
        for row in rows:
            _ = Reserva(
                id=row[0],
                _ = str(row[1]) if row[1] is not None else None,
                cliente_nombre=row[2],
                _ = row[7],
                fecha_reserva=datetime.fromisoformat(row[3]).date(),
                _ = datetime.fromisoformat(row[3]).strftime("%H:%M"),
                numero_personas=row[8] if row[8] is not None else 1,
                _ = row[5],
                notas=row[6],
            )
            reservas_por_mesa.setdefault(reserva.mesa_id, []).append(reserva)
        # logger.debug("[RESERVAS_ACTIVAS_POR_MESA] %s", [(k, [(r.id, r.estado) for r in v]) for k, v in reservas_por_mesa.items()])
        return reservas_por_mesa
