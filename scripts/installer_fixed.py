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
from typing import List, Optional


class HefestInstaller:
    """Instalador principal para el sistema Hefest."""
    
    def __init__(self) -> None:
        """Inicializar el instalador."""
        self.system = platform.system()
        self.python_version = sys.version_info
        self.install_dir = Path.home() / "HEFEST"
        self.errors: List[str] = []

    def check_system_requirements(self) -> bool:
        """Verificar requisitos del sistema."""
        print("🔍 Verificando requisitos del sistema...")

        # Verificar Python 3.8+
        if self.python_version < (3, 8):
            self.errors.append("Python 3.8+ requerido")
            return False

        print(f"✅ Python {self.python_version.major}.{self.python_version.minor}")
        return True

    def install_system_dependencies(self) -> bool:
        """Instalar dependencias del sistema."""
        print("📦 Instalando dependencias del sistema...")

        try:
            if self.system == "Linux":
                subprocess.run([
                    "sudo", "apt-get", "update"
                ], check=True, capture_output=True)
                
                subprocess.run([
                    "sudo", "apt-get", "install", "-y",
                    "python3-pip", "python3-venv", "sqlite3"
                ], check=True, capture_output=True)

            elif self.system == "Darwin":  # macOS
                subprocess.run([
                    "brew", "install", "python", "sqlite3"
                ], check=True, capture_output=True)

            print("✅ Dependencias instaladas")
            return True

        except subprocess.CalledProcessError as e:
            self.errors.append(f"Error instalando dependencias: {e}")
            return False

    def create_virtual_environment(self) -> bool:
        """Crear entorno virtual."""
        print("🐍 Creando entorno virtual...")

        venv_path = self.install_dir / "venv"

        try:
            subprocess.run([
                sys.executable, "-m", "venv", str(venv_path)
            ], check=True, capture_output=True)

            print("✅ Entorno virtual creado")
            return True

        except subprocess.CalledProcessError as e:
            self.errors.append(f"Error creando entorno virtual: {e}")
            return False

    def install_python_dependencies(self) -> bool:
        """Instalar dependencias de Python."""
        print("📦 Instalando dependencias de Python...")

        if self.system == "Windows":
            pip_path = self.install_dir / "venv" / "Scripts" / "pip"
        else:
            pip_path = self.install_dir / "venv" / "bin" / "pip"

        requirements = [
            "PyQt6>=6.5.0",
            "sqlite3",
            "requests>=2.28.0",
            "python-dotenv>=1.0.0"
        ]

        try:
            for req in requirements:
                subprocess.run([
                    str(pip_path), "install", req
                ], check=True, capture_output=True)

            print("✅ Dependencias de Python instaladas")
            return True

        except subprocess.CalledProcessError as e:
            self.errors.append(f"Error instalando dependencias Python: {e}")
            return False

    def setup_database(self) -> bool:
        """Configurar base de datos."""
        print("💾 Configurando base de datos...")

        db_path = self.install_dir / "data" / "hefest.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            conn = sqlite3.connect(str(db_path))
            # Aquí irían las tablas iniciales
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    role TEXT NOT NULL
                )
            """)
            conn.commit()
            conn.close()

            print("✅ Base de datos configurada")
            return True

        except sqlite3.Error as e:
            self.errors.append(f"Error configurando base de datos: {e}")
            return False

    def create_desktop_shortcut(self) -> bool:
        """Crear acceso directo en el escritorio."""
        print("🖥️ Creando acceso directo...")

        try:
            desktop = Path.home() / "Desktop"
            if not desktop.exists():
                return True  # No hay escritorio, no es error

            if self.system == "Windows":
                # Crear .bat file en Windows
                shortcut_path = desktop / "Hefest.bat"
                python_exe = self.install_dir / "venv" / "Scripts" / "python.exe"
                main_py = self.install_dir / "main.py"
                
                with open(shortcut_path, "w", encoding="utf-8") as f:
                    f.write(f'@echo off\n"{python_exe}" "{main_py}"\npause\n')

            else:
                # Crear .desktop file en Linux
                shortcut_path = desktop / "Hefest.desktop"
                python_exe = self.install_dir / "venv" / "bin" / "python"
                main_py = self.install_dir / "main.py"
                
                with open(shortcut_path, "w", encoding="utf-8") as f:
                    f.write(f"""[Desktop Entry]
Name=Hefest
Comment=Sistema Integral de Hostelería
Exec={python_exe} {main_py}
Terminal=false
Type=Application
Categories=Office;
""")
                os.chmod(shortcut_path, 0o755)

            print("✅ Acceso directo creado")
            return True

        except (OSError, PermissionError) as e:
            self.errors.append(f"Error creando acceso directo: {e}")
            return False

    def install(self) -> bool:
        """Ejecutar instalación completa."""
        print("🚀 Iniciando instalación de Hefest...")
        print("=" * 50)

        steps = [
            self.check_system_requirements,
            self.install_system_dependencies,
            self.create_virtual_environment,
            self.install_python_dependencies,
            self.setup_database,
            self.create_desktop_shortcut
        ]

        for step in steps:
            if not step():
                print("\n❌ Instalación fallida:")
                for error in self.errors:
                    print(f"  - {error}")
                return False

        print("\n🎉 ¡Instalación completada exitosamente!")
        print(f"📁 Hefest instalado en: {self.install_dir}")
        return True


def main() -> int:
    """Función principal del instalador."""
    installer = HefestInstaller()
    
    if installer.install():
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
