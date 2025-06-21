#!/usr/bin/env python3
"""
Instalador Avanzado para Hefest
==============================

Instalador inteligente que detecta el sistema y configura automáticamente:
- Dependencias del sistema
- Entorno virtual
- Base de datos
- Configuración inicial
- Iconos del sistema
"""

import os
import sys
import subprocess
import platform
import shutil
import json
import sqlite3
from pathlib import Path
import requests
import zipfile

class HefestInstaller:
    def __init__(self):
        self.system = platform.system()
        self.python_version = sys.version_info
        self.install_dir = Path.home() / "HEFEST"
        self.errors = []
        
    def check_requirements(self):
        """Verifica requisitos del sistema."""
        print("🔍 Verificando requisitos del sistema...")
        
        # Python version
        if self.python_version < (3, 10):
            self.errors.append(f"Python 3.10+ requerido. Actual: {sys.version}")
            
        # Git (opcional)
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            print("✅ Git disponible")
        except:
            print("⚠️ Git no encontrado (opcional)")
            
        # Pip
        try:
            import pip
            print("✅ Pip disponible")
        except ImportError:
            self.errors.append("pip no está instalado")
            
        return len(self.errors) == 0
    
    def create_virtual_environment(self):
        """Crea entorno virtual dedicado."""
        venv_path = self.install_dir / ".venv"
        
        print(f"🐍 Creando entorno virtual en {venv_path}")
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)])
        
        # Activar venv y actualizar pip
        if self.system == "Windows":
            python_exe = venv_path / "Scripts" / "python.exe"
            pip_exe = venv_path / "Scripts" / "pip.exe"
        else:
            python_exe = venv_path / "bin" / "python"
            pip_exe = venv_path / "bin" / "pip"
            
        subprocess.run([str(pip_exe), "install", "--upgrade", "pip"])
        return python_exe, pip_exe
        
    def download_hefest(self):
        """Descarga la última versión de Hefest."""
        print("📥 Descargando Hefest...")
        
        # Para desarrollo, copiar archivos locales
        # En producción, descargar desde GitHub releases
        source_dir = Path(__file__).parent.parent
        
        # Copiar archivos esenciales
        essential_files = [
            "src/", "data/", "config/", "assets/",
            "main.py", "pyproject.toml", "requirements.txt",
            "README.md", "LICENSE"
        ]
        
        for item in essential_files:
            src = source_dir / item
            dst = self.install_dir / item
            
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif src.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                
        print("✅ Archivos copiados")
        
    def install_dependencies(self, pip_exe):
        """Instala dependencias de Python."""
        print("📦 Instalando dependencias...")
        
        requirements_file = self.install_dir / "requirements.txt"
        subprocess.run([str(pip_exe), "install", "-r", str(requirements_file)])
        
        print("✅ Dependencias instaladas")
        
    def setup_database(self):
        """Configura la base de datos inicial."""
        print("🗃️ Configurando base de datos...")
        
        db_path = self.install_dir / "data" / "hefest.db"
        init_script = self.install_dir / "data" / "init_db.py"
        
        if init_script.exists():
            subprocess.run([sys.executable, str(init_script)], 
                         cwd=str(self.install_dir))
            
        print("✅ Base de datos configurada")
        
    def create_shortcuts(self):
        """Crea accesos directos del sistema."""
        print("🔗 Creando accesos directos...")
        
        if self.system == "Windows":
            self._create_windows_shortcuts()
        elif self.system == "Linux":
            self._create_linux_shortcuts()
        elif self.system == "Darwin":  # macOS
            self._create_macos_shortcuts()
            
    def _create_windows_shortcuts(self):
        """Crea shortcuts en Windows."""
        try:
            import winshell
            from win32com.client import Dispatch
            
            # Desktop shortcut
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "HEFEST.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = str(self.install_dir / "main.py")
            shortcut.WorkingDirectory = str(self.install_dir)
            shortcut.IconLocation = str(self.install_dir / "assets" / "icons" / "hefest.ico")
            shortcut.save()
            
            print("✅ Acceso directo en escritorio creado")
            
        except ImportError:
            print("⚠️ No se pudieron crear accesos directos (winshell no disponible)")
            
    def _create_linux_shortcuts(self):
        """Crea .desktop file en Linux."""
        desktop_file = f"""[Desktop Entry]
Name=HEFEST
Comment=Sistema Integral de Hostelería
Exec=python {self.install_dir}/main.py
Icon={self.install_dir}/assets/icons/hefest.png
Terminal=false
Type=Application
Categories=Office;
"""
        
        desktop_path = Path.home() / ".local" / "share" / "applications" / "hefest.desktop"
        desktop_path.parent.mkdir(parents=True, exist_ok=True)
        desktop_path.write_text(desktop_file)
        
        print("✅ Archivo .desktop creado")
        
    def _create_macos_shortcuts(self):
        """Crea app bundle en macOS."""
        # Implementar si es necesario
        print("⚠️ Shortcuts en macOS no implementados aún")
        
    def create_uninstaller(self):
        """Crea script de desinstalación."""
        uninstaller_content = f"""#!/usr/bin/env python3
import shutil
import os
from pathlib import Path

install_dir = Path("{self.install_dir}")
print(f"Desinstalando HEFEST de {{install_dir}}")

# Eliminar directorio completo
if install_dir.exists():
    shutil.rmtree(install_dir)
    print("✅ HEFEST desinstalado correctamente")
else:
    print("⚠️ HEFEST no encontrado")

# Eliminar shortcuts (implementar según SO)
input("Presiona Enter para continuar...")
"""
        
        uninstaller_path = self.install_dir / "uninstall.py"
        uninstaller_path.write_text(uninstaller_content)
        
        print("✅ Desinstalador creado")
        
    def run_installation(self):
        """Ejecuta proceso completo de instalación."""
        print("🚀 Iniciando instalación de HEFEST...")
        print(f"📁 Directorio de instalación: {self.install_dir}")
        
        try:
            # Verificar requisitos
            if not self.check_requirements():
                print("❌ Requisitos no cumplidos:")
                for error in self.errors:
                    print(f"  - {error}")
                return False
                
            # Crear directorio
            self.install_dir.mkdir(parents=True, exist_ok=True)
            
            # Crear entorno virtual
            python_exe, pip_exe = self.create_virtual_environment()
            
            # Descargar archivos
            self.download_hefest()
            
            # Instalar dependencias
            self.install_dependencies(pip_exe)
            
            # Configurar base de datos
            self.setup_database()
            
            # Crear shortcuts
            self.create_shortcuts()
            
            # Crear desinstalador
            self.create_uninstaller()
            
            print("🎉 ¡Instalación completada exitosamente!")
            print(f"📍 HEFEST instalado en: {self.install_dir}")
            print("🖥️ Busca el icono 'HEFEST' en tu escritorio o menú de aplicaciones")
            
            return True
            
        except Exception as e:
            print(f"❌ Error durante la instalación: {e}")
            return False
            
def main():
    print("=" * 50)
    print("  HEFEST - Instalador Automático v0.0.10")
    print("  Sistema Integral de Hostelería")
    print("=" * 50)
    
    installer = HefestInstaller()
    
    # Confirmar instalación
    response = input(f"¿Instalar HEFEST en {installer.install_dir}? (s/N): ")
    if response.lower() not in ['s', 'sí', 'si', 'y', 'yes']:
        print("Instalación cancelada")
        return
        
    success = installer.run_installation()
    
    if success:
        # Preguntar si ejecutar ahora
        run_now = input("¿Ejecutar HEFEST ahora? (s/N): ")
        if run_now.lower() in ['s', 'sí', 'si', 'y', 'yes']:
            main_script = installer.install_dir / "main.py"
            subprocess.run([sys.executable, str(main_script)], 
                         cwd=str(installer.install_dir))
    
if __name__ == "__main__":
    main()
