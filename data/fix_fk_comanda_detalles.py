# Script para corregir la foreign key de comanda_detalles en SQLite desde Python
import sqlite3

DB_PATH = 'data/hefest.db'

SQL_FIX = '''
PRAGMA foreign_keys=off;

CREATE TABLE IF NOT EXISTS comanda_detalles_tmp (
    id INTEGER PRIMARY KEY,
    comanda_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    precio_unitario REAL(10),
    notas TEXT,
    FOREIGN KEY (comanda_id) REFERENCES comandas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

INSERT INTO comanda_detalles_tmp (id, comanda_id, producto_id, cantidad, precio_unitario, notas)
SELECT id, comanda_id, producto_id, cantidad, precio_unitario, notas FROM comanda_detalles;

DROP TABLE comanda_detalles;
ALTER TABLE comanda_detalles_tmp RENAME TO comanda_detalles;

PRAGMA foreign_keys=on;
'''

def main():
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(SQL_FIX)
        print("Foreign key de comanda_detalles corregida (ahora apunta a comandas).")
    except Exception as e:
        print(f"Error al ejecutar el script: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
