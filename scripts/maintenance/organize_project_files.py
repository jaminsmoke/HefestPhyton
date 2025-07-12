#!/usr/bin/env python3
"""
Script para organizar archivos del proyecto según las políticas establecidas
"""

import os
import shutil
import sys
from pathlib import Path

def organize_project_files():
    """Organiza los archivos del proyecto según las políticas"""
    
    project_root = Path(__file__).parent.parent.parent
    
    # Archivos que deben moverse
    files_to_move = {
        # Archivos de análisis -> scripts/analysis/
        'analyze_quality.py': 'scripts/analysis/',
        'analyze_security.py': 'scripts/analysis/',
        'detect_duplications.py': 'scripts/analysis/',
        'quality_analysis.py': 'scripts/analysis/',  # Ya existe, mover como backup
        
        # Archivos de refactoring -> scripts/maintenance/
        'cleanup_modern_duplicates.py': 'scripts/maintenance/',
        'refactor_duplicates.py': 'scripts/maintenance/',
        'refactor_tpv.py': 'scripts/maintenance/',
        
        # Archivos temporales -> scripts/testing/
        'temp_analyze_final.py': 'scripts/testing/',
        'temp_copilot_reset.py': 'scripts/testing/',
        'temp_db_explorer.py': 'scripts/testing/',
        'temp_fix_long_lines.py': 'scripts/testing/',
        'temp_test_file.py': 'scripts/testing/',
        'temp_test_linting.py': 'scripts/testing/',
        'test_pyqt6_simple.py': 'scripts/testing/',
        
        # Archivos de debug -> scripts/analysis/
        'debug_categorias.py': 'scripts/analysis/',
        
        # Reportes -> docs/development/
        'reporte_consolidado.py': 'scripts/analysis/',
        'reporte_progreso_seguridad.md': 'docs/development/',
        'reporte_refactoring_inteligente.json': 'docs/development/',
        
        # Resultados de herramientas -> development-config/
        'bandit-results.json': 'development-config/',
        'flake8-results.json': 'development-config/',
        'pylint-results.json': 'development-config/',
        'security_analysis_fresh.json': 'development-config/',
        'vulture-report.txt': 'development-config/',
        
        # Archivos de configuración de PyRight -> development-config/
        'pyright_after_inventario_service.json': 'development-config/',
        'pyright_current_analysis.json': 'development-config/',
        'pyright_final_analysis.json': 'development-config/',
        
        # Scripts de PowerShell -> scripts/maintenance/
        'run_codacy_local.ps1': 'scripts/maintenance/',
        
        # Archivos de prueba -> scripts/testing/
        'test_spanish.txt': 'scripts/testing/',
    }
    
    # Archivos que deben eliminarse (temporales o duplicados)
    files_to_remove = [
        '.coverage',  # Se regenera automáticamente
    ]
    
    print("Iniciando organización de archivos del proyecto...")
    
    moved_count = 0
    removed_count = 0
    
    # Mover archivos
    for filename, target_dir in files_to_move.items():
        source_path = project_root / filename
        target_path = project_root / target_dir / filename
        
        if source_path.exists():
            # Crear directorio destino si no existe
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Si el archivo ya existe en destino, crear backup
            if target_path.exists():
                backup_path = target_path.with_suffix(target_path.suffix + '.backup')
                print(f"  Creando backup: {target_path} -> {backup_path}")
                shutil.move(str(target_path), str(backup_path))
            
            print(f"  Moviendo: {filename} -> {target_dir}")
            shutil.move(str(source_path), str(target_path))
            moved_count += 1
        else:
            print(f"  No encontrado: {filename}")
    
    # Eliminar archivos temporales
    for filename in files_to_remove:
        file_path = project_root / filename
        if file_path.exists():
            print(f"  Eliminando: {filename}")
            file_path.unlink()
            removed_count += 1
    
    print(f"\nOrganización completada:")
    print(f"  - Archivos movidos: {moved_count}")
    print(f"  - Archivos eliminados: {removed_count}")
    
    # Verificar archivos restantes en raíz
    remaining_files = []
    for item in project_root.iterdir():
        if item.is_file() and not item.name.startswith('.') and item.name not in [
            'main.py', 'README.md', 'requirements.txt', 'pyproject.toml', 
            'LICENSE', 'MANIFEST.in', 'pyrightconfig.json', 'HefestWorkspace.code-workspace'
        ]:
            remaining_files.append(item.name)
    
    if remaining_files:
        print(f"\nArchivos restantes en raíz que podrían necesitar organización:")
        for filename in remaining_files:
            print(f"  - {filename}")
    else:
        print(f"\n✅ Raíz del proyecto limpia - solo archivos esenciales")

if __name__ == "__main__":
    try:
        organize_project_files()
        print("\n🎉 Organización de archivos completada exitosamente")
    except Exception as e:
        print(f"\n❌ Error durante la organización: {e}")
        sys.exit(1)