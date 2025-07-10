from typing import Optional, Dict, List, Any
#!/usr/bin/env python3
"""
Fix para el sistema responsivo del alias en MesaWidget
"""

# Método simplificado y robusto para reemplazar el complejo _ajustar_fuente_nombre

def _ajustar_fuente_nombre_nuevo(self):
    """Sistema responsivo y robusto para el alias de mesa"""
    from PyQt6.QtGui import QFont
    from PyQt6.QtCore import Qt
    
    _ = self.alias_label
    alias = self.mesa.alias if self.mesa.alias else self.mesa.nombre_display
    
    # Configurar word wrap
    label.setWordWrap(True)
    
    # Calcular ancho disponible
    _ = self.width()
    btns_width = 0
    if hasattr(self, 'edit_btn') and self.edit_btn.isVisible():
        btns_width += self.edit_btn.width() + 6
    if hasattr(self, 'restore_btn') and self.restore_btn.isVisible():
        btns_width += self.restore_btn.width() + 6
    
    _ = max(parent_width - btns_width - 24, 80)
    
    # Configurar fuente base
    _ = 9
    max_font_size = 18
    
    # Buscar el tamaño de fuente óptimo
    _ = min_font_size
    
    for font_size in range(max_font_size, min_font_size - 1, -1):
        font = QFont("Segoe UI", font_size, QFont.Weight.Bold)
        label.setFont(font)
        
        # Configurar el texto y medir
        label.setText(alias)
        label.adjustSize()
        
        # Si cabe en el ancho disponible, usar este tamaño
        if label.width() <= available_width:
            _ = font_size
            break
    
    # Aplicar la fuente óptima
    final_font = QFont("Segoe UI", optimal_size, QFont.Weight.Bold)
    label.setFont(final_font)
    label.setText(alias)
    
    # Si el texto sigue siendo muy largo, usar elipsis
    if label.width() > available_width:
        metrics = label.fontMetrics()
        elided_text = metrics.elidedText(alias, Qt.TextElideMode.ElideRight, available_width)
        label.setText(elided_text)
        label.setToolTip(alias)  # Mostrar texto completo en tooltip
    else:
        label.setToolTip("")  # Sin tooltip si no hay elipsis
    
    # Actualizar geometría
    label.adjustSize()
    
    # Si estamos en modo edición, aplicar la misma fuente al editor
    if self.editing_mode and self.alias_line_edit:
        self.alias_line_edit.setFont(final_font)

print("Método simplificado creado. Para aplicarlo:")
print("1. Reemplaza todo el método _ajustar_fuente_nombre en mesa_widget_simple.py")
print("2. Con el código de la función _ajustar_fuente_nombre_nuevo de este archivo")