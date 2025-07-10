"""
Utilidades para compatibilidad CSS en PyQt6
Este módulo proporciona funciones para transformar estilos CSS modernos
en equivalentes compatibles con PyQt6.
"""

import re
import logging
from typing import Optional, Any, Dict
from PyQt6.QtCore import QObject, QEvent
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


def convert_to_qt_compatible_css(css_code: Optional[str]) -> str:
    """
    Convierte propiedades CSS modernas a equivalentes compatibles con QSS (Qt Style Sheets)

    Args:
        css_code (str): Código CSS original con propiedades modernas

    Returns:
        str: CSS compatible con Qt
    """
    # Si el input es None, devolver cadena vacía
    if css_code is None:
        return ""
    # Crear un diccionario de reemplazos
    replacements = {
        # Transiciones (NO SOPORTADO en Qt)
        r"transition:\s*([^;]+);": "",
        r"transition-[^:]+:[^;]+;": "",
        # Sombras (NO SOPORTADO en Qt, se reemplaza por borde sutil)
        r"box-shadow:\s*([^;]+);": "border: 1px solid rgba(200,200,200,0.15);",
        # Filtros
        r"filter:\s*drop-shadow\([^)]+\);": "",
        r"filter:\s*([^;]+);": "",
        # Transformaciones
        r"transform:\s*([^;]+);": "",
        # Animaciones
        r"animation:\s*([^;]+);": "",
        r"@keyframes\s+[^{]+\{[^}]+\}": "",
        # Otras propiedades CSS3 no soportadas
        r"backdrop-filter:\s*([^;]+);": "",
        # Border-radius puede ser problemático en PyQt6, usar una versión simple
        r"border-radius:\s*([^;]+);": "border-radius: 4px;",
        # Algunos outline pueden causar problemas
        r"outline:\s*none;": "",
        r"outline:\s*([^;]+);": "",
        # Gradientes complejos pueden ser problemáticos
        r"background:\s*linear-gradient\([^)]+\);": "background-color: #f3f4f6;",
        r"background:\s*radial-gradient\([^)]+\);": "background-color: #f3f4f6;",
        # Text-shadow
        r"text-shadow:\s*([^;]+);": "",
    }

    result = css_code
    for pattern, replacement in replacements.items():
        result = re.sub(pattern, replacement, result)

    return result


def apply_qt_workarounds(widget: QWidget, style_class: str = "") -> QWidget:
    """
    Aplica workarounds para simular efectos modernos en Qt

    Args:
        widget (QWidget): Widget al que aplicar los workarounds
        style_class (str): Clase de estilo para aplicar efectos específicos
    """  # Si el estilo actual contiene propiedades no compatibles, convertirlo
    if hasattr(widget, "styleSheet") and callable(widget.styleSheet):  # type: ignore[misc]
        current_style = widget.styleSheet()  # type: ignore[misc]
        if current_style and isinstance(current_style, str):
            if (
                "transition" in current_style
                or "box-shadow" in current_style
                or "filter" in current_style
                or "border-radius" in current_style
                or "text-shadow" in current_style
                or "linear-gradient" in current_style
                or "radial-gradient" in current_style
            ):
                compatible_style = convert_to_qt_compatible_css(current_style)
                widget.setStyleSheet(compatible_style)  # type: ignore[misc]

    return widget


class StylesheetFilter(QObject):
    """
    Filtro de eventos global que intercepta y corrige los estilos CSS
    aplicados a cualquier widget en la aplicación.
    """

    def __init__(self, parent: Optional[QObject] = None) -> None:
        """Inicializa el filtro de eventos"""
        super().__init__(parent)
        self._filtered_stylesheets: Dict[str, str] = {}  # Cache para no procesar repetidamente

    def eventFilter(self, obj: Any, event: QEvent) -> bool:
        """Filtra eventos de cambio de estilo"""
        if event.type() == QEvent.Type.DynamicPropertyChange:
            prop_name = event.propertyName().data().decode()  # type: ignore[misc]
            if prop_name == "styleSheet":
                if hasattr(obj, "styleSheet") and callable(obj.styleSheet):  # type: ignore[misc]
                    stylesheet = obj.styleSheet()  # type: ignore[misc]
                    # Solo procesar si contiene propiedades no compatibles
                    if stylesheet and isinstance(stylesheet, str):
                        if (
                            "transition" in stylesheet
                            or "box-shadow" in stylesheet
                            or "filter" in stylesheet
                            or "border-radius" in stylesheet
                            or "text-shadow" in stylesheet
                            or "linear-gradient" in stylesheet
                            or "radial-gradient" in stylesheet
                        ):

                            # Usar cache si ya se procesó este stylesheet
                            if stylesheet in self._filtered_stylesheets:
                                compatible = self._filtered_stylesheets[stylesheet]
                            else:
                                compatible = convert_to_qt_compatible_css(stylesheet)
                                self._filtered_stylesheets[stylesheet] = compatible

                            # Aplicar stylesheet compatible
                            if compatible != stylesheet:
                                obj.setStyleSheet(compatible)  # type: ignore[misc]

        return False  # Siempre permitir que el evento se propague


def install_global_stylesheet_filter(app: Any) -> Any:
    """
    Instala un filtro de eventos global para interceptar y corregir
    todos los styleSheets aplicados en la aplicación.

    Args:
        app: La instancia de QApplication
    """
    # Crear e instalar filtro global
    style_filter = StylesheetFilter(app)
    app.installEventFilter(style_filter)
    logger.info("Filtro global de compatibilidad CSS instalado")
    return style_filter


def purge_modern_css_from_widget_tree(widget: Any) -> Any:
    """
    Limpia recursivamente todos los widgets en un árbol de widgets
    de propiedades CSS modernas no compatibles con PyQt6.

    Args:
        widget: El widget raíz desde el que comenzar la limpieza
    """  # Limpiar el stylesheet del widget actual
    if hasattr(widget, "styleSheet") and callable(widget.styleSheet):  # type: ignore[misc]
        current_style = widget.styleSheet()  # type: ignore[misc]
        if current_style and isinstance(current_style, str):
            if (
                "transition" in current_style
                or "box-shadow" in current_style
                or "filter" in current_style
                or "border-radius" in current_style
                or "text-shadow" in current_style
                or "linear-gradient" in current_style
                or "radial-gradient" in current_style
            ):
                compatible_style = convert_to_qt_compatible_css(current_style)
                widget.setStyleSheet(compatible_style)  # type: ignore[misc]

    # Procesar recursivamente todos los widgets hijos
    if hasattr(widget, "children"):
        for child in widget.children():
            if hasattr(child, "styleSheet"):
                purge_modern_css_from_widget_tree(child)

    return widget
