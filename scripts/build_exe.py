#!/usr/bin/env python3
"""
HEFEST - Build Script para Ejecutables
======================================

Script para generar ejecutables de HEFEST usando PyInstaller.
Soporta múltiples formatos y configuraciones.

Uso:
    python scripts/build_exe.py [opciones]

Ejemplos:
    python scripts/build_exe.py --onefile      # Ejecutable único
    python scripts/build_exe.py --windowed     # Sin consola
    python scripts/build_exe.py --setup        # Generar instalador
"""

import os
import sys
import argparse
import subprocess
import shutil
import platform
from pathlib import Path

# Configuración
PROJECT_NAME = "HEFEST"
VERSION = "0.0.10"
MAIN_SCRIPT = "main.py"
ICON_FILE = "assets/icons/hefest.ico"
COMPANY_NAME = "Hefest Development Team"
COPYRIGHT = f"© 2025 {COMPANY_NAME}"

def get_project_root():
    """Obtener la ruta raíz del proyecto."""
    return Path(__file__).parent.parent

def check_dependencies():
    """Verificar que PyInstaller está instalado."""
    try:
        import PyInstaller
        print(f"✅ PyInstaller {PyInstaller.__version__} encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller no encontrado")
        print("   Instala con: pip install PyInstaller")
        return False

def clean_build_dirs():
    """Limpiar directorios de build anteriores."""
    root = get_project_root()
    dirs_to_clean = ["build", "dist", "__pycache__"]
    
    for dir_name in dirs_to_clean:
        dir_path = root / dir_name
        if dir_path.exists():
            print(f"🧹 Limpiando {dir_path}")
            shutil.rmtree(dir_path)

def get_hidden_imports():
    """Obtener imports ocultos necesarios."""
    return [
        "PyQt6.QtCore",
        "PyQt6.QtGui", 
        "PyQt6.QtWidgets",
        "PyQt6.QtSql",
        "numpy",
        "sqlite3",
        "src.core",
        "src.services",
        "src.ui",
        "src.utils",
    ]

def get_data_files():
    """Obtener archivos de datos a incluir."""
    root = get_project_root()
    data_files = []
    
    # Directorios de datos
    data_dirs = [
        ("data", "data"),
        ("assets", "assets"),
        ("config", "config"),
        ("docs", "docs"),
    ]
    
    for src_dir, dst_dir in data_dirs:
        src_path = root / src_dir
        if src_path.exists():
            # Incluir todos los archivos del directorio
            for file_path in src_path.rglob("*"):
                if file_path.is_file():
                    rel_path = file_path.relative_to(src_path)
                    data_files.append((str(file_path), f"{dst_dir}/{rel_path}"))
    
    return data_files

def build_executable(args):
    """Construir el ejecutable con PyInstaller."""
    root = get_project_root()
    main_path = root / MAIN_SCRIPT
    icon_path = root / ICON_FILE
    
    if not main_path.exists():
        print(f"❌ No se encuentra {main_path}")
        return False
    
    # Argumentos base de PyInstaller
    pyinstaller_args = [
        "python", "-m", "PyInstaller",
        str(main_path),
        "--name", PROJECT_NAME,
        "--clean",
        "--noconfirm",
    ]
    
    # Configurar según opciones
    if args.onefile:
        pyinstaller_args.append("--onefile")
        print("📦 Generando ejecutable único")
    else:
        pyinstaller_args.append("--onedir")
        print("📁 Generando directorio de aplicación")
    
    if args.windowed or platform.system() == "Windows":
        pyinstaller_args.append("--windowed")
        print("🖥️ Modo ventana (sin consola)")
    
    # Icono
    if icon_path.exists():
        pyinstaller_args.extend(["--icon", str(icon_path)])
        print(f"🎨 Usando icono: {icon_path}")
    
    # Imports ocultos
    for import_name in get_hidden_imports():
        pyinstaller_args.extend(["--hidden-import", import_name])
    
    # Archivos de datos
    data_files = get_data_files()
    for src, dst in data_files[:10]:  # Limitar salida
        pyinstaller_args.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
    
    print(f"📄 Incluyendo {len(data_files)} archivos de datos")
    
    # Información de versión (Windows)
    if platform.system() == "Windows":
        version_info = create_version_file()
        if version_info:
            pyinstaller_args.extend(["--version-file", version_info])
    
    # Ejecutar PyInstaller
    print("\n🔨 Ejecutando PyInstaller...")
    print("Comando:", " ".join(pyinstaller_args))
    
    try:
        result = subprocess.run(pyinstaller_args, cwd=root, check=True)
        print("✅ Build completado exitosamente")
        
        # Mostrar ubicación del ejecutable
        dist_dir = root / "dist"
        if args.onefile:
            exe_name = f"{PROJECT_NAME}.exe" if platform.system() == "Windows" else PROJECT_NAME
            exe_path = dist_dir / exe_name
        else:
            exe_path = dist_dir / PROJECT_NAME
        
        print(f"📍 Ejecutable generado en: {exe_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en build: {e}")
        return False

def create_version_file():
    """Crear archivo de información de versión para Windows."""
    if platform.system() != "Windows":
        return None
    
    root = get_project_root()
    version_file = root / "version_info.txt"
    
    version_info_content = f"""# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({VERSION.replace('.', ', ')}, 0),
    prodvers=({VERSION.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'{COMPANY_NAME}'),
           StringStruct(u'FileDescription', u'Sistema Integral de Hostelería y Hospedería'),
           StringStruct(u'FileVersion', u'{VERSION}'),
           StringStruct(u'InternalName', u'{PROJECT_NAME}'),
           StringStruct(u'LegalCopyright', u'{COPYRIGHT}'),
           StringStruct(u'OriginalFilename', u'{PROJECT_NAME}.exe'),
           StringStruct(u'ProductName', u'{PROJECT_NAME}'),
           StringStruct(u'ProductVersion', u'{VERSION}')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    try:
        with open(version_file, 'w', encoding='utf-8') as f:
            f.write(version_info_content)
        print(f"📄 Archivo de versión creado: {version_file}")
        return str(version_file)
    except Exception as e:
        print(f"⚠️ No se pudo crear archivo de versión: {e}")
        return None

def create_installer():
    """Crear instalador usando Inno Setup (Windows) o equivalente."""
    if platform.system() != "Windows":
        print("⚠️ Instaladores solo soportados en Windows actualmente")
        return False
    
    print("🔧 Creando instalador con Inno Setup...")
    print("   (Requiere Inno Setup instalado)")
    
    # Aquí se podría generar un script .iss para Inno Setup
    # Por ahora solo mostramos instrucciones
    print("📝 Para crear instalador manualmente:")
    print("   1. Instalar Inno Setup")
    print("   2. Usar el ejecutable en dist/ como base")
    print("   3. Configurar instalador con wizard de Inno Setup")
    
    return True

def main():
    """Función principal."""
    parser = argparse.ArgumentParser(
        description="Build script para HEFEST",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python scripts/build_exe.py                  # Build básico
  python scripts/build_exe.py --onefile       # Ejecutable único  
  python scripts/build_exe.py --windowed      # Sin consola
  python scripts/build_exe.py --clean         # Limpiar antes de build
  python scripts/build_exe.py --setup         # Generar también instalador
        """
    )
    
    parser.add_argument(
        "--onefile", 
        action="store_true",
        help="Generar ejecutable único en lugar de directorio"
    )
    parser.add_argument(
        "--windowed",
        action="store_true", 
        help="Ejecutable sin ventana de consola"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Limpiar directorios de build antes de empezar"
    )
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Generar también instalador después del build"
    )
    
    args = parser.parse_args()
    
    print("🏨 HEFEST - Build Script")
    print("========================")
    print(f"Versión: {VERSION}")
    print(f"Plataforma: {platform.system()}")
    print()
    
    # Verificar dependencias
    if not check_dependencies():
        return 1
    
    # Limpiar si se solicita
    if args.clean:
        clean_build_dirs()
    
    # Construir ejecutable
    if not build_executable(args):
        return 1
    
    # Crear instalador si se solicita
    if args.setup:
        create_installer()
    
    print("\n🎉 Build completado exitosamente!")
    print("Puedes encontrar el ejecutable en el directorio 'dist/'")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
