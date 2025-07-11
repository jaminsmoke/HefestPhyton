#!/usr/bin/env python3
"""Script simple para probar las herramientas de linting individualmente."""

# Archivo con errores intencionados para pruebas
import os  # unused import
import sys  # unused import


def bad_function(a, b, c, d, e, f, g, h, i):  # too many arguments, bad spacing
    x = 1  # unused variable
    very_long_line_that_definitely_exceeds_the_normal_line_length_limit_and_should_trigger_warnings = (
        "test"  # line too long
    )
    print(undefined_var)  # undefined variable
    return None  # useless return


class Empty:  # empty class
    pass


def no_docs():  # missing docstring
    pass
