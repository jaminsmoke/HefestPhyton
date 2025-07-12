"""
mesas_area_grid.py
Lógica y helpers para el grid de mesas y renderizado de widgets
"""

from typing import Any, Optional, List
from PyQt6.QtWidgets import QGridLayout, QWidget, QLayout, QScrollArea
from PyQt6.QtCore import Qt


def create_scroll_area(instance: Any, layout: QLayout) -> QScrollArea:
    from PyQt6.QtWidgets import QScrollArea, QWidget, QGridLayout
    from PyQt6.QtCore import Qt

    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    from src.utils.styles import ModernStyles

    scroll_area.setStyleSheet(ModernStyles.get_scroll_area_style())
    mesas_container = QWidget()
    mesas_container.setStyleSheet(ModernStyles.get_mesas_container_style())
    instance.mesas_layout = QGridLayout(mesas_container)
    instance.mesas_layout.setSpacing(20)
    instance.mesas_layout.setContentsMargins(20, 20, 20, 20)
    # Centrar el grid de mesas horizontalmente y mantener alineado arriba
    instance.mesas_layout.setAlignment(
        Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter
    )
    scroll_area.setWidget(mesas_container)
    layout.addWidget(scroll_area)
    instance.scroll_area = scroll_area
    return scroll_area


def populate_grid(instance: Any) -> None:
    from ...widgets.mesa_widget_simple import MesaWidget
    from .mesas_area_utils import restaurar_datos_temporales, calcular_columnas_optimas  # type: ignore[misc]
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
        last_row = min(
            instance._total_rows, (scroll.value() + viewport_height) // row_height + 2
        )
        return set(range(first_row, last_row))

    def lazy_load_rows():
        visible_rows = get_visible_rows()
        tpv_service = getattr(instance, "tpv_service", None)
        for row in visible_rows:
            if row in instance._lazy_loaded_rows:
                continue
            for col in range(cols):
                idx = row * cols + col
                if idx >= len(instance.filtered_mesas):
                    break
                mesa = instance.filtered_mesas[idx]
                mesa_widget = MesaWidget(
                    mesa,
                    proxima_reserva=getattr(mesa, "proxima_reserva", None),
                    tpv_service=tpv_service,
                )
                mesa_widget.personas_changed.connect(instance._on_personas_mesa_changed)  # type: ignore
                mesa_widget.restaurar_original.connect(  # type: ignore
                    instance.restaurar_estado_original_mesa
                )
                mesa_widget.reservar_mesa_requested.connect(instance._on_reservar_mesa)  # type: ignore
                mesa_widget.iniciar_tpv_requested.connect(instance._on_iniciar_tpv)  # type: ignore
                instance.mesa_widgets.append(mesa_widget)
                instance.mesas_layout.addWidget(mesa_widget, row, col)
                # logger.debug(f"[CICLO][GRID] addWidget: mesa={getattr(mesa, 'numero', None)} estado={getattr(mesa, 'estado', None)} en row={row} col={col}")
            instance._lazy_loaded_rows.add(row)
        # logger.debug(f"[CICLO][GRID] lazy_load_rows ejecutado. Filas visibles: {visible_rows}")

    # Conectar el evento de scroll para lazy loading
    from PyQt6.QtCore import QTimer

    def on_scroll():
        QTimer.singleShot(10, lazy_load_rows)  # type: ignore

    scroll = instance.scroll_area.verticalScrollBar()
    if scroll:
        scroll.valueChanged.connect(on_scroll)  # type: ignore
    lazy_load_rows()


# Métodos para conectar en la instancia (por ejemplo, en la clase del área de mesas)
def add_mesa_grid_callbacks_to_instance(instance: Any) -> None:
    def _on_reservar_mesa(mesa: Any) -> None:
        try:
            from src.ui.modules.tpv_module.dialogs.reserva_dialog import ReservaDialog
            from src.ui.modules.tpv_module.event_bus import reserva_event_bus

            import logging

            logging.getLogger(__name__).debug(
                f"[mesas_area_grid] _on_reservar_mesa: Abriendo ReservaDialog para mesa_id={getattr(mesa, 'id', None)}"
            )
            # Mantener referencia al dialog para evitar recolección de basura
            if not hasattr(instance, "_active_dialogs"):
                instance._active_dialogs = []  # type: ignore[attr-defined]
            logging.getLogger(__name__).debug(
                f"[mesas_area_grid][DEBUG] Creando ReservaDialog"
            )
            dialog = ReservaDialog(
                instance,
                mesa,
                reserva_service=getattr(instance, "reserva_service", None),
            )
            logging.getLogger(__name__).debug(
                f"[mesas_area_grid][DEBUG] ReservaDialog creado"
            )
            instance._active_dialogs.append(dialog)  # type: ignore[attr-defined]

            def on_reserva_creada(reserva: Any) -> None:
                logging.getLogger(__name__).debug(
                    f"[mesas_area_grid][DEBUG] Callback on_reserva_creada ejecutado. reserva={reserva}"
                )
                reserva_service = getattr(instance, "reserva_service", None)
                if reserva_service is None:
                    logging.getLogger(__name__).error(
                        "[mesas_area_grid][ERROR] No se encontró reserva_service en la instancia. No se puede guardar la reserva."
                    )
                    return
                from datetime import datetime

                # Compatibilidad: aceptar tanto reserva.fecha como reserva.fecha_reserva
                fecha = getattr(reserva, "fecha", None) or getattr(
                    reserva, "fecha_reserva", None
                )
                hora = getattr(reserva, "hora", None) or getattr(
                    reserva, "hora_reserva", None
                )
                if fecha is None or hora is None:
                    logging.getLogger(__name__).error(
                        "[mesas_area_grid][ERROR] No se pudo obtener fecha u hora de la reserva. No se creará la reserva."
                    )
                    return
                if isinstance(hora, str):
                    try:
                        hora_obj = datetime.strptime(hora, "%H:%M").time()
                    except Exception:
                        logging.getLogger(__name__).error(
                            f"[mesas_area_grid][ERROR] Formato de hora inválido: {hora}"
                        )
                        return
                else:
                    hora_obj = hora
                try:
                    fecha_hora = datetime.combine(fecha, hora_obj)
                except Exception as e:
                    logging.getLogger(__name__).error(
                        f"[mesas_area_grid][ERROR] Error combinando fecha y hora: {e}"
                    )
                    return
                # Refuerzo: Usar SIEMPRE mesa.numero como identificador único de negocio
                # TODO: Eliminar referencias a mesa.id cuando se elimine compatibilidad legacy
                logging.getLogger(__name__).debug(
                    f"[mesas_area_grid] Llamando a crear_reserva forzando mesa_numero={getattr(mesa, 'numero', None)} (ignorando reserva.mesa_id={getattr(reserva, 'mesa_id', None)})"
                )
                reserva_db = reserva_service.crear_reserva(
                    mesa_id=str(getattr(mesa, "numero", "")),
                    cliente=getattr(reserva, "cliente", None)
                    or getattr(reserva, "cliente_nombre", None),
                    fecha_hora=fecha_hora,
                    duracion_min=getattr(reserva, "duracion_min", 120),
                    telefono=getattr(reserva, "telefono", None)
                    or getattr(reserva, "cliente_telefono", None),
                    personas=getattr(reserva, "personas", None)
                    or getattr(reserva, "numero_personas", None),
                    notas=getattr(reserva, "notas", None),
                )
                logging.getLogger(__name__).info(
                    f"[mesas_area_grid] Reserva creada en BD: {reserva_db}"
                )
                # Emitir eventos globales para refrescar UI
                if hasattr(mesa, "estado"):
                    mesa.estado = "reservada"
                # Refrescar visualmente el widget de la mesa
                mesa_id = str(getattr(mesa, "id", None))
                for widget in getattr(instance, "mesa_widgets", []):
                    if str(getattr(widget.mesa, "id", None)) == mesa_id:
                        if hasattr(widget, "update_mesa"):
                            widget.update_mesa(mesa)
                        if hasattr(widget, "estado_label"):
                            widget.estado_label.setText(widget.get_estado_texto())
                        if hasattr(widget, "apply_styles"):
                            widget.apply_styles()
                        widget.repaint()
                logging.getLogger(__name__).debug(
                    f"[mesas_area_grid] Emitiendo reserva_creada y actualizando UI para mesa_id={getattr(mesa, 'id', None)}"
                )
                reserva_event_bus.reserva_creada.emit(reserva_db)
                if hasattr(instance, "sincronizar_reservas_en_mesas"):
                    instance.sincronizar_reservas_en_mesas()
                if hasattr(instance, "load_reservas"):
                    instance.load_reservas()
                # Limpiar referencia al dialog
                if hasattr(instance, "_active_dialogs"):
                    try:
                        instance._active_dialogs.remove(dialog)
                    except (ValueError, AttributeError) as e:
                        # Log específico para error de limpieza de dialogs
                        logging.getLogger(__name__).debug(
                            "Error removiendo dialog de active_dialogs: %s", e
                        )

            logging.getLogger(__name__).debug(
                f"[mesas_area_grid][DEBUG] Conectando señal reserva_creada de dialog a on_reserva_creada"
            )
            dialog.reserva_creada.connect(on_reserva_creada)  # type: ignore
            logging.getLogger(__name__).debug(
                f"[mesas_area_grid][DEBUG] Ejecutando dialog.exec() para dialog"
            )
            dialog.exec()
            logging.getLogger(__name__).debug(
                f"[mesas_area_grid][DEBUG] dialog.exec() finalizado para dialog"
            )
            # Si el usuario cierra el diálogo sin crear reserva, limpiar referencia
            if hasattr(instance, "_active_dialogs"):
                try:
                    instance._active_dialogs.remove(dialog)  # type: ignore[attr-defined]
                except (ValueError, AttributeError) as e:
                    # Log específico para error de limpieza final de dialogs
                    logging.getLogger(__name__).debug(
                        "Error final removiendo dialog: %s", e
                    )
        except Exception as e:
            import logging

            logging.getLogger(__name__).error(f"Error abriendo ReservaDialog: {e}")

    def _on_iniciar_tpv(mesa: Any) -> None:
        try:
            from src.ui.modules.tpv_module.components.tpv_avanzado.tpv_avanzado_main import (
                TPVAvanzado,
            )
            from PyQt6.QtWidgets import QDialog, QVBoxLayout

            db_manager = getattr(instance, "db_manager", None)
            if db_manager is None:
                raise ValueError(
                    "db_manager es obligatorio y debe ser inyectado explícitamente en el área de mesas"
                )

            class TPVDialog(QDialog):
                def __init__(self, mesa: Any, parent: Optional[QWidget] = None) -> None:
                    super().__init__(parent)
                    self.setWindowTitle(f"TPV Avanzado - Mesa {mesa.numero}")  # type: ignore[attr-defined]
                    self.setMinimumSize(900, 600)
                    layout = QVBoxLayout(self)
                    tpv_service = getattr(instance, "tpv_service", None)
                    comanda = None
                    if tpv_service and hasattr(tpv_service, "get_comanda_activa"):
                        comanda = tpv_service.get_comanda_activa(mesa.numero)  # type: ignore[attr-defined]
                    self.tpv_widget = TPVAvanzado(
                        mesa,
                        tpv_service=tpv_service,
                        db_manager=db_manager,
                        parent=self,
                    )
                    if comanda:
                        self.tpv_widget.set_pedido_actual(comanda)  # type: ignore[misc]
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
    if hasattr(instance, "status_info"):
        if total_filtered == total_all:
            status_text = f"Mostrando {total_all} mesa(s)"
        else:
            status_text = f"Mostrando {total_filtered} de {total_all} mesa(s)"
        instance.status_info.setText(status_text)


def clear_mesa_widgets(instance):

    try:
        import logging

        logger = logging.getLogger("mesas_area_grid")
        if not hasattr(instance, "mesas_layout") or instance.mesas_layout is None:
            return
        instance.mesa_widgets.clear()  # type: ignore[attr-defined]
        layout = instance.mesas_layout  # type: ignore[attr-defined]
        # Eliminar TODOS los widgets del layout
        while layout.count():  # type: ignore[attr-defined]
            child = layout.takeAt(0)  # type: ignore[attr-defined]
            if child and child.widget():
                widget = child.widget()
                widget.setParent(None)
                widget.deleteLater()
        # Extra: limpiar widgets huérfanos del contenedor (mesas_container)
        parent_widget = layout.parentWidget() if hasattr(layout, "parentWidget") else None  # type: ignore[attr-defined]
        if parent_widget:
            for w in parent_widget.findChildren(QWidget):  # type: ignore[attr-defined]
                if w.parent() == parent_widget and w not in instance.mesa_widgets:  # type: ignore[attr-defined]
                    w.setParent(None)
                    w.deleteLater()
            parent_widget.update()  # type: ignore[attr-defined]
            parent_widget.repaint()  # type: ignore[attr-defined]
        # Forzar update/repaint del layout
        layout.update()  # type: ignore[attr-defined]
    except Exception as e:
        import logging

        logging.getLogger(__name__).error(f"Error limpiando widgets de mesa: {e}")


def show_no_mesas_message(instance: Any) -> None:
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel

    try:
        if not hasattr(instance, "mesas_layout") or instance.mesas_layout is None:
            return
        message_container = QFrame()
        from src.utils.styles import ModernStyles

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
        instance.mesas_layout.addWidget(message_container, 0, 0, 1, 4)  # type: ignore[attr-defined]
    except Exception as e:
        import logging

        logging.getLogger(__name__).error(f"Error mostrando mensaje de no mesas: {e}")


def create_mesas_grid(parent: Any, mesas: Any) -> QWidget:
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
        if hasattr(mesa_widget, "_ajustar_fuente_nombre"):
            try:
                mesa_widget._ajustar_fuente_nombre()
            except Exception as e:
                import logging

                logging.getLogger(__name__).error(
                    f"Error refrescando estilo de mesa widget: {e}"
                )
