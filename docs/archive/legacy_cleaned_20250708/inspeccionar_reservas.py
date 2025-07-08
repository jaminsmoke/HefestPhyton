import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "hefest.db")

with sqlite3.connect(db_path) as conn:
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(reservas);")
    columns = cur.fetchall()
    print("Estructura de la tabla reservas:")
    for col in columns:
        print(col)
