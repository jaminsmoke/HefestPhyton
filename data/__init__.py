"""
Módulo de Gestión de Datos - Proyecto Hefest
============================================

Este módulo contiene todos los componentes relacionados con la gestión de datos
y acceso a la base de datos de la aplicación Hefest.

Componentes disponibles:
- DatabaseManager: Gestor principal de la base de datos SQLite
- Modelos de datos y esquemas de la base de datos
- Utilidades para migración y mantenimiento de datos

El módulo proporciona una interfaz unificada para todas las operaciones
de persistencia de datos en el sistema Hefest.

Autor: Proyecto Hefest
Versión: 0.0.12
"""

# Archivo para hacer que el directorio sea un paquete Python
from .db_manager import DatabaseManager

__all__ = ['DatabaseManager']
