#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hefest - Sistema Integral de Hostelería y Hospedería
Punto de entrada principal de la aplicación
"""

import sys
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# Filtro de avisos Qt
try:
    from PyQt6.QtCore import qInstallMessageHandler
    def qt_message_handler(mode, context, message):
        if ("box-shadow" in message or "transform" in message or 
            "Unknown property" in message):
            return
        print(message)
    qInstallMessageHandler(qt_message_handler)
except Exception as e:
    logging.error("Error configurando Qt handler: %s", e)

def setup_environment():
    """Configura el entorno de Python"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(current_dir, 'src')
    
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    os.environ.setdefault('HEFEST_ROOT', current_dir)
    return src_dir

def main():
    """Función principal"""
    try:
        src_dir = setup_environment()
        
        if not os.path.exists(src_dir):
            print(f"Error: No se encontró el directorio src en {src_dir}")
            return 1
        
        main_file = os.path.join(src_dir, 'hefest_application.py')
        if not os.path.exists(main_file):
            print(f"Error: No se encontró el archivo principal en {main_file}")
            return 1
        
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("hefest_application", main_file)
            
            if spec is None or spec.loader is None:
                print(f"Error: No se pudo cargar {main_file}")
                return 1
            
            main_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_module)
            print("Iniciando Hefest...")
            return main_module.main()
            
        except Exception as e:
            logging.error("Error al importar el módulo principal: %s", e)
            return 1
            
    except Exception as e:
        logging.error("Error crítico en el launcher: %s", e)
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        if exit_code is None:
            exit_code = 0
        
        debug_mode = (
            hasattr(sys, 'gettrace') and sys.gettrace() is not None or
            'debugpy' in sys.modules or
            'pydevd' in sys.modules or
            '--debug' in sys.argv
        )
        
        if debug_mode:
            print(f"[DEBUG MODE] Aplicación terminada con código: {exit_code}")
        else:
            sys.exit(exit_code)
            
    except KeyboardInterrupt:
        logging.info("Aplicación interrumpida por el usuario")
        sys.exit(130)
    except Exception as e:
        logging.error("Error inesperado: %s", e)
        sys.exit(1)