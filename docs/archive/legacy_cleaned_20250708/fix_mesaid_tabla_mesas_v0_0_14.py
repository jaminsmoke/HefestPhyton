"""
Script de migración para convertir el campo id de la tabla mesas a string (ej: 'T01') y actualizar todas las referencias en reservas y comandas.
- Crea una nueva tabla mesas_tmp con id TEXT PRIMARY KEY.
- Copia los datos, usando el campo numero como nuevo id string.
- Actualiza reservas y comandas para que mesa_id apunte al nuevo id string.
- Elimina la tabla mesas original y renombra mesas_tmp a mesas.
"""
import sqlite3

DB_PATH = 'data/hefest.db'

def migrate_mesas_to_string_id():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # 1. Crear nueva tabla con id TEXT PRIMARY KEY
    c.execute('''
        CREATE TABLE IF NOT EXISTS mesas_tmp (
            id TEXT PRIMARY KEY,
            numero TEXT NOT NULL,
            zona TEXT,
            estado TEXT,
            capacidad INTEGER
        )
    ''')
    # 2. Copiar datos usando numero como id string
    c.execute('SELECT id, numero, zona, estado, capacidad FROM mesas')
    for row in c.fetchall():
        id_num, numero, zona, estado, capacidad = row
        id_str = numero  # Asumimos que numero es el id string real (ej: 'T01')
        c.execute('INSERT INTO mesas_tmp (id, numero, zona, estado, capacidad) VALUES (?, ?, ?, ?, ?)',
                  (id_str, numero, zona, estado, capacidad))
    # 3. Actualizar reservas y comandas para que mesa_id apunte al nuevo id string
    c.execute('SELECT id, numero FROM mesas')
    id_map = {str(row[0]): row[1] for row in c.fetchall()}  # {id_num: id_str}
    for old_id, new_id in id_map.items():
        c.execute('UPDATE reservas SET mesa_id = ? WHERE mesa_id = ?', (new_id, old_id))
        c.execute('UPDATE comandas SET mesa_id = ? WHERE mesa_id = ?', (new_id, old_id))
    # 4. Eliminar tabla original y renombrar
    c.execute('DROP TABLE mesas')
    c.execute('ALTER TABLE mesas_tmp RENAME TO mesas')
    conn.commit()
    conn.close()
    print('Migración de tabla mesas a id string completada.')

if __name__ == '__main__':
    migrate_mesas_to_string_id()
