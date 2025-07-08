"""
HEFEST - ANÁLISIS Y PLAN DE LIMPIEZA DE ARCHIVOS OBSOLETOS UI
Análisis exhaustivo de archivos obsoletos tras el rediseño V3 ultra-moderno
"""

from pathlib import Path
import os

def analyze_ui_structure():
    """Analizar estructura actual de UI y identificar archivos obsoletos"""
    
    print("🔍 ANÁLISIS DE ARCHIVOS OBSOLETOS EN UI")
    print("="*60)
    
    # === ARCHIVOS ACTIVOS Y NECESARIOS ===
    ARCHIVOS_ACTIVOS = {
        # Sistema visual V3 (NUEVO)
        "src/ui/components/ultra_modern_system_v3.py": "✅ SISTEMA V3 - MANTENER",
        "src/ui/modules/dashboard_admin_v3/ultra_modern_admin_dashboard.py": "✅ DASHBOARD V3 - MANTENER",
        
        # Componentes base necesarios
        "src/ui/components/sidebar.py": "✅ SIDEBAR - REVISAR/ACTUALIZAR",
        "src/ui/components/user_selector.py": "✅ USER SELECTOR - MANTENER",
        
        # Ventanas principales
        "src/ui/windows/main_window.py": "✅ VENTANA PRINCIPAL - MANTENER",
        "src/ui/windows/login_dialog.py": "✅ LOGIN - MANTENER",
        
        # Diálogos
        "src/ui/dialogs/user_dialog.py": "✅ USER DIALOG - MANTENER",
        
        # Módulos funcionales (otros)
        "src/ui/modules/base_module.py": "✅ BASE MODULE - MANTENER",
        "src/ui/modules/tpv_module.py": "⚠️  TPV - REVISAR PARA MIGRAR A V3",
        "src/ui/modules/advanced_tpv_module.py": "⚠️  TPV AVANZADO - REVISAR",
        "src/ui/modules/hospederia_module.py": "⚠️  HOSPEDERÍA - REVISAR",
        "src/ui/modules/inventario_module.py": "⚠️  INVENTARIO - REVISAR", 
        "src/ui/modules/audit_module.py": "⚠️  AUDITORÍA - REVISAR",
        "src/ui/modules/user_management_module.py": "⚠️  USER MGMT - REVISAR",
        "src/ui/modules/configuracion_module.py": "⚠️  CONFIG - REVISAR",
        "src/ui/modules/reportes_module.py": "⚠️  REPORTES - REVISAR",
        
        # Configuración dashboard
        "src/ui/modules/dashboard_admin_v3/dashboard_config.py": "✅ CONFIG - MANTENER",
        "src/ui/modules/dashboard_admin_v3/admin_data_service.py": "✅ DATA SERVICE - MANTENER",
    }
    
    # === ARCHIVOS OBSOLETOS IDENTIFICADOS ===
    ARCHIVOS_OBSOLETOS = {
        # Sistema visual V2 (OBSOLETO)
        "src/ui/visual_system_v2.py": "❌ VISUAL V2 - ELIMINAR (reemplazado por V3)",
        "src/ui/modern_components.py": "❌ COMPONENTS ANTIGUOS - ELIMINAR",
        
        # Dashboard V3 - archivos de desarrollo/backup (OBSOLETOS)
        "src/ui/modules/dashboard_admin_v3/admin_metrics_widgets.py": "❌ METRICS OLD - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/admin_metrics_widgets_backup_20250613.py": "❌ BACKUP - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/admin_metrics_widgets_clean.py": "❌ CLEAN VERSION - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/advanced_metric_card.py": "❌ OLD METRIC CARD - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/advanced_metric_card_backup_20250613.py": "❌ BACKUP - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/advanced_metric_card_clean.py": "❌ CLEAN - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/advanced_metric_card_compatible.py": "❌ COMPATIBLE - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/advanced_metric_card_minimal.py": "❌ MINIMAL - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/advanced_metric_card_modern.py": "❌ MODERN - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/advanced_metric_card_native.py": "❌ NATIVE - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/advanced_metric_card_new.py": "❌ NEW - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/advanced_metric_card_robust.py": "❌ ROBUST - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/dashboard_admin_controller.py": "❌ OLD CONTROLLER - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/admin_charts_widgets.py": "❌ OLD CHARTS - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/ultra_modern_dashboard.py": "❌ DUPLICATE - ELIMINAR",
        "src/ui/modules/dashboard_admin_v3/ultra_modern_metric_card.py": "❌ DUPLICATE - ELIMINAR", 
        "src/ui/modules/dashboard_admin_v3/ultra_simple_metric_card.py": "❌ SIMPLE - ELIMINAR",
    }
    
    print("\n📁 ARCHIVOS ACTIVOS/NECESARIOS:")
    for archivo, estado in ARCHIVOS_ACTIVOS.items():
        print(f"  {estado} | {archivo}")
    
    print(f"\n🗑️  ARCHIVOS OBSOLETOS IDENTIFICADOS ({len(ARCHIVOS_OBSOLETOS)}):")
    for archivo, razon in ARCHIVOS_OBSOLETOS.items():
        print(f"  {razon} | {archivo}")
    
    return ARCHIVOS_ACTIVOS, ARCHIVOS_OBSOLETOS

def create_cleanup_plan():
    """Crear plan detallado de limpieza"""
    
    print("\n" + "="*60)
    print("📋 PLAN DE LIMPIEZA ESTRUCTURADO")
    print("="*60)
    
    PLAN_LIMPIEZA = {
        "fase_1_backup_adicional": {
            "descripcion": "Crear backup adicional antes de eliminar archivos",
            "acciones": [
                "Crear backup específico de archivos a eliminar",
                "Verificar que el sistema V3 funciona sin estos archivos",
                "Confirmar que no hay dependencias ocultas"
            ]
        },
        
        "fase_2_eliminacion_dashboard_v3": {
            "descripcion": "Limpiar archivos obsoletos en dashboard_admin_v3/",
            "archivos_eliminar": [
                "admin_metrics_widgets.py",
                "admin_metrics_widgets_backup_20250613.py", 
                "admin_metrics_widgets_clean.py",
                "advanced_metric_card.py",
                "advanced_metric_card_backup_20250613.py",
                "advanced_metric_card_clean.py",
                "advanced_metric_card_compatible.py",
                "advanced_metric_card_minimal.py",
                "advanced_metric_card_modern.py",
                "advanced_metric_card_native.py",
                "advanced_metric_card_new.py",
                "advanced_metric_card_robust.py",
                "dashboard_admin_controller.py",
                "admin_charts_widgets.py",
                "ultra_modern_dashboard.py",
                "ultra_modern_metric_card.py",
                "ultra_simple_metric_card.py"
            ]
        },
        
        "fase_3_eliminacion_sistema_v2": {
            "descripcion": "Eliminar sistema visual V2 obsoleto",
            "archivos_eliminar": [
                "visual_system_v2.py",
                "modern_components.py"
            ]
        },
        
        "fase_4_limpieza_cache": {
            "descripcion": "Limpiar archivos de cache Python",
            "acciones": [
                "Eliminar carpetas __pycache__",
                "Eliminar archivos .pyc",
                "Regenerar imports limpios"
            ]
        },
        
        "fase_5_actualizacion_imports": {
            "descripcion": "Actualizar imports en archivos que usen código obsoleto",
            "acciones": [
                "Buscar referencias a archivos eliminados",
                "Actualizar imports a usar solo sistema V3",
                "Verificar que no hay imports rotos"
            ]
        },
        
        "fase_6_validacion": {
            "descripcion": "Validar que todo funciona después de la limpieza",
            "acciones": [
                "Ejecutar aplicación principal",
                "Verificar dashboard V3 funciona",
                "Ejecutar tests de validación",
                "Confirmar que no hay errores de importación"
            ]
        }
    }
    
    for fase, detalles in PLAN_LIMPIEZA.items():
        print(f"\n🔧 {fase.upper()}:")
        print(f"   {detalles['descripcion']}")
        
        if "archivos_eliminar" in detalles:
            print(f"   📁 Archivos a eliminar ({len(detalles['archivos_eliminar'])}):")
            for archivo in detalles["archivos_eliminar"]:
                print(f"      • {archivo}")
        
        if "acciones" in detalles:
            print("   📋 Acciones:")
            for accion in detalles["acciones"]:
                print(f"      • {accion}")
    
    return PLAN_LIMPIEZA

def main():
    """Función principal de análisis"""
    print("🧹 HEFEST - LIMPIEZA EXHAUSTIVA DE ARCHIVOS OBSOLETOS")
    print("="*60)
    print("Análisis post-rediseño V3 ultra-moderno")
    print()
    
    # Análisis
    archivos_activos, archivos_obsoletos = analyze_ui_structure()
    
    # Plan de limpieza
    plan = create_cleanup_plan()
    
    print(f"\n📊 RESUMEN:")
    print(f"   • Archivos activos/necesarios: {len(archivos_activos)}")
    print(f"   • Archivos obsoletos identificados: {len(archivos_obsoletos)}")
    print(f"   • Fases de limpieza planificadas: {len(plan)}")
    
    print(f"\n💾 ESTIMACIÓN DE ESPACIO A LIBERAR:")
    print(f"   • ~{len(archivos_obsoletos)} archivos Python")
    print(f"   • Múltiples carpetas __pycache__") 
    print(f"   • Código duplicado y experimental")
    
    print(f"\n🎯 BENEFICIOS DE LA LIMPIEZA:")
    print(f"   • Codebase más limpio y mantenible")
    print(f"   • Imports más rápidos y claros")
    print(f"   • Menos confusión para futuros desarrolladores")
    print(f"   • Arquitectura V3 como única fuente de verdad")
    
    print(f"\n⚠️  PRECAUCIONES:")
    print(f"   • Crear backup antes de eliminar")
    print(f"   • Verificar que no hay dependencias ocultas")
    print(f"   • Probar aplicación después de cada fase")

if __name__ == "__main__":
    main()
