from pathlib import Path
from typing import Union

"""
Utilidades seguras para operaciones de archivo
"""


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
