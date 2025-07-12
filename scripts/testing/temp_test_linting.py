#!/usr/bin/env python3
"""Archivo de prueba para verificar herramientas de linting."""

import os
import sys
import unused_module  # Error: import no usado

def function_with_errors(arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9):  # Error: demasiados argumentos
    """Función con errores intencionados."""
    variable_not_used = "test"  # Warning: variable no usada
    very_long_line_that_exceeds_the_maximum_length_limit_and_should_trigger_a_warning_from_flake8_and_pylint_tools = "error"  # Error: línea muy larga
    
    if True:
        if True:
            if True:
                if True:
                    if True:  # Error: demasiada complejidad
                        print("Nested too deep")
    
    # Error: variable no definida
    print(undefined_variable)
    
    return None

# Error: clase sin métodos
class EmptyClass:
    pass

# Error: función sin documentación
def undocumented_function():
    pass
