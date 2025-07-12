#!/usr/bin/env python3
"""
Script para eliminar archivos duplicados con sufijo 'modern'
Los archivos que funcionan actualmente son los que NO tienen el sufijo modern.
"""

import os
import shutil
from pathlib import Path


def cleanup_modern_duplicates():
    """Elimina archivos duplicados con sufijo 'modern'"""
    
    # Lista de archivos modern que son duplicados seguros para eliminar
    modern_files_to_remove = [
        # TPV Avanzado - archivos modern duplicados
        ("src/ui/modules/tpv_module/components/tpv_avanzado/"
         "tpv_avanzado_productos_modern.py"),
        ("src/ui/modules/tpv_module/components/tpv_avanzado/"
         "tpv_avanzado_pedido_modern.py"),
        ("src/ui/modules/tpv_module/components/tpv_avanzado/"
         "tpv_avanzado_main_modern.py"),
        ("src/ui/modules/tpv_module/components/tpv_avanzado/"
         "tpv_avanzado_integrator_modern.py"),
        ("src/ui/modules/tpv_module/components/tpv_avanzado/"
         "tpv_avanzado_header_modern.py"),
        "src/ui/modules/tpv_module/components/tpv_avanzado/styles_modern.py",
        
        # Utils modern style (debe ser refactorizado)
        "src/utils/modern_styles.py",
        
        # Dashboard admin modern (tiene duplicado)
        ("src/ui/modules/dashboard_admin_v3/"
         "ultra_modern_admin_dashboard.py")
    ]
    
    print("🧹 LIMPIEZA DE ARCHIVOS DUPLICADOS MODERN")
    print("=" * 50)
    
    # Eliminar archivos modern duplicados
    removed_count = 0
    print("\n🗑️  ELIMINANDO ARCHIVOS MODERN DUPLICADOS:")
    
    for modern_file in modern_files_to_remove:
        if os.path.exists(modern_file):
            try:
                # Crear backup en docs/archive antes de eliminar
                filename = Path(modern_file).name
                backup_dir = f"docs/archive/modern_cleanup_backup_{filename}"
                os.makedirs(backup_dir, exist_ok=True)
                backup_path = os.path.join(backup_dir, filename)
                shutil.copy2(modern_file, backup_path)
                
                # Eliminar archivo original
                os.remove(modern_file)
                print(f"  ✓ Eliminado: {modern_file}")
                print(f"    📁 Backup: {backup_path}")
                removed_count += 1
                
            except OSError as e:
                print(f"  ❌ Error eliminando {modern_file}: {e}")
        else:
            print(f"  ⚠️  {modern_file} - No existe")
    
    print("\n📊 RESUMEN:")
    print(f"  • Archivos eliminados: {removed_count}")
    print("  • Backups creados en: docs/archive/modern_cleanup_backup_*")
    
    print("\n✅ LIMPIEZA COMPLETADA")
    return removed_count


if __name__ == "__main__":
    cleanup_modern_duplicates()
