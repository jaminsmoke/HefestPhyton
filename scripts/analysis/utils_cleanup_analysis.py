#!/usr/bin/env python3
"""
Análisis de archivos obsoletos en la carpeta utils/
"""

import os
import sys

def analyze_utils_folder():
    """Analiza archivos en utils/ y determina cuáles son obsoletos"""
    
    base_path = "src/utils"
    
    # Archivos actuales en utils/
    current_files = [
        "advanced_config.py",           # ✅ ACTIVO - Configuración avanzada
        "animation_helper.py",          # ✅ ACTIVO - Helper de animaciones
        "config.py",                    # ✅ ACTIVO - Configuración base 
        "decorators.py",                # ✅ ACTIVO - Decoradores útiles
        "modern_styles.py",             # ✅ ACTIVO - Estilos principales usados en main.py
        "modern_style_bypass.py",       # 🔄 REVISAR - Sistema bypass, poco usado
        "monitoring.py",                # ✅ ACTIVO - Monitoreo del sistema
        "qt_css_compat.py",            # ✅ ACTIVO - Usado en main.py y main_window.py
        "qt_smart_css.py",             # ❌ OBSOLETO - Duplicado de qt_smart_css_fixed.py
        "qt_smart_css_fixed.py",       # 🔄 REVISAR - Versión "fixed", pero no veo uso activo
        "__init__.py"                   # ✅ ACTIVO - Archivo de paquete
    ]
    
    print("=" * 80)
    print("ANÁLISIS DE LIMPIEZA - CARPETA UTILS/")
    print("=" * 80)
    
    print("\n📋 ARCHIVOS ACTIVOS (MANTENER):")
    active_files = [
        "advanced_config.py",
        "animation_helper.py", 
        "config.py",
        "decorators.py",
        "modern_styles.py",
        "monitoring.py",
        "qt_css_compat.py",
        "__init__.py"
    ]
    
    for file in active_files:
        print(f"  ✅ {file}")
    
    print("\n🗑️  ARCHIVOS OBSOLETOS/DUPLICADOS (ELIMINAR):")
    obsolete_files = [
        "qt_smart_css.py",              # Duplicado de qt_smart_css_fixed.py
        "qt_smart_css_fixed.py"         # No se usa activamente, solo en backups
    ]
    
    for file in obsolete_files:
        print(f"  ❌ {file}")
    
    print("\n🔍 ARCHIVOS A REVISAR:")
    review_files = [
        "modern_style_bypass.py"        # Usado solo internamente, evaluar necesidad
    ]
    
    for file in review_files:
        print(f"  🔄 {file}")
    
    print("\n" + "=" * 80)
    print("PLAN DE LIMPIEZA UTILS/")
    print("=" * 80)
    
    print("\n📁 FASE 1: Crear backup de utils/")
    print(f"  • Copiar carpeta utils/ a version-backups/v0.0.12/utils-cleanup-backup/")
    
    print("\n🗑️ FASE 2: Eliminar archivos obsoletos")
    for file in obsolete_files:
        print(f"  • Eliminar src/utils/{file}")
    
    print("\n🔍 FASE 3: Revisar modern_style_bypass.py")
    print("  • Verificar si modern_style_bypass.py tiene uso real")
    print("  • Si no se usa, eliminarlo también")
    
    print("\n🧹 FASE 4: Limpiar __pycache__")
    print("  • Eliminar src/utils/__pycache__/")
    
    print("\n✅ FASE 5: Verificar imports")
    print("  • Buscar imports a archivos eliminados")
    print("  • Corregir referencias rotas")
    
    return {
        'active': active_files,
        'obsolete': obsolete_files, 
        'review': review_files
    }

if __name__ == "__main__":
    result = analyze_utils_folder()
    
    print(f"\n📊 RESUMEN:")
    print(f"  • Archivos activos: {len(result['active'])}")
    print(f"  • Archivos obsoletos: {len(result['obsolete'])}")
    print(f"  • Archivos a revisar: {len(result['review'])}")
    print(f"  • Total archivos analizados: {len(result['active']) + len(result['obsolete']) + len(result['review'])}")
