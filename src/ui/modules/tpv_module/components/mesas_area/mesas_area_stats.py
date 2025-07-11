"""
Archivo: mesas_area_stats.py
Descripción: Componente de estadísticas de área de mesas para el TPV.

─────────────────────────────────────────────────────────────────────────────
⚠️  EXCEPCIÓN DE TIPADO DINÁMICO PyQt6 (ver README y política de Hefest)
─────────────────────────────────────────────────────────────────────────────
Este archivo utiliza PyQt6 y contiene lógica dinámica (widgets, señales, layouts, etc.)
que genera múltiples advertencias de tipado estático (Pyright/Pylance), especialmente:
  - reportUnknownMemberType
  - reportUnknownArgumentType
  - reportUnknownVariableType
  - reportMissingParameterType
  - reportUnknownParameterType
Estas advertencias son inevitables debido a la arquitectura dinámica de PyQt6 y la naturaleza de los widgets generados en tiempo de ejecución.

Cumpliendo la política de Hefest:
  1. Se documenta aquí la excepción técnica (ver README de la carpeta)
  2. Se agregan comentarios `# type: ignore` o anotaciones `Any` donde sea necesario
  3. Se añaden TODO para refactorización futura si PyQt o las herramientas de tipado mejoran
  4. Se registra la excepción en el README correspondiente

Esta excepción está justificada y registrada. No eliminar los comentarios ni la documentación.
─────────────────────────────────────────────────────────────────────────────
Versión política: v0.0.12
"""

from typing import Any
from src.utils.modern_styles import ModernStyles

# TODO: Si PyQt6 o las herramientas de tipado mejoran, intentar tipar correctamente los miembros dinámicos.
# type: ignore[reportUnknownMemberType,reportUnknownArgumentType,reportUnknownVariableType,reportMissingParameterType,reportUnknownParameterType]
# Excepción documentada en README y en el encabezado de este archivo.


def create_subcontenedor_metric_cards(instance: Any) -> Any:
    # EXCEPCIÓN FUNCIONAL: El parámetro 'instance' y los atributos de widgets son dinámicos (PyQt6),
    # por lo que se usa Any y no se puede tipar estrictamente.
    # EXCEPCIÓN FUNCIONAL: 'widget' es un objeto PyQt6 dinámico, no tipable estrictamente.
    # EXCEPCIÓN FUNCIONAL: 'instance' y sus atributos son dinámicos (PyQt6).
    # EXCEPCIÓN FUNCIONAL: 'instance' y sus atributos son dinámicos (PyQt6).
    # EXCEPCIÓN FUNCIONAL: 'instance' y 'layout' son objetos PyQt6 dinámicos.
    from PyQt6.QtWidgets import (
        QFrame,
        QVBoxLayout,
        QHBoxLayout,
        QLabel,
        QGridLayout,
        QPushButton,
        QDialog,
        QCheckBox,
        QDialogButtonBox,
    )
    from PyQt6.QtCore import Qt

    section = QFrame()
    section.setObjectName("SubContenedorMetricCards")
    section.setStyleSheet(ModernStyles.get_stats_section_style())
    layout = QVBoxLayout(section)
    layout.setContentsMargins(4, 2, 4, 4)
    layout.setSpacing(2)
    # Título compacto
    from PyQt6.QtWidgets import (
        QPushButton,
        QDialog,
        QVBoxLayout,
        QCheckBox,
        QDialogButtonBox,
        QHBoxLayout,
    )

    title_row = QHBoxLayout()
    title_label = QLabel(
        "<span style='font-size:11px; font-weight:600; color:#a21caf; vertical-align:middle;'>📊 Estadísticas en Tiempo Real</span>"
    )
    title_label.setStyleSheet(ModernStyles.get_stats_title_label_style())
    title_row.addWidget(title_label, 0, Qt.AlignmentFlag.AlignLeft)
    # Botón de refresco manual
    refresh_btn = QPushButton("⟳")
    refresh_btn.setToolTip(
        "Actualizar estadísticas ahora (también se actualizan automáticamente)"
    )
    refresh_btn.setFixedSize(28, 28)
    refresh_btn.setStyleSheet(ModernStyles.get_stats_refresh_btn_style())
    title_row.addWidget(refresh_btn, 0, Qt.AlignmentFlag.AlignLeft)
    # Botón de configuración de métricas
    config_btn = QPushButton("⚙️")
    config_btn.setToolTip("Configurar métricas visibles")
    config_btn.setFixedSize(28, 28)
    config_btn.setStyleSheet(ModernStyles.get_stats_config_btn_style())
    title_row.addWidget(config_btn, 0, Qt.AlignmentFlag.AlignLeft)
    title_row.addStretch(1)
    layout.addLayout(title_row)

    # --- Configuración de métricas visibles ---
    # Por defecto, todas visibles
    if not hasattr(instance, "_kpi_visible_metrics"):
        instance._kpi_visible_metrics = {
            "zonas": True,
            "total": True,
            "libres": True,
            "ocupadas": True,
            "reservadas": True,
            "porc_ocup": True,
        }

    from typing import cast

    def show_config_dialog():
        dialog = QDialog(section)
        dialog.setWindowTitle("Configurar métricas visibles")
        vbox = QVBoxLayout(dialog)
        checks: dict[str, Any] = {}
        metric_labels = {
            "zonas": "Zonas",
            "total": "Total",
            "libres": "Libres",
            "ocupadas": "Ocupadas",
            "reservadas": "Reservadas",
            "porc_ocup": "% Ocupación",
        }
        for key, label in metric_labels.items():
            cb = QCheckBox(label)
            cb.setChecked(instance._kpi_visible_metrics.get(key, True))
            checks[key] = cb
            vbox.addWidget(cb)
        btn_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        vbox.addWidget(btn_box)

        def accept():
            for key in checks:
                instance._kpi_visible_metrics[key] = cast(Any, checks[key]).isChecked()  # type: ignore[reportUnknownMemberType]
            dialog.accept()
            update_kpi_visibility()

        btn_box.accepted.connect(accept)  # type: ignore[reportUnknownMemberType]
        btn_box.rejected.connect(dialog.reject)  # type: ignore[reportUnknownMemberType]
        dialog.exec()

    config_btn.clicked.connect(show_config_dialog)  # type: ignore[reportUnknownMemberType]

    # ---
    def update_kpi_visibility():
        # Oculta o muestra widgets según selección
        metric_map = {
            "zonas": cast(Any, instance).zonas_widget,  # type: ignore[reportUnknownMemberType]
            "total": cast(Any, instance).mesas_total_widget,  # type: ignore[reportUnknownMemberType]
            "libres": cast(Any, instance).mesas_libres_widget,  # type: ignore[reportUnknownMemberType]
            "ocupadas": cast(Any, instance).mesas_ocupadas_widget,  # type: ignore[reportUnknownMemberType]
            "reservadas": cast(Any, instance).mesas_reservadas_widget,  # type: ignore[reportUnknownMemberType]
            "porc_ocup": cast(Any, instance).porc_ocup_widget,  # type: ignore[reportUnknownMemberType]
        }
        for key, widget in metric_map.items():
            widget.setVisible(instance._kpi_visible_metrics.get(key, True))  # type: ignore[reportUnknownMemberType]

    # --- Timer de refresco automático ---
    from PyQt6.QtCore import QTimer

    def do_refresh():
        if hasattr(instance, "refresh_stats_callback") and callable(
            instance.refresh_stats_callback
        ):
            instance.refresh_stats_callback()
        else:
            # fallback: forzar update_ultra_premium_stats
            from .mesas_area_stats import update_ultra_premium_stats

            update_ultra_premium_stats(instance)

    refresh_btn.clicked.connect(do_refresh)  # type: ignore[reportUnknownMemberType]
    # Timer auto
    if not hasattr(instance, "_kpi_auto_refresh_timer"):
        instance._kpi_auto_refresh_timer = QTimer()
        instance._kpi_auto_refresh_timer.setInterval(10000)  # 10s
        instance._kpi_auto_refresh_timer.timeout.connect(do_refresh)  # type: ignore[reportUnknownMemberType]
        instance._kpi_auto_refresh_timer.start()
    # Grid de widgets premium
    grid = QGridLayout()
    grid.setSpacing(12)
    grid.setContentsMargins(0, 0, 0, 0)
    # Widgets premium (QFrame+QLabel) igual que en el original
    from .kpi_widget import KPIWidget

    instance.zonas_widget = KPIWidget(
        "📍",
        "Zonas",
        "0",
        "#8b5cf6",
        "#f3e8ff",
        tooltip="Total de zonas activas",
        badge={"text": "Z", "color": "#8b5cf6"},
    )
    instance.mesas_total_widget = KPIWidget(
        "🍽️",
        "Total",
        "0",
        "#3b82f6",
        "#dbeafe",
        tooltip="Total de mesas registradas",
        badge={"text": "T", "color": "#3b82f6"},
    )
    instance.mesas_libres_widget = KPIWidget(
        "🟢",
        "Libres",
        "0",
        "#22c55e",
        "#dcfce7",
        tooltip="Mesas libres disponibles",
        badge={"text": "L", "color": "#22c55e"},
    )
    instance.mesas_ocupadas_widget = KPIWidget(
        "🔴",
        "Ocupadas",
        "0",
        "#ef4444",
        "#fee2e2",
        tooltip="Mesas actualmente ocupadas",
        badge={"text": "O", "color": "#ef4444"},
    )
    instance.mesas_reservadas_widget = KPIWidget(
        "📅",
        "Reservadas",
        "0",
        "#f59e0b",
        "#fef3c7",
        tooltip="Mesas reservadas",
        badge={"text": "R", "color": "#f59e0b"},
    )
    instance.porc_ocup_widget = KPIWidget(
        "📈",
        "% Ocupación",
        "0%",
        "#0ea5e9",
        "#e0f2fe",
        tooltip="Porcentaje de ocupación actual",
        badge={"text": "%", "color": "#0ea5e9"},
    )
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

    instance.kpi_last_refresh_label = QLabel()  # type: ignore[reportUnknownMemberType]
    instance.kpi_last_refresh_label.setObjectName("KPI_LastRefreshLabel")  # type: ignore[reportUnknownMemberType]
    instance.kpi_last_refresh_label.setText("Actualizado: --/--/---- --:--:--")  # type: ignore[reportUnknownMemberType]
    instance.kpi_last_refresh_label.setStyleSheet(ModernStyles.get_stats_last_refresh_label_style())  # type: ignore[reportUnknownMemberType]
    instance.kpi_last_refresh_label.setAlignment(Qt.AlignmentFlag.AlignRight)  # type: ignore[reportUnknownMemberType]
    refresh_row.addWidget(
        instance.kpi_last_refresh_label, 0, Qt.AlignmentFlag.AlignRight
    )
    layout.addLayout(refresh_row)
    return section


from typing import Any


def _update_stat_widget(widget: Any, new_value: str) -> None:
    """Actualiza SOLO el valor (tercer QLabel) de un widget de estadística ultra-premium"""
    from PyQt6.QtWidgets import QLabel

    try:
        if not widget or not hasattr(widget, "layout") or not widget.layout():
            return
        layout: Any = widget.layout()

        # Buscar específicamente el QLabel del valor (índice 2)
        if layout.count() >= 3:
            value_item: Any = layout.itemAt(2)  # Tercer elemento = valor
            if (
                value_item
                and value_item.widget()
                and isinstance(value_item.widget(), QLabel)
            ):
                value_label: Any = value_item.widget()
                value_label.setText(str(new_value))  # type: ignore[reportUnknownMemberType]
                value_label.update()  # type: ignore[reportUnknownMemberType]
    except Exception as e:
        import logging

        logging.getLogger(__name__).warning(
            f"Error actualizando valor de stats ultra premium: {e}"
        )


def update_stats_from_mesas(instance: Any) -> None:
    # EXCEPCIÓN FUNCIONAL: 'instance' es dinámico (PyQt6)
    if not hasattr(instance, "mesas") or not instance.mesas:
        update_ultra_premium_stats(instance)
        # Actualizar compactas a cero
        update_compact_stats(instance, 0, 0, 0, 0)
        return
    zonas_unicas: Any = set(getattr(mesa, "zona", None) for mesa in instance.mesas)  # type: ignore[reportUnknownMemberType]
    zonas_activas: int = len(zonas_unicas)
    total_mesas: int = len(instance.mesas)
    ocupadas: int = len(
        [mesa for mesa in instance.mesas if getattr(mesa, "estado", None) == "ocupada"]
    )
    libres: int = total_mesas - ocupadas
    update_ultra_premium_stats(instance)
    update_compact_stats(instance, zonas_activas, total_mesas, libres, ocupadas)
    if hasattr(instance, "status_info"):
        instance.status_info.setText(f"Mostrando {len(getattr(instance, 'filtered_mesas', []))} de {total_mesas} mesas")  # type: ignore[reportUnknownMemberType]


def update_ultra_premium_stats(instance: Any) -> None:
    # EXCEPCIÓN FUNCIONAL: 'instance' es dinámico (PyQt6)
    import datetime
    from typing import Any, cast

    if not hasattr(instance, "mesas") or not instance.mesas:
        # Si no hay datos, igual actualiza la fecha/hora
        if hasattr(instance, "kpi_last_refresh_label"):
            now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            try:
                cast(Any, instance.kpi_last_refresh_label).setText(f"Actualizado: {now}")  # type: ignore[reportUnknownMemberType]
            except RuntimeError:
                pass  # El label ya fue destruido
        return
    total_mesas: int = len(instance.mesas)
    mesas_ocupadas: int = len(
        [
            m
            for m in instance.mesas
            if hasattr(m, "estado") and getattr(m, "estado", None) == "ocupada"
        ]
    )
    mesas_libres: int = total_mesas - mesas_ocupadas
    mesas_reservadas: int = len(
        [
            m
            for m in instance.mesas
            if hasattr(m, "estado") and getattr(m, "estado", None) == "reservada"
        ]
    )
    zonas_unicas: int = len(set(getattr(m, "zona", "Sin zona") for m in instance.mesas))
    porc_ocup: int = 0
    if not hasattr(instance, "_porc_ocup_history"):
        instance._porc_ocup_history = []  # type: ignore[reportUnknownMemberType]
    if total_mesas > 0:
        porc_ocup = int(round((mesas_ocupadas / total_mesas) * 100))
    # Actualizar historial para sparkline
    cast(Any, instance._porc_ocup_history).append(porc_ocup)  # type: ignore[reportUnknownMemberType]
    # type: ignore[reportUnknownMemberType]
    if len(cast(Any, instance._porc_ocup_history)) > 30:  # type: ignore[reportUnknownMemberType]
        instance._porc_ocup_history = cast(Any, instance._porc_ocup_history)[-30:]  # type: ignore[reportUnknownMemberType]

    # Usar _update_stat_widget para actualizar correctamente
    if hasattr(instance, "mesas_ocupadas_widget"):
        _update_stat_widget(cast(Any, instance).mesas_ocupadas_widget, str(mesas_ocupadas))  # type: ignore[reportUnknownMemberType,reportUnknownArgumentType]
    if hasattr(instance, "mesas_total_widget"):
        _update_stat_widget(cast(Any, instance).mesas_total_widget, str(total_mesas))  # type: ignore[reportUnknownMemberType,reportUnknownArgumentType]
    if hasattr(instance, "mesas_libres_widget"):
        _update_stat_widget(cast(Any, instance).mesas_libres_widget, str(mesas_libres))  # type: ignore[reportUnknownMemberType,reportUnknownArgumentType]
    if hasattr(instance, "mesas_reservadas_widget"):
        _update_stat_widget(cast(Any, instance).mesas_reservadas_widget, str(mesas_reservadas))  # type: ignore[reportUnknownMemberType,reportUnknownArgumentType]
    if hasattr(instance, "zonas_widget"):
        _update_stat_widget(cast(Any, instance).zonas_widget, str(zonas_unicas))  # type: ignore[reportUnknownMemberType,reportUnknownArgumentType]
    if hasattr(instance, "porc_ocup_widget"):
        _update_stat_widget(cast(Any, instance).porc_ocup_widget, f"{porc_ocup}%")  # type: ignore[reportUnknownMemberType,reportUnknownArgumentType]
        # Actualizar sparkline si existe
        porc_ocup_widget: Any = getattr(instance, "porc_ocup_widget", None)
        sparkline: Any = porc_ocup_widget.property("sparkline_widget") if porc_ocup_widget else None  # type: ignore[reportUnknownMemberType]
        if sparkline:
            cast(Any, sparkline).setData(cast(Any, instance._porc_ocup_history))  # type: ignore[reportUnknownMemberType]
    # Actualizar fecha/hora de último refresh
    if hasattr(instance, "kpi_last_refresh_label"):
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            cast(Any, instance.kpi_last_refresh_label).setText(f"Actualizado: {now}")  # type: ignore[reportUnknownMemberType]
        except RuntimeError:
            pass  # El label ya fue destruido


def create_compact_stats(instance: Any, layout: Any) -> None:
    """Crea las estadísticas compactas integradas en el header (idéntico al original)"""
    from PyQt6.QtWidgets import QLabel
    from .kpi_widget import KPIWidget

    # Separador visual antes de las estadísticas
    separator: Any = QLabel("|")
    separator.setStyleSheet(ModernStyles.get_stats_separator_style())
    layout.addWidget(separator)
    # Configuración de stats compactas
    stats_config = [
        ("📍", "Zonas", "0", "#10b981"),
        ("🍽️", "Total", "0", "#2563eb"),
        ("🟢", "Libres", "0", "#059669"),
        ("🔴", "Ocupadas", "0", "#dc2626"),
    ]
    instance.compact_stats_widgets: list[Any] = []  # type: ignore[reportUnknownMemberType]
    for icon, label, value, color in stats_config:
        stat_widget: Any = KPIWidget(
            icon=icon, label=label, value=value, color=color, bg_color="#fff"
        )
        instance.compact_stats_widgets.append(
            {  # type: ignore[reportUnknownMemberType]
                "widget": stat_widget,
                "type": label.lower(),
                "icon": icon,
                "label": label,
            }
        )
        layout.addWidget(stat_widget)


def update_compact_stats(
    instance: Any, zonas: Any, total: Any, libres: Any, ocupadas: Any
) -> None:
    """Actualiza las estadísticas compactas en el header"""
    from typing import Any
    from PyQt6.QtWidgets import QLabel

    if not hasattr(instance, "compact_stats_widgets"):
        return
    values = {
        "zonas": str(zonas),
        "total": str(total),
        "libres": str(libres),
        "ocupadas": str(ocupadas),
    }
    # EXCEPCIÓN FUNCIONAL: 'instance' y los widgets compactos son dinámicos (PyQt6).
    for stat_info in instance.compact_stats_widgets:
        widget: Any = stat_info["widget"]
        stat_type: Any = stat_info["type"]
        if stat_type in values:
            new_value: Any = values[stat_type]
            layout: Any = widget.layout()
            if layout and layout.count() >= 2:
                item: Any = layout.itemAt(1)
                if item:
                    value_label: Any = item.widget()
                    if isinstance(value_label, QLabel):
                        value_label.setText(new_value)  # type: ignore[reportUnknownMemberType]
                        value_label.update()  # type: ignore[reportUnknownMemberType]
            widget.update()  # type: ignore[reportUnknownMemberType]
            widget.repaint()  # type: ignore[reportUnknownMemberType]
