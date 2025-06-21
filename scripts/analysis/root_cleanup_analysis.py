#!/usr/bin/env python3
"""
Análisis de archivos de test obsoletos en la carpeta raíz
"""

import os

def analyze_root_test_files():
    """Analiza archivos de test en la carpeta raíz y determina cuáles son obsoletos"""
    
    print("=" * 80)
    print("ANÁLISIS DE ARCHIVOS DE TEST - CARPETA RAÍZ")
    print("=" * 80)
    
    # Archivos de test encontrados en la raíz
    test_files = [
        "test_architecture_v2.py",              # ❌ OBSOLETO - Arquitectura V2
        "test_dashboard_admin_direct.py",       # ❌ OBSOLETO - Tests directos antiguos
        "test_dashboard_admin_robust.py",       # ❌ OBSOLETO - Tests robustos antiguos
        "test_dashboard_admin_v3_integration.py", # ❌ OBSOLETO - Tests integración V3 antiguos
        "test_dashboard_admin_v3_simple.py",    # ❌ OBSOLETO - Tests V3 simples antiguos
        "test_direct_no_filters.py",            # ❌ OBSOLETO - Tests sin filtros
        "test_final_responsive.py",             # ❌ OBSOLETO - Tests responsive antiguos
        "test_final_validation.py",             # ❌ OBSOLETO - Tests validación antiguos
        "test_mejoras_dashboard.py",            # ❌ OBSOLETO - Tests mejoras dashboard
        "test_responsive_cards.py",             # ❌ OBSOLETO - Tests cards responsive
        "test_robust_cards.py",                 # ❌ OBSOLETO - Tests cards robustas
        "test_ultra_modern_v3_complete.py",     # ❌ OBSOLETO - Tests V3 complete antiguos
        "test_visual_final_metricas.py",        # ❌ OBSOLETO - Tests métricas visuales
        "triple_comparison_test.py"             # ❌ OBSOLETO - Tests de comparación
    ]
    
    # Archivos de análisis/debug también a revisar
    analysis_files = [
        "debug_advanced_vs_basic.py",           # ❌ OBSOLETO - Debug comparaciones
        "debug_cards_visualization.py",         # ❌ OBSOLETO - Debug visualización cards
        "debug_labels_inspection.py",           # ❌ OBSOLETO - Debug inspección labels
        "plan_migracion_visual_v3.py",          # ❌ OBSOLETO - Plan migración ya ejecutado
        "cleanup_analysis.py",                  # ❌ OBSOLETO - Análisis ya ejecutado
        "utils_cleanup_analysis.py"             # 🔄 REVISAR - Este análisis actual
    ]
    
    print("\n🗑️  ARCHIVOS DE TEST OBSOLETOS (ELIMINAR):")
    for file in test_files:
        print(f"  ❌ {file}")
    
    print(f"\n📊 Total archivos de test obsoletos: {len(test_files)}")
    
    print("\n🗑️  ARCHIVOS DE ANÁLISIS/DEBUG OBSOLETOS (ELIMINAR):")
    for file in analysis_files[:-1]:  # Excluir el actual
        print(f"  ❌ {file}")
    
    print(f"\n📊 Total archivos de análisis obsoletos: {len(analysis_files)-1}")
    
    print("\n🔄 ARCHIVO ACTUAL (REVISAR DESPUÉS):")
    print(f"  🔄 {analysis_files[-1]}")
    
    print("\n✅ CARPETA DE TESTS OFICIAL (MANTENER):")
    print("  ✅ tests/ (carpeta con tests oficiales)")
    
    total_obsolete = len(test_files) + len(analysis_files) - 1
    print(f"\n📊 TOTAL ARCHIVOS OBSOLETOS A ELIMINAR: {total_obsolete}")
    
    return {
        'test_files': test_files,
        'analysis_files': analysis_files[:-1],  # Excluir el actual
        'total_obsolete': total_obsolete
    }

if __name__ == "__main__":
    result = analyze_root_test_files()
    
    print("\n" + "=" * 80)
    print("PLAN DE LIMPIEZA - ARCHIVOS DE TEST RAÍZ")
    print("=" * 80)
    
    print("\n📁 FASE 1: Crear backup de archivos de test")
    print("  • Crear version-backups/v0.0.12/root-tests-backup/")
    print("  • Copiar archivos obsoletos antes de eliminar")
    
    print("\n🗑️ FASE 2: Eliminar archivos de test obsoletos")
    for file in result['test_files']:
        print(f"  • Eliminar {file}")
    
    print("\n🗑️ FASE 3: Eliminar archivos de análisis obsoletos")
    for file in result['analysis_files']:
        print(f"  • Eliminar {file}")
    
    print("\n📝 FASE 4: Actualizar CHANGELOG.md")
    print("  • Limpiar referencias a mejoras V3 que no funcionaron")
    print("  • Agregar nueva sección de depuración extensiva")
    print("  • Consolidar información de v0.0.11")
    
    print("\n✅ RESULTADO ESPERADO:")
    print("  • Carpeta raíz limpia de tests obsoletos")
    print("  • CHANGELOG.md actualizado y preciso")
    print("  • Solo tests oficiales en carpeta tests/")
