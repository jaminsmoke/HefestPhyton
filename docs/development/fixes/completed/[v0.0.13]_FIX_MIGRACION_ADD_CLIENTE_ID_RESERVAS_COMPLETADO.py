"""
[v0.0.13]_FIX_MIGRACION_ADD_CLIENTE_ID_RESERVAS_COMPLETADO.py
Cumple con la política de versionado y estructura de docs/.

- Añade la columna cliente_id INTEGER a la tabla reservas si no existe.
- Intenta migrar datos de la columna cliente (texto) a cliente_id usando la tabla clientes (por nombre/dni).
- Compatible con la base de datos real: data/hefest.db
"""
import sqlite3
import os

DB_PATH = 'data/hefest.db'

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(col[1] == column for col in cursor.fetchall())

def migrate():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # 1. Añadir columna cliente_id si no existe
        if not column_exists(c, 'reservas', 'cliente_id'):
            c.execute("ALTER TABLE reservas ADD COLUMN cliente_id INTEGER")
            print("Columna 'cliente_id' añadida a 'reservas'.")
        else:
            print("Columna 'cliente_id' ya existe.")

        # 2. Intentar migrar datos de cliente (texto) a cliente_id
        c.execute("SELECT id, cliente FROM reservas WHERE cliente_id IS NULL OR cliente_id = ''")
        rows = c.fetchall()
        actualizados = 0
        for reserva_id, cliente_texto in rows:
            if not cliente_texto:
                continue
            # Buscar por nombre exacto en clientes
            c.execute("SELECT id FROM clientes WHERE nombre = ? COLLATE NOCASE", (cliente_texto.strip(),))
            result = c.fetchone()
            if result:
                cliente_id = result[0]
                c.execute("UPDATE reservas SET cliente_id = ? WHERE id = ?", (cliente_id, reserva_id))
                actualizados += 1
        conn.commit()
        print(f"Actualizadas {actualizados} reservas con cliente_id.")

if __name__ == "__main__":
    migrate()
    print("Migración completada.")
