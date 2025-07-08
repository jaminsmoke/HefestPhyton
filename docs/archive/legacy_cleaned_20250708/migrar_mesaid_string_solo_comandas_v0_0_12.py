"""
[v0.0.12]_MIGRACION_MESAID_STRING_SOLO_COMANDAS.md
Script de migración para convertir mesa_id a TEXT en la tabla comandas y migrar los datos existentes.
Cumple con la política de versionado y estructura de docs/.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hefest.db")

MIGRATION_SQL = [
    # 1. Renombrar tabla comandas
    "ALTER TABLE comandas RENAME TO comandas_old;",
    # 2. Crear nueva tabla comandas con mesa_id TEXT
    '''
    CREATE TABLE comandas (
        id INTEGER PRIMARY KEY,
        mesa_id TEXT,
        usuario_id INTEGER,
        fecha_hora TEXT,
        estado TEXT,
        total REAL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
    );
    ''',
    # 3. Copiar datos antiguos, convirtiendo mesa_id a string (ej: 1 -> 'T01')
    """
    INSERT INTO comandas (id, mesa_id, usuario_id, fecha_hora, estado, total)
    SELECT id, 'T' || printf('%02d', mesa_id), usuario_id, fecha_hora, estado, total FROM comandas_old;
    """,
    # 4. Eliminar tabla temporal
    "DROP TABLE comandas_old;"
]

def run_migration():
    print("Iniciando migración mesa_id a string SOLO en comandas...")
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        for sql in MIGRATION_SQL:
            print(f"Ejecutando: {sql.splitlines()[0]}")
            cur.executescript(sql) if '\n' in sql else cur.execute(sql)
        conn.commit()
        print("Migración completada con éxito.")
    except Exception as e:
        print(f"Error en la migración: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
