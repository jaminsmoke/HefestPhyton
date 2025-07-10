"""
mesas_area_utils.py
Funciones utilitarias y helpers internos para MesasArea
"""

import math
from typing import Any, Dict, List, Optional


def calcular_columnas_optimas(ancho_disponible: int, total_mesas: int) -> int:
    widget_width: int = 220
    spacing: int = 20  # Debe coincidir con setSpacing en el layout
    margin: int = 20  # Debe coincidir con setContentsMargins en el layout
    scrollbar_width: int = 16  # Aproximado para Windows, puede variar
    # Restar márgenes izquierdo y derecho y el ancho del scrollbar
    usable_width: int = ancho_disponible - (2 * margin) - scrollbar_width

    cols_fit: int = math.floor(usable_width / (widget_width + spacing))
    # Si hay espacio "casi" suficiente para una columna más
    resto: int = usable_width % (widget_width + spacing)
    if resto > widget_width // 2 and cols_fit < 8:
        cols_fit += 1
    cols: int = max(1, min(cols_fit, 8))
    if total_mesas > 0:
        cols = min(cols, total_mesas)
    return cols


def restaurar_datos_temporales(instance: Any, mesas: List[Any]) -> None:
    for mesa in mesas:
        datos: Optional[Dict[str, Any]] = instance._datos_temporales.get(
            mesa.id
        )  # type: ignore[misc]
        if datos:
            mesa.alias = datos.get("alias")  # type: ignore[misc]
            mesa.personas_temporal = datos.get("personas")  # type: ignore[misc]


def guardar_dato_temporal(
    instance: Any,
    mesa_id: Any,
    alias: Optional[str] = None,
    personas: Optional[int] = None,
) -> None:
    mesa_id = str(mesa_id)
    if (
        mesa_id is not None and mesa_id not in instance._datos_temporales
    ):  # type: ignore[misc]
        instance._datos_temporales[mesa_id] = {}  # type: ignore[misc]
    if alias is not None:
        instance._datos_temporales[mesa_id]["alias"] = alias  # type: ignore[misc]
    if personas is not None:
        instance._datos_temporales[mesa_id]["personas"] = personas  # type: ignore[misc]


# Este archivo contendrá utilidades y helpers para el área de mesas.

# Implementación inicial pendiente de migración desde mesas_area.py
