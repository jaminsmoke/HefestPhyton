#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')
from data.db_manager import DatabaseManager

db = DatabaseManager()

# Ver si existe la categoría ID 7
result = db.query('SELECT * FROM categorias WHERE id = 7')
print('Categoría ID 7:', result)

# Ver si hay productos con esa categoría
if result and len(result) > 0:
    categoria = result[0]
    nombre_categoria = categoria[1]  # categoria[1] es el nombre
    productos_result = db.query('SELECT COUNT(*) FROM productos WHERE categoria = ?', (nombre_categoria,))
    count = productos_result[0][0] if productos_result else 0
    print(f'Productos con categoría "{nombre_categoria}": {count}')
    
    # Intentar eliminar manualmente
    try:
        delete_result = db.execute("UPDATE categorias SET activa = 0 WHERE id = ?", (7,))
        print(f'Resultado de eliminación: {delete_result}')
    except Exception as e:
        print(f'Error en eliminación: {e}')
else:
    print('No se encontró la categoría ID 7')
