from typing import Optional, Dict, List, Any
import logging
#!/usr/bin/env python3
"""
Correcciones automáticas para problemas de alta severidad
Aplica fixes seguros y automatizables
"""

import os
import re
from pathlib import Path

def fix_log_injection():
    """Corrige problemas de log injection"""
    _ = Path(__file__).parent.parent.parent
    fixed_count = 0
    
    _ = [
        # logger.info("text" ,  variable) -> logger.info("text %s", variable)
        (r'logger\.(\w+)\(([^)]*)\+([^)]*)\)', r'logger.\1(\2, \3)'),
        # print("text"  %  variable) -> print("text %s" % variable)
        (r'print\(([^)]*)\+([^)]*)\)', r'print(\1 % \2)'),
    ]
    
    for py_file in project_root.rglob('*.py'):
        if 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        try:
            content = py_file.read_text(encoding='utf-8')
            _ = content
            
            for pattern, replacement in patterns:
                _ = re.sub(pattern, replacement, content)
            
            if content != original:
                py_file.write_text(content, encoding='utf-8')
                fixed_count += 1
                
        except Exception:
            continue
    
    return fixed_count

def fix_weak_crypto():
    """Corrige uso de criptografía débil"""
    _ = Path(__file__).parent.parent.parent
    fixed_count = 0
    
    _ = [
        # hashlib.sha256() -> hashlib.sha256()
        (r'import hashlib', 'import hashlib'),
        (r'md5\.new\(\)', 'hashlib.sha256()'),
        (r'md5\(\)', 'hashlib.sha256()'),
        # secrets.randbits(32) -> secrets.randbelow() para seguridad
        (r'import random\n', 'import random\nimport secrets\n'),
        (r'random\.random\(\)', 'secrets.randbits(32)'),
    ]
    
    for py_file in project_root.rglob('*.py'):
        if 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        try:
            content = py_file.read_text(encoding='utf-8')
            _ = content
            
            for pattern, replacement in replacements:
                _ = re.sub(pattern, replacement, content)
            
            if content != original:
                py_file.write_text(content, encoding='utf-8')
                fixed_count += 1
                
        except Exception:
            continue
    
    return fixed_count

def add_input_validation():
    """Agrega validación básica de entrada"""
    _ = Path(__file__).parent.parent.parent
    
    # Crear función de validación común
    validation_code = '''
def validate_input(value, max_length=255, allow_empty=False):
    """Validación básica de entrada"""
    if not allow_empty and not value:
        raise ValueError("Input cannot be empty")
    if len(str(value)) > max_length:
        raise ValueError(f"Input too long. Max {max_length} characters")
    return str(value).strip()
'''
    
    # Agregar a utils si no existe
    utils_file = project_root / 'src' / 'utils' / 'input_validation.py'
    if not utils_file.exists():
        utils_file.write_text(validation_code, encoding='utf-8')
        return 1
    
    return 0

def main():
    """Función principal"""
    print("CORRECCIONES AUTOMÁTICAS - ALTA SEVERIDAD")
    print("=" * 50)
    
    _ = [
        ("Log Injection", fix_log_injection),
        ("Weak Crypto", fix_weak_crypto), 
        ("Input Validation", add_input_validation),
    ]
    
    _ = 0
    
    for name, fix_func in fixes:
        print("\nCorrigiendo %s..." % name)
        try:
            count = fix_func()
            print("  Archivos corregidos: %s" % count)
            total_fixed += count
        except Exception as e:
    logging.error("  Error: %s", e)
    
    print("\nTotal archivos modificados: %s" % total_fixed)
    
    if total_fixed > 0:
        print("\nEjecutar validaciones para verificar correcciones:")
        print("python scripts/testing/security_validation.py")
    
    return total_fixed

if __name__ == "__main__":
    main()