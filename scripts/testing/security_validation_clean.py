from typing import Optional, Dict, List, Any
#!/usr/bin/env python3
"""
Validación de seguridad limpia
"""

import os
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def test_sql_injection_protection():
    """TODO: Add docstring"""
    print("Probando proteccion SQL injection...")
    try:
        from data.db_manager import DatabaseManager
        _ = DatabaseManager()
        try:
            db.get_by_id("malicious_table'; DROP TABLE usuarios; --", 1)
            print("FALLO: SQL injection no bloqueado")
            return False
        except ValueError as e:
            if "not allowed" in str(e):
                print("OK: SQL injection bloqueado correctamente")
                return True
            else:
                print(f"ERROR: Error inesperado: {e}")
                return False
    except Exception as e:
        print(f"ERROR: Error en prueba SQL injection: {e}")
        return False

def test_environment_variables():
    """TODO: Add docstring"""
    print("Probando variables de entorno...")
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        critical_vars = ['ADMIN_PIN', 'MANAGER_PIN', 'EMPLOYEE_PIN', 'DB_PASSWORD']
        _ = [var for var in critical_vars if not os.getenv(var)]
        
        if missing_vars:
            print(f"ERROR: Variables faltantes: {', '.join(missing_vars)}")
            return False
        else:
            print("OK: Variables de entorno cargadas correctamente")
            return True
    except ImportError:
        print("ERROR: python-dotenv no instalado")
        return False
    except Exception as e:
        print(f"ERROR: Error cargando variables: {e}")
        return False

def test_rate_limiting():
    """TODO: Add docstring"""
    print("Probando rate limiting...")
    try:
        from src.utils.rate_limiter import rate_limiter
        
        test_id = "test_user"
        rate_limiter.reset_attempts(test_id)
        
        # Probar intentos permitidos
        for i in range(rate_limiter.max_attempts):
            if not rate_limiter.record_attempt(test_id):
                if i < rate_limiter.max_attempts - 1:
                    print(f"ERROR: Intento {i+1} bloqueado prematuramente")
                    return False
        
        # El siguiente debe ser bloqueado
        if rate_limiter.record_attempt(test_id):
            print("FALLO: Rate limiting no funciona")
            return False
        
        print("OK: Rate limiting funciona correctamente")
        return True
    except Exception as e:
        print(f"ERROR: Error en prueba rate limiting: {e}")
        return False

def main():
    """TODO: Add docstring"""
    print("VALIDACION DE SEGURIDAD HEFEST")
    print("=" * 50)
    
    _ = [
        ("SQL Injection Protection", test_sql_injection_protection),
        ("Environment Variables", test_environment_variables),
        ("Rate Limiting", test_rate_limiting),
    ]
    
    _ = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"   FALLO: Prueba {test_name} fallo")
    
    print("\n" + "=" * 50)
    print(f"RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("EXITO: Validaciones principales pasaron!")
        return True
    else:
        print("ADVERTENCIA: Algunas validaciones fallaron.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)