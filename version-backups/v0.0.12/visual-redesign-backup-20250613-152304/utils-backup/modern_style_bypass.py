"""
Sistema de BYPASS para filtro CSS - Permite estilos modernos selectivos
"""

import logging
from PyQt6.QtCore import QObject

logger = logging.getLogger(__name__)

class ModernStyleBypass:
    """Sistema para bypass del filtro CSS agresivo"""
    
    # Lista de widgets que deben mantener estilos modernos
    _bypass_widgets = set()
    
    @classmethod
    def register_modern_widget(cls, widget):
        """Registra un widget para bypass del filtro CSS"""
        widget_id = id(widget)
        cls._bypass_widgets.add(widget_id)
        
        # Marcar con propiedad para identificación
        widget.setProperty("modern_style_bypass", True)
        
        logger.debug(f"Widget {widget} registrado para bypass de filtro CSS")
    
    @classmethod
    def unregister_modern_widget(cls, widget):
        """Desregistra un widget del bypass"""
        widget_id = id(widget)
        cls._bypass_widgets.discard(widget_id)
        widget.setProperty("modern_style_bypass", False)
    
    @classmethod
    def should_bypass(cls, widget):
        """Verifica si un widget debe evitar el filtro CSS"""
        # Verificar por ID
        widget_id = id(widget)
        if widget_id in cls._bypass_widgets:
            return True
            
        # Verificar por propiedad
        if hasattr(widget, 'property'):
            bypass_prop = widget.property("modern_style_bypass")
            if bypass_prop:
                return True
        
        # Verificar por clase padre
        widget_class = widget.__class__.__name__
        bypass_classes = [
            'AdvancedMetricCardModern', 
            'ModernDashboard', 
            'SophisticatedCard'
        ]
        
        for bypass_class in bypass_classes:
            if bypass_class in widget_class:
                return True
                
        return False
    
    @classmethod
    def apply_modern_style_safe(cls, widget, stylesheet):
        """Aplica estilo moderno de forma segura, evitando filtros"""
        # Registrar para bypass
        cls.register_modern_widget(widget)
        
        # Aplicar estilo
        widget.setStyleSheet(stylesheet)
        
        logger.debug(f"Estilo moderno aplicado a {widget.__class__.__name__}")

# Función para parchear el filtro existente
def patch_existing_filter():
    """Parchea el filtro CSS existente para respetar bypasses"""
    from utils.qt_css_compat import StylesheetFilter
    
    # Guardar método original
    if not hasattr(StylesheetFilter, '_original_eventFilter'):
        StylesheetFilter._original_eventFilter = StylesheetFilter.eventFilter
    
    def patched_eventFilter(self, obj, event):
        """Version parcheada que respeta bypasses"""
        
        # Si el widget tiene bypass, no filtrar
        if ModernStyleBypass.should_bypass(obj):
            return False  # Permitir estilos modernos
            
        # Para otros widgets, usar filtro original
        return self._original_eventFilter(obj, event)
    
    # Reemplazar método
    StylesheetFilter.eventFilter = patched_eventFilter
    logger.info("Filtro CSS parcheado para respetar bypasses modernos")

# Auto-aplicar parche al importar
try:
    patch_existing_filter()
    logger.info("Sistema de bypass moderno activado")
except Exception as e:
    logger.warning(f"No se pudo aplicar parche de bypass: {e}")

# Decorador para widgets modernos
def modern_widget(cls):
    """Decorador para marcar clases como widgets modernos"""
    
    original_init = cls.__init__
    
    def modern_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        # Auto-registrar para bypass
        ModernStyleBypass.register_modern_widget(self)
    
    cls.__init__ = modern_init
    return cls
