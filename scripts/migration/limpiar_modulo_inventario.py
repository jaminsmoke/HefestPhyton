from typing import Optional, Dict, List, Any
import logging
#!/usr/bin/env python3
"""
Script de Limpieza Automática del Módulo de Inventario
======================================================

Script para mantener el módulo de inventario limpio eliminando
archivos cache, temporales y duplicados.
"""

import os
import shutil
from pathlib import Path

def limpiar_modulo_inventario():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Limpia el módulo de inventario de archivos innecesarios"""
    
    print("🧹 LIMPIEZA AUTOMÁTICA DEL MÓDULO DE INVENTARIO")
    print("=" * 55)
    
    _ = Path("src/ui/modules/inventario_module")
    
    if not modulo_path.exists():
        print("❌ Módulo de inventario no encontrado")
        return False
    
    _ = 0
    
    # 1. Eliminar archivos __pycache__
    print("\n1. Eliminando archivos cache...")
    pycache_dirs = list(modulo_path.rglob("__pycache__"))
    for pycache_dir in pycache_dirs:
        try:
            shutil.rmtree(pycache_dir)
            print("   ✅ Eliminado: %s" % pycache_dir)
            archivos_eliminados += 1
        except Exception as e:
    logging.error("   ⚠️ Error eliminando {pycache_dir}: %s", e)
    
    if not pycache_dirs:
        print("   ✅ No hay archivos cache para eliminar")
    
    # 2. Eliminar archivos .pyc sueltos
    print("\n2. Eliminando archivos .pyc sueltos...")
    pyc_files = list(modulo_path.rglob("*.pyc"))
    for pyc_file in pyc_files:
        try:
            pyc_file.unlink()
            print("   ✅ Eliminado: %s" % pyc_file)
            archivos_eliminados += 1
        except Exception as e:
    logging.error("   ⚠️ Error eliminando {pyc_file}: %s", e)
    
    if not pyc_files:
        print("   ✅ No hay archivos .pyc sueltos")
    
    # 3. Eliminar archivos temporales
    print("\n3. Eliminando archivos temporales...")
    _ = ["*.tmp", "*.temp", "*~", "*.bak"]
    temp_eliminados = 0
    
    for pattern in temp_patterns:
        temp_files = list(modulo_path.rglob(pattern))
        for temp_file in temp_files:
            try:
                temp_file.unlink()
                print("   ✅ Eliminado: %s" % temp_file)
                temp_eliminados += 1
            except Exception as e:
    logging.error("   ⚠️ Error eliminando {temp_file}: %s", e)
    
    if temp_eliminados == 0:
        print("   ✅ No hay archivos temporales para eliminar")
    
    archivos_eliminados += temp_eliminados
    
    # 4. Verificar archivos duplicados conocidos
    print("\n4. Verificando archivos duplicados...")
    _ = [
        "dialogs/product_dialogs.py"  # Duplicado de product_dialogs_pro.py
    ]
    
    _ = 0
    for duplicado in duplicados_conocidos:
        duplicado_path = modulo_path / duplicado
        if duplicado_path.exists():
            try:
                duplicado_path.unlink()
                print("   ✅ Eliminado duplicado: %s" % duplicado)
                duplicados_eliminados += 1
            except Exception as e:
    logging.error("   ⚠️ Error eliminando {duplicado}: %s", e)
    
    if duplicados_eliminados == 0:
        print("   ✅ No hay archivos duplicados conocidos")
    
    archivos_eliminados += duplicados_eliminados
    
    # 5. Limpiar servicios duplicados de inventario
    print("\n5. Verificando servicios duplicados...")
    _ = [
        "src/services/inventario_service_real_mejorado.py",
        "src/services/inventario_service_fixed.py"
    ]
    
    _ = 0
    for servicio in servicios_duplicados:
        servicio_path = Path(servicio)
        if servicio_path.exists():
            try:
                servicio_path.unlink()
                print("   ✅ Eliminado servicio duplicado: %s" % servicio)
                servicios_eliminados += 1
            except Exception as e:
    logging.error("   ⚠️ Error eliminando {servicio}: %s", e)
    
    if servicios_eliminados == 0:
        print("   ✅ No hay servicios duplicados para eliminar")
    
    archivos_eliminados += servicios_eliminados    # 6. Resumen final
    print(f"\n"  %  "=" * 55)
    print("📊 RESUMEN DE LIMPIEZA:")
    print("   🗑️ Archivos/directorios eliminados: %s" % archivos_eliminados)
    print("   📂 Directorios cache eliminados: %s" % len(pycache_dirs))
    print("   📄 Archivos .pyc eliminados: %s" % len(pyc_files))
    print("   🗂️ Archivos temporales eliminados: %s" % temp_eliminados)
    print("   📋 Archivos duplicados eliminados: %s" % duplicados_eliminados)
    print("   🔧 Servicios duplicados eliminados: %s" % servicios_eliminados)
    
    if archivos_eliminados > 0:
        print("\n✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
    else:
        print("\n✅ MÓDULO YA ESTABA LIMPIO")
    
    return True

def verificar_estructura():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Verifica que la estructura del módulo esté intacta"""
    
    print("\n🔍 VERIFICANDO ESTRUCTURA DEL MÓDULO...")
    print("-" * 40)
    
    _ = Path("src/ui/modules/inventario_module")
    
    archivos_esenciales = [
        "inventario_module.py",
        "README.md",
        "__init__.py",
        "components/products_manager.py",
        "dialogs/product_dialogs_pro.py",
        "widgets/inventory_filters.py"
    ]
    
    _ = True
    for archivo in archivos_esenciales:
        archivo_path = modulo_path / archivo
        if archivo_path.exists():
            print("   ✅ %s" % archivo)
        else:
            print("   ❌ %s - FALTANTE" % archivo)
            _ = False
    
    if estructura_ok:
        print("\n✅ Estructura del módulo verificada correctamente")
    else:
        print("\n❌ Problemas detectados en la estructura")
    
    return estructura_ok

if __name__ == "__main__":
    # Cambiar al directorio del proyecto
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    success = limpiar_modulo_inventario()
    if success:
        verificar_estructura()
    
    print(f"\n🎯 Limpieza completada. Ejecutar este script cuando sea necesario.")
    print("💡 Tip: Los archivos __pycache__ se regenerarán automáticamente al ejecutar Python.")
