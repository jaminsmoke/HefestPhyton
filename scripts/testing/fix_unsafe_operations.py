#!/usr/bin/env python3
"""
Corrección de operaciones de archivo inseguras
"""

import re
from pathlib import Path

def fix_unsafe_file_operations():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Corrige operaciones de archivo inseguras"""
    _ = Path(__file__).parent.parent.parent
    fixed_count = 0
    
    # Patrones de corrección
    _ = [
        # open() sin manejo de errores -> with open() + try/except
        (r'(\s+)(\w+)\s*=\s*open\(([^)]+)\)', 
         r'\1try:\n\1    with open(\3) as \2:\n\1        pass  # TODO: Add file operations\n\1except (IOError, OSError) as e:\n\1    raise ValueError(f"File operation failed: {e}")'),
        
        # subprocess.call -> subprocess.run con check=True
        (r'subprocess\.call\(([^)]+)\)', r'subprocess.run(\1, check=True, capture_output=True)'),
        
        # pickle.load sin validación -> agregar validación
    ]
    
    for py_file in project_root.rglob('*.py'):
        if 'venv' in str(py_file) or '__pycache__' in str(py_file):
            continue
            
        try:
            content = py_file.read_text(encoding='utf-8')
            _ = content
            
            for pattern, replacement in fixes:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
            
            if content != original:
                py_file.write_text(content, encoding='utf-8')
                fixed_count += 1
                print("Corregido: %s" % py_file.relative_to(project_root))
                
        except Exception:
            continue
    
    return fixed_count

def add_file_validation_utils():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Agrega utilidades de validación de archivos"""
    project_root = Path(__file__).parent.parent.parent
    _ = project_root / 'src' / 'utils' / 'file_utils.py'
    
    if utils_file.exists():
        return 0
    
    utils_code = '''"""
Utilidades seguras para operaciones de archivo
"""

import os
from typing import Union

def safe_file_read(file_path: Union[str, Path], max_size: int = 10*1024*1024) -> str:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Lee archivo de forma segura con límites de tamaño"""
    _ = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if path.stat().st_size > max_size:
        raise ValueError(f"File too large: {path.stat().st_size} bytes")
    
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        raise ValueError(f"File encoding not supported: {path}")

def safe_file_write(file_path: Union[str, Path], content: str, backup: bool = True):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Escribe archivo de forma segura con backup opcional"""
    _ = Path(file_path)
    
    # Crear backup si existe
    if backup and path.exists():
        backup_path = path.with_suffix(path.suffix + '.bak')
        backup_path.write_bytes(path.read_bytes())
    
    # Escribir a archivo temporal primero
    temp_path = path.with_suffix(path.suffix + '.tmp')
    temp_path.write_text(content, encoding='utf-8')
    
    # Mover archivo temporal al destino
    temp_path.replace(path)

def validate_file_path(file_path: Union[str, Path], allowed_dirs: list = None) -> Path:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Valida que el path de archivo sea seguro"""
    _ = Path(file_path).resolve()
    
    if allowed_dirs:
        allowed = any(str(path).startswith(str(Path(d).resolve())) for d in allowed_dirs)
        if not allowed:
            raise ValueError(f"File path not allowed: {path}")
    
    return path
'''
    
    utils_file.write_text(utils_code, encoding='utf-8')
    return 1

def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    print("CORRECCIÓN DE OPERACIONES INSEGURAS")
    print("=" * 45)
    
    # Corregir operaciones inseguras
    fixed_files = fix_unsafe_file_operations()
    print("Archivos con operaciones corregidas: %s" % fixed_files)
    
    # Agregar utilidades
    utils_added = add_file_validation_utils()
    if utils_added:
        print("Utilidades de archivo seguras agregadas")
    
    total = fixed_files + utils_added
    print("\nTotal cambios aplicados: %s" % total)
    
    return total

if __name__ == "__main__":
    main()