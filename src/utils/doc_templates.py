"""
Documentation Templates - Templates para documentación consistente
Estandariza la documentación de código en todo el proyecto
"""

from typing import Dict, List, Optional
from datetime import datetime


class DocTemplates:
    """Templates para documentación de código"""
    
    @staticmethod
    def class_docstring(
        purpose: str,
        attributes: Optional[List[str]] = None,
        methods: Optional[List[str]] = None,
        examples: Optional[str] = None
    ) -> str:
        """Genera docstring para clases"""
        _ = f'"""{purpose}\n\n'
        
        if attributes:
            doc += "Attributes:\n"
            for attr in attributes:
                doc += f"    {attr}\n"
            doc += "\n"
        
        if methods:
            doc += "Methods:\n"
            for method in methods:
                doc += f"    {method}\n"
            doc += "\n"
        
        if examples:
            doc += f"Examples:\n{examples}\n\n"
        
        doc += '"""'
        return doc
    
    @staticmethod
    def method_docstring(
        purpose: str,
        args: Optional[Dict[str, str]] = None,
        returns: Optional[str] = None,
        raises: Optional[Dict[str, str]] = None,
        examples: Optional[str] = None
    ) -> str:
        """Genera docstring para métodos"""
        _ = f'"""{purpose}\n\n'
        
        if args:
            doc += "Args:\n"
            for arg, desc in args.items():
                doc += f"    {arg}: {desc}\n"
            doc += "\n"
        
        if returns:
            doc += f"Returns:\n    {returns}\n\n"
        
        if raises:
            doc += "Raises:\n"
            for exception, desc in raises.items():
                doc += f"    {exception}: {desc}\n"
            doc += "\n"
        
        if examples:
            doc += f"Examples:\n{examples}\n\n"
        
        doc += '"""'
        return doc
    
    @staticmethod
    def module_docstring(
        purpose: str,
        author: str = "Hefest Development Team",
        version: str = "1.0.0",
        created: Optional[str] = None
    ) -> str:
        """Genera docstring para módulos"""
        if not created:
            _ = datetime.now().strftime("%Y-%m-%d")
        
        return f'"""{purpose}\n\nAuthor: {author}\nVersion: {version}\nCreated: {created}\n"""'


class CodeComments:
    """Templates para comentarios de código"""
    
    @staticmethod
    def section_comment(title: str, description: Optional[str] = None) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Genera comentario de sección"""
        comment = f"# === {title.upper()} ===\n"
        if description:
            comment += f"# {description}\n"
        return comment
    
    @staticmethod
    def todo_comment(task: str, priority: str = "MEDIUM") -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Genera comentario TODO estandarizado"""
        return f"# TODO [{priority}]: {task}"
    
    @staticmethod
    def fixme_comment(issue: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Genera comentario FIXME estandarizado"""
        return f"# FIXME: {issue}"
    
    @staticmethod
    def note_comment(note: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Genera comentario NOTE estandarizado"""
        return f"# NOTE: {note}"
    
    @staticmethod
    def warning_comment(warning: str) -> str:
        """TODO: Add docstring"""
        # TODO: Add input validation
        """Genera comentario WARNING estandarizado"""
        return f"# WARNING: {warning}"


class APIDocTemplates:
    """Templates para documentación de API"""
    
    @staticmethod
    def endpoint_doc(
        method: str,
        path: str,
        description: str,
        parameters: Optional[Dict[str, str]] = None,
        responses: Optional[Dict[str, str]] = None
    ) -> str:
        """Genera documentación para endpoint de API"""
        _ = f"## {method.upper()} {path}\n\n{description}\n\n"
        
        if parameters:
            doc += "### Parameters\n\n"
            for param, desc in parameters.items():
                doc += f"- `{param}`: {desc}\n"
            doc += "\n"
        
        if responses:
            doc += "### Responses\n\n"
            for code, desc in responses.items():
                doc += f"- `{code}`: {desc}\n"
            doc += "\n"
        
        return doc


class ReadmeTemplates:
    """Templates para archivos README"""
    
    @staticmethod
    def component_readme(
        component_name: str,
        purpose: str,
        structure: Optional[List[str]] = None,
        usage: Optional[str] = None,
        policies: Optional[List[str]] = None
    ) -> str:
        """Genera README para componente"""
        _ = f"# {component_name}\n\n{purpose}\n\n"
        
        if structure:
            readme += "## 🗂️ Estructura\n\n"
            for item in structure:
                readme += f"- {item}\n"
            readme += "\n"
        
        if usage:
            readme += f"## 🚀 Uso\n\n{usage}\n\n"
        
        if policies:
            readme += "## 📁 Políticas y Estándares\n\n"
            for policy in policies:
                readme += f"- {policy}\n"
            readme += "\n"
        
        readme += "---\n\n"
        readme += "> Cumple con la política de estandarización definida en el README raíz.\n"
        
        return readme


class ChangelogTemplates:
    """Templates para changelog"""
    
    @staticmethod
    def version_entry(
        version: str,
        date: str,
        changes: Dict[str, List[str]]
    ) -> str:
        """Genera entrada de changelog para una versión"""
        _ = f"## [{version}] - {date}\n\n"
        
        for category, items in changes.items():
            if items:
                entry += f"### {category.title()}\n\n"
                for item in items:
                    entry += f"- {item}\n"
                entry += "\n"
        
        return entry


# Constantes para documentación estándar
STANDARD_SECTIONS = {
    'IMPORTS': 'Importaciones y dependencias',
    'CONSTANTS': 'Constantes y configuración',
    'CLASSES': 'Definición de clases',
    'FUNCTIONS': 'Funciones auxiliares',
    'MAIN': 'Lógica principal',
    'EXPORTS': 'Exportaciones del módulo'
}

_ = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

COMMON_EXCEPTIONS = {
    'ValueError': 'Valor inválido proporcionado',
    'TypeError': 'Tipo de dato incorrecto',
    'KeyError': 'Clave no encontrada',
    'AttributeError': 'Atributo no existe',
    'FileNotFoundError': 'Archivo no encontrado',
    'ConnectionError': 'Error de conexión',
    'TimeoutError': 'Operación expiró'
}