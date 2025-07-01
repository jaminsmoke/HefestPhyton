"""
mesas_area_stats.py
Lógica de estadísticas y widgets de KPIs para MesasArea
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

def create_stats_section_ultra_premium(instance):
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
    from PyQt6.QtCore import Qt
    section = QFrame()
    section.setObjectName("StatsSectionUltraPremium")
    section.setStyleSheet("""
        QFrame#StatsSectionUltraPremium {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #fef7ff, stop:0.5 #fdf4ff, stop:1 #fef7ff);
            border: 1.5px solid #d946ef;
            border-radius: 14px;
            padding: 2px 8px 18px 8px;
            margin: 2px 0 8px 0;
            min-height: 120px;
        }
    """)
    layout = QVBoxLayout(section)
    layout.setContentsMargins(4, 2, 4, 4)
    layout.setSpacing(2)
    # Título compacto
    title_row = QHBoxLayout()
    title_label = QLabel("<span style='font-size:11px; font-weight:600; color:#a21caf; vertical-align:middle;'>📊 Estadísticas en Tiempo Real</span>")
    title_label.setStyleSheet("background: #f3e8ff; border-radius: 6px; padding: 1px 10px 1px 6px; border: 1px solid #d946ef; margin-bottom: 0px;")
    title_row.addWidget(title_label, 0, Qt.AlignmentFlag.AlignLeft)
    title_row.addStretch(1)
    layout.addLayout(title_row)
    # Grid de widgets premium
    grid = QGridLayout()
    grid.setSpacing(12)
    grid.setContentsMargins(0, 0, 0, 0)
    # Widgets premium (QFrame+QLabel) igual que en el original
    instance.zonas_widget = create_ultra_premium_stat("📍", "Zonas", "0", "#8b5cf6", "#f3e8ff", size=110, height=120)
    instance.mesas_total_widget = create_ultra_premium_stat("🍽️", "Total", "0", "#3b82f6", "#dbeafe", size=110, height=120)
    instance.mesas_libres_widget = create_ultra_premium_stat("🟢", "Libres", "0", "#22c55e", "#dcfce7", size=110, height=120)
    instance.mesas_ocupadas_widget = create_ultra_premium_stat("🔴", "Ocupadas", "0", "#ef4444", "#fee2e2", size=110, height=120)
    instance.mesas_reservadas_widget = create_ultra_premium_stat("📅", "Reservadas", "0", "#f59e0b", "#fef3c7", size=110, height=120)
    grid.addWidget(instance.zonas_widget, 0, 0)
    grid.addWidget(instance.mesas_total_widget, 0, 1)
    grid.addWidget(instance.mesas_libres_widget, 0, 2)
    grid.addWidget(instance.mesas_ocupadas_widget, 0, 3)
    grid.addWidget(instance.mesas_reservadas_widget, 0, 4)
    layout.addLayout(grid)
    return section

def create_ultra_premium_stat(icon, label, value, color, bg_color, size=80, height=80):
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
    from PyQt6.QtCore import Qt
    stat_widget = QFrame()
    stat_widget.setFixedSize(size, height)
    stat_widget.setStyleSheet(f"""
        QFrame {{
            background: {bg_color};
            border: 2px solid {color};
            border-radius: 14px;
            margin: 2px;
        }}
    """)
    layout = QVBoxLayout(stat_widget)
    layout.setContentsMargins(6, 10, 6, 8)
    layout.setSpacing(2)
    icon_container = QFrame()
    icon_container.setFixedHeight(36)
    icon_container.setStyleSheet("background: transparent; border: none;")
    icon_layout = QVBoxLayout(icon_container)
    icon_layout.setContentsMargins(0, 0, 0, 0)
    icon_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
    icon_label = QLabel(icon)
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    icon_label.setStyleSheet(f"font-size: 28px; color: {color}; line-height: 1.0;")
    icon_layout.addWidget(icon_label)
    layout.addWidget(icon_container)
    label_widget = QLabel(label)
    label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label_widget.setStyleSheet("font-size: 11px; color: #6b7280; font-weight: 600; margin: 2px 0;")
    layout.addWidget(label_widget)
    value_widget = QLabel(str(value))
    value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    value_widget.setStyleSheet(f"font-size: 20px; font-weight: bold; color: {color}; margin-top: 2px;")
    layout.addWidget(value_widget)
    return stat_widget

def _update_stat_widget(widget, new_value: str):
    """Actualiza SOLO el valor (tercer QLabel) de un widget de estadística ultra-premium"""
    try:
        if not widget or not hasattr(widget, 'layout') or not widget.layout():
            return
        layout = widget.layout()

        # Buscar específicamente el QLabel del valor (índice 2)
        if layout.count() >= 3:
            value_item = layout.itemAt(2)  # Tercer elemento = valor
            if value_item and value_item.widget() and isinstance(value_item.widget(), QLabel):
                value_label = value_item.widget()
                value_label.setText(str(new_value))
                value_label.update()
    except Exception:
        # (Eliminado print de error de debug)
        pass

def update_stats_from_mesas(instance):
    if not instance.mesas:
        update_ultra_premium_stats(instance)
        # Actualizar compactas a cero
        update_compact_stats(instance, 0, 0, 0, 0)
        return
    zonas_unicas = set(mesa.zona for mesa in instance.mesas)
    zonas_activas = len(zonas_unicas)
    total_mesas = len(instance.mesas)
    ocupadas = len([mesa for mesa in instance.mesas if mesa.estado == 'ocupada'])
    libres = total_mesas - ocupadas
    update_ultra_premium_stats(instance)
    update_compact_stats(instance, zonas_activas, total_mesas, libres, ocupadas)
    if hasattr(instance, 'status_info'):
        instance.status_info.setText(f"Mostrando {len(instance.filtered_mesas)} de {total_mesas} mesas")

def update_ultra_premium_stats(instance):
    if not hasattr(instance, 'mesas') or not instance.mesas:
        return
    total_mesas = len(instance.mesas)
    mesas_ocupadas = len([m for m in instance.mesas if hasattr(m, 'estado') and m.estado == 'ocupada'])
    mesas_libres = total_mesas - mesas_ocupadas
    mesas_reservadas = len([m for m in instance.mesas if hasattr(m, 'estado') and m.estado == 'reservada'])
    zonas_unicas = len(set(getattr(m, 'zona', 'Sin zona') for m in instance.mesas))

    # Usar _update_stat_widget para actualizar correctamente
    if hasattr(instance, 'mesas_ocupadas_widget'):
        _update_stat_widget(instance.mesas_ocupadas_widget, str(mesas_ocupadas))
    if hasattr(instance, 'mesas_total_widget'):
        _update_stat_widget(instance.mesas_total_widget, str(total_mesas))
    if hasattr(instance, 'mesas_libres_widget'):
        _update_stat_widget(instance.mesas_libres_widget, str(mesas_libres))
    if hasattr(instance, 'mesas_reservadas_widget'):
        _update_stat_widget(instance.mesas_reservadas_widget, str(mesas_reservadas))
    if hasattr(instance, 'zonas_widget'):
        _update_stat_widget(instance.zonas_widget, str(zonas_unicas))

def create_compact_stats(instance, layout):
    """Crea las estadísticas compactas integradas en el header (idéntico al original)"""
    from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout
    from PyQt6.QtGui import QFont
    # Separador visual antes de las estadísticas
    separator = QLabel("|")
    separator.setStyleSheet("color: #d1d5db; font-size: 14px; margin: 0px 8px;")
    layout.addWidget(separator)
    # Configuración de stats compactas
    stats_config = [
        ("📍", "Zonas", "0", "#10b981"),
        ("🍽️", "Total", "0", "#2563eb"),
        ("🟢", "Libres", "0", "#059669"),
        ("🔴", "Ocupadas", "0", "#dc2626")
    ]
    instance.compact_stats_widgets = []
    for icon, label, value, color in stats_config:
        stat_widget = create_compact_stat_widget(icon, label, value, color)
        instance.compact_stats_widgets.append({
            'widget': stat_widget,
            'type': label.lower(),
            'icon': icon,
            'label': label
        })
        layout.addWidget(stat_widget)

def create_compact_stat_widget(icon: str, label: str, value: str, color: str):
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
    from PyQt6.QtGui import QFont
    from PyQt6.QtCore import Qt
    stat_widget = QFrame()
    stat_widget.setFrameStyle(QFrame.Shape.StyledPanel)
    stat_widget.setLineWidth(1)
    layout = QVBoxLayout(stat_widget)
    layout.setContentsMargins(8, 4, 8, 4)
    layout.setSpacing(2)
    label_widget = QLabel(f"{icon} {label}")
    label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_font = QFont()
    title_font.setPointSize(8)
    title_font.setBold(False)
    label_widget.setFont(title_font)
    label_widget.setStyleSheet("color: #64748b; margin: 0px; padding: 0px;")
    layout.addWidget(label_widget)
    value_widget = QLabel(value)
    value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    value_font = QFont()
    value_font.setPointSize(14)
    value_font.setBold(True)
    value_widget.setFont(value_font)
    value_widget.setStyleSheet(f"color: {color}; margin: 0px; padding: 0px;")
    layout.addWidget(value_widget)
    stat_widget.setStyleSheet(f"""
        QFrame {{
            background-color: white;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            margin: 0px 2px;
        }}
        QFrame:hover {{
            border-color: {color};
        }}
    """)
    stat_widget.setFixedSize(65, 40)
    return stat_widget

def update_compact_stats(instance, zonas, total, libres, ocupadas):
    """Actualiza las estadísticas compactas en el header"""
    if not hasattr(instance, 'compact_stats_widgets'):
        return
    values = {
        'zonas': str(zonas),
        'total': str(total),
        'libres': str(libres),
        'ocupadas': str(ocupadas)
    }
    for stat_info in instance.compact_stats_widgets:
        widget = stat_info['widget']
        stat_type = stat_info['type']
        if stat_type in values:
            new_value = values[stat_type]
            layout = widget.layout()
            if layout and layout.count() >= 2:
                item = layout.itemAt(1)
                if item:
                    value_label = item.widget()
                    if isinstance(value_label, QLabel):
                        value_label.setText(new_value)
                        value_label.update()
            widget.update()
            widget.repaint()
