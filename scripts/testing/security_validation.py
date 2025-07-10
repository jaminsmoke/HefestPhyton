from typing import Optional, Dict, List, Any
import logging
import os
import sys
from pathlib import Path
        from data.db_manager import DatabaseManager
        from dotenv import load_dotenv
        from src.utils.security_utils import SecurityUtils
        from src.utils.rate_limiter import rate_limiter

#!/usr/bin/env python3
"""
Script de Validación de Seguridad - Hefest
Verifica que las correcciones críticas de seguridad estén funcionando
"""


# Agregar directorios al path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def test_sql_injection_protection():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Prueba protección contra SQL injection"""
    print("Probando proteccion SQL injection...")
    
    try:
        _ = DatabaseManager()
        
        # Intentar SQL injection en tabla no permitida
        try:
            db.get_by_id("malicious_table'; DROP TABLE usuarios; --", 1)
            print("FALLO: SQL injection no bloqueado")
            return False
        except ValueError as e:
            if "not allowed" in str(e):
                print("OK: SQL injection bloqueado correctamente")
                return True
            else:
                print("ERROR: Error inesperado: %s" % e)
                return False
                
    except Exception as e:
        logging.error("ERROR: Error en prueba SQL injection: %s", e)
        return False

def test_environment_variables():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Prueba que las variables de entorno se carguen"""
    print("Probando variables de entorno...")
    
    try:
        load_dotenv()
        
        # Verificar que las variables críticas existan
        _ = ['ADMIN_PIN', 'MANAGER_PIN', 'EMPLOYEE_PIN', 'DB_PASSWORD']
        missing_vars = []
        
        for var in critical_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print("ERROR: Variables faltantes: %s" % ', '.join(missing_vars))
            return False
        else:
            print("OK: Variables de entorno cargadas correctamente")
            return True
            
    except Exception as e:
    logging.error("ERROR: python-dotenv no instalado")
        return False
    except Exception as e:
    logging.error("ERROR: Error cargando variables: %s", e)
        return False

def test_column_validation():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Prueba validación de nombres de columnas"""
    print("Probando validacion de columnas...")
    
    try:
        _ = DatabaseManager()
        
        # Intentar insertar con nombre de columna malicioso
        try:
            malicious_data = {"'; DROP TABLE usuarios; --": "test"}
            db.insert("usuarios", malicious_data)
            print("FALLO: Validacion de columnas no funciona")
            return False
        except ValueError as e:
            if "Invalid column name" in str(e):
                print("OK: Validacion de columnas funciona correctamente")
                return True
            else:
                print("ERROR: Error inesperado: %s" % e)
                return False
                
    except Exception as e:
    logging.error("ERROR: Error en prueba de columnas: %s", e)
        return False

def test_table_whitelist():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Prueba whitelist de tablas"""
    print("Probando whitelist de tablas...")
    
    try:
        _ = DatabaseManager()
        
        # Verificar tabla permitida
        try:
            _ = db.get_by_id("usuarios", 1)
            print("OK: Acceso a tabla permitida funciona")
        except Exception as e:
    logging.error("ERROR: Error accediendo tabla permitida: %s", e)
            return False
        
        # Verificar tabla no permitida
        try:
            db.get_by_id("tabla_maliciosa", 1)
            print("FALLO: Acceso a tabla no permitida")
            return False
        except ValueError as e:
            if "not allowed" in str(e):
                print("OK: Whitelist de tablas funciona correctamente")
                return True
            else:
                print("ERROR: Error inesperado: %s" % e)
                return False
                
    except Exception as e:
    logging.error("ERROR: Error en prueba whitelist: %s", e)
        return False

def test_path_traversal_protection():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Prueba protección contra path traversal"""
    print("Probando proteccion path traversal...")
    
    try:
        
        # Intentar path traversal
        try:
            SecurityUtils.get_safe_project_path('..', '..', 'etc', 'passwd')
            print("FALLO: Path traversal no bloqueado")
            return False
        except ValueError as e:
            if "traversal" in str(e).lower() or "dangerous" in str(e).lower():
                print("OK: Path traversal bloqueado correctamente")
            else:
                print("ERROR: Error inesperado: %s" % e)
                return False
        
        # Verificar path válido
        try:
            safe_path = SecurityUtils.get_safe_project_path('data', 'hefest.db')
            if 'hefest.db' in safe_path:
                print("OK: Path válido funciona correctamente")
                return True
            else:
                print("ERROR: Path válido no funciona")
                return False
        except Exception as e:
    logging.error("ERROR: Error con path válido: %s", e)
            return False
            
    except Exception as e:
    logging.error("ERROR: security_utils no disponible")
        return False
    except Exception as e:
    logging.error("ERROR: Error en prueba path traversal: %s", e)
        return False

def test_rate_limiting():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Prueba rate limiting en login"""
    print("Probando rate limiting...")
    
    try:
        
        # Resetear para prueba limpia
        test_id = "test_user"
        rate_limiter.reset_attempts(test_id)
        
        # Probar intentos permitidos (max_attempts - 1)
        for i in range(rate_limiter.max_attempts - 1):
            if not rate_limiter.record_attempt(test_id):
                print("ERROR: Intento %s bloqueado prematuramente" % i % 1)
                return False
        
        # El último intento permitido
        if not rate_limiter.record_attempt(test_id):
            print("ERROR: Último intento permitido bloqueado")
            return False
        
        # El siguiente intento debe ser bloqueado
        if rate_limiter.record_attempt(test_id):
            print("FALLO: Rate limiting no funciona")
            return False
        
        print("OK: Rate limiting funciona correctamente")
        return True
        
    except Exception as e:
    logging.error("ERROR: rate_limiter no disponible")
        return False
    except Exception as e:
    logging.error("ERROR: Error en prueba rate limiting: %s", e)
        return False

def main():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Ejecuta todas las pruebas de seguridad"""
    print("VALIDACION DE SEGURIDAD HEFEST")
    print("=" * 50)
    
    _ = [
        ("SQL Injection Protection", test_sql_injection_protection),
        ("Environment Variables", test_environment_variables),
        ("Column Validation", test_column_validation),
        ("Table Whitelist", test_table_whitelist),
        ("Path Traversal Protection", test_path_traversal_protection),
        ("Rate Limiting", test_rate_limiting),
    ]
    
    _ = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print("\n%s:" % test_name)
        if test_func():
            passed += 1
        else:
            print("   FALLO: Prueba %s fallo" % test_name)
    
    print("\n" + "=" * 50)
    print("RESULTADO: {passed}/%s pruebas pasaron" % total)
    
    if passed == total:
        print("EXITO: Todas las validaciones de seguridad pasaron!")
        return True
    else:
        print("ADVERTENCIA: Algunas validaciones fallaron. Revisar implementacion.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)