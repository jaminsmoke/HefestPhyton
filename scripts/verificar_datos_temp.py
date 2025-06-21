#!/usr/bin/env python3
import sqlite3
import os

# Ruta correcta a la base de datos
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
db_path = os.path.join(project_root, 'data', 'hefest.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print('=== DATOS ACTUALES DE LA BASE DE DATOS ===')
print()

# Verificar categorías
cursor.execute('SELECT id, nombre, activa FROM categorias')
cats = cursor.fetchall()
print(f'📊 CATEGORIAS (Total: {len(cats)}):')
for c in cats:
    estado = "ACTIVA" if c[2] else "INACTIVA"
    print(f'  ID: {c[0]} | Nombre: "{c[1]}" | Estado: {estado}')

print()

# Verificar proveedores
cursor.execute('SELECT id, nombre, activo FROM proveedores')
provs = cursor.fetchall()
print(f'🏢 PROVEEDORES (Total: {len(provs)}):')
for p in provs:
    estado = "ACTIVO" if p[2] else "INACTIVO"
    print(f'  ID: {p[0]} | Nombre: "{p[1]}" | Estado: {estado}')

print()

# Verificar productos para ver dependencias
cursor.execute('SELECT COUNT(*) FROM productos')
total_productos = cursor.fetchone()[0]
print(f'📦 PRODUCTOS: {total_productos} total')

# Verificar si hay productos con categorías
cursor.execute('SELECT COUNT(DISTINCT categoria_id) FROM productos WHERE categoria_id IS NOT NULL')
cats_usadas = cursor.fetchone()[0]
print(f'📊 Categorías usadas en productos: {cats_usadas}')

# Verificar si hay productos con proveedores
cursor.execute('SELECT COUNT(DISTINCT proveedor_id) FROM productos WHERE proveedor_id IS NOT NULL')
provs_usados = cursor.fetchone()[0]
print(f'🏢 Proveedores usados en productos: {provs_usados}')

conn.close()
