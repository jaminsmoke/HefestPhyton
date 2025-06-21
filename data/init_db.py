import sqlite3
import os

def initialize_database():
    # Asegurar que estamos en el directorio correcto
    db_path = os.path.join(os.path.dirname(__file__), 'hefest.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Crear tablas
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        role TEXT NOT NULL,
        pin TEXT NOT NULL,
        email TEXT,
        telefono TEXT,
        fecha_creacion TEXT,
        is_active BOOLEAN DEFAULT 1,
        ultimo_acceso TEXT
    )''')    # Insertar datos iniciales
    usuarios_default = [
        (1, 'admin', 'ADMIN', 'admin123', 'admin@hefest.com', '+34-600-000-001', '2025-06-11', 1, None),
        (2, 'manager', 'MANAGER', 'manager123', 'manager@hefest.com', '+34-600-000-002', '2025-06-11', 1, None),
        (3, 'employee', 'EMPLOYEE', 'employee123', 'empleado@hefest.com', '+34-600-000-003', '2025-06-11', 1, None)
    ]
    cursor.executemany('''INSERT INTO usuarios (id, nombre, role, pin, email, telefono, fecha_creacion, is_active, ultimo_acceso)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', usuarios_default)

    connection.commit()
    connection.close()

if __name__ == '__main__':
    initialize_database()