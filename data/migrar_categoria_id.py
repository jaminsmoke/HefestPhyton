import sqlite3

DB_PATH = "data/hefest.db"

# 1. Añadir columna categoria_id a productos
# 2. Actualizar categoria_id usando el nombre de la categoría
# 3. (Opcional) Eliminar columna categoria

def migrar_categoria_id():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Añadir columna categoria_id si no existe
    cursor.execute("PRAGMA table_info(productos);")
    columns = [row[1] for row in cursor.fetchall()]
    if "categoria_id" not in columns:
        cursor.execute("ALTER TABLE productos ADD COLUMN categoria_id INTEGER;")
        print("Columna categoria_id añadida.")
    else:
        print("Columna categoria_id ya existe.")

    # 2. Actualizar categoria_id en cada producto
    cursor.execute("SELECT id, categoria FROM productos;")
    productos = cursor.fetchall()
    for prod_id, categoria_nombre in productos:
        if not categoria_nombre:
            continue
        cursor.execute("SELECT id FROM categorias WHERE nombre = ?;", (categoria_nombre,))
        result = cursor.fetchone()
        if result:
            categoria_id = result[0]
            cursor.execute("UPDATE productos SET categoria_id = ? WHERE id = ?;", (categoria_id, prod_id))
            print(f"Producto {prod_id}: categoria_id actualizado a {categoria_id}")
        else:
            print(f"Producto {prod_id}: categoría '{categoria_nombre}' no encontrada")

    conn.commit()
    # 3. (Opcional) Eliminar columna categoria
    # SQLite no permite DROP COLUMN directamente, requiere migración avanzada
    print("Migración completada. Revisa el backend para usar categoria_id.")
    conn.close()

if __name__ == "__main__":
    migrar_categoria_id()
