#!/usr/bin/env python3
"""Script simple para probar las herramientas de linting individualmente."""


def test_function(a: int, b: int) -> int:
    """Función de prueba con parámetros limitados."""
    result = a + b
    print(f"Resultado: {result}")
    return result


class TestClass:
    """Clase de prueba con documentación."""
    
    def __init__(self) -> None:
        """Inicializar la clase de prueba."""
        self.value = 0
    
    def get_value(self) -> int:
        """Obtener el valor almacenado."""
        return self.value


def documented_function() -> None:
    """Función con documentación apropiada."""
    test_instance = TestClass()
    result = test_function(5, 3)
    print(f"Valor: {test_instance.get_value()}, Resultado: {result}")


if __name__ == "__main__":
    documented_function()
