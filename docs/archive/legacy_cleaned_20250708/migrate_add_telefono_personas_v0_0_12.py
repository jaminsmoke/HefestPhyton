# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
"""
Script de migración para añadir las columnas 'telefono' y 'personas' a la tabla 'reservas'.
Cumple con la política de versionado y estructura de docs/.
"""
import sqlite3

_ = 'data/hefest.db'

ALTERS = [
    ("telefono", "TEXT"),
    ("personas", "INTEGER")
]

def column_exists(cursor, table, column):
    """TODO: Add docstring"""
    # TODO: Add input validation
    cursor.execute(f"PRAGMA table_info({table})")
    return any(col[1] == column for col in cursor.fetchall())

def migrate():
    """TODO: Add docstring"""
    # TODO: Add input validation
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for col, coltype in ALTERS:
            if not column_exists(c, 'reservas', col):
                c.execute(f"ALTER TABLE reservas ADD COLUMN {col} {coltype}")
                print("Columna '%s' añadida a 'reservas'." % col)
            else:
                print("Columna '%s' ya existe." % col)
        conn.commit()

if __name__ == "__main__":
    migrate()
    print("Migración completada.")
