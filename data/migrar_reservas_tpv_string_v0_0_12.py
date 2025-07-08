"""
[v0.0.12]_MIGRACION_RESERVAS_TPV_STRING.md
Script de migración para convertir la tabla reservas al modelo TPV puro (sin campos de hospedería, con los de TPV).
Cumple con la política de versionado y estructura de docs/.
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "hefest.db")

MIGRATION_SQL = [
    # 1. Renombrar tabla antigua
    "ALTER TABLE reservas RENAME TO reservas_old;",
    # 2. Crear nueva tabla reservas con todos los campos requeridos por la lógica actual
    '''
    CREATE TABLE reservas (
        id INTEGER PRIMARY KEY,
        mesa_id TEXT,
        cliente TEXT,
        fecha_hora TEXT,
        duracion_min INTEGER,
        estado TEXT,
        notas TEXT,
        telefono TEXT,
        personas INTEGER,
        cliente_id INTEGER,
        fecha_entrada TEXT,
        fecha_salida TEXT
    );
    ''',
    # 3. Migrar los datos disponibles y dejar los nuevos campos como NULL
    '''
    INSERT INTO reservas (
        id, mesa_id, cliente, fecha_hora, duracion_min, estado, notas, telefono, personas, cliente_id, fecha_entrada, fecha_salida
    )
    SELECT
        id,
        CAST(mesa_id AS TEXT),
        NULL AS cliente,
        NULL AS fecha_hora,
        NULL AS duracion_min,
        estado,
        NULL AS notas,
        NULL AS telefono,
        NULL AS personas,
        cliente_id,
        fecha_entrada,
        fecha_salida
    FROM reservas_old;
    ''',
    # 4. Eliminar tabla temporal
    "DROP TABLE reservas_old;"
]

def run_migration():
    print("Iniciando migración de reservas al modelo TPV string...")
    conn = sqlite3.connect(DB_PATH)
    try:
        cur = conn.cursor()
        for sql in MIGRATION_SQL:
            print(f"Ejecutando: {sql.splitlines()[0]}")
            cur.executescript(sql) if ";" in sql else cur.execute(sql)
        conn.commit()
        print("Migración completada correctamente.")
    except Exception as e:
        print(f"Error en la migración: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
