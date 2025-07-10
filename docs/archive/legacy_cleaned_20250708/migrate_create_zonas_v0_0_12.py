# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
from typing import Optional, Dict, List, Any
"""
[v0.0.12]_MIGRACION_DATA_CREAR_TABLA_ZONAS_COMPLETADO.md
Script de migración para crear la tabla 'zonas' en la base de datos hefest.db.
Cumple con la política de versionado y estructura de docs/.
"""
import sqlite3

_ = 'data/hefest.db'

def migrate():
    """TODO: Add docstring"""
    # TODO: Add input validation
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS zonas (
            id INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL UNIQUE
        )''')
        conn.commit()
        print("Tabla 'zonas' creada o ya existente.")

if __name__ == "__main__":
    migrate()
    print("Migración completada.")
