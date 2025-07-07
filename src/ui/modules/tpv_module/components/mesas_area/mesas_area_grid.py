"""
mesas_area_grid.py
Lógica y helpers para el grid de mesas y renderizado de widgets
"""

from PyQt6.QtWidgets import QGridLayout, QWidget, QLabel, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt

def create_scroll_area(instance, layout):
    from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout
    from PyQt6.QtCore import Qt
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    from src.utils.modern_styles import ModernStyles
    scroll_area.setStyleSheet(ModernStyles.get_scroll_area_style())
    mesas_container = QWidget()
    mesas_container.setStyleSheet(ModernStyles.get_mesas_container_style())
    instance.mesas_layout = QGridLayout(mesas_container)
    instance.mesas_layout.setSpacing(20)
    instance.mesas_layout.setContentsMargins(20, 20, 20, 20)
    # Centrar el grid de mesas horizontalmente y mantener alineado arriba
    instance.mesas_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    scroll_area.setWidget(mesas_container)
    layout.addWidget(scroll_area, 1)
    instance.scroll_area = scroll_area
    return scroll_area

def populate_grid(instance):
    from ...widgets.mesa_widget_simple import MesaWidget
    from .mesas_area_utils import restaurar_datos_temporales, calcular_columnas_optimas
    from PyQt6.QtCore import QTimer
    restaurar_datos_temporales(instance, instance.filtered_mesas)
    clear_mesa_widgets(instance)
    instance.mesa_widgets = []
    if not instance.filtered_mesas:
        show_no_mesas_message(instance)
        return
    cols = calcular_columnas_optimas(instance.width(), len(instance.filtered_mesas))
    instance._lazy_loaded_rows = set()
    instance._total_rows = (len(instance.filtered_mesas) + cols - 1) // cols
    instance._cols = cols
    # Crear widgets solo para las filas visibles inicialmente
    def get_visible_rows():
        scroll = instance.scroll_area.verticalScrollBar()
        if not scroll:
            return set(range(min(4, instance._total_rows)))
        viewport_height = instance.scroll_area.viewport().height()
        row_height = 180  # Aproximado, depende del widget
        first_row = max(0, scroll.value() // row_height - 1)
        last_row = min(instance._total_rows, (scroll.value() + viewport_height) // row_height + 2)
        return set(range(first_row, last_row))
    def lazy_load_rows():
        visible_rows = get_visible_rows()
        for row in visible_rows:
            if row in instance._lazy_loaded_rows:
                continue
            for col in range(cols):
                idx = row * cols + col
                if idx >= len(instance.filtered_mesas):
                    break
                mesa = instance.filtered_mesas[idx]
                mesa_widget = MesaWidget(mesa, proxima_reserva=getattr(mesa, 'proxima_reserva', None))
                mesa_widget.personas_changed.connect(instance._on_personas_mesa_changed)
                mesa_widget.restaurar_original.connect(instance.restaurar_estado_original_mesa)
                mesa_widget.reservar_mesa_requested.connect(instance._on_reservar_mesa)
                mesa_widget.iniciar_tpv_requested.connect(instance._on_iniciar_tpv)
                instance.mesa_widgets.append(mesa_widget)
                instance.mesas_layout.addWidget(mesa_widget, row, col)
            instance._lazy_loaded_rows.add(row)
    # Conectar el evento de scroll para lazy loading
    from PyQt6.QtCore import QTimer
    def on_scroll():
        QTimer.singleShot(10, lazy_load_rows)
    scroll = instance.scroll_area.verticalScrollBar()
    if scroll:
        scroll.valueChanged.connect(on_scroll)
    lazy_load_rows()

# Métodos para conectar en la instancia (por ejemplo, en la clase del área de mesas)
def add_mesa_grid_callbacks_to_instance(instance):
    def _on_reservar_mesa(mesa):
        try:
            from src.ui.modules.tpv_module.dialogs.reserva_dialog import ReservaDialog
            dialog = ReservaDialog(instance, mesa)
            dialog.exec()
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error abriendo ReservaDialog: {e}")

    def _on_iniciar_tpv(mesa):
        try:
            from src.ui.modules.tpv_module.components.tpv_avanzado.tpv_avanzado_main import TPVAvanzado
            from PyQt6.QtWidgets import QDialog, QVBoxLayout
            class TPVDialog(QDialog):
                def __init__(self, mesa, parent=None):
                    super().__init__(parent)
                    self.setWindowTitle(f"TPV Avanzado - Mesa {mesa.numero}")
                    self.setMinimumSize(900, 600)
                    layout = QVBoxLayout(self)
                    self.tpv_widget = TPVAvanzado(mesa, parent=self)
                    layout.addWidget(self.tpv_widget)
            dialog = TPVDialog(mesa, instance)
            dialog.exec()
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Error abriendo TPV Avanzado: {e}")

    instance._on_reservar_mesa = _on_reservar_mesa
    instance._on_iniciar_tpv = _on_iniciar_tpv
    # ...existing code...

    # REFRESCO GLOBAL: Forzar el estilo correcto en todos los widgets de mesa
    # Esto garantiza que todos los labels se vean correctamente desde el inicio
    # sin necesidad de interacción previa (click, cerrar diálogo, etc.)
    from PyQt6.QtCore import QTimer
    def aplicar_refresco_global():
        refresh_all_mesa_widgets_styles(instance)

    # Usar QTimer para ejecutar el refresco después de que se hayan renderizado completamente
    QTimer.singleShot(50, aplicar_refresco_global)

    total_filtered = len(instance.filtered_mesas)
    total_all = len(instance.mesas)
    if hasattr(instance, 'status_info'):
        if total_filtered == total_all:
            status_text = f"Mostrando {total_all} mesa(s)"
        else:
            status_text = f"Mostrando {total_filtered} de {total_all} mesa(s)"
        instance.status_info.setText(status_text)

def clear_mesa_widgets(instance):
    try:
        if not hasattr(instance, 'mesas_layout') or instance.mesas_layout is None:
            return
        instance.mesa_widgets.clear()
        while instance.mesas_layout.count():
            child = instance.mesas_layout.takeAt(0)
            if child and child.widget():
                widget = child.widget()
                if widget:
                    widget.deleteLater()
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error limpiando widgets de mesa: {e}")

def show_no_mesas_message(instance):
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
    try:
        if not hasattr(instance, 'mesas_layout') or instance.mesas_layout is None:
            return
        message_container = QFrame()
        from src.utils.modern_styles import ModernStyles
        message_container.setStyleSheet(ModernStyles.get_empty_message_frame_style())
        container_layout = QVBoxLayout(message_container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.setSpacing(16)
        icon_label = QLabel("🔍")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet(ModernStyles.get_icon_label_style())
        container_layout.addWidget(icon_label)
        title_label = QLabel("No se encontraron mesas")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(ModernStyles.get_title_label_style())
        container_layout.addWidget(title_label)
        subtitle_label = QLabel("No hay mesas que coincidan con los filtros aplicados")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet(ModernStyles.get_subtitle_label_style())
        container_layout.addWidget(subtitle_label)
        instance.mesas_layout.addWidget(message_container, 0, 0, 1, 4)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Error mostrando mensaje de no mesas: {e}")

def create_mesas_grid(parent, mesas):
    # Lógica migrada para crear el grid de mesas
    grid_widget = QWidget(parent)
    layout = QGridLayout(grid_widget)
    layout.setSpacing(20)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
    # ...agregar widgets de mesa aquí...
    return grid_widget

def refresh_all_mesa_widgets_styles(instance):
    """
    Refresca los estilos de todos los widgets de mesa existentes.
    Ejecuta _ajustar_fuente_nombre() en cada widget para garantizar que
    todos los labels tengan el estilo correcto desde el inicio.
    """
    for mesa_widget in instance.mesa_widgets:
        if hasattr(mesa_widget, '_ajustar_fuente_nombre'):
            try:
                mesa_widget._ajustar_fuente_nombre()
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Error refrescando estilo de mesa widget: {e}")
