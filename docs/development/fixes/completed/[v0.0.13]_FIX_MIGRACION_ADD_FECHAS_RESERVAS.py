import sqlite3

DB_PATH = 'data/hefest.db'

ALTERS = [
    # Añadir columna fecha_entrada si no existe
    "ALTER TABLE reservas ADD COLUMN fecha_entrada TEXT;",
    # Añadir columna fecha_salida si no existe
    "ALTER TABLE reservas ADD COLUMN fecha_salida TEXT;"
]

def column_exists(cursor, table, column):
    cursor.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cursor.fetchall())

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        changed = False
        if not column_exists(cur, 'reservas', 'fecha_entrada'):
            cur.execute(ALTERS[0])
            print("[MIGRACION] Columna 'fecha_entrada' añadida a reservas.")
            changed = True
        if not column_exists(cur, 'reservas', 'fecha_salida'):
            cur.execute(ALTERS[1])
            print("[MIGRACION] Columna 'fecha_salida' añadida a reservas.")
            changed = True
        if changed:
            conn.commit()
            print("[MIGRACION] Migración completada.")
        else:
            print("[MIGRACION] No se requirió migración. Las columnas ya existen.")
    except Exception as e:
        print(f"[MIGRACION] Error durante la migración: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
