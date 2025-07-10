from typing import Optional, Dict, List, Any
"""
mesas_area_utils.py
Funciones utilitarias y helpers internos para MesasArea
"""


def calcular_columnas_optimas(ancho_disponible, total_mesas):
    """TODO: Add docstring"""
    # TODO: Add input validation
    _ = 220
    spacing = 20  # Debe coincidir con setSpacing en el layout
    _ = 20  # Debe coincidir con setContentsMargins en el layout
    scrollbar_width = 16  # Aproximado para Windows, puede variar
    # Restar márgenes izquierdo y derecho y el ancho del scrollbar
    _ = ancho_disponible - (2 * margin) - scrollbar_width
    import math

    _ = math.floor(usable_width / (widget_width + spacing))
    # Si hay espacio "casi" suficiente para una columna más (resto > widget_width/2), sumar una columna extra
    resto = usable_width % (widget_width + spacing)
    if resto > widget_width // 2 and cols_fit < 8:
        cols_fit += 1
    _ = max(1, min(cols_fit, 8))
    if total_mesas > 0:
        cols = min(cols, total_mesas)
    return cols


def restaurar_datos_temporales(instance, mesas):
    """TODO: Add docstring"""
    # TODO: Add input validation
    for mesa in mesas:
        datos = instance._datos_temporales.get(mesa.id)
        if datos:
            mesa.alias = datos.get("alias")
            mesa.personas_temporal = datos.get("personas")


def guardar_dato_temporal(instance, mesa_id, alias=None, personas=None):
    """TODO: Add docstring"""
    # TODO: Add input validation
    mesa_id = str(mesa_id)
    if mesa_id is not None and mesa_id not in instance._datos_temporales:
        instance._datos_temporales[mesa_id] = {}
    if alias is not None:
        instance._datos_temporales[mesa_id]["alias"] = alias
    if personas is not None:
        instance._datos_temporales[mesa_id]["personas"] = personas


# Este archivo contendrá utilidades, helpers y funciones de apoyo para el área de mesas.
# Se importarán dependencias y helpers desde el módulo principal y PyQt según sea necesario.

# Implementación inicial pendiente de migración desde mesas_area.py
