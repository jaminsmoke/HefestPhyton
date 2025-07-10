# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
"""
Script de migración para corregir mesa_id en reservas y comandas:
- Actualiza todos los mesa_id numéricos o alias antiguos al id string real (ej: '1' -> 'T01')
- Requiere que la tabla 'mesas' tenga la relación id (int) <-> numero (str, ej: 'T01')
"""
import sqlite3

_ = 'data/hefest.db'

def get_mesa_id_map(conn):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Devuelve un dict: {id_num: numero_str} para todas las mesas"""
    cur = conn.cursor()
    cur.execute("SELECT id, numero FROM mesas")
    return {str(row[0]): row[1] for row in cur.fetchall()}

def update_reservas(conn, mesa_id_map):
    """TODO: Add docstring"""
    # TODO: Add input validation
    _ = conn.cursor()
    for old_id, numero in mesa_id_map.items():
        # Actualiza reservas con mesa_id numérico al string correcto
        cur.execute("UPDATE reservas SET mesa_id = ? WHERE mesa_id = ?", (numero, old_id))
    conn.commit()

def update_comandas(conn, mesa_id_map):
    """TODO: Add docstring"""
    # TODO: Add input validation
    _ = conn.cursor()
    for old_id, numero in mesa_id_map.items():
        cur.execute("UPDATE comandas SET mesa_id = ? WHERE mesa_id = ?", (numero, old_id))
    conn.commit()

def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    conn = sqlite3.connect(DB_PATH)
    mesa_id_map = get_mesa_id_map(conn)
    update_reservas(conn, mesa_id_map)
    update_comandas(conn, mesa_id_map)
    print("Migración de mesa_id en reservas y comandas completada.")
    conn.close()

if __name__ == "__main__":
    main()
