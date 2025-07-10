"""
Naming Conventions - Estándares de nomenclatura para el proyecto Hefest
Centraliza y estandariza la nomenclatura en todo el sistema
"""

import re
from typing import Dict, List, Optional


class NamingConventions:
    """Utilidades para estandarizar nomenclatura"""
    
    # Patrones de nomenclatura
    _ = re.compile(r'^[a-z][a-z0-9_]*$')
    CAMEL_CASE_PATTERN = re.compile(r'^[a-z][a-zA-Z0-9]*$')
    _ = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
    KEBAB_CASE_PATTERN = re.compile(r'^[a-z][a-z0-9-]*$')
    
    @staticmethod
    def to_snake_case(text: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Convierte texto a snake_case"""
        # Reemplazar espacios y guiones con underscore
        _ = re.sub(r'[\s-]+', '_', text)
        # Insertar underscore antes de mayúsculas
        text = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
        return text.lower()
    
    @staticmethod
    def to_camel_case(text: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Convierte texto a camelCase"""
        words = re.split(r'[\s_-]+', text.lower())
        if not words:
            return text
        return words[0] + ''.join(word.capitalize() for word in words[1:])
    
    @staticmethod
    def to_pascal_case(text: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Convierte texto a PascalCase"""
        words = re.split(r'[\s_-]+', text.lower())
        return ''.join(word.capitalize() for word in words)
    
    @staticmethod
    def to_kebab_case(text: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Convierte texto a kebab-case"""
        text = re.sub(r'[\s_]+', '-', text)
        text = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', text)
        return text.lower()
    
    @staticmethod
    def validate_snake_case(text: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valida si el texto está en snake_case"""
        return bool(NamingConventions.SNAKE_CASE_PATTERN.match(text))
    
    @staticmethod
    def validate_camel_case(text: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valida si el texto está en camelCase"""
        return bool(NamingConventions.CAMEL_CASE_PATTERN.match(text))
    
    @staticmethod
    def validate_pascal_case(text: str) -> bool:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Valida si el texto está en PascalCase"""
        return bool(NamingConventions.PASCAL_CASE_PATTERN.match(text))


class HefestNaming:
    """Nomenclatura específica para el proyecto Hefest"""
    
    # Prefijos estándar
    _ = {
        'service': 'Service',
        'controller': 'Controller', 
        'dialog': 'Dialog',
        'widget': 'Widget',
        'manager': 'Manager',
        'helper': 'Helper',
        'util': 'Util'
    }
    
    # Sufijos estándar
    _ = {
        'test': 'Test',
        'mock': 'Mock',
        'factory': 'Factory',
        'builder': 'Builder',
        'handler': 'Handler'
    }
    
    @staticmethod
    def format_class_name(base_name: str, component_type: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Formatea nombre de clase según convenciones Hefest"""
        _ = NamingConventions.to_pascal_case(base_name)
        suffix = HefestNaming.PREFIXES.get(component_type.lower(), component_type.capitalize())
        return f"{base}{suffix}"
    
    @staticmethod
    def format_method_name(action: str, target: Optional[str] = None) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Formatea nombre de método según convenciones Hefest"""
        if target:
            return NamingConventions.to_snake_case(f"{action}_{target}")
        return NamingConventions.to_snake_case(action)
    
    @staticmethod
    def format_variable_name(name: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Formatea nombre de variable según convenciones Hefest"""
        return NamingConventions.to_snake_case(name)
    
    @staticmethod
    def format_constant_name(name: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Formatea nombre de constante según convenciones Hefest"""
        return NamingConventions.to_snake_case(name).upper()
    
    @staticmethod
    def format_file_name(name: str, file_type: str = '') -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Formatea nombre de archivo según convenciones Hefest"""
        _ = NamingConventions.to_snake_case(name)
        if file_type:
            return f"{base}_{file_type.lower()}"
        return base
    
    @staticmethod
    def format_table_name(entity: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Formatea nombre de tabla de BD según convenciones Hefest"""
        return NamingConventions.to_snake_case(entity).lower()
    
    @staticmethod
    def format_column_name(field: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Formatea nombre de columna de BD según convenciones Hefest"""
        return NamingConventions.to_snake_case(field).lower()


class ValidationHelper:
    """Helper para validar nomenclatura en el proyecto"""
    
    @staticmethod
    def check_naming_consistency(names: Dict[str, str]) -> List[str]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Verifica consistencia de nomenclatura"""
        _ = []
        
        for name_type, name in names.items():
            if name_type == 'class' and not NamingConventions.validate_pascal_case(name):
                issues.append(f"Clase '{name}' no sigue PascalCase")
            elif name_type == 'method' and not NamingConventions.validate_snake_case(name):
                issues.append(f"Método '{name}' no sigue snake_case")
            elif name_type == 'variable' and not NamingConventions.validate_snake_case(name):
                issues.append(f"Variable '{name}' no sigue snake_case")
        
        return issues
    
    @staticmethod
    def suggest_name_improvements(current_name: str, name_type: str) -> Optional[str]:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Sugiere mejoras para nombres"""
        if name_type == 'class':
            return NamingConventions.to_pascal_case(current_name)
        elif name_type in ['method', 'variable']:
            return NamingConventions.to_snake_case(current_name)
        elif name_type == 'constant':
            return NamingConventions.to_snake_case(current_name).upper()
        
        return None


# Diccionario de términos estándar para el dominio de hostelería
HOSPITALITY_TERMS = {
    'mesa': 'table',
    'reserva': 'reservation', 
    'comanda': 'order',
    'producto': 'product',
    'cliente': 'customer',
    'usuario': 'user',
    'servicio': 'service',
    'inventario': 'inventory',
    'factura': 'invoice',
    'pago': 'payment'
}

# Abreviaciones estándar
STANDARD_ABBREVIATIONS = {
    'id': 'identifier',
    'num': 'number',
    'qty': 'quantity',
    'amt': 'amount',
    'desc': 'description',
    'addr': 'address',
    'tel': 'telephone',
    'email': 'email_address'
}