#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hefest - Sistema Integral de Hostelería y Hospedería
Punto de entrada principal de la aplicación (Launcher)

Este archivo sirve como launcher y delega la ejecución al módulo principal en src/
Optimizado para funcionar correctamente con VS Code debugging.
"""

import sys
import os

def setup_environment():
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

def main():
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
            import importlib.util
            spec = importlib.util.spec_from_file_location("hefest_application", os.path.join(src_dir, "hefest_application.py"))
            
            # Verificar que spec y loader no sean None
            if spec is None:
                print(f"Error: No se pudo crear spec para {main_file}")
                return 1
                
            if spec.loader is None:
                print(f"Error: No se pudo obtener loader para {main_file}")
                return 1
            
            main_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(main_module)
            print("🚀 Iniciando Hefest...")
            return main_module.main()
        except ImportError as e:
            print(f"Error al importar el módulo principal: {e}")
            print(f"Directorio src: {src_dir}")
            print(f"Python path: {sys.path}")
            return 1
        except Exception as e:
            print(f"Error al ejecutar la aplicación: {e}")
            return 1
            
    except Exception as e:
        print(f"Error crítico en el launcher: {e}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        if exit_code is None:
            exit_code = 0
        
        # Detectar si estamos en modo debug (VS Code, PyCharm, etc.)
        import sys
        debug_mode = (
            hasattr(sys, 'gettrace') and sys.gettrace() is not None or  # Python debugger
            'debugpy' in sys.modules or  # VS Code debugger
            'pydevd' in sys.modules or   # PyCharm debugger
            '--debug' in sys.argv        # Argumento explícito
        )
        
        if debug_mode:
            # En modo debug, evitar sys.exit para mejor compatibilidad
            print(f"🔧 [DEBUG MODE] Aplicación terminada con código: {exit_code}")
            if exit_code != 0:
                print(f"⚠️ [DEBUG MODE] Código de salida indica error: {exit_code}")
        else:
            # Ejecución normal, usar sys.exit
            sys.exit(exit_code)
            
    except KeyboardInterrupt:
        print("\n⏹️ Aplicación interrumpida por el usuario")
        if not debug_mode:
            sys.exit(130)  # Código estándar para Ctrl+C
    except Exception as e:
        print(f"❌ Error inesperado en el launcher: {e}")
        if not debug_mode:
            sys.exit(1)