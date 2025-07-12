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


def main() -> int:
    """Función principal del launcher"""
    try:
        # Configurar entorno
        src_dir = setup_environment()

        # Verificar que el directorio src existe
        if not os.path.exists(src_dir):
            print(f"Error: No se encontró el directorio src en {src_dir}")
            return 1
        
        # Verificar que el archivo principal existe
        main_file = os.path.join(src_dir, 'hefest_application.py')
        if not os.path.exists(main_file):
            print(f"Error: No se encontró el archivo principal en {main_file}")
            return 1
        
        # Importar y ejecutar el main desde src
        try:
            from hefest_application import main as app_main
            print("🚀 Iniciando Hefest...")
            result = app_main()
            return result if isinstance(result, int) else 0
        except ImportError as e:
            print(f"Error al importar el módulo principal: {e}")
            print(f"Directorio src: {src_dir}")
            print(f"Python path: {sys.path}")
            return 1
        except Exception as exc:  # pylint: disable=broad-except
            # TODO: Capturar excepciones más específicas
            print(f"Error al ejecutar la aplicación: {exc}")
            return 1

    except Exception as exc:  # pylint: disable=broad-except
        # TODO: Capturar excepciones más específicas
        print(f"Error crítico en el launcher: {exc}")
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
