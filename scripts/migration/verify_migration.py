#!/usr/bin/env python3
"""
Script para verificar la migración de PyQt6 a PySide6

Este script analiza el código para detectar referencias restantes a PyQt6
después de la migración a PySide6, ayudando a identificar áreas que
requieren atención manual.

Uso:
    python verify_migration.py [directorio]

Ejemplo:
    python verify_migration.py ../src
"""

import os
import sys
import re
import argparse
from typing import List, Dict, Tuple


class MigrationVerifier:
    """Clase para verificar la migración de PyQt6 a PySide6."""

    def __init__(self, verbose: bool = False):
        """Inicializa el verificador.
        
        Args:
            verbose: Si es True, muestra información detallada
        """
        self.verbose = verbose
        self.pyqt_references = []
        self.files_checked = 0
        self.files_with_references = 0
        
        # Patrones a buscar
        self.patterns = [
            r'PyQt6',
            r'pyqtSignal',
            r'pyqtSlot',
            r'QDialog\.DialogCode',
            r'Qt\.AlignmentFlag',
            r'QMessageBox\.Icon',
        ]

    def check_file(self, file_path: str) -> bool:
        """Verifica si un archivo contiene referencias a PyQt6.
        
        Args:
            file_path: Ruta al archivo a verificar
            
        Returns:
            bool: True si se encontraron referencias, False en caso contrario
        """
        self.files_checked += 1
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            references = []
            for pattern in self.patterns:
                matches = re.findall(pattern, content)
                if matches:
                    references.extend(matches)
            
            if references:
                self.files_with_references += 1
                self.pyqt_references.append((file_path, references))
                if self.verbose:
                    print(f"⚠️ {file_path}: {len(references)} referencias a PyQt6")
                return True
            else:
                if self.verbose:
                    print(f"✅ {file_path}: Sin referencias a PyQt6")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando {file_path}: {e}")
            return False

    def check_directory(self, directory: str) -> None:
        """Verifica todos los archivos Python en un directorio y subdirectorios.
        
        Args:
            directory: Directorio a verificar
        """
        print(f"Verificando migración en: {directory}")
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    self.check_file(os.path.join(root, file))
        
        print("\nResumen de verificación:")
        print(f"- Archivos verificados: {self.files_checked}")
        print(f"- Archivos con referencias a PyQt6: {self.files_with_references}")
        
        if self.pyqt_references:
            print("\n⚠️ Se encontraron referencias a PyQt6 en los siguientes archivos:")
            for file_path, references in self.pyqt_references:
                print(f"  - {file_path}: {len(set(references))} referencias")
                if self.verbose:
                    for ref in sorted(set(references)):
                        print(f"    - {ref}")
        else:
            print("\n✅ No se encontraron referencias a PyQt6. Migración completa.")


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Verifica la migración de PyQt6 a PySide6"
    )
    parser.add_argument(
        "directory", 
        help="Directorio a verificar"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Mostrar información detallada"
    )
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.directory):
        print(f"Error: '{args.directory}' no es un directorio válido")
        return 1
    
    verifier = MigrationVerifier(verbose=args.verbose)
    verifier.check_directory(args.directory)
    
    # Devolver código de salida según el resultado
    return 1 if verifier.files_with_references > 0 else 0


if __name__ == "__main__":
    sys.exit(main())