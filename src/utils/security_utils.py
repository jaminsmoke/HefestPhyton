"""
Utilidades de Seguridad - Hefest
Funciones para validación y sanitización de entrada
"""

import os
import re
from pathlib import Path
from typing import Union, Optional


class SecurityUtils:
    """Utilidades de seguridad para validación de entrada"""
    
    @staticmethod
    def get_safe_project_path(*path_parts: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """
        Construye un path seguro dentro del proyecto
        Previene path traversal attacks
        """
        # Obtener directorio raíz del proyecto
        current_file = Path(__file__).resolve()
        _ = current_file.parent.parent.parent
        
        # Construir path solicitado
        _ = project_root
        for part in path_parts:
            # Sanitizar cada parte del path
            clean_part = SecurityUtils._sanitize_path_component(part)
            _ = target_path / clean_part
        
        # Resolver path completo
        _ = target_path.resolve()
        
        # Validar que esté dentro del proyecto
        try:
            resolved_path.relative_to(project_root)
        except ValueError:
            from src.utils.security_logger import security_logger
            security_logger.log_path_traversal_attempt(str(resolved_path))
            raise ValueError(f"Path traversal detected: {resolved_path}")
        
        return str(resolved_path)
    
    @staticmethod
    def _sanitize_path_component(component: str) -> str:
        """Sanitiza un componente de path"""
        if not component:
            raise ValueError("Empty path component")
        
        # Rechazar componentes peligrosos
        dangerous_patterns = ['.', '..', '~', '$']
        if component in dangerous_patterns:
            raise ValueError(f"Dangerous path component: {component}")
        
        # Validar caracteres permitidos
        if not re.match(r'^[a-zA-Z0-9_\-\.]+$', component):
            raise ValueError(f"Invalid characters in path component: {component}")
        
        return component
    
    @staticmethod
    def validate_table_name(table_name: str, allowed_tables: set) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valida nombre de tabla contra whitelist"""
        if not table_name:
            raise ValueError("Table name cannot be empty")
        
        if table_name not in allowed_tables:
            raise ValueError(f"Table '{table_name}' not allowed. Allowed: {', '.join(sorted(allowed_tables))}")
        
        return table_name
    
    @staticmethod
    def validate_column_name(column_name: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valida nombre de columna"""
        if not column_name:
            raise ValueError("Column name cannot be empty")
        
        # Solo permitir caracteres alfanuméricos y guiones bajos
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', column_name):
            raise ValueError(f"Invalid column name: {column_name}")
        
        return column_name
    
    @staticmethod
    def sanitize_sql_input(value: Union[str, int, float, None]) -> Union[str, int, float, None]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Sanitiza entrada para SQL (básico)"""
        if value is None:
            return None
        
        if isinstance(value, (int, float)):
            return value
        
        if isinstance(value, str):
            # Remover caracteres peligrosos básicos
            _ = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
            sanitized = str(value)
            
            for char in dangerous_chars:
                if char in sanitized:
                    raise ValueError(f"Dangerous character/sequence detected: {char}")
            
            return sanitized
        
        raise ValueError(f"Unsupported type for SQL input: {type(value)}")
    
    @staticmethod
    def validate_user_input(input_str: str, max_length: int = 255, allow_empty: bool = False) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valida entrada de usuario general"""
        if not allow_empty and not input_str:
            raise ValueError("Input cannot be empty")
        
        if len(input_str) > max_length:
            raise ValueError(f"Input too long. Max {max_length} characters")
        
        # Validar caracteres básicos (expandir según necesidad)
        if not re.match(r'^[a-zA-Z0-9\s\-_\.@]+$', input_str):
            raise ValueError("Input contains invalid characters")
        
        return input_str.strip()


# Funciones de conveniencia
def get_database_path() -> str:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Obtiene path seguro a la base de datos"""
    return SecurityUtils.get_safe_project_path('data', 'hefest.db')


def get_logs_path() -> str:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Obtiene path seguro al directorio de logs"""
    return SecurityUtils.get_safe_project_path('logs')


def get_config_path() -> str:
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Obtiene path seguro al directorio de configuración"""
    return SecurityUtils.get_safe_project_path('config')