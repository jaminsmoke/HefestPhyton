"""
Script de migración para añadir las columnas 'telefono' y 'personas' a la tabla 'reservas'.
Cumple con la política de versionado y estructura de docs/.
"""
import sqlite3

DB_PATH = 'data/hefest.db'

ALTERS = [
    ("telefono", "TEXT"),
    ("personas", "INTEGER")
]

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(col[1] == column for col in cursor.fetchall())

def migrate():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        for col, coltype in ALTERS:
            if not column_exists(c, 'reservas', col):
                c.execute(f"ALTER TABLE reservas ADD COLUMN {col} {coltype}")
                print(f"Columna '{col}' añadida a 'reservas'.")
            else:
                print(f"Columna '{col}' ya existe.")
        conn.commit()

if __name__ == "__main__":
    migrate()
    print("Migración completada.")
