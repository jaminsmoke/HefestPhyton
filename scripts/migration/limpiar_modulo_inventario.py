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
    """Limpia el módulo de inventario de archivos innecesarios"""
    
    print("🧹 LIMPIEZA AUTOMÁTICA DEL MÓDULO DE INVENTARIO")
    print("=" * 55)
    
    modulo_path = Path("src/ui/modules/inventario_module")
    
    if not modulo_path.exists():
        print("❌ Módulo de inventario no encontrado")
        return False
    
    archivos_eliminados = 0
    
    # 1. Eliminar archivos __pycache__
    print("\n1. Eliminando archivos cache...")
    pycache_dirs = list(modulo_path.rglob("__pycache__"))
    for pycache_dir in pycache_dirs:
        try:
            shutil.rmtree(pycache_dir)
            print(f"   ✅ Eliminado: {pycache_dir}")
            archivos_eliminados += 1
        except Exception as e:
            print(f"   ⚠️ Error eliminando {pycache_dir}: {e}")
    
    if not pycache_dirs:
        print("   ✅ No hay archivos cache para eliminar")
    
    # 2. Eliminar archivos .pyc sueltos
    print("\n2. Eliminando archivos .pyc sueltos...")
    pyc_files = list(modulo_path.rglob("*.pyc"))
    for pyc_file in pyc_files:
        try:
            pyc_file.unlink()
            print(f"   ✅ Eliminado: {pyc_file}")
            archivos_eliminados += 1
        except Exception as e:
            print(f"   ⚠️ Error eliminando {pyc_file}: {e}")
    
    if not pyc_files:
        print("   ✅ No hay archivos .pyc sueltos")
    
    # 3. Eliminar archivos temporales
    print("\n3. Eliminando archivos temporales...")
    temp_patterns = ["*.tmp", "*.temp", "*~", "*.bak"]
    temp_eliminados = 0
    
    for pattern in temp_patterns:
        temp_files = list(modulo_path.rglob(pattern))
        for temp_file in temp_files:
            try:
                temp_file.unlink()
                print(f"   ✅ Eliminado: {temp_file}")
                temp_eliminados += 1
            except Exception as e:
                print(f"   ⚠️ Error eliminando {temp_file}: {e}")
    
    if temp_eliminados == 0:
        print("   ✅ No hay archivos temporales para eliminar")
    
    archivos_eliminados += temp_eliminados
    
    # 4. Verificar archivos duplicados conocidos
    print("\n4. Verificando archivos duplicados...")
    duplicados_conocidos = [
        "dialogs/product_dialogs.py"  # Duplicado de product_dialogs_pro.py
    ]
    
    duplicados_eliminados = 0
    for duplicado in duplicados_conocidos:
        duplicado_path = modulo_path / duplicado
        if duplicado_path.exists():
            try:
                duplicado_path.unlink()
                print(f"   ✅ Eliminado duplicado: {duplicado}")
                duplicados_eliminados += 1
            except Exception as e:
                print(f"   ⚠️ Error eliminando {duplicado}: {e}")
    
    if duplicados_eliminados == 0:
        print("   ✅ No hay archivos duplicados conocidos")
    
    archivos_eliminados += duplicados_eliminados
    
    # 5. Limpiar servicios duplicados de inventario
    print("\n5. Verificando servicios duplicados...")
    servicios_duplicados = [
        "src/services/inventario_service_real_mejorado.py",
        "src/services/inventario_service_fixed.py"
    ]
    
    servicios_eliminados = 0
    for servicio in servicios_duplicados:
        servicio_path = Path(servicio)
        if servicio_path.exists():
            try:
                servicio_path.unlink()
                print(f"   ✅ Eliminado servicio duplicado: {servicio}")
                servicios_eliminados += 1
            except Exception as e:
                print(f"   ⚠️ Error eliminando {servicio}: {e}")
    
    if servicios_eliminados == 0:
        print("   ✅ No hay servicios duplicados para eliminar")
    
    archivos_eliminados += servicios_eliminados    # 6. Resumen final
    print(f"\n" + "=" * 55)
    print("📊 RESUMEN DE LIMPIEZA:")
    print(f"   🗑️ Archivos/directorios eliminados: {archivos_eliminados}")
    print(f"   📂 Directorios cache eliminados: {len(pycache_dirs)}")
    print(f"   📄 Archivos .pyc eliminados: {len(pyc_files)}")
    print(f"   🗂️ Archivos temporales eliminados: {temp_eliminados}")
    print(f"   📋 Archivos duplicados eliminados: {duplicados_eliminados}")
    print(f"   🔧 Servicios duplicados eliminados: {servicios_eliminados}")
    
    if archivos_eliminados > 0:
        print("\n✅ LIMPIEZA COMPLETADA EXITOSAMENTE")
    else:
        print("\n✅ MÓDULO YA ESTABA LIMPIO")
    
    return True

def verificar_estructura():
    """Verifica que la estructura del módulo esté intacta"""
    
    print("\n🔍 VERIFICANDO ESTRUCTURA DEL MÓDULO...")
    print("-" * 40)
    
    modulo_path = Path("src/ui/modules/inventario_module")
    
    archivos_esenciales = [
        "inventario_module.py",
        "README.md",
        "__init__.py",
        "components/products_manager.py",
        "dialogs/product_dialogs_pro.py",
        "widgets/inventory_filters.py"
    ]
    
    estructura_ok = True
    for archivo in archivos_esenciales:
        archivo_path = modulo_path / archivo
        if archivo_path.exists():
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - FALTANTE")
            estructura_ok = False
    
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
