#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hefest - Sistema Integral de Hostelería y Hospedería
Punto de entrada principal de la aplicación (Launcher)

Este archivo sirve como launcher y delega la ejecución al módulo principal
en src/. Optimizado para funcionar correctamente con VS Code debugging.

---
Filtro de avisos Qt:
Se instala un filtro de mensajes de Qt para ignorar avisos de estilos CSS
no soportados (como 'box-shadow' y 'transform') que aparecen en la consola
pero no afectan la funcionalidad ni la experiencia de usuario.
Esto mantiene el log de ejecución más limpio y enfocado en errores relevantes.
"""

import sys
import os
import logging
import importlib.util
from typing import Any

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# === FILTRO DE AVISOS QT (IGNORAR box-shadow/transform) ===
try:
    from PyQt6.QtCore import (
        qInstallMessageHandler, QtMsgType, QMessageLogContext
    )

    def qt_message_handler(
        _msg_type: QtMsgType,
        _context: QMessageLogContext,
        message: str | None
    ) -> None:
        """Filtra avisos irrelevantes de estilos no soportados en Qt."""
        # Filtrar todos los avisos irrelevantes de estilos no soportados
        if message and (
            "box-shadow" in message
            or "transform" in message
            or "Unknown property overflow" in message
            or "Unknown property text-overflow" in message
        ):
            return  # Ignora estos avisos de estilos
        print(message)

    qInstallMessageHandler(qt_message_handler)
except ImportError:
    pass  # Si no está PyQt6, no se instala el filtro


def setup_environment() -> str:
    """Configura el entorno de Python para la aplicación"""
    # Obtener el directorio del proyecto
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')

    # Agregar src al path si no está ya presente
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    # Configurar variables de entorno si es necesario
    os.environ.setdefault('HEFEST_ROOT', current_dir)

    return src_dir


def validate_environment(src_dir: str) -> int | None:
    """Valida que el entorno esté correctamente configurado.

    Returns:
        int: Código de error si hay problemas, None si todo está bien
    """
    if not os.path.exists(src_dir):
        print(f"Error: No se encontró el directorio src en {src_dir}")
        return 1

    main_file = os.path.join(src_dir, 'hefest_application.py')
    if not os.path.exists(main_file):
        print(f"Error: No se encontró el archivo principal en {main_file}")
        return 1

    return None


def load_main_module(src_dir: str) -> tuple[Any | None, int | None]:
    """Carga el módulo principal de la aplicación.

    Returns:
        tuple: (module, error_code) donde error_code es None si no hay errores
    """
    main_file = os.path.join(src_dir, "hefest_application.py")

    try:
        spec = importlib.util.spec_from_file_location(
            "hefest_application", main_file
        )

        if spec is None:
            print(f"Error: No se pudo crear spec para {main_file}")
            return None, 1

        if spec.loader is None:
            print(f"Error: No se pudo obtener loader para {main_file}")
            return None, 1

        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)
        return main_module, None

    except ModuleNotFoundError as exc:
        print(f"Módulo no encontrado: {exc}")
        print(f"Directorio src: {src_dir}")
        print(f"Python path: {sys.path}")
        return None, 1
    except ImportError as exc:
        print(f"Error al importar el módulo principal: {exc}")
        print(f"Directorio src: {src_dir}")
        print(f"Python path: {sys.path}")
        return None, 1
    except AttributeError as exc:
        print(f"Error de atributo al cargar el módulo: {exc}")
        return None, 1


def execute_application(main_module: Any) -> int:
    """Ejecuta la aplicación principal.

    Returns:
        int: Código de retorno de la aplicación
    """
    try:
        print("🚀 Iniciando Hefest...")
        result = main_module.main()
        return result if isinstance(result, int) else 0
    except AttributeError as exc:
        print(f"Error: El módulo no tiene función main(): {exc}")
        return 1
    except Exception as exc:  # pylint: disable=broad-except
        # EXCEPCIÓN FUNCIONAL: Captura errores de ejecución de la aplicación
        # que no se pueden predecir específicamente
        print(f"Error durante la ejecución de la aplicación: {exc}")
        return 1


def main() -> int:
    """Función principal del launcher"""
    try:
        # Configurar entorno
        src_dir = setup_environment()

        # Validar entorno
        error_code = validate_environment(src_dir)
        if error_code is not None:
            return error_code

        # Cargar módulo principal
        main_module, error_code = load_main_module(src_dir)
        if error_code is not None:
            return error_code

        # Ejecutar aplicación
        return execute_application(main_module)

    except FileNotFoundError as exc:
        print(f"Archivo crítico no encontrado: {exc}")
        return 1
    except PermissionError as exc:
        print(f"Error de permisos en el launcher: {exc}")
        return 1
    except Exception as exc:  # pylint: disable=broad-except
        # EXCEPCIÓN FUNCIONAL: Captura errores inesperados del sistema
        # o del entorno que no se pueden predecir específicamente
        print(f"Error crítico inesperado en el launcher: {exc}")
        return 1


if __name__ == "__main__":
    DEBUG_MODE = False
    try:
        EXIT_CODE = main()
        if EXIT_CODE is None:
            EXIT_CODE = 0

        # Detectar si estamos en modo debug (VS Code, PyCharm, etc.)
        DEBUG_MODE = (
            hasattr(sys, 'gettrace') and sys.gettrace() is not None or
            'debugpy' in sys.modules or  # VS Code debugger
            'pydevd' in sys.modules or   # PyCharm debugger
            '--debug' in sys.argv        # Argumento explícito
        )

        if DEBUG_MODE:
            # En modo debug, evitar sys.exit para mejor compatibilidad
            print(
                f"🔧 [DEBUG MODE] Aplicación terminada con código: {EXIT_CODE}"
            )
            if EXIT_CODE != 0:
                print(
                    f"⚠️ [DEBUG MODE] Código de salida indica error: "
                    f"{EXIT_CODE}"
                )
        else:
            # Ejecución normal, usar sys.exit
            sys.exit(EXIT_CODE)

    except KeyboardInterrupt:
        print("\n⏹️ Aplicación interrumpida por el usuario")
        if not DEBUG_MODE:
            sys.exit(130)  # Código estándar para Ctrl+C
    except Exception as exc:  # pylint: disable=broad-except
        print(f"❌ Error inesperado en el launcher: {exc}")
        if not DEBUG_MODE:
            sys.exit(1)
