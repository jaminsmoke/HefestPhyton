"""
FloatingTabsDialog - Diálogo base con pestañas flotantes tipo libreta

Propósito: Componente reutilizable para formularios avanzados con navegación por pestañas flotantes
Ubicación: src/ui/components/FloatingTabsDialog.py
Dependencias: PyQt6
"""

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
from ..prototipos.libreta_tabs_flotantes import LibretaTabFlotante

class FloatingTabsDialog(QDialog):
    """Diálogo base reutilizable con pestañas flotantes externas"""
    def __init__(self, tab_configs, parent=None):
        super().__init__(parent)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.Window)
        self.setFixedSize(420, 600)
        self.tabs_flotantes = []
        self.current_index = 0
        self.tab_configs = tab_configs
        self.setup_ui()
        self.setup_floating_tabs()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget, 1)

    def setup_floating_tabs(self):
        tab_spacing = 38
        for i, (text, color) in enumerate(self.tab_configs):
            tab = LibretaTabFlotante(text, color, self)
            tab.clicked.connect(lambda idx=i: self.set_current_tab(idx))
            tab.setParent(None)
            tab.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
            tab.show()
            self.tabs_flotantes.append(tab)
        if self.tabs_flotantes:
            self.tabs_flotantes[0].set_active(True)
        self.update_floating_tabs_position(force=True)

    def moveEvent(self, event):
        super().moveEvent(event)
        self.update_floating_tabs_position()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_floating_tabs_position()

    def showEvent(self, event):
        super().showEvent(event)
        self.update_floating_tabs_position(force=True)

    def update_floating_tabs_position(self, force=False):
        if not self.tabs_flotantes:
            return
        dialog_pos = self.mapToGlobal(self.rect().topLeft())
        tab_offset_x = -90
        tab_offset_y = 52
        tab_spacing = 38
        for i, tab in enumerate(self.tabs_flotantes):
            tab_x = dialog_pos.x() + tab_offset_x
            tab_y = dialog_pos.y() + tab_offset_y + (i * tab_spacing)
            tab.move(tab_x, tab_y)

    def set_current_tab(self, index: int):
        if 0 <= index < len(self.tabs_flotantes):
            if self.current_index < len(self.tabs_flotantes):
                self.tabs_flotantes[self.current_index].set_active(False)
            self.current_index = index
            self.tabs_flotantes[index].set_active(True)
            self.stacked_widget.setCurrentIndex(index)

    def add_tab_page(self, widget):
        self.stacked_widget.addWidget(widget)
