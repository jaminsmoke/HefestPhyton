#!/usr/bin/env python3
"""
Script para arreglar problemas críticos en hefest_application.py
"""

import os
import sys

def fix_hefest_application():
    """Arregla los problemas principales en hefest_application.py"""
    
    file_path = os.path.join(
        os.path.dirname(__file__), '..', '..', 
        'src', 'hefest_application.py'
    )
    
    if not os.path.exists(file_path):
        print(f"ERROR: No se encontró {file_path}")
        return False
    
    # Leer archivo actual
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Correcciones básicas
    fixes = [
        # Arreglar imports
        ('from PyQt6.QtWidgets import QApplication, QDialog, QInputDialog, QLineEdit, QMessageBox',
         'from PyQt6.QtWidgets import (QApplication, QDialog, QInputDialog, \n                                QLineEdit, QMessageBox)'),
        
        # Simplificar el filtro CSS problemático
        ('        # Filtro para warnings de CSS backdrop-filter (stdout y stderr)',
         '        # Filtro CSS simplificado'),
        
        # Remover el filtro CSS complejo que causa problemas
        ('        import io\n        import sys as _sys\n        from typing import List\n\n        class CSSWarningFilter(io.StringIO):',
         '        # Filtro CSS deshabilitado por problemas de compatibilidad\n        if False:  # Deshabilitado\n            class CSSWarningFilter:'),
    ]
    
    # Aplicar correcciones
    for old, new in fixes:
        if old in content:
            content = content.replace(old, new)
            print(f"✓ Aplicada corrección: {old[:50]}...")
    
    # Escribir archivo corregido
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Archivo corregido: {file_path}")
    return True

if __name__ == "__main__":
    if fix_hefest_application():
        print("✓ Correcciones aplicadas exitosamente")
    else:
        print("✗ Error aplicando correcciones")
        sys.exit(1)