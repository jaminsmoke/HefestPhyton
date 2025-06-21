"""
Configuración de versión centralizada para Hefest
================================================

Archivo central que define la versión del proyecto.
Se utiliza por setup.py, main.py y scripts de build.
"""

__version__ = "0.0.13"
__version_info__ = (0, 0, 13)

# Información adicional
__author__ = "Hefest Development Team"
__email__ = "dev@hefest.com"
__license__ = "MIT"
__copyright__ = "© 2025 Hefest Development Team"

# URLs del proyecto
__homepage__ = "https://github.com/hefest-dev/hefest"
__repository__ = "https://github.com/hefest-dev/hefest.git"
__issues__ = "https://github.com/hefest-dev/hefest/issues"

# Metadatos de build
__build_date__ = "2025-06-12"
__python_requires__ = ">=3.10"


def get_version():
    """Retorna la versión actual como string."""
    return __version__


def get_version_info():
    """Retorna información detallada de versión."""
    return {
        "version": __version__,
        "version_info": __version_info__,
        "author": __author__,
        "build_date": __build_date__,
        "python_requires": __python_requires__,
    }
