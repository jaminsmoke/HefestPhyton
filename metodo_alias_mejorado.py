def _ajustar_fuente_nombre(self):
    """Sistema responsivo garantizando 25-30 caracteres visibles"""
    label = self.alias_label
    alias = self.mesa.alias if self.mesa.alias else self.mesa.nombre_display
    
    # Límites de caracteres garantizados
    MIN_CHARS = 25
    MAX_CHARS = 30
    
    # Calcular ancho disponible
    parent_width = self.width()
    btns_width = 0
    if hasattr(self, 'edit_btn') and self.edit_btn.isVisible():
        btns_width += self.edit_btn.width() + 6
    if hasattr(self, 'restore_btn') and self.restore_btn.isVisible():
        btns_width += self.restore_btn.width() + 6
    
    available_width = max(parent_width - btns_width - 24, 80)
    
    # Si el alias es muy largo, truncar con elipsis
    display_text = alias
    needs_tooltip = False
    
    if len(alias) > MAX_CHARS:
        display_text = alias[:MAX_CHARS] + "..."
        needs_tooltip = True
    
    # Configurar word wrap para textos largos
    label.setWordWrap(len(display_text) > 15)
    
    # Buscar tamaño de fuente que garantice visibilidad
    min_font_size = 8
    max_font_size = 18
    optimal_size = min_font_size
    
    for font_size in range(max_font_size, min_font_size - 1, -1):
        font = QFont("Segoe UI", font_size, QFont.Weight.Bold)
        label.setFont(font)
        label.setText(display_text)
        label.adjustSize()
        
        # Si cabe, usar este tamaño
        if label.width() <= available_width:
            optimal_size = font_size
            break
    
    # Aplicar fuente final
    final_font = QFont("Segoe UI", optimal_size, QFont.Weight.Bold)
    label.setFont(final_font)
    label.setText(display_text)
    
    # Si aún no cabe, usar elipsis de Qt
    if label.width() > available_width:
        metrics = label.fontMetrics()
        elided_text = metrics.elidedText(display_text, Qt.TextElideMode.ElideRight, available_width)
        label.setText(elided_text)
        needs_tooltip = True
    
    # Configurar tooltip
    if needs_tooltip or len(alias) > MAX_CHARS:
        label.setToolTip(alias)
    else:
        label.setToolTip("")
    
    # Actualizar geometría
    label.adjustSize()
    
    # Si estamos en modo edición, aplicar la misma fuente al editor
    if self.editing_mode and self.alias_line_edit:
        self.alias_line_edit.setFont(final_font)