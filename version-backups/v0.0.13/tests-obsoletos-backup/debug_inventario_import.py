#!/usr/bin/env python3
"""
Debug script para investigar el problema de importación del InventarioService
"""
import sys
import os
import importlib

# Añadir rutas (ajustado para scripts/testing/)
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, os.path.join(project_root, 'src'))
sys.path.insert(0, project_root)

print("=== DEBUG IMPORT INVENTARIO SERVICE ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")
print(f"Python path:")
for p in sys.path:
    print(f"  {p}")

print("\n=== INVESTIGANDO IMPORTS ===")

# Test 1: Import directo
try:
    print("1. Importando desde inventario_service_real...")
    from src.services.inventario_service_real import InventarioService as InvServiceReal
    print(f"   ✅ Éxito: {InvServiceReal}")
    print(f"   Archivo: {InvServiceReal.__module__}")
    
    # Probar métodos problemáticos
    from data.db_manager import DatabaseManager
    db = DatabaseManager()
    service = InvServiceReal(db)
    
    print("   Probando get_categorias...")
    result = service.get_categorias()
    print(f"   ✅ get_categorias funciona: {result}")
    
    print("   Probando crear_categoria...")
    result = service.crear_categoria("Test", "Test desc")
    print(f"   ✅ crear_categoria funciona: {result}")
    
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Import desde services module
try:
    print("\n2. Importando desde services module...")
    from src.services import InventarioService as InvServiceModule
    print(f"   ✅ Éxito: {InvServiceModule}")
    print(f"   Archivo: {InvServiceModule.__module__}")
    print(f"   Son la misma clase: {InvServiceReal is InvServiceModule}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: El import problemático de los tests
try:
    print("\n3. Probando import problemático (services.inventario_service)...")
    # Este import está destinado a fallar para probar el manejo de errores
    import importlib
    module = importlib.import_module('services.inventario_service')
    InvServiceProblematic = getattr(module, 'InventarioService')
    print(f"   ✅ Éxito: {InvServiceProblematic}")
    print(f"   Archivo: {InvServiceProblematic.__module__}")
except Exception as e:
    print(f"   ❌ Error (esperado): {e}")

print("\n=== INVESTIGANDO MÉTODOS DB_MANAGER ===")
try:
    from data.db_manager import DatabaseManager
    db = DatabaseManager()
    print(f"DatabaseManager disponible: {type(db)}")
    print("Métodos disponibles en DatabaseManager:")
    methods = [m for m in dir(db) if not m.startswith('_')]
    for method in sorted(methods):
        print(f"  - {method}")
    
    # Verificar métodos problemáticos
    has_fetch_all = hasattr(db, 'fetch_all')
    has_get_last_insert_id = hasattr(db, 'get_last_insert_id')
    print(f"\n¿Tiene fetch_all? {has_fetch_all}")
    print(f"¿Tiene get_last_insert_id? {has_get_last_insert_id}")
    
except Exception as e:
    print(f"Error con DatabaseManager: {e}")

print("\n=== FIN DEBUG ===")
