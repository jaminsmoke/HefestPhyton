"""
mesas_area_utils.py
Funciones utilitarias y helpers internos para MesasArea
"""

def calcular_columnas_optimas(ancho_disponible, total_mesas):
    widget_width = 220
    spacing = 15
    padding = 60
    usable_width = ancho_disponible - padding
    cols_fit = usable_width // (widget_width + spacing)
    cols = max(1, min(cols_fit, 8))
    if total_mesas > 0:
        if total_mesas <= 3:
            cols = min(cols, total_mesas)
        elif total_mesas <= 6:
            cols = min(cols, 3)
        elif total_mesas <= 12:
            cols = min(cols, 4)
    return cols

def restaurar_datos_temporales(instance, mesas):
    for mesa in mesas:
        datos = instance._datos_temporales.get(mesa.id)
        if datos:
            mesa.alias = datos.get('alias')
            mesa.personas_temporal = datos.get('personas')

def guardar_dato_temporal(instance, mesa_id, alias=None, personas=None):
    if mesa_id is not None and mesa_id not in instance._datos_temporales:
        instance._datos_temporales[mesa_id] = {}
    if alias is not None:
        instance._datos_temporales[mesa_id]['alias'] = alias
    if personas is not None:
        instance._datos_temporales[mesa_id]['personas'] = personas

# Este archivo contendrá utilidades, helpers y funciones de apoyo para el área de mesas.
# Se importarán dependencias y helpers desde el módulo principal y PyQt según sea necesario.

# Implementación inicial pendiente de migración desde mesas_area.py
