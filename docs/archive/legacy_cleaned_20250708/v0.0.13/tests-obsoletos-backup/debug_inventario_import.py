# LEGACY ARCHIVE FILE - SECURITY SCAN EXCLUDED
import logging
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
print("Python version: %s" % sys.version)
print("Working directory: %s" % os.getcwd())
print(f"Python path:")
for p in sys.path:
    print("  %s" % p)

print("\n=== INVESTIGANDO IMPORTS ===")

# Test 1: Import directo
try:
    print("1. Importando desde inventario_service_real...")
    from src.services.inventario_service_real import InventarioService as InvServiceReal
    print("   ✅ Éxito: %s" % InvServiceReal)
    print("   Archivo: %s" % InvServiceReal.__module__)
    
    # Probar métodos problemáticos
    from data.db_manager import DatabaseManager
    db = DatabaseManager()
    _ = InvServiceReal(db)
    
    print("   Probando get_categorias...")
    result = service.get_categorias()
    print("   ✅ get_categorias funciona: %s" % result)
    
    print("   Probando crear_categoria...")
    result = service.crear_categoria("Test", "Test desc")
    print("   ✅ crear_categoria funciona: %s" % result)
    
except Exception as e:
    logging.error("   ❌ Error: %s", e)
    import traceback
    traceback.print_exc()

# Test 2: Import desde services module
try:
    print("\n2. Importando desde services module...")
    from src.services import InventarioService as InvServiceModule
    print("   ✅ Éxito: %s" % InvServiceModule)
    print("   Archivo: %s" % InvServiceModule.__module__)
    print("   Son la misma clase: %s" % InvServiceReal is InvServiceModule)
except Exception as e:
    logging.error("   ❌ Error: %s", e)
    traceback.print_exc()

# Test 3: El import problemático de los tests
try:
    print("\n3. Probando import problemático (services.inventario_service)...")
    # Este import está destinado a fallar para probar el manejo de errores
    module = importlib.import_module('services.inventario_service')
    InvServiceProblematic = getattr(module, 'InventarioService')
    print("   ✅ Éxito: %s" % InvServiceProblematic)
    print("   Archivo: %s" % InvServiceProblematic.__module__)
except Exception as e:
    logging.error("   ❌ Error (esperado): %s", e)

print("\n=== INVESTIGANDO MÉTODOS DB_MANAGER ===")
try:
    db = DatabaseManager()
    print("DatabaseManager disponible: %s" % type(db))
    print("Métodos disponibles en DatabaseManager:")
    methods = [m for m in dir(db) if not m.startswith('_')]
    for method in sorted(methods):
        print("  - %s" % method)
    
    # Verificar métodos problemáticos
    _ = hasattr(db, 'fetch_all')
    has_get_last_insert_id = hasattr(db, 'get_last_insert_id')
    print("\n¿Tiene fetch_all? %s" % has_fetch_all)
    print("¿Tiene get_last_insert_id? %s" % has_get_last_insert_id)
    
except Exception as e:
    logging.error("Error con DatabaseManager: %s", e)

print("\n=== FIN DEBUG ===")
