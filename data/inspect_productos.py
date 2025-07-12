import sqlite3

DB_PATH = "data/hefest.db"

# Mostrar estructura de la tabla productos
def mostrar_estructura():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("Estructura de la tabla productos:")
    cursor.execute("PRAGMA table_info(productos);")
    for row in cursor.fetchall():
        print(row)
    conn.close()

# Mostrar primeros registros de la tabla productos
def mostrar_registros():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    print("\nPrimeros 10 registros de la tabla productos:")
    cursor.execute("SELECT * FROM productos LIMIT 10;")
    for row in cursor.fetchall():
        print(row)
    conn.close()

if __name__ == "__main__":
    mostrar_estructura()
    mostrar_registros()
