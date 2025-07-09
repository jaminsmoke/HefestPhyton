# Script para recrear la tabla comanda_detalles con la foreign key correcta (comandas)
# ¡ADVERTENCIA! Esto eliminará todos los datos de comanda_detalles.
from sqlite3 import connect

DB_PATH = 'data/hefest.db'

SQL_RECREATE = '''
PRAGMA foreign_keys=off;
DROP TABLE IF EXISTS comanda_detalles;
CREATE TABLE comanda_detalles (
    id INTEGER PRIMARY KEY,
    comanda_id INTEGER,
    producto_id INTEGER,
    cantidad INTEGER,
    precio_unitario REAL(10),
    notas TEXT,
    FOREIGN KEY (comanda_id) REFERENCES comandas(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);
PRAGMA foreign_keys=on;
'''

def main():
    conn = connect(DB_PATH)
    try:
        conn.executescript(SQL_RECREATE)
        print("Tabla comanda_detalles recreada con foreign key a comandas. Todos los datos anteriores se han eliminado.")
    except Exception as e:
        print(f"Error al ejecutar el script: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
