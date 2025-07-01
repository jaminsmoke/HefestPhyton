"""
Script de migración para recrear la tabla 'reservas' con el esquema correcto.
ADVERTENCIA: Esto eliminará todas las reservas existentes.
"""
import sqlite3

DB_PATH = 'data/hefest.db'

def recreate_reservas_table():
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        # Eliminar la tabla si existe
        c.execute('DROP TABLE IF EXISTS reservas')
        # Crear la tabla con el esquema actualizado
        c.execute('''
            CREATE TABLE reservas (
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
    print("Tabla 'reservas' recreada correctamente.")

if __name__ == "__main__":
    recreate_reservas_table()
