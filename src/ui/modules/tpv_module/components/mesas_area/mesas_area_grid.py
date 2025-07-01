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
    scroll_area.setStyleSheet("""
        QScrollArea {
            border: none;
            background-color: #fafbfc;
            border-radius: 8px;
        }
        QScrollBar:vertical {
            background-color: #f1f3f4;
            width: 12px;
            border-radius: 6px;
        }
        QScrollBar::handle:vertical {
            background-color: #bdc3c7;
            border-radius: 6px;
            margin: 2px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #95a5a6;
        }
    """)
    mesas_container = QWidget()
    mesas_container.setStyleSheet("""
        QWidget {
            background-color: #fafbfc;
            border-radius: 8px;
        }
    """)
    instance.mesas_layout = QGridLayout(mesas_container)
    instance.mesas_layout.setSpacing(20)
    instance.mesas_layout.setContentsMargins(20, 20, 20, 20)
    instance.mesas_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
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
                instance.mesa_widgets.append(mesa_widget)
                instance.mesas_layout.addWidget(mesa_widget, row, col)
            instance._lazy_loaded_rows.add(row)
    # Conectar el evento de scroll para lazy loading
    def on_scroll():
        QTimer.singleShot(10, lazy_load_rows)
    scroll = instance.scroll_area.verticalScrollBar()
    if scroll:
        scroll.valueChanged.connect(on_scroll)
    lazy_load_rows()
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
        message_container = QFrame()
        message_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border: 2px dashed #dee2e6;
                border-radius: 16px;
                padding: 30px;
                margin: 20px;
            }
        """)
        container_layout = QVBoxLayout(message_container)
        container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.setSpacing(16)
        icon_label = QLabel("🔍")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px; color: #6c757d; margin: 10px;")
        container_layout.addWidget(icon_label)
        title_label = QLabel("No se encontraron mesas")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #495057; margin: 8px;")
        container_layout.addWidget(title_label)
        subtitle_label = QLabel("No hay mesas que coincidan con los filtros aplicados")
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("font-size: 14px; color: #6c757d; margin: 4px;")
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

# ...migrar helpers de grid y lógica de renderizado aquí...
