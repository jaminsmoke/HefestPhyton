"""
Estructura visual propuesta para tarjeta KPI avanzada (layout jerárquico y compacto):

┌─────────────────────────────────────────────┐
│                 [ ICONO ]                  │
│ ┌─────────────┬─────────────┬────────────┐ │
│ │   VALOR     │  TENDENCIA  │  BADGE     │ │
│ └─────────────┴─────────────┴────────────┘ │
│         [ MINI-GRÁFICA SPARKLINE ]         │
│                [ ETIQUETA ]                │
│                [ TOOLTIP ]                 │
│      [ ESTADO DE ACTUALIZACIÓN (esquina) ] │
└─────────────────────────────────────────────┘

Notas:
- El layout separa claramente cada zona: icono grande arriba, fila horizontal para valor/tendencia/badge, sparkline centrada, etiqueta secundaria, tooltip enriquecido y estado de actualización en esquina.
- El diseño permite máxima visibilidad y legibilidad de todos los elementos, y es fácilmente adaptable a estilos modernos.
- TODO: Implementar este layout visual en el widget real, ajustando los layouts y estilos de PyQt6 según este esquema.
"""
"""
mesas_area_stats.py
Lógica de estadísticas y widgets de KPIs para MesasArea
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

def create_subcontenedor_metric_cards(instance):
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
    from PyQt6.QtCore import Qt
    section = QFrame()
    section.setObjectName("SubContenedorMetricCards")
    section.setStyleSheet("""
        QFrame#SubContenedorMetricCards {
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
    from PyQt6.QtWidgets import QPushButton, QDialog, QVBoxLayout, QCheckBox, QDialogButtonBox, QHBoxLayout
    title_row = QHBoxLayout()
    title_label = QLabel("<span style='font-size:11px; font-weight:600; color:#a21caf; vertical-align:middle;'>📊 Estadísticas en Tiempo Real</span>")
    title_label.setStyleSheet("background: #f3e8ff; border-radius: 6px; padding: 1px 10px 1px 6px; border: 1px solid #d946ef; margin-bottom: 0px;")
    title_row.addWidget(title_label, 0, Qt.AlignmentFlag.AlignLeft)
    # Botón de refresco manual
    refresh_btn = QPushButton("⟳")
    refresh_btn.setToolTip("Actualizar estadísticas ahora (también se actualizan automáticamente)")
    refresh_btn.setFixedSize(28, 28)
    refresh_btn.setStyleSheet("""
        QPushButton {
            background: #f3e8ff;
            border: 1.5px solid #d946ef;
            border-radius: 14px;
            font-size: 15px;
            color: #a21caf;
            font-weight: bold;
            margin-left: 8px;
        }
        QPushButton:hover {
            background: #e9d5ff;
            color: #7c2dbe;
        }
    """)
    title_row.addWidget(refresh_btn, 0, Qt.AlignmentFlag.AlignLeft)
    # Botón de configuración de métricas
    config_btn = QPushButton("⚙️")
    config_btn.setToolTip("Configurar métricas visibles")
    config_btn.setFixedSize(28, 28)
    config_btn.setStyleSheet("""
        QPushButton {
            background: #f3e8ff;
            border: 1.5px solid #d946ef;
            border-radius: 14px;
            font-size: 15px;
            color: #a21caf;
            font-weight: bold;
            margin-left: 6px;
        }
        QPushButton:hover {
            background: #e9d5ff;
            color: #7c2dbe;
        }
    """)
    title_row.addWidget(config_btn, 0, Qt.AlignmentFlag.AlignLeft)
    title_row.addStretch(1)
    layout.addLayout(title_row)

    # --- Configuración de métricas visibles ---
    # Por defecto, todas visibles
    if not hasattr(instance, '_kpi_visible_metrics'):
        instance._kpi_visible_metrics = {
            'zonas': True,
            'total': True,
            'libres': True,
            'ocupadas': True,
            'reservadas': True,
            'porc_ocup': True
        }

    def show_config_dialog():
        dialog = QDialog(section)
        dialog.setWindowTitle("Configurar métricas visibles")
        vbox = QVBoxLayout(dialog)
        checks = {}
        metric_labels = {
            'zonas': 'Zonas',
            'total': 'Total',
            'libres': 'Libres',
            'ocupadas': 'Ocupadas',
            'reservadas': 'Reservadas',
            'porc_ocup': '% Ocupación'
        }
        for key, label in metric_labels.items():
            cb = QCheckBox(label)
            cb.setChecked(instance._kpi_visible_metrics.get(key, True))
            checks[key] = cb
            vbox.addWidget(cb)
        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        vbox.addWidget(btn_box)
        def accept():
            for key in checks:
                instance._kpi_visible_metrics[key] = checks[key].isChecked()
            dialog.accept()
            update_kpi_visibility()
        btn_box.accepted.connect(accept)
        btn_box.rejected.connect(dialog.reject)
        dialog.exec()

    config_btn.clicked.connect(show_config_dialog)

    # ---
    def update_kpi_visibility():
        # Oculta o muestra widgets según selección
        metric_map = {
            'zonas': instance.zonas_widget,
            'total': instance.mesas_total_widget,
            'libres': instance.mesas_libres_widget,
            'ocupadas': instance.mesas_ocupadas_widget,
            'reservadas': instance.mesas_reservadas_widget,
            'porc_ocup': instance.porc_ocup_widget
        }
        for key, widget in metric_map.items():
            widget.setVisible(instance._kpi_visible_metrics.get(key, True))

    # --- Timer de refresco automático ---
    from PyQt6.QtCore import QTimer
    def do_refresh():
        if hasattr(instance, 'refresh_stats_callback') and callable(instance.refresh_stats_callback):
            instance.refresh_stats_callback()
        else:
            # fallback: forzar update_ultra_premium_stats
            from .mesas_area_stats import update_ultra_premium_stats
            update_ultra_premium_stats(instance)
    refresh_btn.clicked.connect(do_refresh)
    # Timer auto
    if not hasattr(instance, '_kpi_auto_refresh_timer'):
        instance._kpi_auto_refresh_timer = QTimer()
        instance._kpi_auto_refresh_timer.setInterval(10000)  # 10s
        instance._kpi_auto_refresh_timer.timeout.connect(do_refresh)
        instance._kpi_auto_refresh_timer.start()
    # Grid de widgets premium
    grid = QGridLayout()
    grid.setSpacing(12)
    grid.setContentsMargins(0, 0, 0, 0)
    # Widgets premium (QFrame+QLabel) igual que en el original
    from .kpi_widget import KPIWidget
    instance.zonas_widget = KPIWidget("📍", "Zonas", "0", "#8b5cf6", "#f3e8ff", tooltip="Total de zonas activas", badge={"text": "Z", "color": "#8b5cf6"})
    instance.mesas_total_widget = KPIWidget("🍽️", "Total", "0", "#3b82f6", "#dbeafe", tooltip="Total de mesas registradas", badge={"text": "T", "color": "#3b82f6"})
    instance.mesas_libres_widget = KPIWidget("🟢", "Libres", "0", "#22c55e", "#dcfce7", tooltip="Mesas libres disponibles", badge={"text": "L", "color": "#22c55e"})
    instance.mesas_ocupadas_widget = KPIWidget("🔴", "Ocupadas", "0", "#ef4444", "#fee2e2", tooltip="Mesas actualmente ocupadas", badge={"text": "O", "color": "#ef4444"})
    instance.mesas_reservadas_widget = KPIWidget("📅", "Reservadas", "0", "#f59e0b", "#fef3c7", tooltip="Mesas reservadas", badge={"text": "R", "color": "#f59e0b"})
    instance.porc_ocup_widget = KPIWidget("📈", "% Ocupación", "0%", "#0ea5e9", "#e0f2fe", tooltip="Porcentaje de ocupación actual", badge={"text": "%", "color": "#0ea5e9"})
    grid.addWidget(instance.zonas_widget, 0, 0)
    grid.addWidget(instance.mesas_total_widget, 0, 1)
    grid.addWidget(instance.mesas_libres_widget, 0, 2)
    grid.addWidget(instance.mesas_ocupadas_widget, 0, 3)
    grid.addWidget(instance.mesas_reservadas_widget, 0, 4)
    grid.addWidget(instance.porc_ocup_widget, 0, 5)
    layout.addLayout(grid)
    # Aplicar visibilidad inicial
    update_kpi_visibility()
    # Línea de estado de actualización (último refresh)
    from PyQt6.QtWidgets import QHBoxLayout
    refresh_row = QHBoxLayout()
    refresh_row.addStretch(1)
    from PyQt6.QtWidgets import QLabel
    from PyQt6.QtCore import Qt
    instance.kpi_last_refresh_label = QLabel()
    instance.kpi_last_refresh_label.setObjectName("KPI_LastRefreshLabel")
    instance.kpi_last_refresh_label.setText("Actualizado: --/--/---- --:--:--")
    instance.kpi_last_refresh_label.setStyleSheet("font-size: 10px; color: #64748b; background: #f3f4f6; border-radius: 6px; padding: 2px 8px; margin-top: 2px;")
    instance.kpi_last_refresh_label.setAlignment(Qt.AlignmentFlag.AlignRight)
    refresh_row.addWidget(instance.kpi_last_refresh_label, 0, Qt.AlignmentFlag.AlignRight)
    layout.addLayout(refresh_row)
    return section

def create_ultra_premium_stat(icon, label, value, color, bg_color, size=80, height=80):
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QMessageBox
    from PyQt6.QtCore import Qt
    class ClickableStatWidget(QFrame):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._detail_label = label
            self._hover_anim = None
            self._hovered = False
            self.setMouseTracking(True)
        def mousePressEvent(self, event):
            # Drill-down: mostrar detalle en un QMessageBox (puede ser reemplazado por panel futuro)
            QMessageBox.information(self, f"Detalle de {self._detail_label}", f"Detalle de la métrica: {self._detail_label}\n\n(Próximamente: gráfico o desglose avanzado)")
            super().mousePressEvent(event)
        def enterEvent(self, event):
            self._hovered = True
            self.setStyleSheet(self.styleSheet() + "\nQFrame { box-shadow: 0 8px 32px 0 rgba(60,60,120,0.18), 0 2px 8px 0 rgba(60,60,120,0.12); background-color: rgba(255,255,255,0.82); filter: brightness(1.13); transition: box-shadow 0.18s, filter 0.18s; }")
            super().enterEvent(event)
        def leaveEvent(self, event):
            self._hovered = False
            # Restaurar estilo base (sin hover)
            self.setStyleSheet(self.styleSheet().replace("box-shadow: 0 8px 32px 0 rgba(60,60,120,0.18), 0 2px 8px 0 rgba(60,60,120,0.12); background-color: rgba(255,255,255,0.82); filter: brightness(1.13); transition: box-shadow 0.18s, filter 0.18s;",""))
            super().leaveEvent(event)

    stat_widget = ClickableStatWidget()
    stat_widget.setMinimumSize(size, height)
    stat_widget.setMaximumWidth(size+30)
    # --- Estilo visual avanzado: gradiente y glassmorphism ---
    stat_widget.setStyleSheet(f"""
        QFrame {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {bg_color}, stop:0.5 #f3e8ff, stop:1 #e0e7ff);
            border: 2.5px solid {color};
            border-radius: 18px;
            margin: 4px;
            padding: 8px 6px 10px 6px;
            box-shadow: 0 4px 24px 0 rgba(120, 60, 180, 0.10), 0 1.5px 8px 0 rgba(120, 60, 180, 0.08);
            /* Glassmorphism */
            backdrop-filter: blur(8px);
            background-color: rgba(255,255,255,0.55);
        }}
    """)
    # --- INICIO: Layout jerárquico y compacto avanzado ---
    # Estructura: icono arriba, fila horizontal valor/tendencia/badge, sparkline, etiqueta, tooltip, estado actualización
    layout = QVBoxLayout(stat_widget)
    layout.setContentsMargins(8, 10, 8, 8)
    layout.setSpacing(3)
    # TODO: Reemplazar value_row por un QHBoxLayout para valor/tendencia/badge en una sola fila
    # TODO: Añadir estado de actualización en esquina inferior derecha
    # TODO: Ajustar estilos y alineaciones según el diagrama de layout
    # --- FIN: Layout jerárquico y compacto avanzado ---
    # Icono grande arriba
    # --- Iconografía grande y clara ---
    icon_label = QLabel()
    icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    # Soporte para SVG/vectorial si es posible
    try:
        from PyQt6.QtSvgWidgets import QSvgWidget
        import os
        if os.path.exists(icon) and icon.lower().endswith('.svg'):
            svg_widget = QSvgWidget(icon)
            svg_widget.setFixedSize(48, 48)
            layout.addWidget(svg_widget)
            icon_label.hide()
        else:
            icon_label.setText(icon)
            icon_label.setStyleSheet(f"font-size: 38px; color: {color}; line-height: 1.0; margin-bottom: 0px; text-shadow: 0 2px 4px #fff, 0 1px 4px #0002;")
            layout.addWidget(icon_label)
    except Exception:
        icon_label.setText(icon)
        icon_label.setStyleSheet(f"font-size: 38px; color: {color}; line-height: 1.0; margin-bottom: 0px; text-shadow: 0 2px 4px #fff, 0 1px 4px #0002;")
        layout.addWidget(icon_label)

    # Fila horizontal: valor, tendencia, badge
    from PyQt6.QtWidgets import QHBoxLayout
    value_row = QHBoxLayout()
    value_row.setSpacing(4)
    value_row.setContentsMargins(0, 0, 0, 0)
    value_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

    value_widget = QLabel(str(value))
    value_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    value_widget.setMinimumWidth(32)
    value_widget.setMaximumWidth(60)
    value_widget.setStyleSheet(f"font-size: 22px; font-weight: bold; color: #1e293b; background: #fff; border-radius: 7px; padding: 1px 8px; margin: 0; letter-spacing: 0.2px; text-shadow: 0 1px 2px #0001;")
    value_row.addWidget(value_widget)

    trend_widget = QLabel("—")
    trend_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    trend_widget.setMinimumWidth(18)
    trend_widget.setMaximumWidth(26)
    trend_widget.setMinimumHeight(16)
    trend_widget.setMaximumHeight(20)
    trend_widget.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    trend_widget.setStyleSheet("font-size: 15px; color: #64748b; font-weight: bold; background: transparent; border: none; margin: 0 auto 0 auto;")
    value_row.addWidget(trend_widget)

    badge_widget = QLabel("")
    badge_widget.setAlignment(Qt.AlignmentFlag.AlignVCenter)
    badge_widget.setMinimumWidth(14)
    badge_widget.setMaximumWidth(22)
    badge_widget.setStyleSheet("font-size: 13px; color: #fff; background: #ef4444; border-radius: 8px; padding: 0 4px; margin-left: 2px; font-weight: bold;")
    badge_widget.hide()
    value_row.addWidget(badge_widget)

    layout.addLayout(value_row)

    # Mini sparkline (solo para % Ocupación)
    sparkline = None
    if label == "% Ocupación":
        from PyQt6.QtWidgets import QWidget
        from PyQt6.QtGui import QPainter, QPen, QColor
        class SparklineWidget(QWidget):
            def __init__(self, parent=None):
                super().__init__(parent)
                self.data = []
            def setData(self, data):
                self.data = data[-30:]  # Máximo 30 puntos
                self.update()
            def paintEvent(self, event):
                if not self.data or len(self.data) < 2:
                    return
                painter = QPainter(self)
                pen = QPen(QColor("#0ea5e9"), 2)
                painter.setPen(pen)
                w = self.width()
                h = self.height()
                min_val = min(self.data)
                max_val = max(self.data)
                span = max_val - min_val if max_val != min_val else 1
                points = [
                    (
                        int(i * (w / (len(self.data)-1))),
                        h - int((val - min_val) / span * (h-4)) - 2
                    )
                    for i, val in enumerate(self.data)
                ]
                for i in range(len(points)-1):
                    painter.drawLine(points[i][0], points[i][1], points[i+1][0], points[i+1][1])
        sparkline = SparklineWidget()
        sparkline.setFixedHeight(22)
        sparkline.setMinimumWidth(60)
        layout.addWidget(sparkline, alignment=Qt.AlignmentFlag.AlignCenter)
        stat_widget.setProperty('sparkline_widget', sparkline)

    # Etiqueta secundaria
    label_widget = QLabel(label)
    label_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label_widget.setStyleSheet("font-size: 12px; color: #334155; font-weight: 600; margin: 1px 0 0 0; letter-spacing: 0.1px;")
    layout.addWidget(label_widget)
    # Tooltips enriquecidos según la métrica
    tooltip_map = {
        "Zonas": "Cantidad de zonas activas en el establecimiento.",
        "Total": "Número total de mesas registradas.",
        "Libres": "Mesas actualmente disponibles para uso.",
        "Ocupadas": "Mesas actualmente ocupadas por clientes.",
        "Reservadas": "Mesas reservadas para clientes futuros.",
        "% Ocupación": "Porcentaje de mesas ocupadas respecto al total. Ideal para monitorear la demanda en tiempo real."
    }
    stat_widget.setToolTip(tooltip_map.get(label, label))
    # Guardar referencias para lógica de actualización
    # Guardar referencias usando setProperty para compatibilidad con PyQt
    stat_widget.setProperty('value_label', value_widget)
    stat_widget.setProperty('trend_label', trend_widget)
    stat_widget.setProperty('badge_label', badge_widget)
    stat_widget.setProperty('_last_value', None)
    if sparkline:
        stat_widget.setProperty('sparkline_widget', sparkline)
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
    import datetime
    if not hasattr(instance, 'mesas') or not instance.mesas:
        # Si no hay datos, igual actualiza la fecha/hora
        if hasattr(instance, 'kpi_last_refresh_label'):
            now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            instance.kpi_last_refresh_label.setText(f"Actualizado: {now}")
        return
    total_mesas = len(instance.mesas)
    mesas_ocupadas = len([m for m in instance.mesas if hasattr(m, 'estado') and m.estado == 'ocupada'])
    mesas_libres = total_mesas - mesas_ocupadas
    mesas_reservadas = len([m for m in instance.mesas if hasattr(m, 'estado') and m.estado == 'reservada'])
    zonas_unicas = len(set(getattr(m, 'zona', 'Sin zona') for m in instance.mesas))
    porc_ocup = 0
    if not hasattr(instance, '_porc_ocup_history'):
        instance._porc_ocup_history = []
    if total_mesas > 0:
        porc_ocup = int(round((mesas_ocupadas / total_mesas) * 100))
    # Actualizar historial para sparkline
    instance._porc_ocup_history.append(porc_ocup)
    if len(instance._porc_ocup_history) > 30:
        instance._porc_ocup_history = instance._porc_ocup_history[-30:]

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
    if hasattr(instance, 'porc_ocup_widget'):
        _update_stat_widget(instance.porc_ocup_widget, f"{porc_ocup}%")
        # Actualizar sparkline si existe
        sparkline = instance.porc_ocup_widget.property('sparkline_widget') if instance.porc_ocup_widget else None
        if sparkline:
            sparkline.setData(instance._porc_ocup_history)
    # Actualizar fecha/hora de último refresh
    if hasattr(instance, 'kpi_last_refresh_label'):
        now = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        instance.kpi_last_refresh_label.setText(f"Actualizado: {now}")

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
