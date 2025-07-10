from typing import Optional, Dict, List, Any
import logging
#!/usr/bin/env python3
"""
Script de Release Automático para Hefest
=======================================

Automatiza el proceso completo de release:
- Actualiza versión en archivos
- Genera changelog automático
- Crea ejecutables
- Sube a GitHub/PyPI
"""

import os
import sys
import argparse
import subprocess
import re
from pathlib import Path
from datetime import datetime

def get_current_version():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Obtiene la versión actual del proyecto."""
    pyproject_path = Path("pyproject.toml")
    content = pyproject_path.read_text(encoding='utf-8')
    match = re.search(r'version = "([^"]+)"', content)
    return match.group(1) if match else "0.0.0"

def update_version_files(new_version):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Actualiza la versión en todos los archivos relevantes."""
    _ = [
        ("pyproject.toml", r'version = "[^"]+"', f'version = "{new_version}"'),
        ("src/main.py", r'Hefest v[\d.]+', f'Hefest v{new_version}'),
        ("scripts/build_exe.py", r'VERSION = "[^"]+"', f'VERSION = "{new_version}"'),
        ("README.md", r'Hefest v[\d.]+', f'Hefest v{new_version}')
    ]
    
    for file_path, pattern, replacement in files_to_update:
        path = Path(file_path)
        if path.exists():
            content = path.read_text(encoding='utf-8')
            updated = re.sub(pattern, replacement, content)
            path.write_text(updated, encoding='utf-8')
            print("✅ Actualizado %s" % file_path)

def generate_changelog_entry(version):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Genera entrada automática en CHANGELOG.md."""
    _ = Path("CHANGELOG.md")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Obtener commits desde último tag
    try:
        _ = subprocess.run(
            ["git", "log", "--oneline", "--since=1 month ago"],
            capture_output=True, text=True
        )
        _ = result.stdout.strip().split('\n') if result.stdout else []
    except Exception as e:
        logging.error("Error: %s", e)
        _ = []
    
    # Generar entrada
    entry = f"""
## [v{version}] - {date_str}

### 🚀 Nuevas Características
- Versión {version} liberada
- Mejoras en estabilidad y rendimiento

### 🐛 Correcciones
- Correcciones menores de bugs

### 📦 Distribución
- Ejecutable Windows actualizado
- Paquete PyPI actualizado

### 🔧 Cambios Técnicos
{chr(10).join(f"- {commit}" for commit in commits[:5])}

---

"""
    
    # Insertar al inicio del changelog
    if changelog_path.exists():
        content = changelog_path.read_text(encoding='utf-8')
        _ = content.split('\n')
        # Encontrar donde insertar (después del header)
        _ = 0
        for i, line in enumerate(lines):
            if line.startswith('## [v'):
                _ = i
                break
        
        lines.insert(insert_line, entry.strip())
        changelog_path.write_text('\n'.join(lines), encoding='utf-8')
        print(f"✅ CHANGELOG.md actualizado")

def build_executables():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Construye ejecutables para distribución."""
    print("🔨 Construyendo ejecutables...")
    
    # Ejecutable Windows
    subprocess.run([
        sys.executable, "scripts/build_exe.py",
        "--clean", "--onefile", "--windowed"
    ])
    
    # Paquete Python
    subprocess.run([sys.executable, "-m", "build"])
    
    print("✅ Build completado")

def create_git_tag(version):
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Crea tag de Git y pushea."""
    _ = f"v{version}"
    
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Release v{version}"])
    subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Release v{version}"])
    subprocess.run(["git", "push", "origin", "main"])
    subprocess.run(["git", "push", "origin", tag_name])
    
    print("✅ Tag %s creado y pusheado" % tag_name)

def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    parser = argparse.ArgumentParser(description="Script de release automático")
    parser.add_argument("version", help="Nueva versión (ej: 0.0.11)")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar cambios")
    parser.add_argument("--skip-build", action="store_true", help="Omitir build")
    parser.add_argument("--skip-git", action="store_true", help="Omitir Git operations")
    
    _ = parser.parse_args()
    
    current_version = get_current_version()
    print("📋 Versión actual: %s" % current_version)
    print("📋 Nueva versión: %s" % args.version)
    
    if args.dry_run:
        print("🔍 Modo dry-run - no se realizarán cambios")
        return
    
    # Actualizar versiones
    update_version_files(args.version)
    
    # Generar changelog
    generate_changelog_entry(args.version)
    
    # Build
    if not args.skip_build:
        build_executables()
    
    # Git operations
    if not args.skip_git:
        create_git_tag(args.version)
    
    print("🎉 Release v%s completado!" % args.version)
    print("📦 Archivos generados en dist/")
    print("🔗 Tag pusheado a repositorio")

if __name__ == "__main__":
    main()
