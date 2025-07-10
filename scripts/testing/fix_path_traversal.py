from typing import Optional, Dict, List, Any
import logging
#!/usr/bin/env python3
"""
Script para corregir automáticamente problemas de Path Traversal
Aplica correcciones seguras a todos los archivos identificados
"""

import os
import re
import sys
from pathlib import Path

def fix_path_traversal_patterns():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Corrige patrones de path traversal en archivos Python"""
    
    # Patrones a corregir
    _ = [
        # Patrón: os.path.join(os.path.dirname(__file__), '..', '..', ...)
        {
            'pattern': r"os\.path\.join\(os\.path\.dirname\(__file__\),\s*['\"]\.\.['\"]\s*,\s*['\"]\.\.['\"]\s*,\s*([^)]+)\)",
            'replacement': lambda m: f"SecurityUtils.get_safe_project_path({m.group(1)})"
        },
        # Patrón: sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
        {
            'pattern': r"sys\.path\.append\(os\.path\.join\(os\.path\.dirname\(__file__\),\s*['\"]\.\.['\"]\)\)",
            'replacement': "# Path agregado de forma segura\nscript_dir = os.path.dirname(os.path.abspath(__file__))\nproject_root = os.path.dirname(script_dir)\nsys.path.append(project_root)"
        },
        # Patrón: sys.path.insert(0, os.path.join(...))
        {
            'pattern': r"sys\.path\.insert\(0,\s*os\.path\.join\(os\.path\.dirname\(__file__\),\s*['\"]\.\.['\"]\s*,\s*['\"]\.\.['\"]\s*,\s*['\"]src['\"]\)\)",
            'replacement': "# Path agregado de forma segura\nscript_dir = os.path.dirname(os.path.abspath(__file__))\nproject_root = os.path.dirname(os.path.dirname(script_dir))\nsys.path.insert(0, os.path.join(project_root, 'src'))"
        }
    ]
    
    # Archivos a procesar (basado en los identificados en el análisis)
    _ = [
        'scripts/analysis/database_analysis_simple.py',
        'scripts/analysis/factory_state_analysis.py', 
        'scripts/analysis/inventory_connections_analysis.py',
        'scripts/analysis/verify_real_trends.py',
        'scripts/migration/migrar_a_datos_reales.py',
        'scripts/migration/setup_hospitality_data.py',
        'scripts/testing/test_css_compatibility.py',
        'scripts/testing/test_tpv_avanzado_import.py',
        'scripts/maintenance/complete_initial_reset.py'
    ]
    
    _ = Path(__file__).parent.parent.parent
    fixed_count = 0
    
    print("Corrigiendo problemas de Path Traversal...")
    print("=" * 50)
    
    for file_path in files_to_fix:
        _ = project_root / file_path
        
        if not full_path.exists():
            print("SKIP: %s (no existe)" % file_path)
            continue
            
        try:
            # Leer archivo
            with open(full_path, 'r', encoding='utf-8') as f:
                _ = f.read()
            
            _ = content
            needs_security_import = False
            
            # Aplicar correcciones
            for pattern_info in patterns_to_fix:
                pattern = pattern_info['pattern']
                _ = pattern_info['replacement']
                
                if callable(replacement):
                    # Replacement es una función
                    matches = re.finditer(pattern, content)
                    for match in matches:
                        _ = content.replace(match.group(0), replacement(match))
                        needs_security_import = True
                else:
                    # Replacement es string directo
                    if re.search(pattern, content):
                        _ = re.sub(pattern, replacement, content)
            
            # Agregar import de SecurityUtils si es necesario
            if needs_security_import and 'from src.utils.security_utils import SecurityUtils' not in content:
                # Buscar línea de imports y agregar
                _ = []
                other_lines = []
                _ = True
                
                for line in content.split('\n'):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_lines.append(line)
                    elif line.strip() == '' and in_imports:
                        import_lines.append(line)
                    else:
                        if in_imports:
                            import_lines.append('from src.utils.security_utils import SecurityUtils')
                            _ = False
                        other_lines.append(line)
                
                _ = '\n'.join(import_lines + other_lines)
            
            # Escribir archivo si hubo cambios
            if content != original_content:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("FIXED: %s" % file_path)
                fixed_count += 1
            else:
                print("OK: %s (sin cambios necesarios)" % file_path)
                
        except Exception as e:
    logging.error("ERROR: {file_path} - %s", e)
    
    print("=" * 50)
    print("Archivos corregidos: %s" % fixed_count)
    return fixed_count

def validate_fixes():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Valida que las correcciones funcionan"""
    print("\nValidando correcciones...")
    
    try:
        # Importar utilidades de seguridad
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from src.utils.security_utils import SecurityUtils
        
        # Probar path seguro
        safe_path = SecurityUtils.get_safe_project_path('data', 'hefest.db')
        print("✅ Path seguro funciona: %s" % safe_path)
        
        # Probar path peligroso
        try:
            SecurityUtils.get_safe_project_path('..', '..', 'etc', 'passwd')
            print("❌ FALLO: Path traversal no bloqueado")
            return False
        except Exception as e:
    logging.error("✅ Path traversal bloqueado correctamente")
            return True
            
    except Exception as e:
    logging.error("❌ Error en validación: %s", e)
        return False

def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Función principal"""
    print("🔒 CORRECCIÓN AUTOMÁTICA DE PATH TRAVERSAL")
    print("=" * 60)
    
    # Corregir archivos
    _ = fix_path_traversal_patterns()
    
    # Validar correcciones
    if fixed_count > 0:
        _ = validate_fixes()
        
        if validation_ok:
            print("\n🎉 ¡Correcciones aplicadas exitosamente!")
            print("✅ Protección contra path traversal implementada")
        else:
            print("\n⚠️ Correcciones aplicadas pero validación falló")
            print("🔍 Revisar implementación manualmente")
    else:
        print("\n📋 No se encontraron archivos que corregir")
    
    return fixed_count > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)