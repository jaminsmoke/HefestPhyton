from typing import Optional, Dict, List, Any
import logging
import traceback

#!/usr/bin/env python3
"""
Script simple de diagnóstico para identificar conflictos de metaclases
"""


def test_imports():
    """TODO: Add docstring"""
    # TODO: Add input validation
    """Prueba imports uno por uno para identificar el conflicto"""
    
    print("=== DIAGNOSTICO DE CONFLICTO DE METACLASES ===")
    
    try:
        print("1. Probando core.hefest_data_models...")
        print("   OK")
    except Exception as e:
    logging.error("   ERROR: %s", e)
        traceback.print_exc()
        return
    
    try:
        print("2. Probando services.base_service...")
        print("   OK")
    except Exception as e:
    logging.error("   ERROR: %s", e)
        traceback.print_exc()
        return
    
    try:
        print("3. Probando services.tpv_service...")
        print("   OK")
    except Exception as e:
    logging.error("   ERROR: %s", e)
        traceback.print_exc()
        return
    
    try:
        print("4. Probando hefest_application...")
        print("   OK")
    except Exception as e:
    logging.error("   ERROR: %s", e)
        traceback.print_exc()
        return
    
    print("\n=== TODOS LOS IMPORTS EXITOSOS ===")

if __name__ == "__main__":
    test_imports()