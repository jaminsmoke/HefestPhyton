#!/usr/bin/env python3
"""
Script para migrar código de PyQt6 a PySide6

Este script automatiza gran parte del proceso de migración de PyQt6 a PySide6,
realizando reemplazos de patrones comunes y ajustando la sintaxis según sea necesario.

Uso:
    python pyqt_to_pyside_migrator.py [directorio]

Ejemplo:
    python pyqt_to_pyside_migrator.py ../src
"""

import os
import re
import sys
import argparse
from typing import List, Dict, Tuple


class PyQtToPySideMigrator:
    """Clase para migrar código de PyQt6 a PySide6."""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        """Inicializa el migrador.
        
        Args:
            dry_run: Si es True, no modifica archivos, solo muestra cambios
            verbose: Si es True, muestra información detallada
        """
        self.dry_run = dry_run
        self.verbose = verbose
        self.files_processed = 0
        self.files_modified = 0
        self.replacements_made = 0
        
        # Patrones de reemplazo (patrón regex, reemplazo)
        self.patterns = [
            # Imports básicos
            (r'from PyQt6', 'from PySide6'),
            (r'import PyQt6', 'import PySide6'),
            
            # Clases y constantes específicas
            (r'QDialog\.DialogCode\.Accepted', 'QDialog.Accepted'),
            (r'QDialog\.DialogCode\.Rejected', 'QDialog.Rejected'),
            (r'QMessageBox\.Icon\.Critical', 'QMessageBox.Critical'),
            (r'QMessageBox\.Icon\.Warning', 'QMessageBox.Warning'),
            (r'QMessageBox\.Icon\.Information', 'QMessageBox.Information'),
            (r'QMessageBox\.Icon\.Question', 'QMessageBox.Question'),
            
            # Flags de alineación
            (r'Qt\.AlignmentFlag\.AlignRight', 'Qt.AlignRight'),
            (r'Qt\.AlignmentFlag\.AlignLeft', 'Qt.AlignLeft'),
            (r'Qt\.AlignmentFlag\.AlignCenter', 'Qt.AlignCenter'),
            (r'Qt\.AlignmentFlag\.AlignTop', 'Qt.AlignTop'),
            (r'Qt\.AlignmentFlag\.AlignBottom', 'Qt.AlignBottom'),
            (r'Qt\.AlignmentFlag\.AlignVCenter', 'Qt.AlignVCenter'),
            (r'Qt\.AlignmentFlag\.AlignHCenter', 'Qt.AlignHCenter'),
            
            # Atributos de widgets
            (r'Qt\.WidgetAttribute\.WA_DeleteOnClose', 'Qt.WA_DeleteOnClose'),
            
            # Tipos de mensajes Qt
            (r'QtMsgType, QMessageLogContext', 'QtMsgType, QtMessageLogContext'),
            
            # Señales y slots
            (r'\.connect\((.*?)\)  # type: ignore', r'.connect(\1)'),
            
            # Otros ajustes comunes
            (r'pyqtSignal', 'Signal'),
            (r'pyqtSlot', 'Slot'),
        ]

    def migrate_file(self, file_path: str) -> bool:
        """Migra un archivo de PyQt6 a PySide6.
        
        Args:
            file_path: Ruta al archivo a migrar
            
        Returns:
            bool: True si se hicieron cambios, False en caso contrario
        """
        self.files_processed += 1
        
        if self.verbose:
            print(f"Procesando: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Verificar si el archivo usa PyQt6
            if 'PyQt6' not in content:
                if self.verbose:
                    print(f"  Omitiendo: No usa PyQt6")
                return False
            
            # Aplicar patrones de reemplazo
            original_content = content
            replacements_in_file = 0
            
            for pattern, replacement in self.patterns:
                new_content, count = re.subn(pattern, replacement, content)
                if count > 0:
                    content = new_content
                    replacements_in_file += count
                    if self.verbose:
                        print(f"  Reemplazado: '{pattern}' → '{replacement}' ({count} veces)")
            
            # Guardar cambios si se hicieron reemplazos
            if content != original_content:
                self.files_modified += 1
                self.replacements_made += replacements_in_file
                
                if not self.dry_run:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ Migrado: {file_path} ({replacements_in_file} cambios)")
                else:
                    print(f"🔍 [DRY RUN] Se migraría: {file_path} ({replacements_in_file} cambios)")
                return True
            else:
                if self.verbose:
                    print(f"  Sin cambios necesarios")
                return False
                
        except Exception as e:
            print(f"❌ Error procesando {file_path}: {e}")
            return False

    def migrate_directory(self, directory: str) -> None:
        """Migra todos los archivos Python en un directorio y subdirectorios.
        
        Args:
            directory: Directorio a procesar
        """
        print(f"Iniciando migración en: {directory}")
        print(f"Modo: {'Simulación (dry-run)' if self.dry_run else 'Modificación real'}")
        
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.py'):
                    self.migrate_file(os.path.join(root, file))
        
        print("\nResumen de migración:")
        print(f"- Archivos procesados: {self.files_processed}")
        print(f"- Archivos modificados: {self.files_modified}")
        print(f"- Reemplazos realizados: {self.replacements_made}")
        
        if self.dry_run:
            print("\n⚠️ Ejecutado en modo simulación. No se realizaron cambios reales.")
            print("   Para aplicar los cambios, ejecute sin --dry-run")


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description="Migra código de PyQt6 a PySide6"
    )
    parser.add_argument(
        "directory", 
        help="Directorio a procesar"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true", 
        help="Simular migración sin modificar archivos"
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
    
    migrator = PyQtToPySideMigrator(dry_run=args.dry_run, verbose=args.verbose)
    migrator.migrate_directory(args.directory)
    return 0


if __name__ == "__main__":
    sys.exit(main())