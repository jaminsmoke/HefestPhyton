"""
mesas_area_header.py
Componentes de header, filtros y estadísticas para MesasArea
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton, QLineEdit, QMenu
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

def create_title_section_ultra_premium():
    section = QFrame()
    section.setObjectName("TitleSectionUltraPremium")
    section.setFixedSize(260, 75)
    section.setStyleSheet("""
        QFrame#TitleSectionUltraPremium {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #ffffff,
                stop:0.3 #fafbfc,
                stop:0.7 #f6f8fa,
                stop:1 #f1f4f8);
            border: 2px solid #e2e8f0;
            border-radius: 16px;
            margin: 3px;                padding: 2px;
        }
        QFrame#TitleSectionUltraPremium:hover {
            border: 2px solid #cbd5e1;
        }        """)
    layout = QHBoxLayout(section)
    layout.setContentsMargins(12, 6, 12, 6)
    layout.setSpacing(10)
    icon_container = QFrame()
    icon_container.setFixedSize(52, 52)
    icon_container.setStyleSheet("""
        QFrame {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #5b21b6,
                stop:0.3 #4c1d95,
                stop:0.7 #3730a3,
                stop:1 #312e81);
            border: 2px solid #1e1b4b;
            border-radius: 26px;
        }
    """)
    icon_layout = QVBoxLayout(icon_container)
    icon_layout.setContentsMargins(0, 0, 0, 0)
    icon_label = QLabel("🍽️")
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    icon_label.setStyleSheet("""
        QLabel {
            font-size: 20px;
            color: white;
            background: transparent;
            border: none;
        }        """)
    icon_layout.addWidget(icon_label)
    layout.addWidget(icon_container)
    text_container = QVBoxLayout()
    text_container.setSpacing(1)
    text_container.setContentsMargins(0, 0, 0, 0)
    title_label = QLabel("GESTIÓN DE MESAS")
    title_label.setStyleSheet("""
        QLabel {
            font-size: 14px;
            font-weight: bold;
            color: #1e293b;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            letter-spacing: 0.3px;
            margin: 0px;
            padding: 0px;
            line-height: 1.1;
        }
    """)
    text_container.addWidget(title_label)
    subtitle_label = QLabel("Terminal Punto de Venta")
    subtitle_label.setStyleSheet("""
        QLabel {
            font-size: 11px;
            color: #64748b;
            font-weight: 500;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            margin: 0px;
            padding: 0px;
            line-height: 1.0;
        }
    """)
    text_container.addWidget(subtitle_label)
    text_container.addStretch()
    status_label = QLabel("● Sistema Activo")
    status_label.setStyleSheet("""
        QLabel {
            font-size: 10px;
            color: #16a34a;
            font-weight: bold;
            font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
            margin: 0px;
            padding: 0px;
            line-height: 1.0;
        }
    """)
    text_container.addWidget(status_label)
    layout.addLayout(text_container)
    layout.addStretch()
    return section

def create_ultra_premium_separator():
    sep = QFrame()
    sep.setFixedWidth(0)
    sep.setStyleSheet("background: transparent; border: none;")
    return sep

def create_filters_section_ultra_premium(instance):
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QComboBox, QPushButton, QLineEdit, QMenu, QSizePolicy
    from PyQt6.QtGui import QAction
    from PyQt6.QtCore import Qt
    section = QFrame()
    section.setObjectName("FiltersSectionUltraPremium")
    section.setStyleSheet("""
        QFrame#FiltersSectionUltraPremium {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #f0f9ff, stop:0.5 #e0f2fe, stop:1 #f0f9ff);
            border: 1.5px solid #0ea5e9;
            border-radius: 14px;
            padding: 10px 14px 12px 14px;
            margin: 4px;
        }
    """)
    layout = QVBoxLayout(section)
    layout.setContentsMargins(6, 2, 6, 2)
    layout.setSpacing(4)
    header_layout = QHBoxLayout()
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(0)
    section_title = QLabel("🔍 Filtros y Control")
    section_title.setStyleSheet("""
        QLabel {
            font-size: 12px;
            font-weight: bold;
            color: #0369a1;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #dbeafe, stop:1 #bfdbfe);
            border: 1px solid #93c5fd;
            border-radius: 8px;
            padding: 5px 14px;
            margin: 0px;
            letter-spacing: 0.5px;
        }
    """)
    header_layout.addWidget(section_title)
    header_layout.addStretch(1)
    layout.addLayout(header_layout)
    # --- Nuevo layout tipo grid para filtros y controles ---
    grid = QGridLayout()
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setHorizontalSpacing(16)
    grid.setVerticalSpacing(2)
    # Etiquetas elegantes con icono
    search_label = QLabel("<span style='font-size:12px;'>🔎</span> <span style='font-size:11px;font-weight:600;'>Buscar</span>")
    search_label.setStyleSheet("""
        QLabel {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e0f2fe, stop:1 #bae6fd);
            border: 1px solid #38bdf8;
            border-radius: 8px;
            padding: 3px 14px 3px 10px;
            color: #0369a1;
            font-family: 'Segoe UI', Arial, sans-serif;
            margin-bottom: 2px;
            min-width: 60px;
        }
    """)
    zone_label = QLabel("<span style='font-size:12px;'>🗺️</span> <span style='font-size:11px;font-weight:600;'>Zona</span>")
    zone_label.setStyleSheet("""
        QLabel {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e0f2fe, stop:1 #bae6fd);
            border: 1px solid #38bdf8;
            border-radius: 8px;
            padding: 3px 14px 3px 10px;
            color: #0369a1;
            font-family: 'Segoe UI', Arial, sans-serif;
            margin-bottom: 2px;
            min-width: 50px;
        }
    """)
    status_label = QLabel("<span style='font-size:12px;'>📊</span> <span style='font-size:11px;font-weight:600;'>Estado</span>")
    status_label.setStyleSheet("""
        QLabel {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #e0f2fe, stop:1 #bae6fd);
            border: 1px solid #38bdf8;
            border-radius: 8px;
            padding: 3px 14px 3px 10px;
            color: #0369a1;
            font-family: 'Segoe UI', Arial, sans-serif;
            margin-bottom: 2px;
            min-width: 50px;
        }
    """)
    # Campos
    search_input = QLineEdit()
    search_input.setPlaceholderText("Buscar mesa o zona...")
    search_input.setMinimumWidth(0)
    search_input.setMaximumWidth(16777215)
    search_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    search_input.setStyleSheet("""
        QLineEdit {
            border: 1.5px solid #38bdf8;
            border-radius: 7px;
            padding: 6px 10px;
            font-size: 12px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f0f9ff, stop:1 #e0f2fe);
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QLineEdit:focus {
            border-color: #2563eb;
            background: #f8fafc;
        }
    """)
    search_input.textChanged.connect(instance._on_search_changed)
    instance.set_search_input(search_input)
    zone_combo = QComboBox()
    zone_combo.addItems(["Todas", "Terraza", "Interior", "Privada", "Barra"])
    zone_combo.setFixedWidth(100)
    zone_combo.setStyleSheet("""
        QComboBox {
            border: 1.5px solid #38bdf8;
            border-radius: 7px;
            padding: 6px 10px;
            font-size: 12px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f0f9ff, stop:1 #e0f2fe);
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QComboBox:focus {
            border-color: #2563eb;
            background: #f8fafc;
        }
        QComboBox::drop-down {
            border: none;
            width: 20px;
            background: #f1f5f9;
            border-top-right-radius: 7px;
            border-bottom-right-radius: 7px;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid #0ea5e9;
            margin-right: 4px;
        }
    """)
    zone_combo.currentTextChanged.connect(instance._on_zone_changed)
    instance.set_zone_combo(zone_combo)
    status_combo = QComboBox()
    status_combo.addItems(["Todos", "Libre", "Ocupada", "Reservada"])
    status_combo.setFixedWidth(100)
    status_combo.setStyleSheet("""
        QComboBox {
            border: 1.5px solid #38bdf8;
            border-radius: 7px;
            padding: 6px 10px;
            font-size: 12px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f0f9ff, stop:1 #e0f2fe);
            font-family: 'Segoe UI', Arial, sans-serif;
        }
        QComboBox:focus {
            border-color: #2563eb;
            background: #f8fafc;
        }
        QComboBox::drop-down {
            border: none;
            width: 20px;
            background: #f1f5f9;
            border-top-right-radius: 7px;
            border-bottom-right-radius: 7px;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 6px solid #0ea5e9;
            margin-right: 4px;
        }
    """)
    status_combo.currentTextChanged.connect(instance._on_status_changed)
    instance.set_status_combo(status_combo)
    # Botón Gestionar
    acciones_btn = QPushButton("Gestionar ▼")
    acciones_btn.setFixedWidth(110)
    acciones_btn.setStyleSheet("""
        QPushButton {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #10b981, stop:1 #059669);
            color: white;
            border: 1.5px solid #047857;
            border-radius: 7px;
            padding: 7px 10px;
            font-size: 12px;
            font-weight: bold;
            font-family: 'Segoe UI', Arial, sans-serif;
            text-align: left;
        }
        QPushButton:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #059669, stop:1 #047857);
        }
    """)
    menu_acciones = QMenu(acciones_btn)
    menu_acciones.setStyleSheet("""
        QMenu {
            background-color: white;
            border: 2px solid #10b981;
            border-radius: 8px;
            padding: 4px;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 12px;
        }
        QMenu::item {
            background-color: transparent;
            padding: 8px 16px;
            margin: 2px;
            border-radius: 4px;
            color: #374151;
        }
        QMenu::item:selected {
            background-color: #10b981;
            color: white;
        }
    """)
    accion_nueva = QAction("➕ Nueva Mesa", menu_acciones)
    accion_nueva.setToolTip("Crear una nueva mesa")
    accion_nueva.triggered.connect(instance._on_nueva_mesa_clicked)
    menu_acciones.addAction(accion_nueva)
    menu_acciones.addSeparator()
    accion_eliminar = QAction("🗑️ Eliminar Mesa", menu_acciones)
    accion_eliminar.setToolTip("Eliminar una mesa existente")
    accion_eliminar.triggered.connect(instance._on_eliminar_mesa_clicked)
    menu_acciones.addAction(accion_eliminar)
    acciones_btn.setMenu(menu_acciones)
    # Botón Refrescar
    refresh_btn = QPushButton("⟳")
    refresh_btn.setFixedSize(36, 32)
    refresh_btn.setStyleSheet("""
        QPushButton {
            border: 1.5px solid #60a5fa;
            border-radius: 7px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #f0f9ff, stop:1 #e0f2fe);
            font-size: 16px;
            color: #2563eb;
            font-weight: bold;
        }
        QPushButton:hover {
            background: #e0f2fe;
            border-color: #2563eb;
        }
    """)
    refresh_btn.clicked.connect(instance.refresh_mesas)
    refresh_btn.setToolTip("Actualizar vista de mesas")
    # --- Añadir al grid ---
    # Etiquetas en la fila 0
    grid.addWidget(search_label, 0, 0)
    grid.addWidget(zone_label, 0, 1)
    grid.addWidget(status_label, 0, 2)
    # Campos en la fila 1
    grid.addWidget(search_input, 1, 0)
    grid.addWidget(zone_combo, 1, 1)
    grid.addWidget(status_combo, 1, 2)
    grid.addWidget(acciones_btn, 1, 3)
    grid.addWidget(refresh_btn, 1, 4)
    grid.setColumnStretch(0, 6)
    grid.setColumnStretch(1, 1)
    grid.setColumnStretch(2, 1)
    grid.setColumnStretch(3, 0)
    grid.setColumnStretch(4, 0)
    layout.addLayout(grid)
    return section

def create_stats_section_ultra_premium(instance):
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QGridLayout
    section = QFrame()
    section.setObjectName("StatsSectionUltraPremium")
    section.setStyleSheet("""
        QFrame#StatsSectionUltraPremium {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #fef7ff, stop:0.5 #fdf4ff, stop:1 #fef7ff);
            border: 1.5px solid #d946ef;
            border-radius: 14px;
            padding: 2px 8px 32px 8px; /* Más padding inferior */
            margin: 2px 0 8px 0;
            min-height: 160px; /* Más alto para igualar azul */
        }
    """)
    layout = QVBoxLayout(section)
    layout.setContentsMargins(4, 2, 4, 4)
    layout.setSpacing(2)
    title_row = QHBoxLayout()
    title_label = QLabel("<span style='font-size:11px; font-weight:600; color:#a21caf; vertical-align:middle;'>📊 Estadísticas en Tiempo Real</span>")
    title_label.setStyleSheet("background: #f3e8ff; border-radius: 6px; padding: 1px 10px 1px 6px; border: 1px solid #d946ef; margin-bottom: 0px;")
    title_row.addWidget(title_label, 0, Qt.AlignmentFlag.AlignLeft)
    title_row.addStretch(1)
    layout.addLayout(title_row)
    grid = QGridLayout()
    grid.setSpacing(12)
    grid.setContentsMargins(0, 0, 0, 0)
    grid.setAlignment(Qt.AlignmentFlag.AlignTop)
    # Asignar widgets premium SIEMPRE a instance
    instance.zonas_widget = create_ultra_premium_stat("📍", "Zonas", "0", "#8b5cf6", "#f3e8ff", size=110, height=110)
    instance.mesas_total_widget = create_ultra_premium_stat("🍽️", "Total", "0", "#3b82f6", "#dbeafe", size=110, height=110)
    instance.mesas_libres_widget = create_ultra_premium_stat("🟢", "Libres", "0", "#22c55e", "#dcfce7", size=110, height=110)
    instance.mesas_ocupadas_widget = create_ultra_premium_stat("🔴", "Ocupadas", "0", "#ef4444", "#fee2e2", size=110, height=110)
    instance.mesas_reservadas_widget = create_ultra_premium_stat("📅", "Reservadas", "0", "#f59e0b", "#fef3c7", size=110, height=110)
    grid.addWidget(instance.zonas_widget, 0, 0)
    grid.addWidget(instance.mesas_total_widget, 0, 1)
    grid.addWidget(instance.mesas_libres_widget, 0, 2)
    grid.addWidget(instance.mesas_ocupadas_widget, 0, 3)
    grid.addWidget(instance.mesas_reservadas_widget, 0, 4)
    layout.addLayout(grid)
    return section

def create_ultra_premium_stat(icon: str, label: str, value: str, color: str, bg_color: str, size: int = 80, height: int = 80):
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
    stat_widget.value_label = value_widget  # Guardar referencia para actualización
    return stat_widget

def update_ultra_premium_stats_ui(instance, zonas, total, libres, ocupadas, reservadas):
    """Actualiza los valores de las tarjetas premium del header (solo UI, sin lógica de cálculo)"""
    if hasattr(instance, 'zonas_widget') and hasattr(instance.zonas_widget, 'value_label'):
        instance.zonas_widget.value_label.setText(str(zonas))
    if hasattr(instance, 'mesas_total_widget') and hasattr(instance.mesas_total_widget, 'value_label'):
        instance.mesas_total_widget.value_label.setText(str(total))
    if hasattr(instance, 'mesas_libres_widget') and hasattr(instance.mesas_libres_widget, 'value_label'):
        instance.mesas_libres_widget.value_label.setText(str(libres))
    if hasattr(instance, 'mesas_ocupadas_widget') and hasattr(instance.mesas_ocupadas_widget, 'value_label'):
        instance.mesas_ocupadas_widget.value_label.setText(str(ocupadas))
    if hasattr(instance, 'mesas_reservadas_widget') and hasattr(instance.mesas_reservadas_widget, 'value_label'):
        instance.mesas_reservadas_widget.value_label.setText(str(reservadas))
    # Forzar actualización visual
    for attr in ["zonas_widget", "mesas_total_widget", "mesas_libres_widget", "mesas_ocupadas_widget", "mesas_reservadas_widget"]:
        widget = getattr(instance, attr, None)
        if widget:
            widget.update()
            widget.repaint()

def create_header(parent, instance, layout):
    from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSizePolicy
    # Contenedor principal del header
    header_container = QFrame()
    header_container.setObjectName("HeaderContainerUltraPremium")
    header_container.setStyleSheet("""
        QFrame#HeaderContainerUltraPremium {
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #fefefe,
                stop:0.2 #fdfdfd,
                stop:0.8 #f9fafb,
                stop:1 #f3f4f6);
            border: 2px solid;
            border-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #e5e7eb, stop:0.5 #d1d5db, stop:1 #e5e7eb);
            border-radius: 16px;
            margin: 2px;
        }
    """)
    header_layout = QHBoxLayout(header_container)
    header_layout.setContentsMargins(24, 16, 24, 16)
    header_layout.setSpacing(8)  # Reducir el spacing entre azul y rosa
    # Sección izquierda: solo título y estado
    left_section = QVBoxLayout()
    left_section.setSpacing(8)
    title_status_container = create_title_section_ultra_premium()
    left_section.addWidget(title_status_container)
    header_layout.addLayout(left_section, 0)
    # Separador
    separator1 = create_ultra_premium_separator()
    header_layout.addWidget(separator1, 0)
    # Sección central: filtros y control
    filters_container = create_filters_section_ultra_premium(instance)
    filters_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    header_layout.addWidget(filters_container, 4)  # Más stretch para el azul
    # Separador
    separator2 = create_ultra_premium_separator()
    header_layout.addWidget(separator2, 0)
    # Sección derecha: estadísticas premium
    right_section = QVBoxLayout()
    right_section.setSpacing(8)
    stats_container = create_stats_section_ultra_premium(instance)
    right_section.addWidget(stats_container)
    header_layout.addLayout(right_section, 2)  # Menos stretch para el rosa
    layout.addWidget(header_container)
    return header_container
